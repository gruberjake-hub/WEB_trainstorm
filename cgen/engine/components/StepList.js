export function StepList({ props }) {
  const wrap = document.createElement("section");
  wrap.className = "stepList";
  wrap.setAttribute("aria-label", props.title || "Job aid");

  if (props.kicker) {
    const kicker = document.createElement("p");
    kicker.className = "kicker";
    kicker.textContent = props.kicker;
    wrap.appendChild(kicker);
  }

  if (props.title) {
    const title = document.createElement("h3");
    title.textContent = props.title;
    wrap.appendChild(title);
  }

  const ol = document.createElement("ol");
  ol.className = "steps";
  for (const item of props.items || []) {
    const li = document.createElement("li");
    if (item.id) li.dataset.eid = item.id;
    if (item.composed_from) li.dataset.atom = item.composed_from;
    li.textContent = item.text || "";
    ol.appendChild(li);
  }
  wrap.appendChild(ol);
  return wrap;
}
