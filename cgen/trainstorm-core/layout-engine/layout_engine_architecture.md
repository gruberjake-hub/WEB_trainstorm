> **Manifold conformance banner (2026-07-31).** This architecture record is the ORIGINAL
> deliverable-side design. It has since been reconciled to the Manifold as the single source of
> truth. Where this doc says selection fires on *Script_Normalizer enums*, that is superseded:
> selection now fires on the Manifold's governed vocabularies, and bindings select elements by
> `element_id` rather than interpolating storyboard fields. See `README.md` (Manifold conformance)
> and the repo-root `RECONCILIATION.md` for the diff and rationale. The three-orthogonal-concerns
> model below is unchanged and is exactly what carried over.

---

# Layout Engine — architecture record

_Captured 2026-07-31 from a Course_Builder implementation session (GEN607 work). This
is the deliverable-side design for turning content + intent into Storyline-ready PPTX
via reusable layouts. Parallel to, and pending reconciliation with, the Manifold
architecture project._

## Problem

Move toward automated course generation from the tactical side by building reusable
**PPT slide layouts / master templates** (easiest clean import into Storyline). The
layouts must bind with the intent signals the pipeline already produces — brand intent
(Context Capsule) and learning intent (Script_Normalizer per-screen enums).

## Core model — three orthogonal concerns

Keep these strictly separate; it's the property that makes the system scale:

- **Structure (layout)** — the archetype (title+body, reveal grid, scenario sort,
  venn, KC). Selected by learning/interaction intent.
- **Skin (brand)** — palette, fonts, logo, spacing. Applied as a **token theme**, never
  baked per layout.
- **Fill (content)** — storyboard fields poured into named slots with overflow rules.

Consequence: one layout works across every brand (swap tokens); one brand works across
every layout (same tokens). If you ever feel pressure to build "the same layout but for
brand X," the skin has leaked into the structure.

Layouts are the **resolution target**, not a peer of the intent engine. The intent
signals *select* a layout and *fill* it. And the layout set must stay a **small
orthogonal basis** (~8–12 archetypes); the intent space (brand × interaction × visual ×
complexity × tone) is combinatorial, so express variation as tokens/parameters, not new
layouts.

## The physical decision: .potx as capability surface + text sidecar as policy

Chosen approach (of four considered): **author/tune layouts in a `.potx`, and generate
the parameterized layout binding against it.** The `.potx` is the capability surface
(what layouts/slots/theme exist); a text **sidecar** is the policy over that surface
(which layout serves which intent, how fields bind). This reconciles architecture vs.
one-off deliverable — same front door serves both.

Two files, changing for different reasons and by different hands:

1. **Template manifest** — *generated from the `.potx`*, not hand-authored. Theme
   colors/fonts (from `theme1.xml`), canvas, and per-layout **slot** geometry + names +
   Storyline binding metadata. Pure structure/skin, no intent.
2. **Intent sidecar** — *hand-authored* policy. Ordered `selection` rules (predicates
   over Script_Normalizer enums → layout id), per-layout `bindings` (field→slot with
   `repeat`/`overflow`), optional `token_overrides` (re-skin), `interaction_defaults`.
   Pins to a manifest by `sha256`.

One `.potx` supports **many sidecars**: swap sidecar → different *selection + skin*;
swap `.potx` → different *visual vocabulary*. A sidecar can only reference layouts/slots
the `.potx` provides.

## Backward flow (the authored workflow)

Never hand-write the manifest:

1. Author/tune `<brand>_vN.potx` in PowerPoint under an **authoring contract**: real
   placeholders (not free text boxes), theme colors (not pasted hex), named shapes
   (esp. controls: `btn_continue`, `opt`, `choice`), layout names by convention
   (`AST_RevealGrid`).
2. Run the **extractor** (to build) → emits `template_manifest.json` **and** a
   *scaffolded sidecar* (layouts pre-listed, empty selection/bindings). Intent is the
   one thing the `.potx` can't carry, so the scaffold drops you exactly at the one
   hand-authored step.
3. Author sidecar policy (selection + bindings).
4. CI gate validates sidecar ↔ manifest.

## Rendering strategies (per layout)

- **native** — fill the `.potx` layout's own placeholders (highest fidelity, cleanest
  Storyline import, fixed slots). Best for static/simple layouts.
- **programmatic** — re-draw with extracted tokens (pptxgenjs path). Needed for
  variable-N grids, computed reveal panels, overflow. `.potx` supplies one **exemplar**
  card; generator clones/positions N.

## Integration with existing pipeline

- **Context Capsule** `asset_branding.palette` / `brand_tone` / `style_guide` → manifest
  theme + sidecar `token_overrides`.
- **Script_Normalizer** enums (`potential_interaction`, `suggested_visual_type`,
  `complexity_level`, `emotional_tone`, `key_concepts` count, free `flags`) → sidecar
  `selection` predicates.
- **Storyboard** fields → `bindings` (slot map + repeat).
- **CREATOR** PPTX + Storyline wiring (named shapes, `SL_CONTROL` alt-text, trigger
  notes, layers/variables) → the render layer + slot `storyline` metadata. Layouts
  carry the binding contract, not just visuals.

## Git / hosting

Text (manifests, sidecars, schemas, CI) in normal git — diffable, PR-reviewable,
CI-testable. The binary `.potx` in git-LFS or an artifact/object store, pinned by
sha256, never diffed. Volatile policy in git; rare binary as a pinned artifact. (Mirrors
the ADRA corpus-fingerprint habit.)

## Artifacts produced this session

Starter delivered to the user (schemas validated, examples conform, CI contract passes
+ fails correctly on a broken ref):

```
layout-engine/
├── _schema/template_manifest.schema.json
├── _schema/intent_sidecar.schema.json
├── templates/astellas/template_manifest.example.json   # 6 layouts from GEN607 work
├── sidecars/astellas.awareness.sidecar.json
├── ci/validate_sidecar.py                              # schema + sha256 pin + refs/slots
└── README.md
```
Six seed layouts (from real GEN607 slides): `TITLE_BODY`, `STATIC_CARDS_3`,
`REVEAL_GRID`, `SCENARIO_SORT`, `DIAGRAM_VENN`, `KC_SINGLE`.

## Open / next

- Build the `.potx` extractor (python-pptx: theme, fonts, layout placeholders w/
  geometry) → manifest + scaffolded sidecar.
- Reconcile with Manifold's intent-space representation (see rehydration brief).
- Related skill shipped separately: `storyline-review-reconciliation` (SME comments →
  translation matrix).