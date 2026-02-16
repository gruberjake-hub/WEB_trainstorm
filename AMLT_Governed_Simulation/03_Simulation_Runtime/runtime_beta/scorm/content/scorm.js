// Minimal SCORM 1.2 API helper (beta)
// In production, you'd use a tested SCORM wrapper library.

window.SCORM = (() => {
  let api = null;

  function findAPI(win) {
    let tries = 0;
    while (win && tries < 25) {
      if (win.API) return win.API; // SCORM 1.2
      win = win.parent;
      tries++;
    }
    return null;
  }

  function init() {
    api = findAPI(window);
    if (api && api.LMSInitialize) api.LMSInitialize("");
  }

  function commit() {
    if (api && api.LMSCommit) api.LMSCommit("");
  }

  function setValue(k, v) {
    if (api && api.LMSSetValue) api.LMSSetValue(k, String(v));
  }

  function finish() {
    if (api && api.LMSFinish) api.LMSFinish("");
  }

  function setCompleted(score = 100) {
    init();
    setValue("cmi.core.lesson_status", "completed");
    setValue("cmi.core.score.raw", score);
    commit();
    // finish(); // optional; often okay to leave session open
  }

  function setIncomplete() {
    init();
    setValue("cmi.core.lesson_status", "incomplete");
    commit();
  }

  return { setCompleted, setIncomplete };
})();
