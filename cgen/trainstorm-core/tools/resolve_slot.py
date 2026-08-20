#!/usr/bin/env python3
"""
resolve_slot — assemble the grounding packet for ONE ALSAP template slot.

This is the render step for an agent-shaped target. Where project_sop.py projects atoms into a
controlled document, this projects atoms into the working context of an authoring agent: the slot,
where it sits, the guidance around it, the governed values it may take, who is accountable, and the
procedure steps that govern the template's use.

Why it exists at all: the Amanuensis prompt is thin and stable and carries ZERO ALSAP content. If the
agent's knowledge of the ALSAP lived in its prompt, that prompt would be a second source of truth that
drifts the moment the template is revised. Instead the knowledge is a walk, resolved at run time, so a
template revision changes what the agent knows without anyone editing a prompt.

  python3 tools/resolve_slot.py --project <store> --slot <atom_id> [--procedure <other store>]
  python3 tools/resolve_slot.py --project <store> --list
  python3 tools/resolve_slot.py --project <store> --verify-prompt <file> [<file> ...]

Reading across store boundaries is allowed here: the packet is ephemeral context. Persisting an
atom_id across that boundary is not, and this tool never writes.
"""
import json, sys, pathlib, argparse
import harness_paths

P = harness_paths.resolve()
REG, PROJ = P["registry_dir"], P["project_dir"]

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--slot"); ap.add_argument("--procedure"); ap.add_argument("--out")
ap.add_argument("--instance", help="an instance store overlaying this template — what has been authored so far")
ap.add_argument("--list", action="store_true")
ap.add_argument("--verify-prompt", nargs="*")
A, _ = ap.parse_known_args()

def load(p, default=None):
    p = pathlib.Path(p)
    return json.loads(p.read_text()) if p.exists() else default

atoms = load(PROJ / "atoms.json", [])
by_id = {a["atom_id"]: a for a in atoms}
manifest = load(PROJ / "manifest.json", {})

def reg(name, key):
    d = load(REG / name, {key: []})
    return {e["id"]: e for e in d.get(key, [])}

ROLES, RECORDS, DOCS = reg("roles.registry.json", "roles"), reg("records.registry.json", "records"), reg("docs.registry.json", "docs")
OPTIONS = reg("options.registry.json", "options")

def form(a): return a.get("bindings", {}).get("form", {})
def disp(a): return form(a).get("content_disposition")

def idlabel(reg, i):
    """Carry the id AND the label. A label alone cannot be checked against a registry, so an agent
    handed only labels cannot run the 'ungoverned value' drift check its own contract demands."""
    return {"id": i, "label": reg.get(i, {}).get("label", i), "governed": i in reg}

# The decisions an agent may propose on a non-authorable slot. Governed, so it is handed over rather
# than left to be guessed — the first dispatch invented `as_is` precisely because it was absent.
_dv = P["vocab_dir"] / "instance.enum.json"
DECISIONS = []
if _dv.exists():
    _d = json.loads(_dv.read_text())
    DECISIONS = [{"id": v["id"], "label": v.get("label"), "definition": v.get("definition")}
                 for v in _d.get("dimensions", {}).get("disposition_decision", {}).get("values", [])]


# ---------- --verify-prompt : acceptance criterion #1, made runnable ----------
if A.verify_prompt is not None:
    # The rule itself lives in prompt_purity.py — resolve_prompt.py enforces the same one, and a
    # second copy of it would drift exactly like a second copy of a schema.
    import prompt_purity
    texts = {f: pathlib.Path(f).read_text() for f in A.verify_prompt}
    ok = prompt_purity.report(atoms, texts, prompt_purity.scan(atoms, texts))
    sys.exit(0 if ok else 1)


# ---------- --list : the slots an author (and the agent) still owes ----------
if A.list:
    print(f"{'atom_id':66} {'kind':13} {'field_type':12} disposition")
    for a in atoms:
        d = disp(a)
        if d in ("authorable", "example"):
            print(f"{a['atom_id']:66} {a['meaning']['kind']:13} "
                  f"{form(a).get('field_type','-'):12} {d}")
    sys.exit(0)


if not A.slot:
    raise SystemExit("--slot <atom_id> required (or --list / --verify-prompt).")
slot = by_id.get(A.slot)
if slot is None:
    raise SystemExit(f"{A.slot} is not in {PROJ/'atoms.json'}.")


def ancestry(a):
    out, cur = [], a
    while True:
        parent = by_id.get(cur.get("bindings", {}).get("object", {}).get("belongs_to"))
        if parent is None:
            break
        out.append({"atom_id": parent["atom_id"], "kind": parent["meaning"]["kind"],
                    "text": parent["meaning"]["source_text"]})
        cur = parent
    return list(reversed(out))


parent = slot.get("bindings", {}).get("object", {}).get("belongs_to")
def under(root):
    """every descendant of `root` via object.belongs_to"""
    seen, frontier = set(), [root]
    while frontier:
        cur = frontier.pop()
        for a in atoms:
            if a.get("bindings", {}).get("object", {}).get("belongs_to") == cur and a["atom_id"] not in seen:
                seen.add(a["atom_id"]); frontier.append(a["atom_id"])
    return seen

# guidance = instructional/example atoms anywhere under the slot's own section, minus the ones
# already attached to a specific option value (those ride with the option, not the section)
# Option-scoped guidance rides with its own option and must never leak in as ambient section
# guidance elsewhere: the Benefit-Risk phrasings belong to br_profile's values, not to every field
# that happens to share the section.
_attached = {x["atom_id"] for x in atoms
             if any(c.get("equals") for c in form(x).get("conditional_on", []))}
guidance = [{"atom_id": a["atom_id"], "disposition": disp(a),
             "text": a["meaning"]["source_text"]}
            for a in atoms
            if a["atom_id"] != slot["atom_id"]
            and a["atom_id"] in under(parent)
            and a["atom_id"] not in _attached
            and disp(a) in ("instructional_transient", "example")]

opts = None
if form(slot).get("options_ref"):
    ref = form(slot)["options_ref"]
    entry = OPTIONS.get(ref)
    # Attach each governed value's own conditional guidance: atoms that apply only when THIS slot
    # holds THAT value. That is what makes the packet useful to an authoring agent — "you chose
    # conditional_favorable, here is the sanctioned phrasing for it, and nothing else."
    vals = []
    for v in (entry or {}).get("values", []):
        vals.append({**v, "guidance": [
            {"atom_id": x["atom_id"], "disposition": disp(x), "text": x["meaning"]["source_text"]}
            for x in atoms
            if any(c["field"] == slot["atom_id"] and c.get("equals") == v["id"]
                   for c in form(x).get("conditional_on", []))]})
    opts = {"options_ref": ref, "governed": entry is not None,
            "label": (entry or {}).get("label"),
            "description": (entry or {}).get("description"),
            "values": vals}

def resolve_options(ref):
    e = OPTIONS.get(ref)
    return {"options_ref": ref, "governed": e is not None,
            "values": [{k: v[k] for k in ("id", "label", "description") if k in v}
                       for v in (e or {}).get("values", [])]}

def controlling(c):
    """A slot conditional on another must be handed the CONTROLLING field resolved — its type, its
    governed value set, and the predicate. Without them 'the selected profile' has no referent and
    the dependent slot is undraftable no matter how complete its own entry is."""
    ctrl = by_id.get(c["field"])
    out = {**c, "field_text": (ctrl or {}).get("meaning", {}).get("source_text")}
    if ctrl is not None:
        out["field_type"] = form(ctrl).get("field_type")
        out["content_disposition"] = disp(ctrl)
        if form(ctrl).get("options_ref"):
            out["options"] = resolve_options(form(ctrl)["options_ref"])
    if "equals" not in c:
        out["predicate"] = ("UNSPECIFIED — the decomposition records a dependency on this field but "
                            "no triggering value; treat as 'applies whenever the field is set'")
    return out

conds = {
    "this_slot_applies_when": [controlling(c) for c in form(slot).get("conditional_on", [])],
    "fields_conditional_on_this_slot": [
        {"atom_id": a["atom_id"], "text": a["meaning"]["source_text"],
         "equals": next((c.get("equals") for c in form(a).get("conditional_on", [])
                         if c["field"] == slot["atom_id"]), None)}
        for a in atoms
        if any(c["field"] == slot["atom_id"] for c in form(a).get("conditional_on", []))],
}

# What has already been authored for THIS asset. A slot conditional on another is undraftable without
# it — "the selected Benefit-Risk profile" has no referent until you can see which one was selected.
# Read-only and ephemeral, like every other section here.
inst_view = None
if A.instance:
    ia = load(pathlib.Path(A.instance) / "atoms.json", [])
    idec = load(pathlib.Path(A.instance) / "instance_decisions.json", {}).get("decisions", [])
    interest = {slot["atom_id"]} | {c["field"] for c in form(slot).get("conditional_on", [])}
    def _v(a):
        b = a["bindings"]["instance"]
        return {"atom_id": a["atom_id"], "instantiates": b["instantiates"],
                "fills_slot": b.get("fills_slot"), "selected_value": b.get("selected_value"),
                "text": a["meaning"]["source_text"],
                "governance": a["governance"],
                "template_source_hash": b.get("template_source_hash"),
                "stale": b.get("template_source_hash") != by_id.get(b["instantiates"], {}).get("content_hash")}
    vals = [_v(a) for a in ia if a.get("bindings", {}).get("instance", {}).get("instantiates") in interest]
    inst_view = {
        "instance": load(pathlib.Path(A.instance) / "manifest.json", {}).get("project"),
        "this_slot": [v for v in vals if v["instantiates"] == slot["atom_id"]],
        "fields_this_slot_depends_on": [v for v in vals if v["instantiates"] != slot["atom_id"]],
        "decisions": [d for d in idec if d["instantiates"] in interest],
    }

# cross-store: the procedure steps that govern use of THIS template
proc_steps = []
doc = manifest.get("source_document")
if A.procedure and doc:
    for a in load(pathlib.Path(A.procedure) / "atoms.json", []):
        p = a.get("bindings", {}).get("procedure", {})
        if doc in p.get("references", []):
            proc_steps.append({
                "atom_id": a["atom_id"], "step_type": p.get("step_type"),
                "performed_by": [idlabel(ROLES, r) for r in p.get("performed_by", [])],
                "produces_records": [idlabel(RECORDS, r) for r in p.get("produces_records", [])],
                "text": a["meaning"]["source_text"]})

packet = {
    "_note": "Ephemeral grounding for one slot, assembled by a walk over the atom store. Not canon, "
             "not stored. The agent's entire knowledge of the ALSAP for this slot.",
    "project": manifest.get("project"), "source_document": doc,
    "slot": {"atom_id": slot["atom_id"], "content_hash": slot.get("content_hash"),
             "text": slot["meaning"]["source_text"], "kind": slot["meaning"]["kind"],
             "field_type": form(slot).get("field_type"),
             "content_disposition": disp(slot),
             "constraints": form(slot).get("constraints", {})},
    "path": ancestry(slot),
    "guidance": guidance,
    "options": opts,
    "accountable": [idlabel(ROLES, r) for r in form(slot).get("performed_by", [])],
    "captures_record": (idlabel(RECORDS, form(slot)["captures_record"])
                        if form(slot).get("captures_record") else None),
    # An agent is asked to record the source_hash it bound against AND which version of a governed
    # list it resolved. It can only do the second if the packet carries the version.
    "governance": {**slot.get("governance", {}), "content_hash": slot.get("content_hash")},
    "disposition_decisions_available": {
        "values": DECISIONS,
        "_when_none_is_owed":
            "A slot you FILL owes no decision. That covers an `authorable` field and a "
            "`controlled_standard` field with declared `constraints.slots` — for the latter the slot "
            "values ARE the record that the sentence was retained and completed, so do not look for a "
            "`retained_with_fills` id. There is none, and none is needed.",
    },
    "conditions": conds,
    "instance_so_far": inst_view,
    "procedure": proc_steps,
    "gaps": [],
}
for k, why in (("guidance", "no instructional or example siblings in this section"),
               ("procedure", "no governing procedure steps supplied (pass --procedure)"),
               ("accountable", "no performed_by roles on this slot")):
    if not packet[k]:
        packet["gaps"].append(f"{k}: {why}")
if opts and not opts["governed"]:
    packet["gaps"].append(f"options: {opts['options_ref']} is not in the governed options registry")

# `gaps` answers "did the walk resolve everything it referenced?" — an ASSEMBLY question. It does not
# answer "is this enough to fill the slot?" Every agent in the 2026-08-20 dispatch read an empty
# `gaps` as licence to proceed and then had to work out for itself that the decisive input was
# missing. Saying so here costs one field and removes the ambiguity.
_authorable = disp(slot) in ("authorable",) or bool(form(slot).get("constraints", {}).get("slots"))
packet["sufficiency"] = {
    "packet_carries": "template structure + drafting guidance + governing procedure. Grounding for "
                      "WHAT this slot requires and WHO owns it.",
    "packet_does_not_carry": "any evidence about the asset being documented — no safety data, no "
                             "study results, no adverse-event terms, no participant counts, no asset "
                             "identity beyond what the template itself states. There is no asset "
                             "dossier corpus in the manifold yet.",
    "verdict": ("INSUFFICIENT TO FILL — this slot is authored from asset evidence, which this packet "
                "does not contain. Propose the shape and the constraints; do not invent the content."
                if _authorable else
                "SUFFICIENT FOR POSTURE — this slot is not authored from asset evidence; the packet "
                "carries what is needed to decide what may be done with it."),
}

out = json.dumps(packet, indent=2, ensure_ascii=False)
if A.out:
    pathlib.Path(A.out).write_text(out); print(f"packet -> {A.out}")

print("=" * 70)
print(f"GROUNDING PACKET — {slot['atom_id']}")
print("=" * 70)
print(f"  path        : {' > '.join(p['text'].rstrip('.') for p in packet['path']) or '(root)'}")
s = packet["slot"]
print(f"  slot        : {s['text']}")
print(f"  type        : {s['field_type']} · {s['content_disposition']} · {s['constraints'] or '{}'}")
for sl in s.get("constraints", {}).get("slots", []):
    print(f"  slot to fill: [{sl['id']}] {sl['expects']}"
          + (f"  (values: {sl['options_ref']})" if sl.get("options_ref") else ""))
print(f"  accountable : {', '.join(r['label'] for r in packet['accountable']) or '—'}")
if opts:
    print(f"  options     : {opts['options_ref']} "
          f"({'GOVERNED' if opts['governed'] else 'NOT GOVERNED'}) — {len(opts['values'])} values")
    for v in opts["values"]:
        print(f"                - {v['id']:24} {v['label']}")
        for g in v.get("guidance", []):
            print(f"                    [{g['disposition'][:12]}] {g['text'][:72]}")
print(f"  guidance    : {len(packet['guidance'])} sibling atom(s)")
for g in packet["guidance"]:
    print(f"                [{g['disposition']}] {g['text'][:88]}")
c = packet["conditions"]
for x in c["this_slot_applies_when"]:
    print(f"  applies when: {x['field']} == {x.get('equals')}")
for x in c["fields_conditional_on_this_slot"]:
    if x["equals"] is None:
        print(f"  drives      : {x['atom_id']}")
print(f"  procedure   : {len(proc_steps)} governing step(s)")
for p in proc_steps:
    print(f"                [{p['step_type']}] {', '.join(r['label'] for r in p['performed_by'])}: {p['text'][:80]}")
print(f"  gaps        : {len(packet['gaps'])}")
for g in packet["gaps"]:
    print(f"                ! {g}")
