# CURRENT — fhevm-oracle-skill

**Last touched:** 2026-05-10 (NIGHT MODE — judge audit + slide pack + correctness sweep)
**Status:** Repo combed for false claims. AsyncRevealVault live on Sepolia. 9 CapCut-ready slides committed. Awaiting Yana's recording + form submission.

## Status

### Done by night-mode pass (this session)
- [x] Judge audit on README, BUILDER-SUBMISSION, AsyncRevealVault.sol — caught and fixed CRITICAL false claims:
  - README: wrong `FHE.checkSignatures` signature (was 2-arg, now correct 3-arg) + dropped hallucinated "OpenZeppelin's published anti-patterns" reference (commit `b4520d1`)
  - BUILDER-SUBMISSION: dropped fictional `outstandingRequestID` / `CANCEL_GRACE` / `cancelOutstandingRequest` features; mapped each highlight to real AP-NNN (commit `b4520d1`)
  - AsyncRevealVault.sol: added explicit AP-008 + AP-009 comments, removed unused `NotDepositor` error, header NatSpec now states AP-006/007 absent by construction (commit `b4520d1`)
- [x] VIDEO-INSTRUCTIONS + VIDEO-VOICEOVER scrubbed of same fictional API references (commit `8e24442`)
- [x] SKILL.md: replaced `node_modules/...` path with upstream GitHub link (commit `12fe7d4`)
- [x] PNG slide pack generated and committed: 9 × 1920×1080 in `slides/`, gen script `scripts/gen_slides.py` (commit `c18c8e3`)
- [x] Live frontend smoke-test (WebFetch): page loads, Connect-wallet button + contract address visible, no broken state
- [x] Pre-compact prep snapshot kept up to date

### Existing tech artifacts
- [x] SKILL.md (~520 lines)
- [x] contracts/AsyncRevealVault.sol (~220 lines)
- [x] 4/4 mock-mode Hardhat tests pass
- [x] Next.js frontend live at https://fhevm-oracle-frontend.vercel.app
- [x] AsyncRevealVault on Sepolia: `0x256e8948057982D483C60F7c060E3253a4d6A49b`
- [x] FHECounter (companion): `0x839A250cC9E5a55C35EB8b47e3E9f0B42d7ad912`
- [x] hardhat.config.ts supports PRIVATE_KEY var + public RPC fallback
- [x] Repo PUBLIC at github.com/cryptoyasenka/fhevm-oracle-skill

### Yana's remaining manual steps (morning 2026-05-10 → 2026-05-11 deadline)
- [ ] Record demo video using `slides/*.png` per `.planning/VIDEO-INSTRUCTIONS-2026-05-10.md`
- [ ] Run on-chain demo on the live frontend (lock + trigger + fulfill), capture fulfill-tx Etherscan URL
- [ ] (Optional polish) Verify contract on Etherscan: needs `npx hardhat vars set ETHERSCAN_API_KEY` then `npx hardhat verify --network sepolia 0x256e8948057982D483C60F7c060E3253a4d6A49b` — no constructor args. **Not a submission blocker.**
- [ ] Upload video to YouTube **unlisted**
- [ ] Fill BOUNTY-SUBMISSION + BUILDER-SUBMISSION form `[PASTE …]` placeholders (video URL, fulfill-tx URL, prize wallet)
- [ ] Submit both forms before 2026-05-11 11:59 UTC

## Open files
- Nothing in active edit. All work committed and pushed through `8e24442`.

## Next step (concrete)
Yana drives. Agent side waits for her morning checklist execution per `.planning/TOMORROW-2026-05-10.md`.

## Decisions / constraints
- Skill scope = NARROW oracle specialist (complementary to Makabeez/fhevm-skill)
- Demo contract = AsyncRevealVault (universal time-locked reveal primitive); 220 lines, single file
- Solidity 0.8.27 + evmVersion cancun + @fhevm/solidity ^0.11.1
- Replay protection via `revealed` flag (NOT a 24h CANCEL_GRACE — that was the fictional API scrubbed in audit)
- Strict `>` finality on revealAt
- No Claude co-author in commits
- Vercel exception ONLY for this project (per Yana 2026-05-09)
- Repo PUBLIC since 2026-05-10
- Throwaway deploy wallet — do not reuse for anything valuable

## Submission packages — ready for Yana
- `BOUNTY-SUBMISSION.md` → forms.zama.org/developer-program-mainnet-season2-bounty-track
- `BUILDER-SUBMISSION.md` → forms.zama.org/developer-program-mainnet-season2-builder-track (Sepolia address filled, three `[PASTE]` placeholders left for Yana)
- `.planning/VIDEO-INSTRUCTIONS-2026-05-10.md` — recording playbook keyed to `slides/*.png`
- `.planning/VIDEO-VOICEOVER.md` — ~360-word script
- `.planning/TOMORROW-2026-05-10.md` — morning checklist
- `slides/01-…06-outro.png` + `07-…09-callout-*.png` — drop straight into CapCut

## Live URLs
- Frontend: https://fhevm-oracle-frontend.vercel.app
- Repo: https://github.com/cryptoyasenka/fhevm-oracle-skill
- Vault on Etherscan: https://sepolia.etherscan.io/address/0x256e8948057982D483C60F7c060E3253a4d6A49b
- FHECounter on Etherscan: https://sepolia.etherscan.io/address/0x839A250cC9E5a55C35EB8b47e3E9f0B42d7ad912

## Commits on `main` (latest first)
- `8e24442` — fix(video): scrub fictional API refs, point at slide PNGs
- `12fe7d4` — polish: drop node_modules path in SKILL.md, link upstream FHE.sol
- `c18c8e3` — feat: PNG slides for CapCut video assembly (9 slides)
- `e59afcc` — chore: CURRENT.md update
- `a30520d` — docs: video instructions + voiceover + tomorrow checklist
- `b4520d1` — fix: scrub false claims from README + BUILDER + AsyncRevealVault NatSpec
- `9aacba3` — chore: ignore .vercel in frontend
- `db1c799` — feat(hardhat): support PRIVATE_KEY var + public Sepolia RPC fallback
