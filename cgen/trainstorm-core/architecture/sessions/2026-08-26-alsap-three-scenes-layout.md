# Session note — 2026-08-26 ALSAP three-scene layout chrome

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to group the short ALSAP
lesson so it reads as **three scenes**, not sixteen stacked cards. Layout
only: no new beats, no new atoms, no new `ele_` if avoidable. Open a PR.
Do not push `main`. Claude is a co-builder — do not freeze them out of
files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Scene chrome** (`tools/realize.py`, `agents/realizer/spine_v1.md`,
  policy `v1_three_scenes_from_roles`). Named section headings group
  existing spine occurrences from SOP/form roles already in the graph.
  Not an LLM. Not outcome language.
- **Three scenes:** What an ALSAP is (front-matter) → How an ALSAP starts
  (Procedure A job-aid + in-scene sequence practice) → Benefit-risk on
  the form (BR-field presents + instance examples). Definition/purpose
  checks stay at lesson end.
- Same 16 `ele_` ids. Same `composed_from`. `atoms.json` untouched. No
  authored `content.text`. Coverage dump stays ungrouped.
- Cartographer still owns intent. Couturier still owns style. Idempotent
  with realize → cartographer → couturier. Store stays 55 / 47.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, Procedure B, extra form dump,
Dragoman, Storyline, `.potx`, motion, PNG pipelines, inventing a
`retrieve` enum, new meaning.
