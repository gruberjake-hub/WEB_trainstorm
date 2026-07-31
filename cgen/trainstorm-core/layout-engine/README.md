# CGEN layout engine — templates, manifests, sidecars

This is the layout/brand-binding layer of the course generator. It separates three
concerns that change for different reasons and by different hands:

- **Structure** — the layout archetypes (title+body, reveal grid, scenario sort, venn,
  KC…). Authored as a `.potx` in PowerPoint.
- **Skin** — brand theme (palette, fonts, logo). Lives natively in the same `.potx`.
- **Policy** — which layout serves which learning/interaction intent, how storyboard
  fields fill slots, overflow rules, optional re-skin. Lives in text **sidecars**.

## Folder structure

```
CGEN-course-builder/
├── templates/                         # brand shells — BINARY, git-LFS or artifact store
│   └── astellas/
│       ├── astellas_v1.potx           # you author/tune this in PowerPoint
│       └── template_manifest.json     # GENERATED from the .potx (see "backward flow")
├── sidecars/                          # intent policy — TEXT, normal git, diff/PR/CI
│   ├── astellas.awareness.sidecar.json
│   └── astellas.compliance.sidecar.json   # many sidecars, one .potx
├── _schema/
│   ├── template_manifest.schema.json  # contract for the generated manifest
│   └── intent_sidecar.schema.json     # contract for the hand-authored sidecar
└── ci/
    └── validate_sidecar.py            # PR gate: sidecar honors the manifest
```

Rule of thumb for git: **text in normal git, the `.potx` as a pinned artifact.** The
manifest and sidecars diff cleanly and review as PRs; the binary `.potx` goes to LFS or
a release/object store and is referenced by sha256, never diffed.

## The two files

**Template manifest** (`templates/<brand>/template_manifest.json`) — *generated*, not
hand-edited. Pure structure + skin extracted from the `.potx`: theme colors/fonts,
canvas size, and per-layout slot geometry with Storyline binding metadata. Conforms to
`_schema/template_manifest.schema.json`.

**Intent sidecar** (`sidecars/<brand>.<flavor>.sidecar.json`) — *hand-authored* policy.
Ordered `selection` rules mapping your Script_Normalizer enums (`potential_interaction`,
`suggested_visual_type`, `complexity_level`, `key_concepts_count`, free `flags`) to a
layout id; per-layout `bindings` mapping storyboard fields into slots with `repeat` and
`overflow`; optional `token_overrides` to re-skin; `interaction_defaults`. Conforms to
`_schema/intent_sidecar.schema.json`. Pins to a manifest by `sha256`.

Because policy lives here, one `.potx` supports many expressions: swap the sidecar to
change *selection + skin*; swap the `.potx` to change the *visual vocabulary*.

## Backward flow — tune in PowerPoint, generate the JSON

This is the workflow you asked for. You never hand-write the manifest:

1. **Author/tune `astellas_v1.potx`** in PowerPoint. Honor the authoring contract so
   extraction is clean:
   - use real **placeholders**, not free-floating text boxes;
   - use **theme colors**, not pasted hex;
   - **name shapes** — especially interaction controls (`btn_continue`, `opt`, `choice`)
     so their Storyline binding metadata comes across;
   - name layouts by convention (`AST_RevealGrid`, `AST_KCSingle`) so the extractor can
     derive stable layout ids.
2. **Run the extractor** (next build) → it emits `template_manifest.json` (theme + slot
   geometry + control metadata) AND a **scaffolded sidecar** — the layouts pre-listed
   with empty `selection`/`bindings` for you to fill. The one thing the `.potx` can't
   carry is intent, so that scaffold is where you tag it.
3. **Author the sidecar policy** (or edit the scaffold) — the selection rules and
   bindings. This is the only hand-authored step.
4. **CI gate** — `ci/validate_sidecar.py` checks the sidecar against the manifest on
   every PR: schema-valid, sha256 pin matches, and every referenced layout/slot exists.

## Validate locally

```bash
python ci/validate_sidecar.py sidecars/astellas.awareness.sidecar.json
```
