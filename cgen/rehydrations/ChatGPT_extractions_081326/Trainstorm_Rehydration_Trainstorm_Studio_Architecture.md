# Architectural Rehydration: Trainstorm Studio Architecture

> Rehydration generated: 2026-08-13 (America/Chicago)  
> Evidence boundary: This document uses only the visible conversation and its referenced conversation preview. It does not compare against or make claims about the current `trainstorm-core` repository. The repository remains the source of truth for later reconciliation.

## 1. Conversation Identity

- **Conversation title:** Trainstorm Studio Architecture
- **Visible conversation date or date range:** Exact conversation dates are not visible in the supplied material.
- **Rehydration timestamp:** 2026-08-13, America/Chicago.
- **Conversation shape:** The user supplied a product and architecture framing for “Trainstorm Studio.” The assistant responded with a proposed refinement, conceptual object model, runtime pipeline, technical blueprint, MVP sequence, differentiation argument, and design pushbacks. No later user response explicitly accepted, modified, or rejected those assistant proposals in the visible source conversation.

## 2. Relevance Summary

This conversation is directly relevant to a system now represented by `trainstorm-core` because it frames Trainstorm as a configurable, governed runtime that turns client source knowledge into grounded learning interactions. It covers configuration, source ingestion, retrieval, scenario design, orchestration, evaluation, learner experience, evidence, versioning, and deployment boundaries.

The user explicitly rejected the idea of a mere chatbot and described a structured training runtime with hidden instructions, grounding knowledge, scenario logic, and evaluation. The assistant extended that framing into a proposed “training operating system” whose durable objects would include client instances, prompt packs, knowledge collections, scenarios, evaluation packs, and runtime policies. The response also proposed separating generation, retrieval, and evaluation; composing prompts from inspectable layers; and making learner progression and performance evidence more important than the transcript itself.

This material may therefore provide precursor evidence for repository areas involving:

- canonical content and configuration objects;
- knowledge ingestion and retrieval;
- orchestration and model abstraction;
- scenario-native learning interactions;
- evaluation and evidence;
- versioning, governance, and traceability;
- client configuration without bespoke application rebuilds;
- the boundary between Trainstorm-owned instructional logic and commodity infrastructure.

## 3. Chronological Rehydration

### 3.1 User establishes the product intent

The user described **Trainstorm Studio — Client-Configurable AI Training Portal** as a product layer for:

- building custom AI-powered training environments;
- configuring those environments per client;
- demonstrating them as part of learning interventions; and
- eventually scaling them into reusable systems.

The user explicitly stated: **“This is NOT just a chatbot.”** The proposed system was instead a structured training runtime with:

- hidden system prompts;
- grounding knowledge;
- scenario logic; and
- evaluation capability.

The user used platforms such as Azure AI Studio as a conceptual reference for pre-interaction control: inject system instructions, ground responses in source knowledge, and constrain behavior before a learner interacts. The user also expressed a desire to understand and build the architecture personally, even if Azure or another service were later used for production.

### 3.2 User supplies an initial four-layer mental model

The user proposed four layers:

1. **Configuration Layer (Admin Only)** — system prompt, assistant role, tone and behavior rules, scenario type, evaluation rubric, client branding, and uploaded knowledge sources.
2. **Knowledge Layer (Grounding)** — uploaded documents that are chunked and embedded or indexed; example sources included SOPs, training manuals, playbooks, scripts, and policies. The stated purpose was to keep responses grounded in client reality.
3. **Orchestration Layer (Critical)** — user input, relevant-knowledge retrieval, injection of system prompt and context, model call, optional evaluation logic, and response delivery. The user stressed that the learner never interacts with the raw model.
4. **Runtime Layer (Learner Experience)** — a clean interface for scenario setup, chat interaction, coaching feedback, and optional scoring.

This was the explicit user-authored architectural baseline.

### 3.3 Assistant reframes the primary product object

The assistant endorsed the governed-runtime direction but argued that the four-layer model was still “slightly too LLM-centric.” It proposed shifting from a **“portal around a model”** to a **“training operating system that uses models as one component.”**

The assistant proposed the product definition:

> A configuration-driven simulation and coaching runtime for grounded, role-based, evaluable learning interactions.

It further proposed that the primary object should be a **training environment**, not a chat session. That environment would package behavior constraints, retrieval scope, interaction mode, evaluation logic, learner-state handling, UI framing, branding, and deployment settings.

This was an assistant proposal. The visible conversation contains no later user message confirming it.

### 3.4 Assistant proposes a canonical object model

The assistant proposed the following first-class objects:

- **`StudioInstance`** — top-level deployable client environment linking client, branding, default mode, knowledge collections, prompt pack, evaluation pack, runtime policy, UI shell, and deployment profile.
- **`ClientConfig`** — shared client defaults such as display name, branding tokens, compliance controls, data retention, transcript export permissions, model-training restrictions, and default tone.
- **`PromptPack`** — a bundle rather than a single system prompt, including role definition, behavior rules, per-mode instructions, fallback behavior, and version metadata.
- **`KnowledgeCollection`** — named retrieval corpus with document membership and retrieval policy such as `top_k`, minimum score, and citation requirements.
- **`KnowledgeDocument`** — source file plus metadata and derived processing artifacts, including source type, URI, version, authority, audience, parser, chunk count, and embedding model.
- **`ScenarioDefinition`** — mode, learner role, AI role, situation, stakes, success criteria, and difficulty.
- **`EvaluationPack`** — weighted rubric, scoring strategy, and structured feedback template.
- **`RuntimePolicy`** — hallucination policy, citation policy, allowed modes, session limits, and safety restrictions.

The assistant illustrated these as JSON structures. The examples used a Brunswick manager/pay-transparency scenario only as a worked example of the generalized object model.

### 3.5 Assistant expands the runtime pipeline

The assistant argued that the user's initial orchestration sequence was directionally correct but too flat. It proposed six runtime stages:

1. **Session initialization** — load instance, mode, scenario, runtime policy, and learner session state.
2. **Input classification** — determine mode, intent, retrieval need, evaluation timing, and whether the learner is acting in role, asking about the system, or requesting coaching.
3. **Context assembly** — combine hidden instructions, mode instructions, scenario state, learner history, retrieved knowledge, and applicable evaluation rules.
4. **Response generation** — call the model with the assembled packet.
5. **Post-processing** — optionally evaluate the learner response, attach coaching, normalize output, enforce UI-safe formatting, and store a trace.
6. **Presentation** — render roleplay messages, grounded answers, coaching feedback, scorecards, or transcript entries.

The proposed compact pipeline was:

`User Input → Intent / Mode Router → Retrieval + State Resolver → Prompt Composer → Model Call → Evaluation / Policy Checks → Response Formatter → UI Render`

### 3.6 Assistant draws system boundaries

The assistant proposed that Trainstorm should own:

- instance configuration;
- scenario packaging;
- runtime orchestration;
- evaluation logic;
- transcripting;
- learner experience;
- analytics and reporting;
- knowledge ingestion workflow; and
- prompt and rubric versioning.

It proposed treating foundation models, embedding models, vector storage, authentication, cloud storage, and observability infrastructure as externally supplied services.

It also proposed that Trainstorm initially avoid owning foundation-model training, custom embedding research, unnecessary low-level infrastructure abstractions, and complex enterprise IAM beyond standard SSO integration.

### 3.7 Assistant proposes a technical blueprint

For an MVP with room to grow, the assistant proposed:

- **Frontend:** Next.js/React with Tailwind, separating the admin studio from the learner runtime.
- **Backend:** a choice between a TypeScript full stack and a React frontend with Python/FastAPI orchestration.
- **Preferred path:** Next.js frontend plus FastAPI backend, based on the belief that Trainstorm's advantage would lie in evaluation, ingestion, transformation, and structured AI pipelines.
- **Database:** PostgreSQL.
- **Vector storage:** pgvector initially.
- **Object storage:** S3-compatible storage.
- **Authentication:** a service such as Clerk, Auth0, or Supabase Auth.
- **Model access:** a Trainstorm-owned gateway abstraction over providers such as OpenAI, Azure, or Anthropic.

The assistant recommended a **modular monolith with clean boundaries**, rather than early microservices. It proposed modules for admin configuration, knowledge ingestion, runtime orchestration, evaluation, and analytics/traces.

### 3.8 Assistant proposes a product-oriented API and storage model

The assistant argued that the API should expose product concepts rather than raw model concepts. It contrasted endpoints such as `/chat` or `/ask-model` with endpoints organized around instances, sessions, turns, scenarios, prompt packs, knowledge documents, evaluation, transcripts, and traces.

It proposed storing configuration, sessions, transcripts, evaluation results, and version/audit metadata in PostgreSQL; source files, reports, exports, and branding assets in object storage; and chunk embeddings plus metadata and collection relationships in the vector layer.

### 3.9 Assistant proposes compositional prompt architecture

The assistant advised against storing one giant system prompt. It proposed a deterministic, inspectable prompt stack composed from:

1. platform base instructions;
2. client instance instructions;
3. mode instructions;
4. scenario instructions;
5. retrieval context;
6. session state; and
7. the current user turn.

The rationale was governance, diffability, versioning, and reuse.

### 3.10 Assistant sequences the MVP

The assistant proposed this capability order:

1. **Grounded Q&A** — simplest orchestration and quickest proof of hidden instructions plus retrieval.
2. **Rehearsal Mode** — introduces persona and role logic.
3. **Evaluated Simulation** — the strongest differentiation, but requiring more design maturity.

It proposed treating coaching as post-processing layered onto other modes rather than a fully independent architecture at first.

For a demo, the assistant recommended making client configuration, document ingestion, retrieval, prompt assembly, branding, and transcript capture real while simplifying robust authentication, deep analytics, multi-model routing, fine-grained roles, evaluator precision, and enterprise deployment.

It proposed a single “golden vertical slice”: a branded manager conversation using client knowledge and a rubric, ending in structured coaching and a scorecard.

The assistant also proposed milestones:

1. static, JSON-configured prototype;
2. operational ingestion, retrieval, and multi-turn runtime;
3. editable configuration studio; and
4. evaluation, export, and simple analytics.

### 3.11 Assistant identifies the differentiation layer

The assistant argued that Trainstorm should not be positioned as “Azure AI Studio but for training” or as “chatbot plus RAG.” It proposed **training cognition architecture** as the durable differentiation.

The proposed differentiators were:

- scenario-native rather than chat-native design;
- evaluation as a first-class capability;
- a structured learning runtime spanning pre-brief, scenario, reflection, coaching, retry, and evidence;
- per-client configuration without bespoke rebuilds; and
- future learner-state intelligence capable of detecting repeated weaknesses, adapting difficulty, recommending practice, and tracking readiness.

The assistant contrasted Azure as general AI application infrastructure with Trainstorm as an opinionated system for governed learning interactions. It contrasted generic learning platforms, described primarily as content delivery and quiz/reporting systems, with a live cognitive practice system grounded in source truth.

### 3.12 Assistant supplies design pushbacks and a revised five-layer model

The assistant warned against:

- collapsing roleplay, grounding, and evaluation into one prompt;
- treating the chat transcript as the product;
- overtrusting LLM-based evaluation;
- underbuilding knowledge ingestion; and
- allowing implicit or uncontrolled mode switching.

It proposed hybrid evaluation using rubric judgment, rule checks, required-concept detection, prohibited-language detection, and confidence thresholds.

It proposed that knowledge ingestion be treated as a product surface with authoritative-document flags, version control, collection assignment, chunk previews, and retrieval testing.

Finally, it revised the user's four layers into five:

1. **Studio Configuration Layer** — client settings, prompt packs, scenario packs, evaluation packs, knowledge collections, and runtime policies.
2. **Knowledge Processing Layer** — upload, parse, chunk, tag, embed/index, validate, and assign to collections.
3. **Cognitive Orchestration Layer** — session manager, mode router, retrieval manager, prompt composer, model gateway, evaluator, and policy guardrails.
4. **Learning Runtime Layer** — scenario entry, interaction, feedback, scorecards, transcript/export, and analytics hooks.
5. **Evidence and Analytics Layer** — performance traces, rubric outcomes, learner progression, difficulty signals, and administration reporting.

The assistant stated that the fifth layer deserved explicit architectural standing. No visible subsequent user message confirms that revision.

## 4. Explicit User Decisions and Constraints

Only user-authored or clearly user-confirmed items are included here.

### Product intent

- The product is intended to build custom AI-powered training environments.
- Environments must be configurable per client.
- Environments should support demonstrations within learning interventions.
- The system should eventually scale into reusable systems.
- The system is **not just a chatbot**.

### Required runtime capabilities

- Hidden system prompts.
- Grounding knowledge.
- Scenario logic.
- Evaluation capability.
- Model behavior controlled before user interaction.
- Learners must not interact with the raw model directly.

### User's initial architecture

- An admin-only configuration layer controlling prompt, assistant role, tone, behavior, scenario type, evaluation rubric, branding, and knowledge sources.
- A knowledge layer that uploads, chunks, and embeds or indexes source material.
- An orchestration layer that retrieves relevant knowledge, injects system instructions and context, calls the model, optionally evaluates, and returns the result.
- A learner runtime with scenario setup, interaction, feedback, and optional scoring.

### Source knowledge and grounding

- Relevant source types explicitly named: SOPs, training manuals, playbooks, scripts, and policies.
- The purpose of grounding is to ensure responses reflect client reality.

### Build philosophy

- The user wants to understand and build the architecture personally.
- Later production use of Azure or another service remains possible; using such services later does not replace the desire to understand the architecture.

### Non-decisions

- The visible conversation does **not** contain explicit user acceptance of the assistant's recommended stack, object model, five-layer revision, MVP order, or product positioning.
- Lack of objection must not be treated as approval.

## 5. Assistant Proposals

| Assistant proposal | User response status in visible conversation |
|---|---|
| Reframe Trainstorm from a portal around a model to a training operating system using models as components. | No response; unconfirmed. |
| Define Trainstorm as a configuration-driven simulation and coaching runtime for grounded, role-based, evaluable learning interactions. | No response; unconfirmed. |
| Make the training environment, rather than the chat session, the primary product object. | No response; unconfirmed. |
| Adopt first-class objects: `StudioInstance`, `ClientConfig`, `PromptPack`, `KnowledgeCollection`, `KnowledgeDocument`, `ScenarioDefinition`, `EvaluationPack`, and `RuntimePolicy`. | No response; unconfirmed. |
| Expand the runtime into initialization, classification, context assembly, generation, post-processing, and presentation. | No response; unconfirmed. |
| Separate generation, retrieval, and evaluation architecturally. | No response; unconfirmed. |
| Treat foundation models, embeddings, vector storage, authentication, cloud storage, and observability as external/commodity services. | No response; unconfirmed. |
| Start with a modular monolith rather than microservices. | No response; unconfirmed. |
| Prefer Next.js plus FastAPI, PostgreSQL, pgvector, S3-compatible storage, hosted auth, and a model-provider gateway. | No response; unconfirmed. |
| Expose product-domain APIs rather than `/chat` or `/ask-model`. | No response; unconfirmed. |
| Compose prompts from versioned layers instead of storing one large system prompt. | No response; unconfirmed. |
| Build grounded Q&A, then rehearsal, then evaluated simulation; treat coaching initially as post-processing. | No response; unconfirmed. |
| Build one golden vertical slice before a broad studio product. | No response; unconfirmed. |
| Position Trainstorm around “training cognition architecture,” not generic AI tooling or chatbot-plus-RAG. | No response; unconfirmed. |
| Make scenario, role, objective, constraints, rubric, learner state, and outcome logic more primary than chat. | No response; unconfirmed. |
| Use hybrid evaluation rather than relying solely on LLM-as-judge. | No response; unconfirmed. |
| Treat ingestion and retrieval testing as an administrator-facing product surface. | No response; unconfirmed. |
| Add a fifth, explicit Evidence and Analytics Layer to the user's four-layer architecture. | No response; unconfirmed. |

## 6. Concepts and Components

### Product and architectural concepts

- client-configurable training environment;
- structured training runtime;
- governed learning interaction;
- configuration-driven simulation and coaching runtime;
- training operating system;
- scenario-native versus chat-native architecture;
- training cognition architecture;
- golden vertical slice;
- modular monolith;
- product-domain API;
- model gateway/provider abstraction.

### Configuration concepts

- hidden system instructions;
- assistant role;
- tone and behavior rules;
- modes;
- scenario definitions;
- evaluation rubrics;
- client branding;
- deployment profiles;
- runtime policies;
- compliance and retention settings;
- prompt and rubric version metadata.

### Proposed canonical objects

- `StudioInstance`;
- `ClientConfig`;
- `PromptPack`;
- `KnowledgeCollection`;
- `KnowledgeDocument`;
- `ScenarioDefinition`;
- `EvaluationPack`;
- `RuntimePolicy`.

### Knowledge workflow

`Upload → Parse → Chunk → Tag → Embed/Index → Validate → Assign to Collection → Retrieve at Runtime`

Relevant metadata and controls proposed in the conversation include:

- authority status;
- source version;
- audience;
- parser version;
- chunk count;
- embedding model;
- retrieval score threshold;
- top-k retrieval;
- citation policy;
- chunk preview;
- retrieval testing.

### Runtime workflow

`Session Initialization → Input Classification → Context Assembly → Generation → Post-processing → Presentation`

Componentized form:

`User Input → Intent/Mode Router → Retrieval + State Resolver → Prompt Composer → Model Gateway → Evaluation/Policy Checks → Response Formatter → UI`

### Prompt stack

Proposed layers:

1. platform base instructions;
2. client instructions;
3. mode instructions;
4. scenario instructions;
5. retrieved context;
6. session state;
7. current user turn.

### Learning modes

- grounded Q&A;
- rehearsal;
- coaching;
- evaluated simulation.

The assistant proposed explicit mode selection and initially treating coaching as an overlay or post-processing option.

### Evaluation concepts

- weighted criteria;
- rubric-based LLM judgment;
- rule checks;
- required-concept detection;
- prohibited-language detection;
- confidence thresholds;
- structured feedback;
- strengths;
- missed opportunities;
- rewrite suggestions;
- per-turn evaluation;
- final score;
- progress evidence.

### Learner experience concepts

- scenario entry or pre-brief;
- in-role interaction;
- grounded answers;
- coaching feedback;
- reflection;
- retry;
- scorecards;
- transcript and export;
- learner progression;
- future adaptive difficulty and readiness tracking.

### Storage and infrastructure proposals

- PostgreSQL for configuration, sessions, transcripts, evaluation results, and audit metadata;
- pgvector for embeddings and retrieval metadata;
- S3-compatible storage for source files, exports, reports, and brand assets;
- Next.js/React and Tailwind for admin and runtime interfaces;
- FastAPI for orchestration and evaluation;
- third-party authentication and SSO;
- external foundation and embedding models.

### Proposed service/module boundaries

- Admin Config Service;
- Knowledge Ingestion Service;
- Runtime Orchestrator;
- Evaluation Engine;
- Analytics / Trace Service.

## 7. Problems and Design Pressures

### Avoiding a chatbot wrapper

The user's strongest product pressure was to avoid a thin interface over an unconstrained model. Hidden configuration, source grounding, scenario logic, and evaluation were intended to define the interaction before the learner arrived.

### Client specificity without bespoke rebuilding

The product must reflect each client's sources, behavior rules, brand, and evaluation needs while remaining reusable. This creates pressure for configuration packages, stable reusable objects, and a separation between platform behavior and client-specific content.

### Grounding in client reality

Generic model knowledge is insufficient for policies, SOPs, scripts, or playbooks. The architecture must ingest, structure, retrieve, and govern authoritative client sources and provide controlled fallback behavior when grounding is weak.

### Avoiding monolithic prompts

Blending roleplay, grounding, policy, and evaluation in a single prompt may be expedient for demonstrations but makes behavior difficult to inspect, version, validate, or reuse. The assistant's prompt-stack proposal was meant to address this.

### Avoiding transcript-centric product design

A raw conversation log does not express training progression. The assistant proposed designing around scenario entry, attempt, feedback, retry, and improvement evidence.

### Evaluation reliability

LLM evaluation can be inconsistent or overconfident. The proposed pressure is to combine model judgment with explicit rules, concept checks, prohibited-language checks, and confidence thresholds.

### Source and retrieval quality

Training credibility depends on what was ingested and what was retrieved. This motivates authoritative-source flags, versioning, collection assignment, chunk inspection, retrieval tests, and retrieval traces.

### Governed mode behavior

Implicitly allowing the model to choose among practice, Q&A, coaching, and evaluation can reduce product coherence. The assistant proposed explicit modes and routing.

### Traceability and governance

When behavior depends on prompts, sources, scenarios, and rubrics, the system needs versioned and inspectable composition so an output can be traced to the configuration and evidence used.

### Scope and implementation complexity

The architecture spans admin tooling, ingestion, retrieval, interaction, evaluation, analytics, branding, authentication, and deployment. The assistant's modular-monolith and golden-slice proposals were intended to reduce premature complexity.

### Durable IP versus commodity plumbing

The assistant proposed keeping instructional orchestration, scenario packaging, evaluation, and learner evidence within Trainstorm while relying on external providers for models and common infrastructure. This reflects a commercial pressure to invest in training-specific value rather than duplicating commodity services.

## 8. Revisions and Superseded Ideas

### Four layers to five layers

- **Earlier user model:** Configuration, Knowledge, Orchestration, Runtime.
- **Assistant revision:** Studio Configuration, Knowledge Processing, Cognitive Orchestration, Learning Runtime, plus an explicit Evidence and Analytics Layer.
- **Reason for revision:** Performance evidence, rubric results, progression, and reporting were argued to be more than incidental logs.
- **Status:** Proposed, not explicitly accepted by the user in the visible conversation.

### Portal around a model to training operating system

- **Earlier framing:** A client-configurable AI training portal, conceptually comparable to aspects of Azure AI Studio.
- **Assistant revision:** A training operating system in which models are replaceable components.
- **Reason for revision:** To make the training environment and instructional orchestration, rather than the LLM or chat session, the durable product center.
- **Status:** Proposed, not explicitly accepted.

### Flat orchestration to staged orchestration

- **Earlier user flow:** retrieve context, inject prompt, call model, optionally evaluate, return response.
- **Assistant revision:** initialize, classify, assemble context, generate, post-process, and present through explicit routing and policy stages.
- **Status:** Proposed, not explicitly accepted.

### Single system prompt to compositional prompt stack

- **Earlier user wording:** hidden “system prompt” as a configuration item.
- **Assistant revision:** `PromptPack` plus deterministic composition of platform, client, mode, scenario, retrieval, state, and user input.
- **Status:** Proposed, not explicitly accepted.

### Coaching as a mode versus coaching as an overlay

- **Earlier user runtime:** coaching feedback was a visible experience capability.
- **Assistant proposal:** avoid building coaching as a completely independent architecture first; use it as post-processing over other modes.
- **Status:** Proposed and tentative; not confirmed.

### Broad multi-mode product to staged vertical slices

- **Earlier user scope:** scenario rehearsal, guided Q&A, coaching, and evaluated simulations.
- **Assistant revision:** implement grounded Q&A, then rehearsal, then evaluated simulation; prove value with a single golden slice.
- **Status:** Proposed, not confirmed.

### Generic LLM evaluation to hybrid evaluation

- **Initial capability:** optional evaluation logic.
- **Assistant refinement:** rubric-driven LLM judgment plus deterministic checks and confidence thresholds.
- **Status:** Proposed, not confirmed.

No assistant proposal is treated here as superseding an explicit user requirement unless the user visibly confirmed that change; no such confirmation is present.

## 9. Unresolved and Deferred Work

### Product and learning design

- Exact definition and boundaries of each mode.
- Whether coaching remains a distinct mode or becomes an overlay.
- How scenario state transitions are represented.
- How retries, reflection, and progression are modeled.
- How learner identity and learner state persist across sessions.
- What “readiness” means and how it is evidenced.

### Canonical model and governance

- Final object names and schema ownership.
- Stable identifier strategy.
- Relationships among client, instance, scenario, prompt, source, rubric, mode, and deployment versions.
- Publishing, approval, rollback, and deprecation workflows.
- Validation rules for prompt packs, scenarios, rubrics, and knowledge collections.
- Whether UI shell and deployment profile remain first-class objects.

### Knowledge ingestion and retrieval

- Parser and chunking strategy by document type.
- Metadata taxonomy and controlled vocabularies.
- Document precedence when sources conflict.
- Source-update and re-indexing behavior.
- Citation visibility to learners versus administrators.
- Retrieval evaluation, test sets, and acceptance thresholds.
- How non-text content is handled.

### Evaluation

- Evaluator reliability and calibration.
- Separation between formative coaching and summative scoring.
- Rule authoring and concept-detection mechanisms.
- Rubric versioning and comparability across attempts.
- Human review or appeal workflow.
- Bias, fairness, and audit requirements.

### Technical implementation

- Final choice between TypeScript-only and Next.js plus FastAPI.
- Authentication provider and enterprise SSO requirements.
- Model provider strategy and fallback behavior.
- Data-retention defaults and client-specific compliance controls.
- Multi-tenancy and isolation model.
- Observability, cost controls, and failure recovery.
- Deployment topology and environment promotion.

### MVP scope

- Whether grounded Q&A or an evaluated simulation should be the first shipped slice. The assistant recommended grounded Q&A as the first capability while also recommending an evaluated scenario as the most compelling demo package.
- What is “real” versus mocked in the first demonstration.
- Acceptance criteria for the operational prototype.
- Whether an admin UI is required before client demonstration.

### Relationship to `trainstorm-core`

- No repository comparison was performed in this rehydration.
- It remains unresolved which concepts already exist, differ in terminology, have been superseded, or belong outside the repository.

## 10. Referenced Artifacts

Artifacts and systems mentioned in the conversation are listed without claiming access to them.

### Product and repository references

- Trainstorm Studio.
- `trainstorm-core` — named only in the current rehydration request as the repository for later comparison; its contents were not used.

### External platforms and services

- Azure AI Studio — conceptual reference for instruction injection, grounding, and pre-interaction behavior control.
- OpenAI — example model provider.
- Azure — example model/cloud provider and possible future production service.
- Anthropic — example model provider.
- Clerk — example authentication provider.
- Auth0 — example authentication provider.
- Supabase Auth — example authentication provider.
- PostgreSQL.
- pgvector.
- S3-compatible object storage.
- Next.js.
- React.
- Tailwind.
- FastAPI.

### Source-document types

- SOPs.
- Training manuals.
- Playbooks.
- Scripts.
- Policies.
- PDF source documents.

### Worked-example artifacts

- Brunswick Manager Practice Studio — illustrative `StudioInstance`.
- Pay Transparency Materials — illustrative `KnowledgeCollection`.
- Manager Pay Transparency Guide — illustrative `KnowledgeDocument`.
- Employee Questions Pay Positioning — illustrative evaluated scenario.
- Pay transparency guide and FAQ — illustrative source set.
- Evaluation criteria: empathy, policy alignment, clarity, and risk avoidance.

### Proposed configuration artifacts

- client configuration;
- prompt packs;
- scenario packs;
- evaluation packs;
- runtime policies;
- knowledge collections;
- UI shells;
- deployment profiles;
- transcript exports;
- generated reports;
- retrieval traces;
- scorecards.

### Proposed API artifacts

- instance endpoints;
- prompt-pack endpoints;
- scenario endpoints;
- evaluation-pack endpoints;
- knowledge-document and collection endpoints;
- session and turn endpoints;
- transcript endpoints;
- evaluation endpoints;
- analytics and trace endpoints.

No files, diagrams, schemas, prompts, repositories, or external systems mentioned above were inspected as part of this evidence record unless their content was reproduced directly in the visible conversation.

## 11. Provenance Highlights

| Major claim | Source | Supporting excerpt or precise paraphrase |
|---|---|---|
| Trainstorm is not intended to be a chatbot wrapper. | User | “This is NOT just a chatbot.” |
| The product should be configurable per client and reusable. | User | The user wanted to build custom environments, configure them per client, demonstrate them in learning interventions, and eventually scale them into reusable systems. |
| The runtime requires hidden instructions, grounding, scenario logic, and evaluation. | User | The user explicitly listed all four capabilities. |
| Learners should not contact the raw model. | User | “User NEVER interacts with raw model.” |
| Source grounding exists to reflect client reality. | User | The stated purpose of chunking/indexing source documents was to “ensure responses are grounded in client reality.” |
| The user wants architectural understanding even if a managed platform is later used. | User | The user wanted to understand and build the architecture personally, even if Azure or other services were later used in production. |
| The training environment should be the primary object. | Assistant | The assistant proposed that the primary object is not the chat session but the packaged training environment. |
| Trainstorm should be framed as a training operating system. | Assistant | Proposed shift from “portal around a model” to “training operating system that uses models as one component.” |
| Configuration should be decomposed into durable objects. | Assistant | Proposed `StudioInstance`, `ClientConfig`, `PromptPack`, `KnowledgeCollection`, `KnowledgeDocument`, `ScenarioDefinition`, `EvaluationPack`, and `RuntimePolicy`. |
| Prompt composition should be deterministic and inspectable. | Assistant | Proposed a layered stack from platform instructions through client, mode, scenario, retrieval, state, and user turn. |
| Roleplay, grounding, and evaluation should not be collapsed into one prompt. | Assistant | The assistant explicitly identified this as a critical design pushback. |
| Evaluation should combine model judgment with deterministic checks. | Assistant | Proposed “rubric-based judgment,” rule checks, required-concept detection, prohibited-language detection, and confidence thresholds. |
| The product should be built around learning progression rather than transcripts. | Assistant | Proposed scenario entry, guidance, attempt, review, retry, and improvement; stated that the transcript is not the product. |
| Knowledge ingestion should be an admin-facing product surface. | Assistant | Proposed authority flags, version control, collection assignment, chunk previews, and retrieval testing. |
| Evidence and analytics may deserve a separate architectural layer. | Assistant | Proposed a fifth layer for performance traces, rubric outcomes, learner progression, difficulty signals, and reporting. |
| A modular monolith was preferred for the initial implementation. | Assistant | Proposed avoiding premature microservices while maintaining clean module boundaries. |
| Next.js plus FastAPI and pgvector was the assistant's preferred stack. | Assistant | The assistant slightly preferred the Python orchestration path and named Next.js, FastAPI, PostgreSQL, and pgvector. |
| A golden vertical slice should prove the system before broad expansion. | Assistant | Proposed one client, one scenario, one knowledge set, one rubric, and a complete interaction-to-scorecard flow. |
| None of the assistant's significant proposals were visibly approved. | Conversation-level evidence | No later user response accepting, changing, or rejecting them appears in the visible source conversation. |

## 12. Candidate Insights for Repository Comparison

The following claims are deduplicated candidates for later comparison with `trainstorm-core`. They are evidence, not recommendations.

| Claim | Source status | Confidence | Likely architectural area | State | Why it may still matter |
|---|---|---:|---|---|---|
| Trainstorm must be more than a chatbot and must mediate all learner/model interaction. | `explicit_user_decision` | High | Runtime boundary; orchestration | Settled in conversation | Establishes the core product boundary and argues against direct generic chat APIs. |
| Client environments must be configurable and ultimately reusable rather than separately rebuilt. | `explicit_user_decision` | High | Configuration; tenancy; packaging | Settled in conversation | May require canonical configuration packages and separation of platform versus client content. |
| Hidden instructions, grounding knowledge, scenario logic, and evaluation are required capabilities. | `explicit_user_decision` | High | Configuration; retrieval; scenarios; evaluation | Settled in conversation | Provides a minimum capability set against which repository coverage can be checked. |
| The user wants to understand and own the architecture even if managed services are used later. | `user_constraint` | High | Platform abstraction; documentation | Settled in conversation | Supports transparent, inspectable architecture and avoidance of provider-locked product semantics. |
| The training environment, not the chat session, should be the primary domain object. | `assistant_proposal` | High as proposal | Domain model | Tentative | May explain or challenge the repository's aggregate boundaries. |
| A deployable environment may compose client config, prompt pack, knowledge collections, scenario, evaluation pack, runtime policy, UI shell, and deployment profile. | `assistant_proposal` | High as proposal | Domain model; composition | Tentative | Offers an early candidate aggregation model and dependency map. |
| Prompt configuration should be a versioned bundle rather than one system-prompt blob. | `assistant_proposal` | High as proposal | Prompt registry; versioning | Tentative | Supports diffability, governance, reuse, and traceability. |
| Knowledge sources should retain provenance, authority, version, audience, and processing metadata. | `assistant_proposal` | High as proposal | Ingestion; provenance; schema | Tentative | May matter for controlled-source workflows and prevention of content drift. |
| Retrieval collections should carry explicit policies such as thresholds, top-k, and citation requirements. | `assistant_proposal` | High as proposal | Retrieval configuration | Tentative | Makes retrieval behavior governed and reproducible rather than implicit. |
| Scenario definitions should encode learner role, AI role, situation, stakes, success criteria, mode, and difficulty. | `assistant_proposal` | High as proposal | Scenario/content model | Tentative | Provides an early structured representation of instructional intent and simulation state. |
| Evaluation packs should be first-class, versioned structures with weighted criteria and feedback contracts. | `assistant_proposal` | High as proposal | Evaluation schema | Tentative | Evaluation was identified as a potential differentiator and needs stable configuration. |
| Runtime policy should be separate from prompts and scenarios. | `assistant_proposal` | High as proposal | Policy; safety; governance | Tentative | Separates operational constraints from instructional meaning and authored behavior. |
| Runtime orchestration should explicitly separate routing, retrieval/state resolution, prompt composition, generation, evaluation/policy checks, and presentation. | `assistant_proposal` | High as proposal | Orchestration pipeline | Tentative | Helps preserve replaceable components and observable decision points. |
| Generation, retrieval, and evaluation should remain separate concerns even when one model performs several roles. | `assistant_proposal` | High as proposal | Service boundaries; evaluation | Tentative | Reduces coupling and prevents demo prompts from becoming production architecture. |
| Trainstorm should own instructional orchestration and evidence while using external providers for foundation models and commodity infrastructure. | `assistant_proposal` | Medium-high | Platform boundaries; integrations | Tentative | Identifies a possible durable-IP boundary and provider-abstraction requirement. |
| The initial system should be a modular monolith with clean internal modules. | `assistant_proposal` | High as proposal | Repository structure; deployment | Tentative | May be useful when comparing current service decomposition with the original complexity strategy. |
| APIs should expose domain concepts such as instances, sessions, turns, scenarios, knowledge, and evaluations rather than raw model/chat operations. | `assistant_proposal` | High as proposal | API design | Tentative | Reinforces product semantics and discourages provider-shaped interfaces. |
| Prompt assembly should be deterministic, layered, versioned, and inspectable. | `assistant_proposal` | High as proposal | Prompt composition; traces | Tentative | Enables reproduction, audit, debugging, and controlled reuse. |
| Coaching may initially be a feedback overlay rather than an independent architectural mode. | `assistant_proposal` | Medium | Mode model; feedback | Tentative | Could affect whether coaching is represented as a workflow, capability, or separate product type. |
| A golden vertical slice should precede a broad admin studio. | `assistant_proposal` | High as proposal | Delivery roadmap | Tentative | Explains a possible sequencing choice and what minimum end-to-end behavior should exist. |
| Grounded Q&A was proposed as the first capability, but evaluated simulation was proposed as the strongest demo. | `assistant_proposal` | High | Roadmap; demo strategy | Unresolved | The tension between easiest proof and strongest commercial demonstration may still affect prioritization. |
| The learner product should center on progression—entry, attempt, feedback, retry, improvement—not merely transcript storage. | `assistant_proposal` | High as proposal | Learning workflow; learner state | Tentative | May require explicit attempt, feedback, and progression entities rather than only messages. |
| LLM-as-judge should be supplemented with rules, concept checks, prohibited-language detection, and confidence thresholds. | `assistant_proposal` | High as proposal | Evaluation engine; validation | Tentative | Addresses reliability, auditability, and production risk. |
| Knowledge ingestion should expose authority, versioning, chunk preview, collection assignment, and retrieval tests. | `assistant_proposal` | High as proposal | Admin studio; ingestion QA | Tentative | Treats source preparation and retrieval validation as governed production work. |
| Interaction modes should be explicit rather than inferred freely by the model. | `assistant_proposal` | High as proposal | Mode routing; UI; runtime policy | Tentative | May reduce ambiguity and improve reproducibility and safety. |
| Evidence and analytics may be a first-class fifth layer rather than incidental logging. | `assistant_proposal` | High as proposal | Evidence; analytics; reporting | Tentative | Supports performance traces, rubric outcomes, progression, difficulty signals, and reporting. |
| Future learner-state intelligence may support weakness detection, adaptive difficulty, practice recommendations, and readiness tracking. | `assistant_proposal` | Medium-high | Learner model; adaptivity | Unresolved/deferred | Identifies possible future requirements that could influence identifier, event, and evidence design today. |
| The early terminology may correspond to later canonical content/configuration packages, but that relationship cannot be assumed without repository comparison. | `inference` | Medium | Crosswalk; repository reconciliation | Unresolved | Preserves possible lineage while respecting the evidence boundary and later repository authority. |

---

## Closing Evidence Note

This rehydration preserves the distinction between the user's explicit starting architecture and the assistant's extensive proposed refinement. The visible conversation records a strong user commitment to a governed, client-configurable, grounded training runtime, but it does not record explicit user approval of the proposed object model, technology stack, five-layer architecture, sequencing, or positioning. Those items should therefore enter any comparison with `trainstorm-core` as proposals or tentative precursors, not as binding historical decisions.
