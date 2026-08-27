import { brandPackUrl } from "./brandLoader.js";

export function loadTheme(themeName) {
  if (!themeName) return;

  const stylesheets = [
    `${themeName}-tokens.css`,
    `${themeName}-layout.css`,
    `${themeName}-components.css`
  ].map((name) => brandPackUrl(themeName, name));

  stylesheets.forEach(href => {
    if (document.querySelector(`link[href="${href}"]`)) return;

    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  });
}
