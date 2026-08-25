import { nid } from "./ids";
import { parseAlign } from "./style";
import type {
  Align,
  Block,
  BlockStyle,
  CalloutTone,
  ImageBlock,
  Lesson,
} from "./types";

export type HtmlImportResult = {
  lesson: Lesson;
  note?: string;
};

type Flags = {
  usedHtmlFallback: boolean;
  skippedCss: boolean;
  skippedLayout: boolean;
  capturedJs: boolean;
};

const SKIP_TAGS = new Set(["SCRIPT", "STYLE", "LINK", "META", "NOSCRIPT", "TEMPLATE", "HEAD"]);
const WRAPPER_TAGS = new Set(["DIV", "SECTION", "ARTICLE", "MAIN", "HEADER", "FOOTER", "SPAN"]);
const ALLOWED_HTML = new Set([
  "P", "DIV", "SPAN", "H1", "H2", "H3", "H4", "H5", "H6",
  "UL", "OL", "LI", "A", "IMG", "STRONG", "B", "EM", "I",
  "BR", "HR", "BLOCKQUOTE", "FIGURE", "FIGCAPTION",
  "TABLE", "THEAD", "TBODY", "TFOOT", "TR", "TD", "TH",
  "PRE", "CODE", "SUB", "SUP", "SMALL", "MARK", "U",
]);

export function importHtmlDocument(source: string, filename?: string): HtmlImportResult {
  const flags: Flags = {
    usedHtmlFallback: false,
    skippedCss: false,
    skippedLayout: false,
    capturedJs: false,
  };

  const doc = new DOMParser().parseFromString(source, "text/html");
  if (doc.querySelector("style, link[rel='stylesheet']")) flags.skippedCss = true;

  const extraJs = collectScripts(doc, flags);
  const root = pickRoot(doc);
  const titleFromDoc = (doc.querySelector("title")?.textContent || "").trim();
  const titleEl = root.querySelector("h1.lesson-title, .lesson-title") || root.querySelector("h1");
  const subEl = root.querySelector("p.lesson-sub, .lesson-sub, .subtitle");
  const title =
    (titleEl?.textContent || "").trim() ||
    titleFromDoc ||
    filenameToTitle(filename) ||
    "Imported lesson";
  const subtitle = (subEl?.textContent || "").trim();

  const skip = new Set<Element>();
  root.querySelectorAll(".lesson-kicker").forEach((el) => skip.add(el));
  if (titleEl) skip.add(titleEl);
  if (subEl) skip.add(subEl);

  const blocks = childNodesToBlocks(root, flags, skip).filter(Boolean);

  if (!blocks.length) {
    const text = visibleText(root);
    if (text) {
      blocks.push({
        id: nid(),
        type: "paragraph",
        text,
      });
    } else {
      flags.usedHtmlFallback = true;
      blocks.push({
        id: nid(),
        type: "html",
        html: sanitizeHtml(root.innerHTML) || "<p>(Empty document)</p>",
      });
    }
  }

  const lesson: Lesson = {
    id: nid("lesson"),
    title,
    subtitle,
    blocks,
    updatedAt: new Date().toISOString(),
    extraJs: extraJs || undefined,
  };

  return { lesson, note: summarize(flags) };
}

function collectScripts(doc: Document, flags: Flags): string {
  const chunks: string[] = [];
  doc.querySelectorAll("script").forEach((script) => {
    const src = script.getAttribute("src");
    const body = (script.textContent || "").trim();
    if (src) {
      flags.capturedJs = true;
      chunks.push(`/* external script not loaded in the editor: ${src} */`);
      return;
    }
    if (!body) return;
    if (isLuminaPlayer(body)) return;
    flags.capturedJs = true;
    chunks.push(body);
  });
  return chunks.join("\n\n");
}

function isLuminaPlayer(code: string) {
  return code.includes("querySelectorAll") && code.includes(".quiz") && code.includes("data-correct");
}

function pickRoot(doc: Document): HTMLElement {
  return (
    (doc.querySelector("article.lesson-shell, .lesson-shell, article, main") as HTMLElement | null) ||
    doc.body
  );
}

function filenameToTitle(filename?: string) {
  if (!filename) return "";
  return filename.replace(/\.(html?|htm)$/i, "").replace(/[-_]+/g, " ").trim();
}

function childNodesToBlocks(parent: Element, flags: Flags, skip: Set<Element>): Block[] {
  const out: Block[] = [];
  let textBuf = "";
  const flush = () => {
    const text = textBuf.replace(/\s+/g, " ").trim();
    textBuf = "";
    if (text) out.push({ id: nid(), type: "paragraph", text });
  };

  Array.from(parent.childNodes).forEach((node) => {
    if (node.nodeType === Node.TEXT_NODE) {
      textBuf += node.textContent || "";
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return;
    const el = node as HTMLElement;
    if (skip.has(el) || SKIP_TAGS.has(el.tagName)) return;
    flush();
    out.push(...elementToBlocks(el, flags, skip));
  });
  flush();
  return out;
}

function elementToBlocks(el: HTMLElement, flags: Flags, skip: Set<Element>): Block[] {
  const tag = el.tagName;
  if (SKIP_TAGS.has(tag) || skip.has(el)) return [];
  const style = readStyle(el);

  if (/^H[1-6]$/.test(tag)) {
    const level = Math.min(3, Math.max(1, Number(tag.slice(1)))) as 1 | 2 | 3;
    const align = style?.align || "left";
    return [{ id: nid(), type: "heading", level, text: visibleText(el), align, style }];
  }

  if (tag === "P") {
    const onlyLink = loneLink(el);
    if (onlyLink && looksLikeButton(onlyLink, el)) {
      return [linkToButton(onlyLink, style)];
    }
    if (hasMeaningfulInline(el)) {
      flags.usedHtmlFallback = true;
      return [{ id: nid(), type: "html", html: sanitizeHtml(el.outerHTML), style }];
    }
    const text = visibleText(el);
    return text ? [{ id: nid(), type: "paragraph", text, style }] : [];
  }

  if (tag === "IMG") {
    return [imageFrom(el, style)];
  }

  if (tag === "FIGURE") {
    const img = el.querySelector("img");
    const caption = el.querySelector("figcaption")?.textContent?.trim() || "";
    if (img) {
      const block = imageFrom(img, style);
      return [{ ...block, caption: caption || block.caption }];
    }
  }

  if (tag === "UL" || tag === "OL") {
    const items = Array.from(el.querySelectorAll(":scope > li")).map((li) => visibleText(li));
    return [{ id: nid(), type: "list", ordered: tag === "OL", items, style }];
  }

  if (tag === "IFRAME" || tag === "VIDEO" || tag === "EMBED") {
    return [videoFrom(el, style)];
  }

  if (tag === "A" && looksLikeButton(el, el)) {
    return [linkToButton(el, style)];
  }

  if (isQuiz(el)) {
    return [quizFrom(el, style)];
  }

  if (isCallout(el)) {
    return [calloutFrom(el, style)];
  }

  if (isTwoColumn(el)) {
    flags.skippedLayout = true;
    return [columnsFrom(el, flags, skip, style)];
  }

  if (WRAPPER_TAGS.has(tag) || tag === "CENTER") {
    const kids = childNodesToBlocks(el, flags, skip);
    if (kids.length) {
      if (style && kids.length === 1) {
        kids[0] = { ...kids[0], style: mergeStyle(kids[0].style, style) };
      }
      return kids;
    }
    const text = visibleText(el);
    if (text) return [{ id: nid(), type: "paragraph", text, style }];
    return [];
  }

  flags.usedHtmlFallback = true;
  const html = sanitizeHtml(el.outerHTML);
  if (!html.trim()) {
    const text = visibleText(el);
    return text ? [{ id: nid(), type: "paragraph", text, style }] : [];
  }
  return [{ id: nid(), type: "html", html, style }];
}

function readStyle(el: HTMLElement): BlockStyle | undefined {
  const s = el.style;
  const classAlign =
    parseAlign(
      Array.from(el.classList)
        .map((name) => name.replace(/^align-/, "").replace(/^text-/, ""))
        .find((name) => name === "left" || name === "center" || name === "right"),
    ) || parseAlign(s.textAlign);
  const margin = [s.margin, s.marginTop, s.marginBottom].filter(Boolean).join(" ").trim();
  const style: BlockStyle = {};
  if (s.color) style.color = s.color;
  if (s.fontSize) style.fontSize = s.fontSize;
  if (classAlign) style.align = classAlign;
  if (margin) style.margin = s.margin || margin;
  return Object.keys(style).length ? style : undefined;
}

function mergeStyle(a?: BlockStyle, b?: BlockStyle): BlockStyle | undefined {
  if (!a) return b;
  if (!b) return a;
  return { ...b, ...a };
}

function visibleText(el: Element): string {
  const clone = el.cloneNode(true) as HTMLElement;
  clone.querySelectorAll("br").forEach((br) => br.replaceWith("\n"));
  return (clone.textContent || "").replace(/\r/g, "").replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
}

function hasMeaningfulInline(el: HTMLElement) {
  return Array.from(el.children).some((child) => child.tagName !== "BR");
}

function loneLink(el: HTMLElement): HTMLAnchorElement | null {
  const links = el.querySelectorAll("a");
  if (links.length !== 1) return null;
  const text = visibleText(el);
  const linkText = visibleText(links[0]);
  return text === linkText ? (links[0] as HTMLAnchorElement) : null;
}

/** SVG `className` is SVGAnimatedString, not a string — never call string methods on it. */
function classAttr(el: Element): string {
  return (el.getAttribute("class") || "").toLowerCase();
}

function looksLikeButton(el: HTMLElement, host?: HTMLElement) {
  const cls = `${classAttr(el)} ${host ? classAttr(host) : ""}`;
  if (/(btn|button|cta|pill)/.test(cls)) return true;
  if (el.tagName === "A" && el.getAttribute("role") === "button") return true;
  return false;
}

function linkToButton(el: HTMLAnchorElement | HTMLElement, style?: BlockStyle): Block {
  const href = el.getAttribute("href") || "#";
  const variant = /secondary|ghost|outline/.test(classAttr(el)) ? "secondary" : "primary";
  return {
    id: nid(),
    type: "button",
    label: visibleText(el) || "Link",
    href,
    variant,
    style,
  };
}

function imageFrom(el: Element, style?: BlockStyle): ImageBlock {
  return {
    id: nid(),
    type: "image",
    src: el.getAttribute("src") || "",
    alt: el.getAttribute("alt") || "",
    caption: el.getAttribute("title") || "",
    style,
  };
}

function videoFrom(el: HTMLElement, style?: BlockStyle): Block {
  const src = el.getAttribute("src") || el.querySelector("source")?.getAttribute("src") || "";
  const title = el.getAttribute("title") || visibleText(el) || "Video";
  return {
    id: nid(),
    type: "video",
    title: title.slice(0, 120) || "Video",
    duration: "",
    note: src ? `Source: ${src}` : visibleText(el) || "Imported media placeholder.",
    style,
  };
}

function isQuiz(el: HTMLElement) {
  if (el.classList?.contains("quiz") || el.getAttribute("data-correct") != null) return true;
  return /quiz|mcq|multiple-choice/.test(classAttr(el));
}

function quizFrom(el: HTMLElement, style?: BlockStyle): Block {
  const questionEl = el.querySelector(".q, .question, [data-question]");
  const question = visibleText(questionEl || el.querySelector("p, h3, h4") || el).split("\n")[0] || "Question";
  const optionEls = Array.from(el.querySelectorAll(".opt, button.opt, li"));
  let options = optionEls
    .map((node) => visibleText(node))
    .filter((text, index, all) => text && text !== question && all.indexOf(text) === index);
  if (options.length < 2) {
    options = visibleText(el)
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line && line !== question);
  }
  const correctAttr = Number(el.getAttribute("data-correct"));
  const marked = optionEls.findIndex((node) => node.classList.contains("correct"));
  const correctIndex = Number.isFinite(correctAttr) && !Number.isNaN(correctAttr) ? correctAttr : Math.max(0, marked);
  const explainEl = el.querySelector(".explain, .feedback, .rationale");
  return {
    id: nid(),
    type: "quiz",
    question,
    options: options.slice(0, 8).length ? options.slice(0, 8) : ["Option A", "Option B"],
    correctIndex: Math.min(Math.max(0, correctIndex), Math.max(0, (options.length || 1) - 1)),
    explanation: explainEl ? visibleText(explainEl) : "",
    style,
  };
}

function isCallout(el: HTMLElement) {
  if (el.tagName === "ASIDE" || el.tagName === "BLOCKQUOTE") return true;
  return /callout|alert|tip|note|warning|success|notice|info-box|admonition/.test(classAttr(el));
}

function calloutFrom(el: HTMLElement, style?: BlockStyle): Block {
  const cls = classAttr(el);
  let tone: CalloutTone = "info";
  if (/warn|caution|alert/.test(cls)) tone = "warning";
  else if (/tip|hint/.test(cls)) tone = "tip";
  else if (/success|ok|done/.test(cls)) tone = "success";
  const heading = el.querySelector("h1,h2,h3,h4,h5,h6,strong");
  const title = heading ? visibleText(heading) : "Note";
  const bodyEl = el.cloneNode(true) as HTMLElement;
  bodyEl.querySelectorAll("h1,h2,h3,h4,h5,h6").forEach((node) => node.remove());
  const body = visibleText(bodyEl) || visibleText(el);
  return { id: nid(), type: "callout", tone, title, body: body === title ? "" : body, style };
}

function isTwoColumn(el: HTMLElement) {
  if (el.classList?.contains("columns")) return true;
  if (/two-?col|split-?col|side-?by-?side/.test(classAttr(el))) return true;
  const kids = Array.from(el.children);
  if (el.tagName === "TABLE") {
    const cells = el.querySelector("tr")?.children;
    return !!cells && cells.length === 2;
  }
  const style = (el.getAttribute("style") || "").toLowerCase();
  if (kids.length === 2 && (/display:\s*grid/.test(style) || /display:\s*flex/.test(style))) return true;
  if (kids.length === 2 && kids.every((kid) => /(^|\s)col(umn)?s?\b/.test(classAttr(kid)))) return true;
  return false;
}

function columnsFrom(el: HTMLElement, flags: Flags, skip: Set<Element>, style?: BlockStyle): Block {
  let leftHost: Element;
  let rightHost: Element;
  if (el.tagName === "TABLE") {
    const cells = Array.from(el.querySelector("tr")?.children || []);
    leftHost = cells[0] || el;
    rightHost = cells[1] || el;
  } else {
    const kids = Array.from(el.children);
    leftHost = kids[0] || el;
    rightHost = kids[1] || el;
  }
  return {
    id: nid(),
    type: "columns",
    left: childNodesToBlocks(leftHost, flags, skip),
    right: childNodesToBlocks(rightHost, flags, skip),
    style,
  };
}

function sanitizeHtml(html: string): string {
  const parsed = new DOMParser().parseFromString(`<div id="lumina-wrap">${html}</div>`, "text/html");
  const wrap = parsed.querySelector("#lumina-wrap");
  if (!wrap) return "";
  sanitizeNode(wrap);
  return wrap.innerHTML.trim();
}

function sanitizeNode(root: Element) {
  const visit = (node: Node) => {
    if (node.nodeType !== Node.ELEMENT_NODE) return;
    const el = node as HTMLElement;
    if (SKIP_TAGS.has(el.tagName) || el.tagName === "IFRAME" || el.tagName === "OBJECT" || el.tagName === "EMBED") {
      el.remove();
      return;
    }
    if (!ALLOWED_HTML.has(el.tagName) && el !== root) {
      const parent = el.parentNode;
      if (parent) {
        while (el.firstChild) parent.insertBefore(el.firstChild, el);
        parent.removeChild(el);
      }
      return;
    }
    Array.from(el.attributes).forEach((attr) => {
      const name = attr.name.toLowerCase();
      if (name.startsWith("on") || name === "srcdoc") {
        el.removeAttribute(attr.name);
        return;
      }
      if (name === "href" || name === "src") {
        const value = attr.value.trim();
        if (/^javascript:/i.test(value) || /^vbscript:/i.test(value)) el.removeAttribute(attr.name);
      }
    });
    Array.from(el.childNodes).forEach(visit);
  };
  Array.from(root.childNodes).forEach(visit);
}

function summarize(flags: Flags): string | undefined {
  const bits: string[] = [];
  if (flags.skippedLayout) bits.push("some layout was simplified");
  if (flags.skippedCss) bits.push("stylesheet rules were skipped; inline color, size, alignment, and spacing were kept");
  if (flags.usedHtmlFallback) bits.push("unfamiliar markup was kept as HTML blocks so nothing is lost");
  if (flags.capturedJs) bits.push("scripts were stored in Extra JS and do not run in the editor");
  if (!bits.length) return undefined;
  return `${bits.join(". ")}.`;
}

export function isAlign(value: string): value is Align {
  return value === "left" || value === "center" || value === "right";
}
