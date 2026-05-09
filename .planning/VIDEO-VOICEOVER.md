# Voice-over — fhevm-oracle demo (~360 слов, ~2:50 при темпе 130 wpm)

> Пиши под одно дыхание, спокойный темп, тон — как объясняешь коллеге. Дубль одним заходом, паузы между сегментами оставит монтаж. Ударные слова **жирным** — на них акцент.

---

## Сегмент 1 (0:00–0:20) — Hook

FHEVM lets you compute on **encrypted data** on Ethereum. But the moment your contract needs to **reveal a result**, you hit the async decryption oracle — and that's where AI coding agents consistently ship **broken code**. fhevm-oracle is a SKILL.md that fixes that, plus a reference contract that proves the pattern works on Sepolia today.

---

## Сегмент 2 (0:20–0:55) — The five failure modes

Without context, an agent will skip checkSignatures and let anyone fake a decryption. It will mismatch handle order. It will write cleartext **before consuming the request guard**, opening replay attacks. It will assume a sync decrypt that doesn't exist on mainnet. Or it will trigger reveal at exactly block-dot-timestamp equals revealAt — off by one. The skill enumerates **all ten anti-patterns** as muscle memory.

---

## Сегмент 3 (0:55–1:30) — What the skill produces

This is AsyncRevealVault — the reference contract written from the skill. Notice: checkSignatures is the **very first line** of the callback. The request guard is deleted and the outstanding request reset **before any cleartext write**. The timestamp check is a **strict greater-than**. ACL discipline is preserved across every state mutation. Two hundred and twenty lines, one file.

---

## Сегмент 4 (1:30–2:00) — Tests

Four Hardhat mock-mode tests drill the same anti-patterns the skill enumerates: signature absence, request guard not consumed, off-by-one finality, ACL leak. A contract written from the skill **passes them by construction**.

---

## Сегмент 5 (2:00–2:45) — Live on-chain demo

Now the live contract on Sepolia. I'm encrypting a number — **sixty-three**. The relayer SDK takes my plaintext, produces a ciphertext handle plus a zero-knowledge proof. Reveal in sixty seconds. The Lock transaction stores the encrypted handle and binds the ACL to me and the contract.

Sixty seconds pass.

I trigger reveal. The vault submits the ciphertext to the KMS oracle in a single requestDecryption call. The KMS callback verifies signatures, consumes the guard, then writes the cleartext. **Sixty-three.** The number was encrypted on chain until the timer expired.

---

## Сегмент 6 (2:45–3:00) — Outro

Repo at github-dot-com slash cryptoyasenka slash fhevm-oracle-skill. SKILL-dot-MD is the bounty deliverable. AsyncRevealVault is the Builder Track demo, deployed at the address on screen. BSD three-clause-clear, same license as fhevm-solidity. Drop the file in your project's dot-claude slash skills folder and your agent **stops shipping broken FHEVM oracle code**. Thanks Zama.

---

## Запасные фразы (если затупила в записи)

- "Same prompt, correct contract — the skill is the difference."
- "This is the smallest reusable embodiment of the time-locked async-decryption pattern."
- "Sealed-bid auctions, vesting cliffs, dead-man switches — all the same primitive."
