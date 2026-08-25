import { starterLesson } from "./starter-lesson";
import type { Lesson, ProjectMeta } from "./types";

export const STORAGE_KEY = "lumina.lesson.v1";
export const INDEX_KEY = "lumina.library.v1";
export const UNSAVED_KEY = "lumina.unsaved.v1";

type LibraryIndex = {
  activeId: string | null;
  items: ProjectMeta[];
};

function projectKey(id: string) {
  return `lumina.project.${id}`;
}

function readIndex(): LibraryIndex {
  if (typeof window === "undefined") return { activeId: null, items: [] };
  try {
    const raw = window.localStorage.getItem(INDEX_KEY);
    if (raw) {
      const parsed = JSON.parse(raw) as LibraryIndex;
      if (parsed && Array.isArray(parsed.items)) return parsed;
    }
  } catch {
    /* ignore */
  }
  return { activeId: null, items: [] };
}

function writeIndex(index: LibraryIndex) {
  window.localStorage.setItem(INDEX_KEY, JSON.stringify(index));
}

function isLesson(value: unknown): value is Lesson {
  if (!value || typeof value !== "object") return false;
  const lesson = value as Lesson;
  return Array.isArray(lesson.blocks) && typeof lesson.title === "string" && typeof lesson.id === "string";
}

function parseLesson(raw: string | null): Lesson | null {
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as Lesson;
    return isLesson(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

function migrateLegacy() {
  const index = readIndex();
  if (index.items.length) return;
  const legacy = parseLesson(window.localStorage.getItem(STORAGE_KEY));
  if (!legacy) return;
  window.localStorage.setItem(projectKey(legacy.id), JSON.stringify(legacy));
  writeIndex({
    activeId: legacy.id,
    items: [{ id: legacy.id, title: legacy.title, updatedAt: legacy.updatedAt }],
  });
}

export function loadUnsaved(): Lesson | null {
  if (typeof window === "undefined") return null;
  return parseLesson(window.localStorage.getItem(UNSAVED_KEY));
}

export function saveUnsaved(lesson: Lesson) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(UNSAVED_KEY, JSON.stringify({ ...lesson, updatedAt: new Date().toISOString() }));
}

export function clearUnsaved() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(UNSAVED_KEY);
}

export function listProjects(): ProjectMeta[] {
  if (typeof window === "undefined") return [];
  migrateLegacy();
  return readIndex().items.slice().sort((a, b) => (a.updatedAt < b.updatedAt ? 1 : -1));
}

export function loadProject(id: string): Lesson | null {
  if (typeof window === "undefined") return null;
  return parseLesson(window.localStorage.getItem(projectKey(id)));
}

export function loadLesson(): Lesson {
  if (typeof window === "undefined") return starterLesson();
  migrateLegacy();
  const unsaved = loadUnsaved();
  if (unsaved) return unsaved;
  const index = readIndex();
  if (index.activeId) {
    const active = loadProject(index.activeId);
    if (active) return active;
  }
  const legacy = parseLesson(window.localStorage.getItem(STORAGE_KEY));
  if (legacy) return legacy;
  return starterLesson();
}

export function saveLesson(lesson: Lesson) {
  if (typeof window === "undefined") return;
  const next = { ...lesson, updatedAt: new Date().toISOString() };
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  window.localStorage.setItem(projectKey(next.id), JSON.stringify(next));
  const index = readIndex();
  const item: ProjectMeta = { id: next.id, title: next.title, updatedAt: next.updatedAt };
  writeIndex({
    activeId: next.id,
    items: [item, ...index.items.filter((entry) => entry.id !== next.id)],
  });
  clearUnsaved();
}

export function openProject(id: string): Lesson | null {
  const lesson = loadProject(id);
  if (!lesson) return null;
  const index = readIndex();
  writeIndex({ ...index, activeId: id });
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(lesson));
  clearUnsaved();
  return lesson;
}

export function clearLesson() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(STORAGE_KEY);
}
