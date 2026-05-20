# Trainstorm CGEN Toolkit

This folder contains everything needed to run the CGEN context-building pipeline.

---

## Folder Structure

```
CGEN_Toolkit\
  cgen_setup.bat                     ← Run this ONCE to install dependencies
  cgen_build.bat                     ← Run this every time to process a project
  README.md                          ← This file
  scripts\
    file_to_structured_all_md.py     ← Converts project files to structured Markdown
    merge_project_context_hardened.py ← Merges everything into one context file
```

---

## First-Time Setup

1. Double-click `cgen_setup.bat`
2. Follow the prompts — it will install all required Python packages automatically
3. You only need to do this once

> **Note:** Python must already be installed on your machine.  
> If you see an error about Python not being found, install it from [python.org](https://www.python.org/downloads/).  
> During installation, make sure to check **"Add Python to PATH"**.

---

## Running the Pipeline

1. Double-click `cgen_build.bat`
2. A Windows folder browser will open — navigate to your project folder and click OK
3. The tool will process all files and display progress as it runs
4. When it finishes, it will tell you exactly where your `project_context.md` file is
5. Optionally press Y to open the output folder in Explorer

---

## What It Does

The pipeline does two things in sequence:

1. **Converts** all supported files in your project folder into structured Markdown  
   (Supported: `.pptx`, `.docx`, `.xlsx`, `.xlsm`, `.pdf`, `.txt`, `.md`)

2. **Merges** all converted files into a single `project_context.md` that is ready  
   to paste into an AI tool like Claude

Output lands in:  
`[your project folder]\output\[timestamp]\project_context.md`

---

## Questions?

Contact Jake.
