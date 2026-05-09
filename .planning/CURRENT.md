# CURRENT — fhevm-oracle-skill

**Last touched:** 2026-05-09 — bootstrap phase (Stage 1 prep snapshot taken)
**Status:** repo initialized, scaffolding in place; SKILL.md + AsyncRevealVault not yet written (post-compact work)

## Status
- [x] Strategy locked: Idea #1 `fhevm-oracle-skill` (Gap 1 — async decryption specialist), idea-pool ranked 26/30
- [x] Zama Bounty + Builder deadline verified: 2026-05-10 23:59 AOE = 2026-05-11 11:59 UTC
- [x] Bounty Track artifact verified: production-ready SKILL.md + 3-min demo video (judging: accuracy, completeness, agent effectiveness, code quality, error prevention)
- [x] Builder Track artifact verified: confidential dApp (contract+frontend) + 3-min video + Sepolia/mainnet deploy
- [x] Canonical FHEVM API verified from zama-ai/fhevm-hardhat-template@v0.4.1 (May 2026) — see snapshot for package versions, imports, async API
- [x] Repo bootstrapped (git init, .planning/, contracts/, test/, deploy/, tasks/)
- [ ] package.json + hardhat.config.ts + .gitignore
- [ ] hello-world FHECounter.sol (mirror of canonical) — sanity check
- [ ] First commit
- [ ] AUTO-COMPACT happens here (~37K tokens away)
- [ ] SKILL.md (the bounty artifact) — primary deliverable
- [ ] AsyncRevealVault.sol + tests/AsyncRevealVault.ts — Builder Track submission AND skill demo
- [ ] Frontend (Builder Track) — minimal Next.js page (defer if time pressure)
- [ ] README.md + BOUNTY-SUBMISSION.md + BUILDER-SUBMISSION.md + VIDEO-SCRIPT.md + SUBMIT-CHECKLIST.md

## Open files
- `C:/Projects/fhevm-oracle-skill/.planning/CURRENT.md` — this file
- (next) `package.json`, `.gitignore`, `hardhat.config.ts`, `contracts/FHECounter.sol`

## Next step (concrete)
1. Write `package.json` with verified dep versions (@fhevm/solidity@^0.11.1, @fhevm/hardhat-plugin@^0.4.2, etc.)
2. Write `hardhat.config.ts` mirror of canonical fhevm-hardhat-template
3. Write `.gitignore`
4. Write `contracts/FHECounter.sol` (canonical hello-world clone) for sanity
5. Initial commit `chore: bootstrap fhevm-oracle-skill`
6. After auto-compact: read prep snapshot + this CURRENT.md, then write SKILL.md as next deliverable

## Decisions / constraints
- **Skill scope = NARROW oracle specialist** (NOT broad — Makabeez covered broad with executable lint script)
- **Demo contract = AsyncRevealVault** — encrypted (amount, secret) payload with revealAt timestamp; oracle decrypts after reveal time; replay-protected via revealedRequestID guard. Universal time-locked reveal primitive — original (not auction/vote/ERC20 derivative).
- **Solidity 0.8.27** (not 0.8.24 like FHECounter.sol — the hardhat config sets version to 0.8.27, evmVersion cancun, optimizer 800 runs)
- **Mock mode for tests** (`if (!fhevm.isMock) this.skip();` pattern) — no Sepolia required for Bounty Track
- **Sepolia deploy** is Yana's manual step for Builder Track — pre-write deploy.ts + put exact CLI commands in SUBMIT-CHECKLIST.md
- **Frontend** = minimal Next.js (Builder requirement) — defer to phase 2, ship Bounty package first
- **Video** = Yana records using VIDEO-SCRIPT.md
- **No Claude co-author in commits** (memory rule)
- **No Vercel** for any future deploy (memory rule)

## Pointer to prep snapshot
`C:/Users/Yana/.claude/snapshots/pre-compact-prep-96b9106e-b6b1-4dd1-90dd-afd1aba617db.md` — full API surface + competitive intel + canonical code references

## Pointer to radar context
- `C:/Projects/builder-programs-radar/watchlist/zama-bounty-2026-05-10.md`
- `C:/Projects/builder-programs-radar/deep-dives/zama-bounty-track/idea-pool.md`
- `C:/Projects/builder-programs-radar/deep-dives/zama-bounty-track/competitor-analysis.md`
