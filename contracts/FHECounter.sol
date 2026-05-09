// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.27;

import {FHE, euint32, externalEuint32} from "@fhevm/solidity/lib/FHE.sol";
import {ZamaEthereumConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

/// @title  FHECounter — sanity check that the project compiles + the FHEVM dev env works.
/// @notice Mirrors the canonical hello-world from zama-ai/fhevm-hardhat-template.
///         The bounty-track demo lives in `AsyncRevealVault.sol`.
contract FHECounter is ZamaEthereumConfig {
    euint32 private _count;

    function getCount() external view returns (euint32) {
        return _count;
    }

    function increment(externalEuint32 input, bytes calldata proof) external {
        euint32 v = FHE.fromExternal(input, proof);
        _count = FHE.add(_count, v);
        FHE.allowThis(_count);
        FHE.allow(_count, msg.sender);
    }

    function decrement(externalEuint32 input, bytes calldata proof) external {
        euint32 v = FHE.fromExternal(input, proof);
        _count = FHE.sub(_count, v);
        FHE.allowThis(_count);
        FHE.allow(_count, msg.sender);
    }
}
