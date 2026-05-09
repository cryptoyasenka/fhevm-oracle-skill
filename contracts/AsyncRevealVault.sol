// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.27;

import {FHE, euint64, euint256, externalEuint64, externalEuint256} from "@fhevm/solidity/lib/FHE.sol";
import {ZamaEthereumConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

/// @title  AsyncRevealVault
/// @notice Time-locked reveal primitive: deposit an encrypted (amount, secret) pair,
///         decrypt it via the KMS only after `revealAt`. Demonstrates the canonical
///         3-step async-decryption pattern from `fhevm-oracle` SKILL.md as it actually
///         exists in @fhevm/solidity 0.11.1 — `makePubliclyDecryptable` + a callback
///         that verifies signatures with `FHE.checkSignatures(handles, cleartexts, proof)`.
/// @dev    Drills SKILL.md anti-patterns:
///           AP-001 — checkSignatures FIRST in fulfillReveal (else fake decryption)
///           AP-002 — replay guard (`revealed` flag) before any state write
///           AP-003 — handles[] order in fulfillReveal MUST match abi.decode tuple order
///           AP-004 — `allowThis` after every state mutation in lock()
///           AP-005 — `allow(_, depositor)` so the depositor can also user-decrypt off-chain
///           AP-010 — strict `>` finality on revealAt
contract AsyncRevealVault is ZamaEthereumConfig {
    // -----------------------------------------------------------------
    // Storage
    // -----------------------------------------------------------------

    struct Vault {
        euint64  amount;
        euint256 secret;
        uint256  revealAt;
        address  depositor;
        bool     revealed;
        uint64   clearAmount;
        uint256  clearSecret;
    }

    uint256 public nextVaultId;
    mapping(uint256 vaultId => Vault) public vaults;

    // -----------------------------------------------------------------
    // Events
    // -----------------------------------------------------------------

    event Locked(uint256 indexed vaultId, address indexed depositor, uint256 revealAt);
    /// @dev Emitted when both ciphertexts have been flagged for KMS decryption. An
    ///      off-chain relayer is expected to fetch the cleartext + KMS proof and call
    ///      `fulfillReveal(vaultId, cleartexts, proof)`.
    event RevealRequested(uint256 indexed vaultId);
    event Revealed(uint256 indexed vaultId, uint64 amount, uint256 secret);

    // -----------------------------------------------------------------
    // Errors
    // -----------------------------------------------------------------

    error RevealTooEarly();      // block.timestamp <= revealAt (AP-010)
    error AlreadyRevealed();     // anti-replay
    error UnknownVault();
    error NotDepositor();        // (reserved — depositor-only paths)

    // -----------------------------------------------------------------
    // Lock — accept encrypted (amount, secret) and a release timestamp
    // -----------------------------------------------------------------

    /// @notice Deposit an encrypted amount + secret that becomes decryptable after `revealAt`.
    /// @dev    The same `proof` covers both ciphertext handles thanks to single-call binding.
    function lock(
        externalEuint64  encAmount,
        externalEuint256 encSecret,
        bytes calldata   proof,
        uint256          revealAt
    ) external returns (uint256 vaultId) {
        euint64  amount = FHE.fromExternal(encAmount, proof);
        euint256 secret = FHE.fromExternal(encSecret, proof);

        vaultId = ++nextVaultId;

        Vault storage v = vaults[vaultId];
        v.amount    = amount;
        v.secret    = secret;
        v.revealAt  = revealAt;
        v.depositor = msg.sender;

        // AP-004: keep ciphertexts usable across txs by re-allowing self.
        FHE.allowThis(amount);
        FHE.allowThis(secret);
        // AP-005: let the depositor user-decrypt off-chain at any time.
        FHE.allow(amount, msg.sender);
        FHE.allow(secret, msg.sender);

        emit Locked(vaultId, msg.sender, revealAt);
    }

    // -----------------------------------------------------------------
    // Trigger — flag both ciphertexts for public KMS decryption
    // -----------------------------------------------------------------

    /// @notice After `revealAt`, anyone can request the KMS to decrypt the vault.
    /// @dev    Marks both ciphertexts as publicly decryptable. The KMS off-chain
    ///         picks up the event, decrypts, signs `(handles, cleartexts)`, and a
    ///         relayer submits the proof via `fulfillReveal`. Idempotent — a second
    ///         call before fulfillment is harmless: `makePubliclyDecryptable` is
    ///         a no-op on already-flagged handles.
    function triggerReveal(uint256 vaultId) external {
        Vault storage v = vaults[vaultId];
        if (v.depositor == address(0))      revert UnknownVault();
        if (v.revealed)                     revert AlreadyRevealed();
        // AP-010: strict `>` — at exactly revealAt is too early.
        if (block.timestamp <= v.revealAt)  revert RevealTooEarly();

        FHE.makePubliclyDecryptable(v.amount);
        FHE.makePubliclyDecryptable(v.secret);

        emit RevealRequested(vaultId);
    }

    // -----------------------------------------------------------------
    // Fulfill — KMS-signed cleartext callback
    // -----------------------------------------------------------------

    /// @notice Submit KMS-signed cleartexts for a previously-triggered vault.
    /// @dev    SKILL.md FULFILL step. The signature on `(handles, cleartexts)` proves
    ///         the cleartexts came from the KMS for THIS vault's exact ciphertext
    ///         handles — anyone can call this, but only with a real KMS proof.
    ///
    ///         Anti-patterns drilled here:
    ///         - AP-001: `FHE.checkSignatures` is the FIRST line — without it, anyone
    ///                   could submit arbitrary cleartext.
    ///         - AP-002: `revealed = true` consumed BEFORE state writes for the same
    ///                   reason a checks-effects-interactions pattern matters.
    ///         - AP-003: handles[] order MUST match the abi.decode tuple order. A swap
    ///                   would let a real KMS proof for vault A land in vault B's slot.
    function fulfillReveal(
        uint256        vaultId,
        bytes calldata abiEncodedCleartexts,
        bytes calldata decryptionProof
    ) external {
        Vault storage v = vaults[vaultId];
        if (v.depositor == address(0))      revert UnknownVault();
        if (v.revealed)                     revert AlreadyRevealed();
        if (block.timestamp <= v.revealAt)  revert RevealTooEarly();

        // AP-003: handles[] ordering must match the abi.decode tuple order below.
        bytes32[] memory handles = new bytes32[](2);
        handles[0] = FHE.toBytes32(v.amount);
        handles[1] = FHE.toBytes32(v.secret);

        // AP-001: signature verification BEFORE any state read or write. Without this,
        // anyone can call this selector with arbitrary cleartext — fake decryption.
        FHE.checkSignatures(handles, abiEncodedCleartexts, decryptionProof);

        // AP-002: consume the replay guard BEFORE writing the cleartext / emitting.
        v.revealed = true;

        // AP-003 again: tuple order MUST match handles[0], handles[1].
        (uint64 clearAmount, uint256 clearSecret) =
            abi.decode(abiEncodedCleartexts, (uint64, uint256));

        v.clearAmount = clearAmount;
        v.clearSecret = clearSecret;

        emit Revealed(vaultId, clearAmount, clearSecret);
    }

    // -----------------------------------------------------------------
    // Views
    // -----------------------------------------------------------------

    function getEncryptedAmount(uint256 vaultId) external view returns (euint64) {
        return vaults[vaultId].amount;
    }

    function getEncryptedSecret(uint256 vaultId) external view returns (euint256) {
        return vaults[vaultId].secret;
    }

    function getRevealAt(uint256 vaultId) external view returns (uint256) {
        return vaults[vaultId].revealAt;
    }

    function isRevealed(uint256 vaultId) external view returns (bool) {
        return vaults[vaultId].revealed;
    }

    function getClearValues(uint256 vaultId) external view returns (uint64, uint256) {
        Vault storage v = vaults[vaultId];
        return (v.clearAmount, v.clearSecret);
    }
}
