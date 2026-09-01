#!/usr/bin/env python3
"""
The committed-design gate — Case-Author stage-1 contract.

Headwater Case-Author scope-commit emits a durable selection-plus-framing node, not atoms.
This gate is the bookkeeping that makes the mint-wake condition real rather than prompt fiction:

    SCHEMA        — the document validates against schemas/committed-design.schema.json.
    JOIN          — warrant_join is exactly one of: a held warrant (goal_ ref) or a recorded
                    SOP-course Direct escape. Not neither. Not both.
    HITL          — status is proposed until a human validates. validated requires a
                    human-shaped reviewer; the agent never sets it.
    NOT AN ATOM   — design_id is cd_; no atom_ id on the node; no meaning.source_text dump;
                    no occurrence intent/expression/audience.
    TERMINAL      — an unreachable-LO goal (empty trainable slice) is not a held warrant;
                    status=validated against it is not mint-ready.

What it does NOT do: write a committed-design, mint atoms, or promote proposed→validated.
The propose writer is tools/headwater_case_author.py; the only promoter is the human-run
tools/committed_design_accept.py --by. Stage-2 mint still does not exist.

    python3 tools/validate_committed_design.py --selftest
    python3 tools/validate_committed_design.py --file schemas/committed-design.example.json
    python3 tools/validate_committed_design.py --project ../brunswick/projects/paytrans

With --project and no committed-design document present, the run is a contract-only pass
(schema compiles) and says so — live client designs are optional (fixture-only this hop).
"""
import argparse, json, re, sys
from jsonschema import Draft202012Validator
import harness_paths

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--core")
ap.add_argument("--project")
ap.add_argument("--file")
ap.add_argument("--selftest", action="store_true")
args, _ = ap.parse_known_args()

P = harness_paths.resolve_core(args.core)
schema_p = P["schemas_dir"] / "committed-design.schema.json"
if not schema_p.exists():
    raise SystemExit(f"not found: {schema_p}")
schema = json.loads(schema_p.read_text(encoding="utf-8"))
V = Draft202012Validator(schema)

AGENT_SHAPED = re.compile(
    r"(headwater|strategist|case[_\-]?author|dramaturge|dragoman|chameleon|"
    r"realizer|cartographer|couturier|amanuensis|griot|responsive_engine|"
    r"audience_agent|\.py\b)",
    re.I,
)
HUMAN_HANDLE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{0,40}$")
ATOM_PREFIX = re.compile(r"^atom_")
SMUGGLE_KEYS = {"meaning", "source_text", "atom_id", "content_hash", "bindings"}
OCCURRENCE_KEYS = {"intent", "expression", "audience"}
# occurrence facets that may appear as nested keys on this node (never legal here)
NESTED_BANNED = SMUGGLE_KEYS | OCCURRENCE_KEYS | {"ele_id", "element_id"}


def walk_keys(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield path + k
            yield from walk_keys(v, path + k + ".")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_keys(v, path + f"[{i}].")


def walk_values(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk_values(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_values(v)
    else:
        yield obj


def human_shaped(value):
    if not isinstance(value, str) or not value.strip():
        return False
    if AGENT_SHAPED.search(value):
        return False
    return bool(HUMAN_HANDLE.match(value.strip()))


def trainable_substance(goal):
    if not isinstance(goal, dict):
        return False
    reach = goal.get("reachability") or {}
    trainable = reach.get("trainable")
    return isinstance(trainable, str) and bool(trainable.strip())


def schema_compile_row():
    try:
        Draft202012Validator.check_schema(schema)
        return ("committed-design.schema is valid Draft 2020-12", True, "")
    except Exception as e:
        return ("committed-design.schema is valid Draft 2020-12", False, str(e))


def gate_doc(name, doc, results, goals_by_id=None):
    """Append results for one committed-design dict. goals_by_id is optional {goal_id: goal}."""
    errs = sorted(V.iter_errors(doc), key=lambda e: list(e.path))
    results.append((f"{name}: validates against schema", not errs,
                    "; ".join(e.message for e in errs)[:180]))
    if errs:
        return

    did = doc.get("design_id", "")
    results.append((f"{name}: design_id is cd_, not atom_/ele_",
                    bool(re.match(r"^cd_[a-z0-9_]+$", did)) and not ATOM_PREFIX.match(did),
                    f"design_id={did!r}"))

    keys = set(walk_keys(doc))
    smuggled = sorted(k for k in keys if k.split(".")[-1] in NESTED_BANNED
                      or k in NESTED_BANNED)
    # framing/warrant may legally mention goal/obj refs; that's not smuggling meaning
    results.append((f"{name}: no smuggled atom meaning or occurrence facets",
                    not smuggled, "banned keys: " + ", ".join(smuggled[:8])))

    atomish = []
    if "atom_id" in doc or str(did).startswith("atom_"):
        atomish.append("design node identity")
    for val in walk_values(doc):
        if isinstance(val, str) and val.startswith("atom_"):
            # inventory / framing must not hang identity on an atom_
            atomish.append(val)
    results.append((f"{name}: no atom_ id on the design node",
                    not atomish, ", ".join(atomish[:6])))

    wj = doc.get("warrant_join") or {}
    kind = wj.get("kind")
    has_warrant = kind == "held_warrant" and bool(wj.get("goal_id"))
    has_escape = kind == "direct_escape" and bool(wj.get("escape_kind"))
    results.append((f"{name}: warrant-or-escape (exactly one)",
                    (has_warrant ^ has_escape),
                    f"kind={kind!r}"))

    if has_escape:
        results.append((f"{name}: Direct escape recorded_by is human-shaped",
                        human_shaped(wj.get("recorded_by")),
                        f"recorded_by={wj.get('recorded_by')!r}"))

    status = doc.get("status")
    if status == "validated":
        results.append((f"{name}: validated carries a human-shaped reviewer",
                        human_shaped(doc.get("reviewer")),
                        f"reviewer={doc.get('reviewer')!r}"))
        if has_warrant:
            gid = wj["goal_id"]
            goal = (goals_by_id or {}).get(gid)
            if goals_by_id is not None:
                results.append((f"{name}: held goal_ {gid} exists",
                                goal is not None, "no such goal in store"))
            if goal is not None:
                results.append((f"{name}: held goal_ is status validated",
                                goal.get("status") == "validated",
                                f"goal status={goal.get('status')!r}"))
                results.append((f"{name}: held goal_ is not an unreachable-LO terminal",
                                trainable_substance(goal),
                                "empty trainable slice — not validated for mint"))
    elif status == "proposed":
        results.append((f"{name}: proposed has no reviewer (agent never validates)",
                        "reviewer" not in doc, ""))


def report(rows):
    print(f"{'CHECK':<66} RESULT")
    print("-" * 82)
    ok = True
    for nm, passed, detail in rows:
        ok = ok and passed
        print(f"{nm:<66} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
    print("-" * 82)
    print("ALL PASS" if ok else "SOME FAILED")
    return ok


def gate_passes(doc, goals_by_id=None):
    """True iff every gate_doc check for this document passes. Importable; writes nothing."""
    rows = []
    gate_doc("gate", doc, rows, goals_by_id)
    return all(ok for _, ok, _ in rows), rows


def _load_goals_for(doc):
    goals = None
    goals_p = P["schemas_dir"].parent / "ontology" / "goals.json"
    if goals_p.exists() and (doc.get("warrant_join") or {}).get("kind") == "held_warrant":
        store = json.loads(goals_p.read_text(encoding="utf-8"))
        gid = (doc.get("warrant_join") or {}).get("goal_id")
        if gid in store.get("goals", {}):
            goals = store["goals"]
    return goals


def main():
    results = [schema_compile_row()]

    if args.selftest:
        GOALS = {
            "goal_fx_held": {
                "label": "Operators follow the work instruction without inventing steps.",
                "measure": "Audit count of skipped-step incidents on the procedure.",
                "reachability": {
                    "trainable": "Knowing the steps and the verification gate.",
                    "not_trainable": ["Staffing on the line."],
                    "assessed_by": "role_ops_lead",
                },
                "status": "validated",
            },
            "goal_fx_terminal": {
                "label": "Reduce complaints 20%.",
                "measure": "Monthly complaint volume.",
                "reachability": {
                    "trainable": "",
                    "not_trainable": ["Process, staffing, incentives."],
                    "assessed_by": "role_ops_lead",
                },
                "status": "validated",
            },
        }
        good = {
            "schema_version": "committed-design.v0.1",
            "store": "committed-design",
            "design_id": "cd_fx_selftest",
            "version": 1,
            "status": "proposed",
            "client": "fx",
            "project": "selftest",
            "proposed_by": "headwater.case_author",
            "derived_from": {
                "source_store": "fx/projects/selftest/source",
                "inventory_refs": [{"id": "doc_fx_sop", "registry": "docs"}],
            },
            "selection": {
                "in_scope": [{"id": "doc_fx_sop", "registry": "docs"}],
                "left_in_source_store": [],
            },
            "framing": {"shape": "One bounded SOP: mint the procedure and its steps."},
            "warrant_join": {"kind": "held_warrant", "goal_id": "goal_fx_held"},
        }
        n0 = len(results)
        gate_doc("fixture(good)", good, results, GOALS)
        results.append(("selftest: clean fixture passes every check",
                        all(ok for _, ok, _ in results[n0:]), ""))

        escape = json.loads(json.dumps(good))
        escape["warrant_join"] = {
            "kind": "direct_escape",
            "escape_kind": "sop_course",
            "recorded_by": "jake",
            "rationale": "This pile is one bounded SOP; the document is the syllabus.",
        }
        n1 = len(results)
        gate_doc("fixture(escape)", escape, results, GOALS)
        results.append(("selftest: Direct-escape fixture passes",
                        all(ok for _, ok, _ in results[n1:]), ""))

        def red(label, mutate, goals=None):
            doc = json.loads(json.dumps(good))
            g = json.loads(json.dumps(GOALS if goals is None else goals))
            mutate(doc, g)
            scratch = []
            gate_doc("fixture(red)", doc, scratch, g)
            caught = any(not ok for _, ok, _ in scratch)
            results.append((label, caught, "" if caught else "mutation was NOT caught"))

        red("selftest: missing warrant-and-escape is caught",
            lambda d, g: d.pop("warrant_join"))
        red("selftest: status=validated without human-shaped reviewer is caught",
            lambda d, g: d.update(status="validated", reviewer="headwater.case_author"))
        red("selftest: smuggled atom meaning is caught",
            lambda d, g: d.update(meaning={"source_locale": "en",
                                           "source_text": "the whole corpus dumped here"}))
        red("selftest: atom_ id on the design node is caught",
            lambda d, g: d.update(design_id="atom_fx_smuggled"))
        red("selftest: unreachable-LO terminal is not validated for mint",
            lambda d, g: d.update(status="validated", reviewer="jake",
                                  warrant_join={"kind": "held_warrant",
                                                "goal_id": "goal_fx_terminal"}))

        sys.exit(0 if report(results) else 1)

    # --file: gate one document (the schema example, or a draft). No live goal store required
    # unless ontology/goals.json is present AND the join is held_warrant — then join it.
    if args.file:
        path = __import__("pathlib").Path(args.file)
        if not path.exists():
            raise SystemExit(f"not found: {path}")
        doc = json.loads(path.read_text(encoding="utf-8"))
        gate_doc(path.name, doc, results, _load_goals_for(doc))
        sys.exit(0 if report(results) else 1)

    # --project (or default resolve): contract-only when no design is on disk.
    try:
        PP = harness_paths.resolve()
        proj = PP["project_dir"]
    except SystemExit:
        results.append(("no --project / --file — contract-only pass", True,
                        "schema compiled; pass --selftest, --file, or --project to gate a document"))
        sys.exit(0 if report(results) else 1)

    candidates = []
    root = proj / "committed-design.json"
    if root.exists():
        candidates.append(root)
    dd = proj / "committed-design"
    if dd.is_dir():
        candidates.extend(sorted(dd.glob("*.json")))
    if not candidates:
        results.append(("no committed-design in project — contract-only pass", True,
                        f"looked at {root} and {dd}"))
        sys.exit(0 if report(results) else 1)

    goals = None
    goals_p = P["schemas_dir"].parent / "ontology" / "goals.json"
    if goals_p.exists():
        goals = json.loads(goals_p.read_text(encoding="utf-8")).get("goals", {})
    for p in candidates:
        gate_doc(p.name, json.loads(p.read_text(encoding="utf-8")), results, goals)
    sys.exit(0 if report(results) else 1)


if __name__ == "__main__":
    main()
