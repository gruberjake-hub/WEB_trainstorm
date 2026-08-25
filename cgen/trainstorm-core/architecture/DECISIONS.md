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

---

## 2026-08-25 — The narrative decision log moves into git; its entries 2026-08-10 → 2026-08-21 are ratified as history

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** `architecture/decision-log.md` is the reasoning record behind this file — migrated
verbatim from the Claude Project doc `claude/decision-log.md`, which is retired as a writable
source. By merging this block Jake ratifies its entries dated 2026-08-10 through 2026-08-21 as the
decision history of the manifold. The two files are different genres of one history, not two copies:
**this file** holds the settled call in one short block; **the log** holds what was tried, found,
retracted and why. When they disagree, this file wins, and the fix is a new block here plus a new
dated entry there — never a silent edit to either.

**Why:** The 2026-08-25 identity-freeze block at the top of this file was written against a repo that held none of
the prior history, and so it superseded a decision it could not see (see the next block). "If a chat
disagrees with this file, this file wins" is the right rule; it was switched on before the history was
in the repo. The 08-19 log rule already said *the repo wins over the log* — this closes the loop by
making the log part of the repo.

**Consequences:**
- The Project copy `claude/decision-log.md` is a one-way snapshot from git from this commit forward
  (the GitHub sync already covers `architecture/`). Nothing is hand-written there again.
- The one entry in the log still marked **PENDING** (2026-08-21 Fable run — `atom.intent` empty and
  closed, `teaches` + `intended_response` to the occurrence) is **decided but not landed**: its patch
  has not been applied to `main`. Land it, then strike its banner.
- `STRUCTURE.md`'s line about a stale `cgen/trainstorm-core/decision-log.md` refers to a file that no
  longer exists; corrected in the same PR.

**Supersedes:** nothing. Adds the record this file was missing.

---

## 2026-08-25 — Occurrence identity: `atom_id` is the only *node* key; an occurrence of an atom in a course is addressable by its own stable key, linked to its atom. 1:many stands.

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** The 2026-08-20 (eighth) decision stands: **one atom may become many elements; two
stable ids; an explicit link.** `atom_id` is the only key of a *content node* — the lexicon entry,
the thing that carries meaning and `content_hash`, and the key that locale packs join on. An
**element** is one *occurrence* of an atom in a course: the same atom may appear as a `hook` in
module 1 and `reinforce` in module 5, and each occurrence must be addressable — by its own stable
`element_id` (prefix `ele_`), which references its atom (`composed_from`) and never carries authored
text of its own. Occurrence-level facets (`rhetorical`, `move`, expression keys, and — once the
PENDING restitch lands — `teaches`, `intended_response`) bind to the occurrence. Meaning-level facets
bind to the atom.

**Why:** The identity-freeze block above (2026-08-25, Jake / App-maker) re-derived the 2026-08-20
(seventh) reading — "same node, two costumes" — from the same three July documents that the eighth
entry showed cannot settle the question (they conflict, and one is a crosswalk from a parallel
workstream, not core canon). It superseded the 1:many decision without engaging the argument that
made it, which is instructional, not archaeological: *repetition is the instrument.* Preview → teach →
retrieve is the same atom at three positions; a model that cannot say "this one, here" cannot express
spaced retrieval without minting three atoms of identical meaning that then drift apart. Jake, on
review of that block: he did not intend to reverse 1:many, and "we'll be addressing the same atom
over and over again wearing different clothes" — which is exactly the point, and exactly why an
occurrence needs a key. The freeze was right that element is *not a rival canon*; it was wrong that an
occurrence is *not addressable*. Those are different axes, and it settled the wrong one.

**Consequences:**
- `STRUCTURE.md` restores `ele_` as the occurrence prefix. Do not mint `ele_` ids for *content*; do
  not mint `atom_` ids for *occurrences*. Two id spaces, two kinds of node.
- `element_id` is minted at realization (`promptpack_manifold.md` §8 was right on this point), joined
  to its atom by `composed_from` — the "explicit link" the eighth entry requires. Realizer (when it
  exists) mints occurrence ids; Couturier still owns style on the occurrence's expression facet and
  still mints nothing.
- **Locale packs key on `atom_id`** — the freeze's choice and the eighth entry's own "cheaper choice"
  agree. Element-level locale overrides only where presentation constrains the rendering (length
  limits, heading vs sentence), keyed by `element_id`; not built yet.
- `element.content` (authored text on the occurrence) remains a known violation under 1:many — flagged
  in the eighth entry, unchanged here, still owed.
- The 08-21 intent arc (`move` on the occurrence; `teaches` scoped per intervention) keeps its home.

**Supersedes:** the 2026-08-25 identity-freeze block's clauses "do not mint `ele_` IDs", "do not mint
`element_id` at realization", and "any reading that one atom becomes many element IDs". Its
working-process block is untouched. Its clauses that element is not a rival canon, that locale packs
bind to `atom_id`, and that facet owners mint no ids, stand.

**Process note, so it does not recur:** a decision block that supersedes another must quote or cite
the *argument* it is overturning, not only the *documents* it read. And "this file wins" only works
once this file holds the history — hence the block above.

---

## 2026-08-25 — Schemas enforce occurrence identity; the 2026-08-21 intent restitch lands

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The schemas now match the ratified 1:many occurrence identity (this file, previous
block / PR #8). An **element** is one occurrence of an atom in a course: required `composed_from`
(an `atom_id`); `element_id` is the occurrence key (`ele_`, minted at realization); locale packs are
not keyed by `element_id`. Authored meaning does not live on the element — `content` / `content.text`
is no longer required as the source-meaning store; meaning lives on the atom. Occurrence facets stay
on the element: `rhetorical`, `move`, `teaches`, `intended_response`, expression keys. Optional
`content` is flagged as presentation-constraint copy only; default is omit.

The PENDING 2026-08-21 Fable-run restitch is **landed**: `atom.bindings.intent` is empty and closed
(`additionalProperties: false`, no properties). `teaches` and `intended_response` live on the
occurrence. Procedure / form / instance facets are unchanged. Live Astellas SOP/form stores
(`ast_alsap`, `alsap`, `alsap_asp9999`) remain atoms — they are not rewritten into elements.

**Why:** Prose already said 1:many. The schemas still described the element as a rival meaning node
(`content` as source locale, `element_id` as the locale-pack join key) and still stored `teaches` on
the atom. The contract now agrees with the decision.

**Consequences:**
- Gates (`validate_atoms.py`, `validate_objectives.py`) enforce the closed `atom.intent` and the
  occurrence link (`composed_from` required; leftover `intent.teaches` on an atom is a hard fail).
- `reference/example_element.json` carries `composed_from` and no authored `content`.
- `reference/example_atom.json` carries no intent fields.
- The PENDING banner on the 2026-08-21 Fable-run log entry is struck.

**Supersedes:** the "decided but not landed" clause of the 2026-08-25 narrative-log-migration block;
the occurrence-identity block's clause that "`element.content` … remains a known violation … still
owed", as to *required authored meaning on the element*. Optional presentation-constraint copy may
still appear, flagged, not as the meaning store. Realize.py / Dragoman / renderer are not in this
landing.

---

## 2026-08-25 — Realizer v1 exists: one occurrence per atom; 1:many accretes later

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Realizer v1 exists as `tools/realize.py`. It reads a live atom store (default
`cgen/astellas/projects/ast_alsap`, 47 SOP atoms), mints **one occurrence per atom**, and writes a
separate occurrence store plus a double-clickable HTML lesson. Each element gets a new stable
`ele_` id, `composed_from` = that atom's `atom_id`, occurrence `move` = `present` (closed vocab),
and **no authored `content.text`**. Display HTML reads meaning from the atom. Provenance is
`realized_from` / source hashes on the store manifest and on each element (`source_hash` echoes the
atom's `content_hash`). Live SOP/form atoms are not rewritten into elements.

v1 is deliberately 1:1 and ugly. Later 1:many (preview / teach / retrieve as three elements of the
same atom) can accrete more `ele_` records without changing atom ids. Cartographer is not a v1
blocker. The `atom → primitives` hop remains owed; this hop realizes the atom store directly so the
course chain can start.

**Why:** Schemas already enforce 1:many (previous block / PR #9). The course half had never run —
no writer of occurrence nodes. This is that writer.

**Consequences:**
- From `cgen/trainstorm-core`: `python tools/realize.py` (optional `--project` like other harness
  tools). Writes `<project>/occurrences/elements.json`, `occurrences/manifest.json`, and
  `<project>/realized_lesson.html`.
- Minted elements validate against `element.schema.json`. `validate_atoms.py` stays green on the
  three Astellas stores — it still only gates `atoms.json`.
- Couturier (style keys), Dragoman, Storyline, `.potx`, and `tools/render/` PNG pipelines are not
  this landing.

**Supersedes:** `STRUCTURE.md`'s marker that `realize.py` is absent; the previous block's clause
that Realize.py is not in that landing. Atom identity, locale packs on `atom_id`, and "element is
not a rival canon" stand.

