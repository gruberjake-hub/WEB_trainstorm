#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from jsonschema import Draft7Validator, RefResolver


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python scripts/validate_course_json.py path/to/course.json path/to/course.schema.json")
        sys.exit(1)

    course_path = Path(sys.argv[1]).resolve()
    schema_path = Path(sys.argv[2]).resolve()
    schema_dir = schema_path.parent

    course = load_json(course_path)
    schema = load_json(schema_path)

    resolver = RefResolver(
        base_uri=schema_dir.as_uri() + "/",
        referrer=schema
    )

    validator = Draft7Validator(schema, resolver=resolver)
    errors = sorted(validator.iter_errors(course), key=lambda e: e.path)

    if not errors:
        print(f"VALID: {course_path}")
        sys.exit(0)

    print(f"INVALID: {course_path}")
    print()

    for error in errors:
        path = ".".join(str(p) for p in error.absolute_path)
        if not path:
            path = "<root>"
        print(f"- {path}: {error.message}")

    sys.exit(1)


if __name__ == "__main__":
    main()