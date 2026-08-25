"use client";

export function Toolbar({
  title,
  savedAt,
  unsavedImport,
  onTitle,
  onSave,
  onExportHtml,
  onExportZip,
  onReset,
  onImportHtml,
  onLessons,
}: {
  title: string;
  savedAt: string | null;
  unsavedImport: boolean;
  onTitle: (value: string) => void;
  onSave: () => void;
  onExportHtml: () => void;
  onExportZip: () => void;
  onReset: () => void;
  onImportHtml: () => void;
  onLessons: () => void;
}) {
  return (
    <header className="toolbar">
      <div className="brand">
        <span className="mark" aria-hidden>
          ✶
        </span>
        <div>
          <div className="brand-name">Lumina</div>
          <div className="brand-sub">Lesson studio</div>
        </div>
      </div>
      <input
        className="title-input"
        value={title}
        onChange={(event) => onTitle(event.target.value)}
        aria-label="Lesson title"
      />
      <div className="toolbar-actions">
        <span className="save-state">
          {unsavedImport ? "Unsaved import" : savedAt ? `Saved ${savedAt}` : "Unsaved"}
        </span>
        <button type="button" onClick={onLessons}>
          Lessons
        </button>
        <button type="button" onClick={onImportHtml}>
          Import HTML
        </button>
        <button type="button" onClick={onSave}>
          Save
        </button>
        <button type="button" onClick={onExportHtml}>
          Export HTML
        </button>
        <button type="button" onClick={onExportZip}>
          Export zip
        </button>
        <button type="button" className="ghost" onClick={onReset}>
          Starter lesson
        </button>
      </div>
    </header>
  );
}
