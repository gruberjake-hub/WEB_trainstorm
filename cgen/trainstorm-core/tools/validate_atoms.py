#!/usr/bin/env python3
"""
The standing validation gate. Generalises the form-facet validate.py / validate_objectives.py
into one gate that runs on a project's atom store. Three layers:

  1. SCHEMA        — atom shell vs atom.schema.json; bindings.procedure vs procedure.facet.schema.json
  2. DRIFT         — id uniqueness, resolvable refs, content_hash correctness, no embedded localization
  3. VOCAB CONF.   — step_type / roles / records resolve to a GOVERNED member, else must be an
                     explicitly PROPOSED extension (flag, never invent). Ungoverned AND unproposed = hard fail.
  4. INSTANCE      — for an instance store only (one declaring instantiates_template in its manifest):
                     every authored value resolves to a real template slot, is legal for that slot's
                     content_disposition, is pinned to one template version, and is not stale.

Exit policy: HARD failures block at any status. PROPOSED-pending values are allowed while the
atom is status=draft, but block promotion to in_review/approved until adopted into the repo registries.
Staleness and incompleteness are SOFT: an instance is drafted incrementally, but it may not be
promoted while it still owes values or while the template has moved underneath it.
"""
import json, hashlib, pathlib, sys
import re as _re2
import harness_paths
from jsonschema import Draft202012Validator

def load(p): return json.loads(pathlib.Path(p).read_text())

# Anchors (core schemas+vocab, client registry, project store) resolved by the shared resolver —
# canon in the repo, fenced mirror when standalone. Nothing canon-shaped sits next to the tools.
P = harness_paths.resolve()
core_src = harness_paths.announce(P)
SCHEMAS, VOCAB, REG, PROJ = P["schemas_dir"], P["vocab_dir"], P["registry_dir"], P["project_dir"]
TPL = P.get("template_dir")          # None unless this project declares instantiates_template

atom_schema = load(SCHEMAS / "atom.schema.json")
proc_schema = load(SCHEMAS / "procedure.facet.schema.json")
form_schema = load(SCHEMAS / "form.facet.schema.json")
# The instance facet is newer than the two source-type facets; a core checkout without it simply
# runs the gate as before. Same graceful-absence rule the structure.enum union already follows.
_inst_sp = SCHEMAS / "instance.facet.schema.json"
inst_schema = load(_inst_sp) if _inst_sp.exists() else None
roles_reg   = load(REG / "roles.registry.json")
records_reg = load(REG / "records.registry.json")
docs_reg    = load(REG / "docs.registry.json")
# Controlled value sets (reg_ ids behind form.options_ref). No governed registry exists yet — the
# owed reg_benefit_risk_profile is still an open SME question — so a missing file means "nothing
# governed", and every reg_ id must be an explicit PROPOSED extension or the invent-guard trips.
_opts = REG / "options.registry.json"
options_reg = load(_opts) if _opts.exists() else {"options": []}

atoms = load(PROJ / "atoms.json")
store_by_id = {a["atom_id"]: a for a in atoms if "atom_id" in a}
manifest = load(PROJ / "manifest.json") if (PROJ / "manifest.json").exists() else {}
# The pinned template an instance store overlays. Read-only, and read ACROSS a store boundary on
# purpose: per-project isolation governs what a store may PERSIST, and a persisted instantiates ref
# points UP into a shared tier (the same direction as role_/rec_/doc_/reg_ ids), never sideways.
tpl_atoms = load(TPL / "atoms.json") if TPL else []
tpl_by_id = {a["atom_id"]: a for a in tpl_atoms}
# Decisions about template text the author is NOT authoring into. These carry no meaning, so they
# have no atom: external and atom_id-keyed, the same move as reconciliation_log.json / locale packs.
_dec_p = PROJ / "instance_decisions.json"
decisions_doc = load(_dec_p) if _dec_p.exists() else {}
decisions = decisions_doc.get("decisions", [])
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
#   instance.enum  -> instance_value           (an instance store holds authored values only)
gov_kinds   = (govset("procedure.enum.json", "meaning_kind", required=True)
               | govset("structure.enum.json", "meaning_kind")
               | govset("form.enum.json", "meaning_kind")
               | govset("instance.enum.json", "meaning_kind"))
gov_steptyp = govset("procedure.enum.json", "step_type", required=True)
gov_fieldty = govset("form.enum.json", "field_type")
gov_disp    = govset("form.enum.json", "content_disposition")
gov_decision = govset("instance.enum.json", "disposition_decision")
gov_evkind  = govset("evidence.enum.json", "evidence_kind")
gov_supply  = govset("evidence.enum.json", "supplied_by")

# Which evidence kinds are PII-bearing is a property of the vocabulary entry, not a constant in this
# file. Hardcoding {"person_identity"} here would be a second copy of a governed fact, and it would
# not follow the vocab when a later kind is added that also carries PII.
def _pii_kinds():
    fp = vocab_path("evidence.enum.json")
    if not fp.exists():
        return set()
    try:
        return {v["id"] for v in load(fp)["dimensions"]["evidence_kind"]["values"]
                if v.get("pii_bearing")}
    except (KeyError, TypeError):
        return set()
PII_KINDS = _pii_kinds()

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
iv = Draft202012Validator(inst_schema) if inst_schema else None

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
mirror("form.facet.evidence_kind", form_schema, "evidence_kind", gov_evkind)
mirror("form.facet.supplied_by", form_schema, "supplied_by", gov_supply)
# The slot-level copies are a SECOND inline enum of the same closed list, so they need the same
# assertion — an unchecked mirror is exactly how the 08-13 drift got in.
_slot_props = (form_schema.get("properties", {}).get("constraints", {})
               .get("properties", {}).get("slots", {}).get("items", {}))
mirror("form.facet.slots[].evidence_kind", _slot_props, "evidence_kind", gov_evkind)
mirror("form.facet.slots[].supplied_by", _slot_props, "supplied_by", gov_supply)
if inst_schema:
    mirror("instance.facet.disposition_decision", inst_schema, "disposition_decision", gov_decision)

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
    inst = b.get("instance")
    if inst is not None:
        if iv is None:
            fail(f"[schema/instance] {aid}: carries bindings.instance but core has no "
                 f"instance.facet.schema.json to validate it against")
        else:
            for e in iv.iter_errors(inst):
                fail(f"[schema/instance] {aid}: {e.message} (at {'/'.join(map(str,e.path))})")
    # an atom carries EXACTLY ONE source-type facet (procedure | form) — a procedure produces a
    # record and a form is that record's template; merging them into one atom collapses the duality
    if proc is not None and form is not None:
        fail(f"[drift/source-type] {aid}: carries BOTH procedure and form facets (exactly one allowed)")
    # an instance atom is an authored VALUE, not a template node. Carrying a source-type facet would
    # make it a rival declaration of the slot it fills — the filled-in-copy failure, one atom at a time.
    if inst is not None and (proc is not None or form is not None):
        fail(f"[drift/source-type] {aid}: carries an instance facet AND a source-type facet "
             f"(an instance atom fills a template slot; it does not redeclare one)")

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

        # ---- the DEMAND rule (form.facet v0.4) --------------------------------------------
        # A template's unfilled points enumerate a demand on someone OUTSIDE the manifold. An
        # authorable field is a demand; so is each declared slot, in its own right. Naming the kind
        # of evidence and who it falls on is what lets tools/project_socket.py derive an intake
        # CONTRACT rather than a checklist — so a demand that cannot say what it wants is a hard
        # failure, on the same argument that made content_disposition hard: a downstream reader
        # that cannot see it cannot do its job, and silence reads as "nothing is required."
        _ek, _sb = form.get("evidence_kind"), form.get("supplied_by")
        _is_demand = (cd == "authorable")
        if _is_demand:
            if _ek is None:
                fail(f"[socket/demand] {aid}: authorable field declares no evidence_kind "
                     f"(what must the stakeholder supply?)")
            elif _ek not in gov_evkind:
                fail(f"[vocab/evidence_kind] {aid}: '{_ek}' not governed")
            if _sb is None:
                fail(f"[socket/demand] {aid}: authorable field declares no supplied_by "
                     f"(whose obligation is this?)")
            elif _sb not in gov_supply:
                fail(f"[vocab/supplied_by] {aid}: '{_sb}' not governed")
        else:
            # The converse matters as much. A retained sentence or a block that gets deleted
            # demands NOTHING; letting it name an evidence kind would put a phantom obligation in
            # a contract handed to a client. Note this also catches the subtle case: a sentence
            # that CARRIES slots is not itself a demand — its slots are — so the kind belongs on
            # them and never on the sentence.
            for _f, _v in (("evidence_kind", _ek), ("supplied_by", _sb)):
                if _v is not None:
                    fail(f"[socket/demand] {aid}: {cd} field carries {_f}='{_v}' but demands "
                         f"nothing (only an authorable field is a demand; slots carry their own)")

        # A [bracketed] span inside retained text is a fill-in point. If the field declares no
        # matching slot, the instance layer has nothing stable to attach the filled value to, and
        # the author's obligation is invisible to any projection. Soft: square brackets have other
        # uses, so this reports rather than blocks.
        import re as _re
        src = a["meaning"]["source_text"]
        spans = _re.findall(r"\[[^\[\]]{2,}\]", src)
        declared = form.get("constraints", {}).get("slots", [])
        if spans and len(spans) != len(declared):
            flag(f"[form/slots] {aid}: {len(spans)} bracketed span(s) in source_text but "
                 f"{len(declared)} declared slot(s)")
        # A marker that does not appear exactly once is not a stable handle on a span — it is a
        # positional reference wearing a name, which is the failure constraints.slots exists to
        # prevent. Hard, because a renderer would otherwise substitute into the wrong blank or none.
        for _s in declared:
            _m = _s.get("marker")
            if _m is None:
                continue
            _n = src.count(_m)
            if _n != 1:
                fail(f"[form/slots] {aid}: slot '{_s['id']}' marker {_m!r} occurs {_n} time(s) in "
                     f"source_text (must be exactly 1)")
        # Each slot is a demand in its own right — (atom_id, slot_id) IS the demand id in the
        # socket — so each states its own kind rather than inheriting the sentence's.
        for _s in declared:
            for _f, _gov in (("evidence_kind", gov_evkind), ("supplied_by", gov_supply)):
                _v = _s.get(_f)
                if _v is None:
                    fail(f"[socket/demand] {aid}: slot '{_s['id']}' declares no {_f}")
                elif _v not in _gov:
                    fail(f"[vocab/{_f}] {aid}: slot '{_s['id']}': '{_v}' not governed")
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

# ---- 4. INSTANCE LAYER -------------------------------------------------------------------
# Only runs for a store that declares instantiates_template. An authored ALSAP is a SPARSE OVERLAY:
# controlled standard text is never copied down, so the questions this layer answers are "does every
# authored value point at a real template slot it is ALLOWED to fill", "is it still pinned to the
# template it was written against", and "what does this instance still owe".
_pin = manifest.get("instantiates_template") or {}
instance_atoms = [a for a in atoms if "instance" in a.get("bindings", {})]
owed_values, owed_decisions, stale = [], [], []

def _tform(t):  return t.get("bindings", {}).get("form", {})
def _tdisp(t):  return _tform(t).get("content_disposition")
def _tslots(t): return {s["id"] for s in _tform(t).get("constraints", {}).get("slots", [])}

# Which decisions each template disposition permits. Lifted from the template's OWN global rules
# (FORM_RULE_005/006/007) — the same source that produced content_disposition itself, so the matrix
# is read off the controlled document rather than invented here.
LEGAL_DECISIONS = {
    "controlled_standard":     {"retained", "marked_not_applicable"},
    "example":                 {"retained", "modified", "deleted"},
    "instructional_transient": {"deleted"},
    "authorable":              set(),   # an authorable slot is FILLED by an atom, never "decided"
}

if TPL is None:
    for a in instance_atoms:
        fail(f"[instance/store] {a['atom_id']}: carries bindings.instance but this project declares "
             f"no instantiates_template — the reference cannot be resolved")
    if decisions:
        fail(f"[instance/store] instance_decisions.json has {len(decisions)} entrie(s) but this "
             f"project declares no instantiates_template")
else:
    if not instance_atoms and not decisions:
        flag("[instance/empty] project declares a template pin but holds no authored values "
             "or decisions yet")
    seen_keys, decided = {}, {}

    for a in instance_atoms:
        aid, inst = a["atom_id"], a["bindings"]["instance"]
        if a["meaning"].get("kind") != "instance_value":
            fail(f"[drift/instance] {aid}: carries an instance facet but meaning.kind is "
                 f"'{a['meaning'].get('kind')}' (expected 'instance_value')")
        t = tpl_by_id.get(inst["instantiates"])
        if t is None:
            fail(f"[instance/ref] {aid}: instantiates -> unknown template atom "
                 f"{inst['instantiates']} (template store: {TPL})")
            continue

        # ONE atom per (instantiates, fills_slot). The compound key is the whole point of naming
        # slots; two atoms on one key means two rival values for one blank.
        key = (inst["instantiates"], inst.get("fills_slot"))
        if key in seen_keys:
            fail(f"[instance/duplicate] {aid}: second value for "
                 f"{key[0]}{'#' + key[1] if key[1] else ''} (already {seen_keys[key]})")
        seen_keys[key] = aid

        # The whole store is authored against ONE approved template version. A mixed pin means the
        # projection would resolve some slots against one revision and some against another.
        for fld, label in (("template_document", "document"), ("template_version", "version")):
            if _pin.get(label) and inst.get(fld) != _pin[label]:
                fail(f"[instance/pin] {aid}: {fld}='{inst.get(fld)}' but the manifest pins "
                     f"{label}='{_pin[label]}' (one instance store, one template version)")
        _govcheck(aid, "doc", inst.get("template_document", ""), gov_docs, pending_docs, prop_docs)
        if inst.get("authored_by"):
            _govcheck(aid, "role", inst["authored_by"], gov_roles, pending_roles, prop_roles)

        # Staleness: the template atom's MEANING moved after this value was authored. Soft, because
        # an instance mid-draft is allowed to lag; it must not be promoted while it does.
        if inst["template_source_hash"] != t.get("content_hash"):
            stale.append(aid)
            flag(f"[instance/stale] {aid}: template atom {t['atom_id']} has changed since this "
                 f"value was authored (pinned {inst['template_source_hash'][:14]}…, "
                 f"now {str(t.get('content_hash'))[:14]}…)")

        d, slot_id = _tdisp(t), inst.get("fills_slot")
        if slot_id is not None and slot_id not in _tslots(t):
            fail(f"[instance/slot] {aid}: fills_slot '{slot_id}' is not a declared slot on "
                 f"{t['atom_id']} (declared: {sorted(_tslots(t)) or 'none'})")

        # The line the whole overlay rests on. An instance may not overwrite retained standard text
        # — that is a document-control act, not an authoring one. The ONE exception is a declared
        # named slot: the sentence stays controlled, the [bracketed] span is authorable.
        if d == "controlled_standard" and slot_id is None:
            fail(f"[instance/controlled] {aid}: authors over controlled_standard template atom "
                 f"{t['atom_id']} without filling a declared slot (retained text is resolved from "
                 f"the template, never copied into an instance)")
        if d == "instructional_transient":
            fail(f"[instance/controlled] {aid}: authors into instructional_transient template atom "
                 f"{t['atom_id']} (guidance is deleted before final, never authored into)")

        # ---- no PII in a content atom, ENFORCED ------------------------------------------------
        # Some demands are for a named individual (the ALSAP cover requires an Author). The demand
        # is real and stays in the intake contract; the VALUE may never land in a content atom. It
        # keys into a separately-governed identity tier and resolves at render time, exactly as
        # role_ ids already do. Which kinds are PII-bearing is read from the vocabulary entry, so
        # this bites automatically on any kind later marked that way.
        _tf = t.get("bindings", {}).get("form", {})
        _dk = (next((s for s in _tf.get("constraints", {}).get("slots", [])
                     if s.get("id") == slot_id), {}) if slot_id is not None else _tf).get("evidence_kind")
        if _dk in PII_KINDS:
            _val = a["meaning"]["source_text"].strip()
            _where = t["atom_id"] + (f" slot '{slot_id}'" if slot_id else "")
            if _re2.fullmatch(r"person_[a-z0-9_]+", _val):
                pass                       # an opaque key: the manifold holds the handle, not the person
            elif _re2.fullmatch(r"role_[a-z0-9_-]+", _val):
                # Subtle, and worth its own message. A role id is PII-free, so a blanket no-PII check
                # waves it through — but it answers a DIFFERENT question. "Accountable for the field"
                # is not "the value of the field": the 2026-08-20 dispatch declined exactly this
                # inference unprompted, and a store that makes it commits the error its own agent
                # refused. Who is accountable already lives in form.performed_by on the template.
                fail(f"[instance/pii] {aid}: fills the '{_dk}' demand on {_where} with the role id "
                     f"'{_val}'. A role is not a person — accountable FOR a field is not the VALUE "
                     f"of it. Use an opaque person_ key; accountability is already carried by "
                     f"form.performed_by on the template atom.")
            else:
                fail(f"[instance/pii] {aid}: fills the '{_dk}' demand on {_where} with free text. "
                     f"PII-bearing values are never stored in a content atom — store an opaque "
                     f"person_ key and resolve it at render time against the identity tier "
                     f"(vocab/evidence.enum.json storage_rule).")

        dd = inst.get("disposition_decision")
        if d == "example" and dd != "modified":
            fail(f"[instance/decision] {aid}: an atom over an 'example' template slot means the "
                 f"author rewrote it — expected disposition_decision='modified', got {dd!r}")
        if d == "authorable" and dd is not None:
            fail(f"[instance/decision] {aid}: authorable slot carries disposition_decision "
                 f"{dd!r} (an authorable slot is filled, not decided)")

        # "Select one of the six governed values and never invent a seventh", enforced.
        ref, sv = _tform(t).get("options_ref"), inst.get("selected_value")
        if ref:
            if sv is None:
                fail(f"[instance/option] {aid}: template slot takes a controlled value from {ref} "
                     f"but no selected_value is recorded")
            else:
                entry = next((e for e in options_reg["options"] if e["id"] == ref), None)
                allowed = {v["id"] for v in (entry or {}).get("values", [])}
                if entry is None:
                    fail(f"[instance/option] {aid}: options_ref {ref} is not in the governed "
                         f"options registry, so selected_value cannot be checked")
                elif sv not in allowed:
                    fail(f"[instance/option] {aid}: selected_value '{sv}' is not in {ref} "
                         f"(governed: {sorted(allowed)})")
                elif a["meaning"]["source_text"] != sv:
                    # For a controlled value set the authored meaning IS the choice, so the atom's
                    # payload is the option id and nothing else. Prose here would be a second copy
                    # of the option's label, which lives once in the options registry.
                    fail(f"[instance/option] {aid}: meaning.source_text does not match "
                         f"selected_value '{sv}' (a chosen option's meaning is its id; the label "
                         f"lives once, in {ref})")
        elif sv is not None:
            fail(f"[instance/option] {aid}: selected_value '{sv}' but template slot "
                 f"{t['atom_id']} has no options_ref (no value set to choose from)")

    # ---- decisions sidecar: template text the author did NOT author into ----
    for i, e in enumerate(decisions):
        where = f"instance_decisions[{i}]"
        tid = e.get("instantiates")
        t = tpl_by_id.get(tid)
        if t is None:
            fail(f"[instance/ref] {where}: instantiates -> unknown template atom {tid}")
            continue
        if tid in decided:
            fail(f"[instance/duplicate] {where}: second decision for {tid} "
                 f"(already {decided[tid]!r})")
        decided[tid] = e.get("decision")
        dec, d = e.get("decision"), _tdisp(t)
        if dec not in gov_decision:
            fail(f"[instance/decision] {where}: '{dec}' is not a governed disposition_decision")
        elif d is None:
            fail(f"[instance/decision] {where}: template atom {tid} carries no content_disposition "
                 f"— there is nothing to decide")
        elif dec not in LEGAL_DECISIONS.get(d, set()):
            fail(f"[instance/decision] {where}: '{dec}' is not legal for a '{d}' slot "
                 f"(legal: {sorted(LEGAL_DECISIONS.get(d, set())) or 'none — it is filled by an atom'})")
        # 'modified' is the one decision that produces new meaning, so it is the one decision that
        # must name an atom. Every other value is text-free and must NOT.
        auth = e.get("authored_atom")
        if dec == "modified":
            if auth is None:
                fail(f"[instance/decision] {where}: 'modified' but no authored_atom carries the "
                     f"modified text")
            elif auth not in ids:
                fail(f"[instance/ref] {where}: authored_atom -> unknown atom {auth}")
            elif store_by_id[auth].get("bindings", {}).get("instance", {}).get("instantiates") != tid:
                fail(f"[instance/decision] {where}: authored_atom {auth} does not instantiate {tid}")
        elif auth is not None:
            fail(f"[instance/decision] {where}: '{dec}' names authored_atom {auth}, but only "
                 f"'modified' produces new meaning")
        if e.get("decided_by"):
            _govcheck(where, "role", e["decided_by"], gov_roles, pending_roles, prop_roles)
        if e.get("template_source_hash") and e["template_source_hash"] != t.get("content_hash"):
            stale.append(where)
            flag(f"[instance/stale] {where}: template atom {tid} has changed since this decision "
                 f"was recorded")

    # An atom and a non-'modified' decision on the same slot are contradictory instructions to the
    # projection: one says render this text, the other says the template's text stands (or goes).
    for (tid, _slot), aid in seen_keys.items():
        if tid in decided and decided[tid] != "modified":
            fail(f"[instance/conflict] {aid} authors {tid} but instance_decisions records "
                 f"'{decided[tid]}' for it")

    # ---- completeness: what this instance still owes ----
    # Soft by design: an instance is drafted incrementally. But it may not be PROMOTED while any
    # template slot is unanswered — that is the difference between a draft and a document.
    for t in tpl_atoms:
        tid, d = t["atom_id"], _tdisp(t)
        if d is None:
            continue
        if d == "authorable":
            if (tid, None) not in seen_keys:
                owed_values.append(f"{tid} (authorable)")
        elif d == "controlled_standard" and _tslots(t):
            for s in sorted(_tslots(t)):
                if (tid, s) not in seen_keys:
                    owed_values.append(f"{tid}#{s}")
        elif tid not in decided:
            owed_decisions.append(f"{tid} ({d})")
    if owed_values or owed_decisions:
        flag(f"[instance/incomplete] {len(owed_values)} value(s) and {len(owed_decisions)} "
             f"decision(s) still owed against the pinned template")

# ---- report ----
statuses = {a["governance"]["status"] for a in atoms}
print("="*68)
_mf = PROJ / "manifest.json"
_project = load(_mf).get("project", PROJ.name) if _mf.exists() else PROJ.name
_facets = sorted({k for a in atoms for k in a.get("bindings", {})})
print(f"VALIDATION GATE — project {_project} — {len(atoms)} atoms")
print(f"facets present: {', '.join(_facets) or '(none)'}")
if TPL is not None:
    print(f"instance of  : {_pin.get('document','?')} v{_pin.get('version','?')} "
          f"— {len(tpl_atoms)} template atoms, {len(instance_atoms)} authored value(s), "
          f"{len(decisions)} decision(s)")
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
# The owed list is the instance's to-do, and the answer to "what does this ALSAP still need?".
# Printed in full rather than summarised: a silently truncated list reads as "nothing left".
if TPL is not None and (owed_values or owed_decisions):
    print(f"STILL OWED — {len(owed_values)} value(s), {len(owed_decisions)} decision(s):")
    for m in owed_values:    print("  value    ", m)
    for m in owed_decisions: print("  decision ", m)
    print("-"*68)
gate_ok = (len(hard) == 0)
promote_ok = gate_ok and (len(soft) == 0)
print(f"GATE @ draft : {'PASS' if gate_ok else 'FAIL'}")
print(f"PROMOTE >draft: {'PASS' if promote_ok else 'BLOCKED (adopt proposed registry extensions first)'}")
sys.exit(0 if gate_ok else 1)
