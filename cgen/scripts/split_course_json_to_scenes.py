#!/usr/bin/env python3
"""
split_course_json_to_scenes.py

Purpose:
    Split a Trainstorm course.json file into individual scene-level JSON files
    that can be imported into After Effects as footage and referenced via:

        footage("sce_001_content.json").sourceData

Expected input shape:
    {
      "module_id": "...",
      "title": "...",
      "scenes": [
        {
          "scene_id": "sce_001",
          "title": "...",
          "elements": {
            "Head_01": {
              "type": "Head",
              "text": "..."
            }
          },
          "narration": {...},
          "assets": {...},
          "render": {...}
        }
      ]
    }

Output:
    /scene_json/sce_001_content.json
    /scene_json/sce_002_content.json
    ...

Usage:
    python split_course_json_to_scenes.py course.json

Optional:
    python split_course_json_to_scenes.py course.json --out scene_json
"""

import argparse
import json
import re
import sys
from pathlib import Path


SCENE_ID_PATTERN = re.compile(r"^sce_\d{3}$")


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"ERROR: File not found: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: Invalid JSON in {path}: {e}")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def normalize_scene_id(scene_id: str) -> str:
    scene_id = str(scene_id).strip().lower()

    # Allow "scene_001" and normalize to "sce_001"
    if scene_id.startswith("scene_"):
        scene_id = "sce_" + scene_id.split("scene_", 1)[1]

    return scene_id


def validate_scene(scene: dict, index: int) -> str:
    if not isinstance(scene, dict):
        raise SystemExit(f"ERROR: Scene at index {index} is not an object.")

    if "scene_id" not in scene:
        raise SystemExit(f"ERROR: Scene at index {index} is missing 'scene_id'.")

    scene_id = normalize_scene_id(scene["scene_id"])

    if not SCENE_ID_PATTERN.match(scene_id):
        raise SystemExit(
            f"ERROR: Invalid scene_id '{scene.get('scene_id')}' at index {index}. "
            "Expected format like 'sce_001'."
        )

    if "elements" not in scene:
        raise SystemExit(f"ERROR: Scene '{scene_id}' is missing 'elements'.")

    if not isinstance(scene["elements"], dict):
        raise SystemExit(f"ERROR: Scene '{scene_id}' has non-object 'elements'.")

    return scene_id


def make_scene_feed(course: dict, scene: dict, scene_id: str, include_module_meta: bool) -> dict:
    """
    Return the exact scene-level structure AE will consume.
    Keeps the elements nested under data.elements[targetId].text.
    """
    scene_feed = dict(scene)
    scene_feed["scene_id"] = scene_id

    if include_module_meta:
        scene_feed["_module"] = {
            "module_id": course.get("module_id") or course.get("id"),
            "title": course.get("title"),
            "audience": course.get("audience"),
            "duration_estimate_min": course.get("duration_estimate_min")
        }

    return scene_feed


def split_course(course_path: Path, out_dir: Path, include_module_meta: bool, overwrite: bool) -> list[Path]:
    course = load_json(course_path)

    scenes = course.get("scenes")
    if scenes is None and "module" in course and isinstance(course["module"], dict):
        scenes = course["module"].get("scenes")

    if not isinstance(scenes, list):
        raise SystemExit("ERROR: Could not find a scenes[] array in course JSON.")

    written_files = []

    for index, scene in enumerate(scenes):
        scene_id = validate_scene(scene, index)
        out_path = out_dir / f"{scene_id}_content.json"

        if out_path.exists() and not overwrite:
            raise SystemExit(
                f"ERROR: Output file already exists: {out_path}\n"
                "Use --overwrite to replace existing files."
            )

        scene_feed = make_scene_feed(course, scene, scene_id, include_module_meta)
        write_json(out_path, scene_feed)
        written_files.append(out_path)

    return written_files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Split Trainstorm course.json into scene-level JSON files for AE."
    )
    parser.add_argument(
        "course_json",
        help="Path to the course.json file."
    )
    parser.add_argument(
        "--out",
        default="scene_json",
        help="Output folder for scene JSON files. Default: scene_json"
    )
    parser.add_argument(
        "--include-module-meta",
        action="store_true",
        help="Include lightweight module metadata in each scene JSON under _module."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing scene JSON files."
    )

    args = parser.parse_args()

    course_path = Path(args.course_json).resolve()
    out_dir = Path(args.out).resolve()

    written_files = split_course(
        course_path=course_path,
        out_dir=out_dir,
        include_module_meta=args.include_module_meta,
        overwrite=args.overwrite
    )

    print(f"Split complete. Wrote {len(written_files)} scene file(s):")
    for path in written_files:
        print(f"  {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
