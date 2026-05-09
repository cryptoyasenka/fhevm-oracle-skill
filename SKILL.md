---
name: fhevm-oracle
description: |
  Write correct FHEVM async-decryption oracle code first try. Use this skill any time an
  AI agent is asked to (a) call `FHE.requestDecryption` from a Solidity contract, (b) write
  the matching callback that consumes a decrypted result, (c) reason about replay/finality/
  ordering hazards in confidential dApps that reveal state via the Zama KMS oracle.
  Triggers: "FHEVM async decrypt", "request decryption from contract", "Zama oracle callback",
  "confidential reveal", "encrypted lottery / sealed envelope / time-locked vault",
  "decrypt encrypted state on-chain", "callback selector for FHE.requestDecryption".
  Stack: Solidity ^0.8.27, @fhevm/solidity ^0.11, ethers v6, Hardhat ^2.28 + @fhevm/hardhat-plugin ^0.4.
  Verified against zama-ai/fhevm-solidity@v0.7.0-4 (May 2026) interface surface.
license: BSD-3-Clause-Clear
version: 0.1.0
---

# FHEVM Async Decryption Oracle — Skill

> The async decryption oracle is FHEVM's hardest single primitive and its single most
> exploited footgun. OpenZeppelin's published anti-pattern guide spends 3 of 10 critical
> entries on it. This skill drills the canonical 3-step flow + the 10 anti-patterns into
> muscle memory so a coding agent ships correct code first try.

---

## When to apply this skill

Apply when ANY of these are true:

1. The task involves `FHE.requestDecryption(bytes32[], bytes4)` from a Solidity contract.
2. The agent is writing or auditing a callback function whose selector was passed to `FHE.requestDecryption`.
3. The task involves revealing previously-encrypted state on-chain (lottery winners, sealed
   bids, time-locked secrets, prediction-market resolution, RNG reveals, dead-man switches).
4. The agent must decide between user-decrypt, public-decrypt, and `makePubliclyDecryptable`
   for a piece of encrypted state.
5. The task is "implement an FHEVM contract that ___ at time/condition T" where ___ requires
   plaintext access on-chain.

If the only decryption is **client-side** (frontend reads encrypted state and user-decrypts
via their wallet), this skill does not apply — use the frontend-decrypt patterns in the
`@zama-fhe/relayer-sdk` docs instead.

---

## The single canonical pattern

Every async-decryption flow on FHEVM is exactly three steps:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Step 1  — REQUEST                                                        │
│   contract → FHE.requestDecryption(handles[], callbackSelector)          │
│           returns requestID; library auto-saves handles + auto-grants    │
│           ACL allowForDecryption.                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ Step 2  — RELAYER (off-chain)                                            │
│   Zama Decryption Oracle picks up the event, KMS performs threshold      │
│   decrypt, relayer calls back into your contract using callbackSelector. │
├──────────────────────────────────────────────────────────────────────────┤
│ Step 3  — FULFILL (your callback)                                        │
│   external function fulfillX(uint256 requestID, ...decoded values...,    │
│                              bytes[] memory signatures)                  │
│   {                                                                      │
│     FHE.checkSignatures(requestID, signatures);   // MUST be FIRST       │
│     // -- consume request guard atomically --                            │
│     // -- apply decoded values to state --                               │
│     // -- emit fulfillment event --                                      │
│   }                                                                      │
└──────────────────────────────────────────────────────────────────────────┘
```

**Memorize the function signatures:**

```solidity
// Library (zama-ai/fhevm-solidity)
library FHE {
    function requestDecryption(bytes32[] memory ctsHandles, bytes4 callbackSelector)
        internal returns (uint256 requestID);

    function checkSignatures(uint256 requestID, bytes[] memory signatures) internal;
}
```

**Calldata layout the relayer uses for the callback:**

```
[ 4-byte selector ][ 32-byte requestID ][ N decoded values ][ bytes[] signatures ]
```

The decoded values appear in the **same order as `handles[]` was passed to `requestDecryption`**.
Each value is ABI-decoded into the Solidity primitive of its FHE type — the mapping is below.

### FHE-type → Solidity callback parameter type

| FHE type            | Callback param type | Notes                                   |
|---------------------|---------------------|-----------------------------------------|
| `ebool`             | `bool`              |                                         |
| `euint8`            | `uint8`             |                                         |
| `euint16`           | `uint16`            |                                         |
| `euint32`           | `uint32`            |                                         |
| `euint64`           | `uint64`            |                                         |
| `euint128`          | `uint128`           |                                         |
| `euint256`          | `uint256`           |                                         |
| `eaddress`          | `address`           |                                         |
| `ebytes64`          | `bytes memory`      | Length verified by KMS at decrypt time. |
| `ebytes128`         | `bytes memory`      |                                         |
| `ebytes256`         | `bytes memory`      |                                         |

**Order discipline:** if your `handles[]` is `[euint64 amount, euint256 secret, eaddress winner]`,
your callback signature is exactly:

```solidity
function fulfill(uint256 requestID, uint64 amount, uint256 secret, address winner,
                 bytes[] memory signatures) external { ... }
```

Off-by-one in handle order = silent state corruption. The KMS does not type-check positions.

---

## Decision tree — which decrypt path do I want?

```
Is the value ever read in plaintext on-chain after the gate?
├─ YES → Async oracle decryption (THIS SKILL)
│   └─ Use FHE.requestDecryption(...) → callback writes to clear state.
│
└─ NO  → keep encrypted; pick client-side path:
    ├─ Anyone with a wallet can read it?
    │   YES → makePubliclyDecryptable + relayer publicDecrypt (front-end fetches plaintext).
    │   NO  → user-decrypt with EIP-712 signature; only authorised account sees it.
    └─ Inside another contract on-chain (no plaintext leaks)?
         Use FHE.allow(ct, otherContract) and let the other contract operate on it.
```

**Never** use the async oracle when client-side decrypt suffices — every oracle round-trip
costs gas + latency + introduces a replay/finality attack surface.

---

## ACL discipline — non-negotiable

After **every state-mutating operation that produces an encrypted output**, do exactly:

```solidity
encryptedX = FHE.someOp(a, b);
FHE.allowThis(encryptedX);              // contract can re-read encryptedX in later txs
FHE.allow(encryptedX, msg.sender);      // caller can user-decrypt encryptedX off-chain
```

If you skip `allowThis`, the next transaction reading `encryptedX` reverts. If you skip
`allow(*, msg.sender)`, the user cannot see the result of their own action.

Before passing handles to `FHE.requestDecryption`, the library **automatically** calls
`IACL.allowForDecryption(handles)` for you. **You do not** need to grant ACL to the oracle
manually — but you DO need every handle in `handles[]` to currently be readable by the
contract itself (i.e. `allowThis` was called when each was produced).

### ACL persistence vs transient

| Function                                | Lifetime                                        | Use when…                                      |
|-----------------------------------------|-------------------------------------------------|------------------------------------------------|
| `FHE.allow(ct, account)`                | Persistent across transactions.                  | Standard user / contract grant.                |
| `FHE.allowThis(ct)`                     | Persistent — grants `address(this)`.            | After every state mutation producing `ct`.     |
| `FHE.allowTransient(ct, account)`       | Same transaction only — cleared at tx end.      | Pass handle through a router/proxy in one tx.  |
| `FHE.makePubliclyDecryptable(ct)`       | Persistent — anyone can publicDecrypt off-chain.| Public reveal (board, scoreboard, leaderboard).|

**Account-Abstraction caveat:** if you use `allowTransient` inside a UserOperation that batches
multiple sub-calls, you MUST call `cleanTransientStorage()` between sub-calls (not yours; the
EntryPoint-level cleanup) — otherwise transient grants leak across sub-calls and give the next
sub-call ACL it shouldn't have. Mark this loudly in any AA-context contract.

---

## The 10 anti-patterns (drilled with fix templates)

### AP-001 — `checkSignatures` not called first in callback

**Bad:**
```solidity
function fulfill(uint256 requestID, uint64 amount, bytes[] memory signatures) external {
    clearAmount = amount;            // ❌ trusts un-verified KMS payload
    FHE.checkSignatures(requestID, signatures);
}
```

**Why broken:** anyone can call `fulfill` with a forged payload — there is **no msg.sender
restriction** on the relayer callback by design (the KMS signature IS the authentication).
Without the signature check, your contract accepts attacker-supplied "decrypted" values.

**Fix:**
```solidity
function fulfill(uint256 requestID, uint64 amount, bytes[] memory signatures) external {
    FHE.checkSignatures(requestID, signatures);   // ✅ FIRST line of every fulfill
    // … now you can trust `amount`
    clearAmount = amount;
}
```

> **Rule:** the **first non-empty statement** of every callback is `FHE.checkSignatures(...)`.
> Anything before it is reachable by an unauthenticated caller.

---

### AP-002 — Replay: callback can fire twice

**Bad:**
```solidity
function fulfill(uint256 requestID, uint64 amount, bytes[] memory signatures) external {
    FHE.checkSignatures(requestID, signatures);
    Vault storage v = vaults[requestIDToVaultId[requestID]];
    v.clearAmount = amount;
    v.revealed   = true;
    payable(v.depositor).transfer(amount);   // ❌ if relayer re-tries, double-pay
}
```

**Why broken:** `checkSignatures` verifies the payload but does NOT mark the request as
consumed. A retried/forwarded relayer call (or a second submitter racing to claim a relayer
fee) re-runs the entire callback, including the external transfer.

**Fix — atomic consume sentinel:**
```solidity
mapping(uint256 vaultId => uint256 outstandingRequestID) public outstanding;
mapping(uint256 requestID => uint256 vaultId) private requestIDToVault;
uint256 private constant CONSUMED = type(uint256).max;

function fulfill(uint256 requestID, uint64 amount, bytes[] memory signatures) external {
    FHE.checkSignatures(requestID, signatures);
    uint256 vaultId = requestIDToVault[requestID];
    require(outstanding[vaultId] == requestID, "consumed-or-mismatched");
    outstanding[vaultId]      = CONSUMED;        // ✅ atomic guard BEFORE external call
    delete requestIDToVault[requestID];
    Vault storage v = vaults[vaultId];
    v.clearAmount = amount;
    v.revealed    = true;
    payable(v.depositor).transfer(amount);       // safe — guarded
}
```

> **Rule:** consume the request guard **before any external call** in the callback. Use a
> sentinel value (`type(uint256).max`) rather than `delete` if you also need to detect
> "this vault was already revealed" later.

---

### AP-003 — Handle order ≠ callback parameter order

**Bad:**
```solidity
bytes32[] memory h = new bytes32[](2);
h[0] = euint256.unwrap(secret);
h[1] = euint64.unwrap(amount);
FHE.requestDecryption(h, this.fulfill.selector);
// callback claims (uint64 amount, uint256 secret) — WRONG ORDER
function fulfill(uint256 requestID, uint64 amount, uint256 secret, bytes[] memory sigs) external { … }
```

**Why broken:** ABI decoder reads positionally. Your `amount` parameter receives the **first
32 bytes** (truncated to uint64) of what is actually a `uint256 secret`. Silent corruption.

**Fix — make the order rule a comment:**
```solidity
// HANDLE ORDER MUST MATCH CALLBACK PARAMETER ORDER:
//   handles[0]  ↔  param after requestID  (param 1)
//   handles[1]  ↔  param 2
//   …
bytes32[] memory h = new bytes32[](2);
h[0] = euint64.unwrap(amount);     // ↔ uint64 amount
h[1] = euint256.unwrap(secret);    // ↔ uint256 secret
FHE.requestDecryption(h, this.fulfill.selector);

function fulfill(uint256 requestID, uint64 amount, uint256 secret, bytes[] memory sigs) external {
    FHE.checkSignatures(requestID, sigs);
    …
}
```

> **Rule:** put the handle-array build and the callback function in adjacent code blocks with
> a side-by-side comment. Re-order them as a pair or not at all.

---

### AP-004 — Missing `allowThis` after state mutation

**Bad:**
```solidity
function lock(externalEuint64 inAmount, bytes calldata proof) external {
    euint64 amount = FHE.fromExternal(inAmount, proof);
    vaults[nextId++] = Vault({encAmount: amount, revealAt: block.timestamp + 1 days, …});
    // no FHE.allowThis(amount) — next tx that reads vault.encAmount reverts
}
```

**Why broken:** the contract itself is not on the ACL of `amount`, so when `triggerReveal`
later does `bytes32[] memory h = new bytes32[](1); h[0] = euint64.unwrap(v.encAmount);
FHE.requestDecryption(h, …)` the library's internal `allowForDecryption(handles)` reverts
because the contract doesn't have ACL on the handle.

**Fix:**
```solidity
euint64 amount = FHE.fromExternal(inAmount, proof);
FHE.allowThis(amount);                    // ✅ contract retains read access
FHE.allow(amount, msg.sender);            // ✅ depositor can also user-decrypt
vaults[nextId++] = Vault({encAmount: amount, …});
```

> **Rule:** every line that produces an encrypted output (`FHE.fromExternal`, `FHE.add`,
> `FHE.select`, `FHE.eq`, …) is followed within the same function by `FHE.allowThis(out)`
> if the contract will read it later, **and** `FHE.allow(out, msg.sender)` if the user will.

---

### AP-005 — External call before guard consume (cross-function replay)

**Bad:**
```solidity
function fulfill(uint256 requestID, uint64 amount, bytes[] memory signatures) external {
    FHE.checkSignatures(requestID, signatures);
    payoutModule.payWinner(amount);                 // ❌ external call BEFORE guard
    outstanding[requestIDToVault[requestID]] = CONSUMED;
}
```

**Why broken:** `payoutModule` may re-enter `fulfill` (or any other state-touching function)
during its execution. The guard is not yet set, so the re-entrant path looks "open."

**Fix — checks-effects-interactions in the callback too:**
```solidity
function fulfill(uint256 requestID, uint64 amount, bytes[] memory signatures) external {
    FHE.checkSignatures(requestID, signatures);
    uint256 vaultId = requestIDToVault[requestID];
    require(outstanding[vaultId] == requestID, "consumed");
    outstanding[vaultId] = CONSUMED;                // 1. effects first
    delete requestIDToVault[requestID];
    payoutModule.payWinner(amount);                 // 2. interactions last
}
```

---

### AP-006 — Transient ACL bleeding across UserOps

**Bad (Account-Abstraction context):**
```solidity
// inside a UserOp
FHE.allowTransient(secretCt, executor);
executor.runStep1(secretCt);
// ... no cleanTransientStorage ...
executor.runStep2(secretCt);   // ❌ transient grant from step1 still active in step2
```

**Why broken:** `allowTransient` is keyed by transaction-end. In an AA flow that batches
sub-calls inside a single UserOp without clearing transient storage, the grant persists
and may give a different executor in step 2 access it shouldn't have.

**Fix:** always pair `allowTransient` with explicit cleanup at the boundary you care about,
and prefer **persistent** `FHE.allow(ct, account)` for everything that crosses sub-calls.

> **Rule of thumb:** `allowTransient` is for tx-scoped routing. If the call chain spans a
> meta-transaction or batched UserOp, fall back to persistent `FHE.allow`.

---

### AP-007 — Assuming sync decrypt exists

**Bad:**
```solidity
uint64 plain = FHE.decrypt(encAmount);   // ❌ no such function on mainnet
```

**Why broken:** synchronous in-tx decrypt was a Sepolia-mock convenience that no longer
exists in `@fhevm/solidity` ≥0.10. Mainnet provides only the async oracle path.

**Fix:** every reveal flow goes through `FHE.requestDecryption` + a callback. Period.

> **Rule:** if you find yourself wanting `FHE.decrypt` synchronously, the design is wrong.
> Refactor the flow into a `request()` user-tx and a `fulfill()` callback.

---

### AP-008 — Off-by-one finality (`==` vs `>`)

**Bad:**
```solidity
require(block.timestamp == vault.revealAt, "not-yet");   // ❌
```

**Why broken:** miners can choose any timestamp ≥ parent's; reveal can be skipped if no
block lands at exactly `revealAt`. Also, attackers can grief by sending no tx at the exact
second.

**Fix:**
```solidity
require(block.timestamp >= vault.revealAt, "too-early");
```

Use `>=` for time-locked reveals; `>` only when you genuinely require a strictly-after
condition (rare in practice).

---

### AP-009 — No fallback for relayer outage

**Bad:** assume the callback always fires within minutes. Some early FHEVM deployments saw
hour-long delays during KMS upgrades.

**Fix:** record `requestedAt` next to the outstanding requestID. After a configurable
timeout (e.g. 24h), allow the requester to call `cancelOutstandingRequest(vaultId)` which
clears `outstanding[vaultId]` and lets them re-issue. If the original callback later fires,
the guard (`outstanding[vaultId] == requestID`) is no longer satisfied → safely reverts.

```solidity
struct Outstanding { uint256 requestID; uint64 requestedAt; }
mapping(uint256 vaultId => Outstanding) public outstanding;
uint256 public constant ORACLE_TIMEOUT = 24 hours;

function cancelOutstandingRequest(uint256 vaultId) external {
    Outstanding storage o = outstanding[vaultId];
    require(o.requestID != 0,                                  "no-pending");
    require(block.timestamp - o.requestedAt > ORACLE_TIMEOUT,  "too-soon");
    delete outstanding[vaultId];
}
```

---

### AP-010 — Re-using a consumed handle

**Bad:**
```solidity
// inside fulfill
v.encAmount = FHE.asEuint64(amount);   // ❌ throws away encryption invariant
v.clearAmount = amount;
```

**Why broken:** once you have plaintext, re-encrypting it on-chain provides zero privacy —
every observer saw the plaintext flow through the callback. The new ciphertext has the same
"public knowledge" as the cleartext.

**Fix:** keep the original ciphertext (now publicly decrypted, but its handle is unchanged)
or zero out the slot. Don't pretend privacy returns after a public reveal.

```solidity
v.clearAmount = amount;
// optionally: v.encAmount = FHE.asEuint64(0); // nullify
```

---

## Reference contract — `AsyncRevealVault.sol`

This skill ships with `contracts/AsyncRevealVault.sol`, a universal time-locked reveal
primitive that exercises every rule above:

- Encrypted inputs (`euint64 amount`, `euint256 secret`) via `FHE.fromExternal`.
- ACL discipline after every mutation (`allowThis` + `allow(msg.sender)`).
- Correct `bytes32[]` build with handle-order comment.
- `FHE.requestDecryption` with explicit `this.fulfillReveal.selector`.
- `fulfillReveal` with `FHE.checkSignatures` first, atomic `outstanding[…] = CONSUMED` guard
  before any external interaction, off-by-one-safe finality (`>=`), and a `cancelOutstandingRequest`
  fallback for relayer outages.

Tests in `test/AsyncRevealVault.ts` run in mock mode and cover:

1. Reveal before `revealAt` reverts.
2. Successful reveal flow (request → mock fulfill → state consumed).
3. Replay rejection (second fulfill for same `requestID` reverts).
4. ACL discipline (depositor can user-decrypt; non-depositor cannot).

> The contract is intentionally narrow — it is the canonical demo for this skill, not a
> production product. The patterns generalise to lotteries, sealed bids, prediction markets,
> dead-man switches, and any other "encrypt now, reveal later" primitive.

---

## Pre-deploy checklist (paste into PR description)

```
[ ] Every callback's first statement is FHE.checkSignatures(requestID, signatures).
[ ] Every fulfill consumes its outstanding[] guard BEFORE any external call.
[ ] Handle build order matches callback parameter order (line-adjacent comment).
[ ] Every encrypted output is followed by FHE.allowThis(out) and, if user-facing,
    FHE.allow(out, msg.sender).
[ ] Time-locked reveals use `>=`, not `==`.
[ ] Every outstanding request has a timeout-cancel path.
[ ] No FHE.decrypt(...) sync calls anywhere in the codebase.
[ ] Solidity pragma ^0.8.27, evmVersion cancun.
[ ] `npx hardhat test` green in mock mode (≥4 callback-flow assertions).
```

---

## Stack pinning

Verified-working versions for this skill (May 2026, pinned to upstream
`zama-ai/fhevm-hardhat-template@v0.4.1`):

```jsonc
"@fhevm/solidity":      "^0.11.1",
"@fhevm/hardhat-plugin": "^0.4.2",
"@fhevm/mock-utils":    "^0.4.2",
"@zama-fhe/relayer-sdk": "^0.4.1",
"hardhat":              "^2.28.6",
"ethers":               "^6.16.0",
// solidity 0.8.27, evmVersion "cancun", optimizer 800 runs
```

Any older versions of `@fhevm/solidity` (≤0.10) had a different ACL surface — re-read this
skill against the upstream changelog before assuming the rules transfer.

---

## Source authority

- `zama-ai/fhevm-solidity` — `lib/FHE.sol` (the library being documented here).
- `zama-ai/fhevm-hardhat-template` — canonical project skeleton (mirrored in this repo).
- OpenZeppelin "A developer's guide to FHEVM security" — anti-patterns #3, #5, #10 map to
  AP-001, AP-002, AP-005 in this skill.
- Zama Developer Program Mainnet S2 announce blog (2026-04, accessed 2026-05-09).
