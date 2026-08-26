# Session note — 2026-08-26 One procedure on the lesson spine

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to put one real ALSAP
procedure on the short lesson spine. PR #15 made `realized_lesson.html` a
7-beat front-matter lesson; procedure steps lived only in
`realized_coverage.html`. Open a PR. Do not push `main`. Claude is a
co-builder — do not freeze them out of files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Spine heuristic extended** (`tools/realize.py`, `agents/realizer/spine_v1.md`,
  policy `v1_front_matter_one_procedure_then_checks`). After front-matter,
  the first Procedures branch’s lead `procedure_step` (not thin A/B/C
  headings), then the existing checks. Not an LLM call.
- **Procedure A, lead atom `atom_sop_ast29080_proc_a_s1`.** First real work
  in `object.order` (Plan Development — GSO notifies SDS / requests a Lead).
  One present. Later A steps and B/C stay coverage.
- **No extra `ele_` / no procedure check.** Imperative steps have sibling
  sentences but no honest copula invert. Cloze is not sibling contrast.
  Distractor-writer stays parked.
- Cartographer still owns intent. Couturier still owns style. Idempotent
  with realize → cartographer → couturier. Store stays 50.

Out of scope this session: distractor-writer agent, Dragoman, Storyline,
`.potx`, motion primitives, `tools/render/` PNG pipelines, rewriting SOP/form
atoms into elements, inventing a `retrieve` enum value, 1:many of the
procedure tree.
