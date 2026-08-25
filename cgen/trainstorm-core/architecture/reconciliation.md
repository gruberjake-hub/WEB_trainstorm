# Trainstorm Schema Reconciliation

### Mapping `course` / `scene` / `course-primitives` onto the atom manifold

**Inputs:** `course.schema.json`, `scene.schema.json`, `course-primitives.schema.json` (trainstorm.ai).
**Goal:** figure out how these relate to each other and to the atom model — and stop the version sprawl.
**Date:** 20 July 2026

> **Settled 2026-08-25** (`architecture/DECISIONS.md`): `atom_id` is the only node key. Locale packs and expression keys bind to `atom_id`. Historical `element_id` / `ele_…` in this July sketch **are that same key in a course costume**, not a second ID space. Do not mint `ele_` IDs; do not mint `element_id` at realization. If this file and a chat disagree with `DECISIONS.md`, `DECISIONS.md` wins.

---

## TL;DR

1. **These are not three versions to choose between — they're three *views* of one substrate.** `course` is the *authoring* view (nested), `scene` is the *render* view (flat, After-Effects-bound), `course-primitives` is closest to the *data substrate* itself (flat, ID-keyed, localized). The manifold's "one substrate, many charts" resolves them: keep **one canonical store**, generate the other two as projections.
2. **My read on recency:** `course-primitives` is the newest and most evolved — it's the only one on JSON Schema **draft 2020-12** (the others are draft-07), it's flat and data-native, and it explicitly frames itself as the spreadsheet↔JSON bridge. Treat it as the convergence point. *(Confirm against file timestamps — but conceptually it's the furthest along.)*
3. **The one critical fix:** `course-primitives` embeds every translation inline (`content: localizedText` with en/fr/de/es…). That is the exact drift-generator you lived through on AST009. Externalize it — keep the source string on the node, move other locales to packs keyed by `atom_id` (this file's July `element_id` is that same key; see `DECISIONS.md` 2026-08-25).
4. **What's missing in all three:** the **audience/adaptivity** axis, a **pedagogical-objective** sense of intent, and **per-element provenance**. Those are the manifold pieces to add.

---

## 1. What each schema actually is

**`course.schema.json`** — *the authoring view (nested, oldest).* A `module → scenes → elements → (list → bullets)` tree of strongly-typed elements. Its distinctive move: **type and intent are fused** — every `Head` is `orient`, every `Statement` is `assert`, every `Impact` is `persuade`, etc. Rigid, but it encodes a real editorial discipline (each structural type has a canonical rhetorical job). Draft-07.

**`scene.schema.json`** — *the render view (flat scene, motion-oriented).* A single `scene` with an element **map** (`Head_01`, `Bullet_02`…). Its distinctive moves: (a) a rich **rhetorical `intent` enum** (orient/refine/organize/structure/specify/assert/explain/persuade/contextualize/transition/support); (b) **primitive references** — `text_primitive`, `motion_primitive`, `layout_primitive`, `interaction_primitive`, `style_ref` — i.e. keys into primitive libraries; (c) **narration** and a **render target** (`ae_comp` = After Effects, `template`, `output_file`, `review_required`). This is the most sophisticated *expression* model of the three. Draft-07.

**`course-primitives.schema.json`** — *the data substrate (flat, localized, newest).* A flat array of `courseElement`s, each with `element_id` + `row_id`/`section_id`/`slide_id`, a `primitive_type` taxonomy (course/scene/scenario/knowledge_check/assessment/job_aid/…), `content_role`, `layout_hint`, embedded `localizedText` content, a `render` block, and a `relationships` block (parent/group/sequence + `feedback_for`/`correct_option` for assessment). Draft 2020-12. **This is the one that maps almost 1:1 to an atom.**

---

## 2. The reframe: three views of one substrate

```
                 ┌───────────────────────────┐
   authoring →   │   course.schema (nested)  │   ← type→intent discipline
                 └───────────────────────────┘
                              ▲  projection
   SUBSTRATE →   ┌───────────────────────────┐
   (canonical)   │ course-primitives (flat)  │   ← the atom store
                 └───────────────────────────┘
                              ▼  projection
   render →      ┌───────────────────────────┐
                 │   scene.schema (AE-bound)  │   ← primitives + motion + narration
                 └───────────────────────────┘
```

You maintain **one** schema (the flat substrate). The nested authoring shape and the scene/render shape are **generated views** — the same atoms, projected. That is the manifold's core claim applied to your own toolchain: stop hand-maintaining three canonical schemas that drift out of sync; maintain the substrate, derive the rest.

---

## 3. Crosswalk — your fields ↔ the atom facets

| Atom facet | `course-primitives` (substrate) | `scene` (render) | `course` (authoring) |
|---|---|---|---|
| **identity** | `element_id` (+ row_id/section_id/slide_id) | `scene_id` + element key (`Head_01`) | `scene_id`, element `id` (optional) |
| **meaning (source)** | `content.en` — *but embeds all locales* | `text` (+ `voice_text`) | `text` |
| **object · structure** | `relationships.parent_id/group_id/sequence_index` | `parent_id`; ordered element map | nested composition (module→…→bullet) |
| **intent · rhetorical** | `content_role`, `primitive_type` | `intent` enum ✓ (richest) | `intent` const per type ✓ (fused) |
| **intent · pedagogical (objective)** | — | — | — |
| **expression · registry keys** | `layout_hint`, `render.layout_variant` | `text/motion/layout/interaction_primitive`, `style_ref` ✓ (richest) | inline `style`, `animation` |
| **expression · assets/render** | `render.animation_tag/asset_ref/voiceover_ref` | `narration`, `assets`, `render.ae_comp/template/output_file` ✓ | inline `animation` |
| **audience / adaptivity** | — | — | — |
| **assessment** | `relationships.feedback_for/correct_option`; `primitive_type` | `interaction_primitive` (hint) | — |
| **governance / provenance** | course-level `version`, `source`, `notes` | `render.review_required`, `notes` | — |

Two things pop out of the table: `scene` owns the best **expression** model (primitive refs + motion + narration + render target); `course-primitives` owns the best **substrate** shape (flat, ID-keyed, relationships, assessment). Neither has audience, pedagogical objectives, or per-element provenance.

---

## 4. Keep-list — the good ideas already in your schemas

- **`course-primitives`' flat, ID-keyed element array** → this *is* the atom store. Make `element_id` the stable `atom_id`. **Frozen 2026-08-25:** that is one key, not two. Do not mint `ele_` as a parallel space.
- **`scene`'s primitive references** (`text/motion/layout/interaction_primitive`, `style_ref`) → this is the **expression binding done right**: keys into registries, not embedded styles. Pull these onto the canonical element. (`course-primitives` only has a weak `layout_hint` — upgrade it with these.)
- **`scene`'s rhetorical `intent` enum** → keep it, as the *rhetorical* sub-facet of intent.
- **`course`'s type→intent mapping** → keep it, but as a **validation/default rule** applied when projecting the authoring view, not as baked structure. (i.e. "a Head defaults to orient" is a lint rule, not a schema constraint that forbids reuse.)
- **`course-primitives`' `relationships` + assessment fields** (`feedback_for`, `correct_option`) → this is your **assessment facet** in embryo; formalize it as its own facet.
- **`scene`'s narration + render target** → the render agent's inputs; keep, downstream of expression.

---

## 5. Add-list — what the manifold supplies that all three lack

1. **Externalize localization (the critical one).** `content: localizedText` embeds en/fr/de/es inline — the AST009 drift-generator. Fix: keep `content` in the source locale as the node's **meaning**; move every other locale to **locale packs keyed by `atom_id`**, each with `status` / `reviewer` / `source_hash`. (This is exactly the atom spec's §4. It's also what lets your localization agent — proven on AST009 — plug straight in.)
2. **A pedagogical intent, distinct from rhetorical intent.** Your `intent` enum is *rhetorical* (what the element does on the page: orient/assert/persuade). The manifold's intent is *pedagogical* (`teaches: [objective_id]`). Keep both as two sub-fields — they answer different questions and should not be conflated.
3. **The audience/adaptivity binding.** None of the three model *who it's for*. Add `segment_scope` / `difficulty` / `variant_group` so the substrate can feed a responsive engine, not just static generation.
4. **Per-element provenance.** Governance is course-level today (`version`, `source`). Add per-element `version` / `status` / `source_hash` / `owner`. **This is the direct cure for your "which version is this, too much generated" problem** — provenance travels with each element, so staleness and drift are detectable instead of guessed.

---

## 6. The convergence target (sketch)

One reconciled element — your `course-primitives` shape, keeping `scene`'s expression ideas, aligned to the atom. Field names kept close to yours:

```jsonc
{
  "element_id": "atom_ast009_recognize_psi", // = atom_id (stable, the only join key; do not mint ele_)
  "source_hash": "sha256:…",                     // guards meaning across regeneration

  "content": { "locale": "en",                   // meaning: SOURCE only — not all locales
               "text": "Recognize product safety information" },

  "structure": {                                 // object facet
    "section_id": "sec_1", "slide_id": "sld_1_3",
    "parent_id": "atom_ast009_slide_1_3", "sequence_index": 4 },

  "intent": {                                    // TWO senses, separated
    "rhetorical": "assert",                       // your scene enum
    "teaches": ["obj_recognize_psi"] },           // the pedagogical add

  "expression": {                                // scene's primitive refs = registry keys
    "primitive_type": "statement",
    "text_primitive": "tp_statement",
    "motion_primitive": "mp_fade_in",
    "layout_primitive": "lp_centered",
    "interaction_primitive": null,
    "style_ref": "brand.instructional" },

  "audience": {                                  // the manifold add — fit hooks, no PII
    "segment_scope": ["tier1_field"], "difficulty": 0.3, "variant_group": "vg_recognize_psi" },

  "assessment": { "feedback_for": null, "correct_option": null },

  "render": { "animation_tag": "fade_in", "asset_ref": null, "voiceover_ref": null,
              "ae_comp": null, "review_required": true },

  "governance": { "version": 3, "status": "approved", "owner": "authoring", "regulatory_binding": "none" }
}
```
Translations for this node live in `locales/<lang>.json[atom_id]`; the visual/motion/interaction primitives live in their registries; objectives live in the intent ontology. The node stays thin.

---

## 7. On the filesystem chaos (this is the recursive part)

You said it yourself: too much generated, unsure which is current. That is **not a discipline failure — it's the exact problem your product exists to solve, showing up in your own toolchain.** Three schemas with no single canonical source, no provenance, and content (structure) fused with expression (render targets) across files → drift → "which one is real?" It's the AST009 story and the C-drive story a third time.

The cure is the one you've been designing all week:
- **Designate one canonical schema** (the flat substrate) and put it under version control (git). The nested and scene shapes become *generated*, never hand-edited.
- **Stamp provenance** — every schema and every generated artifact carries version + source_hash. "Most recent" stops being a question because there's one source of truth and a hash to prove currency.
- **Reference, don't embed** — the same rule that fixes localization fixes the schema sprawl: one substrate, many derived views.

You don't have a versioning problem. You have three copies of a truth that should be one. Same fix, all the way down.

---

## 8. Next

If this reconciliation lands, the natural next artifact is the **unified `element.schema.json`** — a single formal, validatable schema (draft 2020-12) that merges the three, with the four fixes baked in — plus a short **migration note** showing how each of your existing three maps into it (so nothing you built is lost, just consolidated). That file exists. **Identity (2026-08-25):** it is a course costume of the atom, not a second key — `architecture/DECISIONS.md`.
