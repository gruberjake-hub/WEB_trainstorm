Storyline one-off interaction slide

Produce a single interaction as a Storyline-bound .pptx, fast, for hand-off into an existing project. The user drives the call on what the interaction should be; this skill's job is to render that choice well, not to second-guess it.

Operating principle

The user is the planner. They have already decided the treatment (or will tell you in one line). Build what they asked for. If the treatment seems wrong for the content, you may say so in one sentence — then build what they asked anyway unless they change it. Never silently substitute a different interaction type. This is the line that keeps a fast tool from turning into a template that renders the same layout at everything.

Step 1 — Confirm the three inputs (ask only for what's missing)
Interaction type — reveal (click-to-reveal cards), tabs, scenario (situation + choice), or something described. If the user named it, use it. Don't offer a menu.
Content — the script excerpt, card list, or description of what goes on screen.
Brand — client name + hex values if available. If none given, pick a content-appropriate palette (never default blue), use a QA-safe font, and LABEL the output "approximate brand" so real colors can drop in later.

If exactly one is missing and obvious from context, proceed and state the assumption. If the content is missing, ask — you can't build without it.

Step 2 — Build to these non-negotiables

These come from the PPTX-to-Storyline import reality, not preference:

Author at 13.333 × 7.5 in (LAYOUT_WIDE, = 1280×720) so import lands 1:1 at default story size.
One slide per on-screen state: slide 1 = base state; slides 2…N = one per reveal / tab / outcome, each a self-contained panel positioned where its Storyline layer will sit. These get lifted onto layers after import, then the extra slides are deleted.
Derive names from a stable id: layers Layer_{id}, variables {id}_visited (True/False, default False). Predictable names are what make the wiring reliable.
VO → notes field. On-screen text → canvas. Never put narrator lines on the slide.
Gating: if progression should wait until everything's seen, add the _visited variables and condition the Continue button's Normal state on their AND; show Continue in a disabled treatment until then. If not gated, skip all of that.
Storyline strips formatting on import — fonts, fills, wrap. So the styling is a rebuild reference, not final pixels. Anything that must survive (correct-answer logic, feedback) travels as structured text.

Read references/build-conventions.md for the per-type layout, the exact layer-lift recipe, and the pptxgenjs gotchas before writing the generator.

Step 3 — One gate before hand-off

Before presenting the file, apply the single check that matters most: could the learner actually answer or understand this from the content as written? If a reveal, correct answer, or scenario outcome depends on something the narration doesn't teach — flag it, don't fix it silently. Name the gap and let the user decide. This one check has caught more real problems than any styling pass.

Step 4 — Hand off
Validate the deck (scripts/office/validate.py from the pptx skill).
Do a quick visual QA render and look at it fresh — overflow and overlap are the common defects.
Present the .pptx. In one short message, state: the build (slide count, layer + variable wiring in a sentence), any brand assumption, and any Step 3 flags.
Keep it brief. The user is mid-project and wants the artifact, not an essay.
What this skill does NOT do
It doesn't decide which interaction type fits — that's the user's call.
It doesn't build full decks or multi-scene modules.
It doesn't produce the quiz/question xlsx import — that's a separate workflow.
It doesn't restore or invent missing source content — it flags the gap.