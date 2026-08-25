"use client";

import { lessonDocument } from "@/lib/html-export";
import type { Lesson } from "@/lib/types";

export function PreviewPane({ lesson }: { lesson: Lesson }) {
  const html = lessonDocument(lesson);
  return (
    <div className="preview-wrap">
      <iframe title="Lesson preview" className="preview-frame" srcDoc={html} />
    </div>
  );
}
