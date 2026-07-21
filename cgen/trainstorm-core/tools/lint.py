
#!/usr/bin/env python3
"""
Trainstorm linter — the guardrail across the content stack.
 
Runs governance + drift checks on courses, scenes, and scripts:
  • ungoverned intents / pedagogical intents / primitive types (vs vocab + schema)
  • script validation against schemas/script.primitives.v1.json
  • list integrity (legacy delimited lists, item_count vs children, parent refs)
  • cross-file ID collisions (the sce_003 case)
  • embedded localization (should be externalized to locale packs)
  • asset/naming-contract mismatches (audio/output extension vs build_strategy)
  • unknown delivery targets
 
Usage:
    python lint.py <file-or-dir> [more...] [--root REPO] [--quiet]
 
Exit code: 0 = clean (no ERRORs), 1 = ERRORs found.  (WARN/INFO never fail the build.)
"""
import argparse, glob, hashlib, json, os, sys
from collections import defaultdict, namedtuple
 
try:
    import jsonschema
except ImportError:
    jsonschema = None
 
# ── a finding is one line of the report ───────────────────────────────────────
Finding = namedtuple("Finding", "level check where msg")
ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
 
LOCALE_KEYS = {"en","fr","de","es","ja","it","pt","zh","ko","nl","pl","sv","da","no","fi"}
ALLOWED_DELIVERY = {"ae_render", "storyline_interaction", "storyline_quiz"}
 
 
# ── loading & classification ──────────────────────────────────────────────────
def find_root(start):
    """Walk up from `start` until we find a dir that has schemas/ and vocab/."""
    d = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(d, "schemas")) and os.path.isdir(os.path.join(d, "vocab")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent
 
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
 
def classify(data):
    """Decide what KIND of file this is, from its shape."""
    if isinstance(data, list):
        return "script"                       # an array of primitives
    if isinstance(data, dict):
        if "scenes" in data:
            return "course"                   # course.v0.2 (scenes inline)
        if isinstance(data.get("elements"), dict):
            return "scene"                    # sce_###_content.json
        if isinstance(data.get("elements"), list):
            return "course_primitives"        # flat element array
    return "unknown"
 
def collect_inputs(paths):
    """Expand dirs to *.json, load each, tag with its kind."""
    files = []
    for p in paths:
        files += glob.glob(os.path.join(p, "**", "*.json"), recursive=True) if os.path.isdir(p) else [p]
    docs = []
    for f in files:
        try:
            docs.append((classify(load_json(f)), f, load_json(f)))
        except Exception as e:
            docs.append(("BAD", f, str(e)))
    return docs
 
def load_canon(root):
    """Load the governed vocabularies + the script schema from the repo."""
    canon = {"rhetorical": set(), "pedagogical": set(), "script_schema": None}
    if not root:
        return canon
    ie = os.path.join(root, "vocab", "intent.enum.json")
    if os.path.exists(ie):
        dims = load_json(ie)["dimensions"]
        canon["rhetorical"]  = {v["id"] for v in dims["rhetorical"]["values"]}
        canon["pedagogical"] = {v["id"] for v in dims["pedagogical"]["values"]}
    ss = os.path.join(root, "schemas", "script.primitives.v1.json")
    if os.path.exists(ss):
        canon["script_schema"] = load_json(ss)
    return canon
 
def scenes_of(kind, path, data):
    """Normalize course/scene docs to an iterable of (scene_id, scene_dict, file)."""
    if kind == "course":
        for s in data.get("scenes", []):
            yield s.get("scene_id"), s, path
    elif kind == "scene":
        yield data.get("scene_id"), data, path
 
def loc(path, *parts):
    return ":".join([os.path.basename(path), *[str(p) for p in parts if p is not None]])
 
 
# ── the checks (each yields Findings) ─────────────────────────────────────────
def check_intents(docs, canon):
    if not canon["rhetorical"]:
        yield Finding(INFO, "intent-vocab", "(canon)", "intent.enum.json not found — skipping intent governance")
        return
    for kind, path, data in docs:
        for sid, scene, _ in scenes_of(kind, path, data):
            for key, el in scene.get("elements", {}).items():
                it = el.get("intent")
                if it and it not in canon["rhetorical"]:
                    yield Finding(ERROR, "intent-vocab", loc(path, sid, key),
                                  f"ungoverned intent '{it}' (not in intent.enum rhetorical)")
 
def check_lists(docs, canon):
    for kind, path, data in docs:
        for sid, scene, _ in scenes_of(kind, path, data):
            els = scene.get("elements", {})
            for key, el in els.items():
                t, text = el.get("type"), el.get("text")
                # legacy delimited-string list (real newline OR a literal "\n")
                if t == "List" and isinstance(text, str) and ("\n" in text or "\\n" in text):
                    yield Finding(WARN, "legacy-list", loc(path, sid, key),
                                  "delimited-string List — decompose into ListItem children")
                # item_count vs actual children
                if t == "List" and "item_count" in el:
                    kids = [k for k, v in els.items() if v.get("type") == "ListItem" and v.get("parent") == key]
                    if len(kids) != el["item_count"]:
                        yield Finding(WARN, "list-count", loc(path, sid, key),
                                      f"item_count={el['item_count']} but {len(kids)} ListItem children")
                # parent reference must resolve
                par = el.get("parent") or el.get("parent_id")
                if par and par not in els:
                    yield Finding(ERROR, "parent-ref", loc(path, sid, key),
                                  f"parent '{par}' not found in scene")
 
def check_collisions(docs, canon):
    """Same scene_id → different content across files == a drift collision."""
    seen = defaultdict(list)
    for kind, path, data in docs:
        for sid, scene, _ in scenes_of(kind, path, data):
            if not sid:
                continue
            h = hashlib.sha1(json.dumps(scene.get("elements", {}), sort_keys=True,
                                        ensure_ascii=False).encode()).hexdigest()[:8]
            seen[sid].append((scene.get("title"), h, os.path.basename(path)))
    for sid, entries in seen.items():
        if len({(t, h) for t, h, _ in entries}) > 1:
            variants = "; ".join(f"{f}→{t!r}" for t, h, f in entries)
            yield Finding(ERROR, "id-collision", sid,
                          f"scene_id maps to different content across files: {variants}")
 
def check_embedded_locale(docs, canon):
    for kind, path, data in docs:
        if kind == "course_primitives":
            for i, el in enumerate(data.get("elements", [])):
                c = el.get("content")
                if isinstance(c, dict):
                    langs = [k for k in c if k in LOCALE_KEYS]
                    if len(langs) > 1:
                        yield Finding(WARN, "embedded-locale", loc(path, f"elements[{i}]"),
                                      f"content embeds {len(langs)} locales {langs} — externalize to locale packs")
 
def check_asset_contract(docs, canon):
    for kind, path, data in docs:
        if kind != "course":
            continue
        contract = (data.get("build_strategy") or {}).get("scene_file_contract") or {}
        def ext(pattern): return pattern.rsplit(".", 1)[-1] if "." in pattern else None
        vo_ext, out_ext = ext(contract.get("vo_audio_pattern", "")), ext(contract.get("render_output_pattern", ""))
        for sid, scene, _ in scenes_of(kind, path, data):
            af = (scene.get("narration") or {}).get("audio_file")
            if af and vo_ext and not af.endswith("." + vo_ext):
                yield Finding(WARN, "asset-contract", loc(path, sid),
                              f"audio_file '{af}' ≠ contract .{vo_ext}")
            of = (scene.get("render") or {}).get("output_file")
            if of and out_ext and not of.endswith("." + out_ext):
                yield Finding(WARN, "asset-contract", loc(path, sid),
                              f"output_file '{of}' ≠ contract .{out_ext}")
 
def check_delivery(docs, canon):
    for kind, path, data in docs:
        for sid, scene, _ in scenes_of(kind, path, data):
            d = scene.get("delivery")
            if d and d not in ALLOWED_DELIVERY:
                yield Finding(WARN, "delivery", loc(path, sid), f"unknown delivery '{d}'")
 
def check_scripts(docs, canon):
    schema = canon.get("script_schema")
    for kind, path, data in docs:
        if kind != "script":
            continue
        if schema and jsonschema:
            for e in jsonschema.Draft202012Validator(schema).iter_errors(data):
                where = "/".join(str(x) for x in e.path) or "(root)"
                yield Finding(ERROR, "script-schema", loc(path, where), e.message)
        elif schema and not jsonschema:
            yield Finding(INFO, "script-schema", loc(path), "jsonschema not installed — skipping")
        for i, prim in enumerate(data):
            pi = prim.get("pedagogical_intent") if isinstance(prim, dict) else None
            if pi and canon["pedagogical"] and pi not in canon["pedagogical"]:
                yield Finding(ERROR, "pedagogical-vocab", loc(path, f"[{i}]"),
                              f"ungoverned pedagogical_intent '{pi}'")
 
CHECKS = [check_intents, check_lists, check_collisions, check_embedded_locale,
          check_asset_contract, check_delivery, check_scripts]
 
 
# ── run & report ──────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Trainstorm content linter")
    ap.add_argument("paths", nargs="+", help="files and/or directories to lint")
    ap.add_argument("--root", help="repo root (default: auto-detect)")
    ap.add_argument("--quiet", action="store_true", help="show ERRORs only")
    args = ap.parse_args()
 
    root = args.root or find_root(args.paths[0]) or find_root(".")
    docs = collect_inputs(args.paths)
    canon = load_canon(root)
 
    findings = [Finding(ERROR, "json", os.path.basename(f), d) for k, f, d in docs if k == "BAD"]
    for check in CHECKS:
        findings += list(check([(k, f, d) for k, f, d in docs if k != "BAD"], canon))
 
    sym = {ERROR: "✗", WARN: "⚠", INFO: "·"}
    order = {ERROR: 0, WARN: 1, INFO: 2}
    kinds = ", ".join(sorted({k for k, _, _ in docs})) or "none"
    print(f"Trainstorm lint · {len(docs)} file(s) [{kinds}] · root: {root or 'NOT FOUND'}\n")
 
    shown = [f for f in findings if not (args.quiet and f.level != ERROR)]
    for f in sorted(shown, key=lambda x: (order[x.level], x.check)):
        print(f"  {sym[f.level]} {f.level:5s} [{f.check}] {f.where} — {f.msg}")
 
    n_err = sum(1 for f in findings if f.level == ERROR)
    n_warn = sum(1 for f in findings if f.level == WARN)
    print(f"\nSummary: {n_err} error(s), {n_warn} warning(s)  →  {'FAIL' if n_err else 'OK'}")
    sys.exit(1 if n_err else 0)
 
 
if __name__ == "__main__":
    main()