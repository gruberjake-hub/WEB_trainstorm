export function Heading({ props }) {
  const wrap = document.createElement("div");
  wrap.className = "headingBlock";
  if (props.kicker) {
    const kicker = document.createElement("p");
    kicker.className = "kicker";
    kicker.textContent = props.kicker;
    wrap.appendChild(kicker);
  }
  const level = Math.min(6, Math.max(1, props.level || 2));
  const el = document.createElement(`h${level}`);
  el.textContent = props.text || "";
  wrap.appendChild(el);
  return wrap;
}
