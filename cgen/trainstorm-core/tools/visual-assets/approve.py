#!/usr/bin/env python3
"""
Record a human approval against registry entries.

Approval is a governance ACT, not a derived field — so it gets its own script,
its own record, and its own audit line. Run against the canonical registry;
promote.py preserves whatever this writes on any future regeneration.

Usage:
    python3 approve.py                 # approve everything currently draft
    python3 approve.py --dry-run       # show what would change
"""
import json
import sys
from datetime import date
from pathlib import Path

REGISTRY = "visual-assets.registry.json"
APPROVER = "jake"


def main(dry_run: bool = False) -> None:
    reg = json.loads(Path(REGISTRY).read_text())
    changed = []

    for a in reg["assets"]:
        g = a["governance"]
        if g["status"] == "draft":
            changed.append(a["asset_id"])
            if not dry_run:
                g["status"] = "approved"
                g["approved_by"] = [APPROVER]
                g["effective_date"] = date.today().isoformat()

    if not dry_run:
        reg["status"] = "approved"
        reg["_approval_record"] = {
            "approved_by": APPROVER,
            "date": date.today().isoformat(),
            "entries_newly_approved": len(changed),
            "entries_approved_total": sum(1 for a in reg["assets"] if a["governance"]["status"] == "approved"),
            "note": ("Blanket sign-off of the 2026-07-23 ingest. Two regulatory marks "
                     "(icon_health-authority_logo 3 and 4) remain UNIDENTIFIED by agency — "
                     "their provenance says confirm-before-use, and that still stands: "
                     "approval here clears them to be selected, not to be used unchecked."),
        }
        Path(REGISTRY).write_text(json.dumps(reg, indent=2, ensure_ascii=False))

    print(f"{'would approve' if dry_run else 'approved'}: {len(changed)} entries")
    still_draft = sum(1 for a in reg["assets"] if a["governance"]["status"] == "draft")
    print(f"still draft: {still_draft}")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
