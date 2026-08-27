# Realizer form-field present seed v1 — the field those examples fill

*A documented join from the lesson occurrence store to a sibling form
atom store — not a dump of FORM-AST-34037, and not a parallel meaning
atom.* Implemented by `tools/realize.py`. Policy id:
`v1_form_field_present_seed`. Extra records still stamp
`ext.realized_from.role: extra` (so Cartographer preserves Realizer-stamped
`move`) plus `form_store` / `form_spec` so the join is visible.

The instance beats already on the spine (`agents/realizer/instance_example_v1.md`)
are filled AST-34037 values. They do **not** illustrate Procedure A. This
hop puts **the form field those values fill** on the path first. Then:
here is the field, here is a filled one. Meaning stays on the form atom.
The ALSAP occurrence store mints an `ele_` whose `composed_from` is that
form `atom_id`. No authored `content.text`. `ast_alsap/atoms.json` and
`alsap/atoms.json` are untouched. Form atoms are not rewritten into SOP
atoms.

---

## Which form atoms, and why (honesty bar)

Live form store: `cgen/astellas/projects/alsap` (FORM-AST-34037). The two
instance examples already on the spine `composed_from` instance atoms whose
`bindings.instance.instantiates` is **exactly**:

| Form atom | Verbatim meaning | Instance example that fills it |
|---|---|---|
| `atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile` | *SMT assessment of the overall Benefit-Risk profile of the asset.* | `atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_profile` (`conditional_favorable`) |
| `atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale` | *Rationale and phrasing for the selected Benefit-Risk profile.* | `atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale` (authored SMT judgment; names ASP9999) |

That is a **meaning join**, not a cousin. The instance atom names the form
atom in `instantiates`. Do not stretch `f_br_guidance` (instructional
transient: *Choose from the options below…*) or the phrasing-example
section (`sec_br_phrasing` / per-option example sentences). Those are
not the fields the cited instance values fill. If those two field atoms
were missing, stop rather than pick a nearby form node.

Clothes: `move: present` → Couturier `brand.instructional` / `content_role:
body` / `layout_hint: card`. Compiler form is already `tp_body`. Kicker
**Present**. Not another SOP card. Not example/`cite` clothes (those stay
on the instance beats). Not the rest of the form.

**Not cited:** cover fields, narrative slots, BR option atoms, guidance,
phrasing examples. Dumping them onto the spine would be a form dump.

---

## How `composed_from` crosses stores

Lesson store is `ast_alsap`. Form store is `alsap`. The gate
`composed_from` must resolve to an atom that carries the meaning — not
“must live in *this* project’s `atoms.json`.”

Realizer / Cartographer / Couturier build a **meaning catalog**: SOP atoms
plus the sibling form store plus the sibling instance store, joined by
`atom_id`. They validate and project against that catalog. They do **not**
copy form records into `ast_alsap/atoms.json`. Coverage tree-walk still
uses only SOP atoms (form parents are not in this occurrence store;
mixing the form tree in would mint extra roots / dump the template).

Join is **ALSAP-lesson-only**: `project.name == "ast_alsap"` and sibling
`../alsap/atoms.json` exists. Other projects do not grow guest form
`ele_` records.

Stable extra ids stay `(primary ele_) + "__" + move`:

```
ele_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile__present
ele_form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale__present
```

No primary of those atoms is minted in the ALSAP occurrence store (this
store is not their home). They are extras so Cartographer keeps
Realizer-stamped `present`. Guest extras do not stamp `structure.parent_id`
at a form-section `ele_` that was never minted here.

---

## Spine membership

After Procedure A’s job-aid **and the sequence practice of those four
presents**, **before** the two instance-example beats, then the existing
reinforce checks. Spec: `agents/realizer/spine_v1.md`. Policy
`v1_front_matter_callout_procedure_sequence_form_example_then_checks`.

Order is **both fields, then both filled values** — not interleaved
inside the example pair. The two instance beats are already one worked
example (judgment name + reason). Inserting a second form-present between
them would split that example. Gagné-ish: here are the fields this form
asks for; here is a filled ALSAP.

Do not mint a procedure-step MCQ. Sequence practice is projector-only
(`agents/realizer/check_v1.md`). Scene 3 now also projects a closed-choice
of the BR profile fill from these two presents plus the instance pair
(same spec; no extra `ele_`). Do not 1:many the SOP. Do not dump the
form. Do not stand up Chameleon. Do not host `/cgen/alsap`.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Default project `cgen/astellas/projects/ast_alsap`. Open
`realized_lesson.html`. `--selftest` on all three.
