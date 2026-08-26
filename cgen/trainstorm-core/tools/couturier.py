#!/usr/bin/env python3
"""
Couturier v1 — bind occurrence style keys on an existing Realizer store.

Couturier owns style on the occurrence's expression facet: `style_ref`,
`content_role`, `layout_hint`. v1 is a documented map from
`intent.move` (`agents/couturier/style_map_v1.md`), not a design system and
not ID genius. Realizer binds the compiler `text_primitive` (heading / body /
step / callout / check); Couturier preserves that key and still writes clothes.
It reads already-minted `ele_` records, writes only
`element.expression` style keys (+ `ext.couturier` provenance), and re-projects
`realized_lesson.html` so different moves look like different clothes.
Default HTML is the short lesson spine; `realized_coverage.html` is the dump.
Procedure-step primitives project as a job-aid (`layout_hint: job_aid`).
Activate / `tp_callout` primitives project as a why-this callout.

Never: mint `ele_` / `atom_` ids; copy meaning onto the element; write
`atoms.json`; write `element.intent`; bind `motion_primitive` (stub),
`layout_primitive` (.potx), or `interaction_primitive` (Storyline); put style
on the atom. Locale packs stay keyed on `atom_id`. Style is keyed on
`element_id`.

Usage (from `cgen/trainstorm-core`):

    python3 tools/couturier.py
    python3 tools/couturier.py --project ../astellas/projects/ast_alsap
    python3 tools/couturier.py --selftest

Requires Realizer output at `<project>/occurrences/elements.json`. Run
Cartographer first so 1:many pairs have distinct moves (hook+present,
present+reinforce, objective+reinforce). `reinforce` extras project as a
check in the HTML (Realizer), dressed here as `brand.recall` / `tp_recall`
with `layout_hint: check`. Re-runnable; does not drop extras or Cartographer intent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
from collections import Counter, defaultdict

import harness_paths
from jsonschema import Draft202012Validator

import realize

POLICY = "v1_move_to_look"
COUTURIER = "tools/couturier.py"
SPEC = "agents/couturier/style_map_v1.md"
STYLE_KEYS = ("style_ref", "content_role", "layout_hint")
# text_primitive is Realizer-owned (compiler form). Couturier preserves it.
OWNED_KEYS = STYLE_KEYS
PRESERVED_KEYS = ("motion_primitive", "layout_primitive", "interaction_primitive")
PRIMITIVE_KEY = "text_primitive"

# move → clothes. Closed pedagogical values this SOP actually uses.
# Unmapped (practice / feedback / assess): do not invent a look.
MOVE_TO_LOOK = {
    "hook": {
        "style_ref": "brand.opening",
        "text_primitive": "tp_display",
        "content_role": "title",
        "layout_hint": "banner",
    },
    "present": {
        "style_ref": "brand.instructional",
        "text_primitive": "tp_body",
        "content_role": "body",
        "layout_hint": "card",
    },
    "reinforce": {
        "style_ref": "brand.recall",
        "text_primitive": "tp_recall",
        "content_role": "retrieval",
        "layout_hint": "check",
    },
    "objective": {
        "style_ref": "brand.purpose",
        "text_primitive": "tp_purpose",
        "content_role": "purpose",
        "layout_hint": "purpose_bar",
    },
    "activate": {
        "style_ref": "brand.prior",
        "text_primitive": "tp_callout",
        "content_role": "callout",
        "layout_hint": "callout",
    },
    "exemplify": {
        "style_ref": "brand.example",
        "text_primitive": "tp_body",
        "content_role": "example",
        "layout_hint": "cite",
    },
    "transfer": {
        "style_ref": "brand.job",
        "text_primitive": "tp_body",
        "content_role": "handoff",
        "layout_hint": "job_rail",
    },
}


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def inject_default_project():
    realize.inject_default_project()


def registry_keys(registry, field) -> set[str]:
    return {entry["key"] for entry in registry.get(field) or [] if "key" in entry}


def look_for_move(move: str) -> dict | None:
    row = MOVE_TO_LOOK.get(move)
    return dict(row) if row else None


def bind_expression(el, atom, closed_style_refs, closed_text_primitives) -> tuple[dict | None, dict]:
    """Map occurrence move → expression keys. None expression = undressed (unmapped move)."""
    move = (el.get("intent") or {}).get("move")
    if not move:
        raise SystemExit(f"{el.get('element_id')}: no intent.move to dress from — run cartographer.py")
    look = look_for_move(move)
    stamp = {
        "policy": POLICY,
        "tool": COUTURIER,
        "spec": SPEC,
        "from_move": move,
    }
    ch = atom.get("content_hash") or el.get("source_hash")
    if ch:
        stamp["source_hash"] = ch
    if look is None:
        stamp["flags"] = ["look_unmapped"]
        stamp["confidence"] = "low"
        existing = el.get("expression") or {}
        if existing.get("text_primitive"):
            return {"text_primitive": existing["text_primitive"]}, stamp
        return None, stamp
    if look["style_ref"] not in closed_style_refs:
        raise SystemExit(f"{el.get('element_id')}: style_ref {look['style_ref']!r} is not in the registry")
    if look["text_primitive"] not in closed_text_primitives:
        raise SystemExit(
            f"{el.get('element_id')}: text_primitive {look['text_primitive']!r} is not in the registry"
        )
    expression = dict(look)
    existing = el.get("expression") or {}
    # Realizer owns compiler form. Keep it; do not overwrite from the move→look table.
    if existing.get("text_primitive"):
        expression["text_primitive"] = existing["text_primitive"]
    if expression.get("text_primitive") == realize.PRIMITIVE_STEP:
        expression["layout_hint"] = "job_aid"
        expression["content_role"] = "step"
    if expression.get("text_primitive") == realize.PRIMITIVE_CALLOUT:
        expression["layout_hint"] = "callout"
        expression["content_role"] = "callout"
    kept = []
    for k in PRESERVED_KEYS:
        if k in existing:
            expression[k] = existing[k]
            kept.append(k)
    if kept:
        stamp["preserved_foreign_keys"] = kept
    stamp["confidence"] = "high"
    stamp["flags"] = ["from_move"]
    if expression.get("text_primitive") == realize.PRIMITIVE_STEP:
        stamp["flags"].append("from_primitive_step")
    if expression.get("text_primitive") == realize.PRIMITIVE_CALLOUT:
        stamp["flags"].append("from_primitive_callout")
    return expression, stamp


def apply_expression(el, expression, stamp):
    """Write only Couturier-owned style keys. Do not mint ids, copy meaning, or touch intent."""
    if "content" in el:
        raise SystemExit(f"{el.get('element_id')}: refusing to keep authored content on an occurrence")
    if expression is None:
        el.pop("expression", None)
    else:
        el["expression"] = expression
    ext = el.setdefault("ext", {})
    ext["couturier"] = stamp
    return el


def validate_elements(elements, schema, atoms_by_id, closed_style_refs, closed_text_primitives):
    v = Draft202012Validator(schema)
    hard = []
    seen = set()
    for el in elements:
        eid = el.get("element_id")
        for err in sorted(v.iter_errors(el), key=lambda e: list(e.path)):
            hard.append(f"{eid}: {err.message}")
        if eid in seen:
            hard.append(f"duplicate element_id {eid}")
        seen.add(eid)
        if "content" in el:
            hard.append(f"{eid}: authored content is forbidden (meaning lives on the atom)")
        cf = el.get("composed_from")
        if cf not in atoms_by_id:
            hard.append(f"{eid}: composed_from {cf} is not in the atom store")
        stamp = (el.get("ext") or {}).get("couturier") or {}
        if stamp.get("policy") != POLICY:
            hard.append(f"{eid}: missing ext.couturier.policy={POLICY}")
        expr = el.get("expression")
        flags = stamp.get("flags") or []
        if "look_unmapped" in flags:
            if expr:
                extra = set(expr) & set(STYLE_KEYS)
                if extra:
                    hard.append(f"{eid}: unmapped look must not bind style keys {sorted(extra)}")
            continue
        if not expr:
            hard.append(f"{eid}: dressed occurrence is missing expression")
            continue
        extra = set(expr) - set(STYLE_KEYS) - set(PRESERVED_KEYS) - {PRIMITIVE_KEY}
        if extra:
            hard.append(f"{eid}: expression has ungoverned keys {sorted(extra)}")
        sr = expr.get("style_ref")
        if sr not in closed_style_refs:
            hard.append(f"{eid}: style_ref {sr!r} is not in primitives.registry.json")
        tp = expr.get("text_primitive")
        if tp not in closed_text_primitives:
            hard.append(f"{eid}: text_primitive {tp!r} is not in primitives.registry.json")
        if "motion_primitive" in expr and "motion_primitive" not in stamp.get("preserved_foreign_keys", []):
            hard.append(f"{eid}: v1 must not invent motion_primitive")
    if hard:
        print("COUTURIER VALIDATION FAILURES:", file=sys.stderr)
        for m in hard:
            print("  x", m, file=sys.stderr)
        raise SystemExit(1)


def assert_no_id_minting(before_ids, after_ids):
    if before_ids != after_ids:
        added = after_ids - before_ids
        removed = before_ids - after_ids
        raise SystemExit(
            f"Couturier must not mint or drop ele_ ids. added={sorted(added)} removed={sorted(removed)}"
        )


def assert_intent_untouched(before, after):
    before_by = {e["element_id"]: e.get("intent") for e in before}
    for el in after:
        old = before_by.get(el["element_id"])
        if el.get("intent") != old:
            raise SystemExit(
                f"{el['element_id']}: Couturier must not rewrite intent "
                f"(was {old}, now {el.get('intent')})"
            )


def assert_distinct_clothes_on_pairs(elements):
    by_atom = defaultdict(list)
    for el in elements:
        by_atom[el["composed_from"]].append(el)
    for aid, group in by_atom.items():
        if len(group) < 2:
            continue
        looks = {(e.get("expression") or {}).get("style_ref") for e in group}
        if len(looks) < 2:
            raise SystemExit(
                f"{aid}: 1:many occurrences must not wear the same style_ref; got {sorted(looks)}. "
                "Run cartographer.py first so extras keep a distinct move."
            )


def selftest(closed_style_refs, closed_text_primitives):
    """Tiny fixture: move → clothes, write contract, 1:many pairs differ, unmapped is honest."""
    results = []

    def atom(aid, text="X"):
        return {
            "atom_id": aid,
            "content_hash": "sha256:" + ("b" * 64),
            "meaning": {"source_locale": "en", "source_text": text, "kind": "procedure"},
            "bindings": {},
            "governance": {"version": 1, "status": "draft"},
        }

    def el(eid, aid, move, extra=False):
        rec = {
            "element_id": eid,
            "composed_from": aid,
            "type": "Course",
            "intent": {"rhetorical": "orient", "move": move, "teaches": ["obj_explain_alsap_purpose"]},
            "governance": {"version": 1, "status": "draft", "owner": "realizer"},
            "ext": {
                "realized_from": {
                    "atom_id": aid,
                    "realizer": "tools/realize.py",
                    "role": "extra" if extra else "primary",
                },
                "cartographer": {
                    "policy": "v1_heuristic_compiler",
                    "tool": "tools/cartographer.py",
                    "confidence": "high",
                    "flags": ["root_title"] + (["extra_occurrence_move_preserved"] if extra else []),
                },
            },
        }
        if extra:
            rec["ext"]["realized_from"]["target_move"] = move
        return rec

    a = atom("atom_sop_x")
    hook = el("ele_sop_x", "atom_sop_x", "hook")
    present = el("ele_sop_x__present", "atom_sop_x", "present", extra=True)
    general = el("ele_sop_x_general", "atom_sop_x_general", "present")
    recall = el("ele_sop_x_general__reinforce", "atom_sop_x_general", "reinforce", extra=True)

    for rec, want_ref, want_tp, want_role in (
        (hook, "brand.opening", "tp_display", "title"),
        (present, "brand.instructional", "tp_body", "body"),
        (recall, "brand.recall", "tp_recall", "retrieval"),
    ):
        expr, stamp = bind_expression(rec, a, closed_style_refs, closed_text_primitives)
        apply_expression(rec, expr, stamp)
        ok = (expr["style_ref"] == want_ref
              and expr["text_primitive"] == want_tp
              and expr["content_role"] == want_role)
        results.append((f"{rec['element_id']} → {want_ref}/{want_tp}/{want_role}", ok, expr))

    results.append(("does not mint a new element_id", hook["element_id"] == "ele_sop_x", hook["element_id"]))
    results.append(("does not copy meaning onto the element", "content" not in hook, ""))
    results.append(("does not steal realized_from", "realized_from" in hook["ext"], ""))
    results.append(("does not steal cartographer", "cartographer" in hook["ext"], ""))
    results.append(("does not rewrite move", hook["intent"]["move"] == "hook", hook["intent"]["move"]))
    results.append(("does not rewrite teaches",
                    hook["intent"].get("teaches") == ["obj_explain_alsap_purpose"],
                    hook["intent"].get("teaches")))
    results.append(("does not bind motion_primitive", "motion_primitive" not in hook["expression"],
                    hook["expression"]))
    results.append(("does not bind layout_primitive", "layout_primitive" not in hook["expression"], ""))
    results.append(("does not bind interaction_primitive",
                    "interaction_primitive" not in hook["expression"], ""))
    results.append(("title pair wears distinct clothes",
                    hook["expression"]["style_ref"] != present["expression"]["style_ref"],
                    f"{hook['expression']['style_ref']} vs {present['expression']['style_ref']}"))
    general_expr, general_stamp = bind_expression(general, a, closed_style_refs, closed_text_primitives)
    apply_expression(general, general_expr, general_stamp)
    results.append(("present vs reinforce are not the same look",
                    general["expression"]["style_ref"] != recall["expression"]["style_ref"],
                    f"{general['expression']['style_ref']} vs {recall['expression']['style_ref']}"))
    results.append(("recall layout_hint is check not recap",
                    recall["expression"]["layout_hint"] == "check",
                    recall["expression"].get("layout_hint")))
    results.append(("same composed_from on title pair",
                    hook["composed_from"] == present["composed_from"] == "atom_sop_x", ""))

    # Preserve a foreign layout_primitive already on the occurrence (Realizer collision).
    dressed = el("ele_sop_y", "atom_sop_y", "present")
    dressed["expression"] = {"layout_primitive": "TITLE_BODY"}
    expr, stamp = bind_expression(dressed, a, closed_style_refs, closed_text_primitives)
    apply_expression(dressed, expr, stamp)
    results.append(("preserves foreign layout_primitive",
                    dressed["expression"].get("layout_primitive") == "TITLE_BODY",
                    dressed["expression"]))
    results.append(("still binds style_ref on that occurrence",
                    dressed["expression"].get("style_ref") == "brand.instructional",
                    dressed["expression"].get("style_ref")))
    results.append(("flags preserved_foreign_keys",
                    stamp.get("preserved_foreign_keys") == ["layout_primitive"],
                    stamp.get("preserved_foreign_keys")))

    # Unmapped move: leave undressed, do not invent a look.
    practice = el("ele_sop_z", "atom_sop_z", "practice")
    expr, stamp = bind_expression(practice, a, closed_style_refs, closed_text_primitives)
    apply_expression(practice, expr, stamp)
    results.append(("unmapped practice is not dressed", "expression" not in practice, practice.get("expression")))
    results.append(("unmapped flagged look_unmapped",
                    "look_unmapped" in stamp.get("flags", []), stamp.get("flags")))
    results.append(("unmapped does not mint an id", practice["element_id"] == "ele_sop_z", ""))

    # Idempotent re-bind.
    again, stamp2 = bind_expression(hook, a, closed_style_refs, closed_text_primitives)
    results.append(("re-bind is stable", again == hook["expression"], again))

    # Realizer-bound step primitive: preserve form, dress as job_aid.
    step = el("ele_sop_x_s1", "atom_sop_x_s1", "present")
    step["expression"] = {"text_primitive": "tp_step"}
    expr, stamp = bind_expression(step, a, closed_style_refs, closed_text_primitives)
    apply_expression(step, expr, stamp)
    results.append(("step primitive is preserved (not overwritten to tp_body)",
                    expr["text_primitive"] == "tp_step", expr.get("text_primitive")))
    results.append(("step layout_hint is job_aid",
                    expr["layout_hint"] == "job_aid", expr.get("layout_hint")))
    results.append(("step content_role is step",
                    expr["content_role"] == "step", expr.get("content_role")))
    results.append(("step still wears instructional style_ref",
                    expr["style_ref"] == "brand.instructional", expr.get("style_ref")))
    results.append(("step flagged from_primitive_step",
                    "from_primitive_step" in stamp.get("flags", []), stamp.get("flags")))

    # Realizer-bound callout primitive: preserve form, dress as why-this callout.
    callout = el("ele_sop_x_purpose__activate", "atom_sop_x_purpose", "activate", extra=True)
    callout["expression"] = {"text_primitive": "tp_callout"}
    expr, stamp = bind_expression(callout, a, closed_style_refs, closed_text_primitives)
    apply_expression(callout, expr, stamp)
    results.append(("callout primitive is preserved (not overwritten to tp_body)",
                    expr["text_primitive"] == "tp_callout", expr.get("text_primitive")))
    results.append(("callout layout_hint is callout",
                    expr["layout_hint"] == "callout", expr.get("layout_hint")))
    results.append(("callout content_role is callout",
                    expr["content_role"] == "callout", expr.get("content_role")))
    results.append(("callout still wears prior style_ref",
                    expr["style_ref"] == "brand.prior", expr.get("style_ref")))
    results.append(("callout flagged from_primitive_callout",
                    "from_primitive_callout" in stamp.get("flags", []), stamp.get("flags")))

    print(f"{'CHECK':<72} RESULT")
    print("-" * 86)
    ok = True
    for name, passed, detail in results:
        ok = ok and passed
        print(f"{name:<72} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
    print("-" * 86)
    print("SELFTEST ALL PASS" if ok else "SELFTEST FAILED")
    if not ok:
        raise SystemExit(1)


def main():
    inject_default_project()
    default_shown = os.environ.get("TRAINSTORM_PROJECT") or (
        str(realize.repo_default_project()) if realize.repo_default_project() else "(pass --project)"
    )
    ap = argparse.ArgumentParser(
        description="Couturier v1 — bind occurrence style keys (move→look map) and re-project the lesson HTML.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="From cgen/trainstorm-core:\n"
               "  python3 tools/couturier.py\n"
               "  python3 tools/couturier.py --project ../astellas/projects/ast_alsap\n"
               "  python3 tools/couturier.py --selftest\n",
    )
    ap.add_argument("--project", default=None,
                    help=f"Atom + occurrence store directory (default: {default_shown})")
    ap.add_argument("--core", default=None, help="trainstorm-core (schemas + vocab)")
    ap.add_argument("--registry", default=None)
    ap.add_argument("--out", help="HTML output path (default: <project>/realized_lesson.html)")
    ap.add_argument("--store", help="Occurrence store directory (default: <project>/occurrences)")
    ap.add_argument("--selftest", action="store_true", help="Run the style-map fixture and exit")
    ap.add_argument("--dry-run", action="store_true", help="Bind and validate; do not write the store or HTML")
    args = ap.parse_args()

    P = harness_paths.resolve() if not args.selftest else harness_paths.resolve_core(args.core)
    if not args.selftest:
        print(harness_paths.announce(P))

    schemas = P["schemas_dir"]
    element_schema = load(schemas / "element.schema.json")
    closed_moves = list(element_schema["properties"]["intent"]["properties"]["move"]["enum"])
    for mv in MOVE_TO_LOOK:
        if mv not in closed_moves:
            raise SystemExit(f"style map move {mv!r} is not in the closed pedagogical vocab")

    registry = load(P["vocab_dir"] / "primitives.registry.json")
    closed_style_refs = registry_keys(registry, "style_ref")
    closed_text_primitives = registry_keys(registry, "text_primitive")
    for row in MOVE_TO_LOOK.values():
        if row["style_ref"] not in closed_style_refs:
            raise SystemExit(f"style map style_ref {row['style_ref']!r} is not in primitives.registry.json")
        if row["text_primitive"] not in closed_text_primitives:
            raise SystemExit(
                f"style map text_primitive {row['text_primitive']!r} is not in primitives.registry.json"
            )

    if args.selftest:
        selftest(closed_style_refs, closed_text_primitives)
        return

    project = P["project_dir"]
    atoms_path = project / "atoms.json"
    if not atoms_path.exists():
        raise SystemExit(f"No atoms.json in project store: {project}")
    store_dir = pathlib.Path(args.store).resolve() if args.store else project / "occurrences"
    elements_path = store_dir / "elements.json"
    if not elements_path.exists():
        raise SystemExit(
            f"No occurrence store at {elements_path}. Run `python3 tools/realize.py` first."
        )
    if elements_path.resolve() == atoms_path.resolve():
        raise SystemExit("refusing to treat atoms.json as the occurrence store")

    atoms_bytes = atoms_path.read_bytes()
    atoms_hash_before = sha256_bytes(atoms_bytes)
    atoms = json.loads(atoms_bytes)
    atoms_by_id = {a["atom_id"]: a for a in atoms if "atom_id" in a}
    if len(atoms_by_id) != len(atoms):
        raise SystemExit("atom store has missing or duplicate atom_id values")

    elements = load(elements_path)
    if not isinstance(elements, list) or not elements:
        raise SystemExit(f"{elements_path} is not a non-empty element list")
    before_ids = {e["element_id"] for e in elements}
    before_intent = [{"element_id": e["element_id"], "intent": e.get("intent")} for e in elements]
    before_cart = {
        e["element_id"]: (e.get("ext") or {}).get("cartographer")
        for e in elements
    }

    realize.refresh_text_primitives(elements, atoms_by_id)

    unmapped = []
    dressed = 0
    for el in elements:
        eid = el["element_id"]
        cf = el.get("composed_from")
        atom = atoms_by_id.get(cf)
        if atom is None:
            raise SystemExit(f"{eid}: composed_from {cf} is not in the atom store")
        expression, stamp = bind_expression(el, atom, closed_style_refs, closed_text_primitives)
        apply_expression(el, expression, stamp)
        if expression is None:
            unmapped.append(eid)
        else:
            dressed += 1

    after_ids = {e["element_id"] for e in elements}
    assert_no_id_minting(before_ids, after_ids)
    assert_intent_untouched(before_intent, elements)
    for el in elements:
        old_cart = before_cart.get(el["element_id"])
        new_cart = (el.get("ext") or {}).get("cartographer")
        if old_cart != new_cart:
            raise SystemExit(f"{el['element_id']}: Couturier must not rewrite ext.cartographer")
    validate_elements(elements, element_schema, atoms_by_id, closed_style_refs, closed_text_primitives)
    assert_distinct_clothes_on_pairs(elements)

    look_counts = Counter(
        (e.get("expression") or {}).get("style_ref") or "undressed" for e in elements
    )
    if dressed < 1:
        raise SystemExit("couturier v1 dressed zero occurrences")

    mf_path = store_dir / "manifest.json"
    occ_manifest = load(mf_path) if mf_path.exists() else {}
    occ_manifest["couturier"] = {
        "policy": POLICY,
        "tool": COUTURIER,
        "spec": SPEC,
        "look_counts": dict(sorted(look_counts.items())),
        "dressed": dressed,
        "unmapped": len(unmapped),
        "element_count": len(elements),
        "registry": "vocab/primitives.registry.json",
        "note": ("v1 map from occurrence move to expression style keys. Couturier "
                 "mints no ids, does not rewrite atoms or intent, and does not bind "
                 "motion / layout_primitive / interaction_primitive. Realizer owns "
                 "text_primitive (compiler form); this tool preserves it and writes "
                 "style_ref / content_role / layout_hint. HTML reads these "
                 "keys for clothes; meaning stays on the atom. Lesson spine is Realizer "
                 "projection; this tool does not pick the path."),
    }

    html_path = pathlib.Path(args.out).resolve() if args.out else project / "realized_lesson.html"

    if args.dry_run:
        print(f"Couturier v1 DRY-RUN → {len(elements)} elements ({POLICY})")
        print(f"  looks      : {dict(sorted(look_counts.items()))}")
        print(f"  dressed    : {dressed}  ·  unmapped: {len(unmapped)}")
        print("  no files written")
        return

    realize.apply_spine(occ_manifest, atoms, elements)
    realize.stamp_primitives(occ_manifest, elements)
    elements_path.write_text(json.dumps(elements, indent=2) + "\n")
    mf_path.write_text(json.dumps(occ_manifest, indent=2) + "\n")
    coverage_path = realize.project_html(atoms, elements, occ_manifest, html_path)
    mf_path.write_text(json.dumps(occ_manifest, indent=2) + "\n")

    atoms_hash_after = sha256_bytes(atoms_path.read_bytes())
    if atoms_hash_after != atoms_hash_before:
        raise SystemExit("atoms.json changed during couturier — abort. Couturier must not rewrite atoms.")

    print(f"Couturier v1 → {len(elements)} elements ({POLICY})")
    print(f"  atoms        : {atoms_path} ({len(atoms)} records, unchanged)")
    print(f"  occurrences  : {elements_path}")
    print(f"  manifest     : {mf_path}")
    print(f"  lesson HTML  : {html_path}  ← short spine")
    print(f"  coverage     : {coverage_path}")
    print(f"  looks        : {dict(sorted(look_counts.items()))}")
    print(f"  dressed      : {dressed}  ·  unmapped: {len(unmapped)}")
    extras = [e for e in elements if realize.is_extra_element(e)]
    if extras:
        bits = []
        for e in extras:
            mv = (e.get("intent") or {}).get("move", "?")
            look = (e.get("expression") or {}).get("style_ref", "undressed")
            bits.append(f"{e['element_id']}={mv}/{look}")
        print(f"  extras kept  : {len(extras)} ({', '.join(bits)})")
    print("  schema       : element.schema.json ALL PASS (expression style keys; no authored content.text)")


if __name__ == "__main__":
    main()
