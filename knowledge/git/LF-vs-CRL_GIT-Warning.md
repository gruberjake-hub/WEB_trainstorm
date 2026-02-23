# LF will be replaced by CRLF warning

## Symptom
Git warns about LF -> CRLF conversion.

## Root Cause
Windows line-ending normalization.

## Fix
git config --global core.autocrlf false

Add root .gitattributes:
* text=auto eol=lf

## Guardrail
Use LF-only repos for Netlify / SCORM / Pandoc projects.

## Context
Trainstorm WEB repo.

## Tags
git, line-endings
