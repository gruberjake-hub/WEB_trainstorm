# agents/localize — the localization (translation) agent

One agent = one folder here: its **governed prompt** + this manifest. The *code* that runs it lives in `tools/localize/`; the *memory* it retrieves from lives in `registry/`. This folder holds only the contract, so the prompt can be versioned and reasoned about like a schema.

| | |
|---|---|
| **Prompt** | `system.md` — the paste-ready instruction (`loc-agent.v0.1`). Config header at the top instantiates it for EN→JA. |
| **Reads (memory)** | `registry/glossary/astellas-pv.candidates.csv` · `registry/corpus/astellas-pv.ja.jsonl` |
| **Runtime code** | `tools/localize/build_agent_call.py` (assembles the call) · `tools/localize/verify_agent_output.py` (QE gate + locale mapping) |
| **Input** | one element's `content.text` + `element_id` + `source_hash` (per `schemas/element.schema.json`) |
| **Output** | draft JSON (`status:"draft"`, `confidence`, `term_compliance`, `flags`) → QE gate → human review → `locales/ja.json` |

**Run the assembly demo:** `python tools/localize/build_agent_call.py`
**Run the gate/mapping check:** `python tools/localize/verify_agent_output.py`

The agent never sets `status:"validated"` — only the in-country reviewer does, downstream. The `source_hash` is the join that flags a translation as stale when the English changes.
