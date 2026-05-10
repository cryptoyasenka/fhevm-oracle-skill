# 🎬 Финальный план: запись видео + сабмит обеих форм Zama S2

**Дедлайн:** 10 May 2026, 23:59 AOE = **2026-05-11 11:59 UTC** (≈ 14:59 Киев). Считай что у тебя сутки.

**Что в итоге сделаешь:** ОДИН видеофайл ≤3:00, загруженный на YouTube unlisted. Ссылка идёт в обе формы (Bounty + Builder). Плюс заполнишь два placeholder'а (wallet address + tx URL уже стоит).

---

## 0. Правила конкурса (verified из формы Zama)

Эти правила я подтвердила прямо со страниц форм Zama. Что соблюдаем железно:

### Builder Track (`forms.zama.org/developer-program-mainnet-season2-builder-track`)
- ⚠️ **«A 3-minute video demo to pitching the project (Real-person pitch only. AI-generated video or voice will not be considered.)»**
  - **≤3:00 ровно** (не 3:01)
  - **Голос ТВОЙ живой** — никакой TTS / ElevenLabs / synthesized voice. Запиши своим голосом.
  - **Видео не AI-сгенерированное** — никаких Sora / Runway / HeyGen аватаров. Обычный screencast с твоим голосом — это и есть «real-person pitch». **Лицо/webcam Zama НЕ требует** (verbatim проверено на странице формы 2026-05-10). Анонимность сохраняешь.
- Privacy: на форме Zama нет явной privacy clause. YouTube Unlisted даёт приватность де-факто (только по ссылке, не индексируется поиском, не появляется на канале публично).
- Призовой фонд: **7,000 cUSDT всего, 7 победителей × 1,000 cUSDT каждый**
- Deploy: Sepolia или mainnet (у тебя Sepolia ✓)

### Bounty Track (`forms.zama.org/developer-program-mainnet-season2-bounty-track`)
- Дедлайн идентичный
- Призовой фонд: **3,000 cUSDT, до 3 победителей** (распределение может быть скорректировано «based on the quality of submissions»)
- Specific video rules не процитированы на странице обзора. Используем тот же видеофайл что и для Builder Track — он соответствует более строгим правилам.

### Что это значит для записи:
1. ОДИН видеофайл удовлетворяет оба сабмита
2. Запись своим голосом, не TTS
3. Полный screencast без лица — норм. Никакая webcam не нужна.
4. Жёсткий cut на 3:00 — если выходит дольше, режем Сегмент 5

---

## 1. ДО записи (15 мин подготовки)

### 1.1 НЕ надо открывать 5 окон сразу

Раньше я писала «открой 5 окон» — забудь. Запутаешься. Вместо этого:

**Принцип:** в каждом сегменте открываешь ТОЛЬКО ОДНО окно, записываешь короткий клип (20-45 сек), останавливаешь, закрываешь. Потом следующий сегмент → следующее окно. Получишь 5 коротких файлов. В CapCut склеишь.

То есть никакого Alt+Tab вживую. Никакой паники. Один клип = одно окно = одна короткая речь.

### 1.2 Чем записывать экран — Win+G (самое простое)

В Windows 11 уже встроено. Не надо ничего ставить.

1. Нажми клавиши **Win + G** одновременно. Откроется панелька Game Bar
2. В виджете «Capture» (значок камеры) нажми **круглый красный кружок** = «Start recording»
3. Запись пошла. Теперь говори и кликай мышью — всё пишется
4. Чтобы остановить — **Win+Alt+R** или нажми синий квадратик в всплывающей мини-панельке
5. Файлы сохраняются в `C:\Users\Yana\Videos\Captures\` автоматически с датой+временем в имени

**Микрофон проверь ДО записи:** Win+G → значок шестерёнки → Audio → Default microphone → проверь что Volume не на нуле. Скажи «раз-два-три» в любой записи 5 сек, переслушай — слышно тебя? Окей.

### 1.3 Подготовка к записи (один раз, 5 минут)

- В каждое окно VS Code зайди и **увеличь шрифт** до 18-20pt: `Ctrl+=` (плюсик зажимай несколько раз)
- В терминале PowerShell тоже подними шрифт: правый клик в шапке → Properties → Font → 22pt
- В браузере Chrome: Ctrl+= 2-3 раза для зума ~125%
- На Vercel-фронте **перед записью** нажми × Hide на 4 старых карточках id=1..4 (чтобы список был чистый)
- В MetaMask убедись что подключён к Sepolia и есть ≥0.05 SepETH

### 1.4 Прорепетируй текст один раз без записи

- Прочти voice-over всех 6 сегментов вслух с секундомером на телефоне
- Должно выйти 2:30-3:00. Если сильно меньше — медленнее. Если больше — режем Сегмент 5

### 1.5 Веб-камера НЕ нужна

Zama не требует показа лица. Screencast + твой голос = full compliance.

---

## 2. Запись — пошагово, 6 коротких клипов

**Стратегия (упрощённая):** записываешь 6 отдельных коротких клипов, в каждом своё окно. Голос пишется ВНУТРИ каждого клипа (не отдельной дорожкой) — Win+G сразу пишет и экран, и микрофон. Запутаешься в одном — переснимаешь только тот клип, остальные не трогаешь.

Перед каждым клипом — твоя текущая задача и точный текст. Жирным **акцент** (повышай голос).

⚠️ **Правило 1:** перед каждым «Start recording» закрой все ненужные окна. На экране должно быть ТОЛЬКО то окно которое описано.

⚠️ **Правило 2:** уточняй перед записью — текст ты читаешь со ВТОРОГО монитора или с распечатки на бумаге. Не из этого файла на том же экране что записываешь.

---

### 🎬 КЛИП 1 — Hook (~20 сек)

**Что открыть:** в браузере открой картинку `C:\Projects\fhevm-oracle-skill\slides\01-title.png` (просто двойной клик в Проводнике, откроется в фотопросмотрщике на весь экран).

**Что делать:** ничего. Картинка стоит на экране, ты говоришь.

**Что сказать (читаешь медленно, ~22 сек):**

> «FHEVM lets you compute on **encrypted data** on Ethereum. But the moment your contract needs to **reveal a result**, you hit the async decryption oracle — and that's where AI coding agents consistently ship **broken code**. fhevm-oracle is a SKILL.md that fixes that, plus a reference contract that proves the pattern works on Sepolia today.»

**Запись:** Win+G → Start recording → говори → Stop. Сохрани файл, переименуй в `clip1-hook.mp4`.

---

### 🎬 КЛИП 2 — Проблема (~35 сек)

**Что открыть:** одна из двух опций — выбери что проще:
- **Опция A (легче):** двойной клик на `slides\02-anti-patterns.png` — открой картинку на весь экран. Ничего на ней не делаешь.
- **Опция B (живее):** открой VS Code на файле `C:\Projects\fhevm-oracle-skill\SKILL.md`. Через `Ctrl+G` → введи `184` → Enter. Курсор окажется на секции «The 10 anti-patterns». Закрой Explorer-панельку слева (`Ctrl+B`). Шрифт ≥18pt.

**Что делать:**
- Опция A: ничего, картинка стоит
- Опция B: медленно скроллишь колёсиком ВНИЗ по списку AP-001 → AP-010, не быстрее одной строки в секунду

**Что сказать (~35 сек):**

> «Without context, an agent will skip checkSignatures and let anyone fake a decryption. It will mismatch handle order against the abi-decode tuple. It will write cleartext **before flipping the replay guard**, so the same KMS proof can be re-submitted. It will assume a sync decrypt that doesn't exist on mainnet. Or it will trigger reveal at exactly block-dot-timestamp equals revealAt — off by one. The skill enumerates **all ten anti-patterns** as muscle memory.»

**Запись:** Win+G → Start → говори → Stop → `clip2-problem.mp4`.

---

### 🎬 КЛИП 3 — Контракт (~35 сек) — самый важный

**Что открыть:** VS Code на файле `C:\Projects\fhevm-oracle-skill\contracts\AsyncRevealVault.sol`. `Ctrl+G` → `135` → Enter (попадёшь в `fulfillReveal`). Закрой Explorer (`Ctrl+B`). Шрифт ≥18pt. На экране видны строки ~130-160.

**Что делать на экране (по порядку, синхронно с голосом):**

1. **Когда говоришь «checkSignatures runs before any state write»:** мышью выдели строку 152 (там `FHE.checkSignatures(handles, abiEncodedCleartexts, decryptionProof);`). Подержи выделение 2 сек.
2. **Когда говоришь «cheap input-validity reverts that touch no cleartext»:** скролл колёсиком на 3-4 строки ВВЕРХ. Покажи 3 коротких revert-строки `if (...) revert ...`.
3. **Когда говоришь «replay flag flips to true before the cleartext lands»:** скролл ВНИЗ на 3 строки до `v.revealed = true;` (~строка 155). Выдели её мышью.
4. **Когда говоришь «strict greater-than»:** `Ctrl+G` → `106` → Enter. Выдели строку с `if (block.timestamp <= v.revealAt) revert RevealTooEarly();`.
5. **Когда говоришь «two hundred and twenty lines, one file»:** нажми `Ctrl+Shift+−` (минус) 3-4 раза — экран отдалится, увидишь весь файл целиком как одно полотно.

Не паникуй если не успеваешь идеально синхронизировать — главное чтобы выделение строки было в ~2 сек от фразы. Если разъехалось — переснимешь.

**Что сказать (~35 сек):**

> «This is AsyncRevealVault — the reference contract written from the skill. Notice: checkSignatures runs **before any state write** in the callback — the only lines above it are cheap input-validity reverts that touch no cleartext. The replay flag flips to true **before** the cleartext lands — re-submitting the same KMS proof reverts at AlreadyRevealed. The timestamp check is a **strict greater-than**. ACL discipline is preserved across every state mutation. Two hundred and twenty lines, one file.»

**Запись:** Win+G → Start → говори+кликай → Stop → `clip3-contract.mp4`.

---

### 🎬 КЛИП 4 — Тесты (~25 сек)

**Что открыть:** PowerShell в папке проекта. Открой Windows Terminal (Win→набери «terminal»). Введи:
```
cd C:\Projects\fhevm-oracle-skill
cls
```
Шрифт подними: правый клик в шапке → Properties → Font → 22pt.

**Что делать на экране:**

1. **Сразу после Start recording:** набери `npx hardhat test` и нажми Enter.
2. Жди пока тесты бегут (~20-25 сек). Молчи или говори voice-over (см. ниже).
3. Когда внизу появится **`4 passing`** — подержи кадр 3 сек.
4. Stop.

**Что сказать (~25 сек):**

> «Four Hardhat mock-mode tests drill the same anti-patterns the skill enumerates: signature absence, replay-after-success, off-by-one finality, and the canonical happy path. A contract written from the skill **passes them by construction**.»

**Запись:** Win+G → Start → набираешь команду → говоришь во время выполнения → видишь `4 passing` → ждёшь 3 сек → Stop → `clip4-tests.mp4`.

⚠️ В CapCut потом ускоришь середину этого клипа в 5 раз чтобы тесты «пробежали» за 5 сек а не 25.

---

### 🎬 КЛИП 5 — Live demo (~45 сек) — самый рискованный

**Что открыть:** браузер на https://fhevm-oracle-frontend.vercel.app. **ДО НАЧАЛА ЗАПИСИ:**
- Подключи кошелёк (Connect → MetaMask → Sepolia)
- Нажми × Hide на старых карточках id=1..4 чтобы экран был пустой
- Готов?

**Что делать на экране (после Start recording):**

1. **Введи Amount** = `63`
2. **Введи Secret** = `42`
3. **Reveal time** оставь default (now+60sec)
4. **Нажми Lock** → MetaMask → Confirm → жди зелёную галочку (~15 сек)
5. **Жди 60 секунд** до revealAt (в монтаже это ускоришь)
6. **Нажми Trigger reveal** → MetaMask → Confirm
7. **Нажми Fulfill** → MetaMask → Confirm → на экране появится cleartext `63`
8. Stop.

**Что сказать (~45 сек):**

> «Now the live contract on Sepolia. I'm encrypting a number — **sixty-three**. The relayer SDK takes my plaintext, produces a ciphertext handle plus a zero-knowledge proof. Reveal in sixty seconds. The Lock transaction stores the encrypted handle and binds the ACL to me and the contract.
>
> Sixty seconds pass.
>
> I trigger reveal. The vault flags both ciphertexts as publicly decryptable. The relayer fetches the KMS-signed cleartext and calls fulfillReveal. The callback verifies signatures, flips the replay guard, then writes the cleartext. **Sixty-three.** The number was encrypted on chain until the timer expired.»

**Запись:** Win+G → Start → проходи 8 шагов → Stop → `clip5-demo.mp4`.

⚠️ **Если что-то пошло не так (KMS callback >2 мин не приходит):**
- Stop запись
- Открой готовую транзакцию: https://sepolia.etherscan.io/tx/0xbb66e334506b7f7dcfe68b3f33e30d76f5d778396556553ea0df042091209c70
- Запиши новый клип 30 сек этой страницы (скролл сверху вниз) с тем же voice-over. Назови `clip5-demo-fallback.mp4`.

---

### 🎬 КЛИП 6 — Outro (~18 сек)

**Что открыть:** двойной клик на `slides\06-outro.png`. Картинка на весь экран.

**Что делать:** ничего, картинка стоит.

**Что сказать (~18 сек):**

> «Repo at github-dot-com slash cryptoyasenka slash fhevm-oracle-skill. SKILL-dot-MD is the bounty deliverable. AsyncRevealVault is the Builder Track demo, deployed at the address on screen. BSD three-clause-clear. Drop the file in your project's dot-claude slash skills folder and your agent **stops shipping broken FHEVM oracle code**. Thanks Zama.»

**Запись:** Win+G → Start → говори → Stop → `clip6-outro.mp4`.

---

### Итог: после раздела 2 у тебя

- 6 файлов в `C:\Users\Yana\Videos\Captures\` (или куда указала Win+G)
- Переименуй их в `clip1-hook.mp4` … `clip6-outro.mp4` чтобы не запутаться
- Между клипами в монтаже добавишь короткие слайды (`slides/03-safety.png`, `slides/05-live.png`) — но это уже Раздел 4

### Запасные фразы если в записи затупила

- «Same prompt, correct contract — the skill is the difference.»
- «This is the smallest reusable embodiment of the time-locked async-decryption pattern.»
- «Sealed-bid auctions, vesting cliffs, dead-man switches — all the same primitive.»

---

## 3. Что делать если что-то сломалось

| Проблема | Решение |
|---|---|
| MetaMask тупит на Sepolia | Settings → Networks → Edit Sepolia → RPC URL: `https://ethereum-sepolia-rpc.publicnode.com` (fallback) |
| KMS callback >2 мин | Используй готовую tx на Etherscan (см. Сегмент 5) |
| Тесты `npx hardhat test` упали | `npm install` сначала. Если опять упадут — звони (но они зелёные на 4/4, не должны падать) |
| Голос с эхом в записи | Перезапиши голос сегментом, склей |
| Видео >3:00 | Режь Сегмент 5 — ускоряй места ожидания. Можно поджать Сегмент 1 если нужно. |
| Связь с Etherscan медленная | Открой страницу заранее, обнови перед записью |
| Frontend на Vercel упал | У тебя есть `slides/05-live.png` с адресом и URL — покажи его, скажи «and the live frontend at vercel-dot-app drives this end-to-end» |

---

## 4. Монтаж в CapCut (≈30 мин)

1. **Импорт:** перетащи папку `slides/` в Media. Перетащи 6 кусков screencast'а.
2. **Сборка main video track:** слайды и screencast'ы в порядке 1→6
3. **Аудио track:** voice-over одним файлом сверху. Подрежь паузы.
4. **Между сегментами:** 0.3-0.5 сек паузы для зрителя
5. **Speed-up на ожиданиях:** Сегмент 4 (тесты бегут) и Сегмент 5 (60-сек wait) — ускорь до 3-5 сек реального времени
6. **Subtle background music** (опционально, −20dB чтобы не перебивала голос)
7. **Captions:** не делаешь руками, YouTube auto-CC сделает после загрузки. Это норм.
8. **Финальная проверка:** просмотр от начала до конца, секундомер, **жёстко ≤3:00**
9. **Экспорт:** 1080p, 30fps, H.264, ~8 Мбит/с. Целевой размер ≤200 МБ (обычно ~80-120 МБ выходит).

---

## 5. Загрузка на YouTube

1. youtube.com → Create (камера значок справа сверху) → **Upload video**
2. Выбери .mp4 файл
3. **Title** (скопируй):
   ```
   fhevm-oracle — async-decryption skill for FHEVM agents (Zama S2 demo)
   ```
4. **Description** (скопируй):
   ```
   fhevm-oracle is a SKILL.md that teaches AI coding agents to write
   correct FHEVM async-decryption oracle patterns first try — Zama's
   most error-prone primitive — paired with a 220-line reference
   contract (AsyncRevealVault) that proves the pattern works on
   Sepolia today.

   Repo: https://github.com/cryptoyasenka/fhevm-oracle-skill
   Live frontend: https://fhevm-oracle-frontend.vercel.app
   Contract on Sepolia: 0x256e8948057982D483C60F7c060E3253a4d6A49b
   License: BSD-3-Clause-Clear

   The 10 anti-patterns drilled by the skill:
   AP-001 — checkSignatures not called before state writes
   AP-002 — no replay guard before write
   AP-003 — handle/tuple order mismatch
   AP-004 — missing FHE.allowThis after mutation
   AP-005 — missing FHE.allow(_, depositor) for user-decrypt
   AP-006 — assuming sync FHE.decrypt exists
   AP-007 — re-using allowTransient across transactions
   AP-008 — external calls in callback before state finalize
   AP-009 — non-idempotent triggerReveal blocks relayer retries
   AP-010 — off-by-one finality on revealAt

   Submitted to Zama Developer Program Mainnet Season 2:
   - Bounty Track (the SKILL.md)
   - Builder Track (the AsyncRevealVault demo)
   ```
5. **Audience:** «No, it's not made for kids»
6. **Visibility:** ⚠️ **UNLISTED** (НЕ Private! НЕ Public!) Private = судьи не откроют, Public = индексируется.
7. **Publish** → копируй ссылку из адресной строки или через кнопку Share

Сохрани ссылку в notepad. Она вида `https://youtu.be/XXXXXXXXXXX` или `https://www.youtube.com/watch?v=XXXXXXXXXXX`. Любой формат подойдёт.

---

## 6. Сабмит Bounty Track (the SKILL.md submission)

**Открой:** https://forms.zama.org/developer-program-mainnet-season2-bounty-track

Перед формой будет 1-2 страницы инструкций — кликай Next/Continue до самой формы.

**Заполни поля по `BOUNTY-SUBMISSION.md` в репо** (это твой источник правды). Открой файл `C:/Projects/fhevm-oracle-skill/BOUNTY-SUBMISSION.md` и копируй секциями:

| Поле формы | Откуда брать |
|---|---|
| Title | Section "### Title" → копируй текст внутри `>` |
| Short description | Section "### Short description (1–2 sentences)" |
| Long description | Section "### Long description" |
| GitHub repo URL | `https://github.com/cryptoyasenka/fhevm-oracle-skill` |
| Demo video URL | YouTube ссылка которую только что получила |
| Skill file path | `SKILL.md` |
| Difference from existing skills | Section "### How is this skill different from existing FHEVM coding skills?" |
| Wallet address | Адрес твоего кошелька для prize (тот же что в Builder) |
| License | `BSD-3-Clause-Clear` |
| How verified | Section "### How did you verify the skill works?" |

**Перед нажатием Submit:**
- [ ] Все секции заполнены
- [ ] Demo video URL вставлен и открывается на новой вкладке (проверь — судьи будут открывать)
- [ ] Wallet address правильный (это куда придёт приз — проверь дважды)

Submit → должно показать confirmation page или сообщение «спасибо, ваша заявка получена». Сохрани screenshot этой страницы.

---

## 7. Сабмит Builder Track (the AsyncRevealVault dApp)

**Открой:** https://forms.zama.org/developer-program-mainnet-season2-builder-track

Источник правды: `C:/Projects/fhevm-oracle-skill/BUILDER-SUBMISSION.md`. Все поля уже заполнены кроме video URL и wallet.

| Поле формы | Откуда брать |
|---|---|
| Title | Section "### Title" |
| One-line tagline | Section "### One-line tagline" |
| Long description | Section "### Long description" (включая Highlights for judges) |
| GitHub repo URL | `https://github.com/cryptoyasenka/fhevm-oracle-skill` |
| Sepolia deployment address | `0x256e8948057982D483C60F7c060E3253a4d6A49b` |
| Sepolia transaction (lock + reveal demo) | **УЖЕ ЗАПОЛНЕНО** в файле — `https://sepolia.etherscan.io/tx/0xbb66e334506b7f7dcfe68b3f33e30d76f5d778396556553ea0df042091209c70` |
| Demo video URL | YouTube ссылка (та же что в Bounty) |
| Frontend URL | `https://fhevm-oracle-frontend.vercel.app` |
| Stack | Section "### Stack" |
| License | `BSD-3-Clause-Clear` |
| Wallet address for prize | Тот же что в Bounty |
| Differentiation | Section "## Differentiation" |
| Hand-off note for judges | Section "## Hand-off note for judges" |

**Перед нажатием Submit:** те же проверки + дополнительно:
- [ ] Sepolia tx URL открывается и показывает Status: Success
- [ ] Sepolia deployment address открывается и показывает контракт verified=optional но bytecode виден

Submit → screenshot confirmation.

---

## 8. Финальный чек-лист (отметь когда всё сделано)

### Запись
- [ ] Голос — твой живой, не TTS
- [ ] Видео не AI-сгенерированное (обычный screencast — ОК)
- [ ] Длительность ≤3:00 (проверила секундомером)
- [ ] 1080p, 30fps, .mp4, ≤200 МБ

### YouTube
- [ ] Title скопирован точно
- [ ] Description скопирован точно
- [ ] Visibility = **Unlisted**
- [ ] Ссылка работает в инкогнито-окне (= судьи увидят)

### Bounty form
- [ ] Все поля заполнены
- [ ] Video URL вставлен и работает
- [ ] Wallet address правильный
- [ ] Submit нажат
- [ ] Confirmation screenshot сохранён

### Builder form
- [ ] Все поля заполнены
- [ ] Video URL вставлен и работает
- [ ] Sepolia tx URL открывается
- [ ] Wallet address правильный (тот же что в Bounty)
- [ ] Submit нажат
- [ ] Confirmation screenshot сохранён

### Дедлайн
- [ ] Submit'ы прошли **до** 2026-05-11 11:59 UTC (≈ 14:59 Киев)

---

## 9. Запретный список — НЕ делай

- ❌ TTS / AI-голос (ElevenLabs, Azure Speech, OpenAI tts) — disqualifying для Builder
- ❌ AI-generated video (talking head avatars, Sora/Runway) — disqualifying для Builder
- ❌ Video >3:00 (даже 3:01)
- ❌ YouTube **Private** (судьи не увидят) — только Unlisted
- ❌ Сабмитить ДО загрузки видео (нет URL → нет сабмита)
- ❌ Использовать разные wallet addresses в Bounty и Builder (используй ОДИН твой кошелёк)
- ❌ Fork/изменить контракт `0x256e8948…` после сабмита — Sepolia tx URL завязан на состояние блокчейна
- ❌ Поделиться SKILL.md / репо в Twitter ДО сабмита (если конкурс требует «original undisclosed work» — но это правило не процитировано, так что low risk; всё равно лучше после)
- ❌ Забыть про deadline. **Поставь будильник на 2026-05-11 13:00 Киев** (за 2 часа) на случай форс-мажора.

---

## 10. Если совсем плохо со временем

**Минимально приемлемое видео (если осталось <2 часа):**
- 10 сек статика `slides/01-title.png` + голос «Hi, this is fhevm-oracle — async-decryption skill for FHEVM agents»
- 30 сек screencast SKILL.md anti-patterns секции (Сегмент 2)
- 30 сек screencast AsyncRevealVault.sol fulfillReveal (Сегмент 3)
- 30 сек screencast `npx hardhat test` → 4 passing (Сегмент 4)
- 30 сек screencast Etherscan страницы готовой fulfill-tx (вместо live demo)
- 10 сек статика `slides/06-outro.png` + голос «repo at github.com/cryptoyasenka/fhevm-oracle-skill, thanks Zama»

≈2:20. Покрывает все правила: голос твой живой, видео не AI, ≤3 мин. Сабмиты в обе формы примут.

---

## Готово. Удачи 🚀

Если что-то непонятное в этом плане — скажи прямо сейчас, поправлю. Дальше я стою тихо пока ты записываешь.
