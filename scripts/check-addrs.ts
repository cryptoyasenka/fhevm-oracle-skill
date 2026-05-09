import { ethers, fhevm } from "hardhat";

async function main() {
  await fhevm; // ensure init
  const provider = ethers.provider;
  for (const addr of [
    "0x77627828a55156b04Ac0DC0eb30467f1a552BB03",
    "0xbE0E383937d564D7FF0BC3b46c51f0bF8d5C311A",
    "0x901F8942346f7AB3a01F6D7613119Bca447Bb030",
  ]) {
    const code = await provider.getCode(addr);
    console.log(addr, code.length, code.slice(0, 40));
  }
}
main().then(() => process.exit(0));
