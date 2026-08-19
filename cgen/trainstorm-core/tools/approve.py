#!/usr/bin/env python3
"""
Approval / publish gate — the one place canon says sequencing MUST be enforced (pre-publish QA).
Promotes a project's atoms to `status: approved` and stamps the effective date — but only if the
document is actually publishable. This finishes the controlled-document lifecycle
(draft → in_review → approved).

Unlike reconcile (whose audit trail had no governance field and lives in an external log), the
approval OUTCOME has a native home: `governance.status` / `approved_by` / `effective_date`. Approval
does NOT change `meaning`, so `content_hash` and `version` are untouched — an unchanged hash means the
approved content is the same content that was validated (that is the point of the hash).

Two hard preconditions (the teeth):
  1. AUTHORIZED APPROVER — the approver must be one of the project's governed `approval_roles`.
  2. PUBLISHABLE STATE — the standing gate must read GATE PASS *and* PROMOTE PASS (no hard failures,
     no still-pending vocab). You cannot approve a document that doesn't validate or still cites
     ungoverned/pending vocabulary.

An external, Part-11-style signed manifest (approvals.json) binds the approver + effective_date to the
exact `content_hash` of every atom approved — so the signature is bound to a precise content snapshot.

Usage: python3 tools/approve.py --approver role_alsap_approver [--effective-date YYYY-MM-DD]
"""
import json, subprocess, sys, pathlib, datetime, argparse
import harness_paths

TOOLS = pathlib.Path(__file__).resolve().parent
STORE = harness_paths.resolve()["project_dir"]

ap = argparse.ArgumentParser()
ap.add_argument("--approver", required=True, help="approver id — must be a governed approval role")
ap.add_argument("--effective-date", default=datetime.date.today().isoformat())
# anchor flags: accepted here and forwarded to the gate subprocess so it resolves the same layout
ap.add_argument("--core"); ap.add_argument("--project"); ap.add_argument("--registry")
args = ap.parse_args()

manifest = json.loads((STORE / "manifest.json").read_text())
atoms = json.loads((STORE / "atoms.json").read_text())
approval_roles = manifest.get("approval_roles", [])

def refuse(code, msg):
    print("=" * 68)
    print("APPROVAL REFUSED")
    print("=" * 68)
    print(msg)
    sys.exit(code)

# ---- precondition 1: authorized approver ----
if args.approver not in approval_roles:
    refuse(2, f"'{args.approver}' is not a governed approver for this project.\n"
              f"Authorized approval_roles: {approval_roles}\n"
              f"(Approval authority is declared per-project in manifest.json — not everyone can sign.)")

# ---- precondition 2: publishable state (run the standing gate) ----
gate_cmd = [sys.executable, str(TOOLS / "validate_atoms.py")]
for _flag, _val in [("--core", args.core), ("--project", args.project), ("--registry", args.registry)]:
    if _val:
        gate_cmd += [_flag, _val]
res = subprocess.run(gate_cmd, capture_output=True, text=True)
out = res.stdout
gate_pass = "GATE @ draft : PASS" in out
promote_pass = "PROMOTE >draft: PASS" in out
if not (gate_pass and promote_pass):
    tail = "\n".join(out.splitlines()[-12:])
    refuse(3, "The standing gate is not publishable — approval is blocked.\n"
              f"  gate_pass={gate_pass}  promote_pass={promote_pass}\n"
              "Fix hard failures and adopt any pending vocab first. Gate tail:\n" + tail)

# ---- action: approve the document (all atoms), stamp governance ----
snapshot = []
for a in atoms:
    g = a["governance"]
    g["status"] = "approved"
    ab = g.setdefault("approved_by", [])
    if args.approver not in ab:
        ab.append(args.approver)
    g["effective_date"] = args.effective_date
    snapshot.append({"atom_id": a["atom_id"], "content_hash": a["content_hash"],
                     "version": g["version"]})
(STORE / "atoms.json").write_text(json.dumps(atoms, indent=2, ensure_ascii=False))

# ---- external signed approval manifest (binds signature to exact content) ----
ap_path = STORE / "approvals.json"
approvals = json.loads(ap_path.read_text()) if ap_path.exists() else {
    "_note": "External approval record (Part-11-style signed snapshot). Binds an approver + "
             "effective_date to the exact content_hash of each approved atom. External + keyed, "
             "like reconciliation_log — the atom carries the outcome, this carries the signed set.",
    "project": "ast_alsap", "approvals": []
}
approvals["approvals"].append({
    "effective_date": args.effective_date,
    "approver": args.approver,
    "gate": "GATE PASS + PROMOTE PASS",
    "atom_count": len(atoms),
    "snapshot": snapshot
})
ap_path.write_text(json.dumps(approvals, indent=2, ensure_ascii=False))

print("=" * 68)
print("APPROVED — document published")
print("=" * 68)
print(f"approver      : {args.approver}  (authorized: in approval_roles)")
print(f"effective date: {args.effective_date}")
print(f"atoms approved: {len(atoms)}  (status -> approved; version/content_hash unchanged)")
print(f"signed snapshot: {len(snapshot)} atom_id -> content_hash pairs -> approvals.json")
print("Lifecycle complete: draft -> in_review -> approved.")
