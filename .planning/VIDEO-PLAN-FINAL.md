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

## 1. ДО записи (15-30 мин подготовки)

### 1.1 Окружение

Открой эти 5 окон, сложи в Alt+Tab порядок 1→2→3→4→5:

- **W1 — VS Code**, открыт `C:/Projects/fhevm-oracle-skill/SKILL.md`
  - Скролл на секцию `## The 10 anti-patterns (drilled with fix templates)` (~строка 184)
  - Шрифт ≥16pt, тёмная тема, side panel закрыт
- **W2 — VS Code (новое окно или таб)**, открыт `C:/Projects/fhevm-oracle-skill/contracts/AsyncRevealVault.sol`
  - Курсор на функции `fulfillReveal` (~строка 135)
  - Шрифт ≥16pt
- **W3 — PowerShell в проекте**:
  ```
  cd C:/Projects/fhevm-oracle-skill
  cls
  ```
  - Шрифт ≥18pt
  - Готов запустить `npx hardhat test`
- **W4 — Браузер вкладка 1**: https://fhevm-oracle-frontend.vercel.app
  - MetaMask установлен и УЖЕ подключён к Sepolia
  - В кошельке ≥0.05 SepETH (если меньше — добери из faucet `https://sepoliafaucet.com`)
  - **Перед записью**: нажми × Hide на каждой из 4 карточек id=1..4 чтобы список был чистым (вернуть их обратно нельзя без пересоздания, но это ОК — для видео тебе они не нужны)
- **W5 — Браузер вкладка 2**: https://sepolia.etherscan.io/address/0x256e8948057982D483C60F7c060E3253a4d6A49b

### 1.2 Микрофон (для real-person правила)

- **Микрофон**: записывай через OBS Studio, CapCut Desktop, или просто Win+G GameBar. Проверка: скажи «раз-два-три», переслушай — нет фона, нет эха, не клипует.
- **Веб-камера НЕ нужна.** Zama не требует показа лица. «Real-person pitch» = живой голос + не AI-видео. Screencast + твой голос полностью соответствует правилу.

### 1.3 Тех настройки записи

- Разрешение записи: **1920×1080** (1080p)
- Frame rate: **30 fps**
- Битрейт: 8000 kbps
- Курсор: включи подсветку клика если есть в записывалке (помогает зрителю)

### 1.4 Прорепетируй ОДИН раз без записи

- Пройди все 6 сегментов с текстом (см. ниже)
- Засеки время секундомером на телефоне
- Если выходит >3:00 — режь Сегмент 5 (live demo) в монтаже потом, не сейчас
- Если выходит <2:30 — добавь паузы между сегментами

---

## 2. Запись (≈30-45 мин с дублями)

**Стратегия:** voice-over записываешь **ОДНИМ непрерывным дублем** под весь скрипт. Screencast/слайды записываешь отдельно сегментами. Совмещаешь в монтаже. Если запутаешься — скажи вслух «РЕЗАТЬ» и продолжи фразу заново, в монтаже легко вырежешь.

Жирным **слова под акцент** (повышай голос).

---

### 🎬 Сегмент 1 — Hook (0:00–0:20)

**Видео:** статика `slides/01-title.png` все 20 сек. Голос звучит поверх. Этого достаточно: «real-person» = живой голос + не-AI видео.

**Voice-over (читай ровно, ~50 слов = 22 сек):**

> «FHEVM lets you compute on **encrypted data** on Ethereum. But the moment your contract needs to **reveal a result**, you hit the async decryption oracle — and that's where AI coding agents consistently ship **broken code**. fhevm-oracle is a SKILL.md that fixes that, plus a reference contract that proves the pattern works on Sepolia today.»

---

### 🎬 Сегмент 2 — Проблема (0:20–0:55) — статика или скролл

**Видео (выбери один из двух):**
- **A (быстрый):** статика `slides/02-anti-patterns.png` 35 сек
- **B (живее):** screencast W1 — медленный скролл по секции AP-001…AP-010 в SKILL.md, мышкой выделяешь заголовки пока их называешь

**Voice-over (~75 слов = 35 сек):**

> «Without context, an agent will skip checkSignatures and let anyone fake a decryption. It will mismatch handle order against the abi-decode tuple. It will write cleartext **before flipping the replay guard**, so the same KMS proof can be re-submitted. It will assume a sync decrypt that doesn't exist on mainnet. Or it will trigger reveal at exactly block-dot-timestamp equals revealAt — off by one. The skill enumerates **all ten anti-patterns** as muscle memory.»

---

### 🎬 Сегмент 3 — Что генерит агент со скиллом (0:55–1:30) — screencast W2 — **САМЫЙ ВАЖНЫЙ**

**Видео:** screencast окна W2 (`AsyncRevealVault.sol`). Манипуляции мышью + клавиатурой по таймлайну voice-over:

| В этой фразе voice-over | Делаешь на экране |
|---|---|
| «checkSignatures runs **before any state write** in the callback» | Скролл к `fulfillReveal` строка ~135. Выделяй мышью строку 152 `FHE.checkSignatures(handles, abiEncodedCleartexts, decryptionProof);`. Опционально: накладываешь callout `slides/07-callout-checksig.png` в правый верхний угол на 2-3 сек. |
| «only lines above it are cheap input-validity reverts that touch no cleartext» | Скролл вверх на 3-5 строк, покажи 3 revert строки выше checkSignatures (`if (v.depositor == address(0)) revert ...`, `if (v.revealed) revert ...`, `if (block.timestamp <= v.revealAt) revert ...`) |
| «replay flag flips to true **before** the cleartext lands» | Скролл к строке 155 `v.revealed = true;`. Выдели её. Опционально callout `slides/08-callout-replay.png`. |
| «strict greater-than» | Скролл вверх к `triggerReveal` ~строка 106, выдели `if (block.timestamp <= v.revealAt) revert RevealTooEarly();`. Опционально callout `slides/09-callout-finality.png`. |
| «ACL discipline preserved» | Скролл к `lock` ~строка 67, выдели блок 4 строк `FHE.allowThis(...); FHE.allow(...);` |
| «Two hundred and twenty lines, one file» | Зум-аут (Ctrl+Shift+−) чтобы был виден весь файл целиком |

**Voice-over (~85 слов = 35 сек):**

> «This is AsyncRevealVault — the reference contract written from the skill. Notice: checkSignatures runs **before any state write** in the callback — the only lines above it are cheap input-validity reverts that touch no cleartext. The replay flag flips to true **before** the cleartext lands — re-submitting the same KMS proof reverts at AlreadyRevealed. The timestamp check is a **strict greater-than**. ACL discipline is preserved across every state mutation. Two hundred and twenty lines, one file.»

---

### 🎬 Сегмент 4 — Тесты (1:30–2:00) — терминал W3

**Видео:** 5 сек статика `slides/04-tests.png`, потом screencast терминала W3.

**Действия на экране:**
1. На W3 набери `npx hardhat test` и нажми Enter
2. Жди ~25 сек. **В монтаже** ускорь этот участок до 3-5 сек.
3. Когда появится `4 passing` — подержи кадр 3 сек. Это финальный мани-шот этого сегмента.

**Voice-over (~50 слов = 25 сек):**

> «Four Hardhat mock-mode tests drill the same anti-patterns the skill enumerates: signature absence, replay-after-success, off-by-one finality, and the canonical happy path. A contract written from the skill **passes them by construction**.»

---

### 🎬 Сегмент 5 — Live on-chain demo (2:00–2:45) — frontend W4 — **САМЫЙ РИСКОВЫЙ**

**Видео:** screencast W4 (https://fhevm-oracle-frontend.vercel.app).

**Действия на экране:**

1. **Подключи кошелёк** (если не подключён) — кликни Connect, подтверди в MetaMask. **На запись это не идёт** (либо вырезаем, либо подключаешь до старта записи).
2. **Введи Amount** = `63` (это число произнесёшь в voice-over)
3. **Введи Secret** = `42`
4. **Reveal time** = now+60sec (UI должен подставить, или ставь руками)
5. **Нажми Lock** → подтверди в MetaMask → жди зелёную галочку (~10-15 сек)
6. **Жди 60 секунд.** В монтаже ускорь этот участок до 3-5 сек («время идёт…»).
7. **Нажми Trigger reveal** → подтверди → жди подтверждения
8. **Нажми Fulfill** → подтверди → на странице появится cleartext `63` (amount) + `42` (secret)
9. **Переключись на W5** (Etherscan вкладка) — покажи в списке транзакций строки `triggerReveal` + `fulfillReveal`

**Voice-over (~95 слов = 45 сек):**

> «Now the live contract on Sepolia. I'm encrypting a number — **sixty-three**. The relayer SDK takes my plaintext, produces a ciphertext handle plus a zero-knowledge proof. Reveal in sixty seconds. The Lock transaction stores the encrypted handle and binds the ACL to me and the contract.
>
> Sixty seconds pass.
>
> I trigger reveal. The vault flags both ciphertexts as publicly decryptable. The relayer fetches the KMS-signed cleartext and calls fulfillReveal. The callback verifies signatures, flips the replay guard, then writes the cleartext. **Sixty-three.** The number was encrypted on chain until the timer expired.»

⚠️ **Если KMS callback залип (>2 мин на fulfillment):**
- У тебя есть готовая успешная транзакция на Etherscan (vault id=4, fulfilled 11:42:48 UTC сегодня). URL уже вписан в `BUILDER-SUBMISSION.md`.
- В монтаже: вместо живого fulfill вставь screenshot Etherscan-страницы той транзакции, озвучь «and so the result lands on chain» — судья поймёт.
- Или склей с записанным заранее «эталонным» reveal с одного из прошлых тестов.

---

### 🎬 Сегмент 6 — Outro (2:45–3:00) — слайд

**Видео:** статика `slides/06-outro.png` 15 сек.

**Voice-over (~50 слов = 18 сек):**

> «Repo at github-dot-com slash cryptoyasenka slash fhevm-oracle-skill. SKILL-dot-MD is the bounty deliverable. AsyncRevealVault is the Builder Track demo, deployed at the address on screen. BSD three-clause-clear, same license as fhevm-solidity. Drop the file in your project's dot-claude slash skills folder and your agent **stops shipping broken FHEVM oracle code**. Thanks Zama.»

---

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
