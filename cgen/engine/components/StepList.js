export function StepList({ props }) {
  const wrap = document.createElement("section");
  wrap.className = "stepList";
  const ordered = props.ordered !== false;
  wrap.setAttribute("aria-label", props.title || (ordered ? "Job aid" : "List"));

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

  const list = document.createElement(ordered ? "ol" : "ul");
  list.className = ordered ? "steps" : "items";
  for (const item of props.items || []) {
    const li = document.createElement("li");
    if (item.id) li.dataset.eid = item.id;
    if (item.composed_from) li.dataset.atom = item.composed_from;
    li.textContent = item.text || "";
    list.appendChild(li);
  }
  wrap.appendChild(list);
  return wrap;
}
