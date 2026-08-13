# Trainstorm Core — Repository Structure

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
└── trainstorm-core/                     # the build system itself (the tree below)
```

```
trainstorm-core/
├── README.md
├── STRUCTURE.md                          ← this file
│
├── schemas/                              # the data contracts — validate against these
│   ├── element.schema.json               ✅ presentation unit (HOW shown)
│   ├── atom.schema.json                  ✅ conceptual node (the manifold)
│   ├── script.primitives.v1.json         ✅ generation IR (WHAT knowledge)
│   ├── visual-asset.schema.json          ✅ one visual asset registry entry
│   └── objectives.schema.json            ✅ intent ontology — objective node contract
│
├── vocab/                                # governed, closed vocabularies
│   ├── intent.enum.json                  ✅ rhetorical + pedagogical intents
│   └── primitives.registry.json          ⬜ text/motion/layout/interaction/style keys
│
├── agents/                              # the agents' GOVERNED PROMPTS (contracts, not code) — these sync
│   └── localize/
│       ├── system.md                     ✅ the translation agent's prompt (loc-agent.v0.1)
│       └── README.md                     ✅ manifest: I/O contract + how to run
│       # generator/ realizer/ render/    ⬜ same shape when those agents get prompts
│
├── registry/                            # backing store + retrieval memory (git-only, not synced)
│   ├── visual-assets.registry.json       ✅ 255 governed image assets — the MAP, not the bytes
│   ├── templates/                        ⬜ HTML/CSS layout templates per layout_primitive
│   ├── glossary/
│   │   └── astellas-pv.candidates.csv    ✅ locked-term seed (→ .json once reviewer confirms)
│   └── corpus/
│       └── astellas-pv.ja.jsonl          ✅ 1,164-pair exemplar corpus — fed to the retriever, NEVER synced
│
├── locales/                             # externalized translations, keyed by element_id
│   └── <bcp47>.json                      ⬜ e.g. ja.json, fr-CA.json
│
├── ontology/                            # the intent ontology — objective/competency graph, keyed by obj_
│   └── objectives.json                   ✅ obj_ objective nodes (owner: L&D) — teaches[] resolves here
│
├── architecture/                        # docs of record (the .md files sync to Project knowledge)
│   ├── manifold.md                       ⬜ system map + content graph + audience/join, as TEXT
│   ├── conventions.md                    ⬜ the constitution, expanded
│   ├── reconciliation.md                 ✅ schema reconciliation decisions
│   ├── conversation-reconciliation.md    ✅ chat evidence → candidate → canonical decision
│   ├── script-generation-layer.md        ✅ generation-layer placement + realization table
│   ├── atom-spec.md                      ✅ the atom, annotated
│   ├── localization-agent.md             ✅ the RAG localization pipeline
│   └── diagrams/                         # rendered HTML — visual reference, git-only (don't sync)
│       ├── system-map.html               ✅
│       ├── content-graph.html            ✅
│       └── audience-join.html            ✅
│
├── reference/                           # ONE clean, validated example of each layer
│   ├── example_element.json              ✅
│   ├── example_atom.json                 ✅
│   ├── sample_script.json                ✅
│   └── brunswick.reference.course.json   ⬜ gold-standard course (fix the sce_003 collision first)
│
├── tools/                               # the agents' runtime code & utilities
│   ├── lint.py                           ✅ the drift/vocab linter
│   ├── localize/                         # the translation agent's runtime (reads agents/localize/system.md)
│   │   ├── build_agent_call.py           ✅ assembles the [system,user] call from registry memory
│   │   └── verify_agent_output.py        ✅ QE gate + locale-pack mapping check
│   ├── chat-capture/                      # ChatGPT export → provenance-preserving inventory
│   │   └── extract_chatgpt.py             ✅ local evidence intake; never promotes decisions
│   ├── assets/                           # the visual-asset pipeline: ingest → promote → approve
│   │   ├── ingest_images.py              ✅ mechanical tier: hash · dims · OCR · perceptual dedup
│   │   ├── promote.py                    ✅ staging → registry entries (idempotent; preserves approvals)
│   │   ├── approve.py                    ✅ records a human sign-off (has --dry-run)
│   │   ├── asset_resolve.py              ✅ asset_id → path on disk; verify() + audit()
│   │   └── requirements.txt              ⬜ pillow · imagehash · jsonschema · pytesseract (+ system tesseract)
│   ├── realize.py                        ⬜ (later) primitives → elements
│   └── render/                           ⬜ (later) element → HTML → PNG
│
└── project/                             # Claude Project setup
    ├── custom_instructions.md            ✅ paste into the Project's Custom Instructions
    └── knowledge_manifest.md             ✅ what goes in the knowledge base + sync notes
```

`✅` = already built (in the scaffold). `⬜` = placeholder waiting for you (or me).

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

## First moves

1. Unzip the scaffold → `git init` → first commit (you now have a coherent, validated core).
2. Fill the `⬜` placeholders — the near-term build: `primitives.registry.json`, `manifold.md`, `conventions.md`, `tools/lint.py`, and the cleaned `brunswick.reference.course.json`.
3. Wire `claudesync` with the include/exclude above; point the Project's knowledge at the synced folders.
4. Paste `project/custom_instructions.md` into the Project. You're live.

## Next on the visual-asset track

- **Move 4 files.** The registry declares identity marks at `cgen/brands/<client>/assets/`; `Logo_Astellas_primary`, `Logo_Astellas_LogoOnly`, `Logo_Brunswick_black`, `Logo_Brunswick_white_transback` need to physically land there. `asset_resolve.py --audit` will confirm.
- **`alt_text` is empty on 253 of 255 entries.** It's the prerequisite for matching images to meaning — until an asset has described content, the only semantic signal is `tags`, which are just filename tokens. This is the vision pass.
- **Undecided:** whether an asset binds to the **script primitive** (a `process_flow` wants a process diagram — the more content-pure layer) or to **`expression.content_type`** (which needs `vocab/primitives.registry.json` populated first). Possibly both, at different strengths. `content_type_hints` on each entry is the placeholder either way, and it's advisory — a ranking signal, never a hard filter.
- **Two regulatory marks** (`icon_health-authority_logo` 3 and 4) are approved as *selectable* but their issuing agency is still unidentified; their `provenance` says confirm-before-use.
- **Open, from the same principle that moved `brands/` out of core:** `registry/glossary/astellas-pv.candidates.csv` and `registry/corpus/astellas-pv.ja.jsonl` are also client-specific. Consistency says they follow — but they're the localization agent's retrieval memory, so moving them means giving that agent a path config the way the asset registry now has one. Same pattern, more work.
