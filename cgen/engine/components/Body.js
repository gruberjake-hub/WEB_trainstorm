export function Body({ props }) {
  const wrap = document.createElement("div");
  wrap.className = "bodyBlock";
  if (props.kicker) {
    const kicker = document.createElement("p");
    kicker.className = "kicker";
    kicker.textContent = props.kicker;
    wrap.appendChild(kicker);
  }
  const p = document.createElement("p");
  p.textContent = props.text || "";
  wrap.appendChild(p);
  return wrap;
}
