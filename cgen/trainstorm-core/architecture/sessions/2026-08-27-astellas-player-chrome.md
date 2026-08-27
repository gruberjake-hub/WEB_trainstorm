# Session note — 2026-08-27 Astellas pack as Course Engine player chrome

Not canon. Canon is `architecture/DECISIONS.md`.

Jake asked App-maker (this Cursor cloud agent) to wire the existing
Astellas brand pack into Course Engine v1 at `/cgen` as **player
chrome**, not fused with Couturier occurrence `style_ref`. Open a PR
off current main. Do not push `main`. Claude is a co-builder — do not
freeze them out of files or rewrite their canon. Working-process block
untouched.

Recorded in `DECISIONS.md`:

- Pack (`cgen/brands/<client>/`) is tokens, logos, constraints.
- Couturier `brand.*` stays a pedagogical role.
- `meta.theme` is copied from the overlay (`cgen/astellas/projects/…`)
  onto every lesson JSON projection. Engine loaders under
  `cgen/engine/` resolve the pack from `/cgen`.
- Not occurrence 1:many. No new `ele_`. Sidecar HTML stays stand-in
  clothes.

Out of scope this session: chameleon.py, Headwater outcomes-mode, LLM
distractors, `/cgen/alsap` hosting, Procedure B, Brunswick, restyling
Lumina, a second CSP, changing Couturier style_map.
