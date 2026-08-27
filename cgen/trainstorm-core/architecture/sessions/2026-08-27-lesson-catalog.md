# Session note — 2026-08-27 Lesson catalog + Procedure A third lesson

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to lift lesson records
into **project data**: a closed catalog file Realizer reads and stamps
onto `manifest.lessons`, plus a third lesson pointing at the existing
Procedure A scene. PR #31 had two lessons on one store, but extras
still lived as carry-across on the generated manifest. Same 55 `ele_`
/ 47 atoms. No new pedagogy atoms. No authored `content.text`. Open a
PR off current main (PR #31 second lesson is merged). Do not push
`main`. Claude is a co-builder — do not freeze them out of files or
rewrite their canon.

Recorded in `DECISIONS.md`:

- **Catalog:** `occurrences/lessons.json` is the source of truth.
  `manifest.lessons` is the stamped runtime view. Adding a lesson is
  appending a record (id, scene_ids, optional lesson_end_check_ids,
  paging). Realize does not special-case `ast_alsap_br` /
  `ast_alsap_plan` in Python.
- **Three HTMLs:** `realized_lesson.html` (`ast_alsap_short`, pages
  1–2–3). `realized_lesson_br.html` (scene 3). `realized_lesson_plan.html`
  (scene 2, job-aid + sequence check, pager off). Coverage dump stays
  a dump.
- Default pass emits all catalog lessons. `--lesson <id>` regenerates
  that file. Idempotent realize → cartographer → couturier. Selftest:
  catalog records resolve; no extra lesson_id hardcoded in the
  projector. Cut from current main after PR #31.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, quiz engine, new agent, Procedure B,
inventing a `retrieve` enum, 1:many of the SOP, Dragoman, Storyline,
`.potx`, motion, PNG pipelines, LMS/SCORM, a course catalog UI.
