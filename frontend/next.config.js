/** @type {import('next').NextConfig} */
const nextConfig = {
  // standalone output keeps the deploy footprint small and host-agnostic —
  // works on Vercel (current host), Railway, Cloudflare Workers Containers,
  // or any docker host that can run `node server.js`.
  output: "standalone",
  reactStrictMode: true,
  webpack: (config) => {
    // The relayer SDK ships a WASM blob (TFHE-rs). Next/webpack 5 needs this
    // flag to async-load it on the client.
    config.experiments = { ...config.experiments, asyncWebAssembly: true };
    return config;
  },
};

module.exports = nextConfig;
