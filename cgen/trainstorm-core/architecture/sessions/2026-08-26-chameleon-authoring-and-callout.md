# Session note — 2026-08-26 authoring Chameleon + tp_callout on the spine

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) for one PR with two parts:
(1) split authoring Chameleon from runtime Chameleon in canon; (2) the next
primitives hop — put `tp_callout` on the spine as a real ID beat. Open a PR.
Do not push `main`. Claude is a co-builder — do not freeze them out of files
or rewrite their canon. Do not stand up the Chameleon agent. Do not spend
this PR on Netlify / `/cgen/alsap` hosting; Jake tabled the redirect loop.

Recorded in `DECISIONS.md`:

- **Authoring vs runtime Chameleon.** Authoring half is in-scope for a static
  course (assumed audience, `audience` keys on occurrences, same contract the
  engine would later read). Runtime / LRE stays walled. No PII. Chameleon
  does not mint `ele_` or rewrite atom meaning. Audience 1:many is another
  occurrence of the same atom. Stub amended; no `chameleon.py`; no SOP
  variants. v1, when it happens, is one documented assumed segment on the
  ALSAP lesson.
- **`tp_callout` on the spine.** Verified the purpose atom (*The purpose of
  this SOP is to define the process…*) is the “why this” meaning; title is
  the SOP name (already hook + present). Realizer mints extra
  `ele_sop_ast29080_purpose__activate` (`move: activate` → `tp_callout`).
  Spine heuristic puts that callout before the purpose primary. Meaning via
  `composed_from`. No authored `content.text`. No procedure-step MCQ.
  `atoms.json` untouched.

Out of scope this session: standing up Chameleon, `chameleon.py`, SOP
variants, writing `audience` keys onto the live store, Netlify /
`/cgen/alsap` hosting, distractor-writer, Dragoman, Storyline, `.potx`,
motion, PNG pipelines, procedure B/C on the spine, inventing a `retrieve`
enum.
