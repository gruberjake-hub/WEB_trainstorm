# Trainstorm Toolkit

One folder, one setup, many tools. Every tool in this kit runs from its own
private Python environment, so it works the same on every machine — including
machines with messy or multiple Python installs.

---

## Folder Structure

```
Trainstorm_Toolkit\
  setup.bat                ← Run ONCE to build the private environment
  cgen_build.bat           ← Tool 1: build a project context file for AI
  matrix_extract.bat       ← Tool 2: pull a Storyline translation matrix to Excel
  matrix_reinject.bat      ← Tool 3: put translations back into the matrix
  README.md                ← This file
  venv\                    ← Private Python environment (created by setup.bat)
  scripts\
    file_to_structured_all_md.py
    merge_project_context_hardened.py
    matrix_extract.py
    matrix_reinject.py
    latest_subdir.py
    pick_folder.py
    pick_file.py
```

---

## First-Time Setup

1. Double-click `setup.bat`
2. Follow the prompts — it builds a private Python environment inside this
   folder (the `venv` folder) and installs everything the tools need into it
3. You only need to do this once

> **Note:** Python must already be installed on your machine.
> If setup says Python was not found, install it from
> [python.org](https://www.python.org/downloads/) and check
> **"Add Python to PATH"** during installation. Then run setup again.

**Why the private environment matters:** after setup, the tools never use
your machine's Python directly. They always run
`venv\Scripts\python.exe` by its full path. This is why the toolkit can't be
broken by other Python installs, updates, or PATH problems — everything it
needs lives inside this folder.

---

## The Tools

### 1. Context Builder (`cgen_build.bat`)
Converts every supported file in a project folder into structured Markdown,
then merges them into a single `project_context.md` ready to paste into an
AI tool like Claude.

Supported inputs: `.pptx` `.docx` `.xlsx` `.xlsm` `.pdf` `.txt` `.md`

Output lands in: `[your project folder]\output\[timestamp]\project_context.md`

### 2. Matrix Extract (`matrix_extract.bat`)
Takes a Storyline translation matrix (.docx export) and creates a
**translation job folder** next to it, containing:

- `INSTRUCTIONS.txt` — the step-by-step guide for whoever runs the job
- `1_packets\` — small numbered text files. Each one is a complete,
  ready-to-paste prompt (instructions + segments) sized so that weaker
  AI tools like Copilot handle it reliably
- `2_translated\` — an empty folder where you save the AI's answers
- `master.xlsx` — the full ledger of every segment. You can also type
  translations directly into its Translation column; anything entered
  there wins over the packet answers
- `structure_report.txt` — exactly what the extractor found and skipped

The Word file itself is never edited by hand or by AI. It is read once,
here, and not touched again until reinjection.

### 3. Matrix Reinject (`matrix_reinject.bat`)
Asks for the **original** matrix .docx and the **job folder**, then:

1. Confirms the docx is the exact file the job was extracted from
2. Reads every answer from `2_translated\` and `master.xlsx`
   (file names, order, and duplicates don't matter — segments are
   matched by their IDs)
3. Validates everything and writes `coverage_report.txt`: what's ready,
   what's missing, what's malformed — by segment ID
4. Only when validation passes (or you explicitly choose a partial
   write) does it inject the translations into a **new copy** of the
   matrix — every table, row, cell, and merge passes through untouched;
   only the text in translation cells changes. The original is never
   modified. The new copy is what you import into Storyline.

If anything is missing, the normal fix is: re-run just the affected
packets in Copilot, save the answers into `2_translated\`, and run
reinject again. The loop converges fast because each pass only touches
what failed.

---

## How the Launchers Work (worth 60 seconds)

Each `.bat` file does the same simple thing: it shows you the exact Python
command it is about to run, then runs it using the private environment.
For example:

```
Running: venv\Scripts\python.exe scripts\matrix_extract.py --input "C:\...\matrix.docx"
```

That line is a complete, real command — the same thing you would type in a
terminal yourself. The launcher just types it for you. Over time, these are
the commands you'll recognize and eventually run on your own.

---

## The Translation Round Trip at a Glance

```
Storyline export (.docx)
      │  matrix_extract.bat
      ▼
job folder ── packets ──> Copilot/Studio ──> answers saved to 2_translated\
      │  matrix_reinject.bat  (validates, reports, loops until complete)
      ▼
new translated .docx  ──>  import into Storyline
```

Three rules keep it safe:
1. Never edit the original .docx — not by hand, not with an AI.
2. Never re-export from Storyline mid-job (internal IDs change).
   One export, one round trip.
3. Don't change the `[S0001]`-style IDs anywhere.

## Adding New Tools

New capabilities arrive as two files: a `.bat` launcher for this folder and
a `.py` script for the `scripts` folder. Drop them in and double-click. No
new setup is needed — every tool shares the same private environment.

---

## Questions?

Contact Jake.
