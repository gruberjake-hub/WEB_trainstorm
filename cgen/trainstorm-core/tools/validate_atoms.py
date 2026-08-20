#!/usr/bin/env python3
"""
The standing validation gate. Generalises the form-facet validate.py / validate_objectives.py
into one gate that runs on a project's atom store. Three layers:

  1. SCHEMA        — atom shell vs atom.schema.json; bindings.procedure vs procedure.facet.schema.json
  2. DRIFT         — id uniqueness, resolvable refs, content_hash correctness, no embedded localization
  3. VOCAB CONF.   — step_type / roles / records resolve to a GOVERNED member, else must be an
                     explicitly PROPOSED extension (flag, never invent). Ungoverned AND unproposed = hard fail.

Exit policy: HARD failures block at any status. PROPOSED-pending values are allowed while the
atom is status=draft, but block promotion to in_review/approved until adopted into the repo registries.
"""
import json, hashlib, pathlib, sys
import harness_paths
from jsonschema import Draft202012Validator

def load(p): return json.loads(pathlib.Path(p).read_text())

# Anchors (core schemas+vocab, client registry, project store) resolved by the shared resolver —
# canon in the repo, fenced mirror when standalone. Nothing canon-shaped sits next to the tools.
P = harness_paths.resolve()
core_src = harness_paths.announce(P)
SCHEMAS, VOCAB, REG, PROJ = P["schemas_dir"], P["vocab_dir"], P["registry_dir"], P["project_dir"]

atom_schema = load(SCHEMAS / "atom.schema.json")
proc_schema = load(SCHEMAS / "procedure.facet.schema.json")
form_schema = load(SCHEMAS / "form.facet.schema.json")
roles_reg   = load(REG / "roles.registry.json")
records_reg = load(REG / "records.registry.json")
docs_reg    = load(REG / "docs.registry.json")
# Controlled value sets (reg_ ids behind form.options_ref). No governed registry exists yet — the
# owed reg_benefit_risk_profile is still an open SME question — so a missing file means "nothing
# governed", and every reg_ id must be an explicit PROPOSED extension or the invent-guard trips.
_opts = REG / "options.registry.json"
options_reg = load(_opts) if _opts.exists() else {"options": []}

atoms = load(PROJ / "atoms.json")
# staging pen is dropped after adoption (repo state) — treat a missing file as "no pending proposals"
_pp = PROJ / "proposed_registry_extensions.json"
proposed = load(_pp) if _pp.exists() else {}
for _k in ("roles", "records", "docs", "options"):
    proposed.setdefault(_k, [])

# ---- governed vocabularies -------------------------------------------------------------
# Every vocab file uses ONE canonical shape: dimensions.<name>.values[].id. Read them through a
# single helper so a new vocab file is one line, not a new parser. A file that is present but does
# NOT conform to that shape is a hard failure, not a silent skip — govern-the-vocabularies applied
# to the vocabulary files themselves.
def vocab_path(name):
    """core vocab first; _core_adds is the standalone fallback for not-yet-committed vocab."""
    p1 = VOCAB / name
    return p1 if p1.exists() else P["core_adds_dir"] / name

_vocab_shape_errors = []
def govset(name, dim, required=False):
    fp = vocab_path(name)
    if not fp.exists():
        if required:
            _vocab_shape_errors.append(f"{name}: missing (required)")
        return set()
    d = load(fp)
    try:
        return {v["id"] for v in d["dimensions"][dim]["values"]}
    except (KeyError, TypeError):
        _vocab_shape_errors.append(
            f"{name}: no dimensions.{dim}.values[] — not the canonical vocab shape")
        return set()

# meaning.kind is governed ADDITIVELY across vocab files, each owning a disjoint subset:
#   procedure.enum -> procedure / procedure_step
#   structure.enum -> list / list_item        (source-agnostic)
#   form.enum      -> form / form_section / form_field
gov_kinds   = (govset("procedure.enum.json", "meaning_kind", required=True)
               | govset("structure.enum.json", "meaning_kind")
               | govset("form.enum.json", "meaning_kind"))
gov_steptyp = govset("procedure.enum.json", "step_type", required=True)
gov_fieldty = govset("form.enum.json", "field_type")
gov_disp    = govset("form.enum.json", "content_disposition")

gov_roles   = {e["id"] for e in roles_reg["roles"]}     # entries are now {id, label, …}
gov_records = {e["id"] for e in records_reg["records"]}
gov_docs    = {e["id"] for e in docs_reg["docs"]}
gov_options = {e["id"] for e in options_reg["options"]}
prop_roles   = {r["id"] for r in proposed["roles"]}
prop_records = {r["id"] for r in proposed["records"]}
prop_docs    = {d["id"] for d in proposed["docs"]}
prop_options = {o["id"] for o in proposed["options"]}

hard, soft = [], []
def fail(msg): hard.append(msg)
def flag(msg): soft.append(msg)

av = Draft202012Validator(atom_schema)
pv = Draft202012Validator(proc_schema)
fv = Draft202012Validator(form_schema)

for m in _vocab_shape_errors:
    fail(f"[vocab/shape] {m}")

# ---- 0. MIRROR CONFORMANCE (schema enum == vocab ids) ----
# Both facet schemas inline enums that their vocab files declare to be MIRRORS. The vocab wins.
# Asserting equality here is what stops a drifting second copy of a closed list — the same class of
# failure as the 2026-08-13 vendored-schema incident, caught by a check instead of by accident.
def mirror(label, schema, prop, govern):
    if not govern:
        return  # vocab absent; its own shape/missing check already reported
    inline = set(schema.get("properties", {}).get(prop, {}).get("enum", []))
    if inline != govern:
        fail(f"[vocab/mirror] {label}: schema enum != vocab ids "
             f"(schema-only={sorted(inline - govern)}, vocab-only={sorted(govern - inline)})")

mirror("procedure.facet.step_type", proc_schema, "step_type", gov_steptyp)
mirror("form.facet.field_type", form_schema, "field_type", gov_fieldty)
mirror("form.facet.content_disposition", form_schema, "content_disposition", gov_disp)

# ---- 1. SCHEMA ----
ids = set()
for a in atoms:
    aid = a.get("atom_id", "<no id>")
    for e in av.iter_errors(a):
        fail(f"[schema/atom] {aid}: {e.message} (at {'/'.join(map(str,e.path))})")
    b = a.get("bindings", {})
    proc = b.get("procedure")
    if proc is not None:
        for e in pv.iter_errors(proc):
            fail(f"[schema/procedure] {aid}: {e.message} (at {'/'.join(map(str,e.path))})")
    form = b.get("form")
    if form is not None:
        for e in fv.iter_errors(form):
            fail(f"[schema/form] {aid}: {e.message} (at {'/'.join(map(str,e.path))})")
    # an atom carries EXACTLY ONE source-type facet (procedure | form) — a procedure produces a
    # record and a form is that record's template; merging them into one atom collapses the duality
    if proc is not None and form is not None:
        fail(f"[drift/source-type] {aid}: carries BOTH procedure and form facets (exactly one allowed)")

# ---- 2. DRIFT ----
for a in atoms:
    aid = a["atom_id"]
    if aid in ids: fail(f"[drift/id-collision] duplicate atom_id {aid}")
    ids.add(aid)

for a in atoms:
    aid = a["atom_id"]
    # content_hash correctness
    payload = json.dumps(a["meaning"], sort_keys=True, ensure_ascii=False).encode("utf-8")
    want = "sha256:" + hashlib.sha256(payload).hexdigest()
    if a.get("content_hash") != want:
        fail(f"[drift/content_hash] {aid}: stored hash does not match meaning")
    # embedded localization
    if a["meaning"].get("source_locale") != "en":
        flag(f"[drift/localization] {aid}: source_locale != en (locale content belongs in a locale pack)")
    # governed kind
    if a["meaning"].get("kind") not in gov_kinds:
        fail(f"[vocab/kind] {aid}: meaning.kind '{a['meaning'].get('kind')}' not governed "
             f"(procedure.enum u structure.enum u form.enum)")

# ref resolution
for a in atoms:
    aid = a["atom_id"]
    obj = a.get("bindings", {}).get("object", {})
    bt = obj.get("belongs_to")
    if bt and bt not in ids: fail(f"[drift/ref] {aid}: belongs_to -> unknown {bt}")
    for pr in obj.get("prerequisites", []):
        if pr not in ids: fail(f"[drift/ref] {aid}: prerequisite -> unknown {pr}")
    proc = a.get("bindings", {}).get("procedure", {})
    for br in proc.get("branches", []):
        if br["leads_to"] not in ids: fail(f"[drift/ref] {aid}: branch leads_to -> unknown {br['leads_to']}")
    ar = proc.get("acceptance_ref")
    if ar and ar not in ids: fail(f"[drift/ref] {aid}: acceptance_ref -> unknown {ar}")
    for ref in proc.get("references", []):
        if ref.startswith("atom_") and ref not in ids:
            fail(f"[drift/ref] {aid}: reference -> unknown atom {ref}")
    form = a.get("bindings", {}).get("form", {})
    for c in form.get("conditional_on", []):
        if c["field"] not in ids:
            fail(f"[drift/ref] {aid}: conditional_on -> unknown atom {c['field']}")

# ---- 3. VOCAB CONFORMANCE (flag, never invent) ----
pending_roles, pending_records, pending_docs = set(), set(), set()
for a in atoms:
    aid = a["atom_id"]
    proc = a.get("bindings", {}).get("procedure")
    if not proc: continue
    st = proc.get("step_type")
    if st is not None and st not in gov_steptyp:
        fail(f"[vocab/step_type] {aid}: '{st}' not governed")
    for r in proc.get("performed_by", []):
        if r in gov_roles: continue
        if r in prop_roles: pending_roles.add(r)
        else: fail(f"[vocab/role] {aid}: '{r}' is ungoverned AND unproposed (invent-guard tripped)")
    for rec in proc.get("produces_records", []):
        if rec in gov_records: continue
        if rec in prop_records: pending_records.add(rec)
        else: fail(f"[vocab/record] {aid}: '{rec}' is ungoverned AND unproposed (invent-guard tripped)")
    for ref in proc.get("references", []):
        if not ref.startswith("doc_"): continue  # atom_ refs resolved in drift layer
        if ref in gov_docs: continue
        if ref in prop_docs: pending_docs.add(ref)
        else: fail(f"[vocab/doc] {aid}: '{ref}' is ungoverned AND unproposed (invent-guard tripped)")

pending_options = set()

def _govcheck(aid, kind, val, governed, pending_set, proposed_set):
    """One invent-guard used by both facets: governed -> ok; proposed -> pend; else hard fail."""
    if val in governed:
        return
    if val in proposed_set:
        pending_set.add(val); return
    fail(f"[vocab/{kind}] {aid}: '{val}' is ungoverned AND unproposed (invent-guard tripped)")

for a in atoms:
    aid = a["atom_id"]
    kind = a["meaning"].get("kind")
    form = a.get("bindings", {}).get("form")
    if form is None:
        # a form-family kind with no form binding is an atom that lost its facet
        if kind in ("form", "form_section", "form_field"):
            fail(f"[drift/form] {aid}: meaning.kind '{kind}' but no bindings.form")
        continue
    if kind not in ("form", "form_section", "form_field"):
        fail(f"[drift/form] {aid}: carries a form facet but meaning.kind is '{kind}'")

    ft = form.get("field_type")
    # leaves carry a field_type; containers must not (structure lives in the object facet)
    if kind == "form_field":
        if ft is None:
            fail(f"[drift/form] {aid}: form_field leaf carries no field_type")
        elif ft not in gov_fieldty:
            fail(f"[vocab/field_type] {aid}: '{ft}' not governed "
                 f"(composites like *_plus_* DECOMPOSE into separate field atoms)")
        # content_disposition is the line between reused controlled text and asset-specific
        # authored text. A projection (or an authoring agent) that cannot see it cannot tell what
        # an author may touch — load-bearing, so its absence is a hard failure, not a flag.
        cd = form.get("content_disposition")
        if cd is None:
            fail(f"[drift/form] {aid}: form_field carries no content_disposition")
        elif cd not in gov_disp:
            fail(f"[vocab/content_disposition] {aid}: '{cd}' not governed")
        # A [bracketed] span inside retained text is a fill-in point. If the field declares no
        # matching slot, the instance layer has nothing stable to attach the filled value to, and
        # the author's obligation is invisible to any projection. Soft: square brackets have other
        # uses, so this reports rather than blocks.
        import re as _re
        spans = _re.findall(r"\[[^\[\]]{2,}\]", a["meaning"]["source_text"])
        declared = form.get("constraints", {}).get("slots", [])
        if spans and len(spans) != len(declared):
            flag(f"[form/slots] {aid}: {len(spans)} bracketed span(s) in source_text but "
                 f"{len(declared)} declared slot(s)")
        if ft in ("select_one", "select_many") and not form.get("options_ref"):
            flag(f"[form/options] {aid}: {ft} with no options_ref — controlled value set unidentified")
    else:
        if ft is not None:
            fail(f"[drift/form] {aid}: container kind '{kind}' carries field_type '{ft}' "
                 f"(containers hold structure, not input primitives)")
        # a container may declare a disposition (e.g. an instructional block deleted before final);
        # it is optional there, but if present it must still resolve to a governed value
        cd = form.get("content_disposition")
        if cd is not None and cd not in gov_disp:
            fail(f"[vocab/content_disposition] {aid}: '{cd}' not governed")

    if form.get("options_ref"):
        _govcheck(aid, "options", form["options_ref"], gov_options, pending_options, prop_options)
    if form.get("captures_record"):
        _govcheck(aid, "record", form["captures_record"], gov_records, pending_records, prop_records)
    for r in form.get("performed_by", []):
        _govcheck(aid, "role", r, gov_roles, pending_roles, prop_roles)

for r in sorted(pending_options):
    flag(f"[vocab/options-pending] {r}: PROPOSED extension, not yet governed")
for r in sorted(pending_roles):
    flag(f"[vocab/role-pending] {r}: PROPOSED extension, not yet governed")
for r in sorted(pending_records):
    flag(f"[vocab/record-pending] {r}: PROPOSED extension, not yet governed")
for r in sorted(pending_docs):
    flag(f"[vocab/doc-pending] {r}: PROPOSED extension, not yet governed")

# ---- report ----
statuses = {a["governance"]["status"] for a in atoms}
print("="*68)
_mf = PROJ / "manifest.json"
_project = load(_mf).get("project", PROJ.name) if _mf.exists() else PROJ.name
_facets = sorted({k for a in atoms for k in a.get("bindings", {})})
print(f"VALIDATION GATE — project {_project} — {len(atoms)} atoms")
print(f"facets present: {', '.join(_facets) or '(none)'}")
print(f"schemas: {core_src}")
print("="*68)
print(f"SCHEMA + DRIFT hard failures : {len(hard)}")
print(f"PROPOSED / soft flags        : {len(soft)}")
print(f"atom statuses in store       : {sorted(statuses)}")
print("-"*68)
if hard:
    print("HARD FAILURES (block at any status):")
    for m in hard: print("  x", m)
else:
    print("HARD FAILURES: none — schema valid, refs resolve, hashes match, no invented vocab.")
print("-"*68)
print("SOFT FLAGS (allowed at draft; block promotion to in_review/approved until adopted):")
for m in soft: print("  !", m)
print("-"*68)
gate_ok = (len(hard) == 0)
promote_ok = gate_ok and (len(soft) == 0)
print(f"GATE @ draft : {'PASS' if gate_ok else 'FAIL'}")
print(f"PROMOTE >draft: {'PASS' if promote_ok else 'BLOCKED (adopt proposed registry extensions first)'}")
sys.exit(0 if gate_ok else 1)
