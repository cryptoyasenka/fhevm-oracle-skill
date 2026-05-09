import { DeployFunction } from "hardhat-deploy/types";
import { HardhatRuntimeEnvironment } from "hardhat/types";

/**
 * Sepolia deploy for the Builder Track demo. Run with:
 *   npx hardhat vars set MNEMONIC
 *   npx hardhat vars set INFURA_API_KEY
 *   npm run deploy:sepolia
 *
 * Mock-network deploy is supported too (handy for the frontend dev loop):
 *   npm run deploy:hardhat
 */
const deploy: DeployFunction = async function (hre: HardhatRuntimeEnvironment) {
  const { deployments, getNamedAccounts } = hre;
  const { deploy } = deployments;
  const { deployer } = await getNamedAccounts();

  const counter = await deploy("FHECounter", {
    from: deployer,
    log: true,
    args: [],
  });

  const vault = await deploy("AsyncRevealVault", {
    from: deployer,
    log: true,
    args: [],
  });

  console.log(`FHECounter        : ${counter.address}`);
  console.log(`AsyncRevealVault  : ${vault.address}`);
  console.log(`Network           : ${hre.network.name} (chainId=${hre.network.config.chainId})`);
};

export default deploy;
deploy.tags = ["AsyncRevealVault", "FHECounter"];
