"use client";

import type { ReactNode } from "react";
import type {
  Align,
  Block,
  BlockType,
  ButtonBlock,
  CalloutBlock,
  CalloutTone,
  ColumnsBlock,
  HeadingBlock,
  ImageBlock,
  ListBlock,
  ParagraphBlock,
  QuizBlock,
  VideoBlock,
} from "@/lib/types";

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
    </label>
  );
}

export function PropertiesPanel({
  block,
  lessonTitle,
  lessonSubtitle,
  onLessonMeta,
  onChange,
  onAddNested,
}: {
  block: Block | null;
  lessonTitle: string;
  lessonSubtitle: string;
  onLessonMeta: (patch: { title?: string; subtitle?: string }) => void;
  onChange: (patch: Partial<Block>) => void;
  onAddNested: (side: "left" | "right", type: BlockType) => void;
}) {
  if (!block) {
    return (
      <div className="props">
        <div className="pane-label">Lesson</div>
        <Field label="Title">
          <input value={lessonTitle} onChange={(event) => onLessonMeta({ title: event.target.value })} />
        </Field>
        <Field label="Subtitle">
          <textarea
            rows={4}
            value={lessonSubtitle}
            onChange={(event) => onLessonMeta({ subtitle: event.target.value })}
          />
        </Field>
        <p className="palette-help">Select a block on the canvas to edit its properties.</p>
      </div>
    );
  }

  return (
    <div className="props">
      <div className="pane-label">Properties · {block.type}</div>
      {block.type === "heading" ? <HeadingFields block={block} onChange={onChange} /> : null}
      {block.type === "paragraph" ? <ParagraphFields block={block} onChange={onChange} /> : null}
      {block.type === "image" ? <ImageFields block={block} onChange={onChange} /> : null}
      {block.type === "button" ? <ButtonFields block={block} onChange={onChange} /> : null}
      {block.type === "list" ? <ListFields block={block} onChange={onChange} /> : null}
      {block.type === "callout" ? <CalloutFields block={block} onChange={onChange} /> : null}
      {block.type === "video" ? <VideoFields block={block} onChange={onChange} /> : null}
      {block.type === "quiz" ? <QuizFields block={block} onChange={onChange} /> : null}
      {block.type === "columns" ? <ColumnsFields block={block} onAddNested={onAddNested} /> : null}
    </div>
  );
}

function HeadingFields({
  block,
  onChange,
}: {
  block: HeadingBlock;
  onChange: (patch: Partial<HeadingBlock>) => void;
}) {
  return (
    <>
      <Field label="Level">
        <select
          value={block.level}
          onChange={(event) => onChange({ level: Number(event.target.value) as 1 | 2 | 3 })}
        >
          <option value={1}>H1</option>
          <option value={2}>H2</option>
          <option value={3}>H3</option>
        </select>
      </Field>
      <Field label="Align">
        <select value={block.align} onChange={(event) => onChange({ align: event.target.value as Align })}>
          <option value="left">Left</option>
          <option value="center">Center</option>
          <option value="right">Right</option>
        </select>
      </Field>
      <Field label="Text">
        <input value={block.text} onChange={(event) => onChange({ text: event.target.value })} />
      </Field>
    </>
  );
}

function ParagraphFields({
  block,
  onChange,
}: {
  block: ParagraphBlock;
  onChange: (patch: Partial<ParagraphBlock>) => void;
}) {
  return (
    <Field label="Text">
      <textarea rows={8} value={block.text} onChange={(event) => onChange({ text: event.target.value })} />
    </Field>
  );
}

function ImageFields({
  block,
  onChange,
}: {
  block: ImageBlock;
  onChange: (patch: Partial<ImageBlock>) => void;
}) {
  return (
    <>
      <Field label="Image URL">
        <input value={block.src} onChange={(event) => onChange({ src: event.target.value })} />
      </Field>
      <Field label="Alt text">
        <input value={block.alt} onChange={(event) => onChange({ alt: event.target.value })} />
      </Field>
      <Field label="Caption">
        <input value={block.caption} onChange={(event) => onChange({ caption: event.target.value })} />
      </Field>
    </>
  );
}

function ButtonFields({
  block,
  onChange,
}: {
  block: ButtonBlock;
  onChange: (patch: Partial<ButtonBlock>) => void;
}) {
  return (
    <>
      <Field label="Label">
        <input value={block.label} onChange={(event) => onChange({ label: event.target.value })} />
      </Field>
      <Field label="Link href">
        <input value={block.href} onChange={(event) => onChange({ href: event.target.value })} />
      </Field>
      <Field label="Style">
        <select
          value={block.variant}
          onChange={(event) => onChange({ variant: event.target.value as ButtonBlock["variant"] })}
        >
          <option value="primary">Primary</option>
          <option value="secondary">Secondary</option>
        </select>
      </Field>
    </>
  );
}

function ListFields({
  block,
  onChange,
}: {
  block: ListBlock;
  onChange: (patch: Partial<ListBlock>) => void;
}) {
  return (
    <>
      <Field label="Type">
        <select
          value={block.ordered ? "ol" : "ul"}
          onChange={(event) => onChange({ ordered: event.target.value === "ol" })}
        >
          <option value="ul">Bulleted</option>
          <option value="ol">Numbered</option>
        </select>
      </Field>
      <Field label="Items (one per line)">
        <textarea
          rows={8}
          value={block.items.join("\n")}
          onChange={(event) => onChange({ items: event.target.value.split("\n") })}
        />
      </Field>
    </>
  );
}

function CalloutFields({
  block,
  onChange,
}: {
  block: CalloutBlock;
  onChange: (patch: Partial<CalloutBlock>) => void;
}) {
  return (
    <>
      <Field label="Tone">
        <select
          value={block.tone}
          onChange={(event) => onChange({ tone: event.target.value as CalloutTone })}
        >
          <option value="info">Info</option>
          <option value="tip">Tip</option>
          <option value="warning">Warning</option>
          <option value="success">Success</option>
        </select>
      </Field>
      <Field label="Title">
        <input value={block.title} onChange={(event) => onChange({ title: event.target.value })} />
      </Field>
      <Field label="Body">
        <textarea rows={6} value={block.body} onChange={(event) => onChange({ body: event.target.value })} />
      </Field>
    </>
  );
}

function VideoFields({
  block,
  onChange,
}: {
  block: VideoBlock;
  onChange: (patch: Partial<VideoBlock>) => void;
}) {
  return (
    <>
      <Field label="Title">
        <input value={block.title} onChange={(event) => onChange({ title: event.target.value })} />
      </Field>
      <Field label="Duration">
        <input value={block.duration} onChange={(event) => onChange({ duration: event.target.value })} />
      </Field>
      <Field label="Note">
        <textarea rows={4} value={block.note} onChange={(event) => onChange({ note: event.target.value })} />
      </Field>
    </>
  );
}

function QuizFields({
  block,
  onChange,
}: {
  block: QuizBlock;
  onChange: (patch: Partial<QuizBlock>) => void;
}) {
  return (
    <>
      <Field label="Question">
        <textarea rows={3} value={block.question} onChange={(event) => onChange({ question: event.target.value })} />
      </Field>
      <Field label="Options (one per line)">
        <textarea
          rows={6}
          value={block.options.join("\n")}
          onChange={(event) => onChange({ options: event.target.value.split("\n") })}
        />
      </Field>
      <Field label="Correct option (1-based)">
        <input
          type="number"
          min={1}
          max={Math.max(1, block.options.length)}
          value={block.correctIndex + 1}
          onChange={(event) => onChange({ correctIndex: Math.max(0, Number(event.target.value) - 1) })}
        />
      </Field>
      <Field label="Explanation">
        <textarea
          rows={5}
          value={block.explanation}
          onChange={(event) => onChange({ explanation: event.target.value })}
        />
      </Field>
    </>
  );
}

function ColumnsFields({
  block,
  onAddNested,
}: {
  block: ColumnsBlock;
  onAddNested: (side: "left" | "right", type: BlockType) => void;
}) {
  const types: BlockType[] = ["heading", "paragraph", "list", "callout", "image", "button", "video", "quiz"];
  return (
    <>
      <p className="palette-help">
        Left has {block.left.length} block{block.left.length === 1 ? "" : "s"}; right has {block.right.length}. Nested
        two-column layouts are not allowed.
      </p>
      <Field label="Add to left">
        <select
          defaultValue=""
          onChange={(event) => {
            if (!event.target.value) return;
            onAddNested("left", event.target.value as BlockType);
            event.target.value = "";
          }}
        >
          <option value="">Choose a block…</option>
          {types.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </Field>
      <Field label="Add to right">
        <select
          defaultValue=""
          onChange={(event) => {
            if (!event.target.value) return;
            onAddNested("right", event.target.value as BlockType);
            event.target.value = "";
          }}
        >
          <option value="">Choose a block…</option>
          {types.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </Field>
      <p className="palette-help">Click a nested block on the canvas to edit it.</p>
    </>
  );
}
