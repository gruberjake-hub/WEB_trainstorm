# Realizer lesson spine v1 — short path, full dump as coverage

*A documented selection/sequence of existing occurrences — not fake instructional-design
genius, and not an LLM call.* Implemented by `tools/realize.py`. Policy id:
`v1_front_matter_callout_procedure_sequence_form_example_then_checks` (extends the
earlier `v1_front_matter_callout_procedure_sequence_example_then_checks`
membership: that hop put two instance-example beats after Procedure A;
this hop puts **the form fields those examples fill** immediately before
them). Spec path stamped on the occurrence manifest as `spine.spec`.

The live ALSAP hop already minted `ele_` records, bound `move`/`teaches`
(Cartographer), dressed them (Couturier), bound compiler primitives, put
`tp_callout` on purpose, and projected Procedure A as a job-aid. The job
aid is **how**. The instance is **that it happened** — two guest `ele_`
records whose `composed_from` is an instance `atom_id` from `alsap_asp9999`
(`agents/realizer/instance_example_v1.md`). Those beats are filled
FORM-AST-34037 values; they do not illustrate A. This hop puts **the
field**: two guest `ele_` records whose `composed_from` is a form `atom_id`
from `alsap` (`agents/realizer/form_field_present_v1.md`). Then: here is
the field, here is a filled one. Not B/C. The dump stays coverage.

Realizer owns the projection. Cartographer still owns intent. Couturier still
owns style. Spine **mints no `ele_` ids for membership** (form-present and
instance-example extras are minted by their seeds, then selected) and
**drops none**. `atoms.json` (SOP, form, and instance) is untouched. Locale
packs stay keyed on `atom_id`. Closed vocab still has no `retrieve`; extra
`reinforce` stays a check (`agents/realizer/check_v1.md`). Procedure A’s
four presents also project a **sequence** practice (order those first
sentences; object.order) immediately after the job aid, before the form
presents. That practice mints no `ele_`. Scene 3’s form present + instance
fill also project a **closed_choice** of the BR profile (options_ref value
ids; key = instance `selected_value`). That practice mints no `ele_`.

---

## Why not walk Cartographer's object graph as the path

`bindings.object.belongs_to` + `order` is the SOP tree. Walking it *is* the 47
card dump. It does not imply a short lesson. Spine v1 **reuses those roles as
input** (root vs direct child vs descendant; sibling `order`) and then **selects
a subset**, sequenced as opening → why-this callout of purpose → front-matter
teaching cards → Procedure A job sequence → sequence practice of those
presents → form BR-field presents → instance examples → existing definition
checks.

The Cartographer object tree already lists Procedure A’s children in `order`.
The selector takes those non-heading children — it does not invent a parallel
parent/sequence on the element. Do not mint a pile of new 1:many. Do not call
a model to pick the path. Do not 1:many the procedure tree.

---

## Which procedure, and why

Live ALSAP (`cgen/astellas/projects/ast_alsap`) has three procedure branches
under the thin heading `Procedures.`:

| Branch | Heading (thin — not a teaching card) | What it is |
|---|---|---|
| First in `object.order` | `A. Plan Development of ALSAP.` | How an ALSAP *starts* |
| Second | `B. Develop and Maintain ALSAP.` | Draft / maintain the living plan |
| Third | `C. Develop Analysis Datasets and TLFs.` | Programmer outputs |

**Pick: Procedure A.** It is the first real work in `object.order`. After the
front-matter has said what an ALSAP is and who it applies to, an ID teaching
*Plan Development of ALSAP* would walk the real A steps — you cannot
develop/maintain (B) or produce datasets (C) until a Lead is requested and
the kick-off has happened. The heading atom is thin (`< 50` chars, same bar
as check-sibling rejection).

A is a handful of real steps (four `procedure_step` children). Take **all of
them**, present only, in `object.order`:

| Atom | First sentence (the job) |
|---|---|
| `atom_sop_ast29080_proc_a_s1` | Notify a member of Safety Data Science in QSEG of the need for an ALSAP and request an ALSAP Lead. |
| `atom_sop_ast29080_proc_a_s2` | Collaborate with SMT to identify contributing authors and reviewers. |
| `atom_sop_ast29080_proc_a_s3` | Schedule and conduct the ALSAP Kick-Off Meeting within 15 business days of ALSAP Lead assignment. |
| `atom_sop_ast29080_proc_a_s4` | Collaborate with contributing authors and confirm alignment on section deliverables and target dates. |

Cap is `PROCEDURE_SEQUENCE_CAP = 8` — enough for a handful, truncates only if
A were huge. Live A (4) is under the cap, so all four land. Branches B/C stay
coverage. Not the whole SOP.

---

## Why no extra `ele_` on those atoms (sequence practice is projector-only)

A copula-invert sibling MCQ is still impossible: Procedure-step atoms are
**imperatives** (*Notify…*, *Collaborate…*, *Schedule…*). `derive_check`
cannot invert `{subject} is {complement}`. A stem such as “Which is the
first planning step?” would invent a fact (PR #16 refused it). Jake parked
a distractor-writer.

A **sequence** check *is* honest: items are those four first sentences;
correct order is `bindings.object.order` (already taught on the job aid).
See `agents/realizer/check_v1.md`.

**Do not mint an extra for it.** Composing from s1 (or any one A step) is
a lie — the check is the four siblings. Composing from the thin A heading
is also a lie (that atom is skipped as a teaching card). Project the
check from the four existing present `ele_` records, same honesty as the
job-aid grouping. `supports_honest_sibling_check` stays False for every A
step (that gate is the invert-definition MCQ). Guest extras this hop
does not mint: the two form **present** beats and the two instance
**exemplify** beats remain from their seeds.

The projector kicker is **Practice**. Closed vocab still has no
`retrieve`. Did not stamp `practice` on a fake extra.

---

## Membership (which atoms, which occurrences)

**On the path**

| Role | Which atoms | Which `ele_` | Why |
|---|---|---|---|
| Opening | Document root: no `belongs_to` | Primary (`hook` once Cartographer has bound it) then the seeded extra `present` if it exists | Title hook + title present — already seeded on `atom_sop_ast29080` |
| Why-this callout | Purpose atom `atom_sop_ast29080_purpose` | Seeded extra `activate` (`ele_sop_ast29080_purpose__activate`) | Verified why-this meaning (SOP purpose sentence). Clothes: `tp_callout`. Not invented text. Not the title atom. |
| Front-matter teaching cards | Direct children of the root, `kind` in `procedure` / `form`, **not thin** | Primary occurrence only | Paragraphs an ID would actually say: purpose (objective / `tp_purpose`), scope, what-it-is. Sorted by `object.order`. |
| Procedure A job sequence | First Procedures-container branch in `object.order`; skip thin A/B/C heading; take every non-thin `procedure_step` child (`PROCEDURE_SEQUENCE_CAP = 8`) | Primary occurrence only | Doing the work: Plan Development’s four real steps, in `object.order`. Not B/C. |
| Sequence practice | Same four A-step atoms | **No new `ele_`.** Projector-only check of the four presents (`shape: sequence_order` on `manifest.checks`) | Gagné-ish: practice the steps near the job aid. Items = first sentences. Order = `object.order`. Form presents then instance examples follow. |
| Form BR present | The two FORM-AST-34037 field atoms those instance values `instantiates` (see `form_field_present_v1.md`) | Guest extras `…__present` | Honest referent of the two instance examples already on the spine: BR profile field + rationale field. `composed_from` is the form `atom_id`. Clothes: `present` / `brand.instructional` / `tp_body`. Not a form dump. Not `f_br_guidance` or phrasing-example cousins. |
| Worked example | Two instance atoms from sibling `alsap_asp9999` (see `instance_example_v1.md`) | Guest extras `…__exemplify` | **Procedure A has no honest match** in the instance store (plan-development acts vs filled AST-34037 values). These two illustrate the ALSAP generally: selected BR profile `conditional_favorable` + the authored rationale. `composed_from` is the instance `atom_id`. Clothes: `exemplify` / `brand.example` / `tp_body`. Not another SOP card. Not the other eight instance atoms. Sit **after** the form-field presents. |
| BR profile closed-choice | Same form field + instance fill already on the spine | **No new `ele_`.** Projector-only check (`shape: closed_choice` on `manifest.checks`) | Options = `reg_benefit_risk_profile` value ids. Key = instance `selected_value` (`conditional_favorable`). Prompt is task clothes. In-scene 3, after the field+example. Rationale has no closed set — not this check. Closed shapes: `vocab/check-shape.enum.json`. |
| Checks | Spine atoms that already have an extra `reinforce` | Those extras, in the same atom order as their presents | Reuse the two existing definition checks (`invert_definition` on `ext.check`). Do not mint a procedure-step MCQ. |

**Off the path (coverage, not deleted)**

- Thin headings and glossary pointers (`Roles and Responsibilities.`,
  `Procedures.`, `A. Plan Development of ALSAP.`, `B.…`, `C.…`,
  `For definitions, refer…`) — same bar as check-sibling rejection in
  `check_v1.md`.
- Other descendants: lists, list items, procedure B/C steps, govdocs.
- Any 1:1 leftover whose atom is not front-matter or a Procedure A step.

Live ALSAP therefore yields **sixteen** occurrences, in this order:

1. `ele_sop_ast29080` — hook (title)
2. `ele_sop_ast29080__present` — present extra of the title
3. `ele_sop_ast29080_purpose__activate` — callout (why this SOP; same atom)
4. `ele_sop_ast29080_purpose` — objective (purpose-frame of the same atom)
5. `ele_sop_ast29080_scope` — present (who it applies to)
6. `ele_sop_ast29080_general` — present (what an ALSAP is)
7. `ele_sop_ast29080_proc_a_s1` — present (notify / request Lead)
8. `ele_sop_ast29080_proc_a_s2` — present (identify authors and reviewers)
9. `ele_sop_ast29080_proc_a_s3` — present (15-day kick-off)
10. `ele_sop_ast29080_proc_a_s4` — present (confirm deliverables and dates)
11. `ele_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile__present` — present (BR profile field)
12. `ele_form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale__present` — present (BR rationale field)
13. `ele_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_profile__exemplify` — example (selected BR profile)
14. `ele_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale__exemplify` — example (authored rationale)
15. `ele_sop_ast29080_purpose__reinforce` — check
16. `ele_sop_ast29080_general__reinforce` — check

Teachable order is Gagné-shaped and small: gain attention → why-this
callout → say the thing (purpose-frame / who / what) → walk the Plan
Development job sequence → practice that order (projector-only sequence
check) → present the form fields those examples fill → show a filled
ALSAP (instance, `exemplify`) → enhance retention with the two existing
definition checks.
The sequence practice sits **after** the job aid and **before** the form
presents. Form presents sit **before** the instance example pair (not
interleaved: those two beats are one worked example). Definition checks
stay at the end. Not the 20 procedure steps of A+B+C. Purpose is three
clothes of one atom (activate + objective + reinforce).

---

## Scenes (first-class on the graph)

Membership above is unchanged. Scene records live on `spine.scenes`
(source of truth, analogous to `manifest.checks`) with ordered `ele_`
refs and optional in-scene check-shape refs. Spec:
`agents/realizer/scenes_v1.md`. Policy ids: `v1_three_scenes_from_roles`
(the grouping heuristic) and `v1_scenes_on_graph` (the record). Closed
role vocab: `vocab/scene.enum.json`. Not new beats. Not new atoms. Not
a new `ele_`. Not an LLM. Not invented outcome language (“will be able
to…”).

The projector **reads the selected lesson node** (`manifest.lessons`,
spec `agents/realizer/lesson_v1.md`), then those `spine.scenes` records,
to wrap and page. It does not assume “the ALSAP lesson is these three
headings.” `--lesson` (or the project default) selects the record.

Heuristic — SOP/form roles already used for membership:

| Scene | Role | Heading | Kicker | Which existing beats |
|---|---|---|---|---|
| 1 | `front_matter` | **What an ALSAP is** | Front matter | Document-root opening, why-this callout of purpose, teachable front-matter primaries (purpose / scope / general) |
| 2 | `procedure_a` | **How an ALSAP starts** | Procedure A | Procedure A job-aid presents (`tp_step`). The projector-only sequence practice stays **in-scene** (it is practice of those presents). |
| 3 | `form_br` | **Benefit-risk on the form** | Form | FORM-AST-34037 BR-field presents + the instance examples that instantiate those fields. The projector-only closed-choice of the profile fill stays **in-scene**. |

Headings are the documented labels of those role clusters. Scene 2’s
first-procedure branch already has the thin parent *A. Plan Development
of ALSAP.* (job-aid title). Scene 3’s field atoms already say
*Benefit-Risk profile*. Scene 1 is the SOP’s definitional front-matter.
Do not mint a fourth scene for the two definition/purpose checks —
they stay at **lesson end** (`spine.scenes.lesson_end_checks`) unless a
check clearly belongs in-scene (the sequence practice does; the BR
closed-choice does).

Coverage dump stays ungrouped (no scene chrome).

---

## Player chrome (one scene at a time)

Membership and the three named scenes are unchanged. The projector then
**pages those same `spine.scenes` records** so `realized_lesson.html`
shows one named scene at a time. Policy id: `v1_one_scene_at_a_time`,
stamped as `spine.scenes.paging`. Next / Back (or equivalent) moves
between the three scenes. Not new beats. Not new atoms. Not a new `ele_`.
Not an LLM. Section titles stay the headings on the scene records.

Definition/purpose checks are **not a fourth scene**. They stay at lesson
end (`spine.scenes.lesson_end_checks`) and are a **final player step**
after the last named scene (Next from scene 3). Back from that step
returns to scene 3. Sequence practice stays in scene 2 and still works
when that scene is shown.

Hash (`#what_an_alsap_is`, `#how_an_alsap_starts`,
`#benefit_risk_on_the_form`, `#lesson-end`) is optional.

A lesson whose `scene_ids` are a single scene and whose
`lesson_end_check_ids` are empty is still `v1_one_scene_at_a_time`:
the projector suppresses Next/Back (pager disabled) because there is
nowhere to page. Live: `ast_alsap_br` → `realized_lesson_br.html`.

Coverage dump stays unpaged (no player chrome).

---

## What is written

Occurrence manifest `spine`:

```json
{
  "policy": "v1_front_matter_callout_procedure_sequence_form_example_then_checks",
  "spec": "agents/realizer/spine_v1.md",
  "element_ids": ["ele_sop_ast29080", "ele_sop_ast29080__present", "ele_sop_ast29080_purpose__activate", "…"],
  "count": 16,
  "store_count": 55,
  "note": "Selection of existing ele_ records. Coverage dump keeps the rest. Sequence practice of Procedure A is projector-only (spine.sequence_check). Form BR presents then instance examples then a projector-only closed-choice of the profile fill (spine.br_profile_check). Scene records (spine.scenes) are first-class ordered groupings of those same ids. Player chrome (spine.scenes.paging) shows one named scene at a time; lesson-end checks are a final step, not a fourth scene."
}
```

Ids are stable. A re-run of realize → cartographer → couturier recomputes the
same list from the same heuristic (pure function of atoms + occurrences). It
does not drop extras, Cartographer intent, or Couturier style.

HTML (Realizer projector):

| File | Default experience |
|---|---|
| `<project>/realized_lesson.html` | A **read of the lesson node** (`manifest.lessons`, default `{project}_short`): the spine, in the order above, wrapped as **three named scenes** read from that lesson’s `scene_ids` → `spine.scenes` (What an ALSAP is / How an ALSAP starts / Benefit-risk on the form), **one scene at a time** (Next/Back). Title heuristic is the document-root atom. Title hook (heading primitive), why-this callout (`tp_callout` of purpose), front-matter (body/purpose), Procedure A as **one job-aid step sequence** (`tp_step`), a **sequence practice** of those four presents (order the first sentences; in-scene), two form-field presents (`present` / `tp_body`), two example beats (`exemplify` / `brand.example` / `tp_body`), a **closed-choice** of the BR profile fill (in-scene 3), two definition checks (`tp_recall`) at lesson end (final player step, not a fourth scene). Link to coverage. |
| `<project>/realized_lesson_br.html` | A **read of** `ast_alsap_br`: the same form BR scene (`benefit_risk_on_the_form`) — presents + instance examples + in-scene closed-choice. One scene, pager disabled (single step). Invert-definition extras stay on the short lesson. Path is derived from `lesson_id`; `realize.py` is not forked for ALSAP. Same title heuristic (document-root atom). |
| `<project>/realized_coverage.html` | Full occurrence dump in SOP document order — still card-like. Link back to the default short lesson. Not a third lesson node. |

Compiler primitives (`agents/realizer/primitives_v1.md`) are Realizer-owned
on the occurrence. The projector *uses* those primitives — callout, heading,
body, step list, check — instead of dumping every beat into a generic card.
The form-field presents reuse **body** + Couturier’s existing **present**
look. The instance beats reuse **body** + Couturier’s existing **example**
look. Not a sixth compiler role.

Do not hide coverage by deleting `ele_` records. The store stays 55
(51 SOP-side + 2 guest form extras + 2 guest instance extras).

---

## What this is not

- Not an ID genius and not an LLM path-picker.
- Not a distractor-writer. Definition checks keep closed-contrast distractors from sibling
  atoms (verbatim). Sequence practice uses the four A first sentences and
  `object.order`. BR closed-choice uses the form field’s `options_ref` value
  ids and the instance `selected_value`. Jake parked a future distractor-writer agent. This hop
  does not mint a procedure-step MCQ and does not invent “which is the first
  planning step?” or “which BR profile is required?”
- Not a new `retrieve` enum. No extra `ele_` for Procedure A. Not 1:many
  of the SOP.
- Not Dragoman, Storyline, `.potx`, motion, or `tools/render/` PNG pipelines.
- Not Cartographer writing sequence; not Couturier picking clothes from the
  spine. Clothes still follow `move`. Realizer binds compiler primitives;
  Couturier still owns `style_ref`.
- Not procedure B/C and not a full SOP dump.
- Not Chameleon and not `audience` keys on the store. Not Netlify /
  `/cgen/alsap` hosting (Jake tabled the redirect loop).
- Not rewriting instance or form atoms into SOP atoms. Not dumping all
  ten instance atoms or the whole FORM-AST-34037 onto the spine. Not
  inventing a Procedure A match that the instance store does not contain.
  Not stretching a cousin form field (`f_br_guidance`, phrasing examples)
  if the honest `instantiates` target were missing.
- Not new scene meaning, not a fourth scene of outcomes, and not a
  one-off HTML edit. Scene records are first-class on `spine.scenes` /
  `ext.scene`. A lesson record on `manifest.lessons` points at that list.
  Player chrome pages the selected lesson’s scenes one at a time; it
  does not mint a fourth scene. Coverage dump is a second projection,
  not a second lesson node.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Default project is `cgen/astellas/projects/ast_alsap`. Open
`cgen/astellas/projects/ast_alsap/realized_lesson.html` for the short lesson;
`realized_lesson_br.html` for the BR subset (`--lesson ast_alsap_br`);
`realized_coverage.html` for the full SOP dump. (Public `/cgen/alsap` rewrite
exists from an earlier hop; Jake tabled that redirect loop — the buried
projector path is the demo URL this hop uses.)
