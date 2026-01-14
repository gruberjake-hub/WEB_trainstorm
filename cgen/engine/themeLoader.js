export function loadTheme(themeName) {
  if (!themeName) return;

  const basePath = "../../brands/" + themeName;

  const stylesheets = [
    `${basePath}/${themeName}-tokens.css`,
    `${basePath}/${themeName}-layout.css`,
    `${basePath}/${themeName}-components.css`
  ];

  stylesheets.forEach(href => {
    if (document.querySelector(`link[href="${href}"]`)) return;

    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  });
}
