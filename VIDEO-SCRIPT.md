# 3-Minute Demo Video Script — fhevm-oracle skill

**Target:** Zama Developer Program Mainnet S2 — Bounty Track judging.
**Length:** 2:45–3:00. Hard cap 3:00.
**Tooling:** OBS Studio, screen + mic, no webcam needed.
**File output:** `fhevm-oracle-demo.mp4`, ≤200 MB, 1080p.

---

## Pre-recording checklist

- [ ] `npm install` ran clean
- [ ] `npx hardhat compile` succeeds (FHECounter + AsyncRevealVault)
- [ ] `npx hardhat test` passes all 4 cases
- [ ] Two browser windows ready:
  - **A** — Claude Code WITHOUT the skill (fresh project, just `package.json`)
  - **B** — Claude Code WITH the skill (`SKILL.md` already in cwd, picked up automatically)
- [ ] Both terminals zoomed to 16-18 pt font
- [ ] Mic test, no background music

---

## Segment 1 — Hook (0:00–0:20)

**On screen:** Title card slide.

> "FHEVM lets you compute on encrypted data on Ethereum. But the moment your contract needs to *reveal* a result, you hit the async decryption oracle — and that's where AI coding agents reliably ship broken code. I built a SKILL.md that fixes that."

---

## Segment 2 — The 5 failure modes (0:20–0:50)

**On screen:** SKILL.md scrolling slowly, anti-patterns AP-001 through AP-010 visible.

> "Without context, an agent will skip `FHE.checkSignatures` — letting anyone fake a decryption. It'll mismatch handle order. It'll forget to consume the request guard before the cleartext write — replay. It'll assume sync decrypt that doesn't exist on mainnet. Or it'll trigger reveal at exactly `block.timestamp == revealAt` — off by one. This skill drills all ten as muscle memory."

---

## Segment 3 — Live A/B (0:50–2:20) — THE CRITICAL SEGMENT

### Window A — agent WITHOUT the skill (0:50–1:35)

> "Same prompt, same agent, same model. Window A has no skill loaded."

Type into Claude Code (window A):

> "Write a Solidity contract called TimeVault that locks an encrypted uint64 amount and an encrypted uint256 secret with a release timestamp. After the timestamp anyone can trigger an async KMS decryption that writes the cleartext into storage."

**Show the generated contract.** Pause on the callback function. Highlight in red:

- No `FHE.checkSignatures` call (AP-001) — fake decryption attack possible
- Cleartext write happens before request consume (AP-002) — replay
- Likely uses `>=` or `==` on `revealAt` (AP-010) — off-by-one
- Likely no `FHE.allowThis` after lock (AP-004)

> "Three signed-off vulnerabilities in 60 seconds. Ship this and the auditor sends it straight back."

### Window B — agent WITH the skill (1:35–2:20)

Type the same prompt into window B. Claude Code auto-loads `SKILL.md`.

**Show the generated contract** — `AsyncRevealVault.sol` from this repo (or close to it).

Highlight in green:

- `FHE.checkSignatures(requestID, signatures)` is the FIRST line of `fulfillReveal`
- `delete requestToVault[requestID]` and `outstandingRequestID = type(uint256).max` consumed BEFORE state writes
- `block.timestamp <= v.revealAt` revert with `RevealTooEarly`
- `FHE.allowThis(amount)` + `FHE.allow(amount, msg.sender)` after every state mutation

> "Same prompt. Correct contract. The skill is the difference."

---

## Segment 4 — Tests pass + deploy (2:20–2:45)

**Terminal:** `npx hardhat test`

> "Four mock-mode tests cover the canonical happy path and three of the most common failure modes. They drill the same anti-patterns the skill enumerates — so a contract written from the skill passes them by construction."

Show passing output.

Optional: `npm run deploy:sepolia` — show the deployed Sepolia address.

---

## Segment 5 — Where to find it (2:45–3:00)

**On screen:** GitHub repo URL + the SKILL.md filename + license card.

> "Repo at github.com/cryptoyasenka/fhevm-oracle-skill. SKILL.md is the bounty deliverable. AsyncRevealVault.sol is the Builder Track demo. BSD-3-Clause-Clear, same license as @fhevm/solidity. Drop the file in your project's `.claude/skills/` folder and your agent stops shipping broken FHEVM oracle code. Thanks Zama."

---

## Recording tips

- Pre-record the A/B agent completions to disk so the live demo doesn't depend on network speed. Use Premiere/DaVinci to splice the typed prompt → cached response.
- Caption every red/green callout with on-screen text — judges may watch muted.
- Save twice: full 3-min cut + a 60-second teaser cut for the X post.
- Upload to YouTube unlisted (NOT private — Zama needs to view it). Drop the URL into BOUNTY-SUBMISSION.md.
