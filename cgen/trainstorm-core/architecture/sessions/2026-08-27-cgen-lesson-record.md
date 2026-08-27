# Session note — 2026-08-27 Course Engine plays the lesson node

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to point the existing
**Course Engine v1** at `/cgen` at a **lesson record** from the ALSAP
occurrence graph, so he is not living only in sidecar
`realized_lesson.html`. Sidecar HTML stays a projector. Do **not**
replace `/cgen`. Do **not** touch `/cgen/lumina`. Do **not** revive the
`/cgen/alsap` Netlify rewrite. Default lesson: `ast_alsap_short`. Open
a PR off current main (PR #33 scene catalog is merged). Do not push
`main`. Claude is a co-builder — do not freeze them out of files or
rewrite their canon.

Recorded in `DECISIONS.md`:

- **Adapter:** the engine cannot consume occurrence files as-is.
  Realize writes `realized_lesson.json` — a projection of the lesson
  node (lesson → scenes → element_ids → atoms; checks from
  `manifest.checks`). `/cgen` loads that through existing chrome.
  Not a hand-authored SCORM package. Not a third constitution.
- **Player:** three named scenes, pager, in-scene `sequence_order` +
  `closed_choice`, lesson-end `invert_definition`. Meaning from atoms.
  `SequenceOrder` / `StepList` are the minimum engine additions.
- Idempotent realize → cartographer → couturier emits sidecars **and**
  the JSON `/cgen` reads. Selftest covers the projection. Cut from
  current main after PR #33.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, quiz engine, new agent, Procedure B,
inventing a `retrieve` enum, 1:many of the SOP, Dragoman, Storyline,
`.potx`, motion, PNG pipelines, LMS/SCORM, a course catalog UI, new CSP.
