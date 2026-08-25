import path from "node:path";
import type { NextConfig } from "next";

// Production (Netlify) lives at https://trainstorm.ai/cgen/lumina.
// `next dev` keeps NODE_ENV=development so local studio stays at http://localhost:3000/.
const basePath =
  process.env.DEPLOY_PATH || (process.env.NODE_ENV === "production" ? "/cgen/lumina" : "");

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "export",
  images: { unoptimized: true },
  basePath,
  // Keep this app self-contained even though cgen/ already has a lockfile.
  outputFileTracingRoot: path.join(__dirname),
};

export default nextConfig;
