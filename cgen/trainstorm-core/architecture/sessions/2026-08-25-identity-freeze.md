# Session note — 2026-08-25 identity freeze

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to freeze node identity and install a shared multi-agent working process in `cgen/trainstorm-core/`, then open a PR. Jake merges; he pulls locally. Do not push to `main`. Do not move `cgen/astellas/` stores.

Recorded in `DECISIONS.md`:
1. **`atom_id` is the only node key.** Element = same node, course costume. No `ele_` minting; no new `element_id` at realization. Locale packs and expression keys bind to `atom_id`. Couturier = style on expression; Realizer (later) = layout/render; neither invents an id. Single-writer per facet holds.
2. **Git is the shared brain.** PRs in, Jake merges, Jake pulls. Claude project knowledge is a one-way sync FROM git. `DECISIONS.md` wins over chat.

Claude’s always-on files (`project/custom_instructions.md`, `project/knowledge_manifest.md`) were retargeted to point at git canon instead of restating a second constitution. They no longer claim `element.schema.json` as the canonical unit.

Out of scope this session: Dragoman, `realize.py`, new agents, mass prompt-pack rewrites, Astellas store moves.
