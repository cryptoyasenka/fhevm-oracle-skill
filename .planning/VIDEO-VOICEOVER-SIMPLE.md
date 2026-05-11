# Voice-over SIMPLE — fhevm-oracle (≈220 слов, ≈2:29)

> **Цель:** простой английский, короткие предложения, минимум сложных кластеров.
> Каждое предложение ≤8 слов. Темп **медленный** — 85–100 wpm.
> Голос Yana, не TTS (Zama disqualifying для AI voice).
> Жирным **акцент** (повышай голос на 1 такт).
>
> **Перед записью прочитай вслух 3 раза**, отметь карандашом места где спотыкаешься,
> там сделаешь паузу длиной 0.3 сек — это нормально.

---

## Произношение сложных слов (фонетика английскими буквами)

| Слово | Произнеси как | Заметка |
|---|---|---|
| FHEVM | **«ef eitch ee vee em»** | По буквам, не как слово |
| Sepolia | **«se-PO-lee-a»** | Ударение на PO |
| AsyncRevealVault | **«a-sink ri-VEEL vawlt»** | 3 слова, не одно |
| SDK | **«es-dee-kay»** | По буквам |
| BSD | **«bee-es-dee»** | По буквам |
| oracle | **«OR-uh-kul»** | Ударение на OR |
| signature | **«SIG-na-cher»** | «cher» как в «teacher» |
| Hardhat | **«HARD-hat»** | Два слова |
| MetaMask | **«MET-a-mask»** | Пауза в середине |
| Ethereum | избегаем — заменили на «on chain» | |
| crypto-yasenka | **«KRIP-to ya-SEN-ka»** | Дефис = микропауза |
| github | **«GIT-hab»** | Не «JEE-thab» |

---

## Структура (6 клипов, clip4 dropped)

| # | Клип | Длит. | Слов |
|---|---|---|---|
| 1 | clip1-hook-static | 22s | 36 |
| 2 | clip2-problem-static | 35s | 49 |
| 3 | clip3-contract-v2 (cropped) | 29s | 45 |
| 4 | clip5a-demo-v2 | 20s | 28 |
| 5 | clip5b-reveal-v2 | 25s | 36 |
| 6 | clip6-outro-static | 18s | 30 |
| | **Total** | **2:29** | **224** |

Средний темп: 224 слов / 149 сек ≈ **90 wpm** — медленный, удобный.

---

## Сегмент 1 (0:00–0:22) — Hook | 22s

> Видео: clip1-hook-static.mp4

«**F H E V M**.
It keeps your data secret.
But to read a value, you call the **oracle**.
AI agents make **ten mistakes** here.
We built a skill file to fix that.
Plus a live contract on **Sepolia**.»

---

## Сегмент 2 (0:22–0:57) — The problem | 35s

> Видео: clip2-problem-static.mp4

«AI agents skip the **signature check**.
So **fake data passes**.
They save the value before the replay flag.
So one proof works **twice**.
They use a sync call that does not exist on mainnet.
They miss the time check by **one second**.
The skill teaches all **ten traps**.»

---

## Сегмент 3 (0:57–1:26) — The contract | 29s

> Видео: clip3-contract-v2.mp4 (обрезан с 35s до 29s, без zoom-out на minimap)

«This is **a-sink ri-VEEL vawlt**.
The demo contract from the skill.
The signature check runs **first**.
Only small input checks come before.
The replay flag goes up **before** the value goes in.
So the same proof can not run twice.
The time check uses **greater than**, not equal.
**Four Hardhat tests pass.**»

⚠️ Последнее предложение — компенсация за выкинутый clip4 (тесты). Произнеси с акцентом.

---

## Сегмент 4 (1:26–1:46) — Lock demo | 20s

> Видео: clip5a-demo-v2.mp4

«Now the live demo on **Sepolia**.
I lock the number **sixty three**.
The **S D K** encrypts it.
I set a sixty second timer.
Lock. Sign. **Done.**»

---

## Сегмент 5 (1:46–2:11) — Reveal demo | 25s

> Видео: clip5b-reveal-v2.mp4

«Sixty seconds pass.
I trigger the reveal.
The callback checks the **signature** first.
Then sets the **replay flag**.
Then writes the value.
**Sixty three.**
The number stayed secret until the timer.»

---

## Сегмент 6 (2:11–2:29) — Outro | 18s

> Видео: clip6-outro-static.mp4

«Repo at **GIT-hab** dot com slash **KRIP-to ya-SEN-ka** slash f h e v m oracle skill.
The skill file for the **bounty**.
The contract for the **builder track**.
License **B S D** three clause clear.
Thanks Zama.»

---

## Запасные фразы (если затупила)

- «Same prompt, correct contract.»
- «The skill teaches the safe pattern.»
- «One file, ten traps, zero bugs.»

---

## Что изменилось от v1 скрипта

| Было | Стало | Причина |
|---|---|---|
| Total 3:00, 7 сегментов | Total 2:29, 6 сегментов | clip4 (Hardhat tests, 25s) выкинут из таймлайна |
| Сегмент 3 = 35s, кончался «Two hundred twenty lines. One file.» | Сегмент 3 = 29s, кончается «Four Hardhat tests pass» | clip3-v2 обрезан до 29s (без minimap zoom-out); компенсируем выкинутый clip4 одной фразой про тесты |
| Сегмент 5 = 45s одним блоком | Сегмент 5a (lock, 20s) + 5b (reveal, 25s) разделены | Соответствует двум клипам clip5a-v2 + clip5b-v2 |
