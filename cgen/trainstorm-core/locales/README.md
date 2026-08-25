# locales/  (externalized translations — keyed by atom_id)
One pack per language: en.json, ja.json, fr-CA.json …
Each entry: { "<atom_id>": { "target": "...", "status": "validated",
              "reviewer": "...", "source_hash": "sha256:..." } }
Never embed translations in the atom; they live here.
`atom_id` is the only node key — see `architecture/DECISIONS.md` (2026-08-25). Do not mint `ele_` IDs.
