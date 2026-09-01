# LRE Stage 1 — the Synthetic Learner (design record + build plan)

*Canonical copy. Written 2026-09-01 from the design conversation of that day; the Claude Project doc
of the same name is a one-way snapshot of this file. Status of each part is marked inline.
Companion to `capability_horizon/learner-response-intelligence.capability-horizon.md` (the horizon
this is the first rung of) and `agents-roster.md` (the Audience Agent and the Responsive Engine).*

---

## 1. The idea (Jake's)

The Learner Response Engine (LRE) is frontier because it responds in realtime with no human in the
loop. Develop it in two stages. **Stage 1** is one-directional: the system generates a *static*
course against a **synthetic learner** — an audience segment enacted as a persona, standing in for
the people who will take it. This captures the psychological primitives in relation to a defined
audience and lays the foundation from which the true LRE (Stage 2: live, per-learner) can unfold.

The manifold anticipated this. The roster's Audience Agent already owns "the sibling graph — the
learner/audience model — populations, not persons"; the Responsive Engine is "the only one who knows
both graphs and the only one who meets the learner"; the audience-join diagram names two forms of the
learner model, design-time segments and runtime individuals. Stage 1 builds the design-time form and
the join, with a segment record where the live learner will later sit.

## 2. The hinge — one contract, two stages · BUILT (this hop)

The planner that decides how content should *land* for a learner reads a **learner-state object**
and writes direction bindings with reason traces. It must not be able to tell whether that object is
synthetic or live.

| stage | the state object | written by | governance |
|---|---|---|---|
| 1 | a **segment record** (`kind: segment`) — one per audience segment, static | Audience Agent | content-project store, `audience/<segment_id>.json`, no PII by construction |
| 2 | a **live learner record** (`kind: learner`, reserved) — per person, updated from evidence | Responsive Engine | separate learner-data domain; **never** in a content project store (the gate rejects it there) |

Written against one schema, Stage 2 becomes a change of *input source*, not of architecture.

**`schemas/audience-model.schema.json`** (audience-model.v0.1) is that schema — the Audience
Agent's write contract, seeded from Band B-sub (ADRA S6.1–S6.6 + S7) per unification-map §6 step 5:

- `standing` — survey depth (S1): role, tier, experience, `mastery[]` **keyed by `obj_` ids**.
- `disposition` — the deep pass (S6.3–S6.6): inhibitors, objections, aligners, identity threats,
  belief gaps, meaning anchors, rationalization patterns, affective pattern. Every factor = governed
  id (`vocab/disposition.enum.json`) + strength + `basis` + **`risk_of_overuse`**.
- `baselines` — S7 composite indices, **exactly four**: self_efficacy, risk_sensitivity,
  identity_safety, trust. (§4 below.)
- `cadence` — S6.2: chunk/density tolerance, pace, interaction appetite.
- `governance` — version/status/owner/generated_by/`source_hash` (of the audience analysis) —
  a moved hash means the record, and any per-segment bindings, are stale.

Gate: **`tools/validate_audience.py`** — schema · vocab governance (approved records may not cite
`seed` entries) · harm gate · learner-domain boundary · objective anchoring · segment_id uniqueness.
Selftest proves red on twelve mutations. Reference: `reference/example_audience_segment.json`.

### Why the state joins through objectives, not elements

"The persona knows what it's meant to learn, never which statement on which slide." Jake asked
whether that costs anything. It doesn't — the joins compose:

- **state ↔ objectives** (`mastery[].objective_id`, `factor.objective_ids`): what the population
  knows/believes. Portable across courses; survives re-export (`ele_` ids may be re-minted,
  `obj_` ids don't).
- **planner → element_id**: where direction bindings land.
- **evidence ← element_id → objectives**: what happened at an element rolls up through
  `intent.teaches[]`; that is how mastery gets updated.

Element-keyed state would weld a segment to one course's structure. Objective-keyed state is what
makes the segment reusable and the loop in §6 possible.

## 3. `risk_of_overuse` is a gate · BUILT (contract) / DEFERRED (planner behavior)

The roster's one hard ethical rule, unification-map §2: "promote it to a gate in the responsive
join, not a metadata note — a substrate-aware engine without a harm model is an optimizer pointed at
a human." It is carried on the thing it protects: every disposition factor requires
`risk_of_overuse {level, basis}`. The gate refuses an approved record whose high-risk factor is not
scoped to objectives (high means *never amplified*, so it must say where it applies).

The planner rule — **high ⇒ acknowledge, never amplify or repeat; moderate ⇒ once per course;
low ⇒ unconstrained** — is written in the schema description and will be enforced when the
direction planner exists (§5, D7).

## 4. "No silent lying" — the baselines split · DECIDED 2026-09-01

The earlier Bayesian proposal named eight latent variables. Design beat 2026-09-01: are they audience
baselines the Audience Agent can seed, or should they wait in `ext`? Neither, whole. They are two
kinds of thing wearing one name.

**Dispositions** — self_efficacy, risk_sensitivity, identity_safety, trust — are things a population
can plausibly hold before any course exists. An Audience Agent can assert "tenured hourly workers
start with low trust in HR messaging" from analysis, stamp a basis, and be honest. These are the
four `baselines`. Static in Stage 1; no update machinery exists for them.

**Trajectories** — clarity, agreement, intent_to_act, load — arise *during* an encounter. A segment
cannot have "clarity 0.3" before taking the course; clarity is what the course is for. Writing it as
audience data would be a schema asserting a state that does not exist yet, and a planner would read
it as an input when it is the target. Jake: "we simply cannot have any silent-lying schemas." They
leave the audience model entirely and reappear where the horizon already put them: the **scene's
moment-level learning contract** (Designer's facet — *this scene expects agreement to rise; here is
supporting, partial, disconfirming, low-information evidence*). That is `intent.intended_response`
grown up, and it is a later hop (D9).

Consequence for §6: the synthetic delta is **evidence flags against a contract**, not numeric
deltas on latents — the horizon's "transparent rules before probabilistic inference," exactly.

## 5. What the synthetic learner may change — staged

Jake's requirement: eventually both **how it lands** and **what is said**. Split (Claude's call).

**Hop A — how it lands (NEXT · D7).** Segment record → direction planner → **direction** bindings
(staging / pacing / weight / attention) + expression keys. Same `element_id`, same `content_hash`,
different bindings per segment, external, keyed by element_id / `audience.variant_group`. Zero
content_hash churn, so it validates on the reference course without touching locales or provenance,
and the psychology's whole effect is visible in reason traces. First design beat of that hop: draw
the line between **direction**, **tone** (`vocab/tone.enum.json` — affective feel, upstream signal)
and **arc** (Dramaturge's beats — placement) so we do not mint a fourth overlapping vocabulary.

**Hop B — what is said (FORESEEN · D1).** Meaning variants per segment: a new element with its own
`element_id`, `governance.derived_from` → source, same `variant_group`; new meaning ⇒ new hash ⇒ its
own translations (correct). Prerequisites: Hop A traces reviewed on a real course; a rule for which
segments *earn* a variant (default: none — direction first, wording only when direction can't carry
it); a writer assignment (planner *proposes*, meaning owner approves — single writer holds).

## 6. Stage 1.5 — the synthetic traversal loop (Jake's) · FORESEEN · D7/D8

The segment's mastery is a first-guess hypothesis. Make it a loop: graph generates the course via the
objective join → a **synthetic learner agent** enacts the segment and traverses the course → the
**synthetic delta** is measured → a bounded second planning pass adjusts.

This is the LRE control loop run offline — `state → present → evidence → update → re-plan`. Stage 2
swaps the synthetic agent for a human and the second pass for realtime; nothing else changes.

Constraints: the second pass **drives the planner**, it is not a new writer (adjustments land only
through direction bindings or, after D1, proposed meaning variants) · the delta becomes `basis` on
the re-planned bindings (`evidence:synthetic_pass_2:<ele>:kc_fail`) — a reviewable trail, not
black-box tuning · **bounded** passes (2–3), every delta logged, never looped to convergence silently.

**Model-grading-model.** A synthetic learner enacted by the same model family that planned the
course will tend to find it convincing. So: enact the segment with a **different model**, seeded
**adversarially** from its own inhibitors and objections (the adversary's brief already exists —
"you suspect ranges are legal cover, you're worried you're underpaid, you don't trust HR. Take the
course."), and treat the delta as plausibility-to-a-model until D3 lands real evidence to calibrate
against. When that learner comes out the other side with a scene's contract *supported*, it means
something, because the planner wasn't grading its own homework.

New contract this introduces: **`learner-evidence.schema.json`** (D8) — per element:
`{record_id, element_id, objective_ids (via teaches), observed, contract_flag ∈ {supported, partial,
disconfirmed, low_information}, basis}`. PII-blind. The same record a live LRE consumes in Stage 2.

## 7. Where the psychological primitives live · SETTLED

They are **reasoning, not content**. Never a property of an element; never stored in the audience
model either — the model holds what they reason *from* (disposition, baselines). The planner applies
them and writes into exactly one facet it owns (direction). They appear in the graph only inside a
binding's **reason trace** — provenance, human-reviewable, never read by a renderer:
`emphasis-beat · inhibitor=inh_fear_of_being_underpaid · primitive=PR_IDENTITY_ANCHOR`. Reason
statements, not confidence scores. Same vocabulary, second home in Stage 2 on live learner state —
the learner-data domain — joined to content only by `element_id`.

## 8. Honest caveat

Hop A alone validates the **plumbing**. Stage 1.5 adds *weak* validation — the model is applied
consistently and a model-enacted learner responds as predicted. A synthetic delta is not human
evidence. The reason traces and evidence records are the hedge: they are what real learner data gets
compared against when Stage 2 arrives (D3). *Remember the future without prepaying for it.*

## 9. The persona generator already exists

The psykido builders (ADRA S6.1–S6.6, the emap prompt chain: Audience Analysis, Affective Patterns,
Engagement Cadence, Empathy Tuning, Inhibitor Vaccination, Motivation Reinforcer, Meaning Maker) are
the Audience Agent's skillset per the roster. Block mapping: Audience Analysis → `standing`;
Inhibitor Vaccination → `inhibitors` / `objections` / `rationalization_patterns`; Motivation
Reinforcer → `aligners`; Empathy Tuning → `identity_threats`, `identity_safety`; Meaning Maker →
`meaning_anchors`, `belief_gaps`; Affective Patterns → `affective_pattern`, `risk_sensitivity`,
`trust`; Engagement Cadence → `cadence`. Stage 1's first real segment record is that chain, pointed
at a segment, emitting this schema (D5 → `specified` vocab entries).

## 10. Deferred register

| # | capability | status | trigger |
|---|---|---|---|
| D1 | meaning variants per segment (Hop B) | foreseen | Hop A traces reviewed on a real course |
| D2 | live learner record as planner input (Stage 2 / true LRE) | frontier, separate project | contract stable through ≥2 courses; learner-data governance approved (horizon activation signals) |
| D3 | psychology validated against real learner evidence | needs D2 | Stage 2 data |
| D4 | machine-readable direction registry | proposed | when a validator needs it |
| D5 | `disposition.enum.json` entries promoted `seed` → `specified` by an Audience Agent pass | vocab seeded (13 entries), pass not built | before the first `approved` segment record |
| D6 | `governance.derived_from` present in conventions, absent from `element.schema.json` | schema gap | before D1; trivial |
| D7 | direction planner + Stage 1.5 traversal loop (different model, adversarial seed, bounded) | foreseen | direction facet designed (Hop A design beat) |
| D8 | `learner-evidence.schema.json` — per-element evidence, contract flags, PII-blind | foreseen | with D7 |
| D9 | scene-level **learning contract** (the four trajectory variables' real home; Designer's facet) | foreseen | Hop A; horizon's "scenes can carry explicit learning contracts" |
| D10 | `risk_of_overuse` planner enforcement (high: never amplify; moderate: once) | contract built, behavior not | D7 |

## 11. Open for the next design beat

1. Shape and name of the **direction** facet (own facet vs `intent.direction`), and its line against
   tone and arc; scene-level and unit-level enums seeded from the rehydrated treatment vocabulary
   (didactic-flow / emphasis-frame / progressive-reveal / contrast-frame / assessment-beat;
   primary-assertion / supporting-context / emphasis-beat / progressive-step / contrast-pair /
   interaction-prompt).
2. Where reason traces live — per binding, or a scene-level assessment envelope.
3. The planner contract: `(elements, segment record) → direction bindings + reasons`, honoring D10.
