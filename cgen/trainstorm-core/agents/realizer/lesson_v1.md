# Realizer lesson v1 — one graph object that points at `spine.scenes`

*PR #29 put scene membership on the graph (`agents/realizer/scenes_v1.md`).
The short ALSAP lesson was still a projector convention: `realized_lesson.html`
was “the” lesson because `realize.py` knew this project.* This spec is how a
**lesson** is named on the occurrence manifest and how the HTML projector
**reads** that record — not a second meaning store, not a LMS, not SCORM,
not a course catalog UI, not a `Course` `ele_`.

Implemented in `tools/realize.py`. Closed pedagogical vocab is unchanged.
Lesson records mint **no** `ele_`. Membership is ordered scene ids already
on `spine.scenes`, plus `lesson_end_checks` (existing `ele_` refs). In-scene
checks stay shape refs into `manifest.checks`.

Policy id: `v1_lesson_on_graph`. Paging stays `v1_one_scene_at_a_time`
on `spine.scenes.paging`. Scene records come from the project catalog
(`occurrences/scenes.json`) when present; heuristic stays
`v1_three_scenes_from_roles` as the proposal when no catalog exists.

---

## Why this hop

After PR #29 the three scenes live on `spine.scenes` / `ext.scene`. The
projector still assumed there was one ALSAP short lesson and wrapped
whatever `spine.scenes` held. A later agent could not emit another lesson
without special-casing `realize.py` HTML.

This hop **promotes a lesson record** (analogous to `manifest.checks` and
`spine.scenes`) so `realized_lesson.html` is a **read of that node** + its
scenes + checks. Same 16 beats. Same three scenes. Same pager. Same checks.

No new ALSAP pedagogy. `atoms.json` unchanged. No authored `content.text`.

---

## Closed record (not a second meaning store)

| Field | What it is |
|---|---|
| `lesson_id` | Stable id (`{project}_short` for the default). Lesson-specific, not a closed enum. |
| `title` | Title heuristic, stamped then read. Document-root atom first sentence (`title_from`). Not “will be able to…”. |
| `title_from` | `atom_id` ref. Projector may re-resolve. Not authored `content.text` on an element. |
| `scenes` | Pointer: `{see: spine.scenes}`. Membership lives there. |
| `scene_ids` | Ordered scene id refs into `spine.scenes.scenes[].id`. Must resolve. |
| `lesson_end_checks` | Pointer: `{see: spine.scenes.lesson_end_checks}`. |
| `lesson_end_check_ids` | Ordered `ele_` refs (the invert-definition extras). Not a fourth scene. |
| `paging` | Pointer: `{see: spine.scenes.paging}`. Player UX on that list. |
| `default` | The project’s default lesson (`--lesson` overrides). |

Title heuristic (closed, not an LLM, not outcome language): the
document-root atom already on the spine (opening beat’s `composed_from`).
Live ALSAP: SOP-AST-29080 title sentence.

Do not copy scene headings onto the lesson. Headings live on the scene
records. Do not copy check stems, options, or first sentences onto the
lesson.

Where they live:

- **Manifest:** `lessons` is the **stamped runtime view** (default +
  ordered lesson objects). Analogous to `manifest.checks`. Sibling of
  `spine` / `checks` — not a second `atoms.json`.
- **Project catalog:** `occurrences/lessons.json` is the **source of
  truth**. Closed file. Realizer reads it; it does not rewrite it.
  Adding a lesson is appending a record (`lesson_id`, `scene_ids`,
  optional `lesson_end_check_ids`, optional `paging`). Realize does
  not special-case extra lesson ids in Python.
- **Occurrence store:** no `ext.lesson`, no `Course`/`Module` `ele_`.
  Scene membership stays `ext.scene`. Check shapes stay `ext.check`.
- Coverage dump stays a **second projection** of the store, not a second
  lesson node.

Cartographer still owns `intent`. Couturier still owns style. Realizer
binds the lesson record the way it binds scenes and check shapes.

---

## Why not a `Course` `ele_`

`element.schema.json` already names container types (`Course`, `Module`,
`Section`, `Scene`). `cgen/schema/course.schema.json` and
`course-primitives.schema.json` are the older authored-text course chain
(Head/Statement with `text`) — not this constitution.

This hop does **not** mint a `Course` occurrence:

- A container `ele_` needs `composed_from`. Composing from the SOP root
  would be a third teaching-act of the title atom (it already has hook +
  present). That is a lie.
- Scene records mint no `Scene` `ele_`. The lesson is the same kind of
  object: an index of refs, not a meaning node.
- Store stays **55 / 47**. Spine stays **16**.

Do not create a rival course schema. Do not invent a catalog UI.

---

## Honesty bar

- **Membership** is refs: `scene_ids` ⊆ `spine.scenes.scenes[].id`;
  `lesson_end_check_ids` ⊆ spine `ele_` ids. Union of those scene
  `element_ids` plus lesson-end checks = `spine.element_ids` for the
  default lesson. No new occurrence. No dropped occurrence.
- **Title** is the documented heuristic from `title_from`. Not invented
  outcomes. Not copied onto an element as `content.text`.
- **Projector reads the stamp.** Wrap, page, heading, and which scenes
  appear come from the selected lesson node. The projector does not
  assume “the ALSAP lesson is these three headings.” `--lesson` (or the
  default) selects the record.
- A later agent emits another lesson by writing a lesson record
(`lesson_id` + `scene_ids` + title) that points at existing
`spine.scenes`. **That write is a catalog row**, not a Python
branch: `occurrences/lessons.json` is the closed project file;
Realizer **reads** it and stamps `manifest.lessons`. Extra
`scene_ids` may be a subset. `lesson_end_check_ids` stay empty unless
those invert-definition extras honestly belong on that lesson.
A missing catalog (fixtures) still preserves extras already on the
stamp and only recomputes the default.
- Coverage dump stays ungrouped and unpaged, and is **not** a lesson node.

---

## Who writes what

| Agent | Still owns | This hop |
|---|---|---|
| Realizer | `ele_` ids; HTML projection; compiler `text_primitive`; check shapes; **reads** `occurrences/scenes.json` and stamps `spine.scenes` | **Reads** `occurrences/lessons.json` and stamps `manifest.lessons`. Projector **reads** that node to wrap/page. Also writes a Course Engine JSON projection (`realized_lesson.json`) of the same node for `/cgen`. Does not special-case extra lesson ids. |
| Cartographer | occurrence intent | Does not pick the path. Does not wipe `manifest.lessons`, `ext.scene`, or `ext.check`. |
| Couturier | expression style keys | Does not mint a lesson `ele_`. Does not write `layout_primitive`. Lesson wrap/page is Realizer reading the stamp of existing scenes. |

Re-running realize → cartographer → couturier keeps extra `ele_` ids,
intent, style, check shapes, scene records, and stamps lesson records
from the catalog (pure function of catalog rows + spine + document-root
title). Extra lesson HTML is a sibling file derived from `lesson_id`
(`{project}_{suffix}` → `realized_lesson_{suffix}.html`). A lesson with
one scene and no lesson-end checks has paging chrome suppressed (same
`v1_one_scene_at_a_time` policy; nowhere to page). Default pass emits
every catalog lesson. `--lesson <id>` regenerates that file.

---

## What this is not

- Not new beats, not a new `ele_`, not Procedure B.
- Not an LLM path-picker and not outcome language.
- Not a fourth scene of definition checks.
- Not a LMS, not SCORM, not a course catalog UI.
- Not Chameleon, not Headwater outcomes-mode, not `/cgen/alsap` hosting.
- Not rewriting `atoms.json` or authored `content.text`.
- Not a rival `course.schema.json`. `/cgen` reads a **projection** of this
  lesson node (`realized_lesson.json`), rebuilt by Realize — not a
  hand-authored SCORM package and not a third constitution.
- Not a course catalog UI and not a third lesson minted from the coverage dump.

---

## Lessons are catalog rows (not Python branches)

Live ALSAP proves the lesson node is not a singleton, and that a third
record is an append to the catalog — not a fork of `realize.py`:

| `lesson_id` | `scene_ids` | lesson-end invert_definition | HTML |
|---|---|---|---|
| `ast_alsap_short` (default) | all three scenes | yes (definitional close of front-matter) | `realized_lesson.html` |
| `ast_alsap_br` | `benefit_risk_on_the_form` only | no — those checks do not belong on this form cluster | `realized_lesson_br.html` |
| `ast_alsap_plan` | `how_an_alsap_starts` only | no — those checks do not belong on Procedure A | `realized_lesson_plan.html` |

Same 55 `ele_` / 47 atoms. No new pedagogy atoms. No authored
`content.text`. Title heuristic is still the document-root atom (scene
heading stays on the scene record). In-scene checks stay on the scene
(`sequence_order` on Procedure A; `closed_choice` on form BR). Catalog
path: `cgen/astellas/projects/ast_alsap/occurrences/lessons.json`.
Realize reads that file and stamps `manifest.lessons`. A one-scene
record suppresses Next/Back.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
python3 tools/realize.py --lesson ast_alsap_br
python3 tools/realize.py --lesson ast_alsap_plan
```

Default project: `cgen/astellas/projects/ast_alsap`. Default pass emits
all catalog lessons. Default lesson `ast_alsap_short` →
`realized_lesson.html` plus `realized_lesson.json`. `/cgen` loads that
JSON through Course Engine v1. `--lesson <id>` regenerates that file (path
derived from `lesson_id`; the projector is not forked). `--selftest`
asserts catalog records resolve `scene_ids` from the graph and that
extra lesson ids are not hardcoded in the projector. The engine
projection selftest asserts three named scenes, in-scene
`sequence_order` + `closed_choice`, and lesson-end `invert_definition`.
