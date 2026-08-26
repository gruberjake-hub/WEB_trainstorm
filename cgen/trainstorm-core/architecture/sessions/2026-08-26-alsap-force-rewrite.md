# Session note — 2026-08-26 ALSAP public URL force rewrite

Not canon. Canon is `architecture/DECISIONS.md`.

Jake reported `ERR_TOO_MANY_REDIRECTS` on https://trainstorm.ai/cgen/alsap
after PR #18. Production curl: `/cgen/alsap` 301 → `/cgen/alsap/`;
`/cgen/alsap/` 301 → `/cgen/alsap/` (self). Pretty URLs shadowed the
unforced 200. Open a new PR off current main. Do not push `main`.
Claude is a co-builder — do not freeze them out or rewrite their canon.

Recorded in `DECISIONS.md`:

- **`force = true`** on ALSAP 200 rewrites (and the one-hop 301s).
  Canonical URL stays `/cgen/alsap/`. Coverage forced too (it self-301’d).
- No parallel `cgen/alsap/` HTML store. No second CSP. `/cgen` and
  `/cgen/lumina` untouched. Python tools / `atoms.json` untouched.

Out of scope: Dragoman, Storyline, motion, PNG render, a new app shell,
path-specific CSP.
