# Lumina

Visual HTML authoring GUI for instructional designers. This is the **Lumina / lesson-canvas** studio: a custom block canvas (not GrapesJS) for assembling lessons, editing properties, previewing, inspecting generated HTML, saving to the browser, and exporting a standalone HTML file or zip.

This folder is self-contained. It does not change the rest of Trainstorm or `cgen`.

## Run

```bash
cd cgen/lumina
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## What you get

- Block canvas with heading, paragraph, image, button, list, callout, two-column, video placeholder, and quiz (MCQ)
- Properties panel for the selected block
- Live preview and a generated-HTML code inspector
- Autosave to `localStorage`
- Export as a single HTML file or a zip
- Starter lesson: **Giving constructive feedback**
