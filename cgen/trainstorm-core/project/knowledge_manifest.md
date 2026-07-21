# Trainstorm — Course Engine (Core) · Knowledge Manifest

> What goes in the project's **knowledge base**, what stays out, and how it maps to a git repo you sync from. The rule: knowledge = the **canonical spine only**, kept lean; everything working lives in git and in chats.

---

## The principle: git is truth, knowledge is a synced snapshot

Keep the canonical artifacts in one git repo (`trainstorm-core`). Sync them **one direction** into the project knowledge base — via [`claudesync`](https://pypi.org/project/claudesync/) or a Drive mirror — so the project is always a faithful reflection of git, never a second hand-maintained copy. If you upload copies *and* keep git *and* edit both, you've rebuilt the `sce_003` drift inside your own tooling. One source; sync down.

**Lean knowledge beats big knowledge.** A knowledge base stuffed with every generated course pulls the model toward stale instances and dilutes retrieval. Include the canon and *one* worked example — not the archive.

---

## Proposed repo → knowledge mapping

```
trainstorm-core/
├── schemas/
│   ├── element.schema.json            ✅ have   · CANONICAL unit — validate against this
│   ├── atom.schema.json               ✅ have   · conceptual node (the manifold)
│   └── examples/
│       └── example_element.json       ✅ have   · one validated worked element
├── vocab/
│   ├── intent.enum.json               ⬜ create · governed rhetorical + pedagogical intents
│   └── primitives.registry.json       ⬜ create · text/motion/layout/interaction/style keys
├── architecture/
│   ├── manifold.md                    ⬜ consolidate · system map + content-graph + audience/join, as TEXT
│   ├── conventions.md                 ⬜ create · the constitution, expanded (invariants + defaults + rationale)
│   └── reconciliation.md              ✅ have   · Trainstorm schema reconciliation decisions
├── reference/
│   └── brunswick.reference.course.json ⬜ clean · ONE validated worked course (fix the sce_003 collision)
├── tools/
│   └── lint_course.py                 ⬜ create · the drift-linter (ID collisions, count/vocab/embedded-locale checks)
└── README.md                          ⬜ create · what this repo is + the sync command
```

**Legend:** ✅ exists from this session · ⬜ to create/consolidate.

---

## What goes IN the knowledge base

| File | Why it's canon |
|---|---|
| `schemas/element.schema.json` | The single definition of a valid element. Everything validates against it. |
| `schemas/atom.schema.json` + `examples/example_element.json` | The conceptual node + a worked, validated instance the model can pattern-match to. |
| `vocab/intent.enum.json`, `vocab/primitives.registry.json` | The governed, closed vocabularies. Their existence as files *is* the governance. |
| `architecture/manifold.md` | The conceptual anchor — as **text/markdown**, because knowledge retrieval works far better on prose than on HTML. (Keep the rendered HTML diagrams as visual reference/artifacts, not primary knowledge.) |
| `architecture/conventions.md` | The expanded constitution — the "why" behind the invariants, so any chat can reason from first principles. |
| `architecture/reconciliation.md` | The decisions of record (why course/scene/primitives converged, the four fixes). Prevents relitigating settled calls. |
| `reference/brunswick.reference.course.json` | **One** clean, validated course as the gold-standard example. Fix the `sce_003` ID collision first so the reference is drift-free. |

---

## What STAYS OUT of the knowledge base

- **Every other generated course / draft / client deliverable.** These are *instances*, not canon. They bloat retrieval and drag toward stale patterns. They live in git and in chats.
- **Client-specific corpora** (e.g. the Astellas glossary, the JP exemplar corpus). Those belong to the *client* workstream, not the platform core. If you want a localization reference, include a *tiny* representative sample, not the full asset.
- **Rendered HTML diagrams / one-pagers.** Great as visual reference and for showing people; poor as retrieval knowledge. Keep them in `/reference/visual/` in git, not in the knowledge base.
- **Anything you're still deciding.** Settled decisions go in `reconciliation.md`; open questions stay in chats until resolved.

---

## Chats = workstreams (a convention, not knowledge)

Name chats by spoke so the project stays navigable. Suggested starting set:
- `schema & validation` — evolve `element.schema.json`, run the linter, govern the vocab.
- `localization agent` — locale packs, glossary/termbase, the RAG draft→review loop.
- `render / lottie` — HTML/CSS→PNG render agent; AE→Lottie path; `delivery` routing.
- `visual registry` — brand kits, tokens, fonts, logos, the layout templates.
- `generator` — script→element generation from source.

Keep a one-line index of active chats at the top of `README.md` so you can find them.

---

## Frontier = separate projects (later)

Do **not** fold these into Core. Spin them up when active, each with its own knowledge:
- **Response Engine** — the runtime/adaptivity join (reads content + learner model).
- **Orchestrator** — the coordination layer over the agents.

They share the *substrate* (this repo's schemas), so point their instructions at the same `element.schema.json` — but keep their build context separate so Core stays focused.

---

## First moves (in order)
1. Create the repo, drop in the three ✅ files (`element.schema.json`, `atom.schema.json`, `example_element.json`) and `reconciliation.md`.
2. Create the project; paste in the **Custom Instructions** constitution; wire `claudesync` (or a Drive mirror) so knowledge tracks the repo.
3. In the `schema & validation` chat: build `intent.enum.json`, `primitives.registry.json`, `conventions.md`, `manifold.md`, the drift-linter, and the cleaned Brunswick reference — then sync.
4. From there, open a chat per spoke and build.
