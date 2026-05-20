REHYDRATION PROMPT

We are rebuilding a Trainstorm course generator system that moves from script → structured course data → rendered course assets.

This system is intended to eventually support AI-assisted or AI-driven generation of full learning experiences, including:

1. structured course JSON
2. HTML/CSS/JS runtime rendering
3. AE-generated didactic motion assets
4. optional AI-generated voiceover
5. future brand/theme abstraction per client

The core idea is that the system must separate:

- ontology / semantic meaning
- schema / structural validity
- primitives / render behavior
- theme / brand presentation
- runtime / output rendering

==================================================
PART 1 — COURSE ONTOLOGY
==================================================

We developed a semantic ontology for the on-screen visual elements of a course. These are not merely “screen objects” but cognitively meaningful renderable units.

Important distinction:

- Ontology = what an element IS / what role it plays
- Primitive = how it behaves / animates / renders

Core ontology elements currently include:

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

Current conceptual distinctions:

- List = container
- Bullet = atomic item
- Statement = shorter, more pointed than Paragraph
- Paragraph = fuller explanatory content
- Impact = emotionally weighted / visceral / meaning-heavy
- Quote = contextualizing element
- Content = container/family beneath Scene, often wrapping informational elements

Important insight:
Some entities are:
- renderable nodes
- containers
- or both

We discussed improving the taxonomy by adding concepts like:

- Structural Parent
- Semantic Role
- Cardinality
- Intent

Examples of intent:
- Head → orient
- SubHead → refine
- List → structure
- Bullet → specify
- Statement → assert
- Paragraph → explain
- Impact → persuade
- Quote → contextualize

==================================================
PART 2 — JSON SCHEMA
==================================================

We translated the ontology into a draft JSON structure and then into a real JSON Schema.

The intended architecture is:

Script
↓
AI prompt converts script into structured course JSON
↓
course JSON validates against schema
↓
runtime renders it
↓
AE / motion / voice / interactivity plug in

Important file-structure conclusion:
The schema should live in the repo but outside the runtime, e.g.:

/cgen/schema/course.schema.json

Critical distinction:
- Schema defines allowable structure
- JSON instantiates course data
- Runtime renders valid instances

We also discussed future supporting files like:
- primitive-map.json
- style-map.json

==================================================
PART 3 — BRAND / THEME ABSTRACTION
==================================================

We determined that course JSON should not hardcode final styling values long-term.

Instead, the system should use style references or semantic tokens, such as:

- head-primary
- subhead-secondary
- content-body
- impact-emphasis
- quote-context

Then brand/theme files resolve those to actual client values.

Pattern:

Schema defines allowed style refs
Course JSON uses style refs
Brand/theme layer maps refs to actual CSS/tokens

This allows the same semantic course to render differently for Brunswick, Astellas, AbbVie, etc.

==================================================
PART 4 — AE MOTION SYSTEM
==================================================

We also developed an AE motion runtime approach that is part of the larger Trainstorm vision.

Core architecture:

- Global control comp: __GLOBAL_CONTROLS_EXECUTIVE__
- Global control layer: __GLOBAL_CONTROLS__
- Template comp: __TEMPLATE_TEXT_LAYERS__

Global controls include tokens such as:
- In (sec)
- Out (sec)
- In Delay (sec)
- Out Delay (sec)
- Focus Blur (px)
- Slide X (px)
- Slide Y (px)
- Expo Ease
- Drift (px) [used experimentally]

The AE system is meant to behave like a deterministic motion runtime:
- Animator = WHAT changes
- Selector = WHO changes
- Marker = WHEN it changes
- Global controls = HOW it feels

The intended usage model:
- keep reusable motion layers in a template comp
- copy/paste them into working comps
- edit text only
- drive timing via layer in-point or comp markers depending on use case

We built / discussed:
- Glass fade reveal
- marker-aware vs inPoint-driven animation
- line-by-line bullet reveal
- text formatting expressions
- blur / opacity / scale expressions
- paragraph text wrapping
- text sourced from CSV

Important insight:
AE is functioning as a structured rendering engine, not just animation software.

==================================================
PART 5 — CSV / TEXT-DRIVEN AE CONTENT
==================================================

We operationalized a CSV → AE text pipeline.

Pattern:

Excel
↓
CSV
↓
AE Source Text expression lookup
↓
rendered typography

Typical expression pattern used:
- load course_content.csv via footage()
- lookup by element ID
- select language column based on LANGUAGE_CTRL slider
- replace \n with \r for AE line breaks

Important insight:
The system works best when “missing data” is treated separately from “placeholder data.”

Best practice:
- do not leave reusable placeholders truly missing in CSV
- instead use explicit placeholder values such as:
  [Subhead goes here]
  [Body copy goes here]

We also created Source Text expressions that transform raw text into:
- bullet lists
- numbered lists

These use:
- \r for AE line breaks
- \r\r for blank lines if needed
- \u2003 em space for stable spacing

We also discussed paragraph formatting:
- hanging indents
- left margin / first line indent
- paragraph text vs point text

==================================================
PART 6 — PRIMITIVES VS ONTOLOGY
==================================================

Important distinction established:

Ontology:
- Head
- Paragraph
- Impact
- Bullet
etc.

Primitives:
- GlassReveal
- LineReveal
- BulletReveal
- FocusShift
- QuoteFade
etc.

Example:
{
  "type": "Impact",
  "text": "...",
  "animation": "FocusReveal"
}

Thus:
- ontology answers “what is this?”
- primitive answers “how does it appear/behave?”

This distinction should remain stable in the architecture.

==================================================
PART 7 — COURSE GENERATOR GOAL
==================================================

The broader goal is to build a course generator that can eventually automate the development step of a course.

The system should eventually be able to take:
- SME notes
- scripts
- source docs
- objectives
- brand configuration
- possibly voice instructions

and produce:
- structured course JSON
- renderable scenes
- motion assignments
- UI layout
- voiceover text
- eventual HTML runtime output
- AE assets where needed

This is effectively a compiler architecture for learning design.

==================================================
PART 8 — VOICEOVER / ELEVENLABS DIRECTION
==================================================

A new important development:
I now have access to ElevenLabs voice cloning and want to incorporate voice generation into the course generator.

Future direction:
- script or scene JSON should be able to produce voiceover text segments
- voiceover generation may be triggered through API call from the master build script
- eventually the course generator should unify:
  script
  structure
  motion
  styling
  narration

Potential future architecture:
Script
↓
AI structures into course JSON
↓
course JSON contains narration fields
↓
master build script sends narration to ElevenLabs API
↓
audio assets are generated and linked back into course output

Need help designing this architecture, especially:
- how narration should live in schema / scene objects
- whether narration is per scene, per element, or per segment
- how voice generation should be integrated into the build pipeline
- what output artifacts should be generated

==================================================
TASK FOR THIS NEW INFERENCE
==================================================

Help me rebuild the Trainstorm course generator by integrating:
1. ontology
2. JSON schema
3. runtime structure
4. brand/style abstraction
5. AE motion primitives
6. CSV/content pipeline
7. voiceover generation planning via ElevenLabs API

I want this new inference to help me gather stray pieces into a coherent build architecture.

Start by:
- restating the architecture in a clean systems diagram
- identifying the missing layers / unresolved decisions
- proposing the next best implementation path
- helping me unify the AE, schema, runtime, and voiceover systems into one build pipeline