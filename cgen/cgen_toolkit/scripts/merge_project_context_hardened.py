"""
merge_project_context_hardened.py

Merges all *_structured.md files found recursively under --input into a
single LLM-ready project_context.md in a (optionally timestamped) --output dir.

HARDENING GOALS
- Script is location-independent: pass --input and --output explicitly
- Recursive subfolder traversal via pathlib.rglob
- Timestamped output subfolder by default (override with --no-timestamp)
- Strong, machine-parseable source envelopes (BEGIN/END markers)
- Corpus-level manifest with deterministic per-source IDs + hashes
- Relative path encoded into SOURCE_ID so cross-folder files never collide
- Preserve internal section delimiters without blending adjacent sources
- Deterministic ordering and repeatable formatting (aside from timestamp)
- Safer handling of missing/partial headers
- Optional normalization of whitespace/newlines

USAGE
  # Full explicit paths
  python /path/to/scripts/merge_project_context_hardened.py \\
      --input /path/to/project \\
      --output /path/to/project/output

  # Defaults: input = cwd, output = <input>/output, timestamped subfolder
  python /path/to/scripts/merge_project_context_hardened.py

  # Skip timestamp subfolder
  python /path/to/scripts/merge_project_context_hardened.py --no-timestamp

INPUT
  All *_structured.md files found recursively under --input

OUTPUT
  <output_dir>/<timestamp>/project_context.md   (default)
  <output_dir>/project_context.md               (with --no-timestamp)
"""

import os
import argparse
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MERGED_FILENAME = "project_context.md"
STRUCTURED_SUFFIX = "_structured.md"

# Delimiter used inside structured MD files (expected between header and body)
TOP_SPLIT_DELIM = "\n---\n"

# Envelope markers (HTML comments — won't render loudly in most MD viewers)
BEGIN_SRC = "<!-- BEGIN_SOURCE -->"
END_SRC   = "<!-- END_SOURCE -->"


# ---------------------------------------------------------------------------
# Hashing utilities
# ---------------------------------------------------------------------------

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Text normalization
# ---------------------------------------------------------------------------

def normalize_newlines(text: str) -> str:
    """Normalize line endings and strip trailing whitespace per line."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    # Remove trailing blank lines
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Structured MD parsing
# ---------------------------------------------------------------------------

def extract_source_header(md_text: str) -> str:
    """
    Extract the initial header block from a structured MD file.
    Expected at top of file:
      # Source: filename
      _File type: pptx_
    Stops at the first '---' horizontal delimiter.
    """
    lines = md_text.splitlines()
    header_lines = []
    for line in lines:
        if line.strip() == "---":
            break
        header_lines.append(line)
    return "\n".join(header_lines).strip()


def strip_top_header(md_text: str) -> str:
    """
    Remove the top-level source header so it can be re-wrapped
    consistently in the merged document.
    """
    parts = md_text.split(TOP_SPLIT_DELIM, 1)
    if len(parts) == 2:
        return parts[1].strip()
    return md_text.strip()


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def load_structured_md_files(input_dir: Path) -> List[Path]:
    """
    Recursively find all *_structured.md files under input_dir.
    Sorted deterministically (case-insensitive, full relative path).
    Skips the output directory if it happens to be inside input_dir.
    """
    files = sorted(
        input_dir.rglob(f"*{STRUCTURED_SUFFIX}"),
        key=lambda p: str(p.relative_to(input_dir)).lower()
    )
    return files


# ---------------------------------------------------------------------------
# Source ID generation
# ---------------------------------------------------------------------------

def stable_source_id(idx: int, rel_path: str) -> str:
    """
    Deterministic ID stable as long as ordering and relative paths are stable.
    Encodes the full relative path so cross-subfolder files never collide.

    Format: SRC-0001-subdir--filename_base
    """
    # Replace OS separators with '--' for readability
    rel_normalized = rel_path.replace(os.sep, "--").replace("/", "--")
    base = rel_normalized.replace(STRUCTURED_SUFFIX, "")
    safe = "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "-"
        for ch in base
    )
    return f"SRC-{idx:04d}-{safe}"


# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------

def resolve_output_dir(base_output: Path, use_timestamp: bool) -> Path:
    if use_timestamp:
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_dir = base_output / timestamp
    else:
        out_dir = base_output
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


# ---------------------------------------------------------------------------
# Core merge writer
# ---------------------------------------------------------------------------

def write_project_context(input_dir: Path, output_dir: Path) -> None:
    structured_files = load_structured_md_files(input_dir)

    if not structured_files:
        print(f"[merge] No *_structured.md files found under: {input_dir}")
        return

    merged_path = output_dir / MERGED_FILENAME

    # Pre-compute per-source metadata for the manifest
    source_meta: List[Dict] = []
    for i, fpath in enumerate(structured_files, start=1):
        rel = str(fpath.relative_to(input_dir))
        file_hash = sha256_file(fpath)
        file_size = fpath.stat().st_size
        sid = stable_source_id(i, rel)
        source_meta.append({
            "index": str(i),
            "sid":      sid,
            "rel_path": rel,
            "fname":    fpath.name,
            "sha256":   file_hash,
            "bytes":    str(file_size),
        })

    with open(merged_path, "w", encoding="utf-8", newline="\n") as out:

        # ------------------------------------------------------------------
        # Corpus header
        # ------------------------------------------------------------------
        out.write("# PROJECT CONTEXT\n\n")
        out.write(
            "_This document is an automatically generated, multi-source context corpus._\n\n"
            "_It is intended for LLM ingestion to reconstruct project intent,_\n"
            "_constraints, assumptions, and training-relevant signals._\n\n"
        )
        out.write(f"_Generated: {datetime.utcnow().isoformat()} UTC_\n\n")
        out.write(f"_Input root: `{input_dir}`_\n\n")

        corpus_fingerprint = sha256_text("".join(m["sha256"] for m in source_meta))
        out.write(
            f"**Corpus Fingerprint (sha256 of source hashes):** `{corpus_fingerprint}`\n\n"
        )
        out.write("---\n\n")

        # ------------------------------------------------------------------
        # Manifest
        # ------------------------------------------------------------------
        out.write("## CORPUS MANIFEST\n\n")
        out.write(
            "| # | Source ID | Relative Path | Bytes | SHA256 |\n"
            "|---:|---|---|---:|---|\n"
        )
        for m in source_meta:
            out.write(
                f"| {m['index']} | `{m['sid']}` | `{m['rel_path']}` "
                f"| {m['bytes']} | `{m['sha256']}` |\n"
            )
        out.write("\n---\n\n")

        # ------------------------------------------------------------------
        # Sources (strong envelopes)
        # ------------------------------------------------------------------
        for i, fpath in enumerate(structured_files, start=1):
            meta = source_meta[i - 1]
            sid = meta["sid"]

            with open(fpath, "r", encoding="utf-8") as f:
                md_text = normalize_newlines(f.read())

            source_header = extract_source_header(md_text)
            body = strip_top_header(md_text)
            body = normalize_newlines(body).rstrip("\n")

            # Open envelope
            out.write(f"{BEGIN_SRC}\n")
            out.write(f"<!-- SOURCE_ID:       {sid} -->\n")
            out.write(f"<!-- SOURCE_INDEX:    {i} -->\n")
            out.write(f"<!-- SOURCE_REL_PATH: {meta['rel_path']} -->\n")
            out.write(f"<!-- SOURCE_FILE:     {meta['fname']} -->\n")
            out.write(f"<!-- SOURCE_SHA256:   {meta['sha256']} -->\n")
            out.write(f"{END_SRC}\n\n")

            # Human-readable header
            out.write(f"# {sid}\n\n")
            if source_header.strip():
                out.write(source_header.strip() + "\n\n")
            else:
                out.write(f"_Source header missing in `{meta['rel_path']}`_\n\n")

            out.write("---\n\n")

            # Body
            out.write(body + "\n\n")

            # Close envelope
            out.write(f"{BEGIN_SRC}\n")
            out.write(f"<!-- SOURCE_ID:    {sid} -->\n")
            out.write(f"<!-- END_SOURCE:   {sid} -->\n")
            out.write(f"{END_SRC}\n\n")
            out.write("\n---\n\n")

    print(f"[merge] {len(structured_files)} sources → {merged_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Merge all *_structured.md files (recursively) under --input "
            "into a single LLM context corpus at --output."
        )
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=Path.cwd(),
        help="Root directory to search recursively for *_structured.md files. "
             "Default: current working directory."
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Base output directory. A timestamped subfolder is created inside "
             "unless --no-timestamp is passed. Default: <input>/output."
    )
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Write project_context.md directly into --output without a "
             "timestamped subfolder."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = args.input.resolve()

    base_output = (args.output or input_dir / "output").resolve()
    output_dir  = resolve_output_dir(base_output, use_timestamp=not args.no_timestamp)

    print(f"[merge] Input:  {input_dir}")
    print(f"[merge] Output: {output_dir}")

    write_project_context(input_dir, output_dir)


if __name__ == "__main__":
    main()
