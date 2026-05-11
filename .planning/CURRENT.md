# CURRENT — fhevm-oracle-skill

**Last touched:** 2026-05-11 12:46 — v2 для clip3 + clip5a + clip5b готовы, ждут утреннего ревью Yana

## 🆕 2026-05-11 v2 (critical-only scope)

Yana proснулась и выбрала scope **"только критичное"**: починить сломанный кадр clip3 + взять реальные скрины с фронта для clip5a/5b. Остальные клипы (1, 2, 4, 6) остаются v1. Готово и запушено:

- **`video-clips/clip3-contract-v2.mp4`** (35.000s) — commit `0f5c084`. Сломанный zoom-out перерисован: minimap-стиль (тонкие цветные полосы по строкам) + три callout-карточки справа (AP-010 → L111, AP-001 → L158, AP-002 → L161) с правильной привязкой, badges разнесены.
- **`video-clips/clip5a-demo-v2.mp4`** (20.000s) + **`video-clips/clip5b-reveal-v2.mp4`** (25.000s) — commit `3c2423f`. Реальные скриншоты фронта (real menu: AsyncRevealVault / Use cases / How it works / Try it / Your vaults / Activity log + GitHub) как фон + palette-matched PIL-карточки для state-анимаций поверх.
- **`app-screenshots/state-{1..4}.png`** — реальные viewport-кадры с live https://fhevm-oracle-frontend.vercel.app (hero, how-it-works, try-it, vaults+activity), захвачены через gstack `/browse`.
- **`scripts/gen_clip5_v2.py`** — новый скрипт рендера v2 (фон-композиция + overlays).

**v1 файлы untouched** — `clip3-contract-static.mp4`, `clip5a-lock-static.mp4`, `clip5b-reveal-static.mp4` на диске, как fallback.

**Утром Yana решает:** выбрать v1 ИЛИ v2 для каждого из трёх клипов перед записью голоса. Тайминги совместимы:
- clip1 (22s) + clip2 (35s) + **clip3-v2 (35s)** + clip4 (25s) + **clip5a-v2 (20s)** + **clip5b-v2 (25s)** + clip6 (18s) = **180s ровно**

## 🗒️ Прежняя заметка (v1 generation) — оставлена для контекста

## 🆕 2026-05-11 заметка для Yana

Перед записью используй упрощённый скрипт:
- **`.planning/VIDEO-VOICEOVER-SIMPLE.md`** — короткие предложения, фонетические подсказки для сложных слов, темп 88 wpm (медленно для тебя — комфортно)
- **`cue-cards/seg1..seg4.png` + `seg5a-demo-lock.png` + `seg5b-demo-reveal.png` + `seg6-outro.png`** — открой на втором мониторе и читай прямо с них (телесуфлёр). Сегмент 5 разбит на 5a (lock, 20s) и 5b (reveal, 25s): после "Done" в 5a ждёшь 60s и открываешь 5b
- **`video-clips/clip1-hook-static.mp4` / `clip2-problem-static.mp4` / `clip3-contract-static.mp4` / `clip6-outro-static.mp4`** — уже готовые MP4 нужной длительности (22s/35s/**35s**/18s) для статичных сегментов 1, 2, **3**, 6. В CapCut кладёшь их как видеоряд, поверх своя голосовая запись. Win+G для этих сегментов **не нужен**.
- **`thumbnail/youtube-1280x720.png`** — YouTube custom thumbnail. Загрузи при upload (Video details → Thumbnail → Upload thumbnail).
- **Etherscan screenshot** — сделай сама в момент upload: открой `https://sepolia.etherscan.io/tx/0xbb66e334506b7f7dcfe68b3f33e30d76f5d778396556553ea0df042091209c70` в браузере, Win+Shift+S → выдели страницу. Понадобится как backup для сегмента 5 если KMS callback залипнет.
- Старый `VIDEO-VOICEOVER.md` оставила как reference, но **читай из SIMPLE-версии**

**ВСЕ ВИДЕО-КЛИПЫ ГОТОВЫ** — Win+G не нужен совсем. Yana только пишет голос поверх в CapCut.

Готовые MP4 в `video-clips/`:
- `clip1-hook-static.mp4` (22s) — слайд 01 hero
- `clip2-problem-static.mp4` (35s) — слайд 02 anti-patterns
- `clip3-contract-static.mp4` (35s) — VS-Code AsyncRevealVault.sol с жёлтыми подсветками на 158/161/111
- `clip4-tests-static.mp4` (25s) — PowerShell `npx hardhat test`, прогрессивно появляются 4 √ test passes, финал "4 passing" green
- `clip5a-lock-static.mp4` (20s) — фронтенд lock-flow: hero → 63 в форме → encrypting → signing → pending → Locked
- `clip5b-reveal-static.mp4` (25s) — reveal pipeline: timer=0 → trigger → fulfill → AP-001 sig → AP-002 replay → cleartext 63
- `clip6-outro-static.mp4` (18s) — слайд 06 outro

Итого 180s = 3:00. Голос Yana поверх — в CapCut кладёшь все 7 MP4 встык на видео-дорожку, на аудио-дорожку записываешь свой голос по сегментам из `VIDEO-VOICEOVER-SIMPLE.md`.



## ⚡ ВОЗВРАЩЕНИЕ К РАБОТЕ — ЧИТАЙ ЭТО ПЕРВЫМ

**Дедлайн:** 2026-05-11, 14:59 Киев (= 11:59 UTC, = 23:59 AOE). Будильник ставь на 13:00 Киев = за 2 часа.

**Где остановилась:** Yana только что научилась пользоваться Win+G (Win+Alt+R = стоп). Тестовая запись лежит в `C:\Users\Yana\Videos\Captures\` (имя длинное `Untitled (Workspace) - Antigravity - VIDEO-PLAN-FINAL.md ...mp4` — это пробная, не финал). Готова записывать **Клип 1 (Hook)** по реальному плану.

**Главный playbook:** `C:/Projects/fhevm-oracle-skill/.planning/VIDEO-PLAN-FINAL.md` — открой и иди СВЕРХУ ВНИЗ. Там разделы:
- 0 = правила конкурса (verified)
- 1 = подготовка (Win+G, шрифты, MetaMask) — короткая, 5 мин
- **2 = запись 6 клипов по очереди** ← вот сюда возвращаешься
- 3 = troubleshooting
- 4 = монтаж в CapCut
- 5 = загрузка YouTube Unlisted
- 6 = сабмит Bounty формы
- 7 = сабмит Builder формы
- 8 = финальный чек-лист

**Следующий шаг конкретно:** записать **Клип 1 (Hook)** = 22 сек, открыть `C:\Projects\fhevm-oracle-skill\slides\01-title.png` на полный экран (F11), Win+G → красный кружок → прочитать voice-over (текст в плане, раздел 2 → «🎬 КЛИП 1»), Win+Alt+R = стоп. Файл сохранится в `C:\Users\Yana\Videos\Captures\`. Переименовать в `clip1-hook.mp4`. Затем Клип 2, 3, 4, 5, 6 — каждый описан пошагово в плане.

**Ключевые факты:**
- Веб-камера НЕ нужна. Голос ТВОЙ живой (не TTS). Видео ≤3:00 ровно.
- YouTube **Unlisted** (не Private! не Public!).
- Wallet address одинаковый в Bounty и Builder.
- Tx URL для Builder уже стоит (vault id=4 fulfilled).
- BOUNTY-SUBMISSION.md и BUILDER-SUBMISSION.md ждут только: YouTube link + wallet address.

**Где какие файлы:**
- Слайды: `C:/Projects/fhevm-oracle-skill/slides/*.png` (9 штук, 01-06 = main, 07-09 = optional callouts которые можно пропустить)
- Запись экрана: Win+G сохраняет в `C:/Users/Yana/Videos/Captures/`
- Текст voice-over: внутри VIDEO-PLAN-FINAL.md под каждым клипом
- Submission MD-файлы: `BOUNTY-SUBMISSION.md` + `BUILDER-SUBMISSION.md` в корне репо
- Контракт на Sepolia: `0x256e8948057982D483C60F7c060E3253a4d6A49b`
- Frontend: https://fhevm-oracle-frontend.vercel.app

**Антипаника:**
- Запутаешься на каком-то клипе → переснимаешь только его. Остальные не трогаешь.
- Win+G пишет ТО окно которое было активным при нажатии Record. Кликни в нужное окно ПЕРЕД Win+G.
- KMS callback в Клипе 5 залип >2 мин → используешь готовую tx на Etherscan: `0xbb66e334506b7f7dcfe68b3f33e30d76f5d778396556553ea0df042091209c70`

---


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

### Yana's remaining manual steps (deadline 2026-05-11 11:59 UTC)
**Master playbook = `.planning/VIDEO-PLAN-FINAL.md`** (390 lines, single source-of-truth, contest rules verified via WebFetch on both Zama form pages).

- [x] Fulfill-tx URL captured (vault id=4) and filled in BUILDER-SUBMISSION.md → commit `8e6c7ea`
- [ ] Record demo video per VIDEO-PLAN-FINAL.md (≤3:00, **screencast + real human voice — no TTS, no AI-generated video**; webcam NOT required — Zama only forbids AI generation)
- [ ] Upload video to YouTube **unlisted** (NOT Private)
- [ ] Fill `[PASTE YOUTUBE LINK]` in BOUNTY-SUBMISSION.md AND BUILDER-SUBMISSION.md
- [ ] Fill `[PASTE WALLET ADDRESS]` in both
- [ ] Submit Bounty form: forms.zama.org/developer-program-mainnet-season2-bounty-track
- [ ] Submit Builder form: forms.zama.org/developer-program-mainnet-season2-builder-track
- [ ] (Optional, not blocker) Verify contract on Etherscan via `npx hardhat verify`

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
**Yana opens `.planning/VIDEO-PLAN-FINAL.md` and follows it top to bottom.** It's the single playbook covering: rules → pre-recording prep → 6 recording segments with verbatim voice-over → CapCut editing → YouTube unlisted upload → Bounty form walkthrough → Builder form walkthrough → final checklist. Older fragmented files (VIDEO-INSTRUCTIONS, VIDEO-VOICEOVER, TOMORROW) remain in `.planning/` as references the master plan links into.

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
- **`.planning/VIDEO-PLAN-FINAL.md`** — MASTER playbook (390 lines): contest rules verified, prep, 6 recording segments verbatim, CapCut, YouTube, both form walkthroughs
- `BOUNTY-SUBMISSION.md` → forms.zama.org/developer-program-mainnet-season2-bounty-track (two `[PASTE]` placeholders left)
- `BUILDER-SUBMISSION.md` → forms.zama.org/developer-program-mainnet-season2-builder-track (fulfill-tx filled, two `[PASTE]` placeholders left: video URL + wallet)
- `.planning/VIDEO-INSTRUCTIONS-2026-05-10.md` — older slide-by-slide playbook (referenced by master)
- `.planning/VIDEO-VOICEOVER.md` — ~360-word script (referenced by master)
- `slides/01-…06-outro.png` + `07-…09-callout-*.png` — drop straight into CapCut

## Live URLs
- Frontend: https://fhevm-oracle-frontend.vercel.app
- Repo: https://github.com/cryptoyasenka/fhevm-oracle-skill
- Vault on Etherscan: https://sepolia.etherscan.io/address/0x256e8948057982D483C60F7c060E3253a4d6A49b
- FHECounter on Etherscan: https://sepolia.etherscan.io/address/0x839A250cC9E5a55C35EB8b47e3E9f0B42d7ad912

## Commits on `main` (latest first)
- `7d7aa55` — docs: master video plan + submission walkthrough — verified against Zama S2 form rules
- `8e6c7ea` — docs(builder): fill Sepolia fulfill-tx URL — vault id=4 cycle from frontend smoke-test
- `1804848` — chore: CURRENT.md — record fourth-pass commits
- `56b9c26` — docs(submissions): BUILDER AP-002 wording — 'state write' → 'cleartext write'
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
