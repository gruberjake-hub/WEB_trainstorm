# Realizer primitives v1 — atom → compiler form

*A closed, tiny set — not a design system, not an LLM call, not the 11
script-primitive types.* Implemented by `tools/realize.py`
(`classify_text_primitive`, `refresh_text_primitives`). Policy id:
`v1_atom_to_primitive`. Keys live in `vocab/primitives.registry.json`
(`text_primitive`). Spec path stamped on the occurrence as
`ext.realizer_primitive` and on the store manifest as `primitives.spec`.

The course chain already mints `ele_` records, binds `move`/`teaches`,
dresses `style_ref`, and projects a short spine. Every spine beat was
still **atom text dumped into a styled HTML card**. A prior hop bound a
compiler primitive on the occurrence so the projector can dress *clothes*
(heading, body, step sequence, check). This hop puts **callout** on the
spine as well — why-this / activate clothes of the purpose atom.

**Realizer owns the hop.** It reads the atom (`meaning.kind` / object role)
and the occurrence `intent.move` (Cartographer’s) and writes
`expression.text_primitive`. **Couturier still owns style**
(`style_ref`, `content_role`, `layout_hint`) and preserves the primitive
key. Cartographer still owns intent. No authored `content.text`.
`atoms.json` is untouched. Locale packs stay keyed on `atom_id`.

---

## Closed set (five roles)

| Role | `text_primitive` key | When | Spine proof |
|---|---|---|---|
| heading | `tp_display` (already registered) | `move == hook` | title opening |
| body | `tp_body` (already registered) | default instructional present; also `exemplify` | title extra, scope, general; **on the spine:** two instance-example beats (`brand.example`) |
| step | `tp_step` | atom `kind == procedure_step` | Procedure A s1–s4 as one job aid |
| callout | `tp_callout` | `move == activate` | **on the spine:** extra `ele_sop_ast29080_purpose__activate` (why this) |
| check | `tp_recall` (already registered) | `move == reinforce` | the two existing reinforce extras |

`tp_purpose` stays as Couturier’s look for `objective` (purpose-frame
front-matter). It is not a sixth compiler role; the projector treats it
as body/heading clothes on that move.

First match in `classify_text_primitive`:

1. `reinforce` → check (`tp_recall`)
2. `hook` → heading (`tp_display`)
3. `meaning.kind == procedure_step` → step (`tp_step`) — atom role wins
   over `present` / `transfer`, so a handoff step is still a step
4. `activate` → callout (`tp_callout`)
5. `objective` → keep `tp_purpose` (existing look)
6. else → body (`tp_body`)

Not an ID genius. Not 1:many of the SOP. Procedure-step atoms still
cannot host an honest copula-invert check (`agents/realizer/check_v1.md`).

---

## What the short-lesson projector does with them

`realized_lesson.html` (spine only):

| Primitive | Render |
|---|---|
| heading | display/opening surface — not a body card |
| callout | **why-this / activate** aside of the purpose atom’s existing meaning. Kicker `Why this`. Not invented text. |
| body (and `tp_purpose`) | instructional prose / purpose frame. **`exemplify`** uses this form with Couturier’s example look (`brand.example` / kicker Example) — the two instance beats after Procedure A. |
| step | **one** numbered job-aid sequence for a consecutive run (Procedure A s1–s4), not four SOP cards. Sequence title is the parent atom’s meaning (the thin A heading we already skip as a teaching card). Each `li` still joins its own `composed_from`. |
| check | existing check UI (`agents/realizer/check_v1.md`) |

`realized_coverage.html` stays card-like. Spine is the proof.

Couturier clothes still apply: a step wears `brand.instructional` with
`layout_hint: job_aid`; a check wears `brand.recall` / `layout_hint: check`.
The primitive is the *form*; style is the *look*.

---

## Ownership / idempotency

- Realizer writes `text_primitive` + `ext.realizer_primitive`. It mints guest
  instance extras (two) in addition to the purpose activate callout. Store
  stays 53 / 47 SOP atoms (+ 10 instance atoms remain in their own store).
- A re-run of realize → cartographer → couturier recomputes the same keys
  (pure function of atom kind + occurrence move). Cartographer refreshes the
  primitive after it writes `move` (the input changed). Couturier
  does not overwrite `text_primitive`.
- Re-realize preserves Couturier `style_ref` and then rebinds the
  primitive on top.

Not this hop: Dragoman, Storyline, `.potx`, motion, PNG pipelines,
Netlify / `/cgen/alsap` hosting (Jake tabled the redirect loop; buried
projector path stays the demo URL), distractor-writer, procedure B/C on
the spine, inventing procedure-step MCQs, standing up Chameleon.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Default project `cgen/astellas/projects/ast_alsap`. Open
`cgen/astellas/projects/ast_alsap/realized_lesson.html`.
`--selftest` on all three.
