# Trainstorm Architectural Rehydration — Untitled Conversation

**Rehydration timestamp:** 2026-08-13  
**Evidence boundary:** This document uses only the visible contents of this conversation and files visibly supplied within it. It does not use saved memory, other conversations, current repository contents, or assumptions about what `trainstorm-core` later became.

## 1. Conversation Identity

**Conversation title:** Untitled Conversation  
**Visible date:** 2026-08-13

No explicit conversation title is visible in the supplied conversation context, so the required fallback title is used rather than estimating one.

## 2. Relevance Summary

This conversation is directly relevant to the architecture represented by `trainstorm-core` because it develops a deterministic planning layer for CGEN that sits between semantic meaning and runtime rendering.

The conversation begins from an already-working compiler-like pipeline:

`PROJECT CORPUS → SCRIPT → SEMANTIC MODEL → RENDER PLAN → RUNTIME COURSE → BROWSER EXPERIENCE`

The semantic model is described as the handoff point between interpretation and deterministic compilation. The immediate design problem is that the system can represent meaning and structure but produces courses that feel “clear, structured, but flat.” The conversation therefore develops an explicit **Experience Treatment System** intended to model staging, pacing, rhetorical emphasis, contrast, progressive disclosure, and learner action without collapsing semantic, planning, and runtime responsibilities.

The most architecturally significant developments are:

- formalizing scene-level and unit-level experience treatments;
- separating previously overloaded `treatment` semantics into `rhetoricalTreatment` versus directed experiential roles;
- preserving `treatmentHint` as a separate downstream visual-intent concept;
- introducing `sceneSignals` as deterministic evidence for planner classification;
- creating a stable in-repository treatment registry as controlled planning vocabulary;
- discussing inspectable planner rationale rather than opaque confidence scoring;
- identifying the render-plan schema as the location for formal planning-layer traceability;
- introducing a `plannerAssessment` object in the uploaded schema, while leaving unresolved whether that score-based design should be retained or revised toward reason-first human review.

These ideas matter because they move CGEN beyond content transformation toward a governed, inspectable compiler for learning-experience decisions.

## 3. Chronological Rehydration

### 3.1 Starting checkpoint: semantic → planning → runtime compiler

The conversation was rehydrated from an uploaded checkpoint describing CGEN as a multi-stage compiler pipeline rather than a simple content generator.

The checkpoint stated the architecture as:

`PROJECT CORPUS → SCRIPT → SEMANTIC MODEL (course.semantic.json) → RENDER PLAN (render-plan.json) → RUNTIME COURSE (course.json) → BROWSER EXPERIENCE`

The semantic model was explicitly identified as the boundary between interpretation and deterministic compilation:

- before semantic: LLM interpretation, source analysis, instructional scripting;
- after semantic: schema validation, structural transformation, pedagogic rules, runtime compilation, rendering.

The working implementation included:

- `courses/demo/course.semantic.json`
- `planner/planCourse.js`
- `courses/demo/render-plan.json`
- `compiler/renderPlanToCourse.js`
- `courses/demo/course.json`
- runtime files under `courses/demo/` and `engine/`.

The checkpoint characterized the current output as functional but flat. Scenes rendered; RevealCards and MCQs worked; navigation worked; the planner interpreted semantic structure; visual-intent scaffolding existed. The missing capability was experience staging.

### 3.2 Proposal: add an Experience Treatment Layer

The assistant proposed a minimal treatment vocabulary rather than immediately adding visual polish.

The scene-level set proposed was:

- `didactic-flow`
- `emphasis-frame`
- `progressive-reveal`
- `contrast-frame`
- `assessment-beat`

The unit-level set proposed was:

- `primary-assertion`
- `supporting-context`
- `emphasis-beat`
- `progressive-step`
- `contrast-pair`
- `interaction-prompt`

The assistant framed the missing capability as “temporal + rhetorical control over attention” and recommended keeping the treatment metadata in the planning layer rather than the semantic model.

The user then asked which implementation path would best support conceptual learning: refactor planner logic first or map treatments directly onto existing runtime components.

The assistant recommended planner-first development: first name the experience, then represent it structurally, then let runtime express it. The user explicitly accepted this path: “Makes sense. Let's follow your best suggested path.”

### 3.3 Planner-first implementation path

The assistant proposed adding deterministic scene-signal extraction, scene treatment assignment, and unit treatment assignment to `planCourse.js`.

The initial scene signals discussed included:

- `hasMCQ`
- `hasImpact`
- `hasList`
- `hasLongList`
- `isSparse`
- `hasContrastSignals`
- element counts.

The planner would then assign a scene treatment using ordered deterministic rules. Example logic:

- MCQ present → `assessment-beat`
- sparse + Impact → `emphasis-frame`
- long list → `progressive-reveal`
- contrast signals → `contrast-frame`
- otherwise → `didactic-flow`.

Unit treatment would be derived from semantic/unit type plus scene treatment.

A key design constraint at this stage was explicit: do not yet make runtime behavior branch on treatments. The planner should first become inspectably smarter.

### 3.4 Review of actual `planCourse.js`

The user uploaded the full planner for reference and noted that some earlier suggestions were already incorporated.

The assistant observed that the planner already had several decision dimensions, including:

- `sceneIntent`
- `learningRole`
- `experienceStrategy`
- unit-level `instructionalIntent`
- `rhetoricalWeight`
- an existing generic `treatment`
- `learnerAction`.

This created a naming collision: the old `treatment` field was already being used for content/rhetorical handling, while the new treatment system was intended to represent directed experience.

### 3.5 Rename decision: `treatment` → `rhetoricalTreatment`

The user explicitly stated a preference to rename the existing treatment field:

> “I think I do want to rename semantic treatment to differentiate from directed experiential role.”

The user explained the reason: they intended to study schemas later to understand the design thinking at the time, and wanted the distinction encoded rather than merely remembered.

The assistant proposed `rhetoricalTreatment` as the new name and distinguished:

- `semanticRole` = what the unit is;
- `rhetoricalTreatment` = how it is rhetorically handled;
- `unitTreatment` = the directed experiential role within the scene;
- `sceneTreatment` = the dominant experience mode of the scene.

The assistant recommended against names such as `semanticTreatment`, `contentTreatment`, `displayTreatment`, or `instructionalTreatment`.

The user then asked for hand-holding in finding every code instance to change.

The assistant identified the primary rename locations:

1. return objects in `planningAttrsForSemanticType()`:
   - `treatment` → `rhetoricalTreatment`;

2. `buildRenderUnit()`:
   - `treatment: attrs.treatment`
   - → `rhetoricalTreatment: attrs.rhetoricalTreatment`.

The assistant advised leaving `treatmentHint` unchanged because it belonged to visual intent rather than rhetorical planning.

The user confirmed that after the rename, the only remaining occurrences of “treatment” were `treatmentHint`s.

### 3.6 User articulation of the conceptual model

The user stated that the distinction matched how they naturally think about a linguistic payload:

> “what is it in terms of content nuts and bolts, but also how is it supposed to land in the human nervous system.”

The assistant affirmed that the emerging stack separated content structure, rhetorical shaping, and experiential staging.

This user articulation is important because it makes explicit the intended conceptual boundary behind the fields, rather than treating them as merely technical names.

### 3.7 Threading scene and unit treatment into the planner

The assistant then returned to the implementation sequence:

- define treatment constants;
- ensure `getSceneSignals()` uses the planner's shared `getSceneElements(scene)` extractor;
- add `assignUnitTreatment()`;
- update `buildScenePlan()` to:
  - derive `sceneSignals`;
  - assign `sceneTreatment`;
  - build render units;
  - assign each unit a `unitTreatment`;
  - write these fields to the scene plan.

The assistant advised continuing to keep runtime behavior unchanged until the planner classifications could be reviewed.

### 3.8 Code verification and correction

The user uploaded an intermediate `planCourse.js` for verification.

The assistant found a concrete bug: `getSceneSignals()` accidentally contained a nested duplicate function declaration, leaving `elements` scoped incorrectly. The assistant supplied a corrected version using `getSceneElements(scene).filter(Boolean)`.

The user then uploaded another version for verification. The assistant confirmed that the structural separation was correctly present and that `buildScenePlan()` was already threading:

- `sceneSignals`
- `sceneTreatment`
- `unitTreatment`

while preserving `rhetoricalTreatment` and `treatmentHint`.

The only minor note was that the `scene` parameter to `assignSceneTreatment(scene, signals)` was currently unused.

### 3.9 Inspection of generated `render-plan.json`

The user uploaded the resulting render plan and asked whether the second quality—the one for which `treatment` had been renamed—had actually been encoded.

The assistant confirmed that it had:

- `sceneTreatment` encoded the overall experience mode;
- `unitTreatment` encoded each unit's directed experiential role;
- `rhetoricalTreatment` remained separate.

Examples observed in the output included:

- a heading with `rhetoricalTreatment: "summary-highlight"` and `unitTreatment: "primary-assertion"`;
- an Impact unit with `rhetoricalTreatment: "emphasized-assertion"` and `unitTreatment: "emphasis-beat"`;
- a scene with `sceneTreatment: "progressive-reveal"` and subordinate units assigned `progressive-step`;
- an assessment scene with `sceneTreatment: "assessment-beat"`, MCQ `rhetoricalTreatment: "knowledge-check"`, and `unitTreatment: "interaction-prompt"`.

This demonstrated that the distinction was not merely conceptual; it had been serialized into the planning artifact.

### 3.10 Creation of a treatment index and registry

The user asked for a downloadable table to keep track of the treatment vocabulary.

A Markdown treatment index was created with scene treatments, unit treatments, and examples of rhetorical treatments.

The user then asked for a more organized way to track lower-level fields such as `rhetoricalTreatment`.

The assistant created an expanded **CGEN Treatment Registry**. The registry organized:

- `semanticRole`
- `rhetoricalTreatment`
- `sceneTreatment`
- `unitTreatment`
- `treatmentHint`

and included:

- a layer map;
- definitions;
- usage contexts;
- examples showing how multiple fields combine on one unit;
- a registry template for future vocabulary;
- a governance rule for deciding which field family a new concept belongs to.

The assistant summarized the chain as:

`what it is → how it is framed → how it should land → how it might render`

### 3.11 Registry moved into CGEN as stable system knowledge

The user said the registry felt like it should live as a stable part of CGEN rather than only in progression notes.

The assistant recommended an in-repository location:

`cgen/knowledge/treatment-registry.md`

rather than personal notes or a planner-only documentation folder.

The rationale was that the registry had become controlled system vocabulary used across planner, compiler, runtime, validation, and future tooling.

The assistant suggested treating it as canonical and eventually possibly adding a machine-readable JSON form, but explicitly advised not doing that yet.

The user accepted this proposal and confirmed:

> “Cool. Added to 'knowledge'.”

### 3.12 Return to the core path: validate planner judgments

After moving the registry into `knowledge/`, the assistant recommended returning to planner validation rather than continuing vocabulary expansion.

The proposed human review loop was:

- inspect `sceneTreatment`;
- inspect `unitTreatment`;
- verify that `rhetoricalTreatment` and `unitTreatment` feel meaningfully different;
- identify misclassifications;
- refine signals and thresholds before runtime styling or motion uses the treatments.

The assistant explicitly suggested that the system was probably in a state where the vocabulary was sound but the rules might still be coarse.

### 3.13 Question about confidence and renderer behavior

The user asked whether the registry needed a confidence value so the renderer could decide how confident it was in a classification such as `didactic`.

The assistant rejected placing confidence in the registry, on the grounds that confidence is not an intrinsic property of a vocabulary term. It is a property of a specific planner assignment for a specific scene.

The assistant initially proposed output-level fields such as:

- `sceneTreatmentConfidence`
- potentially `unitTreatmentConfidence`
- and a reason trace such as `sceneTreatmentBasis`.

The assistant also cautioned against fake numerical precision in a deterministic heuristic system and suggested categorical confidence or reason traces could be more honest.

### 3.14 User preference: human-reviewable reason over confidence value

The user explicitly preferred reason statements over confidence values:

> “Yes, a reason statement is better than a value. The point would be something human reviewable.”

This is a significant user decision because it clarifies that the objective is explainability and reviewability rather than probabilistic self-estimation.

The user then asked whether `render-plan.schema.v1.json` was the schema to update.

The assistant answered yes and proposed adding planner-reason fields to the render-plan schema, e.g.:

- `sceneTreatmentReason`
- potentially `unitTreatmentReason`

with short symbolic reasons such as:

- `hasList`
- `hasLongList`
- `noMCQ`
- `sceneTreatment=progressive-reveal`
- `semanticRole=List`.

The assistant recommended keeping these reasons short and consistent rather than verbose prose.

### 3.15 Uploaded `render-plan.schema.v2.json` and unresolved reconciliation

The user then uploaded a schema already modified in a somewhat different direction and asked whether it was functionally the same and where else scripts would need updating.

The uploaded schema identifies itself as:

- `$id`: `https://trainstorm.ai/schema/render-plan.schema.v2.json`
- title: `Trainstorm Render Plan Schema v2`

Its description states that v2 adds `plannerAssessment` to `scenePlan` for classification confidence tracking and human review flagging.

The `plannerAssessment` definition contains:

- `score` from 0.0 to 1.0;
- `rationale` as a plain-language explanation;
- `reviewFlag` boolean;
- optional `dominantSignals` array.

The definition explicitly says it is not consumed by runtime and is intended for tuning, review flagging, and reasoning traceability.

The schema as uploaded still contains a generic definition named `treatment` and requires `treatment` on each `renderUnit`, despite the conversation having already renamed the planner field to `rhetoricalTreatment`. It also does not visibly define or require the newly introduced `sceneTreatment`, `sceneSignals`, or `unitTreatment` fields in the provided schema text.

The conversation ended before the assistant answered the user's reconciliation question. Therefore the compatibility and exact code/schema updates remain unresolved in this conversation.

## 4. Explicit User Decisions and Constraints

### 4.1 Follow planner-first implementation order
**Status:** Explicitly accepted.

The user accepted the recommendation to teach the planner to classify/direct experience before mapping those decisions to runtime behavior:

> “Makes sense. Let's follow your best suggested path.”

### 4.2 Encode the distinction between rhetorical handling and experiential role
**Status:** Explicit user decision.

The user chose to rename the existing generic treatment field because they want later schema inspection to preserve architectural thinking:

> “I think I do want to rename semantic treatment to differentiate from directed experiential role.”

### 4.3 Use `rhetoricalTreatment` for the renamed lower-level field
**Status:** Clearly accepted through implementation.

The user completed the rename and reported that only `treatmentHint` remained under the old substring.

### 4.4 Preserve `treatmentHint` as a distinct visual-intent concept
**Status:** Clearly accepted through implementation.

After the rename, the user confirmed that only `treatmentHint`s remained; no request was made to rename them, and subsequent discussion treated them as intentionally separate.

### 4.5 Treat schema artifacts as architectural memory
**Status:** Explicit user preference.

The user said they study schemas later “to understand the thinking at the time” and are teaching themselves to do this. Therefore naming and schema structure should encode conceptual distinctions rather than rely on undocumented memory.

### 4.6 Keep a stable controlled vocabulary inside CGEN
**Status:** Explicitly accepted.

The user accepted moving the expanded treatment registry into a `knowledge` location:

> “Cool. Added to 'knowledge'.”

### 4.7 Prefer human-reviewable reasons over abstract confidence values
**Status:** Explicit user decision.

The user rejected confidence-as-value as the primary idea and preferred human-reviewable reasoning:

> “Yes, a reason statement is better than a value. The point would be something human reviewable.”

### 4.8 Continue along the core planner/runtime path after registry work
**Status:** Explicitly stated.

After moving the registry, the user asked to return to the core path rather than continue expanding side documentation.

## 5. Assistant Proposals

### 5.1 Add an Experience Treatment System
**Proposal:** Add scene-level and unit-level treatment vocabularies to model experience staging.  
**User response:** Accepted in principle and implementation path.

### 5.2 Minimal scene-treatment vocabulary
**Proposal:** `didactic-flow`, `emphasis-frame`, `progressive-reveal`, `contrast-frame`, `assessment-beat`.  
**User response:** No explicit item-by-item approval, but the vocabulary was incorporated into planner work and render-plan output. Treat as provisionally accepted through implementation, not independently ratified.

### 5.3 Minimal unit-treatment vocabulary
**Proposal:** `primary-assertion`, `supporting-context`, `emphasis-beat`, `progressive-step`, `contrast-pair`, `interaction-prompt`.  
**User response:** Incorporated into implementation. Provisionally accepted through use.

### 5.4 Planner-first sequencing
**Proposal:** Name/represent experience in the planner before runtime mapping.  
**User response:** Explicitly accepted.

### 5.5 Deterministic `sceneSignals`
**Proposal:** Derive signals such as MCQ presence, list length, Impact presence, sparsity, and contrast indicators before assigning scene treatment.  
**User response:** Incorporated into code. Accepted through implementation.

### 5.6 Keep runtime unchanged during classification validation
**Proposal:** Do not yet add CSS, animation, timing, or component switching based on treatment.  
**User response:** Followed throughout the conversation. No explicit rejection.

### 5.7 Rename generic `treatment` to `rhetoricalTreatment`
**Proposal:** Use `rhetoricalTreatment` rather than `semanticTreatment`, `contentTreatment`, etc.  
**User response:** Explicitly accepted and implemented.

### 5.8 Keep `treatmentHint` unchanged
**Proposal:** Preserve this as visual-intent/downstream-render vocabulary.  
**User response:** Accepted through implementation.

### 5.9 Store treatment vocabulary as an in-repository registry
**Proposal:** Put `treatment-registry.md` under `cgen/knowledge/`, mark it canonical, potentially add machine-readable form later.  
**User response:** Accepted; user added it to `knowledge`.

### 5.10 Validate planner judgments before runtime behavior
**Proposal:** Human-review scene-by-scene treatment assignments and tune rule thresholds/signals.  
**User response:** Conversation moved in this direction; no completed review loop is shown before the schema discussion.

### 5.11 Add confidence/basis at plan-output level, not registry level
**Proposal:** Confidence belongs on specific assignments, not vocabulary definitions.  
**User response:** User refined this proposal, preferring human-readable reasons over numeric confidence.

### 5.12 Add reason fields to render-plan schema
**Proposal:** `sceneTreatmentReason` and optionally `unitTreatmentReason`, using compact symbolic reasons.  
**User response:** The user instead presented an already-modified v2 schema with `plannerAssessment`; reconciliation remained unanswered.

### 5.13 `plannerAssessment` as score/rationale/review flag
**Proposal status:** This structure came from the user's uploaded schema, not from the assistant's prior proposal. The assistant had not yet evaluated it before the conversation ended.

## 6. Concepts and Components

### 6.1 Compiler pipeline

The conversation preserves a staged system:

1. Project corpus
2. Script
3. Semantic model
4. Render plan
5. Runtime course
6. Browser experience

The semantic model is the boundary between interpretation and deterministic compilation.

### 6.2 Semantic layer

Referenced semantic artifacts include:

- scenes;
- `sceneIntent`;
- `learnerOutcome`;
- semantic element types including `Head`, `Paragraph`, `Impact`, `List`, `Statement`, `MCQ`;
- optional `modalityHint`.

The semantic layer is intended to encode meaning and instructional intent without binding presentation assets.

### 6.3 Planning layer

Primary implementation artifact:

`planner/planCourse.js`

Existing/planned planning dimensions include:

- `sceneIntent`
- `learningRole`
- `experienceStrategy`
- `instructionalIntent`
- `rhetoricalWeight`
- `rhetoricalTreatment`
- `learnerAction`
- `visualIntent`
- `sceneSignals`
- `sceneTreatment`
- `unitTreatment`
- completion plan
- narration plan
- motion plan.

### 6.4 Experience Treatment System

#### Scene-level vocabulary

- `didactic-flow`
- `emphasis-frame`
- `progressive-reveal`
- `contrast-frame`
- `assessment-beat`

#### Unit-level vocabulary

- `primary-assertion`
- `supporting-context`
- `emphasis-beat`
- `progressive-step`
- `contrast-pair`
- `interaction-prompt`

### 6.5 Rhetorical planning vocabulary

The previous generic `treatment` field was renamed to:

`rhetoricalTreatment`

Examples discussed or visible in outputs:

- `summary-highlight`
- `supporting-detail`
- `emphasized-assertion`
- `plain-exposition`
- `knowledge-check`

The uploaded v2 schema still enumerates the older definition name `treatment` and includes additional values such as:

- `framed-quote`
- `progressive-reveal`
- `comparison`
- `transition-marker`
- `reflective-pause`.

This discrepancy is unresolved.

### 6.6 Visual intent

`treatmentHint` remains part of `visualIntent`, distinct from rhetorical or experiential treatments.

The uploaded v2 schema defines visual treatment hints:

- `text-only`
- `supporting-image`
- `icon-support`
- `diagram`
- `structured-cards`
- `contrast-layout`
- `hero-visual`.

It also defines:

- `visualSupportLevel`
- `visualRole`
- `visualIntent`.

### 6.7 Scene signals

The deterministic classifier uses scene-level evidence such as:

- element count;
- MCQ presence;
- Impact presence;
- list presence;
- long-list status;
- sparsity;
- contrast signals.

These signals are intended both to drive classification and to make it inspectable.

### 6.8 Treatment registry

A Markdown registry was created to govern planning vocabulary.

Its conceptual chain was:

`what it is → how it is framed → how it should land → how it might render`

The user moved the registry into CGEN's `knowledge` area.

### 6.9 Render plan schema

The user supplied a `render-plan.schema.v2.json` with:

- Draft-07 JSON Schema;
- `meta`;
- `globalDirectives`;
- `scenePlans`;
- semantic/planning vocabularies;
- render unit definitions;
- runtime-oriented `renderType`, `styleRef`, `primitive`;
- narration, motion, completion plans;
- `plannerAssessment`.

### 6.10 `plannerAssessment`

The uploaded schema defines:

```text
plannerAssessment
├── score          number 0..1
├── rationale      non-empty string
├── reviewFlag     boolean
└── dominantSignals[] optional
```

Its own description says it is not consumed by runtime and is used for tuning, review flagging, and reasoning traceability.

This object is architecturally adjacent to the user's preference for human-reviewable reason traces, but it also retains the numerical confidence model the user had just questioned.

### 6.11 Runtime/compiler boundary

The conversation repeatedly protects the rule that experience classification should be planned before runtime execution.

Runtime concerns explicitly deferred include:

- CSS branching;
- animation;
- timing;
- component swapping;
- stronger visual treatment;
- asset binding.

## 7. Problems and Design Pressures

### 7.1 Functional but flat output

The central product problem was that the pipeline worked technically but lacked:

- energy;
- staging;
- hierarchy;
- emotional weight;
- rhythm;
- pacing.

This pressure directly motivated the experience-treatment layer.

### 7.2 Layer collapse risk

The conversation repeatedly guards against pushing runtime concerns upstream or using component behavior as a substitute for planning logic.

The user wanted to understand the architecture conceptually while building it, which reinforced planner-first sequencing.

### 7.3 Overloaded vocabulary

The existing `treatment` field became ambiguous once experience staging was introduced. Without renaming, future readers could not tell whether a treatment described rhetorical handling or experiential direction.

### 7.4 Architectural memory and schema legibility

The user specifically wants schemas to preserve the reasoning behind design choices. This creates a pressure toward precise names, controlled vocabularies, and inspectable reasoning rather than opaque implementation shortcuts.

### 7.5 Need for human-reviewable planner logic

A simple classification label such as `didactic-flow` is not enough if a reviewer cannot tell why the planner chose it.

This motivated discussion of:

- confidence;
- reasons;
- dominant signals;
- review flags;
- inspectable planner assessments.

### 7.6 False precision risk

The assistant explicitly warned that numerical confidence values may imply probabilistic rigor that a deterministic heuristic planner does not actually possess.

This pressure supports reason-first traceability.

### 7.7 Vocabulary drift

Once terms such as `sceneTreatment`, `unitTreatment`, `rhetoricalTreatment`, and `treatmentHint` exist across code, schemas, compiler, and runtime, keeping them only in personal notes would risk divergence. The treatment registry was moved into the repository to reduce this drift.

### 7.8 Schema/code drift

The uploaded schema v2 visibly still uses required `treatment` on `renderUnit`, even though the planner discussion and generated render plan had moved to `rhetoricalTreatment`.

The uploaded schema also does not visibly include the new treatment fields and scene-signal fields discussed earlier.

This is an immediate example of the exact drift risk the conversation is trying to prevent.

## 8. Revisions and Superseded Ideas

### 8.1 Generic `treatment` field superseded by `rhetoricalTreatment`

Earlier planner code used generic `treatment` for values such as `summary-highlight`, `supporting-detail`, and `emphasized-assertion`.

This was superseded after the user explicitly requested a name that preserved the conceptual distinction from directed experience.

Current conversational model:

- `rhetoricalTreatment` = rhetorical framing;
- `sceneTreatment` / `unitTreatment` = experience direction.

### 8.2 Runtime-first experimentation rejected in favor of planner-first

The user initially considered whether mapping treatments directly to existing components might teach the concept more naturally.

The assistant recommended the opposite: first make the planner classify the experience, then map it to runtime.

The user explicitly accepted the planner-first path.

### 8.3 Initial nested `getSceneSignals()` implementation corrected

An intermediate planner version accidentally declared `getSceneSignals()` inside itself and placed `elements` in the wrong scope.

The assistant identified this and supplied a corrected version based on shared `getSceneElements(scene)` extraction.

### 8.4 Confidence value de-emphasized in favor of reason trace

The user initially asked whether the registry needed a confidence value.

The assistant relocated confidence to plan assignments rather than the registry, then proposed numeric or categorical confidence plus reasons.

The user sharpened the requirement:

> a reason statement is better than a value; the point is human reviewability.

Thus reason traceability is the later user preference.

### 8.5 `sceneTreatmentReason` proposal potentially displaced by `plannerAssessment`

The assistant proposed direct reason fields on treatment assignment.

The user then uploaded a v2 schema containing a broader `plannerAssessment` object with score, rationale, review flag, and dominant signals.

Whether `plannerAssessment` should replace direct reason fields, coexist with them, or be simplified toward the user's reason-first preference was not resolved.

### 8.6 Personal progression notes displaced by in-repository registry

The user initially kept the treatment index/registry in progression notes but decided it should become a stable CGEN artifact. The accepted location was the repository's `knowledge` area.

## 9. Unresolved and Deferred Work

### 9.1 Reconcile `render-plan.schema.v2.json` with current planner output

The uploaded schema still references:

- definition `treatment`;
- required render-unit property `treatment`.

The planner conversation had already renamed that field to:

- `rhetoricalTreatment`.

This needs reconciliation.

### 9.2 Add schema support for new experience-treatment fields

The conversation indicates planner output now includes:

- `sceneSignals`
- `sceneTreatment`
- `unitTreatment`

The uploaded v2 schema, as visibly supplied, does not include these fields in `scenePlan` or `renderUnit`.

Whether they are defined elsewhere or omitted from this schema remains unresolved.

### 9.3 Resolve `plannerAssessment` versus reason-first traceability

The user's stated preference is human-reviewable reasoning rather than a confidence value.

The uploaded `plannerAssessment` still requires:

- numeric `score`;
- prose `rationale`;
- boolean `reviewFlag`.

Questions left unresolved:

- Should `score` remain?
- Should `rationale` be compact symbolic reasons or plain-language prose?
- Should `dominantSignals` be the primary review trace?
- Should treatment-specific reasons be embedded directly beside `sceneTreatment`/`unitTreatment`?
- Is `reviewFlag` deterministic from rule ambiguity, signal conflicts, fallback status, or score threshold?

### 9.4 Script updates required after schema v2 changes

The user explicitly asked which scripts must be updated after changing the schema.

The conversation ended before this was answered.

Likely candidates visible from the conversation include at least:

- `planner/planCourse.js`, because it emits render-plan fields;
- any render-plan validator;
- `compiler/renderPlanToCourse.js`, if it validates or consumes affected properties;
- tests/fixtures/sample `render-plan.json`;
- any schema reference or planner-version metadata.

This list is an inference from visible architecture, not a completed user-approved change set.

### 9.5 Planner classification tuning

The assistant suggested reviewing 6–8 scenes and tuning:

- sparse/dense thresholds;
- contrast detection;
- long-list/progression thresholds;
- default `didactic-flow` behavior.

A full human-review/tuning pass is not shown as completed.

### 9.6 Runtime expression of treatment

Still deferred:

- mapping treatment to spacing;
- reveal timing;
- component selection;
- CSS;
- motion;
- visual hierarchy;
- runtime behavior.

The conversation consistently treats this as downstream of planner validation.

### 9.7 Possible machine-readable treatment registry

The assistant suggested that the Markdown registry could eventually gain a machine-readable form, e.g. `treatment-registry.json`.

The user did not explicitly accept or implement this in the visible conversation. It remains a future proposal.

### 9.8 Possible derivation-rules section in registry

The assistant suggested later adding a section recording:

- trigger conditions;
- whether derivation is deterministic, heuristic, or LLM-derived.

This was not implemented in the visible conversation.

## 10. Referenced Artifacts

### Uploaded/visible artifacts

- `trainstorm_rehydration.md`
  - Checkpoint describing CGEN semantic → planning → runtime pipeline and the need for an Experience Treatment Layer.

- `Pasted code.js` / multiple uploaded revisions
  - `planner/planCourse.js` content at different points in the implementation.

- uploaded `render-plan.json` content
  - Used to verify that `sceneTreatment`, `unitTreatment`, and `rhetoricalTreatment` were serialized into planner output.

- `cgen_treatment_index.md`
  - Downloadable treatment table generated in this conversation.

- `cgen_treatment_registry.md`
  - Expanded registry generated in this conversation and subsequently moved by the user into CGEN's `knowledge` area.

- uploaded `render-plan.schema.v2.json`
  - User's modified planning-layer JSON Schema including `plannerAssessment`.

### Repository paths and files mentioned

- `planner/planCourse.js`
- `compiler/renderPlanToCourse.js`
- `courses/demo/course.semantic.json`
- `courses/demo/render-plan.json`
- `courses/demo/course.json`
- `courses/demo/index.html`
- `courses/demo/main.js`
- `engine/`
- `cgen/knowledge/treatment-registry.md` (recommended path; user confirmed adding to `knowledge`)
- `render-plan.schema.v1.json`
- `render-plan.schema.v2.json`

### Runtime/interaction concepts mentioned

- RevealCards
- MCQ
- navigation
- narration plan
- motion plan
- completion plan
- primitives
- style refs
- visual intent
- browser runtime.

### Commands referenced

- `node planner/planCourse.js courses/demo/course.semantic.json`
- `node compiler/renderPlanToCourse.js courses/demo/render-plan.json`
- `python -m http.server 8000`

## 11. Provenance Highlights

### Claim: CGEN is conceived as a compiler-like pipeline rather than a simple generator.
**Source:** User-provided rehydration artifact.  
**Evidence:** The checkpoint explicitly calls it a “multi-stage compiler pipeline for learning experiences” and lists the semantic → render-plan → runtime sequence.  
**Status:** Explicit user-provided system description.

### Claim: The semantic model is the handoff from interpretation to deterministic compilation.
**Source:** User-provided rehydration artifact.  
**Evidence:** “The semantic model is the handoff point. Before it = interpretation. After it = compilation.”  
**Status:** Explicit system principle.

### Claim: The missing capability is experience/staging, not basic semantic structure.
**Source:** User-provided rehydration artifact.  
**Evidence:** The system is described as “clear, structured, but flat” and as modeling “meaning and structure” but not “experience and staging.”  
**Status:** Explicit diagnosis in user-supplied checkpoint.

### Claim: Planner-first implementation was chosen over direct runtime mapping.
**Source:** User.  
**Evidence:** After asking which path would be better for conceptual learning, the user accepted: “Makes sense. Let's follow your best suggested path.”  
**Status:** Explicit user decision.

### Claim: Existing generic `treatment` should be renamed to preserve the distinction from directed experiential role.
**Source:** User.  
**Evidence:** “I think I do want to rename semantic treatment to differentiate from directed experiential role.”  
**Status:** Explicit user decision.

### Claim: Schema naming is intended to preserve architectural memory.
**Source:** User.  
**Evidence:** The user said they study schemas later “to understand the thinking at the time” and wanted the distinction encoded.  
**Status:** Explicit user constraint/preference.

### Claim: The user's conceptual distinction is content mechanics versus how language lands in the nervous system.
**Source:** User.  
**Evidence:** “what is it in terms of content nuts and bolts, but also how is it supposed to land in the human nervous system.”  
**Status:** Explicit user conceptual framing.

### Claim: `rhetoricalTreatment`, `sceneTreatment`, and `unitTreatment` were all encoded in render-plan output.
**Source:** Assistant interpretation of user-uploaded render plan.  
**Evidence:** The assistant identified examples where rhetorical and unit treatments differed and where scene treatment drove progressive/assessment classifications.  
**Status:** Assistant-supported observation from uploaded artifact.

### Claim: `treatmentHint` was deliberately left separate.
**Source:** Assistant proposal + user implementation confirmation.  
**Evidence:** The assistant instructed the user not to rename `treatmentHint`; the user later confirmed only `treatmentHint`s remained.  
**Status:** Accepted implementation distinction.

### Claim: The treatment registry became stable in-repository system knowledge.
**Source:** User.  
**Evidence:** After asking where it should live, the user confirmed: “Cool. Added to 'knowledge'.”  
**Status:** Explicit implementation decision.

### Claim: Human-reviewable reasoning is preferred over a confidence value.
**Source:** User.  
**Evidence:** “Yes, a reason statement is better than a value. The point would be something human reviewable.”  
**Status:** Explicit user decision.

### Claim: `plannerAssessment` currently combines confidence scoring and review rationale in the uploaded schema.
**Source:** User-uploaded `render-plan.schema.v2.json`.  
**Evidence:** The visible schema requires `score`, `rationale`, and `reviewFlag`, and optionally records `dominantSignals`.  
**Status:** Explicit artifact content; user asked for reconciliation rather than explicitly approving its final form.

### Claim: The uploaded schema v2 is out of alignment with the just-developed treatment names.
**Source:** Comparison of visible conversation state with user-uploaded schema.  
**Evidence:** Schema v2 still defines/requires `treatment`, while conversation implementation renamed that field to `rhetoricalTreatment`; schema text shown also lacks visible `sceneTreatment`/`unitTreatment` properties.  
**Status:** Inference from visible artifacts; unresolved.

## 12. Candidate Insights for Repository Comparison

The following claims are evidence candidates for later comparison against `trainstorm-core`. They do **not** assert that the repository should change.

### 12.1 Semantic model as interpretation/compilation boundary
- **Claim:** The semantic model should remain the handoff point between LLM interpretation and deterministic compilation.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** pipeline boundaries; semantic schema; planner/compiler separation
- **State:** Settled in the conversation
- **Why it may still matter:** It constrains where subjective interpretation, deterministic rules, and runtime concerns should live.

### 12.2 Explicit experience-direction layer in planning
- **Claim:** CGEN should model experience/staging separately from semantic meaning and runtime rendering.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** planner model; render-plan schema
- **State:** Settled in principle; implementation still evolving
- **Why it may still matter:** It is the core response to the “structured but flat” failure mode.

### 12.3 Scene-level controlled treatment vocabulary
- **Claim:** Scene plans may use a canonical experience-treatment vocabulary including `didactic-flow`, `emphasis-frame`, `progressive-reveal`, `contrast-frame`, and `assessment-beat`.
- **Source status:** `assistant_proposal`
- **Confidence:** Medium-high
- **Likely architectural area:** planning vocabulary; registry; schema enums
- **State:** Provisionally implemented
- **Why it may still matter:** It creates deterministic scene-direction labels that runtime can later interpret.

### 12.4 Unit-level controlled experience vocabulary
- **Claim:** Render units may use experience roles such as `primary-assertion`, `supporting-context`, `emphasis-beat`, `progressive-step`, `contrast-pair`, and `interaction-prompt`.
- **Source status:** `assistant_proposal`
- **Confidence:** Medium-high
- **Likely architectural area:** render-unit planning model
- **State:** Provisionally implemented
- **Why it may still matter:** It provides a second granularity of experience direction below the scene.

### 12.5 Rename generic `treatment` to `rhetoricalTreatment`
- **Claim:** The lower-level rhetorical handling field should be called `rhetoricalTreatment`, not generic `treatment`.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** render-plan schema; planner output; compiler interfaces
- **State:** Settled in conversation and implemented in planner work
- **Why it may still matter:** It prevents conceptual ambiguity and preserves schema readability as architectural memory.

### 12.6 Keep `treatmentHint` separate from rhetorical and experiential treatments
- **Claim:** `treatmentHint` belongs to visual intent/downstream modality and should remain distinct.
- **Source status:** `assistant_proposal`
- **Confidence:** High
- **Likely architectural area:** visual-intent schema
- **State:** Accepted through implementation
- **Why it may still matter:** It prevents visual rendering hints from contaminating rhetorical or experience-direction semantics.

### 12.7 Planner decisions should expose deterministic evidence
- **Claim:** Scene classification should retain signals such as MCQ presence, Impact presence, list length, sparsity, and contrast indicators.
- **Source status:** `assistant_proposal`
- **Confidence:** High
- **Likely architectural area:** planner traceability; render-plan schema
- **State:** Implemented in conversation
- **Why it may still matter:** It supports debugging, tuning, auditability, and human review.

### 12.8 Human-reviewable rationale is more important than confidence scoring
- **Claim:** Planner classifications should expose a reviewable reason statement or evidence trace rather than relying primarily on a confidence number.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** planner assessment; review/governance; schema
- **State:** Settled preference, but schema implementation unresolved
- **Why it may still matter:** It shapes explainability and avoids false probabilistic precision.

### 12.9 Treatment registry should be in-repository knowledge
- **Claim:** Controlled treatment vocabulary should live as a stable artifact in the repository's `knowledge` area rather than only in personal notes.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** repository organization; governance documentation
- **State:** Settled and implemented by user
- **Why it may still matter:** It reduces terminology drift and preserves conceptual contracts across planner/compiler/runtime.

### 12.10 Registry functions as controlled planning vocabulary
- **Claim:** The treatment registry should govern the distinctions among `semanticRole`, `rhetoricalTreatment`, `sceneTreatment`, `unitTreatment`, and `treatmentHint`.
- **Source status:** `assistant_proposal`
- **Confidence:** High
- **Likely architectural area:** ontology/registry; schema governance
- **State:** Accepted through artifact use
- **Why it may still matter:** It gives a durable decision rule for where future planning terms belong.

### 12.11 Runtime should not consume treatment until planner judgments are validated
- **Claim:** Component swaps, CSS, motion, spacing, and timing should remain downstream until treatment classification is human-reviewed and tuned.
- **Source status:** `assistant_proposal`
- **Confidence:** Medium-high
- **Likely architectural area:** planner/runtime interface
- **State:** Followed in conversation; not explicitly declared permanent
- **Why it may still matter:** It protects architectural separation and makes misclassification easier to diagnose.

### 12.12 `plannerAssessment` may be the broader review envelope
- **Claim:** A scene-level `plannerAssessment` object containing rationale, dominant signals, review flag, and possibly confidence can serve as a review/governance envelope.
- **Source status:** `inference`
- **Confidence:** Medium
- **Likely architectural area:** render-plan schema; review workflow
- **State:** Unresolved
- **Why it may still matter:** The uploaded schema already contains this structure, but it needs reconciliation with the user's reason-first preference.

### 12.13 Numeric `score` in `plannerAssessment` may conflict with the user's preference
- **Claim:** Requiring a 0–1 confidence score may be unnecessary or misleading if the planner is deterministic and the real objective is human-readable reasoning.
- **Source status:** `inference`
- **Confidence:** High
- **Likely architectural area:** `plannerAssessment` schema
- **State:** Unresolved
- **Why it may still matter:** The user explicitly preferred reasons over values immediately before presenting the v2 schema.

### 12.14 Schema v2 appears out of sync with planner field names
- **Claim:** `render-plan.schema.v2.json` should be compared against current planner output because the supplied schema still requires `treatment` and does not visibly model all new treatment fields.
- **Source status:** `inference`
- **Confidence:** High
- **Likely architectural area:** schema/code compatibility
- **State:** Unresolved
- **Why it may still matter:** This is a direct content-drift risk and could cause validation failures or semantic ambiguity.

### 12.15 Planner field changes likely require multi-artifact synchronization
- **Claim:** Treatment/schema changes may require coordinated updates to planner output, schema validators, compiler consumption, fixtures/tests, sample render plans, and version metadata.
- **Source status:** `inference`
- **Confidence:** Medium-high
- **Likely architectural area:** build pipeline; validation; tests; compiler
- **State:** Unresolved
- **Why it may still matter:** The user explicitly asked where else scripts must change after schema evolution, and this was not answered before the conversation ended.

---

## Closing Evidence Note

This conversation documents a meaningful architectural shift: CGEN's planner is no longer conceived merely as a structural converter from semantic elements to runtime components. It is being developed as an explicit, deterministic **experience director** whose choices should be inspectable, named with controlled vocabulary, and reviewable by humans before downstream rendering amplifies them.

The clearest user-authored conceptual statement is the distinction between the “content nuts and bolts” of a linguistic payload and “how it is supposed to land in the human nervous system.” The field split among `semanticRole`, `rhetoricalTreatment`, `sceneTreatment`, `unitTreatment`, and `treatmentHint` is the concrete schema-level expression of that distinction in this conversation.

The final unresolved issue is schema reconciliation: the uploaded `render-plan.schema.v2.json` introduces `plannerAssessment`, but its current required fields and legacy `treatment` naming need comparison with the planner state developed earlier in the same conversation.
