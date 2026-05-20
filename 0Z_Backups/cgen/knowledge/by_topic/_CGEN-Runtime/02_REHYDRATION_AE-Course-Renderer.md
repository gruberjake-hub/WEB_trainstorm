REHYDRATION PROMPT

We are resuming work on an AE-based motion/content rendering system that is part of a broader Trainstorm course generator.

The purpose of this AE system is not just animation. It is a deterministic motion runtime for instructional content.

Core mindset:
- Animator = WHAT changes
- Selector = WHO changes
- Marker = WHEN it changes
- Global Controls = HOW it feels

==================================================
AE MOTION SYSTEM
==================================================

Global control comp:
__GLOBAL_CONTROLS_EXECUTIVE__

Global control layer:
__GLOBAL_CONTROLS__

Template comp:
__TEMPLATE_TEXT_LAYERS__

Global sliders include things like:
- In (sec)
- Out (sec)
- In Delay (sec)
- Out Delay (sec)
- Focus Blur (px)
- Slide X (px)
- Slide Y (px)
- Expo Ease
- Drift (px)

Usage model:
- keep reusable motion modules in template comp
- copy/paste motion layers into project comps
- edit only the text/content
- drive timing with comp markers or layer in-point depending on primitive
- avoid keyframes wherever possible

==================================================
MOTION PRIMITIVES DISCUSSED
==================================================

We worked on / discussed:
- Glass fade reveal
- Blur + opacity + scale reveal
- marker-aware vs inPoint-driven animation
- line-by-line list reveals
- executive/documentary motion tone
- typography-preserving animations
- possible future primitives like range reveal, bullet stagger, etc.

Key principle:
Typography Integrity — avoid splitting text into unnecessary layers.

==================================================
TEXT / DATA PIPELINE
==================================================

We also developed / refined a CSV-driven AE content system:

Excel
↓
CSV
↓
AE Source Text expression
↓
Rendered text in AE

Typical Source Text expression logic:
- use footage("course_content.csv")
- find row by element ID
- choose language column by LANGUAGE_CTRL slider
- replace \\n with \\r for AE line breaks

Important insight:
Placeholder data should be explicit, not truly missing, to avoid unstable expression behavior.

We also developed Source Text formatting expressions for:
- bullet lists
- numbered lists

These use:
- \\r for line breaks
- \\r\\r for blank lines if needed
- \\u2003 for em space spacing

We also solved:
- paragraph text vs point text
- hanging indents
- left margin / first line indent
- wrapped lines under bullets/numbers

==================================================
BIGGER GOAL
==================================================

This AE system is not isolated. It is intended to become part of a larger course generator, where AI can generate structured course content that AE can render as didactic assets.

Thus AE should be thought of as:
- a structured renderer
- a motion primitive engine
- a component of the broader Trainstorm compiler architecture

==================================================
TASK FOR THIS NEW INFERENCE
==================================================

Help me continue refining the AE system as a reusable rendering layer for generated course content.

Please help with:
- identifying reusable AE primitives
- refining the CSV/content pipeline
- improving expression architecture
- thinking about how generated JSON could eventually feed AE scenes
- designing a stable file structure for AE expressions, primitives, templates, and content data
- helping me make AE function like a deterministic instructional rendering engine