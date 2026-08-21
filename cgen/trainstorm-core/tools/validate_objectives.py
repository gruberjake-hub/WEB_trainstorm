"""
The intent-ontology gate — Cartographer's gate. Covers the whole WARRANT CHAIN:

    goal_  --(reachability)-->  obj_  --(teaches)-->  content

Extended 2026-08-21 when the chain gained its top rung. Filename kept because Cartographer's prompt
cites it; scope is now goals + objectives + the link between them + the intent vocab mirrors.

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
_gschema_p = P["schemas_dir"] / "goal.schema.json"
_gstore_p = P["core_dir"] / "ontology" / "goals.json"
_vocab_p = P["vocab_dir"] / "intent.enum.json"
_elem_p = P["schemas_dir"] / "element.schema.json"
for _p in (_schema_p, _store_p, _gschema_p, _gstore_p, _vocab_p, _elem_p):
    if not _p.exists():
        raise SystemExit(f"not found: {_p}")
schema = json.loads(_schema_p.read_text())
store = json.loads(_store_p.read_text())
gschema = json.loads(_gschema_p.read_text())
gstore = json.loads(_gstore_p.read_text())
vocab = json.loads(_vocab_p.read_text())
element = json.loads(_elem_p.read_text())
print(f"goals     : {_gstore_p}\nobjectives: {_store_p}\n")

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

# --- The warrant chain (added 2026-08-21) ---

gv = Draft202012Validator(gschema)

# 8. The goal schema is itself valid, and the goal store validates
try:
    Draft202012Validator.check_schema(gschema)
    results.append(("goal schema is valid Draft 2020-12", True, ""))
except Exception as e:
    results.append(("goal schema is valid Draft 2020-12", False, str(e)))
gerrs = sorted(gv.iter_errors(gstore), key=lambda e: e.path)
results.append(("goal store validates against goal schema", not gerrs,
                "; ".join(e.message for e in gerrs)))

# 9. EVERY goal carries a reachability judgment. The schema requires it; assert it here too, because
#    this is the hard gate and a gate stated in only one place is a gate someone will route around.
goal_ids = set(gstore["goals"].keys())
no_reach = [g for g, n in gstore["goals"].items() if not n.get("reachability", {}).get("trainable")]
results.append(("every goal names what training CAN move", not no_reach, f"missing: {no_reach}"))
no_not = [g for g, n in gstore["goals"].items() if "not_trainable" not in n.get("reachability", {})]
results.append(("every goal names what training will NOT fix", not no_not, f"missing: {no_not}"))

# 10. serves[] resolves — the warrant link. Same referential check as requires[], one rung up.
dangling_serves = [(oid, g) for oid, node in store["objectives"].items()
                   for g in node.get("serves", []) if g not in goal_ids]
results.append(("every serves[] ref resolves to a real goal", not dangling_serves,
                f"dangling: {dangling_serves}"))

# 11. A VALIDATED objective must carry its warrant. Draft/example may precede the goal; validated
#     may not — that is the promotion gate, and it is where "derived, not asserted" gets enforced.
unwarranted = [oid for oid, n in store["objectives"].items()
               if n.get("status") == "validated" and not n.get("serves")]
results.append(("no validated objective lacks a warrant (serves)", not unwarranted,
                f"unwarranted: {unwarranted}"))

# 12. Vocab mirrors. element.intent inlines two enums that intent.enum.json owns. Nothing else checks
#     this — validate_atoms.py mirrors the procedure/form facets and never loads element.schema.json.
def _mirror(name, inline, governed):
    ok = set(inline) == set(governed)
    results.append((f"element.intent.{name} mirrors intent.enum {name}", ok,
                    f"schema-only={sorted(set(inline)-set(governed))}, "
                    f"vocab-only={sorted(set(governed)-set(inline))}"))
_ei = element["properties"]["intent"]["properties"]
_mirror("rhetorical", _ei.get("rhetorical", {}).get("enum", []),
        [v["id"] for v in vocab["dimensions"]["rhetorical"]["values"]])
_mirror("move", _ei.get("move", {}).get("enum", []),
        [v["id"] for v in vocab["dimensions"]["pedagogical"]["values"]])

# 13. bloom lives on the objective and NOWHERE else. The 2026-08-21 decision moved it; assert the
#     move stuck, or it quietly reappears the next time someone edits a node schema from memory.
_atom = json.loads((P["schemas_dir"] / "atom.schema.json").read_text())
_ai = _atom["properties"]["bindings"]["properties"]["intent"]["properties"]
results.append(("bloom is on the objective node", "bloom" in schema["$defs"]["objective"]["properties"], ""))
results.append(("bloom is NOT on atom.intent", "bloom" not in _ai, "still present"))
results.append(("bloom is NOT on element.intent", "bloom" not in _ei, "still present"))

# 14. The WORKED EXAMPLES still validate. Added 2026-08-21 because moving `bloom` off both intent
#     bindings silently invalidated reference/example_atom.json and example_element.json, and nothing
#     would have caught it — the stores carry no intent binding, so the gates stayed green while the
#     canonical examples were broken. An example that does not validate is worse than no example: it
#     is a template someone will copy.
for _name, _sch in (("example_atom", _atom), ("example_element", element)):
    _ex_p = P["core_dir"] / "reference" / f"{_name}.json"
    if not _ex_p.exists():
        results.append((f"{_name}.json present", False, "missing"))
        continue
    _errs = sorted(Draft202012Validator(_sch).iter_errors(json.loads(_ex_p.read_text())),
                   key=lambda e: list(e.path))
    results.append((f"{_name}.json validates against its schema", not _errs,
                    "; ".join(e.message for e in _errs)))

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

# 7. An unknown field on a node must be rejected (additionalProperties:false).
#    ROTTED AND REPAIRED 2026-08-21. This case used to pin the rule to `serves` being ungoverned —
#    and `serves` became governed the moment the warrant chain was built, so a correct gate started
#    reporting FAIL. Identical failure to the reg_benefit_risk_profile case on 2026-08-20, and the
#    same standing rule applies: A SELF-TEST ASSERTS A RULE, NEVER THE CURRENT CONTENTS OF A
#    GOVERNED LIST. Retested with a field name chosen never to be governed, plus a companion
#    asserting the now-governed field passes.
bad_field = json.loads(json.dumps(store))
bad_field["objectives"]["obj_define_psi"]["never_a_governed_field"] = "x"
results.append(("unknown node field is rejected (rule, not a named field)",
                bool(list(v.iter_errors(bad_field))), ""))

good_serves = json.loads(json.dumps(store))
results.append(("the now-governed serves[] passes",
                not list(v.iter_errors(good_serves)), ""))

# --- Negative controls for the warrant chain: each new gate must be known to go RED ---

no_reach = json.loads(json.dumps(gstore))
del no_reach["goals"]["goal_ast009_psi_reported_on_time"]["reachability"]
results.append(("a goal with NO reachability judgment is rejected",
                bool(list(gv.iter_errors(no_reach))), ""))

no_notrain = json.loads(json.dumps(gstore))
del no_notrain["goals"]["goal_ast009_psi_reported_on_time"]["reachability"]["not_trainable"]
results.append(("a goal that never says what training will NOT fix is rejected",
                bool(list(gv.iter_errors(no_notrain))), ""))

bad_goal_id = json.loads(json.dumps(gstore))
bad_goal_id["goals"]["reduce_complaints"] = bad_goal_id["goals"]["goal_ast009_psi_reported_on_time"]
results.append(("an ungoverned goal_ prefix is rejected",
                bool(list(gv.iter_errors(bad_goal_id))), ""))

dangle = json.loads(json.dumps(store))
dangle["objectives"]["obj_define_psi"]["serves"] = ["goal_does_not_exist"]
_gids = set(gstore["goals"])
results.append(("a dangling serves[] is caught by the integrity check",
                any(g not in _gids for n in dangle["objectives"].values() for g in n.get("serves", [])), ""))

unwar = json.loads(json.dumps(store))
unwar["objectives"]["obj_define_psi"]["status"] = "validated"
del unwar["objectives"]["obj_define_psi"]["serves"]
results.append(("a VALIDATED objective with no warrant is rejected by the schema",
                bool(list(v.iter_errors(unwar))), ""))

drifted = json.loads(json.dumps(element))
drifted["properties"]["intent"]["properties"]["move"]["enum"].append("improvise")
_gov = [x["id"] for x in vocab["dimensions"]["pedagogical"]["values"]]
results.append(("a drifted element.intent.move mirror is caught",
                set(drifted["properties"]["intent"]["properties"]["move"]["enum"]) != set(_gov), ""))

reappeared = json.loads(json.dumps(_atom))
reappeared["properties"]["bindings"]["properties"]["intent"]["properties"]["bloom"] = {"type": "string"}
results.append(("bloom reappearing on atom.intent is caught",
                "bloom" in reappeared["properties"]["bindings"]["properties"]["intent"]["properties"], ""))

print(f"{'CHECK':<58} RESULT")
print("-" * 72)
ok = True
for name, passed, detail in results:
    ok = ok and passed
    print(f"{name:<58} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
print("-" * 72)
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)