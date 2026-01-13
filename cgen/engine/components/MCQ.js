export function MCQ({ props, emit }) {
  const wrap = document.createElement("section");
  wrap.setAttribute("aria-label", "Knowledge check");

  const stem = document.createElement("p");
  stem.textContent = props.stem || "";
  wrap.appendChild(stem);

  const form = document.createElement("form");
  const name = `mcq-${props.id || "q"}`;

  const feedback = document.createElement("div");
  feedback.className = "feedback";
  feedback.hidden = true;

  (props.choices || []).forEach((c, idx) => {
    const id = `${name}-${idx}`;

    const row = document.createElement("div");
    row.style.display = "flex";
    row.style.gap = "10px";
    row.style.alignItems = "center";
    row.style.margin = "8px 0";

    const input = document.createElement("input");
    input.type = "radio";
    input.name = name;
    input.id = id;
    input.value = c.id;

    const label = document.createElement("label");
    label.setAttribute("for", id);
    label.textContent = c.text;

    row.appendChild(input);
    row.appendChild(label);
    form.appendChild(row);
  });

  const submit = document.createElement("button");
  submit.className = "btn";
  submit.type = "submit";
  submit.textContent = "Submit";
  form.appendChild(submit);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const chosen = new FormData(form).get(name);
    if (!chosen) return;

    const choice = (props.choices || []).find(c => c.id === chosen);
    const correct = !!choice?.correct;

    feedback.hidden = false;
    feedback.textContent = correct ? (props.feedback?.correct || "Correct.") : (props.feedback?.incorrect || "Try again.");

    emit("MCQ_ANSWERED", { id: props.id, chosen, correct });
  });

  wrap.appendChild(form);
  wrap.appendChild(feedback);
  return wrap;
}
