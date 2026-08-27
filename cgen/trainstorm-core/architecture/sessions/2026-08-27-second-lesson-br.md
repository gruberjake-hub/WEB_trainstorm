# Session note — 2026-08-27 Second lesson record (BR subset)

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to **prove the lesson
node is not a singleton**: write a second lesson record on the same
ALSAP occurrence store that points at a subset of existing
`spine.scenes` — the Benefit-risk scene (form presents + instance
examples + closed-choice). Same 55 `ele_` / 47 atoms. No new pedagogy
atoms. No authored `content.text`. Default stays `ast_alsap_short`.
Second id `ast_alsap_br`. Projector reads `--lesson` and writes a
second HTML derived from `lesson_id` without forking `realize.py` for
ALSAP. Open a PR off current main (PR #30 lesson-on-graph is merged).
Do not push `main`. Claude is a co-builder — do not freeze them out of
files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Storage:** `manifest.lessons` now has two records. Default
  `ast_alsap_short` (all three scenes + lesson-end invert_definition).
  Extra `ast_alsap_br` (`scene_ids` = `benefit_risk_on_the_form` only;
  empty `lesson_end_check_ids` — those checks do not belong here).
- **HTML:** `realized_lesson.html` is still the short path (pages
  1–2–3). `realized_lesson_br.html` is a read of `ast_alsap_br` (one
  scene, pager disabled). Coverage dump stays a dump.
- Realize carries extra lesson records across a fresh manifest
  rebuild. Idempotent realize → cartographer → couturier. Selftest:
  both lesson_ids resolve `scene_ids` from the graph. Cut from current
  main after PR #30.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, quiz engine, new agent, Procedure B,
inventing a `retrieve` enum, 1:many of the SOP, Dragoman, Storyline,
`.potx`, motion, PNG pipelines, LMS/SCORM, a course catalog UI.
