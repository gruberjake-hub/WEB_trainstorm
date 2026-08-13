# Decision log — Course Engine / Manifold

*Running log of settled architectural decisions. Newest first. One entry = one decision that is
closed enough to build on; if it reopens, add a new dated entry rather than editing history.*

## 2026-08-10 — Ingest/headwater agent architecture is settled; next rung is the prompt pass

The ingest/decomposition agent is **not** greenfield — it is the **headwater authoring agent**
(`procedure-object-model.md`), now extended to a second source type via the **`form` facet**
(`form-object-model.md`, gated 11/11). Procedure and form are duals on one spine; the object-model
(process_model / form_model) is an **ingest view**, not the output-of-record (the atoms are). Facet
ownership is single-writer: this agent owns `meaning`, `object`, and the source-type facet
(`procedure` | `form`); intent / expression / audience / render are downstream readers. **Next real
rung: the prompt pass** — write the headwater agent's system + intake prompts against this settled
architecture, harvesting the bundle's prompts as raw material. Open items carried: mint 3 registry
seeds (`role_alsap_lead`, `rec_alsap`, `reg_benefit_risk_profile`); resolve the Benefit-Risk
controlled-vs-example SME question.

# Decision log — Course Engine / Manifold

*Running log of settled architectural decisions. Newest first. One entry = one decision that is
closed enough to build on; if it reopens, add a new dated entry rather than editing history.*

## 2026-08-12 — Carry: no owner yet for the authored affective / narrative arc (supra-atomic composition)

Surfaced by Jake's "is this too atomic?" check (use case: a course with a heavy learner-psychological
mapping component). Verdict: the design is **atomic, not atomist** — atoms carry relations (graph, not
chain), *containers are atoms too* so group-level properties bind to the container node (a section's
intensity ramp lives on the Section atom), and shared **closed registries** keep independent per-atom
style choices coherent. So the gestalt is not generally lost.

**The genuine gap it exposed:** psychological/narrative structure that is emergent across
**non-containment** relations — a callback (scene 2 → scene 40), a fear planted early / resolved late, a
recurring motif, a difficulty ramp spanning modules — has *no facet and no agent owner* today. `object`
owns structural relations, `intent` owns objective prerequisites, but the **authored affective/narrative
arc** as a first-class relation is homeless.

The clarifying split:
- **Authored arc** — the emotional/narrative structure the *designer* builds, independent of any learner.
  Content, supra-atomic, currently homeless. Near-term-ish; wants its **own clean pass** — do NOT graft it
  onto another agent's turn. Candidate: a new single-writer facet (working name `affect` / `narrative_arc`)
  bound to **container atoms** for containment and to **typed edges** for cross-cutting relations.
- **Per-learner psychological adaptation** — mapping to *this* learner's motivation/mastery/affect. That
  is the `audience` facet + the **Response Engine** (Chameleon's stub). Frontier, walled off, PII-free on
  the content side.

**Shape of the fix (keeps the philosophy):** make the arc **first-class** — a node or governed typed
relation, single-writer, keyed by IDs; atomic in the good sense (governed, inspectable, reusable), not
atomist. **Anti-pattern to avoid:** letting the arc live only in a render agent's runtime (emergent at
draw time, written nowhere) — that smuggles a supra-atomic truth outside the graph, the exact drift the
manifold exists to kill.

Status: **carry.** Sibling to the deferred ROI/goal node above objectives (same "real gap, cleanly
nameable" character).

## 2026-08-11 — Facet-owner spine adopted; Headwater re-expressed on it

Agent system prompts are now built as **spine + specialization**. `agents/_shared/facet_owner_spine.md`
holds the shared ~70% of every facet owner's contract (single-writer, wake-on-graph-state, vocab
governance, provenance + `source_hash` staleness, no-PII, uncertainty-surfacing, operating loop, drift
checks). Each agent is a small specialization that fills **seven slots**: name, one-line role, the facet
it writes + keys, wake condition, governed vocab refs, modes, schema refs. The spine is canonical and
referenced, never pasted into each agent (reference-don't-embed, applied to the prompts themselves).

- **Load-bearing generalization:** Headwater owns `content_hash` (hash of `meaning`). Every *other* facet
  owner records the `source_hash` it bound against, so "is this facet stale?" is one graph walk.
- **The one exception, documented not smuggled:** Headwater is the *origin writer* — it writes three
  things at birth (`meaning` + `object` + source-type). Single-writer is a rule *per facet*; each of the
  three still has exactly one writer. Every downstream owner writes exactly one facet.
- **Headwater modes settled and written into its prompt:** `direct` (bounded artifact → mint only) and
  `case_author` (large corpus → scope-commit → *durable committed-design artifact* → mint; the mint wakes
  on the artifact, is not handed anything). A lightweight **router** (haiku-class, writes nothing to the
  graph, emits a governed route label) is the single operator-facing front door that selects the mode.
- Files: `agents/_shared/facet_owner_spine.md`; `agents/headwater_ingest/02_system_prompts/core_agent/system_prompt.md` (v0.2-on-spine).

### Agent batch progress (rolling, under this spine)
- **Cartographer** (intent facet) — built, read-then-bind, no loop override needed; also maintains the
  objective ontology as its governed vocabulary. `agents/cartographer/…`.
- **Couturier** (expression · *style* sub-facet) — built. Proves the **sub-facet single-writer split**:
  `expression` has two writers divided **by key** — Couturier owns style keys (`style_ref`,
  text/motion/layout/interaction primitives, `content_type`, `visual_type`); Dragoman owns locale keys
  (locale packs, `term_refs`/glossary). Single-writer holds at *key* granularity. `agents/couturier/…`.
- **Dragoman** (expression · *locale* sub-facet — AST009, the one real agent), **Griot** (narration),
  **Chameleon** (audience — frontier stub) — pending.

## 2026-08-12 — Objectives ontology instantiated + STRUCTURE.md reconciled

The intent ontology is no longer a dangling design. Built and gated 7/7:
- `schemas/objectives.schema.json` — objective-store contract. Governed like the roles/records registries
  (`closed_list: true`, `obj_` prefix enforced, ungoverned ids rejected); grown only by entry + version
  bump. The schema currently **rejects** a `serves` field, so adding the (still un-designed) ROI/goal
  upward link later is a deliberate version bump, not accidental drift.
- `ontology/objectives.json` — seeded with only the objectives canon already names (`obj_recognize_psi`
  from atom-spec §4, plus `obj_define_psi` added as the root the example required but nothing defined —
  fixing a latent dangling prerequisite). Both `status: example`, provenance stamped.
- Validator checks: schema valid Draft 2020-12; seed validates; every `requires[]` resolves; prereq graph
  acyclic; and the negative controls (dangling ref, ungoverned id, premature `serves`) are all rejected.
- **STRUCTURE.md reconciled** (4 edits, byte-clean): `ontology/` added to the tree (beside `registry/` +
  `locales/`), a matching rule-table row, `objectives.schema.json` in the schemas block, and `ontology/*.json`
  added to the SYNC list. The `obj_` prefix was already governed there — the only real gap was the folder.
- **Per-project note:** the objective *schema* is shared core; an objective *instance* (e.g. Astellas PV)
  is per-project content. The shared-core / per-project line runs through the instance stores — a known
  thread (same as the Astellas glossary/corpus classification).

## 2026-08-11 — Deferred: prompt resolver + plain-language explainer (explainer = auto-dogfood candidate)

The spine + specialization split is DRY and machine-facing but adds indirection between a reviewer and
"the prompt itself." Two human-facing **projections** were identified to close that gap. Both deferred,
for different reasons. Discipline for both: one canonical source (spine + specialization); the projection
is *derived*, never authored directly — the same "deterministic projection of an engineering source of
truth" the content model already uses (atom store → controlled Word/PDF). Embedding/inlining is forbidden
in the source but fine in a projection (derived + disposable).

1. **Prompt resolver (compiler).** A small deterministic script that walks `agents/`, fills each agent's
   slots into the spine, and emits a fully-inlined `resolved_prompt.md` per agent. Render-only, never
   hand-edited — edit the spine/specialization and re-render. Cheap, buildable anytime, doubles as a build
   sanity-check. Deferred only because it is not on the path to building the agents. **Pick up whenever.**

2. **Plain-language explainer.** A further, *simplified* projection that translates an agent's rules into
   SME/stakeholder English. Lossy, audience-specific. **Best built as auto-dogfood, not by hand:** once the
   projection/render path exists, feed the manifold's own architecture + prompts in as a corpus (Headwater,
   Case-Author mode) → atoms → a plain-language projection. Deferring is the *right* call, not just triage —
   hand-built now vs. a near-free projection later, and it doubles as an end-to-end self-test on a corpus
   we understand completely. **Revisit after the projection/render path exists.**

## 2026-08-10 — Agent package folder structure locked (v0.1, "for now")

The numbered scaffold from the bundle's `Manifold_Rendering_Agent` is adopted as the standard
**agent operating-package** layout. Each agent folder gets:

```
<agent>/
  README.md
  01_operating_model/
  02_system_prompts/
    core_agent/
    modes/field_guide_mode/
  03_user_prompts/
    model_build_meta-mode/
    quick_starts/
  04_schemas/            # POINTERS to canon + agent-local operating schemas ONLY — see caveat
    canonical_models/
    overlays/
    render_profiles/
  05_modes/field_guide_mode/examples/
  07_examples/<worked_example>/
  08_governance/validation_checklists/
  09_team_guidance/how_to_run/
```

**Caveat (invariant guard):** canonical schemas and vocabularies do **not** get copied into an agent's
`04_schemas/`. They have one home — `cgen/trainstorm-core/schemas/` and `/vocab/`. Putting a copy in the
agent folder would spawn a second, drifting source of truth. `04_schemas/` holds *references* to the
canon schemas plus any agent-local operating schema (e.g. a render-profile config the agent alone uses).

**Where current artifacts land:**
- Headwater Ingest Agent core system prompt → `agents/headwater_ingest/02_system_prompts/core_agent/system_prompt.md`
- `form.facet.schema.json`, `vocab/form.enum.json` → **`cgen/trainstorm-core/`** (canon), *not* the agent's `04_schemas/`.

**Still open ("for now"):** `06` and `10` are unassigned; normalize the range when their contents are known.

## 2026-08-10 — Ingest/headwater agent architecture is settled; next rung is the prompt pass

The ingest/decomposition agent is **not** greenfield — it is the **headwater authoring agent**
(`procedure-object-model.md`), now extended to a second source type via the **`form` facet**
(`form-object-model.md`, gated 11/11). Procedure and form are duals on one spine; the object-model
(process_model / form_model) is an **ingest view**, not the output-of-record (the atoms are). Facet
ownership is single-writer: this agent owns `meaning`, `object`, and the source-type facet
(`procedure` | `form`); intent / expression / audience / render are downstream readers. **Next real
rung: the prompt pass** — write the headwater agent's system + intake prompts against this settled
architecture, harvesting the bundle's prompts as raw material. Open items carried: mint 3 registry
seeds (`role_alsap_lead`, `rec_alsap`, `reg_benefit_risk_profile`); resolve the Benefit-Risk
controlled-vs-example SME question.

Decision log — Course Engine / Manifold

Running log of settled architectural decisions. Newest first. One entry = one decision that is closed enough to build on; if it reopens, add a new dated entry rather than editing history.

2026-08-12 — Facet-owner batch COMPLETE (spine + 6 owners; Dragoman runtime reconciled)

The full facet-owner set is built on the spine — one shared contract + six specializations (five operating, one frontier stub). The spine held across every archetype with no loop override for any reader; the single documented exception is Headwater (origin writer, three facets). Each agent surfaced exactly one honest architectural note:

Headwater (meaning + object + source-type) — origin-writer exception; modes direct / case_author.
Cartographer (intent) — read-then-bind; also maintains the objective ontology as its governed vocabulary.
Couturier (expression · style) — single-writer holds at key granularity (the sub-facet split).
Dragoman (expression · locale — AST009) — retrieval memory (RAG) lives outside the graph-contract cleanly; reconcile mode = the SME human-in-the-loop template. The localize runtime (tools/localize/build_agent_call.py) was reconciled to load spine + specialization from the numbered path (interim "poor-man's resolver": concatenate the two files, spine first; prompt_version bumped to loc-agent.v0.2-spine, pending Jake's confirm). Folder stays agents/localize/; "Dragoman" is the display name.
Griot (narration) — first agent with a real ordering dependency (words before voice), expressed as a richer wake condition (reads Dragoman's validated locale), not an agent-to-agent call — the choreographed form of "sequencing where it matters."
Chameleon (audience) — stub only, frontier (Response Engine / Orchestrator). Holds the seat, documents the wall, enforces no-PII even as a placeholder.

Files: agents/{headwater_ingest,cartographer,couturier,localize,griot,chameleon}/02_system_prompts/core_agent/…

agents/_shared/facet_owner_spine.md.

Threads carried into the harness phase (Piece 2), see claude/handoff-piece2-harness.md: registries several agents are scaffolded ahead of (primitives.registry.json partial; voice/prosody registries absent); the draft pedagogical-intent vocab; the flat→numbered migration + git rm agents/localize/system.md to commit; the prompt_version stamp to confirm. Plus standing carries: affective-arc facet, ROI/goal node, prompt resolver + auto-dogfood explainer.

2026-08-12 — Carry: no owner yet for the authored affective / narrative arc (supra-atomic composition)

Surfaced by Jake's "is this too atomic?" check (use case: a course with a heavy learner-psychological mapping component). Verdict: the design is atomic, not atomist — atoms carry relations (graph, not chain), containers are atoms too so group-level properties bind to the container node (a section's intensity ramp lives on the Section atom), and shared closed registries keep independent per-atom style choices coherent. So the gestalt is not generally lost.

The genuine gap it exposed: psychological/narrative structure that is emergent across non-containment relations — a callback (scene 2 → scene 40), a fear planted early / resolved late, a recurring motif, a difficulty ramp spanning modules — has no facet and no agent owner today. object owns structural relations, intent owns objective prerequisites, but the authored affective/narrative arc as a first-class relation is homeless.

The clarifying split:

Authored arc — the emotional/narrative structure the designer builds, independent of any learner. Content, supra-atomic, currently homeless. Near-term-ish; wants its own clean pass — do NOT graft it onto another agent's turn. Candidate: a new single-writer facet (working name affect / narrative_arc) bound to container atoms for containment and to typed edges for cross-cutting relations.
Per-learner psychological adaptation — mapping to this learner's motivation/mastery/affect. That is the audience facet + the Response Engine (Chameleon's stub). Frontier, walled off, PII-free on the content side.

Shape of the fix (keeps the philosophy): make the arc first-class — a node or governed typed relation, single-writer, keyed by IDs; atomic in the good sense (governed, inspectable, reusable), not atomist. Anti-pattern to avoid: letting the arc live only in a render agent's runtime (emergent at draw time, written nowhere) — that smuggles a supra-atomic truth outside the graph, the exact drift the manifold exists to kill.

Status: carry. Sibling to the deferred ROI/goal node above objectives (same "real gap, cleanly nameable" character).

2026-08-11 — Facet-owner spine adopted; Headwater re-expressed on it

Agent system prompts are now built as spine + specialization. agents/_shared/facet_owner_spine.md holds the shared ~70% of every facet owner's contract (single-writer, wake-on-graph-state, vocab governance, provenance + source_hash staleness, no-PII, uncertainty-surfacing, operating loop, drift checks). Each agent is a small specialization that fills seven slots: name, one-line role, the facet it writes + keys, wake condition, governed vocab refs, modes, schema refs. The spine is canonical and referenced, never pasted into each agent (reference-don't-embed, applied to the prompts themselves).

Load-bearing generalization: Headwater owns content_hash (hash of meaning). Every other facet owner records the source_hash it bound against, so "is this facet stale?" is one graph walk.
The one exception, documented not smuggled: Headwater is the origin writer — it writes three things at birth (meaning + object + source-type). Single-writer is a rule per facet; each of the three still has exactly one writer. Every downstream owner writes exactly one facet.
Headwater modes settled and written into its prompt: direct (bounded artifact → mint only) and case_author (large corpus → scope-commit → durable committed-design artifact → mint; the mint wakes on the artifact, is not handed anything). A lightweight router (haiku-class, writes nothing to the graph, emits a governed route label) is the single operator-facing front door that selects the mode.
Files: agents/_shared/facet_owner_spine.md; agents/headwater_ingest/02_system_prompts/core_agent/system_prompt.md (v0.2-on-spine).
Agent batch progress (rolling, under this spine)
Cartographer (intent facet) — built, read-then-bind, no loop override needed; also maintains the objective ontology as its governed vocabulary. agents/cartographer/….
Couturier (expression · style sub-facet) — built. Proves the sub-facet single-writer split: expression has two writers divided by key — Couturier owns style keys (style_ref, text/motion/layout/interaction primitives, content_type, visual_type); Dragoman owns locale keys (locale packs, term_refs/glossary). Single-writer holds at key granularity. agents/couturier/….
Dragoman (expression · locale — AST009), Griot (narration), Chameleon (audience — frontier stub) — all built; see the 2026-08-12 batch-complete entry at the top.
2026-08-12 — Objectives ontology instantiated + STRUCTURE.md reconciled

The intent ontology is no longer a dangling design. Built and gated 7/7:

schemas/objectives.schema.json — objective-store contract. Governed like the roles/records registries (closed_list: true, obj_ prefix enforced, ungoverned ids rejected); grown only by entry + version bump. The schema currently rejects a serves field, so adding the (still un-designed) ROI/goal upward link later is a deliberate version bump, not accidental drift.
ontology/objectives.json — seeded with only the objectives canon already names (obj_recognize_psi from atom-spec §4, plus obj_define_psi added as the root the example required but nothing defined — fixing a latent dangling prerequisite). Both status: example, provenance stamped.
Validator checks: schema valid Draft 2020-12; seed validates; every requires[] resolves; prereq graph acyclic; and the negative controls (dangling ref, ungoverned id, premature serves) are all rejected.
STRUCTURE.md reconciled (4 edits, byte-clean): ontology/ added to the tree (beside registry/ + locales/), a matching rule-table row, objectives.schema.json in the schemas block, and ontology/*.json added to the SYNC list. The obj_ prefix was already governed there — the only real gap was the folder.
Per-project note: the objective schema is shared core; an objective instance (e.g. Astellas PV) is per-project content. The shared-core / per-project line runs through the instance stores — a known thread (same as the Astellas glossary/corpus classification).
2026-08-11 — Deferred: prompt resolver + plain-language explainer (explainer = auto-dogfood candidate)

The spine + specialization split is DRY and machine-facing but adds indirection between a reviewer and "the prompt itself." Two human-facing projections were identified to close that gap. Both deferred, for different reasons. Discipline for both: one canonical source (spine + specialization); the projection is derived, never authored directly — the same "deterministic projection of an engineering source of truth" the content model already uses (atom store → controlled Word/PDF). Embedding/inlining is forbidden in the source but fine in a projection (derived + disposable).

Prompt resolver (compiler). A small deterministic script that walks agents/, fills each agent's slots into the spine, and emits a fully-inlined resolved_prompt.md per agent. Render-only, never hand-edited — edit the spine/specialization and re-render. Cheap, buildable anytime, doubles as a build sanity-check. Deferred only because it is not on the path to building the agents. Pick up whenever. (Note: tools/localize/build_agent_call.py now does the interim concatenation this resolver would formalize — see the 2026-08-12 batch entry.)
Plain-language explainer. A further, simplified projection that translates an agent's rules into SME/stakeholder English. Lossy, audience-specific. Best built as auto-dogfood, not by hand: once the projection/render path exists, feed the manifold's own architecture + prompts in as a corpus (Headwater, Case-Author mode) → atoms → a plain-language projection. Deferring is the right call, not just triage — hand-built now vs. a near-free projection later, and it doubles as an end-to-end self-test on a corpus we understand completely. Revisit after the projection/render path exists.
2026-08-10 — Agent package folder structure locked (v0.1, "for now")

The numbered scaffold from the bundle's Manifold_Rendering_Agent is adopted as the standard agent operating-package layout. Each agent folder gets:

<agent>/
  README.md
  01_operating_model/
  02_system_prompts/
    core_agent/
    modes/field_guide_mode/
  03_user_prompts/
    model_build_meta-mode/
    quick_starts/
  04_schemas/            # POINTERS to canon + agent-local operating schemas ONLY — see caveat
    canonical_models/
    overlays/
    render_profiles/
  05_modes/field_guide_mode/examples/
  07_examples/<worked_example>/
  08_governance/validation_checklists/
  09_team_guidance/how_to_run/

Caveat (invariant guard): canonical schemas and vocabularies do not get copied into an agent's 04_schemas/. They have one home — cgen/trainstorm-core/schemas/ and /vocab/. Putting a copy in the agent folder would spawn a second, drifting source of truth. 04_schemas/ holds references to the canon schemas plus any agent-local operating schema (e.g. a render-profile config the agent alone uses).

Where current artifacts land:

Headwater Ingest Agent core system prompt → agents/headwater_ingest/02_system_prompts/core_agent/system_prompt.md
form.facet.schema.json, vocab/form.enum.json → cgen/trainstorm-core/ (canon), not the agent's 04_schemas/.

Still open ("for now"): 06 and 10 are unassigned; normalize the range when their contents are known.

2026-08-10 — Ingest/headwater agent architecture is settled; next rung is the prompt pass

The ingest/decomposition agent is not greenfield — it is the headwater authoring agent (procedure-object-model.md), now extended to a second source type via the form facet (form-object-model.md, gated 11/11). Procedure and form are duals on one spine; the object-model (process_model / form_model) is an ingest view, not the output-of-record (the atoms are). Facet ownership is single-writer: this agent owns meaning, object, and the source-type facet (procedure | form); intent / expression / audience / render are downstream readers. Next real rung: the prompt pass — write the headwater agent's system + intake prompts against this settled architecture, harvesting the bundle's prompts as raw material. Open items carried: mint 3 registry seeds (role_alsap_lead, rec_alsap, reg_benefit_risk_profile); resolve the Benefit-Risk controlled-vs-example SME question.


# Decision log — Course Engine / Manifold

*Running log of settled architectural decisions. Newest first. One entry = one decision that is
closed enough to build on; if it reopens, add a new dated entry rather than editing history.*

## 2026-08-13 — Carry (FRONTIER): the tutor learner-profile loop is a working prototype of the Response-Engine per-learner join

Surfaced by Jake mid-harness as a "side note." The pattern used to maintain *his own* tutor
learner-profile is structurally the **Response Engine's core loop**, run on a population of one (him,
fully consented). Same architecture as the content manifold, aimed at a different substrate:
- **Content side:** thin atoms; source meaning embedded; everything else *referenced*; resolved
  per-learner at render time.
- **Learner side:** a thin, living profile; updated by a growth loop (observe → update → hand back);
  *loaded into context at the start of the next session/course.*

That "profile loaded at course start" **is** atom-spec §5 step 4 — *the join*, where `audience`
fit-hooks meet the learner model at render/inference time. The tutor is effectively **Chameleon-for-one**;
we are already auto-dogfooding the responsive loop on the one safely-consented subject (same auto-dogfood
instinct as the plain-language explainer, 2026-08-11).

**Invariant lines this use case tests hardest (both already canon — restated, not new):**
- **Reference, don't embed.** The profile lives in the separately-governed **learner model**, keyed by
  employee id, and is *joined* into course context at load — never embedded in content atoms. ("Embedded
  in the transcript" is fine only if *transcript = the employee's own record*, not the course.)
- **No PII in content.** Content graph stays clean; all learner data sits in the walled, separately-governed
  learner model.

**New boundary this sharpens — the PII governance TIER.** A profile rich enough to be *useful* (the way
Jake's own is — identity, affect, self-model) is heavy PII with real consent/legal weight. So a per-employee
profile splits by tier: (a) fit-hooks + learning preferences — lighter-governed, closest to the existing
`audience` facet; (b) deep affective/psychological modeling — far more sensitive (consent, scope, access
control). The tier boundary constrains what the profile may hold *before* any design exists.

**Status: carry, FRONTIER.** Response Engine / Orchestrator = a separate project, walled off from the
near-term harness — do **not** build in the harness phase. Sibling to the Chameleon `audience` stub and the
affective/narrative-arc carry (2026-08-12). Seed captured so it isn't lost; many implications, deliberately
not unpacked here.

## 2026-08-13 — Piece 2 beta harness: thinnest end-to-end slice built + validated (SOP-AST-29080 / ALSAP)

The harness's first proof is real: **raw corpus → atoms → validation gate → deterministic projection**,
run end to end on a live Astellas SOP (SOP-AST-29080, ALSAP). 35 atoms (10 containers + 25 steps),
gate green (0 hard failures), and a controlled HTML document a GxP reviewer can react to — every clause
tracing back to an `atom_id` + `content_hash`. Built as a self-contained session package (`beta_harness/`),
**not yet in the repo**; landing = commit `registry_adds/` to the Astellas registries and place
schemas/store per STRUCTURE.md.

*(Update, later 2026-08-13: the SME **reconcile round-trip** noted below as "next rung" was subsequently
built this session — see the reconcile entry to be added; review matrix → SME markup → back to canon with
version bump + hash recompute + external `reconciliation_log.json` audit store. Registries also enriched
to `{id, label, description}` at v3.)*

**Settled (buildable):**
- **Atom store = git-native JSON in a per-project namespace** (`store/projects/<proj>/atoms.json`); a
  *walk* is a filter over the store. No database for the beta — a DB is the scaling move, not the beta move.
  The runner is thin Python (`headwater_ingest` / `validate_atoms` / `adopt_registries` / `project_sop`).
- **Gate policy (generalizes `validate.py` / `validate_objectives.py`):** three layers — schema, drift,
  vocab-conformance. HARD failures (schema-invalid / unresolved ref / hash mismatch / **ungoverned-and-
  unproposed** value) block at any status. PROPOSED-pending values pass at `draft`, block promotion to
  `in_review`/`approved` until adopted. **"Flag, never invent" is now a gate verdict, not a slogan.**
- **Router run by hand** for v1 (`direct` mode chosen manually); not automated yet.

**Load-bearing finding — cited controlled docs are GOVERNED references, not free text.** Verifying the
reconstructed procedure facet against the real `procedure.facet.schema.json` (Jake supplied it) caught the
one real drift: `references` must match `^(doc|atom)_`. Raw doc numbers (`SOP-1798`, `WPD-981`, …) were
non-conformant. Fix: they become `doc_` ids (`doc_sop_1798`), and a **`doc_` controlled-document registry**
now governs them — **client-level** (the same `doc_sop_1798` is cited across many Astellas SOPs), governed
once in the Astellas namespace like roles/records. This sharpens the procedure facet's operational meaning:
`references` join into a governed namespace.

**Registry tiers clarified (answers the "client vs project" question):** the governance *pattern*
(`closed_list`, prefix rule, extend-by-version-bump) is **shared core**; *entries* live at the lowest level
still reused without forking. Universal structural vocab (`step_type`; future `list`/`list_item`) →
shared core. Client roles/records/docs (ALSAP roles, `rec_alsap`, `doc_*`) → **Astellas client namespace**.
Project scope is reserved/discouraged (forking risk). Proposals **stage** in the project store
(`proposed_registry_extensions.json`) then get **promoted UP** into the client registry on adoption; the
project then only *references* the governed ids and the staging pen is **dropped** (no shadow copy).

**Adopted this pass (owed seeds delivered):** roles +10 (incl. the owed `role_alsap_lead`), records +4
(incl. the owed `rec_alsap`), docs +13. Registries version-bumped to v2; commit payloads in
`registry_adds/`; gate reads **PROMOTE PASS** post-adoption. (Staged in the beta package — commit to the
real Astellas registries to land. `reg_benefit_risk_profile` remains owed: BRT appears here only as a role.)

**Decision — Safety Programmer Developer vs. Validator → ONE role + a per-step `duty` attribute** (not two
roles). Keeps `role_safety_programmer` clean and puts the SoD distinction where it varies (per step).
Requires a **procedure facet version bump** — `performed_by` is array-of-strings and the facet is
`additionalProperties:false`, so `duty` cannot be smuggled in locally; make it a repo change
(`performed_by → [{role, duty}]` or a parallel `duties` field).

**Carries opened/updated:**
- **`list` / `list_item` as a shared-core structural kind** (NOT `procedure.enum` — a list isn't
  procedural; forms and courses have them too). Front-matter narrative lists were **flagged, not smashed**
  (procedure.enum has no list kind); re-decompose once the shared kind exists.
- Embedded conditional in ALSAP B.s2 ("if an approved ALSAP exists") — candidate `decision` step; kept
  atomic + flagged.
- Schema verification still owed for **`atom.schema.json`** (still vendored) and **`procedure.enum.json`**
  (real facet's `$comment` says `step_type` lives under `dimensions.step_type`; the vendored flat copy
  doesn't mirror that).
- The projection is Word/PDF/HTML-class; the SME **reconcile round-trip** (markup → back to canon w/
  version bump + hash recompute) is the next rung, not built this pass.

## 2026-08-12 — Facet-owner batch COMPLETE (spine + 6 owners; Dragoman runtime reconciled)

The full facet-owner set is built on the spine — one shared contract + six specializations (five
operating, one frontier stub). The spine held across every archetype with **no loop override for any
reader**; the single documented exception is Headwater (origin writer, three facets). Each agent surfaced
exactly one honest architectural note:

- **Headwater** (`meaning` + `object` + source-type) — origin-writer exception; modes `direct` / `case_author`.
- **Cartographer** (`intent`) — read-then-bind; also maintains the objective ontology as its governed vocabulary.
- **Couturier** (`expression` · *style*) — single-writer holds at *key* granularity (the sub-facet split).
- **Dragoman** (`expression` · *locale* — AST009) — retrieval memory (RAG) lives outside the graph-contract
  cleanly; `reconcile` mode = the SME human-in-the-loop template. **The `localize` runtime
  (`tools/localize/build_agent_call.py`) was reconciled** to load spine + specialization from the numbered
  path (interim "poor-man's resolver": concatenate the two files, spine first; `prompt_version` bumped to
  `loc-agent.v0.2-spine`, pending Jake's confirm). Folder stays `agents/localize/`; "Dragoman" is the
  display name.
- **Griot** (`narration`) — first agent with a real ordering dependency (words before voice), expressed as
  a *richer wake condition* (reads Dragoman's **validated** locale), not an agent-to-agent call — the
  choreographed form of "sequencing where it matters."
- **Chameleon** (`audience`) — **stub only**, frontier (Response Engine / Orchestrator). Holds the seat,
  documents the wall, enforces no-PII even as a placeholder.

Files: `agents/{headwater_ingest,cartographer,couturier,localize,griot,chameleon}/02_system_prompts/core_agent/…`
+ `agents/_shared/facet_owner_spine.md`.

**Threads carried into the harness phase (Piece 2), see `claude/handoff-piece2-harness.md`:** registries
several agents are scaffolded ahead of (`primitives.registry.json` partial; voice/prosody registries
absent); the draft pedagogical-intent vocab; the flat→numbered migration + `git rm agents/localize/system.md`
to commit; the `prompt_version` stamp to confirm. Plus standing carries: affective-arc facet, ROI/goal
node, prompt resolver + auto-dogfood explainer.

## 2026-08-12 — Carry: no owner yet for the authored affective / narrative arc (supra-atomic composition)

Surfaced by Jake's "is this too atomic?" check (use case: a course with a heavy learner-psychological
mapping component). Verdict: the design is **atomic, not atomist** — atoms carry relations (graph, not
chain), *containers are atoms too* so group-level properties bind to the container node (a section's
intensity ramp lives on the Section atom), and shared **closed registries** keep independent per-atom
style choices coherent. So the gestalt is not generally lost.

**The genuine gap it exposed:** psychological/narrative structure that is emergent across
**non-containment** relations — a callback (scene 2 → scene 40), a fear planted early / resolved late, a
recurring motif, a difficulty ramp spanning modules — has *no facet and no agent owner* today. `object`
owns structural relations, `intent` owns objective prerequisites, but the **authored affective/narrative
arc** as a first-class relation is homeless.

The clarifying split:
- **Authored arc** — the emotional/narrative structure the *designer* builds, independent of any learner.
  Content, supra-atomic, currently homeless. Near-term-ish; wants its **own clean pass** — do NOT graft it
  onto another agent's turn. Candidate: a new single-writer facet (working name `affect` / `narrative_arc`)
  bound to **container atoms** for containment and to **typed edges** for cross-cutting relations.
- **Per-learner psychological adaptation** — mapping to *this* learner's motivation/mastery/affect. That
  is the `audience` facet + the **Response Engine** (Chameleon's stub). Frontier, walled off, PII-free on
  the content side.

**Shape of the fix (keeps the philosophy):** make the arc **first-class** — a node or governed typed
relation, single-writer, keyed by IDs; atomic in the good sense (governed, inspectable, reusable), not
atomist. **Anti-pattern to avoid:** letting the arc live only in a render agent's runtime (emergent at
draw time, written nowhere) — that smuggles a supra-atomic truth outside the graph, the exact drift the
manifold exists to kill.

Status: **carry.** Sibling to the deferred ROI/goal node above objectives (same "real gap, cleanly
nameable" character).

## 2026-08-11 — Facet-owner spine adopted; Headwater re-expressed on it

Agent system prompts are now built as **spine + specialization**. `agents/_shared/facet_owner_spine.md`
holds the shared ~70% of every facet owner's contract (single-writer, wake-on-graph-state, vocab
governance, provenance + `source_hash` staleness, no-PII, uncertainty-surfacing, operating loop, drift
checks). Each agent is a small specialization that fills **seven slots**: name, one-line role, the facet
it writes + keys, wake condition, governed vocab refs, modes, schema refs. The spine is canonical and
referenced, never pasted into each agent (reference-don't-embed, applied to the prompts themselves).

- **Load-bearing generalization:** Headwater owns `content_hash` (hash of `meaning`). Every *other* facet
  owner records the `source_hash` it bound against, so "is this facet stale?" is one graph walk.
- **The one exception, documented not smuggled:** Headwater is the *origin writer* — it writes three
  things at birth (`meaning` + `object` + source-type). Single-writer is a rule *per facet*; each of the
  three still has exactly one writer. Every downstream owner writes exactly one facet.
- **Headwater modes settled and written into its prompt:** `direct` (bounded artifact → mint only) and
  `case_author` (large corpus → scope-commit → *durable committed-design artifact* → mint; the mint wakes
  on the artifact, is not handed anything). A lightweight **router** (haiku-class, writes nothing to the
  graph, emits a governed route label) is the single operator-facing front door that selects the mode.
- Files: `agents/_shared/facet_owner_spine.md`; `agents/headwater_ingest/02_system_prompts/core_agent/system_prompt.md` (v0.2-on-spine).

### Agent batch progress (rolling, under this spine)
- **Cartographer** (intent facet) — built, read-then-bind, no loop override needed; also maintains the
  objective ontology as its governed vocabulary. `agents/cartographer/…`.
- **Couturier** (expression · *style* sub-facet) — built. Proves the **sub-facet single-writer split**:
  `expression` has two writers divided **by key** — Couturier owns style keys (`style_ref`,
  text/motion/layout/interaction primitives, `content_type`, `visual_type`); Dragoman owns locale keys
  (locale packs, `term_refs`/glossary). Single-writer holds at *key* granularity. `agents/couturier/…`.
- **Dragoman** (expression · locale — AST009), **Griot** (narration), **Chameleon** (audience — frontier
  stub) — **all built; see the 2026-08-12 batch-complete entry at the top.**

## 2026-08-12 — Objectives ontology instantiated + STRUCTURE.md reconciled

The intent ontology is no longer a dangling design. Built and gated 7/7:
- `schemas/objectives.schema.json` — objective-store contract. Governed like the roles/records registries
  (`closed_list: true`, `obj_` prefix enforced, ungoverned ids rejected); grown only by entry + version
  bump. The schema currently **rejects** a `serves` field, so adding the (still un-designed) ROI/goal
  upward link later is a deliberate version bump, not accidental drift.
- `ontology/objectives.json` — seeded with only the objectives canon already names (`obj_recognize_psi`
  from atom-spec §4, plus `obj_define_psi` added as the root the example required but nothing defined —
  fixing a latent dangling prerequisite). Both `status: example`, provenance stamped.
- Validator checks: schema valid Draft 2020-12; seed validates; every `requires[]` resolves; prereq graph
  acyclic; and the negative controls (dangling ref, ungoverned id, premature `serves`) are all rejected.
- **STRUCTURE.md reconciled** (4 edits, byte-clean): `ontology/` added to the tree (beside `registry/` +
  `locales/`), a matching rule-table row, `objectives.schema.json` in the schemas block, and `ontology/*.json`
  added to the SYNC list. The `obj_` prefix was already governed there — the only real gap was the folder.
- **Per-project note:** the objective *schema* is shared core; an objective *instance* (e.g. Astellas PV)
  is per-project content. The shared-core / per-project line runs through the instance stores — a known
  thread (same as the Astellas glossary/corpus classification).

## 2026-08-11 — Deferred: prompt resolver + plain-language explainer (explainer = auto-dogfood candidate)

The spine + specialization split is DRY and machine-facing but adds indirection between a reviewer and
"the prompt itself." Two human-facing **projections** were identified to close that gap. Both deferred,
for different reasons. Discipline for both: one canonical source (spine + specialization); the projection
is *derived*, never authored directly — the same "deterministic projection of an engineering source of
truth" the content model already uses (atom store → controlled Word/PDF). Embedding/inlining is forbidden
in the source but fine in a projection (derived + disposable).

1. **Prompt resolver (compiler).** A small deterministic script that walks `agents/`, fills each agent's
   slots into the spine, and emits a fully-inlined `resolved_prompt.md` per agent. Render-only, never
   hand-edited — edit the spine/specialization and re-render. Cheap, buildable anytime, doubles as a build
   sanity-check. Deferred only because it is not on the path to building the agents. **Pick up whenever.**
   *(Note: `tools/localize/build_agent_call.py` now does the interim concatenation this resolver would
   formalize — see the 2026-08-12 batch entry.)*

2. **Plain-language explainer.** A further, *simplified* projection that translates an agent's rules into
   SME/stakeholder English. Lossy, audience-specific. **Best built as auto-dogfood, not by hand:** once the
   projection/render path exists, feed the manifold's own architecture + prompts in as a corpus (Headwater,
   Case-Author mode) → atoms → a plain-language projection. Deferring is the *right* call, not just triage —
   hand-built now vs. a near-free projection later, and it doubles as an end-to-end self-test on a corpus
   we understand completely. **Revisit after the projection/render path exists.**

## 2026-08-10 — Agent package folder structure locked (v0.1, "for now")

The numbered scaffold from the bundle's `Manifold_Rendering_Agent` is adopted as the standard
**agent operating-package** layout. Each agent folder gets:

```
<agent>/
  README.md
  01_operating_model/
  02_system_prompts/
    core_agent/
    modes/field_guide_mode/
  03_user_prompts/
    model_build_meta-mode/
    quick_starts/
  04_schemas/            # POINTERS to canon + agent-local operating schemas ONLY — see caveat
    canonical_models/
    overlays/
    render_profiles/
  05_modes/field_guide_mode/examples/
  07_examples/<worked_example>/
  08_governance/validation_checklists/
  09_team_guidance/how_to_run/
```

**Caveat (invariant guard):** canonical schemas and vocabularies do **not** get copied into an agent's
`04_schemas/`. They have one home — `cgen/trainstorm-core/schemas/` and `/vocab/`. Putting a copy in the
agent folder would spawn a second, drifting source of truth. `04_schemas/` holds *references* to the
canon schemas plus any agent-local operating schema (e.g. a render-profile config the agent alone uses).

**Where current artifacts land:**
- Headwater Ingest Agent core system prompt → `agents/headwater_ingest/02_system_prompts/core_agent/system_prompt.md`
- `form.facet.schema.json`, `vocab/form.enum.json` → **`cgen/trainstorm-core/`** (canon), *not* the agent's `04_schemas/`.

**Still open ("for now"):** `06` and `10` are unassigned; normalize the range when their contents are known.

## 2026-08-10 — Ingest/headwater agent architecture is settled; next rung is the prompt pass

The ingest/decomposition agent is **not** greenfield — it is the **headwater authoring agent**
(`procedure-object-model.md`), now extended to a second source type via the **`form` facet**
(`form-object-model.md`, gated 11/11). Procedure and form are duals on one spine; the object-model
(process_model / form_model) is an **ingest view**, not the output-of-record (the atoms are). Facet
ownership is single-writer: this agent owns `meaning`, `object`, and the source-type facet
(`procedure` | `form`); intent / expression / audience / render are downstream readers. **Next real
rung: the prompt pass** — write the headwater agent's system + intake prompts against this settled
architecture, harvesting the bundle's prompts as raw material. Open items carried: mint 3 registry
seeds (`role_alsap_lead`, `rec_alsap`, `reg_benefit_risk_profile`); resolve the Benefit-Risk
controlled-vs-example SME question.