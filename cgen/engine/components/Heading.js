export function Heading({ props }) {
  const level = Math.min(6, Math.max(1, props.level || 2));
  const el = document.createElement(`h${level}`);
  el.textContent = props.text || "";
  return el;
}
