// /decks/orchestrator-deck.js
let currentIndex = 0;

function renderSlide() {
  const slide = slides[currentIndex];
  const mainEl = document.getElementById("slide-main");
  const counterEl = document.getElementById("slide-counter");
  const progressInner = document.getElementById("progress-inner");

  const total = slides.length;
  counterEl.textContent = `${currentIndex + 1} / ${total}`;

  const progress = ((currentIndex + 1) / total) * 100;
  progressInner.style.width = progress + "%";

  if (slide.layout === "two-col") {
    mainEl.innerHTML = `
      <div class="slide-title">${slide.title}</div>
      ${slide.subtitle ? `<div class="slide-subtitle">${slide.subtitle}</div>` : ""}
      <div class="layout-two-col">
        <div>${slide.left}</div>
        <div>${slide.right}</div>
      </div>
    `;
  } else {
    mainEl.innerHTML = `
      <div class="slide-title">${slide.title}</div>
      ${slide.subtitle ? `<div class="slide-subtitle">${slide.subtitle}</div>` : ""}
      ${slide.body}
    `;
  }
}

function nextSlide() {
  if (currentIndex < slides.length - 1) {
    currentIndex++;
    renderSlide();
  }
}

function prevSlide() {
  if (currentIndex > 0) {
    currentIndex--;
    renderSlide();
  }
}

// Keyboard navigation
document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight" || e.key === " " || e.key === "PageDown") {
    e.preventDefault();
    nextSlide();
  } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
    e.preventDefault();
    prevSlide();
  }
});

// Click navigation on footer:
// click left half = previous, right half = next
document.addEventListener("DOMContentLoaded", () => {
  renderSlide();

  const footer = document.querySelector(".slide-footer");
  if (footer) {
    footer.style.cursor = "pointer";
    footer.addEventListener("click", (e) => {
      const rect = footer.getBoundingClientRect();
      const mid = rect.left + rect.width / 2;
      if (e.clientX < mid) {
        prevSlide();
      } else {
        nextSlide();
      }
    });
  }
});
