# Realizer scene projection v1 — membership on the graph

*PR #25 grouped the short ALSAP lesson under three named headings.
PR #26 paged those headings one at a time.* This spec is how a scene is
**named on the occurrence store / manifest** and how the HTML projector
**reads** that record — not a new agent, not a second meaning store, not
outcome language, not a fourth scene of definition checks.

Implemented in `tools/realize.py`. Closed pedagogical vocab is unchanged.
Scene records mint **no** `ele_`. Membership is ordered `ele_` refs already
on the spine (`agents/realizer/spine_v1.md`). In-scene checks are shape
refs into `manifest.checks` (`agents/realizer/check_v1.md`) — not a
parallel pedagogy.

Policy ids: `v1_three_scenes_from_roles` (the grouping heuristic, unchanged)
and `v1_scenes_on_graph` (the scene is a first-class record). Closed role
vocab: `vocab/scene.enum.json`. Paging stays `v1_one_scene_at_a_time`.

---

## Why this hop

After PR #28 the three check kinds live on `ext.check` / `manifest.checks`.
Scenes and one-at-a-time paging were still projector chrome: three named
ALSAP headings plus a pager, with membership recomputed from SOP/form
roles at project time. A later agent could not emit a paged lesson
without special-casing `realize.py`.

This hop **promotes `spine.scenes`** (already stamped for paging policy)
to the source of truth — ordered scene objects with `element_ids` —
analogous to `manifest.checks`. The projector **reads** that list to wrap
and page. It does not re-discover scenes by hard-coded atom ids.

No new ALSAP beats. Same 16 spine occurrences. Same three scenes. Same
paging UX. `atoms.json` unchanged. No authored `content.text`.

---

## Closed record (not three meanings)

| Field | What it is |
|---|---|
| `id` | Stable scene id (`what_an_alsap_is` / `how_an_alsap_starts` / `benefit_risk_on_the_form`). Lesson-specific, not a closed enum. |
| `role` | Closed: `front_matter` / `procedure_a` / `form_br` (`vocab/scene.enum.json`). |
| `heading` | Title heuristic for that role. Stamped, then read. Not “will be able to…”. |
| `kicker` | Short role label (Front matter / Procedure A / Form). |
| `element_ids` | Ordered `ele_` refs already on the spine. Must resolve on the occurrence store. |
| `checks` | Optional `{shape, see: checks}` refs into `manifest.checks`. In-scene projector-only checks. |
| `from` | Documented heuristic provenance. |

Title heuristic (closed, not an LLM):

| Role | Heading | Which existing beats |
|---|---|---|
| `front_matter` | **What an ALSAP is** | Document-root opening, why-this callout of purpose, teachable front-matter primaries |
| `procedure_a` | **How an ALSAP starts** | Procedure A job-aid presents. `sequence_order` stays in-scene. |
| `form_br` | **Benefit-risk on the form** | FORM-AST-34037 BR-field presents + instance examples. `closed_choice` stays in-scene. |

Do not mint a fourth scene for the two definition/purpose checks — they
stay at **lesson end** (`spine.scenes.lesson_end_checks`) as a final
player step after Next from scene 3.

Where they live:

- **Manifest:** `spine.scenes` is the index (ordered scene objects +
  `lesson_end_checks` + `paging`). Analogous to `manifest.checks`.
- **Occurrence store:** `ext.scene` on member `ele_` records (`id` +
  `role`). Lesson-end invert-definition hosts are **not** scene members.
  Coverage-only occurrences have no `ext.scene`.
- Paging (`v1_one_scene_at_a_time`) is player UX **on that list**, not a
  second membership heuristic.

Cartographer still owns `intent`. Couturier still owns style. Realizer
binds the scene record the way it binds check shapes and `text_primitive`.

---

## Honesty bar

- **Membership** is a partition of existing spine `ele_` ids. Scene
  `element_ids` ∪ `lesson_end_checks` = `spine.element_ids`. No new
  occurrence. No dropped occurrence.
- **Headings** are the documented title heuristic for the closed role.
  Not invented outcomes. Not copied atom sentences onto the element.
- **In-scene checks** are refs (`shape` + `see: checks`). Wording still
  resolves from `manifest.checks` operands — this hop does not copy
  stems, options, or first sentences onto the scene record.
- **Projector reads the stamp.** Wrap, page, and in-scene check
  placement come from `spine.scenes`. The projector does not ask
  `if atom_id` / `if role == form_br` to decide which heading a beat
  wears, or whether sequence_order / closed_choice land in that scene.
- Coverage dump stays ungrouped and unpaged.

---

## Who writes what

| Agent | Still owns | This hop |
|---|---|---|
| Realizer | `ele_` ids; HTML projection; compiler `text_primitive`; check shapes | Binds `spine.scenes` + `ext.scene` (id, role, ordered `element_ids`, in-scene check refs). Projector **reads** those records to wrap/page. |
| Cartographer | occurrence intent | Does not pick the path. Does not wipe `ext.scene` or `ext.check`. |
| Couturier | expression style keys | Does not mint a scene `ele_`. Does not write `layout_primitive`. Scene wrap/page is Realizer reading the stamp of dressed beats. |

Re-running realize → cartographer → couturier keeps extra `ele_` ids,
intent, style, check shapes, and the same scene records (pure function
of spine membership + SOP/form roles).

---

## What this is not

- Not new beats, not a new `ele_`, not Procedure B.
- Not an LLM path-picker and not outcome language.
- Not a fourth scene of definition checks.
- Not Chameleon, not Headwater outcomes-mode, not `/cgen/alsap` hosting.
- Not a quiz engine and not LLM distractors.
- Not rewriting `atoms.json` or authored `content.text`.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Optional: `python3 tools/realize.py --selftest` asserts scene operands
resolve from the graph (not hardcoded HTML).
