#!/usr/bin/env python3
"""
Adoption step — promote the project's PROPOSED extensions UP into the governed registries
(the Astellas client namespace), by entry + version bump. Emits:
  - schemas/{roles,records,docs}.registry.json   updated to the post-adoption governed state
  - registry_adds/{roles,records,docs}.add.json  the exact delta to commit to the repo registries

The staging pen (store/.../proposed_registry_extensions.json) is NOT the home for these — after
adoption the project only REFERENCES the now-governed ids. This script is the "approve the adds".
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCH = ROOT / "schemas"
STORE = ROOT / "store" / "projects" / "ast_alsap"
ADDS = ROOT / "registry_adds"; ADDS.mkdir(exist_ok=True)

proposed = json.loads((STORE / "proposed_registry_extensions.json").read_text())

def adopt(reg_file, key, proposed_ids, add_payload):
    reg = json.loads((SCH / reg_file).read_text())
    before = set(reg[key])
    added = [x for x in proposed_ids if x not in before]
    reg[key] = sorted(before | set(proposed_ids))
    reg["version"] = reg.get("version", 1) + (1 if added else 0)
    reg["_note"] = f"Astellas client registry — post-adoption state (v{reg['version']}). Governed."
    (SCH / reg_file).write_text(json.dumps(reg, indent=2, ensure_ascii=False))
    (ADDS / add_payload["file"]).write_text(json.dumps(
        {"registry": reg_file, "version_bump_to": reg["version"], "added": add_payload["items"]},
        indent=2, ensure_ascii=False))
    return added

r = adopt("roles.registry.json", "roles", [x["id"] for x in proposed["roles"]],
          {"file": "roles.add.json", "items": proposed["roles"]})
rec = adopt("records.registry.json", "records", [x["id"] for x in proposed["records"]],
            {"file": "records.add.json", "items": proposed["records"]})
d = adopt("docs.registry.json", "docs", [x["id"] for x in proposed["docs"]],
          {"file": "docs.add.json", "items": proposed["docs"]})

print(f"Adopted → roles +{len(r)}, records +{len(rec)}, docs +{len(d)}")
print(f"Commit payloads written to {ADDS}/")
