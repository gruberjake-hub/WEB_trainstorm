#!/usr/bin/env python3
"""
Self-test for the INTAKE SOCKET: the demand rules in the gate, the PII enforcement, and the two
claims tools/project_socket.py makes that a client would rely on.

A gate is only worth its green light if it is known to go red. This builds SYNTHETIC template and
instance stores, mutates them one rule at a time, and asserts each mutation is rejected with the
expected verdict tag — then runs the projector and asserts what it says about coverage.

Synthetic on purpose, and pinned to nothing real. Two tests in this repo have now rotted by naming a
value that later became governed (reg_benefit_risk_profile on 08-20, the premature `serves` on
08-21). The claim under test is always the RULE.

Usage:  python3 tools/selftest_socket.py [--core <cgen/trainstorm-core>] [--registry <.../registry>]
Exit 0 = every case behaved as specified.
"""
import json, hashlib, pathlib, subprocess, sys, tempfile, copy

TOOLS = pathlib.Path(__file__).resolve().parent
def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

CORE = pathlib.Path(arg("--core", TOOLS.parent)).resolve()
REG  = pathlib.Path(arg("--registry", CORE.parent / "astellas" / "registry")).resolve()
DOC, ROLE = "doc_form_ast_34037", "role_alsap_lead"

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

# ---- synthetic TEMPLATE: one demand of each shape the socket must handle ----------------------
TEMPLATE = stamped([
    t_atom("atom_tpl_root", "form", "Synthetic template root."),
    t_atom("atom_tpl_free", "form_field", "A field the author writes from scratch.",
           {"field_type": "text_long", "content_disposition": "authorable",
            "evidence_kind": "judgment", "supplied_by": "stakeholder_decision"},
           "atom_tpl_root", 0),
    t_atom("atom_tpl_who", "form_field", "Author.",
           {"field_type": "person", "content_disposition": "authorable",
            "evidence_kind": "person_identity", "supplied_by": "authoring_context"},
           "atom_tpl_root", 1),
    t_atom("atom_tpl_std", "form_field",
           "Retained standard sentence naming [THE ASSET] exactly once.",
           {"field_type": "text_long", "content_disposition": "controlled_standard",
            "constraints": {"slots": [{"id": "asset", "marker": "[THE ASSET]",
                                       "expects": "the asset code",
                                       "evidence_kind": "identifier",
                                       "supplied_by": "asset_evidence"}]}},
           "atom_tpl_root", 2),
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

BASE_INST = [
    i_atom("atom_inst_free", "Authored prose for this asset.", "atom_tpl_free"),
    i_atom("atom_inst_who", "person_synthetic_author", "atom_tpl_who"),
    i_atom("atom_inst_slot", "ASP0001", "atom_tpl_std", fills_slot="asset"),
]
BASE_DECS = {"decisions": [
    {"instantiates": "atom_tpl_guide", "decision": "deleted",
     "template_source_hash": h("atom_tpl_guide"), "decided_by": ROLE, "decided_on": "2026-08-21"}]}

def write_stores(root, template, atoms, decs, silent=None):
    tdir, idir = root / "tpl", root / "inst"
    tdir.mkdir(); idir.mkdir()
    (tdir / "atoms.json").write_text(json.dumps(template, indent=2, ensure_ascii=False))
    (tdir / "manifest.json").write_text(json.dumps(
        {"project": "selftest_tpl", "source_document": DOC}))
    if silent is not None:
        (tdir / "source_silent.json").write_text(json.dumps(silent, indent=2))
    (idir / "atoms.json").write_text(json.dumps(stamped(atoms), indent=2, ensure_ascii=False))
    (idir / "instance_decisions.json").write_text(json.dumps(decs, indent=2, ensure_ascii=False))
    (idir / "manifest.json").write_text(json.dumps({
        "project": "selftest_inst",
        "instantiates_template": {"store": "../tpl", "document": DOC, "version": "1.0"}}))
    return tdir, idir

def gate(project, template=TEMPLATE, atoms=None, decs=None, core=CORE, silent=None):
    root = pathlib.Path(tempfile.mkdtemp())
    tdir, idir = write_stores(root, template, atoms if atoms is not None else BASE_INST,
                              decs if decs is not None else BASE_DECS, silent)
    r = subprocess.run([sys.executable, str(TOOLS / "validate_atoms.py"),
                        "--core", str(core), "--registry", str(REG),
                        "--project", str(tdir if project == "tpl" else idir)],
                       capture_output=True, text=True)
    return r.stdout + r.stderr

def socket(template=TEMPLATE, silent=None):
    root = pathlib.Path(tempfile.mkdtemp())
    tdir, _ = write_stores(root, template, BASE_INST, BASE_DECS, silent)
    out = root / "socket.json"
    r = subprocess.run([sys.executable, str(TOOLS / "project_socket.py"),
                        "--core", str(CORE), "--registry", str(REG),
                        "--project", str(tdir), "--out", str(out)],
                       capture_output=True, text=True)
    doc = json.loads(out.read_text()) if out.exists() else None
    return r.stdout + r.stderr, doc

# ---- template-side mutations: each breaks exactly one demand rule -----------------------------
def m_no_kind(t):        _f(t, "atom_tpl_free")["form"].pop("evidence_kind")
def m_no_supplier(t):    _f(t, "atom_tpl_free")["form"].pop("supplied_by")
def m_bad_kind(t):       _f(t, "atom_tpl_free")["form"]["evidence_kind"] = "vibes"
def m_bad_supplier(t):   _f(t, "atom_tpl_free")["form"]["supplied_by"] = "someone_else"
def m_slot_no_kind(t):   _slot(t)[0].pop("evidence_kind")
def m_slot_bad_kind(t):  _slot(t)[0]["evidence_kind"] = "vibes"
def m_phantom_std(t):    _f(t, "atom_tpl_std")["form"]["evidence_kind"] = "identifier"
def m_phantom_guide(t):  _f(t, "atom_tpl_guide")["form"]["supplied_by"] = "asset_evidence"
def _f(t, aid):  return next(a for a in t if a["atom_id"] == aid)["bindings"]
def _slot(t):    return _f(t, "atom_tpl_std")["form"]["constraints"]["slots"]

TPL_CASES = [
    ("an authorable demand that names no evidence_kind",       m_no_kind,       "[socket/demand]"),
    ("an authorable demand that names no supplied_by",         m_no_supplier,   "[socket/demand]"),
    ("an ungoverned evidence_kind",                            m_bad_kind,      "[vocab/evidence_kind]"),
    ("an ungoverned supplied_by",                              m_bad_supplier,  "[vocab/supplied_by]"),
    ("a slot that names no evidence_kind",                     m_slot_no_kind,  "[socket/demand]"),
    ("a slot with an ungoverned evidence_kind",                m_slot_bad_kind, "[vocab/evidence_kind]"),
    ("a PHANTOM obligation on retained text",                  m_phantom_std,   "[socket/demand]"),
    ("a PHANTOM obligation on deleted guidance",               m_phantom_guide, "[socket/demand]"),
]

# ---- instance-side: the no-PII invariant, enforced rather than stated -------------------------
def p_name(a):  next(x for x in a if x["atom_id"] == "atom_inst_who")["meaning"]["source_text"] = "Jane Doe, PhD"
def p_role(a):  next(x for x in a if x["atom_id"] == "atom_inst_who")["meaning"]["source_text"] = ROLE
def p_empty(a): next(x for x in a if x["atom_id"] == "atom_inst_who")["meaning"]["source_text"] = "person Jane"

PII_CASES = [
    ("a person's NAME in a content atom",                      p_name,  "[instance/pii]"),
    ("a ROLE id standing in for a person (accountable != value)", p_role, "[instance/pii]"),
    ("a near-miss that is not an opaque key",                  p_empty, "[instance/pii]"),
]

# ---- drive ------------------------------------------------------------------------------------
print("=" * 78)
print("SELF-TEST — intake socket: demand rules, PII enforcement, contract honesty")
print("=" * 78)
results = []
def record(name, ok, verb=""):
    results.append((name, ok))
    print(f"  {'ok ' if ok else 'FAIL'} {verb} {name}")

out = gate("tpl")
record("POSITIVE CONTROL — a template whose demands all declare themselves passes",
       "GATE @ draft : PASS" in out)
out = gate("inst")
record("POSITIVE CONTROL — an opaque person_ key is accepted", "GATE @ draft : PASS" in out)

for name, mut, tag in TPL_CASES:
    t = copy.deepcopy(TEMPLATE); mut(t)
    out = gate("tpl", template=stamped(t))
    ok = tag in out and "GATE @ draft : FAIL" in out
    record(name, ok, "REJECTS")
    if not ok: print("      expected", tag, "— got:", out.strip().splitlines()[-3:])

for name, mut, tag in PII_CASES:
    a = copy.deepcopy(BASE_INST); mut(a)
    out = gate("inst", atoms=a)
    ok = tag in out and "GATE @ draft : FAIL" in out
    record(name, ok, "REJECTS")
    if not ok: print("      expected", tag, "— got:", out.strip().splitlines()[-3:])

# A MIRROR is a second inline copy of a closed list, at two levels. Mutate a COPY of core and
# assert both bite — an unchecked mirror is how the 2026-08-13 drift got in.
for label, mutate_schema in [
    ("field-level evidence_kind mirror drift", lambda s: s["properties"]["evidence_kind"]["enum"].append("vibes")),
    ("slot-level evidence_kind mirror drift",
     lambda s: s["properties"]["constraints"]["properties"]["slots"]["items"]["properties"]["evidence_kind"]["enum"].append("vibes")),
]:
    fake = pathlib.Path(tempfile.mkdtemp()) / "core"
    fake.mkdir(); (fake / "schemas").mkdir(); (fake / "vocab").mkdir()
    for f in (CORE / "schemas").glob("*.json"): (fake / "schemas" / f.name).write_text(f.read_text())
    for f in (CORE / "vocab").glob("*.json"):   (fake / "vocab" / f.name).write_text(f.read_text())
    sp = fake / "schemas" / "form.facet.schema.json"
    sd = json.loads(sp.read_text()); mutate_schema(sd)
    sp.write_text(json.dumps(sd, indent=2, ensure_ascii=False))
    out = gate("tpl", core=fake)
    record(label, "[vocab/mirror]" in out and "GATE @ draft : FAIL" in out, "REJECTS")

# ---- what the CONTRACT claims, which is what a client actually relies on ----------------------
out, doc = socket()
record("the derived socket validates against its own schema", doc is not None and "socket ->" in out)
record("every demand appears exactly once, slots keyed separately",
       doc is not None and len(doc["demands"]) == 3
       and len({d["demand_id"] for d in doc["demands"]}) == 3)
record("a signature obligation is listed OUT OF BAND, not as a demand",
       doc is not None and all("signature" not in json.dumps(d) for d in doc["demands"]))
record("a PII demand carries its storage rule into the contract",
       doc is not None and any(d.get("storage_rule") for d in doc["demands"]
                               if d["evidence_kind"] == "person_identity"))

# The honesty claim. A partial contract that reads as complete is worse than no contract, so both
# directions are asserted: it says PARTIAL when scope is deferred and does NOT when it is not.
_, doc_partial = socket(silent={"deferred_scope": {
    "decomposed": ["Root"], "not_decomposed_sections": ["Section Two", "Section Three"],
    "tables_total": 4, "tables_decomposed": 1}})
record("declares itself PARTIAL when the ingest deferred scope",
       doc_partial is not None and doc_partial["coverage"]["partial"] is True
       and "PARTIAL" in doc_partial["coverage"]["statement"]
       and len(doc_partial["coverage"]["sections_not_decomposed"]) == 2)
_, doc_full = socket(silent={"deferred_scope": {
    "decomposed": ["Root"], "not_decomposed_sections": [],
    "tables_total": 0, "tables_decomposed": 0}})
record("does NOT claim partial when nothing was deferred",
       doc_full is not None and doc_full["coverage"]["partial"] is False)

bad = [n for n, ok in results if not ok]
print("-" * 78)
print(f"{len(results) - len(bad)}/{len(results)} cases behaved as specified.")
if bad:
    for n in bad: print("  x", n)
    sys.exit(1)
print("SELF-TEST: PASS")
