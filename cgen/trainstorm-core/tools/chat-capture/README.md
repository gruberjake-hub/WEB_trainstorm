# ChatGPT conversation capture

`extract_chatgpt.py` creates a provenance-preserving inventory from a ChatGPT data export. It does
not decide which ideas belong in Trainstorm Core and does not edit canonical architecture.

Keep exports and generated output under the ignored `.chat-capture/` directory:

```powershell
python tools/chat-capture/extract_chatgpt.py `
  .chat-capture/raw/chatgpt-export.zip `
  --output .chat-capture/inventory.jsonl `
  --terms CGEN Trainstorm "course generation" manifold schema
```

The input may be an export ZIP, a `conversations.json` file, or a directory containing numbered
conversation JSON files. A conversation is included when a term appears in its title or message
text. With no `--terms`, every conversation is inventoried.

Each JSONL record contains conversation metadata and matching text messages with their original
message IDs, author roles, timestamps, and text. Non-text payloads are noted but not extracted.

See `architecture/conversation-reconciliation.md` for the review and promotion rules.
