import { Store } from "./store.js";
import { RulesEngine } from "./rules.js";
import { getAdapter } from "./scorm.js";

/* Theme + brand loaders: pack from lesson-projection meta.theme */
import { loadTheme } from "./themeLoader.js";
import { loadBrand, brandPackUrl, themeFromMeta } from "./brandLoader.js";

import { roleClassFromMeta } from "./styleRef.js";

import { Heading } from "./components/Heading.js";
import { Body } from "./components/Body.js";
import { RevealCards } from "./components/RevealCards.js";
import { MCQ } from "./components/MCQ.js";
import { StepList } from "./components/StepList.js";
import { SequenceOrder } from "./components/SequenceOrder.js";
import { Cloze } from "./components/Cloze.js";

const COMPONENTS = { Heading, Body, RevealCards, MCQ, StepList, SequenceOrder, Cloze };

function hasNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function hasMediaList(value) {
  return Array.isArray(value) && value.length > 0;
}

function voiceoverHasPayload(vo) {
  if (vo == null || vo === false) return false;
  if (typeof vo === "string") return vo.trim().length > 0;
  if (typeof vo !== "object") return false;
  if (hasNonEmptyString(vo.src) || hasNonEmptyString(vo.captionsVtt)) return true;
  if (hasMediaList(vo.tracks) || hasMediaList(vo.segments)) return true;
  if (hasNonEmptyString(vo.mode) && vo.mode !== "none") return true;
  return false;
}

/** Course JSON has voiceover or captions/tracks on any scene. Not an ALSAP fork. */
export function lessonHasVoiceoverChrome(course) {
  return (course?.scenes || []).some((scene) => {
    if (!scene) return false;
    if (hasNonEmptyString(scene.captions) || hasNonEmptyString(scene.captionsVtt)) {
      return true;
    }
    if (hasMediaList(scene.tracks)) return true;
    return voiceoverHasPayload(scene.voiceover);
  });
}

export class Runtime {
  constructor(opts) {
    /* -------------------------------
       Core runtime wiring (unchanged)
       ------------------------------- */
    this.course = opts.course;
    this.mount = opts.mount;
    this.audioEl = opts.audioEl;

    this.titleEl = opts.titleEl;
    this.progressTextEl = opts.progressTextEl;
    this.progressFillEl = opts.progressFillEl;

    this.prevBtn = opts.prevBtn;
    this.nextBtn = opts.nextBtn;
    this.ccToggle = opts.ccToggle;

    /* -------------------------------
       NEW: declarative theme + brand
       ------------------------------- */

    const theme = themeFromMeta(this.course?.meta);
    this.themeName = theme;

    // 1️⃣ Load CSS immediately (synchronous side-effect)
    loadTheme(theme);

    // 2️⃣ Begin loading brand identity (async)
    //    We store the promise because constructors can't be async
    this.brandPromise = loadBrand(theme);

    // 3️⃣ Cache the logo slot (shell owns the slot)
    this.brandLogoEl = document.getElementById("brandLogo");

    if (theme) {
      const app = document.getElementById("app");
      app?.classList.add(`brand-${theme}`);
    }

    /* -------------------------------
       Persistence, rules, state
       ------------------------------- */

    this.adapter = getAdapter(this.course.meta?.id || "course");
    this.store = new Store(this.course, this.adapter);
    this.rules = new RulesEngine(
      this.course.rules || [],
      this.store,
      (evt) => this.dispatch(evt)
    );
  }

  /* ======================================================
     INIT (now async so we can await brand resolution)
     ====================================================== */
  async init() {
    this.adapter.init?.();

    /* -------------------------------
       NEW: apply brand identity
       ------------------------------- */
    const brand = await this.brandPromise;
    this.applyBrand(brand);

    /* -------------------------------
       Existing init logic (unchanged)
       ------------------------------- */

    const lessonTitle = this.course.meta?.title;
    this.titleEl.textContent = lessonTitle || "Course";
    document.title = lessonTitle || "Course Engine v1";
    this.applyVoiceoverChrome(lessonHasVoiceoverChrome(this.course));
    this.store.load();

    this.prevBtn.addEventListener("click", () =>
      this.dispatch({ type: "NAV_PREV" })
    );

    this.nextBtn.addEventListener("click", () =>
      this.dispatch({ type: "NAV_NEXT" })
    );

    this.ccToggle.addEventListener("click", () =>
      this.dispatch({ type: "CAPTIONS_TOGGLE" })
    );

    this.audioEl.addEventListener("ended", () =>
      this.dispatch({ type: "MEDIA_ENDED" })
    );

    this.dispatch({ type: "COURSE_INIT" });

    const wanted =
      this.store.state.runtime?.sceneId ||
      this.course.nav?.startSceneId;
    const startId = this.course.scenes.some(s => s.id === wanted)
      ? wanted
      : (this.course.nav?.startSceneId || this.course.scenes[0]?.id);

    this.gotoScene(startId);
  }

  /* ======================================================
     NEW: Brand application logic (small + deterministic)
     ====================================================== */
  applyVoiceoverChrome(show) {
    if (this.ccToggle) this.ccToggle.hidden = !show;
    const footer = this.audioEl?.closest?.(".footer");
    if (footer) footer.hidden = !show;
  }

  applyBrand(brand) {
    if (!brand || !this.brandLogoEl) return;

    // Prefer primary logo, fallback safely
    const logo =
      brand.logos?.primary ||
      brand.logos?.inverse ||
      null;

    if (!logo?.src) return;

    const pack = brand.brand || this.themeName;
    this.brandLogoEl.src = brandPackUrl(pack, logo.src);
    this.brandLogoEl.alt = logo.alt || pack;
    this.brandLogoEl.hidden = false;
  }

  /* ======================================================
     Everything below here is unchanged
     ====================================================== */

  dispatch(event) {
    this.rules.handle(event);

    if (event.type === "NAV_NEXT") this.gotoRelative(1);
    if (event.type === "NAV_PREV") this.gotoRelative(-1);

    if (event.type === "CAPTIONS_TOGGLE") {
      const ccOn = !this.store.get("vars.ccOn");
      this.store.set("vars.ccOn", ccOn);
      this.ccToggle.setAttribute("aria-pressed", String(ccOn));
      this.applyCaptionsVisibility(ccOn);
      this.store.save();
    }

    this.updateProgressUI();
  }

  gotoRelative(delta) {
    const scenes = this.course.scenes;
    const idx = scenes.findIndex(
      s => s.id === this.store.state.runtime.sceneId
    );
    const next = scenes[idx + delta];
    if (next) this.gotoScene(next.id);
  }

  gotoScene(sceneId) {
    const scene = this.course.scenes.find(s => s.id === sceneId);
    if (!scene) return;

    this.store.set("runtime.sceneId", sceneId);
    this.store.set("runtime.sceneTitle", scene.title || "");
    const completed = this.store.get("vars.completedScenes") || [];
    if (!completed.includes(sceneId)) {
      this.store.set("vars.completedScenes", [...completed, sceneId]);
    }
    this.store.save();

    this.mount.innerHTML = "";
    this.mount.focus();

    this.dispatch({ type: "SCENE_ENTER", payload: { sceneId } });

    for (const node of scene.components || []) {
      const Cmp = COMPONENTS[node.type];
      if (!Cmp) continue;

      const meta = node.meta || {};
      const el = Cmp({
        props: node.props || {},
        store: this.store,
        emit: (type, payload) =>
          this.dispatch({ type, payload }),
        meta
      });

      const role = roleClassFromMeta(meta);
      if (role) el.classList.add(role);

      this.mount.appendChild(el);
    }

    this.loadVoiceover(scene.voiceover);

    this.prevBtn.disabled =
      this.course.scenes[0].id === sceneId;

    this.nextBtn.disabled =
      this.course.scenes[this.course.scenes.length - 1].id === sceneId;

    this.updateProgressUI();
  }

  loadVoiceover(voiceover) {
    while (this.audioEl.firstChild)
      this.audioEl.removeChild(this.audioEl.firstChild);

    if (!voiceover?.src) {
      this.audioEl.removeAttribute("src");
      return;
    }

    this.audioEl.src = voiceover.src;

    if (voiceover.captionsVtt) {
      const track = document.createElement("track");
      track.kind = "captions";
      track.label = "English";
      track.srclang = "en";
      track.src = voiceover.captionsVtt;
      track.default = true;
      this.audioEl.appendChild(track);
    }

    const ccOn = !!this.store.get("vars.ccOn");
    this.ccToggle.setAttribute("aria-pressed", String(ccOn));
    this.applyCaptionsVisibility(ccOn);
  }

  applyCaptionsVisibility(on) {
    const tracks = this.audioEl.textTracks;
    for (let i = 0; i < tracks.length; i++) {
      tracks[i].mode = on ? "showing" : "hidden";
    }
  }

  updateProgressUI() {
    const total = this.course.scenes.length;
    const completed =
      (this.store.get("vars.completedScenes") || []).length;

    const pct = total
      ? Math.round((completed / total) * 100)
      : 0;

    this.progressTextEl.textContent = `${pct}%`;
    this.progressFillEl.style.width = `${pct}%`;
    this.progressFillEl.parentElement?.setAttribute(
      "aria-valuenow",
      String(pct)
    );
  }
}
