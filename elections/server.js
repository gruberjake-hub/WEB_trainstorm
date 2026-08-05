/* ===========================================================================
 * server.js  —  THE HARNESS
 * ---------------------------------------------------------------------------
 * This is the whole back end, in one file, with no external packages.
 *
 * What it does, in plain terms:
 *   1. On startup it reads two text files off disk — your system profile
 *      (system-prompt.md) and your rule corpus (knowledge/project_context.md)
 *      — and glues them together into ONE big "system prompt". That combined
 *      text is the personality + the law that the AI uses on every request.
 *   2. It serves the field-capture web app (public/index.html) to any phone or
 *      laptop that opens the site.
 *   3. When an observer taps "Draft complaint", the app sends the structured
 *      incident record here to POST /api/draft. This file forwards it to the
 *      Anthropic API together with the system prompt, waits for the draft, and
 *      sends it back to the phone.
 *
 * The one secret — your Anthropic API key — lives HERE, on the server, in an
 * environment variable. It is never sent to the phones. That is the entire
 * point of having a server instead of just a web page.
 * ========================================================================= */

const http = require("http");
const fs = require("fs");
const path = require("path");

// ---- Configuration, read from environment variables -----------------------
// An "environment variable" is just a named value the operating system hands
// to the program when it starts. Locally you set them in a .env file (loaded
// just below). On a host like Render you type them into the dashboard.
loadDotEnvIfPresent();

const API_KEY = process.env.ANTHROPIC_API_KEY || "";
const MODEL = process.env.MODEL || "claude-sonnet-5";
const ACCESS_CODE = process.env.ACCESS_CODE || ""; // drafter code -> /api/draft
// Observer rules-check: a shared team code gates /api/check, and CHECK_MODEL
// picks the (cheaper) model for it. Default Haiku for speed/cost; set to
// claude-sonnet-5 to A/B the quality and see real cost before the midterm.
const TEAM_CODE = process.env.TEAM_CODE || ""; // team code -> /api/check
const CHECK_MODEL = process.env.CHECK_MODEL || "claude-haiku-4-5-20251001";
// Central collection: the URL of your Google Apps Script web app. When set,
// observers' "Submit to team" pushes rows into your Google Sheet through it.
const SHEET_WEBHOOK_URL = process.env.SHEET_WEBHOOK_URL || "";
const PORT = process.env.PORT || 3000;
const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
const ANTHROPIC_VERSION = "2023-06-01";
const MAX_TOKENS = 8000;

// ---- Build the system prompt once, at startup ------------------------------
const PROFILE = readFileSafe(path.join(__dirname, "system-prompt.md"));
const CORPUS = readFileSafe(
  path.join(__dirname, "knowledge", "project_context.md")
);
const SYSTEM_PROMPT =
  PROFILE +
  "\n\n===========================================================\n" +
  "APPENDED SOURCE OF TRUTH — project_context.md (the loaded rule corpus)\n" +
  "===========================================================\n\n" +
  CORPUS;

// ---------------------------------------------------------------------------
// The HTTP server. Every request that arrives is handled by this function.
// ---------------------------------------------------------------------------
const server = http.createServer(async (req, res) => {
  try {
    // Health check — handy for confirming the server is alive and configured.
    if (req.method === "GET" && req.url === "/health") {
      return sendJSON(res, 200, {
        ok: true,
        model: MODEL,
        apiKeyConfigured: Boolean(API_KEY),
        accessCodeRequired: Boolean(ACCESS_CODE),
        centralCollection: Boolean(SHEET_WEBHOOK_URL),
        teamCodeRequired: Boolean(TEAM_CODE),
        checkModel: CHECK_MODEL,
      });
    }

    // The drafting endpoint — the reason the server exists.
    if (req.method === "POST" && req.url === "/api/draft") {
      return await handleDraft(req, res);
    }

    // Observer rules-check: a quick, advisory "what do you think of this?"
    if (req.method === "POST" && req.url === "/api/check") {
      return await handleCheck(req, res);
    }

    // Central collection: forward submitted observations to the Google Sheet.
    if (req.method === "POST" && req.url === "/api/submit") {
      return await handleSubmit(req, res);
    }

    // Everything else: serve a static file from /public.
    if (req.method === "GET") {
      return serveStatic(req, res);
    }

    sendJSON(res, 405, { error: "Method not allowed" });
  } catch (err) {
    console.error("Unhandled error:", err);
    sendJSON(res, 500, { error: "Server error", detail: String(err) });
  }
});

server.listen(PORT, () => {
  console.log(`\n  Election Complaint Harness is running.`);
  console.log(`  Open:   http://localhost:${PORT}`);
  console.log(`  Model:  ${MODEL}`);
  console.log(`  API key configured: ${API_KEY ? "yes" : "NO — set ANTHROPIC_API_KEY"}`);
  console.log(`  Access code gate:   ${ACCESS_CODE ? "on" : "off"}`);
  console.log(`  Central collection: ${SHEET_WEBHOOK_URL ? "on (Google Sheet)" : "off"}`);
  console.log(`  Rules-check model:  ${CHECK_MODEL}`);
  console.log(`  Team code gate:     ${TEAM_CODE ? "on" : "off"}\n`);
});

// ===========================================================================
// Handlers
// ===========================================================================

async function handleDraft(req, res) {
  // 1. Guard the key. If it isn't set, fail loudly and clearly.
  if (!API_KEY) {
    return sendJSON(res, 500, {
      error:
        "The server has no ANTHROPIC_API_KEY set. Add it and restart the server.",
    });
  }

  // 2. Read the JSON the phone sent us.
  const body = await readBody(req);
  let payload;
  try {
    payload = JSON.parse(body || "{}");
  } catch {
    return sendJSON(res, 400, { error: "Request body was not valid JSON." });
  }

  // 3. Optional shared-password gate. If you set ACCESS_CODE, the app must
  //    send a matching code or we refuse — this keeps strangers off your key.
  if (ACCESS_CODE && payload.accessCode !== ACCESS_CODE) {
    return sendJSON(res, 401, {
      error: "Wrong or missing access code.",
    });
  }

  // 4. Turn the structured field record into a clean Mode 2 drafting request.
  const userMessage = buildUserMessage(payload);

  // 5. Call the Anthropic API.
  let apiResponse;
  try {
    apiResponse = await fetch(ANTHROPIC_URL, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": ANTHROPIC_VERSION,
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        system: SYSTEM_PROMPT,
        messages: [{ role: "user", content: userMessage }],
      }),
    });
  } catch (err) {
    return sendJSON(res, 502, {
      error: "Could not reach the Anthropic API.",
      detail: String(err),
    });
  }

  // 6. Handle API errors (bad key, wrong model name, rate limit, no credit...).
  if (!apiResponse.ok) {
    const errText = await apiResponse.text();
    console.error("Anthropic API error:", apiResponse.status, errText);
    return sendJSON(res, 502, {
      error: `Anthropic API returned ${apiResponse.status}.`,
      detail: safeTrim(errText, 600),
    });
  }

  // 7. Pull the draft text out of the response and send it to the phone.
  const data = await apiResponse.json();
  const draft = (data.content || [])
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("\n")
    .trim();

  return sendJSON(res, 200, {
    draft: draft || "(The model returned no text.)",
    model: MODEL,
    usage: data.usage || null,
  });
}

// Convert the app's structured payload into the plain-English request the
// system profile expects for a Mode 2 draft.
function buildUserMessage(p) {
  const filingMode =
    p.filingMode === "attorney" ? "Attorney-filed" : "Observer-filed";

  const lines = [];
  lines.push("MODE 2 — COMPLAINT DRAFTING REQUEST");
  lines.push("");
  lines.push(`Filing mode: ${filingMode}`);
  lines.push("");

  lines.push("== OBSERVER / SOURCE OF RECORD ==");
  const o = p.observer || {};
  lines.push(`Observer name: ${orTBD(o.name)}`);
  lines.push(`Credential / role: ${orTBD(o.credential)}`);
  lines.push(`Organization: ${orTBD(o.organization)}`);
  lines.push(`Standing basis: ${orTBD(o.standing)}`);
  lines.push(`County / jurisdiction: ${orTBD(o.county)}`);
  lines.push(`Observable location type: ${orTBD(o.locationType)}`);
  lines.push("");

  if (p.filingMode === "attorney") {
    lines.push("== FILING ATTORNEY (filer of record) ==");
    const a = p.attorney || {};
    lines.push(`Party / candidate: ${orTBD(a.party)}`);
    lines.push(`Attorney name: ${orTBD(a.name)}`);
    lines.push(`Bar number: ${orTBD(a.bar)}`);
    lines.push(`Contact: ${orTBD(a.contact)}`);
    lines.push("");
  }

  lines.push("== RESPONDENT ==");
  lines.push(orTBD(p.respondent));
  lines.push("");

  lines.push("== RELIEF REQUESTED (observer's preference; refine as needed) ==");
  lines.push(orTBD(p.relief));
  lines.push("");

  lines.push("== FILING TARGET (observer's note; verify) ==");
  lines.push(orTBD(p.filingTarget));
  lines.push("");

  lines.push("== INCIDENT RECORD (first-person field observations) ==");
  const entries = Array.isArray(p.entries) ? p.entries : [];
  if (entries.length === 0) {
    lines.push("(No incident entries were supplied.)");
  }
  entries.forEach((e, i) => {
    lines.push("");
    lines.push(`--- Incident ${i + 1} ---`);
    lines.push(`Date/time observed: ${orTBD(e.time)}`);
    lines.push(`Location (station/table/ward): ${orTBD(e.location)}`);
    lines.push(`What was observed (actions): ${orTBD(e.observed)}`);
    lines.push(
      `Who performed it (role / name / description / wristband / badge): ${orTBD(
        e.actor
      )}`
    );
    lines.push(`Witnesses present: ${orTBD(e.witnesses)}`);
    lines.push(`On-site objection raised?: ${orTBD(e.objectionRaised)}`);
    lines.push(`Objection statement / to whom / response: ${orTBD(e.objectionDetail)}`);
    lines.push(`Evidence and current custody: ${orTBD(e.evidence)}`);
    lines.push(`Recorded by team on EL 104?: ${orTBD(e.el104)}`);
    if (e.issueTags && e.issueTags.length) {
      lines.push(`Issue category tags: ${e.issueTags.join("; ")}`);
    }
    if (e.suggestedCite) {
      lines.push(`Observer's suggested citation (verify against corpus): ${e.suggestedCite}`);
    }
    if (e.notes) lines.push(`Additional notes: ${e.notes}`);
  });

  lines.push("");
  lines.push("== INSTRUCTIONS ==");
  lines.push(
    "Produce a complete Mode 2 draft per the profile: apply the eight-element anatomy, mark every rule citation with [DIRECT CITATION] / [INFERRED] / [NOT FOUND] against the appended corpus, and append the DISMISSAL RISK ASSESSMENT. " +
      (p.filingMode === "attorney"
        ? "Because this is attorney-filed, lead with the ATTORNEY REVIEW CHECKLIST. "
        : "") +
      "Flag any missing or thin element explicitly rather than inventing facts."
  );

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Observer rules-check. A tightly scoped, advisory-only assistant. It is NOT
// the drafting profile — it flags, it never adjudicates, and it always tells
// the observer to capture facts and log the observation regardless.
// ---------------------------------------------------------------------------
const CHECK_INSTRUCTIONS =
  "You are a field rules-check aid for a credentialed election observer in Wisconsin. " +
  "An observer will briefly describe something they are seeing at an observable location. " +
  "Use ONLY the appended rule corpus (Wis. Admin. Code ch. EL 4 and the observer guidance) as authority. " +
  "Respond in 2–4 short sentences, plain language, for someone standing on the counting floor:\n" +
  "1) Say whether what is described MAY implicate a rule, appears likely to be a violation, or does not appear to implicate ch. EL 4 — and name the specific provision (e.g., EL 4.03(1)(b)) when one applies.\n" +
  "2) Open with a confidence tag in brackets: [LIKELY VIOLATION], [POSSIBLE — VERIFY], or [NOT APPARENT], based only on the corpus.\n" +
  "3) Always tell the observer the specific facts to capture now — exact time, location/table/ward, who by role and description, witnesses — and to log the observation regardless. A drafter, and if needed an attorney, decides later.\n" +
  "Rules of the road: never adjudicate with certainty; never discourage logging; if the corpus does not address the scenario, say so plainly and still advise capturing the facts. Do not draft a complaint. Keep it terse.";

async function handleCheck(req, res) {
  if (!API_KEY) {
    return sendJSON(res, 500, {
      error: "The server has no ANTHROPIC_API_KEY set.",
    });
  }

  const body = await readBody(req);
  let payload;
  try {
    payload = JSON.parse(body || "{}");
  } catch {
    return sendJSON(res, 400, { error: "Request body was not valid JSON." });
  }

  // Team-code gate — keeps this paid endpoint off the open internet.
  if (TEAM_CODE && payload.teamCode !== TEAM_CODE) {
    return sendJSON(res, 401, {
      error: "Wrong or missing team code. Enter it under Setup.",
    });
  }

  const text = (payload.text || "").toString().trim();
  if (!text) {
    return sendJSON(res, 400, { error: "Describe what you're seeing first." });
  }

  let apiResponse;
  try {
    apiResponse = await fetch(ANTHROPIC_URL, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": ANTHROPIC_VERSION,
      },
      body: JSON.stringify({
        model: CHECK_MODEL,
        max_tokens: 500,
        // Corpus is marked for prompt caching so repeated checks are cheap.
        system: [
          { type: "text", text: CHECK_INSTRUCTIONS },
          {
            type: "text",
            text:
              "APPENDED SOURCE OF TRUTH — the loaded rule corpus:\n\n" + CORPUS,
            cache_control: { type: "ephemeral" },
          },
        ],
        messages: [
          {
            role: "user",
            content: "Observer is seeing this right now:\n\n" + text,
          },
        ],
      }),
    });
  } catch (err) {
    return sendJSON(res, 502, {
      error: "Could not reach the Anthropic API.",
      detail: String(err),
    });
  }

  if (!apiResponse.ok) {
    const errText = await apiResponse.text();
    return sendJSON(res, 502, {
      error: `Anthropic API returned ${apiResponse.status}.`,
      detail: safeTrim(errText, 500),
    });
  }

  const data = await apiResponse.json();
  const assessment = (data.content || [])
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("\n")
    .trim();

  return sendJSON(res, 200, {
    assessment: assessment || "(No response.)",
    model: CHECK_MODEL,
    usage: data.usage || null,
  });
}

// The columns written to the Google Sheet, in order. The Apps Script writes
// this as the header row the first time, then one row per observation.
const SUBMIT_COLUMNS = [
  "Record ID",
  "Revision",
  "Status",
  "Submitted (server time)",
  "Observer",
  "Organization",
  "County",
  "Time observed",
  "Location",
  "What observed",
  "Who (role/name/description)",
  "Witnesses",
  "Objection raised",
  "Objection detail",
  "Evidence & custody",
  "EL 104?",
  "Issue tags",
  "Suggested citation",
  "Notes",
];

// Receives {observer, entries:[...]} from an observer's phone and forwards it,
// row by row, to your Google Sheet via the Apps Script web app.
async function handleSubmit(req, res) {
  if (!SHEET_WEBHOOK_URL) {
    return sendJSON(res, 501, {
      error:
        "Central collection isn't set up yet. The server has no SHEET_WEBHOOK_URL. See the README, 'Central collection'.",
    });
  }

  const body = await readBody(req);
  let payload;
  try {
    payload = JSON.parse(body || "{}");
  } catch {
    return sendJSON(res, 400, { error: "Request body was not valid JSON." });
  }

  const entries = Array.isArray(payload.entries) ? payload.entries : [];
  if (entries.length === 0) {
    return sendJSON(res, 400, { error: "No observations to submit." });
  }

  const o = payload.observer || {};
  const stamp = new Date().toISOString();
  const rows = entries.map((e) => {
    const rev = Number(e.rev) || 1;
    const status = rev > 1 ? `Edit — supersedes v${rev - 1}` : "Original";
    return [
    e.id || "",
    `v${rev}`,
    status,
    stamp,
    o.name || "",
    o.organization || "",
    o.county || "",
    e.time || "",
    e.location || "",
    e.observed || "",
    e.actor || "",
    e.witnesses || "",
    e.objectionRaised || "",
    e.objectionDetail || "",
    e.evidence || "",
    e.el104 || "",
    Array.isArray(e.issueTags) ? e.issueTags.join("; ") : "",
    e.suggestedCite || "",
    e.notes || "",
    ];
  });

  let r;
  try {
    r = await fetch(SHEET_WEBHOOK_URL, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ header: SUBMIT_COLUMNS, rows }),
    });
  } catch (err) {
    return sendJSON(res, 502, {
      error: "Could not reach the Google Sheet web app.",
      detail: String(err),
    });
  }

  if (!r.ok) {
    const t = await r.text();
    return sendJSON(res, 502, {
      error: `The Google Sheet web app returned ${r.status}.`,
      detail: safeTrim(t, 400),
    });
  }

  return sendJSON(res, 200, { ok: true, submitted: rows.length });
}

// ===========================================================================
// Small helpers
// ===========================================================================

function serveStatic(req, res) {
  // Map "/" to index.html; strip query strings; block path traversal.
  let urlPath = decodeURIComponent(req.url.split("?")[0]);
  if (urlPath === "/") urlPath = "/index.html";
  const filePath = path.join(__dirname, "public", path.normalize(urlPath));
  if (!filePath.startsWith(path.join(__dirname, "public"))) {
    return sendJSON(res, 403, { error: "Forbidden" });
  }
  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404, { "content-type": "text/plain" });
      return res.end("Not found");
    }
    res.writeHead(200, { "content-type": contentType(filePath) });
    res.end(content);
  });
}

function contentType(file) {
  if (file.endsWith(".html")) return "text/html; charset=utf-8";
  if (file.endsWith(".js")) return "text/javascript; charset=utf-8";
  if (file.endsWith(".css")) return "text/css; charset=utf-8";
  if (file.endsWith(".json")) return "application/json; charset=utf-8";
  if (file.endsWith(".svg")) return "image/svg+xml";
  return "application/octet-stream";
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => {
      data += chunk;
      if (data.length > 2_000_000) {
        // ~2MB cap; reject absurdly large bodies.
        reject(new Error("Request body too large"));
        req.destroy();
      }
    });
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

function sendJSON(res, status, obj) {
  res.writeHead(status, { "content-type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(obj));
}

function readFileSafe(p) {
  try {
    return fs.readFileSync(p, "utf8");
  } catch (err) {
    console.error(`Could not read ${p}:`, err.message);
    return "";
  }
}

function orTBD(v) {
  const s = (v == null ? "" : String(v)).trim();
  return s.length ? s : "[NOT PROVIDED]";
}

function safeTrim(s, n) {
  s = String(s || "");
  return s.length > n ? s.slice(0, n) + "…" : s;
}

// A tiny .env loader so you don't need any extra package. It reads a file
// named ".env" in this folder and copies KEY=value lines into the environment.
function loadDotEnvIfPresent() {
  try {
    const envPath = path.join(__dirname, ".env");
    if (!fs.existsSync(envPath)) return;
    const text = fs.readFileSync(envPath, "utf8");
    for (const rawLine of text.split("\n")) {
      const line = rawLine.trim();
      if (!line || line.startsWith("#")) continue;
      const eq = line.indexOf("=");
      if (eq === -1) continue;
      const key = line.slice(0, eq).trim();
      let val = line.slice(eq + 1).trim();
      // strip surrounding quotes if present
      if (
        (val.startsWith('"') && val.endsWith('"')) ||
        (val.startsWith("'") && val.endsWith("'"))
      ) {
        val = val.slice(1, -1);
      }
      if (!(key in process.env)) process.env[key] = val;
    }
  } catch (err) {
    console.error("Could not load .env:", err.message);
  }
}