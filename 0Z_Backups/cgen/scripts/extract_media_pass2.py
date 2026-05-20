"""
extract_media_pass2.py

PASS 2 — Media Extraction (Comprehensive, Modular)

Goal
- Extract ONLY media information (primarily images) from source files in a repo
- Produce deterministic, auditable manifests for downstream "media-to-structure" inference prompts

This script does NOT attempt to preserve full asset libraries for redeployment.
It focuses on extracting media "nodes" that often encode curriculum/module meaning
(e.g., flowcharts, UI screenshots, diagrams, org charts).

Supported inputs (best-effort)
- .pptx : extracts embedded images and maps them to slides when possible
- .docx : extracts embedded images (word/media/*)
- .pdf  : (optional) renders pages to images if PyMuPDF is available; otherwise emits a warning
- .md/.txt/.xlsx are ignored in this pass

Outputs (per source file)
- output/<stem>_media_manifest.json
- output/media/<stem>/images/*   (extracted images and/or page renders)
- output/media_jobs.jsonl        (optional: one record per media node for batching inference)

Design principles
- Deterministic filenames and IDs
- SHA256 hash for every extracted media file
- Strong provenance: source file, location (Slide/Page), media part name
- Safe fallbacks when a library isn't available

Dependencies (recommended)
- none required for pptx/docx extraction (zip-based)
- PyMuPDF (fitz) for PDF rendering:
    pip install pymupdf

Optional
- If you want true PPTX slide "renders" (screenshots), not just embedded images,
  you'll need an external renderer (e.g., LibreOffice `soffice`), which is NOT included here.
  This script intentionally stays portable and uses embedded media extraction first.

Usage
  python extract_media_pass2.py

Configuration
  Edit CONFIG section below.
"""

import os
import re
import json
import zipfile
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import xml.etree.ElementTree as ET


# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
OUTPUT_DIR_NAME = "output"
INPUT_DIR_NAME = ""  # "" = same folder as script

# Walk subdirectories?
WALK_SUBDIRS = False

# File types to process
INCLUDE_EXTENSIONS = {".pptx", ".docx", ".pdf"}

# Where extracted media goes: output/media/<stem>/images
MEDIA_ROOT_DIRNAME = "media"

# If True, create output/media_jobs.jsonl (one record per media node)
WRITE_JOBS_JSONL = True
JOBS_FILENAME = "media_jobs.jsonl"

# PDF rendering
PDF_RENDER_PAGES = True
PDF_RENDER_DPI = 150  # used only if rendering library supports it

# Safety: skip Office temp files
SKIP_PREFIXES = ("~$",)

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def slugify(text: str) -> str:
    text = text or "source"
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "source"


def iter_input_files(input_dir: str) -> List[str]:
    paths: List[str] = []
    if WALK_SUBDIRS:
        for root, _, files in os.walk(input_dir):
            for fn in files:
                if fn.startswith(SKIP_PREFIXES):
                    continue
                ext = os.path.splitext(fn)[1].lower()
                if ext in INCLUDE_EXTENSIONS:
                    paths.append(os.path.join(root, fn))
    else:
        for fn in os.listdir(input_dir):
            if fn.startswith(SKIP_PREFIXES):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in INCLUDE_EXTENSIONS:
                paths.append(os.path.join(input_dir, fn))

    paths.sort(key=lambda s: s.lower())
    return paths


def write_json(data: Dict[str, Any], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def rel_target_to_media_name(target: str) -> Optional[str]:
    """
    PPTX slide rel targets often look like '../media/image1.png'.
    Return 'image1.png' if it's a media target.
    """
    if not target:
        return None
    target = target.replace("\\", "/")
    if "/media/" in target:
        return target.split("/media/")[-1]
    if target.startswith("../media/"):
        return target.split("../media/")[-1]
    return None


# -------------------------------------------------------------------
# PPTX extraction (zip-based) with slide mapping
# -------------------------------------------------------------------
def extract_pptx_images(src_path: str, out_img_dir: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Extract embedded images from ppt/media and map them to slides when possible.
    Returns: (media_nodes, warnings)
    """
    warnings: List[str] = []
    nodes: List[Dict[str, Any]] = []

    with zipfile.ZipFile(src_path, "r") as z:
        names = z.namelist()

        media_files = [n for n in names if n.startswith("ppt/media/")]
        if not media_files:
            warnings.append("No ppt/media/* images found in PPTX.")
            return nodes, warnings

        # Build mapping: media filename -> [slide numbers]
        media_to_slides: Dict[str, List[int]] = {}

        rel_files = [n for n in names if n.startswith("ppt/slides/_rels/") and n.endswith(".rels")]
        for rf in rel_files:
            # rf: ppt/slides/_rels/slide1.xml.rels
            m = re.search(r"slide(\d+)\.xml\.rels$", rf)
            if not m:
                continue
            slide_num = int(m.group(1))
            try:
                xml = z.read(rf)
                root = ET.fromstring(xml)
            except Exception:
                continue

            # Relationship elements are namespaced; handle generically
            for rel in root.findall(".//{*}Relationship"):
                target = rel.attrib.get("Target", "")
                media_name = rel_target_to_media_name(target)
                if not media_name:
                    continue
                media_to_slides.setdefault(media_name, []).append(slide_num)

        # Extract media files and create nodes
        for mf in sorted(media_files, key=lambda s: s.lower()):
            media_name = os.path.basename(mf)
            raw = z.read(mf)

            # Deterministic filename
            # If mapped to slides, include first slide in name for easier human audit
            slide_list = sorted(set(media_to_slides.get(media_name, [])))
            slide_tag = f"slide_{slide_list[0]:03d}_" if slide_list else "slide_000_"
            out_name = f"{slide_tag}{media_name}"
            out_path = os.path.join(out_img_dir, out_name)

            ensure_dir(out_img_dir)
            with open(out_path, "wb") as f:
                f.write(raw)

            node = {
                "media_id": None,  # filled later
                "source_file": os.path.basename(src_path),
                "source_type": "pptx",
                "location": f"Slide {slide_list[0]}" if slide_list else "Unknown slide",
                "locations_all": [f"Slide {s}" for s in slide_list],
                "ppt_part": mf,
                "output_path": os.path.relpath(out_path, start=os.path.dirname(os.path.dirname(out_img_dir))),
                "filename": out_name,
                "sha256": sha256_file(out_path),
            }
            nodes.append(node)

        return nodes, warnings


# -------------------------------------------------------------------
# DOCX extraction (zip-based)
# -------------------------------------------------------------------
def extract_docx_images(src_path: str, out_img_dir: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    warnings: List[str] = []
    nodes: List[Dict[str, Any]] = []

    with zipfile.ZipFile(src_path, "r") as z:
        names = z.namelist()
        media_files = [n for n in names if n.startswith("word/media/")]
        if not media_files:
            warnings.append("No word/media/* images found in DOCX.")
            return nodes, warnings

        ensure_dir(out_img_dir)
        for idx, mf in enumerate(sorted(media_files, key=lambda s: s.lower()), start=1):
            media_name = os.path.basename(mf)
            raw = z.read(mf)

            # Deterministic filename with ordinal (DOCX doesn't expose easy placement without deep XML traversal)
            out_name = f"img_{idx:03d}_{media_name}"
            out_path = os.path.join(out_img_dir, out_name)

            with open(out_path, "wb") as f:
                f.write(raw)

            node = {
                "media_id": None,  # filled later
                "source_file": os.path.basename(src_path),
                "source_type": "docx",
                "location": f"Image {idx}",
                "locations_all": [f"Image {idx}"],
                "doc_part": mf,
                "output_path": os.path.relpath(out_path, start=os.path.dirname(os.path.dirname(out_img_dir))),
                "filename": out_name,
                "sha256": sha256_file(out_path),
            }
            nodes.append(node)

    return nodes, warnings


# -------------------------------------------------------------------
# PDF extraction (page render) — requires PyMuPDF
# -------------------------------------------------------------------
def extract_pdf_pages(src_path: str, out_img_dir: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    warnings: List[str] = []
    nodes: List[Dict[str, Any]] = []

    if not PDF_RENDER_PAGES:
        warnings.append("PDF_RENDER_PAGES is disabled.")
        return nodes, warnings

    try:
        import fitz  # PyMuPDF
    except Exception:
        warnings.append("PyMuPDF (fitz) not installed; cannot render PDF pages. Install via: pip install pymupdf")
        return nodes, warnings

    ensure_dir(out_img_dir)

    doc = fitz.open(src_path)
    zoom = PDF_RENDER_DPI / 72.0  # 72dpi is PDF default
    mat = fitz.Matrix(zoom, zoom)

    for i in range(doc.page_count):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_name = f"page_{i+1:03d}.png"
        out_path = os.path.join(out_img_dir, out_name)
        pix.save(out_path)

        node = {
            "media_id": None,  # filled later
            "source_file": os.path.basename(src_path),
            "source_type": "pdf",
            "location": f"Page {i+1}",
            "locations_all": [f"Page {i+1}"],
            "pdf_page": i + 1,
            "output_path": os.path.relpath(out_path, start=os.path.dirname(os.path.dirname(out_img_dir))),
            "filename": out_name,
            "sha256": sha256_file(out_path),
        }
        nodes.append(node)

    doc.close()
    return nodes, warnings


# -------------------------------------------------------------------
# Main per-file dispatcher
# -------------------------------------------------------------------
def extract_media_for_file(src_path: str, output_dir: str) -> Dict[str, Any]:
    src_name = os.path.basename(src_path)
    stem = os.path.splitext(src_name)[0]
    stem_slug = slugify(stem)

    media_dir = os.path.join(output_dir, MEDIA_ROOT_DIRNAME, stem_slug, "images")
    ensure_dir(media_dir)

    ext = os.path.splitext(src_path)[1].lower()
    nodes: List[Dict[str, Any]] = []
    warnings: List[str] = []

    if ext == ".pptx":
        nodes, warnings = extract_pptx_images(src_path, media_dir)
    elif ext == ".docx":
        nodes, warnings = extract_docx_images(src_path, media_dir)
    elif ext == ".pdf":
        nodes, warnings = extract_pdf_pages(src_path, media_dir)
    else:
        warnings.append(f"Unsupported extension in pass2: {ext}")

    # Assign deterministic media IDs
    # media_id format: <stem_slug>::<type>::<ordinal>
    for i, n in enumerate(nodes, start=1):
        n["media_id"] = f"{stem_slug}::{n['source_type']}::{i:04d}"

    manifest = {
        "source_file": src_name,
        "source_stem": stem,
        "source_stem_slug": stem_slug,
        "source_type": ext.lstrip("."),
        "generated_utc": datetime.utcnow().isoformat() + "Z",
        "media_dir": os.path.relpath(os.path.join(output_dir, MEDIA_ROOT_DIRNAME, stem_slug), start=output_dir),
        "media_nodes": nodes,
        "warnings": warnings,
    }
    return manifest


def append_jobs(jobs_path: str, manifest: Dict[str, Any]) -> None:
    """
    Writes one JSONL record per media node for easy batching into a vision pipeline.
    """
    with open(jobs_path, "a", encoding="utf-8") as f:
        for node in manifest.get("media_nodes", []):
            record = {
                "media_id": node["media_id"],
                "source_file": node["source_file"],
                "source_type": node["source_type"],
                "location": node.get("location", ""),
                "locations_all": node.get("locations_all", []),
                "sha256": node.get("sha256", ""),
                # Local path for your runner to load and send to a vision model
                "local_path": os.path.join(OUTPUT_DIR_NAME, node["output_path"]),
                # Slot for later inference output
                "inference_output": "",
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base, INPUT_DIR_NAME) if INPUT_DIR_NAME else base
    output_dir = os.path.join(base, OUTPUT_DIR_NAME)
    ensure_dir(output_dir)

    files = iter_input_files(input_dir)
    if not files:
        print("No supported media-bearing files found (.pptx/.docx/.pdf).")
        return

    jobs_path = os.path.join(output_dir, JOBS_FILENAME)
    if WRITE_JOBS_JSONL:
        # reset jobs file each run for determinism
        if os.path.exists(jobs_path):
            os.remove(jobs_path)

    failures: List[Tuple[str, str]] = []

    for src_path in files:
        src_name = os.path.basename(src_path)
        print(f"PASS2: extracting media from {src_name}")
        try:
            manifest = extract_media_for_file(src_path, output_dir)
            stem = os.path.splitext(src_name)[0]
            out_manifest = os.path.join(output_dir, f"{stem}_media_manifest.json")
            write_json(manifest, out_manifest)

            if WRITE_JOBS_JSONL:
                append_jobs(jobs_path, manifest)

            if manifest.get("warnings"):
                for w in manifest["warnings"]:
                    print(f"  ! {w}")
            print(f"  -> wrote {out_manifest}")
        except Exception as e:
            failures.append((src_name, str(e)))

    if failures:
        print("\nCompleted with errors:")
        for fn, err in failures:
            print(f" - {fn}: {err}")
    else:
        print("\nPASS2 complete.")


if __name__ == "__main__":
    main()
