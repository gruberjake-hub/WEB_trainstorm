"use client";

import { useRef, useState } from "react";

export function ImportDialog({
  open,
  onClose,
  onImport,
}: {
  open: boolean;
  onClose: () => void;
  onImport: (html: string, filename?: string) => void;
}) {
  const fileRef = useRef<HTMLInputElement>(null);
  const [paste, setPaste] = useState("");
  const [filename, setFilename] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);

  if (!open) return null;

  function reset() {
    setPaste("");
    setFilename(undefined);
    setError(null);
    if (fileRef.current) fileRef.current.value = "";
  }

  async function onFile(file: File | undefined) {
    if (!file) return;
    setFilename(file.name);
    setError(null);
    const text = await file.text();
    setPaste(text);
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal"
        role="dialog"
        aria-labelledby="import-html-title"
        onClick={(event) => event.stopPropagation()}
      >
        <h2 id="import-html-title">Import HTML</h2>
        <p className="modal-lead">
          Open a lesson <code>.html</code> / <code>.htm</code> file, or paste markup. Lumina turns it into editable
          blocks. Scripts are saved as Extra JS and are not run in the studio.
        </p>
        <label className="field">
          <span>Open HTML file</span>
          <input
            ref={fileRef}
            type="file"
            accept=".html,.htm,text/html"
            onChange={(event) => {
              void onFile(event.target.files?.[0]);
            }}
          />
        </label>
        <label className="field">
          <span>Or paste HTML</span>
          <textarea
            rows={10}
            value={paste}
            spellCheck={false}
            placeholder="<!DOCTYPE html>…"
            onChange={(event) => setPaste(event.target.value)}
          />
        </label>
        {error ? <p className="modal-error">{error}</p> : null}
        <div className="modal-actions">
          <button type="button" className="ghost" onClick={onClose}>
            Cancel
          </button>
          <button
            type="button"
            onClick={() => {
              const html = paste.trim();
              if (!html) {
                setError("Choose a file or paste HTML first.");
                return;
              }
              onImport(html, filename);
              reset();
            }}
          >
            Import into canvas
          </button>
        </div>
      </div>
    </div>
  );
}
