export class Store {
  constructor(course, adapter) {
    this.course = course;
    this.adapter = adapter;
    this.state = {
      vars: structuredClone(course.vars || {}),
      runtime: { sceneId: null, sceneTitle: "" },
      ui: { canNext: true, canPrev: true }
    };
  }

  load() {
    const saved = this.adapter.get?.("state");
    if (saved) {
      try { this.state = JSON.parse(saved); } catch {}
    }
    // Ensure vars exist
    this.state.vars = { ...(this.course.vars || {}), ...(this.state.vars || {}) };
    if (!Array.isArray(this.state.vars.completedScenes)) this.state.vars.completedScenes = [];
    if (typeof this.state.vars.ccOn !== "boolean") this.state.vars.ccOn = !!this.course.meta?.defaultCaptionOn;
  }

  save() {
    this.adapter.set?.("state", JSON.stringify(this.state));
    this.adapter.commit?.();
  }

  get(path) {
    return path.split(".").reduce((acc, key) => (acc ? acc[key] : undefined), this.state);
  }

  set(path, value) {
    const keys = path.split(".");
    let obj = this.state;
    for (let i = 0; i < keys.length - 1; i++) {
      obj[keys[i]] ??= {};
      obj = obj[keys[i]];
    }
    obj[keys[keys.length - 1]] = value;
  }
}
