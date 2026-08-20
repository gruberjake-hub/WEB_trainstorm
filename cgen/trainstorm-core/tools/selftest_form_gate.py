#!/usr/bin/env python3
"""
Self-test for the FORM side of the standing gate (tools/validate_atoms.py).

A gate is only worth its green light if it is known to go red. This drives validate_atoms.py as a
subprocess against deliberately broken copies of the worked FORM-AST-34037 fragment
(example_form_fragment.json) and asserts each mutation is REJECTED with the expected verdict tag —
plus a positive control proving the unmutated fragment passes.

Two of the cases mutate a copy of CORE (never the real one) to prove the anti-drift checks bite:
a facet schema whose inline enum diverges from its vocab file, and a vocab file that is not in the
canonical dimensions.<name>.values[] shape.

Usage:  python3 tools/selftest_form_gate.py [--core <cgen/trainstorm-core>] [--registry <.../registry>]
Exit 0 = every case behaved as specified.
"""
import json, hashlib, pathlib, shutil, subprocess, sys, tempfile, copy

TOOLS = pathlib.Path(__file__).resolve().parent
def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

CORE = pathlib.Path(arg("--core", TOOLS.parent)).resolve()
REG  = pathlib.Path(arg("--registry", CORE.parent / "astellas" / "registry")).resolve()
FRAG = CORE / "example_form_fragment.json"

def stamped(atoms):
    out = copy.deepcopy(atoms)
    for a in out:
        payload = json.dumps(a["meaning"], sort_keys=True, ensure_ascii=False).encode()
        a["content_hash"] = "sha256:" + hashlib.sha256(payload).hexdigest()
    return out

BASE = stamped(json.loads(FRAG.read_text())["atoms"])
PROPOSED = {"roles": [], "records": [], "docs": [],
            "options": [{"id": "reg_benefit_risk_profile", "label": "Benefit-Risk Profile"}]}

def by_id(atoms, needle):
    return next(a for a in atoms if needle in a["atom_id"])

def run(atoms, core=CORE, proposed=PROPOSED):
    d = pathlib.Path(tempfile.mkdtemp())
    (d / "atoms.json").write_text(json.dumps(atoms, indent=2, ensure_ascii=False))
    (d / "manifest.json").write_text(json.dumps({"project": "selftest_form"}))
    if proposed is not None:
        (d / "proposed_registry_extensions.json").write_text(json.dumps(proposed, indent=2))
    r = subprocess.run([sys.executable, str(TOOLS / "validate_atoms.py"),
                        "--core", str(core), "--project", str(d), "--registry", str(REG)],
                       capture_output=True, text=True)
    return r.stdout + r.stderr

# ---- mutations ---------------------------------------------------------------------------------
def m_ungoverned_field_type(a):
    by_id(a, "f_br_profile")["bindings"]["form"]["field_type"] = "controlled_choice_plus_rationale"
def m_ungoverned_disposition(a):
    by_id(a, "f_version_date")["bindings"]["form"]["content_disposition"] = "retain_unchanged"
def m_container_with_field_type(a):
    by_id(a, "sec000_cover")["bindings"]["form"]["field_type"] = "text_short"
def m_leaf_without_field_type(a):
    del by_id(a, "f_version_date")["bindings"]["form"]["field_type"]
def m_leaf_without_disposition(a):
    del by_id(a, "f_version_date")["bindings"]["form"]["content_disposition"]
def m_both_source_facets(a):
    by_id(a, "f_version_date")["bindings"]["procedure"] = {"step_type": "action"}
def m_dangling_conditional(a):
    by_id(a, "f_br_rationale")["bindings"]["form"]["conditional_on"] = [{"field": "atom_does_not_exist"}]
def m_form_kind_without_facet(a):
    del by_id(a, "f_agg_data_table")["bindings"]["form"]
def m_slot_missing_expects(a):
    by_id(a, "f_version_date")["bindings"]["form"]["constraints"]["slots"] = [{"id": "when"}]
def m_slot_marker_absent(a):
    # form.facet v0.3: a marker that is not in the text is a positional reference wearing a name.
    by_id(a, "f_version_date")["bindings"]["form"]["constraints"]["slots"] = [
        {"id": "when", "expects": "the date", "marker": "[nowhere in this sentence]"}]
def m_slot_bad_id(a):
    by_id(a, "f_version_date")["bindings"]["form"]["constraints"]["slots"] = [
        {"id": "Version Date", "expects": "the date", "marker": "[x]"}]

CASES = [
    ("ungoverned field_type (smashed composite)", m_ungoverned_field_type, "[schema/form]"),
    ("ungoverned content_disposition",            m_ungoverned_disposition, "[schema/form]"),
    ("container carrying a field_type",           m_container_with_field_type, "[drift/form]"),
    ("form_field leaf with no field_type",        m_leaf_without_field_type, "[drift/form]"),
    ("form_field leaf with no content_disposition", m_leaf_without_disposition, "[drift/form]"),
    ("atom carrying BOTH procedure and form",     m_both_source_facets, "[drift/source-type]"),
    ("conditional_on -> unknown atom",            m_dangling_conditional, "[drift/ref]"),
    ("form kind with no form binding",            m_form_kind_without_facet, "[drift/form]"),
    ("a named slot with no `expects`",            m_slot_missing_expects, "[schema/form]"),
    ("a slot id that is not a stable name",       m_slot_bad_id, "[schema/form]"),
    ("a slot marker absent from source_text",     m_slot_marker_absent, "[form/slots]"),
]

# soft-flag cases: the gate reports rather than blocks, but promotion must still be held
def m_undeclared_slots(a):
    f = by_id(a, "f_version_date")
    f["meaning"]["source_text"] += " Enter [DD-MMM-YYYY] for the [asset code]."

SOFT_CASES = [
    ("bracketed spans with no declared slots", m_undeclared_slots, "[form/slots]"),
]

def mutated_core(mutate):
    d = pathlib.Path(tempfile.mkdtemp()) / "core"
    shutil.copytree(CORE, d, ignore=shutil.ignore_patterns(
        ".git", "tools", "agents", "locales", "layout-engine", "project", "*.zip"))
    mutate(d)
    return d

def c_mirror_drift(core):
    p = core / "schemas" / "form.facet.schema.json"
    s = json.loads(p.read_text())
    s["properties"]["field_type"]["enum"].append("narrative_formula")   # schema-only value
    p.write_text(json.dumps(s, indent=2))

def c_vocab_shape(core):
    p = core / "vocab" / "form.enum.json"
    s = json.loads(p.read_text())
    s["field_type"] = s["dimensions"].pop("field_type")                 # back to the old flat shape
    p.write_text(json.dumps(s, indent=2))

CORE_CASES = [
    ("facet schema enum drifts from its vocab", c_mirror_drift, "[vocab/mirror]"),
    ("vocab file not in canonical shape",       c_vocab_shape, "[vocab/shape]"),
]

# ---- drive -------------------------------------------------------------------------------------
print("=" * 74)
print("SELF-TEST — form side of the standing gate")
print("=" * 74)
results = []

out = run(BASE)
ok = "GATE @ draft : PASS" in out
results.append(("POSITIVE CONTROL — unmutated worked fragment passes", ok))
print(f"  {'ok ' if ok else 'FAIL'} POSITIVE CONTROL — unmutated worked fragment passes")

# Use a SYNTHETIC id, never a real one: the fragment's reg_benefit_risk_profile was adopted into
# the governed options registry on 2026-08-20, and a test that depends on a real id staying
# ungoverned silently rots the moment governance moves. The claim under test is the RULE.
_ig = copy.deepcopy(BASE)
by_id(_ig, "f_br_profile")["bindings"]["form"]["options_ref"] = "reg_selftest_never_governed"
out = run(stamped(_ig), proposed=None)
ok = "invent-guard tripped" in out and "GATE @ draft : FAIL" in out
results.append(("INVENT-GUARD — ungoverned+unproposed reg_ is rejected", ok))
print(f"  {'ok ' if ok else 'FAIL'} INVENT-GUARD — ungoverned+unproposed reg_ is rejected")

out = run(BASE, proposed=None)
ok = "GATE @ draft : PASS" in out
results.append(("ADOPTED value set passes with no proposal needed", ok))
print(f"  {'ok ' if ok else 'FAIL'} ADOPTED value set passes with no proposal needed")

for name, mutate, tag in CASES:
    a = copy.deepcopy(BASE); mutate(a)
    out = run(stamped(a))
    ok = tag in out and "GATE @ draft : FAIL" in out
    results.append((name, ok))
    print(f"  {'ok ' if ok else 'FAIL'} REJECTS {name}  -> {tag}")

for name, mutate, tag in SOFT_CASES:
    a = copy.deepcopy(BASE); mutate(a)
    out = run(stamped(a))
    ok = tag in out and "GATE @ draft : PASS" in out and "PROMOTE >draft: BLOCKED" in out
    results.append((name, ok))
    print(f"  {'ok ' if ok else 'FAIL'} FLAGS (holds promotion) {name}  -> {tag}")

for name, mutate, tag in CORE_CASES:
    out = run(BASE, core=mutated_core(mutate))
    ok = tag in out and "GATE @ draft : FAIL" in out
    results.append((name, ok))
    print(f"  {'ok ' if ok else 'FAIL'} REJECTS {name}  -> {tag}")

bad = [n for n, ok in results if not ok]
print("-" * 74)
print(f"{len(results) - len(bad)}/{len(results)} cases behaved as specified.")
if bad:
    for n in bad: print("  x", n)
    sys.exit(1)
print("SELF-TEST: PASS")
