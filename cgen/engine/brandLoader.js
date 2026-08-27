// engine/brandLoader.js
// Responsibility: load brand identity metadata (logos, rules)
// and expose it to the runtime/shell.
//
// Pack files live at cgen/brands/<name>/, sibling of this engine
// module. Resolve against import.meta.url so /cgen and /cgen/index.html
// (and other engine consumers) hit cgen/brands/, not site-root /brands/.

export function brandPackBase(themeName) {
  return new URL(`../brands/${themeName}/`, import.meta.url);
}

export function brandPackUrl(themeName, relativePath) {
  return new URL(relativePath, brandPackBase(themeName)).href;
}

/** Projection meta.theme wins. brand/client are aliases only. */
export function themeFromMeta(meta = {}) {
  return meta.theme || meta.brand || meta.client || null;
}

export async function loadBrand(themeName) {
  if (!themeName) return null;

  const brandPath = brandPackUrl(themeName, `${themeName}-brand.json`);

  try {
    const res = await fetch(brandPath);
    if (!res.ok) {
      console.warn(`Brand file not found: ${brandPath}`);
      return null;
    }

    const brand = await res.json();
    return brand;
  } catch (err) {
    console.error("Failed to load brand definition:", err);
    return null;
  }
}
