import { Store } from "./store.js";
import { RulesEngine } from "./rules.js";
import { getAdapter } from "./scorm.js";

import { Heading } from "./components/Heading.js";
import { Body } from "./components/Body.js";
import { RevealCards } from "./components/RevealCards.js";
import { MCQ } from "./components/MCQ.js";

const COMPONENTS = { Heading, Body, RevealCards, MCQ };

export class Runtime {
  constructor(opts) {
    this.course = opts.course;
    this.mount = opts.mount;
    this.audioEl = opts.audioEl;

    this.titleEl = opts.titleEl;
    this.progressTextEl = opts.progressTextEl;
    this.progressFillEl = opts.progressFillEl;

    this.prevBtn = opts.prevBtn;
    this.nextBtn = opts.nextBtn;
    this.ccToggle = opts.ccToggle;

    this.adapter = getAdapter(this.course.meta?.id || "course");
    this.store = new Store(this.course, this.adapter);
    this.rules = new RulesEngine(this.course.rules || [], this.store, (evt) => this.dispatch(evt));
  }

  init() {
    this.adapter.init?.();

    this.titleEl.textContent = this.course.meta?.title || "Course";
    this.store.load();

    this.prevBtn.addEventListener("click", () => this.dispatch({ type: "NAV_PREV" }));
    this.nextBtn.addEventListener("click", () => this.dispatch({ type: "NAV_NEXT" }));
    this.ccToggle.addEventListener("click", () => this.dispatch({ type: "CAPTIONS_TOGGLE" }));

    this.audioEl.addEventListener("ended", () => this.dispatch({ type: "MEDIA_ENDED" }));

    this.dispatch({ type: "COURSE_INIT" });

    const startId = this.store.state.runtime?.sceneId || this.course.nav?.startSceneId;
    this.gotoScene(startId);
  }

  dispatch(event) {
    // Run declarative rules first
    this.rules.handle(event);

    // Built-in nav behavior (kept minimal; can be rules-driven later)
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
    const idx = scenes.findIndex(s => s.id === this.store.state.runtime.sceneId);
    const next = scenes[idx + delta];
    if (next) this.gotoScene(next.id);
  }

  gotoScene(sceneId) {
    const scene = this.course.scenes.find(s => s.id === sceneId);
    if (!scene) return;

    this.store.set("runtime.sceneId", sceneId);
    this.store.set("runtime.sceneTitle", scene.title || "");
    this.store.save();

    this.mount.innerHTML = "";
    this.mount.focus();

    this.dispatch({ type: "SCENE_ENTER", payload: { sceneId } });

    // Render components
    for (const node of scene.components || []) {
      const Cmp = COMPONENTS[node.type];
      if (!Cmp) continue;
      const el = Cmp({
        props: node.props || {},
        store: this.store,
        emit: (type, payload) => this.dispatch({ type, payload })
      });
      this.mount.appendChild(el);
    }

    // Media
    this.loadVoiceover(scene.voiceover);

    // Update nav enabled states (v1 simplistic)
    this.prevBtn.disabled = this.course.scenes[0].id === sceneId;
    this.nextBtn.disabled = this.course.scenes[this.course.scenes.length - 1].id === sceneId;

    this.updateProgressUI();
  }

  loadVoiceover(voiceover) {
    // Reset tracks
    while (this.audioEl.firstChild) this.audioEl.removeChild(this.audioEl.firstChild);

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
    const completed = (this.store.get("vars.completedScenes") || []).length;
    const pct = total ? Math.round((completed / total) * 100) : 0;

    this.progressTextEl.textContent = `${pct}%`;
    this.progressFillEl.style.width = `${pct}%`;
    this.progressFillEl.parentElement?.setAttribute("aria-valuenow", String(pct));
  }
}
