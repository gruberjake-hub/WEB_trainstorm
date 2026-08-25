# tools/
Agents & utilities. lint.py (guardrail) · realize.py (Realizer v1: atoms→occurrences + lesson HTML) ·
cartographer.py (Cartographer v1: occurrence intent on an existing store) ·
render/ (element→HTML→PNG, later — not this hop).

## Realizer

From `cgen/trainstorm-core`:

    python3 tools/realize.py
    python3 tools/realize.py --project ../astellas/projects/ast_alsap

Default project is the live ALSAP SOP store (47 atoms). See the module docstring in `realize.py`.
A re-run preserves Cartographer-bound intent (`ext.cartographer`) so Realizer does not clobber the
intent facet.

## Cartographer

From `cgen/trainstorm-core`:

    python3 tools/cartographer.py
    python3 tools/cartographer.py --project ../astellas/projects/ast_alsap
    python3 tools/cartographer.py --selftest

Binds `move` / `teaches` / `rhetorical` / `intended_response` on existing `ele_` records (heuristic
v1, `agents/cartographer/heuristic_v1.md`), validates against `element.schema.json`, leaves
`atoms.json` untouched, and re-projects `realized_lesson.html`. Run realize first if
`occurrences/elements.json` does not exist.
