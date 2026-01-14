import os
import json
from datetime import date

# -----------------------------
# CONFIGURE THESE BEFORE RUNNING
# -----------------------------

ASSET_TYPE = "image"              # image | video | audio | animation | document
MEDIA_EXTENSIONS = [".png", ".jpg", ".jpeg", ".svg"]

LIBRARY = "images"

PURPOSE = "General illustrative asset (not yet classified)"

INTENDED_USE = [
    "concept-introduction",
    "reference"
]

LEARNING_ROLES = [
    "explain",
    "orient"
]

TONE = [
    "neutral",
    "professional"
]

STYLE = [
    "diagrammatic",
    "clean"
]

CONSTRAINTS = [
    "no_text_baked_in",
    "safe_for_regulated_audiences"
]

RESTRICTIONS = {
    "allowed_clients": ["*"],
    "allowed_curricula": ["*"],
    "external_use": True
}

CREATED_BY = "Jake"
SOURCE = "custom"
LICENSE = "internal"

# -----------------------------
# SCRIPT LOGIC
# -----------------------------

def generate_manifest(asset_path):
    base, ext = os.path.splitext(asset_path)
    manifest_path = base + ".asset.json"

    if os.path.exists(manifest_path):
        print(f"⏭ Skipping (already exists): {manifest_path}")
        return

    asset_id = os.path.basename(base).replace(" ", "_").lower()
    asset_id = f"{ASSET_TYPE}_{asset_id}"

    manifest = {
        "id": asset_id,
        "type": ASSET_TYPE,
        "media_format": ext.lstrip("."),
        "library": LIBRARY,
        "path": asset_path.replace("\\", "/"),
        "purpose": PURPOSE,
        "intended_use": INTENDED_USE,
        "learning_roles": LEARNING_ROLES,
        "tone": TONE,
        "style": STYLE,
        "constraints": CONSTRAINTS,
        "restrictions": RESTRICTIONS,
        "origin": {
            "created_by": CREATED_BY,
            "source": SOURCE,
            "license": LICENSE,
            "date_created": date.today().isoformat()
        },
        "usage_history": [],
        "pairing_notes": "",
        "related_assets": []
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Created: {manifest_path}")


def run():
    cwd = os.getcwd()
    print(f"📁 Scanning folder: {cwd}")

    for file in os.listdir(cwd):
        _, ext = os.path.splitext(file)
        if ext.lower() in MEDIA_EXTENSIONS:
            generate_manifest(file)


if __name__ == "__main__":
    run()
