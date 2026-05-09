import { expect } from "chai";
import { ethers, fhevm } from "hardhat";
import { time } from "@nomicfoundation/hardhat-network-helpers";
import { HardhatEthersSigner } from "@nomicfoundation/hardhat-ethers/signers";

import type { AsyncRevealVault } from "../types";

/**
 * Mock-mode tests for AsyncRevealVault. fhevm-solidity 0.11.1 has no
 * `requestDecryption` oracle — public decryption is driven by
 * `FHE.makePubliclyDecryptable(handle)` plus a separate caller-supplied
 * `fulfillReveal(cleartexts, proof)` callback. The mock plugin gives us
 * `hre.fhevm.debugger.createDecryptionSignatures` to forge the KMS proof
 * inside the test.
 *
 * Each `it` drills one SKILL.md anti-pattern from a USER perspective:
 *   - "rejects reveal before time"        — AP-010 strict `>` finality
 *   - "decrypts after revealAt"           — canonical happy path (TRIGGER → FULFILL)
 *   - "rejects double fulfillReveal"      — AP-002 replay guard before any write
 *   - "rejects fulfillReveal without sig" — AP-001 checkSignatures FIRST
 */
describe("AsyncRevealVault", function () {
  let depositor: HardhatEthersSigner;
  let other: HardhatEthersSigner;
  let vault: AsyncRevealVault;
  let vaultAddress: string;

  const AMOUNT = 12_345n;
  const SECRET = 0xc0ffeen;

  beforeEach(async function () {
    if (!fhevm.isMock) {
      // Sepolia tests live in a separate file — mock plugin only.
      this.skip();
    }

    [depositor, other] = await ethers.getSigners();

    const factory = await ethers.getContractFactory("AsyncRevealVault");
    vault = (await factory.connect(depositor).deploy()) as unknown as AsyncRevealVault;
    await vault.waitForDeployment();
    vaultAddress = await vault.getAddress();
  });

  /** Encrypt (amount, secret) for `signer` against `vaultAddress`. */
  async function encryptInputs(signer: HardhatEthersSigner, amount: bigint, secret: bigint) {
    const enc = await fhevm
      .createEncryptedInput(vaultAddress, signer.address)
      .add64(amount)
      .add256(secret)
      .encrypt();
    return { encAmount: enc.handles[0], encSecret: enc.handles[1], proof: enc.inputProof };
  }

  /** Lock a vault that reveals `secondsFromNow` after the latest block. */
  async function lockVault(secondsFromNow: number): Promise<{ vaultId: bigint; revealAt: number }> {
    const now = await time.latest();
    const revealAt = now + secondsFromNow;
    const { encAmount, encSecret, proof } = await encryptInputs(depositor, AMOUNT, SECRET);

    const tx = await vault.connect(depositor).lock(encAmount, encSecret, proof, revealAt);
    await tx.wait();

    return { vaultId: await vault.nextVaultId(), revealAt };
  }

  /**
   * Default mock-mode KMS signer (verified in
   *   `node_modules/@fhevm/hardhat-plugin/src/internal/constants.ts`
   *   PRIVATE_KEY_KMS_SIGNER → 0x0971C80fF03B428fD2094dd5354600ab103201C5).
   * Threshold is 1, so a single signature is sufficient.
   */
  const KMS_SIGNER_PK =
    "0x388b7680e4e1afa06efbfd45cdd1fe39f3c6af381df6555a19661f283b97de91";
  // `ZamaEthereumConfig` switches by `block.chainid`: hardhat (31337) uses
  // the LocalConfig KMSVerifier, NOT the mainnet one. Ref:
  // `node_modules/@fhevm/solidity/config/ZamaConfig.sol getEthereumCoprocessorConfig`.
  const KMS_VERIFIER_ADDRESS = "0x901F8942346f7AB3a01F6D7613119Bca447Bb030";

  /**
   * Build the `(cleartexts, decryptionProof)` pair the KMS would produce for
   * the given vault. The KMS encodes every cleartext value as `uint256`
   * regardless of underlying euint type, then signs `(handles, cleartexts,
   * extraData)` over the EIP-712 `PublicDecryptVerification` typed data of
   * the KMSVerifier contract. The dApp callback decodes to its declared
   * widths (uint64 / uint256 here) — the bytes are identical to
   * `abi.encode(uint256, uint256)` for any value that fits in the narrower
   * type, which is what we rely on.
   *
   * Proof layout (verified against
   *   `node_modules/@fhevm/solidity/lib/FHE.sol` `isPublicDecryptionResultValid`
   *   and `node_modules/@fhevm/mock-utils/.../KMSVerifier.ts buildDecryptionProof`):
   *     numSigners(uint8) || sig0 || sig1 || ... || extraData(uint8 = v0 = 0)
   *
   * AP-003: handles[] order MUST match the abi.decode tuple order in the
   * dApp callback. A swap here would yield a "valid" KMS signature pointing
   * the wrong cleartext at the wrong slot.
   */
  async function buildKmsProof(vaultId: bigint) {
    const handlesBytes32Hex = [
      await vault.getEncryptedAmount(vaultId),
      await vault.getEncryptedSecret(vaultId),
    ];

    const cleartexts = ethers.AbiCoder.defaultAbiCoder().encode(
      ["uint256", "uint256"],
      [AMOUNT, SECRET],
    );
    const extraData = "0x00"; // v0 marker

    const kmsVerifier = new ethers.Contract(
      KMS_VERIFIER_ADDRESS,
      [
        "function eip712Domain() view returns (bytes1 fields, string name, string version, uint256 chainId, address verifyingContract, bytes32 salt, uint256[] extensions)",
      ],
      ethers.provider,
    );
    const [, name, version, chainId, verifyingContract] =
      await kmsVerifier.eip712Domain();

    const domain = {
      name,
      version,
      chainId,
      verifyingContract,
    };
    const types = {
      PublicDecryptVerification: [
        { name: "ctHandles", type: "bytes32[]" },
        { name: "decryptedResult", type: "bytes" },
        { name: "extraData", type: "bytes" },
      ],
    };
    const message = {
      ctHandles: handlesBytes32Hex,
      decryptedResult: cleartexts,
      extraData,
    };

    const kmsWallet = new ethers.Wallet(KMS_SIGNER_PK);
    const sig = await kmsWallet.signTypedData(domain, types, message);

    const proof = ethers.concat([
      ethers.solidityPacked(["uint8"], [1]),
      sig,
      extraData,
    ]);

    return { cleartexts, proof, handlesBytes32Hex };
  }

  // ----------------------------------------------------------------------
  // AP-010: finality strict `>` — reveal at exactly revealAt is too early.
  // ----------------------------------------------------------------------
  it("rejects triggerReveal before revealAt (AP-010 finality)", async function () {
    const { vaultId, revealAt } = await lockVault(1_000);

    await expect(vault.connect(other).triggerReveal(vaultId)).to.be.revertedWithCustomError(
      vault,
      "RevealTooEarly",
    );

    // At exactly revealAt — STILL too early per `>` semantics in the contract.
    await time.setNextBlockTimestamp(revealAt);
    await expect(vault.connect(other).triggerReveal(vaultId)).to.be.revertedWithCustomError(
      vault,
      "RevealTooEarly",
    );
  });

  // ----------------------------------------------------------------------
  // Canonical happy path: TRIGGER → FULFILL with KMS-signed cleartext landing.
  // Drills AP-001 (checkSignatures verifies the KMS proof) and AP-003
  // (handle order matches abi.decode tuple).
  // ----------------------------------------------------------------------
  it("decrypts amount + secret after revealAt (canonical flow)", async function () {
    const { vaultId, revealAt } = await lockVault(1_000);

    await time.setNextBlockTimestamp(revealAt + 1);

    await (await vault.connect(other).triggerReveal(vaultId)).wait();

    const { cleartexts, proof } = await buildKmsProof(vaultId);
    await (await vault.connect(other).fulfillReveal(vaultId, cleartexts, proof)).wait();

    expect(await vault.isRevealed(vaultId)).to.equal(true);
    const [clearAmount, clearSecret] = await vault.getClearValues(vaultId);
    expect(clearAmount).to.equal(AMOUNT);
    expect(clearSecret).to.equal(SECRET);
  });

  // ----------------------------------------------------------------------
  // AP-002: replay guard — once revealed, a second fulfillReveal must
  // revert BEFORE re-running the signature/decode work.
  // ----------------------------------------------------------------------
  it("rejects a second fulfillReveal after a successful one (AP-002 replay)", async function () {
    const { vaultId, revealAt } = await lockVault(1_000);
    await time.setNextBlockTimestamp(revealAt + 1);
    await (await vault.connect(other).triggerReveal(vaultId)).wait();

    const { cleartexts, proof } = await buildKmsProof(vaultId);
    await (await vault.connect(other).fulfillReveal(vaultId, cleartexts, proof)).wait();

    await expect(
      vault.connect(other).fulfillReveal(vaultId, cleartexts, proof),
    ).to.be.revertedWithCustomError(vault, "AlreadyRevealed");
  });

  // ----------------------------------------------------------------------
  // AP-001: only KMS-signed cleartexts pass. A direct call with an empty /
  // forged proof must revert at FHE.checkSignatures, BEFORE any state read.
  // ----------------------------------------------------------------------
  it("rejects fulfillReveal with no valid signatures (AP-001)", async function () {
    const { vaultId, revealAt } = await lockVault(1_000);
    await time.setNextBlockTimestamp(revealAt + 1);
    await (await vault.connect(other).triggerReveal(vaultId)).wait();

    const cleartexts = ethers.AbiCoder.defaultAbiCoder().encode(
      ["uint256", "uint256"],
      [AMOUNT, SECRET],
    );
    // Zero signers + valid extraData byte. KMSVerifier requires >=
    // threshold real KMS signatures, so this MUST revert.
    const bogusProof = ethers.concat([
      ethers.solidityPacked(["uint8"], [0]),
      ethers.solidityPacked(["uint8"], [0]),
    ]);

    await expect(vault.connect(other).fulfillReveal(vaultId, cleartexts, bogusProof)).to.be
      .reverted;
    expect(await vault.isRevealed(vaultId)).to.equal(false);
  });
});
