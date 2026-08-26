# Session note — 2026-08-25 Lesson spine v1

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to project a short ALSAP lesson
path an ID would actually teach, while keeping the full occurrence dump as
coverage. The course hop is proven (PR #14); the HTML was still every SOP atom
in document order. Open a PR. Do not push `main`. Claude is a co-builder —
do not freeze them out of files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Spine projection** (`tools/realize.py`, `agents/realizer/spine_v1.md`).
  Documented heuristic: root opening, teachable front-matter primaries,
  existing `reinforce` checks. Not an LLM call. Reuses object `belongs_to` /
  `order` as input; does not treat the tree walk as the path.
- **Two HTML files:** `realized_lesson.html` (short lesson) and
  `realized_coverage.html` (full dump). No `ele_` or atoms dropped.
- Reuses existing extras (`atom_sop_ast29080` hook+present,
  `atom_sop_ast29080_general` present+check, `atom_sop_ast29080_purpose`
  objective+check). Cartographer still owns intent. Couturier still owns
  style. Idempotent with realize → cartographer → couturier.

Out of scope this session: distractor-writer agent, Dragoman, Storyline,
`.potx`, motion primitives, `tools/render/` PNG pipelines, rewriting SOP/form
atoms into elements, inventing a `retrieve` enum value.
