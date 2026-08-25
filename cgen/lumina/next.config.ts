import path from "node:path";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Keep this app self-contained even though cgen/ already has a lockfile.
  outputFileTracingRoot: path.join(__dirname),
};

export default nextConfig;
