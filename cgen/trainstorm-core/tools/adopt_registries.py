#!/usr/bin/env python3
"""
Adoption step — promote a project's PROPOSED extensions UP into the governed registries
(the Astellas client namespace), by entry + version bump.

What crosses the line on promotion: the id AND the label (the display name the projection
needs). What stays behind: the review-only `note` (the argument for adoption). This is the
concrete answer to "is the label just for review?" — no: the note is review-only, the label
is promoted into the governed record.

Idempotent: an id already governed is skipped (no duplicate, no version bump).
Emits registry_adds/<key>.add.json — the delta to commit to the repo registries.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCH = ROOT / "schemas"
STORE = ROOT / "store" / "projects" / "ast_alsap"
ADDS = ROOT / "registry_adds"; ADDS.mkdir(exist_ok=True)

proposed = json.loads((STORE / "proposed_registry_extensions.json").read_text())

def adopt(reg_file, key, proposed_items):
    reg = json.loads((SCH / reg_file).read_text())
    existing = {e["id"] for e in reg[key]}
    added = []
    for it in proposed_items:
        if it["id"] in existing:
            continue
        entry = {"id": it["id"], "label": it["label"]}   # `note` is intentionally dropped
        if "source_number" in it:
            entry["source_number"] = it["source_number"]
        reg[key].append(entry)
        added.append(it["id"])
    if added:
        reg[key] = sorted(reg[key], key=lambda e: e["id"])
        reg["version"] = reg.get("version", 1) + 1
    (SCH / reg_file).write_text(json.dumps(reg, indent=2, ensure_ascii=False))
    # The add-payload is the exact committable delta: the FULL governed entries for the
    # promoted ids (id + label + description / source_number), not just their ids.
    by_id = {e["id"]: e for e in reg[key]}
    entries = [by_id[i["id"]] for i in proposed_items if i["id"] in by_id]
    (ADDS / f"{key}.add.json").write_text(json.dumps({
        "registry": reg_file,
        "version_after": reg.get("version"),
        "dropped_from_proposal": ["note"],
        "entries": entries
    }, indent=2, ensure_ascii=False))
    return added

r = adopt("roles.registry.json", "roles", proposed["roles"])
rec = adopt("records.registry.json", "records", proposed["records"])
d = adopt("docs.registry.json", "docs", proposed["docs"])

print(f"Adopted (new this run) → roles +{len(r)}, records +{len(rec)}, docs +{len(d)}")
print("id + label promoted into the registries; review-only `note` dropped.")
print(f"Commit payloads written to {ADDS}/")
