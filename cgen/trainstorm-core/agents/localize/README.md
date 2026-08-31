# agents/localize — Dragoman: the meaning-rendering agent

Dragoman owns the **meaning-rendering space**; language and register are coordinates (DECISIONS
2026-08-31, voice-pack contract). Two mode instantiations live here, one file each, sharing the
two-speed principle, the flag discipline, and the draft-only bright line — but each mode declares
its OWN gate profile:

| mode | coordinate | prompt | gate | acceptance | store |
|---|---|---|---|---|---|
| translation | locale | `system.md` (`loc-agent.v0.1`) | `tools/localize/verify_agent_output.py` (QE) | in-country reviewer | `locales/<lang>.json` |
| **voice** | register | `voice.system.md` (`voice-agent.v0.1`) | `tools/localize/voice_gate.py` (invent-guard — the stricter profile: a failing copywriter INVENTS) | `tools/localize/voice_accept.py`, the pack's ONLY writer | `<project>/voice/<register>.json` |

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
