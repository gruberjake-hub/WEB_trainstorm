export type BlockType =
  | "heading"
  | "paragraph"
  | "image"
  | "button"
  | "list"
  | "callout"
  | "columns"
  | "video"
  | "quiz"
  | "html";

export type Align = "left" | "center" | "right";

export type CalloutTone = "info" | "tip" | "warning" | "success";

export type BlockStyle = {
  color?: string;
  fontSize?: string;
  align?: Align;
  margin?: string;
};

export type HeadingBlock = {
  id: string;
  type: "heading";
  level: 1 | 2 | 3;
  text: string;
  align: Align;
  style?: BlockStyle;
};

export type ParagraphBlock = {
  id: string;
  type: "paragraph";
  text: string;
  style?: BlockStyle;
};

export type ImageBlock = {
  id: string;
  type: "image";
  src: string;
  alt: string;
  caption: string;
  style?: BlockStyle;
};

export type ButtonBlock = {
  id: string;
  type: "button";
  label: string;
  href: string;
  variant: "primary" | "secondary";
  style?: BlockStyle;
};

export type ListBlock = {
  id: string;
  type: "list";
  ordered: boolean;
  items: string[];
  style?: BlockStyle;
};

export type CalloutBlock = {
  id: string;
  type: "callout";
  tone: CalloutTone;
  title: string;
  body: string;
  style?: BlockStyle;
};

export type ColumnsBlock = {
  id: string;
  type: "columns";
  left: Block[];
  right: Block[];
  style?: BlockStyle;
};

export type VideoBlock = {
  id: string;
  type: "video";
  title: string;
  duration: string;
  note: string;
  style?: BlockStyle;
};

export type QuizBlock = {
  id: string;
  type: "quiz";
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  style?: BlockStyle;
};

export type HtmlBlock = {
  id: string;
  type: "html";
  html: string;
  style?: BlockStyle;
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
  | QuizBlock
  | HtmlBlock;

export type Lesson = {
  id: string;
  title: string;
  subtitle: string;
  blocks: Block[];
  updatedAt: string;
  extraJs?: string;
};

export type ProjectMeta = {
  id: string;
  title: string;
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
  "html",
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
  { type: "html", label: "HTML", hint: "Kept markup" },
];
