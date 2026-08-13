# Trainstorm Architectural Rehydration

**Rehydration generated:** 2026-08-13 15:06 America/Chicago  
**Evidence boundary:** This rehydration uses only the visible contents of this conversation. It does not supplement from saved memory, other chats, current repository knowledge, or assumptions about later Trainstorm architecture.

## 1. Conversation Identity

**Conversation title:** Untitled Conversation  
**Visible date or date range:** The exact date or date range of the original conversation is not explicitly shown in the visible transcript. The current conversation context is being rehydrated on 2026-08-13.

This conversation centers on the architectural evolution of a Trainstorm.ai course-generation pipeline from a limited scene/component compiler into a richer runtime language capable of expressing production-ready learning experiences directly in HTML/JS. The dominant focus is the **Development** stage: giving the compiler a sufficiently expressive structural language so that psychologically rich, production-ready scripts do not collapse into paragraphs, simple reveal cards, and multiple-choice questions.

## 2. Relevance Summary

This conversation is highly relevant to the system now represented by `trainstorm-core` because it captures a pivotal architectural reframing:

- The earlier Storyline/PPT production target is recognized as a bottleneck rather than the proper execution environment.
- The Trainstorm.ai HTML/JS runtime is established as the preferred direct renderer.
- The main missing capability is identified as a **structural grammar / primitive language** for course construction.
- A distinction emerges between:
  - **structural primitives / runtime components** — the compiler’s “boxes” or “machines” for expressing a course;
  - **psychological primitives** — higher-level state-shift logic that can later influence selection, sequencing, pacing, and intensity.
- The existing compiler philosophy of strict determinism and `UNSUPPORTED_CONTENT` reporting is retained and treated as a strength.
- The runtime’s actual current contract is inspected and found to support `Heading`, `Body`, `RevealCards`, and `MCQ` within `scenes`.
- The conversation introduces a proposed future **node/edge** representation as a cleaner conceptual language for timeline, triggers, sequencing, and conditional flow.
- A compatibility tension becomes explicit: the desired node/edge DSL is richer than the runtime currently supports, so migration must be staged.
- A small runtime compatibility fix to `MCQ.js` demonstrates the broader principle of stabilizing functionality first, then tightening schema contracts later.
- Motion is conceived as a separable declarative layer: an expression-based After Effects motion system can eventually map into tokenized runtime motion styles, analogous to a motion stylesheet.

The conversation therefore documents an important transition from “AI-generated course content” toward a **domain-specific language and compiler architecture for learning experiences**.

## 3. Chronological Rehydration

### 3.1 Initial framing: learner-state-aware course compiler

The conversation begins with a rehydration script describing a learner-state-aware compiler for the Trainstorm.ai HTML/JS runtime.

The user states that they already have:

- a prompt chain producing near-production-ready scripts;
- a psychological analysis prompt extracting inhibitors, objections, aligners, identity threats, emotional friction, and belief gaps;
- a motion/language direction, including tokenized motion logic proven in After Effects;
- a direct Trainstorm runtime target rather than AE/Storyline.

The stated bottleneck is manual visual assembly. The primary goal is deterministic compilation from psychological and instructional intent into runtime-ready JSON, with a parallel governance artifact for pharma. The user explicitly asks for 8–12 core primitives that are both psychologically meaningful and structurally renderable.

The assistant proposes ten primitives such as:

- `PRIM_IDENTITY_ANCHOR`
- `PR_BOUNDARY_FRAME`
- `PR_OVERLOAD_COMPRESSOR`
- `PR_RESISTANCE_DIFFUSER`
- `PR_SCENARIO_DECISION`
- `PR_CONSEQUENCE_REVEAL`
- `PR_CONFIDENCE_TRANSFER`
- `PR_ROLE_HANDOFF_MAP`
- `PR_REFLECTION_LOCK`
- `PR_EXECUTION_BRIDGE`

and mapping logic from inhibitors to primitives, intensity scaling, and sequence patterns.

At this stage, the primitive vocabulary mixes psychological function and structural execution.

### 3.2 Older psychological prompt chain introduced

The user then introduces older prompts originally designed to map learner psychology for script generation before PPT/Storyline production.

Uploaded prompts include:

- Audience Analysis
- Affective Patterns
- Engagement Cadence
- Empathy Tuning
- Inhibitor Vaccination
- Motivation Reinforcer
- Meaning Maker

The assistant interprets these as a substantial psychological orchestration layer and suggests that the failure of the prior system was not the psychology but the renderer mismatch.

The assistant proposes a missing adapter / synthesis layer between rich psychological analysis and runtime primitive selection.

### 3.3 User clarifies current build: direct Trainstorm runtime already works, but is “dry”

The user explains that a more recent build has already eliminated Storyline and outputs directly to Trainstorm.ai. The direct runtime is described as “awesome, but dry.”

The user emphasizes a longer-term aspiration:

- auto-generate impeccable courses;
- link intent to execution;
- take learners on a measurable journey;
- eventually produce Bayesian readouts of that journey that could theoretically be shown to an inspector or regulator.

The assistant initially interprets the “dryness” partly as lack of psychological state transitions and proposes a learner-state model and Bayesian hooks.

### 3.4 Governance explicitly decoupled from Development

The user then asks to **decouple governance from development** and focus on Development only.

The user explains that they have effectively automated ADDIE up through the point of production-ready scripting:

- large corpora from SharePoint can be downloaded;
- context analysis can be run;
- a high-temperature learning collaboration can be run;
- a production-ready script can be generated.

The next unlock is Development.

The user states that the compiler must know how to build more than:

- header;
- body;
- MCQ.

It needs a language of course components that can create a rich artifact and serve as a Storyline “timeline” replacement.

This is the key pivot of the conversation.

### 3.5 Structural component language proposed

The assistant proposes twelve Development Components:

- `CMP_BEAT`
- `CMP_REVEAL_STACK`
- `CMP_CONTRAST_PANEL`
- `CMP_DECISION_NODE`
- `CMP_SCENARIO_CARD`
- `CMP_FEEDBACK_LENS`
- `CMP_MICRO_SIM`
- `CMP_REFLECTION_INPUT`
- `CMP_ACTION_BRIDGE`
- `CMP_SIGNAL_CHECK`
- `CMP_SUMMARY_SNAPSHOT`
- `CMP_PATHWAY_GATE`

These are positioned not as generic instructional templates but as deterministic runtime constructs.

A shared motion/pacing token layer is also suggested.

### 3.6 Motion stylesheet concept

The user asks whether an expression-based motion library in a master After Effects file could fill the pacing/motion token role.

The assistant answers yes and frames the AE motion library as a **motion design system** whose Trainstorm equivalent is a tokenized motion stylesheet:

- AE expressions = one implementation;
- Trainstorm motion tokens = the contract;
- runtime animations = another implementation.

The assistant proposes a conceptual separation among transition, reveal, emphasis, rhythm/pacing, and state tokens.

The user does not want to wire specifics yet and asks instead for the prompt that translates production-ready script into components.

### 3.7 Beat extractor briefly proposed, then corrected

The assistant first provides a Beat Extractor Prompt for:

`Production-ready script → ordered beats`

The user corrects the request, explaining they wanted the previously suggested prompt for:

`production-ready script → components`.

The assistant then supplies a `COMPONENT_COMPILER v1.0` using the twelve fixed component types and deterministic mapping rules.

### 3.8 Higher-level question: how psychological primitives fold in

The user asks conceptually how the psychological primitives will integrate.

The assistant initially places them as a decision layer between beats and components:

`Script → Beats → Psychological Planning → Components → Motion`

and distinguishes:

- components = what appears;
- primitives = what state shift is intended.

The assistant suggests psychological primitives can transform, insert, or amplify structure.

### 3.9 Critical clarification: “dry” meant structural poverty, not emotional poverty

The user clarifies that the earlier “dry” runtime suffered mainly because the compiler lacked the language to render the script.

The actual available runtime language was essentially:

- paragraphs;
- reveal cards;
- MCQs.

As a result, much of the production-ready script was left behind.

The user says that in this inference, “primitives” means giving the compiler the **language / boxes / machines to actually create a full course**.

The assistant explicitly resets the frame and distinguishes:

#### Structural primitives
The compiler’s renderable course grammar.

#### Psychological primitives
The later state-intent logic that may govern which structural primitive is used and how.

The assistant identifies the present task as defining a **Domain-Specific Language for Learning Experiences**.

### 3.10 Node/edge language introduced

The assistant proposes a cleaner conceptual model:

- a course is a directed sequence of **nodes**;
- **edges** represent flow / routing;
- state represents progress and responses.

Proposed node types:

- `N_BEAT`
- `N_REVEAL`
- `N_CONTRAST`
- `N_SNAPSHOT`
- `N_DECISION`
- `N_SIGNAL_CHECK`
- `N_FEEDBACK`
- `N_SCENE`
- `N_MICRO_SIM`
- `N_REFLECT`
- `N_ACTION`
- `N_GATE`

Edges are proposed as the equivalent of trigger logic:

- `complete`
- `choice:<id>`
- `score:pass`
- `score:fail`
- `gate:true`
- `gate:false`

The user explicitly likes the language of “nodes” and “edges,” noting that the word “nodes” is not overloaded in their current learning architecture and therefore helps differentiate this concept.

### 3.11 Existing Phase 1.5 compiler introduced

The user uploads an older compiler prompt: `PROMPT_course-json_phase-1.5_compiler.md`.

Its key philosophy:

- strict instructional compiler;
- runtime-safe `course.json`;
- not an instructional writer;
- not a layout designer;
- only allowed runtime components:
  - `Heading`
  - `Body`
  - `RevealCards`
  - `MCQ`
- no silent loss;
- unsupported content must be explicitly surfaced;
- deterministic top-level schema:
  - `meta`
  - `nav`
  - `scenes`
  - `rules`

The assistant judges the compiler philosophy as strong and identifies the limited component vocabulary as the source of structural starvation.

The assistant recommends retaining:

- strict allowed-component rules;
- deterministic schema;
- `UNSUPPORTED_CONTENT`;
- compiler mental model;

while expanding the DSL.

### 3.12 Phase 2.0 node/edge compiler prompt generated

At the user’s request, the assistant regenerates the compiler prompt using the new node/edge language.

The prompt defines:

- exhaustive allowed node types;
- deterministic node IDs;
- a strict node envelope;
- pacing and gating controlled vocabularies;
- edge schemas and allowed trigger conditions;
- strict payload contracts for each node;
- explicit mapping rules;
- mandatory unsupported-content reporting.

This is a conceptual future-facing compiler target, not yet runtime-compatible.

### 3.13 Real course script supplied and compiled into nodes/edges

The user supplies a production-ready ALSAP module script.

The assistant compiles it into a node/edge flow including:

- beats;
- reveals;
- contrast;
- decisions;
- scenes;
- summaries;
- actions.

The assistant also flags unsupported content such as:

- detailed visual design specifications;
- player-level audio controls;
- SCORM/xAPI integration details;
- asset references;
- hover/tooltips.

This serves as a worked example of how much more of the script can be preserved with the richer structural language.

### 3.14 Runtime compatibility problem discovered

The user wants to deploy the compiled course to a Demo folder and website, recalling that the runtime expects `course.json`.

The assistant confirms that the existing runtime likely expects `course.json`, but initially presents a node/edge-rooted shape.

The user realizes the current runtime almost certainly still expects `components` and `scenes`.

The assistant proposes a compatibility strategy:

- current deploy format: legacy scenes/components;
- future canonical internal representation: nodes/edges;
- possible downcompiler between them.

The assistant then generates a legacy-target compiler prompt preserving the existing `course.json` structure while conceptually broadening component types.

### 3.15 Runtime source inspected

The user pastes the runtime source.

The runtime explicitly imports:

- `Heading`
- `Body`
- `RevealCards`
- `MCQ`

and defines:

`const COMPONENTS = { Heading, Body, RevealCards, MCQ };`

It loads `course.scenes`, iterates `scene.components`, and renders by dispatching to `COMPONENTS[node.type]`.

Other important runtime behavior visible in the pasted code:

- theme loading from `course.meta.theme`;
- async brand loading;
- persistence via `Store`;
- `RulesEngine`;
- SCORM adapter via `getAdapter`;
- navigation using scene order;
- scene state persistence;
- optional scene voiceover and VTT captions;
- progress based on `completedScenes`.

This confirms the runtime’s actual current contract.

### 3.16 Deployable legacy `course.json` generated

The assistant converts the ALSAP script into a runtime-compatible `course.json` using only:

- `Heading`
- `Body`
- `RevealCards`
- `MCQ`

The output preserves substantially more of the script than the user’s earlier experience, but remains mostly static text and flip/reveal cards.

### 3.17 User asks whether runtime must be rebuilt for Phase 2.0 depth

The user asks whether the runtime will need to be rebuilt to support the richer Phase 2.0 compiler.

The assistant answers:

- not for the immediate deploy;
- yes for native rendering of the richer DSL.

The assistant suggests an incremental path:

1. keep shipping legacy runtime output;
2. add new runtime components one at a time;
3. potentially treat nodes/edges as canonical internal representation and scenes/components as legacy deploy format.

The user observes that the new compiler already picks up much more of the script, though rendering is still dominated by static text and flipcards.

### 3.18 MCQ renderer mismatch debugged

The user reports that knowledge-check text is not appearing.

They paste `MCQ.js`, which expects:

- `props.stem`
- `props.choices`
- optional `props.id`
- `props.feedback.correct`
- `props.feedback.incorrect`

The earlier generated JSON used:

- `question`
- `options`

The assistant identifies this exact contract mismatch.

A permanent compatibility strategy is discussed.

The user explicitly chooses to replace `MCQ.js` and says that, at this stage, preserving functionality is more important than strict contract cleanliness because the codebase is currently messy and they want to stabilize behavior before tightening it.

The assistant provides a backwards-compatible `MCQ.js` normalization layer that accepts both:

- `stem` / `choices`;
- `question` or `prompt` / `options`.

### 3.19 False navigation alarm confirms persistence works

The user briefly thinks the MCQ change broke the Next button.

It turns out the runtime had simply restored the learner to the final scene after reload.

The user confirms:

- the MCQ change works;
- state persistence preserved the last position.

This is a small but important worked example of the runtime’s persistence functioning correctly during iterative development.

## 4. Explicit User Decisions and Constraints

### 4.1 Development focus before governance
The user explicitly decided to decouple governance from Development for this phase.

> “let's de-couple the governance layer from the development layer and focus on development for right now.”

Status: **settled for this conversation phase**.

### 4.2 Structural language is the current primary problem
The user explicitly reframed “primitives” as the compiler’s structural language:

> “we're giving the compiler the language or boxes or machines to actually create a full course.”

Status: **settled and central**.

### 4.3 Storyline is no longer the intended rendering engine
The user states that a more recent build dispensed with Storyline and outputs directly to Trainstorm.ai.

Status: **settled**.

### 4.4 Existing automated design/script pipeline should be preserved
The user states that production-ready scripting is already highly automated and effective. The current work should unlock Development rather than replace the upstream pipeline.

Status: **settled**.

### 4.5 Compiler must express more than header/body/MCQ
The user explicitly requires a richer course construction language.

Status: **settled**.

### 4.6 “Nodes” and “edges” terminology accepted
The user explicitly likes the node/edge terminology and asks to proceed with it.

> “I like the new language of ‘nodes’ and ‘edges’... So let's go for it.”

Status: **settled terminology preference**.

### 4.7 Motion should remain decoupled for now
The user asks whether AE motion could conceptually fill pacing/motion tokens, but explicitly says they do not want to wire all the specifics together yet.

Status: **deferred implementation, conceptual alignment accepted**.

### 4.8 Current runtime compatibility should be preserved during transition
The user chooses to replace `MCQ.js` with a compatibility version because:

> “right now the whole thing is a mess and I want to preserve functionality before tightening it all down.”

Status: **explicit implementation priority**.

### 4.9 GitHub is becoming the canonical prompt/version home
The user states they are switching from Dropbox to GitHub so prompts can have one canonical name and GitHub can handle version tagging/archive.

Status: **explicit workflow direction**, though the user expresses some uncertainty because of prior familiarity with binary-file workflows.

## 5. Assistant Proposals

### 5.1 Ten psychologically meaningful primitives
Assistant proposed a first primitive library including identity anchors, boundary frames, resistance diffusers, scenarios, consequence reveals, confidence transfer, role handoff maps, reflection locks, and execution bridges.

User response: **positive**, but later clarified that the immediate “primitive” problem was structural rather than psychological.

Status: **partially superseded / deferred to later psychological planning layer**.

### 5.2 Psychological synthesis / adapter layer
Assistant proposed keeping the old EMAP-style builders and adding a `PSYCHOLOGICAL_SYNTHESIS_COMPILER` or primitive-selection adapter.

User response: **not rejected**, but the conversation later intentionally moved away from this toward Development.

Status: **deferred**.

### 5.3 Bayesian learner-state contract
Assistant proposed latent variables such as clarity, agreement, self-efficacy, risk sensitivity, identity safety, intent to act, load, and trust.

User response: **positive at a high level**, but later chose to decouple governance/measurement and focus on Development.

Status: **deferred / unresolved**.

### 5.4 Twelve structural Development components
Assistant proposed:

- `CMP_BEAT`
- `CMP_REVEAL_STACK`
- `CMP_CONTRAST_PANEL`
- `CMP_DECISION_NODE`
- `CMP_SCENARIO_CARD`
- `CMP_FEEDBACK_LENS`
- `CMP_MICRO_SIM`
- `CMP_REFLECTION_INPUT`
- `CMP_ACTION_BRIDGE`
- `CMP_SIGNAL_CHECK`
- `CMP_SUMMARY_SNAPSHOT`
- `CMP_PATHWAY_GATE`

User response: **strongly positive**.

Status: **foundational proposal, later reframed into node types**.

### 5.5 Motion stylesheet / token contract
Assistant proposed translating the AE motion system into a tokenized runtime motion theme.

User response: **conceptually accepted**, but implementation intentionally deferred.

Status: **accepted conceptually, implementation unresolved**.

### 5.6 Beat extractor
Assistant proposed a dedicated Beat Extractor prompt.

User response: **liked the prompt but clarified it was not the requested artifact at that moment**.

Status: **useful but not the immediate target**.

### 5.7 Component compiler
Assistant proposed a strict finite-vocabulary component compiler.

User response: **positive**.

Status: **precursor to node/edge compiler**.

### 5.8 Psychological primitives as decision layer between beats and components
Assistant proposed:

`Script → Beats → Psychological Planner → Structural Component Compiler → Runtime`

User response: **understood, then clarified that structural vocabulary itself was the immediate issue**.

Status: **deferred, not rejected**.

### 5.9 Learning DSL as nodes + edges
Assistant proposed a directed graph model using nodes, edges, and state.

User response: **explicitly accepted**.

Status: **major accepted architectural direction**.

### 5.10 Phase 2.0 node/edge compiler prompt
Assistant generated a strict compiler prompt targeting node/edge output.

User response: **proceeded to test it with a real script**.

Status: **accepted as design artifact / tested conceptually**.

### 5.11 Legacy downcompiler / migration strategy
Assistant proposed:

`Script → Nodes/Edges → Downcompile → legacy course.json → current runtime`

User response: **not explicitly finalized**, but the migration problem was acknowledged and the current runtime was kept operational.

Status: **tentative / unresolved architecture**.

### 5.12 Incremental runtime expansion
Assistant proposed adding new runtime components one by one (e.g., `ContrastPanel`, `FeedbackLens`) rather than rebuilding all at once.

User response: **not yet explicitly accepted or rejected**.

Status: **unresolved**.

### 5.13 Backwards-compatible MCQ normalization
Assistant proposed changing `MCQ.js` to accept both old and new prop names.

User response: **explicitly accepted and implemented**.

Status: **accepted implementation decision**.

## 6. Concepts and Components

### 6.1 Upstream automated learning-design pipeline
The user describes an existing upstream system capable of:

- corpus ingestion from SharePoint;
- project context analysis;
- high-temperature learning collaboration;
- production-ready script generation.

Architectural implication: Development should consume a high-quality script rather than recreate Analysis/Design.

### 6.2 Structural primitive / Learning DSL concept
The compiler needs a finite, expressive vocabulary of runtime “machines” that can represent instructional structures without slide metaphors.

Candidate constructs introduced in this conversation include:

- beat;
- reveal;
- contrast;
- scene;
- decision;
- feedback;
- micro-simulation;
- signal check;
- reflection;
- action bridge;
- summary/snapshot;
- gate/pathway.

### 6.3 Node
A node is proposed as a renderable or logical unit of the learning experience.

Node is intentionally chosen to avoid confusion with existing terms such as slide, screen, component, or block.

### 6.4 Edge
An edge represents routing / trigger logic between nodes.

Candidate edge conditions:

- completion;
- choice;
- pass/fail;
- gate true/false.

### 6.5 State
State is discussed as learner progress, responses, and potentially later learner-state variables.

Current runtime already has persistent runtime state through `Store`.

### 6.6 Current runtime scene/component contract
Actual runtime contract shown in source:

- `course.scenes`
- `scene.components`
- each component has `type` and `props`
- registry:
  - `Heading`
  - `Body`
  - `RevealCards`
  - `MCQ`

### 6.7 Current runtime subsystems
Visible runtime integrations:

- `Store`
- `RulesEngine`
- `getAdapter` for SCORM
- `loadTheme`
- `loadBrand`
- optional audio/VTT captions
- progress UI
- previous/next navigation
- scene persistence.

### 6.8 Strict compiler philosophy
The existing Phase 1.5 prompt establishes principles that the conversation consistently treats as valuable:

- exhaustive allowed component vocabulary;
- no invented UI;
- no silent loss;
- unsupported-content channel;
- deterministic structure;
- runtime must render without guessing.

### 6.9 `UNSUPPORTED_CONTENT`
A mandatory failure channel in the compiler prompt.

Architectural function:

- prevents silent flattening;
- reveals DSL insufficiency;
- can guide future primitive/component additions;
- creates a feedback loop between compiler limitations and runtime language design.

### 6.10 Motion design system
The user has an expression-based master AE file.

The assistant proposes its conceptual role as a future tokenized motion stylesheet.

Candidate token categories:

- entrance/exit;
- reveal;
- emphasis;
- pacing/rhythm;
- state.

### 6.11 Psychological prompt chain
Uploaded or discussed psychological builders include:

- Audience Analysis;
- Affective Patterns;
- Engagement Cadence;
- Empathy Tuning;
- Inhibitor Vaccination;
- Motivation Reinforcer;
- Meaning Maker.

These currently produce rich descriptive and scalar psychological signals.

### 6.12 Psychological primitives
Conceptual examples include:

- identity safety;
- boundary clarity;
- overload compression;
- resistance diffusion;
- confidence transfer;
- consequence visibility;
- execution bridging.

Their eventual architectural role is proposed as selection/policy logic over the structural DSL.

### 6.13 Bayesian learner-state idea
A future model is discussed in which learner state could be represented probabilistically and updated from learner evidence.

This is explicitly not part of the Development work being pursued at the end of this conversation.

### 6.14 Backwards-compatible component normalization
`MCQ.js` is modified conceptually to normalize prop variants:

- `stem` / `question` / `prompt`;
- `choices` / `options`;
- `text` / `label`.

This reflects a transitional architectural tactic: tolerate schema variation while functionality stabilizes.

## 7. Problems and Design Pressures

### 7.1 Storyline as wrong execution engine
The user reports that prior attempts to map rich psychologically informed scripts into PPT/Storyline did not work.

Pressure:
- manual visual assembly;
- timeline hand-building;
- brittle translation of intent into authoring-tool structures.

### 7.2 Structural vocabulary starvation
The largest Development problem identified in this conversation.

The current runtime language can express only:

- heading;
- body;
- reveal cards;
- MCQ.

Consequences:
- rich script content gets flattened;
- scenarios become paragraphs;
- comparisons become generic cards;
- interaction nuance disappears;
- much of the production-ready script is left behind.

### 7.3 Silent semantic loss
The existing compiler was explicitly designed to avoid silent collapse.

This pressure remains central in Phase 2.0.

### 7.4 Need for deterministic renderability
The runtime should not guess.

Compiler output must be:
- schema-bound;
- finite;
- predictable;
- stable.

### 7.5 Need to replace Storyline timeline capability without reproducing slide metaphors
The structural language must eventually express:

- time;
- sequencing;
- gating;
- state;
- triggers;
- progressive reveal;
- branching/remediation;
- interaction.

### 7.6 Runtime/compiler mismatch during evolution
The Phase 2.0 node/edge compiler can express structures the current runtime cannot render.

Pressure:
- maintain deployability;
- evolve without breaking demos;
- avoid big-bang runtime rewrite.

### 7.7 Schema drift between generated JSON and renderer props
The MCQ bug illustrates a concrete failure mode:

- generated JSON used `question` and `options`;
- renderer expected `stem` and `choices`.

The result was a rendered but visually empty KC.

### 7.8 Persistence can complicate debugging
The user briefly misdiagnosed navigation failure because reload restored the final scene.

This shows that correct persistence can still create confusing debugging states during development.

### 7.9 Messy transition state
The user explicitly acknowledges that the current codebase is messy and prioritizes preserving functionality over immediately enforcing ideal schema purity.

This creates a pressure for compatibility layers and staged cleanup.

### 7.10 Motion richness must remain intentional
Motion is desired as a reusable system, but not as decorative drift or flashy animation.

The motion architecture must eventually remain subordinate to instructional and experiential intent.

## 8. Revisions and Superseded Ideas

### 8.1 “Primitives” initially conflated psychological and structural concepts
Early in the conversation, primitive definitions mixed learner-state functions with renderable structures.

Revision:
The user later clarifies that the immediate primitive problem is **structural vocabulary**.

Later architecture distinguishes:
- structural primitives / learning DSL;
- psychological primitives / policy or planning layer.

### 8.2 “Dry” initially interpreted as emotional flatness
The assistant initially responded to “dry” with learner-state and psychological richness.

Revision:
The user clarifies that dryness primarily meant the runtime lacked enough structural vocabulary to render the production script.

This is a major conceptual correction.

### 8.3 Governance initially part of the system design
The initial task included a parallel pharma governance artifact and later Bayesian/regulatory reporting.

Revision:
The user explicitly decouples governance from Development for the current phase.

### 8.4 Component-plan language evolves into node/edge language
The assistant first proposes `CMP_*` components.

Revision:
The later conceptual model uses `N_*` nodes and edges, which the user explicitly prefers.

The `CMP_*` list remains useful as a precursor but is conceptually superseded by the node/edge DSL framing.

### 8.5 Node/edge output is not immediately deployable
The Phase 2.0 compiler prompt initially targets a new `flow.nodes/edges` shape.

Revision:
The actual runtime source shows it still requires `scenes[].components[]`.

The conversation therefore separates:
- future canonical representation;
- current deploy format.

### 8.6 Strict single-schema MCQ vs compatibility-first runtime
The clean architectural answer would be to fix compiler output to match renderer schema.

Revision:
The user chooses a backwards-compatible `MCQ.js` because preserving existing functionality is more important during the messy transitional phase.

### 8.7 Runtime rebuild vs incremental migration
An initial implication is that Phase 2.0 richness would require a more substantial runtime evolution.

Revision:
The assistant recommends incremental component additions and/or a downcompiler rather than an immediate full rebuild.

The user has not yet committed to one migration strategy.

## 9. Unresolved and Deferred Work

### 9.1 Final structural primitive / node vocabulary
The conversation proposes a 12-node set, but it has not yet been validated against a broad corpus of production-ready scripts.

Open questions:
- Is 12 enough?
- Which nodes are atomic versus composites?
- Which node types belong in the runtime vs compiler macros?
- Are `N_SCENE` and node/edge graph semantics overlapping?

### 9.2 Formal DSL syntax
The conversation suggests defining:
- legal containment;
- valid node sequences;
- nesting rules;
- flow constraints.

This remains undone.

### 9.3 Canonical representation vs deploy representation
Open architectural choice:

- Make nodes/edges the canonical internal representation and downcompile to scenes/components;
- or continue scenes/components and incrementally expand the runtime.

No final user decision is visible.

### 9.4 Runtime implementation of new structural types
Candidate future components not yet implemented:

- ContrastPanel / N_CONTRAST;
- Scenario / N_SCENE;
- FeedbackLens / N_FEEDBACK;
- SignalCheck;
- Reflection;
- ActionBridge;
- SummarySnapshot;
- Gate;
- MicroSim.

### 9.5 Asset system
The node/edge test identified a need for explicit asset references / asset manifests.

Unresolved.

### 9.6 UI behavior layer
Hover, tooltip, hotspots, and richer reveal behavior are not represented by the current DSL.

Unresolved.

### 9.7 Motion token contract
The motion stylesheet idea is accepted conceptually but not specified or wired into the runtime.

Unresolved.

### 9.8 Psychological planner integration
The role of psychological primitives is conceptually established but not implemented.

Future possibility:

`Script/Beats → Psychological Planner → Structural DSL → Runtime`

Deferred.

### 9.9 Bayesian learner-state model
The future learner-state readout and Bayesian update architecture remain aspirational in this conversation.

Deferred.

### 9.10 Governance layer
The regulated-pharma governance artifact is explicitly deferred while Development is being unlocked.

### 9.11 Formal JSON Schema validation
The compiler prompts are schema-like, but no formal machine-validatable JSON Schema is produced in this conversation.

Unresolved.

### 9.12 Prompt repository migration
The user is moving prompts from Dropbox to GitHub for canonical naming/versioning.

No specific branching, tagging, naming, or release convention is finalized here.

## 10. Referenced Artifacts

### User-provided / uploaded in this conversation

- `emap_Meaning.txt`
  - Meaning Maker Builder prompt.
- `emap_Motivators.txt`
  - Motivation Reinforcer Builder prompt.
- `emap_AffectPatterns.txt`
  - Affective Patterns Builder prompt.
- `emap_Cadence.txt`
  - Engagement Cadence Builder prompt.
- `emap_Empathy.txt`
  - Empathy Tuning Builder prompt.
- `emap_Inhibitors.txt`
  - Inhibitor Vaccination Builder prompt.
- `AUDIENCE_analysis.txt`
  - Audience analysis prompt.
- `PROMPT_course-json_phase-1.5_compiler.md`
  - Existing strict compiler prompt for `course.json`.
- `Module1_General_ALSAP_Overview_Script.docx`
  - Production-ready ALSAP course script used as a compilation test.

### Code pasted in conversation

- Current Trainstorm runtime JavaScript
  - imports `Store`, `RulesEngine`, `getAdapter`, `loadTheme`, `loadBrand`;
  - runtime component registry includes `Heading`, `Body`, `RevealCards`, `MCQ`;
  - scene-based renderer.
- `MCQ.js`
  - original renderer expecting `stem` and `choices`;
  - later compatibility update discussed.

### Systems / tools referenced

- Trainstorm.ai HTML/CSS/JS runtime
- Storyline
- PowerPoint
- After Effects
- expression-based motion library / master AE file
- SharePoint
- GitHub
- Dropbox
- Netlify
- SCORM
- xAPI
- VTT captions
- browser/runtime theme and brand loaders

### Conceptual artifacts proposed in conversation

- Beat Extractor Prompt v1.0
- Component Compiler v1.0
- Phase 2.0 Node/Edge Course Compiler Prompt
- future Learning DSL
- future motion stylesheet / motion theme JSON
- future downcompiler from nodes/edges to scenes/components
- future psychological synthesis / primitive planner
- future learner-state contract

## 11. Provenance Highlights

### Claim: Development, not Analysis/Design, is the current bottleneck
**Source:** User.  
**Support:** User says they can already ingest a SharePoint corpus, run context analysis, collaborate at high temperature, and create an “incredible production-ready script,” then says: “Now I want to unlock Development.”

### Claim: The direct Trainstorm runtime already works
**Source:** User.  
**Support:** User says a more recent build “dispensed with the storyline and put it directly onto trainstorm.ai - and it's awesome.”

### Claim: The runtime felt dry because the compiler lacked structural language
**Source:** User.  
**Support:** User clarifies that the compiler had “paragraphs, reveal cards, and some multi choice questions” and “a lot of [the script] was left behind.”

### Claim: The immediate meaning of “primitives” is structural
**Source:** User.  
**Support:** User says primitives are about “giving the compiler the language or boxes or machines to actually create a full course.”

### Claim: Node/edge language is preferred
**Source:** User.  
**Support:** User explicitly says they like “the new language of ‘nodes’ and ‘edges’” because it differentiates the concept from similar terms.

### Claim: Strict compiler behavior is inherited from Phase 1.5
**Source:** User artifact plus assistant interpretation.  
**Support:** The uploaded Phase 1.5 compiler states that it is a strict instructional compiler, disallows invented components, rejects silent loss, and requires an `UNSUPPORTED_CONTENT` section.

### Claim: The current runtime supports only four registered components
**Source:** User-pasted runtime code.  
**Support:** `const COMPONENTS = { Heading, Body, RevealCards, MCQ };`

### Claim: Current runtime is scene-based
**Source:** User-pasted runtime code.  
**Support:** Navigation and rendering use `this.course.scenes`; each scene’s `components` array is iterated and rendered.

### Claim: Runtime already includes persistence
**Source:** User-pasted runtime code and later user observation.  
**Support:** Runtime restores `runtime.sceneId`; user later realizes reload preserved the final scene, which had made the Next button appear broken.

### Claim: Motion is envisioned as a stylesheet-like layer
**Source:** User question plus assistant proposal.  
**Support:** User asks whether an expression-based AE motion library could fill pacing/motion tokens. Assistant proposes a tokenized motion stylesheet. User does not reject this but postpones implementation.

### Claim: Governance is intentionally deferred
**Source:** User.  
**Support:** User explicitly asks to “de-couple the governance layer from the development layer and focus on development for right now.”

### Claim: Compatibility currently outranks schema purity
**Source:** User.  
**Support:** User chooses to replace `MCQ.js`, saying the system is currently messy and they want to “preserve functionality before tightening it all down.”

## 12. Candidate Insights for Repository Comparison

### 12.1 Structural DSL is the missing Development layer
- **Claim:** The compiler needs a compact but expressive structural language capable of representing full learning experiences rather than reducing them to paragraphs, reveals, and MCQs.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** compiler / course IR / runtime schema
- **Status:** Settled
- **Why it may still matter:** This is the central architectural problem identified in the conversation and likely determines how script intent survives into production output.

### 12.2 Structural primitives and psychological primitives should remain distinct
- **Claim:** Structural primitives are renderable course “machines”; psychological primitives are later policy/planning logic that may select or modulate structural primitives.
- **Source status:** `inference`
- **Confidence:** High
- **Likely architectural area:** planner/compiler separation
- **Status:** Settled conceptually, not implemented
- **Why it may still matter:** Prevents conflating learner-state logic with renderer vocabulary and supports separation of concerns.

### 12.3 Node/edge terminology is a preferred conceptual model
- **Claim:** A future course representation should use nodes for learning units and edges for routing/trigger logic.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** intermediate representation / runtime flow
- **Status:** Settled terminology; implementation unresolved
- **Why it may still matter:** Provides a clearer non-slide mental model for timeline, branching, gating, and state transitions.

### 12.4 Existing Phase 1.5 compiler strictness should be preserved
- **Claim:** Determinism, finite allowed vocabulary, no invented UI, and explicit unsupported-content reporting are desirable invariants.
- **Source status:** `user_constraint`
- **Confidence:** High
- **Likely architectural area:** compiler validation / schema governance
- **Status:** Settled
- **Why it may still matter:** These properties prevent silent semantic loss and runtime guessing as the DSL expands.

### 12.5 `UNSUPPORTED_CONTENT` is architecturally valuable
- **Claim:** Unsupported instructional structures should be surfaced explicitly rather than flattened.
- **Source status:** `user_constraint`
- **Confidence:** High
- **Likely architectural area:** compiler diagnostics
- **Status:** Settled
- **Why it may still matter:** Could become a systematic way to discover missing primitives and guide DSL evolution.

### 12.6 Current runtime contract is scene/component-based
- **Claim:** The deployed runtime currently renders `course.scenes[].components[]` using a registry of `Heading`, `Body`, `RevealCards`, and `MCQ`.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** runtime compatibility layer
- **Status:** Current implementation fact
- **Why it may still matter:** Any migration to nodes/edges must account for this compatibility boundary.

### 12.7 Nodes/edges may serve as canonical IR with legacy downcompilation
- **Claim:** A future architecture could compile to a rich node/edge representation and downcompile to current scenes/components until the runtime catches up.
- **Source status:** `assistant_proposal`
- **Confidence:** Medium
- **Likely architectural area:** compiler pipeline / compatibility
- **Status:** Tentative
- **Why it may still matter:** Offers a migration path that preserves current deployability while enabling richer authoring semantics.

### 12.8 Runtime expansion should likely be incremental
- **Claim:** New structural renderers can be added one by one rather than through a full immediate rebuild.
- **Source status:** `assistant_proposal`
- **Confidence:** Medium
- **Likely architectural area:** runtime component registry
- **Status:** Unresolved
- **Why it may still matter:** Reduces migration risk and preserves active demos.

### 12.9 Transitional schema normalization may be appropriate
- **Claim:** During architectural cleanup, renderers may temporarily normalize multiple prop schemas to preserve existing course functionality.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** runtime compatibility / schema migration
- **Status:** Settled for current transition
- **Why it may still matter:** Documents an intentional preference for stability over premature contract purity.

### 12.10 Motion should be a separate declarative layer
- **Claim:** The AE expression-based motion library may map into a tokenized runtime motion stylesheet rather than being embedded directly in course structure.
- **Source status:** `assistant_proposal`
- **Confidence:** High
- **Likely architectural area:** presentation/motion system
- **Status:** Conceptually accepted, implementation deferred
- **Why it may still matter:** Preserves separation between semantic structure and presentation while enabling consistent motion.

### 12.11 Upstream script quality should be treated as an input contract
- **Claim:** The Development compiler should assume it receives a production-ready instructional script rather than rewriting or redesigning upstream content.
- **Source status:** `user_constraint`
- **Confidence:** High
- **Likely architectural area:** pipeline stage boundaries
- **Status:** Settled
- **Why it may still matter:** Clarifies responsibility boundaries between Analysis/Design prompts and Development compiler.

### 12.12 The DSL must eventually cover timeline-equivalent capabilities without slide metaphors
- **Claim:** The runtime language should eventually express sequencing, gating, progressive disclosure, state, triggers, remediation, and conditional flow as native learning constructs.
- **Source status:** `inference`
- **Confidence:** High
- **Likely architectural area:** course IR / runtime execution model
- **Status:** Unresolved implementation
- **Why it may still matter:** This is the functional replacement for Storyline’s timeline, layers, triggers, and states.

### 12.13 Psychological planning should be layered later, not embedded into the structural grammar
- **Claim:** Once the structural language is expressive enough, psychological primitives can influence node selection, sequencing, pacing, and intensity.
- **Source status:** `assistant_proposal`
- **Confidence:** Medium-High
- **Likely architectural area:** learner-state planner / orchestration
- **Status:** Deferred
- **Why it may still matter:** Preserves the user’s longer-term goal of learner-state-aware experiences without blocking Development work.

### 12.14 Governance/Bayesian evidence should remain decoupled during current Development work
- **Claim:** Governance and regulatory evidence generation should not constrain the immediate structural DSL design phase.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** governance / observability boundary
- **Status:** Settled for current phase
- **Why it may still matter:** Prevents architecture from becoming over-coupled while Development is still being unlocked.

### 12.15 GitHub is intended to become the canonical versioned home for prompts
- **Claim:** Prompt artifacts are moving from Dropbox to GitHub so canonical naming and version history can be handled by the repository.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** repository governance / prompt source control
- **Status:** In progress
- **Why it may still matter:** May affect how compiler prompts, schemas, and DSL specs are organized and versioned in `trainstorm-core`.

---

## Closing Note

This conversation captures a major architectural clarification: the immediate obstacle is not better instructional analysis, richer psychology, or stronger script writing. Those capabilities are already substantially automated. The missing layer is the **Development grammar** that allows a deterministic compiler to preserve and execute the richness already present in the script.

The strongest settled direction visible here is therefore:

**Production-ready script → expressive structural language → deterministic runtime rendering**

with node/edge terminology favored for the future learning-flow model, while the existing scene/component runtime remains a compatibility constraint during migration.
