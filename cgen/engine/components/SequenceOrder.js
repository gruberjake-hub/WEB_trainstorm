export function SequenceOrder({ props, emit }) {
  const wrap = document.createElement("section");
  wrap.className = "sequenceOrder";
  wrap.setAttribute("aria-label", "Sequence practice");

  if (props.kicker) {
    const kicker = document.createElement("p");
    kicker.className = "kicker";
    kicker.textContent = props.kicker;
    wrap.appendChild(kicker);
  }

  const stem = document.createElement("p");
  stem.className = "stem";
  stem.textContent = props.prompt || props.stem || "";
  wrap.appendChild(stem);

  const form = document.createElement("form");
  const list = document.createElement("ol");
  list.className = "sequence-items";

  for (const item of props.items || []) {
    const li = document.createElement("li");
    li.dataset.atom = item.id || item.atom_id || "";

    const move = document.createElement("div");
    move.className = "seq-move";

    const up = document.createElement("button");
    up.type = "button";
    up.className = "btn seq-up";
    up.setAttribute("aria-label", "Move up");
    up.textContent = "Up";
    up.addEventListener("click", () => {
      if (li.previousElementSibling) {
        list.insertBefore(li, li.previousElementSibling);
      }
    });

    const down = document.createElement("button");
    down.type = "button";
    down.className = "btn seq-down";
    down.setAttribute("aria-label", "Move down");
    down.textContent = "Down";
    down.addEventListener("click", () => {
      if (li.nextElementSibling) {
        list.insertBefore(li.nextElementSibling, li);
      }
    });

    move.appendChild(up);
    move.appendChild(down);

    const text = document.createElement("span");
    text.className = "seq-text";
    text.textContent = item.text || "";

    li.appendChild(move);
    li.appendChild(text);
    list.appendChild(li);
  }

  const feedback = document.createElement("div");
  feedback.className = "feedback";
  feedback.hidden = true;

  const submit = document.createElement("button");
  submit.className = "btn";
  submit.type = "submit";
  submit.textContent = "Check";

  form.appendChild(list);
  form.appendChild(submit);
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const want = (props.correctIds || []).join(",");
    const got = Array.from(list.querySelectorAll("li")).map((li) => li.dataset.atom || "");
    const correct = got.join(",") === want;
    feedback.hidden = false;
    feedback.textContent = correct
      ? (props.feedback?.correct || "Correct — that’s the order on the job aid already shown.")
      : (props.feedback?.incorrect || "Not yet. Use the sequence on the job aid above.");
    emit("SEQUENCE_ANSWERED", { id: props.id || "sequence", correct, order: got });
  });

  wrap.appendChild(form);
  wrap.appendChild(feedback);
  return wrap;
}
