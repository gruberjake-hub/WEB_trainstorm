"use client";

import { PALETTE, type BlockType } from "@/lib/types";

const ICONS: Record<BlockType, string> = {
  heading: "H",
  paragraph: "¶",
  image: "▣",
  button: "◉",
  list: "≡",
  callout: "!",
  columns: "⧉",
  video: "▶",
  quiz: "?",
  html: "</>",
};

export function Palette({
  onAdd,
  nestOnly = false,
}: {
  onAdd: (type: BlockType) => void;
  nestOnly?: boolean;
}) {
  const items = nestOnly ? PALETTE.filter((item) => item.type !== "columns") : PALETTE;

  return (
    <div className="palette">
      <div className="pane-label">Blocks</div>
      {items.map((item) => (
        <button
          key={item.type}
          type="button"
          className="palette-item"
          draggable
          onDragStart={(event) => {
            event.dataTransfer.setData("application/lumina-block", item.type);
            event.dataTransfer.effectAllowed = "copy";
          }}
          onClick={() => onAdd(item.type)}
        >
          <span className="palette-icon">{ICONS[item.type]}</span>
          <span>
            <strong>{item.label}</strong>
            <em>{item.hint}</em>
          </span>
        </button>
      ))}
      <p className="palette-help">Click to add after the selection, or drag onto the canvas.</p>
    </div>
  );
}
