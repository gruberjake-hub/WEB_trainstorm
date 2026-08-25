"use client";

import type { CSSProperties } from "react";
import { reactStyle } from "@/lib/style";
import type { Block } from "@/lib/types";

function ImagePreview({ src, alt }: { src: string; alt: string }) {
  if (!src) return <div className="img-ph">Image placeholder — add a URL in Properties</div>;
  return <img src={src} alt={alt} />;
}

function withStyle(style: CSSProperties | undefined, className: string) {
  return { className, style };
}

export function BlockPreview({ block }: { block: Block }) {
  const style = reactStyle(block.style);
  switch (block.type) {
    case "heading": {
      const Tag = (`h${block.level}` as "h1" | "h2" | "h3");
      return <Tag {...withStyle(style, `block align-${block.style?.align || block.align}`)}>{block.text}</Tag>;
    }
    case "paragraph":
      return <p {...withStyle(style, "block")}>{block.text}</p>;
    case "image":
      return (
        <figure {...withStyle(style, "figure")}>
          <ImagePreview src={block.src} alt={block.alt} />
          {block.caption ? <div className="caption">{block.caption}</div> : null}
        </figure>
      );
    case "button":
      return (
        <p {...withStyle(style, "block")}>
          <span className={`btn btn-${block.variant}`}>{block.label}</span>
        </p>
      );
    case "list": {
      const Tag = block.ordered ? "ol" : "ul";
      return (
        <Tag {...withStyle(style, "list")}>
          {block.items.map((item, index) => (
            <li key={`${block.id}-${index}`}>{item}</li>
          ))}
        </Tag>
      );
    }
    case "callout":
      return (
        <aside {...withStyle(style, `callout callout-${block.tone}`)}>
          <h4>{block.title}</h4>
          <p>{block.body}</p>
        </aside>
      );
    case "columns":
      return (
        <div {...withStyle(style, "columns")}>
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
        <div {...withStyle(style, "video")}>
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
        <div {...withStyle(style, "quiz")}>
          <p className="q">{block.question}</p>
          {block.options.map((option, index) => (
            <div key={`${block.id}-o${index}`} className={`opt ${index === block.correctIndex ? "correct" : ""}`}>
              {option}
              {index === block.correctIndex ? "  ✓" : ""}
            </div>
          ))}
        </div>
      );
    case "html":
      return (
        <div
          {...withStyle(style, "html-block")}
          dangerouslySetInnerHTML={{ __html: block.html }}
        />
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
