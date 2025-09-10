/** @type {import('next').NextConfig} */
const nextConfig = {
    basePath: "/doc",
    assetPrefix: process.env.NEXT_PUBLIC_ASSET_PREFIX || "http://localhost:3000/doc/",
    eslint: { ignoreDuringBuilds: true },
    typescript: { ignoreBuildErrors: true },
    images: { unoptimized: true },
    output: "standalone",
  };
  
  export default nextConfig;
  