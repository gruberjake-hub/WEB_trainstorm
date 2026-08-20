#!/usr/bin/env python3
"""
Projector — pinned template + sparse instance overlay -> an authored ALSAP (HTML).

This is the payoff of the overlay model, and its proof. The instance store holds ONLY authored
values and decisions; every word of retained standard text in the output below is resolved from the
pinned template at render time and exists nowhere in the instance. If this document reads whole, a
sparse overlay is sufficient — and the alternative (copying 300 template atoms per asset, then
maintaining N drifting copies of controlled boilerplate) was never necessary.

    python3 tools/project_alsap.py --project <instance store> [--out <file.html>]

Four resolutions, one per content_disposition, all read off the template rather than decided here:
  controlled_standard   template text, with declared slots substituted BY MARKER (never by position)
  authorable            the authored instance value; for a controlled value set, the option's label
                        resolved live from the options registry (the prose lives there, once)
  example               template text when retained; the authored rewrite when modified
  instructional_transient   absent — deleted before final, by definition

Nothing here authors meaning; it only arranges. An unanswered slot renders as a visible TODO rather
than as silence, because a document that hides what it still owes is worse than one that is late.
"""
import json, pathlib, html, argparse, re
import harness_paths

P = harness_paths.resolve()
PROJ, TPL, REG = P["project_dir"], P.get("template_dir"), P["registry_dir"]
if TPL is None:
    raise SystemExit(f"{PROJ} declares no instantiates_template — nothing to project.")

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--out")
A, _ = ap.parse_known_args()

def load(p, d=None):
    p = pathlib.Path(p)
    return json.loads(p.read_text()) if p.exists() else d

manifest = load(PROJ / "manifest.json", {})
pin      = manifest.get("instantiates_template") or {}
tpl      = load(TPL / "atoms.json", [])
tpl_by_id = {a["atom_id"]: a for a in tpl}
inst     = load(PROJ / "atoms.json", [])
dec_doc  = load(PROJ / "instance_decisions.json", {"decisions": []})
OUT      = pathlib.Path(A.out) if A.out else PROJ / f"{manifest.get('project','alsap')}.html"

# Labels resolve from the GOVERNED registries — the law — never from a project-local copy.
roles  = {e["id"]: e for e in load(REG / "roles.registry.json", {"roles": []})["roles"]}
docs   = {e["id"]: e for e in load(REG / "docs.registry.json", {"docs": []})["docs"]}
optsets = {e["id"]: e for e in load(REG / "options.registry.json", {"options": []})["options"]}

by_key   = {(a["bindings"]["instance"]["instantiates"],
             a["bindings"]["instance"].get("fills_slot")): a
            for a in inst if "instance" in a.get("bindings", {})}
decided  = {d["instantiates"]: d for d in dec_doc.get("decisions", [])}

def form(t):  return t.get("bindings", {}).get("form", {})
def disp(t):  return form(t).get("content_disposition")
def slots(t): return form(t).get("constraints", {}).get("slots", [])
def kids(pid):
    return sorted([a for a in tpl if a.get("bindings", {}).get("object", {}).get("belongs_to") == pid],
                  key=lambda a: a.get("bindings", {}).get("object", {}).get("order", 0))

esc = html.escape
trace, stale, todo = [], [], []

def fill(t):
    """Template text with each declared slot substituted BY ITS MARKER.

    Markers are swapped for sentinels first and the whole string is escaped ONCE, before any HTML
    is spliced in — escaping per slot would re-escape the markup inserted by the slot before it.
    """
    text, reps, trailing = t["meaning"]["source_text"], [], []
    for i, s in enumerate(slots(t)):
        v = by_key.get((t["atom_id"], s["id"]))
        if v is None:
            todo.append(f"{t['atom_id']}#{s['id']} — {s['expects']}")
            rep = f'<span class=todo>[{esc(s["id"])} — not yet supplied]</span>'
        else:
            trace.append((v["atom_id"], v["content_hash"], f"fills {t['atom_id']}#{s['id']}"))
            rep = f'<span class=filled>{esc(v["meaning"]["source_text"])}</span>'
        marker = s.get("marker")
        if marker and marker in text:
            text = text.replace(marker, f"\x00{i}\x00", 1)   # literal match, never an index
            reps.append((f"\x00{i}\x00", rep))
        else:
            # No marker (a pre-v0.3 slot) — say so rather than guessing a position.
            trailing.append(f' <span class=todo>[{esc(s["id"])} declared with no marker]</span>')
    text = esc(text)
    for sentinel, rep in reps:
        text = text.replace(sentinel, rep)
    return text + "".join(trailing)

def value_html(t, v):
    """An authored value. For a controlled value set, the option's prose resolves live."""
    b = v["bindings"]["instance"]
    sv = b.get("selected_value")
    if sv:
        entry = optsets.get(form(t).get("options_ref"), {})
        opt = next((o for o in entry.get("values", []) if o["id"] == sv), None)
        if opt:
            return (f'<b>{esc(opt["label"])}</b><div class=ex>{esc(opt["description"])}</div>'
                    f'<div class=mono>value: {esc(sv)} · resolved from '
                    f'{esc(form(t).get("options_ref",""))}</div>')
    txt = esc(v["meaning"]["source_text"])
    return f'<span class=filled>{txt}</span>' if b.get("fills_slot") else txt

def render(t, depth):
    tid = t["atom_id"]
    d, dec = disp(t), decided.get(tid)
    kind = t["meaning"]["kind"]

    if d == "instructional_transient" or (dec and dec["decision"] == "deleted"):
        return ""                                   # deleted before final — and so is its subtree
    if dec and dec.get("template_source_hash") and dec["template_source_hash"] != t.get("content_hash"):
        stale.append(tid)

    out = []
    if kind in ("form", "form_section"):
        tag = "h1" if depth == 0 else ("h2" if depth == 1 else "h3")
        out.append(f"<{tag}>{esc(t['meaning']['source_text'].rstrip('.'))}</{tag}>")
        trace.append((tid, t.get("content_hash"), "template · structure"))
        for k in kids(tid):
            out.append(render(k, depth + 1))
        return "".join(out)

    # ---- a leaf field ----
    v = by_key.get((tid, None))
    if v is not None:
        b = v["bindings"]["instance"]
        if b.get("template_source_hash") != t.get("content_hash"):
            stale.append(tid)
        body, src = value_html(t, v), f"authored · {b.get('authored_by','—')}"
        trace.append((v["atom_id"], v["content_hash"], f"instantiates {tid}"))
    elif dec and dec["decision"] == "marked_not_applicable":
        body, src = "<i>Not Applicable</i>", "decision · marked_not_applicable (FORM_RULE_005)"
    elif d == "controlled_standard" or (d == "example" and dec and dec["decision"] == "retained"):
        body, src = fill(t), f"template · {d} retained"
    elif d == "authorable":
        todo.append(f"{tid} — {t['meaning']['source_text']}")
        body, src = '<span class=todo>[not yet authored]</span>', "owed"
    else:
        body, src = fill(t), f"template · {d or 'structural'}"
    trace.append((tid, t.get("content_hash"), "template · text"))

    label = esc(t["meaning"]["source_text"].rstrip("."))
    ft = form(t).get("field_type")
    if ft in ("signature", "person", "date", "text_short", "select_one"):
        return (f'<div class=row><div class=lab>{label}</div>'
                f'<div class=val>{body}<div class=mono>{esc(src)}</div></div></div>')
    return f'<p>{body}</p><div class=mono>{esc(src)}</div>'

root = next(a for a in tpl if not a.get("bindings", {}).get("object", {}).get("belongs_to"))
body = render(root, 0)

statuses = {a["governance"]["status"] for a in inst} or {"draft"}
DOC_STATUS = ("APPROVED" if statuses == {"approved"}
              else "IN REVIEW" if "in_review" in statuses else "DRAFT")
doc_label = docs.get(pin.get("document"), {}).get("label", pin.get("document", "?"))

trace_rows = "".join(
    f"<tr><td class=mono>{esc(a)}</td><td class=mono>{esc(str(h))[:26]}…</td><td>{esc(w)}</td></tr>"
    for a, h, w in trace)
todo_rows = "".join(f"<li>{esc(x)}</li>" for x in todo)

HTML = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>ALSAP — {esc(manifest.get('project',''))} (instance projection)</title>
<style>
:root{{--ink:#0f172a;--mut:#64748b;--line:#e2e8f0;--bg:#f8fafc;--accent:#1e3a8a}}
*{{box-sizing:border-box}}
body{{font:15px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);
 margin:0;background:var(--bg)}}
.page{{max-width:900px;margin:0 auto;background:#fff;padding:48px 56px;
 box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.ctrl{{display:flex;justify-content:space-between;align-items:flex-start;
 border-bottom:2px solid var(--accent);padding-bottom:14px;margin-bottom:8px}}
.ctrl .doc{{font-weight:700;font-size:19px;color:var(--accent)}}
.ctrl .meta{{text-align:right;font-size:12.5px;color:var(--mut)}}
.banner{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:10px 14px;
 font-size:12.5px;color:#92400e;margin:14px 0 26px}}
.warn{{background:#fef2f2;border-color:#fecaca;color:#991b1b}}
h1{{font-size:20px;margin:6px 0 2px}}
h2{{font-size:16px;margin:30px 0 8px;color:var(--accent);border-bottom:1px solid var(--line);
 padding-bottom:4px}}
h3{{font-size:14px;margin:20px 0 6px;color:#334155}}
p{{margin:8px 0}}
.row{{display:flex;gap:16px;border-bottom:1px solid var(--line);padding:8px 0}}
.lab{{width:34%;font-weight:600;color:#334155;font-size:13.5px}}
.val{{flex:1}}
.filled{{background:#ecfdf5;border-bottom:1px solid #6ee7b7;padding:0 3px;border-radius:2px}}
.todo{{background:#fef2f2;color:#991b1b;border-bottom:1px dashed #fca5a5;padding:0 3px}}
.ex{{color:var(--mut);font-size:12.5px;margin-top:2px}}
.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;color:var(--mut)}}
table{{border-collapse:collapse;width:100%;margin:8px 0;font-size:12.5px}}
th,td{{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}}
th{{background:#f1f5f9;font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:#475569}}
details{{margin-top:34px;border-top:1px dashed var(--line);padding-top:14px}}
summary{{cursor:pointer;color:var(--mut);font-size:12.5px}}
.foot{{margin-top:30px;font-size:11.5px;color:var(--mut);border-top:1px solid var(--line);
 padding-top:12px}}
</style></head><body><div class=page>
<div class=ctrl>
 <div><div class=doc>ALSAP · {esc(manifest.get('project',''))}</div>
 <div style="font-size:12.5px;color:var(--mut)">Instance of {esc(doc_label)} v{esc(pin.get('version','?'))}</div></div>
 <div class=meta>Status: <b>{DOC_STATUS}</b><br>Regulatory-bound · GxP controlled<br>
 Sparse overlay · {len(inst)} authored value(s)</div>
</div>
<div class=banner><b>Instance projection.</b> Resolved at render time from
{len(tpl)} template atoms pinned at {esc(doc_label)} v{esc(pin.get('version','?'))}, overlaid with
{len(inst)} authored value(s) and {len(dec_doc.get('decisions', []))} recorded decision(s).
<span class=filled>Green</span> spans are authored for this asset; everything else is controlled
template text that exists only in the template store and was never copied here.</div>
{'<div class="banner warn"><b>STALE.</b> ' + str(len(set(stale))) + ' element(s) were authored against a template atom whose meaning has since changed. Re-open them before approval.</div>' if stale else ''}
{'<div class="banner warn"><b>INCOMPLETE.</b> ' + str(len(todo)) + ' slot(s) still owed:<ul>' + todo_rows + '</ul></div>' if todo else ''}
{body}
<details><summary>Traceability appendix — every projected element ↔ atom (click to expand)</summary>
<table><thead><tr><th>atom_id</th><th>content_hash</th><th>role in this document</th></tr></thead>
<tbody>{trace_rows}</tbody></table></details>
<div class=foot>Template store: {esc(str(TPL))} · Instance store: {esc(str(PROJ))}<br>
Projection generated by tools/project_alsap.py — no meaning authored here, only arranged.</div>
</div></body></html>"""

OUT.write_text(HTML)
print(f"ALSAP projection -> {OUT}")
print(f"  template : {doc_label} v{pin.get('version')} — {len(tpl)} atoms (pinned, not copied)")
print(f"  overlay  : {len(inst)} authored value(s), {len(dec_doc.get('decisions', []))} decision(s)")
print(f"  status   : {DOC_STATUS} · {len(todo)} slot(s) owed · {len(set(stale))} stale")
