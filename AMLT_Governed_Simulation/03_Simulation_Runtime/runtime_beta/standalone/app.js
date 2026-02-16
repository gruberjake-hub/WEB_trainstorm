// ===== CONFIG (edit for your environment) =====
const ENDPOINT_URL = "https://YOUR_AZURE_ENDPOINT/simulate-amlt"; // placeholder
const PROMPT_VERSION = "AMLT_SIM_v4.2";

// ===== Utilities =====
function setStatus(msg) {
  document.getElementById("status").textContent = msg;
}

function extractFencedJson(text) {
  // Finds first ```json ... ``` block
  const match = text.match(/```json\s*([\s\S]*?)\s*```/i);
  if (!match) return null;
  try { return JSON.parse(match[1]); } catch { return null; }
}

function validateGovernanceJson(g) {
  // Minimal deterministic checks (beta)
  const errors = [];
  if (!g) errors.push("No JSON parsed.");
  else {
    const requiredTop = ["simulation_id","asset_id","round","simulation_master","decision_node","completion","governance_signature"];
    requiredTop.forEach(k => { if (!(k in g)) errors.push(`Missing key: ${k}`); });

    // Range check
    const idx = g?.simulation_master?.enterprise_alignment_index;
    if (typeof idx !== "number" || idx < 0 || idx > 1) errors.push("enterprise_alignment_index must be 0..1");

    // Enums check (light)
    const stance = g?.decision_node?.learner_stance;
    if (!["CONSERVATIVE","BALANCED","AGGRESSIVE"].includes(stance)) errors.push("Invalid learner_stance enum");

    // Input quality gate (if present)
    if (g.input_quality && g.input_quality !== "VALID") errors.push(`input_quality=${g.input_quality}`);

    // PASS rules (beta example)
    const status = g?.completion?.status;
    if (!["PASS","REMEDIATE","FAIL"].includes(status)) errors.push("Invalid completion.status");
  }
  return { ok: errors.length === 0, errors };
}

// ===== Main =====
document.getElementById("runBtn").addEventListener("click", async () => {
  setStatus("Running...");
  document.getElementById("narrative").textContent = "";
  document.getElementById("govjson").textContent = "";

  const payload = {
    prompt_version: PROMPT_VERSION,
    round: 1,
    learner_decision_payload: {
      decision_category: document.getElementById("decision_category").value,
      learner_stance: document.getElementById("learner_stance").value,
      rationale: document.getElementById("rationale").value.trim(),
      risks_accepted: document.getElementById("risks_accepted").value.trim(),
      mitigations: document.getElementById("mitigations").value.trim()
    },
    // In later rounds, include prior_round_governance_json here
    prior_round_governance_json: null
  };

  // Basic input checks (deterministic)
  if (payload.learner_decision_payload.rationale.split(/[.!?]/).filter(s => s.trim()).length < 2) {
    setStatus("Please enter a rationale of at least ~2 sentences.");
    return;
  }
  if (!payload.learner_decision_payload.mitigations) {
    setStatus("Please enter at least one mitigation.");
    return;
  }

  try {
    const res = await fetch(ENDPOINT_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();

    document.getElementById("narrative").textContent = text;

    const gov = extractFencedJson(text);
    document.getElementById("govjson").textContent = gov ? JSON.stringify(gov, null, 2) : "No valid ```json``` block parsed.";

    const v = validateGovernanceJson(gov);

    if (v.ok) {
      setStatus("✅ Governance validated. Marking completion...");
      if (window.SCORM?.setCompleted) window.SCORM.setCompleted(100);
    } else {
      setStatus("⚠️ Validation failed: " + v.errors.join(" | "));
      if (window.SCORM?.setIncomplete) window.SCORM.setIncomplete();
    }
  } catch (e) {
    setStatus("❌ Runtime error: " + (e?.message || e));
    if (window.SCORM?.setIncomplete) window.SCORM.setIncomplete();
  }
});
