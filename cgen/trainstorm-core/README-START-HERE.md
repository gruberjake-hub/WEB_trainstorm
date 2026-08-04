# Layout Engine ↔ Manifold — conformed bundle (2026-07-31)

Drop `trainstorm-core/` into your `cgen/trainstorm-core/` checkout (the 3 new vocab files + the
updated primitives.registry.json), apply the two PATCH-*.md docs, and replace the `layout-engine/`
files with these. Then run the gate:

    cd layout-engine
    python ci/validate_sidecar.py sidecars/astellas.awareness.sidecar.json --core-dir ../trainstorm-core

Read `RECONCILIATION.md` first — it's the full diff and the open decisions.
