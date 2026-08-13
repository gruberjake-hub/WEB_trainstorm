#!/usr/bin/env python3
"""
Projector — atoms -> controlled SOP document (HTML).

Deterministic walk of the atom store that rebuilds the SOP a GxP stakeholder reads and reacts to.
The atom store is the engineering source of truth; THIS document is a projection of it. Every row
traces back to an atom_id + content_hash (traceability appendix), so the model earns its status
invisibly. No meaning is authored here — only arranged.
"""
import json, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
STORE = ROOT / "store" / "projects" / "ast_alsap"
OUT = ROOT / "controlled_sop_ast29080.html"

atoms = {a["atom_id"]: a for a in json.loads((STORE / "atoms.json").read_text())}
proposed = json.loads((STORE / "proposed_registry_extensions.json").read_text())
manifest = json.loads((STORE / "manifest.json").read_text())

# role/record id -> human label (governed labels would come from the repo registries;
# here we use the proposed labels + a fallback prettifier).
LABEL = {}
for r in proposed["roles"] + proposed["records"]:
    LABEL[r["id"]] = r["label"]
DOCLABEL = {d["id"]: d["label"] for d in proposed["docs"]}
DOCNUM = {d["id"]: d["source_number"] for d in proposed["docs"]}
def label(idn):
    if idn in LABEL: return LABEL[idn]
    return idn.split("_", 1)[-1].replace("_", " ").title()

def kids(parent):
    ch = [a for a in atoms.values()
          if a["bindings"].get("object", {}).get("belongs_to") == parent]
    return sorted(ch, key=lambda a: a["bindings"]["object"].get("order", 0))

def esc(s): return html.escape(s)

def clean(text):
    # strip the inline [Headwater flag/note ...] annotations from the reader-facing projection
    i = text.find("[Headwater")
    return text[:i].strip() if i != -1 else text.strip()

R = "atom_sop_ast29080"
root = atoms[R]

BADGE = {"action": "#2563eb", "decision": "#b45309", "verification": "#047857"}

rows_trace = []

def render_steps(section):
    out = ['<table class="steps"><thead><tr><th>#</th><th>Responsibility</th>'
           '<th>Action</th><th>Type</th></tr></thead><tbody>']
    for i, s in enumerate(kids(section["atom_id"]), 1):
        proc = s["bindings"].get("procedure", {})
        roles = " / ".join(label(r) for r in proc.get("performed_by", []))
        st = proc.get("step_type", "")
        color = BADGE.get(st, "#64748b")
        action = clean(s["meaning"]["source_text"])
        extras = []
        if proc.get("produces_records"):
            extras.append("Produces: " + ", ".join(label(x) for x in proc["produces_records"]))
        if proc.get("references"):
            extras.append("References: " + ", ".join(
                esc(f"{DOCNUM.get(x, x)} ({DOCLABEL[x]})") if x in DOCLABEL else esc(x)
                for x in proc["references"]))
        if proc.get("branches"):
            extras.append("Loop: repeat until " + ", ".join(esc(b["on"]) for b in proc["branches"]))
        extra_html = ("<div class='ex'>" + " &nbsp;·&nbsp; ".join(extras) + "</div>") if extras else ""
        out.append(
            f"<tr><td class='num'>{i}</td><td class='who'>{esc(roles)}</td>"
            f"<td>{esc(action)}{extra_html}</td>"
            f"<td><span class='badge' style='background:{color}'>{esc(st)}</span></td></tr>")
        rows_trace.append((s["atom_id"], s["content_hash"]))
    out.append("</tbody></table>")
    return "\n".join(out)

# --- assemble body ---
sections = kids(R)
body = []
roman = ["I", "II", "III", "IV", "V", "VI", "VII"]
titles = {
    f"{R}_purpose": "Purpose", f"{R}_scope": "Scope", f"{R}_definitions": "Definitions",
    f"{R}_general": "General", f"{R}_roles": "Roles and Responsibilities",
    f"{R}_procedures": "Procedures",
}
ri = 0
for sec in sections:
    sid = sec["atom_id"]
    if sid not in titles:  # skip anything unexpected
        continue
    body.append(f"<h2>{roman[ri]}. {titles[sid]}</h2>")
    ri += 1
    if sid == f"{R}_roles":
        body.append("<table class='roles'><thead><tr><th>Role</th><th>Responsibility (summary)</th></tr></thead><tbody>")
        for r in proposed["roles"]:
            body.append(f"<tr><td class='who'>{esc(r['label'])}</td><td>{esc(r.get('note',''))}</td></tr>")
        body.append("</tbody></table>")
        rows_trace.append((sid, sec["content_hash"]))
        continue
    if sid == f"{R}_procedures":
        for sub in kids(sid):
            letter = chr(ord('A') + sub["bindings"]["object"]["order"])
            body.append(f"<h3>{letter}. {esc(clean(sub['meaning']['source_text']).rstrip('.').split('. ',1)[-1])}</h3>")
            body.append(render_steps(sub))
            rows_trace.append((sub["atom_id"], sub["content_hash"]))
        continue
    body.append(f"<p>{esc(clean(sec['meaning']['source_text']))}</p>")
    rows_trace.append((sid, sec["content_hash"]))

# references appendix (governed doc_ ids -> source number + title)
ref_rows = "\n".join(
    f"<tr><td>{esc(d['source_number'])}</td><td>{esc(d['label'])}</td>"
    f"<td class='mono'>{esc(d['id'])}</td></tr>" for d in proposed["docs"])

trace_rows = "\n".join(
    f"<tr><td>{esc(aid)}</td><td class='mono'>{esc(h[:19])}…</td></tr>" for aid, h in rows_trace)

HTML = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>SOP-AST-29080 — ALSAP (controlled projection)</title>
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
.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;color:var(--mut)}}
details{{margin-top:34px;border-top:1px dashed var(--line);padding-top:14px}}
summary{{cursor:pointer;color:var(--mut);font-size:12.5px}}
.foot{{margin-top:30px;font-size:11.5px;color:var(--mut);border-top:1px solid var(--line);padding-top:12px}}
</style></head><body><div class=page>
<div class=ctrl>
 <div><div class=doc>SOP-AST-29080</div>
 <div style="font-size:12.5px;color:var(--mut)">Asset Level Safety Assessment Plan (ALSAP)</div></div>
 <div class=meta>Version 1 · Status: DRAFT<br>Regulatory-bound · GxP controlled<br>
 Projection generated from atom store</div>
</div>
<h1>{esc(clean(root['meaning']['source_text']))}</h1>
<div class=banner><b>Controlled projection.</b> This document is a deterministic projection of
{len(atoms)} content atoms (the engineering source of truth). Every clause traces back to a stable
<span class=mono>atom_id</span> and <span class=mono>content_hash</span> — see the traceability
appendix. Roles/records shown in italics-by-label are <b>proposed</b> registry entries pending
adoption; this SOP is at status <b>draft</b> accordingly.</div>
{''.join(body)}
<h2>VIII. References</h2>
<table class=refs><thead><tr><th>Document</th><th>Title</th><th>Governed id</th></tr></thead><tbody>{ref_rows}</tbody></table>
<details><summary>Traceability appendix — every projected element ↔ atom (click to expand)</summary>
<table><thead><tr><th>atom_id</th><th>content_hash</th></tr></thead><tbody>{trace_rows}</tbody></table>
</details>
<div class=foot>Derived from: {esc(manifest['corpus_derived_from'])} · Headwater mode:
{esc(manifest['headwater_mode'])} · Written facets: {esc(', '.join(manifest['written_facets']))} ·
Projector: tools/project_sop.py · This projection is regenerated, never hand-edited.</div>
</div></body></html>"""

OUT.write_text(HTML)
print(f"Wrote {OUT}  ({len(rows_trace)} traced elements)")
