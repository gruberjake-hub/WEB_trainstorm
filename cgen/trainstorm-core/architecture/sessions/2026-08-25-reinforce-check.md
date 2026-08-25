# Session note — 2026-08-25 Extra reinforce as a check

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to make 1:many’s extra
occurrence actually instruct: after Couturier v1 the extra `reinforce` on the
ALSAP definition still read as a Remember recap of the same paragraph.
Traditional ID’s third move is a check. Open a PR. Do not push `main`.
Claude is a co-builder — do not freeze them out of files or rewrite their
canon.

Recorded in `DECISIONS.md`:

- **Check projection** (`tools/realize.py`, `agents/realizer/check_v1.md`).
  Extra `reinforce` (closed vocab; no `retrieve`) renders as a stem + choices
  or cloze derived from the atom via `composed_from`. No authored
  `content.text`. Key is in this atom; distractors are sibling atoms in the
  same store.
- **One more seed atom** (`atom_sop_ast29080_purpose`) so there are two real
  checks. Not the whole SOP. Title extra stays `present`.
- **Couturier** `layout_hint` for `reinforce` is `check` (was `recap`).
  Still `brand.recall` / `tp_recall`. Cartographer still owns intent.
- Idempotent: re-run realize → cartographer → couturier keeps extra `ele_`
  ids, intent, style, and the check projection.

Out of scope this session: Dragoman, Storyline, `.potx`, motion primitives,
`tools/render/` PNG pipelines, rewriting SOP/form atoms into elements,
inventing a `retrieve` enum value.
