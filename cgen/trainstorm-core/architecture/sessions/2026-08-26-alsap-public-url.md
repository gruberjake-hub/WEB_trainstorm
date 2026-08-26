# Session note — 2026-08-26 ALSAP short lesson public URL

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to give the ALSAP short
lesson a first-class live URL on the existing Netlify site after PR #17
left it at `cgen/astellas/projects/ast_alsap/realized_lesson.html`. Open
a PR. Do not push `main`. Claude is a co-builder — do not freeze them
out of files or rewrite their canon.

Recorded in `DECISIONS.md`:

- **Public rewrite, not a parallel store.** `/cgen/alsap` → projector
  `realized_lesson.html`; `/cgen/alsap/coverage` → `realized_coverage.html`.
  After realize → cartographer → couturier, the public path is current.
- **`/cgen` and `/cgen/lumina` untouched.** `/cgen` is the Course Engine
  player, not a lesson index — no new app shell.
- **One site-wide CSP.** `_headers` unchanged (PR #6). No second CSP on
  this path.
- Python tools, `atoms.json`, spine membership, facet writers unchanged.

Out of scope this session: Dragoman, Storyline, motion, PNG render, a
manifold GUI, distractor-writer, replacing the `/cgen` player, path-
specific CSP.
