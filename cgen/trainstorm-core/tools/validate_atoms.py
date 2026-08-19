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
proc_enum   = load(VOCAB / "procedure.enum.json")
roles_reg   = load(REG / "roles.registry.json")
records_reg = load(REG / "records.registry.json")
docs_reg    = load(REG / "docs.registry.json")

atoms = load(PROJ / "atoms.json")
# staging pen is dropped after adoption (repo state) — treat a missing file as "no pending proposals"
_pp = PROJ / "proposed_registry_extensions.json"
proposed = load(_pp) if _pp.exists() else {"roles": [], "records": [], "docs": []}

gov_roles   = {e["id"] for e in roles_reg["roles"]}     # entries are now {id, label, …}
gov_records = {e["id"] for e in records_reg["records"]}
# canonical procedure.enum.json nests governed values under dimensions.<name>.values[].id
gov_kinds   = {v["id"] for v in proc_enum["dimensions"]["meaning_kind"]["values"]}
gov_steptyp = {v["id"] for v in proc_enum["dimensions"]["step_type"]["values"]}
gov_docs    = {e["id"] for e in docs_reg["docs"]}
prop_roles   = {r["id"] for r in proposed["roles"]}
prop_records = {r["id"] for r in proposed["records"]}
prop_docs    = {d["id"] for d in proposed["docs"]}

hard, soft = [], []
def fail(msg): hard.append(msg)
def flag(msg): soft.append(msg)

av = Draft202012Validator(atom_schema)
pv = Draft202012Validator(proc_schema)

# ---- 1. SCHEMA ----
ids = set()
for a in atoms:
    aid = a.get("atom_id", "<no id>")
    for e in av.iter_errors(a):
        fail(f"[schema/atom] {aid}: {e.message} (at {'/'.join(map(str,e.path))})")
    proc = a.get("bindings", {}).get("procedure")
    if proc is not None:
        for e in pv.iter_errors(proc):
            fail(f"[schema/procedure] {aid}: {e.message} (at {'/'.join(map(str,e.path))})")

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
        fail(f"[vocab/kind] {aid}: meaning.kind '{a['meaning'].get('kind')}' not in governed procedure.enum")

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

for r in sorted(pending_roles):
    flag(f"[vocab/role-pending] {r}: PROPOSED extension, not yet governed")
for r in sorted(pending_records):
    flag(f"[vocab/record-pending] {r}: PROPOSED extension, not yet governed")
for r in sorted(pending_docs):
    flag(f"[vocab/doc-pending] {r}: PROPOSED extension, not yet governed")

# ---- report ----
statuses = {a["governance"]["status"] for a in atoms}
print("="*68)
print(f"VALIDATION GATE — project ast_alsap — {len(atoms)} atoms")
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
