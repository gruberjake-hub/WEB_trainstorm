"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { createBlock } from "@/lib/blocks";
import { exportHtmlFile, exportZipFile } from "@/lib/html-export";
import { importHtmlDocument } from "@/lib/html-import";
import { loadLesson, listProjects, openProject, saveLesson, saveUnsaved } from "@/lib/storage";
import { starterLesson } from "@/lib/starter-lesson";
import {
  cloneTree,
  duplicateBlock,
  findBlock,
  insertAfter,
  insertIntoColumn,
  moveBlock,
  removeBlock,
  reorder,
  updateBlock,
} from "@/lib/tree";
import type { Block, BlockType, Lesson, ProjectMeta } from "@/lib/types";
import { Canvas } from "./Canvas";
import { CodeInspector } from "./CodeInspector";
import { ImportDialog } from "./ImportDialog";
import { LessonsDialog } from "./LessonsDialog";
import { Palette } from "./Palette";
import { PreviewPane } from "./PreviewPane";
import { PropertiesPanel } from "./PropertiesPanel";
import { Toolbar } from "./Toolbar";

type RightTab = "properties" | "preview" | "code";

function isBlockType(value: string): value is BlockType {
  return [
    "heading",
    "paragraph",
    "image",
    "button",
    "list",
    "callout",
    "columns",
    "video",
    "quiz",
    "html",
  ].includes(value);
}

function formatTime(iso: string) {
  try {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

export function Studio() {
  const [lesson, setLesson] = useState<Lesson>(starterLesson);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [hydrated, setHydrated] = useState(false);
  const [tab, setTab] = useState<RightTab>("properties");
  const [savedLabel, setSavedLabel] = useState<string | null>(null);
  const [unsavedImport, setUnsavedImport] = useState(false);
  const [importNote, setImportNote] = useState<string | null>(null);
  const [importOpen, setImportOpen] = useState(false);
  const [lessonsOpen, setLessonsOpen] = useState(false);
  const [projects, setProjects] = useState<ProjectMeta[]>([]);

  useEffect(() => {
    const loaded = loadLesson();
    setLesson(loaded);
    const draft = typeof window !== "undefined" && window.localStorage.getItem("lumina.unsaved.v1");
    if (draft) {
      setUnsavedImport(true);
      setSavedLabel(null);
    } else {
      setSavedLabel(formatTime(loaded.updatedAt));
    }
    setProjects(listProjects());
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    const handle = window.setTimeout(() => {
      if (unsavedImport) {
        saveUnsaved(lesson);
        return;
      }
      saveLesson(lesson);
      setSavedLabel(formatTime(new Date().toISOString()));
      setProjects(listProjects());
    }, 400);
    return () => window.clearTimeout(handle);
  }, [lesson, hydrated, unsavedImport]);

  const selected = useMemo(
    () => (selectedId ? findBlock(lesson.blocks, selectedId) : null),
    [lesson.blocks, selectedId],
  );

  const setBlocks = useCallback((blocks: Block[] | ((current: Block[]) => Block[])) => {
    setLesson((current) => ({
      ...current,
      blocks: typeof blocks === "function" ? blocks(current.blocks) : blocks,
    }));
  }, []);

  const addBlock = useCallback(
    (type: BlockType, afterId: string | null = selectedId) => {
      const next = createBlock(type);
      setBlocks((blocks) => insertAfter(blocks, afterId, next));
      setSelectedId(next.id);
    },
    [selectedId, setBlocks],
  );

  const onCanvasDrop = useCallback(
    (targetId: string | null, data: DataTransfer) => {
      const type = data.getData("application/lumina-block");
      const fromId = data.getData("application/lumina-move");
      if (type && isBlockType(type)) {
        addBlock(type, targetId);
        return;
      }
      if (fromId && targetId) {
        setBlocks((blocks) => reorder(blocks, fromId, targetId));
        setSelectedId(fromId);
      }
    },
    [addBlock, setBlocks],
  );

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      const target = event.target as HTMLElement | null;
      if (target && ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName)) return;
      if ((event.key === "Backspace" || event.key === "Delete") && selectedId) {
        event.preventDefault();
        setBlocks((blocks) => removeBlock(blocks, selectedId));
        setSelectedId(null);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selectedId, setBlocks]);

  return (
    <div className="studio">
      <Toolbar
        title={lesson.title}
        savedAt={savedLabel}
        unsavedImport={unsavedImport}
        onTitle={(title) => setLesson((current) => ({ ...current, title }))}
        onLessons={() => {
          setProjects(listProjects());
          setLessonsOpen(true);
        }}
        onImportHtml={() => setImportOpen(true)}
        onSave={() => {
          saveLesson(lesson);
          const stamp = new Date().toISOString();
          setLesson((current) => ({ ...current, updatedAt: stamp }));
          setSavedLabel(formatTime(stamp));
          setUnsavedImport(false);
          setProjects(listProjects());
        }}
        onExportHtml={() => exportHtmlFile(lesson)}
        onExportZip={() => {
          void exportZipFile(lesson);
        }}
        onReset={() => {
          const next = starterLesson();
          setLesson(next);
          setSelectedId(null);
          setImportNote(null);
          setUnsavedImport(false);
          saveLesson(next);
          setProjects(listProjects());
        }}
      />
      {importNote ? (
        <div className="import-banner">
          <span>{importNote}</span>
          <button type="button" className="ghost" onClick={() => setImportNote(null)}>
            Dismiss
          </button>
        </div>
      ) : null}
      <div className="workspace">
        <aside className="left-pane">
          <Palette onAdd={(type) => addBlock(type)} />
          {selectedId ? (
            <div className="block-actions">
              <button type="button" onClick={() => setBlocks((blocks) => moveBlock(blocks, selectedId, -1))}>
                Move up
              </button>
              <button type="button" onClick={() => setBlocks((blocks) => moveBlock(blocks, selectedId, 1))}>
                Move down
              </button>
              <button
                type="button"
                onClick={() => {
                  setBlocks((blocks) => duplicateBlock(blocks, selectedId, cloneTree));
                }}
              >
                Duplicate
              </button>
              <button
                type="button"
                className="danger"
                onClick={() => {
                  setBlocks((blocks) => removeBlock(blocks, selectedId));
                  setSelectedId(null);
                }}
              >
                Delete
              </button>
            </div>
          ) : null}
        </aside>
        <Canvas
          blocks={lesson.blocks}
          selectedId={selectedId}
          onSelect={setSelectedId}
          onDrop={onCanvasDrop}
        />
        <aside className="right-pane">
          <div className="tabs">
            {(["properties", "preview", "code"] as const).map((item) => (
              <button
                key={item}
                type="button"
                className={tab === item ? "is-on" : ""}
                onClick={() => setTab(item)}
              >
                {item === "properties" ? "Properties" : item === "preview" ? "Preview" : "Code"}
              </button>
            ))}
          </div>
          {tab === "properties" ? (
            <PropertiesPanel
              block={selected}
              lessonTitle={lesson.title}
              lessonSubtitle={lesson.subtitle}
              extraJs={lesson.extraJs || ""}
              onLessonMeta={(patch) => setLesson((current) => ({ ...current, ...patch }))}
              onChange={(patch) => {
                if (!selectedId) return;
                setBlocks((blocks) => updateBlock(blocks, selectedId, patch));
              }}
              onAddNested={(side, type) => {
                if (!selected || selected.type !== "columns") return;
                const next = createBlock(type);
                setBlocks((blocks) => insertIntoColumn(blocks, selected.id, side, next));
                setSelectedId(next.id);
              }}
            />
          ) : null}
          {tab === "preview" ? <PreviewPane lesson={lesson} /> : null}
          {tab === "code" ? <CodeInspector lesson={lesson} /> : null}
        </aside>
      </div>
      <ImportDialog
        open={importOpen}
        onClose={() => setImportOpen(false)}
        onImport={(html, filename) => {
          const result = importHtmlDocument(html, filename);
          setLesson(result.lesson);
          setSelectedId(null);
          setUnsavedImport(true);
          setSavedLabel(null);
          setImportNote(result.note || "Imported as a new project. Save to keep it without replacing the previous lesson.");
          saveUnsaved(result.lesson);
          setImportOpen(false);
          setLessonsOpen(false);
          setTab("properties");
        }}
      />
      <LessonsDialog
        open={lessonsOpen}
        projects={projects}
        onClose={() => setLessonsOpen(false)}
        onImportHtml={() => {
          setLessonsOpen(false);
          setImportOpen(true);
        }}
        onOpen={(id) => {
          const opened = openProject(id);
          if (!opened) return;
          setLesson(opened);
          setSelectedId(null);
          setUnsavedImport(false);
          setImportNote(null);
          setSavedLabel(formatTime(opened.updatedAt));
          setLessonsOpen(false);
        }}
      />
    </div>
  );
}
