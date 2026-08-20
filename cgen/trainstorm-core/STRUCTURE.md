# Trainstorm Core — Repository Structure

*Tree and status reconciled against the repo 2026-08-20. The **one rule**, the naming conventions,
the sync split and the logo decision below are unchanged and still correct — they were right the
first time. What had gone stale was the tree, the ✅/⬜ markers, and the layering (see "The three
layers" below, which is new).*

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
│   ├── astellas/assets/                  ✅ identity marks only (tokens.css · fonts/ to follow)
│   └── brunswick/assets/                 ✅ same convention for every client that follows
│
├── astellas/                            # ⚠ THIRD SIBLING — client atom stores + client registries
│   ├── projects/{ast_alsap,alsap,alsap_asp9999}/   ✅ procedure · template · instance stores
│   └── registry/{roles,records,docs,options}.registry.json  ✅ client-tier governed ENTRIES
│
└── trainstorm-core/                     # the build system itself (the tree below)
```

**⚠ On `cgen/astellas/`:** this sibling post-dates the original tree and sits in tension with the one
rule's "a client's actual course → **not here**." The 2026-08-19 namespace decision chose it
deliberately, so the exception is real and should be stated rather than left implicit: **client
*courses* go to a separate `trainstorm-courses/` repo; client *document stores and governed
registries* live here**, because the harness resolves a project store and its client registry as
sibling anchors (`harness_paths.py`). Revisit if a client store ever needs to ship separately from
core. Everything else under `cgen/` (zips, toolkits, loose HTML) is pre-manifold accretion and is not
part of this structure.

```
trainstorm-core/
├── README.md · README-START-HERE.md
├── STRUCTURE.md                          ← this file  (STRUCTURE_dep*.md = deprecated, being removed)
├── decision-log.md                       ⚠ stale duplicate of claude/decision-log.md — delete or export one-way
│
├── schemas/                              # the data contracts — validate against these
│   ├── atom.schema.json                  ✅ conceptual node — CONTENT CANON (see "The three layers")
│   ├── element.schema.json               ✅ production contract, COURSE chain — same node as atom, ⬜ id question open
│   ├── script.primitives.v1.json / .v2   ✅ generation IR (WHAT knowledge)
│   ├── procedure.facet.schema.json       ✅ source-type facet — procedures  (procedure.v0.1)
│   ├── form.facet.schema.json            ✅ source-type facet — forms       (form.v0.3, named slots + markers)
│   ├── instance.facet.schema.json        ✅ authored overlay on a pinned template (instance.v0.1)
│   ├── objectives.schema.json            ✅ intent ontology — objective node contract
│   ├── template_manifest.schema.json     ✅
│   ├── visual-asset.schema.json          ✅ one visual asset registry entry
│   └── intent_sidecar.schema.json        ✅
│
├── vocab/                                # governed, closed vocabularies
│   ├── procedure.enum.json               ✅ meaning_kind · step_type
│   ├── form.enum.json                    ✅ meaning_kind · field_type · content_disposition   (form.v0.2)
│   ├── instance.enum.json                ✅ meaning_kind · disposition_decision
│   ├── structure.enum.json               ✅ list · list_item (source-agnostic)
│   ├── intent.enum.json                  ✅ rhetorical + pedagogical intents  — ⬜ unexercised
│   ├── primitives.registry.json          ⬜ text/motion/layout/interaction/style keys — partial
│   └── complexity · tone · visual-type    ✅
│
├── agents/                               # GOVERNED PROMPTS (contracts, not code) — these sync
│   ├── _shared/facet_owner_spine.md      ✅ spine v0.2 (optional {{WRITE_CONTRACT}} slot)
│   ├── headwater_ingest/                 ✅ meaning + object + source-type (the only agent that WRITES)
│   ├── alsap_builder/                    ✅ Amanuensis — proposes into `instance`; dispatched 2026-08-20
│   │   └── 07_examples/dispatch_2026-08-20/findings.md   ✅ first live dispatch record
│   ├── couturier/ · griot/ · chameleon/  ✅ prompts exist — ⬜ none has ever written a binding
│   ├── localize/                         ✅ Dragoman — ⚠ flat `system.md` still un-`git rm`'d
│   ├── ingest-decompose/                 ⚠ predecessor of headwater_ingest; retire or merge
│   └── cartographer/                     ⬜ DOES NOT EXIST despite the 08-12 entry listing it as built
│
├── registry/                             # backing store + retrieval memory (git-only, not synced)
│   ├── visual-assets.registry.json       ✅ 255 governed image assets — the MAP, not the bytes
│   ├── roles/records.registry.json       ⚠ 4 and 1 entries; client tier holds 14 and 5. Seed or drift — unlabelled
│   ├── templates/                        ⬜ HTML/CSS layout templates per layout_primitive
│   ├── glossary/ · corpus/               ✅ locked-term seed · 1,164-pair exemplar corpus (NEVER synced)
│   └── brands/                           ✅
│
├── locales/                              ⬜ externalized translations keyed by element_id — README only
├── ontology/objectives.json              ✅ obj_ nodes — 2 seeded, `status: example`
│
├── architecture/                         # docs of record (the .md files sync to Project knowledge)
│   ├── manifold.md · conventions.md · atom-spec.md          ✅
│   ├── unification-map.md                ⚠ names element.schema.json as canon — SUPERSEDED, see log 08-20 (sixth)
│   ├── agents-roster.md · promptpack_manifold.md            ✅
│   ├── reconciliation.md · conversation-reconciliation.md   ✅
│   ├── script-generation-layer.md · localization-agent.md   ✅
│   └── diagrams/                         ✅ rendered HTML — git-only
│
├── reference/                            # ONE clean, validated example of each layer
│   ├── example_atom.json                 ✅
│   ├── example_element.json              ⚠ duplicates the atom's text with no link — see log 08-20 (sixth)
│   ├── sample_script.json / .v2.json     ✅
│   └── brunswick.reference.course.json   ⬜ `{"_todo": …}` — the gold course has NEVER existed
│
├── tools/                                # the agents' runtime code & utilities
│   ├── harness_paths.py                  ✅ 4 anchors: core · registry · project · template
│   ├── validate_atoms.py                 ✅ THE GATE — schema · drift · vocab · instance
│   ├── selftest_form_gate.py             ✅ 17/17     selftest_instance_gate.py  ✅ 17/17
│   ├── headwater_ingest.py / _form.py    ✅ procedure · form ingests
│   ├── store_merge.py                    ✅ the idempotent merge rule — lives once, both ingests import it
│   ├── resolve_slot.py                   ✅ the walk: one slot → grounding packet (+ sufficiency)
│   ├── resolve_prompt.py                 ✅ spine + specialization + packet → dispatchable payload
│   ├── prompt_purity.py                  ✅ the no-content-in-prompt rule — shared by both above
│   ├── accept_value.py                   ✅ the ONLY writer into an instance store
│   ├── reconcile.py · approve.py · adopt_registries.py      ✅ round-trip · sign-off · promote-UP
│   ├── project_sop.py · project_alsap.py · project_review_table.py  ✅ projections
│   ├── lint.py · validate_objectives.py  ✅
│   ├── localize/ · chat-capture/ · visual-assets/           ✅
│   ├── realize.py                        ⬜ primitives → elements — ABSENT
│   └── render/                           ⬜ element → HTML → PNG — directory exists, EMPTY
│
└── project/                              # Claude Project setup
    ├── custom_instructions.md            ⚠ still names element as the canonical unit — correct it
    ├── knowledge_manifest.md             ✅
    └── ast_alsap/review_matrix.csv       ⚠ stray store fragment — misfiled by the one rule above
```

`✅` = built and exercised. `⬜` = placeholder. `⚠` = present but wrong, stale, or misfiled.

## Naming conventions (so files sort and read predictably)

- **Schemas:** `*.schema.json`
- **Vocabularies:** `*.enum.json` (closed value lists) · `*.registry.json` (keyed lookups)
- **Locale packs:** `<bcp47>.json` — `en.json`, `ja.json`, `fr-CA.json`
- **Examples:** `example_*.json` · reference courses: `*.reference.course.json`
- **Stable ID prefixes** (never reused/edited): `ele_` element · `atom_` atom · `obj_` objective · `term_` glossary term · `asset_` visual asset · `prim_`/`p###` script primitive · `sce_`/`sec_`/`mod_` structure.
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

## `atom` and `element` — one node, not two layers (2026-08-20)

*An earlier version of this section, added the same day, described atom / primitives / element as
three layers awaiting a join. **That was wrong and is retracted** — see decision log 2026-08-20
(seventh), which quotes the July documents.*

**The atom is the design; the element is the contract. They are the same node.**

- **`atom.schema.json`** — the *conceptual* node. Thin: owns its meaning, everything else keyed,
  single-writer per binding. `architecture/atom-spec.md` is its annotated reading.
- **`element.schema.json`** — the *reconciled production* node that implements that model, unifying
  three legacy schemas (`course` authoring / `scene` render / `course-primitives` substrate).

`architecture/promptpack_manifold.md` §1 is explicit: they are *"not two temperatures of one node…
**You validate against the element. There is no runtime atom→element promotion.**"* And
`architecture/reconciliation.md` §4: *"`course-primitives`' flat, ID-keyed element array → **this is
the atom store.** Make `element_id` the stable `atom_id`."*

The generation pipeline contains **no atom layer** — the atom is what an element *is*:

```
source material → generator → SCRIPT PRIMITIVES → realizer → ELEMENTS → render agents → RENDERED FORMS
```

**A translation is not an element.** `element.content` is source-locale only; translations live in
`locales/<bcp47>.json` keyed by `element_id`. One element per language would make `locales/`
redundant and re-embed language in the node — the drift this schema exists to fix.

### Open — identity, and only identity

The relationship is settled; the **id** is not. Three sources disagree: `reconciliation.md` says
`element_id` **=** `atom_id`; this file's naming conventions list `ele_` and `atom_` as two separate
prefixes; `promptpack_manifold.md` §8 says `element_id`s are minted **at realization**, joined by a
`derivation` stamp. Settle this before building anything that depends on either id.

### Live hypothesis — element as a course-chain facet (PROPOSED, not decided)

`element`'s own field descriptions call its parts **facets** — "Assessment facet", "Render-target
facet", `expression` carrying "Owner: Brand + Localization", and `ext` as "a sanctioned extension
point… so new facets can accrete." That is the `bindings` convention, written before `bindings`
existed. Which suggests `element` is the atom **specialized for the course chain**, exactly as
`form.facet` and `procedure.facet` specialize it for the document chain — not a layer above it.

If that holds, the move is `element.facet.schema.json` as a fourth source-type facet, one `atom_id`,
and the gate already validates this shape three times over. It needs a field-by-field pass and the
identity question answered first.

## First moves

*(The original four — unzip, fill placeholders, wire claudesync, paste custom instructions — are
done. Superseded 2026-08-20 by the state above.)*

The **document half** of the machine is built and green: three atom stores, a gate with two
self-tests at 17/17, ingest · reconcile · approve · project, and an agent that has been dispatched
and behaves correctly. The **course half has never run** — no store carries an `intent`,
`expression`, `audience` or `render` binding; only Headwater has ever written a binding;
`realize.py` is absent and `render/` is empty.

Near-term, in dependency order:

1. **Settle identity** — `element_id` vs `atom_id`: one key, or two joined by a `derivation` stamp.
   Three docs disagree (see the section above). Everything below depends on it.
2. **Test the element-as-course-facet hypothesis** field by field against `element.schema.json`.
   If it holds, the reconciliation costs no new concepts.
3. **`atom → primitives`** — the first hop of the pipeline has no listed transform at all.
4. **`tools/realize.py`** (primitives → elements) and **`tools/render/`** (element → HTML → PNG).
5. **A real `brunswick.reference.course.json`** — still `{"_todo": …}`, and the only thing that would
   prove the course half end to end.

Correct as you go: `architecture/unification-map.md` and `project/custom_instructions.md` describe
`element.schema.json` as the canonical unit. Per the July reading that is *correct* for the course
chain — but it reads as a contradiction next to a harness that validates against `atom`, so both
should say which chain they mean.

## Next on the visual-asset track

- **Move 4 files.** The registry declares identity marks at `cgen/brands/<client>/assets/`; `Logo_Astellas_primary`, `Logo_Astellas_LogoOnly`, `Logo_Brunswick_black`, `Logo_Brunswick_white_transback` need to physically land there. `asset_resolve.py --audit` will confirm.
- **`alt_text` is empty on 253 of 255 entries.** It's the prerequisite for matching images to meaning — until an asset has described content, the only semantic signal is `tags`, which are just filename tokens. This is the vision pass.
- **Undecided:** whether an asset binds to the **script primitive** (a `process_flow` wants a process diagram — the more content-pure layer) or to **`expression.content_type`** (which needs `vocab/primitives.registry.json` populated first). Possibly both, at different strengths. `content_type_hints` on each entry is the placeholder either way, and it's advisory — a ranking signal, never a hard filter.
- **Two regulatory marks** (`icon_health-authority_logo` 3 and 4) are approved as *selectable* but their issuing agency is still unidentified; their `provenance` says confirm-before-use.
- **Open, from the same principle that moved `brands/` out of core:** `registry/glossary/astellas-pv.candidates.csv` and `registry/corpus/astellas-pv.ja.jsonl` are also client-specific. Consistency says they follow — but they're the localization agent's retrieval memory, so moving them means giving that agent a path config the way the asset registry now has one. Same pattern, more work.
