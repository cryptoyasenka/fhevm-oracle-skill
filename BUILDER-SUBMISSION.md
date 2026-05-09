# Builder Track Submission — Pre-filled Form Answers

**Form:** https://forms.zama.org/developer-program-mainnet-season2-builder-track
**Deadline:** 2026-05-10 23:59 AOE (= 2026-05-11 11:59 UTC)
**Submitter:** cryptoyasenka — yamihmih@gmail.com

---

## Project — AsyncRevealVault

### Title

> AsyncRevealVault — universal time-locked encrypted reveal primitive on FHEVM

### One-line tagline

> Lock an encrypted (amount, secret) pair until a future timestamp, then KMS-decrypt it on-chain in a single round-trip.

### Long description

> AsyncRevealVault is a minimal, reusable building block for any FHEVM contract that needs to keep a value encrypted on-chain until a specific moment, then reveal it through the KMS oracle. The depositor calls `lock(externalEuint64 amount, externalEuint256 secret, bytes proof, uint256 revealAt)` to store an encrypted amount + secret bound to themselves and the contract. After `revealAt`, anyone can call `triggerReveal(vaultId)`, which submits both ciphertexts to the relayer in a single `FHE.requestDecryption` call. The KMS callback `fulfillReveal` verifies signatures, consumes the request guard, then writes the cleartext.
>
> What this enables, with no extra plumbing:
>
> - **Sealed-bid auctions** — every bid is a vault, the auction-end timestamp is `revealAt`, the auctioneer calls `triggerReveal` on the winning bid only.
> - **Vesting cliffs** — locked salary or token grant becomes claimable only after the cliff date, no off-chain trusted signer needed.
> - **Time-locked dead-man switches** — a secret message that auto-publishes if you fail to reset the timer.
> - **Commit-reveal randomness** — multi-party seed commitment with a single shared reveal slot.
>
> The contract is deliberately small (~220 lines, 1 file) so it composes cleanly. It also serves as the reference implementation for the companion `fhevm-oracle` SKILL.md — an AI-coding-agent skill submitted to the same season's Bounty Track.
>
> ### Highlights for judges
>
> - `FHE.checkSignatures` is the FIRST line of the callback (no fake-decryption attack)
> - Replay-protected: `delete requestToVault[requestID]` + `outstandingRequestID = type(uint256).max` consumed BEFORE state writes, so a duplicate or out-of-order callback aborts at `UnknownRequest`
> - Strict `>` finality on `revealAt` (no off-by-one)
> - Relayer-outage fallback: depositor can `cancelOutstandingRequest` after `CANCEL_GRACE` (24h) and re-trigger
> - ACL discipline preserved across every state mutation: `allowThis` + `allow(_, depositor)` after `lock`
> - Mock-mode Hardhat tests cover happy path + three failure modes; deterministic via `hre.fhevm.awaitDecryptionOracle()`

### GitHub repo URL

> https://github.com/cryptoyasenka/fhevm-oracle-skill

### Sepolia deployment address

> [PASTE AsyncRevealVault SEPOLIA ADDRESS AFTER `npm run deploy:sepolia`]

### Sepolia transaction (lock + reveal demo)

> [PASTE SEPOLIA ETHERSCAN URL AFTER ON-CHAIN DEMO]

### Demo video URL

> [PASTE YOUTUBE LINK — same as Bounty Track]

### Frontend URL (live)

> [PASTE FRONTEND URL — Railway/Cloudflare Pages, NOT Vercel per project rules]
>
> Source: `frontend/` in this repo. Next.js 14 App Router, single client page,
> standalone build output. Implements Connect → Encrypt+Lock → Trigger →
> Fulfill (publicDecrypt + checkSignatures) end-to-end against Sepolia.
> See `frontend/README.md` for local dev + Railway deploy instructions.

### Stack

- `@fhevm/solidity` 0.11.1 (FHE library)
- `@fhevm/hardhat-plugin` 0.4.2 (mock-mode dev loop)
- `@zama-fhe/relayer-sdk` 0.4.1 (frontend encrypt + user-decrypt)
- Solidity 0.8.27, EVM cancun, optimizer 800 runs
- Hardhat 2.28.6, ethers 6.16.0, Node ≥ 20

### License

> BSD-3-Clause-Clear

### Wallet address for prize

> [PASTE WALLET ADDRESS]

---

## Differentiation

> Most existing FHEVM demo contracts are domain-specific (an auction, a sealed ballot, a confidential ERC-20). AsyncRevealVault is a **primitive** — the smallest reusable contract that encodes the time-locked async-decryption pattern correctly. Anyone building one of the domain-specific contracts can either inherit from it or copy the 220 lines and replace the storage layout. That has higher reuse value than yet another vertical-specific demo, and it's the natural pairing for the SKILL.md submitted in parallel: the skill teaches the pattern, the vault contract is its smallest correct embodiment.

---

## Hand-off note for judges

> Read `SKILL.md` and `contracts/AsyncRevealVault.sol` side-by-side: every numbered anti-pattern in the skill (AP-001 through AP-010) maps to an explicit comment line in the contract. The skill is what an agent reads; the contract is what an agent writes when the skill is loaded.
