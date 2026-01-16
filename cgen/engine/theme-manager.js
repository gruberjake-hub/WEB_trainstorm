import { loadBrand } from "./brandLoader.js";
import { loadTheme } from "./themeLoader.js";

export async function applyBranding(meta = {}) {
  const brandName = meta.client || meta.brand || meta.theme;

  if (!brandName) {
    console.warn("No brand specified in course meta");
    return;
  }

  // 1. Load brand identity (metadata, rules, logo, constraints)
  const brand = await loadBrand(brandName);

  // 2. Apply brand styles (tokens, layout, components)
  loadTheme(brandName);

  // 3. Apply brand identity to shell (logo, metadata)
  if (brand && brand.logos && brand.logos.primary) {
    const logoEl = document.getElementById("brandLogo");

    if (logoEl) {
      logoEl.src = `../../brands/${brand.brand}/${brand.logos.primary.src}`;
      logoEl.alt = brand.logos.primary.alt || brand.brand;
    }

    // Optional: expose brand to runtime later
    window.__ACTIVE_BRAND__ = brand;
  }

  // 4. Apply root class for CSS scoping
  const app = document.getElementById("app");
  if (app) {
    app.classList.add(`brand-${brandName}`);
  }
}
