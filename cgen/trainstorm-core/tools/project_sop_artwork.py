#!/usr/bin/env python3
"""
Projector — ast_artwork atoms -> controlled SOP HTML.

Sibling of project_sop.py (ALSAP-hardcoded). Deterministic walk; no authored
meaning. Roles/docs that are only proposed resolve to the proposal label,
never silently into the governed registries.
"""
import html, json, pathlib

STORE = pathlib.Path(__file__).resolve().parent.parent.parent / "astellas" / "projects" / "ast_artwork"
REG = STORE.parent.parent / "registry"
OUT = STORE / "controlled_sop_2290.html"

atoms = {a["atom_id"]: a for a in json.loads((STORE / "atoms.json").read_text())}
manifest = json.loads((STORE / "manifest.json").read_text())
proposed = json.loads((STORE / "proposed_registry_extensions.json").read_text())
roles_reg = json.loads((REG / "roles.registry.json").read_text())
docs_reg = json.loads((REG / "docs.registry.json").read_text())

LABEL, DESC = {}, {}
for e in roles_reg["roles"]:
    LABEL[e["id"]] = e["label"]
    DESC[e["id"]] = e.get("description", "")
for e in proposed.get("roles", []):
    LABEL.setdefault(e["id"], e["label"])
    DESC.setdefault(e["id"], e.get("note", "") + " [proposed]")
for e in proposed.get("records", []):
    LABEL.setdefault(e["id"], e["label"])
DOCLABEL = {d["id"]: d["label"] for d in docs_reg["docs"]}
DOCNUM = {d["id"]: d["source_number"] for d in docs_reg["docs"]}
for d in proposed.get("docs", []):
    DOCLABEL.setdefault(d["id"], d["label"])
    DOCNUM.setdefault(d["id"], d.get("source_number", d["id"]))

R = "atom_sop_2290"


def kids(parent):
    ch = [a for a in atoms.values()
          if a["bindings"].get("object", {}).get("belongs_to") == parent]
    return sorted(ch, key=lambda a: a["bindings"]["object"].get("order", 0))


def esc(s):
    return html.escape(s or "")


def clean(text):
    i = text.find("[Headwater")
    return text[:i].strip() if i != -1 else text.strip()


def label(idn):
    if idn in LABEL:
        return LABEL[idn]
    return idn.split("_", 1)[-1].replace("_", " ").title()


BADGE = {"action": "#2563eb", "decision": "#b45309", "verification": "#047857"}
rows_trace = []


def render_steps(section):
    out = ['<table class="steps"><thead><tr><th>#</th><th>Responsibility</th>'
           '<th>Action</th><th>Type</th></tr></thead><tbody>']
    for i, s in enumerate(kids(section["atom_id"]), 1):
        if s["meaning"]["kind"] != "procedure_step":
            continue
        proc = s["bindings"].get("procedure", {})
        roles = " / ".join(label(r) for r in proc.get("performed_by", [])) or "—"
        st = proc.get("step_type", "")
        color = BADGE.get(st, "#64748b")
        action = clean(s["meaning"]["source_text"])
        extras = []
        if proc.get("produces_records"):
            extras.append("Produces: " + ", ".join(label(x) for x in proc["produces_records"]))
        if proc.get("references"):
            extras.append("References: " + ", ".join(
                esc(f"{DOCNUM.get(x, x)}") for x in proc["references"]))
        extra_html = ("<div class='ex'>" + " &nbsp;·&nbsp; ".join(extras) + "</div>") if extras else ""
        out.append(
            f"<tr><td class='num'>{i}</td><td class='who'>{esc(roles)}</td>"
            f"<td>{esc(action)}{extra_html}</td>"
            f"<td><span class='badge' style='background:{color}'>{esc(st) or '—'}</span></td></tr>")
        rows_trace.append((s["atom_id"], s["content_hash"]))
    out.append("</tbody></table>")
    return "\n".join(out)


def render_lists(parent_id):
    out = []
    for lst in kids(parent_id):
        if lst["meaning"]["kind"] != "list":
            continue
        out.append(f"<p class='listcap'>{esc(clean(lst['meaning']['source_text']))}</p><ul>")
        for it in kids(lst["atom_id"]):
            out.append(f"<li>{esc(clean(it['meaning']['source_text']))}</li>")
            rows_trace.append((it["atom_id"], it["content_hash"]))
        out.append("</ul>")
        rows_trace.append((lst["atom_id"], lst["content_hash"]))
    return "".join(out)


root = atoms[R]
body = []
titles = {
    f"{R}_purpose": "Purpose", f"{R}_scope": "Scope", f"{R}_definitions": "Definitions",
    f"{R}_roles": "Roles and Responsibilities", f"{R}_procedures": "Procedures",
}
roman = ["I", "II", "III", "IV", "V"]
ri = 0
for sec in kids(R):
    sid = sec["atom_id"]
    if sid not in titles:
        continue
    body.append(f"<h2>{roman[ri]}. {titles[sid]}</h2>")
    ri += 1
    if sid == f"{R}_roles":
        body.append(f"<p>{esc(clean(sec['meaning']['source_text']))}</p>")
        used = sorted({r for a in atoms.values()
                       for r in a.get("bindings", {}).get("procedure", {}).get("performed_by", [])})
        body.append("<table class='roles'><thead><tr><th>Role</th><th>Note</th></tr></thead><tbody>")
        for rid in used:
            body.append(f"<tr><td class='who'>{esc(LABEL.get(rid, rid))}</td>"
                        f"<td>{esc(DESC.get(rid, ''))}</td></tr>")
        body.append("</tbody></table>")
        rows_trace.append((sid, sec["content_hash"]))
        continue
    if sid == f"{R}_procedures":
        for sub in kids(sid):
            kind = sub["meaning"]["kind"]
            text = clean(sub["meaning"]["source_text"])
            if kind == "procedure" and kids(sub["atom_id"]):
                body.append(f"<h3>{esc(text)}</h3>")
                body.append(render_steps(sub))
            else:
                body.append(f"<p>{esc(text)}</p>")
            rows_trace.append((sub["atom_id"], sub["content_hash"]))
        continue
    body.append(f"<p>{esc(clean(sec['meaning']['source_text']))}</p>")
    for child in kids(sid):
        if child["meaning"]["kind"] in ("procedure",) and child["atom_id"] not in (
                f"{R}_purpose_items", f"{R}_scope_who", f"{R}_scope_related"):
            body.append(f"<p>{esc(clean(child['meaning']['source_text']))}</p>")
            rows_trace.append((child["atom_id"], child["content_hash"]))
    body.append(render_lists(sid))
    rows_trace.append((sid, sec["content_hash"]))

ref_rows = "\n".join(
    f"<tr><td>{esc(d.get('source_number', d['id']))}</td><td>{esc(d['label'])}</td>"
    f"<td class='mono'>{esc(d['id'])} · proposed</td></tr>"
    for d in proposed.get("docs", []))
trace_rows = "\n".join(
    f"<tr><td>{esc(aid)}</td><td class='mono'>{esc(h[:19])}…</td></tr>" for aid, h in rows_trace)

HTML = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>SOP-2290 — Artwork approval (controlled projection)</title>
<style>
:root{{--ink:#0f172a;--mut:#64748b;--line:#e2e8f0;--bg:#f8fafc;--accent:#1e3a8a}}
*{{box-sizing:border-box}}
body{{font:15px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);
 margin:0;background:var(--bg)}}
.page{{max-width:900px;margin:0 auto;background:#fff;padding:48px 56px;
 box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.ctrl{{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid var(--accent);
 padding-bottom:14px;margin-bottom:8px}}
.ctrl .doc{{font-weight:700;font-size:19px;color:var(--accent)}}
.ctrl .meta{{text-align:right;font-size:12.5px;color:var(--mut)}}
.banner{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:10px 14px;
 font-size:12.5px;color:#92400e;margin:14px 0 26px}}
h1{{font-size:20px;margin:6px 0 2px}}
h2{{font-size:16px;margin:30px 0 8px;color:var(--accent);border-bottom:1px solid var(--line);padding-bottom:4px}}
h3{{font-size:14px;margin:20px 0 6px;color:#334155}}
p{{margin:8px 0}}
table{{border-collapse:collapse;width:100%;margin:8px 0 4px;font-size:13.5px}}
th,td{{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}}
th{{background:#f1f5f9;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:#475569}}
.steps .num{{width:34px;text-align:center;color:var(--mut)}}
.who{{white-space:nowrap;font-weight:600;color:#334155;width:1%}}
.badge{{color:#fff;border-radius:4px;padding:1px 7px;font-size:11px;text-transform:uppercase;letter-spacing:.02em}}
.ex{{color:var(--mut);font-size:12px;margin-top:4px}}
.listcap{{margin:10px 0 2px;color:#334155;font-weight:600;font-size:13.5px}}
ul{{margin:2px 0 10px 22px}} li{{margin:2px 0}}
.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;color:var(--mut)}}
details{{margin-top:34px;border-top:1px dashed var(--line);padding-top:14px}}
summary{{cursor:pointer;color:var(--mut);font-size:12.5px}}
.foot{{margin-top:30px;font-size:11.5px;color:var(--mut);border-top:1px solid var(--line);padding-top:12px}}
</style></head><body><div class=page>
<div class=ctrl>
 <div><div class=doc>SOP-2290</div>
 <div style="font-size:12.5px;color:var(--mut)">Artwork approval process and artwork text management</div></div>
 <div class=meta>Working id · Vault face does not print SOP number<br>
 Status: <b>DRAFT</b> (projection) · source face: Effective<br>
 Regulatory-bound · GxP controlled</div>
</div>
<h1>{esc(clean(root['meaning']['source_text']))}</h1>
<div class=banner><b>Controlled projection.</b> Deterministic projection of
{len(atoms)} content atoms. Working id <span class=mono>SOP-2290</span> — the Vault
export used for this hop does not print its own SOP number on the face
(supersedes SOP-2290 v 4.0). Roles/docs in italics-by-proposal are
<b>proposed</b>, not adopted into the governed registries. ASTELLAS CONFIDENTIAL
AND PROPRIETARY on the source face. Not ISO 14971.</div>
{''.join(body)}
<h2>VI. References (proposed — not in governed docs.registry)</h2>
<table class=refs><thead><tr><th>Document</th><th>Title</th><th>Id</th></tr></thead><tbody>{ref_rows}</tbody></table>
<details><summary>Traceability appendix — every projected element ↔ atom (click to expand)</summary>
<table><thead><tr><th>atom_id</th><th>content_hash</th></tr></thead><tbody>{trace_rows}</tbody></table>
</details>
<div class=foot>Derived from: {esc(manifest['corpus_derived_from'])} · Headwater mode:
{esc(manifest['headwater_mode'])} · Written facets: {esc(', '.join(manifest['written_facets']))} ·
Projector: tools/project_sop_artwork.py · This projection is regenerated, never hand-edited.</div>
</div></body></html>"""

OUT.write_text(HTML)
print(f"Wrote {OUT}  ({len(rows_trace)} traced elements)")
