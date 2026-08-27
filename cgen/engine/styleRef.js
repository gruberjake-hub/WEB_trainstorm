// Closed map matching realize.py CLOTHES_CLASS / sidecar HTML.
// Couturier style_ref is a pedagogical role, not a hex or a font.
// Unmapped or missing: no class (sidecar look_unmapped — do not invent a look).

export const STYLE_REF_CLASS = {
  "brand.opening": "style-opening",
  "brand.instructional": "style-instructional",
  "brand.recall": "style-recall",
  "brand.purpose": "style-purpose",
  "brand.prior": "style-prior",
  "brand.example": "style-example",
  "brand.job": "style-job"
};

export function roleClassFromMeta(meta) {
  const ref = meta && meta.style_ref;
  if (!ref) return "";
  return STYLE_REF_CLASS[ref] || "";
}
