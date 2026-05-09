// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.27;

import {FHE, euint64, euint256, externalEuint64, externalEuint256} from "@fhevm/solidity/lib/FHE.sol";
import {ZamaEthereumConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

/// @title  AsyncRevealVault
/// @notice Time-locked reveal primitive: deposit an encrypted (amount, secret) pair,
///         decrypt it via the KMS oracle only after `revealAt`. Demonstrates the
///         canonical 3-step async-decryption pattern from `fhevm-oracle` SKILL.md.
/// @dev    Drills SKILL.md anti-patterns: signature check first (AP-001), guard
///         consume before any external call (AP-002 / AP-008), handle order matches
///         callback parameter order (AP-003), ACL discipline after every state mutation
///         (AP-004), strict `>` finality on revealAt (AP-010).
contract AsyncRevealVault is ZamaEthereumConfig {
    // -----------------------------------------------------------------
    // Storage
    // -----------------------------------------------------------------

    struct Vault {
        euint64  amount;                // encrypted at lock(), decrypted at fulfillReveal()
        euint256 secret;                // encrypted at lock(), decrypted at fulfillReveal()
        uint256  revealAt;              // unix seconds; reveal allowed when block.timestamp > revealAt
        address  depositor;
        uint256  outstandingRequestID;  // 0 = no pending request, type(uint256).max = consumed
        bool     revealed;
        uint64   clearAmount;           // populated by fulfillReveal()
        uint256  clearSecret;           // populated by fulfillReveal()
    }

    /// @dev sentinel written to a vault's outstandingRequestID after the callback
    ///      consumes it. Any subsequent callback that hits this vault aborts.
    uint256 private constant CONSUMED = type(uint256).max;

    uint256 public nextVaultId;
    mapping(uint256 vaultId => Vault) public vaults;
    mapping(uint256 requestID => uint256 vaultId) public requestToVault;

    // -----------------------------------------------------------------
    // Events
    // -----------------------------------------------------------------

    event Locked(uint256 indexed vaultId, address indexed depositor, uint256 revealAt);
    event RevealRequested(uint256 indexed vaultId, uint256 indexed requestID);
    event Revealed(uint256 indexed vaultId, uint64 amount, uint256 secret);
    event RequestCanceled(uint256 indexed vaultId, uint256 indexed requestID);

    // -----------------------------------------------------------------
    // Errors
    // -----------------------------------------------------------------

    error RevealTooEarly();          // block.timestamp <= revealAt
    error AlreadyRevealed();
    error RequestPending();          // a previous triggerReveal is still in flight
    error UnknownRequest();          // callback for a vault that already consumed
    error NotDepositor();
    error CancelTooEarly();          // grace window for relayer outage not elapsed yet
    error NoPendingRequest();

    /// @dev grace window after revealAt during which only the relayer may fulfill.
    ///      Past this, the depositor can `cancelOutstandingRequest` and re-trigger.
    ///      24h matches the SKILL.md AP-009 fallback recommendation.
    uint256 public constant CANCEL_GRACE = 1 days;

    // -----------------------------------------------------------------
    // Lock — accept encrypted (amount, secret) and a release timestamp
    // -----------------------------------------------------------------

    /// @notice Deposit an encrypted amount + secret that becomes decryptable after `revealAt`.
    /// @param  encAmount  client-encrypted euint64 amount
    /// @param  encSecret  client-encrypted euint256 secret
    /// @param  proof      ZK input proof binding both ciphertexts to msg.sender + this contract
    /// @param  revealAt   unix timestamp; reveal allowed strictly AFTER this moment
    function lock(
        externalEuint64  encAmount,
        externalEuint256 encSecret,
        bytes calldata   proof,
        uint256          revealAt
    ) external returns (uint256 vaultId) {
        // proof verifies BOTH handles + the (sender, this) binding in one call.
        euint64  amount = FHE.fromExternal(encAmount, proof);
        euint256 secret = FHE.fromExternal(encSecret, proof);

        vaultId = ++nextVaultId;

        Vault storage v = vaults[vaultId];
        v.amount    = amount;
        v.secret    = secret;
        v.revealAt  = revealAt;
        v.depositor = msg.sender;

        // SKILL.md AP-004: keep ciphertext usable across txs by re-allowing self.
        FHE.allowThis(amount);
        FHE.allowThis(secret);
        // Allow the depositor to user-decrypt their own values off-chain at any time.
        FHE.allow(amount, msg.sender);
        FHE.allow(secret, msg.sender);

        emit Locked(vaultId, msg.sender, revealAt);
    }

    // -----------------------------------------------------------------
    // Trigger — ask the KMS oracle to decrypt (after revealAt)
    // -----------------------------------------------------------------

    /// @notice After `revealAt`, anyone can ask the relayer to decrypt the vault.
    /// @dev    Single in-flight request per vault. SKILL.md canonical step REQUEST.
    function triggerReveal(uint256 vaultId) external returns (uint256 requestID) {
        Vault storage v = vaults[vaultId];

        if (v.depositor == address(0))     revert UnknownRequest();
        if (v.revealed)                    revert AlreadyRevealed();
        // AP-010: strict `>` — the second equal to revealAt is the FIRST allowed.
        if (block.timestamp <= v.revealAt) revert RevealTooEarly();

        // Single in-flight: outstandingRequestID must be 0 (never used) or CONSUMED.
        // We re-use CONSUMED as "callback already ran" — that path is blocked by `revealed`.
        if (v.outstandingRequestID != 0 && v.outstandingRequestID != CONSUMED) {
            revert RequestPending();
        }

        // AP-003: handles[0]=amount, handles[1]=secret — callback parameter order MUST
        // match this exactly (uint64 amount, uint256 secret).
        bytes32[] memory handles = new bytes32[](2);
        handles[0] = euint64.unwrap(v.amount);
        handles[1] = euint256.unwrap(v.secret);

        requestID = FHE.requestDecryption(handles, this.fulfillReveal.selector);

        v.outstandingRequestID = requestID;
        requestToVault[requestID] = vaultId;

        emit RevealRequested(vaultId, requestID);
    }

    // -----------------------------------------------------------------
    // Fulfill — the KMS oracle calls this with cleartext + signatures
    // -----------------------------------------------------------------

    /// @notice KMS callback. SKILL.md canonical step FULFILL.
    /// @dev    Signature MUST be: (uint256 requestID, decoded values..., bytes[] signatures).
    ///         Decoded values appear in the same order as handles[] passed to requestDecryption.
    function fulfillReveal(
        uint256        requestID,
        uint64         amount,
        uint256        secret,
        bytes[] memory signatures
    ) external {
        // AP-001: signature verification BEFORE any state read or write. Without this,
        // anyone can call this selector with arbitrary cleartext — a fake-decryption.
        FHE.checkSignatures(requestID, signatures);

        uint256 vaultId = requestToVault[requestID];
        if (vaultId == 0) revert UnknownRequest();

        Vault storage v = vaults[vaultId];

        // AP-002 / AP-008: consume the guard BEFORE writing the cleartext / emitting.
        // Two parallel mappings cleared atomically — a second callback for this requestID
        // hits requestToVault[requestID] == 0 above and reverts with UnknownRequest.
        delete requestToVault[requestID];
        v.outstandingRequestID = CONSUMED;

        v.revealed     = true;
        v.clearAmount  = amount;
        v.clearSecret  = secret;

        emit Revealed(vaultId, amount, secret);
    }

    // -----------------------------------------------------------------
    // Cancel — relayer-outage fallback (SKILL.md AP-009)
    // -----------------------------------------------------------------

    /// @notice If the KMS callback never fires within `CANCEL_GRACE` after revealAt,
    ///         the depositor can drop the in-flight request and call `triggerReveal` again.
    /// @dev    Only the depositor can cancel. The cancellation invalidates the previous
    ///         requestID — if it lands later, `requestToVault[requestID] == 0` aborts it.
    function cancelOutstandingRequest(uint256 vaultId) external {
        Vault storage v = vaults[vaultId];

        if (v.depositor != msg.sender)               revert NotDepositor();
        if (v.revealed)                              revert AlreadyRevealed();
        if (v.outstandingRequestID == 0)             revert NoPendingRequest();
        if (v.outstandingRequestID == CONSUMED)      revert NoPendingRequest();
        if (block.timestamp <= v.revealAt + CANCEL_GRACE) revert CancelTooEarly();

        uint256 stale = v.outstandingRequestID;
        delete requestToVault[stale];
        v.outstandingRequestID = 0; // back to "no request" — depositor may re-trigger

        emit RequestCanceled(vaultId, stale);
    }

    // -----------------------------------------------------------------
    // Views — convenience accessors (the public mapping already exposes structs,
    // but typed getters read better in tests + frontend).
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
