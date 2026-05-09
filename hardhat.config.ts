import "@fhevm/hardhat-plugin";
import "@nomicfoundation/hardhat-chai-matchers";
import "@nomicfoundation/hardhat-ethers";
import "@nomicfoundation/hardhat-verify";
import "@typechain/hardhat";
import "hardhat-deploy";
import "hardhat-gas-reporter";
import type { HardhatUserConfig } from "hardhat/config";
import { vars } from "hardhat/config";
import "solidity-coverage";

const MNEMONIC: string = vars.get(
  "MNEMONIC",
  "test test test test test test test test test test test junk",
);
const INFURA_API_KEY: string = vars.get("INFURA_API_KEY", "");
const PRIVATE_KEY_RAW: string = vars.get("PRIVATE_KEY", "");
const PRIVATE_KEY: string = PRIVATE_KEY_RAW
  ? PRIVATE_KEY_RAW.startsWith("0x")
    ? PRIVATE_KEY_RAW
    : `0x${PRIVATE_KEY_RAW}`
  : "";

const SEPOLIA_RPC_URL: string = vars.get(
  "SEPOLIA_RPC_URL",
  INFURA_API_KEY
    ? `https://sepolia.infura.io/v3/${INFURA_API_KEY}`
    : "https://ethereum-sepolia-rpc.publicnode.com",
);

const sepoliaAccounts = PRIVATE_KEY
  ? [PRIVATE_KEY]
  : {
      mnemonic: MNEMONIC,
      path: "m/44'/60'/0'/0/",
      count: 10,
    };

const config: HardhatUserConfig = {
  defaultNetwork: "hardhat",
  namedAccounts: {
    deployer: 0,
  },
  etherscan: {
    apiKey: {
      sepolia: vars.get("ETHERSCAN_API_KEY", ""),
    },
  },
  gasReporter: {
    currency: "USD",
    enabled: process.env.REPORT_GAS ? true : false,
    excludeContracts: [],
  },
  networks: {
    hardhat: {
      accounts: {
        mnemonic: MNEMONIC,
      },
      chainId: 31337,
    },
    sepolia: {
      accounts: sepoliaAccounts,
      chainId: 11155111,
      url: SEPOLIA_RPC_URL,
    },
  },
  paths: {
    artifacts: "./artifacts",
    cache: "./cache",
    sources: "./contracts",
    tests: "./test",
  },
  solidity: {
    version: "0.8.27",
    settings: {
      metadata: {
        bytecodeHash: "none",
      },
      optimizer: {
        enabled: true,
        runs: 800,
      },
      evmVersion: "cancun",
    },
  },
  typechain: {
    outDir: "types",
    target: "ethers-v6",
  },
};

export default config;
