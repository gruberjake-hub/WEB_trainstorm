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

**Pointer:** a later 2026-08-26 block pays that hop (`agents/realizer/primitives_v1.md`).

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

---

## 2026-08-25 — Cartographer v1: heuristic compiler writes occurrence intent on the ALSAP store

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Cartographer v1 exists as `tools/cartographer.py`. It is a **documented heuristic
compiler** (`agents/cartographer/heuristic_v1.md`, policy `v1_heuristic_compiler`), not an ID
genius. It reads atoms for meaning and writes **only occurrence intent** (`move`, `teaches`,
`rhetorical`, `intended_response`) onto the Realizer's existing `ele_` records. It never mints
`ele_` or `atom_` ids, never copies meaning onto the element, never rewrites `atoms.json`.

`teaches` is now bindable because the ontology has a **small real ALSAP seed**: one draft goal
(`goal_alsap_asset_safety_monitored`) and five draft `obj_` nodes distilled from SOP-AST-29080 —
the procedure the live atom store already is. Status is `draft`, not `example` and not `validated`:
the SOP is real; the human objective-lock conversation has not happened. The AST009 PSI goal + two
objectives remain `status: example`. This is not a 50-node fake competency graph.

`move` is a first-match walk over atom structure/kind (title → `hook`, purpose → `objective`,
definitions/roles → `activate` flagged low, govdocs → `exemplify` flagged low, handoff steps →
`transfer` flagged low, steps/lists → `present`). Closed vocab from `intent.enum.json`. No
`practice`/`assess`/`reinforce` invented for atoms this SOP does not contain. Low-confidence is
flagged on `ext.cartographer`, not silently upgraded.

Single-writer: only Cartographer writes those intent fields. A re-run of `realize.py` preserves
`ext.cartographer` + bound intent. HTML (`realized_lesson.html`) is re-projected so move pills are
not all `present`.

**Why:** Previous Cartographer dispatches wrote nothing because `teaches` was unbindable (ontology
was two PSI examples). Realizer v1 minted 47 occurrences, all `move=present`. Intent is occurrence-
level under 1:many; this is the first writer of that facet on a live store.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/cartographer.py` (optional `--project` like realize).
  Updates `<project>/occurrences/elements.json` in place, stamps the occurrence manifest, rewrites
  `<project>/realized_lesson.html`.
- `python3 tools/validate_objectives.py` and `python3 tools/validate_atoms.py` stay green. Elements
  validate against `element.schema.json`. Atoms unchanged.
- Next hop is **Couturier** (style keys on the occurrence) or **Realizer 1:many minting** (a second
  `ele_` for hook+present). Cartographer does not mint occurrences.

**Supersedes:** the Realizer v1 block's clause that "Cartographer is not a v1 blocker" as to *this
facet remaining unbound*. Realizer still mints `ele_` ids; Cartographer still mints none. The
example PSI ontology is not deleted.

---

## 2026-08-25 — Realizer 1:many seed: two ALSAP atoms mint a second occurrence

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The live ALSAP occurrence store is no longer strictly 1:1. Realizer
mints a **small, honest extra-occurrence seed** (`agents/realizer/one_to_many_v1.md`,
store policy `v1_one_to_many_seed`) — not the whole SOP. Two teaching-worthy atoms
get a second `ele_` record, each with its own stable id, `composed_from` pointing
at the same `atom_id`, and a distinct `intent.move`. The other 45 atoms stay 1:1.
`atoms.json` is untouched. No authored `content.text` on occurrences. Locale packs
still key on `atom_id`.

Seed:

- `atom_sop_ast29080` (SOP title): primary remains Cartographer’s `hook`; extra
  `ele_sop_ast29080__present` is stamped `present` (hook + present).
- `atom_sop_ast29080_general` (what an ALSAP is): primary remains Cartographer’s
  `present`; extra `ele_sop_ast29080_general__reinforce` is stamped `reinforce`
  (present + retrieve/retention). Closed vocab has no `retrieve`; `reinforce` is
  Gagné 9a and is the legal name.

Idempotency: extra ids are `(primary ele_) + "__" + move`. A re-run of
`realize.py` accretes missing extras and never drops existing extras or
Cartographer bindings. Cartographer remains the single writer of occurrence
intent on re-run, except it **preserves Realizer-stamped `move` on extra
occurrences** (the extra exists because that move is different) and still binds
`teaches` / `rhetorical` / `intended_response`. HTML groups cards that share
`composed_from`.

**Why:** Schemas and this file already said 1:many. The store was still 1:1
(Realizer v1 minted one `ele_` per atom; Cartographer bound intent on those
records). This hop proves the instrument — the same atom, twice, under different
teaching acts — without an ID treatment of all 47 atoms and without duplicating
authored meaning.

**Consequences:**

- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py`. Optional `--no-one-to-many` skips minting new
  extras but still preserves any that exist. `--selftest` on both tools.
- Next hop is still **Couturier** (style keys). Not a full spaced-retrieval
  treatment of the SOP. Couturier still mints nothing.

**Pointer:** a later 2026-08-25 block adds one more seed atom (`purpose`) and
projects extra `reinforce` as a check, not a recap.

**Supersedes:** the Realizer v1 block’s “v1 is deliberately 1:1” as to *the live
ALSAP store remaining 1:1*; one occurrence per atom remains the default for
unseeded atoms. Cartographer v1’s “Next hop is Couturier or Realizer 1:many
minting” as to the minting half — Couturier is still unbuilt. Cartographer still
mints no ids. Working-process block untouched.

---

## 2026-08-25 — Couturier v1: first writer of style on the occurrence

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Couturier v1 exists as `tools/couturier.py`. It is a **documented
move→look map** (`agents/couturier/style_map_v1.md`, policy `v1_move_to_look`),
not a design system and not ID genius. It reads already-minted `ele_` records
and writes **only occurrence style keys** onto `element.expression`
(`style_ref`, `text_primitive`, `content_role`, `layout_hint`). It never mints
`ele_` or `atom_` ids, never copies meaning onto the element, never rewrites
`atoms.json`, never writes `element.intent`. Locale packs stay keyed on
`atom_id`. Style is keyed on `element_id`.

The map is from Cartographer’s `intent.move`. Three looks carry the 1:many
instrument: `hook` → `brand.opening` / `tp_display`; `present` →
`brand.instructional` / `tp_body`; `reinforce` → `brand.recall` / `tp_recall`
(retrieve/retention; closed vocab has no `retrieve`). Other live moves
(objective / activate / exemplify / transfer) get a distinct look so the page
is not 36 identical present-cards. Unmapped moves (`practice` / `feedback` /
`assess`) are left undressed — no invented look. `teaches` does not change
clothes in v1.

v1 does **not** bind `motion_primitive` (registry still empty — stub),
`layout_primitive` (the `.potx` / Storyline set), or `interaction_primitive`.
If a foreign key is already set, it is preserved, not overwritten. HTML
(`realized_lesson.html`) reads the expression keys for clothes; meaning still
comes from the atom. 1:many pairs must wear distinct `style_ref` values.

Idempotency: re-run of Couturier mints nothing. Re-run of realize preserves
`expression` + `ext.couturier` (and extras, and Cartographer intent). Re-run
of cartographer does not wipe style.

**Why:** Realizer minted `ele_` records (including a 1:many seed) and
Cartographer bound `move` / `teaches`, but the HTML still looked like the same
SOP card for every move. Style is an occurrence-level facet — the same atom
wears different clothes at hook vs present vs reinforce. This is the first
writer of that facet on a live store. The expression facet already existed on
`element.schema.json`; no parallel store.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Optional `--project` / `--selftest` like the others.
- `vocab/primitives.registry.json` is `v0.3`: a handful of `style_ref` +
  `text_primitive` keys seeded. Layout/interaction keys unchanged. Motion
  still empty.
- Next hop is not this landing: Dragoman, Storyline, `.potx`, motion
  primitives, `tools/render/` PNG pipelines.

**Supersedes:** the Realizer 1:many seed block’s “Couturier is still unbuilt”
and “Next hop is still Couturier”. Realizer still mints `ele_` ids;
Cartographer still owns intent; Couturier still mints none. Working-process
block untouched.

**Pointer:** a later 2026-08-25 block projects `reinforce` / `brand.recall` as a
check UI (`layout_hint: check`), not a quoted recap.

---

## 2026-08-25 — Extra `reinforce` is a check: render of move + atom meaning

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Traditional ID’s third move is a check. Extra `reinforce`
occurrences (Gagné 9a; closed vocab has no `retrieve`) now **project as a
check the reader can attempt**, derived only from the atom’s existing
meaning. Not a new agent. Realizer still mints `ele_` ids and owns the HTML
projection (`agents/realizer/check_v1.md`, policy `v1_check_from_atom`).
Cartographer still owns intent. Couturier still owns style (`brand.recall` /
`tp_recall`; `layout_hint` is `check`, not `recap`). No authored
`content.text` on the element. `atoms.json` unchanged. Locale packs stay
keyed on `atom_id`.

The check is a **shape**, not a second meaning. Stem is a grammatical invert
of this atom’s first sentence (`{subject} is {complement}` → `What is
{subject}?`). Key is the complement — a substring of this atom. Distractors,
if any, are first sentences of sibling atoms in the same store (closed
contrast). If siblings are thin, fall back to a cloze of this atom. Do not
invent facts, numbers, SOP rules, or misconceptions.

Seed stays small. The ALSAP definition extra
(`ele_sop_ast29080_general__reinforce`) is the required check. One more
teaching-worthy atom is minted: `atom_sop_ast29080_purpose` → extra
`ele_sop_ast29080_purpose__reinforce`. Title extra stays `present`. Do not
1:many the entire store.

Idempotent: re-run of realize → cartographer → couturier keeps extra `ele_`
ids, intent, style, and the same check projection (pure function of store +
move).

**Why:** After Couturier v1 the extra `reinforce` *looked* like recall
clothes but still *read* as an italic reprint of the SOP sentence. Clothes
without a check are not instruction. 1:many’s extra occurrence has to
instruct.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  `--selftest` on all three. Default project `cgen/astellas/projects/ast_alsap`.
- Open `cgen/astellas/projects/ast_alsap/realized_lesson.html` — the two
  `reinforce` extras are stem + choices, not a Remember recap.
- Elements still validate against `element.schema.json`. No new move enum.
  No `interaction_primitive` (Storyline). No option labels on
  `element.assessment`.

**Supersedes:** the Couturier v1 clause that `reinforce` HTML is a “quoted
recap”; the 1:many seed’s “two atoms” count as to *the live store remaining
two extras* — three extras now, still a seed. Realizer still mints `ele_`
ids; Cartographer still owns intent; Couturier still mints none.
Working-process block untouched.

**Pointer:** a later 2026-08-25 block projects a short lesson spine; the full
dump remains as coverage.

---

## 2026-08-25 — Lesson spine v1: short path; full dump is coverage

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The default realized HTML is a **short ALSAP lesson**, not every
SOP atom in document order. Spine membership is a documented heuristic
(`agents/realizer/spine_v1.md`, policy `v1_front_matter_then_checks`), not
fake ID genius and not an LLM call. Realizer projects a stable sequence of
**existing** `ele_` ids onto the occurrence manifest and default-renders
that order. The full dump remains as `realized_coverage.html`. No
`ele_` records or atoms are dropped. `atoms.json` unchanged.

The object graph (`belongs_to` / `order`) is SOP document structure. Walking
it *is* the 47-card dump, so it is not the path. Spine v1 reuses those roles
as input: document root (hook + seeded title present), then teachable
direct-child procedure/form paragraphs in `object.order` (skip thin headings
and glossary pointers — same bar as check siblings), then the existing
`reinforce` extras as checks. Descendants (lists, steps, A/B/C heads) stay
coverage.

Live ALSAP path (seven occurrences): `ele_sop_ast29080` (hook) →
`ele_sop_ast29080__present` → `ele_sop_ast29080_purpose` (objective) →
`ele_sop_ast29080_scope` → `ele_sop_ast29080_general` →
`ele_sop_ast29080_purpose__reinforce` (check) →
`ele_sop_ast29080_general__reinforce` (check). Reuses the existing 1:many
seed. Does not mint a pile of new extras. Does not invent `retrieve`.
Distractors stay closed-contrast sibling atoms (verbatim). Jake parked a
future distractor-writer agent; this hop does not build it.

Cartographer still owns intent. Couturier still owns style. Spine is
sequence/selection — Realizer projection. Idempotent with realize →
cartographer → couturier.

**Why:** The course hop is proven (atoms → occurrences → move/teaches →
style → reinforce checks). The HTML was still a dressed SOP. A course is a
short teachable path plus coverage, not 47 sequential cards.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`.
- Open `cgen/astellas/projects/ast_alsap/realized_lesson.html` — short
  lesson. Open `realized_coverage.html` — full SOP dump. Link both ways.
- Manifest carries `spine.element_ids`. Store stays 50 `ele_` / 47 atoms.

**Pointer:** a later 2026-08-26 block puts one real procedure lead on this
spine (still coverage for the rest of the SOP).

**Supersedes:** the Realizer v1 / Cartographer / Couturier clauses that the
default HTML *is* the document-order walk of every occurrence. Those walks
remain as coverage. Working-process block untouched. Single-writer per facet
stands. Locale packs stay keyed on `atom_id`.

---

## 2026-08-26 — One real procedure on the ALSAP lesson spine

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The short ALSAP lesson now includes **one teaching-worthy
procedure present** after front-matter and before the existing checks.
Spine membership is still a documented heuristic (`agents/realizer/spine_v1.md`,
policy `v1_front_matter_one_procedure_then_checks`), not fake ID genius and
not an LLM call. Realizer projects a stable sequence of **existing** `ele_`
ids. `atoms.json` unchanged. Store gains **no** extra `ele_`.

**Which procedure / atom, and why.** Object `belongs_to` / `order` already
has the procedure parent/sequence. The first branch under the thin
`Procedures.` heading is Procedure A — *Plan Development of ALSAP.* That is
the entry to doing the work: B (develop/maintain) and C (analysis outputs)
cannot start until a Lead is requested. The A/B/C heading atoms are thin
(same bar as check siblings). The lead atom is the first `procedure_step`
child: `atom_sop_ast29080_proc_a_s1` (*Notify a member of Safety Data
Science in QSEG of the need for an ALSAP and request an ALSAP Lead.*) —
one present, cap 1 of the allowed 1–3 beats. Later A steps and all of B/C
stay coverage.

**No check on that atom.** Extra `reinforce` would need sibling-atom closed
contrast (verbatim first sentences / sibling steps). Procedure steps are
imperatives; they have sibling sentences but no `{subject} is {complement}`
to invert. Cloze is not sibling contrast. Inventing “which is the first
planning step?” is a new fact. Jake parked a distractor-writer; this hop
does not build it. Present only.

Cartographer still owns intent. Couturier still owns style. Closed vocab
still has no `retrieve`. Idempotent with realize → cartographer → couturier.

**Why:** Spine v1 (previous block / PR #15) was front-matter then checks —
an ID would still not teach *doing* the work. One lead step is that hop
without dumping the SOP.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`.
- Open `realized_lesson.html` — 8 of 50 occurrences (front-matter, Procedure
  A lead, two existing checks). Open `realized_coverage.html` — full dump.
- Manifest `spine.element_ids` gains `ele_sop_ast29080_proc_a_s1` before the
  checks. Store stays 50 `ele_` / 47 atoms.

**Pointer:** a later 2026-08-26 block walks Procedure A as a job sequence
on this spine (still coverage for B/C and the rest of the SOP).

**Supersedes:** the previous spine block’s live path of seven occurrences
and its “Not the 20 procedure steps” as to *zero* procedure atoms on the
path — one lead is now on the path; the dump of the rest stands.
Working-process block untouched. Single-writer per facet stands.

---

## 2026-08-26 — Procedure A as a job sequence on the ALSAP lesson spine

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The short ALSAP lesson now walks **Procedure A’s real steps**
after front-matter and before the existing checks — a job sequence, not a
single notify sentence. Spine membership is still a documented heuristic
(`agents/realizer/spine_v1.md`, policy
`v1_front_matter_procedure_sequence_then_checks`), not fake ID genius and
not an LLM call. Realizer projects a stable sequence of **existing** `ele_`
ids. `atoms.json` unchanged. Store gains **no** extra `ele_`.

**Which atoms, and why.** Object `belongs_to` / `order` already lists
Procedure A’s children. The first branch under the thin `Procedures.`
heading is still A — *Plan Development of ALSAP.* An ID teaching that job
would walk the real A steps, not stop after the GSO notify. The A/B/C
heading atoms are thin (same bar as check siblings). The four non-thin
`procedure_step` children, in `object.order`:

- `atom_sop_ast29080_proc_a_s1` — Notify SDS in QSEG / request an ALSAP Lead
- `atom_sop_ast29080_proc_a_s2` — Collaborate with SMT to identify authors and reviewers
- `atom_sop_ast29080_proc_a_s3` — Schedule and conduct the kick-off within 15 business days
- `atom_sop_ast29080_proc_a_s4` — Confirm section deliverables and target dates

A is a handful (4), under `PROCEDURE_SEQUENCE_CAP = 8`, so all four land
as primary presents. Branches B/C stay coverage.

**No check on those atoms.** Extra `reinforce` would need sibling-atom
closed contrast (verbatim first sentences / sibling steps). Procedure steps
are imperatives; they have sibling sentences but no `{subject} is
{complement}` to invert. Cloze is not sibling contrast. Inventing “which is
the first planning step?” is a new fact. Jake parked a distractor-writer;
this hop does not build it. Present only.

Cartographer still owns intent. Couturier still owns style. Closed vocab
still has no `retrieve`. Idempotent with realize → cartographer → couturier.

**Why:** The previous 2026-08-26 block put one lead present on the spine —
an ID would still not teach *doing Plan Development*. The four A steps are
that hop without dumping B/C or the SOP.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`.
- Open `realized_lesson.html` — 11 of 50 occurrences (front-matter,
  Procedure A sequence, two existing checks). Open
  `realized_coverage.html` — full dump.
- Manifest `spine.element_ids` gains `ele_sop_ast29080_proc_a_s2` /
  `_s3` / `_s4` after s1 and before the checks. Store stays 50 `ele_` /
  47 atoms.

**Pointer:** a later 2026-08-26 block publishes this HTML at a short
public URL (`/cgen/alsap`) via a Netlify rewrite — same projector file,
not a parallel store. Jake tabled that redirect loop; a later block on
the same day pays the atom → primitives hop on this spine.

**Supersedes:** the previous spine block’s live path of eight occurrences
and its “one present, cap 1 / later A steps stay coverage” as to *how much
of A is on the path* — the four real A steps are now on the path; B/C and
the dump of the rest stand. Working-process block untouched. Single-writer
per facet stands.

---

## 2026-08-26 — ALSAP short lesson public URL: `/cgen/alsap`

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The short ALSAP lesson has a first-class public path on the
existing Netlify site (`publish = "."`, live https://trainstorm.ai).
**https://trainstorm.ai/cgen/alsap** (canonical trailing slash
`/cgen/alsap/`) is a **rewrite** of the projector file
`cgen/astellas/projects/ast_alsap/realized_lesson.html`. Coverage is
**https://trainstorm.ai/cgen/alsap/coverage** (same rewrite to
`realized_coverage.html`). There is no third lesson store and no
hand-copied HTML. After `python3 tools/realize.py` → `cartographer.py` →
`couturier.py` from `cgen/trainstorm-core`, that projector file is
current, so the public URL is current.

`/cgen` (Course Engine player) and `/cgen/lumina` (Lumina) are untouched.
`_headers` is untouched: **one site-wide CSP** (PR #6). Do not add a
path-specific CSP for `/cgen/alsap` — Netlify ANDs matching
`Content-Security-Policy` headers and blacks out the page. The existing
`/*` policy already allows the projector’s inline script/style
(`'unsafe-inline'`).

`/cgen` is the player, not a lesson index. No new app shell. Relative
`href`s in the projector stay sibling filenames so local `file://`
browsing still works; the rewrite table aliases those names under
`/cgen/alsap/` plus the short `/coverage` path.

**Why:** After PR #17 the lesson already existed, but only at
`cgen/astellas/projects/ast_alsap/realized_lesson.html`. Jake should be
able to send a short, obvious URL. The pipeline already emits the HTML;
hosting aliases it.

**Consequences:**
- Live: https://trainstorm.ai/cgen/alsap and
  https://trainstorm.ai/cgen/alsap/coverage. Buried projector paths still
  work.
- `netlify.toml` holds the rewrites. Python tools, `atoms.json`, spine
  membership, and facet writers are unchanged this hop.
- No new 1:many. No LLM distractors. No B/C on the spine. No
  distractor-writer agent.

**Supersedes:** nothing about spine membership, identity, or facet
ownership. Adds the public URL those blocks did not have. Working-process
block untouched.

**Pointer:** a later 2026-08-26 block sets `force = true` on these
rewrites so Pretty URLs cannot 301 `/cgen/alsap/` to itself.

---

## 2026-08-26 — `/cgen/alsap/` rewrite must `force = true`

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The ALSAP public rewrite from the previous block stands —
same projector file, same canonical `/cgen/alsap/`, no parallel store —
but every ALSAP `200` (and the one-hop `301`s) in `netlify.toml` now
sets `force = true` (Netlify `_redirects` `200!`). Pretty URLs treat
`/cgen/alsap/` as a directory and 301 it to `/cgen/alsap/` again; an
unforced 200 never wins, which is `ERR_TOO_MANY_REDIRECTS` after PR #18.

Canonical URL stays `/cgen/alsap/` so relative `href="realized_coverage.html"`
still resolves under that prefix. `/cgen/alsap` is still one 301 to the
slash, then a forced 200. Coverage `/cgen/alsap/coverage` is also forced
(production 301’d that path to itself too). `_headers` untouched: one
site-wide CSP. No second CSP. `/cgen` and `/cgen/lumina` untouched.
Python tools and `atoms.json` untouched.

**Why:** Confirmed on production: `GET /cgen/alsap` → 301 `/cgen/alsap/`;
`GET /cgen/alsap/` → 301 `/cgen/alsap/` (self). Buried
`realized_lesson.html` stayed 200.

**Consequences:**
- After merge, Jake opens https://trainstorm.ai/cgen/alsap (at most one
  301 to slash, then 200) and https://trainstorm.ai/cgen/alsap/coverage.
- Do not copy HTML into `cgen/alsap/`. Do not add a path-specific CSP.

**Supersedes:** the previous public-URL block’s unforced `status = 200`
rewrites as to *whether Pretty URLs will honor them*. The public path,
projector file, and “no parallel store” clauses stand. Working-process
block untouched.

---

## 2026-08-26 — Atom → primitives: closed compiler form on the occurrence

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** A real, small **atom → primitives** hop now exists. Realizer
binds a **closed, tiny** compiler vocabulary onto
`element.expression.text_primitive` from atom object-role (`meaning.kind`)
plus occurrence `move`. Keys live in `vocab/primitives.registry.json` v0.4
(`compiler_vocabulary` + `text_primitive`). Spec:
`agents/realizer/primitives_v1.md`, policy `v1_atom_to_primitive`. Not a
design system. Not an LLM call. Not the 11 script-primitive types.

Closed set (five roles):

| Role | Key | Spine use |
|---|---|---|
| heading | `tp_display` (already registered) | title `hook` |
| body | `tp_body` (already registered) | title extra, scope, general |
| step | `tp_step` (this hop) | Procedure A s1–s4 |
| callout | `tp_callout` (this hop) | `activate` — not on the spine |
| check | `tp_recall` (already registered) | the two existing `reinforce` extras |

`tp_purpose` stays as the existing objective look (purpose-frame
front-matter). It is not a sixth compiler role.

**Who owns the hop.** Realizer reads atoms and binds the primitive key on
the occurrence. After Cartographer writes `move`, it asks Realizer to
refresh that key (form depends on move). **Couturier still owns style**
(`style_ref`, `content_role`, `layout_hint`) and preserves `text_primitive`.
A procedure-step primitive is dressed `layout_hint: job_aid`, not `card`.
No authored `content.text`. `atoms.json` unchanged. Store stays 50 `ele_`
/ 47 atoms. Locale packs stay keyed on `atom_id`.

**HTML.** `realized_lesson.html` renders those primitives: Procedure A
s1–s4 as **one numbered job-aid**, front-matter as heading/body, reinforce
as the existing check. Meaning still comes from the atom via
`composed_from`. Coverage dump stays card-like. Spine membership is
unchanged.

**Why:** The course chain worked, but every beat was still atom text
dumped into a styled HTML card. Primitives are the compiler vocabulary so
Couturier/Realizer dress clothes, not SOP sentences.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on all
  three.
- Open `cgen/astellas/projects/ast_alsap/realized_lesson.html` — job aid,
  not four Procedure A cards. Open `realized_coverage.html` — dump still
  card-like.
- Registry `primitives.v0.4`. Manifest stamps `primitives.counts`.
- **Not this hop:** Netlify / `/cgen/alsap` hosting (Jake tabled the
  redirect loop; buried projector path stays the demo URL). No distractor-
  writer. No procedure-step MCQs. No 1:many of the SOP. No Dragoman,
  Storyline, `.potx`, motion, PNG render.

**Supersedes:** the Realizer v1 clause that the `atom → primitives` hop
“remains owed”; STRUCTURE.md’s “first hop of the pipeline has no listed
transform.” Working-process block untouched. Single-writer per facet
stands (Realizer owns `text_primitive`; Couturier owns `style_ref`).

**Pointer:** a later 2026-08-26 block puts `tp_callout` on the spine as
why-this / activate clothes of the purpose atom, and splits authoring
Chameleon from runtime Chameleon in canon.

---

## 2026-08-26 — Authoring Chameleon is in-scope for static artifacts; runtime stays walled

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The Chameleon stub mixed two jobs. They share one facet
contract; they do not share a wake.

**Authoring Chameleon** is in-scope for a **static course**: an assumed
audience, so the course is generated around that impression. It would
write `audience` facets onto **occurrences** (`element.audience`) — not
onto atoms’ meaning, not PII — using the same keys a later engine would
read (`segment_scope`, `difficulty`, `variant_group`). Without LRE the
impression is a documented hypothesis, like Cartographer’s heuristic.
The wake is a content-pipeline write.

**Runtime Chameleon** (wake on a live learner, pick a variant) stays
**Learner Response Engine / frontier**. Do not build it. The wake is a
learner-context event. The facet contract does not change between
halves.

Chameleon does **not** mint `ele_` (Realizer mints). It does **not**
rewrite atom meaning (Headwater owns meaning). It does **not** own
style (Couturier owns `element.expression`). Audience 1:many is
**another occurrence of the same atom**, not a variant SOP and not a
parallel meaning node.

**Do not build the agent this hop.** No `chameleon.py`. No variants of
the SOP. v1, when it happens, is one documented assumed segment on the
ALSAP lesson. The stub (`agents/chameleon/chameleon_STUB.md` and the
system-prompt stub it points at) no longer says “writes nothing / do
not build” for the **authoring** half. Runtime / LRE remains “do not
build.” **No PII — ever.**

**Why:** A static course still needs an assumed audience. Walling
*both* halves because runtime is frontier froze a job the production
pipeline can own. Splitting the wake keeps LRE out of beta without
pretending the facet does not exist.

**Consequences:**
- Canon and the stub record the split. No writer, no live `audience`
  bind, no SOP variants in this hop.
- Working-process block untouched. Single-writer per facet stands.

**Supersedes:** the stub’s blanket “Chameleon writes nothing / do not
build” as applied to the *authoring* half. Runtime / LRE wall stands.
Working-process block untouched.

---

## 2026-08-26 — `tp_callout` on the ALSAP spine: why-this clothes of the purpose atom

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The closed compiler set already had `tp_callout` (clothes
for `activate`) but it was unused on the short lesson. This hop puts
**one callout on the spine** as a real ID beat: learner-facing “why
this / activate” clothes of an **existing** atom.

**Which atom, and why.** Verified against `atoms.json` (not invented
text): `atom_sop_ast29080_purpose` is *The purpose of this SOP is to
define the process for planning, developing, executing, maintaining,
and archiving the ALSAP…* — that is the why-this meaning. The title
atom (`atom_sop_ast29080`) is the SOP name and already wears hook +
present. Do not invent a second purpose sentence.

Realizer mints one extra occurrence,
`ele_sop_ast29080_purpose__activate`, `composed_from` that atom,
Realizer-stamped `move: activate`. Classifier already maps `activate`
→ `tp_callout`. Cartographer preserves the extra’s move and still
binds `teaches` / `rhetorical`. Couturier still owns style
(`brand.prior`, `layout_hint: callout`) and preserves `text_primitive`.
The projector kicker is **Why this**. Meaning from the atom via
`composed_from`. No authored `content.text`. `atoms.json` unchanged.

Spine heuristic (`agents/realizer/spine_v1.md`, policy
`v1_front_matter_callout_procedure_sequence_then_checks`) places that
callout after the title opening and **before** the purpose primary
(objective / `tp_purpose` stays). Then scope, general, Procedure A as
the existing job-aid, then the two existing checks. No procedure-step
MCQ. Store gains **one** extra `ele_` (51 / 47). Purpose is now three
clothes of one atom: activate + objective + reinforce.

Idempotent with realize → cartographer → couturier. Demo remains
`cgen/astellas/projects/ast_alsap/realized_lesson.html`. Hosting /
`/cgen/alsap` stays tabled. Not Chameleon — no `audience` keys written
this hop.

**Why:** PR #20 paid atom → primitives: Procedure A is `tp_step`;
heading/body/check exist; `tp_callout` was in the closed set but unused
on the spine. An ID would put a why-this beat on the path, not leave
the primitive as coverage-only honesty.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three.
- Open `realized_lesson.html` — 12 of 51 occurrences (why-this
  callout of purpose, then the rest of the short path). Open
  `realized_coverage.html` — full dump.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.

**Supersedes:** the previous primitives block’s “callout — `activate`
— not on the spine” as to *spine membership*; the closed set and
classifier stand. Working-process block untouched. Single-writer per
facet stands. Chameleon agent still not stood up.

---

## 2026-08-26 — One worked example on the ALSAP spine from instance atoms

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The short ALSAP lesson now includes **one worked example**
after Procedure A’s job aid and before the existing reinforce checks.
The job aid is how; the instance is that it happened. Meaning comes from
existing instance atoms in `cgen/astellas/projects/alsap_asp9999`
(fictional ASP-9999). No authored `content.text` on the element.
`ast_alsap/atoms.json` is unchanged. Instance atoms are not rewritten
into SOP atoms.

**Which atoms, and why.** Procedure A has **no honest match** in the
instance store. A’s four steps are process acts (notify SDS / request a
Lead; identify authors; kick-off; confirm dates). The ten instance
atoms are filled AST-34037 form values (cover + purpose/safety-profile).
Citing them as Plan Development would invent a fact. They **do**
illustrate the ALSAP generally. Seed of two, not ten
(`agents/realizer/instance_example_v1.md`):

- `atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_profile`
  — `conditional_favorable` (the SMT’s selected BR conclusion)
- `atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale`
  — the authored judgment (hepatic monitoring; names ASP9999)

**How `composed_from` crosses stores.** Realizer mints two guest extras
in the ALSAP occurrence store whose `composed_from` is the instance
`atom_id`. Meaning lookup is a **join catalog** (SOP atoms + sibling
instance store), not a copy into `ast_alsap/atoms.json`. Join is
ALSAP-lesson-only (`project.name == "ast_alsap"`). Cartographer
preserves Realizer-stamped `exemplify` on those extras (an unbound
`instance_value` with no `belongs_to` would otherwise classify as
`hook`). Couturier’s existing map dresses `exemplify` as
`brand.example` / `content_role: example` / `layout_hint: cite`.
Compiler form is already `tp_body` — not a sixth primitive, not another
SOP card.

Spine heuristic (`agents/realizer/spine_v1.md`, policy
`v1_front_matter_callout_procedure_sequence_example_then_checks`) places
those two beats after Procedure A and before the two existing checks.
Store gains **two** extra `ele_` (53 / 47 SOP atoms). Instance store
stays 10 atoms. No procedure-step MCQ. No Chameleon. No `/cgen/alsap`
hosting.

Idempotent with realize → cartographer → couturier.

**Why:** After PR #21 the spine had opening, why-this callout, front-
matter, Procedure A as a job-aid, then checks. An ID would show that
the job happened, from real instance meaning, without dumping the form
or inventing a Procedure A walkthrough the instance store does not
contain.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three.
- Open `realized_lesson.html` — 14 of 53 occurrences (example beats
  after the job aid, before checks). Open `realized_coverage.html` —
  full dump (SOP tree; guest extras in the index).
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.

**Supersedes:** the previous spine block’s live path of twelve
occurrences as to *membership after Procedure A* — two instance-example
beats are now on the path; B/C and the dump of the rest stand. Working-
process block untouched. Single-writer per facet stands. Chameleon
agent still not stood up.

**Pointer:** a later 2026-08-26 block projects a sequence practice of
Procedure A’s four presents after the job aid (projector-only; no extra
`ele_`). The instance example stays `exemplify` after that practice. A
still later 2026-08-26 block puts the two FORM-AST-34037 BR-field
presents those examples fill immediately before this example pair.

---

## 2026-08-26 — Procedure A sequence practice: order the four existing step atoms

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** After the Procedure A job aid, the short ALSAP lesson now
includes an interactive **order/sequence check** of the four existing
Plan Development step atoms. Items are those atoms’ first sentences
(verbatim). Correct order is Cartographer `bindings.object.order` — the
sequence already taught. Not an MCQ stem such as “which is the first
planning step?” (that invents a fact; PR #16 correctly refused it). Not
LLM distractors. Jake parked a distractor-writer; this hop does not
build it. `atoms.json` unchanged. No authored `content.text`.

**Composition choice — mint nothing.** Prefer one extra `ele_` with
`move: reinforce` (closed vocab; do not invent `retrieve`) if that extra
can honestly `composed_from` one atom. Composing from a single A step
is a lie (the check is the four siblings). Composing from the thin A
heading (`atom_sop_ast29080_proc_a`) is also a lie (skipped teaching
card; children’s sentences under a parent `composed_from`). So: **no
new `ele_`.** Project the check from the four existing present records
`ele_sop_ast29080_proc_a_s1` … `_s4` (same honesty as grouping them into
one job-aid). Documented on the occurrence manifest as
`spine.sequence_check`. Store stays **53 / 47**. A-step primaries stay
`present`. Did not stamp `practice` on a fake extra.

**Shape.** New check shape `sequence` in `agents/realizer/check_v1.md`
(alongside invert-definition `mcq_siblings` / `cloze`). Sequence is for
`procedure_step` groups that already have `object.order`. Definition
checks stay as they are. Prompt is task clothes: *Put these in the order
already taught.* Feedback names object.order; it does not invent SOP
facts. Initial display is a stable non-identity permutation so the
learner can be wrong, then right.

**Placement.** After the job aid, before the instance example
(Gagné-ish: practice the steps near the job aid). Instance example stays
`exemplify`. Two existing definition checks stay at the end. Spine
`element_ids` membership is unchanged (14). Coverage dump stays
card-like (no sequence form).

Cartographer still owns intent. Couturier still owns style. Closed vocab
still has no `retrieve`. No chameleon.py. No Headwater outcomes-mode.
No `/cgen/alsap` hosting. No 1:many of the whole SOP. Idempotent with
realize → cartographer → couturier.

**Why:** After PR #22 the spine had a job-aid then an instance example
then definition checks. An ID would let the learner **practice the
order** of the steps just taught, without inventing a planning-step MCQ
or minting a dishonest extra.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three.
- Open `realized_lesson.html` — job aid, then sequence practice, then
  instance example, then the two definition checks. Open
  `realized_coverage.html` — full dump, no sequence form.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.

**Supersedes:** the previous spine blocks’ “no procedure check” as to
*invert-definition MCQ / invented stem* — that refusal stands; a
sequence practice of the four existing presents is now on the path.
Working-process block untouched. Single-writer per facet stands.
Chameleon agent still not stood up.

**Pointer:** a later 2026-08-26 block puts the two FORM-AST-34037 BR-field
presents those instance examples fill after this sequence practice and
before the instance pair.

---

## 2026-08-26 — Form BR-field present before the instance examples

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The short ALSAP lesson now presents the **form fields** the
two ASP-9999 instance examples fill, immediately after Procedure A’s
sequence practice and **before** those instance beats. Here is the field;
here is a filled one. Meaning comes from existing form atoms in
`cgen/astellas/projects/alsap` (FORM-AST-34037). Guest `ele_` records in
the ALSAP occurrence store `composed_from` those form `atom_id`s. No
authored `content.text`. SOP and form `atoms.json` unchanged. Instance
atoms unchanged.

**Which atoms, and why.** The two instance examples already on the spine
`composed_from` instance atoms whose `bindings.instance.instantiates` is
exactly:

- `atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile`
  — *SMT assessment of the overall Benefit-Risk profile of the asset.*
- `atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale`
  — *Rationale and phrasing for the selected Benefit-Risk profile.*

That is a meaning join, not a cousin. Do not stretch `f_br_guidance`
(instructional transient) or the phrasing-example section. If those two
field atoms were missing, stop.

**How `composed_from` crosses stores.** Realizer mints two guest extras
(`…__present`) in the ALSAP occurrence store. Meaning lookup is a join
catalog (SOP + form `alsap` + instance `alsap_asp9999`). Join is
ALSAP-lesson-only. Cartographer preserves Realizer-stamped `present` and
classifies `form_field` as present / specify; empty `teaches` is honest
(not a SOP objective). Couturier dresses `present` as
`brand.instructional` / `content_role: body` / kicker Present. Compiler
form is already `tp_body`. Guest extras do not stamp `structure.parent_id`
at a form-section `ele_` never minted here.

**Placement.** Both form-field presents, then both instance examples —
not interleaved. The two instance beats are already one worked example
(judgment name + reason). Inserting a form-present between them would
split that pair. Gagné-ish: job aid → sequence practice → form BR present
→ instance examples → definition checks. Spine policy
`v1_front_matter_callout_procedure_sequence_form_example_then_checks`.
Store gains **two** extra `ele_` (55 / 47 SOP atoms). Spine membership
16. Not a form dump. No procedure-step MCQ. No chameleon.py. No Headwater
outcomes-mode. No `/cgen/alsap` hosting.

Idempotent with realize → cartographer → couturier.

**Why:** After PR #23 the spine taught Procedure A, then showed filled
FORM-AST-34037 values that do not illustrate A. An ID would show the
field those values fill, from real form meaning, before the filled
example.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three.
- Open `realized_lesson.html` — 16 of 55 occurrences (form BR presents
  after the sequence practice, before the instance examples). Open
  `realized_coverage.html` — full dump (SOP tree; guest extras in the
  index).
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.

**Supersedes:** the previous spine block’s live path of fourteen
occurrences as to *membership after Procedure A* — two form-field
presents are now on the path before the instance pair; B/C and the dump
of the rest stand. Working-process block untouched. Single-writer per
facet stands. Chameleon agent still not stood up.

---

## 2026-08-26 — ALSAP short lesson reads as three scenes (layout chrome)

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The short ALSAP lesson still has the same ~16 spine
occurrences (front-matter, Procedure A job-aid + sequence practice, form
BR presents + ASP-9999 examples, definition/purpose checks). The
projector now wraps those **existing** beats in three named section
headings so the page reads as three scenes, not sixteen stacked cards.
Layout only. Same `composed_from`. `atoms.json` unchanged. No authored
`content.text`. No new `ele_`.

**Scenes (documented heuristic, not an LLM, not outcome language):**

1. **What an ALSAP is** — `front_matter`: document-root opening, why-this
   callout of purpose, teachable front-matter primaries (purpose / scope /
   general). Those atoms are the SOP’s definitional front-matter.
2. **How an ALSAP starts** — `procedure_a`: first Procedures-container
   branch in `object.order` (thin heading *A. Plan Development of ALSAP.*).
   Job-aid presents. Sequence practice stays **in-scene** (it is practice
   of those presents; projector-only, no extra `ele_`).
3. **Benefit-risk on the form** — `form_br`: FORM-AST-34037 BR-field
   presents (Benefit-Risk profile + rationale) plus the instance examples
   that instantiate those fields.

Definition/purpose reinforce extras stay at **lesson end**, not a fourth
scene. Headings are role labels of those clusters, not “will be able to…”
copy. Stamped `spine.scenes` policy `v1_three_scenes_from_roles`.
Membership policy is unchanged
(`v1_front_matter_callout_procedure_sequence_form_example_then_checks`).
Coverage dump stays ungrouped.

Cartographer still owns intent. Couturier still owns occurrence style;
scene chrome is Realizer projector grouping of dressed beats. Store stays
**55 / 47**. Spine membership 16. No chameleon.py. No Headwater
outcomes-mode. No LLM distractors. No `/cgen/alsap` hosting. No Procedure
B. No extra form dump.

Idempotent with realize → cartographer → couturier.

**Why:** After PR #24 the short lesson was a coherent SOP-course seed
(front-matter, Procedure A, form BR, examples, checks) that still *looked*
like sixteen stacked cards. An ID would group those existing beats as
three scenes without adding meaning.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three.
- Open `realized_lesson.html` — three named section headings grouping
  the same 16 occurrences. Open `realized_coverage.html` — full dump,
  no scene chrome.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.

**Supersedes:** nothing about membership, meaning, or clothes. Adds
layout chrome on the existing spine. Working-process block untouched.
Single-writer per facet stands. Chameleon agent still not stood up.

---

## 2026-08-26 — ALSAP short lesson pages one named scene at a time (player chrome)

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The short ALSAP lesson still has the same ~16 spine
occurrences, still grouped as the three named scenes from the previous
block (`v1_three_scenes_from_roles`). The projector now **pages** those
existing sections so `realized_lesson.html` shows **one named scene at a
time**. Next / Back moves between:

1. **What an ALSAP is**
2. **How an ALSAP starts** (Procedure A job-aid + in-scene sequence check)
3. **Benefit-risk on the form** (form presents + instance examples)

Definition/purpose checks stay at **lesson end**, not a fourth scene —
a final player step after Next from scene 3. Same headings (documented
heuristic, not an LLM, not outcome language). Same `composed_from`.
`atoms.json` unchanged. No authored `content.text`. No new `ele_`.
Hash deep-link is optional.

Stamped `spine.scenes.paging` policy `v1_one_scene_at_a_time`.
Membership policy is unchanged
(`v1_front_matter_callout_procedure_sequence_form_example_then_checks`).
Coverage dump stays ungrouped and unpaged.

Cartographer still owns intent. Couturier still owns occurrence style;
player chrome is Realizer projector paging of the existing scene
sections. Store stays **55 / 47**. Spine membership 16. No chameleon.py.
No Headwater outcomes-mode. No LLM distractors. No `/cgen/alsap` hosting.
No Procedure B. No extra form dump. No extra beats.

Idempotent with realize → cartographer → couturier.

**Why:** After PR #25 the short lesson read as three named scenes but
still *scrolled* as one long page. An ID would page those existing
scenes without adding meaning.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three.
- Open `realized_lesson.html` — one named scene at a time; Next/Back;
  sequence check still in scene 2; definition checks after scene 3.
  Open `realized_coverage.html` — full dump, no scene or player chrome.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.

**Supersedes:** nothing about membership, meaning, clothes, or the three
scene headings. Adds player chrome on those existing scenes.
Working-process block untouched. Single-writer per facet stands.
Chameleon agent still not stood up.

---

## 2026-08-26 — Scene 3 BR closed-choice: the fill already shown, from the form field’s value set

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** After scene 3 teaches the FORM-AST-34037 BR profile + rationale
fields and shows the ASP-9999 fills, the short ALSAP lesson now includes
**one honest check** of that profile fill. Options are the verbatim value
**ids** of `reg_benefit_risk_profile` (the form field’s `options_ref`).
Key is the existing instance fill `conditional_favorable` (`selected_value`
= `source_text`). Prompt is task clothes: *Choose the closed value already
shown.* Not “which BR profile is required?” (that invents a fact). Not LLM
distractors. Jake parked a distractor-writer; this hop does not build it.
`atoms.json` unchanged. No authored `content.text`.

**Composition choice — mint nothing.** Prefer one extra `ele_` with
`move: reinforce` if that extra can honestly `composed_from` one atom.
Composing from the instance fill alone hides the options set (it lives on
the form field). Composing from the form field alone hides the key (it
lives on the instance). So: **no new `ele_`.** Project from the two
existing guest records already on the spine (form present + instance
exemplify). Documented as `spine.br_profile_check`. Store stays **55 / 47**.
Spine membership 16. The rationale field is `text_long` with no
`options_ref` — no honest closed set; do not MCQ it.

**Shape.** Check shape `closed_choice` in `agents/realizer/check_v1.md`
(alongside invert-definition `invert_definition` and Procedure A
`sequence_order`). Full governed set, not a cherry-picked pair, not phrasing-
example cousins, not registry description prose. Feedback names the fill
already shown; it does not invent SOP facts. Initial display is a stable
non-identity permutation so the learner can be wrong, then right.

**Placement.** In-scene 3 (Benefit-risk on the form), after the field+
example, before lesson-end definition checks. Paging from PR #26 stays:
three named scenes, one at a time; definition/purpose checks remain the
final player step, not a fourth scene.

Cartographer still owns intent. Couturier still owns style. Closed vocab
still has no `retrieve`. No chameleon.py. No Headwater outcomes-mode.
No `/cgen/alsap` hosting. No Procedure B. No extra form dump. No 1:many
of the SOP. Idempotent with realize → cartographer → couturier.

**Why:** After PR #26 scene 3 taught the fields and showed the fills, then
jumped to lesson-end definition checks. An ID would let the learner
**practice the closed value just shown**, without inventing a BR-profile
MCQ or minting a dishonest extra.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three.
- Open `realized_lesson.html` — scene 3: form BR presents, instance
  examples, then closed-choice; Next still opens lesson-end definition
  checks. Open `realized_coverage.html` — full dump, no closed-choice form.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.

**Supersedes:** the previous spine / scene blocks’ “scene 3 has no elicit”
as to *a closed-choice of the existing fill* — that practice is now
in-scene. The refusal to invent a stem, to write LLM distractors, and to
stretch cousin fields stands. Working-process block untouched.
Single-writer per facet stands. Chameleon agent still not stood up.

---

## 2026-08-27 — Check shapes are first-class on the graph

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The three honest ALSAP check kinds are now a **closed
shape vocab** on the occurrence store / manifest, so a later agent can
emit the same checks without special-casing `realize.py` HTML branches.
No new ALSAP beats. No Procedure B. Spine stays **16** of **55**. Same
paging (`v1_one_scene_at_a_time`). `atoms.json` unchanged. No authored
`content.text`. No new agent. No quiz engine. No LLM distractors.

**Shapes** (`vocab/check-shape.enum.json`):

| Shape | Operands (refs, not copied strings) | Host |
|---|---|---|
| `invert_definition` | `key_atom_id`, `contrast_atom_ids` (sibling first sentences) | Extra `reinforce` `ele_` |
| `sequence_order` | `atom_ids` + `element_ids` of Procedure A presents; `order_from: bindings.object.order` | Projector-only (composing from one atom is a lie) |
| `closed_choice` | `options_ref` (`reg_benefit_risk_profile`), `instance_atom_id` (`selected_value`), `form_atom_id` | Projector-only of the existing form present + instance fill (composing from one atom hides the other half). Options are value **ids**. Prompt is task clothes. |

`ext.check` holds invert-definition host records. `manifest.checks` is the
index (including projector-only `sequence_order` and `closed_choice`).
`spine.sequence_check` and `spine.br_profile_check` remain pointers
(`see: checks`). Projector **reads** the stamped shape and resolves
wording from the graph. It does not re-discover pedagogy by if-atom-id.
Cloze is a **render** of `invert_definition` when `contrast_atom_ids` is
empty — not a fourth shape. Option strings are not copied onto the element.

Cartographer still owns intent (`rhetorical` / `move` / `teaches` /
`intended_response`). Couturier still owns style. Realizer binds the
check shape the way it binds `text_primitive`. Closed pedagogical vocab
still has no `retrieve`. No chameleon.py. No Headwater outcomes-mode.
No `/cgen/alsap` hosting.

Idempotent with realize → cartographer → couturier.

**Why:** After PR #27 the three kinds already existed as Python/HTML
branches (`mcq_siblings` / `sequence` / `derive_br_profile_check` by atom
id). An ID would name them on the graph so the next hop can emit the same
checks from operand refs, while keeping PR #26 paging and PR #27’s
projector-only closed-choice honesty.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three (includes: a check’s operands resolve from the graph, not
  hardcoded HTML).
- Open `realized_lesson.html` — one named scene at a time; wrong then
  right on invert_definition, sequence_order, and closed_choice. Open
  `realized_coverage.html` — full dump; sequence_order and closed_choice
  stay lesson-only.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.

**Supersedes:** the previous check-projection blocks’ “shape is not
written onto the element” as to *storage* — the honesty bar stands;
the shape + operand refs now live on `ext.check` / `manifest.checks`.
Paging and projector-only closed-choice placement from the 2026-08-26
blocks stand. Working-process block untouched. Single-writer per facet
stands. Chameleon agent still not stood up.




