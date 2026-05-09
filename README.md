# fhevm-oracle-skill

A focused **SKILL.md** that teaches AI coding agents to write correct **FHEVM async decryption oracle** patterns — Zama's most error-prone primitive — first try.

> Submission to **Zama Developer Program — Mainnet Season 2**
> - Bounty Track: this `SKILL.md` (production-ready)
> - Builder Track: `contracts/AsyncRevealVault.sol` + minimal frontend

## What this is

When an AI agent (Claude, Cursor, etc.) tries to write an FHEVM contract that decrypts encrypted state asynchronously through the KMS oracle, it almost always botches one of:

1. Handle ordering (which `bytes32[]` index maps to which decoded type)
2. Replay protection (the same `requestID` callback being processed twice)
3. Finality / consume-before-call (state being read after a stale callback)
4. Forgetting `FHE.checkSignatures(requestID, signatures)` — opens up fake-decryption attacks
5. Using sync decrypt that no longer exists on mainnet

A general-purpose FHEVM skill mentions all of these in passing. **This skill drills them as muscle memory** with a 3-step canonical template, a decision tree, embedded reference contract, and an error-prevention checklist that maps to OpenZeppelin's published anti-patterns #3, #5, and #10.

## Repo structure

```
SKILL.md                       <-- the bounty artifact (read this first)
contracts/
  FHECounter.sol               <-- canonical hello-world (sanity)
  AsyncRevealVault.sol         <-- the demo contract written by an agent USING this skill
test/
  AsyncRevealVault.ts          <-- Hardhat mock-mode tests proving the contract is correct
hardhat.config.ts
deploy/
  deploy.ts                    <-- Sepolia deploy script for the Builder Track demo
frontend/                      <-- Next.js 14 client app (Builder Track URL artifact)
  README.md                    <-- local dev + Railway deploy guide
  app/page.tsx                 <-- Connect / Lock / Trigger / Fulfill UI
  lib/fhevm.ts                 <-- relayer-sdk lazy init wrapper
SUBMIT-CHECKLIST.md            <-- step-by-step actions for submission
BOUNTY-SUBMISSION.md           <-- pre-filled answers for forms.zama.org bounty form
BUILDER-SUBMISSION.md          <-- pre-filled answers for forms.zama.org builder form
VIDEO-SCRIPT.md                <-- 3-min recording script
```

## Quick start

```bash
npm install
npx hardhat compile
npx hardhat test            # mock mode, ~5s
```

Sepolia deploy (Builder Track only):

```bash
npx hardhat vars set MNEMONIC
npx hardhat vars set INFURA_API_KEY
npm run deploy:sepolia
```

## Stack

- `@fhevm/solidity@^0.11.1` — FHE library (fully verified against canonical 2026-05 release)
- `@fhevm/hardhat-plugin@^0.4.2` — mock-mode Hardhat plugin
- `@zama-fhe/relayer-sdk@^0.4.1` — frontend relayer client
- Solidity `0.8.27`, Node ≥20, Hardhat 2.28.6, ethers 6.16.0

## License

BSD-3-Clause-Clear (matches the upstream `@fhevm/solidity` license).
