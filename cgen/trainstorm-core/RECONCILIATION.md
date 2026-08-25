# Layout Engine → Manifold — reconciliation record

*2026-07-31. The Manifold is the single source of truth; the layout engine was refactored to
conform, plus small additive changes flowed the other way into the canonical vocab. This is the
diff and the rationale. Nothing here writes to git — apply the `trainstorm-core/` files and the two
PATCH docs to your repo yourself.*

> **Settled 2026-08-25** (`architecture/DECISIONS.md`): the node join key is `atom_id`. This July
> record's `element_id` is that same key in a course costume, not a second ID space. Do not mint
> `ele_` IDs.

## What was already right (kept)

The three-orthogonal-concerns model (structure / skin / fill) is the Manifold's *reference-don't-embed*
invariant reached from the deliverable side. It maps cleanly: **structure → `layout_primitive`,
skin → `style_ref`/`token_overrides`, fill → element `content` + selectors**. The `.potx`-as-
capability-surface / sidecar-as-policy split is single-writer in physical form; the `sha256` pin is
`content_hash` applied to the shell. All kept as-is.

## Direction 1 — the layout engine bent to the Manifold

| # | Was (drift) | Now (conformant) | Invariant honored |
|---|---|---|---|
| 1 | `selection.when` fired on ungoverned Script_Normalizer enums (`potential_interaction`, `suggested_visual_type`, `complexity_level`, `emotional_tone`) | `selection.when` fires on governed axes: `script_primitive`, `rhetorical`, `pedagogical`, `tone`, `complexity`, `visual_type`, `requested_interaction`, structural `child_count`; `flags` retained as an ungoverned escape that only warns | Govern the vocabularies / one canonical source |
| 2 | `bindings` interpolated free storyboard strings (`{screen_title}`) — no join key | `bindings` select scene elements by facet (`{scope, where, take}`); every slot resolves to an `element_id`; render record is element-keyed | Stable IDs are the sole join key; renderings keyed by `element_id` |
| 3 | Schema `$id`s used a `cgen.local` placeholder namespace | `$id`s now `https://trainstorm.ai/schemas/...` | One canonical namespace |
| 4 | `SCENARIO_SORT` exemplar grid `3-up` but binding allowed up to 6 (geometry/count drift) | grid normalized to `2x2`, binding max `4` | item_count vs actual |

## Direction 2 — additive into the canonical Manifold (review before commit)

- **`vocab/primitives.registry.json`** — was empty (`status: todo`). Now seeded: 6 `layout_primitive`
  keys (LE ids canonical) + 3 `interaction_primitive` keys (`click_reveal`, `scenario_select`,
  `mcq_single`). First real content for the registry.
- **`vocab/tone.enum.json`, `vocab/complexity.enum.json`, `vocab/visual-type.enum.json`** — NEW
  governed closed lists, promoted from the retired Script_Normalizer axes (your call: promote, not
  map). Governance pattern mirrors `intent.enum.json`.
- **`schemas/PATCH-element.schema.md`** — additive fields: `intent.tone`, `intent.pedagogical`,
  `audience.complexity`, `expression.visual_type`. Delivered as a patch (not a rewritten schema) to
  avoid a drifting copy.
- **`schemas/template_manifest.schema.json` + `schemas/intent_sidecar.schema.json`** — ADOPTED
  into `trainstorm-core/schemas/` as canonical contracts (decision 2026-07-31), alongside
  `element.schema.json`. Per-brand manifests/sidecars stay in `layout-engine/`.
- **`architecture/PATCH-realization-table.md`** — the §4 starter table now references the registered
  `layout_primitive` keys, and names three real coverage gaps the six-layout basis exposes.

## Gaps surfaced

1. ~~**`scenario_select` has no owning script primitive**~~ — **RESOLVED 2026-07-31 (Jake).** Minted
   a governed `scenario` script primitive: a branching decision (situation → decision_points →
   gradient-quality branches with consequences + `leads_to`), structurally distinct from
   `knowledge_check` (which is flat boolean). Delivered as `PATCH-script-primitives-scenario.md`
   (v1 → v1.1, additive). Sidecar now routes `script_primitive:[scenario] → SCENARIO_SORT`; the old
   interaction-only rule stays as fallback. Validated: valid schema, branching sample passes, a
   kc-shaped instance is rejected, full CI clean.
2. **No `process_flow`/timeline layout** in the six — routes to `TITLE_BODY` for now.
3. **`tone`/`visual_type` placement** — modeled on the element; could move to the script primitive
   (see the note in PATCH-element.schema.md). Softest of the placements.
4. **`.potx` sha256 is still all-zeros** — nominal pin until the real extractor runs against
   `astellas_v1.potx`.

## Validation performed

`ci/validate_sidecar.py` on `astellas.awareness`: **OK, 0 warnings** against the full governed set.
Negative tests all fail correctly: ungoverned `script_primitive` value → FAIL; unregistered layout →
FAIL; legacy free-string binding → FAIL (schema + selector check); non-empty `flags` → WARN, still
passes.
