# Bounty Track Submission — Pre-filled Form Answers

**Form:** https://forms.zama.org/developer-program-mainnet-season2-bounty-track
**Deadline:** 2026-05-10 23:59 AOE (= 2026-05-11 11:59 UTC)
**Submitter:** cryptoyasenka — yamihmih@gmail.com
**Reward:** 1500 / 1000 / 500 cUSDT (1st / 2nd / 3rd)

---

## Form fields — copy/paste

### Title

> fhevm-oracle: a SKILL.md that teaches AI agents to write correct FHEVM async-decryption contracts on the first try

### Short description (1–2 sentences)

> An AI-coding-agent skill drilling the canonical 3-step FHEVM async-decryption flow (`makePubliclyDecryptable` → relayer → signed callback) and ten failure modes that generic FHEVM skills demonstrably miss. Ships with a reference contract (AsyncRevealVault) that agents reproduce correctly when the skill is loaded — and botch when it's not.

### Long description

> When an AI agent (Claude Code, Cursor, Cline, etc.) is asked to write an FHEVM contract that decrypts encrypted state through the KMS oracle, it almost always botches at least one of:
>
> 1. Forgetting `FHE.checkSignatures(handles, cleartexts, proof)` before consuming any cleartext in the callback — opening a fake-decryption attack
> 2. Writing cleartext into storage before flipping the replay guard — same KMS proof can land twice
> 3. Mismatching the order of `bytes32[] handles` passed to `checkSignatures` and the tuple order in `abi.decode(cleartexts, (T1, T2, ...))`
> 4. Forgetting `FHE.allowThis(ct)` after a state-mutating operation, so future reads from `this` revert
> 5. Assuming a sync `FHE.decrypt(...)` exists — fhevm-solidity 0.11.1 has only `makePubliclyDecryptable` + signed callback or off-chain `userDecrypt`
> 6. Off-by-one finality (`>=` instead of `>`) on `revealAt` checks
> 7. No relayer-outage fallback path
>
> Generic FHEVM skills mention these in passing. **fhevm-oracle drills them as muscle memory** with a single 3-step canonical template, an FHE-type → callback-parameter mapping table, a decision tree for choosing between async oracle / user-decrypt / publicly-decryptable paths, ACL discipline rules, ten concrete anti-patterns each with bad-code / why-broken / fix-template, and a pre-deploy checklist.
>
> The skill is `SKILL.md` at the root of the repo. The reference contract (`contracts/AsyncRevealVault.sol`) is what an agent loaded with the skill produces — universal time-locked-reveal primitive that can be reused for sealed-bid auctions, vesting cliffs, time-locked dead-man switches, and similar patterns. Mock-mode Hardhat tests in `test/AsyncRevealVault.ts` exercise the canonical happy path and three failure modes via `hre.fhevm.publicDecrypt(handles)` — the mock-plugin entry that runs the full ACL → KMS-signature → `(cleartexts, proof)` flow inside the JSON-RPC interceptor.
>
> Pinned to `@fhevm/solidity ^0.11.1`, `@fhevm/hardhat-plugin ^0.4.2`, Solidity 0.8.27, EVM cancun. License BSD-3-Clause-Clear (matches `@fhevm/solidity`).

### GitHub repo URL

> https://github.com/cryptoyasenka/fhevm-oracle-skill

### Demo video URL (3-min, YouTube unlisted)

> [PASTE YOUTUBE LINK AFTER UPLOAD]

### Skill file path inside the repo

> `SKILL.md` (root)

### How is this skill different from existing FHEVM coding skills?

> Two existing FHEVM skills are public as of 2026-05-09 (most prominently Makabeez/fhevm-skill posted to the forum 2026-05-04). Both are broad surveys covering encrypted types, FHE ops, ACL, input proofs, decryption, frontend, testing, and anti-patterns at one section each. fhevm-oracle is intentionally narrow — it covers the single most error-prone primitive (async decryption) with the depth that broad skills cannot afford to spend. The two are complementary, not competing: load both, the agent gets generalist coverage from the broad skill and specialist accuracy on the highest-risk surface from this one.

### Wallet address for cUSDT prize (Sepolia or mainnet ETH compatible)

> [PASTE WALLET ADDRESS — same one Yana uses for retrodrops]

### License

> BSD-3-Clause-Clear

### How did you verify the skill works?

> Two synthetic tests:
>
> 1. Same prompt → same model (Claude Opus 4.7) → with vs. without the skill in cwd. The without-skill output omits at least three of the ten anti-patterns (recorded in the demo video). The with-skill output reproduces `AsyncRevealVault.sol` correctness.
> 2. Hardhat mock-mode tests in `test/AsyncRevealVault.ts` — four cases covering the canonical happy path, the AP-010 finality edge, the AP-002 replay guard, and AP-001 direct-call rejection. Run via `npx hardhat test`. They use `hre.fhevm.publicDecrypt(handles)` from `@fhevm/hardhat-plugin` to deterministically forge the KMS proof against the mock `KMSVerifier` and exercise `fulfillReveal` end-to-end.

---

## Source provenance — every claim in SKILL.md is grounded in:

- `@fhevm/solidity@0.11.1` — `lib/FHE.sol` source (`checkSignatures`, `makePubliclyDecryptable`, `allowThis`, `allow`, `fromExternal`, `toBytes32` signatures verbatim)
- `@fhevm/hardhat-plugin@0.4.2` — canonical `hardhat.config.ts` shape, mock-mode `fhevm.publicDecrypt(handles)` and `fhevm.createEncryptedInput` entry points
- `@zama-fhe/relayer-sdk@0.4.1` — `createEncryptedInput.add64.add256.encrypt` and `publicDecrypt` frontend wiring
- Zama documentation: `docs.zama.ai/protocol` for the KMS oracle architecture and the async-only mainnet decision
