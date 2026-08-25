# Prompt Pack → Manifold: the generation pipeline map
 
*First project doc · 2026-07-21. Maps Jake's e-learning prompt pack (`PROMPTPACK_elearningscripts`) onto the manifold's generation layers, validated against the live schemas in `cgen/trainstorm-core/`. Supersedes the first-pass conversational map, which had one wrong hinge (§1).*
 
## 0. What this is
 
The prompt pack takes a messy corpus to a production-ready script — and, in its newer prompts, to typed JSON — mostly by hand, mostly successfully. The manifold is the data architecture those outputs should live in. This doc is the crosswalk: which pack stage is which manifold agent, writing to which schema. It is the spec the "implementable machine" gets built from.
 
## 1. The correction (what changed from the first pass)
 
The conversational map had the pack cooling from hot ideation into a single **atom → element promotion**, "where identity is born." That does not survive the files:
 
- `atom.schema.json` and `element.schema.json` are **not two temperatures of one node.** The atom is the node (meaning + keyed bindings); the element is the *course costume* of that same node (`reconciliation.md`'s unification of `course` / `scene` / `course-primitives`). **Settled 2026-08-25:** one `atom_id`; do not mint a second key. Validate the live graph with `tools/validate_atoms.py`. See `architecture/DECISIONS.md`.
- Identity is not born in one step. Script-primitive ids are still minted at generation. **`element_id`s are not minted at realization** — that §8 line is superseded.
## 2. The canonical pipeline (from `architecture/script-generation-layer.md`)
 
```
source material
   │  generator agent      — WHAT knowledge, structurally
   ▼
SCRIPT PRIMITIVES   ← script.primitives.v1.json   (11 governed types)
   │  realizer agent       — HOW it is presented
   ▼
ELEMENTS            ← element.schema.json          (Head/Statement/List + intent + expression keys)
   │  render agents        — pixels / behavior
   ▼
RENDERED FORMS      — AE / Lottie / HTML → Storyline
```
 
Three layers, two named agents (generator, realizer) plus render agents, and a **governed closed vocabulary at every layer**:
 
- **script primitives** — 11 types: orientation, context_frame, definition, decomposition, distinction, process_flow, role_relevance, knowledge_check, boundary_statement, resource_pointer, closure.
- **intent** — rhetorical (11, settled) + pedagogical (Gagné-based, draft) in `intent.enum.json`.
- **element `type`** — the Head/Statement/List/Callout/… enum in `element.schema.json`.
Each element carries a `derivation` back-pointer (`realizes_primitive`, `script_ref`) so source → primitive → element → render is one traceable chain — the `content_hash` / `source_hash` discipline extended across layers.
 
## 3. Crosswalk — pack piece → agent/layer → schema
 
| Pack piece | Role in the machine | Represents / writes | Schema |
|---|---|---|---|
| `file_to_structured_md.py` (+ `_all`, `merge_project_context.py`) | corpus loader | `project_context.md` with provenance + density | source store (pre-manifold) |
| `PROMPT_ingestion` (Context Digest) | diagnosis / headwater capture | project intent, ROI, stated-vs-implied objectives, gap map | *ROI has no node yet — prose* (§7) |
| `PROMPT_exploratory` (high-temp) | divergent design studio | candidate knowledge-moves, primitives, tensions | *no home yet — prose* (pre-generator) |
| `PROMPT_design_commitment` | commitment / lock scope | the ordered knowledge design (a "script") | the **generator's input** |
| `PROMPT_Optimized` → `typed_script_json` | **generator** (typed) | ordered knowledge moves (`type: orientation`…) | **≈ `script.primitives.v1.json`** |
| `PROMPT_course-json` compiler → `course.json` | **realizer** (+ render routing) | presentation units (Heading/Body/RevealCards/MCQ) | **≈ `element.schema.json`** |
 
## 4. The two IR schemas are two layers, not two drafts
 
The two typed outputs first flagged as "drifting duplicates" are actually unlabeled versions of the two real layers:
 
- `typed_script_json` (blocks of `type: "orientation"`) = the **script-primitives** layer (WHAT knowledge). The Optimized prompt even stamps `schema_version: "script.primitives.v1"` — the *same name* as the repo's `script.primitives.v1.json`.
- `course.json` (Heading/Body/RevealCards/MCQ) = the **elements** layer (HOW shown).
The realizer's job — primitives → elements — is already written down as the **realization table** in `script-generation-layer.md`, and it matches what the compiler does by hand: `decomposition → ListHead + List + ListItem` (the compiler's RevealCards), `knowledge_check → MCQ`, `boundary_statement → Statement via callout` (callout is a role, not a type).
 
**The drift that is real:** the pack's `script.primitives.v1` and the repo's `script.primitives.v1.json` share a name but not a shape. The repo's primitives are rich typed knowledge structures (`definition` = term + meaning + example; `decomposition` = whole + parts[]); the pack's are a thin `{type, delivery, content.text}`. Same story for `course.json` vs `element.schema.json` (the pack's is a four-component subset). Resolution: one canonical source *per layer* — point each pack output at the repo schema and let the thin versions become validation targets, not rivals.
 
## 5. The pack fills the manifold's notional agents
 
The system map states the generator, pedagogy, and presentation agents "can stay notional and still compose later, because they only ever meet on the shared substrate" — only the localization agent (AST009) is currently real. **The pack is the concrete fill for the generator and realizer slots.** These agents were built as prompts before the schema knew they existed. The marriage is therefore not new construction; it is pointing prompts already in use at the graph the architecture already defines.
 
## 6. Two axes, not one (commitment ≠ pipeline)
 
The first-pass map overlaid two different motions. They chain rather than coincide:
 
- **Commitment axis (the pack's front):** ingestion → exploratory → commitment is a *hot-to-cool gradient of design judgment* — diverge, then lock scope. Its product is a committed design.
- **Abstraction axis (the manifold):** generator → realizer → render is a *knowledge → presentation → pixels* descent. It takes the committed design as input.
The commitment gradient produces the generator's input; it is not the same motion as the generator/realizer/render pipeline. Keep them distinct or the map lies.
 
## 7. The headwater — one missing rung above a designed layer
 
*Re-settled 2026-07-21 against the FULL repo (the synced subset is filtered; `atom-spec.md`'s stores section was under-read on the first pass — my error, corrected here).*
 
The objective layer **is designed and in the grounding** — not missing. `atom-spec.md` §4 specifies the intent ontology as `ontology/objectives.json` (owner: L&D), with objective nodes shaped `{ label, requires: [obj_ prereqs], framework }` (e.g. CASE); §5 defines how `teaches[]` resolves against it at render time (sequencing + scoring); and `STRUCTURE.md` governs `obj_` as a stable ID prefix. So `teaches` points at a defined node type — not a dangling design.
 
What is **not built yet** is the store file itself: there is no `ontology/` directory in the repo — the same scaffolded-but-empty status as `registry/` and `locales/` (the Brunswick reference course carries no objectives yet either). That is build status, not a design gap.
 
The one genuinely **un-designed** piece is the **business-outcome / ROI node above the objectives.** The designed objective node points *sideways* (`requires` = prerequisite objectives) and *outward* (`framework` = external competency standard), but has **no upward link to a business result** — no `serves: [goal_id]`, no goal/outcome node type. So the ladder business-outcome → learning-objective → element has its bottom two rungs designed and only its top rung absent. `PROMPT_ingestion` captures that business ROI as prose; nothing in the manifold holds it as a node.
 
*Minor drift found:* `atom-spec.md` designs `ontology/objectives.json`, but `STRUCTURE.md`'s canonical tree omits an `ontology/` folder. Reconcile (add `ontology/` to the tree) when the objective store gets built.
 
**Proposed small fix (deferrable):** one `goal`/`outcome` node type (`goal_` id, business result, measure) plus a `serves: [goal_id]` field on the objective node — added when purpose-tracing up to ROI is wanted. Not on the critical path to shipping a course.
 
## 8. Identity — mint early, not at compile
 
The pack mints IDs positionally at the compiler (`S01`, `b1`) — the coldest end — so they renumber on every re-run, violating *stable, opaque IDs, never reused*. Move minting up to the transforms. **Script-primitive ids at generation; the content node keeps `atom_id`.** Do not mint `element_id` at realization as a new key — superseded by `architecture/DECISIONS.md` (2026-08-25 identity freeze). A course costume is not a second ID space.
 
## 9. Validated vs. open
 
**Validated against the files:** the generator → realizer → render pipeline; facet names and single-writer owners; the two-layer reading of the pack's two schemas; the realization table matching the compiler; the choreography-not-orchestration model at the cold end; and (§7) that the objective layer is designed (`ontology/objectives.json` in `atom-spec.md`) but not yet instantiated, with only the ROI node above it genuinely un-designed.
 
**Open:**
 
- **ROI/outcome node** — add a `goal_` node + `serves` link above objectives, for purpose-tracing? Small, deferrable. (§7)
- **objective store not instantiated** — `ontology/objectives.json` designed but no `ontology/` dir yet; `STRUCTURE.md` tree omits it. Build + reconcile when a course needs governed objectives. (§7)
- `script.primitives.v1` name collision — repo shape vs pack shape (§4)
- `intent.enum.json` pedagogical dimension is `draft_for_reconciliation`, not settled
- `conventions.md` is a stub (TODO) — the constitution-expanded is not yet written