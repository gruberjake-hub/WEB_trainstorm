# Realizer check projection v1 — `reinforce` as a check, not a recap

*Traditional ID’s third move is a check.* Couturier already dresses
`reinforce` as `brand.recall` / `tp_recall`. This spec is how the HTML
projector **renders** that move from atom meaning — not a new agent, not a
second meaning store, not a new pedagogical enum.

Implemented in `tools/realize.py` (`derive_check`, `project_html`).
Policy id: `v1_check_from_atom`. Closed vocab stays `reinforce` (Gagné 9a).
Do not invent `retrieve`.

Question clothes are occurrence-level (`intent.move`, Couturier
`layout_hint: check`). **No authored `content.text` on the element.**
The stem, key, and any distractors are computed at project time from the
atom store via `composed_from`.

---

## Honesty bar (same as Amanuensis: no fabricated evidence)

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

Shape is a key (`mcq_siblings` | `cloze`), not a second meaning. It is
**not** written onto the element. Couturier records the surface as
`layout_hint: check`. Do not put option labels on `element.assessment`
(that would be authored meaning on the occurrence). Do not bind
`interaction_primitive` (Storyline; not this hop).

---

## What is seeded to *have* a check

The 1:many seed (`one_to_many_v1.md`) mints extra `reinforce` occurrences.
This hop keeps the ALSAP definition extra and adds **one** more
teaching-worthy atom — still a seed, not the whole SOP.

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

---

## Who writes what

| Agent | Still owns | This hop |
|---|---|---|
| Realizer | `ele_` ids; HTML projection | Derives and renders the check from move + atom meaning |
| Cartographer | occurrence intent | Does not mint `practice`/`assess`; extra `reinforce` move stays Realizer-stamped |
| Couturier | expression style keys | `layout_hint` for `reinforce` is `check` (was `recap`); still `brand.recall` / `tp_recall` |

Re-running realize → cartographer → couturier keeps extra `ele_` ids,
intent, style, and the same check projection (pure function of store +
move).

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Optional: `python3 tools/realize.py --selftest` (includes the honesty bar).
