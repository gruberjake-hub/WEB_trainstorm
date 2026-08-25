import JSZip from "jszip";
import { applyInlineStyle } from "./style";
import type { Block, Lesson } from "./types";

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function textToHtml(value: string): string {
  return escapeHtml(value).replace(/\n/g, "<br />");
}

export const LESSON_CSS = `* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
  color: #241f1a;
  background: #efe7d8;
  line-height: 1.55;
}
.lesson-shell {
  max-width: 760px;
  margin: 0 auto;
  padding: 48px 24px 80px;
}
.lesson-kicker {
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  font-size: 11px;
  color: #8a6a3b;
  margin: 0 0 10px;
}
.lesson-title {
  font-size: 42px;
  line-height: 1.15;
  margin: 0 0 12px;
  font-weight: 600;
}
.lesson-sub {
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  font-size: 18px;
  color: #5c5346;
  margin: 0 0 36px;
}
.block { margin: 0 0 22px; }
h1.block, h2.block, h3.block { margin: 28px 0 12px; line-height: 1.2; }
h1.block { font-size: 36px; }
h2.block { font-size: 26px; }
h3.block { font-size: 20px; }
p.block { font-size: 18px; }
.align-left { text-align: left; }
.align-center { text-align: center; }
.align-right { text-align: right; }
.figure { margin: 0 0 22px; }
.figure img {
  display: block;
  width: 100%;
  border-radius: 16px;
  background: #e4d9c6;
  min-height: 160px;
  object-fit: cover;
}
.img-ph {
  display: grid;
  place-items: center;
  min-height: 180px;
  border-radius: 16px;
  background: repeating-linear-gradient(-45deg, #e8dcc8, #e8dcc8 12px, #f0e6d4 12px, #f0e6d4 24px);
  color: #7a6c59;
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  font-size: 14px;
}
.caption {
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  font-size: 13px;
  color: #6b6256;
  margin: 8px 2px 0;
}
.btn {
  display: inline-block;
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  text-decoration: none;
  border-radius: 999px;
  padding: 12px 20px;
  font-weight: 650;
  font-size: 15px;
}
.btn-primary { background: #1f4d45; color: #f4efe4; }
.btn-secondary { background: transparent; color: #1f4d45; box-shadow: inset 0 0 0 1.5px #1f4d45; }
.list { padding-left: 1.2em; margin: 0 0 22px; font-size: 18px; }
.list li { margin: 0 0 8px; }
.callout {
  border-radius: 16px;
  padding: 16px 18px;
  margin: 0 0 22px;
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
}
.callout h4 { margin: 0 0 6px; font-size: 14px; letter-spacing: 0.04em; text-transform: uppercase; }
.callout p { margin: 0; font-size: 16px; }
.callout-info { background: #e4eef2; }
.callout-tip { background: #ece6d3; }
.callout-warning { background: #f3ddd0; }
.callout-success { background: #dce8e2; }
.columns { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin: 0 0 22px; }
.col { background: rgba(255,255,255,0.35); border-radius: 16px; padding: 8px 16px 4px; }
.video {
  background: #241f1a;
  color: #f4efe4;
  border-radius: 18px;
  min-height: 220px;
  display: grid;
  place-items: center;
  text-align: center;
  padding: 28px;
  margin: 0 0 22px;
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
}
.video .play {
  width: 64px; height: 64px; border-radius: 50%;
  background: #c46b3a; display: grid; place-items: center; margin: 0 auto 14px;
  font-size: 22px;
}
.video .dur { opacity: 0.7; font-size: 13px; margin-top: 8px; }
.quiz {
  background: #fffaf2;
  border-radius: 18px;
  padding: 20px;
  margin: 0 0 22px;
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
}
.quiz .q { font-family: Georgia, serif; font-size: 20px; margin: 0 0 14px; }
.opt {
  display: block; width: 100%; text-align: left;
  background: #fff; border: 1px solid #d9cdb8; border-radius: 12px;
  padding: 10px 12px; margin: 0 0 8px; font: inherit; cursor: pointer;
}
.opt:hover { border-color: #1f4d45; }
.opt.correct { background: #dce8e2; border-color: #1f4d45; }
.opt.wrong { background: #f3ddd0; border-color: #c46b3a; }
.explain { display: none; margin-top: 10px; color: #5c5346; }
.explain.show { display: block; }
.html-block { margin: 0 0 22px; }
@media (max-width: 700px) {
  .columns { grid-template-columns: 1fr; }
  .lesson-title { font-size: 32px; }
}`;

function renderBlock(block: Block): string {
  let html = "";
  switch (block.type) {
    case "heading": {
      const tag = `h${block.level}`;
      html = `<${tag} class="block align-${block.align}">${textToHtml(block.text)}</${tag}>`;
      break;
    }
    case "paragraph":
      html = `<p class="block">${textToHtml(block.text)}</p>`;
      break;
    case "image": {
      const img = block.src
        ? `<img src="${escapeHtml(block.src)}" alt="${escapeHtml(block.alt)}" />`
        : `<div class="img-ph">Image placeholder</div>`;
      const cap = block.caption ? `<div class="caption">${textToHtml(block.caption)}</div>` : "";
      html = `<figure class="figure">${img}${cap}</figure>`;
      break;
    }
    case "button":
      html = `<p class="block"><a class="btn btn-${block.variant}" href="${escapeHtml(block.href)}">${textToHtml(block.label)}</a></p>`;
      break;
    case "list": {
      const tag = block.ordered ? "ol" : "ul";
      const items = block.items.map((item) => `<li>${textToHtml(item)}</li>`).join("");
      html = `<${tag} class="list">${items}</${tag}>`;
      break;
    }
    case "callout":
      html = `<aside class="callout callout-${block.tone}"><h4>${textToHtml(block.title)}</h4><p>${textToHtml(block.body)}</p></aside>`;
      break;
    case "columns":
      html = `<div class="columns"><div class="col">${block.left.map(renderBlock).join("")}</div><div class="col">${block.right.map(renderBlock).join("")}</div></div>`;
      break;
    case "video":
      html = `<div class="video"><div><div class="play">▶</div><div>${textToHtml(block.title)}</div><div class="dur">${textToHtml(block.duration)}</div><p>${textToHtml(block.note)}</p></div></div>`;
      break;
    case "quiz": {
      const options = block.options
        .map((option, index) => `<button type="button" class="opt" data-index="${index}">${textToHtml(option)}</button>`)
        .join("");
      html = `<div class="quiz" data-correct="${block.correctIndex}"><p class="q">${textToHtml(block.question)}</p>${options}<div class="explain">${textToHtml(block.explanation)}</div></div>`;
      break;
    }
    case "html":
      html = `<div class="html-block">${block.html}</div>`;
      break;
  }
  return applyInlineStyle(html, block.style);
}

const PLAYER_JS = `document.querySelectorAll(".quiz").forEach(function (quiz) {
  var correct = Number(quiz.getAttribute("data-correct"));
  quiz.querySelectorAll(".opt").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (quiz.classList.contains("done")) return;
      quiz.classList.add("done");
      var index = Number(btn.getAttribute("data-index"));
      quiz.querySelectorAll(".opt").forEach(function (other, i) {
        if (i === correct) other.classList.add("correct");
      });
      if (index !== correct) btn.classList.add("wrong");
      var explain = quiz.querySelector(".explain");
      if (explain) explain.classList.add("show");
    });
  });
});`;

export function lessonInnerHtml(lesson: Lesson): string {
  return lesson.blocks.map(renderBlock).join("\n");
}

export function lessonDocument(lesson: Lesson): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${escapeHtml(lesson.title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:wght@500;600&display=swap" />
  <style>${LESSON_CSS}</style>
</head>
<body>
  <article class="lesson-shell">
    <p class="lesson-kicker">Lumina lesson</p>
    <h1 class="lesson-title">${textToHtml(lesson.title)}</h1>
    <p class="lesson-sub">${textToHtml(lesson.subtitle)}</p>
    ${lessonInnerHtml(lesson)}
  </article>
  <script>${PLAYER_JS}</script>
  ${lesson.extraJs ? `<script>\n${lesson.extraJs.replace(/<\/script/gi, "<\\/script")}\n</script>` : ""}
</body>
</html>`;
}

export function prettyHtml(html: string): string {
  const padded = html.replace(/></g, ">\n<");
  const lines = padded.split("\n");
  let depth = 0;
  return lines
    .map((line) => {
      const trimmed = line.trim();
      if (!trimmed) return "";
      if (/^<\//.test(trimmed)) depth = Math.max(0, depth - 1);
      const out = `${"  ".repeat(depth)}${trimmed}`;
      if (/^<[^/!][^>]*[^/]>$/.test(trimmed) && !/^<(br|img|meta|link|input|hr)\b/i.test(trimmed)) {
        depth += 1;
      }
      return out;
    })
    .join("\n");
}

function downloadBlob(filename: string, blob: Blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function slugify(value: string): string {
  return (
    value
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "")
      .slice(0, 60) || "lesson"
  );
}

export function exportHtmlFile(lesson: Lesson) {
  const html = lessonDocument(lesson);
  downloadBlob(`${slugify(lesson.title)}.html`, new Blob([html], { type: "text/html" }));
}

export async function exportZipFile(lesson: Lesson) {
  const zip = new JSZip();
  const slug = slugify(lesson.title);
  zip.file("index.html", lessonDocument(lesson));
  zip.file(
    "README.txt",
    `Lumina export: ${lesson.title}\n\nOpen index.html in a browser. The quiz is self-contained — no server required.\n`,
  );
  const blob = await zip.generateAsync({ type: "blob" });
  downloadBlob(`${slug}.zip`, blob);
}
