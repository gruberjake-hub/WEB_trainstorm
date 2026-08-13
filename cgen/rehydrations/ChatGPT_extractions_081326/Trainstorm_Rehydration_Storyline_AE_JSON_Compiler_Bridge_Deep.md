# Trainstorm Rehydration: Storyline_AE_JSON_Compiler_Bridge (Deep Version)

## 1. Conversation Identity

**Conversation title:** Storyline_AE_JSON_Compiler_Bridge (placeholder because no visible title was available)

**Visible date:** Not available from the visible conversation.

---

## 2. Relevance Summary

This conversation represents a major architectural transition from an AI-assisted *script generator* toward an AI-assisted *compiler*.

A recurring theme was reducing the friction of the **Development** phase of instructional design while preserving the production quality normally achieved manually inside After Effects and Storyline.

The discussion establishes several important architectural boundaries:

- AE is not the runtime.
- AE is an intermediary presentation compiler.
- JSON becomes the canonical content substrate.
- Schemas become contractual interfaces rather than documentation.
- Validation becomes mandatory between AI generation and rendering.
- Rendering concerns become separated from semantic concerns.

These concepts are broadly applicable to Trainstorm Core regardless of implementation.

---

## 3. Chronological Rehydration

### Motion Language

The conversation began with practical work in After Effects:

- reusable expressions
- motion reuse
- bullet formatting
- text animation
- expression controls

These gradually evolved into discussion of reusable motion primitives.

Important shift:

Instead of thinking about animations as individual AE tricks, they became reusable behaviors.

---

### Spreadsheet-driven rendering

The discussion explored wiring Source Text to spreadsheet content.

Original architecture:

Excel
↓

CSV

↓

AE expressions

↓

Rendered video

This demonstrated that AE could become data-driven.

The user observed that changing spreadsheet content immediately propagated into AE compositions.

This became the conceptual bridge toward compiler thinking.

---

### Scene identity

Originally the IDs were globally unique.

Later discussion concluded that scene-local IDs are preferable.

Instead of

scene004_how_pay_ranges_are_determined_header_01

the preferred identifiers became

Head_01
SubHead_01
Body_01

because the scene itself provides namespace isolation.

This simplified authoring dramatically.

---

### AE as compiler

One of the major pivots occurred when the user realized AE should not be viewed as the runtime.

Instead:

AI
↓

course.json

↓

AE template

↓

Video assets

↓

Runtime

The assistant proposed describing AE as a presentation compiler.

The user explicitly agreed.

This reframed the purpose of the AE templates.

---

### Compiler metaphor

The user described the spreadsheet as a "Jake compiler."

Meaning:

Much of the instructional relationship information existed implicitly inside the author's head.

The assistant proposed making those relationships explicit.

This became one of the central architectural principles.

---

### Explicit ontology

Discussion shifted toward describing every on-screen object.

The user proposed:

Head

SubHead

Paragraph

Impact

Statement

Quote

List

Bullet

ContentHead

ListHead

These were initially viewed primarily as visual categories.

The assistant proposed treating them as semantic ontology.

This distinction later became critical.

---

### Primitive decomposition

The conversation reached an important insight:

"type" was overloaded.

The assistant proposed decomposing rendering into multiple primitive families.

Instead of

primitive

there became

motion_primitive

layout_primitive

text_primitive

interaction_primitive

style_ref

This allows semantic meaning to remain independent of rendering.

---

### Semantic vs rendering

One of the strongest conceptual breakthroughs occurred here.

The conversation separated:

Identity

Meaning

Behavior

Layout

Style

Specifically:

element_id

↓

type

↓

intent

↓

render primitives

↓

brand styling

The user recognized this as the correct abstraction.

---

### CSV failure

Considerable effort was spent debugging AE CSV parsing.

Observed problems:

- null values
- inconsistent parsing
- Excel export issues

Eventually JSON testing succeeded immediately.

The user interpreted this as evidence that the architecture should lean into JSON rather than CSV.

The assistant agreed.

This became an architectural decision rather than merely a bug fix.

---

### Scene JSON

The conversation then produced a complete scene schema.

Each scene contains:

elements

narration

assets

render

The AE expression became

data.elements[targetId].text

This established a stable renderer contract.

---

### Course JSON

The discussion expanded the scene schema into a complete course schema.

course

↓

scenes[]

↓

scene

↓

elements

Interaction scenes were intentionally excluded from AE.

Storyline remains responsible for those.

---

### Scene splitting

Rather than maintaining one large JSON file for AE, the conversation proposed:

course.json

↓

Python splitter

↓

scene JSON

↓

AE

This balances canonical storage with renderer efficiency.

---

### Validation

The assistant proposed validation as a mandatory pipeline stage.

Pipeline:

LLM

↓

course.json

↓

schema validation

↓

scene splitting

↓

AE

↓

runtime

The user immediately recognized the importance of making the system LLM agnostic.

---

## 4. Explicit User Decisions

- AE is an intermediary renderer.
- Preserve senior instructional quality.
- Development automation is highest leverage.
- JSON preferred over CSV.
- Storyline owns interaction scenes.
- Scene-local identifiers preferred.
- Future narration should use ElevenLabs.
- Long-term objective is a substrate-aware intervention engine.

## 5. Assistant Proposals

Accepted:
- Presentation compiler abstraction.
- Ontology/render separation.
- Primitive families.
- Scene schemas.
- Validation.
- Python scene splitter.

## 6. Concepts and Components

- course.json
- scene.schema.json
- course.schema.json
- presentation compiler
- motion primitives
- text primitives
- layout primitives
- interaction primitives
- semantic ontology
- validator
- scene splitter
- AE renderer
- Storyline interaction layer

## 7. Design Pressures

- Reduce development from months to days.
- Preserve production quality.
- Make AI output deterministic.
- Remove tacit knowledge.
- Enable future compiler implementation.

## 8. Revisions

CSV → JSON

Spreadsheet → structured scene object

Implicit relationships → explicit schema

Animation scripts → motion primitives

Renderer → presentation compiler

## 9. Deferred Work

- ElevenLabs pipeline
- Validator implementation
- Full compiler
- Primitive registries
- Runtime replacement of AE

## 10. Referenced Artifacts

- course.json
- scene.schema.json
- course.schema.json
- split_course_json_to_scenes.py
- AE expressions
- Brunswick script

## 11. Provenance Highlights

User:
- Development is the bottleneck.
- AE is a bridge.
- JSON is the right direction.

Assistant:
- Separate ontology from rendering.
- Validate before rendering.
- Use scene-local namespaces.

## 12. Candidate Insights

1. AE functions as a presentation compiler rather than runtime.
2. JSON is the canonical interchange format.
3. Semantic ontology should be isolated from rendering primitives.
4. Validation should gate all LLM outputs.
5. Scene-local IDs simplify rendering contracts.
6. Compiler stages should progressively transform rather than reinterpret content.
