#!/usr/bin/env python3
"""
validate_sidecar.py — the contract test between an intent sidecar, its template
manifest, AND the governed Manifold vocabularies. Run in CI on every sidecar PR so
policy, shell, and the canonical vocabularies can't silently drift.

Structural checks (sidecar <-> manifest):
  1. sidecar conforms to intent_sidecar.schema.json
  2. manifest conforms to template_manifest.schema.json
  3. sidecar.template_ref.sha256 == manifest.template_ref.sha256        (version pin)
  4. every layout id the sidecar references exists in the manifest
  5. every slot a binding maps into exists on that layout in the manifest

Manifold conformance checks (sidecar <-> trainstorm-core):
  6. every selection predicate value is a member of its GOVERNED vocabulary
     (script.primitives, intent.enum rhetorical/pedagogical, tone.enum,
      complexity.enum, visual-type.enum, primitives.registry interaction_primitive)
  7. every layout id the sidecar uses is a REGISTERED layout_primitive key
     in primitives.registry.json
  8. every binding fills slots via ELEMENT SELECTORS (objects with `scope`), never
     legacy free-string templates — this is what guarantees the element_id join
  9. selector `where` clauses use governed intent facets (rhetorical/pedagogical)

Governed vocabularies are read from --core-dir (default ../../trainstorm-core), i.e.
the canonical repo, never a copy bundled here. If a vocabulary file is missing, the
axis it governs is SKIPPED with a NOTE rather than passing silently.

Usage:
  python validate_sidecar.py SIDECAR.json [--schema-dir ../../trainstorm-core/schemas] [--core-dir ../../trainstorm-core]

Exit 0 = contract holds (warnings/notes allowed); non-zero = fail (prints violations).
"""
import json, sys, os, argparse

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("FAIL — jsonschema not installed (pip install jsonschema)")
    sys.exit(2)

# Fallback list of the 11 governed script-primitive types, used only if
# script.primitives.v1.json can't be read from --core-dir.
SCRIPT_PRIMITIVE_FALLBACK = [
    "orientation", "context_frame", "definition", "decomposition", "distinction",
    "process_flow", "role_relevance", "knowledge_check", "boundary_statement",
    "resource_pointer", "closure",
]


def load(p):
    with open(p) as f:
        return json.load(f)


def maybe_load(p):
    try:
        return load(p)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def ids_from_enum_values(obj, *path):
    """Pull [].id from a nested list of {id: ...} objects at obj[path...]."""
    cur = obj
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    if isinstance(cur, list):
        return {v["id"] for v in cur if isinstance(v, dict) and "id" in v}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sidecar")
    ap.add_argument("--schema-dir", default=os.path.join(os.path.dirname(__file__), "..", "..", "trainstorm-core", "schemas"))
    ap.add_argument("--core-dir", default=os.path.join(os.path.dirname(__file__), "..", "..", "trainstorm-core"))
    args = ap.parse_args()

    side = load(args.sidecar)
    side_dir = os.path.dirname(os.path.abspath(args.sidecar))
    man_path = os.path.join(side_dir, side["template_ref"]["manifest"]) \
        if not os.path.isabs(side["template_ref"]["manifest"]) else side["template_ref"]["manifest"]
    if not os.path.exists(man_path):
        man_path = side["template_ref"]["manifest"]
    man = load(man_path)

    side_schema = load(os.path.join(args.schema_dir, "intent_sidecar.schema.json"))
    man_schema = load(os.path.join(args.schema_dir, "template_manifest.schema.json"))

    errs, warns, notes = [], [], []

    # ---- 1,2 schema validity -------------------------------------------------
    for label, obj, schema in [("sidecar", side, side_schema), ("manifest", man, man_schema)]:
        for e in Draft202012Validator(schema).iter_errors(obj):
            errs.append(f"[{label} schema] {list(e.path)}: {e.message}")

    # ---- 3 version pin -------------------------------------------------------
    if side["template_ref"]["sha256"] != man["template_ref"]["sha256"]:
        errs.append("[pin] sidecar.template_ref.sha256 != manifest.template_ref.sha256 "
                    "(sidecar was authored against a different .potx build)")

    layouts = {l["id"]: l for l in man["layouts"]}
    referenced = {r["use"] for r in side.get("selection", [])} \
        | ({side["default_layout"]} if side.get("default_layout") else set()) \
        | set(side.get("bindings", {}).keys())

    # ---- 4 layout refs exist -------------------------------------------------
    for lid in sorted(referenced - set(layouts)):
        errs.append(f"[refs] sidecar references layout '{lid}' not present in manifest")

    # ---- 5 slot refs exist ---------------------------------------------------
    for lid, binding in side.get("bindings", {}).items():
        if lid not in layouts:
            continue
        slot_names = {s["name"] for s in layouts[lid]["slots"]}
        for slot in binding.get("map", {}):
            if slot not in slot_names:
                errs.append(f"[slots] binding for '{lid}' maps unknown slot '{slot}'")
        rep = binding.get("repeat")
        if rep and rep["slot"] not in slot_names:
            errs.append(f"[slots] binding for '{lid}' repeats unknown slot '{rep['slot']}'")

    # ---- load governed vocabularies -----------------------------------------
    vocab_dir = os.path.join(args.core_dir, "vocab")
    schemas_dir = os.path.join(args.core_dir, "schemas")

    intent = maybe_load(os.path.join(vocab_dir, "intent.enum.json"))
    tone = maybe_load(os.path.join(vocab_dir, "tone.enum.json"))
    complexity = maybe_load(os.path.join(vocab_dir, "complexity.enum.json"))
    visual = maybe_load(os.path.join(vocab_dir, "visual-type.enum.json"))
    registry = maybe_load(os.path.join(vocab_dir, "primitives.registry.json"))
    sp_schema = maybe_load(os.path.join(schemas_dir, "script.primitives.v1.json"))
    el_schema = maybe_load(os.path.join(schemas_dir, "element.schema.json"))

    rhetorical_ids = ids_from_enum_values(intent, "dimensions", "rhetorical", "values") if intent else None
    pedagogical_ids = ids_from_enum_values(intent, "dimensions", "pedagogical", "values") if intent else None
    tone_ids = ids_from_enum_values(tone, "values") if tone else None
    complexity_ids = ids_from_enum_values(complexity, "values") if complexity else None
    visual_ids = ids_from_enum_values(visual, "values") if visual else None

    interaction_keys = None
    layout_keys = None
    if registry:
        interaction_keys = {e["key"] for e in registry.get("interaction_primitive", []) if isinstance(e, dict)}
        layout_keys = {e["key"] for e in registry.get("layout_primitive", []) if isinstance(e, dict)}

    if sp_schema:
        sp_ids = set()
        for d in (sp_schema.get("$defs") or {}).values():
            t = (d.get("properties", {}).get("type", {}) or {})
            if "const" in t:
                sp_ids.add(t["const"])
        script_primitive_ids = sp_ids or set(SCRIPT_PRIMITIVE_FALLBACK)
    else:
        script_primitive_ids = set(SCRIPT_PRIMITIVE_FALLBACK)
        notes.append("[note] script.primitives.v1.json not found in core-dir; using built-in 11-type fallback.")

    element_types = set((el_schema or {}).get("properties", {}).get("type", {}).get("enum", [])) or None

    # axis -> (allowed set or None-if-skip, human name, core file)
    axis_specs = {
        "script_primitive":     (script_primitive_ids, "script.primitives"),
        "rhetorical":           (rhetorical_ids,       "intent.enum > rhetorical"),
        "pedagogical":          (pedagogical_ids,      "intent.enum > pedagogical"),
        "tone":                 (tone_ids,             "tone.enum"),
        "complexity":           (complexity_ids,       "complexity.enum"),
        "visual_type":          (visual_ids,           "visual-type.enum"),
        "requested_interaction":(interaction_keys,     "primitives.registry > interaction_primitive"),
    }
    for axis, (allowed, name) in axis_specs.items():
        if allowed is None:
            notes.append(f"[note] governed vocabulary for '{axis}' ({name}) not reachable — axis skipped.")

    # ---- 6 governed selection values ----------------------------------------
    for rule in side.get("selection", []):
        when = rule.get("when", {})
        for axis, (allowed, name) in axis_specs.items():
            if allowed is None or axis not in when:
                continue
            for v in when[axis]:
                if v not in allowed:
                    errs.append(f"[vocab] selection rule '{rule['id']}' uses ungoverned {axis} "
                                f"value '{v}' (not in {name})")
        # 10 ungoverned flags warning
        if when.get("flags"):
            warns.append(f"[flags] selection rule '{rule['id']}' matches on ungoverned flags "
                         f"{when['flags']} — promote recurring flags into a governed vocabulary.")

    # ---- 7 layouts are registered layout_primitives -------------------------
    if layout_keys is not None:
        for lid in sorted(referenced):
            if lid not in layout_keys:
                errs.append(f"[registry] layout '{lid}' is used but not a registered "
                            f"layout_primitive in primitives.registry.json")
    else:
        notes.append("[note] primitives.registry.json not reachable — layout registration + interaction axis skipped.")

    # ---- 8 element-selector bindings (the element_id join) ------------------
    def check_selector(sel, ctx):
        if not isinstance(sel, dict) or "scope" not in sel:
            errs.append(f"[binding] {ctx}: expected an element selector object with 'scope', "
                        f"got {type(sel).__name__} — legacy free-field templates are not allowed "
                        f"(they break the element_id join).")
            return
        # 9 governed where-facets
        where = sel.get("where", {})
        if rhetorical_ids is not None:
            for v in where.get("rhetorical", []):
                if v not in rhetorical_ids:
                    errs.append(f"[binding] {ctx}: where.rhetorical '{v}' not in intent.enum > rhetorical")
        if pedagogical_ids is not None:
            for v in where.get("pedagogical", []):
                if v not in pedagogical_ids:
                    errs.append(f"[binding] {ctx}: where.pedagogical '{v}' not in intent.enum > pedagogical")
        if element_types is not None:
            for v in where.get("type", []):
                if v not in element_types:
                    errs.append(f"[binding] {ctx}: where.type '{v}' not in element.schema type enum")

    for lid, binding in side.get("bindings", {}).items():
        for slot, sel in binding.get("map", {}).items():
            check_selector(sel, f"{lid}.map.{slot}")
        rep = binding.get("repeat")
        if rep:
            check_selector(rep.get("source"), f"{lid}.repeat.source")
            for sub, sel in (rep.get("item_map") or {}).items():
                check_selector(sel, f"{lid}.repeat.item_map.{sub}")

    # ---- report --------------------------------------------------------------
    for n in notes:
        print(n)
    for w in warns:
        print("WARN", w)

    if errs:
        print(f"FAIL — {len(errs)} contract violation(s):")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print(f"OK — sidecar honors the manifest + Manifold contract "
          f"({len(warns)} warning(s), {len(notes)} note(s)).")


if __name__ == "__main__":
    main()
