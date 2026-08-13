# Trainstorm Rehydration: Storyline_AE_JSON_Compiler_Bridge

## 1. Conversation Identity
- **Title:** Storyline_AE_JSON_Compiler_Bridge (placeholder; no visible conversation title)
- **Visible date:** Not available.

## 2. Relevance Summary
This conversation captures architectural evolution of an AI-assisted instructional production pipeline. It develops an intermediary compiler architecture centered on After Effects, scene-oriented JSON, schema validation, and deterministic rendering contracts that bridge AI-generated course structures and production-ready outputs.

## 3. Chronological Rehydration
- Refined reusable AE motion grammar and expressions.
- Developed spreadsheet→AE binding.
- Reframed AE as an intermediary presentation compiler rather than runtime.
- Built semantic taxonomy for screen elements (Head, SubHead, List, Impact, etc.).
- Distinguished ontology from rendering primitives.
- Investigated CSV scene feeds, then pivoted to JSON after AE JSON integration proved reliable.
- Designed scene schema and course.json.
- Proposed per-scene JSON outputs for AE.
- Added schema validation concepts.
- Added reusable Python scene splitter.

## 4. Explicit User Decisions and Constraints
- Strategic objective is a substrate-aware intervention engine.
- Immediate goal is reducing development time while preserving senior instructional quality.
- AE is an intermediary renderer, not the destination runtime.
- Storyline remains responsible for interactive scenes.
- JSON preferred over CSV for AE scene feeds.
- Scene-local IDs (Head_01, SubHead_01, etc.) are preferred.

## 5. Assistant Proposals
- Presentation compiler abstraction (accepted).
- Scene-local namespaces (accepted).
- Separate semantic type from rendering primitives (accepted).
- course.schema + scene.schema (accepted).
- Validation before splitting (accepted).
- Python scene splitter (accepted).

## 6. Concepts and Components
- course.json
- scene.schema.json
- course.schema.json
- scene JSON feeds
- motion_primitive
- text_primitive
- layout_primitive
- interaction_primitive
- style_ref
- semantic type
- AE presentation compiler
- Storyline interaction layer
- JSON validator
- scene splitter

## 7. Problems and Design Pressures
- Development bottleneck.
- CSV instability in AE.
- Need LLM-agnostic contracts.
- Preserve instructional orchestration quality.
- Make tacit design decisions explicit.

## 8. Revisions and Superseded Ideas
- Single CSV → scene CSV → scene JSON.
- Global IDs → scene-local IDs.
- CSV lookup → JSON lookup.
- AE runtime concept → AE presentation compiler.

## 9. Unresolved and Deferred Work
- Complete schemas.
- Validator implementation.
- ElevenLabs integration.
- Full compiler pipeline.
- Primitive selection rules.
- Runtime replacing AE.

## 10. Referenced Artifacts
- Brunswick Pay Transparency Employee script.
- course.json
- scene.schema.json
- course.schema.json
- split_course_json_to_scenes.py
- AE motion library.

## 11. Provenance Highlights
- User: AE is a bridge to a larger intervention engine.
- User: Preserve instructional craft while automating production.
- Assistant: Separate ontology from rendering primitives.
- Assistant: Validate then split into scene JSON.

## 12. Candidate Insights for Repository Comparison

| Claim | Status | Confidence | Area | State | Why |
|---|---|---|---|---|---|
| AE is a presentation compiler | explicit_user_decision | High | Rendering | Settled | Defines architectural boundary |
| JSON scene feeds replace CSV | explicit_user_decision | High | Data | Settled | Improves robustness |
| Scene-local IDs | explicit_user_decision | High | Ontology | Settled | Simplifies lookup |
| Separate semantic type from primitives | assistant_proposal | High | Schema | Accepted | Future extensibility |
| Validate before split | assistant_proposal | High | Governance | Accepted | LLM agnostic pipeline |
