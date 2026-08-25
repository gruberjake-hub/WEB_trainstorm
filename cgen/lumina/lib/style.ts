import type { CSSProperties } from "react";
import type { Align, BlockStyle } from "./types";

export function cssString(style?: BlockStyle): string {
  if (!style) return "";
  const parts: string[] = [];
  if (style.color) parts.push(`color: ${style.color}`);
  if (style.fontSize) parts.push(`font-size: ${style.fontSize}`);
  if (style.align) parts.push(`text-align: ${style.align}`);
  if (style.margin) parts.push(`margin: ${style.margin}`);
  return parts.join("; ");
}

export function reactStyle(style?: BlockStyle): CSSProperties {
  return {
    color: style?.color,
    fontSize: style?.fontSize,
    textAlign: style?.align,
    margin: style?.margin,
  };
}

export function applyInlineStyle(html: string, style?: BlockStyle): string {
  const css = cssString(style);
  if (!css) return html;
  return html.replace(/^<([a-zA-Z0-9]+)([^>]*)>/, (_match, tag: string, rest: string) => {
    if (/\sstyle\s*=/.test(rest)) {
      return `<${tag}${rest.replace(/style\s*=\s*"([^"]*)"/, (_s, existing: string) => `style="${existing}; ${css}"`)}>`;
    }
    return `<${tag}${rest} style="${css.replace(/"/g, "&quot;")}">`;
  });
}

export function parseAlign(value: string | undefined): Align | undefined {
  const v = (value || "").trim().toLowerCase();
  if (v === "left" || v === "center" || v === "right") return v;
  if (v === "start") return "left";
  if (v === "end") return "right";
  return undefined;
}
