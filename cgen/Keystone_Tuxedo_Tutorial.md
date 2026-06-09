# Keystone Tuxedo — How to Work the System

A practical, plain-language tutorial. No terminal fluency assumed. If you can describe
what you want a deck to say, you can drive this.

---

## 0. The one thing to understand first

**This is not software you install. It's a spec plus a small helper library that an
assistant runs for you.** You already operated it once — that's how the AMT deck got
built. You brought the content and the intent; the machinery (Node, icons, rendering)
ran behind the scenes. This tutorial just makes that repeatable and shows you where the
levers are.

So there are two ways to run it:

- **The easy way — drive it through Claude.** You hand over content + brand colors, say
  "use the Keystone Tuxedo system," and it does all the terminal work, shows you pictures
  of every slide, and fixes what you flag. *You never touch a terminal.* Start here.
- **The hands-on way — run the build file yourself.** More setup, useful if you want to
  tinker offline. Covered last, kept optional.

---

## 1. What you bring to any new deck

Three inputs. None of them need to be polished.

1. **The content.** A narrative, an outline, or even a messy brief like the original AMT
   prompt. Rough is fine — the arc matters more than the wording.
2. **The brand.** Hex color codes and a font name. Or just paste the brand guidelines and
   let Claude map them to the palette *roles* (accent, ink, surface, text, etc.).
3. **The structure (optional).** Either name the archetypes you want (hub-and-spoke,
   two-column contrast, numbered close…) or just describe the *relationships* between your
   ideas and let Claude pick. Remember the system's sweet spot: **asymmetric relationships**
   — one source → many outputs, a whole → its parts, a sequence of steps. If your idea is a
   peer-to-peer web or a tradeoff matrix, say so, because that's where the look needs extra
   thought.

---

## 2. The easy way: driving it through Claude

This is the whole loop. It mirrors what you did to get the AMT deck.

1. **Open a session with file creation turned on** — the same kind of chat you're in now
   (web, desktop app, or Cowork). If you can ask it to make a file, you're set.
2. **Give it the two reference files** (`Keystone_Tuxedo_Tutorial.md` and the style system
   doc) plus your content and brand colors. Tell it to **use the Keystone Tuxedo system**.
3. **Let it build and show its work.** It writes the deck, renders each slide to an image,
   and shows them to you. It catches and fixes the obvious defects before you even look.
4. **Review the pictures and talk back in plain language.** You don't edit code — you say
   things like *"slide 4 feels cramped,"* *"make the closing line land harder,"* or
   *"swap the hub diagram for a part-whole breakdown."*
5. **Download the .pptx and open it in PowerPoint.** It's fully native — real editable
   text and shapes, not a flat image. Tweak freely from there.

### Your copy-paste kickoff prompt

Keep this. Fill in the blanks and paste it to start any new deck:

```
Use the Keystone Tuxedo deck style system (style guide attached). Build a [N]-slide
executive .pptx.

AUDIENCE: [who is this for, and what do they already know / not know]
PURPOSE: [what should they understand, decide, or do after seeing it]
NARRATIVE ARC: [your outline, or paste a rough brief — bullet points are fine]

BRAND:
- Dominant accent: [#HEX]
- Dark "ink": [#HEX or "use a near-black neutral"]
- Font: [brand sans, e.g. Arial]
- (or: brand guide attached — map it to the palette roles)

STRUCTURE NOTES: [which archetypes, or describe the relationships and pick for me]
TONE: [e.g. calm, practical, non-technical, not hype-driven]

Build it, render every slide to an image, show me, and fix any defects. Then give me
the downloadable .pptx.
```

That prompt is doing the same job the original AMT brief did — it just front-loads the
audience/purpose questions the system cares about most.

---

## 3. Reading the build file (so you can tweak, not fear it)

When Claude builds a deck it produces a `build.js` file. You don't have to touch it, but
knowing its three parts makes you dangerous in a good way:

1. **The palette block at the top.** A list of color tokens (`ACCENT`, `INK`, `SURFACE`…).
   *This is the only thing you change to re-brand.* Swap a hex code here and the whole deck
   re-skins.
2. **The helper functions.** `kicker`, `title`, `takeaway`, `card`, `iconBadge`,
   `connector`. These ARE the motif — the accent square, the cards, the dashed connectors.
   You rarely change these; they keep every deck consistent.
3. **One block per slide.** Each slide is its own section that calls the helpers. To change
   a headline, find that slide's text and edit the words. To reorder, move a block. To drop
   a slide, delete its block.

You cannot permanently break anything. If an edit goes wrong, you rebuild from the file or
ask Claude to regenerate it. Nothing you do in a draft touches a "master" until you decide.

---

## 4. The review loop: how to give feedback that lands

When you look at the rendered slide images, scan in this order — it's the same checklist
the build uses:

1. **Does the text fit inside its box?** Overflow is the most common issue and always
   visible. Flag any text that's cut off or crammed to an edge.
2. **Anything overlapping?** Lines through words, shapes on top of text.
3. **Even margins and gaps?** Roughly half an inch of breathing room from every edge;
   consistent spacing between cards.
4. **Did a title wrap to two lines and shove something?** Headroom matters.

Phrase fixes by *outcome*, not by coordinate: *"the third card is too tight,"* not
*"move it 0.2 inches." * Let the build figure out the numbers. And one healthy discipline:
fix the real defects, then stop. Endless micro-nudging rarely improves a deck a viewer
would already call clean.

---

## 5. The hands-on way: running the build file yourself (optional)

Only if you want to run it offline on your own computer. Honest heads-up: this needs a
little setup, and the *automatic slide-to-image* step is the fussy part. Good news — you
can skip that fussy part entirely, because **you have eyes**: just open the finished
PowerPoint and look at it. Here's the minimum path.

**One-time setup**
1. Install **Node.js** from the official site (nodejs.org — take the version it recommends).
   This gives you the `node` and `npm` commands. That's the only required install.
2. Put the `build.js` file in a folder of its own, e.g. `Documents\KeystoneTuxedo`.

**Each time you build**
1. **Open a terminal in that folder.**
   - Windows: open the folder in File Explorer, then type `cmd` in the address bar and press
     Enter (or right-click the folder → "Open in Terminal").
   - Mac: right-click the folder → "New Terminal at Folder."
   A terminal is just a window where you type one instruction per line and press Enter.
2. **Install the building blocks** (first time in a folder only). Type this line and press Enter:
   ```
   npm install pptxgenjs react react-dom react-icons sharp
   ```
   It downloads the pieces the build needs. Wait for it to finish.
3. **Build the deck.** Type:
   ```
   node build.js
   ```
   This creates the `.pptx` file in the same folder.
4. **Open the `.pptx` in PowerPoint and review it yourself.** Done.

*The render-to-image commands in the style guide (LibreOffice, `pdftoppm`) are only there
so an assistant can inspect slides automatically. As a human, you don't need them — opening
the file is the same check.* If you ever do want them, that's a separate, more involved
install (LibreOffice + Poppler), and it's genuinely easier to let Claude handle that QA pass
for you.

---

## 6. Troubleshooting — phrases that work

- Deck feels generic → *"Lean harder into the Keystone Tuxedo motif — dark bookends, accent
  pocket-square, kicker squares on every slide."*
- A diagram doesn't fit the idea → *"This is a part-whole relationship, not one-to-many —
  use the decomposition cards, not the hub."*
- Too much color → *"Pull the accent back; it should read like a pocket square, not a suit."*
- Text overflowing → *"Slide N has text spilling its box — shrink or split."*
- Want a Word/PDF version → ask for it; the same content can be re-cut into other formats.
- Lost the build file → paste the style guide and ask Claude to regenerate `build.js`.

---

## 7. Starting a brand-new deck from zero (the 30-second recipe)

1. Decide **audience** and **purpose** in one sentence each. (This is the real work.)
2. Sketch the **arc** — even four rough bullets.
3. Grab the **brand accent hex** and **font**.
4. Paste the kickoff prompt from Section 2, attach the style guide, fill the blanks.
5. Review the rendered slides, ask for fixes in plain words, download the `.pptx`.

That's the system. You bring the thinking; Keystone Tuxedo handles the looking-good.
