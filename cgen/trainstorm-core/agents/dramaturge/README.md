# agents/dramaturge — the arc facet owner

**Dramaturge** shapes the course's ARC: the authored, supra-atomic layer of rhetorical and
pedagogical moves — welcomes, closures, persuade glosses, transitions — that the 08-12
decision-log flagged as ownerless and the 2026-08-31 voice hop-two finding (the withheld
midpoint reassurance) made concrete. The seat decided 2026-08-31: a REAL agent seat, one live
wake, the rest declared as placeholders (Jake's split — he wants to tune wake conditions and
watch how the beats arrive differently).

| spine slot | filled with |
|---|---|
| AGENT_NAME | Dramaturge |
| ONE_LINE_ROLE | Proposes where the course needs a content-free beat, and with what intent. |
| FACET / KEYS | arc — beat placement + intent (`occurrences/beats.json`) |
| WAKE_ON | the predicates in `wakes.json` — each a graph query; only `"live": true` wakes run |
| VOCAB_REFS | `vocab/intent.enum.json` (both dimensions — beats carry governed intent, never a new type) |
| MODES | one mode: propose. Dramaturge NEVER writes copy — words are Dragoman voice-mode work against a beat, inverse-guarded |
| SCHEMA_REFS | `schemas/beats.catalog.schema.json` |

**Write contract (the important narrowing):** Dramaturge writes ONLY `status:"proposed"` beat
records into the project's beat catalog. It never sets `accepted` — the designer ratifies by
flipping status in the catalog (authored project data, the scenes.json pattern). It never writes
copy, never touches atoms, elements, scenes, or any voice pack.

| | |
|---|---|
| **Wakes (tunable)** | `wakes.json` — edit params, flip `live`, re-run; that file is the play surface |
| **Runtime code** | `tools/dramaturge.py` (runs live wakes, merges proposals, validates before writing) |
| **Gate** | `tools/validate_arc.py` (schema + governed intent + placement refs resolve; selftest proves red) |
| **Spec** | `beats_v1.md` — the beat model, beat_hash, and the copy flow |

**Run:** `python3 tools/dramaturge.py --project ../brunswick/projects/paytrans`
**Gate:** `python3 tools/validate_arc.py --project ../brunswick/projects/paytrans`
