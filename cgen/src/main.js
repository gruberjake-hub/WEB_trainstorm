import { Runtime } from "../engine/runtime.js";
import {
  DEFAULT_CATALOG_URL,
  missingProjectionMessage,
  selectCatalogLesson,
  unknownLessonMessage
} from "./lessonCatalog.js";

/** Stand-in loader: /cgen plays a project catalog lesson id.
 *  `?lesson=` selects a record on occurrences/lessons.json. No param
 *  uses the catalog default (live: ast_alsap_short). Unknown id fails
 *  in the stage — it does not fall back to short. `?course=` stays a
 *  raw-path escape hatch (wins if both are set). Future URL names
 *  client + course (which catalog). This hop is which lesson loads.
 *  Not a catalog UI. Do not treat one JSON filename as the contract. */

function showStageError(stage, message) {
  console.error(message);
  if (stage) stage.textContent = message;
}

async function fetchJson(url) {
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}`);
  }
  return res.json();
}

async function resolveCourseSource(stage) {
  const params = new URLSearchParams(location.search);
  const rawCourse = params.get("course");
  if (rawCourse) {
    return rawCourse;
  }

  let catalog;
  try {
    catalog = await fetchJson(DEFAULT_CATALOG_URL);
  } catch (err) {
    console.error("Failed to load lesson catalog", DEFAULT_CATALOG_URL, err);
    showStageError(
      stage,
      "Could not load the lesson catalog. Rebuild with realize → cartographer → couturier."
    );
    return null;
  }

  const requested = params.has("lesson") ? params.get("lesson") : null;
  const selected = selectCatalogLesson(catalog, requested, DEFAULT_CATALOG_URL);
  if (!selected.ok && selected.reason === "unknown_lesson") {
    showStageError(stage, unknownLessonMessage(selected.lessonId, selected.ids));
    return null;
  }
  if (!selected.ok) {
    showStageError(stage, missingProjectionMessage(selected.lessonId));
    return null;
  }
  return selected.href;
}

async function boot() {
  const stage = document.getElementById("stage");
  const src = await resolveCourseSource(stage);
  if (!src) return;

  let course;
  try {
    course = await fetchJson(src);
  } catch (err) {
    console.error("Failed to load lesson projection", src, err);
    showStageError(
      stage,
      "Could not load the lesson projection. Rebuild with realize → cartographer → couturier."
    );
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
