export type BlockType =
  | "heading"
  | "paragraph"
  | "image"
  | "button"
  | "list"
  | "callout"
  | "columns"
  | "video"
  | "quiz";

export type Align = "left" | "center" | "right";

export type CalloutTone = "info" | "tip" | "warning" | "success";

export type HeadingBlock = {
  id: string;
  type: "heading";
  level: 1 | 2 | 3;
  text: string;
  align: Align;
};

export type ParagraphBlock = {
  id: string;
  type: "paragraph";
  text: string;
};

export type ImageBlock = {
  id: string;
  type: "image";
  src: string;
  alt: string;
  caption: string;
};

export type ButtonBlock = {
  id: string;
  type: "button";
  label: string;
  href: string;
  variant: "primary" | "secondary";
};

export type ListBlock = {
  id: string;
  type: "list";
  ordered: boolean;
  items: string[];
};

export type CalloutBlock = {
  id: string;
  type: "callout";
  tone: CalloutTone;
  title: string;
  body: string;
};

export type ColumnsBlock = {
  id: string;
  type: "columns";
  left: Block[];
  right: Block[];
};

export type VideoBlock = {
  id: string;
  type: "video";
  title: string;
  duration: string;
  note: string;
};

export type QuizBlock = {
  id: string;
  type: "quiz";
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
};

export type Block =
  | HeadingBlock
  | ParagraphBlock
  | ImageBlock
  | ButtonBlock
  | ListBlock
  | CalloutBlock
  | ColumnsBlock
  | VideoBlock
  | QuizBlock;

export type Lesson = {
  id: string;
  title: string;
  subtitle: string;
  blocks: Block[];
  updatedAt: string;
};

export const NESTABLE_TYPES: BlockType[] = [
  "heading",
  "paragraph",
  "image",
  "button",
  "list",
  "callout",
  "video",
  "quiz",
];

export const PALETTE: { type: BlockType; label: string; hint: string }[] = [
  { type: "heading", label: "Heading", hint: "H1–H3 title" },
  { type: "paragraph", label: "Paragraph", hint: "Body copy" },
  { type: "image", label: "Image", hint: "URL + caption" },
  { type: "button", label: "Button", hint: "Link action" },
  { type: "list", label: "List", hint: "Bullets or numbers" },
  { type: "callout", label: "Callout", hint: "Tip, warning, info" },
  { type: "columns", label: "Two-column", hint: "Side-by-side blocks" },
  { type: "video", label: "Video", hint: "Placeholder stage" },
  { type: "quiz", label: "Quiz (MCQ)", hint: "One correct answer" },
];
