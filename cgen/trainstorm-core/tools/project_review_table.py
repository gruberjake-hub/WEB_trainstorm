#!/usr/bin/env python3
"""
Projection #2 — atoms -> SME review matrix (CSV).

The SME never edits JSON. This is the surface they DO edit: one row per procedure step, with the
current source text and an empty `proposed_source_text` column to fill where they want a change.
It reconciles deterministically (match by atom_id), and it's the same matrix shape proven on the
localization round-trip. Word-with-tracked-changes is a richer surface to add later (needs a diff).
"""
import json, csv, pathlib
import harness_paths

_P = harness_paths.resolve()
SCH = _P["registry_dir"]
STORE = _P["project_dir"]
OUT = STORE / "review_matrix.csv"

atoms = json.loads((STORE / "atoms.json").read_text())
roles = {e["id"]: e["label"] for e in json.loads((SCH / "roles.registry.json").read_text())["roles"]}

def clean(t):
    i = t.find("[Headwater")
    return t[:i].strip() if i != -1 else t.strip()

def section_of(a):
    bt = a["bindings"].get("object", {}).get("belongs_to", "")
    return {"atom_sop_ast29080_proc_a": "A", "atom_sop_ast29080_proc_b": "B",
            "atom_sop_ast29080_proc_c": "C"}.get(bt, "")

steps = [a for a in atoms if a["meaning"]["kind"] == "procedure_step"]
steps.sort(key=lambda a: (section_of(a), a["bindings"]["object"].get("order", 0)))

with OUT.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["atom_id", "section", "performed_by", "current_source_text",
                "proposed_source_text", "reviewer_note", "reviewer_id"])
    for a in steps:
        who = " / ".join(roles.get(r, r) for r in a["bindings"]["procedure"].get("performed_by", []))
        w.writerow([a["atom_id"], section_of(a), who, clean(a["meaning"]["source_text"]), "", "", ""])

print(f"Wrote review matrix ({len(steps)} step rows) -> {OUT}")
