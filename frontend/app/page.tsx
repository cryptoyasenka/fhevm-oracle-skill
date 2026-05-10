"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { BrowserProvider, Contract, EventLog, ethers } from "ethers";
import { VAULT_ABI } from "@/lib/vault-abi";
import { getFhevm } from "@/lib/fhevm";

const VAULT_ADDRESS = process.env.NEXT_PUBLIC_VAULT_ADDRESS as string | undefined;
const SEPOLIA_CHAIN_ID = 11_155_111n;

type Status = "idle" | "busy";
type Vault = {
  id: bigint;
  depositor: string;
  revealAt: number;
  triggered: boolean;
  revealed: boolean;
  clearAmount?: bigint;
  clearSecret?: bigint;
};

export default function Page() {
  const [account, setAccount] = useState<string | null>(null);
  const [chainId, setChainId] = useState<bigint | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [log, setLog] = useState<string[]>([]);
  const [vaults, setVaults] = useState<Vault[]>([]);
  const [amount, setAmount] = useState("12345");
  const [secret, setSecret] = useState("0xc0ffee");
  const [delaySec, setDelaySec] = useState("60");
  // Local-only "hide from dashboard" — vaults are immutable on-chain, but the
  // UI can keep a per-browser list of ids the user has dismissed. Persisted to
  // localStorage so it survives reloads. Lazy init to avoid SSR window access.
  const [hidden, setHidden] = useState<Set<string>>(() => new Set());
  const [showHidden, setShowHidden] = useState(false);
  // Synchronous click guard. setStatus("busy") schedules a render — between
  // the click handler and the next render, a fast double-click can fire lock()
  // twice, both pop a MetaMask confirmation, and you end up with two vaults
  // for what felt like a single press. A ref flips synchronously so the
  // second call returns immediately.
  const inFlight = useRef(false);
  // 1-second tick so locked → "timer up" transitions, countdown text, and the
  // canTrigger gate update without the user having to refresh or interact.
  const [now, setNow] = useState(() => Math.floor(Date.now() / 1000));

  const onSepolia = chainId === SEPOLIA_CHAIN_ID;
  const vaultConfigured = !!VAULT_ADDRESS && VAULT_ADDRESS !== ethers.ZeroAddress;

  const append = useCallback((line: string) => {
    setLog((l) => [...l.slice(-50), `[${new Date().toLocaleTimeString()}] ${line}`]);
  }, []);

  const connect = useCallback(async () => {
    if (!window.ethereum) {
      append("No EIP-1193 wallet detected — install MetaMask.");
      return;
    }
    try {
      setStatus("busy");
      const provider = new BrowserProvider(window.ethereum);
      const accounts = (await provider.send("eth_requestAccounts", [])) as string[];
      const net = await provider.getNetwork();
      setAccount(accounts[0]);
      setChainId(net.chainId);
      append(`Connected ${accounts[0].slice(0, 10)}… on chain ${net.chainId}`);
    } catch (e) {
      append(`Connect failed: ${(e as Error).message}`);
    } finally {
      setStatus("idle");
    }
  }, [append]);

  const disconnect = useCallback(async () => {
    setAccount(null);
    setChainId(null);
    setVaults([]);
    append("Disconnected.");
    // EIP-2255: ask the wallet to drop its eth_accounts grant for this site so
    // a fresh "Connect" reopens the account picker. MetaMask 11+ supports it;
    // older wallets will throw — swallow it, the local clear above is enough.
    try {
      await window.ethereum?.request({
        method: "wallet_revokePermissions",
        params: [{ eth_accounts: {} }],
      });
    } catch {
      /* unsupported wallet — local disconnect is sufficient */
    }
  }, [append]);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("fhevm-vault-hidden");
      if (stored) setHidden(new Set(JSON.parse(stored) as string[]));
    } catch {
      /* localStorage unavailable / bad JSON — start fresh */
    }
  }, []);

  const persistHidden = useCallback((next: Set<string>) => {
    try {
      localStorage.setItem("fhevm-vault-hidden", JSON.stringify([...next]));
    } catch {
      /* quota / private mode — in-memory only */
    }
  }, []);

  const toggleHidden = useCallback(
    (id: bigint) => {
      setHidden((prev) => {
        const next = new Set(prev);
        const k = String(id);
        if (next.has(k)) next.delete(k);
        else next.add(k);
        persistHidden(next);
        return next;
      });
    },
    [persistHidden],
  );

  useEffect(() => {
    // Silent re-hydrate on page load: if the wallet still has us in its
    // permissioned-sites list, eth_accounts returns the address without a
    // popup. eth_requestAccounts (used by Connect) would always prompt.
    if (!window.ethereum) return;
    let cancelled = false;
    (async () => {
      try {
        const provider = new BrowserProvider(window.ethereum!);
        const accounts = (await provider.send("eth_accounts", [])) as string[];
        if (cancelled || accounts.length === 0) return;
        const net = await provider.getNetwork();
        setAccount(accounts[0]);
        setChainId(net.chainId);
      } catch {
        /* no prior connection — stay disconnected */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    // EIP-1193 events live on the provider but ethers' Eip1193Provider type
    // doesn't model them. MetaMask + every other injected wallet implements them.
    const eth = window.ethereum as unknown as
      | {
          on?: (event: string, handler: (...args: unknown[]) => void) => void;
          removeListener?: (event: string, handler: (...args: unknown[]) => void) => void;
        }
      | undefined;
    if (!eth?.on) return;
    const onAccountsChanged = (...args: unknown[]) => {
      const accounts = (args[0] as string[]) ?? [];
      if (accounts.length === 0) {
        setAccount(null);
        setVaults([]);
        append("Wallet disconnected.");
      } else {
        setAccount(accounts[0]);
        setVaults([]);
        append(`Switched to ${accounts[0].slice(0, 10)}…`);
      }
    };
    const onChainChanged = (...args: unknown[]) => {
      const id = BigInt(args[0] as string);
      setChainId(id);
      append(`Network changed to chain ${id}`);
    };
    eth.on("accountsChanged", onAccountsChanged);
    eth.on("chainChanged", onChainChanged);
    return () => {
      eth.removeListener?.("accountsChanged", onAccountsChanged);
      eth.removeListener?.("chainChanged", onChainChanged);
    };
  }, [append]);

  const switchToSepolia = useCallback(async () => {
    if (!window.ethereum) return;
    try {
      await window.ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: "0xaa36a7" }],
      });
      const provider = new BrowserProvider(window.ethereum);
      const net = await provider.getNetwork();
      setChainId(net.chainId);
    } catch (e) {
      append(`Switch failed: ${(e as Error).message}`);
    }
  }, [append]);

  const refreshVaults = useCallback(async () => {
    if (!account || !vaultConfigured || !window.ethereum) return;
    try {
      const provider = new BrowserProvider(window.ethereum);
      const vault = new Contract(VAULT_ADDRESS!, VAULT_ABI, provider);
      // Some injected wallets route eth_getLogs through their own RPC
      // (e.g. rpc.walletconnect.org) which caps the block range at 50K.
      // Cap the lookback window — the contract was deployed recently, so a
      // 49K-block window covers ~1 week of Sepolia, plenty for demo vaults.
      const head = await provider.getBlockNumber();
      const fromBlock = Math.max(0, head - 49_000);
      const lockedFilter = vault.filters.Locked(undefined, account);
      const events = (await vault.queryFilter(lockedFilter, fromBlock, "latest")).filter(
        (e): e is EventLog => "args" in e,
      );
      // Pull RevealRequested events in the same window so we know which vaults
      // have already had their handles flagged for public decryption — this is
      // what gates the Fulfill button. Without this we'd let the user call
      // publicDecrypt before the contract authorised it (the relayer rejects
      // it with "handles are not allowed for public decryption").
      const requestedFilter = vault.filters.RevealRequested();
      const reqEvents = (await vault.queryFilter(requestedFilter, fromBlock, "latest")).filter(
        (e): e is EventLog => "args" in e,
      );
      const triggeredIds = new Set(reqEvents.map((e) => String(e.args.vaultId as bigint)));
      const list: Vault[] = [];
      for (const ev of events) {
        const id = ev.args.vaultId as bigint;
        const revealAt = Number(ev.args.revealAt as bigint);
        const revealed = (await vault.isRevealed(id)) as boolean;
        const triggered = triggeredIds.has(String(id));
        const v: Vault = { id, depositor: account, revealAt, triggered, revealed };
        if (revealed) {
          const [a, s] = (await vault.getClearValues(id)) as [bigint, bigint];
          v.clearAmount = a;
          v.clearSecret = s;
        }
        list.push(v);
      }
      // Priority sort: actionable vaults float to the top so the user always
      // sees the one that needs a click first. Within each priority bucket,
      // newest id first.
      const now = Math.floor(Date.now() / 1000);
      const priority = (v: Vault) => {
        if (v.revealed) return 3;                              // done — bottom
        if (now > v.revealAt && v.triggered) return 1;         // ready to fulfill
        if (now > v.revealAt && !v.triggered) return 0;        // ready to trigger — top
        return 2;                                              // still locked
      };
      list.sort((a, b) => {
        const pa = priority(a);
        const pb = priority(b);
        if (pa !== pb) return pa - pb;
        return Number(b.id - a.id);
      });
      setVaults(list);
    } catch (e) {
      append(`Refresh failed: ${(e as Error).message}`);
    }
  }, [account, vaultConfigured, append]);

  useEffect(() => {
    if (account && onSepolia) refreshVaults();
  }, [account, onSepolia, refreshVaults]);

  useEffect(() => {
    const t = setInterval(() => setNow(Math.floor(Date.now() / 1000)), 1000);
    return () => clearInterval(t);
  }, []);

  const lock = useCallback(async () => {
    if (!vaultConfigured || !account) return;
    if (inFlight.current) return;
    inFlight.current = true;
    setStatus("busy");
    try {
      append(`Encrypting amount=${amount}, secret=${secret}…`);
      const provider = new BrowserProvider(window.ethereum!);
      const signer = await provider.getSigner();
      const fhevm = await getFhevm();

      // viem's strict isAddress (used by relayer-sdk) rejects mixed-case
      // addresses without a valid EIP-55 checksum — which some injected
      // wallets return. ethers.getAddress() normalises to checksummed form
      // and also acts as a final validity guard.
      const userAddress = ethers.getAddress(account);
      const input = fhevm.createEncryptedInput(VAULT_ADDRESS!, userAddress);
      input.add64(BigInt(amount));
      input.add256(BigInt(secret));
      const enc = await input.encrypt();
      append("Ciphertexts ready, submitting lock()…");

      const revealAt = Math.floor(Date.now() / 1000) + Number(delaySec || "60");
      const vault = new Contract(VAULT_ADDRESS!, VAULT_ABI, signer);
      const tx = await vault.lock(enc.handles[0], enc.handles[1], enc.inputProof, revealAt);
      append(`tx: ${tx.hash}`);
      await tx.wait();
      append(`Locked. Reveal at ${new Date(revealAt * 1000).toLocaleString()}`);
      await refreshVaults();
    } catch (e) {
      append(`Lock failed: ${(e as Error).message}`);
    } finally {
      setStatus("idle");
      inFlight.current = false;
    }
  }, [account, amount, secret, delaySec, vaultConfigured, append, refreshVaults]);

  const trigger = useCallback(
    async (id: bigint) => {
      if (inFlight.current) return;
      inFlight.current = true;
      setStatus("busy");
      try {
        const provider = new BrowserProvider(window.ethereum!);
        const signer = await provider.getSigner();
        const vault = new Contract(VAULT_ADDRESS!, VAULT_ABI, signer);
        append(`triggerReveal(${id})…`);
        const tx = await vault.triggerReveal(id);
        await tx.wait();
        append(`Triggered. Now press Fulfill to fetch the KMS proof and write the cleartext on-chain.`);
        await refreshVaults();
        // Optimistic flag: if the RPC node hasn't indexed RevealRequested yet
        // when refreshVaults runs, the on-chain query above might miss it.
        // We just confirmed the tx, so we know it's true. Re-set after refresh
        // (functional updater sees the most-recent committed state) so the
        // Fulfill button enables immediately.
        setVaults((vs) => vs.map((v) => (v.id === id ? { ...v, triggered: true } : v)));
      } catch (e) {
        append(`Trigger failed: ${(e as Error).message}`);
      } finally {
        setStatus("idle");
        inFlight.current = false;
      }
    },
    [append, refreshVaults],
  );

  const fulfill = useCallback(
    async (id: bigint) => {
      if (inFlight.current) return;
      inFlight.current = true;
      setStatus("busy");
      try {
        const provider = new BrowserProvider(window.ethereum!);
        const signer = await provider.getSigner();
        const vault = new Contract(VAULT_ADDRESS!, VAULT_ABI, signer);

        const handles = [
          (await vault.getEncryptedAmount(id)) as string,
          (await vault.getEncryptedSecret(id)) as string,
        ];
        append("Asking the relayer for cleartext + KMS proof…");
        const fhevm = await getFhevm();
        const result = await fhevm.publicDecrypt(handles);
        append("Submitting fulfillReveal()…");
        const tx = await vault.fulfillReveal(id, result.abiEncodedClearValues, result.decryptionProof);
        await tx.wait();
        append(`Revealed.`);
        await refreshVaults();
      } catch (e) {
        append(`Fulfill failed: ${(e as Error).message}`);
      } finally {
        setStatus("idle");
        inFlight.current = false;
      }
    },
    [append, refreshVaults],
  );

  const explorer = useMemo(
    () => (VAULT_ADDRESS ? `https://sepolia.etherscan.io/address/${VAULT_ADDRESS}` : null),
    [],
  );

  return (
    <main>
      <header className="hero">
        <div className="hero-text">
          <span className="pill live">FHEVM · Sepolia testnet</span>
          <h1>Lock a number on-chain that nobody can read — until your timer expires.</h1>
          <p className="hero-lede">
            <strong>AsyncRevealVault</strong> is a 220-line Solidity primitive that takes an
            encrypted amount + secret from your wallet, stores them on Ethereum where neither
            the contract, the validators, nor anyone else can decrypt them, and only after a
            timestamp you choose lets the Zama KMS network reveal them publicly. Think
            sealed-bid auctions, vesting cliffs, or messages that auto-publish if you stop
            paying attention.
          </p>
        </div>
        <div className="hero-actions">
          {!account ? (
            <button onClick={connect} disabled={status === "busy"}>Connect wallet</button>
          ) : !onSepolia ? (
            <>
              <button onClick={switchToSepolia} className="secondary">Switch to Sepolia</button>
              <button onClick={disconnect} className="ghost-btn" title="Disconnect wallet">
                Disconnect
              </button>
            </>
          ) : (
            <>
              <span className="pill ok">{account.slice(0, 6)}…{account.slice(-4)}</span>
              <button onClick={disconnect} className="ghost-btn" title="Disconnect wallet">
                Disconnect
              </button>
            </>
          )}
          <a className="ghost-link" href="https://github.com/cryptoyasenka/fhevm-oracle-skill" target="_blank" rel="noreferrer">
            View source on GitHub →
          </a>
        </div>
      </header>

      <section className="card">
        <h2>What you can build with this</h2>
        <div className="usecases">
          <div>
            <h3>Sealed-bid auctions</h3>
            <p>Every bid is a vault. Bids stay encrypted until the auction ends, then the
            highest reveals — no off-chain auctioneer required.</p>
          </div>
          <div>
            <h3>Vesting cliffs</h3>
            <p>Lock a salary or grant amount; it becomes claimable only after the cliff
            date. No trusted release agent.</p>
          </div>
          <div>
            <h3>Dead-man switches</h3>
            <p>A secret message that auto-publishes if you fail to reset the timer — a will,
            a whistleblower drop, an SLA penalty.</p>
          </div>
          <div>
            <h3>Commit-reveal randomness</h3>
            <p>Multi-party seed commitment with a single shared reveal slot. Verifiable
            fairness, no MEV-able ordering.</p>
          </div>
          <div>
            <h3>Encrypted DAO votes</h3>
            <p>Voters submit ciphertext ballots during the window; tallies reveal only
            after it closes. Kills momentum-based vote manipulation.</p>
          </div>
          <div>
            <h3>Embargoed disclosures</h3>
            <p>Bug reports, security advisories, or press releases stay sealed on-chain
            until the agreed embargo lifts. No leaks, no manual handoff.</p>
          </div>
        </div>
      </section>

      <section className="card">
        <h2>How it works in 4 steps</h2>
        <ol className="steps">
          <li>
            <span className="step-n">1</span>
            <div>
              <strong>Encrypt in your browser.</strong> The Zama relayer SDK loads a TFHE
              WASM engine, encrypts <code>amount</code> + <code>secret</code> with the live
              KMS public key, and produces an input proof bound to your wallet.
            </div>
          </li>
          <li>
            <span className="step-n">2</span>
            <div>
              <strong>Lock on-chain.</strong> A single <code>lock()</code> tx stores both
              ciphertexts plus the <code>revealAt</code> timestamp. From here even the
              contract itself can&apos;t read the values.
            </div>
          </li>
          <li>
            <span className="step-n">3</span>
            <div>
              <strong>Trigger after the timer.</strong> Anyone calls{" "}
              <code>triggerReveal(id)</code> once <code>now &gt; revealAt</code>. The
              contract flags both ciphertexts as publicly decryptable.
            </div>
          </li>
          <li>
            <span className="step-n">4</span>
            <div>
              <strong>Fulfill with the KMS proof.</strong> The relayer asks the KMS network
              to decrypt and sign. <code>fulfillReveal()</code> verifies the threshold
              signatures on-chain via <code>FHE.checkSignatures</code>, then writes the
              cleartext.
            </div>
          </li>
        </ol>
      </section>

      <section className="card">
        <h2>Try it{vaultConfigured ? "" : " — preview"}</h2>
        <p className="callout">
          <strong>Role-play: a sealed-bid auction.</strong> Pretend you&apos;re a bidder.
          You set a <strong>bid</strong> (a number) and a <strong>note</strong> (any
          payload up to 32 bytes — a hash, an ID, a message), encrypt them in your
          browser, and lock them on Sepolia. Until the timer expires, nobody — not
          other bidders, not the auctioneer, not even the contract — can see your bid.
          After the timer, anyone can run Trigger + Fulfill to surface the cleartext
          and settle the auction.
        </p>
        <p className="hint" style={{ marginBottom: 20 }}>
          The contract is a <em>primitive</em> — it doesn&apos;t run the auction itself,
          and no tokens move. It just provides the seal-and-reveal mechanic. Real apps
          would compose this with auction / vesting / DAO-vote / dead-man-switch logic
          (see the use-cases above).
        </p>
        {!vaultConfigured ? (
          <p className="lede">
            The live contract on Sepolia is going up just before the Builder Track
            submission — this preview deployment doesn&apos;t have its address wired up
            yet. The flow you&apos;ll be able to run from this page:{" "}
            <strong>connect wallet → encrypt amount + secret locally → lock on-chain
            → wait for the timer → trigger → KMS reveals.</strong> Everything
            client-side; no off-chain trusted party. The contract source is in this
            project&apos;s GitHub repo (linked at the bottom of the page).
          </p>
        ) : !account ? (
          <p className="lede">Connect a wallet to start. Need test ETH? <a href="https://sepoliafaucet.com" target="_blank" rel="noreferrer">sepoliafaucet.com</a>.</p>
        ) : !onSepolia ? (
          <p className="lede">Wrong network — switch to Sepolia (chain id 11155111).</p>
        ) : (
          <div className="row">
            <div>
              <label>
                Amount (your bid)
                <span
                  className="info-icon"
                  title="The bid you'd place in this pretend auction. Any whole number up to 18 quintillion. It's encrypted right here in your browser before it ever leaves — even Ethereum validators only see scrambled bytes. The 12345 default is just a placeholder; change it to any number you want to seal."
                >?</span>
              </label>
              <input value={amount} onChange={(e) => setAmount(e.target.value)} />
              <p className="hint">e.g. <code>12345</code> as a bid of $12,345. Encrypted as <code>euint64</code>.</p>
            </div>
            <div>
              <label>
                Secret (note attached to bid)
                <span
                  className="info-icon"
                  title="A second piece of data sealed together with the bid — think of it as a tag on the envelope. Could be a bidder ID, a hash that links this bid to your identity, or a short private memo. Up to 32 bytes. Hex (0x…) or a decimal number both work. The 0xc0ffee default is just a memorable example."
                >?</span>
              </label>
              <input value={secret} onChange={(e) => setSecret(e.target.value)} />
              <p className="hint">e.g. <code>0xc0ffee</code> as a bidder hash. Encrypted as <code>euint256</code>.</p>
            </div>
            <div>
              <label>
                Reveal in (sec)
                <span
                  className="info-icon"
                  title="Seconds until the auction 'closes'. The bid stays sealed for this long — no one can read it. Once the timer is up, anyone can run Trigger and then Fulfill to open it. 60 is the shortest value that lets you walk through the full lock → reveal round-trip in about a minute."
                >?</span>
              </label>
              <input value={delaySec} onChange={(e) => setDelaySec(e.target.value)} />
              <p className="hint">Use 60 to see the full round-trip in a minute.</p>
            </div>
            <button onClick={lock} disabled={status === "busy"}>
              Encrypt and lock
            </button>
          </div>
        )}
      </section>

      {vaultConfigured && account && onSepolia && (
        <section className="card">
          <h2>
            Your vaults{" "}
            <span className="pill">
              {vaults.filter((v) => showHidden || !hidden.has(String(v.id))).length}
            </span>
            <button
              onClick={refreshVaults}
              className="ghost-btn"
              style={{ marginLeft: 12 }}
              disabled={status === "busy"}
              title="Re-read the chain to pick up any vault state that changed since you last loaded the page."
            >
              ↻ Refresh
            </button>
            {vaults.some((v) => hidden.has(String(v.id))) && (
              <button
                onClick={() => setShowHidden((s) => !s)}
                className="ghost-btn"
                style={{ marginLeft: 8 }}
                title="Toggle the vaults you've dismissed"
              >
                {showHidden
                  ? "hide dismissed"
                  : `show ${vaults.filter((v) => hidden.has(String(v.id))).length} hidden`}
              </button>
            )}
          </h2>
          {vaults.length === 0 && (
            <p className="lede">No vaults yet for this account on Sepolia.</p>
          )}
          {vaults
            .filter((v) => showHidden || !hidden.has(String(v.id)))
            .map((v) => {
            const ready = now > v.revealAt;
            const canTrigger = ready && !v.triggered && !v.revealed;
            const canFulfill = ready && v.triggered && !v.revealed;
            const isHidden = hidden.has(String(v.id));
            const remaining = v.revealAt - now;
            const countdown =
              remaining > 0
                ? remaining >= 60
                  ? `${Math.floor(remaining / 60)}m ${remaining % 60}s`
                  : `${remaining}s`
                : null;
            return (
              <div
                key={String(v.id)}
                className="card vault-row"
                style={isHidden ? { opacity: 0.5 } : undefined}
              >
                <div className="row" style={{ alignItems: "start" }}>
                  <dl className="kv" style={{ flex: 2 }}>
                    <dt>id</dt><dd>{String(v.id)}</dd>
                    <dt>revealAt</dt><dd>{new Date(v.revealAt * 1000).toLocaleString()}</dd>
                    <dt>state</dt>
                    <dd>
                      {v.revealed ? (
                        <span className="pill ok">revealed</span>
                      ) : v.triggered ? (
                        <span className="pill live">triggered — fulfill next</span>
                      ) : ready ? (
                        <span className="pill live">timer up — trigger next</span>
                      ) : (
                        <span className="pill">locked</span>
                      )}
                    </dd>
                    {v.revealed && (
                      <>
                        <dt>amount</dt><dd>{String(v.clearAmount)}</dd>
                        <dt>secret</dt><dd>{"0x" + (v.clearSecret ?? 0n).toString(16)}</dd>
                      </>
                    )}
                  </dl>
                  <div className="vault-actions">
                    {!v.revealed && (
                      <>
                        <span className="action-pair">
                          <button
                            disabled={!canTrigger || status === "busy"}
                            onClick={() => trigger(v.id)}
                          >
                            Trigger
                          </button>
                          <span
                            className="info-icon"
                            title="First half of the reveal. After the timer is up, Trigger marks the sealed bid as 'safe to open' so Zama's decryption network is allowed to publish the cleartext. One MetaMask transaction. In a real auction this step is permissionless — the bidder, the auctioneer, or any observer can close the bidding once the deadline passes; here too, anyone can press it."
                          >?</span>
                        </span>
                        <span className="action-pair">
                          <button
                            disabled={!canFulfill || status === "busy"}
                            onClick={() => fulfill(v.id)}
                          >
                            Fulfill
                          </button>
                          <span
                            className="info-icon"
                            title="Second half of the reveal. After Trigger has marked the bid as openable, Fulfill fetches the actual cleartext from Zama's decryption network and writes it on-chain. The contract checks the network's signature before accepting the answer, so nobody can forge a fake one. One MetaMask transaction. Has to come after Trigger."
                          >?</span>
                        </span>
                      </>
                    )}
                    <button
                      onClick={() => toggleHidden(v.id)}
                      className="ghost-btn"
                      title={
                        hidden.has(String(v.id))
                          ? "Restore this vault to the visible list"
                          : "Hide this vault from the dashboard. The vault stays on-chain — this only affects your local view."
                      }
                      style={{ marginLeft: "auto" }}
                    >
                      {hidden.has(String(v.id)) ? "↺ Restore" : "✕ Hide"}
                    </button>
                  </div>
                </div>
                {!v.revealed && (
                  <p className="hint" style={{ marginTop: 12 }}>
                    {!ready ? (
                      <>
                        <strong>Sealed — {countdown} left.</strong> Your bid sits on-chain in
                        encrypted form. Nobody can read it — not even the contract — until{" "}
                        <code>{new Date(v.revealAt * 1000).toLocaleTimeString()}</code>. The
                        Trigger button will light up on its own when the timer runs out.
                      </>
                    ) : !v.triggered ? (
                      <>
                        <strong>Timer&apos;s up — press Trigger.</strong> This calls{" "}
                        <code>triggerReveal()</code> which tells Zama&apos;s decryption network
                        it&apos;s now allowed to publish your bid. One MetaMask transaction.
                      </>
                    ) : (
                      <>
                        <strong>Bid is openable — press Fulfill.</strong> Zama&apos;s network
                        decrypts your bid and signs the result. <code>fulfillReveal()</code>
                        {" "}checks that signature on-chain, then writes the cleartext below.
                        One MetaMask transaction.
                      </>
                    )}
                  </p>
                )}
              </div>
            );
          })}
        </section>
      )}

      <section className="card">
        <h2>Activity log</h2>
        <pre className="log">{log.length === 0 ? "Nothing yet. Connect a wallet and lock a value to see the round-trip." : log.join("\n")}</pre>
      </section>

      <footer>
        <a href="https://github.com/cryptoyasenka/fhevm-oracle-skill" target="_blank" rel="noreferrer">
          GitHub
        </a>
        {" · "}
        <a href="https://github.com/cryptoyasenka/fhevm-oracle-skill/blob/main/SKILL.md" target="_blank" rel="noreferrer">
          fhevm-oracle skill
        </a>
        {" · "}
        <a href="https://docs.zama.ai/protocol" target="_blank" rel="noreferrer">
          Zama Protocol docs
        </a>
        {explorer && (
          <>
            {" · "}
            <a href={explorer} target="_blank" rel="noreferrer">
              Vault on Etherscan
            </a>
          </>
        )}
      </footer>
    </main>
  );
}
