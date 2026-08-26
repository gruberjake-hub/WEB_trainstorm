# Session note — 2026-08-26 Procedure A sequence practice

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) for honest Procedure A
**practice**: after the job aid (Gagné-ish: practice the steps near the
job aid; instance example can stay as exemplify), add a check that is
**order the four existing Procedure A step atoms**. Not an MCQ stem
like “which is the first planning step?” (PR #16 refused that invented
fact). Not LLM distractors. Jake parked a distractor-writer. Open a PR.
Do not push `main`. Claude is a co-builder — do not freeze them out of
files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **New check shape `sequence`** (`agents/realizer/check_v1.md`). Items
  = first sentences of `atom_sop_ast29080_proc_a_s1` … `_s4`. Correct
  order = `bindings.object.order`. Definition checks stay invert-
  definition MCQ.
- **Mint nothing.** Composing from one A step (or the thin A heading)
  is a lie. Project from the four existing present `ele_` records.
  Store stays 53. `atoms.json` untouched. No authored `content.text`.
- Placement: after the job aid, before the instance example. Learner
  can be wrong, then right. Feedback does not invent SOP facts.
- Closed vocab. No `retrieve`. No chameleon.py. No `/cgen/alsap`
  hosting. No 1:many of the SOP. Idempotent realize → cartographer →
  couturier.

Out of scope this session: distractor-writer, chameleon.py, Headwater
outcomes-mode, `/cgen/alsap` hosting, Dragoman, Storyline, `.potx`,
motion, PNG pipelines, procedure B/C on the spine, inventing a
`retrieve` enum, 1:many of the procedure tree.
