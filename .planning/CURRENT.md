# CURRENT — fhevm-oracle-skill

**Last touched:** 2026-05-10 (fourth-pass polish — judge-eye sweep on video assets)
**Status:** Four audit passes complete. First (`576a6bf`): purged fictional APIs in submissions. Second (`155aa50`+`7b773c2`): fixed BUILDER "FIRST line" wording, frontend/README AP-NNN table, stale Vercel directive. Third (`be77687`): contract NatSpec @dev block "FIRST line" → "BEFORE any state write" with parenthetical (matched the inline comment), test docstring `debugger.createDecryptionSignatures` → `publicDecrypt` (matched the real API), `next.config.js` + `.env.example` "NOT vercel-specific" → host-agnostic phrasing. Fourth (`2d76979`): VIDEO-VOICEOVER segment 3, VIDEO-INSTRUCTIONS line 50, `scripts/gen_slides.py` strings + regenerated `slides/03-safety.png` and `slides/07-callout-checksig.png` — all rewordings now match contract NatSpec exactly so judge cross-referencing video to contract sees zero contradiction. SKILL.md prescriptive "FIRST" left intact (it's the teaching abstraction, contract honors it in spirit). 4/4 tests still pass.

## Status

### Done in morning live-testing pass (2026-05-10)
- [x] Frontend wallet UX: Disconnect button + EIP-1193 listeners + reload persistence (commits `982449b`, `7dd31b4`)
- [x] Use-cases grid filled to 6 cards / 3×2 (commit `3145085`)
- [x] Wallet RPC compat: `eth_getLogs` block-range cap at 49K + EIP-55 address normalize via `ethers.getAddress()` in lock/trigger/fulfill (commit `a5d3aac`)
- [x] Vercel project repair: linked to GitHub `cryptoyasenka/fhevm-oracle-skill` main branch + Root Directory patched from `.` to `frontend` via Vercel API (CLI lacks command). Auto-deploy now triggers on push.
- [x] Manual prod deploy after fixes via `vercel --prod` to confirm latest live at https://fhevm-oracle-frontend.vercel.app

### Done by night-mode pass (previous session)
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
- Nothing in active edit. All work committed and pushed through `576a6bf` + this CURRENT.md update.

## Deep-audit pass (2026-05-10) — all 7 steps clean

1. **`contracts/AsyncRevealVault.sol`** — clean. AP-001 NatSpec tightened (`e31f2bb`): clarified that `checkSignatures` runs BEFORE any state write/cleartext use (not literally first line — 3 cheap reverts precede it).
2. **`SKILL.md`** — read 434 lines end-to-end. All 10 AP code examples + 3-step skeleton + decision tree + frontmatter pins verbatim correct.
3. **`package.json`** — pin parity with SKILL.md frontmatter confirmed: `@fhevm/solidity ^0.11.1`, `@fhevm/hardhat-plugin ^0.4.2`, `@zama-fhe/relayer-sdk ^0.4.1`, hardhat ^2.28.6, ethers ^6.16.0, solidity 0.8.27, evm cancun, node ≥20.
4. **`README.md`** — clean. Repo tree, 5-failure list, live links, stack — all correct after `8e24442`+`6e8da4d`. `FHE.checkSignatures(handles, abiEncodedCleartexts, decryptionProof)` 3-arg form correct.
5. **`hardhat.config.ts`** — clean. All secrets via `vars.get(KEY, default)`, public RPC fallback, no hardcoded keys, `bytecodeHash: none` for reproducibility.
6. **`test/AsyncRevealVault.ts`** — clean. 4 mock-mode cases drilling AP-010, canonical happy path, AP-002 replay, AP-001 sig absence. Real ciphertexts via `fhevm.createEncryptedInput.add64.add256.encrypt`. Real KMS proof via `fhevm.publicDecrypt(handles)`.
7. **Submissions** — fictional APIs purged (`576a6bf`). BOUNTY now uses `makePubliclyDecryptable`/`publicDecrypt`/3-arg `checkSignatures` consistently; BUILDER long description rewritten to match real flow.

## UX commits today (after morning hardening)
- `c7122e1` UX audit (9 issues), `30b1af2` wallet pill in navbar, `6120af5` activity-log empty state, `bab4372` Restore button visible, `95027bd` button cluster, `11556fe` Showing-all pill + dismissed badge, `1894a20` simplify vaults header, `609ee01` Connect button in navbar (REVERTED), `afacaa9` move Connect from navbar to Try-it section, `65b9694` Connect resilience (20s timeout + Connecting label + 4001 handling).

## Open UX item
- Yana said earlier "поле трай ит снова непонятным и перегруженным" — clarification asked but not answered. May resurface after Connect-button feedback. Try-it section has role-play callout + primitive hint + 3 inputs each with label + ?-tooltip + always-on hint — candidates for compaction.

## Next step (concrete)
Submission code + docs are clean. Yana's manual run:
1. Hide vault id=2,3 in UI (one click each).
2. Trigger + Fulfill vault id=1 → grab fulfill-tx Etherscan URL.
3. Fill `BUILDER-SUBMISSION.md` placeholders: fulfill-tx URL, video URL, prize wallet.
4. Fill `BOUNTY-SUBMISSION.md` placeholders: video URL, prize wallet.
5. Record 3-min LIVE VOICE demo via `.planning/VIDEO-VOICEOVER.md` + `.planning/VIDEO-INSTRUCTIONS-2026-05-10.md` slide pack.
6. Upload video to YouTube **unlisted** → paste URL into both submission MDs.
7. Submit Bounty + Builder forms before 2026-05-11 11:59 UTC.

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
- `2d76979` — docs(video): fourth-pass — script + slides match contract NatSpec ('FIRST line' → 'before any state write')
- `be77687` — docs: third-pass polish — NatSpec/test header consistency + drop stale Vercel comments
- `14f7935` — chore: CURRENT.md — second-pass audit complete
- `7b773c2` — chore(checklist): Phase 4 — mark frontend deploy DONE
- `155aa50` — docs: fix internal contradictions caught on second-pass audit
- `c59555d` — chore: CURRENT.md — deep-audit pass complete
- `576a6bf` — docs(submissions): purge fictional async-decryption API references
- `e31f2bb` — docs(contract): tighten AP-001 NatSpec
- `6e8da4d` — chore: drop stale VIDEO-SCRIPT.md
- `bf3507f` — copy: clarify domain-neutrality + mainnet-readiness
- `f58aa3a` — chore: CURRENT.md update
- `65b9694` — fix: Connect button resilience (20s timeout)
- `afacaa9` — ui: move Connect from navbar to Try-it section
- `a5d3aac` — fix(frontend): wallet RPC compat — block-range cap + EIP-55 address normalize
- `3145085` — ui: fill use-cases grid with two more primitives (DAO votes, embargoed disclosures)
- `7dd31b4` — feat(frontend): persist wallet connection across page reloads
- `982449b` — feat(frontend): Disconnect button + EIP-1193 event listeners
- `8e24442` — fix(video): scrub fictional API refs, point at slide PNGs
- `12fe7d4` — polish: drop node_modules path in SKILL.md, link upstream FHE.sol
- `c18c8e3` — feat: PNG slides for CapCut video assembly (9 slides)
- `e59afcc` — chore: CURRENT.md update
- `a30520d` — docs: video instructions + voiceover + tomorrow checklist
- `b4520d1` — fix: scrub false claims from README + BUILDER + AsyncRevealVault NatSpec
- `9aacba3` — chore: ignore .vercel in frontend
- `db1c799` — feat(hardhat): support PRIVATE_KEY var + public Sepolia RPC fallback
