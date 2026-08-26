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
occurrences project as a check from the atom (`agents/realizer/check_v1.md`). Default HTML is
the short lesson spine (`agents/realizer/spine_v1.md`); `realized_coverage.html` is the full
SOP dump. Realizer also binds compiler primitives (`agents/realizer/primitives_v1.md`) so
the spine is heading/callout/body/job-aid/example/check, not a stack of SOP cards. The
projector wraps those existing beats as **three named scenes** (front-matter /
Procedure A / form BR) from SOP/form roles — layout chrome, not new meaning.
A small
instance-example seed (`agents/realizer/instance_example_v1.md`) mints two guest `ele_`
records whose `composed_from` is an `alsap_asp9999` atom_id. A small form-field
present seed (`agents/realizer/form_field_present_v1.md`) mints two guest `ele_`
records whose `composed_from` is an `alsap` FORM-AST-34037 field atom_id (the
referent of those instance examples). `--no-one-to-many` skips
new extras but still preserves any that exist. `--selftest` checks stable extra ids, the
check honesty bar, spine membership (why-this callout of purpose, front-matter, Procedure A
as a job sequence, sequence practice of those presents, form BR-field presents, instance
example, then checks), and the atom → primitives bind (procedure_step → `tp_step`,
activate → `tp_callout`, job-aid HTML).

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
