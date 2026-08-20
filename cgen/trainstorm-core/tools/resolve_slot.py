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


# ---------- --verify-prompt : acceptance criterion #1, made runnable ----------
if A.verify_prompt is not None:
    # No atom's source text may appear in the agent's prompt. If it does, the prompt has become a
    # second copy of the controlled document.
    leaks, checked = [], []
    for f in A.verify_prompt:
        text = pathlib.Path(f).read_text()
        checked.append(f)
        for a in atoms:
            src = a["meaning"]["source_text"].strip().rstrip(".")
            if len(src) < 25:
                continue          # short labels ("Cover.", "Author.") are not content
            if src in text:
                leaks.append((f, a["atom_id"], src[:70]))
    print("=" * 70)
    print(f"PROMPT PURITY — {len(atoms)} atoms vs {len(checked)} prompt file(s)")
    print("=" * 70)
    for f in checked:
        print(f"  checked: {f}")
    if leaks:
        for f, aid, s in leaks:
            print(f"  x LEAK {f}: contains {aid} — \"{s}...\"")
        print("VERDICT: FAIL — the prompt carries ALSAP content; it is a second source of truth.")
        sys.exit(1)
    print("VERDICT: PASS — no atom content found in the prompt. Grounding is a walk, not a paste.")
    sys.exit(0)


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

conds = {
    "this_slot_applies_when": [
        {**c, "field_text": by_id.get(c["field"], {}).get("meaning", {}).get("source_text")}
        for c in form(slot).get("conditional_on", [])],
    "fields_conditional_on_this_slot": [
        {"atom_id": a["atom_id"], "text": a["meaning"]["source_text"],
         "equals": next((c.get("equals") for c in form(a).get("conditional_on", [])
                         if c["field"] == slot["atom_id"]), None)}
        for a in atoms
        if any(c["field"] == slot["atom_id"] for c in form(a).get("conditional_on", []))],
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
                "performed_by": [ROLES.get(r, {}).get("label", r) for r in p.get("performed_by", [])],
                "produces_records": [RECORDS.get(r, {}).get("label", r) for r in p.get("produces_records", [])],
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
    "accountable": [ROLES.get(r, {}).get("label", r) for r in form(slot).get("performed_by", [])],
    "captures_record": RECORDS.get(form(slot).get("captures_record", ""), {}).get("label"),
    "conditions": conds,
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
print(f"  accountable : {', '.join(packet['accountable']) or '—'}")
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
    print(f"                [{p['step_type']}] {', '.join(p['performed_by'])}: {p['text'][:80]}")
print(f"  gaps        : {len(packet['gaps'])}")
for g in packet["gaps"]:
    print(f"                ! {g}")
