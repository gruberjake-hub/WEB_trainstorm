# Session note — 2026-08-27 Check shapes on the graph

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to make the three honest
ALSAP check kinds **first-class on the graph** so a later agent can emit
the same checks without special-casing `realize.py`. No new beats. No
Procedure B. Same 16 spine occurrences. Same paging. `atoms.json`
unchanged. No authored `content.text`. Open a PR. Do not push `main`.
Claude is a co-builder — do not freeze them out of files or rewrite
their canon.

Recorded in `DECISIONS.md`:

- **Closed vocab** `vocab/check-shape.enum.json`: `invert_definition`,
  `sequence_order`, `closed_choice`. Operands are refs (atoms / `ele_` /
  `options_ref` / `object.order`), not copied option strings.
- **Storage:** `ext.check` on host occurrences; `manifest.checks` is the
  index (sequence_order stays projector-only). Projector **reads** the
  shape. It does not re-discover pedagogy by if-atom-id.
- **Hosts:** definition extras keep invert_definition; Procedure A
  sequence_order still mints no extra `ele_`; closed_choice is
  projector-only of the existing form present + instance fill
  (`selected_value` + `reg_benefit_risk_profile` value ids; task-clothes
  prompt). Store stays 55 / 47. Spine 16. Paging from PR #26 stands.
- Idempotent realize → cartographer → couturier. Selftest: operands
  resolve from the graph, not hardcoded HTML. Wrong then right on all
  three kinds. Rebased onto main after PR #26 (scene paging) and PR #27
  (projector-only BR closed-choice).

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, quiz engine, new agent, Procedure B,
inventing a `retrieve` enum, 1:many of the SOP, Dragoman, Storyline,
`.potx`, motion, PNG pipelines.
