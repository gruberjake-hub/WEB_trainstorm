# Cartographer heuristic v2 — expository kinds + the intent_map (additive to v1)

*2026-08-31, Brunswick paytrans drive. Additive: every v1 rule stands; a store with no
`occurrences/intent_map.json` behaves byte-identically to v1 (proven on ast_alsap and
ast_artwork by regeneration diff). Policy ids: `v1_heuristic_compiler` + `v1_intent_map`.*

## Why v2 exists

The first expository corpus (structure.v0.2 kinds: `document` / `section` / `statement`)
broke two v1 assumptions:

1. **"No `belongs_to` → hook" assumed one root.** A multi-document corpus has several
   document roots, and which one opens the lesson is COURSE DESIGN, not structure. A
   heuristic cannot know it; a designer must say it.
2. **`bind_teaches` is ALSAP-hardcoded Python.** The 2026-08-27 decisions retired exactly
   this shape for scenes and lessons ("a later agent appends JSON; it does not edit
   realize.py"). Objective bindings are the designer's judgment — the same class of
   project data.

## New classification rules (first-match order preserved)

| When | move | rhetorical | confidence |
|---|---|---|---|
| `kind: document` (fires BEFORE the no-belongs_to hook rule) | `present` | `orient` | **low** — `document_root_expository`; the intent_map elects at most one hook |
| `kind: statement` | `present` | `assert` | high (`kind_present`) |
| `kind: section` | falls to `section_head_as_present` | `organize` | high |

SOP roots keep `kind: procedure` and still take the v1 hook rule — nothing moves for them.

## The intent_map — designer bindings as project data

`occurrences/intent_map.json`: `{"policy": "v1_intent_map", "map": {"<atom_id>":
{"teaches": [obj_ids], "move": optional, "why": optional}}}`. Closed entry shape.

- **Cartographer stays the single writer** of the intent facet. The map is its governed
  input — validated on load: every obj id must exist in `ontology/objectives.json`, every
  move in the closed pedagogical vocab, and **at most one entry may elect `hook`** (a
  lesson opens once).
- A map `move` never overrides a Realizer-stamped **extra** occurrence's move (the extra
  exists because that move is different); `teaches` still binds on extras.
- When the map binds `teaches` on an atom the heuristic had demoted ONLY for
  `teaches_unbound`, the classifier's own confidence is restored; a map move override
  stamps confidence `map`.
- Atoms absent from the map keep pure heuristic bindings, and `teaches_unbound` keeps
  reporting them honestly. Unbound is a statement, not a failure.

Self-tested: document-root default, statement classification, hook election + teaches
binding on a primary, extra-move preservation under a map override, ungoverned-obj
rejection, double-hook rejection.
