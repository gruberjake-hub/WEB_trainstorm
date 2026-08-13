"""Create a filtered, provenance-preserving inventory of ChatGPT conversations."""

from __future__ import annotations

import argparse
import json
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="ChatGPT export ZIP, JSON file, or directory")
    parser.add_argument("--output", type=Path, required=True, help="Destination JSONL file")
    parser.add_argument("--terms", nargs="*", default=[], help="Case-insensitive search terms")
    return parser.parse_args()


def load_json_files(root: Path) -> Iterable[dict[str, Any]]:
    files = [root] if root.is_file() else sorted(root.rglob("*conversation*.json"))
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            yield from (item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            conversations = payload.get("conversations")
            if isinstance(conversations, list):
                yield from (item for item in conversations if isinstance(item, dict))
            else:
                yield payload


def message_text(message: dict[str, Any]) -> str:
    content = message.get("content") or {}
    parts = content.get("parts") or []
    return "\n".join(part for part in parts if isinstance(part, str)).strip()


def iter_messages(conversation: dict[str, Any]) -> Iterable[dict[str, Any]]:
    mapping = conversation.get("mapping") or {}
    for node in mapping.values():
        message = node.get("message") if isinstance(node, dict) else None
        if not isinstance(message, dict):
            continue
        text = message_text(message)
        if not text:
            continue
        author = message.get("author") or {}
        yield {
            "message_id": message.get("id"),
            "author_role": author.get("role"),
            "create_time": message.get("create_time"),
            "update_time": message.get("update_time"),
            "text": text,
        }


def inventory(conversation: dict[str, Any], terms: list[str]) -> dict[str, Any] | None:
    title = str(conversation.get("title") or "Untitled")
    messages = list(iter_messages(conversation))
    needles = [term.casefold() for term in terms if term.strip()]
    haystack = "\n".join([title, *(message["text"] for message in messages)]).casefold()
    matched_terms = [term for term, needle in zip(terms, needles) if needle in haystack]
    if needles and not matched_terms:
        return None
    return {
        "conversation_id": conversation.get("id") or conversation.get("conversation_id"),
        "title": title,
        "create_time": conversation.get("create_time"),
        "update_time": conversation.get("update_time"),
        "matched_terms": matched_terms,
        "message_count": len(messages),
        "messages": messages,
    }


def write_inventory(source: Path, output: Path, terms: list[str]) -> tuple[int, int]:
    scanned = included = 0
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as destination:
        for conversation in load_json_files(source):
            scanned += 1
            record = inventory(conversation, terms)
            if record is None:
                continue
            destination.write(json.dumps(record, ensure_ascii=False) + "\n")
            included += 1
    return scanned, included


def main() -> int:
    args = parse_args()
    if not args.input.exists():
        raise SystemExit(f"Input does not exist: {args.input}")

    if zipfile.is_zipfile(args.input):
        with tempfile.TemporaryDirectory(prefix="trainstorm-chat-capture-") as temp_dir:
            with zipfile.ZipFile(args.input) as archive:
                archive.extractall(temp_dir)
            scanned, included = write_inventory(Path(temp_dir), args.output, args.terms)
    else:
        scanned, included = write_inventory(args.input, args.output, args.terms)

    print(f"Scanned {scanned} conversations; wrote {included} to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
