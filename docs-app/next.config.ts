/** @type {import('next').NextConfig} */
const nextConfig = {
    basePath: "/doc",
    assetPrefix: process.env.ASSET_PREFIX || "http://localhost:3001/doc/",
    eslint: { ignoreDuringBuilds: true },
    typescript: { ignoreBuildErrors: true },
    images: { unoptimized: true },
    output: "standalone",
  };
  
  export default nextConfig;
  