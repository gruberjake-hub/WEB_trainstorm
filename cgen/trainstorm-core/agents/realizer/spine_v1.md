# Realizer lesson spine v1 — short path, full dump as coverage

*A documented selection/sequence of existing occurrences — not fake instructional-design
genius, and not an LLM call.* Implemented by `tools/realize.py`. Policy id:
`v1_front_matter_procedure_sequence_then_checks` (extends the earlier
`v1_front_matter_one_procedure_then_checks` membership: that hop put Procedure
A’s *lead* on the path; this hop walks A’s **real steps as a job sequence**).
Spec path stamped on the occurrence manifest as `spine.spec`.

The live ALSAP hop already minted `ele_` records, bound `move`/`teaches`
(Cartographer), dressed them (Couturier), and projected extra `reinforce` as
checks. Spine v1 then took front-matter only; a later hop added one Plan
Development present. This hop keeps that opening and puts **Procedure A’s
real steps** on the path — skip thin A/B/C headings, take every non-thin
`procedure_step` child of the first Procedures branch, in `object.order`.
Not B/C. The dump stays coverage.

Realizer owns the projection. Cartographer still owns intent. Couturier still
owns style. Spine **mints no `ele_` ids** and **drops none**. `atoms.json` is
untouched. Locale packs stay keyed on `atom_id`. Closed vocab still has no
`retrieve`; extra `reinforce` stays a check (`agents/realizer/check_v1.md`).

---

## Why not walk Cartographer's object graph as the path

`bindings.object.belongs_to` + `order` is the SOP tree. Walking it *is* the 47
card dump. It does not imply a short lesson. Spine v1 **reuses those roles as
input** (root vs direct child vs descendant; sibling `order`) and then **selects
a subset**, sequenced as opening → front-matter teaching cards → Procedure A
job sequence → existing checks.

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

## Why no extra `reinforce` on those atoms

A check for this hop must be **sibling-atom closed contrast**: verbatim first
sentences of sibling steps. No LLM. No invented stem.

`derive_check` can invert `{subject} is {complement}` → `What is {subject}?`
(the two existing checks). Procedure-step atoms are **imperatives** (*Notify…*,
*Collaborate…*, *Schedule…*). They have usable sibling sentences, but no
copula to invert. A cloze of a step is not sibling contrast. A stem such as
“Which is the first planning step?” would invent a fact. Jake parked a
distractor-writer agent for later.

So: **present only. No extra `ele_`.** Store stays 50.
`supports_honest_sibling_check` is the gate (`tools/realize.py`); it is False
for every A step.

---

## Membership (which atoms, which occurrences)

**On the path**

| Role | Which atoms | Which `ele_` | Why |
|---|---|---|---|
| Opening | Document root: no `belongs_to` | Primary (`hook` once Cartographer has bound it) then the seeded extra `present` if it exists | Title hook + title present — already seeded on `atom_sop_ast29080` |
| Front-matter teaching cards | Direct children of the root, `kind` in `procedure` / `form`, **not thin** | Primary occurrence only | Paragraphs an ID would actually say: purpose, scope, what-it-is. Sorted by `object.order`. Purpose may be Cartographer `objective`; that is still a teaching card, not a check. |
| Procedure A job sequence | First Procedures-container branch in `object.order`; skip thin A/B/C heading; take every non-thin `procedure_step` child (`PROCEDURE_SEQUENCE_CAP = 8`) | Primary occurrence only | Doing the work: Plan Development’s four real steps, in `object.order`. Not B/C. |
| Checks | Spine atoms that already have an extra `reinforce` | Those extras, in the same atom order as their presents | Reuse the two existing checks. Do not mint more. |

**Off the path (coverage, not deleted)**

- Thin headings and glossary pointers (`Roles and Responsibilities.`,
  `Procedures.`, `A. Plan Development of ALSAP.`, `B.…`, `C.…`,
  `For definitions, refer…`) — same bar as check-sibling rejection in
  `check_v1.md`.
- Other descendants: lists, list items, procedure B/C steps, govdocs.
- Any 1:1 leftover whose atom is not front-matter or a Procedure A step.

Live ALSAP therefore yields **eleven** occurrences, in this order:

1. `ele_sop_ast29080` — hook (title)
2. `ele_sop_ast29080__present` — present extra of the title
3. `ele_sop_ast29080_purpose` — objective (why this SOP)
4. `ele_sop_ast29080_scope` — present (who it applies to)
5. `ele_sop_ast29080_general` — present (what an ALSAP is)
6. `ele_sop_ast29080_proc_a_s1` — present (notify / request Lead)
7. `ele_sop_ast29080_proc_a_s2` — present (identify authors and reviewers)
8. `ele_sop_ast29080_proc_a_s3` — present (15-day kick-off)
9. `ele_sop_ast29080_proc_a_s4` — present (confirm deliverables and dates)
10. `ele_sop_ast29080_purpose__reinforce` — check
11. `ele_sop_ast29080_general__reinforce` — check

Teachable order is Gagné-shaped and small: gain attention → say the thing
(purpose / who / what) → walk the Plan Development job sequence → enhance
retention with the two existing checks. Checks come **after** the teaching
cards, not interleaved. Not the 20 procedure steps of A+B+C.

---

## What is written

Occurrence manifest `spine`:

```json
{
  "policy": "v1_front_matter_procedure_sequence_then_checks",
  "spec": "agents/realizer/spine_v1.md",
  "element_ids": ["ele_sop_ast29080", "ele_sop_ast29080__present", "…"],
  "count": 11,
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
| `<project>/realized_lesson.html` | The spine, in the order above. Title hook, front-matter, Procedure A sequence, two checks. Link to coverage. |
| `<project>/realized_coverage.html` | Full occurrence dump in SOP document order. Link back to the lesson. |

Do not hide coverage by deleting `ele_` records. The store stays 50.

---

## What this is not

- Not an ID genius and not an LLM path-picker.
- Not a distractor-writer. Checks keep closed-contrast distractors from sibling
  atoms (verbatim). Jake parked a future distractor-writer agent. This hop
  does not mint a procedure-step check.
- Not a new `retrieve` enum. Not new 1:many (no extra `ele_` this hop).
- Not Dragoman, Storyline, `.potx`, motion, or `tools/render/` PNG pipelines.
- Not Cartographer writing sequence; not Couturier picking clothes from the
  spine. Clothes still follow `move`.
- Not procedure B/C and not a full SOP dump.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Default project is `cgen/astellas/projects/ast_alsap`. Open
`cgen/astellas/projects/ast_alsap/realized_lesson.html` for the short lesson;
`realized_coverage.html` for the full SOP dump. Live (Netlify rewrite of those
same files, not a copy): https://trainstorm.ai/cgen/alsap and
https://trainstorm.ai/cgen/alsap/coverage.
