import { expect } from "chai";
import { ethers, fhevm } from "hardhat";
import { time } from "@nomicfoundation/hardhat-network-helpers";
import { HardhatEthersSigner } from "@nomicfoundation/hardhat-ethers/signers";

import type { AsyncRevealVault } from "../types";

/**
 * Mock-mode tests for AsyncRevealVault. The @fhevm/hardhat-plugin auto-fulfills
 * decryption requests via `hre.fhevm.awaitDecryptionOracle()` — same pattern as
 * upstream zama-ai/fhevm-mocks/.../TestAsyncDecrypt.ts.
 *
 * Each `it` drills one SKILL.md anti-pattern from a USER perspective:
 *   - "rejects reveal before time" — AP-010 finality
 *   - "decrypts after revealAt"     — canonical happy path (REQUEST → RELAYER → FULFILL)
 *   - "rejects double-trigger"      — AP-002/008 single in-flight guard
 *   - "rejects unknown requestID"   — AP-002 callback after consume returns 0 lookup
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
      // The fhevm plugin is not in mock mode — Sepolia tests live in a separate file.
      this.skip();
    }

    [depositor, other] = await ethers.getSigners();

    const factory = await ethers.getContractFactory("AsyncRevealVault");
    vault = (await factory.connect(depositor).deploy()) as unknown as AsyncRevealVault;
    await vault.waitForDeployment();
    vaultAddress = await vault.getAddress();
  });

  /** Helper: encrypt (amount, secret) for `signer` against `vaultAddress`. */
  async function encryptInputs(signer: HardhatEthersSigner, amount: bigint, secret: bigint) {
    const enc = await fhevm
      .createEncryptedInput(vaultAddress, signer.address)
      .add64(amount)
      .add256(secret)
      .encrypt();
    return { encAmount: enc.handles[0], encSecret: enc.handles[1], proof: enc.inputProof };
  }

  /** Helper: lock a vault that reveals `secondsFromNow` from latest block timestamp. */
  async function lockVault(secondsFromNow: number): Promise<{ vaultId: bigint; revealAt: number }> {
    const now = await time.latest();
    const revealAt = now + secondsFromNow;
    const { encAmount, encSecret, proof } = await encryptInputs(depositor, AMOUNT, SECRET);

    const tx = await vault
      .connect(depositor)
      .lock(encAmount, encSecret, proof, revealAt);
    await tx.wait();

    // First lock → vaultId = 1.
    return { vaultId: await vault.nextVaultId(), revealAt };
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
  // Canonical happy path: REQUEST → RELAYER → FULFILL with cleartext landing.
  // Drills AP-001 (signature verified by FHE.checkSignatures inside callback)
  // and AP-003 (handle order matches callback parameter order).
  // ----------------------------------------------------------------------
  it("decrypts amount + secret after revealAt (canonical flow)", async function () {
    const { vaultId, revealAt } = await lockVault(1_000);

    // Strictly past revealAt.
    await time.setNextBlockTimestamp(revealAt + 1);

    const triggerTx = await vault.connect(other).triggerReveal(vaultId);
    await triggerTx.wait();

    // Plugin auto-fulfills the oracle request.
    await fhevm.awaitDecryptionOracle();

    expect(await vault.isRevealed(vaultId)).to.equal(true);
    const [clearAmount, clearSecret] = await vault.getClearValues(vaultId);
    expect(clearAmount).to.equal(AMOUNT);
    expect(clearSecret).to.equal(SECRET);
  });

  // ----------------------------------------------------------------------
  // AP-002 / AP-008: a second triggerReveal while a request is in flight reverts.
  // ----------------------------------------------------------------------
  it("rejects a second triggerReveal while one is in flight", async function () {
    const { vaultId, revealAt } = await lockVault(1_000);
    await time.setNextBlockTimestamp(revealAt + 1);

    const tx1 = await vault.connect(other).triggerReveal(vaultId);
    await tx1.wait();

    // BEFORE the relayer fulfills, a second trigger must revert.
    await expect(vault.connect(depositor).triggerReveal(vaultId)).to.be.revertedWithCustomError(
      vault,
      "RequestPending",
    );

    // After fulfillment, the `revealed` flag blocks further triggers via AlreadyRevealed.
    await fhevm.awaitDecryptionOracle();
    await expect(vault.connect(other).triggerReveal(vaultId)).to.be.revertedWithCustomError(
      vault,
      "AlreadyRevealed",
    );
  });

  // ----------------------------------------------------------------------
  // AP-001: only the KMS oracle (with valid signatures) can call fulfillReveal.
  // A direct user call must revert at FHE.checkSignatures.
  // ----------------------------------------------------------------------
  it("rejects fulfillReveal called directly with no signatures (AP-001)", async function () {
    const { vaultId, revealAt } = await lockVault(1_000);
    await time.setNextBlockTimestamp(revealAt + 1);

    const tx = await vault.connect(other).triggerReveal(vaultId);
    const receipt = await tx.wait();

    // Pull the requestID out of the RevealRequested event.
    const evt = receipt!.logs
      .map((l) => {
        try {
          return vault.interface.parseLog({ topics: l.topics as string[], data: l.data });
        } catch {
          return null;
        }
      })
      .find((x) => x?.name === "RevealRequested");
    const requestID = evt!.args.requestID as bigint;

    // No valid signatures — must revert (signature check is the FIRST line of the callback).
    await expect(
      vault.connect(other).fulfillReveal(requestID, AMOUNT, SECRET, []),
    ).to.be.reverted; // checkSignatures throws; specific revert reason comes from FHE library.
  });
});
