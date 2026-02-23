import express from "express";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors()); // OK for local demo. Tighten later.
app.use(express.json({ limit: "2mb" }));

const PORT = process.env.PORT || 3000;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

if (!OPENAI_API_KEY) {
  console.error("Missing OPENAI_API_KEY in .env");
  process.exit(1);
}

// Minimal endpoint: accepts your learner payload, calls OpenAI, returns text
app.get("/health", (req, res) => {
  res.json({ ok: true, service: "amlt-proxy", ts: new Date().toISOString() });
});
app.post("/run-amlt", async (req, res) => {
  try {
    const learner = req.body?.learner_decision_payload;
    if (!learner?.rationale) {
      return res.status(400).send("Missing learner_decision_payload.rationale");
    }

    // For demo, we keep this simple: send the AMLT prompt as a single instruction
    // Later you can inject the full AMLT_Simulation_Prompt_v4_2_1 content server-side.
    const systemInstructions = `
You are executing AMLT Meeting Simulation Prompt v4.2.1 (Governance-Hardened).
Return narrative + a single fenced \`\`\`json block matching the governance schema.
Evidence snippets must be direct substrings of learner rationale.
`;

    const userMessage = `
Learner Decision Payload:
- decision_category: ${learner.decision_category}
- learner_stance: ${learner.learner_stance}
- rationale: ${learner.rationale}
- risks_accepted: ${learner.risks_accepted}
- mitigations: ${learner.mitigations}

Start Round 1. Produce the meeting output and governance JSON.
`.trim();

    // Use Responses API (recommended direction in OpenAI docs) :contentReference[oaicite:1]{index=1}
    const resp = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${OPENAI_API_KEY}`, // Bearer auth :contentReference[oaicite:2]{index=2}
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-5",              // adjust to your access
        input: [
          { role: "system", content: systemInstructions },
          { role: "user", content: userMessage }
        ]
      })
    });

    if (!resp.ok) {
      const errText = await resp.text();
      return res.status(resp.status).send(errText);
    }

    const data = await resp.json();

    // Responses API returns output in structured parts; easiest is to concatenate text parts
    const text =
      (data.output || [])
        .flatMap(o => o.content || [])
        .filter(c => c.type === "output_text")
        .map(c => c.text)
        .join("\n\n");

    return res.send(text || JSON.stringify(data, null, 2));
  } catch (e) {
    return res.status(500).send(e?.message || String(e));
  }
});

app.listen(PORT, () => {
  console.log(`AMLT proxy listening on http://localhost:${PORT}`);
});
