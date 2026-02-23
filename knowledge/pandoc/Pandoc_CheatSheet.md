pandoc --version

## Basic conversions
pandoc input.md -o output.docx


pandoc input.docx -t markdown -o output.md

pandoc input.docx -t gfm+yaml_metadata_block -o output.md 
    //use before feeding Trainstorm to JSON parser

pandoc input.md -o output.pdf

With margins:
pandoc input.md -o output.pdf --pdf-engine=xelatex -V geometry:margin=1in

pandoc input.md -t pptx -o slides.pptx

### with corporate template
pandoc input.md -o output.docx --reference-doc=template.docx

## HTML conversions

Basic Html
pandoc input.md -o output.html --standalone


Style Html
pandoc input.md -o output.html --standalone --css=styles.css
    (use for Netlify preview)

Html with TOC
pandoc input.md -o output.html --standalone --toc --toc-depth=3

Reveal.js Slides
pandoc input.docx \
  -t revealjs \
  -s \
  -o slides.html \
  -V revealjs-url=https://unpkg.com/reveal.js \
  -V theme=white \
  --slide-level=2

### Interactive Course Skeleton
pandoc lesson.md \
  -o lesson.html \
  --standalone \
  --template=course-template.html

        Template can include:

        Sidebar nav

        Progress tracker

        SCORM JS hooks

        👉 Bridge to your native HTML runtime.

## Batch Conversion
for f in *.docx; do pandoc "$f" -t markdown -o "${f%.docx}.md"; done

for f in *.md; do pandoc "$f" -o "${f%.md}.html"; done

## Add Metadata
pandoc lesson.md \
  -o lesson.html \
  -M title="ALSAP Training" \
  -M author="Trainstorm.ai"

## Use Custom CSS Theme
pandoc lesson.md \
  -o lesson.html \
  --css=theme.css \
  --standalone

## Markdown → SCORM Skeleton
pandoc lesson.md \
  -o lesson.html \
  --template=scorm-template.html \
  --standalone


Then package with:

imsmanifest.xml
scormdriver.js
lesson.html


👉 Long-term Storyline replacement.

## 10. PowerShell vs Bash Reminder

Bash line continuation:

pandoc input.md \
  --css=styles.css \
  --standalone


PowerShell:

pandoc input.md `
  --css=styles.css `
  --standalone

##  11. Trainstorm Pipeline Pattern
SME.docx
   ↓ pandoc
normalized.md
   ↓ GPT
course.json
   ↓ runtime
lesson.html


Pandoc = deterministic normalization → less context drift.

Exactly like your sister’s nursing exam chunking idea.