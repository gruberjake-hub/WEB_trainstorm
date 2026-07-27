# Unification Map — Four Layers, One Machine

*2026-07-24 · Reconciles the Course_Builder handoff (ADRA_PIPELINE_v2, PROFILE_*_v2,
MANIFOLD_HANDOFF) and Jake's expression-nature notes against trainstorm-core. Companion to
`architecture/manifold.md` and `claude/promptpack-manifold-map.md`. Proposed home:
`trainstorm-core/architecture/`.*

---

## 0. The verdict in three sentences

Nothing in the archaeology is a rival architecture; every layer is a **partial discovery of
the same manifold**, each strongest where the others are blind. The handoff's proposal to
"invert CREATOR_v2 to the canonical centre" is rejected — that would mint a second canonical
source beside `element.schema.json`, violating *one canonical source*. Instead, every legacy
artifact **dissolves into the existing substrate**: its novel fields become facet upgrades,
its stages become agents/tools/skills placed by the grouping rule in §3, and its prompts
become the implementation behind contracts the graph already defines.

---

## 1. The archaeology, settled

| Layer | When | What it is | What it uniquely contributed | What it lacked |
|---|---|---|---|---|
| **Prompt pack** | Oct 2025 | End-to-end generation chain | The generator + realizer fill (already mapped in promptpack-manifold-map.md) | Stable IDs, substrate |
| **Four profiles** (Azure) | — | Role-separated ADDIE chain: LEADER → GENERATOR → DESIGNER → CREATOR | **Provenance discipline** (`source_reference` per step), authority-graded context, the divergent pass, the review loop, the response-feature assessment form | Substrate model, render targets, stable IDs |
| **ADRA** | — | 19-stage inference pipeline | **The substrate band (S6.1–S7)** — the only learner-psychology model anywhere; render emitters (PPTX/XLSX/VTT/XLIFF); composite indices | Provenance, divergence, a closed loop, render-agnostic units |
| **Manifold** (trainstorm-core) | Jul 2026 | The data architecture | Stable IDs, facets, single-writer, content_hash, governed vocabularies, the audience join | Populated learner model, warrant gate, evidence loop |

Both legacy systems independently produced **falsifiable claims about learners**
(`misconception_predictions`, `observables`, `rationalization_pattern`, `risk_of_overuse`)
that nothing consumes. That unconsumed hypothesis surface is the compounding asset — it is
what the Responsive Engine will eventually run posteriors over.

---

## 2. Where everything lands (the dissolution table)

The handoff's band structure maps onto the manifold almost 1:1. Bands were the same idea
discovered from the pipeline side.

| Handoff band | Manifold home | What moves there |
|---|---|---|
| **WARRANT** (absent — GAP-05) | **The missing `goal_` node** (promptpack map §7) + a hard gate in the Strategist | The intervention warrant IS the business-outcome node: no `goal_`, no project. Three independent analyses (LEADER regen note 2, GAP-05, promptpack §7) all found this same missing top rung. One fix closes all three. |
| **Band A — Constraint** | `governance` facet + a **source store with authority bands** | `source_context` / `project_context` become authority levels on source material (authoritative → citable; formative → implicit). `context_capsule` = the machine-readable slice. `regulatory_binding` already encodes the consequence. |
| **Band B-mat** (material) | **The content graph** (elements + script primitives + intent ontology) | CREATOR_v2 dissolves: `learning_objectives` → `ontology/objectives.json` nodes (+ `competency_type`); `content_structure` → object facet; `scenario_blocks[].steps` → an upgraded `knowledge_check` primitive (§4); `observables` → objective-node measurement model; `source_reference` → per-element provenance (already designed). ADRA S1–S4 dissolve into Strategist/Designer analysis skills. |
| **Band B-sub** (subject) | **The learner/audience model** — the sibling graph | ADRA S6.1–S7 in full: affective, cadence, empathy, meaning, inhibitor, motivator, composite indices — keyed to audience **segments** at design time, to individual learners at runtime. This is not content and never touches the content graph; it populates the graph your audience-axis diagram drew empty. **KEEP-04: preserve, don't reconcile — it has no counterpart anywhere.** |
| **Band C — Expression** | Expression registries + **render agents** (all equal citizens) | Storyboard, PPTX, Storyline-native XLSX, SCORM, VTT, XLIFF, asset briefs — each a render target reading the same substrate. CONFLICT-02 resolved by naming two targets (`storyline_native_xlsx`, `internal_exchange_csv`), never one masquerading as the other. Storyboard loses its privileged status; S5 (Pass A scaffold) is deleted, not migrated. |
| **EVIDENCE** (absent — GAP-06) | **The Responsive Engine** (frontier project) | Learner response → posterior over composite indices + misconception priors. Already designed as the join in the audience axis. The legacy systems' unconsumed predictions become its priors. |

**Protected during unification** (per the handoff, endorsed):
- The substrate band (B-sub) will look like dead weight — most fields have no consumer yet. They are the priors for the Responsive Engine. Do not flatten.
- `risk_of_overuse` (S6.6) is the only harm model in any layer. Promote it to a **gate** in the responsive join, not a metadata note. A substrate-aware engine without a harm model is an optimizer pointed at a human.

---

## 3. The grouping rule — agent vs prompt chain vs tool vs skill

The manifold already contains the test. Apply it to every legacy piece and the sorting is
mechanical:

> **Agent** — owns a facet (single-writer), wakes on graph state, coordinates only through
> the graph. The *ownership boundary* is what makes something an agent.
> **Prompt chain** — a sequence of stages *inside one ownership boundary*. Implementation
> detail of an agent; invisible to the graph.
> **Tool** — deterministic code. No judgment, no temperature. Validators, extractors,
> QE gates, renderers, hashers.
> **Skill** — loadable expertise an agent invokes *on demand*. Packaged prompts + method
> (the psykido prompts are a skill, not an agent).

The roster:

| Legacy piece | Becomes | Why |
|---|---|---|
| LEADER | **Strategist agent** (writes: `goal_` nodes, project dossier, warrant) | Owns the outcome facet. Gains the warrant gate (GAP-05) and an output schema — currently the only unversionable artifact in any chain. |
| GENERATOR (profile) | **Divergent mode of the generation agents**, not a standalone agent | It owns no facet — it produces candidates. Divergence is a *temperature setting + candidate envelope* (stable candidate IDs, logged selection), available to Strategist, Designer, and the script generator alike. ADRA's S10b moodboards were the vestigial trace of the same need. |
| DESIGNER_A | **Designer agent** (writes: intent facets, objectives, audience segment scope) | Owns pedagogical intent + the objective ontology. Dual-mode survives — |
| DESIGNER_B | **Validator tool + review gate**, not an agent mode | Payload-vs-schema checking is deterministic (the linter); SOP-alignment judgment stays a human gate. Schema invariants live in ONE validator, never restated as prose obligations (DESIGNER regen note 3). |
| CREATOR | **Dissolved.** Schema → substrate upgrades (§2); "compile" → the realizer | A deterministic compiler with zero temperature is not an agent — it was always the realizer + validator wearing a role costume. |
| SIMULATOR (reserved, never built) | **The Responsive Engine** (frontier) | OPEN-05 answered: three profiles reserved territory for the runtime band; the manifold already designed it. |
| ADRA S0 | **Ingestion tools** (py extractors) + Strategist intake | Already matches the prompt-pack loaders. |
| ADRA S1–S3 | **Analysis skills** loaded by Strategist/Designer | Audience/outcome analysis at survey depth. |
| ADRA S4 (Script_Normalizer) | **Generator agent** (source → script primitives) | With LEAK-05 fixed: segmentation emits primitives, never screens. |
| ADRA S6.1–S6.6 + S7 (psykido) | **Audience-analysis skills** loaded by the **Audience agent** (writes: the learner/audience model, segment-level) | One agent owns the sibling graph; the six builders are its deep-analysis skillset, invoked selectively (§5). |
| ADRA S8 (Storyboard B) | **A render agent** | One render target among equals. |
| ADRA S9 (Assessment) | **Deleted as a stage**; assessment = primitive + realization (§4) | CONFLICT-01 resolved. |
| ADRA S10a / S10b | **Asset-brief render target** + divergent mode | S10b's orphaned moodboards = divergence without a selection contract; fixed by the candidate envelope. |
| ADRA S11 (QA_Exporter) | **Render agents**, one per named target | Emitters split per CONFLICT-02. |

Note what happened to ADDIE: **Strategist → Designer → Developer survives as choreography
ordering** (which gates fire in what sequence), not as architecture. The agents still meet
only on the graph. The "loses coherence between Designer and Generator" problem you saw in
Azure was the cost of role-to-role handoffs carrying meaning in prose; facet writes carry it
in schema, which is why coherence stops decaying.

---

## 4. The assessment unification (the single highest-value schema change)

Adopt the handoff's CONFLICT-01 resolution, expressed as an upgrade to
`script.primitives.v1.json` → **v2 version bump** (governed vocab, so this is the legal
route):

```jsonc
// knowledge_check, v2 — describes what a correct response CONTAINS,
// not lettered options. MC/MR/TF/matching/sequence become RENDERS of it.
{
  "type": "knowledge_check",
  "prompt": "…",
  "check_type": "recall | application | scenario",
  "expected_response_features": ["…"],          // from CREATOR_v2 — the semantic key
  "misconception_predictions": [                 // structured, not free text (Phase 4 prep)
    { "id": "mc_001", "claim": "…", "confidence": 0.6 }
  ],
  "feedback_correct": "…",
  "feedback_incorrect": "…",
  "source_reference": "…"                        // provenance, per step
}
```

- The realizer generates `options[]` at realization time: the key from
  `expected_response_features`, distractors from `misconception_predictions` — run as a
  **divergent pass** (the GENERATOR finding its real job). This fixes distractor quality
  (GAP-01) structurally: wrong answers come from stated hypotheses about learners, not
  invented alongside the key.
- ADRA's A–D fixed labels (LEAK-08) and the 10-choice Storyline capacity both stop being
  schema problems — they're render parameters.
- `observables` (`evidence_of_mastery` / `evidence_of_error`) attach to **objective nodes**
  in the ontology: they are the likelihood function the Responsive Engine will need. A
  measurement model, stored where the thing being measured lives.

One move collapses CONFLICT-01, LEAK-08, GAP-01, and pre-wires Phase 4.

---

## 5. Where "the nature of expression" lives (your dispatcher question)

Your instinct — some mind decides the *nature* of expression from the deltas, and that
decision selects which deep analysis runs — is right, and it has a precise home:

- **It is a Designer decision, informed by a cheap Audience-agent survey.** Sequence:
  Strategist writes `goal_` + constraints → Audience agent runs *survey-depth* analysis
  (ADRA S1-level) → Designer reads both and classifies the gap: **large delta / potent
  inhibitors → persuasive nature; technical gap → didactic/clarity nature; skill gap →
  practice-heavy nature.**
- **The classification is written as data, not passed as a message**: it lands in the
  intent facet (dominant pedagogical strategy, rhetorical weighting) and in the audience
  facet (`segment_scope`, and a flag for depth-of-analysis required).
- **Progressive deepening is the token-economics loop you described**: only when the
  nature is persuasive does the Audience agent load the psykido skills (S6.1–S6.6) and
  write the deep substrate model. No persuasive nature → no deep pass → no burned tokens.
  The loop is legal because it never crosses an ownership boundary: the Audience agent
  deciding how deep to analyze is an agent's internal judgment, not coordination.
- **And the sequencing answer**: the "persuasive agent" outputs *to no one*. It writes
  segment psychographics (inhibitors, motivators, objections, aligners) into the learner/
  audience model. The Designer reads them to shape objectives; the generator reads them to
  shape moves (a `context_frame` targeting a named inhibitor); the realizer reads them to
  route expression; one day the Responsive Engine reads them as priors. Analysis upstream
  of script — as you suspected it had to be — and the "later pass that conforms observations
  into actionable language" is simply each downstream agent reading the facet for its own
  purpose. No conforming pass needed; the schema IS the conformance.

---

## 6. Decisions Jake owns (open, blocking, ordered)

1. **Ratify the dissolution** (this doc's §2–3) over the handoff's CREATOR-inversion. —
   *Blocks everything; costs one decision.*
2. **OPEN-03**: is the substrate model segment-scoped, per-unit, or both (design-time
   segments + runtime trajectories)? Recommended: **both**, matching the audience-axis
   diagram's two forms. — *Blocks the learner-model schema.*
3. **CONFLICT-01 adoption**: bump `script.primitives` to v2 with the response-feature
   `knowledge_check`. — *Blocks assessment work; §4 is the draft.*
4. **Warrant gate placement** (OPEN-06): above the Strategist or its first act?
   Recommended: **its first act** — the warrant is the `goal_` node's existence test.
5. **Naming**: retire "ADRA" (undefined expansion, OPEN-01) and the profile names; the
   agents get manifold names (Strategist, Designer, Audience, Generator, Realizer, Render,
   Governance, Responsive).

## 7. Build order (non-destructive first, per the handoff's phasing — endorsed)

1. `goal_` node + warrant gate + Strategist output schema (closes GAP-05, promptpack §7,
   LEADER note 2 in one artifact).
2. Split the Storyline emitters into two named render targets (delivery value, zero risk).
3. Candidate envelope for divergent passes (IDs + logged selection — auditability).
4. `script.primitives` v2 (§4) + realizer distractor pass.
5. Learner/audience model schema seeded from B-sub (after decision 2), `risk_of_overuse`
   promoted to a gate.
6. Evidence loop — Responsive Engine territory; frontier, not near-term.

*Steps 1–4 are production-pipeline work. Steps 5–6 begin the frontier.*
