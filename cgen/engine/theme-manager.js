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

  // 3. Apply brand identity to shell (if present)
  if (brand) {
    if (brand.logo) {
      const logoEl = document.getElementById("brandLogo");
      if (logoEl) {
        logoEl.src = brand.logo;
        logoEl.alt = brand.displayName || brandName;
      }
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
