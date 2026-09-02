# The studio and the ledger — how free-form design and the deterministic graph meet

*Canonical. Settled in the design beat of 2026-09-02 (after PR #77). Companion:
`direction-facet.md` (the last beat's precedent for "propose into a governed slot"),
`agents/strategist/` (the seat that becomes the room), `schemas/dossier.schema.json` (the first
harvest shape), `localization-agent.md` §4 ("examples of good" — the retrieval machinery the
harvest feeds). The Claude Project note `claude/studio-and-ledger.md` is a one-way snapshot of
this file.*

---

## 1. The question

Two things were true at once and felt like a contradiction. One-off prompts — the ingestion
prompt that produces a Context Digest, the prompts that produce a landing page or a whole
course — give results Jake calls fantastic. The graph, fed the same corpus, gives something
faithful, restrained, and one-dimensional. Every attempt to move the first kind of quality into
the second kind of system felt like regression.

The question underneath: *where does the probabilistic work live, relative to the deterministic
work, so that the graph holds the best thinking without thinning it?*

## 2. What the repo actually is, as of main 74c564d

Read before deciding, because the shape was sharper than remembered:

- **There is no in-pipeline LLM call except `tools/localize/build_agent_call.py`.**
  `headwater_ingest.py` "encodes the Headwater agent's *authored decomposition* as data" — the
  thinking happened in a chat, the script serialises and stamps it. Cartographer, Couturier,
  Griot, Dramaturge and the Responsive Engine are deterministic rule tables. Couturier is
  `move → look`, seven rows.
- **The design vocabulary is nearly empty.** Seven `style_ref` roles mapped one-to-one to seven
  CSS classes (`engine/styleRef.js`); six `text_primitive` keys; six `layout_primitive` keys, all
  lifted from the Astellas `.potx` for Storyline, none for the HTML player; zero
  `motion_primitive`; a brand pack of 29 tokens (`brands/brunswick/brunswick.css`). Couturier is
  not restrained. The reservoir it draws from is.
- **The ingestion prompt is already in the graph** as the Strategist seat, and
  `dossier.schema.json` gives its output a home. But the only dossier in the repo is the fixture
  `reference/example_dossier.json`. No `doss_` exists for paytrans or any Astellas project. The
  Brunswick and Grok runs produced the thinking; nothing harvested it.
- **The seat spine-ified the prompt into a writer.** The Strategist spec says "behaviors, not a
  dumped essay" and "do not emit a diagnostic essay unless he asks"; the snapshot compresses the
  nine-section digest into six one-paragraph strings, and three sections (canonicalised
  concepts, assumptions, signal-vs-noise) have no field at all. The rich document that makes the
  prompt good has no home, so every pass through the seat squeezes it to fit the JSON — and the
  JSON is all the gate checks. That compression is what regression felt like.

## 3. The finding

**Judgment already enters the graph one way, everywhere: a session proposes into a governed
slot, a gate validates, a human accepts, code applies.** Dramaturge proposes beats; the
Responsive Engine emits `proposed` direction entries; Dragoman drafts and a human accepts;
Headwater is a chat serialised by a script. "Nothing unaccepted renders" is already law.

So probabilistic-before-deterministic is not something to add. It is the graph's shape. What
was missing is two things, and they are the same thing seen from two sides:

1. **The room.** A conversation is not a writer. Single-writer per facet is a rule about
   *writes*; an hour arguing a dossier, then interventions, then objectives, then a script,
   touches no store and can violate nothing. The invariant bites only at the moment something is
   written down, and then it says: this lands in the store that owns it, stamped by that owner.
   **Seats are the org chart of the write. The conversation is the meeting.** The Strategist was
   built as a writer's spec and then asked to be a room; that is why it keeps refusing essays.
2. **The harvest.** The generating prompt and the schema-emitting prompt must be different
   prompts. Asking one prompt to think richly *and* emit valid JSON lets the JSON win, because
   only the JSON is gated. Split them: the one-off prompt runs **verbatim, hot**, and produces
   the whole document; a **cold harvest** extracts the structured slots from that document into
   the owning stores and points back at the document by reference (`derived_from`). The
   document is the meaning; the JSON is the index. A harvester extracts; it never shortens or
   rewrites. This is *reference, don't embed* applied to Jake's own thinking.

## 4. The studio, as the designer experiences it

One conversation, one voice (the designer does not know or care which model), with **stopping
points**. Drop the corpus; it asks a few questions; it produces the Context Digest. Argue it.
When the argument lands, it offers to write it down: the document is saved whole, the harvest
files the slots to their owners, the gates run, the designer accepts. The same room continues
to reachable interventions, then objectives, then the production script — same persona, hot
and opinionated the whole way, and behind the wall a ledger that only ever receives what was
ratified, filed to the right owner. **The designer never sees a seat.** Seats are governance,
not UX.

Four stopping points, and where each harvest lands:

| stopping point | the document (saved whole) | the harvest (slots, by owner) | gate / promoter |
|---|---|---|---|
| Context Digest | `dossier/context_digest.md` | `dossier/doss_*.json` — Strategist | `validate_dossier.py` / `dossier_accept.py --by` (exists) |
| Reachable interventions | the argued intervention memo | dossier `finding` + `proposed_goals`; `ontology/goals` when that rung is designed | dossier gate (exists); goals gate (open carry) |
| Objectives | the objective rationale | `obj_` — Cartographer / ontology | `validate_objectives.py` (exists) |
| Production script | the script, as authored | atoms — Headwater; beats — Dramaturge; occurrences — Realizer | `validate_atoms.py`, `validate_arc.py` (exist) |

The front end, for now, is a folder and a script. The app comes when the loop is proven by
hand, exactly as `localize` was proven before it was wired.

## 5. What the ledger buys that the unified prompt cannot

The unified prompt yields a production script. It is excellent and it is a one-off: change one
definition next quarter and the whole script is regenerated and re-reviewed sentence by
sentence, and the Japanese version is now a separate problem. The graph's script is the *same
words* — the conversation authored them — but every sentence is keyed, so when the definition
changes, one atom's `content_hash` changes, and exactly the elements, translations, beats and
narration that depend on it go stale and loud, and nothing else moves.

**Deterministic does not mean the agents invent the script. It means that once the script
exists, everything downstream of it is reproducible.** The conversation's quality is not reduced
by the graph; the graph is what the conversation leaves behind so it never has to happen twice.

## 6. The same shape for visual design

The design gap is the identical gap, one facet over, and closes the same way. Taste enters the
graph the way meaning does — a session mints, a gate ratifies, code applies — at two levels
that must stay separate for the reason meaning and locale stay separate:

- **Minting the language** (rare, per client, wide latitude). Inputs: the brand guidelines,
  "examples of good" (Jake's best one-off pages, external references), the scenes the course
  needs. The prompt asks for what a one-off asks for — real HTML/CSS, bold, composed, on-brand —
  but the output comes back **keyed**: tokens and component classes into `brands/<client>/`,
  `style_ref` / `text_primitive` / `motion_primitive` entries into
  `vocab/primitives.registry.json`, and **scene-level composition templates with typed slots**
  (the missing middle layer; `layout_primitive` today is the `.potx` set, not this). A
  **specimen sheet** rendering every entry is the acceptance surface — judged by looking, the
  way an SME judges a projected Word doc; the sheet is a projection, the vocabulary is canon. A
  lint gate does the deterministic part: every key named, no hex outside tokens, slots typed
  against element kinds, closed lists extended only through the proposed-extension path.
- **Binding per scene** (per course, judged per scene) — Couturier's real `propose` mode. Given
  a scene's occurrences with intent, direction weight/tempo and Dramaturge's beats, a model
  proposes composition and style keys *from the minted language*; status `proposed`; the gate
  checks every key exists and single-writer holds; the designer accepts. The model never touches
  a pixel — it makes choices, and the choices are data, so rendering stays deterministic and
  regenerable. Accepted bindings become exemplars the next scene's proposal retrieves
  (`localization-agent.md` §4), so the designer's eye compounds.

Couturier's rule table grows one input at a time — `move` today, direction next (already
reserved for it in `direction-facet.md`), composition after — and only once there is a richer
vocabulary for it to point at. Widening the table first would help nothing.

## 7. Rules (the part that must not drift)

1. **The room writes nothing.** Conversation is not a facet write and is not bound by
   single-writer. Only the harvest writes, and it writes by owner.
2. **Generating prompt ≠ harvest prompt.** The one-off prompt runs verbatim and is never
   rewritten into spine voice. A harvester extracts slots; it never shortens, paraphrases, or
   improves the document.
3. **Document whole, JSON by reference.** Every harvest carries `derived_from` → the saved
   document. The JSON is an index of the meaning, never a substitute for it.
4. **Status is `proposed` until a human promotes.** Unchanged law; the harvest inherits it.
5. **Taste is data.** Design sessions mint vocabulary (brand pack, registry, compositions) and
   Couturier binds from it. No agent invents a look at render time.
6. **Judge projections, ratify canon.** Specimen sheets and rendered digests are how a human
   decides; what gets accepted is the keyed thing behind them.

## 8. First moves (in order; each is one hop)

1. **First real dossier.** Run the ingestion prompt on the paytrans corpus as-is → save
   `cgen/brunswick/projects/paytrans/dossier/context_digest.md` → harvest
   `doss_paytrans.json` with `derived_from` → the digest; extend `dossier.schema.json` so
   `context_digest` carries the reference and the three missing sections → `validate_dossier.py`
   → `dossier_accept.py --by`. Proof that the graph can hold the best thinking whole.
2. **Re-seat the Strategist as the room.** Dialogue mode carries all four stopping points;
   snapshot modes per stopping point emit the owner's shape; the "not a dumped essay" rule
   becomes "the essay is saved whole, the snapshot indexes it."
3. **First design-minting session** against Brunswick: brand PDF + paytrans scenes + Jake's best
   one-off prompt in; proposed brand pack v2 + composition templates + specimen sheet out; lint
   gate; accept. Then, and only then, Couturier reads direction.

## 9. Deliberately not decided here

The app. Which model sits in the room (`build_agent_call.py` / `resolve_prompt.py` already own
that stitch). The composition-template schema (designed in move 3, not before). Whether the
intervention memo gets its own store or lives in the dossier until the goals rung exists.
