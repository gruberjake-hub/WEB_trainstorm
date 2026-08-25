"use client";

import { BlockCard } from "./BlockCard";
import type { Block } from "@/lib/types";

export function Canvas({
  blocks,
  selectedId,
  onSelect,
  onDrop,
}: {
  blocks: Block[];
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  onDrop: (targetId: string | null, data: DataTransfer) => void;
}) {
  return (
    <div
      className="canvas"
      onClick={() => onSelect(null)}
      onDragOver={(event) => event.preventDefault()}
      onDrop={(event) => {
        event.preventDefault();
        onDrop(null, event.dataTransfer);
      }}
    >
      <div className="lesson-shell canvas-page">
        {blocks.length === 0 ? (
          <div className="empty">Add a block from the left to start the lesson.</div>
        ) : (
          blocks.map((block) => (
            <BlockCard
              key={block.id}
              block={block}
              selected={selectedId === block.id}
              onSelect={onSelect}
              onDrop={onDrop}
            />
          ))
        )}
      </div>
    </div>
  );
}
