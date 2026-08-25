# Session note — 2026-08-25 Couturier v1

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to give Couturier a first real write:
style / expression keys on existing ALSAP `ele_` records so different moves look
like different clothes, then open a PR. Do not push `main`. Claude is a co-builder
— do not freeze them out of files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Couturier v1** (`tools/couturier.py`, `agents/couturier/style_map_v1.md`).
  Writes only occurrence style keys on `element.expression`. Never mints `ele_`
  / `atom_` ids. Never copies meaning onto the element. Never rewrites
  `atoms.json` or `element.intent`.
- **Small map** from `move` (hook / present / reinforce-as-retrieve, plus the
  other live moves). Not a design system. Motion / Storyline / `.potx` not bound.
- HTML re-projected so the 1:many pairs (title hook+present, definition
  present+reinforce) do not look identical. Meaning still from the atom.
- Idempotent with realize and cartographer: extras, intent, and style survive
  re-runs.

Out of scope this session: Dragoman, Storyline, `.potx`, motion primitives
beyond a stub mention, `tools/render/` PNG pipelines, rewriting SOP/form atoms
into elements.
