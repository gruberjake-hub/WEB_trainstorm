# Rehydration: Storyline Translation Matrix Transformation
_Trainstorm CGEN Pipeline — Architectural Rehydration Document_
_Version 1.0 — June 2026_

---

## Purpose

This document rehydrates the key discovery, technical method, and
formalized pipeline that emerged from a single inference session in
which a Storyline translation matrix was used — for the first time in
this pipeline — as a programmatic edit target rather than a localization
tool.

Load this document at the start of any inference that involves:
- Applying reviewer comments to a Storyline course
- Generating or consuming a Storyline Review Manifest
- Running or extending `sl_apply.py` or `sl_index.py`
- Designing prompt profiles for the manifest generation pipeline

---

## The Core Discovery

Articulate Storyline's translation matrix export (DOCX format) is
structurally a **diff file**. It contains every text element in the
course, each with a stable element ID, a Source Text column, and a
Translation column. On import, Storyline replaces each element's content
with whatever is in its Translation column.

**The insight:** if you populate the Translation column with revised
wording — while leaving everything else identical to Source Text — a
single import pass applies all edits to the course simultaneously.

This transforms what was a localization utility into a **bulk content
edit mechanism**. A reviewer comment reconciliation that would normally
require manual edits to dozens of slides in Storyline becomes a single
import operation.

This was validated in production: 28 targeted text changes across 10
slides of a live Astellas course (ALSAP_vCUR_.story) were applied in
one import pass with no errors.

---

## The Matrix Structure

The translation matrix DOCX contains one large table with four columns:

| Column | Content |
|--------|---------|
| 0 — ID 🔒 | Storyline element ID (stable within an export cycle) |
| 1 — Type | Element type label (TEXT, Slide Notes, BUT, Trigger, Table cell, etc.) |
| 2 — Source Text | Current text content of the element |
| 3 — Translation | Target text — initially identical to Source Text |

**Multi-segment elements** span multiple rows, all sharing the same
element ID. Column 1 (Type) and Column 2 (Source Text) are blank on
continuation rows; only Column 3 (Translation) carries the segment text.

**Run structure** within a Translation cell mirrors the Source Text
formatting. A cell may contain multiple runs with different formatting
(bold, italic, normal). The executor targets individual runs by index,
preserving formatting on runs it does not touch.

---

## ID Stability

Storyline element IDs are stable within a single export/import cycle
on the same story file. They may regenerate on certain operations
(cross-file copy/paste, scene duplication, some imports).

**The operational contract:** treat IDs as ephemeral across cycles but
reliable within one. The correct workflow is:

```
Export fresh matrix from Storyline
       ↓
Build element index from that matrix (sl_index.py)
       ↓
Generate manifest against that index
       ↓
Apply manifest to that matrix (sl_apply.py)
       ↓
Import revised matrix into the same story file
```

Never reuse a manifest from a previous cycle against a new matrix export
without verifying that the element IDs still match.

---

## The Addressing Model

Each change targets a specific location in the matrix using a three-part
tuple:

```
( id , segment_index , run_index )
```

**`id`** — the element ID from Column 0. Resolved at runtime from the
live matrix; never hardcoded as a row number.

**`segment_index`** — which row within the ID's row group to target.
Count rows sharing the same ID from top to bottom, starting at 0.
Single-row elements are always `segment_index: 0`.

**`run_index`** — which run within the Translation cell paragraph to
modify. Most cells have a single run (`run_index: 0`). Cells with mixed
formatting (e.g. bold label + normal description) have multiple runs.

### Run index patterns

| Pattern | run_index | Use case |
|---------|-----------|----------|
| Single run, any formatting | 0 | Narrative paragraphs, table cells, button labels, slide notes |
| Bold label + normal description | 1 | `"SMT (Safety Management Team): "` + description |
| Bold phrase within sentence | varies | Target the specific bold run; leave surrounding runs |
| Full paragraph rewrite (multi-run) | 0 = new text; 1,2,3… = `""` | Collapse multi-run paragraph into single run |

---

## The Change Manifest

The manifest is the handoff artifact between the reconciliation step
(LLM) and the execution step (Python). It is both the SME-reviewable
change record and the machine-executable instruction set.

Schema reference: `MANIFEST_SCHEMA.md`

Key design principles:
- Every reviewer comment appears in the manifest, regardless of whether
  it produces a text change. Non-text issues (DEV_FIX, DEFERRED, etc.)
  are recorded for the audit log.
- `disposition: "REVISE"` is the only value the executor acts on.
- `review_flag: true` marks entries where human post-hoc review is
  warranted — replacement text was generated from inference rather than
  direct canon quotation, or safety-critical terminology was changed.
- `canon_basis` is a required traceability field. It must cite a
  specific section, principle, or constraint from the canon. Vague
  rationale is not acceptable.

### Disposition values

| Value | Executor | Meaning |
|-------|----------|---------|
| `REVISE` | Applied | Canon-grounded; execute |
| `VERIFY` | Skipped | Needs SME or regulatory confirmation |
| `DEV_FIX` | Skipped | Storyline dev task; not a text change |
| `DEFERRED` | Skipped | Out of scope for this cycle |
| `CONSIDER` | Skipped | SME input needed before a position can be taken |

---

## The Toolchain

### `sl_index.py` _(planned)_
Reads a matrix DOCX and produces a structured element index JSON.
Input to MANIFEST_RECONCILER and MANIFEST_GENERATOR profiles.

```bash
python sl_index.py --matrix matrix.docx --output element_index.json
```

### `sl_apply.py`
Reads a manifest JSON and a matrix DOCX. Applies all REVISE entries.
Produces a revised matrix DOCX and an audit log JSON.

```bash
# Dry run — validate without writing
python sl_apply.py --matrix matrix.docx --manifest changes.json --dry-run

# Live run
python sl_apply.py --matrix matrix.docx --manifest changes.json \
                   --output matrix_revised.docx --audit audit.json
```

Key behaviors:
- Builds ID→row lookup at runtime (not hardcoded row indices)
- Skips non-REVISE entries and records them in the audit log
- Reports MISSING entries (ID in manifest not found in matrix) without
  crashing — continues processing and exits with non-zero status
- `--dry-run` prints OLD/NEW text for every entry without touching files

---

## The Prompt Profiles

Three profiles generate manifests. All produce the same schema.
Choice depends on model capability and pipeline wiring.

### MANIFEST_NORMALIZER (Step A)
Reads raw reviewer CSV + matrix. Produces normalized comment objects.
No adjudication. No element IDs generated. Fast and cheap.
Reliable on mid-tier models.

### MANIFEST_RECONCILER (Step B)
Reads normalized comments + canon JSON + element index.
Produces the manifest. All intelligence lives here.
Requires clean structured input from Step A.

### MANIFEST_GENERATOR (single pass)
Collapses normalization and reconciliation into one generation call.
Six explicit chain-of-thought stages before JSON emission.
Designed for frontier models (Claude Sonnet / Opus class).
Produces identical manifest schema to the two-step path.

---

## The Full Pipeline

```
Storyline story file
       ↓  [export translation matrix]
matrix.docx
       ↓  [sl_index.py]
element_index.json
       ↓
reviewer_comments.csv  ──┐
canon_documents.json   ──┤──  MANIFEST_GENERATOR  (or NORMALIZER → RECONCILER)
element_index.json     ──┘
       ↓
manifest.json          ←── SME reviews review_flag: true entries
       ↓  [sl_apply.py]
matrix_revised.docx  +  audit.json
       ↓  [import into Storyline]
Updated story file
```

---

## What This Enables

**Immediate:** Reviewer comment cycles that previously required manual
slide-by-slide edits in Storyline can now be executed as a single import
operation, with a full audit trail and canon traceability on every change.

**Near-term:** The manifest generation step (currently a manual Claude
session) can be automated via API call once an Anthropic key is
available, making the full pipeline runnable from a single local command.

**Architectural significance:** The translation matrix hack generalizes.
Any Storyline course with a matrix export can be targeted by this
pipeline. The canon JSON format and manifest schema are course-agnostic.
The toolchain is reusable across clients and projects.

---

## Known Constraints and Edge Cases

**Multi-run paragraph rewrites** require explicit clearing entries for
residual runs. Failing to clear them leaves empty runs in the cell that
produce no visible text but may cause unexpected behavior in some
Storyline versions.

**Slide Notes as VO scripts.** When on-screen text is revised, the
corresponding Slide Notes element (which typically contains the
voiceover script) must also be revised to stay consistent. The
MANIFEST_RECONCILER and MANIFEST_GENERATOR profiles both include a
slide notes check in their quality verification step.

**Bold label preservation.** Cells with a bold label + normal description
pattern (common in role and process description text boxes) must use
`run_index: 1` to target the description while leaving the bold label
intact. Using `run_index: 0` on these cells will overwrite the label.

**Trigger and variable elements.** Storyline trigger variables (e.g.
`Set Variable: Head = "Why ALSAP Matters"`) appear in the matrix as
text elements and can be targeted like any other element. This is how
section header variables are updated via the matrix.

**ID not found.** If `sl_apply.py` reports a MISSING entry, the most
likely cause is that the matrix was re-exported from an updated story
file after element IDs regenerated. Re-run `sl_index.py` against the
new matrix and update the manifest before retrying.

---

## Provenance

This architecture was developed and validated in a single Claude Projects
inference session (June 2026) against the ALSAP Introduction training
course for Astellas (ALSAP_vCUR_.story), using:
- SOP-AST-29080 v1.0 as the primary canon document
- FORM-AST-34037 v1.0 as secondary canon
- 42 reviewer comments from the Astellas training review committee
- A Word-format translation matrix exported from Articulate Storyline 360

28 changes were applied and validated. The revised matrix imported
successfully into Storyline on the first attempt.
