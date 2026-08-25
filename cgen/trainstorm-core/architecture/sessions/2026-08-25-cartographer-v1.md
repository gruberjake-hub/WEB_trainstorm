# Session note — 2026-08-25 Cartographer v1

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to give Cartographer a first real write:
occurrence-level `move` and `teaches` on the ALSAP Realizer output, then open a PR. Do not push
`main`.

Recorded in `DECISIONS.md`:
- **Cartographer v1** (`tools/cartographer.py`) is a documented heuristic compiler
  (`agents/cartographer/heuristic_v1.md`). Writes only occurrence intent. Never mints `ele_` /
  `atom_` ids. Never copies meaning onto the element. Never rewrites `atoms.json`.
- **Ontology seed:** 1 draft ALSAP goal + 5 draft objectives, distilled from SOP-AST-29080. Status
  `draft` (SOP is real; not human-locked). AST009 PSI example goal/objectives kept. Not a 50-node
  graph.
- HTML re-projected so move pills are not all `present`. `teaches` bound sparsely.

**Why previous Cartographer dispatches wrote nothing:** ontology was example seed, so `teaches` was
unbindable. That is the gap this seed closes for this SOP.

**Next:** Couturier (style keys) or Realizer 1:many minting. Not this hop.

Out of scope: Couturier, Dragoman, Storyline, a new Realizer architecture.
