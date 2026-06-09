# Keystone Tuxedo — Deck Style System

*Keystone* names the structure: one privileged anchor that everything else leans on.
*Tuxedo* names the surface: dark bookends around a white middle, with the brand accent
worn like a pocket square — one sharp spark, never the whole suit.

A client-agnostic specification for building polished, calm, senior-friendly slide decks.
Built with **pptxgenjs** (from-scratch), **react-icons + sharp** for icons, and a
LibreOffice render-and-QA loop.

To re-skin for any client: replace the **palette tokens** and **font** in Section 2.
Everything else — layout, motif, archetypes, helpers — stays the same.

---

## 1. The look in one paragraph

One dominant brand accent on a mostly-white deck, with dark "ink" slides bookending the
content (title + close) for a sandwich structure. Every slide opens with a small accent
square + an uppercase, letter-spaced kicker label, followed by a large bold title. Content
lives in flat cards (light surface fill, hairline border, very soft shadow) marked with a
thin accent bar and, where useful, an icon sitting in a soft-tinted circle. Most content
slides close with a single italic takeaway line behind a short accent bar. No full-width
colored header bars, no underline rules beneath titles, no gradients.

---

## 2. Canvas & palette tokens (the only things you swap per client)

```javascript
// Canvas
pres.layout = "LAYOUT_WIDE";   // 13.3" x 7.5"
const W = 13.3, H = 7.5;
const FONT = "Arial";          // use the client's brand sans; bold for all headers

// ---- PALETTE ROLES (assign client brand colors to these slots) ----
const ACCENT     = "D91E49";   // ONE dominant brand color — used sparingly but consistently
const ACCENT_DK  = "A62B4E";   // darker accent (optional, hover/secondary)
const SOFT_ACCENT= "FBE7EC";   // ~8% tint of ACCENT — icon-circle fills, takeaway band
const INK        = "2F2F31";   // dark slide background + dark contrast panels
const INK_CARD   = "3A3A3C";   // card fill when sitting ON a dark slide
const TEXT       = "4D4D4F";   // primary text on light slides
const MUTED      = "6F7072";   // secondary/descriptive text
const LIGHT      = "A7A9AC";   // captions, subtitles on dark, page numbers
const SURFACE    = "F7F8F9";   // card fill on light slides
const PANEL      = "FFFFFF";   // white card fill / slide background
const BORDER     = "E3E5E8";   // hairline card border
const BORDER_STR = "C9CDD2";   // stronger border / ghost numbers
const WHITE      = "FFFFFF";
```

**Rules for assigning the palette from a brand:**
- **The accent is the pocket square.** Pick exactly **one** dominant accent and wear it like
  a tuxedo's pocket square: a single sharp spark against black-and-white, never the whole suit.
  Keep 60–70% of the deck white. If the brand has several accents, the extras appear only as
  rare single-use highlights — never give colors equal weight.
- `SOFT_ACCENT` = the accent at roughly 8–12% tint (light enough that dark icons read on top).
- `INK` should be near-black with a hint of the brand's neutral, not pure `000000`.
- `TEXT`/`MUTED`/`LIGHT` come from the brand's gray ramp (dark → mid → light).
- Backgrounds are **white or INK only**. Never cream/beige.

---

## 3. Typography scale

| Element | Size | Weight | Color |
|---|---|---|---|
| Title-slide headline | 44pt | bold | WHITE (on INK) |
| Content slide title | 34pt | bold | TEXT |
| Kicker label | 12pt | bold, `charSpacing: 2`, UPPERCASE | ACCENT (or WHITE on dark) |
| Card / section header | 14–16pt | bold | TEXT (WHITE on dark) |
| Body / description | 11–12.5pt | regular | MUTED |
| Takeaway line | 15–16pt | bold italic | TEXT (accent for the emphasis clause) |
| Ghost numbers | 30–38pt | bold | BORDER_STR (light) or ACCENT (on dark) |
| Captions / footer / page no. | 9–11pt | regular | LIGHT |

Headers use the brand sans in bold. Don't introduce a second display font — the brand
font carries it.

---

## 4. The signature motif (repeat on every slide)

These five elements are what make the deck feel like one system. Define them once as
helpers (Section 6) and reuse.

1. **Kicker marker** — a `0.16"` accent square at `(0.6, 0.62)` with an UPPERCASE,
   letter-spaced label beside it at `(0.85, 0.5)`. This replaces an underline rule.
2. **Title** — 34pt bold at `(0.6, 1.0)`, width `12.1"`, left-aligned, `margin: 0`.
3. **Cards** — `SURFACE` fill, `1px BORDER`, soft shadow (`outer, blur 7, offset 3,
   angle 135, opacity 0.10`). A thin `0.1"` accent bar on the **left or top** edge.
4. **Icon-in-circle** — react-icon rasterized to PNG (size 256), centered inside a
   `~0.85"` `OVAL` filled with `SOFT_ACCENT`. The icon itself is ACCENT-colored.
5. **Takeaway line** — a `0.16" × 0.55"` accent bar at `(0.6, H-1.35)` with a bold-italic
   sentence beside it. Emphasis clause recolored to ACCENT.
6. **Footer** — tiny deck label bottom-left (9pt LIGHT) + page number bottom-right (10pt LIGHT).

---

## 5. Slide archetypes (the sandwich)

Build decks by composing these. Open and close dark; keep the middle light.

- **A — Title (dark):** INK background. Short accent bar `0.55"` wide above a 44pt white
  headline (2 lines OK). Light subtitle below; a small caption line near the bottom.
- **B — 4-card row (light):** kicker + title, then 4 cards across (`w≈2.78`, gap `0.34`,
  top `2.25`). Icon-in-circle top-left of each, bold header, muted description. Takeaway.
- **C — Hub & spokes (light):** central accent block (the "source") with white icon + label;
  4 satellite cards in the corners; thin dashed `LIGHT` connectors drawn **corner-to-corner
  in the gap** (never through a label). Used for "one thing → many things."
- **D — 3-card with ghost numbers (light):** 3 wide cards, big ghost number top-right of
  each, icon-in-circle top-left. Optional full-width note panel below for a key line.
- **E — Two-column contrast (light):** left card on `SURFACE` ("what people experience"),
  right card on `INK` ("what happens behind the scenes") with accent number bullets.
  Bottom accent-tinted band carries the one-line summary. Great for reassurance / before-after.
- **F — Flow chain (light):** dark source block → arrow → row of equal output cards, each
  with a top accent bar. Used for "source of truth → outputs."
- **G — Close (dark):** INK background, kicker + white title, a row of numbered dark cards
  (`INK_CARD` fill, large ACCENT number), then a bold-italic closing line + muted tagline.

Vary the archetype slide-to-slide — never repeat the same layout twice in a row.

---

## 6. Reusable helper code (drop-in)

```javascript
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// --- icon: react-icon component -> base64 PNG (crisp at size 256) ---
async function icon(IconComponent, hexNoHash, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: "#" + hexNoHash, size: String(size) })
  );
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}

// --- ALWAYS make a fresh shadow object per shape (pptxgenjs mutates in place) ---
const makeShadow = () => ({ type: "outer", color: "000000", blur: 7, offset: 3, angle: 135, opacity: 0.10 });

// --- kicker: accent square + uppercase tracked label ---
function kicker(pres, slide, label, accent, onDark = false) {
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.62, w: 0.16, h: 0.16, fill: { color: accent }, line: { type: "none" } });
  slide.addText(label.toUpperCase(), { x: 0.85, y: 0.5, w: 9, h: 0.4, fontFace: FONT,
    fontSize: 12, bold: true, color: onDark ? accent : accent, charSpacing: 2, valign: "middle" });
}

// --- title ---
function title(pres, slide, t, color, y = 1.0) {
  slide.addText(t, { x: 0.6, y, w: 12.1, h: 1.0, fontFace: FONT,
    fontSize: 34, bold: true, color, align: "left", valign: "top", margin: 0 });
}

// --- takeaway: short accent bar + bold-italic line ---
function takeaway(pres, slide, runs, accent, text = TEXT) {
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: H - 1.35, w: 0.16, h: 0.55, fill: { color: accent }, line: { type: "none" } });
  slide.addText(runs, { x: 0.85, y: H - 1.35, w: 11.6, h: 0.55, fontFace: FONT,
    fontSize: 15, italic: true, bold: true, color: text, valign: "middle", margin: 0 });
}

// --- footer ---
function footer(slide, deckLabel, n) {
  slide.addText(deckLabel, { x: 0.6, y: H - 0.55, w: 5, h: 0.3, fontFace: FONT, fontSize: 9, color: LIGHT, charSpacing: 1 });
  slide.addText(`${n}`, { x: W - 0.9, y: H - 0.55, w: 0.5, h: 0.3, fontFace: FONT, fontSize: 10, color: LIGHT, align: "right" });
}

// --- icon-in-circle (call inside a card) ---
function iconBadge(slide, iconData, x, y, soft, d = 0.85) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: soft }, line: { type: "none" } });
  const inset = d * 0.27;
  slide.addImage({ data: iconData, x: x + inset, y: y + inset, w: d - 2 * inset, h: d - 2 * inset });
}

// --- card with left accent bar ---
function card(pres, slide, x, y, w, h, fill, accent, side = "left") {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: BORDER, width: 1 }, shadow: makeShadow() });
  if (side === "left")  slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.1, h, fill: { color: accent }, line: { type: "none" } });
  if (side === "top")   slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.1, fill: { color: accent }, line: { type: "none" } });
}
```

**Hub-and-spoke connector** (keeps the dashed line out of the labels):
```javascript
// doc = central block rect {cx, cy, halfW, halfH}; box = satellite rect {x,y,w,h}
function connector(pres, slide, cx, cy, hW, hH, bx, by, bw, bh, color) {
  const bcx = bx + bw / 2, bcy = by + bh / 2;
  const isLeft = bcx < cx, isTop = bcy < cy;
  const p1x = cx + (isLeft ? -hW : hW), p1y = cy + (isTop ? -hH : hH);   // doc corner
  const p2x = isLeft ? bx + bw : bx,    p2y = isTop ? by + bh : by;       // box corner
  slide.addShape(pres.shapes.LINE, {
    x: Math.min(p1x, p2x), y: Math.min(p1y, p2y),
    w: Math.abs(p1x - p2x), h: Math.abs(p1y - p2y),
    line: { color, width: 1.5, dashType: "dash" },
    flipV: ((p1x < p2x) !== (p1y < p2y)),
  });
}
```

---

## 7. Layout & spacing rules

- Standard left margin **0.6"**; content width **12.1"**. Keep ≥ **0.5"** from every edge.
- Card grids: equal widths, gaps **0.26–0.34"**, used consistently within a slide.
- Title block occupies the top ~`1.9"`; content starts around `y = 2.2`; takeaway sits at
  `y = H − 1.35`. This rhythm repeats so slides feel aligned when flipped through.
- Icon-circle ≈ `0.85"`; icon rasterized at **256px** (display size set by `w`/`h` in inches).
- Set `margin: 0` on any text box you're aligning to a shape, bar, or icon edge.

---

## 8. Do / Don't

**Do**
- Keep 60–70% of the deck white; wear the accent like a pocket square — one spark, never the suit.
- Bookend dark (title + close), light in the middle.
- Repeat the kicker + title + takeaway rhythm on every content slide.
- Give cards a hairline border AND a whisper-soft shadow (not one or the other).
- Vary the archetype each slide.

**Don't**
- No underline/accent rules under titles (AI-slop tell) — the kicker square does that job.
- No full-width colored header/footer bars or side ribbons.
- No gradients (pptxgenjs can't do them natively; a flat fill or INK reads better anyway).
- Don't center body text — left-align everything except the title slide's headline if desired.
- Don't run connector lines through card labels — use the corner-to-corner helper.
- Don't reuse a shadow/options object across `addShape` calls — pptxgenjs mutates it; use `makeShadow()`.
- Don't let two-line titles collide with elements positioned for one line — leave headroom.

---

## 9. Build & QA pipeline

```bash
# 1. install
npm install pptxgenjs react react-dom react-icons sharp

# 2. build
node build.js

# 3. render to images for inspection
soffice --headless --convert-to pdf deck.pptx     # via the skill's soffice.py wrapper
pdftoppm -jpeg -r 130 deck.pdf slide

# 4. content QA — catch placeholders / typos
extract-text deck.pptx | grep -iE "lorem|ipsum|TODO|\[insert|undefined|\bx{3,}\b"
```

Then **look at every rendered slide** (fresh eyes — a subagent or a clean view pass).
Check, in order: (1) text fits inside its box, (2) no overlaps, (3) ≥0.5" edge margins
and even gaps, (4) two-line titles haven't pushed anything. Apply fixes, re-render the
affected slides once, and stop — don't chase sub-pixel nudges.

---

## 10. Icon vocabulary that fit this style (react-icons/fa)

Clean, single-weight Font Awesome solid icons read well in the circle badges:
`FaCompass, FaCubes, FaUsersCog, FaLifeRing, FaFileAlt, FaQuestionCircle, FaUserCheck,
FaBullseye, FaRegLightbulb, FaSitemap, FaArrowRight, FaPenFancy, FaCheckDouble, FaSyncAlt,
FaToolbox, FaBoxOpen, FaClipboardCheck, FaSeedling`. Keep all icons from one set for a
consistent line weight; recolor to ACCENT (or WHITE on dark blocks).
