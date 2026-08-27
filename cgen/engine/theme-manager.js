import { loadBrand, brandPackUrl, themeFromMeta } from "./brandLoader.js";
import { loadTheme } from "./themeLoader.js";

export async function applyBranding(meta = {}) {
  const brandName = themeFromMeta(meta);

  if (!brandName) {
    console.warn("No brand specified in course meta");
    return;
  }

  // 1. Load brand identity (metadata, rules, logo, constraints)
  const brand = await loadBrand(brandName);

  // 2. Apply brand styles (tokens, layout, components)
  loadTheme(brandName);

  // 3. Apply brand identity to shell (logo, metadata)
  const packName = brand?.brand || brandName;
  const logo = brand?.logos?.primary || brand?.logos?.inverse || null;
  const logoEl = document.getElementById("brandLogo");

  if (logoEl && logo?.src) {
    logoEl.src = brandPackUrl(packName, logo.src);
    logoEl.alt = logo.alt || packName;
    logoEl.hidden = false;
  }

  if (brand) {
    window.__ACTIVE_BRAND__ = brand;
  }

  // 4. Apply root class for CSS scoping
  const app = document.getElementById("app");
  if (app) {
    app.classList.add(`brand-${brandName}`);
  }
}
