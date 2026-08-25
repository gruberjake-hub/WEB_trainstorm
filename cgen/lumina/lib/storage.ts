import { starterLesson } from "./starter-lesson";
import type { Lesson } from "./types";

export const STORAGE_KEY = "lumina.lesson.v1";

export function loadLesson(): Lesson {
  if (typeof window === "undefined") return starterLesson();
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return starterLesson();
    const parsed = JSON.parse(raw) as Lesson;
    if (!parsed || !Array.isArray(parsed.blocks) || typeof parsed.title !== "string") {
      return starterLesson();
    }
    return parsed;
  } catch {
    return starterLesson();
  }
}

export function saveLesson(lesson: Lesson) {
  if (typeof window === "undefined") return;
  const next = { ...lesson, updatedAt: new Date().toISOString() };
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
}

export function clearLesson() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(STORAGE_KEY);
}
