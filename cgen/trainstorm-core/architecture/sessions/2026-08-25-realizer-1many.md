# Session note — 2026-08-25 Realizer 1:many seed

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to prove 1:many in the live occurrence store:
mint extra `ele_` records so a couple of teaching-worthy ALSAP atoms appear more than once
with different moves, without duplicating atoms or authored meaning. Open a PR. Do not push
`main`. Claude is a co-builder — do not freeze them out of files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Realizer 1:many seed** (`tools/realize.py`, `agents/realizer/one_to_many_v1.md`). Two
  atoms only: title (`hook` + `present`) and the ALSAP definition (`present` + `reinforce`).
  Extra ids are stable. Re-run does not wipe extras or Cartographer intent.
- **Cartographer** stays the intent writer on re-run, except extra `move` is preserved
  (Realizer stamped it). `teaches` / rest of intent still bind. HTML groups same
  `composed_from`.
- `atoms.json` unchanged. No authored `content.text` on occurrences. Not a full SOP
  treatment. Couturier still unbuilt.

Out of scope this session: Couturier, Dragoman, Storyline, `.potx`, `tools/render/` PNG
pipelines, rewriting SOP/form atoms into elements, inventing a `retrieve` enum value.
