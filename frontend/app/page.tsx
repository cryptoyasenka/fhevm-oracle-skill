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
      <header>
        <div>
          <h1>AsyncRevealVault</h1>
          <p className="lede">
            Deposit an encrypted (amount, secret) pair, decrypt it via the Zama KMS only after the
            time lock expires. Demo of the canonical{" "}
            <code>makePubliclyDecryptable → checkSignatures</code> flow from the{" "}
            <code>fhevm-oracle</code> skill.
          </p>
        </div>
        <div>
          {!account ? (
            <button onClick={connect} disabled={status === "busy"}>Connect wallet</button>
          ) : !onSepolia ? (
            <button onClick={switchToSepolia} className="secondary">Switch to Sepolia</button>
          ) : (
            <span className="pill ok">{account.slice(0, 6)}…{account.slice(-4)}</span>
          )}
        </div>
      </header>

      {!vaultConfigured && (
        <section className="card">
          <h2>Not configured</h2>
          <p className="lede">
            Set <code>NEXT_PUBLIC_VAULT_ADDRESS</code> in your hosting env to the Sepolia
            deployment of <code>AsyncRevealVault</code>. Until then, this UI is read-only.
          </p>
        </section>
      )}

      {vaultConfigured && (
        <section className="card">
          <h2>Lock</h2>
          <div className="row">
            <div>
              <label>Amount (uint64)</label>
              <input value={amount} onChange={(e) => setAmount(e.target.value)} />
            </div>
            <div>
              <label>Secret (uint256, hex or dec)</label>
              <input value={secret} onChange={(e) => setSecret(e.target.value)} />
            </div>
            <div>
              <label>Reveal in (sec)</label>
              <input value={delaySec} onChange={(e) => setDelaySec(e.target.value)} />
            </div>
            <button onClick={lock} disabled={!account || !onSepolia || status === "busy"}>
              Encrypt + lock
            </button>
          </div>
        </section>
      )}

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
              <div key={String(v.id)} className="card" style={{ marginTop: 8 }}>
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
                  <div style={{ display: "flex", gap: 8, flex: 1 }}>
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
        <h2>Activity</h2>
        <pre className="log">{log.length === 0 ? "Waiting for actions…" : log.join("\n")}</pre>
      </section>

      <footer>
        <a href="https://github.com/zama-ai/fhevm" target="_blank" rel="noreferrer">
          Zama FHEVM
        </a>
        {" · "}
        Built on the <code>fhevm-oracle</code> skill
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
