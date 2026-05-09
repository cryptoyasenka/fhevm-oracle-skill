# CURRENT — fhevm-oracle-skill

**Last touched:** 2026-05-09 (tests green at cd10cef)
**Status:** ALL primary artifacts on disk + committed + 4/4 mock tests pass; awaiting Yana's GitHub push + Sepolia deploy + video record + form submit

## Status
- [x] Strategy locked: narrow async-decryption specialist (Gap 1 vs. Makabeez baseline)
- [x] Zama Bounty + Builder deadline verified: 2026-05-10 23:59 AOE = 2026-05-11 11:59 UTC
- [x] Repo bootstrapped + first commit `3bb5331`
- [x] **SKILL.md** (primary Bounty Track artifact) — committed `a927d86`, ~520 lines
- [x] **contracts/AsyncRevealVault.sol** (Builder Track demo + skill proof) — committed `9fc032d`, ~220 lines
- [x] **test/AsyncRevealVault.ts** (mock-mode tests, 4 cases) — committed `3b14aeb`
- [x] **deploy/deploy.ts** + `deploy:hardhat` npm script — committed `3014fce`
- [x] **VIDEO-SCRIPT.md** + **BOUNTY-SUBMISSION.md** + **BUILDER-SUBMISSION.md** + **SUBMIT-CHECKLIST.md** — committed `f4b529b`
- [x] `npm install` clean
- [x] `npx hardhat compile` clean (AsyncRevealVault + FHECounter)
- [x] `npx hardhat test` — **4/4 PASS** via `fhevm.publicDecrypt(handles)` (commit `cd10cef`)
- [ ] **YANA'S MANUAL STEPS** (per SUBMIT-CHECKLIST.md): GitHub push, Sepolia deploy, video record, form fill, submit

## Open files
- All primary artifacts committed; nothing in active edit
- Next agent action: verify npm install + compile + test pass cleanly before declaring "done"

## Next step (concrete)
1. Wait for `npm install` background task (id `btn8gwhxa`) to finish
2. Run `npx hardhat compile` — fix any pragma / import issues if AsyncRevealVault doesn't compile
3. Run `npx hardhat test` — fix any test setup issues
4. Optional: scaffold minimal `frontend/` Next.js page using @zama-fhe/relayer-sdk (Builder Track requires frontend URL)
5. Final atomic commit + update this CURRENT.md to status: complete

## Decisions / constraints
- Skill scope = NARROW oracle specialist (complementary to Makabeez/fhevm-skill, not competing)
- Demo contract = AsyncRevealVault (universal time-locked reveal primitive — sealed-bid auction / vesting cliff / dead-man switch in 220 lines)
- Solidity 0.8.27 + evmVersion cancun + @fhevm/solidity ^0.11.1 + @fhevm/hardhat-plugin ^0.4.2
- Mock-mode tests via `hre.fhevm.awaitDecryptionOracle()` (verified canonical from zama-ai/fhevm-mocks)
- Replay protection: `delete requestToVault[requestID]` + `outstandingRequestID = type(uint256).max` BEFORE state writes
- Strict `>` on revealAt (AP-010 finality)
- 24h CANCEL_GRACE for relayer-outage fallback (AP-009)
- No Claude co-author in commits, no .env in git, no Vercel for frontend deploy

## Submission packages — ready for Yana
- BOUNTY-SUBMISSION.md → forms.zama.org/developer-program-mainnet-season2-bounty-track
- BUILDER-SUBMISSION.md → forms.zama.org/developer-program-mainnet-season2-builder-track
- VIDEO-SCRIPT.md → 3-min demo recording template
- SUBMIT-CHECKLIST.md → 6 phases, ~3-5h total work for Yana

## Pointer to prep snapshot
`C:/Users/Yana/.claude/snapshots/pre-compact-prep-96b9106e-b6b1-4dd1-90dd-afd1aba617db.md`

## Commits on `main`
- 3bb5331 — bootstrap (package.json, hardhat.config, FHECounter, .gitignore, README, CURRENT.md)
- a927d86 — Add SKILL.md (Bounty Track primary deliverable)
- 9fc032d — Add AsyncRevealVault demo contract (Builder Track)
- 3b14aeb — Add Hardhat mock-mode tests (4 cases drilling AP-001/002/008/010)
- 3014fce — Add Sepolia deploy script
- f4b529b — Add submission packages (video script, both forms pre-filled, checklist)
