REHYDRATION PROMPT

We are designing a Trainstorm course generator that can eventually automate the development step of a learning experience.

This system should move from source material to structured course output using a compiler-like approach.

==================================================
CORE ARCHITECTURE
==================================================

The intended layers are:

1. ontology / semantic layer
2. JSON schema / structural contract
3. course JSON instance
4. primitive mapping / behavior layer
5. style mapping / brand layer
6. runtime rendering layer
7. optional AE rendering layer
8. optional voice generation layer

Key separation:
- Ontology = what an element IS
- Primitive = how it behaves/renders
- Style/theme = how it looks for a client/brand
- Runtime = how it is output/rendered

==================================================
ONTOLOGY
==================================================

Core elements include:
- Module
- Scene
- Head
- SubHead
- Content
- ContentHead
- ListHead
- List
- Bullet
- Statement
- Paragraph
- Impact
- Quote

Important distinctions:
- List = container
- Bullet = atomic item
- Content = container/family
- Impact = meaning-heavy / emotionally weighted
- Statement vs Paragraph differ in length, density, and rhetorical role

We also discussed adding concepts like:
- Structural Parent
- Semantic Role
- Cardinality
- Intent

Examples:
- Head → orient
- SubHead → refine
- List → structure
- Bullet → specify
- Statement → assert
- Paragraph → explain
- Impact → persuade
- Quote → contextualize

==================================================
JSON SCHEMA
==================================================

We created a real JSON Schema to validate course files.

The architecture is:

Script
↓
AI converts into course JSON
↓
Schema validates
↓
Runtime renders

The schema lives outside the runtime, e.g.:
/cgen/schema/course.schema.json

We also discussed future files like:
- primitive-map.json
- style-map.json

==================================================
STYLE / BRAND ABSTRACTION
==================================================

Important conclusion:
The schema should not hardcode final CSS values long-term.

Instead:
- course JSON should use style references or semantic style tokens
- client/brand files should resolve those tokens to actual CSS/tokens

Pattern:
Schema validates allowable style refs
Course JSON uses them
Brand/theme maps them to actual values

This allows client-specific rendering without rewriting content.

==================================================
PRIMITIVES
==================================================

Ontology and primitives are related but distinct.

Examples of primitives:
- LineReveal
- GlassReveal
- BulletReveal
- FocusReveal
- QuoteFade

Example:
{
  "type": "Impact",
  "text": "...",
  "animation": "FocusReveal"
}

Thus:
- type = ontology
- animation = primitive

Need help building a clean mapping layer between these.

==================================================
VOICEOVER / ELEVENLABS
==================================================

A major new development:
I now want to incorporate ElevenLabs voice cloning into the generator.

The long-term idea is that the master build script should eventually be able to:
- read narration text from course structure
- call ElevenLabs via API
- generate audio assets
- connect those assets back into the course build

Need help thinking through:
- how narration should live in course JSON
- whether narration belongs at scene level, element level, or segment level
- what output artifacts should be generated
- how the ElevenLabs API call should fit into the build pipeline
- how to keep this modular so audio can be optional

==================================================
OVERALL GOAL
==================================================

The system should eventually be able to take:
- source docs
- SME notes
- scripts
- learning objectives
- brand/theme config
- voice config

and produce:
- validated course JSON
- runtime-renderable scenes
- motion assignments
- style mappings
- optional AE render instructions
- optional ElevenLabs voiceover assets

==================================================
TASK FOR THIS NEW INFERENCE
==================================================

Help me unify the ontology, schema, primitive mapping, style abstraction, and voiceover generation into one coherent course-generator architecture.

Please:
- restate the full pipeline
- identify unresolved architectural decisions
- propose where narration should live in the data model
- suggest how ElevenLabs API calls should integrate into the build system
- help me think through the generator as a true compiler for learning experiences