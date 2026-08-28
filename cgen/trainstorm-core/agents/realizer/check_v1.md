# Realizer check projection v1 — shapes on the graph

*Traditional ID’s third move is a check.* Couturier already dresses
`reinforce` as `brand.recall` / `tp_recall`. This spec is how a check is
**named on the occurrence store** and how the HTML projector **reads**
that record — not a new agent, not a second meaning store, not a new
pedagogical enum, not a quiz engine.

Implemented in `tools/realize.py`. Closed pedagogical vocab stays
`reinforce` (Gagné 9a). Do not invent `retrieve`. `practice` exists on the
closed list; this hop does **not** stamp it on a new `ele_`.

Question clothes are occurrence-level (`intent.move`, Couturier
`layout_hint: check`) **or** projector-only (sequence practice of existing
presents; closed-choice of existing form present + instance fill). **No authored
`content.text` on the element.** Prefer keys/refs over copying option
strings. Stem, key, distractors, sequence items, and closed value ids are
**resolved** from the graph at project time, from the stamped operands —
not invented in HTML.

Policy ids: `v1_check_from_atom` (honesty bar, unchanged) and
`v1_check_shapes_on_graph` (the shape is a first-class record).
Closed shape vocab: `vocab/check-shape.enum.json`.

---

## Three shapes (not three meanings)

Closed list. A later agent emits the same checks by writing the same
`shape` + operand refs. The projector does **not** re-discover pedagogy
by `if atom_id` / `if move == reinforce` / `if this is a job-aid`.

| Shape | When | Operands (refs) | What the learner does |
|---|---|---|---|
| `invert_definition` | Extra `reinforce` of a definitional atom that has `{subject} is {complement}` | `key_atom_id`, `contrast_atom_ids` (siblings), `host_element_id` | Invert-definition MCQ. Cloze is a **render** of this shape when `contrast_atom_ids` is empty — not a fourth shape. Was `mcq_siblings` / `cloze`. |
| `sequence_order` | A `procedure_step` group that already has `bindings.object.order` (Procedure A s1–s4) | `atom_ids`, `element_ids` of those presents, `order_from: bindings.object.order` | Order those first sentences. Was `sequence`. Projector-only: no extra `ele_`. |
| `closed_choice` | Form field with `options_ref` + instance fill of that field already on the spine (FORM-AST-34037 BR profile) | `options_ref`, `instance_atom_id`, `form_atom_id`, `key_from: bindings.instance.selected_value` | Pick the value already shown on the example. Options = verbatim value **ids** of the governed set. Key = instance `selected_value`. Learner-visible **labels** are a Realizer projection into the engine JSON (registry `label`, never `description`); they are not copied onto the element. Prompt is task clothes, not an SOP stem. Projector-only: no extra `ele_`. |

Where they live:

- **Occurrence store:** `ext.check` on invert-definition host `ele_` records
  (the two definition extras). `ext` is the sanctioned extension; do not put
  option labels on `element.assessment`.
- **Manifest:** `checks[]` is the index of every shape, including
  projector-only `sequence_order` and `closed_choice`. `spine.sequence_check`
  and `spine.br_profile_check` remain pointers (`see: checks`).

Cartographer still owns `intent` (`rhetorical`, `move`, `teaches`,
`intended_response`). Couturier still owns style. Realizer binds the
check shape, the way it binds `text_primitive`.

Definition checks stay invert-definition. Sequence is for procedure_step
groups that already have order — not a copula invert, and not “which is
the first planning step?” (that would invent a fact; PR #16 correctly
refused it). Closed-choice is for a **select_one** form field whose options
already live in the client registry and whose instance fill is already taught —
not “which BR profile is required?” and not LLM distractors. Jake parked a
distractor-writer; this hop does not build it. LLM distractors stay parked.

---

## Honesty bar (same as Amanuensis: no fabricated evidence)

**Definition checks (`invert_definition`; cloze is a render)**

- **Key** is a substring of *this* atom’s `meaning.source_text` (after the
  usual Headwater-note trim). If a candidate key is not in the atom, it is
  refused — never paraphrased into existence.
- **Stem** is a grammatical invert of this atom’s own first sentence
  (`{subject} is {complement}` → `What is {subject}?`). That is a question
  transform, not a new SOP fact, number, or rule.
- **Distractors**, if any, are first sentences of **sibling atoms in the
  same store** (same `belongs_to`). Verbatim. Closed contrast, not invented
  misconceptions.
- **Feedback** is learner task-clothes: correct names the wording from
  this definition (may quote the key already used as the correct choice —
  that string ⊆ the atom); incorrect says the other options are other
  sentences from this lesson, not this definition. Do not say atom /
  `ele_` / sibling store.
- If two usable siblings are not available, the shape falls back to a
  **cloze** of this atom’s first sentence (no distractors). Still a check
  the reader can attempt.
- Thin headings and glossary pointers are not used as siblings
  (`Roles and Responsibilities.`, `Procedures.`, `For definitions, refer…`).

**Sequence checks (`sequence_order`)**

- **Items** are the first sentences of the procedure_step atoms in the
  group (`atom_sop_ast29080_proc_a_s1` … `_s4`). Verbatim. Each item ⊆ that
  atom.
- **Correct order** is `bindings.object.order` of those atoms — the
  sequence already taught on the job aid. Not a new ranking.
- **Prompt** is task clothes, not an SOP stem: *Put these in the order
  already taught.* Do not author “Which is the first planning step?”
- **Feedback** is learner task-clothes projected by Realizer: correct
  names the order on the job aid already shown; incorrect points the
  learner back to that sequence. It does not say `object.order` / atoms,
  and it does not invent SOP facts (“the first planning step is…”).
- Initial display is a **stable non-identity permutation** so the learner
  can be wrong, then right.

**Closed-choice checks (`closed_choice`)**

- **Options** are the value **ids** of the governed set named by the form
  field’s `bindings.form.options_ref` (`reg_benefit_risk_profile` on
  FORM-AST-34037). Verbatim. The full set — not a cherry-picked pair, not
  phrasing-example cousin sentences, not registry `description` prose.
  Do not copy labels onto the element. The Course Engine projection (and
  the sidecar HTML) may **resolve** each id to that registry entry’s
  `label` for learner-visible text; if a label is missing, fall back to
  the id. Submitting still keys on the id.
- **Key** is the instance atom’s `bindings.instance.selected_value`, which
  the gate already requires to equal `meaning.source_text`. It must be a
  member of that set. Live fill: `conditional_favorable`. An id, never
  copied prose.
- **Prompt** is task clothes, not an SOP stem: *Choose the value already
  shown on the example.* Do not author “Which Benefit-Risk profile is
  required?” or “When should SMT select conditional_favorable?” Drop
  “closed” — that word is compiler-speak.
- **Feedback** is learner task-clothes: correct names the value already
  shown on the example; incorrect points the learner back to that
  example. It does not say “closed value set” / registry, and it does
  not invent SOP facts (“SMT should…”, rationale implications).
- **Host** is projector-only (`manifest.checks`). Composing from the
  instance extra would hide `options_ref`. Composing from the form field
  would hide `selected_value`. No extra minted.
- **Clothes on the JSON adapter.** Projector-only sequence and
  closed-choice components wear `meta.style_ref: brand.recall` in the
  disposable engine JSON so `/cgen` dresses them as recall checks. That
  is not minting an `ele_`, not writing `style_ref` onto a present
  occurrence, and not a new Couturier map row.
- Initial display is a **stable non-identity permutation** so the learner
  can be wrong, then right.
- The rationale field is `text_long` with no `options_ref`. It has **no
  honest closed set**. Do not MCQ it. Do not invent distractor rationales.

Shape is a key (`invert_definition` | `sequence_order` | `closed_choice`)
stored on the graph. Couturier still records `reinforce` surfaces as
`layout_hint: check`. Sequence practice and the BR closed-choice are
projector-only. Do not put option labels on `element.assessment`. Do not
bind `interaction_primitive` (Storyline; not this hop).

---

## Composition choice (Procedure A sequence) — mint nothing

Prefer one extra `ele_` with `move: reinforce` (or another closed-vocab
move; do not invent `retrieve`) *if* that extra can honestly
`composed_from` one atom.

**Composing from a single A step is a lie.** The check is the four
siblings’ order, not s1’s notify sentence. `composed_from` would claim
the occurrence realizes one atom while displaying four others’ meaning.

**Composing from the thin A heading (`atom_sop_ast29080_proc_a`, “A.
Plan Development of ALSAP.”) is also a lie.** That atom is skipped as a
teaching card. The extra would display children’s first sentences under
a parent `composed_from`. That duplicates no step atom, but it still
isn’t the heading’s meaning.

So: **mint nothing new.** Project the sequence check from the four
existing present `ele_` records (`ele_sop_ast29080_proc_a_s1` …
`_s4`) already on the spine as the job aid. Same honesty as grouping
those presents into one job-aid: projector clothes of existing
occurrences. Spine `element_ids` membership is unchanged (14). Manifest
stamps `spine.sequence_check.from_atom_ids` / `from_element_ids` so the
projection is documented. Store stays 53 / 47. `atoms.json` unchanged.

Closed vocab: no `retrieve`. Did not stamp `practice` on a fake extra
(that would still need a dishonest `composed_from`). The projector
kicker is **Practice** (Gagné 6 clothes of the job-aid presents).
Instance example stays `exemplify`, after this practice.

---

## Composition choice (FORM-AST-34037 BR profile) — mint nothing

Prefer one extra `ele_` with `move: reinforce` *if* that extra can honestly
`composed_from` one atom.

**Composing from the instance fill alone is a half-lie.** The key *is*
that atom’s `selected_value`. The options are **not** — they live on the
form field’s `options_ref` (`reg_benefit_risk_profile`). An extra of the
instance would display a value set it does not own.

**Composing from the form field alone is also a half-lie.** The field
atom’s meaning is *SMT assessment of the overall Benefit-Risk profile of
the asset.* The key is the ASP-9999 fill, not that sentence.

So: **mint nothing new.** Project the closed-choice from the two existing
guest `ele_` records already on the spine (form present + instance
exemplify). Same honesty as the sequence practice. Manifest stamps
`spine.br_profile_check`. Store stays **55 / 47**. Spine membership 16.
`atoms.json` unchanged. The projector kicker is **Practice**. Lives in
scene 3 (Benefit-risk on the form), after the field+example, before
lesson-end definition checks.

If the form field had no `options_ref`, or the instance fill were not a
member of that set, **stop** rather than stretch phrasing-example cousins
or invent a seventh value.

---

## What is seeded to *have* a definition check

The 1:many seed (`one_to_many_v1.md`) mints extra `reinforce` occurrences.
This hop keeps the ALSAP definition extra and the purpose extra — still a
seed, not the whole SOP. Sequence practice and the BR closed-choice do
**not** add a seed row.

| Extra `ele_` | Atom | Primary move | Why this atom is worth a check |
|---|---|---|---|
| `ele_sop_ast29080_general__reinforce` | `atom_sop_ast29080_general` | `present` | What an ALSAP *is* |
| `ele_sop_ast29080_purpose__reinforce` | `atom_sop_ast29080_purpose` | `objective` | What this SOP is *for* |

Title extra stays `present` (hook + present). It is not a check.

---

## Worked derivation (so Jake can see nothing was invented)

Live store, first sentences (verbatim from `atoms.json`):

**`atom_sop_ast29080_general`**
> The ALSAP is the central cross-functional framework for ongoing
> identification, evaluation, and communication of emerging safety risks
> at the asset level.

- Subject → stem: **What is the ALSAP?**
- Complement → **key:** the central cross-functional framework for ongoing
  identification, evaluation, and communication of emerging safety risks
  at the asset level.
- Sibling distractors (same parent `atom_sop_ast29080`, usable meaning):
  - `atom_sop_ast29080_purpose` first sentence (the SOP’s purpose — closed
    contrast with what the ALSAP *is*)
  - `atom_sop_ast29080_scope` first sentence (who the SOP *applies to*)

The rest of the general atom (one-per-asset, ALCOA+, annual SMT review)
is **not** turned into extra claims. It remains on the atom; the `present`
occurrence still shows it. The check tests the definitional first sentence.

**`atom_sop_ast29080_purpose`**
> The purpose of this SOP is to define the process for planning,
> developing, executing, maintaining, and archiving the Asset Level Safety
> Assessment Plan (ALSAP) for use in asset-level safety monitoring during
> clinical development.

- Stem: **What is the purpose of this SOP?**
- Key: the complement after `is` (verbatim).
- Distractors: first sentences of `general` and `scope` (siblings).

**Procedure A sequence** (`atom_sop_ast29080_proc_a_s1` … `_s4`)

Items (verbatim first sentences; `object.order` 0–3):

1. Notify a member of Safety Data Science in QSEG of the need for an ALSAP and request an ALSAP Lead.
2. Collaborate with SMT to identify contributing authors and reviewers.
3. Schedule and conduct the ALSAP Kick-Off Meeting within 15 business days of ALSAP Lead assignment.
4. Collaborate with contributing authors and confirm alignment on section deliverables and target dates.

Prompt (clothes, not a fact): **Put these in the order already taught.**
Correct order = those four `object.order` values. Not “which is the first
planning step?”

**FORM-AST-34037 BR profile closed-choice**

Form field: `atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile`
(`options_ref`: `reg_benefit_risk_profile`).

Instance fill: `atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_profile`
(`selected_value` / `source_text`: `conditional_favorable`).

Options (verbatim registry ids, full set):

1. `favorable`
2. `unfavorable`
3. `uncertain_inconclusive`
4. `conditional_favorable` ← key
5. `contextual`
6. `other_smt_defined`

Prompt (clothes, not a fact): **Choose the value already shown on the example.**
Not “which BR profile is required?” Rationale has no closed set — not
this check. Shape + operand refs live on `manifest.checks`. Learner-
visible choice text is the registry `label` for each id, projected into
the engine JSON / sidecar — not stored on the element.

---

## Who writes what

| Agent | Still owns | This hop |
|---|---|---|
| Realizer | `ele_` ids; HTML projection; compiler `text_primitive` | Binds `ext.check` + `manifest.checks` (shape + operand refs). Projector **reads** those records to render invert-definition, sequence_order, and closed_choice. Learner-facing check copy (stems/prompts already on the graph operands; feedback; closed-choice display labels) is this projector. Projector-only checks may wear `brand.recall` on the engine JSON adapter. |
| Cartographer | occurrence intent | Does not mint `practice`/`assess`; extra `reinforce` move stays Realizer-stamped; A-step primaries stay `present`; form/instance extras keep Realizer-stamped `present` / `exemplify`. Does not wipe `ext.check` or `ext.scene`. |
| Couturier | expression style keys | `layout_hint` for `reinforce` is `check`; still `brand.recall` / `tp_recall`. Sequence practice and BR closed-choice are projector clothes of existing beats. Couturier.py / `style_map_v1.md` unchanged. |

Re-running realize → cartographer → couturier keeps extra `ele_` ids,
intent, style, and the same check records (pure function of store +
move + object.order + options_ref / selected_value).

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Optional: `python3 tools/realize.py --selftest` (includes the honesty bar).

The short lesson path that *uses* these checks is Realizer projection
(`agents/realizer/spine_v1.md`). Sequence practice sits after the job aid
and before the form presents (Gagné-ish: practice the steps near the
job aid). BR closed-choice sits in scene 3 after the field+example.
Definition checks stay at the end. Optional:
`python3 tools/realize.py --selftest` asserts a check’s operands resolve
from the graph (not hardcoded HTML).
