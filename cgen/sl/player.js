/**
 * Player two — Storyline-shaped chrome around the same realized_lesson.json
 * the stock Course Engine plays at /cgen.
 *
 * Interchangeable adapter: same query contract, same Runtime, same catalog.
 * Import lessonCatalog + engine; do not fork meaning. A third player is a
 * sibling folder (not a rewrite of this one or of /cgen).
 *
 * Catalog paths in lessonCatalog.js are relative to /cgen/. Resolve them
 * against that root so /cgen/sl/ does not 404 sibling stores.
 */

import { Runtime, lessonHasVoiceoverChrome } from "../engine/runtime.js";
import {
  catalogUrlForProject,
  missingProjectionMessage,
  selectCatalogLesson,
  unknownLessonMessage,
  unknownProjectMessage
} from "../src/lessonCatalog.js";

const CHECK_TYPES = new Set(["MCQ", "SequenceOrder", "Cloze"]);
const CGEN_ROOT = new URL("../", import.meta.url);

function hrefFromCgen(relOrAbs) {
  return new URL(relOrAbs, CGEN_ROOT).href;
}

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

/** Same contract as /cgen/src/main.js; hrefs are rooted at /cgen/. */
async function resolveCourseSource(stage) {
  const params = new URLSearchParams(location.search);
  const rawCourse = params.get("course");
  if (rawCourse) {
    return hrefFromCgen(rawCourse);
  }

  const rawProject = params.has("project") ? params.get("project") : null;
  const catalogRel = catalogUrlForProject(rawProject);
  if (!catalogRel) {
    showStageError(stage, unknownProjectMessage(rawProject));
    return null;
  }
  const catalogUrl = hrefFromCgen(catalogRel);

  let catalog;
  try {
    catalog = await fetchJson(catalogUrl);
  } catch (err) {
    console.error("Failed to load lesson catalog", catalogUrl, err);
    showStageError(
      stage,
      "Could not load the lesson catalog. Rebuild with realize → cartographer → couturier."
    );
    return null;
  }

  const requested = params.has("lesson") ? params.get("lesson") : null;
  const selected = selectCatalogLesson(catalog, requested, catalogUrl);
  if (!selected.ok && selected.reason === "unknown_lesson") {
    showStageError(stage, unknownLessonMessage(selected.lessonId, selected.ids));
    return null;
  }
  if (!selected.ok) {
    showStageError(stage, missingProjectionMessage(selected.lessonId));
    return null;
  }
  return hrefFromCgen(selected.href);
}

function sceneHasCheck(scene) {
  return (scene?.components || []).some((node) => CHECK_TYPES.has(node.type));
}

function sceneLabel(scene, index) {
  const title = (scene?.title || "").trim();
  if (title) return title;
  if (scene?.kind === "lesson_end") return "Check";
  return `Scene ${index + 1}`;
}

function formatTime(seconds) {
  const n = Number.isFinite(seconds) ? Math.max(0, seconds) : 0;
  const m = Math.floor(n / 60);
  const s = Math.floor(n % 60);
  return `${m}:${String(s).padStart(2, "0")}`;
}

function lockSvg() {
  return `<svg class="sl-mark" viewBox="0 0 16 16" aria-hidden="true"><rect x="4" y="7" width="8" height="7" rx="1" fill="currentColor"/><path d="M6 7V5a2 2 0 1 1 4 0v2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`;
}

function checkSvg() {
  return `<svg class="sl-mark" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 8.5 6.5 11.5 12.5 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}

function buildOutline(course, onPick) {
  const list = document.getElementById("sceneMenu");
  const titleEl = document.getElementById("menuLessonTitle");
  if (titleEl) titleEl.textContent = course.meta?.title || "Course";
  if (!list) return;
  list.innerHTML = "";

  (course.scenes || []).forEach((scene, index) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.type = "button";
    btn.dataset.sceneId = scene.id;
    btn.innerHTML = `<span class="sl-idx">${index + 1}</span><span class="sl-label"></span><span class="sl-mark-slot"></span>`;
    btn.querySelector(".sl-label").textContent = sceneLabel(scene, index);
    btn.addEventListener("click", () => onPick(scene.id));
    li.appendChild(btn);
    list.appendChild(li);
  });
}

function paintOutline(visited, currentId) {
  const list = document.getElementById("sceneMenu");
  if (!list) return;
  for (const btn of list.querySelectorAll("button[data-scene-id]")) {
    const id = btn.dataset.sceneId;
    const isCurrent = id === currentId;
    const isVisited = visited.has(id);
    const locked = !isVisited && !isCurrent;
    btn.setAttribute("aria-current", isCurrent ? "true" : "false");
    btn.setAttribute("aria-disabled", locked ? "true" : "false");
    const slot = btn.querySelector(".sl-mark-slot");
    if (slot) {
      if (locked) slot.innerHTML = lockSvg();
      else if (isVisited && !isCurrent) slot.innerHTML = checkSvg();
      else slot.innerHTML = "";
    }
  }
}

function paintSubmit(course, sceneId) {
  const submitBtn = document.getElementById("submitBtn");
  if (!submitBtn) return;
  const scene = (course.scenes || []).find((s) => s.id === sceneId);
  submitBtn.hidden = !sceneHasCheck(scene);
}

function bindSubmit(mount) {
  const submitBtn = document.getElementById("submitBtn");
  if (!submitBtn) return;
  submitBtn.addEventListener("click", () => {
    mount.querySelectorAll("form").forEach((form) => form.requestSubmit());
  });
}

function bindMedia(audio) {
  const playBtn = document.getElementById("playBtn");
  const seek = document.getElementById("seek");
  const volume = document.getElementById("volume");
  const timeEl = document.getElementById("mediaTime");
  if (!playBtn || !seek || !volume || !timeEl) return;

  const sync = () => {
    const hasSrc = Boolean(audio.getAttribute("src") || audio.currentSrc);
    playBtn.disabled = !hasSrc;
    seek.disabled = !hasSrc;
    playBtn.textContent = audio.paused ? "Play" : "Pause";
    const dur = Number.isFinite(audio.duration) ? audio.duration : 0;
    if (!seek.dataset.dragging) {
      seek.max = String(dur || 0);
      seek.value = String(audio.currentTime || 0);
    }
    timeEl.textContent = formatTime(audio.currentTime);
  };

  playBtn.addEventListener("click", () => {
    if (playBtn.disabled) return;
    if (audio.paused) audio.play();
    else audio.pause();
  });
  seek.addEventListener("pointerdown", () => {
    seek.dataset.dragging = "1";
  });
  seek.addEventListener("input", () => {
    audio.currentTime = Number(seek.value);
    timeEl.textContent = formatTime(audio.currentTime);
  });
  seek.addEventListener("change", () => {
    delete seek.dataset.dragging;
  });
  volume.addEventListener("input", () => {
    audio.volume = Number(volume.value);
  });
  ["play", "pause", "ended", "loadedmetadata", "timeupdate", "emptied"].forEach((evt) => {
    audio.addEventListener(evt, sync);
  });
  sync();
  return sync;
}

function attachChrome(runtime) {
  const visited = new Set();
  const origGoto = runtime.gotoScene.bind(runtime);

  buildOutline(runtime.course, (sceneId) => {
    if (!visited.has(sceneId)) return;
    runtime.gotoScene(sceneId);
  });

  bindSubmit(runtime.mount);
  const syncMedia = bindMedia(runtime.audioEl);

  runtime.gotoScene = (sceneId) => {
    const scenes = runtime.course.scenes || [];
    const scene = scenes.find((s) => s.id === sceneId);
    if (!scene) return;
    origGoto(sceneId);
    const idx = scenes.findIndex((s) => s.id === sceneId);
    if (idx >= 0) {
      for (let i = 0; i <= idx; i++) visited.add(scenes[i].id);
    }
    visited.add(sceneId);
    paintOutline(visited, sceneId);
    paintSubmit(runtime.course, sceneId);
    syncMedia?.();
  };

  document.addEventListener("keydown", (event) => {
    if (event.target.closest("input, textarea, select, [contenteditable='true']")) return;
    if (event.key === "ArrowRight") runtime.dispatch({ type: "NAV_NEXT" });
    if (event.key === "ArrowLeft") runtime.dispatch({ type: "NAV_PREV" });
  });
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

  attachChrome(runtime);
  await runtime.init();

  if (!lessonHasVoiceoverChrome(course)) {
    const media = document.querySelector(".sl-media");
    if (media) media.hidden = true;
  }
}

boot();
