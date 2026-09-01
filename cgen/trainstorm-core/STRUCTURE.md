# Trainstorm Core — Repository Structure

*Tree and status reconciled against the repo 2026-08-30. The **one rule**, the naming conventions,
the sync split and the logo decision below are unchanged and still correct — they were right the
first time. What had gone stale was the tree, the ✅/⬜/⚠ markers, and First moves (the course-half
hops after 2026-08-26 were still written as if they had not landed).*

The cure for getting sideways: **don't decide file-by-file. Follow one rule and this tree.**

## The one rule

*"Where does X go?"* — decide by **what kind of thing it is**, not what it's about:

| If it's… | it goes in |
|---|---|
| a **data contract** you validate against | `schemas/` |
| a **closed list of allowed values** | `vocab/` |
| an **agent's instruction/prompt** (its governed behavior contract) | `agents/<agent>/` |
| **brand/visual assets, templates, locked terms, retrieval corpora** | `registry/` |
| a **translation** | `locales/` |
| a **governed graph of learning objectives / competencies** | `ontology/` |
| a **doc that explains or decides** | `architecture/` |
| a **worked example** | `reference/` |
| **code that transforms, checks, or runs an agent** | `tools/` |
| a **client's actual course** | **not here** → separate `trainstorm-courses/` repo |

An **agent is three kinds, not one** — so it lives in three places, never one feature folder: its **prompt** (a governed contract, like a schema) → `agents/<agent>/`; the **code** that runs it → `tools/<agent>/`; the **memory** it retrieves from (glossary, exemplar corpus) → `registry/`. That's why the localization agent's prompt is not in `tools/` next to its scripts — the prompt and the plumbing have different lifecycles, editors, and sync rules.

That single question answers ~95% of "where does this file go." Note it's *kind*, not *topic*: a Brunswick example course is a "worked example" (→ `reference/`), not a "Brunswick thing."

## The tree

Two siblings sit under `cgen/`. The split is deliberate: **`trainstorm-core/` is the machinery; `brands/` is client property.** Core can be shared, forked, or handed over without client IP riding along inside it.

```
cgen/
├── brands/                              # CLIENT property — not machinery. One folder per client.
│   ├── astellas/                        ✅ player chrome at `/cgen` (`meta.theme`; tokens · components · logo)
│   │   └── assets/                      ✅ identity marks (fonts/ to follow)
│   └── brunswick/assets/                 ✅ same convention for every client that follows
│
├── brunswick/                           # second client namespace (2026-08-31, paytrans drive) — same shape as astellas
│   ├── projects/paytrans/                ✅ 68 atoms + 70 occurrences — first EXPOSITORY corpus; employee course plays (5 scenes, 2 checks, intent_map; DECISIONS 2026-08-31 hop three)
│   └── registry/{roles,records,docs,options}.registry.json  ✅ seeded v1 at namespace creation; grown by propose→adopt
│
├── astellas/                            # ⚠ THIRD SIBLING — client atom stores + client registries
│   ├── projects/{ast_alsap,alsap,alsap_asp9999,ast_artwork}/  ✅ procedure · template · instance · artwork stores
│   │                                               (`ast_artwork` store **and** `?project=` loader on main, PR #42.
│   │                                               `/cgen/?project=ast_artwork` plays SOP-2290; `/cgen` stays ALSAP.)
│   └── registry/{roles,records,docs,options}.registry.json  ✅ client-tier governed ENTRIES
│
├── sl/                                  ✅ player two — Storyline chrome on the same realized_lesson.json (`/cgen` remains stock)
│
└── trainstorm-core/                     # the build system itself (the tree below)
```

**⚠ On `cgen/astellas/`:** this sibling post-dates the original tree and sits in tension with the one
rule's "a client's actual course → **not here**." The 2026-08-19 namespace decision chose it
deliberately, so the exception is real and should be stated rather than left implicit: **client
*courses* go to a separate `trainstorm-courses/` repo; client *document stores and governed
registries* live here**, because the harness resolves a project store and its client registry as
sibling anchors (`harness_paths.py`). Revisit if a client store ever needs to ship separately from
core.

**⚠ Vestiges under `cgen/` (accretion — not remaining core work):** `cgen/lumina`; the tabled
`/cgen/alsap` Netlify rewrite; zips (`layout-engine.zip`, `manifold_bundle_copilot_aug626.zip`,
`trainstorm-core.zip`, and other toolkit zips); `.lnk` / `desktop.ini`. `README-START-HERE.md` is a
2026-07-31 layout-engine drop note. `trainstorm-core/README.md` on main is locales README text
(misfiled). `cgen/schema/course.schema.json` is the Course Engine runtime shape, **not** a rival
constitution. Layout-engine potx/sidecars remain a parallel expression path, not the live `/cgen`
HTML player. `project/ast_alsap/review_matrix.csv` is already flagged in the tree below. Do not
treat these as First-moves work.

```
trainstorm-core/
├── README.md                             ⚠ locales README text, misfiled at the core root
├── README-START-HERE.md                  ⚠ 2026-07-31 layout-engine drop note
├── STRUCTURE.md                          ← this file  (STRUCTURE_dep*.md = deprecated, being removed)
│
├── schemas/                              # the data contracts — validate against these
│   ├── atom.schema.json                  ✅ CONTENT CANON — the meaning node; atom_id is the only content-node key (DECISIONS.md 2026-08-25)
│   ├── element.schema.json               ✅ one OCCURRENCE of an atom in a course — its own ele_ key, linked by composed_from; 1:many (DECISIONS.md 2026-08-25, occurrence identity)
│   ├── script.primitives.v1.json / .v2   ✅ generation IR (WHAT knowledge)
│   ├── procedure.facet.schema.json       ✅ source-type facet — procedures  (procedure.v0.1)
│   ├── form.facet.schema.json            ✅ source-type facet — forms       (form.v0.5, + evidence_kind/supplied_by)
│   ├── instance.facet.schema.json        ✅ authored overlay on a pinned template (instance.v0.1)
│   ├── objectives.schema.json            ✅ intent ontology — objective node contract  (v2: serves + bloom)
│   ├── goal.schema.json                  ✅ business-outcome node — reachability is a REQUIRED gate
│   ├── committed-design.schema.json      ✅ Case-Author stage-1 node (selection + framing, `cd_`); writer is `tools/headwater_case_author.py` (propose-only); mint does not exist (DECISIONS 2026-09-01)
│   ├── dossier.schema.json               ✅ Strategist open-project warrant snapshot (`doss_`); propose-only; human accept; does not write ontology/goals.json (DECISIONS 2026-09-01)
│   ├── socket.schema.json                ✅ the INTAKE CONTRACT — derived, never authored (socket.v0.1)
│   ├── template_manifest.schema.json     ✅
│   ├── visual-asset.schema.json          ✅ one visual asset registry entry
│   └── intent_sidecar.schema.json        ✅
│
├── vocab/                                # governed, closed vocabularies
│   ├── procedure.enum.json               ✅ meaning_kind · step_type
│   ├── form.enum.json                    ✅ meaning_kind · field_type · content_disposition   (form.v0.2)
│   ├── evidence.enum.json                ✅ evidence_kind · supplied_by — the socket's terms  (evidence.v0.2)
│   ├── instance.enum.json                ✅ meaning_kind · disposition_decision
│   ├── structure.enum.json               ✅ list · list_item (source-agnostic)
│   ├── check-shape.enum.json             ✅ invert_definition · sequence_order · closed_choice (DECISIONS 2026-08-27)
│   ├── scene.enum.json                   ✅ front_matter · procedure_a · form_br (DECISIONS 2026-08-27)
│   ├── intent.enum.json                  ✅ rhetorical + pedagogical intents  — ✅ pedagogical → element.intent.move
│   ├── primitives.registry.json          ⬜ text/motion/layout/interaction/style keys — partial
│   └── complexity · tone · visual-type    ✅
│
├── agents/                               # GOVERNED PROMPTS (contracts, not code) — these sync
│   ├── _shared/facet_owner_spine.md      ✅ spine v0.2 (optional {{WRITE_CONTRACT}} slot)
│   ├── headwater_ingest/                 ✅ meaning + object + source-type (the only agent that WRITES)
│   ├── alsap_builder/                    ✅ Amanuensis — proposes into `instance`; dispatched 2026-08-20
│   │   └── 07_examples/dispatch_2026-08-20/findings.md   ✅ first live dispatch record
│   ├── couturier/ · griot/ · chameleon/  ✅ Couturier v1 writes style; chameleon is a stub (authoring in-scope as contract, runtime/LRE do not build; no chameleon.py)
│   ├── strategist/                       ✅ operating prompt (`02_system_prompts/core_agent/strategist_system_prompt.md`) + contract (`warrant_STUB.md`); propose-only dossier; no strategist.py (DECISIONS 2026-09-01)
│   ├── localize/                         ✅ Dragoman — ⚠ flat `system.md` still un-`git rm`'d
│   ├── ingest-decompose/                 ⚠ predecessor of headwater_ingest; folder already absent — retire or merge still named
│   ├── cartographer/                     ✅ prompt + heuristic_v1.md; tools/cartographer.py writes occurrence intent
│   └── realizer/                         ✅ one_to_many · primitives · check_v1 · scenes_v1 · lesson_v1 · instance_example · form_field_present · spine_v1
│
├── registry/                             # backing store + retrieval memory (git-only, not synced)
│   ├── visual-assets.registry.json       ✅ 255 governed image assets — the MAP, not the bytes
│   ├── roles/records.registry.json       ⚠ 4 and 1 entries; client tier holds 14 and 5. Seed or drift — unlabelled
│   ├── templates/                        ⬜ HTML/CSS layout templates per layout_primitive
│   ├── glossary/ · corpus/               ✅ locked-term seed · 1,164-pair exemplar corpus (NEVER synced)
│   └── brands/                           ✅
│
├── layout-engine/                        # Storyline/.potx expression path — per-brand DATA + its CI gate (parallel to the /cgen HTML player)
│   ├── ci/validate_sidecar.py            ✅ repaired 2026-08-30 — auto-detects core (old default pointed at a non-existent ../../trainstorm-core); OK, 0 violations
│   ├── sidecars/ · templates/            ✅ astellas.awareness sidecar now governed: `Bullet` not `ListItem`; ungoverned `scenario` primitive rule removed
│   └── _schema/                          ✅ REMOVED 2026-08-30 — held two drifted copies of schemas that live in schemas/ (one home)
│
├── locales/                              ⬜ externalized translations keyed by atom_id — README only
├── ontology/objectives.json              ✅ obj_ nodes — 7 seeded (2 AST009 `status: example`; 5 ALSAP `draft`)
├── ontology/goals.json                   ✅ goal_ nodes — 2 seeded (1 AST009 `status: example`; 1 ALSAP `draft`); the WARRANT
│
├── architecture/                         # docs of record (the .md files sync to Project knowledge)
│   ├── DECISIONS.md                      ✅ append-only canon, one short block per settled call — if a chat disagrees, this file wins
│   ├── decision-log.md                   ✅ the narrative record behind DECISIONS.md (migrated from the Claude Project 2026-08-25); newest first
│   ├── sessions/                         ✅ dated notes, not canon
│   ├── lineage/                          ✅ proto-agent prompt lineage (2026-01 Brunswick prompts + mapping) — history, not canon
│   ├── manifold.md · conventions.md · atom-spec.md          ✅
│   ├── unification-map.md                ⚠ names element.schema.json as canon — SUPERSEDED, see DECISIONS.md 2026-08-25
│   ├── agents-roster.md · promptpack_manifold.md            ✅  (promptpack is a crosswalk from a parallel workstream — cite as such, not as canon)
│   ├── reconciliation.md · conversation-reconciliation.md   ✅
│   ├── script-generation-layer.md · localization-agent.md   ✅
│   └── diagrams/                         ✅ rendered HTML — git-only. `schema-graph.html` (2026-09-01) is the diagram of record for how the schemas join — hand-read edges, stamped with the commit read; live at `/cgen/schema-graph`
│
├── reference/                            # ONE clean, validated example of each layer
│   ├── example_atom.json                 ✅
│   ├── example_element.json              ✅ occurrence of example_atom (`composed_from`, no authored content)
│   ├── example_corpus_inventory.json     ✅ Case-Author stage-1 fixture listing (not a live client dump)
│   ├── example_committed_design.json     ✅ proposed design from that listing (`cd_`; not paytrans)
│   ├── example_dossier.json              ✅ proposed Strategist warrant snapshot (`doss_`; not a live engagement)
│   ├── sample_script.json / .v2.json     ✅
│   └── brunswick.reference.course.json   ✅ RATIFIED v1 structural (2026-08-31) — a pointer to the paytrans course, never a copy; v2 scope named (voice, Griot, arc, expression)
│
├── tools/                                # the agents' runtime code & utilities
│   ├── harness_paths.py                  ✅ 4 anchors: core · registry · project · template
│   ├── validate_atoms.py                 ✅ THE GATE — schema · drift · vocab · instance
│   ├── selftest_form_gate.py             ✅ 17/17     selftest_instance_gate.py  ✅ 17/17
│   ├── selftest_socket.py                ✅ 21/21     demand rules · PII · contract honesty
│   ├── headwater_ingest.py / _form.py    ✅ procedure · form ingests
│   ├── headwater_ingest_artwork.py       ✅ sibling Headwater ingest for `ast_artwork` (SOP-2290); ALSAP ingest untouched
│   ├── headwater_ingest_paytrans.py      ✅ sibling Headwater ingest for brunswick/paytrans — first expository corpus (2026-08-31)
│   ├── headwater_case_author.py          ✅ Case-Author stage 1 — proposes committed-design (status proposed); human-run committed_design_accept.py --by is the only promoter; mint does not exist
│   ├── validate_dossier.py               ✅ Strategist dossier gate — schema · warrant terminal · HITL · no atoms · no PII · no strategist.py
│   ├── dossier_accept.py                 ✅ ONLY writer of dossier `validated`; human-shaped `--by`; writes nothing on refuse; does not write ontology/goals.json
│   ├── project_sop_artwork.py            ✅ sibling SOP-2290 projector
│   ├── store_merge.py                    ✅ the idempotent merge rule — lives once, both ingests import it
│   ├── resolve_slot.py                   ✅ the walk: one slot → grounding packet (+ sufficiency)
│   ├── resolve_prompt.py                 ✅ spine + specialization + packet → dispatchable payload
│   ├── prompt_purity.py                  ✅ the no-content-in-prompt rule — shared by both above
│   ├── accept_value.py                   ✅ the ONLY writer into an instance store
│   ├── reconcile.py · approve.py · adopt_registries.py      ✅ round-trip · sign-off · promote-UP
│   ├── project_sop.py · project_alsap.py · project_review_table.py  ✅ projections
│   ├── project_socket.py                 ✅ template → INTAKE CONTRACT (json + client-facing html)
│   ├── lint.py                           ✅ repaired 2026-08-30 — classifies atom/element stores instead of linting them as scripts (was 254 false errors); element stores schema-checked; v2 scripts get the v2 schema
│   ├── validate_objectives.py            ✅ 45/45 — the warrant chain + worked examples
│   ├── localize/ · chat-capture/ · visual-assets/           ✅
│   ├── realize.py                        ✅ Realizer v1 — atoms → occurrences (1 ele_ per atom + small 1:many seed) + realized_lesson.html (spine) + extra lesson HTML from occurrences/lessons.json + scenes from occurrences/scenes.json + realized_lesson.json (`/cgen` via `?lesson=`) + realized_coverage.html
│   ├── cartographer.py                   ✅ Cartographer v1 — occurrence intent on existing ele_ records (preserves extra moves)
│   ├── couturier.py                      ✅ Couturier v1 — occurrence style keys on existing ele_ records (mints nothing)
│   └── render/                           ⬜ element → HTML → PNG — NOT this hop (no PNG pipeline)
│
└── project/                              # Claude Project setup — one-way snapshot FROM git, not a second constitution
    ├── custom_instructions.md            ✅ points at STRUCTURE.md + architecture/DECISIONS.md; atom is the node
    ├── knowledge_manifest.md             ✅ git is truth; knowledge is a one-way sync
    └── ast_alsap/review_matrix.csv       ⚠ stray store fragment — misfiled by the one rule above
```

`✅` = built and exercised. `⬜` = placeholder. `⚠` = present but wrong, stale, or misfiled.

## Naming conventions (so files sort and read predictably)

- **Schemas:** `*.schema.json`
- **Vocabularies:** `*.enum.json` (closed value lists) · `*.registry.json` (keyed lookups)
- **Locale packs:** `<bcp47>.json` — `en.json`, `ja.json`, `fr-CA.json`
- **Examples:** `example_*.json` · reference courses: `*.reference.course.json`
- **Stable ID prefixes** (never reused/edited): `atom_` **content node** (the only key meaning is stored under) · `ele_` **occurrence** of an atom in a course (minted at realization, linked to its atom by `composed_from`, never carries authored text) · `obj_` objective · `goal_` business outcome · `cd_` committed-design (Case-Author stage-1 selection + framing; not an atom) · `doss_` dossier (Strategist open-project warrant snapshot; not an atom, not a write into `ontology/goals.json`) · `term_` glossary term · `asset_` visual asset · `prim_`/`p###` script primitive · `sce_`/`sec_`/`mod_` structure. Two id spaces, two kinds of node: never mint `ele_` for content, never mint `atom_` for an occurrence (`architecture/DECISIONS.md`, 2026-08-25 occurrence identity; decision-log 2026-08-20 eighth). Never mint `atom_` for a committed-design or a dossier.
- **Asset ids** are minted from the file's content hash at first ingest (`asset_img_<hash12>`) and then **frozen**. Opaque is correct here — but on re-ingest, match against the registry rather than re-deriving, or a re-exported image mints a second identity for the same asset.
- **Two new governed closed lists** ship with the visual asset registry, both `v0.1` draft, both bumped by version not by silent extension: `role` (signature · motif · chrome) and `mark_class` (identity · sub_brand · program · third_party). `mark_class` is **required when `role: signature`**, enforced by a conditional in the schema — an unclassified signature is the exact ambiguity it exists to remove. Note it is deliberately *not* named `*_tier`: "tier" already means audience segment here (`tier1_field`, `tier2_msl`).

## What syncs to the Claude Project knowledge (vs. git-only)

Keep the knowledge base **lean**. Configure `.claudesync` (or your Drive mirror) to include only:

- **SYNC:** `schemas/`, `vocab/`, `ontology/*.json`, `agents/**/*.md` (the prompts — you refine these *in* the Project), `architecture/*.md` (not `diagrams/`), `reference/*.json`, `project/`
- **GIT-ONLY (don't sync):** `registry/` assets and **especially `registry/corpus/`** (fed to the retriever, never loaded into context — a 600 KB corpus in the knowledge base would wreck it), `locales/` packs, `architecture/diagrams/` (HTML), `tools/` code, and anything under a client courses repo.

The visual asset registry follows that split exactly, and it's the clearest illustration of why the rule is *kind*, not *topic*: `schemas/visual-asset.schema.json` **syncs** (it's a contract you reason about — 5 KB), while `registry/visual-assets.registry.json` **does not** (273 KB of keyed lookup data the compiler queries at runtime; the model never needs all 255 records in context). Same subject, opposite sides of the line.

Reason: the agent prompts are governed contracts you reason about, so they belong in context — but the corpus is *retrieval fuel*, not reading material. The retriever pulls 3 exemplars per string at runtime; the model never needs all 1,164 in its context. Fonts, HTML diagrams, and code likewise bloat retrieval without helping the model reason.

## Settled — where logos live (and why it wasn't one question)

The original tree planned `registry/brands/<brand>/` holding `tokens.css · fonts/ · logos/`. Resolving it took separating two things that had been fused:

**1. Bytes vs. map.** A folder is *where bytes live*; the registry is *the map*. They were never rivals — an identity mark sits in `brands/astellas/assets/` **and** has a registry entry with `asset_id`, `role`, `scope`, `content_hash`. Resolution always goes through the registry; the folder is just storage.

**2. Not all logos are the same kind of mark.** `role: signature` says "high-specificity mark" but not *whose authority it carries*. Ask for "the Astellas logo" and a program lockup was an equally valid answer. Hence **`mark_class`** — and only `identity` earns a place in `brands/`:

| `mark_class` | what it is | lives in |
|---|---|---|
| `identity` | the client's corporate mark — their brand team governs it, outlives every engagement | `cgen/brands/<client>/assets/` (git) |
| `sub_brand` | a company/division they own (Mercury, Simrad) — its own brand system, **not** interchangeable with the parent | library |
| `program` | an initiative mark (E2E, ALSAP, Achieve) — created for an engagement, retired with it | library |
| `third_party` | an external org's mark (PMDA, EMA) — neither ours nor the client's, own usage restrictions | library |

Where classification is uncertain, **under-claim**: default to `sub_brand`, never `identity`. A misfiled sub-brand is harmless; a program mark passing as the corporate identity is the failure this exists to prevent.

## Where the rest lives (deliberately NOT in core)

- **Bulk image/video/audio bytes** → **Dropbox**, at the `library` root declared in `visual-assets.registry.json` → `asset_roots` (currently `F:/Dropbox/3a-Brainstorm/_TRAINSTORM-local/__ASSETS/`). Deliberately not git: 400 MB and growing, and git keeps every version of every binary forever. That root is on a different volume from the repo, so it **must** be absolute — which makes it machine-specific, so `asset_resolve.py` prefers the **`TRAINSTORM_ASSET_ROOT`** env var and falls back to the registry value. Set the env var per machine; commit the registry once.
- **Identity marks** → `cgen/brands/<client>/assets/`, in git. Small (0.6 MB for all of them), rarely changed, build-critical, and genuinely part of the brand contract alongside tokens and fonts. Their `brand` root is **relative** to the registry and therefore portable with **no env var at all** — it travels with the clone. That portability is the direct payoff of keeping them in the repo rather than the bulk store.
- **Client courses** (Brunswick production, Astellas, future clients) → a **separate `trainstorm-courses/<client>/` repo** that references core schemas. Only *one clean copy of one course* lives here, in `reference/`, as the gold example.
- **Frontier** (Response Engine, Orchestrator) → their **own repos/projects** when active; they import these schemas but keep their own build context.

## `atom` and `element` — lexicon and utterance: one atom, many occurrences (decided 2026-08-20, re-affirmed 2026-08-25)

*Three readings of this relationship were produced on 2026-08-20 — three layers, one node, two
nodes — and the third was decided by Jake on instructional-design grounds
(`architecture/decision-log.md`, 2026-08-20 eighth). A 2026-08-25 PR re-derived the "one node" reading
from the July documents and was corrected the same day; see `architecture/DECISIONS.md`
(2026-08-25, occurrence identity).*

**The atom is the lexicon entry. The element is one utterance of it. `atom_id` keys meaning;
`element_id` keys the occurrence; `composed_from` links them. One atom → many elements.**

- **`atom.schema.json`** — CONTENT CANON. Thin: owns its meaning and `content_hash`, everything else
  keyed, single-writer per binding. `bindings.intent` is empty and closed (`teaches` +
  `intended_response` live on the occurrence). `architecture/atom-spec.md` is its annotated reading
  (July sketch; the schema is the contract). The live gate is `tools/validate_atoms.py`.
- **`element.schema.json`** — one *occurrence* of an atom in a course: this atom, at this position,
  shown this way. The same atom is a `hook` in module 1 and `reinforce` in module 5 — that is spaced
  repetition, and it is why an occurrence needs its own key. Occurrence-level facets (`rhetorical`,
  `move`, expression keys, `teaches`, `intended_response`) bind here. Not a rival canon — it never
  carries meaning of its own. `content`/`content.text` is not the source-meaning store (optional
  presentation-constraint copy only; default omit).

`architecture/reconciliation.md` §4's *"make `element_id` the stable `atom_id`"* is the one-node
reading and is **wrong** under 1:many; `promptpack_manifold.md` §8 (mint `element_id`s at
realization, joined by a derivation stamp) is **right** on that point, though it is a crosswalk from
a parallel workstream, not core canon.

The generation pipeline realizes atoms into occurrences; identity is minted at each transform:

```
source material → generator → SCRIPT PRIMITIVES → realizer → ELEMENTS (ele_, composed_from atom_) → render agents → RENDERED FORMS
```

**A translation is not a new node.** Source-locale meaning lives on the atom; translations live in
`locales/<bcp47>.json` keyed by `atom_id`. One node per language would make `locales/` redundant and
re-embed language — the drift this schema exists to fix.

### Element as a course-chain facet (hypothesis — does NOT survive 1:many as written)

*A facet on the atom is per-atom; an occurrence is per-placement. Under 1:many the element is a
different node kind, not a fourth source-type facet. What may survive is the observation below that
element's top-level fields are facets merely unnested — worth a field-by-field pass when `realize.py`
is built, but as the shape of the occurrence node, not as a binding on the atom.*

`element`'s own field descriptions call its parts **facets** — "Assessment facet", "Render-target
facet", `expression` carrying "Owner: Brand + Localization", and `ext` as "a sanctioned extension
point… so new facets can accrete." That is the `bindings` convention, written before `bindings`
existed. Which suggests `element` is the atom **specialized for the course chain**, exactly as
`form.facet` and `procedure.facet` specialize it for the document chain — not a layer above it.

Locale packs key on `atom_id` (meaning is translated once), with occurrence-level overrides keyed by
`element_id` only where presentation constrains the rendering — not built yet. Couturier owns style on
the occurrence's expression facet; Realizer (`tools/realize.py`) mints `ele_` ids and owns layout/render;
Couturier mints nothing. Couturier v1 (`tools/couturier.py`) writes style keys on
the occurrence's `expression` facet from a documented move→look map.

## First moves

*(The original four — unzip, fill placeholders, wire claudesync, paste custom instructions — are
done. Superseded 2026-08-20 by the state above.)*

The **document half** of the machine is built and green: Headwater authored ingest, `validate_atoms`,
form / instance / socket gates. Identity 1:many, the primitives hop, Procedure A as a job-aid +
sequence, form BR present, and the ASP-9999 instance example are already decided — do not
re-litigate. The **course half beyond Realizer / Cartographer / Couturier v1** has landed the
post-2026-08-26 hops below (cite `architecture/DECISIONS.md` dates). Dragoman and `tools/render/`
PNG pipelines are unbuilt. Authoring Chameleon stays a contract (assumed-audience facets); there is
no `chameleon.py`. The open-project warrant has an operating prompt
(`agents/strategist/02_system_prompts/core_agent/strategist_system_prompt.md`) and a
propose-only dossier store (`schemas/dossier.schema.json`); human-run
`tools/dossier_accept.py --by` is the only promoter. There is no `strategist.py`.
Case-Author stage 1 writer is `tools/headwater_case_author.py` (propose-only); there is
no stage-2 mint this hop. This hop does not mint atoms, lock `obj_`, or write
`ontology/goals.json`.

Near-term, in dependency order:

1. ~~**Settle identity**~~ — **done 2026-08-20, re-affirmed 2026-08-25.** Two ids: `atom_` for
   meaning, `ele_` for an occurrence, `composed_from` between them. See `architecture/DECISIONS.md`.
2. ~~**Land the PENDING restitch**~~ — **done 2026-08-25.** `atom.intent` empty and closed;
   `teaches` + `intended_response` on the occurrence. See `architecture/DECISIONS.md`.
3. ~~**`atom → primitives`**~~ — **done 2026-08-26.** Closed compiler form
   (`heading` / `body` / `step` / `callout` / `check`) on the occurrence;
   spine projector uses it. See `architecture/DECISIONS.md`.
4. ~~**`tools/realize.py`**~~ — **done 2026-08-25, v1.** One `ele_` per atom, `composed_from`, no
   authored text, `realized_lesson.html`. **1:many seed 2026-08-25** — two ALSAP atoms mint a
   second occurrence; extra `reinforce` projects as a check from the atom. **Lesson spine
   2026-08-25** — default HTML is a short path; `realized_coverage.html` is the dump.
   **2026-08-26** — that path includes Procedure A as a job sequence
   (present only; no extra `ele_` on A; no invented procedure-step MCQ),
   a sequence practice of those four presents (projector-only; object.order),
   then one worked example from two `alsap_asp9999` instance atoms
   (`composed_from` crosses stores; SOP `atoms.json` untouched).
   **`tools/render/`** (PNG) remains.
5. ~~**Cartographer v1**~~ — **done 2026-08-25.** Heuristic compiler writes `move`/`teaches` on the
   ALSAP occurrence store; re-runnable on extras (preserves stamped `move`).
6. ~~**Couturier v1**~~ — **done 2026-08-25.** Move→look map writes expression style keys; HTML
   clothes the 1:many pairs differently. Extra `reinforce` is a check, not a recap.
   **Lesson spine v1** — short path is the default HTML; dump is coverage.
   **2026-08-26** — Procedure A’s real steps as a job sequence on that path
   (no extra `ele_`; no invented procedure-step MCQ). **Same day — atom →
   primitives:** those steps project as a job-aid, not four SOP cards.
   **Same day — sequence practice:** order those four first sentences
   (projector-only; `object.order`). Couturier `style_ref` stays pedagogical
   roles; brand tokens are player chrome (landed hop below).

   Landed after 2026-08-26 (same course half; not new product):

   - ~~**Check shapes on the graph**~~ — **done 2026-08-27.** Closed vocab
     `invert_definition` / `sequence_order` / `closed_choice`
     (`vocab/check-shape.enum.json`). See `architecture/DECISIONS.md`.
   - ~~**Scenes catalog + one-scene pager**~~ — **done 2026-08-26 pager /
     2026-08-27 catalog.** `occurrences/scenes.json` is source of truth;
     projector pages one scene at a time. See `architecture/DECISIONS.md`.
   - ~~**Lesson as a graph object + lessons catalog**~~ — **done 2026-08-27.**
     `occurrences/lessons.json` (ALSAP short / br / plan). See
     `architecture/DECISIONS.md`.
   - ~~**`/cgen` Course Engine**~~ — **done 2026-08-27 player / 2026-08-30
     `?lesson=` / `?project=`.** Reads `realized_lesson.json` via catalog
     `?lesson=` inside the catalog selected by `?project=` (default ALSAP).
     `ast_artwork` store **and** `?project=` loader are on main (PR #42).
     Live `/cgen/?project=ast_artwork` plays SOP-2290; `/cgen` stays ALSAP.
     See `architecture/DECISIONS.md`.
   - ~~**Astellas brand pack as player chrome**~~ — **done 2026-08-27.**
     `cgen/brands/` via `meta.theme`. Couturier `style_ref` stays
     pedagogical roles. See `architecture/DECISIONS.md`.
   - ~~**Learner-facing check copy + registry labels**~~ — **done
     2026-08-27.** Engine JSON wears labels; graph still holds ids. See
     `architecture/DECISIONS.md`.
   - ~~**Instance example fill shows registry labels**~~ — **done
     2026-08-28.** Same label projection as closed-choice. See
     `architecture/DECISIONS.md`.
   - ~~**ALSAP scene 1 in-scope org + governance-doc lists**~~ — **done
     2026-08-29.** Children already on the graph; catalog membership.
     See `architecture/DECISIONS.md`.
   - ~~**Hide unused CC/audio unless the lesson has voiceover**~~ —
     **done 2026-08-29.** See `architecture/DECISIONS.md`.
7. **A real `brunswick.reference.course.json`** — still `{"_todo": …}`, and the only thing that would
   prove the course half end to end.

**Specified, still open** (already named above or on the visual-asset track — not vestiges, not
parked walls): `tools/render/` PNG pipeline; Dragoman / `locales/` (README only); 
`vocab/primitives.registry.json` still partial; `registry/templates/` HTML/CSS per
`layout_primitive`; visual-asset track (logos to `cgen/brands/<client>/assets/`, empty `alt_text`,
`process_flow` layout gap); `ingest-decompose/` predecessor — retire or merge; ontology
goals/objectives that are still `status: example`.

**Parked / walled — not next hops:** runtime Chameleon / LRE / Responsive Engine serve-mode; Headwater
outcomes-mode; LLM distractor-writer; pretty `/cgen/{client}/{course}` URLs; `/cgen/alsap`
rewrite; slide-authoring frontend; ingest UI on the static Netlify site; ISO 14971; Procedure B
on ALSAP; Generator's divergent distractors; Designer as a live agent; Strategist as a
*compiler* (the operating prompt and dossier store exist; there is still no `strategist.py`;
Case-Author stage-1 propose is `tools/headwater_case_author.py`; mint does not exist; accepting
a dossier does not write `ontology/goals.json` — that is a named next hop). Authoring Chameleon
stays a contract.

`project/custom_instructions.md` now points at this file and `architecture/DECISIONS.md`.
`architecture/unification-map.md` still names `element.schema.json` as canon in July prose —
historical; the living rule is the occurrence-identity block in `architecture/DECISIONS.md`.

## Next on the visual-asset track

- **Move 4 files.** The registry declares identity marks at `cgen/brands/<client>/assets/`; `Logo_Astellas_primary`, `Logo_Astellas_LogoOnly`, `Logo_Brunswick_black`, `Logo_Brunswick_white_transback` need to physically land there. `asset_resolve.py --audit` will confirm.
- **`alt_text` is empty on 253 of 255 entries.** It's the prerequisite for matching images to meaning — until an asset has described content, the only semantic signal is `tags`, which are just filename tokens. This is the vision pass.
- **Undecided:** whether an asset binds to the **script primitive** (a `process_flow` wants a process diagram — the more content-pure layer) or to **`expression.content_type`** (which needs `vocab/primitives.registry.json` populated first). Possibly both, at different strengths. `content_type_hints` on each entry is the placeholder either way, and it's advisory — a ranking signal, never a hard filter.
- **Two regulatory marks** (`icon_health-authority_logo` 3 and 4) are approved as *selectable* but their issuing agency is still unidentified; their `provenance` says confirm-before-use.
- **Open, from the same principle that moved `brands/` out of core:** `registry/glossary/astellas-pv.candidates.csv` and `registry/corpus/astellas-pv.ja.jsonl` are also client-specific. Consistency says they follow — but they're the localization agent's retrieval memory, so moving them means giving that agent a path config the way the asset registry now has one. Same pattern, more work.
