# Voice-over SIMPLE — fhevm-oracle (≈260 слов, ≈2:54)

> **Цель:** простой английский, короткие предложения, минимум сложных кластеров.
> Каждое предложение ≤8 слов. Темп **медленный** — 85–100 wpm.
> Голос Yana, не TTS (Zama disqualifying для AI voice).
> Жирным **акцент** (повышай голос на 1 такт).

---

## Произношение сложных слов

| Слово | Произнеси как | Заметка |
|---|---|---|
| FHEVM | **«ef eitch ee vee em»** | По буквам |
| Sepolia | **«se-PO-lee-a»** | Ударение на PO |
| AsyncRevealVault | **«a-sink ri-VEEL vawlt»** | 3 слова |
| SDK | **«es-dee-kay»** | По буквам |
| BSD | **«bee-es-dee»** | По буквам |
| oracle | **«OR-uh-kul»** | Ударение на OR |
| signature | **«SIG-na-cher»** | «cher» как в teacher |
| Hardhat | **«HARD-hat»** | Два слова |
| crypto-yasenka | **«KRIP-to ya-SEN-ka»** | Дефис = микропауза |
| github | **«GIT-hab»** | Не «JEE-thab» |

---

## Структура (7 клипов = 7 cue-cards)

| # | Cue card | Видео | Длит. | Слов |
|---|---|---|---|---|
| 1 | seg1-hook-v2 | clip1-hook-static | 22s | 36 |
| 2 | seg2-problem-v2 | clip2-problem-static | 35s | 49 |
| 3 | seg3-contract-v2 | clip3-contract-v2 (cropped) | 29s | 46 |
| 4 | seg4-tests-v2 | clip4-tests-static | 25s | 30 |
| 5 | seg5-demo-lock-v2 | clip5a-demo-v2 | 20s | 28 |
| 6 | seg6-demo-reveal-v2 | clip5b-reveal-v2 | 25s | 36 |
| 7 | seg7-outro-v2 | clip6-outro-static | 18s | 30 |
| | | **Total** | **2:54** | **255** |

---

## Сегмент 1 (0:00–0:22) — Hook | 22s | clip1 + seg1

«**F H E V M**.
It keeps your data secret.
But to read a value, you call the **oracle**.
AI agents make **ten mistakes** here.
We built a skill file to fix that.
Plus a live contract on **Sepolia**.»

---

## Сегмент 2 (0:22–0:57) — Problem | 35s | clip2 + seg2

«AI agents skip the **signature check**.
So **fake data passes**.
They save the value before the replay flag.
So one proof works **twice**.
They use a sync call that does not exist on mainnet.
They miss the time check by **one second**.
The skill teaches all **ten traps**.»

---

## Сегмент 3 (0:57–1:26) — Contract | 29s | clip3-v2 + seg3

«This is **a-sink ri-VEEL vawlt**.
The demo contract from the skill.
The signature check runs **first**.
Only small input checks come before.
The replay flag goes up **before** the value goes in.
So the same proof can not run twice.
The time check uses **greater than**, not equal.»

---

## Сегмент 4 (1:26–1:51) — Tests | 25s | clip4 + seg4

«Four Hardhat tests run in mock mode.
They cover the same traps.
**Missing** signature.
**Replay** attack.
**Time** off by one.
And the happy path.
The skill contract **passes them all**.»

---

## Сегмент 5 (1:51–2:11) — Live demo: LOCK | 20s | clip5a-v2 + seg5

«Now the live demo on **Sepolia**.
I lock the number **sixty three**.
The **S D K** encrypts it.
I set a sixty second timer.
Lock. Sign. **Done.**»

---

## Сегмент 6 (2:11–2:36) — Live demo: REVEAL | 25s | clip5b-v2 + seg6

«Sixty seconds pass.
I trigger the reveal.
The callback checks the **signature** first.
Then sets the **replay flag**.
Then writes the value.
**Sixty three.**
The number stayed secret until the timer.»

---

## Сегмент 7 (2:36–2:54) — Outro | 18s | clip6 + seg7

«Repo at **GIT-hab** dot com slash **KRIP-to ya-SEN-ka** slash f h e v m oracle skill.
The skill file for the **bounty**.
The contract for the **builder track**.
License **B S D** three clause clear.
Thanks Zama.»

---

## Запасные фразы

- «Same prompt, correct contract.»
- «The skill teaches the safe pattern.»
- «One file, ten traps, zero bugs.»
