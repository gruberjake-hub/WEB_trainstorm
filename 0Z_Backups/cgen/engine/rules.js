export class RulesEngine {
  constructor(rules, store, dispatch) {
    this.rules = rules;
    this.store = store;
    this.dispatch = dispatch;
  }

  handle(event) {
    for (const rule of this.rules) {
      if (rule.on !== event.type) continue;
      if (rule.when && !this.evalWhen(rule.when, event)) continue;
      this.runActions(rule.then || [], event);
    }
  }

  evalWhen(conds, event) {
    // v1 = AND semantics
    return conds.every(c => this.evalCond(c, event));
  }

  evalCond(cond, event) {
    if (cond.type === "SCENE_IS") {
      return this.store.get("runtime.sceneId") === cond.sceneId;
    }
    if (cond.type === "MATCH") {
      const value = cond.path.split(".").reduce((acc, k) => (acc ? acc[k] : undefined), { event });
      return value === cond.equals;
    }
    if (cond.type === "VAR_EQUALS") {
      return this.store.get(cond.path) === cond.equals;
    }
    return false;
  }

  runActions(actions, event) {
    for (const a of actions) {
      if (a.type === "ACTION_SET") {
        this.store.set(a.path, a.value);
        this.store.save();
      }
      if (a.type === "ACTION_INCREMENT") {
        const cur = Number(this.store.get(a.path) || 0);
        this.store.set(a.path, cur + Number(a.by || 1));
        this.store.save();
      }
      if (a.type === "ACTION_GOTO_SCENE") {
        this.dispatch({ type: "NAV_GOTO", payload: { sceneId: a.sceneId } });
      }
      if (a.type === "ACTION_MARK_SCENE_COMPLETE") {
        const id = this.store.get("runtime.sceneId");
        const completed = new Set(this.store.get("vars.completedScenes") || []);
        completed.add(id);
        this.store.set("vars.completedScenes", Array.from(completed));
        this.store.save();
      }
    }
  }
}
