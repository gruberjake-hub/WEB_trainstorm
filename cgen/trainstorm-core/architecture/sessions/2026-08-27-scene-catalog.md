# Session note — 2026-08-27 Scene catalog is project data

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to lift scene membership
into **project data**: a closed catalog file Realizer reads and stamps
onto `spine.scenes`, the same write path as `occurrences/lessons.json`.
PR #32 made lessons a catalog; scenes were still a spine heuristic
inside Realizer. Same 55 `ele_` / 47 atoms. Same three scenes. Same
three lessons. No new ALSAP pedagogy. No authored `content.text`. Open
a PR off current main (PR #32 lesson catalog is merged). Do not push
`main`. Claude is a co-builder — do not freeze them out of files or
rewrite their canon.

Recorded in `DECISIONS.md`:

- **Catalog:** `occurrences/scenes.json` is the source of truth.
  `spine.scenes` is the stamped runtime view. Adding a scene is
  appending a record (id, title heuristic/ref, ordered element_ids,
  in-scene checks). Realize does not special-case the three ALSAP
  headings in Python beyond reading the catalog. Lessons keep pointing
  at `scene_ids` only.
- **Membership:** the three scenes PR #29 already stamped
  (`what_an_alsap_is` / `how_an_alsap_starts` /
  `benefit_risk_on_the_form`) — not a rival list. Heuristic may still
  propose a default when the file is absent. Live path is read-the-file.
- HTML should feel unchanged: short pages 1–2–3; br and plan
  single-scene. Coverage dump stays a dump. Idempotent realize →
  cartographer → couturier. Selftest: scene catalog `element_ids`
  resolve from the graph; lesson catalog `scene_ids` resolve. Cut from
  current main after PR #32.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, quiz engine, new agent, Procedure B,
inventing a `retrieve` enum, 1:many of the SOP, Dragoman, Storyline,
`.potx`, motion, PNG pipelines, LMS/SCORM, a course catalog UI.
