"use client";

import type { ProjectMeta } from "@/lib/types";

export function LessonsDialog({
  open,
  projects,
  onClose,
  onOpen,
  onImportHtml,
}: {
  open: boolean;
  projects: ProjectMeta[];
  onClose: () => void;
  onOpen: (id: string) => void;
  onImportHtml: () => void;
}) {
  if (!open) return null;
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" role="dialog" aria-labelledby="lessons-title" onClick={(event) => event.stopPropagation()}>
        <h2 id="lessons-title">Lessons</h2>
        <p className="modal-lead">Saved projects stay in this browser. Import HTML creates a new project — the previous lesson is not overwritten until you Save.</p>
        <div className="modal-actions" style={{ marginBottom: 12 }}>
          <button type="button" onClick={onImportHtml}>
            Import HTML
          </button>
        </div>
        {projects.length === 0 ? (
          <p className="palette-help">No saved projects yet. Import HTML or click Save on the starter.</p>
        ) : (
          <ul className="project-list">
            {projects.map((project) => (
              <li key={project.id}>
                <button type="button" className="project-item" onClick={() => onOpen(project.id)}>
                  <strong>{project.title || "Untitled"}</strong>
                  <em>{new Date(project.updatedAt).toLocaleString()}</em>
                </button>
              </li>
            ))}
          </ul>
        )}
        <div className="modal-actions">
          <button type="button" className="ghost" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
