#!/usr/bin/env python3
"""
Ingestion pass 2 — mechanical facts + filename inference, kept strictly separate.

TIER 1 (mechanical, zero judgment): hash, dims, format, perceptual dedup.
TIER 2 (inference, proposals only): parse the filename convention.

The critical distinction Tier 2 enforces:
  A client token in a filename can mean TWO different things, and conflating
  them is how you either leak a logo or needlessly imprison a stock photo.

    brand ownership   -> "this IS Brunswick's asset"       -> scope.clients=[brunswick]
    project provenance-> "I USED this in a Brunswick deck" -> scope stays open; the
                                                              client token is history,
                                                              not a restriction

  The category token is what disambiguates. logo/brand => ownership.
  stock/people/background/misc => provenance.

Nothing here writes scope directly. It writes PROPOSALS with confidence,
into a staging file. Promotion to the real registry stays a human act.
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from PIL import Image
import pytesseract
import imagehash

# .jfif is jpeg with a different extension; .svg is vector (PIL can't raster-open it)
RASTER_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".jfif"}
VECTOR_EXTS = {".svg"}
NON_ASSET_EXTS = {".lnk", ".json", ".db", ".ini"}

KNOWN_CLIENTS = {"brunswick", "astellas", "abbvie"}
UNIVERSAL_TOKENS = {"general"}

# category token -> (role proposal, what the client token MEANS for this category)
OWNERSHIP_CATEGORIES = {"logo", "brand", "logos"}
PROVENANCE_CATEGORIES = {
    "stock", "people", "contextual", "background", "misc",
    "abstract", "computer-perspective", "computer-monitor", "dualmonitor",
}
CHROME_CATEGORIES = {"button", "nav", "icon"}


def normalize_tokens(stem: str) -> list[str]:
    stem = re.sub(r"\s*\(\d+\)\s*$", "", stem)           # strip Windows "(3)" dupe suffix
    return [t for t in re.split(r"[_\s]+", stem.lower()) if t]


def parse_filename(path: Path) -> dict:
    tokens = normalize_tokens(path.stem)
    tokset = set(tokens)

    clients_found = sorted(tokset & KNOWN_CLIENTS)
    is_general = bool(tokset & UNIVERSAL_TOKENS)

    is_ownership = bool(tokset & OWNERSHIP_CATEGORIES)
    is_chrome = bool(tokset & CHROME_CATEGORIES)
    is_provenance = bool(tokset & PROVENANCE_CATEGORIES)

    proposal = {
        "tokens": tokens,
        "client_token": clients_found[0] if clients_found else None,
        "role_proposal": None,
        "scope_proposal": None,
        "client_token_means": None,
        "confidence": "low",
        "note": "",
    }

    if is_ownership and clients_found:
        # A logo bearing a client's name IS that client's property.
        proposal.update(
            role_proposal="signature",
            scope_proposal={"industries": [], "clients": clients_found},
            client_token_means="brand_ownership",
            confidence="high",
            note="Client-owned brand asset. Locking scope is correct and required.",
        )
    elif is_ownership and not clients_found:
        proposal.update(
            role_proposal="signature",
            client_token_means="unresolved",
            confidence="low",
            note="Logo-type asset with no recognized client token. Needs eyes — could be "
                 "a third-party mark with its own usage restrictions.",
        )
    elif is_general or (is_chrome and not clients_found):
        proposal.update(
            role_proposal="chrome" if is_chrome else "motif",
            scope_proposal={"industries": [], "clients": []},
            client_token_means="explicitly_general",
            confidence="high",
            note="Named general / no client tie. Universal scope.",
        )
    elif clients_found and is_provenance:
        # THE IMPORTANT CASE. The client token records where it was used,
        # not who owns it. Do NOT auto-lock.
        proposal.update(
            role_proposal="motif",
            scope_proposal={"industries": [], "clients": []},
            client_token_means="project_provenance",
            confidence="medium",
            note=f"Used in the {clients_found[0]} project, but category suggests stock/"
                 f"generic imagery. Scope proposed OPEN. Verify licensing before approving — "
                 f"a stock licence bought for one client may not travel.",
        )
    elif clients_found:
        proposal.update(
            client_token_means="ambiguous",
            confidence="low",
            note=f"Carries '{clients_found[0]}' but category is unclear. Cannot tell "
                 f"ownership from provenance. Needs eyes.",
        )
    else:
        proposal.update(
            client_token_means="none",
            confidence="low",
            note="No client token, no clear category. Needs eyes.",
        )
    return proposal


def ingest_one(path: Path) -> dict:
    raw = path.read_bytes()
    ext = path.suffix.lower()
    rec = {
        "asset_id": "asset_img_" + hashlib.sha256(raw).hexdigest()[:12],
        "original_filename": path.name,
        "file": str(path),
        "media_type": "jpeg" if ext == ".jfif" else ext.lstrip("."),
        "content_hash": "sha256:" + hashlib.sha256(raw).hexdigest(),
        "needs_format_conversion": ext == ".jfif",
        "perceptual_hash": None,
        "likely_duplicate_of": None,
        "metadata": {"native_dimensions_px": None, "aspect_ratio": None},
        "ocr_text": "",
        "inference": parse_filename(path),
        "role": None, "scope": None, "tags": [],
        "governance": {"version": 1, "status": "draft", "owner": None,
                       "approved_by": [], "effective_date": None},
        "review_needed": True,
    }

    if ext in RASTER_EXTS:
        try:
            with Image.open(path) as img:
                w, h = img.size
                rec["metadata"] = {"native_dimensions_px": [w, h],
                                   "aspect_ratio": round(w / h, 3) if h else None}
                rec["perceptual_hash"] = str(imagehash.phash(img))
                try:
                    rec["ocr_text"] = pytesseract.image_to_string(img).strip()
                except Exception:
                    pass
        except Exception as e:
            rec["error"] = f"could not open: {e}"
    return rec


def cluster_duplicates(records: list[dict], max_distance: int = 4) -> None:
    seen: list[tuple] = []
    for rec in records:
        if not rec.get("perceptual_hash"):
            continue
        h = imagehash.hex_to_hash(rec["perceptual_hash"])
        match = next((aid for sh, aid in seen if h - sh <= max_distance), None)
        if match:
            rec["likely_duplicate_of"] = match
        else:
            seen.append((h, rec["asset_id"]))


def main(inbox: str, out_path: str) -> None:
    all_files = sorted(p for p in Path(inbox).rglob("*") if p.is_file())
    assets, skipped = [], []
    for p in all_files:
        ext = p.suffix.lower()
        if ext in RASTER_EXTS or ext in VECTOR_EXTS:
            assets.append(p)
        else:
            skipped.append((p.name, ext))

    records = [ingest_one(p) for p in assets]
    cluster_duplicates(records)

    exact = Counter(r["content_hash"] for r in records)
    exact_dupes = sum(c - 1 for c in exact.values() if c > 1)
    near_dupes = sum(1 for r in records if r["likely_duplicate_of"])

    Path(out_path).write_text(json.dumps({
        "staging_version": "ingest.v0.2",
        "source_inbox": inbox,
        "counts": {
            "files_seen": len(all_files),
            "asset_candidates": len(records),
            "skipped_non_assets": len(skipped),
            "exact_duplicate_files": exact_dupes,
            "near_duplicate_files": near_dupes,
        },
        "skipped": skipped,
        "records": records,
    }, indent=2, ensure_ascii=False))

    print(f"files seen:          {len(all_files)}")
    print(f"asset candidates:    {len(records)}")
    print(f"skipped (non-asset): {len(skipped)}  {[s[0] for s in skipped]}")
    print(f"exact byte-dupes:    {exact_dupes}")
    print(f"near-dupes (phash):  {near_dupes}")
    print(f"-> staging written:  {out_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "inbox",
         sys.argv[2] if len(sys.argv) > 2 else "staging.json")