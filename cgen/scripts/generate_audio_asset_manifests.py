import os
import json
from datetime import date

# -----------------------------
# CONFIGURE THESE BEFORE RUNNING
# -----------------------------

ASSET_TYPE = "audio"
MEDIA_EXTENSIONS = [".mp3", ".wav", ".ogg"]

LIBRARY = "corporate-mood-music"

PURPOSE = "Provide subtle background music to support focus and tone"

INTENDED_USE = [
    "background",
    "*"
]

LEARNING_ROLES = [
    "support",
    "transition"
]

AUDIO_ROLE = "background-music"   # background-music | sting | ambience | ui-sound

ENERGY_LEVEL = "low"               # low | medium | high

INTRUSIVENESS = "low"              # low | medium | high

VO_SAFE = True                     # safe under narration

LOOPABLE = True                    # loops cleanly

TONE = [
    "neutral",
    "professional"
]

STYLE = [
    "ambient",
    "corporate"
]

CONSTRAINTS = [
    "non-distracting",
    "no-vocals",
    "safe_for_regulated_audiences"
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
    asset_id = f"aud_{asset_id}"

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
            "audio_role": AUDIO_ROLE,
            "energy_level": ENERGY_LEVEL,
            "intrusiveness": INTRUSIVENESS,
            "vo_safe": VO_SAFE,
            "loopable": LOOPABLE
        },

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
    print(f"🎵 Scanning audio folder: {cwd}")

    for file in os.listdir(cwd):
        _, ext = os.path.splitext(file)
        if ext.lower() in MEDIA_EXTENSIONS:
            generate_manifest(file)


if __name__ == "__main__":
    run()
