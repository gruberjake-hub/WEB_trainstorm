# Session note — 2026-08-27 Scenes on the graph

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to make scene membership
and order **first-class on the occurrence store / manifest** so a later
agent can emit a paged lesson without special-casing `realize.py`. No
new beats. No Procedure B. Same 16 spine occurrences. Same three
scenes. Same paging. `atoms.json` unchanged. No authored
`content.text`. Open a PR off current main (PR #28 check-shapes is
merged). Do not push `main`. Claude is a co-builder — do not freeze
them out of files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Closed vocab** `vocab/scene.enum.json`: roles `front_matter` /
  `procedure_a` / `form_br`. Title heuristic is the documented heading
  for that role (What an ALSAP is / How an ALSAP starts / Benefit-risk
  on the form), not outcome language.
- **Storage:** `spine.scenes` is the source of truth (ordered scene
  objects with `element_ids`), analogous to `manifest.checks`. Member
  occurrences carry `ext.scene`. In-scene checks are shape refs into
  `manifest.checks`. Projector **reads** that list to wrap/page. It
  does not re-discover scenes by if-atom-id.
- **Hosts:** no new `ele_`. Sequence_order stays in scene 2;
  closed_choice stays in scene 3; invert_definition extras stay
  lesson-end (not a fourth scene). Store stays 55 / 47. Spine 16.
  Paging from PR #26 stands.
- Idempotent realize → cartographer → couturier. Selftest: scene
  operands resolve from the graph, not hardcoded HTML. Cut from
  current main after PR #28.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, quiz engine, new agent, Procedure B,
inventing a `retrieve` enum, 1:many of the SOP, Dragoman, Storyline,
`.potx`, motion, PNG pipelines.
