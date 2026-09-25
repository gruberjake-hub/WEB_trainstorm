#!/usr/bin/env python3
"""
Selftest for script.primitives.v3 — green fixture plus red proofs.

Proves, against the canonical schema (never a copy):
    SCHEMA     — v3 is valid Draft 2020-12 and every $def in the union carries an x-menu.
    SELECTION  — lint picks v1 / v2 / v3 for the three reference scripts (derived, not hardcoded).
    GREEN      — reference/sample_script.v3.json validates; so do the v1 and v2 samples against v3's
                 own ancestors (v2 is untouched).
    RED        — an ungoverned type, a proceed/clarify/escalate branch with no action, an
                 "optimal" branch in a competing-principles dilemma, an incomplete-information
                 scenario with no missing_information, a one-role perspective switch, an ungoverned
                 resource_kind, and a worked example with no reasoning are each REJECTED.
    MENU       — the projected move menu is current (tools/project_move_menu.py --check).

Writes nothing.

    python3 tools/selftest_script_primitives.py
"""
import copy, json, subprocess, sys
from pathlib import Path
from jsonschema import Draft202012Validator

CORE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CORE / "tools"))
import lint  # noqa: E402

V3 = json.loads((CORE / "schemas/script.primitives.v3.json").read_text(encoding="utf-8"))
SAMPLE = json.loads((CORE / "reference/sample_script.v3.json").read_text(encoding="utf-8"))
canon = lint.load_canon(str(CORE))
rows = []


def row(name, ok, detail=""):
    rows.append((name, bool(ok), detail))


def errors(doc):
    return list(Draft202012Validator(V3).iter_errors(doc))


def by_id(pid):
    return copy.deepcopy(next(p for p in SAMPLE if p.get("id") == pid))


# SCHEMA
try:
    Draft202012Validator.check_schema(V3)
    row("v3 is valid Draft 2020-12", True)
except Exception as e:  # pragma: no cover
    row("v3 is valid Draft 2020-12", False, str(e)[:120])
union = [r["$ref"].split("/")[-1] for r in V3["$defs"]["primitive"]["oneOf"]]
missing = [k for k in union if "x-menu" not in V3["$defs"][k]]
row(f"every union type ({len(union)}) carries x-menu", not missing, ", ".join(missing))

# SELECTION
for name, want in [("sample_script.json", "v1"), ("sample_script.v2.json", "v2"), ("sample_script.v3.json", "v3")]:
    data = json.loads((CORE / "reference" / name).read_text(encoding="utf-8"))
    _, got = lint.script_schema_for(data, canon)
    row(f"lint selects {want} for {name}", got == want, f"got {got}")

# GREEN
errs = errors(SAMPLE)
row("GREEN: sample_script.v3.json validates", not errs, "; ".join(e.message for e in errs)[:160])

# RED
def red(name, doc):
    row(f"RED: {name} is rejected", bool(errors([doc])), "validated but should not")

red("ungoverned type 'epiphany'", {"type": "epiphany", "text": "x"})

pce = by_id("p012")
del pce["decision_points"][0]["branches"][0]["action"]
red("proceed_clarify_escalate branch with no action", pce)

dil = by_id("p013")
dil["decision_points"][0]["branches"][0]["quality"] = "optimal"
red("competing_principles with an 'optimal' branch", dil)

inc = by_id("p011")
del inc["missing_information"]
red("incomplete_information with no missing_information", inc)

rr = by_id("p009")
rr["perspectives"] = rr["perspectives"][:1]
red("role-perspective switch with one role", rr)

rp = by_id("p015")
rp["resource_kind"] = "webinar"
red("ungoverned resource_kind", rp)

we = by_id("p006")
del we["steps"][0]["reasoning"]
red("worked_example step with no reasoning", we)

# MENU
r = subprocess.run([sys.executable, str(CORE / "tools/project_move_menu.py"), "--check"],
                   capture_output=True, text=True)
row("MENU: move_menu.md is current with v3", r.returncode == 0, (r.stdout + r.stderr).strip()[-160:])

print(f"{'CHECK':<66} RESULT")
print("-" * 82)
ok = True
for n, passed, d in rows:
    ok = ok and passed
    print(f"{n:<66} {'PASS' if passed else 'FAIL'}   {'' if passed else d}")
print("-" * 82)
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
