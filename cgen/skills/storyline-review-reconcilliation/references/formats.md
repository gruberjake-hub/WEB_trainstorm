# Storyline translation export formats

Read this when you need the structural detail behind the two export types, or when the
input is an XLIFF rather than the preferred Word doc.

## Word "Export to Translation" (.docx) — preferred

Storyline: *Translation → Export* produces a .docx with two tables. The first is
project metadata (filename, author, export date). The **second** is the translation
grid:

| Col | Header        | Meaning |
|-----|---------------|---------|
| 0   | `ID` (locked) | Stable per-string ID inside a content control. Never edit. |
| 1   | `Type`        | Object kind: `Slide name`, `Scene name`, `Text Box 1`, `Rectangle 8`, `Page Title 1`, `Project title`, etc. Useful context for matching. |
| 2   | `Source Text` | The full text of the object, with `1`/`2`/`3` markers prefixing each paragraph. **Repeated on every row of a multi-paragraph object.** |
| 3   | `Translation` | The single paragraph for this row. Pre-filled = source. **This is what re-import reads and what you edit.** |

Key facts that drive correct edits:

- **One row per paragraph.** A text box with three paragraphs occupies three rows.
  Blank lines between paragraphs are their own rows too (Translation = a newline).
- **Match on the Translation column, not Source.** Because Source repeats the whole box
  on every row, searching Source for a phrase matches all the box's rows. Translation
  holds the one paragraph — it's the precise key.
- **Runs carry formatting.** A paragraph can be several runs (e.g. a bold document name
  mid-sentence, or a hyperlink). Edit the specific run; a whole-cell overwrite flattens
  formatting, which Storyline then imports as unstyled text.
- **Re-import matches by the locked ID and expects the table shape intact.** Adding,
  removing, or reordering rows, or changing the ID/Source columns, is what breaks or
  silently no-ops the import.

`Slide name` / `Scene name` rows: editing the Translation renames that slide/scene on
import (and updates the course menu/outline). Do it only when intended and say so.
`Project title`: leave alone unless asked — it can drive the published/LMS title.

## XLIFF (.xlf) — fallback, with a catch

A Storyline XLIFF export is XML: `<trans-unit id="...">` elements, each with a
`<source>` that wraps the visible text in inline tags
(`<bpt>`/`<ept>`/`<ph>`/`<g ctype="x-text">…</g>`).

The catch: a **monolingual** export (source language only) often has **no `<target>`**.
Storyline re-imports from the target, so editing `<source>` and re-importing can do
nothing visible. Before editing an XLIFF, confirm targets exist or that the user's
workflow imports from source. Otherwise ask for the Word export — it is the reliable
path.

If you do edit an XLIFF, the same brittleness rule applies, one level deeper: change
only the character data **inside** an existing `<g ctype="x-text">…</g>` node. Never
add, remove, or reorder any `<bpt>/<ept>/<ph>/<g>` tag, never change a `trans-unit id`,
and preserve the file's BOM and encoding. Operate with scoped string replacements
inside a single `trans-unit` block (ids are unique), then verify the unit count and the
`<bpt>/<ept>/<ph>/<g>` tag counts are unchanged and the file still parses as XML.

## Structural-change taxonomy (neither format can do these)

A translation import only edits text on objects that already exist. These require
Storyline itself — flag them, don't attempt them:

- add a new box, shape, caption, or marker
- delete or remove an object
- insert, delete, duplicate, or reorder a slide or scene
- add, remove, or replace a graphic, icon, image, chevron, or photo
- move an object, change layout, restyle, or re-time anything on the timeline

Where such a comment includes text (e.g. "add a box that says X"), still surface the
exact text in the change log so the human can paste it in quickly.