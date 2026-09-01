#!/usr/bin/env python3
"""
The dossier gate — Strategist open-project warrant snapshot.

The operating prompt proposes (or a human hand-authors) a durable dossier, not atoms
and not a live goals-store write. This gate is the bookkeeping that makes HITL real:

    SCHEMA        — the document validates against schemas/dossier.schema.json.
    WARRANT       — open_project: three questions + outcome + Q1 human_case, consistent.
                    direct_escape: recorded SOP-course escape, no pretended warrant.
    HITL          — status is proposed until a human validates. validated requires a
                    human-shaped reviewer; the agent never sets it.
    NOT AN ATOM   — dossier_id is doss_; no atom_ / obj_ / cd_ identity; no
                    meaning.source_text dump; no occurrence facets.
    PII           — no person-shaped keys; no email-looking values.
    EXAMPLE       — a fixture marked EXAMPLE stays proposed (not a live engagement).
    NO COMPILER   — tools/strategist.py must not exist.

What it does NOT do: write a dossier, mint atoms, write ontology/goals.json, or
promote proposed→validated. The only promoter is the human-run
tools/dossier_accept.py --by. There is no strategist.py.

    python3 tools/validate_dossier.py --selftest
    python3 tools/validate_dossier.py --file reference/example_dossier.json
"""
import argparse, json, re, sys, pathlib
from jsonschema import Draft202012Validator
import harness_paths

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--core")
ap.add_argument("--file")
ap.add_argument("--selftest", action="store_true")
args, _ = ap.parse_known_args()

P = harness_paths.resolve_core(args.core)
HERE = pathlib.Path(__file__).resolve().parent
schema_p = P["schemas_dir"] / "dossier.schema.json"
if not schema_p.exists():
    raise SystemExit(f"not found: {schema_p}")
schema = json.loads(schema_p.read_text(encoding="utf-8"))
V = Draft202012Validator(schema)

AGENT_SHAPED = re.compile(
    r"(headwater|strategist|case[_\-]?author|dramaturge|dragoman|chameleon|"
    r"realizer|cartographer|couturier|amanuensis|griot|responsive_engine|"
    r"audience_agent|\.py\b|claude|grok|chatgpt|copilot|cursor|app-maker)",
    re.I,
)
HUMAN_HANDLE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{0,40}$")
EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PII_KEYS = {
    "name", "email", "full_name", "first_name", "last_name", "ssn", "phone",
    "person", "persons", "learner_name", "employee_name", "pii",
}
SMUGGLE_KEYS = {
    "meaning", "source_text", "atom_id", "content_hash", "bindings",
    "ele_id", "element_id", "objectives", "atoms",
}
OCCURRENCE_KEYS = {"intent", "expression", "audience"}
NESTED_BANNED = SMUGGLE_KEYS | OCCURRENCE_KEYS | PII_KEYS
VERDICTS = {"pass", "partial", "fail"}
OUTCOMES = {"full_pass", "partial_pass", "full_fail"}
NO_GOAL_FINDINGS = {"no_course", "not_this_course", "direct_escape"}


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


def is_example_fixture(doc):
    note = str(doc.get("_note") or "")
    return "EXAMPLE" in note.upper()


def schema_compile_row():
    try:
        Draft202012Validator.check_schema(schema)
        return ("dossier.schema is valid Draft 2020-12", True, "")
    except Exception as e:
        return ("dossier.schema is valid Draft 2020-12", False, str(e))


def warrant_complete(w):
    if not isinstance(w, dict):
        return False, "warrant missing"
    for key in ("value_evidence", "adoption_legitimacy", "cynicism_audit"):
        q = w.get(key) or {}
        if q.get("verdict") not in VERDICTS:
            return False, f"{key} missing verdict"
        if not str(q.get("rationale") or "").strip():
            return False, f"{key} missing rationale"
    if not str((w.get("value_evidence") or {}).get("human_case") or "").strip():
        return False, "Q1 human_case missing"
    if w.get("outcome") not in OUTCOMES:
        return False, "outcome missing"
    return True, ""


def warrant_consistent(w):
    v1 = (w.get("value_evidence") or {}).get("verdict")
    v2 = (w.get("adoption_legitimacy") or {}).get("verdict")
    v3 = (w.get("cynicism_audit") or {}).get("verdict")
    fails = [v for v in (v1, v2, v3) if v == "fail"]
    outcome = w.get("outcome")
    q3 = w.get("cynicism_audit") or {}
    if len(fails) >= 2:
        return outcome == "full_fail", "two or more fails must be full_fail"
    if v1 == "pass" and v2 == "pass" and v3 == "fail":
        ok = outcome == "partial_pass" and q3.get("trust_repair") is True
        return ok, "Q3 fail with Q1+Q2 pass is trust-repair / partial_pass"
    if all(v == "pass" for v in (v1, v2, v3)):
        return outcome == "full_pass", "all-pass must be full_pass"
    return outcome == "partial_pass", "partials / single fail must be partial_pass"


def finding_consistent(doc):
    door = doc.get("door")
    finding = doc.get("finding")
    goals = doc.get("proposed_goals") or []
    if door == "direct_escape":
        if finding != "direct_escape":
            return False, f"finding={finding!r} (want direct_escape)"
        if goals:
            return False, "Direct escape must not mint decorative goal_ sketches"
        return True, ""
    w = doc.get("warrant") or {}
    outcome = w.get("outcome")
    if outcome == "full_fail":
        if finding not in ("no_course", "not_this_course"):
            return False, f"full_fail finding={finding!r}"
        if goals:
            return False, "no-course terminal must not mint decorative goal_ sketches"
        return True, ""
    if outcome in ("full_pass", "partial_pass"):
        if finding != "course_warranted":
            return False, f"{outcome} finding={finding!r}"
        return True, ""
    return False, f"outcome={outcome!r}"


def pii_hits(doc):
    keys = []
    for k in walk_keys(doc):
        leaf = k.split(".")[-1]
        if leaf in PII_KEYS:
            keys.append(k)
    emails = []
    for val in walk_values(doc):
        if isinstance(val, str) and EMAIL.search(val):
            emails.append(val[:80])
    return keys, emails


def smuggled_identity(doc):
    did = str(doc.get("dossier_id") or "")
    bad = []
    if not re.match(r"^doss_[a-z0-9_]+$", did):
        bad.append(f"dossier_id={did!r}")
    for prefix in ("atom_", "obj_", "cd_", "ele_"):
        if did.startswith(prefix):
            bad.append(f"dossier_id uses {prefix}")
    for val in walk_values(doc):
        if isinstance(val, str) and val.startswith("atom_"):
            bad.append(val)
        if isinstance(val, str) and val.startswith("obj_") and not val.startswith("obj_x"):
            # obj_ as an identity token (not prose). Skip short false friends.
            if re.match(r"^obj_[a-z0-9_]+$", val):
                bad.append(val)
    return bad


def gate_doc(name, doc, results):
    """Append results for one dossier dict. Importable; writes nothing."""
    errs = sorted(V.iter_errors(doc), key=lambda e: list(e.path))
    results.append((f"{name}: validates against schema", not errs,
                    "; ".join(e.message for e in errs)[:180]))
    if errs:
        return

    did = doc.get("dossier_id", "")
    results.append((f"{name}: dossier_id is doss_, not atom_/obj_/cd_/ele_",
                    bool(re.match(r"^doss_[a-z0-9_]+$", did)),
                    f"dossier_id={did!r}"))

    keys = set(walk_keys(doc))
    # audience_segment is a legal nested object; the banned leaf is occurrence 'audience'
    smuggled = []
    for k in keys:
        leaf = k.split(".")[-1]
        if leaf in NESTED_BANNED and leaf != "audience":
            smuggled.append(k)
        if k == "audience" or k.startswith("audience.") and not k.startswith("audiences"):
            smuggled.append(k)
    results.append((f"{name}: no smuggled atom meaning, obj_ store, or occurrence facets",
                    not smuggled, "banned keys: " + ", ".join(smuggled[:8])))

    ident = smuggled_identity(doc)
    # proposed_goals[].goal_id is a legal goal_ sketch, not an atom/obj mint
    ident = [x for x in ident if not str(x).startswith("goal_")]
    results.append((f"{name}: no atom_/obj_ identity on the dossier node",
                    not ident, ", ".join(str(x) for x in ident[:6])))

    pii_k, pii_e = pii_hits(doc)
    results.append((f"{name}: no PII-looking person keys or emails",
                    not pii_k and not pii_e,
                    "keys=" + ",".join(pii_k[:6]) + " emails=" + ",".join(pii_e[:3])))

    door = doc.get("door")
    if door == "open_project":
        w = doc.get("warrant") or {}
        ok, why = warrant_complete(w)
        results.append((f"{name}: warrant terminal complete (Q1–Q3 + outcome)", ok, why))
        if ok:
            cok, cwhy = warrant_consistent(w)
            results.append((f"{name}: warrant outcome consistent with the three verdicts",
                            cok, cwhy))
            fok, fwhy = finding_consistent(doc)
            results.append((f"{name}: finding matches warrant terminal", fok, fwhy))
        results.append((f"{name}: open_project has no direct_escape block",
                        "direct_escape" not in doc, ""))
    elif door == "direct_escape":
        de = doc.get("direct_escape") or {}
        results.append((f"{name}: Direct escape recorded (sop_course + rationale)",
                        de.get("escape_kind") == "sop_course"
                        and bool(str(de.get("rationale") or "").strip()),
                        f"escape={de!r}"[:120]))
        fok, fwhy = finding_consistent(doc)
        results.append((f"{name}: finding is direct_escape (no pretended warrant)",
                        fok, fwhy))
        status = doc.get("status")
        if status == "proposed":
            results.append((f"{name}: proposed Direct escape has no recorded_by",
                            "recorded_by" not in de, ""))
        elif status == "validated":
            results.append((f"{name}: validated Direct escape recorded_by is human-shaped",
                            human_shaped(de.get("recorded_by")),
                            f"recorded_by={de.get('recorded_by')!r}"))

    status = doc.get("status")
    if status == "validated":
        results.append((f"{name}: validated carries a human-shaped reviewer",
                        human_shaped(doc.get("reviewer")),
                        f"reviewer={doc.get('reviewer')!r}"))
        results.append((f"{name}: example fixture is not a live validated engagement",
                        not is_example_fixture(doc),
                        "EXAMPLE fixtures stay proposed"))
    elif status == "proposed":
        results.append((f"{name}: proposed has no reviewer (agent never validates)",
                        "reviewer" not in doc, ""))

    for g in doc.get("proposed_goals") or []:
        if "status" in g or g.get("status") == "validated":
            results.append((f"{name}: proposed_goals must not auto-validate a goal_",
                            False, "nested status on a goal sketch"))
            break


def report(rows):
    print(f"{'CHECK':<70} RESULT")
    print("-" * 86)
    ok = True
    for nm, passed, detail in rows:
        ok = ok and passed
        print(f"{nm:<70} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
    print("-" * 86)
    print("ALL PASS" if ok else "SOME FAILED")
    return ok


def gate_passes(doc):
    """True iff every gate_doc check for this document passes. Importable; writes nothing."""
    rows = []
    gate_doc("gate", doc, rows)
    return all(ok for _, ok, _ in rows), rows


def strategist_py_absent():
    return not (HERE / "strategist.py").exists()


def load_example():
    p = P["schemas_dir"].parent / "reference" / "example_dossier.json"
    if not p.exists():
        raise SystemExit(f"not found: {p}")
    return json.loads(p.read_text(encoding="utf-8")), p


def main():
    results = [schema_compile_row()]
    results.append(("no tools/strategist.py compiler", strategist_py_absent(),
                    "strategist.py exists — this hop forbids a batch compiler"))

    if args.selftest:
        good, example_p = load_example()
        n0 = len(results)
        gate_doc("fixture(example)", good, results)
        results.append(("selftest: reference example stays proposed and passes",
                        all(ok for _, ok, _ in results[n0:])
                        and good.get("status") == "proposed",
                        f"status={good.get('status')!r} path={example_p}"))

        escape = json.loads(json.dumps(good))
        escape["_note"] = "selftest Direct-escape fixture — not the example file"
        escape["dossier_id"] = "doss_fx_direct_escape_selftest"
        escape["door"] = "direct_escape"
        escape["finding"] = "direct_escape"
        escape["direct_escape"] = {
            "escape_kind": "sop_course",
            "rationale": "This pile is one bounded SOP; the document is the syllabus.",
        }
        escape.pop("warrant", None)
        escape["proposed_goals"] = []
        escape["outcomes"] = []
        n1 = len(results)
        gate_doc("fixture(escape)", escape, results)
        results.append(("selftest: Direct-escape fixture passes",
                        all(ok for _, ok, _ in results[n1:]), ""))

        def red(label, mutate):
            doc = json.loads(json.dumps(good))
            mutate(doc)
            scratch = []
            gate_doc("fixture(red)", doc, scratch)
            caught = any(not ok for _, ok, _ in scratch)
            results.append((label, caught, "" if caught else "mutation was NOT caught"))

        red("selftest: status=validated without human-shaped reviewer is caught (auto-validate)",
            lambda d: d.update(status="validated", reviewer="strategist"))
        red("selftest: agent-shaped reviewer is caught",
            lambda d: d.update(status="validated", reviewer="headwater.case_author"))
        red("selftest: smuggled atom meaning is caught",
            lambda d: d.update(meaning={"source_locale": "en",
                                        "source_text": "the whole corpus dumped here"}))
        red("selftest: atom_ id on the dossier node is caught",
            lambda d: d.update(dossier_id="atom_fx_smuggled"))
        red("selftest: obj_ smuggling as dossier_id is caught",
            lambda d: d.update(dossier_id="obj_fx_smuggled"))
        red("selftest: PII-looking person name field is caught",
            lambda d: d["audiences"].append({"segment_id": "lead_ops",
                                             "label": "Shift leads",
                                             "name": "Jane Doe"}))
        red("selftest: missing warrant terminal is caught",
            lambda d: d.pop("warrant"))
        red("selftest: example fixture cannot auto-validate",
            lambda d: d.update(status="validated", reviewer="jake"))
        red("selftest: decorative goal_ on a no-course terminal is caught",
            lambda d: d.update(
                warrant={
                    **d["warrant"],
                    "value_evidence": {**d["warrant"]["value_evidence"], "verdict": "fail"},
                    "adoption_legitimacy": {**d["warrant"]["adoption_legitimacy"], "verdict": "fail"},
                    "outcome": "full_fail",
                },
                finding="no_course",
            ))

        sys.exit(0 if report(results) else 1)

    if args.file:
        path = pathlib.Path(args.file)
        if not path.exists():
            raise SystemExit(f"not found: {path}")
        doc = json.loads(path.read_text(encoding="utf-8"))
        gate_doc(path.name, doc, results)
        sys.exit(0 if report(results) else 1)

    results.append(("no --file — contract-only pass", True,
                    "schema compiled; pass --selftest or --file to gate a document"))
    sys.exit(0 if report(results) else 1)


if __name__ == "__main__":
    main()
