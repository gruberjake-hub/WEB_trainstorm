export function RevealCards({ props, emit }) {
  const wrap = document.createElement("section");
  wrap.setAttribute("aria-label", "Click to reveal");
  const grid = document.createElement("div");
  grid.className = "cardGrid";

  const revealed = new Set();
  const items = props.items || [];

  function checkComplete() {
    if (props.requireAllRevealedToComplete && revealed.size === items.length) {
      emit("REVEALCARDS_COMPLETE", { id: props.id || "revealsComplete" });
    }
  }

  for (const item of items) {
    const card = document.createElement("div");
    card.className = "card";

    const btn = document.createElement("button");
    btn.className = "btn";
    btn.type = "button";
    btn.setAttribute("aria-expanded", "false");
    btn.textContent = item.title;

    const body = document.createElement("div");
    body.hidden = true;
    body.style.marginTop = "10px";
    body.textContent = item.body || "";

    btn.addEventListener("click", () => {
      const open = body.hidden;
      body.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
      if (open) revealed.add(item.id);
      checkComplete();
    });

    card.appendChild(btn);
    card.appendChild(body);
    grid.appendChild(card);
  }

  wrap.appendChild(grid);
  return wrap;
}
