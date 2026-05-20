import fs from "fs";
import path from "path";

const ASSETS_DIR = path.resolve("assets");
const OUTPUT_FILE = path.join(ASSETS_DIR, "asset-index.json");

const index = {};
const errors = [];

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      walk(fullPath);
    }

    if (entry.isFile() && entry.name.endsWith(".asset.json")) {
      processManifest(fullPath);
    }
  }
}

function processManifest(manifestPath) {
  try {
    const raw = fs.readFileSync(manifestPath, "utf-8");
    const manifest = JSON.parse(raw);

    const { id, type, path: assetPath, restrictions, purpose, intended_use } = manifest;

    if (!id || !type || !assetPath) {
      errors.push(`Missing required fields in ${manifestPath}`);
      return;
    }

    if (index[id]) {
      errors.push(`Duplicate asset id "${id}" in ${manifestPath}`);
      return;
    }

    const resolvedAssetPath = path.resolve(assetPath);
    if (!fs.existsSync(resolvedAssetPath)) {
      errors.push(`Asset file not found for "${id}": ${assetPath}`);
    }

    index[id] = {
      type,
      path: "/" + assetPath.replace(/\\/g, "/"),
      restrictions: restrictions || {},
      purpose,
      intended_use
    };
  } catch (e) {
    errors.push(`Failed to parse ${manifestPath}: ${e.message}`);
  }
}

console.log("🔍 Scanning asset manifests...");
walk(ASSETS_DIR);

if (errors.length) {
  console.warn("⚠ Asset index warnings:");
  errors.forEach(e => console.warn("  -", e));
}

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(index, null, 2));
console.log(`✅ Asset index written to ${OUTPUT_FILE}`);
