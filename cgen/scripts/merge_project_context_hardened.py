"""
merge_project_context_hardened.py

Merges all *_structured.md files in ./output into a single
LLM-ready project_context.md file.

HARDENING GOALS
- Strong, machine-parseable source envelopes (BEGIN/END markers)
- Corpus-level manifest with deterministic per-source IDs + hashes
- Preserve internal section delimiters without blending adjacent sources
- Deterministic ordering and repeatable formatting (aside from timestamp)
- Safer handling of missing/partial headers
- Optional normalization of whitespace/newlines

USAGE
  python merge_project_context_hardened.py

INPUT
  ./output/*_structured.md

OUTPUT
  ./output/project_context.md
"""

import os
import hashlib
from datetime import datetime
from typing import List, Tuple, Dict

OUTPUT_DIR_NAME = "output"
MERGED_FILENAME = "project_context.md"
STRUCTURED_SUFFIX = "_structured.md"

# Delimiter used inside structured MD files (expected)
TOP_SPLIT_DELIM = "\n---\n"

# Envelope markers (intentionally HTML comments so they won't render loudly)
BEGIN_SRC = "<!-- BEGIN_SOURCE -->"
END_SRC = "<!-- END_SOURCE -->"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_newlines(text: str) -> str:
    # Normalize to \n and strip trailing whitespace on each line
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    # Preserve intentional blank lines but avoid excessive trailing blank lines
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def extract_source_header(md_text: str) -> str:
    """
    Extract the initial source header block from a structured MD file.
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
    Remove the top-level source header so we can re-wrap it
    in the merged document.
    """
    parts = md_text.split(TOP_SPLIT_DELIM, 1)
    if len(parts) == 2:
        return parts[1].strip()
    return md_text.strip()


def load_structured_md_files(output_dir: str) -> List[str]:
    files = [f for f in os.listdir(output_dir) if f.endswith(STRUCTURED_SUFFIX)]
    # Deterministic, case-insensitive sort
    files.sort(key=lambda s: s.lower())
    return files


def stable_source_id(idx: int, fname: str) -> str:
    """
    Deterministic ID that remains stable as long as ordering and filenames remain stable.
    Format: SRC-0001-filename_base
    """
    base = fname.replace(STRUCTURED_SUFFIX, "")
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in base)
    return f"SRC-{idx:04d}-{safe}"


def parse_filename_base(fname: str) -> str:
    return fname.replace(STRUCTURED_SUFFIX, "")


def write_project_context(output_dir: str) -> None:
    structured_files = load_structured_md_files(output_dir)
    if not structured_files:
        print("No *_structured.md files found to merge.")
        return

    merged_path = os.path.join(output_dir, MERGED_FILENAME)

    # Precompute per-source metadata for manifest
    source_meta: List[Dict[str, str]] = []
    for i, fname in enumerate(structured_files, start=1):
        path = os.path.join(output_dir, fname)
        file_hash = sha256_file(path)
        file_size = os.path.getsize(path)
        sid = stable_source_id(i, fname)
        base = parse_filename_base(fname)
        source_meta.append(
            {
                "index": str(i),
                "sid": sid,
                "fname": fname,
                "base": base,
                "sha256": file_hash,
                "bytes": str(file_size),
            }
        )

    with open(merged_path, "w", encoding="utf-8", newline="\n") as out:
        # ------------------------------------------------------------------
        # Corpus header (human + machine friendly)
        # ------------------------------------------------------------------
        out.write("# PROJECT CONTEXT\n\n")
        out.write(
            "_This document is an automatically generated, multi-source context corpus._\n\n"
        )
        out.write(
            "_It is intended for large language model (LLM) ingestion to reconstruct project intent,_\n"
            "_constraints, assumptions, and training-relevant signals._\n\n"
        )
        out.write(f"_Generated: {datetime.utcnow().isoformat()} UTC_\n\n")

        corpus_fingerprint = sha256_text("".join(m["sha256"] for m in source_meta))
        out.write(f"**Corpus Fingerprint (sha256 of source hashes):** `{corpus_fingerprint}`\n\n")
        out.write("---\n\n")

        # ------------------------------------------------------------------
        # Manifest
        # ------------------------------------------------------------------
        out.write("## CORPUS MANIFEST\n\n")
        out.write("The following source files are included in this context corpus:\n\n")
        out.write("| # | Source ID | Source File | Bytes | SHA256 |\n")
        out.write("|---:|---|---|---:|---|\n")
        for m in source_meta:
            out.write(
                f"| {m['index']} | `{m['sid']}` | `{m['base']}` | {m['bytes']} | `{m['sha256']}` |\n"
            )
        out.write("\n---\n\n")

        # ------------------------------------------------------------------
        # Sources (strong envelopes)
        # ------------------------------------------------------------------
        for i, fname in enumerate(structured_files, start=1):
            path = os.path.join(output_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                md_text = normalize_newlines(f.read())

            source_header = extract_source_header(md_text)
            body = strip_top_header(md_text)
            body = normalize_newlines(body).rstrip("\n")

            sid = stable_source_id(i, fname)
            base = parse_filename_base(fname)
            fhash = next(m["sha256"] for m in source_meta if m["fname"] == fname)

            # Source envelope (machine-parseable)
            out.write(f"{BEGIN_SRC}\n")
            out.write(f"<!-- SOURCE_ID: {sid} -->\n")
            out.write(f"<!-- SOURCE_INDEX: {i} -->\n")
            out.write(f"<!-- SOURCE_NAME: {base} -->\n")
            out.write(f"<!-- SOURCE_FILE: {fname} -->\n")
            out.write(f"<!-- SOURCE_SHA256: {fhash} -->\n")
            out.write(f"{END_SRC}\n\n")

            # Human header (kept simple + consistent)
            out.write(f"# {sid}\n\n")
            if source_header.strip():
                out.write(source_header.strip() + "\n\n")
            else:
                out.write(f"_Source header missing in {fname}_\n\n")

            out.write("---\n\n")

            # Body
            out.write(body + "\n\n")

            # Close envelope
            out.write(f"{BEGIN_SRC}\n")
            out.write(f"<!-- SOURCE_ID: {sid} -->\n")
            out.write(f"<!-- SOURCE_INDEX: {i} -->\n")
            out.write(f"<!-- SOURCE_NAME: {base} -->\n")
            out.write(f"<!-- SOURCE_FILE: {fname} -->\n")
            out.write(f"<!-- SOURCE_SHA256: {fhash} -->\n")
            out.write(f"{END_SRC}\n\n")
            out.write("\n---\n\n")

    print(f"Merged context written to: {merged_path}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, OUTPUT_DIR_NAME)

    if not os.path.isdir(output_dir):
        print(f"Output directory not found: {output_dir}")
        return

    write_project_context(output_dir)


if __name__ == "__main__":
    main()
