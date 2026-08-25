import { nid } from "./ids";
import type { Lesson } from "./types";

const SBI_DIAGRAM = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="960" height="360" viewBox="0 0 960 360" fill="none">
  <rect width="960" height="360" rx="24" fill="#F4EFE4"/>
  <rect x="48" y="70" width="248" height="220" rx="20" fill="#1F4D45"/>
  <rect x="356" y="70" width="248" height="220" rx="20" fill="#C46B3A"/>
  <rect x="664" y="70" width="248" height="220" rx="20" fill="#2C6E8A"/>
  <text x="172" y="150" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#F4EFE4">Situation</text>
  <text x="172" y="186" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#D7E8E3">When and where</text>
  <text x="480" y="150" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#F4EFE4">Behavior</text>
  <text x="480" y="186" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#F8E2D4">What you observed</text>
  <text x="788" y="150" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#F4EFE4">Impact</text>
  <text x="788" y="186" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#D5E8F1">Why it mattered</text>
  <text x="480" y="44" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" fill="#5C5346">SBI — a sentence, not a speech</text>
</svg>`)}`;

export function starterLesson(): Lesson {
  return {
    id: nid("lesson"),
    title: "Giving constructive feedback",
    subtitle: "A short studio lesson for managers and peers who need to say the hard thing well.",
    updatedAt: new Date().toISOString(),
    blocks: [
      {
        id: nid(),
        type: "heading",
        level: 1,
        text: "Giving constructive feedback",
        align: "left",
      },
      {
        id: nid(),
        type: "paragraph",
        text: "Most people delay feedback because they do not want to sound harsh. The delay is what makes the conversation worse. This lesson gives you a small, repeatable shape for the words: name the moment, name the behavior, name the impact. Then stop talking long enough for the other person to respond.",
      },
      {
        id: nid(),
        type: "callout",
        tone: "info",
        title: "By the end of this lesson you will be able to",
        body: "Tell constructive feedback from vague criticism. Draft a Situation–Behavior–Impact (SBI) statement in one sitting. Choose a first sentence that keeps the conversation about the work, not the person.",
      },
      {
        id: nid(),
        type: "heading",
        level: 2,
        text: "Constructive is specific. Unhelpful is fog.",
        align: "left",
      },
      {
        id: nid(),
        type: "columns",
        left: [
          {
            id: nid(),
            type: "heading",
            level: 3,
            text: "Constructive",
            align: "left",
          },
          {
            id: nid(),
            type: "list",
            ordered: false,
            items: [
              "Tied to a moment the other person can remember",
              "Describes observable behavior",
              "Names the effect on the work, the client, or the team",
              "Leaves room for their account of what happened",
            ],
          },
        ],
        right: [
          {
            id: nid(),
            type: "heading",
            level: 3,
            text: "Unhelpful",
            align: "left",
          },
          {
            id: nid(),
            type: "list",
            ordered: false,
            items: [
              "Labels (“you’re careless”, “you’re not a team player”)",
              "Piles up weeks of grievances in one sitting",
              "Hides the request inside a compliment sandwich",
              "Uses “always” and “never”",
            ],
          },
        ],
      },
      {
        id: nid(),
        type: "heading",
        level: 2,
        text: "Use the SBI model",
        align: "left",
      },
      {
        id: nid(),
        type: "paragraph",
        text: "SBI is a sentence pattern, not a form. Write it down before you walk into the room. If you cannot fit it on a sticky note, you are still arguing with yourself.",
      },
      {
        id: nid(),
        type: "list",
        ordered: true,
        items: [
          "Situation — when and where it happened, in one clause.",
          "Behavior — what you saw or heard, without a motive attached.",
          "Impact — the consequence for the work, the client, a teammate, or the next step.",
        ],
      },
      {
        id: nid(),
        type: "image",
        src: SBI_DIAGRAM,
        alt: "Three panels labeled Situation, Behavior, and Impact",
        caption: "Keep SBI to one beat each. If a panel needs a paragraph, split the conversation.",
      },
      {
        id: nid(),
        type: "callout",
        tone: "tip",
        title: "A usable example",
        body: "“In yesterday’s client review, when the risk slide was skipped, the sponsor left without a decision. I need that slide in the room next time so we do not slip the date.”",
      },
      {
        id: nid(),
        type: "heading",
        level: 2,
        text: "Watch a short example",
        align: "left",
      },
      {
        id: nid(),
        type: "video",
        title: "Feedback in 90 seconds",
        duration: "1:32",
        note: "A manager uses SBI after a missed handoff. Placeholder only — drop in your hosted clip before you publish.",
      },
      {
        id: nid(),
        type: "button",
        label: "Open the SBI pocket card",
        href: "#sbi-card",
        variant: "primary",
      },
      {
        id: nid(),
        type: "heading",
        level: 2,
        text: "Check your understanding",
        align: "left",
      },
      {
        id: nid(),
        type: "quiz",
        question: "Which statement is the best SBI-style feedback?",
        options: [
          "You never listen in meetings and it is becoming a problem.",
          "I need you to be more professional with stakeholders.",
          "In this morning’s standup, when the blocker was not raised, the build sat idle until noon.",
          "Great energy lately, but the quality is not where it needs to be.",
        ],
        correctIndex: 2,
        explanation: "Option C names a time, an observable action, and a work impact. The others label the person, hide the request, or split the message with a compliment.",
      },
      {
        id: nid(),
        type: "callout",
        tone: "success",
        title: "Before your next conversation",
        body: "Write SBI on a sticky note. Say only that. Then ask, “How does that land?” The silence after the question is part of the design.",
      },
      {
        id: nid(),
        type: "button",
        label: "Reset the practice prompt",
        href: "#practice",
        variant: "secondary",
      },
    ],
  };
}
