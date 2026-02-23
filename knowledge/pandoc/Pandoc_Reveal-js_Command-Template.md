# Pandoc reveal.js template

## Symptom
Need HTML slides with navigation.

## Fix
pandoc MythEngine.docx -t revealjs -s -o slides.html \
  -V revealjs-url=https://unpkg.com/reveal.js \
  -V theme=white \
  --slide-level=2

## Guardrail
Store in scripts/build_slides.sh

## Context
AI Learning Architect presentations.

## Tags
pandoc, revealjs
