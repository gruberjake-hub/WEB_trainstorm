import { Store } from "./store.js";
import { RulesEngine } from "./rules.js";
import { getAdapter } from "./scorm.js";

/* NEW: theme loader */
import { loadTheme } from "./themeLoader.js";

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

    /* NEW: load theme declared by course.json */
    const theme = this.course?.meta?.theme;
    loadTheme(theme);

    this.adapter = getAdapter(this.course.meta?.id || "course");
    this.store = new Store(this.course, this.adapter);
    this.rules = new RulesEngine(
      this.course.rules || [],
      this.store,
      (evt) => this.dispatch(evt)
    );
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

    const startId =
      this.store.state.runtime?.sceneId ||
      this.course.nav?.startSceneId;

    this.gotoScene(startId);
  }

  /* --- rest of file unchanged --- */
}
