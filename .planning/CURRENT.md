# CURRENT — fhevm-oracle-skill

**Last touched:** 2026-05-10 (Sepolia contract deployed, frontend wired, Vercel redeployed)
**Status:** Tech artifacts COMPLETE. AsyncRevealVault live on Sepolia + frontend live on Vercel pointing at it. Awaiting Yana's manual submission steps (demo video + form fills).

## Status
- [x] SKILL.md committed (`a927d86`, ~520 lines)
- [x] contracts/AsyncRevealVault.sol committed (`9fc032d`, ~220 lines)
- [x] 4/4 mock-mode Hardhat tests pass (`cd10cef`)
- [x] Next.js frontend committed (`7497f46`) + plain-language rewrite (`507669d`) + preview-copy fix (`596634f`)
- [x] **AsyncRevealVault deployed to Sepolia: `0x256e8948057982D483C60F7c060E3253a4d6A49b`**
- [x] FHECounter (companion): `0x839A250cC9E5a55C35EB8b47e3E9f0B42d7ad912`
- [x] Frontend live: https://fhevm-oracle-frontend.vercel.app — full interactive mode (no longer in "needs config" preview)
- [x] `NEXT_PUBLIC_VAULT_ADDRESS` set in Vercel production env, redeploy verified by smoke-test
- [x] GitHub repo `cryptoyasenka/fhevm-oracle-skill` PUBLIC
- [x] hardhat.config.ts gained `PRIVATE_KEY` var support + public-RPC fallback (commit `db1c799`)
- [x] BUILDER-SUBMISSION.md updated with Sepolia address + Etherscan link
- [ ] **YANA'S REMAINING MANUAL STEPS:**
  - [ ] Record 3-min demo video per VIDEO-SCRIPT.md
  - [ ] Upload to YouTube unlisted, paste link into both forms
  - [ ] On-chain demo: connect wallet on the live frontend, run lock + trigger + reveal, capture Etherscan tx URL for BUILDER-SUBMISSION.md `Sepolia transaction` field
  - [ ] Fill prize wallet address in BUILDER form
  - [ ] Submit Bounty form: forms.zama.org/developer-program-mainnet-season2-bounty-track
  - [ ] Submit Builder form: forms.zama.org/developer-program-mainnet-season2-builder-track
  - [ ] Deadline: 2026-05-11 11:59 UTC

## Open files
- Nothing in active edit. All work committed and pushed.

## Next step (concrete)
None on agent side. Yana drives video + form submission.

## Decisions / constraints
- Skill scope = NARROW oracle specialist (complementary to Makabeez/fhevm-skill)
- Demo contract = AsyncRevealVault (universal time-locked reveal primitive)
- Solidity 0.8.27 + evmVersion cancun + @fhevm/solidity ^0.11.1
- Replay protection + strict `>` finality + 24h CANCEL_GRACE
- No Claude co-author in commits
- Vercel exception ONLY for this project (per Yana 2026-05-09)
- Repo PUBLIC since 2026-05-10 (Yana confirmed via AskUserQuestion)
- Throwaway deploy wallet — do not reuse for anything valuable; mnemonic was typed at hidden Hardhat prompt (not exposed in shell history)

## Submission packages — ready for Yana
- BOUNTY-SUBMISSION.md → forms.zama.org/developer-program-mainnet-season2-bounty-track
- BUILDER-SUBMISSION.md → forms.zama.org/developer-program-mainnet-season2-builder-track (Sepolia address now filled)
- VIDEO-SCRIPT.md → 3-min demo recording template
- SUBMIT-CHECKLIST.md → 6-phase guide

## Live URLs
- Frontend: https://fhevm-oracle-frontend.vercel.app
- Repo: https://github.com/cryptoyasenka/fhevm-oracle-skill
- Vault on Etherscan: https://sepolia.etherscan.io/address/0x256e8948057982D483C60F7c060E3253a4d6A49b
- FHECounter on Etherscan: https://sepolia.etherscan.io/address/0x839A250cC9E5a55C35EB8b47e3E9f0B42d7ad912

## Commits on `main` (latest)
- 9aacba3 — chore: ignore .vercel in frontend
- db1c799 — feat(hardhat): support PRIVATE_KEY var + public Sepolia RPC fallback
- (next) docs: BUILDER-SUBMISSION.md Sepolia address fill + CURRENT.md update
