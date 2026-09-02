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

---

## 2026-08-27 — Scene membership and order are first-class on the graph

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Scene membership and order are now **first-class records**
on the occurrence store / manifest, so a later agent can emit a paged
lesson without special-casing `realize.py`. No new ALSAP beats. No
Procedure B. Spine stays **16** of **55**. Same three scenes. Same
paging (`v1_one_scene_at_a_time`). `atoms.json` unchanged. No authored
`content.text`. No new agent.

**Where they live.** `spine.scenes` is the source of truth (ordered scene
objects with `element_ids`), analogous to `manifest.checks`. Closed role
vocab `vocab/scene.enum.json`: `front_matter` / `procedure_a` / `form_br`.
Spec: `agents/realizer/scenes_v1.md`. Policy `v1_scenes_on_graph`
(heuristic `v1_three_scenes_from_roles` unchanged). Member occurrences
carry `ext.scene` (`id` + `role`). In-scene checks are `{shape, see:
checks}` refs into `manifest.checks` — not a parallel pedagogy.
Lesson-end invert-definition extras stay `spine.scenes.lesson_end_checks`,
not a fourth scene.

Title heuristic (closed, not an LLM, not outcome language):

1. **What an ALSAP is** — `front_matter`
2. **How an ALSAP starts** — `procedure_a` (sequence_order in-scene)
3. **Benefit-risk on the form** — `form_br` (closed_choice in-scene)

Projector **reads** that list to wrap and page. It does not re-discover
scenes by hard-coded atom ids. Player chrome is unchanged: one named
scene at a time; Next from scene 3 still opens lesson-end definition
checks.

Cartographer still owns intent. Couturier still owns style. Realizer
binds the scene record the way it binds check shapes. Closed pedagogical
vocab still has no `retrieve`. No chameleon.py. No Headwater
outcomes-mode. No `/cgen/alsap` hosting.

Idempotent with realize → cartographer → couturier.

**Why:** After PR #28 the three check kinds lived on the graph, but
scenes and paging were still projector chrome (three named ALSAP
headings + pager). An ID would name membership on the graph so the next
hop can emit the same paged lesson from ordered `ele_` refs.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. `--selftest` on
  all three (includes: scene operands resolve from the graph, not
  hardcoded HTML).
- Open `realized_lesson.html` — What an ALSAP is → How an ALSAP starts
  → Benefit-risk on the form → lesson-end definition checks. Sequence
  check in scene 2; BR closed-choice in scene 3; invert_definition at
  end. Open `realized_coverage.html` — full dump, no scene wrap.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`;
  check-shape selftests still green.

**Supersedes:** the previous scene / paging blocks’ “layout chrome /
player chrome” as to *storage* — the three headings, the membership,
and the paging UX stand; the records now live on `spine.scenes` /
`ext.scene`. Check-shape storage from the previous 2026-08-27 block
stands. Working-process block untouched. Single-writer per facet
stands. Chameleon agent still not stood up.

---

## 2026-08-27 — The short lesson is a graph object that points at `spine.scenes`

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The ALSAP short lesson is now a **first-class lesson
record** on the occurrence manifest, so a later agent can emit another
lesson by writing a lesson record, not by forking HTML. No new ALSAP
beats. No Procedure B. Spine stays **16** of **55**. Same three scenes.
Same paging (`v1_one_scene_at_a_time`). Same checks. `atoms.json`
unchanged. No authored `content.text`. No new agent. Not a LMS. Not
SCORM. Not a course catalog UI.

**Where it lives.** `manifest.lessons` is the index (analogous to
`manifest.checks` / `spine.scenes`). Spec: `agents/realizer/lesson_v1.md`.
Policy `v1_lesson_on_graph`. Default lesson id `{project}_short` (live:
`ast_alsap_short`). Fields: `lesson_id`, title heuristic + `title_from`
(document-root atom), `scene_ids` refs into `spine.scenes`,
`lesson_end_check_ids`, paging pointer. Lesson records mint **no**
`ele_`. `element.schema.json` already names `Course` / `Module` /
`Scene` as occurrence types — this hop does not mint a `Course`
occurrence (no honest `composed_from` for a container; the document-root
`ele_` is already `type: Course`). Older `cgen/schema/course.schema.json`
is the authored-text course chain, not this constitution.

Title heuristic (closed, not an LLM, not outcome language): the
document-root atom already on the spine.

Projector **reads** the selected lesson (`--lesson` or the default) then
its scenes and checks. It does not hard-code “the ALSAP lesson is these
three headings.” Coverage dump stays a second projection of the store,
not a second lesson node. Extra lesson records are preserved on re-stamp;
only the default is recomputed.

Cartographer still owns intent. Couturier still owns style. Realizer
binds the lesson record the way it binds scenes and check shapes. Closed
pedagogical vocab still has no `retrieve`. No chameleon.py. No Headwater
outcomes-mode. No `/cgen/alsap` hosting.

Idempotent with realize → cartographer → couturier.

**Why:** After PR #29 scene membership lived on the graph, but the
lesson itself was still projector convention (`realize.py` knew this
project). An ID would name the lesson so the next hop can emit another
one from scene refs, while keeping the same 16 beats, three scenes,
pager, and checks.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. Optional
  `--lesson ast_alsap_short`. `--selftest` on all three (includes:
  lesson → scenes → element_ids resolve from the graph, not hardcoded
  HTML).
- Open `realized_lesson.html` — a read of `ast_alsap_short` + its
  scenes + checks. Same pager: What an ALSAP is → How an ALSAP starts
  → Benefit-risk on the form → lesson-end definition checks. Open
  `realized_coverage.html` — full dump, not a second lesson.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`;
  check-shape and scenes selftests still green.

**Supersedes:** the previous scene block’s “projector reads
`spine.scenes`” as to *which object the HTML is* — membership still
lives on `spine.scenes`; the lesson node now points at that list and
the projector reads the lesson. Working-process block untouched.
Single-writer per facet stands. Chameleon agent still not stood up.

---

## 2026-08-27 — A second lesson record proves the lesson node is not a singleton

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The ALSAP occurrence store now holds **two** lesson
records on `manifest.lessons`. Default remains `ast_alsap_short` (all
three `spine.scenes`). Second id `ast_alsap_br` points only at
`benefit_risk_on_the_form` (form presents + instance examples +
in-scene `closed_choice`). Invert-definition extras stay on the short
lesson; they are the definitional close of front-matter, not this form
cluster. Same **55** `ele_` / **47** atoms. No new pedagogy atoms. No
authored `content.text`. No `Course` `ele_`. Not a LMS. Not SCORM. Not
a course catalog UI. Coverage dump stays a dump, not a third lesson.

**Where it lives.** Same contract: `agents/realizer/lesson_v1.md`,
policy `v1_lesson_on_graph`. Extra records are preserved on re-stamp
(realize carries them across a fresh occurrence-manifest rebuild).
Projector reads `--lesson` and writes a sibling HTML **derived from
`lesson_id`** (`ast_alsap_br` → `realized_lesson_br.html`). It does not
fork `realize.py` for ALSAP. A one-scene lesson with empty
`lesson_end_check_ids` keeps paging policy `v1_one_scene_at_a_time`
and **suppresses** Next/Back (single step; nowhere to page).

Title heuristic is still the document-root atom (`title_from`:
`atom_sop_ast29080`). The scene heading stays on the scene record.

Cartographer still owns intent. Couturier still owns style. Closed
pedagogical vocab still has no `retrieve`. No chameleon.py. No
Headwater outcomes-mode. No `/cgen/alsap` hosting. No Procedure B.

Idempotent with realize → cartographer → couturier.

**Why:** PR #30 put one lesson on the graph so a later agent could emit
another by writing a record, not forking HTML. This hop **is** that
later agent. One record would have left “lesson” a singleton in
practice.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. Default lesson
  `ast_alsap_short` → `realized_lesson.html` (pages 1–2–3 then
  lesson-end checks). `python3 tools/realize.py --lesson ast_alsap_br`
  regenerates `realized_lesson_br.html` (one scene, pager disabled).
  A default pass also emits extra lesson HTML. `--selftest` on all
  three (both lesson_ids resolve `scene_ids` from the graph).
- Open `realized_lesson.html` — still the short path. Open
  `realized_lesson_br.html` — BR scene only. Open
  `realized_coverage.html` — full dump, not a third lesson.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`;
  check-shape, scenes, and lesson selftests still green.

**Supersedes:** the previous lesson-on-graph block’s “one default
lesson on this project” as to *how many records* — the default, the
three scenes, and the paging policy stand; a second record now points
at a subset. Working-process block untouched. Single-writer per facet
stands. Chameleon agent still not stood up.

---

## 2026-08-27 — Lesson records are a closed project catalog, not ALSAP branches in `realize.py`

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Lesson records are **project data**. Source of truth is
`occurrences/lessons.json` (closed catalog). Realizer **reads** that
file and stamps the runtime view onto `manifest.lessons`. Adding a
lesson is appending a catalog record (`lesson_id`, `scene_ids`,
optional `lesson_end_check_ids`, optional `paging`). Realize does not
special-case `ast_alsap_br` / `ast_alsap_plan` in Python. No new ALSAP
beats. No Procedure B. Spine stays **16** of **55**. Same 47 atoms.
No authored `content.text`. No `Course` `ele_`. Not a LMS. Not SCORM.
Not a course catalog UI. Coverage dump stays a dump.

**Third lesson.** `ast_alsap_plan` points only at `how_an_alsap_starts`
(Procedure A job-aid + in-scene `sequence_order`). Pager off (single
scene). HTML derived from `lesson_id`: `realized_lesson_plan.html`.
Invert-definition extras stay on `ast_alsap_short`. Default remains
`ast_alsap_short` (pages 1–2–3 then lesson-end). `ast_alsap_br` stays
the form BR scene.

**Where it lives.** Spec still `agents/realizer/lesson_v1.md`. Catalog
policy `v1_lesson_catalog`. Stamped block keeps `v1_lesson_on_graph`.
Title heuristic is still the document-root atom. One-scene records
keep paging policy `v1_one_scene_at_a_time` and suppress Next/Back.
Default pass emits all catalog lessons. `--lesson <id>` regenerates
that file.

Cartographer still owns intent. Couturier still owns style. Closed
pedagogical vocab still has no `retrieve`. No chameleon.py. No
Headwater outcomes-mode. No `/cgen/alsap` hosting. No Procedure B.

Idempotent with realize → cartographer → couturier.

**Why:** PR #31 proved two lessons on one store, but extras still lived
as carry-across on the generated manifest — a later agent still had to
touch `realize.py` or hand-edit a regenerated file. An ID would make
the catalog the write path so the next hop appends JSON.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. Default pass
  emits `realized_lesson.html` (short, pages 1–2–3),
  `realized_lesson_br.html` (scene 3), `realized_lesson_plan.html`
  (scene 2). `python3 tools/realize.py --lesson ast_alsap_plan`
  regenerates that file. `--selftest` on all three (catalog records
  resolve; no extra lesson_id hardcoded in the projector).
- Open `realized_lesson.html` — still the short path. Open
  `realized_lesson_br.html` — BR scene only. Open
  `realized_lesson_plan.html` — Procedure A only. Open
  `realized_coverage.html` — full dump, not a fourth lesson.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`;
  check-shape, scenes, and lesson selftests still green.

**Supersedes:** the previous second-lesson block’s “carry extra records
from the previous stamp” as to *where extras are authored* — they now
live in the catalog; `manifest.lessons` remains the stamped runtime
view; the two existing records, three scenes, and paging policy stand.
Working-process block untouched. Single-writer per facet stands.
Chameleon agent still not stood up.

---

## 2026-08-27 — Scene records are a closed project catalog, not ALSAP headings in `realize.py`

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Scene membership is **project data**. Source of truth is
`occurrences/scenes.json` (closed catalog). Realizer **reads** that
file and stamps the runtime view onto `spine.scenes`. Adding a scene
is appending a catalog record (`id`, title heuristic/ref, ordered
`element_ids`, in-scene checks). Realize does not special-case the
three ALSAP scene headings in Python beyond reading the catalog. Lessons
keep pointing at `scene_ids` only. No new ALSAP beats. No Procedure B.
Spine stays **16** of **55**. Same 47 atoms. Same three scenes. Same
three lessons. No authored `content.text`. No `Scene` `ele_`. Not a
catalog UI. Coverage dump stays a dump.

**Where it lives.** Spec still `agents/realizer/scenes_v1.md`. Catalog
policy `v1_scene_catalog`. Stamped block keeps `v1_scenes_on_graph`.
Grouping heuristic `v1_three_scenes_from_roles` may still **propose** a
default catalog when the file is absent (fixtures / first mint). Live
path is read-the-file. Membership is the list PR #29 already stamped on
`spine.scenes` / `ext.scene` — not a rival grouping. Headings stay the
documented title heuristic, not outcome language. In-scene checks stay
shape refs (`sequence_order` on Procedure A; `closed_choice` on form
BR). Lesson-end invert-definition extras stay `lesson_end_check_ids`,
not a fourth scene.

Default realize → cartographer → couturier emits all catalog lessons.
HTML should feel unchanged: short pages 1–2–3; br and plan single-scene.

Cartographer still owns intent. Couturier still owns style. Closed
pedagogical vocab still has no `retrieve`. No chameleon.py. No
Headwater outcomes-mode. No `/cgen/alsap` hosting. No Procedure B.

Idempotent with realize → cartographer → couturier.

**Why:** PR #32 lifted lessons into a closed catalog, but scenes were
still a spine heuristic inside Realizer (`SCENE_DEFS` / three ALSAP
headings). An ID would make adding a scene an append to JSON, the same
write path as adding a lesson.

**Consequences:**
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default project `cgen/astellas/projects/ast_alsap`. Default pass
  emits `realized_lesson.html` (short, pages 1–2–3),
  `realized_lesson_br.html` (scene 3), `realized_lesson_plan.html`
  (scene 2). `--selftest` on all three (scene catalog `element_ids`
  resolve from the graph; lesson catalog `scene_ids` resolve; no ALSAP
  headings hardcoded on the catalog stamp path).
- Open `realized_lesson.html` — still the short path. Open
  `realized_lesson_br.html` — BR scene only. Open
  `realized_lesson_plan.html` — Procedure A only. Open
  `realized_coverage.html` — full dump, not a fourth lesson.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`;
  check-shape, scenes, and lesson selftests still green.

**Supersedes:** the previous scenes-on-graph block’s “`spine.scenes` is
the source of truth” as to *where membership is authored* — it now
lives in the catalog; `spine.scenes` remains the stamped runtime view;
the three existing scenes, headings, paging policy, and lesson records
stand. Working-process block untouched. Single-writer per facet stands.
Chameleon agent still not stood up.

---

## 2026-08-27 — Course Engine v1 at `/cgen` plays the ALSAP lesson node

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** `/cgen` (Course Engine v1) plays the default occurrence
lesson `ast_alsap_short`. The engine cannot consume
`lessons.json` / `scenes.json` / `elements.json` as-is (it expects
linear scenes of Heading / Body / MCQ). The **minimum adapter** is a
JSON **projection of that lesson node**, rebuilt by `realize.py` as
`realized_lesson.json` (sibling of the HTML sidecar). `/cgen` loads
that file through the existing player chrome. Meaning is still from
atoms via `composed_from`. No authored `content.text` on elements.
Sidecar HTML stays a projector. This is **not** a hand-authored SCORM
package and **not** `cgen/schema/course.schema.json` as a rival
constitution. `/cgen/lumina` is untouched. The tabled `/cgen/alsap`
Netlify rewrite is untouched (not revived). No catalog UI. No
chameleon. No Headwater outcomes-mode. No Procedure B. No new CSP
stacking (PR #6: one site-wide CSP).

**Where it lives.** Same graph walk as the HTML projector: lesson →
`scene_ids` → `element_ids` → atoms; in-scene `sequence_order` and
`closed_choice` plus lesson-end `invert_definition` from
`manifest.checks`. Engine pager steps are the three named scenes plus
lesson-end as a final step (not a fourth named scene on the graph).
Sequence practice needed a `SequenceOrder` component (MCQ would have
been a lie). Job-aid presents are `StepList`. Invert-definition and
closed-choice use existing `MCQ`. `/cgen/src/main.js` fetches
`./astellas/projects/ast_alsap/realized_lesson.json` by default.

Idempotent with realize → cartographer → couturier: sidecars **and**
the JSON `/cgen` reads. `atoms.json` unchanged.

**Why:** Jake was living only in sidecar `realized_lesson.html`. The
Course Engine at `/cgen` already existed (`index.html` + `engine/`)
but `src/main.js` was missing, and `courses/demo/course.json` is a
parallel authored ALSAP, not this graph.

**Consequences:**
- After merge Jake opens **https://trainstorm.ai/cgen** (or `/cgen/`).
  That plays `ast_alsap_short`: three scenes, pager, in-scene sequence
  + closed-choice, lesson-end invert_definition.
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `python3 tools/cartographer.py` then `python3 tools/couturier.py`.
  Default pass still emits HTML sidecars **and** `realized_lesson.json`
  (plus br/plan JSON siblings). `--selftest` covers the projection.
- Gates stay green: `validate_atoms` on ast_alsap / alsap /
  alsap_asp9999; existing selftests; elements vs `element.schema.json`.
- `/cgen/lumina` untouched. `netlify.toml` `/cgen/alsap` rewrite
  untouched (still tabled). `_headers` untouched.

**Supersedes:** nothing about the lesson/scene catalogs, paging, or
check shapes. Working-process block untouched. Single-writer per facet
stands. Chameleon agent still not stood up.

---

## 2026-08-27 — Astellas brand pack is Course Engine player chrome at `/cgen`

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Client brand packs live at `cgen/brands/<client>/` and are
**player chrome** for Course Engine v1 at `/cgen`: tokens, logos,
layout/components CSS, constraints. They are not fused with Couturier
occurrence style. Couturier `style_ref` values (`brand.opening` /
`brand.instructional` / `brand.recall` / …) remain pedagogical **roles**
on `ele_` records (`agents/couturier/style_map_v1.md`). Brand token
resolution is this hop: the player loads `cgen/brands/<theme>/`, not hex
or fonts stamped onto occurrences.

**Which pack.** Source of truth is the **ALSAP project overlay**, not
each occurrence and not a player hardcoded string. The overlay folder
(`cgen/astellas/projects/<proj>`) is already the client axis
(`harness_paths.py`: registry = `project/../..`). Realize copies that
client name onto every lesson JSON projection as `meta.theme` (live:
`"astellas"`). All three catalog lessons share it. `lessons.json` does
not grow a per-lesson brand field. Runtime reads `course.meta.theme`
(aliases `meta.brand` / `meta.client` only as fallback). Deleted the
unused `runtimeConfig.js` hardcoded `astellas` path; graph/projection
meta wins.

**Engine socket.** Loaders stay under `cgen/engine/`. Fetch and
stylesheet hrefs resolve `cgen/brands/<name>/` from `/cgen` and
`/cgen/index.html` (via `import.meta.url` against the engine module).
`#brandLogo` in `cgen/index.html` takes `logos.primary` from
`astellas-brand.json` (`assets/logo-primary.png` relative to the pack).
Engine chrome variables (`--bg` / `--panel` / `--text` / `--brand` /
`--font-body`) alias the pack’s semantic tokens after tokens.css loads
(white/clinical surfaces, Arial, red accent, extra-dark-gray text,
visible focus). Respect `astellas-constraints.md`: calm, no playful UI,
chrome mostly neutral, red for emphasis/active. Do not restyle Lumina.
Do not invent a second CSP. Sidecar HTML keeps stand-in clothes; `/cgen`
is where client chrome lands. Brunswick is a different pack shape; not
this hop.

This is **not** occurrence 1:many. No new `ele_` / `atom_` ids.
Couturier still mints nothing. Single-writer per facet stands.

**Why:** Couturier v1 already wrote role keys and said brand token
resolution (`brands/<client>/`) is later. Course Engine already had
loaders and `applyBrand`, but `meta` had no theme, fetch paths
`../../brands/` 404’d from `/cgen`, and there was no `#brandLogo`.
This hop wires the existing pack into the existing socket.

**Consequences:**
- After `python3 tools/realize.py` → `cartographer.py` →
  `couturier.py` from `cgen/trainstorm-core`, every
  `realized_lesson*.json` carries `meta.theme: "astellas"`.
- After merge Jake opens **https://trainstorm.ai/cgen**: tokens + logo
  from `cgen/brands/astellas/` (no 404); chrome reads as Astellas;
  scenes/checks still play.
- `--selftest` / existing gates stay green. `/cgen/lumina` untouched.
  `netlify.toml` `/cgen/alsap` rewrite untouched (still tabled).
  `_headers` untouched. No catalog UI. No chameleon.py. No Headwater
  outcomes-mode. No LLM distractors. No Procedure B.

**Supersedes:** the style_map clause that brand token resolution is
“later” as to *player chrome at `/cgen`* — occurrence `style_ref` stays
a role; this file’s working-process block is untouched. Single-writer
per facet stands. Chameleon agent still not stood up.

---

## 2026-08-27 — Course Engine resolves Couturier `style_ref` as role classes inside loaded player chrome

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Course Engine v1 at `/cgen` resolves Couturier `style_ref`
on lesson-JSON component `meta` into the same closed role classes the
HTML sidecar already uses (`realize.py` `CLOTHES_CLASS`: `brand.opening`
→ `style-opening`, instructional / recall / purpose / prior / example /
job). Runtime stamps that class on the mounted component (and passes
`meta` in). Unmapped or missing `style_ref`: no class, no invented look.
Roles stay pedagogical. Tokens stay the pack (`cgen/brands/<theme>/`).
Do not stamp hex or fonts onto `ele_` records. Do not fuse client
identity into Couturier. Same Heading / Body / MCQ / StepList /
SequenceOrder / Cloze. No new `ele_` / `atom_` ids. Couturier still
mints nothing. Invert checks copy the occurrence’s existing
`brand.recall` onto engine JSON meta so lesson-end is dressed as
recall; projector-only sequence / closed-choice stay checks without
an invented `style_ref`.

**URL (parked, not this hop).** `/cgen` plus default
`./astellas/projects/ast_alsap/realized_lesson.json` (and the existing
`?course=` escape hatch in `src/main.js`) is a **stand-in loader**.
A future URL names client + course (which pack + which lesson
projection). Not a catalog UI. Do not implement pretty paths, Netlify
rewrites, or revive `/cgen/alsap` (tabled redirect loop).

**Why:** JSON components already carried `meta.style_ref`. The player
dropped `node.meta` in `gotoScene`, so `/cgen` was Astellas chrome
around identical cards. Jake: Couturier = roles, pack = chrome.

**Consequences:**
- After merge Jake opens **https://trainstorm.ai/cgen**: scene 1
  opening / instructional / why-this are visibly different roles
  inside Astellas chrome (logo + white / Arial / red). Scene 2
  sequence and scene 3 closed-choice still play. Lesson-end invert
  is still a check, dressed as recall.
- `style_ref` remains on JSON meta only. Couturier map / `ele_` ids
  unchanged.
- From `cgen/trainstorm-core`: `python3 tools/realize.py` then
  `cartographer.py` then `couturier.py`. `--selftest` / `validate_atoms`
  on ast_alsap / alsap / alsap_asp9999 stay green.
- `/cgen/lumina` untouched. `netlify.toml` `/cgen/alsap` rewrite
  stays tabled. `_headers` untouched. No catalog UI. No chameleon.py.
  No Headwater outcomes-mode. No LLM distractors. No Procedure B.
  Claude remains a co-builder.

**Supersedes:** nothing about pack-as-chrome, lesson catalogs, or
paging. Working-process block untouched. Single-writer per facet
stands. Chameleon agent still not stood up.

---

## 2026-08-27 — Learner-facing check copy is a Realizer projection of graph operands

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Learner-facing check copy at `/cgen` is a **Realizer
projection** of graph operands: task clothes + registry labels in the
disposable Course Engine JSON. The graph stays honest (ids, no LLM, no
invented SOP facts). Compiler vocabulary (`atom`, `ele_`,
`object.order`, sibling store, “closed value set” as jargon) does not
appear in `/cgen`. The element store still holds ids/refs. Projector-only
checks (`sequence_order`, `closed_choice`) may wear recall clothes
(`meta.style_ref: brand.recall`) on the JSON adapter — not by minting an
`ele_`, not by writing `style_ref` onto a present occurrence, not by a
new Couturier map row. Couturier.py / `style_map_v1.md` unchanged.

**What the learner sees.** Invert-definition feedback names the wording
from this definition (may quote the key, which ⊆ the atom); incorrect
says the other options are other sentences from this lesson, not this
definition. Sequence feedback names the order on the job aid already
shown. Closed-choice feedback names the value already shown on the
example. Closed-choice prompt drops “closed” (compiler-speak) and stays
task clothes pointing at the example. Display labels for closed-choice
are the registry `label` for each governed id (`options.registry.json`);
never `description`. Missing label falls back to the id. Submitting
still keys on the id. Sidecar HTML uses the same copy so the two
projectors do not drift.

**Honesty bar, unchanged** (`agents/realizer/check_v1.md`): no LLM
distractors; invert distractors stay sibling first sentences, verbatim;
sequence items stay atom first sentences, order from
`bindings.object.order`; closed-choice options stay governed value ids
on the occurrence / `ext.check`; do not author “Which Benefit-Risk
profile is required?” or “Which is the first planning step?”; do not
invent SOP rules in feedback (“SMT should…”, “the first planning step
is…”).

**Why:** Live `realized_lesson.json` leaked compiler vocabulary into
learner feedback and showed snake_case ids as closed-choice text.
Invert checks already wore `brand.recall`; projector-only sequence and
closed-choice sat undressed next to them. Labels already existed on the
governed registry; copying them onto the element would have been a
second meaning store.

**Consequences:**
- After `python3 tools/realize.py` → `cartographer.py` →
  `couturier.py` from `cgen/trainstorm-core`, `/cgen` closed-choice
  shows labels such as “Conditional Favorable Benefit-Risk Profile”;
  sequence and invert feedback are learner-facing; scene 2/3 practice
  blocks wear `style-recall`.
- `--selftest` / `validate_atoms` on ast_alsap / alsap / alsap_asp9999
  stay green. No authored `content.text` on elements.
- `/cgen/lumina` untouched. Pretty client/course URLs parked.
  `netlify.toml` `/cgen/alsap` rewrite stays tabled. No chameleon.py.
  No Headwater outcomes-mode. No Procedure B. No LLM distractors.
  Claude remains a co-builder.

**Supersedes:** the check_v1 clauses that feedback “names object.order”
or “the field’s closed set” as learner-visible copy, and the #36 clause
that projector-only sequence / closed-choice stay undressed. Graph
operands, ids on the element store, and the honesty bar stand.
Working-process block untouched. Single-writer per facet stands.


## 2026-08-28 — Instance fills that are governed option ids get the same Realizer label projection as closed-choice

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** When Realizer projects an `exemplify` / instance-fill body
whose `meaning.source_text` equals a `selected_value` id that is a
member of the form field’s `options_ref` set (`options.registry.json`,
already on the check/form graph), learner-visible text is the registry
**`label`**. Same helper as closed-choice (`option_value_label` in
`realize.py`). Never `description`. Missing label falls back to the id
(honest). The graph keeps the id: atom `source_text` / `selected_value`
stay `conditional_favorable`; no authored `content.text` on the element;
no label stamped onto `ele_`. Sidecar HTML uses the same projection so
the two projectors do not drift.

The example body stays the fill, dressed. Do not invent a sentence
(“ASP-9999 has a Conditional Favorable profile”, “SMT should select…”).
If context is needed, use kickers/meta already on the graph. The
rationale beat is `text_long` with no `options_ref` — leave that prose
atom. Closed-choice still keys on the governed id.

**Why:** After #37, scene 3’s check showed “Conditional Favorable
Benefit-Risk Profile” while the Example body above it still spoke
`conditional_favorable`. Same leftover: the fill is a governed option
id; the projector copied the id instead of the registry label.

**Honesty bar, unchanged:** no LLM; no new distractors; no pretty URLs;
no `/cgen/alsap` rewrite; no Lumina / Brunswick / chameleon / Procedure
B / Headwater outcomes-mode. Couturier map unchanged. Do not weaken
`check_v1`. `validate_atoms` on ast_alsap / alsap / alsap_asp9999 stays
green. Rebuild with realize → cartographer → couturier.

**Consequences:**
- After `python3 tools/realize.py` → `cartographer.py` →
  `couturier.py` from `cgen/trainstorm-core`, scene 3’s example body
  shows “Conditional Favorable Benefit-Risk Profile”; the closed-choice
  still keys on `conditional_favorable`; rationale example stays the
  prose atom.
- `--selftest` on realize / cartographer / couturier stays green.
- Claude remains a co-builder.

**Supersedes:** the #37 note that the EXAMPLE body still shows the
instance atom’s `source_text` (`conditional_favorable`) as learner-
visible copy. Graph operands, ids on the element store, closed-choice
keying on the id, and the honesty bar stand. Working-process block
untouched.

---

## 2026-08-29 — Short-lesson scene 1 includes the children “listed below”

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The short-lesson front-matter scene (`what_an_alsap_is`)
includes the in-scope org children and the governance-doc children
because those presents already say “listed below.” Thin list-container
headings stay skipped. Membership is the scene catalog
(`occurrences/scenes.json`). The projector groups consecutive
`list_item` siblings as lists (one org list under the scope body; one
doc list under the general body), the same way consecutive `tp_step`
presents are already one StepList. No new `ele_` / `atom_` ids. No new
check. No new Couturier map row. Kickers are one list label each (scope
list / the documents listed), not stacked Present cards. Verbatim atom
text. No Procedure B/C. Claude remains a co-builder.

**Why:** Scene 1 said the organizations and the governance documents
were listed below, then showed an empty page. The child atoms and
occurrences already existed. Catalog append is the membership source;
realize.py does not fork a hardcoded ALSAP id list.

**Consequences:**
- After `python3 tools/realize.py` → `cartographer.py` →
  `couturier.py` from `cgen/trainstorm-core`, `/cgen` scene 1 shows
  six org names as one list after scope and four governance docs as
  one list after general. Still three named scenes + lesson-end
  checks.
- `--selftest` / `validate_atoms` on ast_alsap / alsap / alsap_asp9999
  stay green. Coverage dump keeps the rest.
- `/cgen/lumina` untouched. Pretty URLs parked. `netlify.toml`
  `/cgen/alsap` rewrite stays tabled. No chameleon.py. No Headwater
  outcomes-mode. No LLM. Working-process block untouched.

**Supersedes:** the spine / scene clauses that front-matter is purpose /
scope / general **only**, and that lists / govdocs stay coverage-only
even when a present already names them. Heuristic spine without a
catalog still skips those descendants. Single-writer per facet stands.

---

## 2026-08-29 — Course Engine caption/voiceover chrome follows the lesson projection

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Course Engine chrome for captions and voiceover (`#ccToggle`
and the footer `<audio>`) is shown only when the loaded lesson projection
has voiceover (or captions/tracks) on a scene. `/cgen` ALSAP
(`realized_lesson.json`) has none, so CC and the empty audio bar are
hidden. The player is brand header + scene pager + stage. Runtime
audio/CC wiring stays; a future lesson with `scene.voiceover` shows the
chrome again. Read from the course JSON — not an ALSAP special-case.
Document `<title>` becomes the lesson title once the course loads
(fallback remains generic). Sidecar HTML stays a projector (no fake
audio bar). Claude remains a co-builder.

**Why:** The ALSAP short lesson at `/cgen` was wearing unused Course
Engine chrome: a CC button and an empty audio footer that do nothing
because scenes have no voiceover. That leftover was the loudest
unfinished thing on the stakeholder URL.

**Consequences:**
- After merge, https://trainstorm.ai/cgen has no CC button and no empty
  audio bar. Logo, title, prev/next, progress, scenes, and checks
  unchanged.
- `engine/runtime.js` still loads voiceover and toggles captions when a
  scene has them. Do not delete that wiring.
- Working-process block untouched. No pretty client/course URLs.
  `/cgen/alsap` stays tabled. No Procedure B/C. No new scenes, checks,
  `ele_` / `atom_` ids. No Lumina/Brunswick/chameleon. No new CSP.

**Supersedes:** nothing about lesson catalogs, brand packs, Couturier
roles, or check surfaces. Player chrome visibility is projection-driven.

---

## 2026-08-30 — `/cgen` plays a lesson catalog id (`?lesson=`)

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Course Engine v1 at `/cgen` plays a **lesson catalog id**,
not one hardcoded JSON file. `?lesson=<lesson_id>` selects a record on
the existing project catalog (`occurrences/lessons.json`). No param
uses that file’s `default` (`ast_alsap_short`). The player resolves
the Course Engine JSON from the record’s **`projection`** field
(existing realize names: `realized_lesson.json`,
`realized_lesson_br.json`, `realized_lesson_plan.json`). Realize
stamps `projection` onto `manifest.lessons`. Unknown id fails in the
stage; it does not silently fall back to short. `?course=` stays the
raw-path escape hatch (wins if both are set).

**URL (still later).** `?lesson=` is the stand-in for a future URL
that names client + course (which pack + which lesson). This hop is
which lesson projection loads, not the pretty path. No catalog UI.
No `?client=`. Do not implement `/cgen/{client}/{course}` or revive
`/cgen/alsap` (tabled redirect loop).

**Why:** Jake: this early ALSAP version has gone deep enough. The
short course is one catalog record, not the player. `/cgen` was still
hardcoded to `realized_lesson.json`. The catalog already had the three
lessons; the player needed to read them.

**Consequences:**
- After merge, https://trainstorm.ai/cgen still plays the short
  course (three scenes + lesson-end).
- `?lesson=ast_alsap_br` plays BR-only (scene 3 + closed-choice).
- `?lesson=ast_alsap_plan` plays Procedure A only.
- A bad id names the unknown id and the catalog’s ids; it does not
  load short by accident.
- No Procedure B. No more scene-1 content. No more clothes. Hide-VO
  chrome untouched. Claude remains a co-builder.

**Supersedes:** the stand-in that `/cgen` fetches
`./astellas/projects/ast_alsap/realized_lesson.json` as *the* player
path. The catalog, realize naming, brand chrome, Couturier roles, and
check surfaces stand. Pretty client/course URL still later.
Working-process block untouched. Single-writer per facet stands.

---

## 2026-08-30 — Second SOP through the Manifold pipe: `ast_artwork` (SOP-2290 working id)

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.* Claude remains a co-builder.

**Decision:** A second Astellas SOP rides the existing Manifold pipe as its
own project store — not a second player, not a rewrite of ALSAP, and not
ISO 14971. Project slug **`ast_artwork`**. Working document id **SOP-2290**
(current; supersedes SOP-2290 v 4.0). The Vault export used for this hop
does **not** print its own SOP number on the face (common). That gap is
named in the ingest corpus string, `proposed_registry_extensions.json`,
and this block — the working id is not pretended to be a printed face
number.

Headwater ingest is **authored decomposition**
(`tools/headwater_ingest_artwork.py`). `tools/headwater_ingest.py` stays
ALSAP-hardcoded. Do not overwrite it. Controlled HTML is a sibling
projector (`tools/project_sop_artwork.py`).

`/cgen` default catalog stays ALSAP short. `?project=ast_artwork` loads
`cgen/astellas/projects/ast_artwork/occurrences/lessons.json` (default
short). `?lesson=` still selects a record inside the selected catalog.
No pretty-URL, no Netlify rewrite, no catalog UI. Astellas brand pack
from overlay (`meta.theme` astellas). Hide-VO chrome still applies.

**Short course (SOP-course mode):** front-matter (title, four purpose
bullets as one list, scope who / products / out-of-scope
dispatch/shipment of PPC) + Procedure A as one job-aid of the ACM
actions in `object.order` + projector-only `sequence_order` of those
steps. Intro line from the SOP: “For new artwork start with Section A.
For existing artwork start with Section C.” No FORM-AST instance scene
(this SOP has no honest closed form fill). Lesson-end invert-definition
of BLUE only (copula). Coverage dump keeps B–L `procedure_step` atoms so
the graph is not a stub. Thin headings stay thin. Roles table is a
Headwater note — actors are not in the governed `roles.registry`; this
is not a taught RACI course.

Ungoverned roles (ACM, RA Representative, LMG EU, Manufacturing Plant,
SPD, Affiliate) and document numbers not in `docs.registry` are
**proposed** in `proposed_registry_extensions.json` — not silently added
to governed registries. Verbatim `meaning.source_text`. No paraphrased
SOP rules. No LLM distractors. No invented “which is the first BLUE
task?”

Realize / cartographer: a second project does not inherit ALSAP 1:many
seed ids, `obj_explain_alsap_*`, or form/instance guests.
`procedure_sequence_atoms` skips intro children under Procedures and
takes the first branch that has non-thin `procedure_step` children
(ALSAP A is still first-with-steps). `first_sentence` / `list_item_display`
do not treat `e.g.` / `i.e.` as a sentence boundary (purpose bullet 1 is
one sentence). ALSAP atoms / scenes untouched except the player loader.

**Why:** Jake: second SOP through the existing pipe, the same way ALSAP
is already in it. WEB_trainstorm is public. Claude is a co-builder — do
not freeze them out.

**Consequences:**
- After merge, https://trainstorm.ai/cgen still plays ALSAP short.
- `?project=ast_artwork` plays the artwork short lesson in Astellas chrome.
- `?lesson=` still works inside the selected catalog. Unknown project or
  lesson fails in the stage; it does not fall back to ALSAP short.
- ALSAP `atoms.json` / `occurrences/scenes.json` unchanged.
- Working-process block untouched. No pretty client/course URLs.
  `/cgen/alsap` stays tabled. No ISO 14971.

**Supersedes:** nothing about ALSAP lesson catalogs, hide-VO chrome, or
the `?lesson=` stand-in. Adds `?project=` as a sibling catalog stand-in.
Pretty client/course URL still later.

---

## 2026-08-30 — STRUCTURE score: course-half hops since 2026-08-26 vs `cgen/` vestiges

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Score this checkout against `cgen/trainstorm-core` (the
essential structure), not the wider `cgen/` accretion. Update
`STRUCTURE.md` (tree + First moves; reconciled 2026-08-30). This is a
**log refresh**, not new product. Working-process block untouched.
Claude remains a co-builder.

**On this main (2026-08-30, hop start):** no `ast_artwork` project;
`cgen/src/lessonCatalog.js` is ALSAP-only (`?lesson=`, no `?project=`);
PR #42 is still Draft. That hop-start snapshot was a raw.githubusercontent
read still at #41. **Same-day correction below:** #42 merged (`f9642bc`
and later). Artwork **store and** `?project=` loader are on main.

**Course half landed after the 2026-08-26 first-moves** (mark ✅; cite
the dated blocks already in this file):

- Check shapes on the graph — 2026-08-27
  (`invert_definition` / `sequence_order` / `closed_choice`)
- Scenes catalog + one-scene pager — 2026-08-26 / 2026-08-27
- Lesson as a graph object + `occurrences/lessons.json` — 2026-08-27
- `/cgen` Course Engine reads `realized_lesson.json` — 2026-08-27;
  catalog `?lesson=` — 2026-08-30; catalog `?project=` stand-in — 2026-08-30
  via #42 (`DEFAULT_PROJECT` / `catalogUrlForProject`; live
  `/cgen/?project=ast_artwork` plays SOP-2290; `/cgen` stays ALSAP)
- Astellas brand pack as **player chrome** — 2026-08-27
  (`cgen/brands/`, `meta.theme`); Couturier `style_ref` stays
  pedagogical roles
- Learner-facing check copy + registry **labels** — 2026-08-27
- Instance example fill shows registry labels — 2026-08-28
- ALSAP scene 1 in-scope org + governance-doc lists — 2026-08-29
- Hide unused CC/audio unless the lesson has voiceover — 2026-08-29

Document half was already green. Identity 1:many, primitives hop,
Procedure A job-aid + sequence, form BR present, ASP-9999 example:
already decided — do not re-litigate.

**Vestiges (not remaining core work):** `cgen/lumina`; tabled
`/cgen/alsap` rewrite; zips (`layout-engine.zip`,
`manifold_bundle_copilot_aug626.zip`, `trainstorm-core.zip`); `.lnk` /
`desktop.ini`; `README-START-HERE.md` (2026-07-31 drop note);
`trainstorm-core/README.md` locales text (misfiled);
`project/ast_alsap/review_matrix.csv` (already flagged);
`cgen/schema/course.schema.json` is not a rival constitution.
Layout-engine potx/sidecars stay a parallel expression path, not the
live `/cgen` HTML player. Do not delete those files in this hop.

**Specified, still open:** `reference/brunswick.reference.course.json`
still `{"_todo"}` (proof of the course half end-to-end);
`tools/render/` PNG; Dragoman / `locales/`;
`vocab/primitives.registry.json` partial; `registry/templates/`;
visual-asset track; `ingest-decompose/` retire or merge; ontology
goals/objectives still `status: example`.

**Parked / walled — not next hops:** runtime Chameleon / LRE /
Responsive Engine; Headwater outcomes-mode; LLM distractor-writer;
pretty `/cgen/{client}/{course}` URLs; `/cgen/alsap` rewrite;
slide-authoring frontend; ingest UI on the static Netlify site;
ISO 14971; Procedure B on ALSAP; Generator's divergent distractors;
Strategist / Designer / Audience as live agents. Authoring Chameleon
stays a contract; no `chameleon.py`.

**Why:** First moves still read as if the course half had only reached
Realizer / Cartographer / Couturier v1. The hops after 2026-08-26 are
on main and already have dated blocks here. Scoring them in
`STRUCTURE.md` keeps the tree honest without opening new product.

**Consequences:**
- `STRUCTURE.md` First moves 1–6 stay done; post-26 hops marked done;
  item 7 brunswick gold course stays open.
- Assistants name remaining specified-open work; they do not treat
  vestiges or parked walls as next hops.
- No agent-prompt or tools rewrite. No zip cleanup.

**Supersedes:** the 2026-08-20 STRUCTURE reconciliation date and any
reading that the post-2026-08-26 course-half hops are still First
moves. Those hops' own blocks stand. Working-process block untouched.
Single-writer per facet stands.

---

## 2026-08-30 — Artwork store **and** `?project=` loader are on main via #42

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** PR #42 merged onto origin (`f9642bc` and later). On main:

- **Store:** `cgen/astellas/projects/ast_artwork/` and
  `tools/headwater_ingest_artwork.py` (sibling projector
  `tools/project_sop_artwork.py`).
- **Loader:** `cgen/src/lessonCatalog.js` has `DEFAULT_PROJECT`,
  `catalogUrlForProject`, `unknownProjectMessage`; `cgen/src/main.js`
  selects the catalog from `?project=`. Live
  `https://trainstorm.ai/cgen/?project=ast_artwork` plays SOP-2290;
  `/cgen` stays ALSAP.

A separate loader restore PR was **not** needed and was **not**
opened. Strike “until the loader PR lands” / “do not claim `?project=`
plays.” Those sentences were false: an earlier
raw.githubusercontent.com read was still at #41.

Log refresh only. Working-process block untouched. Claude remains a
co-builder.

**Why:** The STRUCTURE score hop started against a #41 snapshot. Jake
merged #42 the same day. The #42 consequence that `?project=` plays
is the live fact.

**Consequences:**
- `STRUCTURE.md` names the artwork store **and** the `?project=`
  stand-in as on main.
- Assistants may write that `/cgen/?project=ast_artwork` plays SOP-2290.
- No product on this hop. No loader rewrite.

**Supersedes:** the hop-start snapshot that artwork / `?project=` were
only on PR #42 Draft, and the earlier same-day log line that a loader
PR was still required. The #42 store-and-loader decision (second SOP
through the pipe; sibling ingest; not ISO 14971) stands.
Working-process block untouched.

---

## 2026-08-30 — Two dormant gates repaired; sidecar brought under the governed vocabularies; `_schema/` copies removed

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** `tools/lint.py` and `layout-engine/ci/validate_sidecar.py` are live gates again.
`lint.py` classifies atom stores (deferred to `validate_atoms.py`), element stores (schema-checked
against `element.schema.json`) and scripts (v1, or v2 when a v2-only field is present) instead of
treating every JSON array as a script. `validate_sidecar.py` auto-detects the enclosing
`trainstorm-core` instead of a pre-move relative path. The Astellas awareness sidecar conforms to
canon: repeat sources select `Bullet` (the governed element type), and the selection rule that fired
on an ungoverned `script_primitive: scenario` is removed — the governed `requested_interaction:
scenario_select` rule already routes that layout. `layout-engine/_schema/` is deleted; the two schemas
have one home in `schemas/`.

**Why:** Both gates were marked ✅ and could not execute against the current repo (254 false errors;
a crash on a path that no longer exists). A gate nobody can run is a claim. The three violations the
repaired gate found are all "a data file invented a value" — the exact class the govern-the-
vocabularies invariant exists to catch, resolved by conforming the data, not by widening canon.

**Consequences:**
- `python3 tools/lint.py reference schemas vocab ontology ../astellas` → 0 errors, and goes red on
  negative controls. `python3 layout-engine/ci/validate_sidecar.py layout-engine/sidecars/<x>.json`
  → OK with no flags.
- **Open, not decided here:** whether a 12th script primitive `scenario` (branching decision)
  should exist. If yes, it is a `script.primitives` version bump plus a sidecar rule — in that order.
- **Prose drift to fix on the next Project re-sync:** `project/custom_instructions.md` and the Claude
  Project instructions say "`ListItem`"; the governed spelling is `Bullet` (element type) over a
  `list_item` atom kind. One line.
- `STRUCTURE.md` gains a `layout-engine/` entry and corrected markers for both tools.

**Supersedes:** the `STRUCTURE.md` ✅ on `lint.py` as it stood 2026-08-30 (a marker on a tool that
could not run). Nothing in the working-process block. Single-writer per facet, one home per schema,
govern the vocabularies — all stand and are what this enforces.

---

## 2026-08-31 — Brunswick paytrans drive, hop one: structure.v0.2 (document/section/statement), the brunswick namespace, and the drafted warrant chain

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** The full-course drive runs on the real Brunswick pay-transparency corpus; its
validated projection will become `reference/brunswick.reference.course` (no hand-authored reference).
Employee awareness course first; manager course is drive two on the same store. To carry an
expository corpus, `vocab/structure.enum.json` bumps to **v0.2** adding `document`, `section`,
`statement` — the didactic duals of the procedural kinds. `cgen/brunswick/` is the second client
namespace (registries seeded v1 at creation: 8 docs, 5 roles; growth by propose→adopt).
`tools/headwater_ingest_paytrans.py` authors 68 atoms (meaning + object only; no source-type facet,
legal under the at-most-one rule). `ontology/goals.json` v3 adds `goal_bw_pay_understood` and
`ontology/objectives.json` v4 adds five `obj_bw_emp_*` nodes verbatim from the client-ready LO
document — **all draft**: merging ratifies them as BPS's working draft, and the objective-lock
conversation (hop two) is where Jake promotes them. The Jan-2026 proto-agent prompts are recorded
as lineage (`architecture/lineage/`), with the exploratory-phase agent seat named as the roster's
one structural absence — parked, not opened.

**Why:** The course half has run only on SOP walks. A course-shaped proof needs a real corpus, a
real warrant, and a control — this corpus supplies all three (Jake hand-built the same course in
January). The vocab bump is the governed path for the first new content family since forms.

**Consequences:**
- `python3 tools/headwater_ingest_paytrans.py` regenerates the store idempotently;
  `validate_atoms --project ../brunswick/projects/paytrans` PASS/PASS; `validate_objectives` ALL PASS.
- Manager-course sources and the FAQ jurisdiction table are registered, not decomposed (named
  Headwater notes). The ten manager LOs stay unminted until drive two.
- Realize/cartographer/couturier are NOT run on this store yet — hop three, after objective lock.
- Open carry restated: instances still live in the core ontology seed (no per-project ontology
  store); this drive will press on that and it should be decided deliberately, not drifted into.

**Supersedes:** the July intent that `brunswick.reference.course.json` be authored as a standalone
worked example — it will be produced by the pipe or not at all. Nothing else; single-writer,
one-home-per-schema, and the working-process block stand.

---

## 2026-08-31 — Objective lock: the Brunswick warrant chain is `validated`

**Signed:** Jake / Claude — *Jake ratified in conversation; merge makes it durable.*

**Decision:** `goal_bw_pay_understood` and the five `obj_bw_emp_*` nodes are `validated` (goals v4,
objectives v5) — the ontology's first validated nodes. `validated` here means the warrant holds for
building the employee-awareness course; Brunswick client sign-off is a separate, later event,
recorded when it happens. The promotion gate (serves required at validated) now guards live nodes
and was proven to go red in the same session.

**Why:** Hop two of the paytrans drive. Building a course on an unratified warrant would make the
whole chain decorative.

**Consequences:** Hop three may bind `teaches` against validated objectives. The ten manager LOs
remain unminted (drive two). Amending any of the six now means a new dated entry and a version
bump, not an edit.

**Supersedes:** the draft status of those six nodes. Nothing else.

---

## 2026-08-31 — Hop three: the employee course plays from the graph; heuristic v2; scene.v2 `topic`

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** The Brunswick employee-awareness course exists as project data + pipeline output:
five authored scenes (`scenes.json`), an authored lesson record with designer title
(`lessons.json`), two reinforce extras (`one_to_many_seed.json`), and designer objective bindings
in the NEW `occurrences/intent_map.json` (Cartographer heuristic v2 — validated project-data input;
Cartographer stays the intent facet's single writer; at most one hook election). `scene.enum` v2
adds the `topic` role. `kind document → present/low` (a multi-root corpus's opening is course
design); `kind statement → present/assert`. Two lesson-end invert-definition checks from the only
two honest copulas; colon-form definitions deliberately unseeded. A realize selftest that pinned
the scene-role list was repaired to assert the rule (third recurrence of the 08-20 rot).

**Why:** First expository corpus through the course half. The two ALSAP-hardcoded assumptions it
broke (single root; Python teaches walk) are retired the same way scenes and lessons were on
08-27: as closed project data, not code branches.

**Consequences:**
- `realize → cartographer → couturier --project ../brunswick/projects/paytrans` regenerates
  everything; all gates and selftests green; ast_alsap and ast_artwork regenerate **byte-identical**
  (no intent_map = v1 behavior).
- `realized_lesson.json` carries `meta.theme: brunswick`; `/cgen?project=paytrans` becomes playable
  the moment this lands (hop four verifies live).
- Scene/lesson/membership/title remain redraftable in Jake's review before the reference-course
  ratification (hop five).

**Supersedes:** the realize selftest's pinned three-role list; `bind_teaches`'s ALSAP-only reach as
the ONLY teaches path (the hardcoded walk still runs for ast_alsap, unchanged). Single-writer per
facet, catalogs-as-project-data, and the working-process block stand.

---

## 2026-08-31 — `?project=` accepts a client-qualified ref (`brunswick/paytrans`)

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** `catalogUrlForProject` resolves `<client>/<slug>` to
`cgen/<client>/projects/<slug>/occurrences/lessons.json`; a bare slug still means astellas, so
existing URLs are unchanged. Unsafe refs (extra segments, traversal) resolve to "" and fail in the
stage. Not a client registry; not a catalog UI; no pretty URLs (still tabled).

**Why:** The loader baked `./astellas/` into the path — true while astellas was the only client,
an assumption once `cgen/brunswick` landed. The URL now names the store the way the tree does.

**Consequences:** `/cgen/?project=brunswick/paytrans` plays the employee course in Brunswick
chrome (`meta.theme` from the projection; pack at `cgen/brands/brunswick/`). `/cgen` stays ALSAP.

**Supersedes:** the astellas-only path rule inside `catalogUrlForProject`; the #42 block's
`?project=` stand-in otherwise stands.

---

## 2026-08-31 — Brunswick pack conforms to the Course Engine pack contract

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** `cgen/brands/brunswick/` gains the four contract files the engine loads
(`brunswick-brand.json`, `brunswick-{tokens,layout,components}.css`), on the same semantic variable
contract as the astellas pack. The January `brand.json` / `brunswick.css` remain as the distillation
source. Non-brand status colors are flagged in-file, not invented. Layout/components are copies of
the astellas files (brand spots swapped) — a shared engine base layer is a NAMED CARRY, and until it
exists component/layout edits go to both packs.

**Why:** The pack predates the contract; `?project=brunswick/paytrans` played unbranded because the
loader's 404 fallback is silent. Conform the data, don't teach the loader legacy names.

**Consequences:** `/cgen/?project=brunswick/paytrans` plays in Brunswick chrome (verified headless
against this branch). Carries: engine base stylesheet; a visible dev notice on brand-load fallback.

**Supersedes:** nothing — the astellas pack layout is confirmed as the pack contract of record.

---

## 2026-08-31 — `brunswick.reference.course` v1 ratified (structural); voice pack is the next build

**Signed:** Jake / Claude — *Jake ratified in conversation; merge makes it durable.*

**Decision:** `reference/brunswick.reference.course.json` is a ratified POINTER record naming the
paytrans employee course as the gold worked course — v1 structural scope (corpus→atoms→warrant→
catalogs→occurrences→branded player, all gated). The July `_todo` is closed by the pipe. Named v2
scope, in build order: voice pack (learner-register rendering store keyed by element id — the next
build), Griot narration, authored arc, player expression; motion and Storyline stay parked. The
projection is never copied into reference/ — the pointer IS the reference.

**Why:** The reference exists to prove the machine's shape on a real course, which v1 does; the
artisan side-by-side (decision-log, hop five) shows every remaining gap has an architectural home.

**Consequences:** Assistants may cite the paytrans store as the worked course example. The voice
pack arc opens next with its own design pass; its store decision (pack shape, writer, review gate)
is made there, not assumed here.

**Supersedes:** the `_todo` stub and the July intent of a hand-dropped gold course file. The
2026-08-31 hop-one clause "produced by the pipe or not at all" is fulfilled, not changed.

---

## 2026-08-31 — Voice-pack contract: Dragoman voice MODE, two pins, register.v0.1

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** The voice pack's design, landed in the 2026-08-31 design conversation and built as
contract-before-writer:

- **The writer is a Dragoman MODE, not a new agent** (Jake's call). Dragoman owns the
  meaning-rendering space; language and register are coordinates. Precedent: Dragoman already has
  a mode (`reconcile`), and single-writer is proven at key granularity (Couturier/Dragoman split).
  Payoff: locale × register composition ordering is one seat's internal concern, never inter-agent
  coordination. The strain, handled by contract: the modes differ in LICENSE (translation ≈
  fidelity; voice = real authorship) and their failure modes invert (a failing translator garbles,
  a failing copywriter INVENTS) — therefore **each mode declares its own gate profile**, and mode
  reuse must never import translation's leniency into voice.
- **Two pins.** The atom anchors meaning, always: every rendering at every coordinate is gated
  against the atom's `content_hash`, never transitively. The writer works from the accepted voice
  rendering where one exists (localization localizes the EXPRESSION, judged against the ATOM),
  recorded as `derived_from` with the source text's hash pinned. Three protections, three scopes:
  the atom guards what must be true; Dragoman's libraries guard what the client always says; the
  chained source transmits what the voice writer chose here.
- **`vocab/register.enum.json` (register.v0.1):** governed, versioned, closed. Four registers
  (taxonomy-up-front, Jake's call), each with abstract spec fields (person/stance/formality)
  realized natively per locale — register does not translate. Per-register `status`: only a
  `specified` register may carry accepted renderings; `warm_direct` is reverse-specified from the
  January artisan control course and is the arc's validation target; the other three are `draft`
  and the gate flags renderings against them. Boundaries stated in-file: TONE MODULATES WITHIN
  REGISTER (tone stays per-element at the intent layer; the voice writer reads it as input);
  register is a chosen input, never a judgment about learners — segment→register selection is
  Chameleon's join, downstream.
- **`schemas/voice.pack.schema.json`:** per-project packs `voice/<register>.json`
  (vocab/schema in core, instances per-project — answering the standing per-project-store carry
  FOR PACKS). Entries key on `atom_id` per the 08-25 occurrence-identity precedent, with
  `element_overrides` only where placement constrains; fields mirror the locale contract
  (`status`/`reviewer`/`source_hash`) plus `derived_from`; propose→accept statuses
  `draft`/`accepted`, `reviewer` required at accepted — the agent never sets accepted.
- **Locale contract addition (backward-compatible):** locale entries MAY carry `derived_from`
  when rendered from an accepted voice entry; `source_hash` still pins the atom.
- **`tools/validate_voice.py`:** the bookkeeping gate — schema, register governance, atom anchor
  freshness, chain freshness; selftest proves red eight ways. It does NOT check meaning
  preservation itself — that is voice mode's review gate (the invent-guard), a later hop.

**Why:** Opening hop of the voice-pack arc: land the contract so the writer lands into a gated
store, not the reverse. The stakes sentence for the arc: let the words change while proving the
meaning didn't.

**Consequences:** Hop two = Dragoman voice-mode prompt + propose→accept on paytrans (the
Amanuensis shape). Hop three = realize learns "accepted voice rendering if present, else verbatim
atom" — every existing store plays unchanged until then, proven byte-identical this hop (no
pipeline code touched). Chameleon carry recorded in the decision-log: every pack axis widens its
decision space; revisit after player expression.

**Supersedes:** the hop-five block's passing parenthetical "keyed by element id" — refined to
atom_id + element overrides, exactly the pack-shape decision that block deferred to this design
pass. Nothing else; single-writer, reference-don't-embed, and the working-process block stand.

---

## 2026-08-31 — Voice hop two: Dragoman's voice mode exists and has proposed; the invent-guard is two-speed; acceptance is one human-run script

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** The voice writer, per the hop-two design beat (three calls, all Jake's):

- **The mode contract:** `agents/localize/voice.system.md` (`voice-agent.v0.1`) — the register-
  coordinate instantiation of Dragoman's frame: same two-speed principle, same flag discipline,
  same draft-only bright line, STRICTER invention profile. New flag taxonomy (`invented-risk`,
  `compression-loss`, `register`, `ambiguous-source`, `defined-name`, `verbatim-kept`). Verbatim
  is legal and declared. The mode reads element tone where present (absent in paytrans — proceeds
  without) and never reasons about learners (register is a chosen input; selection is Chameleon's).
- **The invent-guard is TWO-SPEED** (`tools/localize/voice_gate.py`): a deterministic class —
  draft-only bright line, anchor freshness against the atom's current `content_hash`, and NO
  INVARIANT IMPORT (numbers/dates/names in a rendering must exist in the atom; a sibling-atom
  fact passes WITH a visible note; an absent fact fails) — plus a judgment class: writer
  self-flags + confidence, with human acceptance as the meaning gate. Honest limit stated in the
  prompt_purity.py manner: the deterministic guard catches imported facts with countable surface
  forms, not paraphrased invention; that residue is what acceptance is FOR. Selftest proves red
  seven ways.
- **Acceptance is `tools/localize/voice_accept.py`** — the accept_value.py pattern: the pack's
  ONLY writer, run by a person, `--by` required. Re-runs the invent-guard at acceptance time
  (stale or invariant-violating drafts are refused), refuses acceptance against a non-`specified`
  register, supports `--edit` (accepted-with-edit — the human's authorship, recorded), and
  validates the pack against the schema before writing. Drafts live in
  `voice/proposals/<register>.json`, NEVER in the pack.
- **Execution (this run):** the mode was executed in-session (implementation varies behind the
  contract); provenance in the proposals store records agent, prompt_version, and the January
  artisan course as exemplar_ref. **Scope: the 50 course-played atoms** (of 68 — the arc's
  validation target is the played course).
- **The proposals exist:** `cgen/brunswick/projects/paytrans/voice/proposals/warm_direct.json` —
  50 drafts, all gate-green, one sibling-atom note (U.S. rendered where the atom writes USA), and
  one deliberately WITHHELD reassurance: the artisan control's "a solid, positive place to be"
  (midpoint atom) is an evaluative claim no atom carries — flagged `invented-risk`, not written.
  That flag is the honesty line working, and it re-opens the invented-copy design question
  (closure/persuade) with a concrete case.

**Why:** First dispatched LLM writer, landed into the store hop one gated. The pack itself stays
empty until Jake accepts — acceptance is the human's act, mechanically.

**Consequences:** Jake reviews the proposals (flags are the triage signal) and runs voice_accept
— per-id, or `--all` after reading the gate report. Hop three: realize learns "accepted voice
rendering if present, else verbatim atom." Griot's "words before voice" wake gains its first
words once entries are accepted. Brunswick termbase remains absent (defined names constrained by
atoms + flags) — a carry, not a blocker.

**Supersedes:** nothing. The hop-one contract block, single-writer, and the working-process
block stand.

---

## 2026-08-31 — Voice hop three: the course SPEAKS. Realize's voice overlay; loud stale fallback; checks stay meaning-anchored

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** Realize applies **"accepted voice rendering if present, else verbatim atom"**:

- **One choke point.** `load_voice_overlay` runs inside `project_lesson_htmls` — the projection
  entry every caller shares (realize main, cartographer, couturier both import and re-project) —
  so all three emit the same words. First regen exposed exactly this: main-only loading left
  couturier's re-projection verbatim; the overlay moved into the shared entry, plus main's early
  load for the manifest stamp.
- **Application rules:** only `status:"accepted"` entries whose `source_hash` matches the atom's
  CURRENT `content_hash`; element overrides (chain-hash checked) beat atom entries. A STALE
  accepted entry falls back to the verbatim atom and is reported LOUDLY at realize time and in
  the manifest (`voice.stale_fallbacks`) — the silent brand-load fallback cost a round trip; not
  again. **Two packs refuse rather than guess** — applying one of several needs an authored
  register choice, which no store carries yet; add it deliberately when a second register is
  accepted.
- **Provenance stamps** (only when a pack applies, so no-pack projects stay byte-identical —
  proven this hop for ast_alsap and ast_artwork): occurrence manifest gains `voice`
  {register, pack, applied, element_overrides, stale_fallbacks}; the lesson projection gains
  `meta.voice_register`.
- **Checks stay meaning-anchored — a named scope line, not an oversight.** Check stems, keys,
  and distractors still derive from verbatim atom text: `assert_check_honest` proves choices
  against atoms, and voicing them would dissolve that proof. Consequence, visible in the played
  course: teaching copy speaks `warm_direct` while check choices quote the atom. Voicing checks
  is its own honesty design (the key must remain provably the atom's claim) — future hop, taken
  deliberately or declined deliberately.
- **Windows/UTF-8 hardening** (the acceptance-run failure on Jake's machine): every read in the
  three voice tools now passes `encoding="utf-8"`. The wider toolset (realize.py's `load`, etc.)
  still reads locale-default — NAMED CARRY, fix as one sweep, not silently.

**Why:** The fallback hop the arc promised: every store without a pack plays unchanged; the one
store with an accepted pack plays in its accepted register.

**Consequences:** `/cgen/?project=brunswick/paytrans` plays warm_direct (verified headless-
Chromium: voice lines render on-screen through all five scenes, Brunswick chrome, the withheld
reassurance ABSENT, check choices verbatim). Realize selftest gains six voice checks (fresh
applies; stale falls back loudly; override beats entry; register stamped; two packs refuse;
reset = pre-hop verbatim). Griot's "words before voice" wake now has accepted words to read.
Next per the arc: the ARC PASS design conversation (beats/intangibles — see hop-two decision-log)
before Griot builds.

**Supersedes:** nothing. Both prior voice blocks, single-writer, and the working process stand.

---

## 2026-08-31 — Arc hop one: the arc facet has an owner. Dramaturge (real seat, one live wake), beats as governed project data

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** The 08-12 ownerless "affective/narrative-arc facet" carry closes into a seat, per
the arc-pass design conversation (species distinction, inverse guard, placement-keyed store —
decision-log, voice hop two) and three calls of Jake's: a REAL agent seat now — one wake live,
the rest declared placeholders, wake conditions exposed as a tunable file because he wants to
watch how the beats arrive differently; beat copy lives INSIDE the register's voice pack; v1
placement granularity is lesson + scene + element-adjacent.

- **The species, named:** a BEAT is a content-free rhetorical/pedagogical move keyed by
  PLACEMENT, not by atom — the homeless kind the withheld-reassurance finding surfaced. Scene
  `heading`/`kicker` fields were this species in embryo (designer-authored, learner-facing,
  atom-free, already rendering); beats are that embryo given a first-class, gated home. Actual
  new factual claims remain invention, remain forbidden — the existing guard already draws that
  line. **Never mint pseudo-atoms for rhetorical moves.**
- **`schemas/beats.catalog.schema.json`** — `occurrences/beats.json` as authored project data
  beside scenes.json. Placement: lesson_start/lesson_end, scene_start/scene_end(+scene_id),
  after_element(+element_id). Intent is GOVERNED and sufficient: welcome = pedagogical `hook`,
  closure = pedagogical `transfer`, gloss = rhetorical `persuade` — no vocab bump was needed,
  which is the design validating itself: a beat kind is an intent, not a new type. Beats carry
  NO text (schema-enforced); `beat_hash` (canonical {beat_id, placement, intent}) is the
  staleness anchor beat copy will pin.
- **The seat: `agents/dramaturge/`** — Dramaturge, arc facet owner. Writes ONLY
  `status:"proposed"` beats; the designer ratifies by flipping status in the catalog (the
  authored-catalog pattern); never writes copy, never sets accepted. `wakes.json` is the play
  surface: `missing_arc_frame` LIVE (≥min_scenes and no lesson frame → propose welcome +
  closure); `withheld_gloss`, `hook_persuade`, `pacing_interlude` declared `live:false` —
  contract first, implementation when deliberately enabled. `tools/dramaturge.py` runs live
  wakes, defers to any claimed placement (a designer's decision, including deletion-by-edit, is
  never re-litigated by a re-run — idempotence proven), and schema-validates before writing.
- **`tools/validate_arc.py`** — the gate: schema, governed intent, placement refs resolve;
  selftest proves red seven ways (including copy smuggled onto a beat). Home of `beat_hash`.
- **voice.pack.schema gains a `beats` section** (keyed `bt_*`): beat copy is register-specific
  and flows through the PROVEN machinery — voice mode proposes, the INVERSE guard gates
  (claim-free proven: no figures at all, no names beyond the governed course allowlist),
  voice_accept stays the only writer, provenance `authored`. Twin stakes sentence: *let words
  with no meaning anchor exist, while proving they carry none.*
- **First run:** Dramaturge proposed `bt_paytrans_welcome` (hook) and `bt_paytrans_closure`
  (transfer) for the employee course — the exact frame the January artisan control has and the
  pipeline course lacks. Both `proposed`; ratification is Jake's edit.

**Why:** Narration (Griot) hits the same missing-welcome problem the on-screen copy did; the arc
store must exist first. And the seat exists because tuning WHERE beats arrive is design work
Jake wants his hands on.

**Consequences:** Arc hop two = beat copy (inverse guard in voice_gate, Dragoman proposes
against accepted beats, beat_hash pinning). Arc hop three = realize injects accepted-and-fresh
beat copy at placement (a beat without accepted copy renders nothing; no-catalog projects stay
byte-identical — proven untouched this hop). Scene heading/kicker REMAIN in scene records for
now — migrating them into beats is a candidate later hop, deliberate, not assumed.

**Supersedes:** the 08-12 "affective/narrative-arc facet has no owner" carry (it does now).
Nothing else; the three voice blocks and the working process stand.

---

## 2026-08-31 — Arc hop two: the INVERSE guard exists and the frame has words. Copy cannot outrun its beat

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** Beat copy flows through the voice machinery under a guard that INVERTS:

- **`inverse_findings` in voice_gate.py** — beat copy is content-free BY CONTRACT, so the check
  proves it carries nothing: ZERO digits anywhere (a figure in a welcome is a claim that belongs
  to an atom), and no capitalized content word that isn't sentence-initial, exempt, in the
  project corpus, or in the ARC ALLOWLIST (data-derived: lesson titles + scene headings/kickers
  + project/client names — no hand-kept list to drift). Anchor: the beat's `beat_hash`
  (imported from validate_arc — one definition). Honest limit stated and DEMONSTRATED in the
  selftest: a claim built from ordinary lowercase words, or a name at sentence start, slips the
  deterministic net — human acceptance remains the meaning gate.
- **`voice_accept` routes `bt_` ids** through the beat flow with one rule the run itself proved:
  **copy cannot outrun its beat** — acceptance refuses while the beat is `proposed` (ratify the
  catalog first), refuses stale `beat_hash`, re-runs the inverse guard, supports `--edit`.
  `validate_voice` gates the pack's `beats` section the same way (real beat, accepted beat under
  accepted copy, fresh hash). `beat_hash` deliberately EXCLUDES status, so ratifying a beat
  never stales copy authored while it was proposed; editing placement or intent does.
- **The frame has words** (Dragoman voice mode, in-session, `warm_direct`), both gate-green,
  both `draft` in `voice/proposals/warm_direct.json` `beat_proposals`:
  - `bt_paytrans_welcome`: "Welcome — this is about your pay: what's changing, how it's set,
    and what it means for you." (flagged: "what's changing" presupposes change — confirm)
  - `bt_paytrans_closure`: "You're informed. You know how your pay is set and what's behind it
    — and that knowledge is yours to use." (flagged: assures the LEARNER — the artisan
    control's closure stance — confirm)

**Why:** The intangibles get words the same way meaning got renderings: proposed under contract,
gated deterministically where possible, accepted by a human where it matters. Twin stakes
sentence enforced: let words with no meaning anchor exist, while proving they carry none.

**Consequences:** Jake's path: ratify the two beats in `occurrences/beats.json` (edit status →
accepted, commit to main), then `voice_accept --ids bt_paytrans_welcome,bt_paytrans_closure
--by jake` (or `--edit`). Arc hop three: realize injects accepted-and-fresh beat copy at
placement; a beat without accepted copy renders nothing; no-catalog projects stay
byte-identical (all stores proven untouched this hop). Then the course opens with a welcome and
lands a closure — and Griot narrates an arc, not a list.

**Supersedes:** nothing. The five prior 2026-08-31 blocks and the working process stand.

---

## 2026-08-31 — Arc hop three: the course greets and closes. Beat injection at the engine projection; a placed beat is a plan, not a promise

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** Realize renders accepted beat copy at its placement:

- **Loading joins three acceptances.** The voice overlay (same choke point, `project_lesson_htmls`)
  admits a beat only when the CATALOG beat is accepted AND the PACK copy is accepted AND the
  copy's `source_hash` matches the beat's current `beat_hash` — stale copy is reported loudly
  (manifest `stale_fallbacks`); an unratified beat or missing copy renders NOTHING, silently by
  design (a placed beat is a plan, not a promise).
- **`_inject_beat_components`** (pure, selftested): `lesson_start` → first component of the first
  scene; `lesson_end` → appended to the LAST scene, i.e. AFTER the lesson-end checks — the
  closure lands once the work is done, matching the artisan control's shape; `scene_start`/
  `scene_end` → that scene's components; `after_element` → directly after that element's
  component. A beat whose target is not in this lesson is skipped and reported, never guessed.
- **Stamps:** manifest `voice.beats_applied`; beat components carry `meta.beat_id`/`intent`/
  `placement` — provenance visible in the projection.
- **Scope line, named:** beats render in the ENGINE projection (the played course). The dev HTML
  sidecar and coverage dump do not show beats yet — carry, taken knowingly; the learner surface
  is the one that matters and the manifest records what applied.

**Why:** The last hop of the arc's first pass: the frame Dramaturge proposed and Jake ratified,
in the words Dragoman proposed and Jake accepted, on the screen the learner sees.

**Consequences:** `/cgen/?project=brunswick/paytrans` OPENS with "Welcome — this is about your
pay…" and CLOSES with "You're informed…" after the checks (verified headless: welcome on the
first screen, closure only on the last, teaching voice intact between). Realize selftest +3 beat
checks (three-acceptance join; all four placements; unplaceable skipped-and-reported). ast
stores regenerate byte-identical. The artisan side-by-side's voice/arc gaps are now CLOSED at
v1: rewritten copy, welcome, closure. Remaining from that table: narration (Griot — now with
words AND an arc), player expression, motion (parked). The withheld midpoint gloss remains the
demo case for the `withheld_gloss` wake when Jake flips it live.

**Supersedes:** nothing. The six prior 2026-08-31 blocks and the working process stand.

---

## 2026-08-31 — Learner surface: authored copy only. Derived kickers suppressed; list titles speak voice

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** Jake's first full viewing of the played course surfaced internal taxonomy rendering
learner-facing: the KICKER map's derived labels ("Present" on 34 of 36 Body components, "Scope
list", "Opening", "Check", "Practice", "Job aid", "Example"). The rule, made explicit and
enforced: **the learner surface renders AUTHORED copy only.**

- **Engine projection emits no derived kickers.** Scene-record kickers (authored in scenes.json
  — "Why this", "The philosophy", …) render; beat copy renders; everything the machine derived
  from internal vocabulary is suppressed (`kicker: ""` at every engine builder). Want a label
  somewhere? Author it — the same pattern as every other learner-facing word. The KICKER map
  stays for the dev HTML sidecar, where taxonomy belongs.
- **`job_aid_title` routes through the voice overlay** — list titles were reading atom text
  directly, bypassing accepted renderings (the range-positions list showed the verbatim
  "The following illustrates…" instead of the accepted "Where people typically fall within the
  range:"). Same class as the hop-three choke-point lesson: a text path we missed, now closed.
- **Selftest repaired to the rule, not the pin** (the 08-20 discipline): three assertions had
  pinned derived kicker VALUES; they now assert suppression, plus one positive rule check —
  no non-Heading engine component carries a kicker.

**Why:** The stakes principle applied to labels: copy the machine derived is copy nobody
accepted. This is deliberately a BEHAVIOR change for every projection that carried derived
kickers — ast_alsap and ast_artwork projections regenerate with kickers stripped (diff verified
kicker-lines-only), not byte-identical, and that is the point.

**Consequences:** The played paytrans course now shows exactly five kickers — all Jake's
(scene records). Voiced list titles render. Verified headless (derived labels absent, authored
survive — the player uppercases kickers via CSS). Remaining visual fine-tuning is player
expression's hop, as planned; this closes the one Jake called disruptive.

**Supersedes:** the engine builders' KICKER defaults (dev sidecar keeps them). Nothing else.

---

## 2026-08-31 — Structure hop (thin): the projection stops flattening the object tree

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** Jake's second viewing surfaced that related chunks render visually flat — header,
subhead, and description at one level, unrelated to the eye. Diagnosis: the object facet ALREADY
carries the tree (`belongs_to` + `order` — his exact example: philosophy → benchmarking +
benchmarking_how, ordered); the engine projection discarded it. Sequencing (Jake's call): this
THIN structural hop now; Griot next as ordered; the full formatting-rules design conversation
opens the PLAYER-EXPRESSION phase, where hierarchy aesthetics properly live.

- **`_stamp_structure_meta` (realize):** scene element components gain
  `meta.structure = {group, depth, head}` walked from `belongs_to`/`order` (data only — IDs are
  never parsed; list components cluster under their container atom). Beats, checks, and scene
  headings are untouched.
- **The player (`engine/runtime.js`):** consecutive same-group components wrap in
  `<section class="structGroup">`; depth/head become classes. Components without structure
  render flat, exactly as before.
- **NEUTRAL styling only, copied into BOTH brand packs** (the engine-base-stylesheet carry,
  honored and flagged in-file): cluster separation, child indentation, head emphasis. Real
  hierarchy aesthetics — type scale, cards, the 255-asset registry — are the expression phase's
  design conversation, not this hop's.
- **Noted for Couturier (expression phase):** section atoms carry `tp_body` — the pillar heads
  read as headings but are typed as body. Primitive assignment is Couturier's facet; the
  structure meta makes the gap visible without reaching into it.

**Why:** A lossy projection is a bug against the constitution's own claim that structure is a
governed facet. Fix the data path thin and now; design the look deliberately and later.

**Consequences:** "How pay is determined" renders as three clusters — "Brunswick's Compensation
Philosophy" heads six indented children (verified headless, computed styles applied). All
projections regenerate with structure meta added (meta-only diff; behavior change named).
Selftest asserts the tree survives projection. Formatting rules = the expression-phase opener.

**Supersedes:** nothing. The nine prior 2026-08-31 blocks and the working process stand.

---

## 2026-08-31 — Griot hop one: the narration SCRIPT layer. Dragoman's third mode; scene-level tracks, multi-pinned; the union guard

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** Narration splits into SCRIPT and PERFORMANCE, completing (not contradicting) the
08-12 Griot design — his own contract says "you do not write words"; the artisan control proves
narration words are a RENDERING (fuller, flowing, for the ear). Three calls, all Jake's:

- **Script = Dragoman `narrate` mode** (`agents/localize/narrate.system.md`,
  narrate-agent.v0.1) — the third coordinate of the one rendering space (language, register,
  now CHANNEL). Chains from accepted voice entries and woven beats; two-speed; connective
  tissue is beat-law (claim-free, flagged); never sets accepted. **Performance stays Griot's
  facet as ratified** (voice_ref/prosody/locale/voiceover_ref) — his "words before voice" wake
  now means: an ACCEPTED track exists and lacks a narration binding. Audio is stage two.
- **Tracks are SCENE-LEVEL and MULTI-PINNED** (`schemas/narration.pack.schema.json`): one
  flowing script per engine scene (incl. lesson_end); `sources` maps every contributing
  atom_id → content_hash and beat_id → beat_hash — any source moves, the track is stale, one
  walk. Pack at `voice/narration/<register>.json`; proposals at
  `voice/proposals/narration.<register>.json`.
- **The UNION guard** (voice_gate `gate_track_proposals`): pins must resolve and be fresh;
  every invariant in the track must exist in the UNION of pinned sources (atom text + its
  accepted voice rendering + beat copy); sentence-initial capitals exempt in track prose (the
  same documented limit the inverse guard demonstrates); figures never exempt. Selftest proves
  red five ways (unanchored figure, stale atom pin, stale beat pin, ghost pin, self-accept).
- **Acceptance:** `voice_accept --tracks <scene_ids>` — same human-run bright line; re-gates at
  acceptance (a stale pin refuses with the moved source NAMED); `--edit` recorded;
  schema-validated before writing.
- **First run (scope: six tracks, 5 scenes + lesson_end):** 676 words of `warm_direct` spoken
  prose proposed, all gate-green, all `draft`. Welcome woven into track one; the accepted
  closure beat lands the final track verbatim. Flags carry the judgment calls: one authored
  causal join, one compression sweep, one evaluative gloss, and the artisan's "no trick
  questions" reassurance WITHHELD again — the midpoint lesson holds in this mode too.

**Why:** Words before voice, at last with the words. The ear's channel gets the same law the
screen's got: proposed under contract, deterministically guarded where possible, humanly
accepted where it matters.

**Consequences:** Jake reviews the six tracks (flags are triage) and runs
`voice_accept --tracks ... --by jake`. Griot hop two: the performance binding (voice registry
seed — per-brand, as his contract predicts — + narration facet bindings) and the player's
voiceover/caption stage. All stores regenerate byte-identical (no pipeline code touched).

**Supersedes:** the 08-12 assumption that narration speaks existing words verbatim — narrowed,
not overturned: Griot's seat, keys, wake, and staleness design stand exactly as written.

---

## 2026-08-31 — Player two: Storyline-shaped chrome at `/cgen/sl` (stock `/cgen` unchanged)

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Players are interchangeable adapters on `realized_lesson.json`. `/cgen` remains the
stock Course Engine. `/cgen/sl/` is player two: Storyline-shaped chrome (left MENU from the
lesson's scenes + title; PREV / NEXT; Submit when the visible scene has a check; bottom media
bar only if the projection actually has voiceover/media) around the **same** graph projection.
The stage still renders existing engine components (Heading, Body, checks, beats, structGroup).
Identity still comes from `cgen/brands/<theme>/` via `meta.theme`. In-session visited/lock on
the MENU is tab state, not an LRE / learner model. Claude is a co-builder: this hop does not
freeze them out of the stock player, engine, catalogs, or graph.

**Not this hop / not touched:** Review 360 commenting or sign-in; forty chrome buttons; After
Effects on the stage; new atoms; Storyline file import; Couturier `style_ref` fused into client
hex; `cgen/index.html`; `cgen/src/main.js`; `cgen/src/lessonCatalog.js` (imported); engine
runtime/components `/cgen` uses (imported, APIs unchanged); ALSAP / artwork / paytrans atoms,
occurrences, realize, cartographer, couturier, voice packs, beats; `cgen/lumina`; `/cgen/alsap`
rewrite; pretty URLs. Working-process block untouched.

**Query contract.** Same as stock: `?project=` (bare slug = astellas; `brunswick/paytrans`
client-qualified), `?lesson=` inside that catalog, `?course=` raw-path hatch. Unknown
project/lesson fails in the stage; no silent ALSAP fallback. Default catalog remains ALSAP
short so the adapter is not Brunswick-only. Catalog/projection paths resolve against `/cgen/`
(the stock root), not `/cgen/sl/`.

**Why:** Jake is testing Claude's paytrans / voice / arc work on the stock player. A second
chrome must sit beside that work, not replace it.

**Consequences:**
- Live stand-in: **https://trainstorm.ai/cgen/sl/?project=brunswick/paytrans** next to unchanged
  **https://trainstorm.ai/cgen/?project=brunswick/paytrans**.
- **https://trainstorm.ai/cgen/sl/** default is ALSAP short (same catalog default as stock).
- Hide-VO honesty is the same rule: paytrans currently has no VO file — do not fake a playbar
  or a video stage. Griot hop two still owns the voiceover/caption stage.
- A third player is a sibling folder, same adapter contract; do not fork meaning to add chrome.

**Supersedes:** nothing. `/cgen` as the stock Course Engine stands. Claude's 2026-08-31
paytrans / voice / arc / Griot / structure / learner-surface blocks stand.
## 2026-08-31 — Griot hop two: the seat RUNS. Performance bindings, the brand voice registry seeded, caption-first playback

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** Griot's ratified facet finally executes, and the script reaches the learner —
caption-first (Jake's call: reviewable today, zero audio dependency), with the voice registry
seeded per-brand (Jake's call; the seat's own prediction).

- **`brands/brunswick/brunswick-voice.registry.json`** — the per-brand voice/persona store
  Griot's contract predicted, closed-list governed, seeded with ONE candidate
  (`voice_bw_narrator`, reverse-specified from the artisan control's VO direction) — flagged
  for Jake's review, never an inline voice.
- **`tools/griot.py`** (griot.v0.1) — read-then-bind: wakes on accepted tracks lacking
  bindings; binds voice_ref/register/locale/narration_source/script_hash into
  `occurrences/narration.json`; `voiceover_ref` stays NULL — audio is a render step ("you
  choose, they produce"). Writes no words; refuses an ungoverned voice_ref; never re-litigates
  an existing binding; refuses to guess among multiple voices (an authored choice, when a
  second voice exists). Selftest proves the contract four ways.
- **Staleness both ways, per the seat:** `script_hash` pins the accepted track text (re-accept
  with new words → binding stale); the track multi-pins its sources (meaning moves → track
  stale → binding transitively). Realize joins THREE acceptances again — accepted track +
  binding + fresh hash — before projecting `scene.voiceover`; stale is loud
  (`stale_fallbacks: narration:<scene>`); anything short projects nothing.
- **Caption-first playback:** the projection carries `captionText` (+ `voiceRef`, `locale`;
  `src` only once a render step fills `voiceover_ref` — the same field then feeds VTT). The
  player treats captionText as a payload: CC chrome appears, a `captionStrip` renders the
  scene's script under the CC toggle, styled neutrally in BOTH brand packs (carry honored ×3).
  Manifest stamps `voice.narration_scenes`.

**Why:** Words before voice, then voice before audio: every layer reviewable the moment it
exists, none pretending to be the next.

**Consequences:** `/cgen/?project=brunswick/paytrans` with CC on shows each scene's narration —
verified headless (toggle appears, strip carries the script per scene, hides cleanly).
Remaining for narration: the audio render step (TTS or recorded VO consuming the bindings,
asset entries per visual-asset.schema.json, VTT from captionText) — a deliberate later hop.
ast stores byte-identical. Jake's review items: the candidate voice entry, and the captions
read aloud in place.

**Supersedes:** nothing. Ten prior 2026-08-31 blocks and the working process stand.

## 2026-09-01 — Audience hop one: the sibling graph's schema. Segment records, seeded from B-sub; `risk_of_overuse` a gate; LRE Stage 1 = a segment enacted as a synthetic learner

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** The Audience Agent's write contract exists, and the Learner Response Engine's first
rung is defined as a one-directional stage that plans against it. Three calls, Jake's:

- **`schemas/audience-model.schema.json`** (audience-model.v0.1) is the learner/audience model —
  Band B-sub (ADRA S6.1–S6.6 + S7) as a governed record per SEGMENT, written only by the Audience
  Agent into a project's `audience/<segment_id>.json`, beside `voice/` and `locales/`. It joins the
  content graph through `obj_` ids only (mastery, factor scope) — never through elements. Every
  psychological value is a governed id (`vocab/disposition.enum.json`, eight families, closed) +
  strength + `basis` — a `<source>:<ref>` reason token, never prose, never a confidence.
- **`risk_of_overuse` is a gate, carried on every factor.** Schema-required; the planner rule
  (high: acknowledge, never amplify or repeat · moderate: once per course · low: free) is written
  and will be enforced when the direction planner exists (D10). `tools/validate_audience.py`
  refuses an approved record whose high-risk factor is unscoped.
- **Baselines are exactly four — self_efficacy, risk_sensitivity, identity_safety, trust.** The
  other four candidates (clarity, agreement, intent_to_act, load) are trajectories, not audience
  properties; a schema that asserted them at design time would be lying. They belong to the
  scene's learning contract (D9). "No silent-lying schemas" is now a standing test.
- **`kind: learner` is reserved for the Responsive Engine** and is illegal in any content project
  store (gate red, not warning). Same shape as `segment`, so the planner cannot tell synthetic
  from live — that is the hinge of the two-stage LRE (`architecture/lre-stage1-synthetic-learner.md`).
- **The psychological primitives are reasoning, not content:** never a property of an element or
  of the audience record; they appear only in a binding's reason trace.

**Why:** The horizon says build the deterministic contract first and prepay for nothing. A synthetic
learner that fills the same contract a live one will is the cheapest way to exercise the whole
LRE loop — state → plan → evidence → re-plan — before a human is in it, with every step reviewable.

**Consequences:** Nothing renders differently; no store changes (byte-identical proven). New gate
in the sweep: `validate_audience.py --selftest` / `--project`. Deferred and named (D1–D10 in the
design record): direction facet + planner (next design beat: its line against tone and arc), the
Stage 1.5 traversal loop (different model, adversarially seeded, bounded, evidence flags against a
contract), `learner-evidence.schema.json`, the scene learning contract, meaning variants,
`disposition` seeds promoted by an Audience Agent pass, `derived_from` added to element governance.

**Supersedes:** nothing. Extends unification-map §6 step 5 from "begins the frontier" to "first
rung built." Prior 2026-08-31 blocks and the working process stand — with one process amendment
recorded in the Project doc `claude/workflow-patch-series.md`: pull the real repo before designing.

## 2026-09-01 — Schema graph: a diagram of record for how the schemas join, live at `/cgen/schema-graph`

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** The relationships between `schemas/`, `vocab/`, `registry/`, `ontology/` and the
README-contracted stores are drawn once, as data-backed HTML, and hosted from the repo.

- **`architecture/diagrams/schema-graph.html`** — 37 nodes, 90 field-level edges, each read
  from the file it names; six edge types (keyed reference · binds under · hash pin ·
  derived/realized · governed value/mirror · proposed-not-built). Includes the audience model
  (PR #62) as the sibling graph it is. Stamped with the commit it was read at (`main@8b349d9`);
  re-read and bump the stamp when a schema changes.
- **Self-contained by the site CSP:** vendored `d3.v7.9.0.min.js` beside the page, no CDN, no
  web fonts (`/_headers` is `script-src 'self'`; no second CSP — PR #6).
- **`/cgen/schema-graph`** — forced-200 rewrite in `netlify.toml`, the `/cgen/alsap/coverage`
  pattern; d3 loaded by absolute path.
- **Flagged, not fixed:** `atom.schema.json` `$id` still `astellas.example`; tone / complexity /
  visual-type name element fields the schema lacks; no locale-pack schema; no core seed for
  `doc_` / `reg_`.

**Why:** The one rule (STRUCTURE.md) puts a rendered diagram in `architecture/diagrams/`, git-only,
and the schemas are now numerous enough that their joins need a picture a cold reader can hover.

**Consequences:** Nothing gated changed; full sweep green (validate_atoms ×4 — `ast_artwork`
still BLOCKED on unadopted registry extensions, pre-existing; lint 0/0; sidecar OK;
validate_objectives ALL PASS; selftests ×3 PASS). Next layer, named not built: a derived
`tools/schema_graph.py` so the page cannot drift.

**Supersedes:** nothing. The Audience hop one block above stands.

## 2026-09-01 — Direction hop one: the audience coordinate. Weight + tempo as an external pack; the Responsive Engine seat activated in design-time mode; risk_of_overuse becomes executable

**Signed:** Jake / Claude — *PROPOSED until merged; merge is the ratification.*

**Decision:** Experiential direction is its own facet, owned by the roster's Responsive Engine,
and it is the audience coordinate of the rendering space.

- **The line.** Tone, arc and expression are audience-invariant; **direction is the one thing that
  varies per audience segment while meaning, tone and arc stay fixed.** A field that would be set
  identically for every segment is not direction. Written into `vocab/direction.enum.json` as its
  governing rule. Five of the eleven rehydrated "treatment" values dissolved into facets that
  already own them; there is deliberately **no scene-level enum**.
- **Two axes, closed and versioned:** weight (`anchor` · `lead` · `support` · `aside`) and tempo
  (`brisk` · `measured` · `dwell` · `progressive`). Every value must name a resolver rule that can
  produce it — `pivot` was withheld under that rule.
- **An external pack, not a field on the element:** `direction/<segment_id>.json`
  (`schemas/direction.pack.schema.json`), sibling to `locales/<lang>.json` and `voice/<register>.json`.
  **Two pins:** the entry's `source_hash` (the element's meaning) and `audience_ref.source_hash`
  (the segment record's analysis). Reason traces live **per entry**, as short governed tokens —
  which closes the long-open `plannerAssessment` question: reasons, never a confidence value.
- **A pack is the audience DELTA.** An entry is written only where the binding differs from the
  audience-blind baseline, so the invariance test is structural, not aspirational. And an audience
  rule may promote at most **one element per scene** to `lead`: direction does not re-emphasise
  what the content already emphasises.
- **The seat is the Responsive Engine, activated — not a new name.** It owns `direction` and holds
  **no PII in either mode**; the old entry's claim on "learner × objective runtime state" is
  removed. The horizon already separates what that line compressed: **LRE serves · Bayesians infer ·
  Transcript stores.** Two modes are declared and one runs: `resolve` (live, design-time batch,
  a human accepts BINDINGS) and `serve` (`live:false`, runtime, a human would accept the POLICY).
  The core is a **pure resolver**, so promotion swaps the harness, not the architecture. Nine seats
  still.
- **`risk_of_overuse` is now executable (D10 closed):** high — never `lead`, never `dwell`, cited
  once per pack; moderate — once per pack; low — free. The budget is checked BEFORE a rule fires
  (a spent factor withholds the EFFECT, not just the citation), and every spend is recorded in
  `harm_budget` because it can land on an element that produces no entry.

**Why:** The audience model needed a consumer, and the LRE needed a first rung that prepays for
nothing. Both are the same artifact: a deterministic, reviewable resolver whose accepted output is
what will one day license accepting a policy — the only way "nothing renders that a human didn't
accept" survives a runtime with no human in it.

**Consequences:** Nothing renders differently; all stores byte-identical (no renderer reads
direction yet — Couturier reading it as an upstream signal, like tone, is the next hop). New in the
sweep: `responsive_engine.py --selftest` and `validate_direction.py --selftest|--project`. The
schema-graph diagram gained the direction node and its edges. No direction pack was written into a
client project (paytrans has no segment record; the reference record is seed data). Still deferred:
D7b the Stage-1.5 traversal loop, D8 `learner-evidence.schema.json`, D9 the scene learning contract,
D1 meaning variants, D5 promoting seed dispositions by a real Audience Agent pass.

**Supersedes:** the roster's prior Responsive Engine entry (rewritten in this hop); the Project note
`claude/design-beat-direction.md` (drafted the beat, now superseded by
`architecture/direction-facet.md`). Extends the 2026-09-01 audience block. Prior blocks and the
working process stand.

## 2026-09-01 — Open-project warrant seated: two front doors; unreachable LOs are a terminal; Case-Author mint gated; Headwater outcomes-mode stays parked

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Jake's open-project instructional-design workflow (vast messy corpus; learning
objectives that support the business goal may or may not be reachable) lives in the **named
seats**, not in Headwater. This hop seats the contract. It does not stand up a Strategist
agent, a Case-Author tool, a workbench UI, Headwater outcomes-mode, `chameleon.py`, or LRE.

**Two front doors, recorded. Do not share a plug-and-play upload.**

| Door | When | Who fires |
|---|---|---|
| **Direct (SOP-course)** | one bounded SOP/form; the document *is* the syllabus | Headwater Direct — mint. Existing mode. Unchanged this hop. |
| **Open-project dossier** | messy corpus; LOs that support the goal may or may not be reachable | Strategist warrant first → Designer `obj_` on a **validated** goal → Headwater Case-Author mint only when committed-design is validated **and** a warrant is held (or an explicit SOP-course Direct escape is recorded). |

**Seats (quoted, not a new species):**

1. **Strategist** — first act is the warrant. Roster: *"does a `goal_` node exist — a business
   outcome, with a measure, that an intervention could plausibly move? No warrant, no
   project."* Unification-map OPEN-06: warrant gate is *"its first act."* `goal.schema.json`
   already requires `label`, `measure`, and `reachability` (*"If nothing here is true, the
   project should not exist"*). If LOs cannot support the goal, that is a **valid terminal**
   (no course, or not this course). Do not invent objectives to save the project. Writes
   draft `goal_` / dossier only as `proposed`; a human ratifies. No PII. Stub:
   `agents/strategist/warrant_STUB.md`, same genre as
   `agents/chameleon/chameleon_STUB.md` (*"This is not an operating prompt and not
   an agent"*). No `strategist.py`.
2. **Audience** — design-time segments gleaned from the corpus (no PII). Later input to
   Authoring Chameleon. Not LRE / runtime Chameleon.
3. **Designer** — `obj_` that `serves` a **validated** goal. Lock before `teaches` binds.
   Roster: *"Objectives never lock without a human conversation; she insists on it."*
   Brunswick objective-lock (this file, 2026-08-31): *"`validated` here means the warrant
   holds for building"*; *"Hop three may bind `teaches` against validated objectives."*
   No lock without a human.
4. **Headwater Direct** — one bounded SOP/form; document is syllabus; mint. Existing mode
   in `agents/headwater_ingest/02_system_prompts/core_agent/headwater_system_prompt.md`
   (*"Input is one artifact whose whole content is in scope: a single SOP, a single form.
   There is no selection to make; everything in the source becomes canon. Go straight to
   the mint."*). Direct is not rewritten.
5. **Headwater Case-Author** — messy corpus. Stage 1 scope-commit emits a
   **committed-design** artifact (not atoms). Stage 2 mint wakes only when that artifact is
   validated **and** a warrant is held (or an explicit SOP-course Direct escape is
   recorded). Headwater still writes only meaning + object + source-type. It does not mint
   `goal_` or `obj_` or audience.

Headwater **outcomes-mode** stays parked and is not this. This is Strategist / Designer /
Case-Author coupling, not Headwater writing LOs.

**Why:** An open corpus is not an SOP. Treating it as a plug-and-play upload would skip the
warrant and invent objectives to save the project — the failure the schema, the roster, and
the Brunswick lock already name. Direct remains the SOP-course door; the dossier is the
other door.

**Consequences:**
- Stub contract only. No Python, no UI, no store writes. `/cgen`, `/cgen/sl`, ALSAP,
  artwork, paytrans, realize, voice, and beats are untouched.
- Case-Author mint in the Headwater specialization gains the warrant / Direct-escape gate.
  Direct mode text is unchanged. No Case-Author tool.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology, or later
  agent prompts.
- Working-process block (this file, 2026-08-25) is untouched.

**Supersedes:** nothing. Seats the roster Strategist / Designer / Audience bios and the
existing Headwater Direct / Case-Author modes; does not replace them. Headwater
outcomes-mode remains parked. Prior blocks and the working process stand.

## 2026-09-01 — Committed-design is the Case-Author stage-1 node; contract-before-writer; mint still does not exist this hop

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The Case-Author mint gate seated in the 2026-09-01 warrant block is no longer
prompt fiction. Headwater Case-Author stage 1 emits a durable **committed-design** node —
selection plus framing, not atoms — and that node has a schema:
`schemas/committed-design.schema.json`. Stage 2 mint still does not exist this hop. A writer
does not exist this hop. No tool proposes designs.

- **Not an atom.** Opaque `cd_` id. Never `atom_` / `ele_`. Never `meaning.source_text` dumps
  of the corpus. Never PII. Never occurrence intent / expression / audience. `goal_` and
  `obj_` stay Strategist / Designer; this node may **reference** a held `goal_` and locked
  `obj_` ids.
- **Selection + framing.** `derived_from` names the corpus as source-store / inventory refs
  (`doc_` / `rec_`), not embedded blobs. Selection partitions what is in-scope for mint vs
  left in the source store (never deleted). Framing is the teachable shape, enough for a
  future mint to know what to decompose.
- **Warrant join.** Exactly one of: a held/validated `goal_` ref, or a recorded SOP-course
  **Direct escape**. Not neither. An unreachable-LO terminal is not a held warrant — this
  artifact is then **not** validated for mint.
- **Status.** Species-closed v0.1 list: `proposed` | `validated`. Reuses those house words
  (beats start at `proposed`; the warrant chain ratifies as `validated`) without silently
  extending `beats.catalog`, voice, or `goal.schema` enums. Agent writes `proposed`. A human
  sets `validated` and a human-shaped `reviewer`. Escape kind `sop_course` is the same kind
  of closed list; version-bump to extend.
- **Gate, not a writer.** `tools/validate_committed_design.py` — schema + warrant-or-escape +
  HITL reviewer + not-an-atom. `--selftest` proves red. `--project` with no document is a
  contract-only pass. Example: `schemas/committed-design.example.json` (`status: proposed`,
  marked example; not a live paytrans design).
- **Headwater.** Case-Author stage 1 points at this schema. Direct mode is unchanged. No
  Case-Author tool, no `strategist.py`, no workbench UI, no Headwater outcomes-mode, no
  `chameleon.py`, no LRE, no atom minting.

**Why:** PR #66 seated the wake condition in the Headwater prompt and the Strategist stub.
Without a schema the mint gate had nothing to point at. Contract before writer: Jake can
read one example; Claude is not frozen out of Headwater; nothing proposes designs.

**Consequences:**
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans atoms/voice/beats, realize, cartographer,
  and couturier are untouched. Working-process block (this file, 2026-08-25) is untouched.
- The 2026-09-01 warrant block stands. This hop gives its committed-design sentence a
  contract. Mint remains unbuilt.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology, or later
  agent prompts.

**Supersedes:** nothing. Extends the 2026-09-01 warrant block by naming the stage-1 artifact.
Prior blocks and the working process stand.

## 2026-09-01 — Case-Author stage-1 writer exists; propose-only; mint still does not; human validates

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Headwater Case-Author stage 1 has a runtime. `tools/headwater_case_author.py`
reads a corpus inventory and **proposes** a committed-design document (`cd_`, status
`proposed`, `proposed_by` stamped). It does not mint atoms. It does not set `validated`.
It never writes `reviewer`. A human-run `tools/committed_design_accept.py --by` is the
only promoter to `validated`, and it re-runs `tools/validate_committed_design.py` first
(refuses unreachable-LO, missing warrant-and-escape, agent-shaped `--by`). Stage-2 mint
still does not exist.

- **Dramaturge pattern.** Propose, never accept. A designer's existing design at `--out`
  (proposed or validated) is not re-litigated.
- **Selection is a partition.** `in_scope` vs `left_in_source_store`. The fixture listing
  has out-of-scope docs; smashing the whole corpus into `in_scope` with an empty leftover
  is refused. Gate before write.
- **Fixture only.** Inventory and proposed design live under `reference/` (schema example
  stays under `schemas/`). No live Brunswick/Astellas `cd_`. Direct-mode
  `headwater_ingest*.py` scripts are untouched.
- **Headwater prompt.** Case-Author stage 1 points at this tool as the scope-commit
  runtime. Claude is a co-builder; this hop does not freeze them out of Headwater.

**Why:** PR #67 landed the contract. The mint gate had a schema and no writer. This hop
is the Dramaturge hop for that node: a propose tool a designer can run, a human accept,
no atoms.

**Consequences:**
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans live stores are untouched. Working-process
  block (this file, 2026-08-25) is untouched. No `strategist.py`, no workbench UI, no
  Headwater outcomes-mode, no `chameleon.py`, no LRE, no Direct-mode ingest rewrite, no
  Case-Author stage-2 mint.
- The 2026-09-01 committed-design contract block stands. This hop gives it a writer.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology, or
  later agent prompts.

**Supersedes:** nothing. Extends the 2026-09-01 committed-design contract block by adding
the stage-1 writer. Prior blocks and the working process stand.

## 2026-09-01 — Strategist operating prompt seated; propose-only dossier; human accept; still no strategist.py

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** The Strategist seat is no longer a stub-only contract. Jake's ad-hoc pack is
seated as one operating prompt in the same genre as Headwater (spine slots at
`agents/_shared/facet_owner_spine.md` + specialization at
`agents/strategist/02_system_prompts/core_agent/strategist_system_prompt.md`). The file
`agents/strategist/warrant_STUB.md` is now the **contract that points at that prompt**. It
is no longer "this is not an operating prompt." There is still **no `strategist.py`**.

**Inherited into the operating prompt (compressed, one voice — not pasted wholesale):**
- Ingest Context Digest (`architecture/lineage/PROMPT_ingestion_project-context-md.md`) —
  facts vs interpretations, stated vs implied, operational reality, diagnostic gaps with
  no prescriptions yet, open questions that expose hidden assumptions.
- Exploratory instructional script (`architecture/lineage/PROMPT_exploratory_instructional_script.md`) —
  hot, non-binding; permission to say this is probably not a course; harvestable close.
  Standing mode is **dialogue with Jake**, not a dumped essay unless he asks for a snapshot.
- Intervention Warrant v0.1 (`cgen/knowledge/intervention_warrant_v0.1.md`) — the hard gate:
  Value Evidence (human-level case; regulation is crystallized memory of a human cost),
  Adoption Legitimacy, Cynicism Audit (Q3-fail + Q1+Q2-pass is trust-repair, a partial
  pass). Designer's shield: the system requires a warrant.
- Proto-agent mapping (`architecture/lineage/2026-01-proto-agent-prompts.md`): ingest +
  warrant absorbed into this seat; exploratory had no agent home — that hole is this hop.
- Overlay: systems-diagnostic *questions* folded in (not a second agent). Devil's-advocate
  is an **on-demand pass**, not the standing voice. Conversational default: working
  collaborator for an ID in regulated industries.

**Left out of this prompt (on purpose):**
- `PROMPT_design_commitment_production_script.md` — cool lock / production script /
  compiler contract. Designer / script later.
- October 2025 Course-Design-Prompt-Chain (AA/OA extractors, storyboard, PPT, QA).
- Orchestrator product prompts. Headwater mint rules, Realizer, Cartographer, Couturier,
  player chrome.

**Dossier store (new species — do not extend `goal.schema` with `proposed`):**
`schemas/dossier.schema.json` (`dossier.v0.1`, `doss_`, status `proposed` | `validated`).
May embed proposed `goal_` *payloads* (label / measure / reachability). `measure` is the
business discharge test; warrant Q1 is the human-level case — keep both. Gate:
`tools/validate_dossier.py`. Human-run `tools/dossier_accept.py --by` is the only writer
of `validated` (human-shaped `--by`; writes nothing on refuse). Example fixture stays
`proposed` (`reference/example_dossier.json` — not a live engagement). **Accept promotes
the dossier only.** Writing proposed payloads into `ontology/goals.json` is a named next
hop. Unreachable-LO terminal is valid (empty `proposed_goals`; finding `no_course` /
`not_this_course`). Direct escape is recorded as itself, not as a pretended warrant.

**Still not this hop:** `strategist.py`; atoms; `obj_` lock; Case-Author mint (stage-2
still unbuilt; stage-1 writer untouched); Headwater outcomes-mode; chameleon.py; LRE;
workbench UI; `/cgen` player; `/cgen/sl`. First live wake is still a messy corpus Jake
actually has — not this PR's fixture.

**Why:** PR #66 seated the stub; PRs #67–#68 gave Case-Author a contract and a propose
writer. The exploratory prompt still had no agent home. A stub cannot make a mediocre ID
excellent. The operating prompt is the seat; the dossier is the snapshot; the human is
the only ratification.

**Consequences:**
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans live stores, realize, cartographer,
  couturier, Case-Author tools, Audience / Direction hops are untouched. Working-process
  block (this file, 2026-08-25) is untouched.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology,
  Audience, Direction, or later agent prompts.
- Temperature: this seat is hot. Mint / Realizer / Cartographer stay cold.

**Supersedes:** the 2026-09-01 open-project warrant block's clauses that the Strategist
file is *"not an operating prompt and not an agent"* and *"stub contract only. No
Python."* Its two front doors, unreachable-LO terminal, Case-Author mint gate, parked
outcomes-mode, and "no `strategist.py`" stand. This hop gives the stub an operating
prompt and a propose-only dossier store; it does not stand up a compiler.

---

## 2026-09-01 — Accepted CCI Public Disclosure goal seated in the live goals store (named hop after dossier accept)

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** `ontology/goals.json` bumps to **v5**. `goal_ast_cci_library_used` is copied from the
accepted Strategist dossier `doss_ast_cci_pd` (`proposed_goals[0]`) into the **core seed**, the
same seating as paytrans (`goal_bw_pay_understood`). Status **validated** — the warrant holds
for building, same sense as the 2026-08-31 paytrans lock. `goal.schema.json` is unchanged
(no silent `proposed` on the node status enum). Store owner remains the client-business note
already on the file.

No per-project `ontology/goals.json` exists (paytrans and ALSAP instances still live in this
seed). This hop does not invent a per-project ontology layout and does not migrate the other
three goals off core.

`tools/dossier_accept.py` still does **not** write the goals store. Accepting the dossier
promoted `doss_ast_cci_pd` only (status `validated`, reviewer `jake`). **This PR is the named
write** that hop pointed at. Designer may now lock `obj_` that `serves` `goal_ast_cci_library_used`;
that lock is **not** this PR.

Owner / `assessed_by`: `role_pd_lead`. No Public Disclosure / DS Business & Operations role
exists in `cgen/trainstorm-core/registry/roles.registry.json` or
`cgen/astellas/registry/roles.registry.json`. Do not invent a person name. The role id is not
minted into a registry this hop.

Parked copy of the validated dossier: `reference/doss_ast_cci_pd.json` (status `validated`,
reviewer `jake`, no EXAMPLE marker). The live Downloads file was not in this VM; the parked
copy reconstructs the accepted identity and `proposed_goals[0]` from the hop payload, and
rewrites the stale `_note` that still said "Status proposed. Not accepted." Nested sketches
still must not carry `status: validated` (that lives on the goals-store node).

**Still not this hop:** `obj_` lock; atoms / `cd_` / `ele_` mint; Case-Author stage-2;
`strategist.py`; Designer as a live agent; Headwater outcomes-mode; `chameleon.py`; LRE;
workbench UI; `/cgen` player; `/cgen/sl`. Claude sibling files (Audience, schema-graph,
Direction) untouched.

**Why:** A validated dossier that never writes a `goal_` leaves Designer with nothing to
`serves`. Building on an unseated sketch would make the warrant decorative. The accept script
was correct not to smash the store; the copy is a separate, named act.

**Consequences:**
- `python3 tools/validate_objectives.py` gates the store (generic schema + reachability;
  no new selftest — the house does not pin individual `goal_` ids that way).
- `python3 tools/validate_dossier.py --file reference/doss_ast_cci_pd.json` gates the parked
  copy. Example fixture stays `proposed`.
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans live stores, realize, cartographer,
  couturier, Case-Author tools, Audience / Direction hops are untouched. Working-process
  block (this file, 2026-08-25) is untouched.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology,
  Audience, Direction, or later agent prompts.

**Supersedes:** the 2026-09-01 Strategist operating-prompt block's clause that writing
proposed payloads into `ontology/goals.json` is still an *unwritten* named next hop. Accept
still does not write the store. The two front doors, unreachable-LO terminal, no
`strategist.py`, and "validated means the warrant holds for building" stand.

---

## 2026-09-01 — Designer objective-lock: four `obj_ast_cci_*` nodes serve `goal_ast_cci_library_used`

**Signed:** Jake / Claude / App-maker — *Jake locked the trainable slice in conversation; merge makes it durable.*

**Decision:** `ontology/objectives.json` bumps to **v6**. Four nodes are seated in the **core seed**,
the same seating as paytrans (`obj_bw_emp_*`). Status **validated** — the warrant holds for
building, same sense as the 2026-08-31 paytrans lock and as `goal_ast_cci_library_used` (goals v5,
PR #70). Every `serves`: `goal_ast_cci_library_used`. `framework`: `none` (no CASE mapping for
this SOP family). Store owner remains L&D / Instructional Design.

The four-chunk split is the dossier `design_insights` reachable slice, not a remainder-bin dump:

1. `obj_ast_cci_public_irreversible` (understand, root) — connect CCI disclosure rules to
   irreversible public-domain errors and to participant data in the same files.
2. `obj_ast_cci_classify_with_guide` (apply; requires 1) — classify CCI / may-be-CCI / not-CCI
   using GUIDE-AST-6011, including that classification can change by development phase.
3. `obj_ast_cci_complete_form_before_ind` (apply; requires 2) — complete FORM-AST-35734 as the
   CCI library for an in-scope asset before IND.
4. `obj_ast_cci_follow_or_escalate` (apply; requires 1) — given an archived FORM, follow it when
   preparing or posting an in-scope public disclosure, or escalate a deviation before ship.
   This is not "where the FORM repository lives" and not the notify path (`not_trainable`).

No fifth `obj_` for Helix/Kachi trigger, FORM storage/notify, the production tracking tool,
governing body, WS3, or org-wide CCI literacy.

No per-project `ontology/objectives.json` exists (ALSAP, paytrans, and AST009 instances still
live in this seed). This hop does not invent a per-project ontology layout and does not migrate
the other twelve objectives off core.

`tools/dossier_accept.py` still does **not** write the objectives store. This PR is the Designer
lock after PR #70; it is **not** Case-Author mint. Headwater Case-Author mint still waits on a
validated `cd_`.

**Still not this hop:** atoms / `cd_` / `ele_` / `teaches` bindings; Case-Author stage 2;
Designer as a live agent; `strategist.py`; Headwater outcomes-mode; `chameleon.py`; LRE;
Audience; schema-graph; Direction; workbench UI; `/cgen` player; `/cgen/sl`. Claude sibling
files untouched.

**Why:** A validated goal with no `obj_` leaves Cartographer nothing to `teaches`. Building on
an unlocked slice would mint remainder-bin operating model as learning objectives. Jake locked
the four we can.

**Consequences:**
- `python3 tools/validate_objectives.py` gates the store (generic schema + reachability +
  promotion gate; no new selftest pinning individual `obj_` ids — the house does not).
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans live stores, realize, cartographer,
  couturier, Case-Author tools, Audience / Direction hops are untouched. Working-process
  block (this file, 2026-08-25) is untouched.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology,
  Audience, Direction, or later agent prompts.
- Amending any of the four now means a new dated entry and a version bump, not an edit.

**Supersedes:** the 2026-09-01 CCI-PD goals-store block's clause that Designer may now lock
`obj_` that `serves` `goal_ast_cci_library_used` and that lock is *not* that PR. The seated
goal, the six `not_trainable` causes, "validated means the warrant holds for building," and
accept still not writing ontology stores stand.

---

## 2026-09-01 — First live Case-Author stage-1 propose: `cd_ast_cci_pd` (synthetic CCI Public Disclosure); mint still does not exist; human validates

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Headwater Case-Author stage 1 wakes on a live (synthetic) corpus for the first
time. The QD-nucleus inventory at
`cgen/astellas/projects/cci_public_disclosure/corpus_inventory.json` is proposed to
`committed-design.json` (`cd_ast_cci_pd`, status `proposed`, `proposed_by`
`headwater.case_author`) by `tools/headwater_case_author.py`. The agent does not mint atoms,
does not set `validated`, does not write `reviewer`. Jake accepts after merge:
`python tools\committed_design_accept.py --file … --by jake`. Stage-2 mint still does not
exist.

- **Writer bump (named, not silent):** `IN_SCOPE_KINDS` adds `guide`. GUIDE-AST-6011 is
  in_scope because `obj_ast_cci_classify_with_guide` requires it; lying that a GUIDE is an
  SOP is refused. `deck` / `faq` / `sow` / `talking_points` / `stakeholder` stay leftover
  kinds. The SH parking-lot "training guide" is kind `stakeholder` so the word "guide" in
  the label does not pull it into in_scope.
- **Thin project store.** Canonical instances live per-project
  (`committed-design.schema.json`). The store is inventory + proposed `cd_` only. No
  `atoms.json`, no `ele_`, no source PDF dump. Inventory refs are pointers, not a smash
  into `cgen/astellas/registry/docs.registry.json` (that registry remains the live
  ALSAP-era closed list). `validate_committed_design` does not require docs.registry
  membership — the example fixture never did.
- **Selection is a partition.** in_scope: SOP-AST-29658, GUIDE-AST-6011, FORM-AST-35734.
  left_in_source_store: representative remainder (tracking tool, Helix/Kachi trigger,
  WS3 RI, connections/comms, SH parking-lot training guide) — enough that
  `selection_honest` cannot see a smashed corpus; not 114 fake ids; not the 8.6MB dump.
- **Warrant join.** `held_warrant` on seated `goal_ast_cci_library_used` (goals v5, PR #70)
  with the four locked `obj_ast_cci_*` (objectives v6, PR #71). Framing is QD-nucleus
  SOP-course plus a short Q1 living-connection frame. Not CM, not Helix/tracker/repo/
  governing body.
- **Not this hop.** Stage-2 mint; atoms; `ele_`; `teaches`; Headwater ingest of the 114
  files; `strategist.py`; more `obj_`; goal/objectives schema; `/cgen` player; `/cgen/sl`;
  Audience; schema-graph; Direction; docs.registry smash; overwriting
  `reference/example_*.json`; `--out` at paytrans / ast_alsap / ast_artwork.

**Why:** PRs #70–#71 seated the warrant and locked the trainable slice. Case-Author stage 1
had only a fixture. A live propose is the next named act; mint still waits on Jake's
`--by`.

**Consequences:**
- Gates: `python3 tools/headwater_case_author.py --selftest`;
  `python3 tools/validate_committed_design.py --selftest`;
  `python3 tools/validate_committed_design.py --file` the new `cd_`;
  `python3 tools/committed_design_accept.py --selftest` (accept still refuses agent `--by`;
  example stays proposed). Do not run accept on the live `cd_` in this PR.
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans live stores, realize, cartographer,
  couturier, Audience / Direction hops are untouched. Working-process block (this file,
  2026-08-25) is untouched.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology,
  Audience, Direction, or later agent prompts.

**Supersedes:** the 2026-09-01 Case-Author stage-1 writer block's "Fixture only / No live
Brunswick/Astellas `cd_`" clause. The Dramaturge pattern, propose-only, human `--by`, no
stage-2 mint, and "do not re-litigate a claimed `--out`" stand. The 2026-09-01 Designer
objective-lock block's "Headwater Case-Author mint still waits on a validated `cd_`"
stands — this hop proposes; it does not validate.

---

## 2026-09-01 — Human accept of `cd_ast_cci_pd` recorded in git; mint still does not exist

**Signed:** Jake / Claude / App-maker — *Jake already ran accept locally; this PR only records that accept in git. Merge is the ratification.*

**Decision:** The live (synthetic) Case-Author stage-1 node
`cgen/astellas/projects/cci_public_disclosure/committed-design.json` (`cd_ast_cci_pd`)
is recorded as **validated**, reviewer **jake**. Jake already ran:

    python tools\committed_design_accept.py --file ..\astellas\projects\cci_public_disclosure\committed-design.json --by jake

Output: `+ cd_ast_cci_pd: validated by jake`. This PR copies that accepted node into git.
The agent does **not** re-run accept. The agent does **not** mint atoms. Stage-2 mint
still does not exist.

Selection, framing, warrant_join, ids, status, and reviewer are Jake's local write
after accept. Only `_note` is rewritten so it no longer says "status proposed" /
"Jake accepts with…" — accepted 2026-09-01 by jake via
`committed_design_accept.py`; not a mint; stage 2 still does not exist.

**Still not this hop.** Stage-2 mint; atoms; `ele_`; `teaches`; Headwater ingest of
the 114-file pile; `strategist.py`; more `obj_`; `/cgen` player; `/cgen/sl`; ALSAP;
paytrans; artwork; `docs.registry.json`. Claude remains a co-builder.

**Why:** PR #72 proposed `cd_ast_cci_pd` and left accept to Jake. Jake accepted. A
validated `cd_` that lives only on one laptop is not durable. This hop records the
accept; it is not a second accept and not a mint.

**Consequences:**
- Gates: `python3 tools/validate_committed_design.py --file` the live `cd_` (status
  `validated`, reviewer `jake`, `held_warrant`, not an atom);
  `python3 tools/committed_design_accept.py --selftest` (example fixture stays
  `proposed`; agent `--by` still refused). Re-running accept on this file must
  REFUSE (already validated).
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans live stores, realize, cartographer,
  couturier, Audience / Direction hops are untouched. Working-process block (this
  file, 2026-08-25) is untouched.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology,
  Audience, Direction, or later agent prompts.

**Supersedes:** the 2026-09-01 first-live-propose block's clauses that `cd_ast_cci_pd`
is status `proposed`, that Jake accepts *after* merge, and that "this hop proposes;
it does not validate." The Dramaturge pattern, human `--by` as the only promoter,
no stage-2 mint, and "do not re-litigate a claimed `--out`" stand. Mint still waits
on a later hop.

---

## 2026-09-02 — First live Case-Author stage-2 mint: `cd_ast_cci_pd`; v2.0 QDs; remainder not minted

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Headwater Case-Author stage 2 wakes. `tools/headwater_case_author_mint.py`
gates a validated `cd_` (`--file`) and, if the wake is legal, runs the sibling ingest
`tools/headwater_ingest_cci_pd.py` into the project atom store. It does **not** mutate
the `cd_`. It does **not** mint `ele_`. It does **not** write `bindings.intent` /
teaches. `--selftest` proves refuse of proposed, leftover smash, and unreachable-LO.

First live mint is `cd_ast_cci_pd` (reviewer **jake**, `held_warrant` on
`goal_ast_cci_library_used`, four locked `obj_ast_cci_*`). In-scope QDs only, **v2.0**
(April 2026, supersede v1.0 — not the Feb 2025 v1 pile):

- SOP-AST-29658 — procedure tree (ALSAP kinds). B/C NOTE *already public is not
  confidential* is the living-connection. E names a Tracking Tool in source_text
  and does not lock an `obj_` or pretend it is live. History/approvals skipped
  (no approval-page PII/emails).
- GUIDE-AST-6011 — four type containers (CMC, Nonclinical, Clinical, Other), each
  with MAY-BE vs Not-CCI leaves; bullets collapsed; not 80 atoms.
- FORM-AST-35734 — form specialisation like FORM-AST-34037. Project ID (Helix) is
  a FIELD, not a trigger. One-tab-per-phase is an instruction atom, not 12 empty
  workbooks.

Remainder inventory is **not** minted: tracking tool, Helix trigger, WS3, comms,
SH parking-lot training-guide. Ungoverned roles/records/docs are flagged to
`proposed_registry_extensions.json`. `cgen/astellas/registry/docs.registry.json`
is not grown. Source `*.pdf` / `*.xlsx` gitignored in the project. Gate:
`validate_atoms.py` must PASS at draft.

**Still not this hop.** Realizer; Cartographer; Couturier; `/cgen` player;
`/cgen/sl`; ALSAP / paytrans / artwork edits; `strategist.py`; chameleon; LRE;
Headwater outcomes-mode; leftover smash; `ele_`; teaches/intent on atoms.

**Why:** PR #73 recorded jake's accept of `cd_ast_cci_pd`. Stage 2 had a wake
condition and no writer. This hop is the first live mint: three QDs, authored
decomposition, remainder stays in the source store.

**Consequences:**
- Gates: `python3 tools/headwater_case_author_mint.py --selftest`;
  `python3 tools/headwater_case_author_mint.py --file` the live `cd_`;
  `python3 tools/validate_atoms.py --project ../astellas/projects/cci_public_disclosure`.
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans live stores, realize, cartographer,
  couturier, Audience / Direction hops are untouched. Working-process block (this
  file, 2026-08-25) is untouched.
- Claude is a co-builder: this hop does not freeze them out of Headwater, ontology,
  Audience, Direction, or later agent prompts.

**Supersedes:** the 2026-09-01 accept-recorded block's clauses that stage-2 mint
still does not exist, that the agent does not mint atoms, and "Mint still waits
on a later hop." Dramaturge propose-only, human `--by` as the only promoter to
`validated`, leftover partition, no `ele_`, and "do not re-litigate a claimed
`--out`" stand. Direct-mode `headwater_ingest*.py` scripts are untouched.

---

## 2026-09-02 — First Realizer pass on live `cci_public_disclosure`; 1:1 `ele_` + QD-nucleus spine; catalog overlay, not a CCI fork of `realize.py`

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Realizer v1 wakes on the live CCI atom store. From
`cgen/trainstorm-core`:

    python3 tools/realize.py --project ../astellas/projects/cci_public_disclosure

Default project remains `ast_alsap` — `--project` is required. The 101 draft
atoms from PR #74 are locked (SOP/GUIDE/FORM v2.0). `cd_ast_cci_pd` stays
validated. Four `obj_ast_cci_*` stay locked and are **not** bound this hop
(`teaches` lives on `ele_` via Cartographer later). Mint still does not write
`ele_`.

**Catalog, not heuristic surgery.** The default spine is a closed project
overlay (`occurrences/scenes.json` + `lessons.json`), same house as paytrans /
ALSAP / artwork. It is the QD-nucleus, not a 101-atom dump and not ALSAP
Procedure-A+BR-field heuristics. `realize.py` is not rewritten into a CCI-only
fork. Sibling form/instance guests stay ALSAP-only (`name==ast_alsap`); do not
fake a sibling. CCI FORM atoms live in the **same** `atoms.json` and receive
1:1 `ele_` like the SOP/GUIDE trees — `assemble_elements` already walks every
atom in the store.

Default lesson `cci_public_disclosure_short` (authored title *Public Disclosure
of Astellas CCI* — a three-root corpus has no single document-root):

1. `why_already_public` (`front_matter`) — SOP root, overview PI/PPD, GUIDE+FORM
   object leaves, B/C NOTE *already public is not confidential*
2. `guide_classify` (`topic`) — phase-decay + four type MAY-BE vs Not-CCI
   (not 80 bullets)
3. `form_as_object` (`topic`) — cover fields + library columns + one-tab-per-phase.
   Helix Project ID is a field present, not a trigger scene. Not `form_br` —
   there is no honest closed fill.
4. `asset_lead_path` (`procedure_a`) — CN-to-IND intro + Procedure A steps
   (initiate / classify / document / inform PD Lead / archive / inform parties)
5. `discloser_path` (`topic`) — Procedure D follow-or-escalate. The mailbox is
   a contact on D.s2, not a person.

Procedure E tracking exists as 1:1 `ele_` and stays **off** the default spine
(`not_trainable` tool). Remainder inventory was never atoms. Coverage dump
keeps the rest.

**1:many seed is empty, and that is honest.** `check_v1` invert_definition needs
`{subject} is {complement}` plus two usable sibling first-sentences. Colon-form
defs (CCI / Public Disclosure / Public Domain) are not copulas. Procedure
steps are imperatives. The one real copula (`FORM-AST-35734 is the
asset-specific library`) has no usable sibling. The B/C NOTE copula inverts
into a nonsense stem. Cloze-without-siblings is not sibling contrast. No LLM
distractors. No invented procedure-step MCQ.

**sequence_order stayed off, catalog preferred over heuristic surgery.** The
projector still derives Procedure A sequence from `procedure_sequence_atoms`
(first real branch, skip thin teaching atoms). Five of six CCI A steps are
under the 50-char thin bar, so the selector returns only s2 and a one-item
sequence is not a check. Widening that selector would be realize.py surgery
for one corpus. Catalog membership still places all six A presents on the
Asset Lead scene. No extra `ele_` for sequence.

**Still not this hop.** Cartographer / `teaches`; Couturier; `/cgen` / `/cgen/sl`
edits; ALSAP / paytrans / artwork stores; minting more atoms; push to main.
Claude remains a co-builder.

**Why:** PR #74 minted the QD-nucleus atoms. The course half had never run on
this store. A catalog overlay is the same move that retired ALSAP-hardcoded
scenes/lessons on 2026-08-27 and paytrans on 2026-08-31.

**Consequences:**
- `python3 tools/realize.py --selftest` — ALL PASS (ALSAP fixture).
- Live run: 101 primary `ele_` (SOP 71 / GUIDE 16 / FORM 14), 0 extras, 0 ALSAP
  guests. Spine 36 of 101 from the catalog. `element.schema.json` ALL PASS; no
  authored `content.text`; `teaches` unbound. Re-run is idempotent (101/0/36).
- `python3 tools/validate_atoms.py --project ../astellas/projects/cci_public_disclosure`
  still GATE @ draft: PASS. `lint.py` on `occurrences/elements.json` OK.
- Writes: `occurrences/{elements,manifest}.json`, `realized_lesson.html` /
  `realized_lesson.json` / `realized_coverage.html`. Catalogs are source of
  truth and are not rewritten.
- `/cgen`, `/cgen/sl`, ALSAP, artwork, paytrans live stores, cartographer,
  couturier, Case-Author tools are untouched. Working-process block (this
  file, 2026-08-25) is untouched.

**Supersedes:** the 2026-09-02 stage-2 mint block's "Still not this hop.
Realizer" and "no `ele_`" clauses as to this store. Mint still does not write
`ele_`. Cartographer / `teaches` still wait. Direct-mode `headwater_ingest*.py`
scripts are untouched.

---

## 2026-09-02 — First non-ALSAP SOP through cartographer + couturier + `/cgen/sl` via `intent_map`; CCI QD-nucleus plays; machinery test, not a gold course

**Signed:** Jake / Claude / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Cartographer and Couturier wake on the live
`cci_public_disclosure` occurrence store. From `cgen/trainstorm-core`:

    python3 tools/cartographer.py --project ../astellas/projects/cci_public_disclosure
    python3 tools/couturier.py --project ../astellas/projects/cci_public_disclosure

Default project remains `ast_alsap` — `--project` is required. Cartographer
is still the single writer of `element.intent`. Designer bindings live as
project data in `occurrences/intent_map.json` (policy `v1_intent_map`), the
same overlay house as paytrans. `bind_teaches()` stays `[]` for any project
other than `ast_alsap`; a second SOP does not inherit `obj_explain_alsap_*`.
Couturier still writes only expression style keys from `intent.move`. It
does not write intent, mint ids, or invent looks for unmapped moves.

**Playable after merge.** `/cgen/sl/?project=cci_public_disclosure` (and
stock `/cgen/?project=cci_public_disclosure`) load the existing catalog
(`occurrences/lessons.json` → `realized_lesson.json`). Default `/cgen` and
`/cgen/sl` without `?project` stay ALSAP. The SL player was not forked;
catalog hrefs are already rooted at `/cgen/`. No voiceover chrome (existing
`lessonHasVoiceoverChrome`). No LLM distractors. No new invert_definition
extras — the empty `one_to_many_seed` from PR #75 stands. No invented
checks.

**`intent_map` binds four locked `obj_ast_cci_*` on QD-nucleus spine atoms
(plus the FORM escalate instructional primary). Live `atom_id`s from
`atoms.json`:**

- SOP root `atom_sop_ast29658` — one hook election (empty `teaches`). GUIDE
  (`kind: procedure`) and FORM (`kind: form`) are also no-`belongs_to` roots
  and would heuristic-hook; the map keeps them `present`.
- Living-connection (overview PI/PPD, B/C NOTE already-public is not
  confidential) → `obj_ast_cci_public_irreversible`. Overview object leaves
  bind the named tool (`GUIDE for classification` /
  `FORM is the library`).
- GUIDE phase-decay + four type MAY-BE / Not-CCI leaves →
  `obj_ast_cci_classify_with_guide`. Thin type headings (CMC. / Nonclinical.
  / Clinical. / Other.) stay unbound.
- FORM cover / library columns / one-tab-per-phase + Procedure A steps
  (complete library before IND) → `obj_ast_cci_complete_form_before_ind`.
  Helix Project ID is a field, not a trigger obj.
- Procedure D follow-or-escalate + FORM escalate instructional
  (`atom_form_ast35734_f_escalate`) → `obj_ast_cci_follow_or_escalate`.
- Procedure E tracking: not in the map. Empty `teaches` is correct. Do not
  bind a tracking obj. Do not bind `obj_explain_alsap_*` or `obj_bw_emp_*`.

Intended_response uses the existing non-ALSAP branch of
`bind_intended_response`. Closed entry shape only (`teaches`, optional
`move`, optional `why`).

**Still not this hop.** chameleon.py; LRE; workbench UI; strategist.py; more
`obj_`; remainder mint; ISO 14971; pretty URLs; `/cgen` player rewrite.
Claude remains a co-builder of Cartographer / Couturier prompts.

**Why:** PR #75 realized 101 1:1 `ele_` and the QD-nucleus catalog spine.
Jake asked to cook the remaining machinery under real-world conditions —
not a second gold Brunswick course, not invented checks.

**Consequences:**
- `python3 tools/cartographer.py --selftest` — ALSAP fixture still green.
- `python3 tools/couturier.py --selftest`
- `python3 tools/realize.py --selftest`
- Live CCI: 101 primary `ele_` (no new ids). One hook. `teaches` bound on 32
  occurrences: irreversible 2, classify 11, complete-form 15, follow-or-escalate
  4. Procedure E unbound. No ALSAP / Brunswick `obj_` on CCI `ele_`. Element
  schema ALL PASS. Couturier dressed 101 / unmapped 0. `atoms.json` and
  `cd_ast_cci_pd` sha unchanged.
- Writes: `occurrences/intent_map.json` (authored); cartographer+couturier
  re-project `occurrences/{elements,manifest}.json` and
  `realized_lesson.{html,json}` / `realized_coverage.html`. Catalogs
  (`scenes.json` / `lessons.json` / `one_to_many_seed.json`) are membership
  source of truth and were not rewritten.
- `/cgen/sl/?project=cci_public_disclosure` is the click target after Jake
  pulls. Working-process block (this file, 2026-08-25) is untouched.

**Supersedes:** the 2026-09-02 Realizer-pass block's "Still not this hop.
Cartographer / `teaches`; Couturier" and "Cartographer / `teaches` still
wait" clauses as to this store. Mint still does not write `ele_`. Empty
1:many seed, no invented checks, and catalog-not-heuristic-surgery stand.

---

## 2026-09-02 — First Astellas/CCI Dramaturge wake; welcome+closure proposed only; Jake ratifies later

**Signed:** Jake / App-maker — *PROPOSED until merged; merge is the ratification.*

**Decision:** Dramaturge's live `missing_arc_frame` wake runs on the five-scene
`cci_public_disclosure` QD-nucleus lesson. Propose-only. From
`cgen/trainstorm-core`:

    python3 tools/dramaturge.py --project ../astellas/projects/cci_public_disclosure

Five scenes ≥ `min_scenes` 3 and no lesson frame → two beats, same shape as
the paytrans first run (`bt_paytrans_welcome` / `bt_paytrans_closure`):

- `bt_cci_public_disclosure_welcome` — placement `lesson_start`, pedagogical
  `hook`, status `proposed`
- `bt_cci_public_disclosure_closure` — placement `lesson_end`, pedagogical
  `transfer`, status `proposed`

**Agent never validates.** There is no `beat_accept.py`. Jake ratifies later
by flipping status to `accepted` in `occurrences/beats.json` (the paytrans
designer catalog flip). Do not invent an accept tool this hop.

**Idempotent.** A re-run skips both placements ("already claimed — not
re-litigating"). `validate_arc` gates before write; `--selftest` stays green.

**Still not this hop.** Griot. Dragoman. Voice / narration copy. An Astellas
voice registry. Atoms / `ele_`. ALSAP or paytrans beats. `/cgen` / `/cgen/sl`
rewrites. Realize / cartographer / couturier re-project. Claude remains a
co-builder of Dramaturge.

Griot still waits on accepted tracks **and** a brand voice registry.

**Why:** PR #75/#76 locked the five-scene QD-nucleus spine and dressed it.
The lesson has no welcome and no closure — the same missing frame the
paytrans artisan control had. Dramaturge's one live wake is the seat for
that. Copy is a later hop, against accepted beats, in a register this
project does not yet have.

**Consequences:**
- Writes: `cgen/astellas/projects/cci_public_disclosure/occurrences/beats.json`
  only (plus this block). Status stays `proposed`. Beats carry no text.
- `python3 tools/dramaturge.py --project ../astellas/projects/cci_public_disclosure`
  succeeds; second run proposes nothing. `python3 tools/validate_arc.py
  --project …` ALL PASS. `python3 tools/validate_arc.py --selftest` ALL PASS.
- Realize was not re-run. Proposed beats stay off the learner surface until
  Jake accepts: `load_voice_overlay` injects a beat only when the catalog
  beat is `accepted` **and** pack copy is `accepted` **and** `source_hash`
  matches `beat_hash`. CCI has no voice pack. `/cgen/sl` plays
  `realized_lesson.json`, which still opens on the QD-nucleus scene heading
  ("Already public is not confidential") and closes on Procedure D — no
  `beat_id`, no welcome/closure copy.
- Paytrans beats remain `accepted`. ALSAP untouched. Working-process block
  (this file, 2026-08-25) is untouched.

**Supersedes:** nothing. The 2026-09-02 cartographer+couturier block stands.
The 2026-08-31 arc hops (Dramaturge seat, inverse guard, beat injection)
already named this path; this is the first Astellas/CCI firing of that seat.


