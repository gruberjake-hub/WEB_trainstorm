# tools/
Agents & utilities. lint.py (guardrail) · realize.py (Realizer v1: atoms→occurrences + lesson HTML) ·
cartographer.py (Cartographer v1: occurrence intent on an existing store) ·
couturier.py (Couturier v1: occurrence style keys on an existing store) ·
render/ (element→HTML→PNG, later — not this hop).

## Realizer

From `cgen/trainstorm-core`:

    python3 tools/realize.py
    python3 tools/realize.py --project ../astellas/projects/ast_alsap

Default project is the live ALSAP SOP store (47 atoms). See the module docstring in `realize.py`.
A re-run preserves Cartographer-bound intent (`ext.cartographer`), Couturier style
(`expression` / `ext.couturier`), and extra 1:many `ele_` records. Default run mints a small
1:many seed (`agents/realizer/one_to_many_v1.md`) on a few ALSAP atoms. Extra `reinforce`
occurrences project as a check from a stamped `invert_definition` shape
(`agents/realizer/check_v1.md`). Default HTML is
the short lesson spine (`agents/realizer/spine_v1.md`); `realized_coverage.html` is the full
SOP dump. Realizer also binds compiler primitives (`agents/realizer/primitives_v1.md`) so
the spine is heading/callout/body/job-aid/example/check, not a stack of SOP cards. Scene
records (`agents/realizer/scenes_v1.md`) group those existing beats as **three named
scenes** (front-matter / Procedure A / form BR). Source of truth is the
project catalog (`occurrences/scenes.json`); `spine.scenes` / `ext.scene`
is the stamped runtime view. The grouping heuristic may still propose a
default when no catalog exists. The projector **reads** that list and pages
**one scene at a time** (Next/Back).
A **lesson** record (`agents/realizer/lesson_v1.md`) on `manifest.lessons`
is the stamped runtime view of the project catalog
(`occurrences/lessons.json`). Lessons point at `scene_ids` only.
`realized_lesson.html` is a read of the
default node (`{project}_short`, or `--lesson`). Extra catalog records
project to a sibling HTML derived from `lesson_id` (pager disabled when
the record is one scene). Live ALSAP: `ast_alsap_short` (pages 1–2–3),
`ast_alsap_br` (scene 3), `ast_alsap_plan` (scene 2). Adding a lesson is
appending a catalog row; Realize does not special-case those ids.
Definition/purpose checks stay a final step after scene 3 on the short
lesson, not a fourth scene, and are **not** forced onto subset lessons.
Coverage dump stays a second projection, not a lesson node.
Default pass emits all catalog lessons. `--lesson <id>` regenerates
that file.
A small
instance-example seed (`agents/realizer/instance_example_v1.md`) mints two guest `ele_`
records whose `composed_from` is an `alsap_asp9999` atom_id. A small form-field
present seed (`agents/realizer/form_field_present_v1.md`) mints two guest `ele_`
records whose `composed_from` is an `alsap` FORM-AST-34037 field atom_id (the
referent of those instance examples). `--no-one-to-many` skips
new extras but still preserves any that exist. `--selftest` checks stable extra ids, the
check honesty bar, spine membership (why-this callout of purpose, front-matter, Procedure A
as a job sequence, sequence practice of those presents, form BR-field presents, instance
example, then checks), that check operands resolve from the graph (not hardcoded HTML),
and the atom → primitives bind (procedure_step → `tp_step`,
activate → `tp_callout`, job-aid HTML). Scene catalog `element_ids`
resolve from the graph, not hardcoded HTML. Lesson catalog `scene_ids`
resolve from that stamp (no extra lesson id hardcoded in
the projector). Scene 3 also projects a closed-choice
of the BR profile fill (`options_ref` value ids; key = instance
`selected_value`; projector-only `closed_choice` on `manifest.checks`).

## Cartographer

From `cgen/trainstorm-core`:

    python3 tools/cartographer.py
    python3 tools/cartographer.py --project ../astellas/projects/ast_alsap
    python3 tools/cartographer.py --selftest

Binds `move` / `teaches` / `rhetorical` / `intended_response` on existing `ele_` records (heuristic
v1, `agents/cartographer/heuristic_v1.md`), validates against `element.schema.json`, leaves
`atoms.json` untouched, and re-projects `realized_lesson.html` (spine) plus
`realized_coverage.html` (full dump). Extra 1:many occurrences keep
their Realizer-stamped `move`; Cartographer still binds the rest of intent. Does not wipe
Couturier style. Run realize first if `occurrences/elements.json` does not exist.

## Couturier

From `cgen/trainstorm-core`:

    python3 tools/couturier.py
    python3 tools/couturier.py --project ../astellas/projects/ast_alsap
    python3 tools/couturier.py --selftest

Binds style keys on existing `ele_` records (`style_ref`, `content_role`,
`layout_hint`) from a documented move→look map (`agents/couturier/style_map_v1.md`).
Preserves Realizer’s `text_primitive` (compiler form). Mints no
ids. Does not write `atoms.json` or `element.intent`. HTML reads those keys so hook vs present
vs reinforce do not look like the same card; extra `reinforce` is a check, not a recap;
procedure steps on the spine are a job-aid, not four body cards.
HTML default is the short spine; coverage dump is the sibling file. Run realize then cartographer first.
