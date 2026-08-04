# CGEN layout engine — templates, manifests, sidecars (Manifold-conformant)

This is the layout/brand-binding layer of the course generator — the **Storyline-branch
expression + render backend of the Manifold**. It separates three concerns that change for
different reasons and by different hands:

- **Structure** — the layout archetypes (title+body, reveal grid, scenario sort, venn, KC…).
  Authored as a `.potx` in PowerPoint. Each layout id **is** a registered `layout_primitive`
  key in `trainstorm-core/vocab/primitives.registry.json`.
- **Skin** — brand theme (palette, fonts, logo). Lives natively in the same `.potx`; the
  layout-engine's `token_overrides` are the `expression.style_ref` override channel.
- **Policy** — which layout serves which learning/interaction intent, how the scene's
  **elements** fill slots, overflow rules, optional re-skin. Lives in text **sidecars**.

## Manifold conformance (2026-07-31)

This folder was reconciled to make the Manifold the single source of truth. Three things changed:

1. **Selection is governed.** Sidecar `selection` rules fire on the Manifold's governed
   vocabularies (`script.primitives`, `intent.enum` rhetorical/pedagogical, `tone.enum`,
   `complexity.enum`, `visual-type.enum`, and `primitives.registry` interaction keys) — not the
   old ungoverned Script_Normalizer enums. `ci/validate_sidecar.py` rejects any value not in its
   governed list.
2. **Bindings carry the `element_id` join.** Bindings no longer interpolate free storyboard
   strings (`{screen_title}`). They **select scene elements by facet**, so every filled slot
   resolves to an `element_id` and the render record is keyed by it — which is what lets a rendered
   Storyline screen live in the render store and go stale via `source_hash` like everything else.
3. **Layouts are registered.** The six layouts (and their controls) are the first real entries in
   `primitives.registry.json`. A sidecar may only `use` a registered `layout_primitive`.

New governed vocab promoted from the retired Script_Normalizer axes lives in `trainstorm-core/vocab/`:
`tone.enum.json`, `complexity.enum.json`, `visual-type.enum.json`. Element-schema attachment points
are in `trainstorm-core/schemas/PATCH-element.schema.md`.

## Folder structure

```
trainstorm-core/                       # canonical Manifold (drop these into your repo)
├── vocab/
│   ├── primitives.registry.json       # UPDATED — 6 layout_primitive + 3 interaction_primitive keys
│   ├── tone.enum.json                 # NEW governed vocab
│   ├── complexity.enum.json           # NEW governed vocab
│   └── visual-type.enum.json          # NEW governed vocab
├── schemas/
│   ├── template_manifest.schema.json  # ADOPTED here (was layout-engine/_schema/) — canonical
│   ├── intent_sidecar.schema.json     # ADOPTED here — canonical
│   └── PATCH-element.schema.md         # additive patch (apply to element.schema.json)
└── architecture/PATCH-realization-table.md

layout-engine/                         # per-brand DATA + the CI gate (not canonical schemas)
├── templates/astellas/
│   ├── astellas_v1.potx               # you author/tune this in PowerPoint (BINARY, git-LFS)
│   └── template_manifest.example.json # GENERATED from the .potx (interaction_primitive per layout)
├── sidecars/
│   └── astellas.awareness.sidecar.json   # governed selection + element-selector bindings
└── ci/
    └── validate_sidecar.py            # PR gate: manifest contract + Manifold governance
```

The two schemas now live under `trainstorm-core/schemas/` alongside `element.schema.json` — one
repo, one source of truth (decision 2026-07-31). Manifests and sidecars stay in `layout-engine/`
because they are per-brand data, not canonical contracts.

## The two files

**Template manifest** — *generated*, not hand-edited. Pure structure + skin extracted from the
`.potx`. Conforms to `_schema/template_manifest.schema.json`. Each `layout.id` is the
`layout_primitive` key; `layout.interaction_primitive` names the interaction it provides (or null).

**Intent sidecar** — *hand-authored* policy. Ordered `selection` rules over governed intent signals
→ a registered layout id; per-layout `bindings` mapping the scene's elements into slots via
selectors (`{ "scope": "child", "where": { "rhetorical": ["orient"] } }`) with `repeat` + `overflow`;
optional `token_overrides`; `interaction_defaults`. Pins to a manifest by `sha256`.

## Validate locally

```bash
# schemas + vocab both read from your trainstorm-core checkout
# (defaults: --schema-dir ../../trainstorm-core/schemas, --core-dir ../../trainstorm-core)
python ci/validate_sidecar.py sidecars/astellas.awareness.sidecar.json \
  --schema-dir ../trainstorm-core/schemas --core-dir ../trainstorm-core
```

The gate checks: schema validity, sha256 pin, layout/slot existence, **governed selection values**,
**layout_primitive registration**, and **element-selector bindings** (no legacy free-field
templates). Non-empty `flags` warn but don't fail — promote recurring flags into a governed vocab.

## Backward flow — tune in PowerPoint, generate the JSON (unchanged)

1. Author/tune `astellas_v1.potx` under the authoring contract (real placeholders; theme colors;
   named control shapes `btn_continue`/`opt`/`choice`; layout names `AST_RevealGrid`…).
2. Run the extractor → emits `template_manifest.json` + a scaffolded sidecar (layouts pre-listed,
   empty governed `selection`/`bindings`). The one thing the `.potx` can't carry is intent — the
   scaffold drops you at that one hand-authored step.
3. Author the sidecar policy (governed selection + element-selector bindings).
4. CI gate — `ci/validate_sidecar.py` on every PR.
