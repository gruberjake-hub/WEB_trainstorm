# Couturier style map v1 — occurrence clothes from move

*A handful of look keys, not a design system.* Bound values are registry
members (`vocab/primitives.registry.json` `style_ref` / `text_primitive`) plus
two occurrence-local labels (`content_role`, `layout_hint`) already on
`element.expression`. v1 does **not** bind `motion_primitive` (registry still
empty — stub), `layout_primitive` (those keys are the `.potx` / Storyline set),
or `interaction_primitive`.

Implemented by `tools/couturier.py`. Policy id: `v1_move_to_look`.

Couturier writes **style keys on existing `ele_` records**. It never mints
`ele_` or `atom_` ids, never copies meaning onto the element, never writes
`atoms.json`, never writes `element.intent`. Locale packs stay keyed on
`atom_id`. Style is keyed on `element_id`.

The map is from Cartographer's `intent.move` (already on the occurrence).
`teaches` does not change clothes in v1.

---

## Why three looks matter more than seven

The live 1:many seed is two pairs plus a third check:

- SOP title: `hook` + `present` → opening clothes vs instructional clothes
- ALSAP definition: `present` + `reinforce` → instructional clothes vs recall **check**
- SOP purpose: `objective` + `reinforce` → purpose clothes vs recall **check**

Those pairs must not look like the same SOP card. `reinforce` is a check
projected from the atom (`agents/realizer/check_v1.md`), dressed here as
`brand.recall`. Other live moves get a distinct look so the page is not 36
identical present-cards, but the map is still one row per closed pedagogical
value this SOP actually uses. No `practice` / `feedback` / `assess` looks
until those moves exist.

---

## `move` → expression keys

| move | `style_ref` | `text_primitive` | `content_role` | `layout_hint` | What Jake should see |
|---|---|---|---|---|---|
| `hook` | `brand.opening` | `tp_display` | `title` | `banner` | large centered opening, not a body card |
| `present` | `brand.instructional` | `tp_body` | `body` | `card` | instructional body card |
| `reinforce` | `brand.recall` | `tp_recall` | `retrieval` | `check` | a check the reader can attempt (stem + choices or cloze), not a quoted recap |
| `objective` | `brand.purpose` | `tp_purpose` | `purpose` | `purpose_bar` | purpose frame |
| `activate` | `brand.prior` | `tp_body` | `prior` | `callout` | prior-knowledge callout |
| `exemplify` | `brand.example` | `tp_body` | `example` | `cite` | named-example / citation |
| `transfer` | `brand.job` | `tp_body` | `handoff` | `job_rail` | job-bridge |

`style_ref` is a **role** ("this is an opening surface"), not a hex or a font.
Brand token resolution (`brands/<client>/`) is later. The HTML projector reads
these keys and applies stand-in clothes so the difference is visible now.

Unmapped closed-vocab moves (`practice`, `feedback`, `assess`): **do not invent
a look**. Flag `look_unmapped` and leave the occurrence undressed. Honest gap.

`reinforce` is the closed-vocab name for retrieve/retention (Gagné 9a). The
look is `brand.recall` with `layout_hint: check`. Do not invent a `retrieve`
move. The HTML projector (Realizer) turns that look into a check UI from
atom meaning — Couturier still writes only the style keys.

---

## Keys v1 does not write

- `motion_primitive` — registry empty; motion is a stub mention, not this hop
- `layout_primitive` — `TITLE_BODY` / `REVEAL_GRID` / … are the `.potx` set
- `interaction_primitive` — Storyline; not this hop
- anything on the atom, including `atom.bindings.expression`
- `element.intent` (Cartographer) or new `ele_` ids (Realizer)

If a key Couturier does not own is already set (the known Realizer /
`layout_primitive` collision), **do not silently overwrite it.** Keep it and
bind only the style keys in the table.

---

## Provenance

Each occurrence this pass dresses gets `ext.couturier`:

```json
{
  "policy": "v1_move_to_look",
  "tool": "tools/couturier.py",
  "spec": "agents/couturier/style_map_v1.md",
  "from_move": "hook",
  "source_hash": "sha256:…"
}
```

`source_hash` is the atom `content_hash` bound against (via `composed_from`).
`ext.realized_from` and `ext.cartographer` stay theirs. Couturier does not
take `governance.owner` of the occurrence node.

---

## Idempotency

- Re-run of Couturier does not mint or drop `ele_` ids.
- Re-run of `realize.py` preserves `expression` + `ext.couturier` (and extras,
  and Cartographer intent).
- Re-run of `cartographer.py` does not wipe `expression`.
- 1:many members of the same atom must wear **distinct** `style_ref` values
  (that is the instrument). Run Cartographer before Couturier so the title
  pair is `hook` + `present`, not two `present`s.
- HTML projector reads `expression` keys for clothes; meaning still from the
  atom. No authored `content.text`.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Optional: `python3 tools/couturier.py --selftest` · `--project` like the others.
