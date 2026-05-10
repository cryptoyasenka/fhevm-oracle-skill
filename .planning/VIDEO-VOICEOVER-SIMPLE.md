# Voice-over SIMPLE — fhevm-oracle (≈256 слов, ≈2:50 при темпе 90 wpm)

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

## Сегмент 1 (0:00–0:22) — Hook | 36 слов

> Картинка: `slides/01-title.png` на весь экран

«**F H E V M**.
It keeps your data secret.
But to read a value, you call the **oracle**.
AI agents make **ten mistakes** here.
We built a skill file to fix that.
Plus a live contract on **Sepolia**.»

**Темп:** 36 слов / 22 сек = 98 wpm. Делай паузы 0.3 сек после каждой точки.

---

## Сегмент 2 (0:22–0:57) — The problem | 49 слов

> Картинка: `slides/02-anti-patterns.png`
> (или scroll по SKILL.md в VS Code — выбор по плану)

«AI agents skip the **signature check**.
So **fake data passes**.
They save the value before the replay flag.
So one proof works **twice**.
They use a sync call that does not exist on mainnet.
They miss the time check by **one second**.
The skill teaches all **ten traps**.»

**Темп:** 49 слов / 35 сек = 84 wpm. Это медленный темп — ок, для тебя комфортно.

---

## Сегмент 3 (0:57–1:32) — The contract | 54 слова

> Картинка: VS Code на `contracts/AsyncRevealVault.sol`, строка 135

«This is **a-sink ri-VEEL vawlt**.
The demo contract from the skill.
Look here.
The signature check runs **first**.
Only small input checks come before.
The replay flag goes up **before** the value goes in.
So the same proof can not run twice.
The time check uses **greater than**, not equal.
Two hundred twenty lines. One file.»

**Темп:** 54 слова / 35 сек = 93 wpm.

**Что показать мышкой синхронно:**
- На «signature check runs first» → выдели строку 152 `FHE.checkSignatures(...)`
- На «replay flag goes up before» → скролл вниз к `v.revealed = true;` (~155)
- На «greater than not equal» → `Ctrl+G` → 106 → выдели `if (block.timestamp <= v.revealAt)`
- На «two hundred twenty lines» → `Ctrl+Shift+−` 3 раза (отдалить, видно весь файл)

---

## Сегмент 4 (1:32–1:57) — Tests | 33 слова

> Терминал: `npx hardhat test` запущен

«Four Hardhat tests run in mock mode.
They cover the same traps.
**Missing signature**.
**Replay attack**.
**Time off by one**.
And the happy path.
A contract built from the skill **passes them all**.»

**Темп:** 33 слова / 25 сек = 79 wpm. Очень медленно — у тебя есть запас.

⚠️ В CapCut потом ускорь середину клипа в 5×, чтобы тесты «пробежали» за 5 сек.

---

## Сегмент 5 (1:57–2:42) — Live demo | 61 слово

> Frontend: https://fhevm-oracle-frontend.vercel.app

«Now the live demo on **Sepolia**.
I lock the number **sixty three**.
The **S D K** encrypts it.
I set a sixty second timer.
Lock. Sign. Done.

(пауза, ждёшь 60 сек — в монтаже ускоришь)

Sixty seconds pass.
I trigger the reveal.
Now I call fulfill.
The callback checks the signature.
Sets the replay flag.
Then writes the value.
**Sixty three**.
The number stayed secret until the timer.»

**Темп:** 61 слово / 45 сек = 81 wpm.

⚠️ Если KMS callback залип >2 мин — используй готовую tx (см. CURRENT.md антипаника блок).

---

## Сегмент 6 (2:42–3:00) — Outro | 30 слов

> Картинка: `slides/06-outro.png`

«Repo at **GIT-hab** dot com slash **KRIP-to ya-SEN-ka** slash f h e v m oracle skill.
The skill file for the **bounty**.
The contract for the **builder track**.
License **B S D** three clause clear.
Thanks Zama.»

**Темп:** 30 слов / 18 сек = 100 wpm.

---

## Итог по таймингу

| # | Длительность | Слов | wpm |
|---|---|---|---|
| 1 | 22s | 36 | 98 |
| 2 | 35s | 49 | 84 |
| 3 | 35s | 54 | 93 |
| 4 | 25s | 33 | 79 |
| 5 | 45s | 61 | 81 |
| 6 | 18s | 30 | 100 |
| **Total** | **3:00** | **263** | **88 avg** |

Запас: при темпе 88 wpm реальная длина = 263/88×60 = **179 сек = 2:59**.
Если читаешь медленнее — режем сегмент 5 (paused waits можно ужать в CapCut).

---

## Запасные фразы (если затупила)

- «Same prompt, correct contract.»
- «The skill teaches the safe pattern.»
- «One file, ten traps, zero bugs.»

---

## Чем отличается от исходного `VIDEO-VOICEOVER.md`

| Было | Стало | Причина |
|---|---|---|
| «consistently ship broken code» | «make ten mistakes» | /kənˈsɪstəntli/ = 4 слога, кластеры |
| «mismatch handle order against the abi-decode tuple» | удалено | непроизносимо |
| «before flipping the replay guard» | «before the replay flag» | /flɪpɪŋ ðə/ — три /ð/ подряд |
| «assume a sync decrypt that doesn't exist on mainnet» | «use a sync call that does not exist on mainnet» | проще, короче |
| «enumerates all ten anti-patterns as muscle memory» | «teaches all ten traps» | /ɪˈnjuːməreɪts/ катастрофа |
| «cheap input-validity reverts that touch no cleartext» | «small input checks come before» | в 3 раза короче |
| «ACL discipline is preserved across every state mutation» | удалено | теряет смысл при упрощении |
| «strict greater-than» | «greater than, not equal» | /str/+/kt/ кластер |
| «relayer SDK takes my plaintext, produces a ciphertext handle plus a zero-knowledge proof» | «the S D K encrypts it» | вся фраза в 4 слова |
| «The vault flags both ciphertexts as publicly decryptable» | «I trigger the reveal» | непроизносимо |
| «BSD three-clause-clear, same license as fhevm-solidity» | «License B S D three clause clear» | убрали половину |
