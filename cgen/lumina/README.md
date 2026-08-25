# Lumina

Visual HTML authoring GUI for instructional designers. This is the **Lumina / lesson-canvas** studio: a custom block canvas (not GrapesJS) for assembling lessons, editing properties, previewing, inspecting generated HTML, saving to the browser, and exporting a standalone HTML file or zip.

This folder is self-contained. It does not change the rest of Trainstorm or `cgen`.

## Run

Local studio (no base path):

```bash
cd cgen/lumina
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

Production is a static export on the existing Netlify site: [https://trainstorm.ai/cgen/lumina](https://trainstorm.ai/cgen/lumina). Netlify runs `npm ci && npm run build` in this folder on push and copies `out/` onto `/cgen/lumina` (the `/cgen` course player is unchanged).

```bash
cd cgen/lumina
npm run build
```

That writes a static site to `out/` (`output: "export"`). Do not commit `out/` or `.next/`.

## What you get

- Block canvas with heading, paragraph, image, button, list, callout, two-column, video placeholder, and quiz (MCQ)
- Properties panel for the selected block
- Live preview and a generated-HTML code inspector
- Autosave to `localStorage` (imported HTML is a new project and does not overwrite the previous lesson until you Save)
- **Import HTML** (file picker or paste) — headings, lists, images, links/buttons, callouts, columns, video/iframes, quizzes; leftover markup is kept as an HTML block
- Export as a single HTML file or a zip
- Starter lesson: **Giving constructive feedback**
