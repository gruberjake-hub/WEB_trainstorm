"""
canonical_ledger_to_md.py

Converts output/canonical_ledger.json (from merge_ledgers.py) into a clean Markdown
"Ledger Appendix" that is easy to paste into Systems Diagnostic Mode.

Input:
  output/canonical_ledger.json

Outputs:
  output/canonical_ledger.md
  output/canonical_ledger_by_category.md  (optional: grouped view)

Usage:
  python canonical_ledger_to_md.py
"""

import os
import json
from datetime import datetime
from typing import Any, Dict, List

OUTPUT_DIR = "output"
IN_JSON = os.path.join(OUTPUT_DIR, "canonical_ledger.json")
OUT_MD = os.path.join(OUTPUT_DIR, "canonical_ledger.md")
OUT_MD_BY_CAT = os.path.join(OUTPUT_DIR, "canonical_ledger_by_category.md")

# If True, include anchors under each item
INCLUDE_ANCHORS = True

# Max anchors to show per item (keeps MD readable). Set to 0 for all.
MAX_ANCHORS_PER_ITEM = 12


def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clip_anchors(anchors: List[str]) -> List[str]:
    if MAX_ANCHORS_PER_ITEM and len(anchors) > MAX_ANCHORS_PER_ITEM:
        return anchors[:MAX_ANCHORS_PER_ITEM] + [f"...(+{len(anchors)-MAX_ANCHORS_PER_ITEM} more)"]
    return anchors


def write_markdown_flat(obj: Dict[str, Any], path: str) -> None:
    items = obj.get("items", [])
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# CANONICAL EVIDENCE LEDGER\n\n")
        f.write(f"_Generated: {datetime.utcnow().isoformat()} UTC_\n\n")
        f.write("This appendix is a consolidated, de-duplicated set of evidence statements extracted from chunked corpus processing.\n\n")
        f.write("## Ledger Items (Flat)\n\n")

        for i, it in enumerate(items, start=1):
            cat = it.get("category", "unknown")
            text = (it.get("text") or "").strip()
            anchors = it.get("anchors", []) or []
            f.write(f"### {i}. [{cat}] {text}\n\n")
            if INCLUDE_ANCHORS:
                anchors2 = clip_anchors(anchors)
                if anchors2:
                    f.write("**Anchors:**\n\n")
                    for a in anchors2:
                        f.write(f"- {a}\n")
                    f.write("\n")


def write_markdown_by_category(obj: Dict[str, Any], path: str) -> None:
    items = obj.get("items", [])
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for it in items:
        grouped.setdefault(it.get("category", "unknown"), []).append(it)

    cats = sorted(grouped.keys())

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# CANONICAL EVIDENCE LEDGER (GROUPED)\n\n")
        f.write(f"_Generated: {datetime.utcnow().isoformat()} UTC_\n\n")
        f.write("## Categories\n\n")
        for c in cats:
            f.write(f"- {c} ({len(grouped[c])})\n")
        f.write("\n---\n\n")

        for c in cats:
            f.write(f"## {c} ({len(grouped[c])})\n\n")
            for i, it in enumerate(grouped[c], start=1):
                text = (it.get("text") or "").strip()
                anchors = it.get("anchors", []) or []
                f.write(f"### {c}.{i} {text}\n\n")
                if INCLUDE_ANCHORS:
                    anchors2 = clip_anchors(anchors)
                    if anchors2:
                        f.write("**Anchors:**\n\n")
                        for a in anchors2:
                            f.write(f"- {a}\n")
                        f.write("\n")
            f.write("---\n\n")


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    in_path = os.path.join(base, IN_JSON)
    if not os.path.exists(in_path):
        print(f"Input not found: {IN_JSON}")
        print("Run merge_ledgers.py first to create output/canonical_ledger.json.")
        return

    ensure_dir(os.path.join(base, OUTPUT_DIR))
    obj = read_json(in_path)

    write_markdown_flat(obj, os.path.join(base, OUT_MD))
    write_markdown_by_category(obj, os.path.join(base, OUT_MD_BY_CAT))

    print("Ledger Markdown written:")
    print(f"- {OUT_MD}")
    print(f"- {OUT_MD_BY_CAT}")


if __name__ == "__main__":
    main()
