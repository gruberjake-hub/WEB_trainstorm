# Realizer instance-example seed v1 — one worked example on the short lesson

*A documented join from the lesson occurrence store to a sibling instance
atom store — not a dump of every filled field, and not a parallel meaning
atom.* Implemented by `tools/realize.py`. Policy id:
`v1_instance_example_seed`. Extra records still stamp
`ext.realized_from.role: extra` (so Cartographer preserves Realizer-stamped
`move`) plus `instance_store` / `instance_spec` so the join is visible.

The job aid is **how**. The instance is **that it happened**. Meaning stays
on the instance atom. The ALSAP occurrence store mints an `ele_` whose
`composed_from` is that instance `atom_id`. No authored `content.text`.
`ast_alsap/atoms.json` is untouched. Instance atoms are not rewritten into
SOP atoms.

---

## Which instance atoms, and why

Live instance store: `cgen/astellas/projects/alsap_asp9999` (fictional
ASP-9999; the store’s own manifest says so). Ten `instance_value` atoms.
This hop cites **two**.

**Procedure A has no honest match.** A’s four steps are process actions
(notify SDS / request a Lead; identify authors and reviewers; kick-off
within 15 business days; confirm deliverables and dates). None of the ten
instance atoms describe those acts. They are filled AST-34037 form values
(cover + purpose/safety-profile). Citing them as “this is step 1 of Plan
Development” would invent a fact. Amanuensis honesty bar: do not.

They **do** illustrate the ALSAP **generally** — that an ALSAP happened for
this asset. The two richest “it happened” atoms in Purpose / Safety Profile:

| Atom | Meaning (verbatim) | Why this beat |
|---|---|---|
| `atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_profile` | `conditional_favorable` | The SMT’s selected benefit-risk conclusion on this ALSAP. |
| `atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale` | *The benefit-risk profile of ASP9999 is favorable provided the additional hepatic monitoring…* (full sentence on the atom) | The authored judgment that makes the selection a worked example, not a coded stub. Names ASP-9999. |

Together: the judgment name + the reason. One worked example, two beats.
Clothes: `move: exemplify` → Couturier `brand.example` / `content_role:
example` / `layout_hint: cite`. Compiler form is already `tp_body` (closed
set; primitives have body/callout/step — this is body, not a new SOP card
and not a sixth compiler role).

**Not cited** (the other eight): cover asset code / version / author
(metadata; the rationale already names ASP9999); duplicate narrative
`asset_code`; participant count `412`; prevalent AEs; SAEs. Those are
real instance values. Dumping them onto the spine would be a form dump,
not a worked example. Do not mint primaries for all ten.

---

## How `composed_from` crosses stores

Lesson store is `ast_alsap`. Instance store is `alsap_asp9999`. The gate
`composed_from` must resolve to an atom that carries the meaning — not
“must live in *this* project’s `atoms.json`.”

Realizer / Cartographer / Couturier build a **meaning catalog**: SOP atoms
plus the sibling instance store, joined by `atom_id`. They validate and
project against that catalog. They do **not** copy instance records into
`ast_alsap/atoms.json`. Coverage tree-walk still uses only SOP atoms
(instance atoms have no `belongs_to`; mixing them in would mint extra
roots).

Join is **ALSAP-lesson-only**: `project.name == "ast_alsap"` and sibling
`../alsap_asp9999/atoms.json` exists. Other projects do not grow guest
`ele_` records.

Stable extra ids stay `(primary ele_) + "__" + move`:

```
ele_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_profile__exemplify
ele_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale__exemplify
```

No primary of those atoms is minted in the ALSAP occurrence store (this
store is not their home). They are extras so Cartographer keeps
Realizer-stamped `exemplify` (an unbound instance_value with no
`belongs_to` would otherwise classify as `hook`).

---

## Spine membership

After Procedure A’s job-aid, before the two existing reinforce checks.
Spec: `agents/realizer/spine_v1.md`. Policy
`v1_front_matter_callout_procedure_sequence_example_then_checks`.

Do not mint a procedure-step MCQ. Do not 1:many the SOP. Do not stand up
Chameleon. Do not host `/cgen/alsap`.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Default project `cgen/astellas/projects/ast_alsap`. Open
`realized_lesson.html`. `--selftest` on all three.
