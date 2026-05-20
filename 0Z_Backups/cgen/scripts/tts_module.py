#!/usr/bin/env python3
"""
tts_module.py — Standalone Kokoro TTS renderer
------------------------------------------------
Inputs:  .txt file | course.json | manual paste
Output:  WAV or MP3 (chosen at runtime)

Install dependencies:
    pip install kokoro soundfile pydub
    # For MP3 support, also install ffmpeg:
    # Windows: winget install ffmpeg   or   choco install ffmpeg
    # Mac:     brew install ffmpeg

Usage examples:
    python tts_module.py --file script.txt --output narration.mp3 --format mp3
    python tts_module.py --file course.json --output module_audio.wav --format wav
    python tts_module.py --paste --output test.mp3 --format mp3
    python tts_module.py --list-voices
"""

import argparse
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Available Kokoro voices
# ---------------------------------------------------------------------------
VOICES = {
    "af_heart":   "Female, American, warm (default)",
    "af_bella":   "Female, American, professional",
    "af_nicole":  "Female, American, conversational",
    "af_aoede":   "Female, American, expressive",
    "am_adam":    "Male, American, neutral",
    "am_michael": "Male, American, authoritative",
    "bf_emma":    "Female, British",
    "bm_george":  "Male, British",
    "bm_lewis":   "Male, British, warm",
}


# ---------------------------------------------------------------------------
# Input handlers
# ---------------------------------------------------------------------------

def load_from_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if p.suffix.lower() == ".json":
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        return extract_narration_from_json(data)
    else:
        return p.read_text(encoding="utf-8")


def extract_narration_from_json(data) -> str:
    """
    Walk course.json and collect all narration/script/text field values.
    Adjust the target keys below to match your actual course.json schema.
    """
    TARGET_KEYS = {"narration", "script", "narrator_text", "vo", "voiceover", "text"}
    lines = []

    def walk(obj):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if key.lower() in TARGET_KEYS and isinstance(val, str) and val.strip():
                    lines.append(val.strip())
                else:
                    walk(val)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)

    if not lines:
        raise ValueError(
            "No narration fields found in JSON. "
            "Check TARGET_KEYS in extract_narration_from_json() against your schema."
        )

    return "\n\n".join(lines)


def load_from_paste() -> str:
    print("Paste your script below.")
    print("When finished: press Enter, then Ctrl+D (Mac/Linux) or Ctrl+Z + Enter (Windows).")
    print("-" * 60)
    lines = []
    try:
        for line in sys.stdin:
            lines.append(line)
    except EOFError:
        pass
    return "".join(lines).strip()


# ---------------------------------------------------------------------------
# Audio rendering
# ---------------------------------------------------------------------------

def render(text: str, voice: str, speed: float, output_path: Path, fmt: str):
    # Lazy imports so the module is importable even without deps installed
    try:
        from kokoro import KPipeline
    except ImportError:
        sys.exit("Kokoro not found. Run: pip install kokoro")

    try:
        import numpy as np
        import soundfile as sf
    except ImportError:
        sys.exit("Missing audio deps. Run: pip install soundfile numpy")

    print(f"\nLoading Kokoro (voice: {voice}, speed: {speed}x)...")
    pipeline = KPipeline(lang_code="a")  # 'a' = American English

    print(f"Rendering {len(text):,} characters of script...")
    chunks = []
    for _, _, audio in pipeline(text, voice=voice, speed=speed):
        chunks.append(audio)
        print(".", end="", flush=True)
    print()

    if not chunks:
        sys.exit("Kokoro returned no audio. Check your script content.")

    full_audio = np.concatenate(chunks)
    sample_rate = 24000  # Kokoro native sample rate

    if fmt == "wav":
        sf.write(str(output_path), full_audio, sample_rate)
        print(f"\nSaved WAV → {output_path}")

    else:  # mp3
        # Write temp WAV, convert to MP3 via pydub + ffmpeg
        tmp = output_path.with_suffix(".tmp.wav")
        sf.write(str(tmp), full_audio, sample_rate)
        try:
            from pydub import AudioSegment
            AudioSegment.from_wav(str(tmp)).export(str(output_path), format="mp3")
            tmp.unlink()
            print(f"\nSaved MP3 → {output_path}")
        except ImportError:
            fallback = output_path.with_suffix(".wav")
            tmp.rename(fallback)
            print(
                "\npydub not installed — saved as WAV instead.\n"
                "To enable MP3: pip install pydub  (also requires ffmpeg)\n"
                f"Saved WAV → {fallback}"
            )


# ---------------------------------------------------------------------------
# Output path helper
# ---------------------------------------------------------------------------

def resolve_output(output_arg: str, fmt: str) -> Path:
    p = Path(output_arg)
    if p.suffix.lower() not in (".mp3", ".wav"):
        p = p.with_suffix(f".{fmt}")
    return p


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Kokoro TTS — script in, audio out.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Input — mutually exclusive
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", metavar="PATH",
                     help=".txt script or course.json file")
    src.add_argument("--paste", action="store_true",
                     help="Paste script text interactively")
    src.add_argument("--list-voices", action="store_true",
                     help="Print available voices and exit")

    # Output
    parser.add_argument("--output", "-o", metavar="PATH",
                        help="Output file path (e.g. narration.mp3)")
    parser.add_argument("--format", "-f", choices=["mp3", "wav"],
                        help="Output format")

    # Voice / quality
    parser.add_argument("--voice", "-v", default="af_heart",
                        metavar="VOICE_ID",
                        help="Kokoro voice ID (default: af_heart)")
    parser.add_argument("--speed", type=float, default=1.0,
                        metavar="N",
                        help="Speech speed multiplier (default: 1.0)")

    args = parser.parse_args()

    # --- List voices ---
    if args.list_voices:
        print("\nAvailable Kokoro voices:\n")
        for vid, desc in VOICES.items():
            marker = "  *" if vid == "af_heart" else "   "
            print(f"{marker} {vid:<14}  {desc}")
        print("\n  * = default\n")
        return

    # --- Validate output args when rendering ---
    if not args.output:
        parser.error("--output is required when rendering audio")
    if not args.format:
        parser.error("--format (mp3 or wav) is required when rendering audio")

    # --- Load script ---
    if args.file:
        print(f"Loading script from: {args.file}")
        script = load_from_file(args.file)
    else:
        script = load_from_paste()

    if not script.strip():
        sys.exit("No script content found. Nothing to render.")

    # Preview
    preview = script[:120].replace("\n", " ")
    ellipsis = "..." if len(script) > 120 else ""
    print(f"\nScript loaded ({len(script):,} chars)")
    print(f"Preview: {preview}{ellipsis}\n")

    # --- Validate voice ---
    if args.voice not in VOICES:
        print(f"Warning: '{args.voice}' not in known voice list. Attempting anyway.")
        print(f"Run --list-voices to see confirmed options.\n")

    # --- Render ---
    output_path = resolve_output(args.output, args.format)
    render(script, args.voice, args.speed, output_path, args.format)
    print("Done.")


if __name__ == "__main__":
    main()