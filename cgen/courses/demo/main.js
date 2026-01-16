import { Runtime } from "../../engine/runtime.js";
import { applyBranding } from "../../engine/theme-manager.js";

function say(msg) {
  const stage = document.getElementById("stage");
  if (!stage) return;
  const p = document.createElement("p");
  p.textContent = msg;
  stage.appendChild(p);
}

async function boot() {
  try {
    say("✅ main.js loaded");

    say("⏳ fetching course.json...");
    const res = await fetch("./course.json", { cache: "no-store" });
    say(`✅ course.json response: ${res.status} ${res.statusText}`);

    const text = await res.text();
    say(`ℹ️ course.json first 60 chars: ${text.slice(0, 60).replace(/\s+/g, " ")}`);

    let course;
    try {
      course = JSON.parse(text);
      say("✅ course.json parsed as JSON");
    } catch (e) {
      say("❌ course.json is NOT valid JSON (likely HTML/redirect). See console.");
      console.error("course.json parse error:", e, "Raw response:", text);
      return;
    }

  // 🔑 🔑 🔑 ONE-LINE FIX (actually one call, async-safe)
    say("🎨 Applying brand...");
    await applyBranding(course.meta);
    say("✅ Brand applied");
    
    const runtime = new Runtime({
      course,
      mount: document.getElementById("stage"),
      audioEl: document.getElementById("vo"),
      titleEl: document.getElementById("courseTitle"),
      progressTextEl: document.getElementById("progressText"),
      progressFillEl: document.getElementById("progressFill"),
      prevBtn: document.getElementById("prevBtn"),
      nextBtn: document.getElementById("nextBtn"),
      ccToggle: document.getElementById("ccToggle")
    });

    say("✅ Runtime created. Calling init()...");
    runtime.init();
    say("✅ Runtime init() completed (if you still see no scene, it’s scene resolution)");
  } catch (e) {
    say("❌ boot() crashed — see console");
    console.error(e);
  }
}

boot();
