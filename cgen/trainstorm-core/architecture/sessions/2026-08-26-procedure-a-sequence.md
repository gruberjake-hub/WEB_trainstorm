# Session note — 2026-08-26 Procedure A as a job sequence

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to turn Procedure A on the
short lesson from a single notify sentence into a job sequence. PR #16 put
`atom_sop_ast29080_proc_a_s1` / `ele_sop_ast29080_proc_a_s1` on the spine as
one present. Open a PR. Do not push `main`. Claude is a co-builder — do not
freeze them out of files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Spine heuristic extended** (`tools/realize.py`, `agents/realizer/spine_v1.md`,
  policy `v1_front_matter_procedure_sequence_then_checks`). After front-matter,
  the first Procedures branch’s non-thin `procedure_step` children in
  `object.order` (not thin A/B/C headings), then the existing checks. Cap 8.
  Not an LLM call.
- **Procedure A, four real steps.** `atom_sop_ast29080_proc_a_s1` through
  `_s4` (notify Lead → identify authors → 15-day kick-off → confirm
  deliverables). All four presents. B/C stay coverage.
- **No extra `ele_` / no procedure check.** Imperative steps have sibling
  sentences but no honest copula invert. Cloze is not sibling contrast.
  Distractor-writer stays parked.
- Cartographer still owns intent. Couturier still owns style. Idempotent
  with realize → cartographer → couturier. Store stays 50.

Out of scope this session: distractor-writer agent, Dragoman, Storyline,
`.potx`, motion primitives, `tools/render/` PNG pipelines, rewriting SOP/form
atoms into elements, inventing a `retrieve` enum value, 1:many of the
procedure tree, procedure B/C on the spine.
