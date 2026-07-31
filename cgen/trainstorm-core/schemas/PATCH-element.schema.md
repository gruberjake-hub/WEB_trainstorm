# PATCH — element.schema.json (additive, for the layout-engine reconciliation)

*2026-07-31. Additive only — no field is removed or retyped, so existing elements stay valid.
Delivered as a patch, not a rewritten file, so it applies cleanly on top of the canonical
`element.schema.json` in git without spawning a drifting copy. Apply the three (optionally four)
snippets below.*

These fields let the governed layout-engine `selection` fire on element facets instead of the
retired Script_Normalizer enums. Each points at a governed vocabulary added in `vocab/`.

---

## 1. `intent.tone` — governed by `vocab/tone.enum.json`

Add inside `properties.intent.properties` (alongside `rhetorical`, `teaches`, `bloom`):

```json
"tone": {
  "type": "string",
  "description": "Affective tone of the element/scene. Governed closed list — see vocab/tone.enum.json. Upstream signal read by the realizer/layout-engine selection. Owner: L&D / Instructional Design.",
  "enum": ["neutral", "pragmatic", "confident", "empathetic", "reflective", "urgent"]
}
```

## 2. `intent.pedagogical` — governed by `vocab/intent.enum.json > pedagogical`

`intent.enum.json` already declares the pedagogical dimension as *"Proposed as
element.intent.pedagogical"*, but the element schema doesn't carry the field yet. Add it inside
`properties.intent.properties` so the pedagogical axis is real (the enum body stays governed in
`intent.enum.json`; mirror its ids here, or keep this as a plain string validated by the linter to
avoid duplicating the list):

```json
"pedagogical": {
  "type": "string",
  "description": "The instructional job this element does. Governed by vocab/intent.enum.json > pedagogical. Validated by the linter against that file so the list isn't duplicated here."
}
```

## 3. `audience.complexity` — governed by `vocab/complexity.enum.json`

Add inside `properties.audience.properties` (alongside `segment_scope`, `difficulty`,
`variant_group`). Distinct from `difficulty` (continuous 0..1 per-learner target); this is the
authored design-time band:

```json
"complexity": {
  "type": "string",
  "description": "Authored content-complexity band (design-time). Governed closed list — see vocab/complexity.enum.json. Complements audience.difficulty, does not replace it. Owner: L&D Adaptivity.",
  "enum": ["low", "medium", "high"]
}
```

## 4. `expression.visual_type` — governed by `vocab/visual-type.enum.json`

Add inside `properties.expression.properties` (next to the existing advisory `layout_hint`):

```json
"visual_type": {
  "type": ["string", "null"],
  "description": "Advisory: the KIND of visual treatment the element wants (not a concrete asset). Governed closed list — see vocab/visual-type.enum.json. Pairs with visual-assets.registry content_type_hints; the resolved asset lives in render.asset_ref. Owner: Brand + Localization.",
  "enum": ["photo", "icon", "animation", "diagram", "quote", "data_graphic", null]
}
```

---

## Note on placement (the one spot worth a second look)

`tone` and `visual_type` are the two placements most open to relocation. Both are *upstream advisory
signals* (generator/normalizer sets them; the realizer reads them). They're modeled here on the
element so a single reconciled node carries them, but they could equally live on the **script
primitive** (`script.primitives.v1.json`), which already carries exactly this kind of upstream
signal via `pedagogical_intent`. If you'd rather the element stay leaner and push these to the
generation layer, move `tone`/`visual_type` onto the primitive and have the realizer copy the
resolved values down. Nothing else in the reconciliation changes.
