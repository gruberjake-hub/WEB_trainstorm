# Trainstorm Rehydration — AE Motion System Design

## 1. Conversation Identity

**Conversation title:** AE Motion System Design

**Visible date:** March 6, 2026, based on the visible project-conversation metadata (`20260306T11:50`). Exact message-level timestamps for the exchange reproduced here are not visible, so no finer-grained chronology is asserted.

**Rehydration timestamp:** 2026-08-13 14:53 America/Chicago

**Evidence boundary:** This rehydration uses only the visible contents of this conversation. It does not rely on saved memory, other chats, current repository contents, or assumptions about what `trainstorm-core` later became.

---

## 2. Relevance Summary

This conversation is relevant to the architecture represented by `trainstorm-core` because it exposes a production-layer tension between **dynamic, reusable, localization-ready content** and **renderer stability**.

The most architecturally important user statement is that the After Effects composition uses “a lot of expressions to link text back to Excel in case it needs a language translation.” That reveals an attempt to make AE compositions data-driven and localization-ready by keeping text externally governed rather than manually embedded. The immediate downside is that the user suspects this expression-heavy linkage is “causing havoc” in After Effects.

The assistant then proposed an architectural separation: centralize external-data access, reduce expression evaluation, pre-bake data where possible, and treat AE primarily as a renderer rather than as a data-processing runtime. Although those proposals were not explicitly accepted by the user in the visible exchange, they identify a possible design pressure relevant to any governed content-to-production pipeline: **the canonical content source and localization logic may need to live upstream of the renderer, while AE receives stable, renderer-ready inputs**.

A second relevant thread concerns motion-expression behavior. A visible earlier assistant response identifies perpetual post-intro motion caused by a sine-wave “idle drift” block, then offers a stable expression variant and an optional decaying-settle variant. That material suggests the conversation also addressed the need for **predictable, reusable motion primitives whose runtime behavior terminates deterministically rather than drifting forever**.

Taken together, the conversation suggests two architectural concerns that may merit later repository comparison:

1. localization-ready source text should remain externally governed while avoiding per-frame data-system behavior inside AE; and
2. reusable motion primitives should have deterministic lifecycle behavior suitable for compilation or governed reuse.

---

## 3. Chronological Rehydration

### 3.1 Motion-expression instability: perpetual idle drift

A visible prior assistant response diagnoses a motion-expression problem in which a layer continued moving indefinitely after its intro animation. The assistant identifies the cause as a post-intro `drift` value continuously added to the final position:

> `var p = endPos + drift;`

and later:

> `var base = endPos + drift;`

The response explains that sine functions using continually increasing `time` produce perpetual motion:

> `Math.sin(time*0.9 + index)*driftPx`

The assistant proposes two variants:

- a **stable version** that holds at `endPos` after the intro and before the outro;
- a **brief decaying settle** version in which residual motion decays over a fixed `settleDur`.

The assistant explicitly recommends the first version unless a residual settle is intentionally desired.

**Architectural significance:** This introduces a distinction between uncontrolled procedural motion and bounded motion behavior. In a reusable motion system, primitives should ideally have clear phases—intro, hold, outro—and any settle behavior should be explicit and time-bounded.

**Source status:** Assistant proposal and diagnosis. No visible user acceptance or rejection is shown in the current evidence window.

### 3.2 Composition becomes invisible while editing, then self-recovers

The user reports an After Effects composition where:

> “the stage is suddenly invisible”

They state that they did not intentionally change settings and that:

> “I can see the composition in other comps, but I absolutely cannot find it when I try to edit.”

The assistant initially offers a broad troubleshooting set: zoom state, wrong viewer, hidden layers, off-frame content, camera state, transparency, timeline position, expression behavior, scale/anchor state, and related possibilities.

The user then reports that the problem resolved without intervention:

> “No, it's working now. And I didn't do anything. My AE will simply NOT STOP screwing up.”

This changes the problem from a deterministic authoring error to a suspected intermittent application/runtime instability.

The assistant interprets the self-recovery as consistent with a viewer, GPU, cache, panel, or expression-evaluation desynchronization and proposes practical mitigation ideas such as purging cache, toggling GPU/software rendering, forcing redraw, and periodically restarting AE.

**Architectural significance:** The production renderer is behaving nondeterministically under the current project load. Even if the exact cause is not proven, the incident creates a design pressure to reduce dependence on fragile runtime behavior inside AE.

**Source status:** User observation is explicit. Assistant causal explanation remains a proposal/inference, not a confirmed diagnosis.

### 3.3 User identifies expression-heavy Excel linkage for localization

The user then supplies the most important architectural detail:

> “Yeah, I'm using a lot of expressions to link text back to Excel in case it needs a language translation. But I think it's causing havoc.”

This establishes three explicit facts:

1. the AE composition uses many expressions;
2. those expressions link text to Excel;
3. the purpose is to preserve the possibility of language translation.

It also establishes a user hypothesis, not a confirmed diagnosis:

4. the expression-heavy design may be contributing to AE instability.

This is the clearest precursor to a governed localization/rendering pipeline in the conversation. The user is already trying to avoid hard-coding text directly into final production artifacts, presumably so translated text can be substituted centrally.

### 3.4 Assistant reframes AE as renderer rather than data engine

In response, the assistant characterizes the current implementation as one where many layers may repeatedly perform external-data lookups and language-selection logic. The assistant argues that this can create a large expression-evaluation surface and proposes several architectural changes.

The main proposal is:

> “AE should be the renderer, not the data engine”

The assistant recommends:

- a **single source / many consumers** pattern in which one controller performs external-data lookup and other layers reference centralized values;
- using `posterizeTime(0)` for content that does not need per-frame reevaluation;
- **pre-baking** data when runtime dynamism is unnecessary;
- reducing “expression surface area” by asking whether each behavior genuinely needs to remain dynamic;
- moving data preparation outside AE and feeding AE “clean, final inputs”;
- potentially producing “AE-ready JSON / text” or using JSX to populate text;
- longer-term, creating a “Trainstorm-compatible AE bridge” where upstream logic outputs AE-ready data and AE performs rendering with minimal expressions.

The assistant also describes the current design as effectively creating:

> “A mini runtime engine… inside AE’s expression system”

and suggests that this may exceed what AE expressions are best suited to do.

**Architectural significance:** This introduces a possible separation-of-concerns boundary between canonical/localizable content, transformation/compilation, and rendering.

**Source status:** Assistant proposal. The user did not visibly accept, reject, or modify these proposals in the current exchange.

---

## 4. Explicit User Decisions and Constraints

Only explicit user statements or clearly confirmed constraints are included here.

### 4.1 Localization must remain possible

The user explicitly states that text is linked back to Excel:

> “in case it needs a language translation.”

This establishes a production requirement that the system preserve a path for language substitution or localization rather than relying exclusively on manually embedded text inside AE.

**Status:** Explicit user constraint.

### 4.2 The current implementation uses many AE expressions

The user states:

> “I'm using a lot of expressions”

This is a description of the current production architecture rather than a preference, but it is relevant as an explicit implementation fact.

**Status:** Explicit user implementation detail.

### 4.3 Excel is currently used as the external text source

The user states that expressions:

> “link text back to Excel”

This makes Excel the currently visible external source mechanism for AE text.

**Status:** Explicit user implementation detail.

### 4.4 The user suspects the expression-heavy approach is destabilizing AE

The user says:

> “But I think it's causing havoc.”

This is a user hypothesis, not a confirmed root cause.

**Status:** Explicit user concern; tentative causal interpretation.

### 4.5 Intermittent AE instability is unacceptable enough to be a recurring concern

The user says:

> “My AE will simply NOT STOP screwing up.”

This indicates the invisible-stage incident is not perceived as an isolated anomaly but part of a recurring instability pattern.

**Status:** Explicit user problem statement.

No explicit user decision to replace Excel, remove expressions, adopt JSON, adopt JSX, centralize lookups, or restructure the renderer is visible in this conversation.

---

## 5. Assistant Proposals

### 5.1 Replace perpetual idle drift with deterministic hold behavior

**Proposal:** Remove continuous sine-wave drift after the intro so the layer reaches and holds a stable final position.

**Visible rationale:** A time-driven sine wave continues changing forever and therefore never truly settles.

**User response status:** No visible response in the current evidence window.

### 5.2 Optional bounded settle behavior

**Proposal:** If some residual motion is aesthetically desired, use a short `settleDur` with a decaying amplitude rather than permanent drift.

**User response status:** No visible response.

### 5.3 Treat self-resolving invisibility as possible application/runtime instability

**Proposal:** Consider GPU, viewer/panel desynchronization, cache corruption, or expression evaluation as possible causes of the disappearing composition.

**User response status:** The user subsequently introduced heavy expression/Excel linkage as a possible source of instability, which is compatible with one of the assistant’s hypotheses but does not confirm it.

### 5.4 Centralize external-data access

**Proposal:** Use a single “DATA CONTROLLER” or equivalent layer to perform external-data lookups, with other text layers consuming centralized values rather than independently querying the source.

**User response status:** No visible acceptance or rejection.

### 5.5 Reduce unnecessary per-frame expression evaluation

**Proposal:** Use `posterizeTime(0)` for data expressions that do not need to change over time.

**User response status:** No visible acceptance or rejection.

### 5.6 Pre-bake data when runtime dynamism is unnecessary

**Proposal:** Populate text before or at build/render setup time rather than requiring every frame to dynamically resolve external source data.

**Possible mechanisms mentioned:** AE-ready JSON/text or JSX-based population.

**User response status:** No visible acceptance or rejection.

### 5.7 Reduce expression surface area

**Proposal:** Keep expressions only where dynamic runtime behavior is truly necessary.

**User response status:** No visible acceptance or rejection.

### 5.8 Separate data preparation from rendering

**Proposal:** Move data preparation outside After Effects and feed AE clean, final, renderer-ready inputs.

**Key formulation:** “AE should be the renderer, not the data engine.”

**User response status:** No visible acceptance or rejection.

### 5.9 Potential “Trainstorm-compatible AE bridge”

**Proposal:** Create an upstream bridge/compiler that outputs AE-ready data, allowing AE to consume stable content with minimal expression logic.

**User response status:** No visible acceptance or rejection.

---

## 6. Concepts and Components

### 6.1 After Effects as production renderer

After Effects is the visible production environment in which text, compositions, expressions, and reusable motion behavior are authored and rendered.

### 6.2 Externalized text source

Excel is explicitly used as an external source for text so the composition can support later language translation.

### 6.3 Expression-linked localization

The current method uses AE expressions to connect text layers back to Excel. This is a form of runtime or quasi-runtime data binding inside the motion project.

### 6.4 Data controller pattern

Introduced by the assistant: one centralized layer or controller would own source-data lookup while downstream layers consume values from it.

### 6.5 AE-ready intermediate data

Introduced by the assistant: JSON, text, or another prepared representation could become an intermediate artifact supplied to AE after upstream transformation.

### 6.6 JSX population

Introduced by the assistant as a possible script-driven mechanism to populate AE text without maintaining continuous runtime lookups.

### 6.7 Deterministic motion primitive

Implied by the corrected motion expression: a reusable primitive can have bounded stages such as:

- intro;
- stable hold;
- outro;

with optional settle behavior that decays within a defined duration.

### 6.8 Global motion controls

The visible corrected expression references a global controls composition and layer:

- `__GLOBAL_CONTROLS_EXECUTIVE__`
- `__GLOBAL_CONTROLS__`

and retrieves shared controls such as:

- `In (sec)`
- `Out (sec)`
- `In Delay (sec)`
- `Out Delay (sec)`
- `Slide X (px)`
- `Slide Y (px)`
- `Expo Ease`
- `Drift (px)`

This suggests a reusable motion-control system in which multiple elements can inherit common motion parameters.

**Evidence caution:** The expression is visible in the assistant-provided material, but the current conversation does not establish who originally authored the global-control architecture or whether the user had formally adopted it.

### 6.9 Renderer/data-engine boundary

Introduced by the assistant as an architectural principle: content retrieval, language logic, and transformation should potentially occur upstream, while AE should focus on rendering prepared inputs.

---

## 7. Problems and Design Pressures

### 7.1 Intermittent nondeterministic AE behavior

The composition became invisible during editing but remained visible when nested elsewhere and later recovered without user intervention.

This is a serious production pressure because it complicates debugging: a failure that self-resolves can be difficult to reproduce or diagnose.

### 7.2 High expression count

The user explicitly reports “a lot of expressions.” High expression surface area can make projects harder to inspect, debug, and reason about even before any performance claim is made.

### 7.3 Localization requirement creates dynamic-data pressure

The user wants text to remain translation-ready. This motivates keeping content separate from visual composition but creates a question of **where** that separation should be implemented.

The current answer is Excel-linked AE expressions. The assistant proposes moving more of that responsibility upstream.

### 7.4 Renderer fragility versus reusable-system ambition

The user’s workflow attempts to make AE more system-like: text is externally linked, behavior is expression-driven, and motion uses reusable controls. The visible failures suggest a tension between reuse/dynamism and AE stability.

### 7.5 Perpetual procedural motion as a failure mode

The idle-drift expression demonstrates how a reusable procedural animation can unintentionally remain active forever. This creates a need for explicit lifecycle constraints in motion primitives.

### 7.6 Debugging cost

When a composition disappears and then returns without intervention, or when many layers depend on expression logic, the cost of identifying a single root cause rises substantially.

### 7.7 Translation changes must not require manual re-authoring

The Excel linkage exists specifically to preserve translation flexibility. Any replacement architecture must retain this functional requirement.

---

## 8. Revisions and Superseded Ideas

### 8.1 Permanent idle drift → stable hold

The visible assistant diagnosis treats perpetual drift as undesirable. The revised stable expression removes post-intro drift entirely.

This is a clear supersession inside the assistant’s proposed motion logic:

**Earlier behavior:** intro → continuous drift → outro  
**Revised behavior:** intro → hold → outro

### 8.2 Permanent idle drift → optional bounded settle

A second variant preserves some organic motion but constrains it to a short post-intro settle window.

This does not supersede the stable-hold version; it is an optional alternative. The assistant explicitly prefers the stable version unless residual settle is intentionally desired.

### 8.3 Direct per-layer external lookup → proposed centralized or pre-baked data

The current user implementation uses many expressions linked to Excel.

The assistant proposes that this be displaced by one or both of:

- centralized lookup; and
- upstream/pre-baked population.

Because the user did not visibly confirm a change, this remains a proposed revision rather than an adopted one.

### 8.4 AE as mini runtime → proposed AE as renderer

The assistant reframes the architecture from a dynamic runtime embedded in AE toward a rendering endpoint receiving prepared data.

Again, this is a proposed conceptual revision, not an explicit user decision.

---

## 9. Unresolved and Deferred Work

### 9.1 Root cause of AE instability remains unproven

The user suspects heavy expressions are “causing havoc,” but no controlled test is shown that establishes causation.

Unresolved questions include whether instability comes primarily from:

- expression evaluation;
- Excel/CSV access;
- GPU rendering;
- cache/viewer state;
- AE bugs;
- interactions among these factors.

### 9.2 No migration plan from Excel-linked expressions is finalized

The assistant suggests several alternatives, but the visible conversation does not choose among them.

### 9.3 No canonical localization data format is selected

Excel is the current source. JSON is mentioned by the assistant as a possible AE-ready intermediate representation, but not adopted.

### 9.4 No compiler or bridge specification is defined

The “Trainstorm-compatible AE bridge” is only a high-level assistant proposal. No schema, interface, stable identifier strategy, validation behavior, or render contract is defined here.

### 9.5 No proof that centralized lookup would resolve instability

Centralization is an assistant optimization proposal. The conversation does not benchmark it.

### 9.6 No rule is established for what remains dynamic in AE

The assistant proposes reducing expression surface area, but no formal classification is created for:

- build-time data;
- render-time data;
- frame-time animation;
- localization variables;
- layout-responsive values;
- global style controls.

### 9.7 No localization workflow beyond text substitution is specified

The user’s requirement is only that language translation remain possible. This conversation does not address:

- text expansion/contraction;
- font fallback;
- right-to-left layouts;
- locale-specific line breaks;
- terminology governance;
- translation memory;
- voiceover localization;
- culturally adaptive visuals.

---

## 10. Referenced Artifacts

### 10.1 After Effects composition

The user refers to a composition whose stage temporarily became invisible while editing.

### 10.2 Excel

Explicitly identified by the user as the external source to which AE text is linked for potential translation.

### 10.3 AE expressions

Explicitly identified by the user as heavily used in the current composition architecture.

### 10.4 Motion expression with global controls

Visible assistant-provided code references:

- `__GLOBAL_CONTROLS_EXECUTIVE__`
- `__GLOBAL_CONTROLS__`

and shared timing/motion controls.

### 10.5 Stable motion-expression variant

Assistant-provided code removing post-intro drift.

### 10.6 Decaying-settle motion-expression variant

Assistant-provided alternative that allows short residual motion and then stops.

### 10.7 JSON

Mentioned by the assistant as a possible AE-ready representation.

### 10.8 JSX

Mentioned by the assistant as a possible scripting mechanism for populating text.

### 10.9 Trainstorm-compatible AE bridge

Mentioned by the assistant as a possible future integration concept. No implementation artifact is shown.

### 10.10 `trainstorm-core`

Referenced only by the user in the rehydration request as the repository against which this evidence may later be compared. No repository contents are visible or used here.

---

## 11. Provenance Highlights

### Claim: The current AE workflow uses many expressions linked to Excel for translation flexibility

**Source:** User.

**Supporting excerpt:** “I'm using a lot of expressions to link text back to Excel in case it needs a language translation.”

**Interpretation boundary:** This directly supports externalized, translation-ready text. It does not prove any specific localization architecture beyond Excel-linked expressions.

### Claim: The user suspects the expression architecture contributes to AE instability

**Source:** User.

**Supporting excerpt:** “But I think it's causing havoc.”

**Interpretation boundary:** This is a hypothesis, not a verified cause.

### Claim: AE showed intermittent self-resolving composition visibility failure

**Source:** User.

**Supporting paraphrase:** The user reported that the stage was suddenly invisible while editing, remained visible inside other compositions, and later began working again without any intervention.

**Interpretation boundary:** The precise technical cause is unknown.

### Claim: Reusable procedural motion can accidentally remain active indefinitely

**Source:** Assistant.

**Supporting excerpt:** “The culprit is the idle drift block.”

**Supporting paraphrase:** The assistant identified time-driven sine-wave drift added to `endPos` as the reason a layer never stopped moving after its intro.

**Interpretation boundary:** This applies to the visible expression shown in the assistant response; it is not a universal AE behavior.

### Claim: A bounded intro/hold/outro model was proposed

**Source:** Assistant.

**Supporting paraphrase:** The stable expression defaults to `endPos`, performs the intro before `tIn1`, and performs the outro after `tOut0`.

**Interpretation boundary:** This is an assistant-proposed motion behavior, not a user-confirmed system requirement.

### Claim: External data access should be centralized

**Source:** Assistant.

**Supporting excerpt:** “Single Source → Many Consumers.”

**Supporting paraphrase:** One controller would perform data access and other layers would reference centralized values.

**User acceptance status:** No visible response.

### Claim: AE should be used primarily as renderer rather than data engine

**Source:** Assistant.

**Supporting excerpt:** “AE should be the renderer, not the data engine.”

**User acceptance status:** No visible response.

### Claim: Upstream preparation could output AE-ready data

**Source:** Assistant.

**Supporting paraphrase:** The assistant suggested generating AE-ready JSON/text or using JSX to populate text, reducing live lookup logic in AE.

**User acceptance status:** No visible response.

### Claim: A Trainstorm-compatible AE bridge may be useful

**Source:** Assistant.

**Supporting paraphrase:** The assistant proposed a bridge where a compiler outputs AE-ready data and AE consumes it with minimal expressions.

**Interpretation boundary:** This is a forward-looking assistant proposal only.

---

## 12. Candidate Insights for Repository Comparison

The following items are evidence candidates only. They are not recommendations to modify `trainstorm-core`, and the repository remains the source of truth.

### 12.1 Preserve externally governed text so language substitution does not require manual AE re-authoring

- **Concise claim:** Production text should remain separable from AE visuals so translation can be substituted without rebuilding content manually.
- **Source status:** `user_constraint`
- **Confidence:** High
- **Likely architectural area:** localization; canonical content; renderer integration
- **State:** Settled as a requirement, though the implementation method is not settled
- **Why it may still matter:** This is the explicit reason the user linked AE text back to Excel. Any later architecture should be compared against whether it preserves this capability.

### 12.2 Excel-linked per-layer expressions are a current implementation, not necessarily the desired final architecture

- **Concise claim:** The visible system currently uses many AE expressions linked to Excel.
- **Source status:** `explicit_user_decision`
- **Confidence:** High
- **Likely architectural area:** rendering integration; localization pipeline
- **State:** Current implementation, but potentially unstable and therefore not clearly settled
- **Why it may still matter:** Repository comparison should distinguish the underlying requirement—externalized translation-ready text—from this specific implementation mechanism.

### 12.3 AE expression-heavy data binding may be a production stability risk

- **Concise claim:** Heavy AE expression use tied to external text data may contribute to renderer instability.
- **Source status:** `user_constraint`
- **Confidence:** Medium
- **Likely architectural area:** rendering; runtime boundaries; performance/stability
- **State:** Tentative
- **Why it may still matter:** Even without proven causation, the user identifies this as a recurring production concern that could justify moving logic upstream.

### 12.4 AE may need a narrower responsibility boundary

- **Concise claim:** Treat AE as a renderer receiving prepared inputs rather than as the primary data-processing/runtime layer.
- **Source status:** `assistant_proposal`
- **Confidence:** High as a faithful record of the proposal; not evidence of user adoption
- **Likely architectural area:** compiler/render separation; production adapters
- **State:** Unresolved
- **Why it may still matter:** This is the strongest architectural response proposed to the observed instability and localization requirement.

### 12.5 Centralized data access could reduce expression duplication

- **Concise claim:** One controller could own external-data lookup while downstream layers consume centralized values.
- **Source status:** `assistant_proposal`
- **Confidence:** High
- **Likely architectural area:** AE adapter; rendering runtime; data binding
- **State:** Unresolved
- **Why it may still matter:** It may represent an intermediate migration path between fully dynamic per-layer Excel access and fully precompiled renderer inputs.

### 12.6 Static content should not necessarily reevaluate every frame

- **Concise claim:** Non-animated source-data expressions could be frozen or otherwise prevented from evaluating continuously.
- **Source status:** `assistant_proposal`
- **Confidence:** High
- **Likely architectural area:** renderer performance; expression policy
- **State:** Unresolved
- **Why it may still matter:** If any live expression layer remains in a future AE adapter, a build-time versus frame-time evaluation policy may be useful.

### 12.7 AE-ready intermediate representations may be preferable to direct spreadsheet runtime dependence

- **Concise claim:** An upstream process could transform source content into AE-ready JSON/text or scripted assignments.
- **Source status:** `assistant_proposal`
- **Confidence:** High
- **Likely architectural area:** compiler; intermediate representation; production adapter
- **State:** Unresolved
- **Why it may still matter:** This directly addresses separation between canonical/localizable content and renderer-specific implementation.

### 12.8 A dedicated AE bridge/compiler adapter is a plausible system boundary

- **Concise claim:** A bridge could emit renderer-ready data into AE while minimizing live expression logic.
- **Source status:** `assistant_proposal`
- **Confidence:** Medium
- **Likely architectural area:** renderer adapter; compilation pipeline
- **State:** Tentative
- **Why it may still matter:** It is a concrete integration pattern that could be compared with any existing `trainstorm-core` renderer or export abstraction.

### 12.9 Reusable motion primitives should have deterministic lifecycle phases

- **Concise claim:** Procedural motion should define bounded intro, hold, and outro behavior, with any settle explicitly time-limited.
- **Source status:** `inference`
- **Confidence:** High
- **Likely architectural area:** motion primitives; renderer behavior; template governance
- **State:** Tentative inference from the corrected drift expression
- **Why it may still matter:** It converts a one-off animation bug into a reusable design principle for governed motion systems.

### 12.10 Global motion controls may be part of the desired reusable AE production model

- **Concise claim:** Shared global timing and motion controls can parameterize reusable animation behavior across layers.
- **Source status:** `inference`
- **Confidence:** Medium
- **Likely architectural area:** motion system; template parameters; design tokens
- **State:** Unresolved
- **Why it may still matter:** The visible expression references a global control composition and shared sliders, suggesting a reusable control architecture, but the conversation does not establish its ownership or formal status.

### 12.11 Renderer instability should be treated as an architectural constraint, not only a debugging nuisance

- **Concise claim:** Self-resolving, nondeterministic AE failures create pressure to reduce fragile runtime coupling.
- **Source status:** `inference`
- **Confidence:** Medium
- **Likely architectural area:** production reliability; renderer adapter; validation
- **State:** Unresolved
- **Why it may still matter:** A content system that depends on repeatable generation and rendering may need to design around the failure characteristics of downstream authoring tools.

### 12.12 Localization and motion should remain separable concerns

- **Concise claim:** External text/localization logic and motion behavior should likely be governed independently and composed at render time.
- **Source status:** `inference`
- **Confidence:** Medium
- **Likely architectural area:** separation of concerns; localization; motion/render schema
- **State:** Unresolved
- **Why it may still matter:** The conversation exposes both dynamic text binding and reusable motion expressions as separate sources of complexity inside AE. Their separation may improve maintainability and deterministic output.
