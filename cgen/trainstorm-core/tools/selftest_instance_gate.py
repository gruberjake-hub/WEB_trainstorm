#!/usr/bin/env python3
"""
Self-test for the INSTANCE side of the standing gate (tools/validate_atoms.py).

A gate is only worth its green light if it is known to go red. This builds a SYNTHETIC template
store and a synthetic instance store over it, mutates the instance one rule at a time, and asserts
each mutation is rejected with the expected verdict tag.

Synthetic on purpose. The form self-test learned this the hard way on 2026-08-20: a case pinned to
a real id (reg_benefit_risk_profile) silently rotted the moment that id was governed. The claim
under test here is always the RULE, never the current contents of the ALSAP store — so this file
keeps passing when the template grows, and fails only when a rule stops being enforced.

Usage:  python3 tools/selftest_instance_gate.py [--core <cgen/trainstorm-core>] [--registry <.../registry>]
Exit 0 = every case behaved as specified.
"""
import json, hashlib, pathlib, subprocess, sys, tempfile, copy

TOOLS = pathlib.Path(__file__).resolve().parent
def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

CORE = pathlib.Path(arg("--core", TOOLS.parent)).resolve()
REG  = pathlib.Path(arg("--registry", CORE.parent / "astellas" / "registry")).resolve()
DOC  = "doc_form_ast_34037"          # a governed doc id; the rules under test are not about it
ROLE = "role_alsap_lead"

def stamped(atoms):
    out = copy.deepcopy(atoms)
    for a in out:
        payload = json.dumps(a["meaning"], sort_keys=True, ensure_ascii=False).encode()
        a["content_hash"] = "sha256:" + hashlib.sha256(payload).hexdigest()
    return out

def t_atom(aid, kind, text, form=None, parent=None, order=0):
    b = {"object": ({"belongs_to": parent, "order": order} if parent else {"order": order})}
    b["form"] = form if form is not None else {}
    return {"atom_id": aid, "meaning": {"source_locale": "en", "source_text": text, "kind": kind},
            "bindings": b, "governance": {"version": 1, "status": "draft"}}

# ---- synthetic TEMPLATE: one of every content_disposition, plus a named slot ------------------
TEMPLATE = stamped([
    t_atom("atom_tpl_root", "form", "Synthetic template root."),
    t_atom("atom_tpl_free", "form_field",
           "A field the author writes from scratch.",
           {"field_type": "text_long", "content_disposition": "authorable"},
           "atom_tpl_root", 0),
    t_atom("atom_tpl_std", "form_field",
           "Retained standard sentence naming [THE ASSET] exactly once.",
           {"field_type": "text_long", "content_disposition": "controlled_standard",
            "constraints": {"slots": [{"id": "asset", "marker": "[THE ASSET]",
                                       "expects": "the asset code"}]}},
           "atom_tpl_root", 1),
    t_atom("atom_tpl_example", "form_field", "Example wording the author may keep or rewrite.",
           {"field_type": "text_long", "content_disposition": "example"}, "atom_tpl_root", 2),
    t_atom("atom_tpl_guide", "form_field", "Guidance to the author, deleted before final.",
           {"field_type": "text_long", "content_disposition": "instructional_transient"},
           "atom_tpl_root", 3),
])
TPL_BY_ID = {a["atom_id"]: a for a in TEMPLATE}
def h(aid): return TPL_BY_ID[aid]["content_hash"]

def i_atom(aid, text, instantiates, **inst):
    b = {"instantiates": instantiates, "template_document": DOC, "template_version": "1.0",
         "template_source_hash": h(instantiates), "authored_by": ROLE}
    b.update(inst)
    return {"atom_id": aid, "meaning": {"source_locale": "en", "source_text": text,
                                        "kind": "instance_value"},
            "bindings": {"instance": b}, "governance": {"version": 1, "status": "draft"}}

# ---- a COMPLETE, valid instance over it -------------------------------------------------------
BASE_ATOMS = [
    i_atom("atom_inst_free", "Authored prose for this asset.", "atom_tpl_free"),
    i_atom("atom_inst_slot", "ASP0001", "atom_tpl_std", fills_slot="asset"),
]
BASE_DECS = {"decisions": [
    {"instantiates": "atom_tpl_example", "decision": "retained",
     "template_source_hash": h("atom_tpl_example"), "decided_by": ROLE, "decided_on": "2026-08-20"},
    {"instantiates": "atom_tpl_guide", "decision": "deleted",
     "template_source_hash": h("atom_tpl_guide"), "decided_by": ROLE, "decided_on": "2026-08-20"},
]}

def run(atoms, decs, template=TEMPLATE):
    root = pathlib.Path(tempfile.mkdtemp())
    tdir, idir = root / "tpl", root / "inst"
    tdir.mkdir(); idir.mkdir()
    (tdir / "atoms.json").write_text(json.dumps(template, indent=2, ensure_ascii=False))
    (tdir / "manifest.json").write_text(json.dumps({"project": "selftest_tpl"}))
    (idir / "atoms.json").write_text(json.dumps(stamped(atoms), indent=2, ensure_ascii=False))
    (idir / "instance_decisions.json").write_text(json.dumps(decs, indent=2, ensure_ascii=False))
    (idir / "manifest.json").write_text(json.dumps({
        "project": "selftest_inst",
        "instantiates_template": {"store": "../tpl", "document": DOC, "version": "1.0"}}))
    r = subprocess.run([sys.executable, str(TOOLS / "validate_atoms.py"),
                        "--core", str(CORE), "--project", str(idir), "--registry", str(REG)],
                       capture_output=True, text=True)
    return r.stdout + r.stderr

# ---- mutations: each breaks exactly one rule --------------------------------------------------
def m_unknown_slot(a, d):
    a[0]["bindings"]["instance"]["instantiates"] = "atom_tpl_does_not_exist"
def m_over_controlled(a, d):
    a.append(i_atom("atom_inst_bad", "Rewriting retained standard text.", "atom_tpl_std"))
def m_into_guidance(a, d):
    a.append(i_atom("atom_inst_guide", "My own guidance.", "atom_tpl_guide"))
    d["decisions"] = [x for x in d["decisions"] if x["instantiates"] != "atom_tpl_guide"]
def m_undeclared_slot_id(a, d):
    a[1]["bindings"]["instance"]["fills_slot"] = "not_a_declared_slot"
def m_duplicate_key(a, d):
    a.append(i_atom("atom_inst_slot_again", "ASP0002", "atom_tpl_std", fills_slot="asset"))
def m_mixed_pin(a, d):
    a[0]["bindings"]["instance"]["template_version"] = "2.0"
def m_illegal_decision(a, d):
    d["decisions"][1]["decision"] = "retained"           # 'guide' is instructional_transient
def m_decision_on_authorable(a, d):
    d["decisions"].append({"instantiates": "atom_tpl_free", "decision": "retained",
                           "template_source_hash": h("atom_tpl_free"), "decided_by": ROLE})
def m_ungoverned_decision(a, d):
    d["decisions"][0]["decision"] = "tidied_up"
def m_modified_without_atom(a, d):
    d["decisions"][0]["decision"] = "modified"           # 'example', legal — but names no atom
def m_atom_and_decision_conflict(a, d):
    d["decisions"].append({"instantiates": "atom_tpl_free", "decision": "deleted",
                           "template_source_hash": h("atom_tpl_free"), "decided_by": ROLE})
def m_wrong_kind(a, d):
    a[0]["meaning"]["kind"] = "form_field"
def m_source_facet_too(a, d):
    a[0]["bindings"]["form"] = {"field_type": "text_long", "content_disposition": "authorable"}

CASES = [
    ("instantiates -> unknown template atom",          m_unknown_slot,        "[instance/ref]"),
    ("authoring over retained controlled_standard",    m_over_controlled,     "[instance/controlled]"),
    ("authoring into instructional_transient",         m_into_guidance,       "[instance/controlled]"),
    ("fills_slot that the template never declared",    m_undeclared_slot_id,  "[instance/slot]"),
    ("two values on one (atom_id, slot_id) key",       m_duplicate_key,       "[instance/duplicate]"),
    ("a second template version in one store",         m_mixed_pin,           "[instance/pin]"),
    ("a decision illegal for that disposition",        m_illegal_decision,    "[instance/decision]"),
    ("a decision on an authorable slot",               m_decision_on_authorable, "[instance/decision]"),
    ("an ungoverned disposition_decision",             m_ungoverned_decision, "[instance/decision]"),
    ("'modified' naming no authored atom",             m_modified_without_atom, "[instance/decision]"),
    ("an atom and a contradicting decision",           m_atom_and_decision_conflict, "[instance/conflict]"),
    ("an instance atom with the wrong meaning.kind",   m_wrong_kind,          "[drift/instance]"),
    ("an instance atom carrying a source-type facet",  m_source_facet_too,    "[drift/source-type]"),
]

# soft: reported, does not block drafting, but must hold promotion
def m_stale(a, d):
    a[0]["bindings"]["instance"]["template_source_hash"] = "sha256:" + "0" * 64
def m_incomplete(a, d):
    a.pop(0)                                             # the authorable field is now unanswered

SOFT_CASES = [
    ("a value authored against a since-changed template atom", m_stale, "[instance/stale]"),
    ("a template slot with no value and no decision",          m_incomplete, "[instance/incomplete]"),
]

# ---- drive -----------------------------------------------------------------------------------
print("=" * 78)
print("SELF-TEST — instance side of the standing gate")
print("=" * 78)
results = []

def record(name, ok, verb):
    results.append((name, ok))
    print(f"  {'ok ' if ok else 'FAIL'} {verb} {name}")

out = run(BASE_ATOMS, BASE_DECS)
record("POSITIVE CONTROL — a complete, valid instance passes clean",
       "GATE @ draft : PASS" in out and "PROMOTE >draft: PASS" in out, "")

for name, mutate, tag in CASES:
    a, d = copy.deepcopy(BASE_ATOMS), copy.deepcopy(BASE_DECS)
    mutate(a, d)
    out = run(a, d)
    record(name, tag in out and "GATE @ draft : FAIL" in out, f"REJECTS")
    if tag not in out or "GATE @ draft : FAIL" not in out:
        print("      expected", tag, "— got:\n       ", out.strip().splitlines()[-3:])

for name, mutate, tag in SOFT_CASES:
    a, d = copy.deepcopy(BASE_ATOMS), copy.deepcopy(BASE_DECS)
    mutate(a, d)
    out = run(a, d)
    record(name, tag in out and "GATE @ draft : PASS" in out and "PROMOTE >draft: BLOCKED" in out,
           "FLAGS (holds promotion)")

# The property the whole overlay rests on, asserted rather than assumed: re-binding a FACET on a
# template atom changes no meaning, so content_hash is untouched, so no instance goes stale. If this
# ever fails, every facet correction on a template silently invalidates every ALSAP written against it.
rebound = copy.deepcopy(TEMPLATE)
next(t for t in rebound if t["atom_id"] == "atom_tpl_free")["bindings"]["form"]["performed_by"] = [ROLE]
out = run(BASE_ATOMS, BASE_DECS, template=rebound)
record("a template FACET re-binding does not stale the instance (meaning intact)",
       "[instance/stale]" not in out and "GATE @ draft : PASS" in out, "HOLDS:")

bad = [n for n, ok in results if not ok]
print("-" * 78)
print(f"{len(results) - len(bad)}/{len(results)} cases behaved as specified.")
if bad:
    for n in bad: print("  x", n)
    sys.exit(1)
print("SELF-TEST: PASS")
