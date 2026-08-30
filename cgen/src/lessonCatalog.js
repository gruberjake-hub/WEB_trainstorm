/** Resolve a Course Engine lesson from the project catalog.
 *
 *  `occurrences/lessons.json` is the source of truth. Each record's
 *  `projection` is the existing realize sidecar name at the project
 *  root (`realized_lesson.json` / `realized_lesson_{suffix}.json`).
 *  The player is not an ALSAP filename special-case.
 *
 *  `/cgen` still points at one stand-in catalog. A future URL names
 *  client + course (which catalog). `?lesson=` is which record loads.
 *  Not a catalog UI.
 */

export const DEFAULT_CATALOG_URL =
  "./astellas/projects/ast_alsap/occurrences/lessons.json";

const CATALOG_MARKER = "/occurrences/lessons.json";

export function projectRootFromCatalogUrl(catalogUrl) {
  const url = String(catalogUrl || "");
  const idx = url.toLowerCase().lastIndexOf(CATALOG_MARKER);
  if (idx >= 0) return url.slice(0, idx);
  return url.replace(/\/[^/]*$/, "");
}

export function projectionFilename(projection) {
  if (typeof projection !== "string") return "";
  const name = projection.trim().replace(/\\/g, "/").split("/").pop() || "";
  if (!name || name.includes("..") || !name.endsWith(".json")) return "";
  return name;
}

export function projectionHref(catalogUrl, projection) {
  const name = projectionFilename(projection);
  if (!name) return "";
  const root = projectRootFromCatalogUrl(catalogUrl);
  return `${root}/${name}`;
}

export function catalogLessonIds(catalog) {
  const lessons = Array.isArray(catalog?.lessons) ? catalog.lessons : [];
  return lessons.map((row) => row?.lesson_id).filter(Boolean);
}

export function catalogDefaultId(catalog) {
  if (typeof catalog?.default === "string" && catalog.default) {
    return catalog.default;
  }
  const lessons = Array.isArray(catalog?.lessons) ? catalog.lessons : [];
  const marked = lessons.find((row) => row?.default && row.lesson_id);
  return marked?.lesson_id || "";
}

/** `lessonId` null/undefined → catalog default. Empty string is unknown. */
export function selectCatalogLesson(
  catalog,
  lessonId,
  catalogUrl = DEFAULT_CATALOG_URL
) {
  const ids = catalogLessonIds(catalog);
  const lessons = Array.isArray(catalog?.lessons) ? catalog.lessons : [];
  const requested = lessonId == null ? catalogDefaultId(catalog) : String(lessonId);
  const record = lessons.find((row) => row?.lesson_id === requested);
  if (!record) {
    return { ok: false, reason: "unknown_lesson", lessonId: requested, ids };
  }
  const href = projectionHref(catalogUrl, record.projection);
  if (!href) {
    return {
      ok: false,
      reason: "missing_projection",
      lessonId: requested,
      ids,
      record
    };
  }
  return { ok: true, lessonId: requested, ids, record, href };
}

export function unknownLessonMessage(lessonId, ids) {
  const listed = ids.length ? ids.join(", ") : "(none)";
  const shown = lessonId ? `"${lessonId}"` : "(empty)";
  return `Unknown lesson id ${shown}. This catalog has: ${listed}.`;
}

export function missingProjectionMessage(lessonId) {
  const shown = lessonId ? `"${lessonId}"` : "(empty)";
  return `Lesson ${shown} has no projection path on the catalog.`;
}
