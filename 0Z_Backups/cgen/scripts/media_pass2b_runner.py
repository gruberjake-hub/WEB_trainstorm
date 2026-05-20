"""
media_pass2b_runner.py

PASS 2B — Media-to-Structure Runner (Mode B)

Purpose
- Reads output/media_jobs.jsonl produced by extract_media_pass2.py
- For each media node, runs a "vision inference" step to produce structured signals
  aligned to MEDIA_STRUCTURAL_EXTRACTION_MODE_B.md (strict JSON output)
- Writes:
  - output/media_signals.jsonl  (one JSON per media item)
  - output/<source_stem>_media_signals.json (grouped by source file)
  - updates output/media_jobs_with_signals.jsonl (jobs + attached signal json)

Important
- This script is PROVIDER-AGNOSTIC by default. It includes a stubbed VisionClient.
- Plug in your preferred vision model/provider by implementing VisionClient.generate().
- The runner enforces schema presence (keys) and will flag malformed outputs.

How to use
1) Run PASS 2: python extract_media_pass2.py
2) Configure your VisionClient implementation (see section below).
3) Run PASS 2B: python media_pass2b_runner.py

Config
- See CONFIG section for paths and toggles.
"""

import os
import json
import time
import hashlib
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path


# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
OUTPUT_DIR = "output"
JOBS_JSONL = os.path.join(OUTPUT_DIR, "media_jobs.jsonl")

# Outputs
SIGNALS_JSONL = os.path.join(OUTPUT_DIR, "media_signals.jsonl")
JOBS_WITH_SIGNALS_JSONL = os.path.join(OUTPUT_DIR, "media_jobs_with_signals.jsonl")

# Grouped per-source outputs go to OUTPUT_DIR/<source_stem>_media_signals.json
WRITE_GROUPED_PER_SOURCE = True

# Rate limiting / retries
SLEEP_BETWEEN_REQUESTS_SEC = 0.25
MAX_RETRIES = 2

# If True, skip items that already exist in media_signals.jsonl by media_id
RESUME_MODE = True


# -------------------------------------------------------------------
# REQUIRED SCHEMA KEYS (Mode B)
# -------------------------------------------------------------------
REQUIRED_TOP_KEYS = ["source", "media", "extracted"]
REQUIRED_SOURCE_KEYS = ["source_id", "source_name", "location"]
REQUIRED_MEDIA_KEYS = ["media_type", "short_structural_summary", "confidence"]
REQUIRED_EXTRACTED_KEYS = ["visible_text", "entities", "process", "decision_logic", "ui_workflow", "signals", "ambiguities"]


# -------------------------------------------------------------------
# Utility helpers
# -------------------------------------------------------------------
def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def append_jsonl(path: str, obj: Dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def index_existing_media_ids(signals_jsonl_path: str) -> set:
    existing = set()
    if not os.path.exists(signals_jsonl_path):
        return existing
    with open(signals_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                mid = obj.get("source", {}).get("media_id") or obj.get("media_id")
                if mid:
                    existing.add(mid)
            except Exception:
                continue
    return existing


def validate_schema(signal: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []

    for k in REQUIRED_TOP_KEYS:
        if k not in signal:
            errors.append(f"Missing top key: {k}")

    src = signal.get("source", {})
    for k in REQUIRED_SOURCE_KEYS:
        if k not in src:
            errors.append(f"Missing source.{k}")

    med = signal.get("media", {})
    for k in REQUIRED_MEDIA_KEYS:
        if k not in med:
            errors.append(f"Missing media.{k}")

    ext = signal.get("extracted", {})
    for k in REQUIRED_EXTRACTED_KEYS:
        if k not in ext:
            errors.append(f"Missing extracted.{k}")

    # enforce deterministic key presence for nested structures (light checks)
    conf = med.get("confidence", {})
    if not isinstance(conf, dict) or "overall" not in conf:
        errors.append("Missing media.confidence.overall")

    return (len(errors) == 0), errors


# -------------------------------------------------------------------
# VisionClient (provider-agnostic stub)
# -------------------------------------------------------------------
@dataclass
class VisionRequest:
    media_id: str
    source_file: str
    source_type: str
    location: str
    local_path: str
    sha256: str
    prompt_text: str


class VisionClient:
    """
    Implement this class for your chosen provider.

    Expected behavior:
      - Accept VisionRequest with a local image path
      - Return a dict that matches the Mode B JSON schema
    """
    def generate(self, req: VisionRequest) -> Dict[str, Any]:
        raise NotImplementedError("Implement VisionClient.generate() for your provider.")


class StubVisionClient(VisionClient):
    """
    Safe default: produces an 'unknown' structured signal without any inference.
    Replace with a real provider client when ready.
    """
    def generate(self, req: VisionRequest) -> Dict[str, Any]:
        return {
            "source": {
                "media_id": req.media_id,
                "source_id": "",  # optionally map to your corpus SOURCE_ID later
                "source_name": req.source_file,
                "location": req.location,
            },
            "media": {
                "media_type": "unknown",
                "short_structural_summary": "No inference executed (stub client).",
                "confidence": {"overall": 0.0, "notes": "Stub client output."},
            },
            "extracted": {
                "visible_text": [],
                "entities": {
                    "roles": [],
                    "systems": [],
                    "artifacts": [],
                    "policies_or_guardrails": [],
                },
                "process": {"steps": [], "handoffs": []},
                "decision_logic": {"decision_points": []},
                "ui_workflow": {
                    "screen_or_page": "",
                    "fields": [],
                    "actions": [],
                    "validation_or_errors": [],
                },
                "signals": {
                    "contains_sequence": False,
                    "contains_branching": False,
                    "contains_escalation": False,
                    "contains_role_handoffs": False,
                    "contains_compliance_rules": False,
                },
                "ambiguities": [
                    {
                        "issue": "Inference not executed (stub).",
                        "possible_interpretations": [],
                        "recommended_disambiguation_question": "Run with a real VisionClient provider implementation.",
                    }
                ],
            },
        }


# -------------------------------------------------------------------
# Prompt loading
# -------------------------------------------------------------------
def load_mode_b_prompt(base_dir: str) -> str:
    """
    Looks for MEDIA_STRUCTURAL_EXTRACTION_MODE_B.md in base_dir, otherwise uses a minimal embedded prompt.
    """
    candidate = os.path.join(base_dir, "MEDIA_STRUCTURAL_EXTRACTION_MODE_B.md")
    if os.path.exists(candidate):
        with open(candidate, "r", encoding="utf-8") as f:
            return f.read().strip()

    # Minimal fallback (should be replaced by your canonical prompt file)
    return (
        "You are operating in Media Structural Extraction Mode (Mode B). "
        "Return strict JSON per the defined schema."
    )


# -------------------------------------------------------------------
# Grouping by source
# -------------------------------------------------------------------
def group_by_source(signals: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for s in signals:
        src_name = s.get("source", {}).get("source_name", "unknown_source")
        grouped.setdefault(src_name, []).append(s)
    return grouped


# -------------------------------------------------------------------
# Main runner
# -------------------------------------------------------------------
def main():
    base = os.path.dirname(os.path.abspath(__file__))
    ensure_dir(os.path.join(base, OUTPUT_DIR))

    if not os.path.exists(os.path.join(base, JOBS_JSONL)):
        print(f"Jobs file not found: {JOBS_JSONL}")
        print("Run PASS 2 first: python extract_media_pass2.py")
        return

    prompt_text = load_mode_b_prompt(base)

    jobs = read_jsonl(os.path.join(base, JOBS_JSONL))
    if not jobs:
        print("No jobs found in media_jobs.jsonl")
        return

    existing = index_existing_media_ids(os.path.join(base, SIGNALS_JSONL)) if RESUME_MODE else set()

    # Choose your provider here:
    client: VisionClient = StubVisionClient()  # <-- replace with your implementation

    # Reset outputs for determinism if not resuming
    if not RESUME_MODE:
        for p in [SIGNALS_JSONL, JOBS_WITH_SIGNALS_JSONL]:
            fp = os.path.join(base, p)
            if os.path.exists(fp):
                os.remove(fp)

    collected_signals: List[Dict[str, Any]] = []

    for j in jobs:
        media_id = j.get("media_id", "")
        if not media_id:
            continue
        if RESUME_MODE and media_id in existing:
            continue

        local_path = j.get("local_path", "")
        abs_path = os.path.join(base, local_path) if local_path else ""
        if not abs_path or not os.path.exists(abs_path):
            # write an error signal
            signal = {
                "source": {
                    "media_id": media_id,
                    "source_id": "",
                    "source_name": j.get("source_file", ""),
                    "location": j.get("location", ""),
                },
                "media": {
                    "media_type": "unknown",
                    "short_structural_summary": "Missing local image file; cannot infer.",
                    "confidence": {"overall": 0.0, "notes": "File not found."},
                },
                "extracted": {
                    "visible_text": [],
                    "entities": {"roles": [], "systems": [], "artifacts": [], "policies_or_guardrails": []},
                    "process": {"steps": [], "handoffs": []},
                    "decision_logic": {"decision_points": []},
                    "ui_workflow": {"screen_or_page": "", "fields": [], "actions": [], "validation_or_errors": []},
                    "signals": {
                        "contains_sequence": False,
                        "contains_branching": False,
                        "contains_escalation": False,
                        "contains_role_handoffs": False,
                        "contains_compliance_rules": False,
                    },
                    "ambiguities": [
                        {
                            "issue": "Local image file missing.",
                            "possible_interpretations": [],
                            "recommended_disambiguation_question": "Verify Pass 2 extraction output paths.",
                        }
                    ],
                },
            }
            append_jsonl(os.path.join(base, SIGNALS_JSONL), signal)
            append_jsonl(os.path.join(base, JOBS_WITH_SIGNALS_JSONL), {**j, "inference_output": signal})
            collected_signals.append(signal)
            continue

        req = VisionRequest(
            media_id=media_id,
            source_file=j.get("source_file", ""),
            source_type=j.get("source_type", ""),
            location=j.get("location", ""),
            local_path=abs_path,
            sha256=j.get("sha256", ""),
            prompt_text=prompt_text,
        )

        last_err = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                signal = client.generate(req)

                # Attach required provenance fields if provider didn't include them
                signal.setdefault("source", {})
                signal["source"].setdefault("media_id", media_id)
                signal["source"].setdefault("source_name", req.source_file)
                signal["source"].setdefault("location", req.location)
                signal["source"].setdefault("source_id", "")

                ok, errors = validate_schema(signal)
                if not ok:
                    # Convert validation failure into a structured error signal
                    signal = {
                        "source": {
                            "media_id": media_id,
                            "source_id": "",
                            "source_name": req.source_file,
                            "location": req.location,
                        },
                        "media": {
                            "media_type": "unknown",
                            "short_structural_summary": "Provider returned malformed JSON; validation failed.",
                            "confidence": {"overall": 0.0, "notes": "Schema validation failure."},
                        },
                        "extracted": {
                            "visible_text": [],
                            "entities": {"roles": [], "systems": [], "artifacts": [], "policies_or_guardrails": []},
                            "process": {"steps": [], "handoffs": []},
                            "decision_logic": {"decision_points": []},
                            "ui_workflow": {"screen_or_page": "", "fields": [], "actions": [], "validation_or_errors": []},
                            "signals": {
                                "contains_sequence": False,
                                "contains_branching": False,
                                "contains_escalation": False,
                                "contains_role_handoffs": False,
                                "contains_compliance_rules": False,
                            },
                            "ambiguities": [
                                {
                                    "issue": "Schema validation failure.",
                                    "possible_interpretations": errors,
                                    "recommended_disambiguation_question": "Ensure provider returns strict Mode B schema.",
                                }
                            ],
                        },
                    }

                append_jsonl(os.path.join(base, SIGNALS_JSONL), signal)
                append_jsonl(os.path.join(base, JOBS_WITH_SIGNALS_JSONL), {**j, "inference_output": signal})
                collected_signals.append(signal)
                break
            except Exception as e:
                last_err = str(e)
                if attempt < MAX_RETRIES:
                    time.sleep(0.5)
                    continue
                # Write structured error signal
                signal = {
                    "source": {
                        "media_id": media_id,
                        "source_id": "",
                        "source_name": req.source_file,
                        "location": req.location,
                    },
                    "media": {
                        "media_type": "unknown",
                        "short_structural_summary": "Inference call failed.",
                        "confidence": {"overall": 0.0, "notes": last_err or "Unknown error"},
                    },
                    "extracted": {
                        "visible_text": [],
                        "entities": {"roles": [], "systems": [], "artifacts": [], "policies_or_guardrails": []},
                        "process": {"steps": [], "handoffs": []},
                        "decision_logic": {"decision_points": []},
                        "ui_workflow": {"screen_or_page": "", "fields": [], "actions": [], "validation_or_errors": []},
                        "signals": {
                            "contains_sequence": False,
                            "contains_branching": False,
                            "contains_escalation": False,
                            "contains_role_handoffs": False,
                            "contains_compliance_rules": False,
                        },
                        "ambiguities": [
                            {
                                "issue": "Inference call failed.",
                                "possible_interpretations": [],
                                "recommended_disambiguation_question": "Check provider credentials, endpoint, and image path.",
                            }
                        ],
                    },
                }
                append_jsonl(os.path.join(base, SIGNALS_JSONL), signal)
                append_jsonl(os.path.join(base, JOBS_WITH_SIGNALS_JSONL), {**j, "inference_output": signal})
                collected_signals.append(signal)

        time.sleep(SLEEP_BETWEEN_REQUESTS_SEC)

    # Optionally write grouped per-source JSON files (cumulative across runs)
    if WRITE_GROUPED_PER_SOURCE:
        all_signals = read_jsonl(os.path.join(base, SIGNALS_JSONL))
        grouped = group_by_source(all_signals)

        for source_name, items in grouped.items():
            stem = os.path.splitext(source_name)[0]
            out_path = os.path.join(base, OUTPUT_DIR, f"{stem}_media_signals.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "source_file": source_name,
                        "generated_utc": datetime.utcnow().isoformat() + "Z",
                        "media_signals": items,
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )

    print("PASS 2B complete.")
    print(f"- Signals JSONL: {SIGNALS_JSONL}")
    print(f"- Jobs w/ signals JSONL: {JOBS_WITH_SIGNALS_JSONL}")
    if WRITE_GROUPED_PER_SOURCE:
        print(f"- Per-source grouped JSON: output/*_media_signals.json")


if __name__ == "__main__":
    from datetime import datetime
    main()
