# Session note — 2026-08-26 form BR-field present before instance examples

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to put a short present of
the form field(s) the two ASP-9999 instance examples fill, from existing
`alsap` form atoms (FORM-AST-34037), on the spine **before** those
instance examples. Then: here is the field, here is a filled one. SOP-
course mode. No invented text. Open a PR. Do not push `main`. Claude is
a co-builder — do not freeze them out of files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Honest referent.** The two instance examples instantiate exactly
  `atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile` and
  `atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale`.
  Not `f_br_guidance`. Not phrasing-example cousins.
- **Cross-store join.** Guest `ele_` records in the ALSAP occurrence
  store `composed_from` those form `atom_id`s. Meaning catalog joins
  SOP + form + instance. `ast_alsap/atoms.json` and `alsap/atoms.json`
  untouched. Clothes: existing `present` / `brand.instructional` /
  `tp_body`. Not another SOP card. Not a form dump.
- Placement: after Procedure A sequence practice, **before** the
  instance pair (not interleaved — that pair is one worked example).
  Store 55 / 47. Spine 16. No authored `content.text`. No procedure-
  step MCQ.

Out of scope this session: chameleon.py, audience variants, LLM
distractors, procedure-step MCQ, `/cgen/alsap` hosting, Headwater
outcomes-mode, Dragoman, Storyline, `.potx`, motion, PNG pipelines,
procedure B/C on the spine, inventing a `retrieve` enum, dumping the
form.
