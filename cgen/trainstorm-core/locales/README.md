# locales/  (externalized translations — keyed by atom_id)
One pack per language: en.json, ja.json, fr-CA.json …
Each entry: { "<atom_id>": { "target": "...", "status": "validated",
              "reviewer": "...", "source_hash": "sha256:..." } }
Never embed translations in the atom; they live here.
Packs key on `atom_id` — meaning is translated once, not once per occurrence. Occurrence-level overrides (length limits, heading vs sentence) would key on `element_id`; not built. See `architecture/DECISIONS.md` (2026-08-25, occurrence identity).
