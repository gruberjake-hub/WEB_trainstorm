#!/usr/bin/env python3
"""
Realizer v1 — atoms → occurrence elements + a double-clickable HTML lesson.

The Realizer is the typesetter of meaning (`architecture/agents-roster.md`). It
does not invent authored text. Display HTML reads meaning from the atom via
`composed_from`. Default is still **one occurrence per atom** (move placeholder
`present`). A small documented 1:many seed then mints extra `ele_` records for
a couple of teaching-worthy atoms — same `composed_from`, distinct `move`,
stable extra ids. The rest of the store stays 1:1. Not a full ID treatment of
the SOP.

Idempotency: extra ids are `(primary ele_) + "__" + move`. A re-run accretes
missing extras and never drops existing extras or Cartographer bindings.

Not this tool: Dragoman (locale packs), Storyline, .potx, PNG pipelines,
`tools/render/`. Couturier (`tools/couturier.py`) owns style keys on the
occurrence; a re-realize preserves them. Does not rewrite SOP/form atoms into
elements — `atoms.json` is read-only. Cartographer still binds `teaches` / rest
of intent.

Usage (from `cgen/trainstorm-core`):

    python tools/realize.py
    python tools/realize.py --project ../astellas/projects/ast_alsap
    python tools/realize.py --selftest
    python tools/cartographer.py          # re-runnable on the mixed store
    python tools/couturier.py             # dresses existing ele_; mints nothing

Default `--project` is the live ALSAP SOP store (47 atoms). Writes (regenerated,
never hand-edited):

    <project>/occurrences/elements.json     occurrence store (does not touch atoms.json)
    <project>/occurrences/manifest.json     realized_from / source hashes
    <project>/realized_lesson.html          open in a browser
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import pathlib
import re
import sys

import harness_paths
from jsonschema import Draft202012Validator

POLICY = "v1_one_occurrence_per_atom"
EXTRA_POLICY = "v1_extra_occurrence"
STORE_POLICY = "v1_one_to_many_seed"
REALIZER = "tools/realize.py"
DEFAULT_MOVE = "present"
ELE_ID_RE = re.compile(r"^ele_[A-Za-z0-9_-]+$")

# Honest 1:many seed — a couple of teaching-worthy ALSAP atoms, not the whole SOP.
# Primary occurrence keeps Cartographer's bound move; Realizer stamps `move` only
# on the extra. Closed pedagogical vocab has no `retrieve`; `reinforce` is Gagné
# 9a (enhance retention), the legal name for a later placement of the same meaning.
# Spec: agents/realizer/one_to_many_v1.md
ONE_TO_MANY_SEED = (
    ("atom_sop_ast29080", "present"),            # title: hook (primary) + present
    ("atom_sop_ast29080_general", "reinforce"),  # what ALSAP is: present + retrieve
)

KIND_TO_TYPE = {
    "procedure": "Section",
    "procedure_step": "Statement",
    "list": "List",
    "list_item": "Bullet",
    "form": "Section",
    "form_section": "Section",
    "form_field": "Statement",
    "instance_value": "Statement",
}
TYPE_TO_RHETORICAL = {
    "Course": "orient",
    "Section": "structure",
    "Head": "orient",
    "ListHead": "organize",
    "List": "organize",
    "Bullet": "specify",
    "Statement": "assert",
    "Paragraph": "explain",
    "Impact": "persuade",
    "Quote": "contextualize",
    "Callout": "support",
}


def repo_default_project():
    """Sibling live ALSAP SOP store: cgen/astellas/projects/ast_alsap."""
    p = pathlib.Path(__file__).resolve().parent.parent.parent / "astellas" / "projects" / "ast_alsap"
    return p if (p / "atoms.json").exists() else None


def argv_has_flag(name):
    prefix = name + "="
    for a in sys.argv[1:]:
        if a == name or a.startswith(prefix):
            return True
    return False


def inject_default_project():
    """Other harness tools require --project. Realizer v1 has a known first hop."""
    if argv_has_flag("--project") or os.environ.get("TRAINSTORM_PROJECT"):
        return
    d = repo_default_project()
    if d is not None:
        os.environ["TRAINSTORM_PROJECT"] = str(d)


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def mint_element_id(atom_id: str) -> str:
    if not atom_id.startswith("atom_"):
        raise SystemExit(f"cannot mint ele_ from {atom_id!r}: not an atom_ id")
    eid = "ele_" + atom_id[len("atom_"):]
    if not ELE_ID_RE.match(eid):
        raise SystemExit(f"minted id fails ele_ pattern: {eid}")
    return eid


def mint_extra_element_id(atom_id: str, move: str) -> str:
    """Stable extra occurrence id: primary ele_ + '__' + closed-vocab move."""
    if not re.match(r"^[a-z]+$", move):
        raise SystemExit(f"cannot mint extra ele_ for ungoverned move {move!r}")
    eid = mint_element_id(atom_id) + "__" + move
    if not ELE_ID_RE.match(eid):
        raise SystemExit(f"minted extra id fails ele_ pattern: {eid}")
    return eid


def is_primary_element(el) -> bool:
    cf = el.get("composed_from")
    return bool(cf) and el.get("element_id") == mint_element_id(cf)


def is_extra_element(el) -> bool:
    rf = (el.get("ext") or {}).get("realized_from") or {}
    if rf.get("role") == "extra":
        return True
    cf = el.get("composed_from")
    return bool(cf) and el.get("element_id") != mint_element_id(cf)


def element_type(atom) -> str:
    kind = (atom.get("meaning") or {}).get("kind")
    belongs = (atom.get("bindings") or {}).get("object", {}).get("belongs_to")
    if not belongs:
        return "Course"
    return KIND_TO_TYPE.get(kind, "Statement")


def clean_meaning(text: str) -> str:
    i = text.find("[Headwater")
    return text[:i].strip() if i != -1 else text.strip()


def kids(atoms, parent_id):
    ch = [a for a in atoms
          if (a.get("bindings") or {}).get("object", {}).get("belongs_to") == parent_id]
    return sorted(ch, key=lambda a: (a.get("bindings") or {}).get("object", {}).get("order", 0))


def roots(atoms):
    r = [a for a in atoms
         if not (a.get("bindings") or {}).get("object", {}).get("belongs_to")]
    if r:
        return r
    return list(atoms)


def portable_atom_store_path(atoms_path: pathlib.Path) -> str:
    """Repo-relative path when possible — never a machine-local absolute."""
    repo = pathlib.Path(__file__).resolve().parents[3]  # …/cgen/trainstorm-core/tools → repo
    try:
        return str(atoms_path.resolve().relative_to(repo))
    except ValueError:
        return "atoms.json"


def mint_element(atom, move: str, *, role: str = "primary") -> dict:
    aid = atom["atom_id"]
    obj = (atom.get("bindings") or {}).get("object") or {}
    typ = element_type(atom)
    extra = role == "extra"
    realized_from = {
        "atom_id": aid,
        "realizer": REALIZER,
        "policy": EXTRA_POLICY if extra else POLICY,
        "role": "extra" if extra else "primary",
    }
    if extra:
        realized_from["target_move"] = move
    ch = atom.get("content_hash")
    if ch:
        realized_from["content_hash"] = ch
    structure = {}
    if obj.get("belongs_to"):
        structure["parent_id"] = mint_element_id(obj["belongs_to"])
    if "order" in obj:
        structure["sequence_index"] = obj["order"]
    if obj.get("prerequisites"):
        structure["prerequisites"] = [mint_element_id(p) for p in obj["prerequisites"]]
    gov = {
        "version": 1,
        "status": "draft",
        "owner": "realizer",
    }
    rb = (atom.get("governance") or {}).get("regulatory_binding")
    if rb:
        gov["regulatory_binding"] = rb
    el = {
        "element_id": mint_extra_element_id(aid, move) if extra else mint_element_id(aid),
        "composed_from": aid,
    }
    if ch:
        el["source_hash"] = ch
    el["type"] = typ
    if structure:
        el["structure"] = structure
    el["intent"] = {
        "rhetorical": TYPE_TO_RHETORICAL.get(typ, "assert"),
        "move": move,
    }
    el["governance"] = gov
    el["ext"] = {"realized_from": realized_from}
    return el


def apply_group_ids(elements):
    """Pair 1:many members via structure.group_id = composed_from (atom_id)."""
    from collections import defaultdict
    by_atom = defaultdict(list)
    for el in elements:
        by_atom[el["composed_from"]].append(el)
    for aid, group in by_atom.items():
        if len(group) < 2:
            continue
        for el in group:
            el.setdefault("structure", {})["group_id"] = aid


def extra_move_of(el) -> str | None:
    intent_move = (el.get("intent") or {}).get("move")
    rf = (el.get("ext") or {}).get("realized_from") or {}
    return rf.get("target_move") or intent_move


def assemble_elements(atoms, previous, default_move: str, *, mint_extras: bool = True) -> list:
    """
    Mint one primary per atom, then extra occurrences from the seed and from
    any extras already in the store. Never drop an existing extra. Preserve
    Cartographer intent on matching element_id values.
    """
    prev = {e.get("element_id"): e for e in (previous or []) if e.get("element_id")}
    atoms_by_id = {a["atom_id"]: a for a in atoms}
    seed_moves = {}
    if mint_extras:
        for aid, move in ONE_TO_MANY_SEED:
            seed_moves.setdefault(aid, []).append(move)

    elements = []
    claimed = set()

    for atom in atoms:
        aid = atom["atom_id"]
        primary = mint_element(atom, default_move, role="primary")
        preserve_cartographer_intent([primary], previous)
        preserve_couturier_expression([primary], previous)
        elements.append(primary)
        claimed.add(primary["element_id"])

        wanted = []  # (element_id, move)
        seen_eids = set()
        for move in seed_moves.get(aid, []):
            eid = mint_extra_element_id(aid, move)
            wanted.append((eid, move))
            seen_eids.add(eid)
        for old in prev.values():
            if old.get("composed_from") != aid or not is_extra_element(old):
                continue
            eid = old["element_id"]
            if eid in seen_eids:
                continue
            move = extra_move_of(old)
            if not move:
                continue
            wanted.append((eid, move))
            seen_eids.add(eid)

        for eid, move in wanted:
            extra = mint_element(atom, move, role="extra")
            extra["element_id"] = eid
            preserve_cartographer_intent([extra], previous)
            preserve_couturier_expression([extra], previous)
            if not (extra.get("ext") or {}).get("cartographer"):
                extra["intent"]["move"] = move
            elements.append(extra)
            claimed.add(eid)

    for eid, old in prev.items():
        if eid in claimed:
            continue
        cf = old.get("composed_from")
        if cf in atoms_by_id and is_extra_element(old):
            elements.append(old)
            claimed.add(eid)

    apply_group_ids(elements)
    return elements


def validate_elements(elements, schema, atoms_by_id):
    v = Draft202012Validator(schema)
    hard = []
    seen = set()
    for el in elements:
        for err in sorted(v.iter_errors(el), key=lambda e: list(e.path)):
            hard.append(f"{el.get('element_id', '?')}: {err.message}")
        eid = el.get("element_id")
        if eid in seen:
            hard.append(f"duplicate element_id {eid}")
        seen.add(eid)
        if "content" in el:
            hard.append(f"{eid}: authored content is forbidden on v1 occurrences "
                        "(meaning lives on the atom)")
        cf = el.get("composed_from")
        if cf not in atoms_by_id:
            hard.append(f"{eid}: composed_from {cf} is not in the atom store")
        if el.get("intent", {}).get("move") is None:
            hard.append(f"{eid}: missing intent.move")
        if is_extra_element(el):
            rf = (el.get("ext") or {}).get("realized_from") or {}
            if rf.get("role") and rf.get("role") != "extra":
                hard.append(f"{eid}: extra occurrence realized_from.role is {rf.get('role')!r}")
    if hard:
        print("REALIZER VALIDATION FAILURES:", file=sys.stderr)
        for m in hard:
            print("  x", m, file=sys.stderr)
        raise SystemExit(1)


def move_counts(elements):
    counts = {}
    for el in elements:
        m = (el.get("intent") or {}).get("move") or "?"
        counts[m] = counts.get(m, 0) + 1
    return counts


def preserve_cartographer_intent(elements, previous):
    """Single-writer: Cartographer owns occurrence intent. A re-realize must not clobber it.

    Extra occurrences also keep their Cartographer binding. Their `move` exists
    because Realizer minted a second teaching act; Realizer must not wipe it on re-run.
    """
    if not previous:
        return
    prev = {e.get("element_id"): e for e in previous if e.get("element_id")}
    for el in elements:
        old = prev.get(el.get("element_id"))
        if not old:
            continue
        cart = (old.get("ext") or {}).get("cartographer")
        if not cart:
            # Extra without Cartographer yet: keep Realizer-stamped move.
            if is_extra_element(el) and (old.get("intent") or {}).get("move"):
                el.setdefault("intent", {})["move"] = old["intent"]["move"]
            continue
        if "intent" in old:
            el["intent"] = old["intent"]
        el.setdefault("ext", {})["cartographer"] = cart


def preserve_couturier_expression(elements, previous):
    """Single-writer: Couturier owns occurrence style. A re-realize must not clobber it."""
    if not previous:
        return
    prev = {e.get("element_id"): e for e in previous if e.get("element_id")}
    for el in elements:
        old = prev.get(el.get("element_id"))
        if not old:
            continue
        cout = (old.get("ext") or {}).get("couturier")
        if not cout and "expression" not in old:
            continue
        if "expression" in old:
            el["expression"] = old["expression"]
        if cout:
            el.setdefault("ext", {})["couturier"] = cout


CLOTHES_CLASS = {
    "brand.opening": "style-opening",
    "brand.instructional": "style-instructional",
    "brand.recall": "style-recall",
    "brand.purpose": "style-purpose",
    "brand.prior": "style-prior",
    "brand.example": "style-example",
    "brand.job": "style-job",
}

KICKER = {
    "title": "Opening",
    "body": "Present",
    "retrieval": "Remember",
    "purpose": "Purpose",
    "prior": "Already known",
    "example": "Example",
    "handoff": "On the job",
}


def project_html(atoms, elements, manifest, out_path: pathlib.Path):
    by_atom = {a["atom_id"]: a for a in atoms}
    esc = html.escape
    cart = manifest.get("cartographer") or {}
    counts = cart.get("move_counts") or move_counts(elements)
    mixed = len([k for k in counts if k != "?"]) > 1
    from collections import Counter, defaultdict
    cf_counts = Counter(e["composed_from"] for e in elements)
    by_cf = defaultdict(list)
    for e in elements:
        by_cf[e["composed_from"]].append(e)
    extra_n = sum(1 for e in elements if is_extra_element(e))

    def occs_for(atom_id):
        occs = list(by_cf.get(atom_id) or [])
        occs.sort(key=lambda e: (0 if is_primary_element(e) else 1, e["element_id"]))
        return occs

    def pills_for(el):
        intent = el.get("intent") or {}
        expr = el.get("expression") or {}
        move = intent.get("move", DEFAULT_MOVE)
        low = (el.get("ext") or {}).get("cartographer", {}).get("confidence") == "low"
        extra = is_extra_element(el)
        out = [f'<span class="pill move-{esc(move)}{ " low" if low else ""}">{esc(move)}</span>']
        if extra:
            out.append('<span class="pill extra-occ">extra</span>')
        if expr.get("style_ref"):
            out.append(f'<span class="pill style" title="expression.style_ref">{esc(expr["style_ref"])}</span>')
        for oid in intent.get("teaches") or []:
            short = oid[4:] if oid.startswith("obj_") else oid
            out.append(f'<span class="pill teaches" title="{esc(oid)}">{esc(short)}</span>')
        if low:
            out.append('<span class="pill dim">low-conf</span>')
        return "".join(out)

    def card_html(el, atom, extra_cls):
        meaning = clean_meaning(atom["meaning"]["source_text"])
        kind = atom["meaning"].get("kind", "")
        sh = (el.get("source_hash") or "")[:19]
        expr = el.get("expression") or {}
        clothes = CLOTHES_CLASS.get(expr.get("style_ref"), "")
        clothes_cls = f" {clothes}" if clothes else ""
        kicker = KICKER.get(expr.get("content_role"), "")
        kicker_html = f'<div class="kicker">{esc(kicker)}</div>' if kicker else ""
        meaning_tag = "h2" if expr.get("text_primitive") == "tp_display" else "p"
        tp = expr.get("text_primitive") or ""
        hint = expr.get("layout_hint") or ""
        join_bits = [
            f'composed_from <span class="mono">{esc(el["composed_from"])}</span>',
            f'source_hash <span class="mono">{esc(sh)}…</span>',
        ]
        if expr:
            join_bits.append(
                f'clothes <span class="mono">{esc(expr.get("style_ref", ""))}'
                f' · {esc(tp)} · {esc(expr.get("content_role", ""))}'
                f' · {esc(hint)}</span>'
            )
        return (
            f'<article class="occ{extra_cls}{clothes_cls}">'
            f'{kicker_html}'
            f'<div class="meta">'
            f'<span class="id">{esc(el["element_id"])}</span>'
            f'{pills_for(el)}'
            f'<span class="pill dim">{esc(el["type"])}</span>'
            f'<span class="pill dim">{esc(kind)}</span>'
            f'</div>'
            f'<{meaning_tag} class="meaning">{esc(meaning)}</{meaning_tag}>'
            f'<div class="join">{" · ".join(join_bits)}</div>'
            f'</article>'
        )

    def walk(atom, depth, acc):
        occs = occs_for(atom["atom_id"])
        if not occs:
            raise SystemExit(f"no occurrence for atom {atom['atom_id']}")
        if len(occs) > 1:
            moves = " + ".join((o.get("intent") or {}).get("move", "?") for o in occs)
            acc.append(
                f'<section class="pair d{depth}">'
                f'<div class="pair-label">1:many pair · same atom · {len(occs)} occurrences · '
                f'composed_from <span class="mono">{esc(atom["atom_id"])}</span> · '
                f'moves <span class="mono">{esc(moves)}</span></div>'
            )
            for el in occs:
                extra_cls = " extra" if is_extra_element(el) else ""
                acc.append(card_html(el, atom, extra_cls))
            acc.append("</section>")
        else:
            acc.append(card_html(occs[0], atom, f" d{depth}"))
        for ch in kids(atoms, atom["atom_id"]):
            walk(ch, depth + 1, acc)

    body = []
    for r in roots(atoms):
        walk(r, 0, body)

    rows = []
    for el in elements:
        a = by_atom[el["composed_from"]]
        teaches = ", ".join((el.get("intent") or {}).get("teaches") or []) or "—"
        pair = cf_counts[el["composed_from"]] > 1
        row_cls = " class=pair-row" if pair else ""
        many = "1:many" if pair else "1:1"
        look = (el.get("expression") or {}).get("style_ref") or "—"
        rows.append(
            f"<tr{row_cls}><td class=mono>{esc(el['element_id'])}</td>"
            f"<td class=mono>{esc(el['composed_from'])}</td>"
            f"<td>{esc((el.get('intent') or {}).get('move', ''))}</td>"
            f"<td class=mono>{esc(look)}</td>"
            f"<td class=mono>{esc(teaches)}</td>"
            f"<td>{esc(el['type'])}</td>"
            f"<td>{esc(a['meaning'].get('kind', ''))}</td>"
            f"<td>{many}</td></tr>"
        )

    rf = manifest.get("realized_from") or {}
    otm = manifest.get("one_to_many") or {}
    cout = manifest.get("couturier") or {}
    title = f"Realized lesson — {esc(manifest.get('project', 'course'))}"
    count_bits = " · ".join(f"{esc(k)} {v}" for k, v in sorted(counts.items()))
    look_counts = cout.get("look_counts") or {}
    look_bits = " · ".join(f"{esc(k)} {v}" for k, v in sorted(look_counts.items()))
    extras_bit = (f" · {extra_n} extra" + ("s" if extra_n != 1 else "")
                  + f" on {otm.get('seeded_atom_count', sum(1 for n in cf_counts.values() if n > 1))} atoms"
                  if extra_n else "")
    many_note = (
        f" Two atoms carry a second <span class=mono>ele_</span> (same "
        f"<span class=mono>composed_from</span>, distinct <span class=mono>move</span>) — grouped below. "
        if extra_n else
        " Later 1:many can mint additional elements without changing atom ids. "
    )
    clothes_note = (
        " Couturier dressed each occurrence from its <span class=mono>move</span> "
        "(<span class=mono>style_ref</span> / <span class=mono>text_primitive</span>) — "
        "hook vs present vs reinforce must not look like the same card. "
        if cout else
        " Couturier (style keys) is the next hop so different moves look like different clothes. "
    )
    if cout:
        ctrl_doc = "Couturier v1"
        ctrl_sub = f'{esc(manifest.get("project", ""))} · occurrence style bound'
        ctrl_meta = (f"{len(elements)} occurrences{extras_bit} · {look_bits or count_bits}<br>"
                     f"policy {esc(cout.get('policy', ''))}")
        banner = (
            "<b>Meaning lives on the atom.</b> Clothes come from <span class=mono>element.expression</span> "
            "(Couturier). Intent (<span class=mono>move</span>, <span class=mono>teaches</span>) is "
            "Cartographer’s. The Realizer minted the <span class=mono>ele_</span> ids and copied no authored "
            f"<span class=mono>content.text</span>.{many_note}{clothes_note}"
            "Dragoman / Storyline / PNG render are not this hop."
        )
        projector = (f"{esc(REALIZER)} + {esc(cart.get('tool', 'tools/cartographer.py'))} + "
                     f"{esc(cout.get('tool', 'tools/couturier.py'))}")
    elif cart:
        ctrl_doc = "Cartographer v1"
        ctrl_sub = f'{esc(manifest.get("project", ""))} · occurrence intent bound'
        ctrl_meta = (f"{len(elements)} occurrences{extras_bit} · {count_bits}<br>"
                     f"policy {esc(cart.get('policy', ''))}")
        banner = (
            "<b>Meaning lives on the atom.</b> Occurrence intent "
            "(<span class=mono>move</span>, <span class=mono>teaches</span>) is Cartographer’s. "
            "v1 is a documented heuristic compiler, not ID genius — low-confidence pills are flagged. "
            "The Realizer minted the <span class=mono>ele_</span> ids and copied no authored "
            f"<span class=mono>content.text</span>.{many_note}{clothes_note}"
            "Dragoman / PNG render are not this hop."
        )
        projector = f"{esc(REALIZER)} + {esc(cart.get('tool', 'tools/cartographer.py'))}"
    else:
        ctrl_doc = "Realizer v1"
        ctrl_sub = f'{esc(manifest.get("project", ""))} · occurrence hop'
        ctrl_meta = (f"{len(elements)} occurrences{extras_bit} · default move "
                     f"<b>{esc(manifest.get('default_move', DEFAULT_MOVE))}</b><br>"
                     f"policy {esc(manifest.get('policy', POLICY))}")
        banner = (
            "<b>Meaning lives on the atom.</b> Each card is one occurrence "
            "(<span class=mono>ele_</span>), linked by <span class=mono>composed_from</span>. "
            "The Realizer copied no authored <span class=mono>content.text</span>. Ugly typography "
            f"is v1.{many_note}{clothes_note}"
            "Dragoman / PNG render are not this hop."
        )
        projector = esc(REALIZER)
    HTML = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
:root{{--ink:#0f172a;--mut:#64748b;--line:#e2e8f0;--bg:#f8fafc;--accent:#1e3a8a}}
*{{box-sizing:border-box}}
body{{font:15px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);
 margin:0;background:var(--bg)}}
.page{{max-width:920px;margin:0 auto;background:#fff;padding:40px 48px;
 box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.ctrl{{display:flex;justify-content:space-between;align-items:flex-start;
 border-bottom:2px solid var(--accent);padding-bottom:14px;margin-bottom:8px}}
.ctrl .doc{{font-weight:700;font-size:19px;color:var(--accent)}}
.ctrl .meta{{text-align:right;font-size:12.5px;color:var(--mut)}}
.banner{{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:10px 14px;
 font-size:12.5px;color:#1e3a8a;margin:14px 0 22px}}
h1{{font-size:20px;margin:8px 0 4px}}
.occ{{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:8px 0}}
.d1{{margin-left:18px}}.d2{{margin-left:36px}}.d3{{margin-left:54px}}.d4{{margin-left:72px}}
.occ .meta{{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:6px}}
.id{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;font-weight:600}}
.pill{{background:#1e3a8a;color:#fff;border-radius:999px;padding:1px 8px;font-size:11px;
 text-transform:uppercase;letter-spacing:.03em}}
.pill.dim{{background:#e2e8f0;color:#334155}}
.pill.teaches{{background:#e0e7ff;color:#3730a3;text-transform:none;letter-spacing:0}}
.pill.low{{box-shadow:0 0 0 2px #f59e0b inset}}
.pill.move-hook{{background:#b45309}}
.pill.move-objective{{background:#047857}}
.pill.move-activate{{background:#0f766e}}
.pill.move-present{{background:#1e3a8a}}
.pill.move-exemplify{{background:#6d28d9}}
.pill.move-practice{{background:#be123c}}
.pill.move-feedback{{background:#9f1239}}
.pill.move-assess{{background:#7f1d1d}}
.pill.move-reinforce{{background:#334155}}
.pill.move-transfer{{background:#c2410c}}
.pill.extra-occ{{background:#0f766e;text-transform:none}}
.pair{{border:2px solid #1e3a8a;border-radius:10px;padding:10px 12px 6px;margin:12px 0;
 background:#f1f5f9}}
.pair-label{{font-size:12px;color:#1e3a8a;font-weight:600;margin:0 0 8px}}
.pair .occ{{background:#fff}}
.occ.extra{{background:#fffbeb;border-color:#f59e0b}}
.pill.style{{background:#fef3c7;color:#92400e;text-transform:none;letter-spacing:0}}
.kicker{{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
 margin:0 0 8px;color:inherit;opacity:.85}}
.occ.style-opening{{background:linear-gradient(135deg,#b45309,#d97706);color:#fff;border:none;
 border-radius:4px;padding:28px 24px 22px;text-align:center}}
.occ.style-opening .id,.occ.style-opening .join,.occ.style-opening .pill.dim{{color:#fde68a}}
.occ.style-opening .meaning{{font-size:22px;font-weight:700;line-height:1.25;letter-spacing:-.02em;
 margin:8px 0 10px}}
.occ.style-opening .kicker{{color:#fffbeb;opacity:1}}
.occ.style-instructional{{background:#fff;border:1px solid #cbd5e1;border-left:5px solid #1e3a8a;
 border-radius:6px;padding:14px 16px}}
.occ.style-instructional .meaning{{font-size:15px;line-height:1.55}}
.occ.style-recall{{background:#f8fafc;border:2px dashed #64748b;border-radius:4px;padding:16px 18px}}
.occ.style-recall .meaning{{font-size:14px;font-style:italic;color:#334155;
 border-left:3px solid #94a3b8;padding:4px 0 4px 12px}}
.occ.style-recall .kicker{{color:#475569}}
.occ.style-purpose{{background:#ecfdf5;border:1px solid #059669;border-left:6px solid #047857;
 border-radius:6px}}
.occ.style-purpose .meaning{{font-weight:600}}
.occ.style-purpose .kicker{{color:#047857}}
.occ.style-prior{{background:#f0fdfa;border:1px solid #0f766e;border-radius:6px;font-size:14px}}
.occ.style-prior .kicker{{color:#0f766e}}
.occ.style-example{{background:#faf5ff;border:1px solid #c4b5fd;border-radius:6px;padding:12px 14px 12px 18px}}
.occ.style-example .meaning{{font-family:Georgia,Times,serif;font-size:14px}}
.occ.style-example .kicker{{color:#6d28d9}}
.occ.style-job{{background:#fff7ed;border:1px solid #c2410c;border-left:6px solid #c2410c;border-radius:6px}}
.occ.style-job .kicker{{color:#c2410c}}
tr.pair-row td{{background:#eff6ff}}
.meaning{{margin:4px 0 6px}}
.join{{font-size:12px;color:var(--mut)}}
.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px}}
table{{border-collapse:collapse;width:100%;margin:8px 0;font-size:12.5px}}
th,td{{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}}
th{{background:#f1f5f9;font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:#475569}}
details{{margin-top:28px;border-top:1px dashed var(--line);padding-top:14px}}
summary{{cursor:pointer;color:var(--mut);font-size:12.5px}}
.foot{{margin-top:28px;font-size:11.5px;color:var(--mut);border-top:1px solid var(--line);
 padding-top:12px}}
</style></head><body><div class=page>
<div class=ctrl>
 <div><div class=doc>{ctrl_doc}</div>
 <div style="font-size:12.5px;color:var(--mut)">{ctrl_sub}</div></div>
 <div class=meta>{ctrl_meta}</div>
</div>
<h1>Realized lesson</h1>
<div class=banner>{banner}</div>
{''.join(body)}
<details><summary>Occurrence index — {len(elements)} ele_ records (click to expand)</summary>
<table><thead><tr><th>element_id</th><th>composed_from</th><th>move</th><th>style_ref</th><th>teaches</th><th>type</th><th>atom kind</th><th>arity</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></details>
<div class=foot>Atom store: {esc(str(rf.get("atom_store", "")))} ·
atoms_sha256 {esc(str(rf.get("atoms_sha256", ""))[:19])}…<br>
Projector: {projector} · this HTML is regenerated, never hand-edited.
Meaning is read from atoms.json. Occurrence intent is Cartographer’s when bound.
Clothes are Couturier’s when bound (expression keys, not authored text).
{"Moves are mixed." if mixed else "All moves still share one value — run tools/cartographer.py."}
{" 1:many pairs share composed_from." if extra_n else ""}
{" Clothes are mixed." if cout and len(look_counts) > 1 else (" Run tools/couturier.py to dress occurrences." if not cout else "")}</div>
</div></body></html>"""
    out_path.write_text(HTML)


def selftest(closed_moves):
    """Tiny fixture: extra ids are stable, 1:many shares composed_from, re-run keeps extras."""
    results = []

    def atom(aid, kind, text, parent=None, order=0):
        a = {
            "atom_id": aid,
            "content_hash": "sha256:" + ("a" * 64),
            "meaning": {"source_locale": "en", "source_text": text, "kind": kind},
            "bindings": {},
            "governance": {"version": 1, "status": "draft"},
        }
        if parent:
            a["bindings"]["object"] = {"belongs_to": parent, "order": order}
        return a

    title = atom("atom_sop_x", "procedure", "SOP-X — Do the thing.")
    general = atom("atom_sop_x_general", "procedure", "X is the framework.", "atom_sop_x", 0)
    other = atom("atom_sop_x_other", "procedure", "A 1:1 leftover.", "atom_sop_x", 1)

    primary = mint_element(title, DEFAULT_MOVE, role="primary")
    extra = mint_element(title, "reinforce", role="extra")
    results.append(("primary id is ele_ + suffix",
                    primary["element_id"] == "ele_sop_x", primary["element_id"]))
    results.append(("extra id is primary + __move",
                    extra["element_id"] == "ele_sop_x__reinforce", extra["element_id"]))
    results.append(("same composed_from", extra["composed_from"] == primary["composed_from"] == "atom_sop_x",
                    extra["composed_from"]))
    results.append(("distinct moves", extra["intent"]["move"] != primary["intent"]["move"]
                    and extra["intent"]["move"] == "reinforce", extra["intent"]["move"]))
    results.append(("no authored content on extra", "content" not in extra, ""))
    results.append(("extra role stamped", extra["ext"]["realized_from"]["role"] == "extra", ""))
    results.append(("reinforce is closed vocab", extra["intent"]["move"] in closed_moves, extra["intent"]["move"]))

    # assemble with a local seed override via previous extras + seed atoms that exist
    orig_seed = ONE_TO_MANY_SEED
    try:
        # Can't mutate the tuple in place; assemble reads the module-level seed.
        # Drive extras via a previous extra + seed atoms that match the real seed ids? Those
        # atoms are not in this fixture. Instead, plant a previous extra and rely on preserve.
        prev_extra = mint_element(general, "reinforce", role="extra")
        prev_primary_g = mint_element(general, DEFAULT_MOVE, role="primary")
        previous = [primary, extra, prev_primary_g, prev_extra]
        assembled = assemble_elements([title, general, other], previous, DEFAULT_MOVE, mint_extras=False)
        ids = [e["element_id"] for e in assembled]
        results.append(("re-run without seed keeps planted extras",
                        "ele_sop_x__reinforce" in ids and "ele_sop_x_general__reinforce" in ids, ids))
        results.append(("1:1 atom stays singleton",
                        sum(1 for e in assembled if e["composed_from"] == "atom_sop_x_other") == 1, ""))
        results.append(("title has two occs",
                        sum(1 for e in assembled if e["composed_from"] == "atom_sop_x") == 2, ""))
        # Cartographer stamp survives re-realize
        extra["ext"]["cartographer"] = {"policy": "v1_heuristic_compiler", "tool": "tools/cartographer.py",
                                        "confidence": "high", "flags": ["extra_occurrence_move_preserved"]}
        extra["intent"]["teaches"] = ["obj_explain_alsap_purpose"]
        extra["intent"]["move"] = "reinforce"
        extra["expression"] = {
            "style_ref": "brand.recall",
            "text_primitive": "tp_recall",
            "content_role": "retrieval",
            "layout_hint": "recap",
        }
        extra["ext"]["couturier"] = {
            "policy": "v1_move_to_look",
            "tool": "tools/couturier.py",
            "from_move": "reinforce",
        }
        assembled2 = assemble_elements([title, general, other], [primary, extra, prev_primary_g, prev_extra],
                                       DEFAULT_MOVE, mint_extras=False)
        kept = next(e for e in assembled2 if e["element_id"] == "ele_sop_x__reinforce")
        results.append(("re-realize preserves extra move", kept["intent"]["move"] == "reinforce",
                        kept["intent"].get("move")))
        results.append(("re-realize preserves extra teaches",
                        kept["intent"].get("teaches") == ["obj_explain_alsap_purpose"],
                        kept["intent"].get("teaches")))
        results.append(("re-realize preserves cartographer stamp",
                        "cartographer" in kept.get("ext", {}), ""))
        results.append(("re-realize preserves couturier stamp",
                        "couturier" in kept.get("ext", {}), ""))
        results.append(("re-realize preserves expression style_ref",
                        (kept.get("expression") or {}).get("style_ref") == "brand.recall",
                        (kept.get("expression") or {}).get("style_ref")))
        results.append(("ids stable across re-run",
                        {e["element_id"] for e in assembled} == {e["element_id"] for e in assembled2}, ""))
    finally:
        assert ONE_TO_MANY_SEED is orig_seed

    print(f"{'CHECK':<72} RESULT")
    print("-" * 86)
    ok = True
    for name, passed, detail in results:
        ok = ok and passed
        print(f"{name:<72} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
    print("-" * 86)
    print("SELFTEST ALL PASS" if ok else "SELFTEST FAILED")
    if not ok:
        raise SystemExit(1)


def main():
    # --selftest must not require a project store.
    if "--selftest" in sys.argv[1:]:
        inject_default_project()
        P = harness_paths.resolve_core(None)
        element_schema = load(P["schemas_dir"] / "element.schema.json")
        closed_moves = list(element_schema["properties"]["intent"]["properties"]["move"]["enum"])
        for _aid, mv in ONE_TO_MANY_SEED:
            if mv not in closed_moves:
                raise SystemExit(f"seed move {mv!r} is not in the closed vocab")
        selftest(closed_moves)
        return

    inject_default_project()
    default_shown = os.environ.get("TRAINSTORM_PROJECT") or (
        str(repo_default_project()) if repo_default_project() else "(pass --project)"
    )
    ap = argparse.ArgumentParser(
        description="Realizer v1 — mint occurrence elements (1:1 default + small 1:many seed) and project a lesson HTML.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="From cgen/trainstorm-core:\n"
               "  python tools/realize.py\n"
               "  python3 tools/realize.py --project ../astellas/projects/ast_alsap\n"
               "  python3 tools/realize.py --selftest\n"
               "  python3 tools/cartographer.py\n"
               "  python3 tools/couturier.py\n",
    )
    ap.add_argument("--project", default=None,
                    help=f"Atom store directory containing atoms.json (default: {default_shown})")
    ap.add_argument("--core", default=None, help="trainstorm-core (schemas + vocab); usually auto-detected")
    ap.add_argument("--registry", default=None, help="Client registry; usually auto-derived from --project")
    ap.add_argument("--out", help="HTML output path (default: <project>/realized_lesson.html)")
    ap.add_argument("--store", help="Occurrence store directory (default: <project>/occurrences)")
    ap.add_argument("--move", default=DEFAULT_MOVE,
                    help=f"Closed pedagogical move for every v1 primary occurrence (default: {DEFAULT_MOVE})")
    ap.add_argument("--selftest", action="store_true", help="Run the 1:many minting fixture and exit")
    ap.add_argument("--no-one-to-many", action="store_true",
                    help="Do not mint new extras from the seed; still preserve extras already in the store")
    args = ap.parse_args()  # harness_paths re-reads --project/--core/--registry from argv

    P = harness_paths.resolve()
    print(harness_paths.announce(P))
    project = P["project_dir"]
    schemas = P["schemas_dir"]
    atoms_path = project / "atoms.json"
    if not atoms_path.exists():
        raise SystemExit(f"No atoms.json in project store: {project}")

    atoms_bytes = atoms_path.read_bytes()
    atoms_hash_before = sha256_bytes(atoms_bytes)
    atoms = json.loads(atoms_bytes)
    if not isinstance(atoms, list) or not atoms:
        raise SystemExit(f"{atoms_path} is not a non-empty atom list")
    atoms_by_id = {a["atom_id"]: a for a in atoms if "atom_id" in a}
    if len(atoms_by_id) != len(atoms):
        raise SystemExit("atom store has missing or duplicate atom_id values")

    element_schema = load(schemas / "element.schema.json")
    closed_moves = list(element_schema["properties"]["intent"]["properties"]["move"]["enum"])
    move = args.move
    if move not in closed_moves:
        raise SystemExit(f"--move {move!r} is not in the closed vocab: {closed_moves}")
    for _aid, mv in ONE_TO_MANY_SEED:
        if mv not in closed_moves:
            raise SystemExit(f"seed move {mv!r} is not in the closed vocab: {closed_moves}")

    store_dir = pathlib.Path(args.store).resolve() if args.store else project / "occurrences"
    previous = []
    prev_path = store_dir / "elements.json"
    prev_mf = {}
    if prev_path.exists() and prev_path.resolve() != atoms_path.resolve():
        previous = load(prev_path)
        if not isinstance(previous, list):
            previous = []
        mf_prev_path = store_dir / "manifest.json"
        if mf_prev_path.exists():
            prev_mf = load(mf_prev_path)

    mint_extras = not args.no_one_to_many
    elements = assemble_elements(atoms, previous, move, mint_extras=mint_extras)
    validate_elements(elements, element_schema, atoms_by_id)

    primaries = [e for e in elements if is_primary_element(e)]
    extras = [e for e in elements if is_extra_element(e)]
    if len(primaries) != len(atoms):
        raise SystemExit(f"every atom needs one primary occurrence; got {len(primaries)} vs {len(atoms)}")
    from collections import defaultdict
    moves_by_atom = defaultdict(set)
    for e in elements:
        moves_by_atom[e["composed_from"]].add((e.get("intent") or {}).get("move"))
    for aid, mvset in moves_by_atom.items():
        if len([e for e in elements if e["composed_from"] == aid]) > 1 and len(mvset) < 2:
            raise SystemExit(f"{aid}: 1:many occurrences must have distinct moves; got {sorted(mvset)}")

    store_dir.mkdir(parents=True, exist_ok=True)
    elements_path = store_dir / "elements.json"
    if elements_path.resolve() == atoms_path.resolve():
        raise SystemExit("refusing to overwrite atoms.json")

    mf_path = project / "manifest.json"
    project_name = load(mf_path).get("project", project.name) if mf_path.exists() else project.name
    seeded_present = [
        {"atom_id": aid, "extra_element_id": mint_extra_element_id(aid, mv), "move": mv}
        for aid, mv in ONE_TO_MANY_SEED if aid in atoms_by_id
    ]
    occ_manifest = {
        "store": "occurrences",
        "project": project_name,
        "policy": STORE_POLICY if extras else POLICY,
        "default_move": move,
        "element_count": len(elements),
        "generated_by": REALIZER,
        "realized_from": {
            "atom_store": portable_atom_store_path(atoms_path),
            "atom_count": len(atoms),
            "atoms_sha256": atoms_hash_before,
        },
        "one_to_many": {
            "spec": "agents/realizer/one_to_many_v1.md",
            "seeded_atom_count": len({s["atom_id"] for s in seeded_present}),
            "extra_count": len(extras),
            "seed": seeded_present,
            "note": ("Small honest seed, not the whole SOP. Extra ele_ ids are stable. "
                     "Re-run accretes missing extras and never drops existing extras, "
                     "Cartographer bindings, or Couturier style."),
        },
        "note": ("Primary: one ele_ per atom. 1:many seed mints extra occurrences of a couple "
                 "of teaching-worthy atoms (same composed_from, distinct move, no authored "
                 "content.text). Cartographer owns occurrence intent; Couturier owns expression "
                 "style. A re-realize preserves both plus extra ele_ records."),
    }
    if any((e.get("ext") or {}).get("cartographer") for e in elements):
        cart = dict(prev_mf.get("cartographer") or {})
        cart["move_counts"] = move_counts(elements)
        cart["teaches_bound"] = sum(1 for e in elements if (e.get("intent") or {}).get("teaches"))
        cart["low_confidence"] = sum(
            1 for e in elements
            if (e.get("ext") or {}).get("cartographer", {}).get("confidence") == "low"
        )
        cart["element_count"] = len(elements)
        occ_manifest["cartographer"] = cart
    if any((e.get("ext") or {}).get("couturier") for e in elements):
        from collections import Counter
        cout = dict(prev_mf.get("couturier") or {})
        cout["look_counts"] = dict(sorted(Counter(
            (e.get("expression") or {}).get("style_ref") or "undressed" for e in elements
        ).items()))
        cout["dressed"] = sum(1 for e in elements if e.get("expression"))
        cout["element_count"] = len(elements)
        occ_manifest["couturier"] = cout
    elements_path.write_text(json.dumps(elements, indent=2) + "\n")
    (store_dir / "manifest.json").write_text(json.dumps(occ_manifest, indent=2) + "\n")

    html_path = pathlib.Path(args.out).resolve() if args.out else project / "realized_lesson.html"
    project_html(atoms, elements, occ_manifest, html_path)

    atoms_hash_after = sha256_bytes(atoms_path.read_bytes())
    if atoms_hash_after != atoms_hash_before:
        raise SystemExit("atoms.json changed during realize — abort. Realizer must not rewrite atoms.")

    print(f"Realizer v1 → {len(elements)} elements ({occ_manifest['policy']}, default_move={move})")
    print(f"  atoms      : {atoms_path} ({len(atoms)} records, unchanged)")
    print(f"  primaries  : {len(primaries)}")
    print(f"  extras     : {len(extras)} ({', '.join(e['element_id'] + '=' + (e.get('intent') or {}).get('move', '?') for e in extras) or 'none'})")
    print(f"  occurrences: {elements_path}")
    print(f"  manifest   : {store_dir / 'manifest.json'}")
    print(f"  lesson HTML: {html_path}")
    print("  schema     : element.schema.json ALL PASS (no authored content.text)")


if __name__ == "__main__":
    main()
