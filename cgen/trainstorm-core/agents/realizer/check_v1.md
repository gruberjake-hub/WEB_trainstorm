# Realizer check projection v1 — `reinforce` as a check, not a recap

*Traditional ID’s third move is a check.* Couturier already dresses
`reinforce` as `brand.recall` / `tp_recall`. This spec is how the HTML
projector **renders** a check from atom meaning — not a new agent, not a
second meaning store, not a new pedagogical enum.

Implemented in `tools/realize.py` (`derive_check`, `derive_sequence_check`,
`project_html`). Policy id: `v1_check_from_atom`. Closed vocab stays
`reinforce` (Gagné 9a). Do not invent `retrieve`. `practice` exists on the
closed list; this hop does **not** stamp it on a new `ele_`.

Question clothes are occurrence-level (`intent.move`, Couturier
`layout_hint: check`) **or** projector-only (sequence practice of existing
presents). **No authored `content.text` on the element.** Stem, key,
distractors, and sequence items are computed at project time from the atom
store.

---

## Two shapes (not two meanings)

| Shape | When | What the learner does | Honesty |
|---|---|---|---|
| `mcq_siblings` / `cloze` | Extra `reinforce` of a definitional atom that has `{subject} is {complement}` | Invert-definition MCQ (or cloze fallback) | Key ⊆ this atom. Distractors ⊆ sibling first sentences. Stem is a grammatical invert, not a new SOP fact. |
| `sequence` | A `procedure_step` group that already has `bindings.object.order` (Procedure A s1–s4) | Order those four first sentences | Items = verbatim first sentences. Correct order = Cartographer `object.order` (the sequence already taught). No invented stem. |

Definition checks stay as they are. Sequence is for procedure_step groups
that already have order — not a copula invert, and not “which is the first
planning step?” (that would invent a fact; PR #16 correctly refused it).
Jake parked a distractor-writer; this hop does not build it. LLM
distractors stay parked.

---

## Honesty bar (same as Amanuensis: no fabricated evidence)

**Definition checks (`mcq_siblings` / `cloze`)**

- **Key** is a substring of *this* atom’s `meaning.source_text` (after the
  usual Headwater-note trim). If a candidate key is not in the atom, it is
  refused — never paraphrased into existence.
- **Stem** is a grammatical invert of this atom’s own first sentence
  (`{subject} is {complement}` → `What is {subject}?`). That is a question
  transform, not a new SOP fact, number, or rule.
- **Distractors**, if any, are first sentences of **sibling atoms in the
  same store** (same `belongs_to`). Verbatim. Closed contrast, not invented
  misconceptions.
- If two usable siblings are not available, the shape falls back to a
  **cloze** of this atom’s first sentence (no distractors). Still a check
  the reader can attempt.
- Thin headings and glossary pointers are not used as siblings
  (`Roles and Responsibilities.`, `Procedures.`, `For definitions, refer…`).

**Sequence checks (`sequence`)**

- **Items** are the first sentences of the procedure_step atoms in the
  group (`atom_sop_ast29080_proc_a_s1` … `_s4`). Verbatim. Each item ⊆ that
  atom.
- **Correct order** is `bindings.object.order` of those atoms — the
  sequence already taught on the job aid. Not a new ranking.
- **Prompt** is task clothes, not an SOP stem: *Put these in the order
  already taught.* Do not author “Which is the first planning step?”
- **Feedback** names object.order / the taught sequence. It does not
  invent SOP facts (“the first planning step is…”).
- Initial display is a **stable non-identity permutation** so the learner
  can be wrong, then right.

Shape is a key (`mcq_siblings` | `cloze` | `sequence`), not a second
meaning. It is **not** written onto the element. Couturier records
`reinforce` surfaces as `layout_hint: check`. The sequence practice is
projector-only (see composition choice below). Do not put option labels
on `element.assessment`. Do not bind `interaction_primitive` (Storyline;
not this hop).

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

## What is seeded to *have* a definition check

The 1:many seed (`one_to_many_v1.md`) mints extra `reinforce` occurrences.
This hop keeps the ALSAP definition extra and the purpose extra — still a
seed, not the whole SOP. Sequence practice does **not** add a seed row.

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

---

## Who writes what

| Agent | Still owns | This hop |
|---|---|---|
| Realizer | `ele_` ids; HTML projection | Derives and renders definition checks from extra `reinforce`; derives and renders sequence practice from the four Procedure A presents |
| Cartographer | occurrence intent | Does not mint `practice`/`assess`; extra `reinforce` move stays Realizer-stamped; A-step primaries stay `present` |
| Couturier | expression style keys | `layout_hint` for `reinforce` is `check`; still `brand.recall` / `tp_recall`. Sequence practice is projector clothes of the existing presents |

Re-running realize → cartographer → couturier keeps extra `ele_` ids,
intent, style, and the same check projection (pure function of store +
move + object.order).

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
and before the instance example (Gagné-ish: practice the steps near the
job aid; instance stays `exemplify`). Definition checks stay at the end.
