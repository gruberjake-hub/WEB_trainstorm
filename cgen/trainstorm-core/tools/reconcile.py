#!/usr/bin/env python3
"""
Reconcile — fold an SME's marked-up review matrix BACK into canon.

This is the return leg that makes the loop bidirectional. For every row the SME filled in
`proposed_source_text`, the matching atom is updated in place:
  - meaning.source_text := the SME's text
  - content_hash        := recomputed (meaning CHANGED → downstream renderings/translations go stale)
  - governance.version  := +1
  - governance.status   := in_review (SME-reviewed, pending approval)

HONEST NOTE surfaced by this build: the atom's `governance` object is additionalProperties:false and
has NO field for review provenance (who / when / why / which source_hash was reviewed). So the audit
trail can't live in the atom without breaking the schema. It lives instead in an EXTERNAL store keyed
by atom_id — reconciliation_log.json — exactly like locale packs / renderings. Reference, don't embed:
the atom stays clean; the audit trail is another keyed side-store.

Usage: python3 tools/reconcile.py <filled_matrix.csv>
"""
import json, csv, hashlib, pathlib, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
STORE = ROOT / "store" / "projects" / "ast_alsap"
MATRIX = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else STORE / "review_matrix.filled.csv"

atoms = json.loads((STORE / "atoms.json").read_text())
idx = {a["atom_id"]: a for a in atoms}
today = datetime.date.today().isoformat()

def h(meaning):
    return "sha256:" + hashlib.sha256(
        json.dumps(meaning, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

def clean(t):
    i = t.find("[Headwater")
    return t[:i].strip() if i != -1 else t.strip()

log_path = STORE / "reconciliation_log.json"
log = json.loads(log_path.read_text()) if log_path.exists() else {
    "_note": "External reconciliation/audit store, keyed by atom_id. Holds the review provenance the "
             "atom's governance object has no field for (who/when/why/from-hash). Reference, don't embed.",
    "project": "ast_alsap", "events": []
}

changed = []
with MATRIX.open() as f:
    for row in csv.DictReader(f):
        proposed = (row.get("proposed_source_text") or "").strip()
        aid = row["atom_id"]
        if not proposed or aid not in idx:
            continue
        a = idx[aid]
        if proposed == clean(a["meaning"]["source_text"]):
            continue  # no real change
        before_text = a["meaning"]["source_text"]
        before_hash = a.get("content_hash")
        before_ver = a["governance"]["version"]
        # apply the SME edit to canon
        a["meaning"]["source_text"] = proposed
        after_hash = h(a["meaning"])
        a["content_hash"] = after_hash
        a["governance"]["version"] = before_ver + 1
        a["governance"]["status"] = "in_review"
        log["events"].append({
            "atom_id": aid, "date": today,
            "reviewer": row.get("reviewer_id") or "unknown_reviewer",
            "note": row.get("reviewer_note") or "",
            "from_version": before_ver, "to_version": before_ver + 1,
            "from_hash": before_hash, "to_hash": after_hash,
            "meaning_changed": before_hash != after_hash,
            "text_before": clean(before_text), "text_after": proposed
        })
        changed.append((aid, before_hash, after_hash, before_ver, before_ver + 1, row.get("reviewer_note", "")))

(STORE / "atoms.json").write_text(json.dumps(atoms, indent=2, ensure_ascii=False))
log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False))

print("=" * 68)
print(f"RECONCILE — {MATRIX.name} -> canon")
print("=" * 68)
if not changed:
    print("No edits found in the matrix.")
else:
    print(f"{len(changed)} atom(s) reconciled into canon (version bumped, status -> in_review):\n")
    for aid, bh, ah, bv, av, note in changed:
        print(f"  {aid}")
        print(f"    v{bv} -> v{av} | hash {bh[7:15]}… -> {ah[7:15]}…  (meaning CHANGED -> downstream stale)")
        if note: print(f"    reviewer note: {note}")
    print(f"\nAudit trail: {len(changed)} event(s) appended to reconciliation_log.json (external, keyed by atom_id).")
    print("Staleness: each changed content_hash invalidates any facet that bound against the OLD")
    print("source_hash (locale packs, renderings). No locale packs yet, so notional — but the trigger fired.")
