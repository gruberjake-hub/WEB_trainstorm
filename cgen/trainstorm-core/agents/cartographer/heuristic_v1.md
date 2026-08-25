# Cartographer heuristic v1 — occurrence intent compiler

*A first compiler pass, not fake instructional-design genius.* Bound values
are closed-vocab members (`vocab/intent.enum.json` / `element.schema.json`
`intent.move` and `intent.rhetorical`). Low-confidence matches are **flagged**
(`ext.cartographer.confidence: low` plus a reason); they are not silently
invented as `practice` / `assess` / `feedback` this SOP does not contain.

Implemented by `tools/cartographer.py`. Policy id: `v1_heuristic_compiler`.

This pass writes **occurrence intent only** (`move`, `teaches`, `rhetorical`,
`intended_response`) onto existing `ele_` records. It never mints `ele_` or
`atom_` ids, never copies meaning onto the element, never writes `atoms.json`.

---

## `move` — first match wins

| # | When (atom structure / kind / id) | `move` | Confidence |
|---|---|---|---|
| 1 | No `belongs_to` (document title / root) | `hook` | high |
| 2 | `atom_id` ends `_purpose`, or source text starts with a purpose-of-this-SOP frame | `objective` | high |
| 3 | Definitions / glossary pointer (`_definitions` in id, or “glossary”/“definitions” as the section) | `activate` | **low** — could be `present`/`support`; treating the glossary as prior knowledge |
| 4 | Roles heading (`_roles` / “Roles and Responsibilities”) | `activate` | **low** — who-acts-here as recall, not a role table dump |
| 5 | Governance-document list or item (`govdocs` in id) | `exemplify` | **low** — named docs that make “operationalizes existing governance” concrete |
| 6 | Handoff / job-bridge step: notify-of-approval, provide outputs to SMT, or “review per SOP-…” | `transfer` | **low** — these are still procedure steps; transfer is the honest Gagné 9b reading, not a new atom |
| 7 | `kind` in `procedure_step`, `list`, `list_item` | `present` | high |
| 8 | Remaining procedure sections (purpose already matched; these are body / section heads) | `present` | high |

No `reinforce`: this SOP store has no closing/summary atom. Do not mint one.
No `practice` / `feedback` / `assess`: the atomized SOP has no learner check.

Closed pedagogical list (must match `intent.enum.json` `dimensions.pedagogical`):
`hook` · `objective` · `activate` · `present` · `exemplify` · `practice` ·
`feedback` · `assess` · `reinforce` · `transfer`.

---

## `teaches[]` — sparse, ontology-bound

Bind to the small ALSAP ontology in `ontology/objectives.json` (draft nodes
distilled from SOP-AST-29080, plus the older AST009 **example** seeds which
this SOP does not teach). Not every occurrence gets every objective.

| Occurrences | `teaches` |
|---|---|
| Root title, purpose, general statement, govdocs list/items | `obj_explain_alsap_purpose` |
| Scope, in-scope org list/items, roles heading | `obj_identify_alsap_scope` |
| Plan-development **steps** (`_proc_a_s*`) | `obj_execute_alsap_plan` |
| Develop-and-maintain **steps** (`_proc_b_s*`) | `obj_execute_alsap_develop_maintain` |
| Analysis-outputs **steps** (`_proc_c_s*`) | `obj_produce_alsap_analysis_outputs` |
| Container labels (`Procedures.`, `A.`/`B.`/`C.` section heads) | **empty** — coverage is a walk over children, not a union stored on the parent (dispatch 2026-08-21) |
| Definitions pointer | **empty** — it names a glossary, it does not teach a capability |

Unknown atoms: empty `teaches`, flag low-confidence. Never mint an `obj_` id
to fill a gap.

---

## `rhetorical` — also a compiler pass

Not a `type`→enum default (the schema forbids treating that as a binding).
Derived from the same atom structure:

| When | `rhetorical` |
|---|---|
| Root / title | `orient` |
| Purpose | `assert` |
| Scope (the applies-to statement, not the org list) | `contextualize` |
| Definitions pointer | `support` |
| `kind: list` | `structure` |
| `kind: list_item` | `specify` |
| `kind: procedure_step` | `assert` |
| General/body explanation | `explain` |
| Section heads (roles, procedures, A/B/C) | `organize` |

Closed rhetorical list: `vocab/intent.enum.json` `dimensions.rhetorical`.

---

## `intended_response` — sparse

Written only where the teaching act names a response worth recording
(hook, objective, transfer). Omitted elsewhere. Open string; not a vocab.

---

## Provenance

Each occurrence that this pass touches gets `ext.cartographer`:

```json
{
  "policy": "v1_heuristic_compiler",
  "tool": "tools/cartographer.py",
  "confidence": "high | low",
  "flags": ["reason_ids"]
}
```

`ext.realized_from` stays Realizer’s. Cartographer does not take
`governance.owner` of the occurrence node. Couturier (`tools/couturier.py`)
owns `element.expression`; this compiler does not write or wipe it.

---

## Extra occurrences (Realizer 1:many seed)

Realizer may mint a second `ele_` of the same atom (`agents/realizer/one_to_many_v1.md`).
That extra exists because its `move` is *different* from the primary. This compiler:

- does **not** re-derive `move` from atom structure for extras — it keeps the
  Realizer-stamped value (`ext.realized_from.target_move` / existing `intent.move`)
- still binds `teaches`, `rhetorical`, and `intended_response` (the last using the
  preserved move)
- flags `extra_occurrence_move_preserved` on `ext.cartographer`
- still mints no ids and still copies no meaning onto the element

Primary occurrences keep the first-match walk above. Do not treat an extra
`reinforce` as a license to invent `practice` / `assess` on 1:1 atoms this SOP
does not contain.
