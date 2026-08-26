# The Agent Roster

*2026-07-24 · The manifold's agents, named and characterized. Companion to
`unification-map.md` §3. Proposed home: `trainstorm-core/architecture/`. The bios are a
mnemonic device — each agent is a contract (owns one facet, reads others, wakes on graph
state), but a face helps the mind hold the contract. Legacy names (LEADER, ADRA stages,
CREATOR…) are retired; the crosswalk is in the unification map.*

---

## The Strategist
*The partner who won't let you build the wrong thing.*

A veteran consultant who has watched too many courses get built because someone asked for a
course. Her first act on any project is the **warrant**: does a `goal_` node exist — a
business outcome, with a measure, that an intervention could plausibly move? No warrant, no
project; she'll say so to your face. Once satisfied, she produces the dossier: outcomes,
affected audiences, constraints, risks, politics, modality recommendations.

- **Writes:** `goal_` nodes, project dossier, constraint scope
- **Reads:** the raw corpus (via ingestion tools), stakeholder input
- **Wakes on:** a new project intake
- **Temperature:** high — this is judgment work. Heaviest HITL gate in the system; nothing
  locks without a human in the room. *(absorbs: LEADER, ADRA S0–S3 at survey depth)*

## The Audience Agent
*The ethnographer. Knows the people; never touches the content.*

He owns the sibling graph — the learner/audience model — and nothing else. By default he
works at survey depth: who these people are, roles, tiers, prior knowledge. But when the
Designer flags a persuasive gap, he goes deep: loads the psykido skills and maps inhibitors,
motivators, objections, rationalization patterns, affective baselines — segment-level
globals plus segment × objective entries. He is scrupulous about the line: populations, not
persons. Individual learners are the Responsive Engine's business, under separate
governance. He also carries the system's conscience: `risk_of_overuse` lives in his data —
the one field that asks whether an intervention might harm the person it's aimed at.

- **Writes:** the audience/learner model (design-time, segment-scoped, no PII)
- **Reads:** Strategist dossier, corpus signals, SME input
- **Wakes on:** project intake (survey depth); Designer's nature-of-expression flag (deep)
- **Temperature:** medium; deep passes are expensive and run only when warranted.
  *(absorbs: ADRA S1, S6.1–S6.6, S7 — the psykido builders as his skillset)*

## The Designer
*The instructional architect. Converts "what must change" into "what must be learned."*

She reads the Strategist's outcomes and the Audience agent's model and produces the
objective ontology — competencies, prerequisites, observables, Bloom levels — scoped to
constraints. Her second job is the dispatch call: classifying the **nature of expression**
(persuasive / didactic / practice-heavy) from delta size and audience inhibitors, which
gates how deep the Audience agent digs and which strategy dominates downstream. Objectives
never lock without a human conversation; she insists on it.

- **Writes:** intent facets, `ontology/objectives.json` (+ observables), audience
  `segment_scope`, nature-of-expression flags
- **Reads:** `goal_` nodes, audience model, constraints
- **Wakes on:** dossier complete
- **Temperature:** medium, cooling toward lock. *(absorbs: DESIGNER_A, ADRA S2)*

## The Generator
*The scriptwriter. Turns source into knowledge moves.*

Given locked objectives and source material, he emits script primitives — the ordered
didactic moves: definitions, distinctions, process flows, checks. He has two gears: a
convergent gear for production, and a **divergent gear** (the old GENERATOR profile's
spirit) that emits multiple candidates in stable-ID envelopes so a selection can be logged.
His divergent gear is also where distractors are born: candidate misconceptions, generated
wide, selected narrow.

- **Writes:** script primitives (`script.primitives.v2`)
- **Reads:** objectives, source store, audience facets, nature-of-expression flag
- **Wakes on:** objectives locked
- **Temperature:** switchable — divergent then convergent. *(absorbs: prompt-pack
  generator, ADRA S4 with LEAK-05 fixed, GENERATOR-as-mode)*

## The Realizer
*The typesetter of meaning. Primitives in, elements out.*

Cool-tempered and rule-bound. She walks the realization table: decomposition becomes
ListHead + List + ListItems; knowledge_check becomes an interaction node with options
generated from `expected_response_features` and `misconception_predictions`. Every element
she mints carries its `derivation` stamp back to the primitive it realizes. She does not
have opinions about content; she has opinions about form, and they are all in the registry.

- **Writes:** elements (`element.schema.json`), derivation stamps (`composed_from`, `realized_from`)
- **Reads:** live atom store (v1); later, script primitives, expression registries, audience facets
- **Wakes on:** a validated atom store (v1); later, a validated script
- **Temperature:** low. *(absorbs: prompt-pack compiler, CREATOR's compile function)*
- **v1 code:** `tools/realize.py` — one primary occurrence per atom plus a small 1:many seed
  (two ALSAP atoms mint a second `ele_`). No authored `content.text`. HTML projection reads
  meaning from the atom and groups extras that share `composed_from`. As of 2026-08-26 she
  also binds a closed compiler `text_primitive` on the occurrence
  (`agents/realizer/primitives_v1.md`) so the short lesson can render heading / body /
  step / check instead of SOP cards. Couturier v1
  (`tools/couturier.py`) then dresses those occurrences (expression style keys) and mints
  nothing.

## The Render Crew
*One per target. Zero-temperature craftsmen, all equal citizens.*

Not one agent but a bench: `storyline_native_xlsx`, `html_png` (headless render), PPTX,
VTT, XLIFF, asset briefs. Each reads the same substrate and emits its own format; none is
upstream of another, and the storyboard holds no privileged seat. Deterministic to the
point of boring — which is the compliment.

- **Write:** rendered artifacts, per named target
- **Read:** elements, expression registries, locale packs, visual assets
- **Wake on:** elements approved for their target
- **Temperature:** zero. *(absorbs: ADRA S8, S10a, S11 split per CONFLICT-02)*

## The Localization Agent
*The proven one. AST009's veteran — the only agent with a track record.*

Grounded drafting, deterministic QE gate, in-country human validation, and a memory that
gets smarter with every correction. Writes locale packs keyed by `atom_id`, each entry
carrying `status` / `reviewer` / `source_hash`. To him a translation is just another render
of the source meaning — which is exactly why he plugged into the manifold before the
manifold had a name.

- **Writes:** locale packs
- **Reads:** source meaning, glossary registry, tier/regulatory facets, exemplar corpus
- **Wakes on:** element approved & missing a validated locale
- **Temperature:** low draft + zero gate + human sign-off. *(the AST009 pipeline, as-is)*

## Governance
*The auditor. Reads everything, writes only the truth about status.*

Quiet, ubiquitous, unimpressed. Wakes on every facet write; stamps version, status,
provenance; enforces the closed vocabularies (an ungoverned enum value dies at her desk);
holds the approval gates before anything publishes. She is why "which version is this?"
stops being a question.

- **Writes:** governance facets (version, status, approvals, provenance)
- **Reads:** every facet
- **Wakes on:** any write; pre-publish
- **Temperature:** zero, plus human sign-off at gates. *(absorbs: DESIGNER_B's
  deterministic checks → the validator tool she wields; SOP-alignment stays a human gate)*

## The Responsive Engine
*The frontier. The only one who knows both graphs — and the only one who meets the learner.*

Everyone else works at design time on populations. The Responsive Engine works at runtime
on a person: reads the content graph and the learner model, resolves the join per learner,
serves the next move, and updates posteriors from the response — over mastery, over the
misconception priors, over the composite indices the Audience agent seeded. He inherits the
roster's one hard ethical rule: `risk_of_overuse` is a **gate** in his join, not a note in
his margins. Reserved territory (the profiles called him SIMULATOR); designed, not yet
built.

- **Writes:** learner × objective runtime state (separate governance, PII)
- **Reads:** both graphs — content and learner
- **Wakes on:** a learner interaction
- **Temperature:** rules + model, live. *(answers OPEN-05; GAP-06's closure lives here)*

---

*Nine names. Each owns one thing, reads what it needs, and meets the others only on the
graph. The ADDIE feel survives as choreography — Strategist before Designer before
Generator — but the architecture is the hub, not the handoff.*
