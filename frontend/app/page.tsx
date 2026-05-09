"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
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
      const lockedFilter = vault.filters.Locked(undefined, account);
      const events = (await vault.queryFilter(lockedFilter)).filter(
        (e): e is EventLog => "args" in e,
      );
      const list: Vault[] = [];
      for (const ev of events) {
        const id = ev.args.vaultId as bigint;
        const revealAt = Number(ev.args.revealAt as bigint);
        const revealed = (await vault.isRevealed(id)) as boolean;
        const v: Vault = { id, depositor: account, revealAt, revealed };
        if (revealed) {
          const [a, s] = (await vault.getClearValues(id)) as [bigint, bigint];
          v.clearAmount = a;
          v.clearSecret = s;
        }
        list.push(v);
      }
      list.sort((a, b) => Number(b.id - a.id));
      setVaults(list);
    } catch (e) {
      append(`Refresh failed: ${(e as Error).message}`);
    }
  }, [account, vaultConfigured, append]);

  useEffect(() => {
    if (account && onSepolia) refreshVaults();
  }, [account, onSepolia, refreshVaults]);

  const lock = useCallback(async () => {
    if (!vaultConfigured || !account) return;
    setStatus("busy");
    try {
      append(`Encrypting amount=${amount}, secret=${secret}…`);
      const provider = new BrowserProvider(window.ethereum!);
      const signer = await provider.getSigner();
      const fhevm = await getFhevm();

      const input = fhevm.createEncryptedInput(VAULT_ADDRESS!, account);
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
    }
  }, [account, amount, secret, delaySec, vaultConfigured, append, refreshVaults]);

  const trigger = useCallback(
    async (id: bigint) => {
      setStatus("busy");
      try {
        const provider = new BrowserProvider(window.ethereum!);
        const signer = await provider.getSigner();
        const vault = new Contract(VAULT_ADDRESS!, VAULT_ABI, signer);
        append(`triggerReveal(${id})…`);
        const tx = await vault.triggerReveal(id);
        await tx.wait();
        append(`Triggered. Now any client (including this UI) can submit the KMS proof.`);
        await refreshVaults();
      } catch (e) {
        append(`Trigger failed: ${(e as Error).message}`);
      } finally {
        setStatus("idle");
      }
    },
    [append, refreshVaults],
  );

  const fulfill = useCallback(
    async (id: bigint) => {
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
            <button onClick={switchToSepolia} className="secondary">Switch to Sepolia</button>
          ) : (
            <span className="pill ok">{account.slice(0, 6)}…{account.slice(-4)}</span>
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
              <label>Amount</label>
              <input value={amount} onChange={(e) => setAmount(e.target.value)} />
              <p className="hint">A regular number ≤ 2⁶⁴-1. Stored encrypted as <code>euint64</code>.</p>
            </div>
            <div>
              <label>Secret</label>
              <input value={secret} onChange={(e) => setSecret(e.target.value)} />
              <p className="hint">Hex (<code>0x…</code>) or decimal, up to 32 bytes. Stored as <code>euint256</code>.</p>
            </div>
            <div>
              <label>Reveal in (sec)</label>
              <input value={delaySec} onChange={(e) => setDelaySec(e.target.value)} />
              <p className="hint">Try 60 to see the full round-trip in a minute.</p>
            </div>
            <button onClick={lock} disabled={status === "busy"}>
              Encrypt + lock
            </button>
          </div>
        )}
      </section>

      {vaultConfigured && account && onSepolia && (
        <section className="card">
          <h2>
            Your vaults <span className="pill">{vaults.length}</span>
          </h2>
          {vaults.length === 0 && (
            <p className="lede">No vaults yet for this account on Sepolia.</p>
          )}
          {vaults.map((v) => {
            const now = Math.floor(Date.now() / 1000);
            const ready = now > v.revealAt;
            return (
              <div key={String(v.id)} className="card vault-row">
                <div className="row" style={{ alignItems: "start" }}>
                  <dl className="kv" style={{ flex: 2 }}>
                    <dt>id</dt><dd>{String(v.id)}</dd>
                    <dt>revealAt</dt><dd>{new Date(v.revealAt * 1000).toLocaleString()}</dd>
                    <dt>state</dt>
                    <dd>
                      {v.revealed ? (
                        <span className="pill ok">revealed</span>
                      ) : ready ? (
                        <span className="pill live">ready</span>
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
                        <button
                          className="secondary"
                          disabled={!ready || status === "busy"}
                          onClick={() => trigger(v.id)}
                        >
                          1. Trigger
                        </button>
                        <button
                          disabled={!ready || status === "busy"}
                          onClick={() => fulfill(v.id)}
                        >
                          2. Fulfill
                        </button>
                      </>
                    )}
                  </div>
                </div>
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
