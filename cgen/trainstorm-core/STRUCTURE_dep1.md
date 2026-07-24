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
| a **doc that explains or decides** | `architecture/` |
| a **worked example** | `reference/` |
| **code that transforms, checks, or runs an agent** | `tools/` |
| a **client's actual course** | **not here** → separate `trainstorm-courses/` repo |

An **agent is three kinds, not one** — so it lives in three places, never one feature folder: its **prompt** (a governed contract, like a schema) → `agents/<agent>/`; the **code** that runs it → `tools/<agent>/`; the **memory** it retrieves from (glossary, exemplar corpus) → `registry/`. That's why the localization agent's prompt is not in `tools/` next to its scripts — the prompt and the plumbing have different lifecycles, editors, and sync rules.

That single question answers ~95% of "where does this file go." Note it's *kind*, not *topic*: a Brunswick example course is a "worked example" (→ `reference/`), not a "Brunswick thing."

## The tree

```
trainstorm-core/
├── README.md
├── STRUCTURE.md                          ← this file
│
├── schemas/                              # the data contracts — validate against these
│   ├── element.schema.json               ✅ presentation unit (HOW shown)
│   ├── atom.schema.json                  ✅ conceptual node (the manifold)
│   └── script.primitives.v1.json         ✅ generation IR (WHAT knowledge)
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
│   ├── brands/<brand>/                   ⬜ tokens.css · fonts/ · logos/
│   ├── templates/                        ⬜ HTML/CSS layout templates per layout_primitive
│   ├── glossary/
│   │   └── astellas-pv.candidates.csv    ✅ locked-term seed (→ .json once reviewer confirms)
│   └── corpus/
│       └── astellas-pv.ja.jsonl          ✅ 1,164-pair exemplar corpus — fed to the retriever, NEVER synced
│
├── locales/                             # externalized translations, keyed by element_id
│   └── <bcp47>.json                      ⬜ e.g. ja.json, fr-CA.json
│
├── architecture/                        # docs of record (the .md files sync to Project knowledge)
│   ├── manifold.md                       ⬜ system map + content graph + audience/join, as TEXT
│   ├── conventions.md                    ⬜ the constitution, expanded
│   ├── reconciliation.md                 ✅ schema reconciliation decisions
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
- **Stable ID prefixes** (never reused/edited): `ele_` element · `atom_` atom · `obj_` objective · `term_` glossary term · `prim_`/`p###` script primitive · `sce_`/`sec_`/`mod_` structure.

## What syncs to the Claude Project knowledge (vs. git-only)

Keep the knowledge base **lean**. Configure `.claudesync` (or your Drive mirror) to include only:

- **SYNC:** `schemas/`, `vocab/`, `agents/**/*.md` (the prompts — you refine these *in* the Project), `architecture/*.md` (not `diagrams/`), `reference/*.json`, `project/`
- **GIT-ONLY (don't sync):** `registry/` assets and **especially `registry/corpus/`** (fed to the retriever, never loaded into context — a 600 KB corpus in the knowledge base would wreck it), `locales/` packs, `architecture/diagrams/` (HTML), `tools/` code, and anything under a client courses repo.

Reason: the agent prompts are governed contracts you reason about, so they belong in context — but the corpus is *retrieval fuel*, not reading material. The retriever pulls 3 exemplars per string at runtime; the model never needs all 1,164 in its context. Fonts, HTML diagrams, and code likewise bloat retrieval without helping the model reason.

## Where the rest lives (deliberately NOT in core)

- **Client courses** (Brunswick production, Astellas, future clients) → a **separate `trainstorm-courses/<client>/` repo** that references core schemas. Only *one clean copy of one course* lives here, in `reference/`, as the gold example.
- **Frontier** (Response Engine, Orchestrator) → their **own repos/projects** when active; they import these schemas but keep their own build context.

## First moves

1. Unzip the scaffold → `git init` → first commit (you now have a coherent, validated core).
2. Fill the `⬜` placeholders — the near-term build: `primitives.registry.json`, `manifold.md`, `conventions.md`, `tools/lint.py`, and the cleaned `brunswick.reference.course.json`.
3. Wire `claudesync` with the include/exclude above; point the Project's knowledge at the synced folders.
4. Paste `project/custom_instructions.md` into the Project. You're live.
