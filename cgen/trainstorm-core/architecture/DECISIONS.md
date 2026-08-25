# Decisions

Append-only. Dated blocks, one decision each. If a chat disagrees with this file, **this file wins.**

Signed: **Jake** / **Claude** / **App-maker** (Cursor cloud agents on this repo) / other.

---

## 2026-08-25 — Identity freeze: `atom_id` is the only node key

**Signed:** Jake / App-maker

**Decision:** `atom_id` is the only node key. An **element** is the same node in a course costume, not a second ID space. Do not mint `ele_` IDs. Do not mint `element_id` at realization as a new key. Locale packs and expression keys bind to `atom_id`. Couturier owns style on the expression facet; Realizer (when it exists) owns layout/render; neither invents a new id. Single-writer per facet still holds.

**Why:** Three sources disagreed: `STRUCTURE.md` listed `ele_` and `atom_` as separate prefixes; `architecture/reconciliation.md` already said make `element_id` the stable `atom_id`; `architecture/promptpack_manifold.md` §8 minted `element_id`s at realization, joined by a `derivation` stamp. A second ID space at realization would split the graph the live harness already validates as atoms (`tools/validate_atoms.py`, `atom.schema.json`). Costume is not identity.

**Consequences:**
- New content nodes take an `atom_` id and keep it. Never reuse, never edit.
- Locale packs, expression keys, and other facet stores join on `atom_id`.
- `element.schema.json` remains the course-chain *costume* (fields, render facets) of that same node — not a rival canon and not a second key.
- Historical `ele_…` strings in examples and July docs are costumes of a node, not a license to mint a parallel space.
- Couturier / Realizer / Dragoman (when built) write their facet; they do not mint node ids.

**Supersedes:** the open identity question in `STRUCTURE.md` (2026-08-20); minting `element_id`s at realization in `architecture/promptpack_manifold.md` §8; any reading that one atom becomes many element IDs (including the 2026-08-20 Couturier 1:many ID-space note). The “same node, two costumes” reading stands.

---

## 2026-08-25 — Working process: git is the shared brain

**Signed:** Jake / App-maker

**Decision:** Git is the only shared brain between Claude and other assistants (including App-maker). Assistants open pull requests. Jake merges. Jake pulls to his machine. He prefers this over an assistant editing local files and pushing. This file (`architecture/DECISIONS.md`) is canon for settled calls. Claude project knowledge (`project/custom_instructions.md`, `project/knowledge_manifest.md`, and whatever is synced into the Claude Project) is a **one-way snapshot FROM git** — a pointer at canon, not a second constitution. Do not push to `main`.

**Why:** Always-on Claude notes drifted: they still named `element.schema.json` as the canonical unit while the live graph is atoms. Dual-maintained prose rebuilds the same drift the manifold exists to prevent.

**Consequences:**
- Propose on a branch; open a PR; Jake merges; Jake pulls. That is the write path.
- Before claiming a contradiction is settled, read this file. If a chat and this file disagree, this file wins — then, if the chat was right, append a new dated block (do not silently edit an old one except to add a **Supersedes** pointer from a newer block).
- After merge, re-sync Claude knowledge from git. Do not hand-edit the Project copy into a rival source.
- Session notes under `architecture/sessions/` are memory, not canon.

**Supersedes:** treating Claude Custom Instructions / Project knowledge as an independently maintained constitution.
