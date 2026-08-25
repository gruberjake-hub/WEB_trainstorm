"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { createBlock } from "@/lib/blocks";
import { exportHtmlFile, exportZipFile } from "@/lib/html-export";
import { loadLesson, saveLesson } from "@/lib/storage";
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
import type { Block, BlockType, Lesson } from "@/lib/types";
import { Canvas } from "./Canvas";
import { CodeInspector } from "./CodeInspector";
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

  useEffect(() => {
    const loaded = loadLesson();
    setLesson(loaded);
    setSavedLabel(formatTime(loaded.updatedAt));
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    const handle = window.setTimeout(() => {
      saveLesson(lesson);
      setSavedLabel(formatTime(new Date().toISOString()));
    }, 400);
    return () => window.clearTimeout(handle);
  }, [lesson, hydrated]);

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
        onTitle={(title) => setLesson((current) => ({ ...current, title }))}
        onSave={() => {
          saveLesson(lesson);
          const stamp = new Date().toISOString();
          setLesson((current) => ({ ...current, updatedAt: stamp }));
          setSavedLabel(formatTime(stamp));
        }}
        onExportHtml={() => exportHtmlFile(lesson)}
        onExportZip={() => {
          void exportZipFile(lesson);
        }}
        onReset={() => {
          const next = starterLesson();
          setLesson(next);
          setSelectedId(null);
          saveLesson(next);
        }}
      />
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
    </div>
  );
}
