/* =============================================================================
   KEYSTONE TUXEDO — STARTER build.js
   -----------------------------------------------------------------------------
   A working skeleton. Run it as-is to produce a reference deck with one slide
   per archetype, then edit to make your own.

   HOW TO USE
     1) npm install pptxgenjs react react-dom react-icons sharp   (first time)
     2) node build.js                                             (builds the .pptx)
     3) open the .pptx in PowerPoint

   WHAT TO EDIT
     • To rebrand:  change the PALETTE block (Section 1). That is usually all.
     • To retell:   edit the words inside each archetype function (Section 4).
     • To reorder:  rearrange the addSlide calls in main() (bottom of file).

   You cannot permanently break this — if an edit goes wrong, rebuild from a copy.
   ============================================================================= */

const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaLayerGroup, FaCompass, FaUsersCog, FaCubes, FaSitemap, FaUserCheck,
  FaBullseye, FaRegLightbulb, FaFileAlt, FaPenFancy, FaCheckDouble, FaArrowRight,
} = require("react-icons/fa");

/* =============================================================================
   SECTION 1 — PALETTE  (the only block you change to rebrand)
   The accent is the pocket square: ONE sharp spark against black-and-white.
   ============================================================================= */
const ACCENT     = "0F766E";   // ← the one dominant brand color (deep teal default)
const ACCENT_DK  = "0B5A54";   // darker accent (optional)
const SOFT_ACCENT= "E3F0EE";   // ~10% tint of ACCENT — icon circles, takeaway band
const INK        = "22272E";   // dark slide background + dark contrast panels
const INK_CARD   = "2D343C";   // card fill when sitting ON a dark slide
const TEXT       = "2B2F36";   // primary text on light slides
const MUTED      = "5C636D";   // secondary / descriptive text
const LIGHT      = "9AA1AB";   // captions, subtitles on dark, page numbers
const SURFACE    = "F6F7F8";   // card fill on light slides
const PANEL      = "FFFFFF";   // white card fill / slide background
const BORDER     = "E4E7EA";   // hairline card border
const BORDER_STR = "C8CDD3";   // stronger border / ghost numbers
const WHITE      = "FFFFFF";

const FONT = "Arial";          // ← use the client's brand sans
const DECK_LABEL = "Keystone Tuxedo";   // footer text

/* =============================================================================
   SECTION 2 — ARCHETYPE → INTENT MAP
   Seed for a learner-intent library: each visual archetype encodes a structural
   relationship, and each relationship serves a learner intent. Extend this as the
   library grows (e.g., add emotional state, ADRA phase, evidence type per entry).
   ============================================================================= */
const ARCHETYPE_INTENT = {
  A_title:    { relationship: "frame",           intent: "ORIENT — set stance and stakes before any content" },
  B_cards:    { relationship: "part-whole",      intent: "INVENTORY — show a whole is made of known parts" },
  C_hubspoke: { relationship: "one-to-many",     intent: "DERIVE — one source authors many outputs" },
  D_numbered: { relationship: "ordered set",     intent: "SEQUENCE — impose order or decision steps" },
  E_contrast: { relationship: "correspondence",  intent: "REASSURE — map what-you-see to what-happens" },
  F_flow:     { relationship: "provenance flow", intent: "TRACE — follow source of truth to deliverables" },
  G_close:    { relationship: "path / sequence", intent: "COMMIT — a low-risk ordered way forward" },
};

/* =============================================================================
   SECTION 3 — CANVAS + HELPERS (the motif; rarely changed)
   ============================================================================= */
const W = 13.3, H = 7.5;

// react-icon component -> base64 PNG (crisp at size 256)
async function icon(IconComponent, hexNoHash, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: "#" + hexNoHash, size: String(size) })
  );
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}

// fresh shadow object per shape (pptxgenjs mutates options in place)
const makeShadow = () => ({ type: "outer", color: "000000", blur: 7, offset: 3, angle: 135, opacity: 0.10 });

// accent square + uppercase letter-spaced kicker label (replaces an underline rule)
function kicker(pres, slide, label, onDark = false) {
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.62, w: 0.16, h: 0.16, fill: { color: ACCENT }, line: { type: "none" } });
  slide.addText(label.toUpperCase(), { x: 0.85, y: 0.5, w: 11, h: 0.4, fontFace: FONT,
    fontSize: 12, bold: true, color: ACCENT, charSpacing: 2, valign: "middle", margin: 0 });
}

// title
function title(pres, slide, t, color = TEXT, y = 1.0, size = 34) {
  slide.addText(t, { x: 0.6, y, w: 12.1, h: 1.0, fontFace: FONT,
    fontSize: size, bold: true, color, align: "left", valign: "top", margin: 0 });
}

// takeaway: short accent bar + bold-italic line (runs = string or rich-text array)
function takeaway(pres, slide, runs) {
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: H - 1.35, w: 0.16, h: 0.55, fill: { color: ACCENT }, line: { type: "none" } });
  slide.addText(runs, { x: 0.85, y: H - 1.35, w: 11.6, h: 0.55, fontFace: FONT,
    fontSize: 15, italic: true, bold: true, color: TEXT, valign: "middle", margin: 0 });
}

// footer: deck label left + page number right
function footer(slide, n) {
  slide.addText(DECK_LABEL, { x: 0.6, y: H - 0.55, w: 5, h: 0.3, fontFace: FONT, fontSize: 9, color: LIGHT, charSpacing: 1, margin: 0 });
  slide.addText(`${n}`, { x: W - 0.9, y: H - 0.55, w: 0.5, h: 0.3, fontFace: FONT, fontSize: 10, color: LIGHT, align: "right", margin: 0 });
}

// icon centered inside a soft-tinted circle
function iconBadge(pres, slide, iconData, x, y, d = 0.85, fill = SOFT_ACCENT) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" } });
  const inset = d * 0.27;
  slide.addImage({ data: iconData, x: x + inset, y: y + inset, w: d - 2 * inset, h: d - 2 * inset });
}

// card with a thin accent bar on one edge
function card(pres, slide, x, y, w, h, fill = SURFACE, side = "left") {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill },
    line: fill === SURFACE || fill === PANEL ? { color: BORDER, width: 1 } : { type: "none" }, shadow: makeShadow() });
  if (side === "left") slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.1, h, fill: { color: ACCENT }, line: { type: "none" } });
  if (side === "top")  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.1, fill: { color: ACCENT }, line: { type: "none" } });
}

// dashed connector from a central block corner to a satellite box corner (stays in the gap)
function connector(pres, slide, cx, cy, hW, hH, bx, by, bw, bh) {
  const bcx = bx + bw / 2, bcy = by + bh / 2;
  const isLeft = bcx < cx, isTop = bcy < cy;
  const p1x = cx + (isLeft ? -hW : hW), p1y = cy + (isTop ? -hH : hH);
  const p2x = isLeft ? bx + bw : bx,    p2y = isTop ? by + bh : by;
  slide.addShape(pres.shapes.LINE, {
    x: Math.min(p1x, p2x), y: Math.min(p1y, p2y),
    w: Math.abs(p1x - p2x), h: Math.abs(p1y - p2y),
    line: { color: LIGHT, width: 1.5, dashType: "dash" },
    flipV: ((p1x < p2x) !== (p1y < p2y)),
  });
}

/* =============================================================================
   SECTION 4 — ARCHETYPES (one function each; edit the words inside)
   Each adds one slide. Pass `ic` (pre-rendered icons) where needed.
   ============================================================================= */

// A — TITLE (dark). intent: ORIENT
function A_title(pres) {
  const s = pres.addSlide();
  s.background = { color: INK };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.9, y: 2.35, w: 0.55, h: 0.16, fill: { color: ACCENT }, line: { type: "none" } });
  s.addText("Keystone Tuxedo", { x: 0.85, y: 2.6, w: 11.5, h: 1.5, fontFace: FONT, fontSize: 48,
    bold: true, color: WHITE, align: "left", valign: "top", margin: 0 });
  s.addText("A starter deck — one archetype per slide.", { x: 0.9, y: 4.35, w: 11, h: 0.5,
    fontFace: FONT, fontSize: 18, color: LIGHT, align: "left", margin: 0 });
  s.addText("Edit the palette block to rebrand · edit each slide block to retell.", { x: 0.9, y: 6.55,
    w: 11, h: 0.4, fontFace: FONT, fontSize: 12, color: MUTED, align: "left", charSpacing: 1, margin: 0 });
  s.addNotes(`Archetype A — ${ARCHETYPE_INTENT.A_title.relationship}. Intent: ${ARCHETYPE_INTENT.A_title.intent}.`);
}

// B — 4-CARD ROW (light). intent: INVENTORY (part-whole)
function B_cards(pres, ic) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(pres, s, "Archetype B · Part–Whole");
  title(pres, s, "A whole made of known parts");

  const blocks = [
    { ic: ic.layer,   h: "First component", d: "One short supporting line." },
    { ic: ic.compass, h: "Second component", d: "One short supporting line." },
    { ic: ic.users,   h: "Third component", d: "One short supporting line." },
    { ic: ic.cubes,   h: "Fourth component", d: "One short supporting line." },
  ];
  const cardW = 2.78, gap = 0.34, startX = 0.6, cardY = 2.25, cardH = 2.45;
  blocks.forEach((b, i) => {
    const x = startX + i * (cardW + gap);
    card(pres, s, x, cardY, cardW, cardH, SURFACE, "none");
    iconBadge(pres, s, b.ic, x + 0.3, cardY + 0.32);
    s.addText(b.h, { x: x + 0.28, y: cardY + 1.35, w: cardW - 0.5, h: 0.5, fontFace: FONT,
      fontSize: 15, bold: true, color: TEXT, valign: "top", margin: 0 });
    s.addText(b.d, { x: x + 0.28, y: cardY + 1.85, w: cardW - 0.5, h: 0.5, fontFace: FONT,
      fontSize: 11.5, color: MUTED, valign: "top", margin: 0, lineSpacingMultiple: 1.05 });
  });
  takeaway(pres, s, "Use when the point is: this thing is built from these specific pieces.");
  footer(s, 2);
  s.addNotes(`Archetype B — ${ARCHETYPE_INTENT.B_cards.relationship}. Intent: ${ARCHETYPE_INTENT.B_cards.intent}.`);
}

// C — HUB & SPOKES (light). intent: DERIVE (one-to-many)
function C_hubspoke(pres, ic) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(pres, s, "Archetype C · One-to-Many");
  title(pres, s, "One source, many outputs");

  const cx = 6.65, cy = 3.95, hW = 0.95, hH = 0.55;
  const boxes = [
    { t: "Output one",   x: 0.9,  y: 2.7 },
    { t: "Output two",   x: 9.5,  y: 2.7 },
    { t: "Output three", x: 0.9,  y: 4.9 },
    { t: "Output four",  x: 9.5,  y: 4.9 },
  ];
  const bw = 2.9, bh = 1.0;
  boxes.forEach(b => {
    connector(pres, s, cx, cy, hW, hH, b.x, b.y, bw, bh);
    card(pres, s, b.x, b.y, bw, bh, SURFACE, "none");
    s.addText(b.t, { x: b.x + 0.15, y: b.y, w: bw - 0.3, h: bh, fontFace: FONT,
      fontSize: 14, bold: true, color: TEXT, align: "center", valign: "middle", margin: 0 });
  });
  // central source block (drawn last so connectors tuck under it)
  s.addShape(pres.shapes.RECTANGLE, { x: cx - hW, y: cy - hH, w: hW * 2, h: hH * 2, fill: { color: ACCENT }, line: { type: "none" }, shadow: makeShadow() });
  s.addImage({ data: ic.sitemap, x: cx - 0.3, y: cy - 0.45, w: 0.6, h: 0.6 });
  s.addText("THE SOURCE", { x: cx - hW, y: cy + 0.12, w: hW * 2, h: 0.4, fontFace: FONT,
    fontSize: 11, bold: true, color: WHITE, align: "center", charSpacing: 1, margin: 0 });
  takeaway(pres, s, "Use when the point is: one stable thing generates everything downstream.");
  footer(s, 3);
  s.addNotes(`Archetype C — ${ARCHETYPE_INTENT.C_hubspoke.relationship}. Intent: ${ARCHETYPE_INTENT.C_hubspoke.intent}.`);
}

// D — 3-CARD WITH GHOST NUMBERS (light). intent: SEQUENCE (ordered set)
function D_numbered(pres, ic) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(pres, s, "Archetype D · Ordered Set");
  title(pres, s, "Three questions, in order");

  const qs = [
    { ic: ic.userCheck, h: "Who is this for?", d: "Name the audience first." },
    { ic: ic.bullseye,  h: "What is the goal?", d: "Be clear on the outcome." },
    { ic: ic.bulb,      h: "What is the format?", d: "Match it to the need." },
  ];
  const cardW = 3.9, gap = 0.3, startX = 0.6, cardY = 2.2, cardH = 2.55;
  qs.forEach((b, i) => {
    const x = startX + i * (cardW + gap);
    card(pres, s, x, cardY, cardW, cardH, PANEL, "none");
    iconBadge(pres, s, b.ic, x + 0.32, cardY + 0.34);
    s.addText(`0${i + 1}`, { x: x + cardW - 1.0, y: cardY + 0.28, w: 0.8, h: 0.6, fontFace: FONT,
      fontSize: 30, bold: true, color: BORDER_STR, align: "right", margin: 0 });
    s.addText(b.h, { x: x + 0.32, y: cardY + 1.35, w: cardW - 0.6, h: 0.55, fontFace: FONT,
      fontSize: 15, bold: true, color: TEXT, valign: "top", margin: 0 });
    s.addText(b.d, { x: x + 0.32, y: cardY + 1.9, w: cardW - 0.6, h: 0.4, fontFace: FONT,
      fontSize: 11.5, color: MUTED, valign: "top", margin: 0 });
  });
  // full-width note panel for a key line
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 5.05, w: 12.1, h: 1.0, fill: { color: SURFACE }, line: { color: BORDER, width: 1 } });
  s.addText([
    { text: "Skip these and the fallback is to add more content. ", options: { bold: true, color: TEXT } },
    { text: "Bigger — not more useful.", options: { bold: true, color: ACCENT } },
  ], { x: 0.9, y: 5.05, w: 11.5, h: 1.0, fontFace: FONT, fontSize: 15, valign: "middle", margin: 0 });
  footer(s, 4);
  s.addNotes(`Archetype D — ${ARCHETYPE_INTENT.D_numbered.relationship}. Intent: ${ARCHETYPE_INTENT.D_numbered.intent}.`);
}

// E — TWO-COLUMN CONTRAST (light + dark panel). intent: REASSURE (correspondence)
function E_contrast(pres, ic) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(pres, s, "Archetype E · Correspondence");
  title(pres, s, "What you see, and what happens");

  const colY = 2.2, colH = 3.35, leftX = 0.6, leftW = 5.85, rightX = 6.85, rightW = 5.85;
  // LEFT — light
  s.addShape(pres.shapes.RECTANGLE, { x: leftX, y: colY, w: leftW, h: colH, fill: { color: SURFACE }, line: { color: BORDER, width: 1 }, shadow: makeShadow() });
  s.addText("WHAT YOU EXPERIENCE", { x: leftX + 0.35, y: colY + 0.28, w: leftW - 0.7, h: 0.4, fontFace: FONT,
    fontSize: 12.5, bold: true, color: ACCENT, charSpacing: 1, margin: 0 });
  const leftItems = [
    { ic: ic.file,   t: "A familiar step", d: "Described in plain terms." },
    { ic: ic.pen,    t: "Another familiar step", d: "Described in plain terms." },
    { ic: ic.check,  t: "A third familiar step", d: "Described in plain terms." },
  ];
  leftItems.forEach((it, i) => {
    const y = colY + 0.85 + i * 0.82;
    iconBadge(pres, s, it.ic, leftX + 0.35, y + 0.02, 0.5);
    s.addText(it.t, { x: leftX + 1.05, y: y - 0.05, w: leftW - 1.4, h: 0.35, fontFace: FONT,
      fontSize: 13.5, bold: true, color: TEXT, valign: "top", margin: 0 });
    s.addText(it.d, { x: leftX + 1.05, y: y + 0.3, w: leftW - 1.4, h: 0.35, fontFace: FONT,
      fontSize: 11, color: MUTED, valign: "top", margin: 0 });
  });
  // RIGHT — dark
  s.addShape(pres.shapes.RECTANGLE, { x: rightX, y: colY, w: rightW, h: colH, fill: { color: INK }, line: { type: "none" }, shadow: makeShadow() });
  s.addText("WHAT HAPPENS UNDERNEATH", { x: rightX + 0.35, y: colY + 0.28, w: rightW - 0.7, h: 0.4, fontFace: FONT,
    fontSize: 12.5, bold: true, color: WHITE, charSpacing: 1, margin: 0 });
  ["The matching mechanism, step one.", "The matching mechanism, step two.", "The matching mechanism, step three."].forEach((t, i) => {
    const y = colY + 0.85 + i * 0.82;
    s.addShape(pres.shapes.OVAL, { x: rightX + 0.35, y: y + 0.02, w: 0.5, h: 0.5, fill: { color: ACCENT }, line: { type: "none" } });
    s.addText(`${i + 1}`, { x: rightX + 0.35, y: y + 0.02, w: 0.5, h: 0.5, fontFace: FONT,
      fontSize: 16, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(t, { x: rightX + 1.05, y: y - 0.02, w: rightW - 1.45, h: 0.6, fontFace: FONT,
      fontSize: 13, color: WHITE, valign: "middle", margin: 0, lineSpacingMultiple: 1.05 });
  });
  // bottom band
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 5.75, w: 12.1, h: 1.0, fill: { color: SOFT_ACCENT }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 5.75, w: 0.14, h: 1.0, fill: { color: ACCENT }, line: { type: "none" } });
  s.addText([
    { text: "The left is where people act.   ", options: { bold: true, color: TEXT } },
    { text: "The right is what keeps it all consistent.", options: { bold: true, color: ACCENT } },
  ], { x: 0.95, y: 5.75, w: 11.6, h: 1.0, fontFace: FONT, fontSize: 16, valign: "middle", margin: 0 });
  footer(s, 5);
  s.addNotes(`Archetype E — ${ARCHETYPE_INTENT.E_contrast.relationship}. Intent: ${ARCHETYPE_INTENT.E_contrast.intent}.`);
}

// F — FLOW CHAIN (light). intent: TRACE (provenance flow)
function F_flow(pres, ic) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(pres, s, "Archetype F · Provenance Flow");
  title(pres, s, "Source of truth to deliverables");
  s.addText("One approved source feeds every output — built once, kept aligned.", {
    x: 0.6, y: 1.95, w: 12.1, h: 0.5, fontFace: FONT, fontSize: 15, color: MUTED, margin: 0 });

  const sy = 3.05, sh = 1.7, srcX = 0.6, srcW = 3.0;
  s.addShape(pres.shapes.RECTANGLE, { x: srcX, y: sy, w: srcW, h: sh, fill: { color: INK }, line: { type: "none" }, shadow: makeShadow() });
  s.addText("Core source", { x: srcX + 0.25, y: sy + 0.3, w: srcW - 0.5, h: 0.7, fontFace: FONT,
    fontSize: 16, bold: true, color: WHITE, valign: "top", margin: 0 });
  s.addText("The approved source of truth", { x: srcX + 0.25, y: sy + 1.0, w: srcW - 0.5, h: 0.5,
    fontFace: FONT, fontSize: 11.5, color: LIGHT, valign: "top", margin: 0 });
  s.addImage({ data: ic.arrow, x: srcX + srcW + 0.15, y: sy + sh / 2 - 0.25, w: 0.5, h: 0.5 });

  const outs = ["Output one", "Output two", "Output three", "Output four"];
  const fx0 = srcX + srcW + 0.85, fw = 1.95, fgap = 0.2;
  outs.forEach((o, i) => {
    const x = fx0 + i * (fw + fgap);
    card(pres, s, x, sy, fw, sh, SURFACE, "top");
    s.addText(o, { x: x + 0.18, y: sy + 0.4, w: fw - 0.36, h: 0.9, fontFace: FONT,
      fontSize: 14, bold: true, color: TEXT, valign: "top", margin: 0 });
    s.addText("from the same source", { x: x + 0.18, y: sy + sh - 0.5, w: fw - 0.36, h: 0.35,
      fontFace: FONT, fontSize: 9.5, italic: true, color: MUTED, valign: "top", margin: 0 });
  });
  takeaway(pres, s, "Use when the point is: trace any deliverable back to one trusted origin.");
  footer(s, 6);
  s.addNotes(`Archetype F — ${ARCHETYPE_INTENT.F_flow.relationship}. Intent: ${ARCHETYPE_INTENT.F_flow.intent}.`);
}

// G — CLOSE (dark). intent: COMMIT (path / sequence)
function G_close(pres) {
  const s = pres.addSlide();
  s.background = { color: INK };
  kicker(pres, s, "Archetype G · Path Forward", true);
  title(pres, s, "A low-risk way forward", WHITE, 1.0, 32);

  const steps = [
    { t: "Keep what works", d: "Nothing valuable is discarded." },
    { t: "Extract the core", d: "Make it the stable foundation." },
    { t: "Pilot a few outputs", d: "Prove value before scaling." },
    { t: "Keep it aligned", d: "Use the change process going forward." },
  ];
  const cardW = 2.86, gap = 0.32, startX = 0.6, cardY = 2.35, cardH = 2.55;
  steps.forEach((b, i) => {
    const x = startX + i * (cardW + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: cardY, w: cardW, h: cardH, fill: { color: INK_CARD }, line: { type: "none" }, shadow: makeShadow() });
    s.addText(`${i + 1}`, { x: x + 0.28, y: cardY + 0.25, w: 0.9, h: 0.8, fontFace: FONT,
      fontSize: 38, bold: true, color: ACCENT, margin: 0 });
    s.addText(b.t, { x: x + 0.3, y: cardY + 1.15, w: cardW - 0.6, h: 0.65, fontFace: FONT,
      fontSize: 15.5, bold: true, color: WHITE, valign: "top", margin: 0, lineSpacingMultiple: 1.02 });
    s.addText(b.d, { x: x + 0.3, y: cardY + 1.78, w: cardW - 0.6, h: 0.65, fontFace: FONT,
      fontSize: 11.5, color: LIGHT, valign: "top", margin: 0, lineSpacingMultiple: 1.08 });
  });
  s.addText("Preserve the value of the work.  Improve the way it is used.", {
    x: 0.6, y: 5.5, w: 12.1, h: 0.7, fontFace: FONT, fontSize: 20, bold: true, italic: true,
    color: WHITE, valign: "middle", margin: 0 });
  s.addText("Less rewriting.  More precision.  Better adoption.", {
    x: 0.6, y: 6.25, w: 12.1, h: 0.5, fontFace: FONT, fontSize: 14, color: LIGHT, charSpacing: 1, margin: 0 });
  s.addNotes(`Archetype G — ${ARCHETYPE_INTENT.G_close.relationship}. Intent: ${ARCHETYPE_INTENT.G_close.intent}.`);
}

/* =============================================================================
   SECTION 5 — MAIN  (reorder / add / remove slides here)
   ============================================================================= */
(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.author = "Keystone Tuxedo";
  pres.title = "Keystone Tuxedo — Starter";

  const ic = {
    layer:    await icon(FaLayerGroup, ACCENT),
    compass:  await icon(FaCompass, ACCENT),
    users:    await icon(FaUsersCog, ACCENT),
    cubes:    await icon(FaCubes, ACCENT),
    sitemap:  await icon(FaSitemap, WHITE),
    userCheck:await icon(FaUserCheck, ACCENT),
    bullseye: await icon(FaBullseye, ACCENT),
    bulb:     await icon(FaRegLightbulb, ACCENT),
    file:     await icon(FaFileAlt, ACCENT),
    pen:      await icon(FaPenFancy, ACCENT),
    check:    await icon(FaCheckDouble, ACCENT),
    arrow:    await icon(FaArrowRight, LIGHT),
  };

  A_title(pres);
  B_cards(pres, ic);
  C_hubspoke(pres, ic);
  D_numbered(pres, ic);
  E_contrast(pres, ic);
  F_flow(pres, ic);
  G_close(pres);

  const out = "Keystone_Tuxedo_Starter.pptx";
  await pres.writeFile({ fileName: out });
  console.log("WROTE", out);
})();
