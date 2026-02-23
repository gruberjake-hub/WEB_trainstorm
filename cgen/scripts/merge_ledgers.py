"""
merge_ledgers.py

Merges per-chunk "evidence ledger" outputs into a canonical ledger suitable for
cross-corpus synthesis and systems diagnosis, even when the original corpus exceeds token limits.

Expected inputs:
- A directory containing JSON or JSONL files produced by "Ledger Extraction Mode"
  (one file per chunk).

This script:
- Loads ledger files
- Normalizes and de-duplicates items by (category + normalized_text)
- Aggregates anchors/citations across duplicates
- Writes:
    output/canonical_ledger.json
    output/canonical_ledger.jsonl

Usage:
  python merge_ledgers.py

Config:
  Edit CONFIG section below.
"""

import os
import re
import json
from datetime import datetime
from typing import Any, Dict, List, Tuple

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
OUTPUT_DIR = "output"
LEDGERS_DIR = os.path.join(OUTPUT_DIR, "ledgers")  # put your per-chunk outputs here

OUT_JSON = os.path.join(OUTPUT_DIR, "canonical_ledger.json")
OUT_JSONL = os.path.join(OUTPUT_DIR, "canonical_ledger.jsonl")

# -------------------------------------------------------------------
def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def norm_text(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def load_json_or_jsonl(path: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    if path.lower().endswith(".jsonl"):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                items.append(json.loads(line))
        return items

    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)

    # allow either {"items":[...]} or raw list or a single ledger object
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        if "items" in obj and isinstance(obj["items"], list):
            return obj["items"]
        # if it's a single ledger object with arrays per category, explode it:
        if "ledger" in obj and isinstance(obj["ledger"], dict):
            exploded = []
            for cat, arr in obj["ledger"].items():
                if isinstance(arr, list):
                    for it in arr:
                        if isinstance(it, dict):
                            it = {**it, "category": it.get("category", cat)}
                        else:
                            it = {"text": str(it), "category": cat}
                        exploded.append(it)
            return exploded
        # else treat as one item
        return [obj]
    return items

def merge_items(all_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Dedupe by (category, normalized_text).
    Aggregate anchors into a unique list.
    """
    merged: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for it in all_items:
        cat = it.get("category", "unknown")
        text = it.get("text", "") or it.get("statement", "") or ""
        key = (cat, norm_text(text))
        if key[1] == "":
            continue

        anchors = it.get("anchors", []) or it.get("citations", []) or []
        # Allow single anchor strings
        if isinstance(anchors, str):
            anchors = [anchors]

        if key not in merged:
            merged[key] = {
                "category": cat,
                "text": text.strip(),
                "anchors": [],
                "meta": {},
            }

        # merge anchors
        cur = merged[key]["anchors"]
        for a in anchors:
            if a and a not in cur:
                cur.append(a)

        # merge meta shallowly (keep first non-empty)
        meta = it.get("meta", {}) or {}
        if isinstance(meta, dict):
            for k, v in meta.items():
                if k not in merged[key]["meta"] and v not in (None, "", [], {}):
                    merged[key]["meta"][k] = v

    # stable ordering: by category then text
    out = list(merged.values())
    out.sort(key=lambda x: (x["category"], x["text"].lower()))
    return out

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    led_dir = os.path.join(base, LEDGERS_DIR)

    if not os.path.isdir(led_dir):
        print(f"Ledgers directory not found: {led_dir}")
        print("Create it and drop per-chunk ledger outputs inside.")
        return

    files = [f for f in os.listdir(led_dir) if f.lower().endswith((".json", ".jsonl"))]
    files.sort(key=lambda s: s.lower())
    if not files:
        print("No ledger files found (.json/.jsonl).")
        return

    all_items: List[Dict[str, Any]] = []
    for fn in files:
        path = os.path.join(led_dir, fn)
        try:
            items = load_json_or_jsonl(path)
            # If file is a full ledger object with categories, it may not have "category" per item.
            # If so, infer category from container key is handled in load_json_or_jsonl.
            for it in items:
                if "category" not in it:
                    it["category"] = it.get("category", "unknown")
                all_items.append(it)
        except Exception as e:
            print(f"Failed to load {fn}: {e}")

    merged_items = merge_items(all_items)

    ensure_dir(os.path.join(base, OUTPUT_DIR))

    out_obj = {
        "generated_utc": datetime.utcnow().isoformat() + "Z",
        "ledger_dir": os.path.relpath(led_dir, start=os.path.join(base, OUTPUT_DIR)),
        "source_files": files,
        "item_count_in": len(all_items),
        "item_count_out": len(merged_items),
        "items": merged_items,
    }

    with open(os.path.join(base, OUT_JSON), "w", encoding="utf-8") as f:
        json.dump(out_obj, f, indent=2, ensure_ascii=False)

    with open(os.path.join(base, OUT_JSONL), "w", encoding="utf-8") as f:
        for it in merged_items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    print("Ledger merge complete.")
    print(f"- {OUT_JSON}")
    print(f"- {OUT_JSONL}")

if __name__ == "__main__":
    main()
