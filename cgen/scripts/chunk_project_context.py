"""
chunk_project_context.py

Splits a merged project_context.md (from merge_project_context_hardened.py) into
LLM-ingestion-safe chunks WITHOUT breaking provenance.

Primary strategy:
- Split by per-source headings: lines starting with "# SRC-...." (SOURCE_ID heading)
Fallback strategy:
- If those headings are not present, split by "<!-- BEGIN_SOURCE -->" markers.

Optional second-stage splitting:
- If a source chunk exceeds MAX_CHARS, split by "## SECTION " boundaries.

Outputs:
- chunks/<SOURCE_ID>.md
- chunks/manifest.json

Usage:
  python chunk_project_context.py

Config:
  Edit CONFIG section below.
"""

import os
import re
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
OUTPUT_DIR = "output"
INPUT_FILENAME = "project_context.md"

CHUNKS_DIRNAME = "chunks"
MANIFEST_FILENAME = "manifest.json"

# If >0, split any single-source chunk into sub-chunks no larger than this many characters
# using SECTION boundaries. Set to 0 to disable.
MAX_CHARS = 180_000  # safe-ish for many LLM contexts; tune per model

# Prefer splitting by SOURCE_ID headings in the hardened merge output
SOURCE_HEADING_RE = re.compile(r"(?m)^#\s+(SRC-\d{4}-[A-Za-z0-9_-]+)\s*$")

# SECTION split marker
SECTION_HEADING_RE = re.compile(r"(?m)^##\s+SECTION\s+\d+\s*:")

# Fallback marker (if your merged file uses comment envelopes)
BEGIN_MARKER = "<!-- BEGIN_SOURCE -->"

# -------------------------------------------------------------------
def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def split_by_source_headings(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Returns: (preamble, [(source_id, source_block), ...])
    """
    matches = list(SOURCE_HEADING_RE.finditer(text))
    if not matches:
        return text, []

    preamble = text[:matches[0].start()].rstrip() + "\n"
    blocks = []
    for i, m in enumerate(matches):
        sid = m.group(1)
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        blocks.append((sid, text[start:end].rstrip() + "\n"))
    return preamble, blocks

def split_by_begin_marker(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Fallback: splits by BEGIN_MARKER occurrences. Uses ordinal IDs if no SRC headers exist.
    """
    parts = text.split(BEGIN_MARKER)
    if len(parts) <= 1:
        return text, []
    preamble = parts[0].rstrip() + "\n"
    blocks = []
    for i, part in enumerate(parts[1:], start=1):
        sid = f"SRC-{i:04d}-unknown"
        block = (BEGIN_MARKER + part).rstrip() + "\n"
        blocks.append((sid, block))
    return preamble, blocks

def split_large_block_by_sections(block: str, max_chars: int) -> List[str]:
    """
    Splits a source block into sub-blocks at SECTION boundaries if too large.
    Keeps the source header intact in each sub-block.
    """
    if max_chars <= 0 or len(block) <= max_chars:
        return [block]

    # Identify where the first SECTION begins; keep everything before as header
    sec_matches = list(SECTION_HEADING_RE.finditer(block))
    if not sec_matches:
        # no sections; brute split
        return [block[i:i+max_chars] for i in range(0, len(block), max_chars)]

    header = block[:sec_matches[0].start()].rstrip() + "\n\n"
    sections = []
    for i, m in enumerate(sec_matches):
        start = m.start()
        end = sec_matches[i+1].start() if i+1 < len(sec_matches) else len(block)
        sections.append(block[start:end].rstrip() + "\n")

    # Accumulate sections into chunks
    chunks = []
    cur = header
    for s in sections:
        if len(cur) + len(s) > max_chars and cur.strip() != header.strip():
            chunks.append(cur.rstrip() + "\n")
            cur = header + s
        else:
            cur += s
    if cur.strip():
        chunks.append(cur.rstrip() + "\n")
    return chunks

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    in_path = os.path.join(base, OUTPUT_DIR, INPUT_FILENAME)
    if not os.path.exists(in_path):
        print(f"Input not found: {in_path}")
        print("Run merge_project_context_hardened.py first.")
        return

    out_dir = os.path.join(base, OUTPUT_DIR, CHUNKS_DIRNAME)
    ensure_dir(out_dir)

    text = read_text(in_path)

    preamble, blocks = split_by_source_headings(text)
    split_mode = "SOURCE_HEADING"
    if not blocks:
        preamble, blocks = split_by_begin_marker(text)
        split_mode = "BEGIN_MARKER" if blocks else "NONE"

    if not blocks:
        print("No source blocks detected. Nothing to chunk.")
        return

    manifest: Dict[str, Any] = {
        "generated_utc": datetime.utcnow().isoformat() + "Z",
        "input_file": os.path.relpath(in_path, start=os.path.join(base, OUTPUT_DIR)),
        "split_mode": split_mode,
        "max_chars": MAX_CHARS,
        "sources": [],
    }

    for sid, block in blocks:
        sub_blocks = split_large_block_by_sections(block, MAX_CHARS)
        if len(sub_blocks) == 1:
            fname = f"{sid}.md"
            out_path = os.path.join(out_dir, fname)
            write_text(out_path, preamble + "\n---\n\n" + sub_blocks[0])
            manifest["sources"].append({
                "source_id": sid,
                "chunk_files": [fname],
                "char_counts": [len(sub_blocks[0])],
            })
        else:
            chunk_files = []
            char_counts = []
            for i, sb in enumerate(sub_blocks, start=1):
                fname = f"{sid}__part_{i:02d}.md"
                out_path = os.path.join(out_dir, fname)
                write_text(out_path, preamble + "\n---\n\n" + sb)
                chunk_files.append(fname)
                char_counts.append(len(sb))
            manifest["sources"].append({
                "source_id": sid,
                "chunk_files": chunk_files,
                "char_counts": char_counts,
            })

    man_path = os.path.join(out_dir, MANIFEST_FILENAME)
    with open(man_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Chunking complete: {len(manifest['sources'])} sources")
    print(f"- Chunks dir: {out_dir}")
    print(f"- Manifest: {man_path}")

if __name__ == "__main__":
    main()
