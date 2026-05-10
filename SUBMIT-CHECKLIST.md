# Submission Checklist — Yana

**Drop-dead deadline:** 2026-05-10 23:59 AOE = **2026-05-11 11:59 UTC**.
That's 50 hours from this snapshot. Plan for 24h slack — finish by 2026-05-10 12:00 UTC if possible.

---

## Phase 0 — sanity (15 min, do FIRST when you wake up)

```bash
cd C:/Projects/fhevm-oracle-skill
npm install
npx hardhat compile
npx hardhat test
```

- [ ] `npm install` succeeds — if it complains about peer deps, add `--legacy-peer-deps`
- [ ] `npx hardhat compile` produces `artifacts/contracts/AsyncRevealVault.sol/AsyncRevealVault.json`
- [ ] `npx hardhat test` — all 4 cases pass

If any of these break, stop and ping me before continuing. The submission is worthless if the demo doesn't compile.

---

## Phase 1 — push to GitHub (15 min)

```bash
gh auth status                                          # sanity
gh repo create cryptoyasenka/fhevm-oracle-skill --public --source=. --remote=origin --push
```

- [ ] Repo public at `https://github.com/cryptoyasenka/fhevm-oracle-skill`
- [ ] All commits visible (you should see ~6: bootstrap → SKILL.md → AsyncRevealVault → tests → deploy → submission docs)
- [ ] README renders correctly on the GitHub frontpage

---

## Phase 2 — Sepolia deploy (30 min, Builder Track only)

```bash
npx hardhat vars set MNEMONIC                           # paste your dev mnemonic
npx hardhat vars set INFURA_API_KEY                     # paste your Infura key
npm run deploy:sepolia
```

- [ ] Output prints `AsyncRevealVault : 0x...` — copy that address
- [ ] Verify on Sepolia Etherscan (optional but nice): `npx hardhat verify --network sepolia 0x<address>`
- [ ] Paste the address into `BUILDER-SUBMISSION.md` → "Sepolia deployment address"
- [ ] Optional bonus: do one `lock()` + wait + `triggerReveal()` on Sepolia, paste the tx hash into `BUILDER-SUBMISSION.md` → "Sepolia transaction"

If `npm run deploy:sepolia` fails on gas, top up the deployer address from a Sepolia faucet before retrying.

---

## Phase 3 — record the 3-min demo (60–90 min)

Open `.planning/VIDEO-INSTRUCTIONS-2026-05-10.md` (recording playbook) and `.planning/VIDEO-VOICEOVER.md` (script). Follow segment by segment.

- [ ] Two screen recordings (window A no-skill, window B with-skill) saved
- [ ] Spliced into one ≤3:00 cut with on-screen captions
- [ ] Uploaded to YouTube — set to **Unlisted**, not Private
- [ ] Copy the YouTube URL → paste into BOTH `BOUNTY-SUBMISSION.md` and `BUILDER-SUBMISSION.md`

If you skip the live A/B and use cached agent responses, that's fine — judges care about the contrast, not the latency.

---

## Phase 4 — frontend deploy ✅ DONE

**Live at https://fhevm-oracle-frontend.vercel.app** — Vercel auto-deploys
`main` (root directory `frontend`, env `NEXT_PUBLIC_VAULT_ADDRESS=0x256e…`).
Latest commit = latest production. One-time exception to the no-Vercel rule
for this submission, locked in 2026-05-09.

- [x] Public URL responds 200
- [x] Connect-wallet button works on Sepolia
- [x] Live URL already in `BUILDER-SUBMISSION.md` → "Frontend URL"
- [ ] **Manual demo before recording**: hide vault id=2,3 → trigger+fulfill id=1 → grab fulfill-tx Etherscan URL → paste into `BUILDER-SUBMISSION.md` → "Sepolia transaction"

---

## Phase 5 — fill the forms (30 min)

### Bounty Track form

URL: https://forms.zama.org/developer-program-mainnet-season2-bounty-track

- [ ] Open `BOUNTY-SUBMISSION.md` in another tab
- [ ] Copy/paste each field into the form
- [ ] Wallet address: use your retrodrop wallet (the one that holds your other Sepolia faucet funds)
- [ ] Submit. Save the confirmation email.

### Builder Track form

URL: https://forms.zama.org/developer-program-mainnet-season2-builder-track

- [ ] Open `BUILDER-SUBMISSION.md` in another tab
- [ ] Copy/paste each field
- [ ] Submit. Save the confirmation email.

---

## Phase 6 — post-submission (15 min)

- [ ] Tweet the bounty submission with a direct link to the demo video and the GitHub repo (use `@yasenka244` or `@cryptoyasenka`, mention `@zama_fhe`). One image: the side-by-side window A/B screenshot.
- [ ] Drop a forum post at https://community.zama.ai under "Developer Program" — paste the README + the demo URL. Same body, different surface — maximizes judge eyeballs.
- [ ] Update `MEMORY.md` with a project entry pointing to this folder + submission status.

---

## Hard rules — DO NOT SKIP

- **No Claude co-author** in any commit (already enforced by the commit messages so far)
- **No `.env` in any commit** — secrets only via `npx hardhat vars set` or Railway env panel
- **No Vercel** for the frontend deploy (Cloudflare Pages, Railway, Fleek instead)
- **No mainnet deploy** — Sepolia only. Mainnet is a December 2026 milestone; deploying earlier is wasted gas.

---

## What to ping me about

- `npm install` errors that aren't fixed by `--legacy-peer-deps`
- `npx hardhat test` failing (means a contract/test bug I shipped)
- Sepolia deploy reverting on a specific function selector
- Any wording in `BOUNTY-SUBMISSION.md` or `BUILDER-SUBMISSION.md` you want to change
- Frontend stuck — I can scaffold a minimum 30-line page from the relayer-sdk README

The rest is mechanical. You've shipped harder things.
