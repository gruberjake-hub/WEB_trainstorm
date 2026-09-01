# agents/responsive_engine — the direction facet owner

**The Responsive Engine**, born in its design-time mode. The roster seat that will one day meet
the learner, doing today the half of its job that needs no learner: **resolving the audience join**
and writing `direction`.

| spine slot | filled with |
|---|---|
| AGENT_NAME | Responsive Engine |
| ONE_LINE_ROLE | Resolves the audience join and directs how content should LAND for one segment — weight and tempo, never words, never styles. |
| FACET / KEYS | `direction` — weight + tempo + reason trace (`direction/<segment_id>.json`) |
| WAKE_ON | a project has a segment record in `audience/` and elements whose direction is unresolved or stale against either pin |
| VOCAB_REFS | `vocab/direction.enum.json` (weight · tempo) · `vocab/disposition.enum.json` (the factors a reason may cite) |
| MODES | `resolve` (live) · `serve` (declared, `live:false`) — see `modes.json` |
| SCHEMA_REFS | `schemas/direction.pack.schema.json` (validates its writes) · reads `audience-model.schema.json`, `element.schema.json` |

**Write contract.** Sole writer of `direction`. It never writes meaning, style, narration, arc or
the audience model itself — and it holds **no PII in either mode**. The learner-state half of the
roster's old one-line Responsive Engine (transcript, posteriors, evidence) is a **separate future
seat**; the horizon already separates them (*LRE serves · Bayesians infer · Transcript stores*),
and this seat is the *decision* half, which is exactly why it can exist now.

**Two modes, one of which runs.**

- `resolve` — **live.** Design-time batch: walk every element × one segment record, materialize a
  pack of `proposed` bindings. A human accepts **bindings**.
- `serve` — **declared, not live.** The same pure resolver under a serve-one harness: one element,
  one live learner, nothing materialized. A human accepts the **policy**, and the runtime may serve
  only what the accepted policy produces. Asking for it is refused with its reason. It waits on the
  horizon's activation signals — and on an accepted-binding corpus large enough to license
  accepting a policy at all.

The promotion path is therefore not new wiring. `propose()` / `clamp()` / `baseline()` are **pure
functions** — dicts in, dicts out, no I/O and no clock. Only the harness swaps.

| | |
|---|---|
| **Runtime code** | `tools/responsive_engine.py` (policy `direction_v1`; `--selftest` proves the core 14 ways) |
| **Gate** | `tools/validate_direction.py` |
| **Spec** | `direction_v1.md` — the rule set, the two structural disciplines, and the harm clamp |
| **Modes** | `modes.json` — the play surface; flipping `serve` to live is a decision, not a config tweak |

**Run:** `python3 tools/responsive_engine.py --project ../brunswick/projects/paytrans`
**Dry-run one record:** `… --audience reference/example_audience_segment.json --dry-run`
**Gate:** `python3 tools/validate_direction.py --project ../brunswick/projects/paytrans`
