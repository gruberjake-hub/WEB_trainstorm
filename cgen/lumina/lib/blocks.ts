import { nid } from "./ids";
import type { Block, BlockType } from "./types";

export function createBlock(type: BlockType): Block {
  switch (type) {
    case "heading":
      return { id: nid(), type, level: 2, text: "New heading", align: "left" };
    case "paragraph":
      return {
        id: nid(),
        type,
        text: "Write the instructional copy here. Keep one idea per paragraph.",
      };
    case "image":
      return { id: nid(), type, src: "", alt: "", caption: "" };
    case "button":
      return {
        id: nid(),
        type,
        label: "Continue",
        href: "#",
        variant: "primary",
      };
    case "list":
      return {
        id: nid(),
        type,
        ordered: false,
        items: ["First point", "Second point", "Third point"],
      };
    case "callout":
      return {
        id: nid(),
        type,
        tone: "info",
        title: "Note",
        body: "A short teaching note the learner should not miss.",
      };
    case "columns":
      return {
        id: nid(),
        type,
        left: [
          {
            id: nid(),
            type: "heading",
            level: 3,
            text: "Left",
            align: "left",
          },
          {
            id: nid(),
            type: "paragraph",
            text: "Add supporting content in this column.",
          },
        ],
        right: [
          {
            id: nid(),
            type: "heading",
            level: 3,
            text: "Right",
            align: "left",
          },
          {
            id: nid(),
            type: "paragraph",
            text: "Pair a contrast, example, or job aid here.",
          },
        ],
      };
    case "video":
      return {
        id: nid(),
        type,
        title: "Lesson video",
        duration: "2:00",
        note: "Replace this placeholder with a hosted clip when you export.",
      };
    case "quiz":
      return {
        id: nid(),
        type,
        question: "Which option is correct?",
        options: ["Option A", "Option B", "Option C", "Option D"],
        correctIndex: 0,
        explanation: "Explain why the correct choice works on the job.",
      };
  }
}
