import { Runtime } from "../engine/runtime.js";

/** Stand-in loader for /cgen: ast_alsap_short projection. Not a catalog UI.
 *  Future URL names client + course (pack + which lesson). `?course=` stays
 *  an escape hatch. Do not treat this default path as the contract. */
const DEFAULT_COURSE = "./astellas/projects/ast_alsap/realized_lesson.json";

function courseUrl() {
  const params = new URLSearchParams(location.search);
  return params.get("course") || DEFAULT_COURSE;
}

async function boot() {
  const stage = document.getElementById("stage");
  const src = courseUrl();
  let course;
  try {
    const res = await fetch(src, { cache: "no-store" });
    if (!res.ok) {
      throw new Error(`${res.status} ${res.statusText}`);
    }
    course = await res.json();
  } catch (err) {
    console.error("Failed to load lesson projection", src, err);
    if (stage) {
      stage.textContent =
        "Could not load the lesson projection. Rebuild with realize → cartographer → couturier.";
    }
    return;
  }

  const runtime = new Runtime({
    course,
    mount: stage,
    audioEl: document.getElementById("vo"),
    titleEl: document.getElementById("courseTitle"),
    progressTextEl: document.getElementById("progressText"),
    progressFillEl: document.getElementById("progressFill"),
    prevBtn: document.getElementById("prevBtn"),
    nextBtn: document.getElementById("nextBtn"),
    ccToggle: document.getElementById("ccToggle")
  });

  await runtime.init();
}

boot();
