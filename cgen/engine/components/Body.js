export function Body({ props }) {
  const p = document.createElement("p");
  p.textContent = props.text || "";
  return p;
}
