"use client";

import type { Block } from "@/lib/types";

function ImagePreview({ src, alt }: { src: string; alt: string }) {
  if (!src) return <div className="img-ph">Image placeholder — add a URL in Properties</div>;
  return <img src={src} alt={alt} />;
}

export function BlockPreview({ block }: { block: Block }) {
  switch (block.type) {
    case "heading": {
      const Tag = (`h${block.level}` as "h1" | "h2" | "h3");
      return <Tag className={`block align-${block.align}`}>{block.text}</Tag>;
    }
    case "paragraph":
      return <p className="block">{block.text}</p>;
    case "image":
      return (
        <figure className="figure">
          <ImagePreview src={block.src} alt={block.alt} />
          {block.caption ? <div className="caption">{block.caption}</div> : null}
        </figure>
      );
    case "button":
      return (
        <p className="block">
          <span className={`btn btn-${block.variant}`}>{block.label}</span>
        </p>
      );
    case "list": {
      const Tag = block.ordered ? "ol" : "ul";
      return (
        <Tag className="list">
          {block.items.map((item, index) => (
            <li key={`${block.id}-${index}`}>{item}</li>
          ))}
        </Tag>
      );
    }
    case "callout":
      return (
        <aside className={`callout callout-${block.tone}`}>
          <h4>{block.title}</h4>
          <p>{block.body}</p>
        </aside>
      );
    case "columns":
      return (
        <div className="columns">
          <div className="col">
            {block.left.map((child) => (
              <BlockPreview key={child.id} block={child} />
            ))}
          </div>
          <div className="col">
            {block.right.map((child) => (
              <BlockPreview key={child.id} block={child} />
            ))}
          </div>
        </div>
      );
    case "video":
      return (
        <div className="video">
          <div>
            <div className="play">▶</div>
            <div>{block.title}</div>
            <div className="dur">{block.duration}</div>
            <p>{block.note}</p>
          </div>
        </div>
      );
    case "quiz":
      return (
        <div className="quiz">
          <p className="q">{block.question}</p>
          {block.options.map((option, index) => (
            <div key={`${block.id}-o${index}`} className={`opt ${index === block.correctIndex ? "correct" : ""}`}>
              {option}
              {index === block.correctIndex ? "  ✓" : ""}
            </div>
          ))}
        </div>
      );
  }
}

export function BlockCard({
  block,
  selected,
  onSelect,
  onDrop,
}: {
  block: Block;
  selected: boolean;
  onSelect: (id: string) => void;
  onDrop: (targetId: string, data: DataTransfer) => void;
}) {
  return (
    <div
      className={`block-card ${selected ? "is-selected" : ""}`}
      onClick={(event) => {
        event.stopPropagation();
        onSelect(block.id);
      }}
      draggable
      onDragStart={(event) => {
        event.dataTransfer.setData("application/lumina-move", block.id);
        event.dataTransfer.effectAllowed = "move";
      }}
      onDragOver={(event) => {
        event.preventDefault();
      }}
      onDrop={(event) => {
        event.preventDefault();
        event.stopPropagation();
        onDrop(block.id, event.dataTransfer);
      }}
    >
      <div className="block-meta">
        <span>{block.type}</span>
        <span className="grip">⠿</span>
      </div>
      <BlockPreview block={block} />
    </div>
  );
}
