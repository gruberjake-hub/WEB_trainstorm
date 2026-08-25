# Trainstorm — Course Engine (Core) · Knowledge Manifest

> What goes in the project's **knowledge base**, what stays out, and how it maps to git. The rule: knowledge = the **canonical spine only**, kept lean; everything working lives in git and in chats.

---

## The principle: git is truth, knowledge is a one-way snapshot

Keep the canonical artifacts in one git repo (`cgen/trainstorm-core` inside `WEB_trainstorm`). Sync them **one direction** into the Claude Project knowledge base — via [`claudesync`](https://pypi.org/project/claudesync/) or a Drive mirror — so the project is always a faithful reflection of git, never a second hand-maintained copy. If you upload copies *and* keep git *and* edit both, you've rebuilt the `sce_003` drift inside your own tooling. One source; sync down.

**Settled 2026-08-25** (`architecture/DECISIONS.md`): git is the only shared brain between Claude and other assistants. Assistants open PRs; Jake merges; Jake pulls. Claude Custom Instructions and this manifest **point at git canon** — they do not restate a second constitution. If a chat disagrees with `DECISIONS.md`, the file wins.

**Lean knowledge beats big knowledge.** A knowledge base stuffed with every generated course pulls the model toward stale instances and dilutes retrieval. Include the canon and *one* worked example — not the archive.

---

## Current canon (sync these)

```
trainstorm-core/
├── STRUCTURE.md                         ✅ tree, prefixes, same-node-two-costumes
├── schemas/
│   ├── atom.schema.json                 ✅ CANONICAL NODE — validate against this
│   ├── element.schema.json              ✅ course costume of the same node (not a second key)
│   ├── procedure.facet.schema.json      ✅
│   ├── form.facet.schema.json           ✅
│   ├── instance.facet.schema.json       ✅
│   └── … sibling contracts
├── vocab/                               ✅ governed closed lists — existence *is* governance
│   ├── intent.enum.json                 ✅ rhetorical + pedagogical
│   ├── primitives.registry.json         ⚠ partial (layout/interaction seeded; text/motion still thin)
│   ├── procedure.enum.json · form.enum.json · evidence.enum.json · instance.enum.json
│   ├── structure.enum.json · complexity.enum.json · tone.enum.json · visual-type.enum.json
├── architecture/
│   ├── DECISIONS.md                     ✅ append-only canon (identity freeze · working process)
│   ├── reconciliation.md                ✅ July schema-convergence record (identity now frozen)
│   ├── manifold.md · atom-spec.md · conventions.md (stub)
│   └── sessions/                        ⚠ notes, not canon — optional sync
├── reference/
│   └── example_atom.json                ✅ one validated worked atom
├── tools/
│   └── validate_atoms.py                ✅ THE GATE (code is git-only; name it in instructions)
└── project/
    ├── custom_instructions.md           ✅ this constitution, pointed at git
    └── knowledge_manifest.md            ✅ this file
```

**Legend:** ✅ exists and is current enough to sync · ⚠ present but thin/stale in a labelled way · ⬜ still to create.

Do **not** keep a ⬜ “create `intent.enum.json` / `primitives.registry.json`” on this list — those files exist.

---

## What goes IN the knowledge base

| File | Why it's canon |
|---|---|
| `STRUCTURE.md` | Tree, prefixes, same node / two costumes. |
| `architecture/DECISIONS.md` | Settled calls. Chat loses if it disagrees. |
| `schemas/atom.schema.json` | The single definition of a valid node. The gate validates against it. |
| `reference/example_atom.json` | A worked, validated instance the model can pattern-match to. |
| `vocab/*.enum.json`, `vocab/primitives.registry.json` | Governed, closed vocabularies. Their existence as files *is* the governance. |
| `architecture/manifold.md` | The conceptual anchor — as **text/markdown**, because knowledge retrieval works far better on prose than on HTML. |
| `architecture/conventions.md` | The expanded constitution (still a stub; do not invent a rival copy). |
| `architecture/reconciliation.md` | Historical convergence of course/scene/primitives. Identity freeze lives in `DECISIONS.md`. |
| `project/custom_instructions.md` | Always-on pointer at the above — not a second source. |

`element.schema.json` may sync as the **course costume** contract. It is not the canonical unit and not a second ID space.

---

## What STAYS OUT of the knowledge base

- **Every other generated course / draft / client deliverable.** These are *instances*, not canon. They bloat retrieval and drag toward stale patterns. They live in git and in chats.
- **Client-specific corpora** (e.g. the Astellas glossary, the JP exemplar corpus). Those belong to the *client* workstream, not the platform core. Client **stores** live in `cgen/astellas/` and stay there.
- **Rendered HTML diagrams / one-pagers.** Great as visual reference and for showing people; poor as retrieval knowledge. Keep them in git, not in the knowledge base.
- **Anything you're still deciding.** Settled decisions go in `architecture/DECISIONS.md`; open questions stay in chats (or `architecture/sessions/` notes) until resolved.

---

## Chats = workstreams (a convention, not knowledge)

Name chats by spoke so the project stays navigable. Suggested starting set:
- `schema & validation` — evolve `atom.schema.json`, run `validate_atoms.py`, govern the vocab. Read `DECISIONS.md` first.
- `localization agent` — locale packs keyed by `atom_id`, glossary/termbase, the RAG draft→review loop. (Do not implement Dragoman unless asked.)
- `render / lottie` — HTML/CSS→PNG render agent; AE→Lottie path; `delivery` routing.
- `visual registry` — brand kits, tokens, fonts, logos, the layout templates.
- `generator` — script primitives from source; realizer writes a course costume of the **same** `atom_id`.

Keep a one-line index of active chats at the top of `README.md` so you can find them.

---

## Frontier = separate projects (later)

Do **not** fold these into Core. Spin them up when active, each with its own knowledge:
- **Response Engine** — the runtime/adaptivity join (reads content + learner model).
- **Orchestrator** — the coordination layer over the agents.

They share the *substrate* (this repo's schemas), so point their instructions at the same `atom.schema.json` and `architecture/DECISIONS.md` — but keep their build context separate so Core stays focused.

---

## First moves (in order)
1. After Jake merges a PR, **pull** locally; re-sync this knowledge base FROM git (one way).
2. Read `architecture/DECISIONS.md` and `STRUCTURE.md` at the start of a session.
3. Run `tools/validate_atoms.py` against the live stores before changing them. Do not move `cgen/astellas/`.
4. Course-chain work (realize / render / Brunswick gold course) is still owed — without minting `ele_` IDs.
