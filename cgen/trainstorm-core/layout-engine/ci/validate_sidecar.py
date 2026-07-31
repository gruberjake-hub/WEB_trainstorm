#!/usr/bin/env python3
"""
validate_sidecar.py — the contract test between an intent sidecar and its template
manifest. Run in CI on every sidecar PR so policy and shell can't silently drift.

Checks:
  1. sidecar conforms to intent_sidecar.schema.json
  2. manifest conforms to template_manifest.schema.json
  3. sidecar.template_ref.sha256 == manifest.template_ref.sha256   (version pin)
  4. every layout id the sidecar references (selection.use, default_layout,
     bindings keys) exists in the manifest
  5. every slot a binding maps into exists on that layout in the manifest

Usage:
  python validate_sidecar.py SIDECAR.json --schema-dir ../_schema
  (manifest path is read from sidecar.template_ref.manifest, relative to sidecar)

Exit 0 = contract holds; non-zero = fail (prints the violations).
"""
import json, sys, os, argparse
from jsonschema import Draft202012Validator


def load(p):
    with open(p) as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sidecar")
    ap.add_argument("--schema-dir", default=os.path.join(os.path.dirname(__file__), "..", "_schema"))
    args = ap.parse_args()

    side = load(args.sidecar)
    side_dir = os.path.dirname(os.path.abspath(args.sidecar))
    man_path = os.path.join(side_dir, side["template_ref"]["manifest"]) \
        if not os.path.isabs(side["template_ref"]["manifest"]) else side["template_ref"]["manifest"]
    # allow manifest path relative to repo root too
    if not os.path.exists(man_path):
        man_path = side["template_ref"]["manifest"]
    man = load(man_path)

    side_schema = load(os.path.join(args.schema_dir, "intent_sidecar.schema.json"))
    man_schema = load(os.path.join(args.schema_dir, "template_manifest.schema.json"))

    errs = []

    for label, obj, schema in [("sidecar", side, side_schema), ("manifest", man, man_schema)]:
        for e in Draft202012Validator(schema).iter_errors(obj):
            errs.append(f"[{label} schema] {list(e.path)}: {e.message}")

    if side["template_ref"]["sha256"] != man["template_ref"]["sha256"]:
        errs.append("[pin] sidecar.template_ref.sha256 != manifest.template_ref.sha256 "
                    "(sidecar was authored against a different .potx build)")

    layouts = {l["id"]: l for l in man["layouts"]}
    referenced = {r["use"] for r in side.get("selection", [])} \
        | ({side["default_layout"]} if side.get("default_layout") else set()) \
        | set(side.get("bindings", {}).keys())
    for lid in sorted(referenced - set(layouts)):
        errs.append(f"[refs] sidecar references layout '{lid}' not present in manifest")

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

    if errs:
        print(f"FAIL — {len(errs)} contract violation(s):")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print("OK — sidecar honors the manifest contract.")


if __name__ == "__main__":
    main()
