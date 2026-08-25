"use client";

import { lessonDocument, prettyHtml } from "@/lib/html-export";
import type { Lesson } from "@/lib/types";

export function CodeInspector({ lesson }: { lesson: Lesson }) {
  const html = prettyHtml(lessonDocument(lesson));
  return (
    <div className="code-wrap">
      <div className="code-toolbar">
        <span>Generated HTML</span>
        <button
          type="button"
          onClick={async () => {
            await navigator.clipboard.writeText(html);
          }}
        >
          Copy
        </button>
      </div>
      <pre className="code-pre">
        <code>{html}</code>
      </pre>
    </div>
  );
}
