"use client";

import type { createInstance } from "@zama-fhe/relayer-sdk/web";

let instancePromise: Promise<Awaited<ReturnType<typeof createInstance>>> | null = null;

declare global {
  interface Window {
    ethereum?: import("ethers").Eip1193Provider;
  }
}

/**
 * Lazily initialise the FHEVM relayer SDK against Sepolia. The SDK is
 * dynamic-imported so its top-level `self` reference (a browser global)
 * never executes during Next.js SSR / static generation. The first call in
 * the browser loads the WASM TFHE engine, then `createInstance` downloads
 * the live KMS public key + CRS from the relayer.
 */
export async function getFhevm() {
  if (typeof window === "undefined") {
    throw new Error("FHEVM SDK runs in the browser only");
  }
  if (!window.ethereum) {
    throw new Error("Wallet not detected — install MetaMask or another EIP-1193 provider");
  }
  if (!instancePromise) {
    instancePromise = (async () => {
      const { initSDK, createInstance, SepoliaConfig } = await import(
        "@zama-fhe/relayer-sdk/web"
      );
      await initSDK();
      return createInstance({
        ...SepoliaConfig,
        network: window.ethereum!,
      });
    })();
  }
  return instancePromise;
}
