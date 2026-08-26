# Session note — 2026-08-26 atom → primitives

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to pay the owed atom →
primitives hop so the short lesson dresses compiler clothes (step, body,
check, heading) instead of dumping SOP sentences into styled cards. Open
a PR. Do not push `main`. Claude is a co-builder — do not freeze them
out of files or rewrite their canon. Do not spend this PR on Netlify /
`/cgen/alsap` hosting; Jake tabled the redirect loop.

Recorded in `DECISIONS.md`:

- **Closed compiler vocabulary** (`agents/realizer/primitives_v1.md`,
  policy `v1_atom_to_primitive`). Realizer binds `text_primitive` from
  atom kind + occurrence move. Registry v0.4 adds `tp_step` and
  `tp_callout`; heading/body/check reuse existing keys.
- **Spine projector uses those primitives.** Procedure A s1–s4 render as
  one job-aid step list. Front-matter as heading/body. Reinforce as the
  existing check. Coverage stays card-like.
- **Couturier still owns style.** It preserves `text_primitive` and
  dresses a step as `layout_hint: job_aid`. Cartographer refreshes the
  primitive after writing `move`.
- Idempotent with realize → cartographer → couturier. Store stays 50.
  `atoms.json` untouched. No authored `content.text`.

Out of scope this session: Netlify / `/cgen/alsap` hosting, distractor-
writer agent, Dragoman, Storyline, `.potx`, motion primitives,
`tools/render/` PNG pipelines, rewriting SOP/form atoms into elements,
inventing a `retrieve` enum, procedure-step MCQs, 1:many of the procedure
tree, procedure B/C on the spine.
