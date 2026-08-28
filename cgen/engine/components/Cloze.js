export function Cloze({ props, emit }) {
  const wrap = document.createElement("section");
  wrap.setAttribute("aria-label", "Knowledge check");

  if (props.kicker) {
    const kicker = document.createElement("p");
    kicker.className = "kicker";
    kicker.textContent = props.kicker;
    wrap.appendChild(kicker);
  }

  const stem = document.createElement("p");
  stem.className = "stem";
  stem.textContent = props.stem || props.prompt || "";
  wrap.appendChild(stem);

  const form = document.createElement("form");
  const input = document.createElement("input");
  input.type = "text";
  input.className = "cloze-in";
  input.autocomplete = "off";
  input.setAttribute("aria-label", "Your recall");

  const submit = document.createElement("button");
  submit.className = "btn";
  submit.type = "submit";
  submit.textContent = "Check";

  const feedback = document.createElement("div");
  feedback.className = "feedback";
  feedback.hidden = true;

  form.appendChild(input);
  form.appendChild(submit);
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const typed = (input.value || "").replace(/\s+/g, " ").trim().toLowerCase();
    const key = (props.key || "").replace(/\s+/g, " ").trim().toLowerCase();
    if (!typed) return;
    const correct = typed === key;
    feedback.hidden = false;
    feedback.textContent = correct
      ? (props.feedback?.correct || "Correct — that’s the wording from this definition.")
      : (props.feedback?.incorrect || "Not yet. The other options are other sentences from this lesson, not this definition.");
    emit("CLOZE_ANSWERED", { id: props.id || "cloze", correct });
  });

  wrap.appendChild(form);
  wrap.appendChild(feedback);
  return wrap;
}
