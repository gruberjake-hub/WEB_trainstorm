import os
import json
from datetime import date

# -----------------------------
# CONFIGURE THESE BEFORE RUNNING
# -----------------------------

ASSET_TYPE = "audio"
MEDIA_EXTENSIONS = [".wav", ".mp3", ".ogg"]

LIBRARY = "ui-sound-effects"

PURPOSE = "Provide short, non-intrusive sound effects for UI feedback and transitions"

INTENDED_USE = ["*"]        # classify later if heterogeneous
LEARNING_ROLES = ["reinforce", "orient"]

SFX_ROLE = "*"              # confirmation | error | transition | attention | success
FEEDBACK_VALENCE = "*"      # positive | neutral | negative
INTENSITY = "*"             # low | medium | high
DURATION_MS = "*"           # fill later if needed

FREQUENCY_SAFE = True       # safe to hear repeatedly
ACCESSIBILITY_SAFE = True   # not startling or shrill

CONSTRAINTS = [
    "non-startling",
    "no-musical-melody",
    "safe-for-professional-use"
]

RESTRICTIONS = {
    "allowed_clients": ["*"],
    "allowed_curricula": ["*"],
    "external_use": True
}

CREATED_BY = "Jake"
SOURCE = "stock"
LICENSE = "royalty-free"

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
    asset_id = f"sfx_{asset_id}"

    manifest = {
        "id": asset_id,
        "type": ASSET_TYPE,
        "media_format": ext.lstrip("."),
        "library": LIBRARY,
        "path": asset_path.replace("\\", "/"),

        "purpose": PURPOSE,
        "intended_use": INTENDED_USE,
        "learning_roles": LEARNING_ROLES,

        "audio": {
            "sfx_role": SFX_ROLE,
            "feedback_valence": FEEDBACK_VALENCE,
            "intensity": INTENSITY,
            "duration_ms": DURATION_MS,
            "frequency_safe": FREQUENCY_SAFE,
            "accessibility_safe": ACCESSIBILITY_SAFE
        },

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
    print(f"🔊 Scanning SFX folder: {cwd}")

    for file in os.listdir(cwd):
        _, ext = os.path.splitext(file)
        if ext.lower() in MEDIA_EXTENSIONS:
            generate_manifest(file)


if __name__ == "__main__":
    run()
