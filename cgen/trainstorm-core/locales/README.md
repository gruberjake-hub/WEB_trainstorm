# locales/  (externalized translations — keyed by atom_id)
One pack per language: en.json, ja.json, fr-CA.json …
Each entry: { "<atom_id>": { "target": "...", "status": "validated",
              "reviewer": "...", "source_hash": "sha256:..." } }
Never embed translations in the atom; they live here.
Packs key on `atom_id` — meaning is translated once, not once per occurrence. Occurrence-level overrides (length limits, heading vs sentence) would key on `element_id`; not built. See `architecture/DECISIONS.md` (2026-08-25, occurrence identity).

**Sibling family (2026-08-31):** locale packs are one axis of the rendering space; VOICE packs
(`voice/<register>.json`, per-project) are the other — register instead of language, same keying,
same fields, gated by `schemas/voice.pack.schema.json` against `vocab/register.enum.json`.

**`derived_from` (optional, 2026-08-31):** when a translation was rendered from an accepted voice
entry rather than the verbatim atom, the entry additionally carries
`"derived_from": { "pack": "voice/<register>.json", "key": "<atom_id>", "hash": "sha256:<of the voice entry's text>" }`.
`source_hash` STILL pins the atom — the meaning gate always judges against the atom, never
transitively. `derived_from` records the text the writer worked from, so authored voice choices
transmit and staleness propagates down the chain (atom changes → voice stale → descendants stale).
Backward-compatible: entries without `derived_from` were rendered from the verbatim atom.
