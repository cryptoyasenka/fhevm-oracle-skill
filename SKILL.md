---
name: fhevm-oracle
description: Drill the canonical FHEVM async-decryption flow — flag with `makePubliclyDecryptable`, accept a KMS-signed cleartext callback, verify with `checkSignatures` BEFORE writing state. Use when an AI agent is asked to (a) write a Solidity contract that decrypts encrypted state via the KMS, (b) write or audit a callback that takes `(bytes abiEncodedCleartexts, bytes decryptionProof)`, (c) review an FHEVM contract for replay or fake-decryption bugs, (d) explain why mainnet has no synchronous decrypt.
license: BSD-3-Clause-Clear
version: 0.2.0
stack:
  fhevm-solidity: ^0.11.1
  fhevm-hardhat-plugin: ^0.4.2
  zama-fhe-relayer-sdk: ^0.4.1
  solidity: 0.8.27
  evm: cancun
---

# FHEVM Async Decryption Oracle — Skill

Generic FHEVM coding skills cover encrypted types, ops, ACL, input proofs, decryption,
frontend, testing, and anti-patterns at one section each. This skill goes deep on
the single most error-prone primitive: **moving an encrypted value back to cleartext
through the KMS**. AI agents botch it the same way every time. Drill the pattern below
as muscle memory.

---

## When to apply this skill

Trigger if any of the following are true:

1. The task involves `FHE.makePubliclyDecryptable(handle)` from a Solidity contract.
2. The agent is writing or auditing a callback that receives `(bytes abiEncodedCleartexts, bytes decryptionProof)` from a KMS relayer.
3. The contract has an encrypted value (`euint*`, `ebool`, `eaddress`) whose cleartext needs to land in storage at a specific moment (after a vote ends, after a deadline, on a winning condition).
4. The user mentions "decrypt encrypted state on-chain", "KMS oracle", "publicly decrypt", or "fhevm callback".
5. Code under review uses `FHE.checkSignatures(...)` and the agent must verify it's wired correctly.

If a task only does **user-decryption** (the result is shown to a single end-user via the relayer SDK off-chain, not stored as cleartext on-chain), skip this skill and use `FHE.allow(ct, user)` + frontend `userDecrypt` instead — see the decision tree below.

---

## The single canonical pattern

Three steps. Memorize the names.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  STEP 1 — REQUEST                                                        │
│   Anyone calls a contract function (you name it) that does:              │
│     FHE.makePubliclyDecryptable(handle1);                                │
│     FHE.makePubliclyDecryptable(handle2);                                │
│   No requestID. No callback selector. The KMS picks up the on-chain      │
│   flag off-chain.                                                        │
├──────────────────────────────────────────────────────────────────────────┤
│  STEP 2 — RELAYER                                                        │
│   The KMS decrypts off-chain, signs (handles, cleartexts) → produces a   │
│   `decryptionProof` blob. A relayer (or anyone — including the dApp      │
│   itself or the depositor) submits cleartext+proof to a callback YOU     │
│   defined on YOUR contract.                                              │
├──────────────────────────────────────────────────────────────────────────┤
│  STEP 3 — FULFILL                                                        │
│   Your callback rebuilds the same handles[] array, calls                 │
│   `FHE.checkSignatures(handles, abiEncodedCleartexts, decryptionProof)`  │
│   FIRST, then sets the replay-guard flag, then `abi.decode`s cleartexts  │
│   in the SAME ORDER as handles[] and writes them to storage.             │
└──────────────────────────────────────────────────────────────────────────┘
```

### Imports (verbatim)

```solidity
// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.27;

import {FHE, euint64, euint256, externalEuint64, externalEuint256}
    from "@fhevm/solidity/lib/FHE.sol";
import {ZamaEthereumConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

contract MyDecrypt is ZamaEthereumConfig { /* ... */ }
```

### Canonical 3-step skeleton

```solidity
// STEP 1 — REQUEST
function triggerReveal(uint256 id) external {
    /* gating: time / role / state */
    FHE.makePubliclyDecryptable(items[id].encA);   // euint64
    FHE.makePubliclyDecryptable(items[id].encB);   // euint256
    emit RevealRequested(id);
}

// STEP 3 — FULFILL (anyone with a valid KMS proof can call)
function fulfillReveal(
    uint256        id,
    bytes calldata abiEncodedCleartexts,
    bytes calldata decryptionProof
) external {
    Item storage it = items[id];
    if (it.revealed) revert AlreadyRevealed();      // replay guard

    // Rebuild the handles list — order MUST match the abi.decode tuple below.
    bytes32[] memory handles = new bytes32[](2);
    handles[0] = FHE.toBytes32(it.encA);
    handles[1] = FHE.toBytes32(it.encB);

    // (1) AP-001 — verify FIRST, no exceptions.
    FHE.checkSignatures(handles, abiEncodedCleartexts, decryptionProof);

    // (2) AP-002 — flip the guard BEFORE any state write or external call.
    it.revealed = true;

    // (3) AP-003 — tuple order matches handles[] order.
    (uint64 a, uint256 b) = abi.decode(abiEncodedCleartexts, (uint64, uint256));
    it.clearA = a;
    it.clearB = b;

    emit Revealed(id, a, b);
}
```

### FHE-type → callback decode pair

When you write `abi.decode(abiEncodedCleartexts, (T1, T2, ...))`, each `Ti` MUST match the encrypted type at the same position in `handles[]`:

| Encrypted handle      | Cleartext type in `abi.decode`     |
|-----------------------|------------------------------------|
| `ebool`               | `bool`                             |
| `euint8`              | `uint8`                            |
| `euint16`             | `uint16`                           |
| `euint32`             | `uint32`                           |
| `euint64`             | `uint64`                           |
| `euint128`            | `uint128`                          |
| `euint256`            | `uint256`                          |
| `eaddress`            | `address`                          |
| `ebytes64/128/256`    | `bytes` (decoded length must match)|

**A mismatch is a silent bug**: `checkSignatures` will revert with `KMSInvalidSigner` because the KMS signed cleartexts in the right type sizes but `abi.decode` reads them as the wrong shape.

---

## Decision tree — which decrypt path do I want?

```
Is the cleartext supposed to land in on-chain storage?
├─ NO, it's only displayed to a single user
│   └─ Use FHE.allow(ct, user) + frontend zama-fhe/relayer-sdk userDecrypt(handle).
│       NOT this skill's territory.
│
└─ YES, on-chain storage / further on-chain logic depends on cleartext
    │
    ├─ Is the cleartext supposed to be public to all chain observers?
    │   ├─ YES (auction-end, dead-man switch, vote tally)
    │   │   └─ Use FHE.makePubliclyDecryptable + signed callback. THIS SKILL.
    │   │
    │   └─ NO, only your contract should ever read it
    │       └─ Reconsider — once cleartext lands in storage everyone sees it.
    │           If you need on-chain comparisons but not raw cleartext, use
    │           encrypted comparison ops (FHE.eq, FHE.lt, FHE.select) and
    │           publicly decrypt only the BOOLEAN result, never the operands.
```

There is **no synchronous on-chain decrypt** in fhevm-solidity 0.11.1. Anyone writing `FHE.decrypt(ct)` and expecting an immediate cleartext is using an outdated mental model (older fhevm versions exposed it; mainnet does not).

---

## ACL discipline — non-negotiable

Every state-mutating operation that produces a new ciphertext handle must be re-allowed for `address(this)`, or the next read from `this` will revert with an ACL error. Three rules:

1. **After every state mutation in a function**, call `FHE.allowThis(newCt)`.
2. **After every state mutation in a user-facing function**, also call `FHE.allow(newCt, msg.sender)` if the user is supposed to be able to user-decrypt off-chain.
3. **Before `makePubliclyDecryptable`**, the handle must already be `allowThis`-ed (which it will be if rule 1 was followed everywhere).

### `allow` vs `allowThis` vs `allowTransient` vs `makePubliclyDecryptable`

| Function                          | Scope                                  | Persistence       |
|-----------------------------------|----------------------------------------|-------------------|
| `FHE.allow(ct, user)`             | Lets `user` user-decrypt off-chain     | Persistent        |
| `FHE.allowThis(ct)`               | Lets `address(this)` read in next tx   | Persistent        |
| `FHE.allowTransient(ct, account)` | Lets `account` use ct in current tx    | Cleared at tx end |
| `FHE.makePubliclyDecryptable(ct)` | Anyone can publicly decrypt via KMS    | Persistent        |

`allowTransient` is for sub-call composition within ONE transaction. Trying to read it from a later UserOp / cross-tx will revert.

---

## The 10 anti-patterns (drilled with fix templates)

### AP-001 — `checkSignatures` not called first in callback

**Broken:**
```solidity
function fulfillReveal(uint256 id, bytes calldata cleartexts, bytes calldata proof) external {
    items[id].revealed = true;                                 // ← writes state
    (uint64 a) = abi.decode(cleartexts, (uint64));
    items[id].clearA = a;
    bytes32[] memory handles = new bytes32[](1);
    handles[0] = FHE.toBytes32(items[id].encA);
    FHE.checkSignatures(handles, cleartexts, proof);           // ← too late
}
```

**Why broken:** anyone can call this with arbitrary cleartext. `checkSignatures` only reverts if the proof is invalid — but state writes already happened. Worse: a partial revert that bubbles up doesn't unwind external effects in some patterns (events, ETH transfers).

**Fix template:**
```solidity
function fulfillReveal(uint256 id, bytes calldata cleartexts, bytes calldata proof) external {
    bytes32[] memory handles = new bytes32[](1);
    handles[0] = FHE.toBytes32(items[id].encA);
    FHE.checkSignatures(handles, cleartexts, proof);   // FIRST
    items[id].revealed = true;
    items[id].clearA = abi.decode(cleartexts, (uint64));
}
```

### AP-002 — No replay guard before write

**Broken:**
```solidity
function fulfillReveal(uint256 id, bytes calldata cleartexts, bytes calldata proof) external {
    bytes32[] memory handles = /* ... */;
    FHE.checkSignatures(handles, cleartexts, proof);
    items[id].clearA = abi.decode(cleartexts, (uint64));
    emit Revealed(id, items[id].clearA);    // ← anyone can re-call this forever
}
```

**Why broken:** the KMS proof is valid forever for those handles. Anyone can submit it again, re-emitting `Revealed` and re-writing storage (idempotent for `clearA`, but the event log is now noisy and downstream indexers double-count).

**Fix template:** flip a `revealed` flag BEFORE the write, and revert on second attempt:
```solidity
if (items[id].revealed) revert AlreadyRevealed();
FHE.checkSignatures(handles, cleartexts, proof);
items[id].revealed = true;                                  // consumed
items[id].clearA = abi.decode(cleartexts, (uint64));
emit Revealed(id, items[id].clearA);
```

### AP-003 — Handle order ≠ `abi.decode` tuple order

**Broken:**
```solidity
bytes32[] memory handles = new bytes32[](2);
handles[0] = FHE.toBytes32(it.encA);     // euint64
handles[1] = FHE.toBytes32(it.encB);     // euint256
FHE.checkSignatures(handles, cleartexts, proof);
(uint256 b, uint64 a) = abi.decode(cleartexts, (uint256, uint64));   // ← swapped
it.clearA = a;
it.clearB = b;
```

**Why broken:** `checkSignatures` PASSES (the KMS signed cleartexts in the order of handles[]), but the decode reads them in the wrong slots. `it.clearA` ends up holding the high bits of `b`. Hardest bug to spot in review because there's no compiler warning and tests pass for matching-length tuples.

**Fix:** keep handles[i] and decode-tuple position `i` lockstep. Audit checklist: read the function bottom-up, draw a line from each `handles[i] = ...` to its corresponding `abi.decode` slot.

### AP-004 — Missing `allowThis` after state mutation

**Broken:**
```solidity
function add(externalEuint64 enc, bytes calldata proof) external {
    euint64 v = FHE.fromExternal(enc, proof);
    total = FHE.add(total, v);                              // new ciphertext
    /* ← missing: FHE.allowThis(total) */
}

function getTotal() external view returns (euint64) { return total; }
```

**Why broken:** the next time anyone calls `getTotal` and tries to user-decrypt or pass `total` into another op, the ACL check reverts because `address(this)` no longer has permission on the new handle.

**Fix:** every assignment to a state ciphertext is followed by `FHE.allowThis(ct)`:
```solidity
total = FHE.add(total, v);
FHE.allowThis(total);
FHE.allow(total, msg.sender);   // if the caller should also user-decrypt
```

### AP-005 — Missing `allow(ct, user)` for user-facing returns

**Broken:** depositor locks an encrypted balance, dApp wants them to user-decrypt off-chain, but the lock function only does `FHE.allowThis(bal)`. Off-chain `userDecrypt` reverts.

**Fix:** always `FHE.allow(ct, depositor)` whenever a user is expected to user-decrypt the value via the relayer SDK.

### AP-006 — `allowTransient` outliving its transaction

**Broken:**
```solidity
function start(externalEuint64 enc, bytes calldata proof) external {
    euint64 v = FHE.fromExternal(enc, proof);
    FHE.allowTransient(v, otherContract);
    pending = v;                       // ← stored to state
    FHE.allowThis(pending);
}
function laterTx() external {
    OtherContract(otherContract).consume(pending);   // ← reverts
}
```

**Why broken:** `allowTransient` is cleared at the end of the original transaction. The later tx sees no permission for `otherContract`.

**Fix:** use persistent `FHE.allow(ct, otherContract)` if the permission must outlive the transaction. Use `allowTransient` only for sub-call composition WITHIN a single tx.

### AP-007 — Assuming sync decrypt exists

**Broken:**
```solidity
uint64 cleartext = FHE.decrypt(handle);   // ← does not exist on mainnet 0.11.1
```

**Why broken:** older versions of fhevm exposed an in-place `decrypt`. The current library does not. Decryption is always async via `makePubliclyDecryptable` + signed callback (this skill's pattern) or off-chain via `userDecrypt` (relayer SDK).

**Fix:** rework the contract to be two-step. If the agent is iterating on a contract that does sync decrypt, push back: ask whether the cleartext can stay off-chain (use `allow` + relayer SDK) or whether the contract really needs the cleartext to land on-chain (use this skill's flow).

### AP-008 — External call before guard consume (cross-fn replay)

**Broken:**
```solidity
function fulfillReveal(uint256 id, bytes calldata cleartexts, bytes calldata proof) external {
    bytes32[] memory handles = /* ... */;
    FHE.checkSignatures(handles, cleartexts, proof);
    payouts[id] = abi.decode(cleartexts, (uint64));
    payable(items[id].winner).transfer(payouts[id]);            // ← external call
    items[id].revealed = true;                                  // ← guard set AFTER
}
```

**Why broken:** the `transfer` re-enters via the recipient's fallback which calls `fulfillReveal` again with the same proof, double-pays.

**Fix:** checks-effects-interactions. Set `revealed = true` BEFORE the external call.

### AP-009 — No fallback for KMS / relayer outage

**Broken:** the contract calls `makePubliclyDecryptable` once and assumes a relayer will always submit cleartext within a known window. If the relayer is down for hours, the contract is stuck — no way for the depositor to retry.

**Fix:** make `triggerReveal` idempotent (re-flagging an already-flagged handle is a no-op). Anyone, including the depositor, can re-call it. Document the expected relayer SLA. If you need a hard fallback (cancel and refund), gate it on a `reveal_at + grace_window` timestamp.

### AP-010 — Off-by-one finality (`>=` vs `>` on `revealAt`)

**Broken:**
```solidity
if (block.timestamp < revealAt) revert RevealTooEarly();   // ≡ allows reveal at exactly revealAt
```

**Why broken:** the user said "decryptable AFTER 5pm Friday". 5:00:00pm Friday is exactly the boundary. With `<`, at exactly 5pm the reveal works. The user expected the first allowed second to be 5:00:01.

**Fix:** use `<=` (i.e. `revert if block.timestamp <= revealAt`) when "AFTER" should be strict, and document the choice in a `///` comment so future readers know which interpretation was chosen.

---

## Reference contract — `AsyncRevealVault.sol`

The file `contracts/AsyncRevealVault.sol` in this repo is the smallest correct embodiment of the pattern. Every numbered anti-pattern above maps to a labelled comment line in the contract. Read them side-by-side.

### Test pattern (mock mode)

`@fhevm/hardhat-plugin@0.4.2` exposes `hre.fhevm.debugger.createDecryptionSignatures(handlesBytes32Hex, clearTextValues)` which produces an array of mock KMS signatures. Pack them as the `decryptionProof` blob the contract expects:

```ts
import { ethers, fhevm } from "hardhat";

// 1. Encrypt input + lock
const enc = await fhevm.createEncryptedInput(vaultAddress, signer.address)
  .add64(AMOUNT).add256(SECRET).encrypt();
await vault.lock(enc.handles[0], enc.handles[1], enc.inputProof, revealAt);

// 2. After revealAt, trigger
await vault.triggerReveal(vaultId);

// 3. Build cleartexts blob + KMS signatures
const cleartexts = ethers.AbiCoder.defaultAbiCoder()
  .encode(["uint64", "uint256"], [AMOUNT, SECRET]);

const handlesBytes32Hex = [
  ethers.toBeHex(await vault.getEncryptedAmount(vaultId), 32),
  ethers.toBeHex(await vault.getEncryptedSecret(vaultId), 32),
];
const sigs = await fhevm.debugger.createDecryptionSignatures(
  handlesBytes32Hex, [AMOUNT, SECRET]);

// 4. Pack proof = numSigners(uint8) || sigs[0] || ... || extraData
const proof = ethers.concat([
  ethers.solidityPacked(["uint8"], [sigs.length]),
  ...sigs,
  ethers.solidityPacked(["uint8"], [0]),   // extraData v0
]);

// 5. Fulfill
await vault.fulfillReveal(vaultId, cleartexts, proof);
```

(Verify the proof packing format by reading `FHE.isPublicDecryptionResultValid` in [`@fhevm/solidity/lib/FHE.sol`](https://github.com/zama-ai/fhevm-solidity) — that function describes the exact layout.)

---

## Pre-deploy checklist (paste into PR description)

- [ ] Every callback that consumes `(bytes cleartexts, bytes proof)` calls `FHE.checkSignatures(handles, cleartexts, proof)` as its FIRST statement
- [ ] Every callback flips a `revealed`-style replay flag BEFORE writing cleartext or making external calls
- [ ] `handles[]` ordering and `abi.decode(cleartexts, (T1, T2, ...))` tuple ordering visually match line-by-line
- [ ] Every state-mutating function ends with `FHE.allowThis(ct)` for any new ciphertext handles
- [ ] User-facing functions also `FHE.allow(ct, msg.sender)` if the user should user-decrypt off-chain
- [ ] No `FHE.decrypt(...)` calls anywhere — only `makePubliclyDecryptable` + callback OR `allow` + frontend `userDecrypt`
- [ ] Time-locked reveals use the correct `>` / `>=` boundary and the choice is documented in a comment
- [ ] `triggerReveal`-style functions are idempotent so anyone can retry on relayer outage
- [ ] No `allowTransient` permissions are read across transactions
- [ ] `pragma solidity ^0.8.27;` with `evmVersion: "cancun"` (transient storage)

---

## Stack pinning

```
@fhevm/solidity:        ^0.11.1
@fhevm/hardhat-plugin:  ^0.4.2
@zama-fhe/relayer-sdk:  ^0.4.1
solidity:               0.8.27
evmVersion:             cancun
hardhat:                ^2.28.6
ethers:                 ^6.16.0
node:                   ≥20
```

---

## Source authority

Every claim in this skill is grounded in code we read at version-pin time:

- `@fhevm/solidity@0.11.1` `lib/FHE.sol` — `makePubliclyDecryptable`, `checkSignatures(handles, cleartexts, proof)`, `allowThis`, `allow`, `fromExternal`, `toBytes32` signatures verbatim.
- `zama-ai/fhevm/library-solidity/examples/OnchainPublicDecrypt.sol` — canonical 1-handle async-decrypt example.
- `zama-ai/fhevm/library-solidity/test/onchainPublicDecrypt/OnchainPublicDecrypt.ts` — canonical signature-verification test, including 1-of-1 and 2-of-3 KMS threshold cases.
- `@fhevm/hardhat-plugin@0.4.2` `src/internal/FhevmDebugger.ts` — `createDecryptionSignatures` API used in mock-mode tests.
- `zama-ai/dapps/.../BlindAuction.sol`, `.../FHEWordle.sol`, `.../SwapERC7984ToERC20.sol` — production usage of `FHE.checkSignatures(handles, cleartexts, proof)`.
- Zama documentation `docs.zama.ai/protocol` — KMS oracle architecture; async-only mainnet decision.

If you suspect this skill has drifted from the current library, re-verify against `lib/FHE.sol` before trusting the patterns here.
