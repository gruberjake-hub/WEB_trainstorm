export function MCQ({ props, emit }) {
  const wrap = document.createElement("section");
  wrap.setAttribute("aria-label", "Knowledge check");

  // ✅ Backward-compatible normalization (supports old + new schemas)
  const stemText = props.stem ?? props.question ?? props.prompt ?? "";
  const choices = props.choices ?? props.options ?? [];
  const qid = props.id ?? props.qid ?? "q";

  const stem = document.createElement("p");
  stem.textContent = stemText;
  wrap.appendChild(stem);

  const form = document.createElement("form");
  const name = `mcq-${qid}`;

  const feedback = document.createElement("div");
  feedback.className = "feedback";
  feedback.hidden = true;

  (choices || []).forEach((c, idx) => {
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
    label.textContent = c.text ?? c.label ?? "";

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

    const choice = (choices || []).find(c => c.id === chosen);
    const correct = !!choice?.correct;

    feedback.hidden = false;
    feedback.textContent = correct
      ? (props.feedback?.correct || "Correct.")
      : (props.feedback?.incorrect || "Try again.");

    emit("MCQ_ANSWERED", { id: qid, chosen, correct });
  });

  wrap.appendChild(form);
  wrap.appendChild(feedback);
  return wrap;
}