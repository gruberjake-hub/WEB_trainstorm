#!/usr/bin/env python3
"""
Realizer v1 — atoms → occurrence elements + a double-clickable HTML lesson.

The Realizer is the typesetter of meaning (`architecture/agents-roster.md`). v1 is
deterministic and ugly on purpose: **one occurrence per atom**, default move `present`.
It does not invent authored text. Display HTML reads meaning from the atom via
`composed_from`. 1:many (preview / teach / retrieve) can accrete more `ele_` records
later without changing atom ids. Cartographer is not required for this hop.

This is the first course hop. The pipeline's `atom → primitives` transform is still
owed; v1 realizes the live atom store directly so the occurrence graph can start.

Not this tool: Couturier (style keys), Dragoman (locale packs), Storyline, .potx,
PNG pipelines, `tools/render/`. Does not rewrite SOP/form atoms into elements —
`atoms.json` is read-only.

Usage (from `cgen/trainstorm-core`):

    python tools/realize.py
    python tools/realize.py --project ../astellas/projects/ast_alsap
    python tools/realize.py --project ../astellas/projects/alsap

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
REALIZER = "tools/realize.py"
DEFAULT_MOVE = "present"
ELE_ID_RE = re.compile(r"^ele_[A-Za-z0-9_-]+$")

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


def mint_element(atom, move: str) -> dict:
    aid = atom["atom_id"]
    obj = (atom.get("bindings") or {}).get("object") or {}
    typ = element_type(atom)
    realized_from = {
        "atom_id": aid,
        "realizer": REALIZER,
        "policy": POLICY,
    }
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
        "element_id": mint_element_id(aid),
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
    """Single-writer: Cartographer owns occurrence intent. A re-realize must not clobber it."""
    if not previous:
        return
    prev = {e.get("element_id"): e for e in previous if e.get("element_id")}
    for el in elements:
        old = prev.get(el.get("element_id"))
        if not old:
            continue
        cart = (old.get("ext") or {}).get("cartographer")
        if not cart:
            continue
        if "intent" in old:
            el["intent"] = old["intent"]
        el.setdefault("ext", {})["cartographer"] = cart


def project_html(atoms, elements, manifest, out_path: pathlib.Path):
    by_atom = {a["atom_id"]: a for a in atoms}
    by_ele = {e["element_id"]: e for e in elements}
    esc = html.escape
    cart = manifest.get("cartographer") or {}
    counts = cart.get("move_counts") or move_counts(elements)
    mixed = len([k for k in counts if k != "?"]) > 1

    def pills_for(el):
        intent = el.get("intent") or {}
        move = intent.get("move", DEFAULT_MOVE)
        low = (el.get("ext") or {}).get("cartographer", {}).get("confidence") == "low"
        out = [f'<span class="pill move-{esc(move)}{ " low" if low else ""}">{esc(move)}</span>']
        for oid in intent.get("teaches") or []:
            short = oid[4:] if oid.startswith("obj_") else oid
            out.append(f'<span class="pill teaches" title="{esc(oid)}">{esc(short)}</span>')
        if low:
            out.append('<span class="pill dim">low-conf</span>')
        return "".join(out)

    def walk(atom, depth, acc):
        el = by_ele[mint_element_id(atom["atom_id"])]
        meaning = clean_meaning(atom["meaning"]["source_text"])
        kind = atom["meaning"].get("kind", "")
        sh = (el.get("source_hash") or "")[:19]
        acc.append(
            f'<article class="occ d{depth}">'
            f'<div class="meta">'
            f'<span class="id">{esc(el["element_id"])}</span>'
            f'{pills_for(el)}'
            f'<span class="pill dim">{esc(el["type"])}</span>'
            f'<span class="pill dim">{esc(kind)}</span>'
            f'</div>'
            f'<p class="meaning">{esc(meaning)}</p>'
            f'<div class="join">composed_from <span class="mono">{esc(el["composed_from"])}</span>'
            f' · source_hash <span class="mono">{esc(sh)}…</span></div>'
            f'</article>'
        )
        for ch in kids(atoms, atom["atom_id"]):
            walk(ch, depth + 1, acc)

    body = []
    for r in roots(atoms):
        walk(r, 0, body)

    rows = []
    for el in elements:
        a = by_atom[el["composed_from"]]
        teaches = ", ".join((el.get("intent") or {}).get("teaches") or []) or "—"
        rows.append(
            f"<tr><td class=mono>{esc(el['element_id'])}</td>"
            f"<td class=mono>{esc(el['composed_from'])}</td>"
            f"<td>{esc((el.get('intent') or {}).get('move', ''))}</td>"
            f"<td class=mono>{esc(teaches)}</td>"
            f"<td>{esc(el['type'])}</td>"
            f"<td>{esc(a['meaning'].get('kind', ''))}</td></tr>"
        )

    rf = manifest.get("realized_from") or {}
    title = f"Realized lesson — {esc(manifest.get('project', 'course'))}"
    count_bits = " · ".join(f"{esc(k)} {v}" for k, v in sorted(counts.items()))
    if cart:
        ctrl_doc = "Cartographer v1"
        ctrl_sub = f'{esc(manifest.get("project", ""))} · occurrence intent bound'
        ctrl_meta = (f"{len(elements)} occurrences · {count_bits}<br>"
                     f"policy {esc(cart.get('policy', ''))}")
        banner = (
            "<b>Meaning lives on the atom.</b> Occurrence intent "
            "(<span class=mono>move</span>, <span class=mono>teaches</span>) is Cartographer’s. "
            "v1 is a documented heuristic compiler, not ID genius — low-confidence pills are flagged. "
            "The Realizer minted the <span class=mono>ele_</span> ids and copied no authored "
            "<span class=mono>content.text</span>. Couturier / Dragoman / PNG render are not this hop."
        )
        projector = f"{esc(REALIZER)} + {esc(cart.get('tool', 'tools/cartographer.py'))}"
    else:
        ctrl_doc = "Realizer v1"
        ctrl_sub = f'{esc(manifest.get("project", ""))} · occurrence hop'
        ctrl_meta = (f"{len(elements)} occurrences · move "
                     f"<b>{esc(manifest.get('default_move', DEFAULT_MOVE))}</b><br>"
                     f"policy {esc(POLICY)}")
        banner = (
            "<b>Meaning lives on the atom.</b> Each card is one occurrence "
            "(<span class=mono>ele_</span>), linked by <span class=mono>composed_from</span>. "
            "The Realizer copied no authored <span class=mono>content.text</span>. Ugly typography "
            "is v1. Later 1:many can mint preview/teach/retrieve as additional elements without "
            "changing atom ids. Couturier / Dragoman / PNG render are not this hop."
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
<table><thead><tr><th>element_id</th><th>composed_from</th><th>move</th><th>teaches</th><th>type</th><th>atom kind</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></details>
<div class=foot>Atom store: {esc(str(rf.get("atom_store", "")))} ·
atoms_sha256 {esc(str(rf.get("atoms_sha256", ""))[:19])}…<br>
Projector: {projector} · this HTML is regenerated, never hand-edited.
Meaning is read from atoms.json. Occurrence intent is Cartographer’s when bound.
{"Moves are mixed." if mixed else "All moves still share one value — run tools/cartographer.py."}</div>
</div></body></html>"""
    out_path.write_text(HTML)


def main():
    inject_default_project()
    default_shown = os.environ.get("TRAINSTORM_PROJECT") or (
        str(repo_default_project()) if repo_default_project() else "(pass --project)"
    )
    ap = argparse.ArgumentParser(
        description="Realizer v1 — mint one occurrence element per atom and project a lesson HTML.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="From cgen/trainstorm-core:\n"
               "  python tools/realize.py\n"
               "  python3 tools/realize.py --project ../astellas/projects/ast_alsap\n",
    )
    ap.add_argument("--project", default=None,
                    help=f"Atom store directory containing atoms.json (default: {default_shown})")
    ap.add_argument("--core", default=None, help="trainstorm-core (schemas + vocab); usually auto-detected")
    ap.add_argument("--registry", default=None, help="Client registry; usually auto-derived from --project")
    ap.add_argument("--out", help="HTML output path (default: <project>/realized_lesson.html)")
    ap.add_argument("--store", help="Occurrence store directory (default: <project>/occurrences)")
    ap.add_argument("--move", default=DEFAULT_MOVE,
                    help=f"Closed pedagogical move for every v1 occurrence (default: {DEFAULT_MOVE})")
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

    elements = [mint_element(a, move) for a in atoms]
    preserve_cartographer_intent(elements, previous)
    validate_elements(elements, element_schema, atoms_by_id)
    if len(elements) != len(atoms):
        raise SystemExit(f"v1 policy is one occurrence per atom; got {len(elements)} vs {len(atoms)}")

    store_dir.mkdir(parents=True, exist_ok=True)
    elements_path = store_dir / "elements.json"
    if elements_path.resolve() == atoms_path.resolve():
        raise SystemExit("refusing to overwrite atoms.json")

    mf_path = project / "manifest.json"
    project_name = load(mf_path).get("project", project.name) if mf_path.exists() else project.name
    occ_manifest = {
        "store": "occurrences",
        "project": project_name,
        "policy": POLICY,
        "default_move": move,
        "element_count": len(elements),
        "generated_by": REALIZER,
        "realized_from": {
            "atom_store": portable_atom_store_path(atoms_path),
            "atom_count": len(atoms),
            "atoms_sha256": atoms_hash_before,
        },
        "note": ("v1 mints one ele_ per atom. 1:many can accrete more elements later "
                 "without changing atom ids. Meaning is not copied onto the occurrence. "
                 "Cartographer owns occurrence intent; a re-realize preserves ext.cartographer."),
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
    elements_path.write_text(json.dumps(elements, indent=2) + "\n")
    (store_dir / "manifest.json").write_text(json.dumps(occ_manifest, indent=2) + "\n")

    html_path = pathlib.Path(args.out).resolve() if args.out else project / "realized_lesson.html"
    project_html(atoms, elements, occ_manifest, html_path)

    atoms_hash_after = sha256_bytes(atoms_path.read_bytes())
    if atoms_hash_after != atoms_hash_before:
        raise SystemExit("atoms.json changed during realize — abort. Realizer must not rewrite atoms.")

    print(f"Realizer v1 → {len(elements)} elements ({POLICY}, move={move})")
    print(f"  atoms      : {atoms_path} ({len(atoms)} records, unchanged)")
    print(f"  occurrences: {elements_path}")
    print(f"  manifest   : {store_dir / 'manifest.json'}")
    print(f"  lesson HTML: {html_path}")
    print("  schema     : element.schema.json ALL PASS (no authored content.text)")


if __name__ == "__main__":
    main()
