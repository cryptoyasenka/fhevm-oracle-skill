/** @type {import('next').NextConfig} */
const nextConfig = {
  // standalone output keeps the deploy footprint small on Railway / Cloudflare
  // Workers Containers / any docker host. NOT vercel-specific.
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
