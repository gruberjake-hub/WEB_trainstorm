#!/usr/bin/env python3
"""
project_socket — derive the INTAKE SOCKET from a form template store.

The third render target. project_sop.py projects atoms into a controlled document; resolve_slot.py
projects them into an agent's working context; this projects them into a CONTRACT — the statement of
what a stakeholder must supply for the delivered agent to do its work.

Why it exists: the manifold's first-order product is an agent, and that agent is itself an intake
surface for someone else's evidence (decision log 2026-08-20, fifth). That evidence arrives at THEIR
runtime and may never be the instructional designer's to hold, so the engine has to be deliverable
and demonstrable without it — permanently. The socket is what makes that honest instead of merely
incomplete: it says exactly what is owed, by whom, and in what form, using nothing but the template.

DERIVED, NEVER AUTHORED. Every field here comes from a template atom. Correcting a demand means
correcting the atom; hand-editing the output would make the contract a second source of truth that
drifts the moment the template is revised. That is the failure this architecture exists to prevent,
so the emitted file says so in its own header and the gate refuses a demand the template cannot
support.

  python3 tools/project_socket.py --project <template store> [--procedure <sop store>]
                                  [--out socket.json] [--html socket.html]

What is a demand: an authorable field, or a named slot inside otherwise-retained text. A
controlled_standard sentence with no slots demands nothing (its text is resolved from the template);
an instructional_transient block is deleted, not filled; an `example` block is a keep/modify/delete
DECISION, which the instance layer already carries and which is not an intake obligation.
"""
import json, sys, pathlib, argparse, collections
import harness_paths

P = harness_paths.resolve()
REG, PROJ, VOCAB = P["registry_dir"], P["project_dir"], P["vocab_dir"]

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--procedure", help="an SOP store whose steps govern this template's use")
ap.add_argument("--out"); ap.add_argument("--html")
A, _ = ap.parse_known_args()

def load(p, d=None):
    p = pathlib.Path(p)
    return json.loads(p.read_text()) if p.exists() else d

atoms = load(PROJ / "atoms.json", [])
by_id = {a["atom_id"]: a for a in atoms}
manifest = load(PROJ / "manifest.json", {})
silent = load(PROJ / "source_silent.json", {})

def reg(name, key):
    return {e["id"]: e for e in (load(REG / name, {key: []}) or {key: []}).get(key, [])}
ROLES, DOCS, OPTIONS = reg("roles.registry.json", "roles"), reg("docs.registry.json", "docs"), reg("options.registry.json", "options")

def idlabel(r, i):
    """id AND label AND governed. A label alone cannot be checked against a registry, so a reader
    handed only labels cannot run the ungoverned-value drift check the contract implies."""
    return {"id": i, "label": r.get(i, {}).get("label", i), "governed": i in r}

def form(a): return a.get("bindings", {}).get("form", {})
def obj(a):  return a.get("bindings", {}).get("object", {})

EV = load(VOCAB / "evidence.enum.json", {"dimensions": {}})
EK = {v["id"]: v for v in EV.get("dimensions", {}).get("evidence_kind", {}).get("values", [])}

def path_of(aid):
    """Outermost-first trail of container labels, so a stakeholder can find the point in their own
    copy of the template rather than in our id space."""
    out, cur = [], by_id.get(aid, {})
    while (parent := obj(cur).get("belongs_to")):
        cur = by_id.get(parent, {})
        if not cur: break
        if cur["meaning"].get("kind") in ("form_section", "form"):
            out.append(cur["meaning"]["source_text"].rstrip("."))
    return list(reversed(out))

# ---- the governing procedure, joined across the store boundary by doc_ id --------------------
# Reading across stores is allowed: this walk is ephemeral and nothing is persisted. The join key is
# the shared doc_ id, the same one the SOP's steps already reference.
SRC_DOC = manifest.get("source_document")
proc_steps = []
if A.procedure and SRC_DOC:
    for pa in load(pathlib.Path(A.procedure) / "atoms.json", []) or []:
        pb = pa.get("bindings", {}).get("procedure", {})
        refs = pb.get("references", []) or pb.get("refs", []) or []
        if SRC_DOC in refs or SRC_DOC in json.dumps(pb):
            proc_steps.append({"atom_id": pa["atom_id"],
                               "text": pa["meaning"]["source_text"]})

# ---- demands ---------------------------------------------------------------------------------
def base(a, ek, sb, expects):
    d = {"demand_id": a["atom_id"], "source_atom": a["atom_id"],
         "path": path_of(a["atom_id"]), "expects": expects,
         "evidence_kind": ek, "supplied_by": sb}
    if EK.get(ek, {}).get("pii_bearing"):
        d["storage_rule"] = EK[ek].get("storage_rule", "PII-bearing: never stored in a content atom.")
    return d

demands, out_of_band = [], []
for a in sorted(atoms, key=lambda x: (path_of(x["atom_id"]), obj(x).get("order", 0))):
    f = a.get("bindings", {}).get("form", {})
    if a["meaning"].get("kind") != "form_field":
        continue
    cd, ft = f.get("content_disposition"), f.get("field_type")
    cons = f.get("constraints", {}) or {}

    # An obligation the template imposes that this engine does not collect. Listing it keeps the
    # contract from understating the ask; marking it keeps it from implying the tool gathers it.
    if ft == "signature":
        out_of_band.append({
            "ref": a["atom_id"],
            "obligation": a["meaning"]["source_text"].rstrip(".") +
                          " — applied to the rendered document, not authored through this engine.",
            "accountable": [idlabel(ROLES, r) for r in f.get("performed_by", [])]})
        continue

    if cd == "authorable":
        d = base(a, f.get("evidence_kind"), f.get("supplied_by"), a["meaning"]["source_text"])
        d["field_type"] = ft
        if cons.get("required") is not None: d["required"] = cons["required"]
        if cons.get("format"): d["format"] = cons["format"]
        if f.get("options_ref"):
            o = OPTIONS.get(f["options_ref"], {})
            d["options"] = {"options_ref": f["options_ref"],
                            "governed": f["options_ref"] in OPTIONS,
                            "values": [{"id": v["id"], "label": v.get("label", v["id"]),
                                        "governed": True} for v in o.get("values", [])]}
        if f.get("performed_by"):
            d["accountable"] = [idlabel(ROLES, r) for r in f["performed_by"]]
        # A conditional demand listed unconditionally over-states the ask. An UNSTATED predicate is
        # named as unstated rather than passed as a silent null — the same fix the 08-20 dispatch
        # forced on the grounding packet.
        if f.get("conditional_on"):
            d["applies_when"] = [{"demand_id": c["field"], "equals": c.get("equals"),
                                  "predicate_stated": "equals" in c}
                                 for c in f["conditional_on"]]
        if proc_steps: d["governed_by"] = proc_steps
        demands.append(d)

    # Each named slot is a demand in its own right; the sentence around it is not.
    for s in cons.get("slots", []):
        d = base(a, s.get("evidence_kind"), s.get("supplied_by"), s.get("expects", ""))
        d["demand_id"] = f"{a['atom_id']}#{s['id']}"
        d["slot_id"] = s["id"]
        if s.get("marker"): d["marker"] = s["marker"]
        if s.get("options_ref"):
            o = OPTIONS.get(s["options_ref"], {})
            d["options"] = {"options_ref": s["options_ref"],
                            "governed": s["options_ref"] in OPTIONS,
                            "values": [{"id": v["id"], "label": v.get("label", v["id"]),
                                        "governed": True} for v in o.get("values", [])]}
        if proc_steps: d["governed_by"] = proc_steps
        demands.append(d)

# ---- coverage: the honesty field --------------------------------------------------------------
# A contract listing ten demands from a template with eight undecomposed sections reads to a client
# as the whole obligation. Rests on structured data from the ingest, never on scraping prose.
ds = silent.get("deferred_scope") or {}
not_done = ds.get("not_decomposed_sections", [])
cov = {
    "partial": bool(not_done) or (ds.get("tables_decomposed", 0) < ds.get("tables_total", 0)),
    "sections_decomposed": ds.get("decomposed", []),
    "sections_not_decomposed": not_done,
}
if "tables_total" in ds:
    cov["tables_total"], cov["tables_decomposed"] = ds["tables_total"], ds.get("tables_decomposed", 0)
cov["statement"] = (
    f"PARTIAL CONTRACT. It covers {len(cov['sections_decomposed'])} decomposed area(s) of the "
    f"template and enumerates {len(demands)} demand(s). {len(not_done)} section(s) are not yet "
    f"decomposed and may carry demands of their own, which this contract cannot yet list."
    if cov["partial"] else
    f"COMPLETE for this template as decomposed: {len(demands)} demand(s) across the whole document.")

summary = {
    "by_evidence_kind": dict(sorted(collections.Counter(d["evidence_kind"] for d in demands).items())),
    "by_supplied_by": dict(sorted(collections.Counter(d["supplied_by"] for d in demands).items())),
}

socket = {
    "artifact": "intake_socket",
    "version": 1,
    "generated_by": "tools/project_socket.py — DERIVED. Do not edit: correct the template atom.",
    "template": {k: v for k, v in {
        "document": SRC_DOC,
        "version": manifest.get("template_version", "1.0"),
        "title": next((a["meaning"]["source_text"].rstrip(".") for a in atoms
                       if a["meaning"].get("kind") == "form"), None),
        "store": manifest.get("project"),
        "atom_count": len(atoms)}.items() if v is not None},
    "coverage": cov,
    "demands": demands,
    "out_of_band": out_of_band,
    "summary": summary,
}

# ---- validate our own output before anyone reads it -------------------------------------------
from jsonschema import Draft202012Validator
schema = load(P["schemas_dir"] / "socket.schema.json")
errs = sorted(Draft202012Validator(schema).iter_errors(socket), key=lambda e: list(e.path))
for e in errs:
    print(f"  x SCHEMA {'/'.join(map(str, e.path)) or '(root)'}: {e.message}", file=sys.stderr)
if errs:
    raise SystemExit("refusing to emit a socket that does not validate against its own schema.")

if A.out:
    pathlib.Path(A.out).write_text(json.dumps(socket, indent=2, ensure_ascii=False) + "\n")
    print(f"socket -> {A.out}")

# ---- the same contract, for a human ------------------------------------------------------------
# The JSON is what a stakeholder's ingest validates against; this is what a person reads before
# agreeing to it. One derivation, two renderings — never two documents that can disagree.
if A.html:
    import html as _h
    def esc(x): return _h.escape(str(x))
    KIND_DEF = {k: v.get("definition", "") for k, v in EK.items()}
    SUP_DEF = {v["id"]: v.get("definition", "") for v in
               EV.get("dimensions", {}).get("supplied_by", {}).get("values", [])}
    GROUPS = [("asset_evidence", "Gathered from your asset evidence",
               "Assemble these before authoring begins. They are the second-order intake this "
               "engine is built around, and nothing here is knowable from the template alone."),
              ("stakeholder_decision", "Decided by an accountable body",
               "These cannot be gathered in advance. The contract states who must have decided "
               "them; the document records the decision."),
              ("authoring_context", "Known at the moment of authoring",
               "No dossier required — the tool asks for these inline.")]
    rows = []
    for gid, gtitle, gblurb in GROUPS:
        ds = [d for d in socket["demands"] if d["supplied_by"] == gid]
        if not ds: continue
        rows.append(f'<h2>{esc(gtitle)} <span class="n">{len(ds)}</span></h2>'
                    f'<p class="blurb">{esc(gblurb)}</p>')
        for d in ds:
            where = " › ".join(esc(x) for x in d.get("path", [])) or "—"
            bits = [f'<span class="kind">{esc(d["evidence_kind"])}</span>',
                    f'<span class="loc">{where}</span>']
            if d.get("required"): bits.append('<span class="req">required</span>')
            if d.get("format"): bits.append(f'<span class="fmt">format {esc(d["format"])}</span>')
            extra = []
            if d.get("evidence_kind") in KIND_DEF and KIND_DEF[d["evidence_kind"]]:
                extra.append(f'<div class="def">{esc(KIND_DEF[d["evidence_kind"]])}</div>')
            if d.get("options"):
                vals = ", ".join(esc(v["label"]) for v in d["options"]["values"])
                extra.append(f'<div class="opts"><b>One of {len(d["options"]["values"])} '
                             f'governed values</b> ({esc(d["options"]["options_ref"])}): {vals}. '
                             f'A value outside this set is not a valid submission.</div>')
            if d.get("applies_when"):
                for w in d["applies_when"]:
                    cond = (f'when <code>{esc(w["demand_id"])}</code> = '
                            f'<code>{esc(w["equals"])}</code>' if w["predicate_stated"]
                            else f'when <code>{esc(w["demand_id"])}</code> is set — '
                                 f'<b>the template does not state which value triggers it</b>')
                    extra.append(f'<div class="cond">Owed only {cond}.</div>')
            if d.get("storage_rule"):
                extra.append(f'<div class="pii"><b>Personal data.</b> {esc(d["storage_rule"])}</div>')
            if d.get("accountable"):
                extra.append('<div class="acc">Accountable: ' +
                             ", ".join(esc(r["label"]) for r in d["accountable"]) + "</div>")
            rows.append(f'<div class="d"><div class="dh"><code>{esc(d["demand_id"])}</code>'
                        f'<div class="tags">{"".join(bits)}</div></div>'
                        f'<div class="ex">{esc(d["expects"])}</div>{"".join(extra)}</div>')
    oob = ""
    if socket["out_of_band"]:
        items = "".join(f'<li>{esc(o["obligation"])}'
                        + (f' <span class="acc">— {", ".join(esc(r["label"]) for r in o.get("accountable", []))}</span>'
                           if o.get("accountable") else "") + "</li>"
                        for o in socket["out_of_band"])
        oob = (f'<h2>Not collected by this engine <span class="n">{len(socket["out_of_band"])}</span></h2>'
               f'<p class="blurb">The template imposes these, and they are listed so the contract '
               f'does not understate the ask — but they are applied to the rendered document rather '
               f'than authored through the tool.</p><ul class="oob">{items}</ul>')
    gov = ""
    if proc_steps:
        gov = ('<h2>Authority</h2><p class="blurb">These demands are not ours. They come from the '
               'template, whose use is governed by:</p><ul class="oob">' +
               "".join(f'<li><code>{esc(s["atom_id"])}</code> — {esc(s["text"])}</li>'
                       for s in proc_steps) + "</ul>")
    cov = socket["coverage"]
    covbox = (f'<div class="{"warn" if cov["partial"] else "ok"}"><b>'
              f'{"Partial contract." if cov["partial"] else "Complete for this template."}</b> '
              f'{esc(cov["statement"])}'
              + (f'<div class="und">Not yet enumerated: '
                 + "; ".join(esc(s) for s in cov["sections_not_decomposed"]) + "</div>"
                 if cov.get("sections_not_decomposed") else "") + "</div>")
    tpl = socket["template"]
    pathlib.Path(A.html).write_text(f"""<!doctype html><meta charset="utf-8">
<title>Intake contract — {esc(tpl.get('title') or 'template')}</title>
<style>
:root{{--ink:#0f172a;--mut:#64748b;--line:#e2e8f0;--accent:#1e3a5f}}
*{{box-sizing:border-box}}
body{{font:15px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);
 background:#f1f5f9;margin:0;padding:28px 16px}}
.page{{max-width:900px;margin:0 auto;background:#fff;padding:48px 56px;
 box-shadow:0 1px 3px rgba(15,23,42,.12);border-radius:4px}}
.ctrl{{display:flex;justify-content:space-between;align-items:baseline;
 border-bottom:2px solid var(--accent);padding-bottom:10px}}
.ctrl .doc{{font-weight:700;font-size:19px;color:var(--accent)}}
.ctrl .meta{{text-align:right;font-size:12.5px;color:var(--mut)}}
h1{{font-size:22px;margin:26px 0 6px}}
.lede{{color:var(--mut);font-size:14px;margin:0 0 20px}}
.warn,.ok{{border:1px solid #fcd34d;background:#fffbeb;color:#92400e;
 border-radius:4px;padding:12px 14px;font-size:13.5px;margin:16px 0 26px}}
.ok{{border-color:#a7f3d0;background:#ecfdf5;color:#065f46}}
.und{{margin-top:6px;font-size:12.5px;opacity:.85}}
h2{{font-size:15.5px;margin:34px 0 4px;color:var(--accent);
 border-bottom:1px solid var(--line);padding-bottom:5px}}
h2 .n{{float:right;color:var(--mut);font-weight:400;font-size:13px}}
.blurb{{color:var(--mut);font-size:13px;margin:6px 0 14px}}
.d{{border-left:3px solid var(--line);padding:10px 0 10px 14px;margin:0 0 14px}}
.dh{{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap}}
code{{font:12.5px ui-monospace,SFMono-Regular,Menlo,monospace;color:#334155;
 background:#f8fafc;padding:1px 5px;border-radius:3px;word-break:break-all}}
.tags{{display:flex;gap:6px;flex-wrap:wrap;font-size:11.5px}}
.kind{{background:#1e3a5f;color:#fff;padding:1px 7px;border-radius:10px}}
.loc,.req,.fmt{{color:var(--mut);border:1px solid var(--line);padding:1px 7px;border-radius:10px}}
.req{{color:#991b1b;border-color:#fecaca}}
.ex{{margin:7px 0 0;font-size:14.5px}}
.def,.opts,.cond,.acc,.pii{{font-size:12.5px;margin-top:7px;color:var(--mut)}}
.opts{{color:#334155}}
.cond{{color:#7c2d12}}
.pii{{background:#fef2f2;border:1px solid #fecaca;color:#991b1b;padding:8px 10px;border-radius:3px}}
ul.oob{{margin:8px 0 0;padding-left:20px;font-size:13.5px;color:#334155}}
ul.oob li{{margin-bottom:6px}}
footer{{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);
 font-size:12px;color:var(--mut)}}
@media print{{body{{background:#fff;padding:0}}.page{{box-shadow:none;padding:0}}}}
</style>
<div class="page">
<div class="ctrl"><div class="doc">{esc(tpl.get('title') or '')}</div>
<div class="meta">{esc(tpl.get('document') or '')} v{esc(tpl.get('version') or '')}<br>
Intake contract · derived from the template, not authored</div></div>
<h1>What you need to supply</h1>
<p class="lede">This is the complete set of points the template leaves for you to fill, grouped by
where each one comes from. It is derived from the template itself — every line below traces to a
specific point in the document, and nothing here is our invention.</p>
{covbox}
{"".join(rows)}
{oob}
{gov}
<footer>Derived by <code>tools/project_socket.py</code> from
<code>{esc(tpl.get('store') or '')}</code> ({tpl.get('atom_count')} atoms).
Do not edit this file: it is regenerated from the template, and a correction belongs to the
template. Machine-readable form: the accompanying <code>socket.json</code>, which a submission
can be validated against.</footer>
</div>""")
    print(f"contract -> {A.html}")

print("=" * 78)
print(f"INTAKE SOCKET — {socket['template'].get('title')} ({SRC_DOC})")
print("=" * 78)
print(f"  {cov['statement']}")
if not_done:
    print(f"  not yet decomposed: {'; '.join(not_done)}")
print()
for d in demands:
    tag = f"{d['evidence_kind']}/{d['supplied_by']}"
    print(f"  {d['demand_id'].replace('atom_form_ast34037_', '…')}")
    print(f"      {tag:34} {d['expects'][:78]}")
    if d.get("options"):
        print(f"      {'':34} one of {len(d['options']['values'])} governed value(s) "
              f"in {d['options']['options_ref']}")
    if d.get("applies_when"):
        for w in d["applies_when"]:
            print(f"      {'':34} only when {w['demand_id'].replace('atom_form_ast34037_', '…')}"
                  + (f" == {w['equals']}" if w["predicate_stated"] else " is set (predicate UNSTATED in source)"))
    if d.get("storage_rule"):
        print(f"      {'':34} PII: value never stored in a content atom")
print()
for k, v in summary.items():
    print(f"  {k:18} {v}")
if out_of_band:
    print(f"  out of band        {len(out_of_band)} obligation(s) not collected by this engine")
