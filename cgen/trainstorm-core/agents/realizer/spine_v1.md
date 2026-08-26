# Realizer lesson spine v1 — short path, full dump as coverage

*A documented selection/sequence of existing occurrences — not fake instructional-design
genius, and not an LLM call.* Implemented by `tools/realize.py`. Policy id:
`v1_front_matter_then_checks`. Spec path stamped on the occurrence manifest as
`spine.spec`.

The live ALSAP hop already minted `ele_` records, bound `move`/`teaches`
(Cartographer), dressed them (Couturier), and projected extra `reinforce` as
checks. The default HTML was still **every SOP atom in document order**. That is
coverage, not a course. This hop projects a **short lesson path** an ID would
actually teach, and keeps the dump as a second view.

Realizer owns the projection. Cartographer still owns intent. Couturier still
owns style. Spine **mints no `ele_` ids** and **drops none**. `atoms.json` is
untouched. Locale packs stay keyed on `atom_id`. Closed vocab still has no
`retrieve`; extra `reinforce` stays a check (`agents/realizer/check_v1.md`).

---

## Why not walk Cartographer's object graph as the path

`bindings.object.belongs_to` + `order` is the SOP tree. Walking it *is* the 47
card dump. It does not imply a short lesson. Spine v1 **reuses those roles as
input** (root vs direct child vs descendant; sibling `order`) and then **selects
a subset**, sequenced as opening → front-matter teaching cards → existing
checks.

Do not invent a parallel parent/sequence on the element. Do not mint a pile of
new 1:many. Do not call a model to pick the path.

---

## Membership (which atoms, which occurrences)

**On the path**

| Role | Which atoms | Which `ele_` | Why |
|---|---|---|---|
| Opening | Document root: no `belongs_to` | Primary (`hook` once Cartographer has bound it) then the seeded extra `present` if it exists | Title hook + title present — already seeded on `atom_sop_ast29080` |
| Front-matter teaching cards | Direct children of the root, `kind` in `procedure` / `form`, **not thin** | Primary occurrence only | Paragraphs an ID would actually say: purpose, scope, what-it-is. Sorted by `object.order`. Purpose may be Cartographer `objective`; that is still a teaching card, not a check. |
| Checks | Spine atoms that already have an extra `reinforce` | Those extras, in the same atom order as their presents | Reuse the two existing checks. Do not mint more. |

**Off the path (coverage, not deleted)**

- Thin headings and glossary pointers (`Roles and Responsibilities.`,
  `Procedures.`, `For definitions, refer…`) — same bar as check-sibling
  rejection in `check_v1.md`. Headwater already marked definitions as an
  external reference with no embedded meaning.
- Descendants: lists, list items, procedure steps, govdocs, A/B/C section
  heads. Those are the job/procedure dump.
- Any 1:1 leftover whose atom is not front-matter.

Live ALSAP (`cgen/astellas/projects/ast_alsap`) therefore yields seven
occurrences, in this order:

1. `ele_sop_ast29080` — hook (title)
2. `ele_sop_ast29080__present` — present extra of the title
3. `ele_sop_ast29080_purpose` — objective (why this SOP)
4. `ele_sop_ast29080_scope` — present (who it applies to)
5. `ele_sop_ast29080_general` — present (what an ALSAP is)
6. `ele_sop_ast29080_purpose__reinforce` — check
7. `ele_sop_ast29080_general__reinforce` — check

Teachable order is Gagné-shaped and small: gain attention → say the thing
(purpose / who / what) → enhance retention with the two existing checks.
Checks come **after** the front-matter cards, not interleaved, so the two
recalls sit together at the end. Not the 20 procedure steps.

---

## What is written

Occurrence manifest `spine`:

```json
{
  "policy": "v1_front_matter_then_checks",
  "spec": "agents/realizer/spine_v1.md",
  "element_ids": ["ele_sop_ast29080", "ele_sop_ast29080__present", "…"],
  "count": 7,
  "store_count": 50,
  "note": "Selection of existing ele_ records. Coverage dump keeps the rest."
}
```

Ids are stable. A re-run of realize → cartographer → couturier recomputes the
same list from the same heuristic (pure function of atoms + occurrences). It
does not drop extras, Cartographer intent, or Couturier style.

HTML (Realizer projector):

| File | Default experience |
|---|---|
| `<project>/realized_lesson.html` | The spine, in the order above. Title hook, a handful of teaching cards, two checks. Link to coverage. |
| `<project>/realized_coverage.html` | Full occurrence dump in SOP document order (the previous default). Link back to the lesson. |

Do not hide coverage by deleting `ele_` records. The store stays 50.

---

## What this is not

- Not an ID genius and not an LLM path-picker.
- Not a distractor-writer. Checks keep closed-contrast distractors from sibling
  atoms (verbatim). Jake parked a future distractor-writer agent.
- Not a new `retrieve` enum. Not new 1:many beyond the existing seed.
- Not Dragoman, Storyline, `.potx`, motion, or `tools/render/` PNG pipelines.
- Not Cartographer writing sequence; not Couturier picking clothes from the
  spine. Clothes still follow `move`.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Default project is `cgen/astellas/projects/ast_alsap`. Open
`cgen/astellas/projects/ast_alsap/realized_lesson.html` for the short lesson;
`realized_coverage.html` for the full SOP dump.
