# Демо-видео — пошаговая инструкция (на день записи 2026-05-10)

**Длительность:** 2:30–3:00 (жёсткий потолок 3:00)
**Формат:** screencast + voice-over (без вебкамеры), 1080p, mp4 ≤ 200 МБ
**Платформа:** YouTube **unlisted** (НЕ private — судьи не откроют)

> ⚠ Важно: упрощённая версия исходного скрипта. Никаких A/B сравнений двух Claude Code в реальном времени — слишком рискованно записывать вживую. Вместо этого делаем 6 чистых сегментов с заранее открытыми вкладками.

---

## Что подготовить до записи (15 мин)

**1. Окна (по порядку Alt+Tab):**
- **W1** — VS Code, открыт `SKILL.md`, проскроллен на секцию `## Anti-patterns (AP-001 … AP-010)`. Шрифт 16+pt, тёмная тема. Боковую панель закрыть.
- **W2** — VS Code, открыт `contracts/AsyncRevealVault.sol`. Курсор на функции `fulfillReveal`. Шрифт 16+pt.
- **W3** — Терминал в папке проекта, готов к `npx hardhat test`. Шрифт 18+pt.
- **W4** — Браузер с https://fhevm-oracle-frontend.vercel.app, MetaMask установлен, Sepolia активна, на коше есть >0.05 SepETH.
- **W5** — Браузер второй вкладкой: https://sepolia.etherscan.io/address/0x256e8948057982D483C60F7c060E3253a4d6A49b

**2. Тех:**
- OBS Studio (или встроенный ScreenRecorder Win+G + Audacity для звука + потом склеить в Clipchamp/DaVinci)
- Микрофон проверь: говори 10 секунд, переслушай — никакого фона, нет эха
- Скорость записи 30 fps, битрейт 8000 kbps хватит

**3. Прорепетируй один раз без записи** — пройди все 6 сегментов с текстом. Засеки время. Если выходит >3:00 — режь на сегменте 5.

---

## Сегмент 1 — Hook (0:00–0:20)

**Экран:** title card. Можно сделать слайд в PowerPoint / Canva: чёрный фон, текст:

```
fhevm-oracle
async-decryption skill for FHEVM agents

Zama Developer Program — Mainnet S2
Bounty + Builder Track
```

**Голос:** см. `VIDEO-VOICEOVER.md` сегмент 1.

---

## Сегмент 2 — Проблема (0:20–0:55)

**Экран:** окно W1 (SKILL.md), медленно скроллишь секцию anti-patterns AP-001 → AP-010.

**Что подсветить:**
- Можно мышкой выделять заголовки AP-001, AP-002, AP-008, AP-010 пока их называешь
- Не задерживайся надолго, цель — показать что таких anti-patterns *много*

**Голос:** см. `VIDEO-VOICEOVER.md` сегмент 2.

---

## Сегмент 3 — Что генерит агент со скиллом (0:55–1:30)

**Экран:** окно W2 (`AsyncRevealVault.sol`).

**Что показать (скроллом или подсветкой):**
1. Функция `fulfillReveal` → строка `FHE.checkSignatures(requestID, signatures);` — это **первая строка** callback'а
2. Дальше — `delete requestToVault[requestID];` и сброс `outstandingRequestID = type(uint256).max;` ДО любых записей cleartext
3. Функция `triggerReveal` → строка `if (block.timestamp <= v.revealAt) revert RevealTooEarly();` — строгое `<=`, не `<`
4. После `lock` — `FHE.allowThis(amount); FHE.allow(amount, msg.sender);` — ACL discipline

**Голос:** см. `VIDEO-VOICEOVER.md` сегмент 3.

---

## Сегмент 4 — Тесты (1:30–2:00)

**Экран:** окно W3 (терминал).

**Действия:**
1. Очисти терминал (`cls`)
2. Запусти `npx hardhat test`
3. Дождись вывода `4 passing`
4. Подержи финальный экран ~3 секунды

**Подсказка:** если запуск тестов идёт >25 сек — запиши его отдельно, потом ускорь в 2-3x в монтаже (только tests-running участок, не финальный pass).

**Голос:** см. `VIDEO-VOICEOVER.md` сегмент 4.

---

## Сегмент 5 — On-chain демо на live фронте (2:00–2:45) — **КРИТИЧНЫЙ**

**Экран:** окно W4 (https://fhevm-oracle-frontend.vercel.app).

**Действия (репетируй ДО записи!):**
1. **Connect wallet** — кликни кнопку, подтверди в MetaMask
2. **Введи число** — например `63` в поле amount
3. **Reveal time** — поставь now+60sec (или `+1 minute`, как реализовано в UI)
4. **Click Lock** — подтверди транзакцию в MetaMask, дождись зелёной галочки
5. **Подожди 60 секунд** (на этом моменте можно ускорить в монтаже до 3-5 сек)
6. **Click Trigger reveal** — подтверди транзакцию
7. **Дождись Fulfill** — KMS callback, на странице появится cleartext `63`
8. **Переключись на W5** (Etherscan) — покажи tx hash контракта, особенно `triggerReveal` и `fulfillReveal` транзакции

**Если KMS callback задерживается** (>2 мин на ожидание fulfillment):
- Запиши заранее «эталонную» сессию вечером, используй её как backup в монтаже
- Или: смонтируй разрыв («время идёт…») и склей с уже готовым reveal с раннего теста

**Голос:** см. `VIDEO-VOICEOVER.md` сегмент 5.

---

## Сегмент 6 — Outro (2:45–3:00)

**Экран:** title card с тремя строками:

```
github.com/cryptoyasenka/fhevm-oracle-skill

AsyncRevealVault on Sepolia:
0x256e8948057982D483C60F7c060E3253a4d6A49b

License: BSD-3-Clause-Clear
```

**Голос:** см. `VIDEO-VOICEOVER.md` сегмент 6.

---

## Монтаж (30 мин)

1. Импорт всех 6 кусков в Clipchamp / DaVinci Resolve / iMovie
2. Положи звуковую дорожку поверх (запиши voice-over одним дублем по `VIDEO-VOICEOVER.md`, потом порезка)
3. Пауза 0.5 сек между сегментами — чтобы зритель догнал
4. Subtle background music по желанию (если используешь — громкость −20dB чтобы не глушить голос)
5. Captions через YouTube auto-CC после загрузки (Zama может смотреть с выключенным звуком)

---

## Загрузка на YouTube

1. youtube.com → Create → Upload video
2. **Visibility: Unlisted** (не Private!)
3. Title: `fhevm-oracle — async-decryption skill for FHEVM agents (Zama S2 demo)`
4. Description: ссылка на репо + одно предложение что это
5. Скопируй ссылку → впиши в `BOUNTY-SUBMISSION.md` И `BUILDER-SUBMISSION.md` поле "Demo video URL"

---

## Edge cases

- **Если запутаешься в записи** — не переписывай весь дубль, просто пометь "[РЕЗАТЬ]" вслух и продолжай. В монтаже легко вырежешь.
- **Если frontend упадёт** в момент записи — всегда есть screenshots-fallback, скажи в voice-over "и так выглядит результат" и покажи статичную картинку
- **Если MetaMask тупит на Sepolia** — у тебя в кош добавлен фоллбек RPC `https://ethereum-sepolia-rpc.publicnode.com`? Если нет — добавь до записи через Settings → Networks → Edit
