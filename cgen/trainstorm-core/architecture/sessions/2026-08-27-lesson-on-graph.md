# Session note — 2026-08-27 Lesson on the graph

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to make a **lesson a
graph object**: one course/lesson node that points at the existing
`spine.scenes` (ordered scene records with `element_ids`). Today the
ALSAP short lesson was a projector convention (realize.py knew this
project). A later agent should be able to emit another lesson by
writing a lesson record, not by forking HTML. Same 16 beats. Same
three scenes. Same pager. Same checks. No new ALSAP pedagogy.
`atoms.json` unchanged. No authored `content.text`. Open a PR off
current main (PR #29 scenes-on-graph is merged). Do not push `main`.
Claude is a co-builder — do not freeze them out of files or rewrite
their canon.

Recorded in `DECISIONS.md`:

- **Storage:** `manifest.lessons` (policy `v1_lesson_on_graph`, spec
  `agents/realizer/lesson_v1.md`). Default `{project}_short`. Title
  heuristic from the document-root atom (`title_from`). `scene_ids`
  point at `spine.scenes`. `lesson_end_check_ids` stay lesson-end.
  Paging pointer. No `Course` `ele_` (no honest `composed_from`).
  Older `course.schema.json` is not this constitution.
- **Projector** reads `--lesson` or the default lesson, then its
  scenes + checks. It does not hard-code “the ALSAP lesson is these
  three headings.” Coverage dump stays a second projection.
- Idempotent realize → cartographer → couturier. Selftest: lesson →
  scenes → element_ids resolve from the graph. Extra lesson records
  preserved. Cut from current main after PR #29.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, quiz engine, new agent, Procedure B,
inventing a `retrieve` enum, 1:many of the SOP, Dragoman, Storyline,
`.potx`, motion, PNG pipelines, LMS/SCORM, a course catalog UI.
