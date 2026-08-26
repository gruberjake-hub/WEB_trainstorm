# Session note — 2026-08-26 FORM-AST-34037 BR closed-choice

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) for **one honest check**
in scene 3 after the FORM-AST-34037 BR field presents and ASP-9999
examples, before lesson-end definition checks. Same honesty bar as
Procedure A sequence: do not invent an MCQ stem, do not use an LLM
distractor writer, options must be verbatim closed values already in
the graph. If there is no honest closed set, stop. Open a PR. Do not
push `main`. Claude is a co-builder — do not freeze them out of files
or rewrite their canon. PR #26 paging stays.

Recorded in `DECISIONS.md`:

- **New check shape `closed_choice`** (`agents/realizer/check_v1.md`).
  Options = value ids of `reg_benefit_risk_profile`. Key = instance
  `selected_value` `conditional_favorable`. Prompt is task clothes:
  *Choose the closed value already shown.* Rationale has no closed set.
- **Mint nothing.** Composing from only the form field or only the
  instance is a half-lie. Project from the two existing guest `ele_`
  records. Store stays 55. Spine membership 16. `atoms.json` untouched.
  No authored `content.text`.
- Placement: in-scene 3, after field+example. Learner can be wrong,
  then right. Feedback invents no SOP facts. Paging still works.
- Closed vocab. No `retrieve`. No chameleon.py. No `/cgen/alsap`
  hosting. No Procedure B. No extra form dump. Idempotent realize →
  cartographer → couturier.

Out of scope this session: distractor-writer, chameleon.py, Headwater
outcomes-mode, `/cgen/alsap` hosting, Dragoman, Storyline, `.potx`,
motion, PNG pipelines, procedure B/C on the spine, inventing a
`retrieve` enum, stretching phrasing-example cousins, a rationale MCQ.
