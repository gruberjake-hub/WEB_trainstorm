# Realizer 1:many seed v1

*A small, honest extra-occurrence seed — not a full instructional-design treatment
of the SOP.* Implemented by `tools/realize.py`. Policy id: `v1_one_to_many_seed`.
Extra records stamp `ext.realized_from.policy: v1_extra_occurrence`.

Realizer mints `ele_` ids. Cartographer still writes occurrence intent, except it
**preserves the extra's stamped `move`** (that is why the extra exists).

---

## What is seeded (ALSAP live store only)

Two teaching-worthy atoms originally; later hops added a purpose
`reinforce` check and, this hop, a purpose **`activate` callout**. The
other atoms stay 1:1.

| Atom | Primary `move` (Cartographer) | Extra `ele_` | Extra `move` | Why |
|---|---|---|---|---|
| `atom_sop_ast29080` (SOP title) | `hook` | `ele_sop_ast29080__present` | `present` | hook + present of the same meaning |
| `atom_sop_ast29080_general` (what an ALSAP is) | `present` | `ele_sop_ast29080_general__reinforce` | `reinforce` | present + retrieve/retention of the same meaning — HTML projects this extra as a **check** (`agents/realizer/check_v1.md`) |
| `atom_sop_ast29080_purpose` (what this SOP is for) | `objective` | `ele_sop_ast29080_purpose__activate` | `activate` | why-this / activate clothes — HTML projects this extra as a **callout** (`tp_callout`) of the existing purpose sentence |
| `atom_sop_ast29080_purpose` (same atom) | `objective` | `ele_sop_ast29080_purpose__reinforce` | `reinforce` | objective + retrieve/retention — second check, still a seed |

Purpose therefore wears three clothes: activate + objective + reinforce.
Closed pedagogical vocab has no `retrieve`. `reinforce` is Gagné 9a
(enhance retention) — the legal name for a later placement of the same
atom. Do not invent a new enum value. The extra `reinforce` is a check
the reader can attempt, not a recap reprint of the atom. The extra
`activate` is a callout, not a second authored purpose.

A later hop adds **guest instance extras** (not 1:many of SOP atoms): two
`exemplify` occurrences in the ALSAP store whose `composed_from` is an
`alsap_asp9999` atom_id. Spec: `agents/realizer/instance_example_v1.md`.
Those extras are not a second meaning of a SOP atom.

Do not mint extras for the whole SOP. Do not duplicate atoms. Do not copy
`content.text` onto the occurrence.

---

## Stable extra ids

```
extra_element_id = mint_element_id(atom_id) + "__" + move
```

Example: `atom_sop_ast29080_general` → primary `ele_sop_ast29080_general` → extra
`ele_sop_ast29080_general__reinforce`. Grain is `(atom_id, move)`.

---

## Idempotency

- A re-run of `realize.py` accretes missing seed extras and **never drops**
  extras already in the store, nor Cartographer bindings (`ext.cartographer` +
  bound intent) on matching `element_id`s.
- `--no-one-to-many` skips minting *new* seed extras; existing extras are still
  preserved.
- A re-run of `cartographer.py` does not mint or drop `ele_` ids. On extras it
  keeps Realizer-stamped `move` and still binds `teaches` / `rhetorical` /
  `intended_response`. Flag: `extra_occurrence_move_preserved`.

---

## Commands (from `cgen/trainstorm-core`)

```
python3 tools/realize.py
python3 tools/cartographer.py
python3 tools/couturier.py
```

Optional: `python3 tools/realize.py --selftest` · `python3 tools/cartographer.py --selftest`.
Couturier (`python3 tools/couturier.py`) dresses extras; it mints nothing and does not drop them.

The short lesson that *selects* these extras into a teachable order is
`agents/realizer/spine_v1.md` (title opening, purpose activate callout,
front-matter, Procedure A as a job sequence, a small instance example, then these checks). This spec
still does not 1:many the SOP.
