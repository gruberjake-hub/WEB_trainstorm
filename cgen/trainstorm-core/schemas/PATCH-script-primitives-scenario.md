# PATCH — add `scenario` to script.primitives.v1.json

**Apply to:** `trainstorm-core/schemas/script.primitives.v1.json` (canonical, in git).
**Type:** additive. Existing scripts still validate — this only adds a new member to the
primitive union. Bump the vocabulary marker **v1 → v1.1**.
**Decision:** 2026-07-31 (Jake). Resolves open gap #1 from the layout-engine reconciliation:
`scenario_select` had no owning script primitive.

## Why a new type (and not a knowledge_check variant)

A `knowledge_check` is a flat right/wrong check: each option carries a boolean `correct`. The
thing Jake wants is a **branching decision the learner works through** — a real situation, choices
graded on a *gradient* (optimal / acceptable / suboptimal / incorrect), each with a *consequence*
narrative, and optional `leads_to` pointers that fork to further decision points. That shape is
genuinely different from `knowledge_check` and can't be expressed by it, which is what earns it a
first-class type rather than a presentation variant. (The illustrate-a-concept sense of "scenario"
stays where it already lives: pedagogical `exemplify` realized via `role_relevance`/`context_frame`.)

## 1. Add to `$defs`

```json
{
  "type": "object",
  "description": "A branching decision the learner works through: a real situation, one or more decision points, and choices whose consequences and feedback differ by QUALITY on a gradient — not a single right/wrong check (that is knowledge_check). Structural home for scenario_select interactions; delivery is interactive (behavior-driven / Storyline).",
  "required": ["type", "situation", "decision_points"],
  "additionalProperties": false,
  "properties": {
    "type": { "const": "scenario" },
    "situation": { "type": "string", "description": "The real-world setup the learner is placed in — the grounding narrative (source-locale meaning)." },
    "role": { "type": "string", "description": "Optional target role/segment the situation is framed for (may map to audience.segment_scope)." },
    "decision_points": {
      "type": "array", "minItems": 1,
      "description": "Ordered decision nodes. More than one node, or any use of branch.leads_to, makes the scenario multi-step / branching.",
      "items": {
        "type": "object",
        "required": ["id", "prompt", "branches"],
        "additionalProperties": false,
        "properties": {
          "id": { "type": "string", "description": "Local node id, referenced by branch.leads_to." },
          "prompt": { "type": "string", "description": "The decision the learner faces at this node." },
          "branches": {
            "type": "array", "minItems": 2,
            "description": "The choices at this node — two or more.",
            "items": {
              "type": "object",
              "required": ["label", "quality"],
              "additionalProperties": false,
              "properties": {
                "label": { "type": "string", "description": "The choice as the learner sees it." },
                "quality": { "type": "string", "enum": ["optimal", "acceptable", "suboptimal", "incorrect"],
                  "description": "Graded on a gradient, not a boolean — this is what distinguishes a scenario from a knowledge_check." },
                "consequence": { "type": "string", "description": "What happens in the situation if this is chosen (the branching narrative)." },
                "feedback": { "type": "string", "description": "Coaching shown for this choice." },
                "leads_to": { "type": "string", "description": "Optional decision_point id this choice branches to; omit to end the scenario." }
              }
            }
          }
        }
      }
    },
    "id": { "type": "string" },
    "pedagogical_intent": { "type": "string", "description": "Default: practice (or assess)." },
    "notes": { "type": "string" }
  }
}
```

## 2. Add to the primitive union

Add `{ "$ref": "#/$defs/scenario" }` to the top-level `oneOf` that unions the primitive types
(the same union that lists `knowledge_check`, `process_flow`, etc.).

## 3. Routing / realization (derived, not hand-set)

- `pedagogical_intent` default **practice** (or **assess**) → `delivery` = **interactive**
  (behavior-driven / Storyline), consistent with the intent.enum render-routing note.
- Realization: **scenario_select** interaction_primitive → **SCENARIO_SORT** layout. The sidecar
  now routes `script_primitive: [scenario] → SCENARIO_SORT` as the primary rule; the older
  `requested_interaction: [scenario_select]` rule remains as an explicit fallback.
- registries unchanged: `scenario_select` is already a registered `interaction_primitive` and
  `SCENARIO_SORT` a registered `layout_primitive` — this patch just gives them a governed source.

## 4. Validation evidence

Checked before delivery (`scenario.example.json` is the worked instance):
- the `$def` is a valid JSON Schema (Draft 2020-12);
- a two-node **branching** sample validates against it (0 errors);
- a `knowledge_check`-shaped instance (boolean `correct`) is **rejected** as a scenario —
  confirming the two types don't collapse into each other;
- the full CI contract test (`validate_sidecar.py`) passes clean with `scenario` governed and routed.
