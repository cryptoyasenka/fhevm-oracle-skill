# fhevm-oracle-skill

A focused **SKILL.md** that teaches AI coding agents to write correct **FHEVM async-decryption oracle** patterns first try — Zama's most error-prone primitive — paired with a 220-line reference contract that proves the pattern works on mainnet shape.

> Submission to **Zama Developer Program — Mainnet Season 2**
> - **Bounty Track:** [`SKILL.md`](./SKILL.md) — drop-in skill for Claude / Cursor / any agent that respects `.claude/skills/`
> - **Builder Track:** [`contracts/AsyncRevealVault.sol`](./contracts/AsyncRevealVault.sol) + Next.js frontend — live on Sepolia today

## Live links

- **Frontend (Next.js, Sepolia):** https://fhevm-oracle-frontend.vercel.app
- **AsyncRevealVault on Etherscan:** https://sepolia.etherscan.io/address/0x256e8948057982D483C60F7c060E3253a4d6A49b
- **Skill file (the bounty):** [`SKILL.md`](./SKILL.md)
- **Reference contract (220 LOC):** [`contracts/AsyncRevealVault.sol`](./contracts/AsyncRevealVault.sol)

## What this is

When an AI coding agent writes an FHEVM contract that decrypts encrypted state through the KMS oracle, it almost always trips on one of these:

1. **Forgetting `FHE.checkSignatures(handles, abiEncodedCleartexts, decryptionProof)`** — without it, anyone can submit arbitrary cleartext (fake-decryption attack).
2. **Handle-tuple ordering drift** — `handles[i]` order must match `abi.decode(cleartexts, (T1, T2, ...))` order; a swap is a silent state-corruption bug.
3. **Replay protection** — flipping the `revealed` guard *after* state writes lets the same KMS proof be re-submitted.
4. **Off-by-one finality** — `block.timestamp >= revealAt` vs `>` reads "at" as "after".
5. **Assuming sync decrypt exists** — fhevm-solidity 0.11.1 has no synchronous on-chain `decrypt`; only `makePubliclyDecryptable` + signed callback or off-chain `userDecrypt`.

A general FHEVM skill mentions these in passing. **This skill drills them as muscle memory** with a 3-step canonical template, a decision tree, an embedded reference contract, and a pre-deploy checklist. Ten anti-patterns (`AP-001`..`AP-010`) each get a broken example, the failure mode, and a fix template.

## Repo structure

```
SKILL.md                       <-- the bounty artifact (read this first)
contracts/
  AsyncRevealVault.sol         <-- the demo contract written from the skill
  FHECounter.sol               <-- canonical hello-world (sanity check)
test/
  AsyncRevealVault.ts          <-- Hardhat mock-mode tests proving the contract is correct
deploy/
  deploy.ts                    <-- Sepolia deploy script
hardhat.config.ts              <-- supports MNEMONIC or PRIVATE_KEY var, public RPC fallback
frontend/
  app/page.tsx                 <-- Connect / Lock / Trigger / Fulfill UI (Next.js 14)
  lib/fhevm.ts                 <-- relayer-sdk lazy initialisation
  README.md                    <-- local dev + Vercel deploy guide
BOUNTY-SUBMISSION.md           <-- pre-filled answers for the Bounty Track form
BUILDER-SUBMISSION.md          <-- pre-filled answers for the Builder Track form
.planning/VIDEO-VOICEOVER.md   <-- 3-min recording voice-over (~360 words)
.planning/VIDEO-INSTRUCTIONS-2026-05-10.md  <-- recording playbook keyed to slides/*.png
```

## Quick start

```bash
npm install
npx hardhat compile
npx hardhat test            # 4/4 mock-mode tests, ~5s
```

Sepolia deploy (Builder Track):

```bash
npx hardhat vars set PRIVATE_KEY      # one-string secret, run alone, paste at the prompt
# (or use `npx hardhat vars set MNEMONIC` if you prefer a 12-word seed)
npm run deploy:sepolia                # public RPC by default; INFURA_API_KEY is optional
```

The deploy script prints both contract addresses. Set `NEXT_PUBLIC_VAULT_ADDRESS` in your hosting env, then build the frontend.

## Stack

- `@fhevm/solidity@^0.11.1` — FHE library (verified against the canonical 2026-05 release)
- `@fhevm/hardhat-plugin@^0.4.2` — mock-mode Hardhat plugin
- `@zama-fhe/relayer-sdk@^0.4.1` — frontend relayer client (encrypt + publicDecrypt)
- Solidity `0.8.27` (`evmVersion: cancun`), Node ≥20, Hardhat 2.28.6, ethers 6.16.0

## License

BSD-3-Clause-Clear — matches the upstream `@fhevm/solidity` license.
