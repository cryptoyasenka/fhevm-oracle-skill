# VIDEO V2 PLAN — Yana feedback 2026-05-11

## Контекст
v1 клипы (`video-clips/clip*-static.mp4`) сделаны программно, но Yana найдена их слабыми:
- clip3 кадр zoom-out (30-35s) **сломан** — текст наслаивается на номера строк
- Слайды слишком статичные, особенно clip2 (35s статики = boring)
- clip5a фронтенд НЕ совпадает с реальной апкой (у Yana другое меню)
- Hook в первые 30s не объясняет идею проекта/пользу, не цепляет

**Цель v2:** профессиональные клипы с анимациями, real-app скрины, мощный hook. v1 НЕ удалять — рендерить рядом как `clip*-v2.mp4`. Утром Yana ревьюит и решает какую версию писать голосом.

**Дедлайн:** 2026-05-11 11:59 UTC = 14:59 Киев. Yana проснётся ~07:00 Киев = ~04:00 UTC. Нужно успеть к ~03:00 UTC чтобы был час на ревью.

## Правила Zama (перепроверить WebFetch'ом перед стартом)
- **Запрещено:** AI voice (TTS), AI talking-head video, AI-generated frames
- **Разрешено:** реальный голос (Yana), screencast, статичные слайды, программно отрендеренные слайды/анимации (= аналог PowerPoint/Keynote, наш подход OK)
- **Лимит:** ≤ 3:00 ровно (180s)
- **YouTube:** Unlisted
- **Ссылки форм:**
  - https://forms.zama.org/developer-program-mainnet-season2-bounty-track
  - https://forms.zama.org/developer-program-mainnet-season2-builder-track

**ПЕРВАЯ ЗАДАЧА после старта:** WebFetch обеих форм + поиск anti-AI правил.

## Phase 1 — Verify rules (5 min)
- [ ] WebFetch bounty form, искать "AI" / "generated" / "synthesis"
- [ ] WebFetch builder form, искать то же
- [ ] Записать verified выдержки в этот файл (секция "Verified rules" ниже)

## Phase 2 — Real app screenshots via /browse (15 min)
Frontend live: https://fhevm-oracle-frontend.vercel.app
Цель: получить реальные скрины app states для clip5a/5b.

- [ ] `/browse` → открыть URL
- [ ] Screenshot 1: hero (top of page, "Live on Sepolia" badge видна)
- [ ] Screenshot 2: Try-it section / Lock form blank
- [ ] Screenshot 3: Lock form заполненная (вписать "63", "123456789", "60" через playwright fill)
- [ ] Screenshot 4: Vaults section если есть существующие vault'ы
- [ ] Сохранить в `app-screenshots/state-{1..4}.png`

## Phase 3 — Дизайн clip1-v2 HOOK (22s)
**Не "F H E V M по буквам"** — слабо. Перепридумать на основе feedback "захватить внимание в первые 30s + объяснить идею".

**Концепт v2:** Quick montage — что такое FHEVM в действии:
- 0-3s: dark screen, появляется текст "Encrypted on-chain" (fade-in)
- 3-6s: рядом "Decrypt via oracle" (slide-in справа)
- 6-9s: рядом "AI agents botch 10 ways" (slide-in сверху, accent yellow)
- 9-14s: 5 быстрых "анти-паттерн карточек" появляются по 1 (1s each), красные с AP-номерами
- 14-18s: всё сжимается в "fhevm-oracle skill" logo (zoom-out)
- 18-22s: "Live on Sepolia" + repo URL появляются

Voice-over синхрон: "FHEVM keeps data secret. To read it, you call the oracle. AI agents make ten mistakes. We built a skill to fix that. Plus a live contract on Sepolia."

## Phase 4 — Дизайн clip2-v2 PROBLEM (35s)
v1 = статичный список. v2 = 5 AP-карточек появляются ПО ОЧЕРЕДИ.

- 0-3s: title "5 ways agents botch async decrypt" (typewriter)
- 3-9s: AP-001 карточка fade+slide-in, мини-код "❌ no checkSignatures()" → "✓ FHE.checkSignatures(...)" diff
- 9-15s: AP-002 (same animation)
- 15-21s: AP-003 (handles[] / abi.decode swap)
- 21-27s: AP-007 (FHE.decrypt() doesn't exist)
- 27-33s: AP-010 (>= vs >)
- 33-35s: "skill drills all ten as muscle memory" финал

## Phase 5 — Дизайн clip3-v2 CONTRACT (35s) — **главный фикс**
- 0-3s: file header "AsyncRevealVault.sol" с typewriter
- 3-11s: smooth pan to line 158, highlight slides in (line 158 area centered)
- 11-19s: smooth pan to line 161
- 19-27s: smooth pan to line 111
- 27-32s: **починить** zoom-out (правильный line_h в `draw_full_file_frame`)
- 32-35s: финал "220 lines · one file · all three traps fixed"

**Технический фикс zoom-out:**
- Текущий баг: `line_h = (code_bottom - code_top) / total_lines` = ~3px, при font_size 11 → перекрытие
- Решение: либо уменьшить font_size до 8 (нужен моноширинный 8px фон), либо отрисовать только КЛЮЧЕВЫЕ строки (highlight rows) + dim rest, либо без line numbers совсем, или сократить total_lines view (показать только функции fulfillReveal+triggerReveal compact)
- **Лучшее:** view "code map" — миниатюра каждой строки как тонкая полоска (3-4px высота) + цветная заливка только для подсвеченных. Похоже на minimap в VS Code справа.

## Phase 6 — Дизайн clip4-v2 TESTS (25s)
- 0-3s: пустой PS prompt + cursor мигает (2 кадра альт)
- 3-5s: typewriter `npx hardhat test`
- 5-7s: compile output появляется
- 7-11s: тест AP-001 — pulsing dot → √ tick с rotation
- 11-15s: тест AP-002 — то же
- 15-19s: тест AP-010 — то же
- 19-22s: тест canonical — то же
- 22-25s: large "4 passing" — scale-in с bounce

## Phase 7 — Дизайн clip5a-v2 LOCK (20s)
**Использовать реальные screenshots** (из Phase 2).
- 0-3s: real hero screenshot — pan/zoom (Ken Burns) к Connect-wallet section
- 3-6s: real form blank screenshot
- 6-10s: real form filled "63"/"123"/"60" screenshot — слово "63" подсвечивается жёлтым highlight rect (overlay)
- 10-13s: overlay "🔒 Encrypting via FHEVM SDK..." поверх формы (pulsing)
- 13-16s: overlay "Awaiting wallet signature..."
- 16-20s: "✓ Locked. Vault #5. Etherscan: 0xbb66..." с зелёным фоном

## Phase 8 — Дизайн clip5b-v2 REVEAL (25s)
- 0-3s: countdown "00:00" pulse (анимированный timer)
- 3-7s: "Trigger reveal" button highlight + click animation
- 7-12s: handles[] block typewriter + checkSignatures call
- 12-15s: AP-001 ✓ pulse green
- 15-18s: AP-002 ✓ pulse green
- 18-22s: cleartext "63" appears with scale-in + accent glow
- 22-25s: "stayed secret until the timer" финал

## Phase 9 — Дизайн clip6-v2 OUTRO (18s)
v1 — статика. v2 — slow Ken Burns zoom (background) + текст elements appear sequentially:
- 0-3s: "Repo: github.com/cryptoyasenka/fhevm-oracle-skill" slide-in
- 3-7s: badge "Bounty + Builder" появляется
- 7-11s: "License: BSD-3-Clause-Clear"
- 11-15s: "Live on Sepolia: 0x256e..."
- 15-18s: "Thanks Zama" с глоу

## Phase 10 — QA + commit
- [ ] Прочесть случайные кадры каждого v2 клипа (`Read tool` на PNG)
- [ ] ffprobe длительность каждого
- [ ] Сумма всех = 180s ровно
- [ ] Commit + push после КАЖДОГО клипа (Yana в зоне отключений)
- [ ] Финальный commit: "feat(video): v2 clips ready for review — Yana to pick variant"
- [ ] Записать `AUTO_CONTINUE: DONE` в `.planning/V2-STATUS.md`

## Verified rules (заполнить в Phase 1)
_TBD_

## Inspiration refs (заполнить если найдём)
- Yana's Solana hackathon video 2 и 3 — поискать в `C:/Projects/solana-frontier-hackathon/`, MEMORY entries, или YouTube ссылки
