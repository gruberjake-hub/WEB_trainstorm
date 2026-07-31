Build conventions — per-type layout, layer-lift recipe, generator notes

Read this before writing the pptxgenjs generator. It carries the details SKILL.md summarizes.

Canvas & palette setup
js
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";          // 13.333 × 7.5 in = 1280 × 720, imports 1:1

Palette roles (assign per brand; these are the roles, not fixed values):

dominant — 60–70% of visual weight (usually the background on dark builds)
primary — interactive/motif color (chips, buttons)
accent — reveal pills, highlights
surface_light / surface_dark — card backgrounds
text_on_light / text_on_dark, muted_* — type

Fonts: use QA-safe faces (Arial, Calibri) for body so LibreOffice QA renders true to width. If the client font is outside that set, use it but leave ~10% slack and don't trust the QA preview's text-fit on those boxes.

The layer-lift recipe (applies to every type)
Build slide 1 as the base state — everything visible before the learner acts.
Build slides 2…N as one self-contained panel each, positioned exactly where its layer should sit on slide 1.
After importing into Storyline: on slide 1, add a layer Layer_{id} per extra slide and copy that slide's panel group onto it.
Wire per element: variable {id}_visited (True/False, default False), set True on the layer's show (or via a Visited state on the trigger object).
Gated Continue: button Normal state shown only when AND(all {id}_visited); disabled visual treatment otherwise.
Delete slides 2…N. They existed only to carry layer content through import.

Put the narrator VO in slide 1's notes field. Put a one-line "layer content for {id}" marker in each reveal slide's notes so the build step is self-documenting.

Type: reveal (click-to-reveal cards)

Slide 1: prompt text (on-screen) + a grid of card fronts. Each card = number chip (primary-filled circle, the repeating motif) + front text + a "Select to reveal" affordance. Gated Continue bottom-right in disabled treatment.

Grid geometry: 2×2 for 4 cards, 3-up row for 3, single column for 2. Cards size to their content — don't force content into a fixed card.

Slide per card: a panel restating the front, the reveal labels as pills (accent fill), and the reveal body below. Position it centered/overlaying where the layer will sit.

Variables: {cardId}_visited per card. Continue condition = AND of all.

Type: tabs (persistent tabbed content)

Same skeleton as reveal, one behavioral difference: the tab row stays visible and the active tab carries a Selected state; body content swaps in place (not a modal).

Slide 1: a row of tab buttons + the first tab's body shown by default. Slide per tab: that tab's body panel, positioned for Layer_{tabId}. Each tab button gets Normal / Selected states; showing a layer sets its button Selected and clears the others. Gating optional; if on, same _visited + Continue pattern.

Use for 3–5 peer categories the learner browses. Not for sequential steps (that's a stepper/process treatment).

Type: scenario (situation + choice)

Two modes:

single_best — one situation, one best answer, feedback per choice. If it's graded and untimed, it is a Pick One question — prefer routing it through the xlsx question-import path (Question Type MC, * on the correct choice, | before feedback) instead of a bespoke slide. Build a freeform slide only for custom layout or an ungraded reflection.

branching — choices lead to different outcomes.

Slide 1: the setup/stem + choice buttons.
Slide per outcome: outcome panel for Layer_{outcomeId} (or a separate jump-to slide if the branch is long).
Click triggers: show-layer or jumpTo per choice; honor any return-to-stem loop.
pptxgenjs gotchas that bite on these builds
Set pres.layout before adding slides, or coordinates past 10" silently fall off the slide.
Hex colors: no #, no 8-digit alpha — "026AFE", not "#026AFE". The wrong form corrupts the file. For translucency use transparency: 0–100 on fills.
Don't share one options/shadow object across two addText/addShape calls — pptxgenjs mutates it in place. Build a fresh object each time.
Shadow offset must be ≥ 0. For an upward shadow use angle: 270 with a positive offset.
rectRadius works only on roundRect, not rect.
Text boxes have built-in padding — set margin: 0 when text must align to a shape edge at the same x.
Speaker notes go in slide.addNotes("..."), once per slide, never as a text box.
QA before hand-off
bash
# validate (uses the pptx skill's validator)
python /mnt/skills/public/pptx/scripts/office/validate.py OUT.pptx

# visual render
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf OUT.pptx
rm -f slide-*.jpg && pdftoppm -jpeg -r 110 OUT.pdf slide

Look at the rendered images fresh. Most common defects: text overflow at a box edge, overlapping elements, panels with dead space at the bottom (tighten panel height). Fix in the generator and re-render.