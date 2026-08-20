#!/usr/bin/env python3
"""
accept_value — the ONLY writer into an ALSAP instance store.

This is the acceptance half of the authoring loop. Amanuensis proposes; a human accepts; this script
is what acceptance *is*, mechanically. The agent writes nothing — it has no path to the store — and
that is enforced by there being exactly one script, run by a person, that can put a value in.

    # fill an authorable slot
    accept_value.py --project <instance> --slot <template atom_id> \
        --value "..." [--select <governed value id>] --by role_alsap_lead [--agent amanuensis]

    # fill ONE named slot inside retained standard text
    accept_value.py --project <instance> --slot <template atom_id> --fills-slot participant_count \
        --value "412" --by role_alsap_lead

    # record what was done with template text that is NOT authored into
    accept_value.py --project <instance> --slot <template atom_id> --decision deleted \
        --by role_alsap_lead

Two writes, one owner. Values that carry new meaning become atoms in atoms.json; decisions that
carry no meaning go to instance_decisions.json, external and atom_id-keyed — the same
reference-don't-embed move as reconciliation_log.json. `modified` is the one decision that does both.

Every write PINS the template: document, version, and the template atom's content_hash at the moment
of acceptance. That pin is what makes staleness a one-line walk later instead of a re-read of the
controlled document.

Note on store_merge: this deliberately does NOT use store_merge.merge(). That rule serialises a whole
authored decomposition and orphans anything absent from it — correct for an ingest, wrong here, where
an author fills one slot at a time over weeks and the other 30 slots being absent means "not yet",
not "deleted". The genuinely shared piece, stamp() (content_hash + key order), IS imported, so the
hash rule still lives in one place.
"""
import json, pathlib, sys, argparse, datetime
import harness_paths
from store_merge import stamp

P = harness_paths.resolve()
PROJ, TPL, REG = P["project_dir"], P.get("template_dir"), P["registry_dir"]
if TPL is None:
    raise SystemExit(f"{PROJ} declares no instantiates_template — not an instance store.")

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--slot", required=True)
ap.add_argument("--fills-slot", dest="fills_slot")
ap.add_argument("--value")
ap.add_argument("--select")
ap.add_argument("--decision")
ap.add_argument("--by", dest="authored_by")
ap.add_argument("--agent")
ap.add_argument("--on", help="ISO date of acceptance; defaults to today")
A, _ = ap.parse_known_args()

if not A.value and not A.select and not A.decision:
    raise SystemExit("Nothing to accept: pass --value / --select (a value) or --decision.")
if A.decision and A.decision != "modified" and (A.value or A.select):
    raise SystemExit(f"--decision {A.decision} carries no text; drop --value/--select "
                     f"(only 'modified' produces new meaning).")

def load(p, d=None):
    p = pathlib.Path(p)
    return json.loads(p.read_text()) if p.exists() else d

manifest = load(PROJ / "manifest.json", {})
pin = manifest.get("instantiates_template") or {}
tpl = {a["atom_id"]: a for a in load(TPL / "atoms.json", [])}

t = tpl.get(A.slot)
if t is None:
    raise SystemExit(f"{A.slot} is not in the pinned template store ({TPL}).")
tform = t.get("bindings", {}).get("form", {})
tdisp = tform.get("content_disposition")
today = A.on or datetime.date.today().isoformat()

# The template's own rules decide what may happen to this slot. Refuse early and in plain words —
# the gate will refuse too, but an author deserves the reason before the write, not after.
declared = {s["id"] for s in tform.get("constraints", {}).get("slots", [])}
if A.fills_slot and A.fills_slot not in declared:
    raise SystemExit(f"'{A.fills_slot}' is not a declared slot on {A.slot} "
                     f"(declared: {sorted(declared) or 'none'}).")
if (A.value or A.select) and tdisp == "controlled_standard" and not A.fills_slot:
    raise SystemExit(f"{A.slot} is controlled_standard: its text is retained and resolved from the "
                     f"template, never copied into an instance. Fill one of its declared slots "
                     f"({sorted(declared) or 'none declared'}) or record a --decision instead.")
# The same legality matrix the gate enforces, checked here so the refusal arrives before the write.
# The GATE remains the authority — a hand-edited store still has to answer to it.
LEGAL_DECISIONS = {
    "controlled_standard":     {"retained", "marked_not_applicable"},
    "example":                 {"retained", "modified", "deleted"},
    "instructional_transient": {"deleted"},
    "authorable":              set(),
}
if A.decision and A.decision not in LEGAL_DECISIONS.get(tdisp, set()):
    _legal = sorted(LEGAL_DECISIONS.get(tdisp, set()))
    raise SystemExit(f"'{A.decision}' is not legal for a '{tdisp}' slot (legal: "
                     + (", ".join(_legal) if _legal
                        else "none — an authorable slot is filled with --value, not decided") + ").")
if (A.value or A.select) and tdisp == "instructional_transient":
    raise SystemExit(f"{A.slot} is instructional_transient — guidance to be deleted before final, "
                     f"not a slot to author into. Use --decision deleted.")

atoms = load(PROJ / "atoms.json", [])
by_id = {a["atom_id"]: a for a in atoms}
dec_doc = load(PROJ / "instance_decisions.json", {
    "instance": manifest.get("project"),
    "template_document": pin.get("document"),
    "template_version": pin.get("version"),
    "_note": "Decisions recorded against template atoms this instance does NOT author into. "
             "External and atom_id-keyed because they carry no meaning, and only meaning embeds "
             "in an atom. Governed by vocab/instance.enum.json disposition_decision.",
    "decisions": [],
})

wrote = []

# ---- the authored value (an atom, because it carries new meaning) ----
if A.value or A.select:
    # Semantic-but-stable id, matching the house style of the template store. The slot suffix is
    # what makes (instantiates, fills_slot) a real compound key rather than a convention.
    tail = A.slot[len("atom_"):] if A.slot.startswith("atom_") else A.slot
    aid = f"atom_{manifest.get('project','instance')}__{tail}" + (f"__{A.fills_slot}" if A.fills_slot else "")

    # For a controlled value set the authored meaning IS the choice, and the choice is an id. The
    # option's label and definition live once, in the options registry — writing the prose here
    # would spawn the drifting second copy the whole registry tier exists to prevent.
    text = A.value if A.value else A.select
    inst = {
        "instantiates": A.slot,
        "template_document": pin.get("document"),
        "template_version": pin.get("version"),
        "template_source_hash": t.get("content_hash"),
    }
    if A.fills_slot: inst["fills_slot"] = A.fills_slot
    if A.select:     inst["selected_value"] = A.select
    if tdisp == "example": inst["disposition_decision"] = "modified"
    if A.authored_by:      inst["authored_by"] = A.authored_by
    if A.agent:            inst["proposed_by_agent"] = A.agent

    prior = by_id.get(aid)
    if prior is None:
        atoms.append({
            "atom_id": aid,
            "meaning": {"source_locale": "en", "source_text": text, "kind": "instance_value"},
            "bindings": {"instance": inst},
            "governance": {"version": 1, "status": "draft", "regulatory_binding": "regulatory",
                           "owner": A.authored_by or "role_alsap_lead"},
        })
        wrote.append(f"MINT   {aid} v1/draft")
    else:
        changed = prior["meaning"]["source_text"] != text
        prior["meaning"]["source_text"] = text
        prior["bindings"]["instance"] = inst
        if changed:
            # New meaning on a controlled document: prior sign-off no longer covers this content.
            prior["governance"]["version"] += 1
            prior["governance"]["status"] = "draft"
            prior["governance"].pop("approved_by", None)
            prior["governance"].pop("effective_date", None)
            wrote.append(f"UPDATE {aid} v{prior['governance']['version']}/draft (meaning changed, "
                         f"approvals cleared)")
        else:
            wrote.append(f"REPIN  {aid} (same meaning; template pin refreshed)")

# ---- the decision (no atom, because there is no new meaning) ----
if A.decision:
    entry = {
        "instantiates": A.slot,
        "decision": A.decision,
        "template_source_hash": t.get("content_hash"),
        "decided_by": A.authored_by,
        "decided_on": today,
    }
    if A.decision == "modified":
        tail = A.slot[len("atom_"):] if A.slot.startswith("atom_") else A.slot
        entry["authored_atom"] = f"atom_{manifest.get('project','instance')}__{tail}"
    dec_doc["decisions"] = [d for d in dec_doc["decisions"] if d.get("instantiates") != A.slot]
    dec_doc["decisions"].append(entry)
    dec_doc["decisions"].sort(key=lambda d: d["instantiates"])
    wrote.append(f"DECIDE {A.slot} -> {A.decision}")

(PROJ / "atoms.json").write_text(json.dumps(stamp(atoms), indent=2, ensure_ascii=False) + "\n")
(PROJ / "instance_decisions.json").write_text(json.dumps(dec_doc, indent=2, ensure_ascii=False) + "\n")

print("=" * 70)
print(f"ACCEPTED into {manifest.get('project')} — against {pin.get('document')} v{pin.get('version')}")
print("=" * 70)
print(f"  template slot : {A.slot}" + (f"#{A.fills_slot}" if A.fills_slot else ""))
print(f"  disposition   : {tdisp}")
for w in wrote:
    print(f"  {w}")
print(f"  store         : {len(atoms)} authored value(s), {len(dec_doc['decisions'])} decision(s)")
print("  next          : run validate_atoms.py --project <this store> before trusting it.")
