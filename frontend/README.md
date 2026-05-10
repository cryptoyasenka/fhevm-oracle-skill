# AsyncRevealVault — frontend

Minimal Next.js 14 demo for the [`fhevm-oracle`](../SKILL.md) skill. Lets a user
encrypt `(uint64 amount, uint256 secret)` in the browser, lock them in
`AsyncRevealVault` with a time delay, then trigger and fulfill the public
decryption via the Zama KMS.

This is the URL artifact required by the **Builder Track** of the Zama
Developer Program Mainnet S2. The contract proper lives at
[`contracts/AsyncRevealVault.sol`](../contracts/AsyncRevealVault.sol).

## Stack

- Next.js 14 App Router (client-only — no server actions, no API routes)
- `@zama-fhe/relayer-sdk@^0.4.1` for client-side encryption + `publicDecrypt`
- `ethers@^6.16` for wallet + contract calls
- Plain CSS (no Tailwind / no Vercel-only deps)

## Local development

```sh
# from this directory
npm install
cp .env.example .env.local        # then fill in NEXT_PUBLIC_VAULT_ADDRESS
npm run dev                        # http://127.0.0.1:3000
```

You need:
- An EIP-1193 wallet (MetaMask) on **Sepolia** (`chainId 11155111`).
- The vault address from `npm run deploy:sepolia` in the project root, set
  in `.env.local` as `NEXT_PUBLIC_VAULT_ADDRESS=0x…`.
- Some Sepolia ETH to pay for `lock()` + `triggerReveal()` + `fulfillReveal()`.

## Production build

```sh
npm run build
npm run start                      # serves the standalone build on :3000
```

`next.config.js` is set to `output: "standalone"` so the build can run on any
node host. The current live deployment is on Vercel via GitHub auto-deploy
(see live URL in the project root README); Railway / Cloudflare / fly.io
work the same way given the standalone output.

### Vercel (current host)

1. Vercel → New Project → Import the GitHub repo.
2. Settings → Root directory: `frontend`.
3. Variables tab → `NEXT_PUBLIC_VAULT_ADDRESS=0x…`.
4. Deploy. Auto-redeploys on every push to `main`.

### Railway alternative

1. Railway → New → Deploy from GitHub → set root directory = `frontend`.
2. Set the env var `NEXT_PUBLIC_VAULT_ADDRESS=0x…`.
3. Railway autodetects Next.js + the `standalone` output and runs
   `npm run build && npm run start`. Default port `3000` is fine.

## How it maps to the skill

| UI step | SDK call | Contract call | What it drills |
| --- | --- | --- | --- |
| "Encrypt + lock" | `createEncryptedInput(...).add64.add256.encrypt()` | `lock(encA, encS, proof, revealAt)` → `FHE.fromExternal` + `allowThis` + `allow(_, depositor)` | input-proof binding, ACL discipline (AP-004 + AP-005) |
| "Trigger" | — | `triggerReveal(id)` → `FHE.makePubliclyDecryptable` | strict-`>` finality (AP-010), idempotent retrigger on relayer outage (AP-009) |
| "Fulfill" | `publicDecrypt([encA, encS])` | `fulfillReveal(id, cleartexts, proof)` → `FHE.checkSignatures` then replay-guard flip then `abi.decode` | KMS proof verify before state write (AP-001), replay guard (AP-002), handle-tuple ordering (AP-003) |

Read [`../SKILL.md`](../SKILL.md) for the full anti-pattern catalogue.
