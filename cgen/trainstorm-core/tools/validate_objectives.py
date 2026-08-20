"""
The objective-ontology gate — Cartographer's gate.

The checks below were written and demonstrated on 2026-08-12 (gated 7/7). They then sat unrunnable:
the two paths were hardcoded build-machine absolutes (`/home/claude/objectives.schema.json`), so this
file has never executed inside the repo. Found 2026-08-20 while reconstructing Cartographer, whose
prompt cites this as its gate. Repointed at the shared resolver like every other tool.

    python3 tools/validate_objectives.py [--core <trainstorm-core>]
"""
import json, sys, pathlib
from jsonschema import Draft202012Validator
import harness_paths

import argparse
_ap = argparse.ArgumentParser(add_help=False); _ap.add_argument("--core")
_a, _ = _ap.parse_known_args()
P = harness_paths.resolve_core(_a.core)     # core-only: the ontology is core canon, not project data
_schema_p = P["schemas_dir"] / "objectives.schema.json"
_store_p = P["core_dir"] / "ontology" / "objectives.json"
for _p in (_schema_p, _store_p):
    if not _p.exists():
        raise SystemExit(f"not found: {_p}")
schema = json.loads(_schema_p.read_text())
store = json.loads(_store_p.read_text())
print(f"schema: {_schema_p}\nstore : {_store_p}\n")

results = []

# 1. Schema is itself a valid Draft 2020-12 schema
try:
    Draft202012Validator.check_schema(schema)
    results.append(("schema is valid Draft 2020-12", True, ""))
except Exception as e:
    results.append(("schema is valid Draft 2020-12", False, str(e)))

v = Draft202012Validator(schema)

# 2. The seed store validates against the schema
errs = sorted(v.iter_errors(store), key=lambda e: e.path)
results.append(("seed store validates against schema", not errs,
                "; ".join(e.message for e in errs)))

# 3. Referential integrity: every requires[] id exists in the store
ids = set(store["objectives"].keys())
dangling = [(oid, r) for oid, node in store["objectives"].items()
            for r in node["requires"] if r not in ids]
results.append(("every requires[] ref resolves in-store", not dangling,
                f"dangling: {dangling}"))

# 4. Acyclic prerequisite graph (no objective requires itself, directly or transitively)
def has_cycle(nodes):
    WHITE, GREY, BLACK = 0, 1, 2
    color = {k: WHITE for k in nodes}
    def dfs(u):
        color[u] = GREY
        for w in nodes[u]["requires"]:
            if w not in color:      # dangling handled above
                continue
            if color[w] == GREY:
                return True
            if color[w] == WHITE and dfs(w):
                return True
        color[u] = BLACK
        return False
    return any(color[k] == WHITE and dfs(k) for k in nodes)
results.append(("prerequisite graph is acyclic", not has_cycle(store["objectives"]), ""))

# --- Negative controls: the gates must REJECT bad input ---

# 5. A dangling requires must be catchable (referential check, not schema)
bad_ref = json.loads(json.dumps(store))
bad_ref["objectives"]["obj_recognize_psi"]["requires"] = ["obj_ghost"]
ids2 = set(bad_ref["objectives"].keys())
dangles = any(r not in ids2 for n in bad_ref["objectives"].values() for r in n["requires"])
results.append(("dangling requires is rejected by integrity check", dangles, ""))

# 6. An ungoverned (non-obj_) id must be rejected by the schema
bad_id = json.loads(json.dumps(store))
bad_id["objectives"]["safety_stuff"] = {"label": "x", "requires": [], "framework": "none"}
results.append(("ungoverned id prefix is rejected by schema",
                bool(list(v.iter_errors(bad_id))), ""))

# 7. An unknown field on a node must be rejected (additionalProperties:false)
bad_field = json.loads(json.dumps(store))
bad_field["objectives"]["obj_define_psi"]["serves"] = ["goal_reduce_complaints"]
results.append(("unknown node field (e.g. premature serves) is rejected",
                bool(list(v.iter_errors(bad_field))), ""))

print(f"{'CHECK':<58} RESULT")
print("-" * 72)
ok = True
for name, passed, detail in results:
    ok = ok and passed
    print(f"{name:<58} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
print("-" * 72)
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)