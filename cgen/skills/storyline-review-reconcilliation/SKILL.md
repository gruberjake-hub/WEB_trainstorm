---
name: storyline-review-reconciliation
description: >-
  Reconcile course reviewer/SME comments into an Articulate Storyline translation
  export so the edits re-import cleanly. Use this whenever someone has a list of
  e-learning review comments (a spreadsheet, CSV, or Articulate review-portal export)
  AND a Storyline translation file (the Word "Export to Translation" .docx, or an
  XLIFF), and wants the comments applied to that file. Trigger on phrases like
  "incorporate the SME comments into the translation matrix", "apply these review
  comments to the Storyline export", "update the course text from this feedback so I
  can re-import", or when a review-comment list and a Storyline export appear together.
  The skill matches each comment to the right row, edits only what re-imports safely,
  and flags comments that need structural changes the matrix cannot make. Do NOT use
  it to build interaction slides (that is a slide-build task) or for the quiz/question
  xlsx import.
---

# Storyline review reconciliation

Instructional designers collect reviewer/SME comments (often a spreadsheet exported
from the Articulate review portal) and need those changes back into the course. The
established shortcut is to apply them to a **Storyline translation export** and
re-import — much faster than editing every slide by hand. This skill does that
reconciliation *without breaking the re-import*, which is the whole trick: these files
are brittle, and a re-import that silently does nothing (or corrupts the file) wastes a
full round trip.

## The one thing that costs a round trip: pick the right export

Storyline offers two translation exports. They are not equally safe to hand-edit:

- **Word "Export to Translation" (.docx) — PREFERRED.** A table whose columns are
  `ID (locked) | Type | Source Text | Translation`. The Translation column is
  pre-filled with the source text, and re-import reads **Translation**. Edit that
  column and it works.
- **XLIFF (.xlf).** A monolingual export often has only `<source>` and **no populated
  `<target>`**. Storyline re-imports from the target — so editing source and
  re-importing can silently do nothing. If you must use XLIFF, confirm targets exist
  (or that the user's workflow imports from source); otherwise ask for the Word export.

If the user hands you an XLIFF and changes "don't show up on the Storyline side," that
is almost always this. Recommend the Word export and proceed there. Format details and
the XLIFF fallback live in `references/formats.md`.

## Workflow

### 1. Read both inputs
Read the comment list (columns are usually author, comment, slide/scene, resolved) and
the translation export. In the Word file, the grid is the table containing a
"Translation" header. Dump it to see every row:

```bash
python scripts/matrix_tools.py dump FILE.docx --grep "some text" --runs
```

Each on-screen **paragraph is its own row**. The Source Text column repeats the whole
text box (with 1/2/3 markers) on every row of that box; the **Translation** cell holds
the single paragraph — that is your edit target and your matching key.

### 2. Match each comment to its row
The export has **no slide/scene labels**, so match by content, not by the comment's
slide name. Search the Translation column for the phrase the comment references. Use
the `Type` column and neighboring rows (rows are in document order, so a slide's rows
sit together) to disambiguate. Watch for content that repeats across slides (e.g. an
objectives list echoed on a summary slide) — decide, and tell the user, whether the
change applies to one or both.

### 3. Classify every comment — text vs structural
This is the judgment that keeps you from trying the impossible. A translation import can
only change the **text of objects that already exist**. Sort each comment:

- **Text edit — the matrix can do it:** reword, replace a phrase, append a sentence or
  note, remove a paragraph (clear its text). Apply these.
- **Structural — the matrix CANNOT do it, flag for Storyline:** add a new box/shape,
  remove or delete an object, delete a slide or scene, remove/replace a graphic,
  chevron, or image, insert a new slide, re-order. Editing text cannot create or
  destroy objects. Name these in the change log and, where a text string is involved,
  provide the ready-to-paste text so the human can do it in Storyline quickly.

Renaming rows of `Type` "Slide name"/"Scene name" renames the item on import (updates
the course menu/outline) — fine when intended, but call it out. Leave "Project title"
metadata alone unless the user asks, since it can change the published/LMS title.

### 4. Apply the safe edits
The cardinal rule: **change only the character data inside existing runs.** Never add,
remove, or reorder rows; never touch the locked ID column; preserve run formatting so
bold/italic survive import. Edit run-by-run (not whole-cell overwrites) so a bolded
document name or link inside a paragraph keeps its formatting.

Write the edits as JSON and let the script apply + verify them:

```bash
python scripts/matrix_tools.py apply FILE.docx edits.json OUT.docx
```

Edit modes: `replace` (swap a substring in the run that holds it — safest for a phrase
change inside a longer paragraph), `append` (add a sentence/note to the paragraph),
`set` (replace a whole one-run cell), `clear` (empty a paragraph's runs to remove it,
keeping the row). Target by `row` (from `dump`) when you can; `anchor` matches the
Translation cell containing that string. See the script header for the JSON schema.

To append a note as its own line, include a leading `\n` in the append text — that
keeps it one run (a soft line break) rather than needing a new row.

### 5. Verify before hand-off
Re-import fails quietly on structural drift, so confirm none happened:

```bash
python scripts/matrix_tools.py verify ORIGINAL.docx OUT.docx
```

It must report the same **row count**, zero **ID** mismatches, and zero **Source
Text** mismatches — only Translation cells may differ, and the changed count should
equal the number of edits you made. If any of those fail, do not ship the file.

### 6. Deliver the file + a change log
Return the edited export and a concise change log so the ID has a defensible record.
The log is part of the deliverable, not padding. Use this shape:

```
## SME Review Reconciliation — <course>
Source: <file>  →  Updated: <file>

### A. Incorporated into the matrix (text edits)
| # | Slide (from comment) | Row | Change | Confidence |

### B. Must be done in Storyline (structural — matrix can't)
| # | Slide | Ask | Why the matrix can't | Ready-to-paste text |

### C. Flags for review / possible SME push-back
- low-confidence matches, terminology/accuracy concerns, and places where the ID
  should reasonably push back on the reviewer.
```

Flag two kinds of item explicitly: **low-confidence** matches (a phrase that was hard
to locate, or content that repeats), and **content concerns** where applying the
comment verbatim would be inaccurate or invite an auditor/inspector question — state
the concern, apply the user's call, and note it.

## Guardrails

- Do the edits as targeted character-data changes; never re-serialize the whole
  document by rebuilding the table. Small, scoped, verifiable.
- When unsure whether a change is text or structural, treat it as structural and flag
  it — a wrongly-attempted structural edit is worse than a flagged one.
- If the only export available is an XLIFF without targets, say so and ask for the Word
  export rather than shipping edits that won't import.