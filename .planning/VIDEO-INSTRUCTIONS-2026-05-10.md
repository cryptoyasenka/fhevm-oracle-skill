# Демо-видео — пошаговая инструкция (день записи 2026-05-10)

**Длительность:** 2:30–3:00 (жёсткий потолок 3:00)
**Формат:** screencast + voice-over (без вебкамеры), 1080p, mp4 ≤ 200 МБ
**Платформа:** YouTube **unlisted** (НЕ private — судьи не откроют)
**Редактор:** CapCut (по твоему выбору; инструкции написаны под CapCut, но любой NLE подойдёт)

> Готовые слайды лежат в `slides/*.png` (1920×1080) — их нужно просто перетащить на таймлайн. Никаких PowerPoint / Canva. Скрипт-генератор: `scripts/gen_slides.py` (на случай если захочешь править — Python+Pillow, без внешних ассетов).

---

## Что подготовить до записи (15 мин)

**1. Окна (по порядку Alt+Tab):**
- **W1** — VS Code, открыт `SKILL.md`, проскроллен на секцию `## Anti-patterns (AP-001 … AP-010)`. Шрифт 16+pt, тёмная тема. Боковую панель закрыть.
- **W2** — VS Code, открыт `contracts/AsyncRevealVault.sol`. Курсор на функции `fulfillReveal` (строка ~150). Шрифт 16+pt.
- **W3** — Терминал в папке проекта (`cd C:/Projects/fhevm-oracle-skill`), готов к `npx hardhat test`. Шрифт 18+pt. Перед записью прогони `cls`.
- **W4** — Браузер, https://fhevm-oracle-frontend.vercel.app, MetaMask установлен, Sepolia активна, на кошельке есть >0.05 SepETH.
- **W5** — Браузер вторая вкладка, https://sepolia.etherscan.io/address/0x256e8948057982D483C60F7c060E3253a4d6A49b

**2. Тех:**
- CapCut Desktop / OBS Studio / Win+G ScreenRecorder + Audacity — на твой вкус
- Микрофон проверь: говори 10 секунд, переслушай — никакого фона, нет эха
- Скорость записи 30 fps, битрейт 8000 kbps хватит

**3. Прорепетируй один раз без записи** — пройди все 6 сегментов с текстом из `VIDEO-VOICEOVER.md`. Засеки время. Если выходит >3:00 — режь на сегменте 5.

---

## Шесть сегментов

В CapCut: каждый сегмент = одна дорожка картинок (PNG из `slides/`) + одна дорожка screencast'а. Голос идёт сверху отдельной аудио-дорожкой одним непрерывным дублем.

### Сегмент 1 — Hook (0:00–0:20)

**Картинка:** `slides/01-title.png` — статика 20 сек. Никакого скринкаста.
**Голос:** `VIDEO-VOICEOVER.md` сегмент 1.

### Сегмент 2 — Проблема (0:20–0:55)

**Вариант A (быстрый):** `slides/02-anti-patterns.png` — статика 35 сек.
**Вариант B (живой):** скринкаст W1 — медленный скролл по секции AP-001…AP-010 в SKILL.md, мышкой выделяешь заголовки пока их называешь. Если выбрал A — пропускай W1.
**Голос:** `VIDEO-VOICEOVER.md` сегмент 2.

### Сегмент 3 — Что генерит агент со скиллом (0:55–1:30)

**Экран:** скринкаст W2 (`AsyncRevealVault.sol`).

**Что показать (скроллом + выделением мышью):**
1. Функция `fulfillReveal` (строка ~135) → `FHE.checkSignatures(handles, abiEncodedCleartexts, decryptionProof);` (строка 152) — это **первая строка** после проверок состояния. Это AP-001.
2. Строка ниже — `v.revealed = true;` (строка 155) — replay-guard ставится **до** записи cleartext. Это AP-002.
3. Скроллим вверх к `triggerReveal` (~ строка 106) → `if (block.timestamp <= v.revealAt) revert RevealTooEarly();` — строгое `<=`, не `<`. Это AP-010.
4. Скроллим к `lock` (строка 67) → блок `FHE.allowThis(amount); FHE.allowThis(secret); FHE.allow(amount, msg.sender); FHE.allow(secret, msg.sender);` — ACL discipline. Это AP-004 + AP-005.

**Overlay-callout'ы (опционально, поверх скринкаста в CapCut):**
- На моменте п.1 — наложи `slides/07-callout-checksig.png` в правый верхний угол на 2-3 сек.
- На моменте п.2 — `slides/08-callout-replay.png`.
- На моменте п.3 — `slides/09-callout-finality.png`.
Все три PNG прозрачные — просто перетащи поверх видео-дорожки.

**Голос:** `VIDEO-VOICEOVER.md` сегмент 3.

### Сегмент 4 — Тесты (1:30–2:00)

**Картинка-вступление:** `slides/04-tests.png` — статика 5 сек, пока произносишь первую фразу.
**Дальше:** скринкаст W3.
1. Запусти `npx hardhat test`.
2. Если запуск идёт >25 сек — в CapCut ускорь только этот участок до 3-5 сек, финальный экран `4 passing` оставь нормальной скоростью на 3 сек.
3. Подержи финальный кадр.

**Голос:** `VIDEO-VOICEOVER.md` сегмент 4.

### Сегмент 5 — On-chain демо на live фронте (2:00–2:45) — **КРИТИЧНЫЙ**

**Экран:** скринкаст W4 (https://fhevm-oracle-frontend.vercel.app).

**Действия (репетируй ДО записи!):**
1. **Connect wallet** — кликни кнопку, подтверди в MetaMask.
2. **Amount** — например `63`. **Secret** — `42`.
3. **Reveal time** — now+60sec (или то значение, которое предлагает UI).
4. **Click Lock** — подтверди в MetaMask, дождись зелёной галочки.
5. **Подожди ~60 сек** (в CapCut ускорь этот участок до 3-5 сек).
6. **Click Trigger reveal** — подтверди.
7. **Click Fulfill** — KMS callback, на странице появится cleartext `63` + `42`.
8. **Переключись на W5** (Etherscan) — покажи `triggerReveal` и `fulfillReveal` транзакции в списке. Скопируй URL fulfill-tx — он пойдёт в форму Builder Track ("Sepolia transaction").

**Если KMS callback тупит** (>2 мин на fulfillment):
- Запиши заранее «эталонную» сессию вечером, используй её как backup в монтаже.
- Или: смонтируй разрыв («время идёт…») и склей с уже готовым reveal с раннего теста.

**Под низ кадра можно вывести `slides/05-live.png`** в углу (frontend URL + contract address) — но это полировка, не обязательно.

**Голос:** `VIDEO-VOICEOVER.md` сегмент 5.

### Сегмент 6 — Outro (2:45–3:00)

**Картинка:** `slides/06-outro.png` — статика 15 сек.
**Голос:** `VIDEO-VOICEOVER.md` сегмент 6.

---

## Монтаж (30 мин в CapCut)

1. **Импорт:** перетащи всю папку `slides/` в Media. Перетащи 6 screencast-кусков.
2. **Сборка:** на main video track клади слайды и screencast'ы по порядку 1→6.
3. **Аудио:** запиши voice-over одним дублем по `VIDEO-VOICEOVER.md`, импортируй mp3/wav, положи на audio-track. Подрежь паузы.
4. **Между сегментами** — пауза 0.3-0.5 сек, чтобы зритель догнал.
5. **Subtle background music** по желанию (если используешь — −20dB чтобы не глушить голос).
6. **Captions** через YouTube auto-CC после загрузки (Zama может смотреть со звуком выключенным — это распространено).
7. **Экспорт:** 1080p, 30fps, H.264, ~8 Мбит/с. Размер целевой ≤ 200 МБ.

---

## Загрузка на YouTube

1. youtube.com → Create → Upload video
2. **Visibility: Unlisted** (не Private!)
3. Title: `fhevm-oracle — async-decryption skill for FHEVM agents (Zama S2 demo)`
4. Description: ссылка на репо + одно предложение что это + список 10 anti-patterns кратко.
5. Скопируй ссылку → впиши в `BOUNTY-SUBMISSION.md` И `BUILDER-SUBMISSION.md` поле "Demo video URL".

---

## Edge cases

- **Если запутаешься в записи** — не переписывай весь дубль, просто пометь «[РЕЗАТЬ]» вслух и продолжай. В монтаже легко вырежешь.
- **Если frontend упадёт** в момент записи — есть слайд `05-live.png` с адресом и URL, плюс screenshot fallback. Озвучь «и так выглядит результат», покажи слайд.
- **Если MetaMask тупит на Sepolia** — добавь фоллбек RPC `https://ethereum-sepolia-rpc.publicnode.com` через Settings → Networks → Edit. Это уже выручало.
- **Если оба варианта плохи** — смонтируй из A) экрана терминала с тестами B) скролла по контракту C) слайдов 01/02/03/05/06. Без on-chain демо это всё равно валидный submit, просто слабее.
