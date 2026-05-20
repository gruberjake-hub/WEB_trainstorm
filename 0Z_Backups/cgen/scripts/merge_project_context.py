"""
merge_project_context.py

Merges all *_structured.md files in ./output into a single
LLM-ready project_context.md file.

Design goals:
- Preserve source provenance
- Preserve internal section delimiters
- Add a clear corpus-level manifest
- Be deterministic and repeatable
"""

import os
import re
from datetime import datetime

OUTPUT_DIR_NAME = "output"
MERGED_FILENAME = "project_context.md"


def extract_source_header(md_text: str) -> str:
    """
    Extract the initial source header block from a structured MD file.
    Expected at top of file:
      # Source: filename
      _File type: pptx_
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
    parts = md_text.split("\n---\n", 1)
    if len(parts) == 2:
        return parts[1].strip()
    return md_text.strip()


def load_structured_md_files(output_dir: str):
    files = [
        f
        for f in os.listdir(output_dir)
        if f.endswith("_structured.md")
    ]
    files.sort(key=str.lower)
    return files


def write_project_context(output_dir: str) -> None:
    structured_files = load_structured_md_files(output_dir)
    if not structured_files:
        print("No *_structured.md files found to merge.")
        return

    merged_path = os.path.join(output_dir, MERGED_FILENAME)

    with open(merged_path, "w", encoding="utf-8") as out:
        # ------------------------------------------------------------------
        # Corpus header
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
        out.write("---\n\n")

        # ------------------------------------------------------------------
        # Manifest
        # ------------------------------------------------------------------
        out.write("## CORPUS MANIFEST\n\n")
        out.write("The following source files are included in this context corpus:\n\n")

        for fname in structured_files:
            out.write(f"- {fname.replace('_structured.md', '')}\n")

        out.write("\n---\n\n")

        # ------------------------------------------------------------------
        # Sources
        # ------------------------------------------------------------------
        for idx, fname in enumerate(structured_files, start=1):
            path = os.path.join(output_dir, fname)

            with open(path, "r", encoding="utf-8") as f:
                md_text = f.read()

            source_header = extract_source_header(md_text)
            body = strip_top_header(md_text)

            # Source wrapper
            out.write(f"# SOURCE {idx}\n\n")
            out.write(source_header + "\n\n")
            out.write("---\n\n")
            out.write(body + "\n\n")
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
