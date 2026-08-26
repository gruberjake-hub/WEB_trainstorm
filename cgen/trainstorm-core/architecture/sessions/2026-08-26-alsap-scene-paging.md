# Session note — 2026-08-26 ALSAP scene player chrome

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to page the short ALSAP
lesson so it shows **one named scene at a time**, with Next/Back. Player
chrome only: no new beats, no new atoms, no new `ele_` if avoidable.
PR #25’s three scene headings stay. Open a PR. Do not push `main`.
Claude is a co-builder — do not freeze them out of files or rewrite
their canon.

Recorded in `DECISIONS.md`:

- **Player chrome** (`tools/realize.py`, `agents/realizer/spine_v1.md`,
  policy `v1_one_scene_at_a_time`). Next/Back pages the existing named
  sections from `v1_three_scenes_from_roles`. Not an LLM. Not outcome
  language. Hash optional.
- **Three scenes, unchanged titles:** What an ALSAP is → How an ALSAP
  starts (Procedure A job-aid + in-scene sequence practice) →
  Benefit-risk on the form (BR-field presents + instance examples).
  Definition/purpose checks stay a final step after scene 3, not a
  fourth scene.
- Same 16 `ele_` ids. Same `composed_from`. `atoms.json` untouched. No
  authored `content.text`. Coverage dump stays ungrouped and unpaged.
- Cartographer still owns intent. Couturier still owns style. Idempotent
  with realize → cartographer → couturier. Store stays 55 / 47.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, Procedure B, extra form dump,
Dragoman, Storyline, `.potx`, motion, PNG pipelines, inventing a
`retrieve` enum, new meaning.
