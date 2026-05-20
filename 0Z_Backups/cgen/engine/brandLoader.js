// engine/brandLoader.js
// Responsibility: load brand identity metadata (logos, rules)
// and expose it to the runtime/shell

export async function loadBrand(themeName) {
  if (!themeName) return null;

  const brandPath = `../../brands/${themeName}/${themeName}-brand.json`;

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
