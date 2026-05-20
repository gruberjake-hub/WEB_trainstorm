export function getAdapter(namespace) {
  const api2004 = findAPI("API_1484_11");
  const api12 = findAPI("API");

  // v1: default localStorage; SCORM can be added without changing runtime
  if (api2004 || api12) return scormStub(namespace, api2004, api12);
  return localStorageAdapter(namespace);
}

function localStorageAdapter(ns) {
  const key = (k) => `${ns}:${k}`;
  return {
    init() {},
    get(k) { return localStorage.getItem(key(k)); },
    set(k, v) { localStorage.setItem(key(k), v); },
    commit() {},
    setStatus() {},
    setScore() {},
    finish() {}
  };
}

// This is intentionally a stub. We’ll harden it when you’re ready.
function scormStub(ns, api2004, api12) {
  const base = localStorageAdapter(ns);
  return {
    ...base,
    init() {
      // Later: Initialize SCORM session and read suspend_data → state
    },
    commit() {
      // Later: Write suspend_data + status + score
    }
  };
}

function findAPI(name) {
  let w = window;
  for (let i = 0; i < 10 && w; i++) {
    if (w[name]) return w[name];
    w = w.parent;
  }
  return null;
}
