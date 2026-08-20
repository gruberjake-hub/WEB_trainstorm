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
import harness_paths

_P = harness_paths.resolve()
SCH = _P["registry_dir"]              # client registries (roles/records/docs) live here
STORE = _P["project_dir"]
ADDS = STORE / "registry_adds"; ADDS.mkdir(exist_ok=True)

proposed = json.loads((STORE / "proposed_registry_extensions.json").read_text())

def adopt(reg_file, key, proposed_items):
    reg = json.loads((SCH / reg_file).read_text())
    existing = {e["id"] for e in reg[key]}
    added = []
    for it in proposed_items:
        if it["id"] in existing:
            continue
        entry = {"id": it["id"], "label": it["label"]}   # `note` is intentionally dropped
        # `description` and `values` are NOT review-only — they are the governed record itself
        # (registries are v3 {id, label, description}; an options entry additionally carries the
        # members of its set). Promote them when the proposal supplies them.
        for k in ("description", "source_number", "values"):
            if k in it:
                entry[k] = it[k]
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

TIERS = [("roles.registry.json", "roles"),
         ("records.registry.json", "records"),
         ("docs.registry.json", "docs"),
         # controlled value sets behind form.options_ref — same client tier, set-shaped entries
         ("options.registry.json", "options")]

counts = {}
for reg_file, key in TIERS:
    items = proposed.get(key) or []
    if not items:
        counts[key] = 0
        continue
    if not (SCH / reg_file).exists():
        # never conjure a governed registry as a side effect of adoption — establishing a
        # vocabulary is its own deliberate act
        raise SystemExit(f"{reg_file} does not exist in {SCH}. Seed the governed registry first "
                         f"(closed_list, version 1, empty {key}[]), then re-run adoption.")
    counts[key] = len(adopt(reg_file, key, items))

print("Adopted (new this run) → " + ", ".join(f"{k} +{v}" for k, v in counts.items()))
print("id + label promoted into the registries; review-only `note` dropped.")
print(f"Commit payloads written to {ADDS}/")
