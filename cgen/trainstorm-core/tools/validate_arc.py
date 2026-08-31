#!/usr/bin/env python3
"""
The arc gate — Dramaturge's gate. Validates a project's beat catalog:

    SCHEMA      — occurrences/beats.json validates against schemas/beats.catalog.schema.json.
    GOVERNANCE  — every beat intent resolves to intent.enum.json (both dimensions, closed lists).
    REFERENCES  — scene placements name a scene in scenes.json; after_element names an element
                  in occurrences/elements.json; beat_ids are unique.

Also home to `beat_hash` — sha256 over canonical {beat_id, placement, intent} — the staleness
anchor beat COPY pins as its source_hash (voice pack `beats` section). One definition, imported
by dramaturge.py and the voice tools; never copied.

    python3 tools/validate_arc.py --project ../brunswick/projects/paytrans
    python3 tools/validate_arc.py --selftest
"""
import argparse, hashlib, json, sys, pathlib
from jsonschema import Draft202012Validator
import harness_paths

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--core"); ap.add_argument("--project"); ap.add_argument("--selftest", action="store_true")
args, _ = ap.parse_known_args()

P = harness_paths.resolve_core(args.core)
schema = json.loads((P["schemas_dir"] / "beats.catalog.schema.json").read_text(encoding="utf-8"))
_intent = json.loads((P["vocab_dir"] / "intent.enum.json").read_text(encoding="utf-8"))
PEDAGOGICAL = {v["id"] for v in _intent["dimensions"]["pedagogical"]["values"]}
RHETORICAL = {v["id"] for v in _intent["dimensions"]["rhetorical"]["values"]}
V = Draft202012Validator(schema)


def beat_hash(beat: dict) -> str:
    """sha256 over canonical {beat_id, placement, intent}. Placement or intent moves → copy stale."""
    canon = json.dumps({"beat_id": beat["beat_id"], "placement": beat["placement"],
                         "intent": beat["intent"]}, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canon.encode("utf-8")).hexdigest()


def gate_catalog(name, cat, scene_ids, element_ids, results):
    errs = sorted(V.iter_errors(cat), key=lambda e: list(e.path))
    results.append((f"{name}: validates against schema", not errs,
                    "; ".join(e.message for e in errs)[:160]))
    if errs:
        return
    seen = set()
    for b in cat.get("beats", []):
        bid = b["beat_id"]
        results.append((f"{name}: {bid} unique", bid not in seen, "duplicate beat_id"))
        seen.add(bid)
        it = b["intent"]
        ok_int = (("pedagogical" not in it or it["pedagogical"] in PEDAGOGICAL)
                  and ("rhetorical" not in it or it["rhetorical"] in RHETORICAL))
        results.append((f"{name}: {bid} intent governed", ok_int, json.dumps(it)))
        pl = b["placement"]
        if pl["type"] in ("scene_start", "scene_end"):
            results.append((f"{name}: {bid} scene ref resolves", pl.get("scene_id") in scene_ids,
                            f"scene_id {pl.get('scene_id')!r} not in scenes.json"))
        if pl["type"] == "after_element":
            results.append((f"{name}: {bid} element ref resolves", pl.get("element_id") in element_ids,
                            f"element_id {pl.get('element_id')!r} not in elements.json"))


def report(results):
    print(f"{'CHECK':<66} RESULT")
    print("-" * 82)
    ok = True
    for nm, passed, detail in results:
        ok = ok and passed
        print(f"{nm:<66} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
    print("-" * 82)
    print("ALL PASS" if ok else "SOME FAILED")
    return ok


if __name__ == "__main__" and args.selftest:
    try:
        Draft202012Validator.check_schema(schema)
        results = [("beats.catalog.schema is valid Draft 2020-12", True, "")]
    except Exception as e:
        results = [("beats.catalog.schema is valid Draft 2020-12", False, str(e))]
    SC, EL = {"sc_a", "sc_b"}, {"ele_x_mid"}
    good = {"store": "beats", "project": "fx", "policy": "v1_beat_catalog", "beats": [
        {"beat_id": "bt_fx_welcome", "placement": {"type": "lesson_start"},
         "intent": {"pedagogical": "hook"}, "status": "proposed",
         "from": "fixture", "proposed_by": "dramaturge.v0.1/missing_arc_frame"},
        {"beat_id": "bt_fx_gloss", "placement": {"type": "after_element", "element_id": "ele_x_mid"},
         "intent": {"rhetorical": "persuade"}, "status": "accepted", "from": "fixture"},
    ]}
    n0 = len(results)
    gate_catalog("fixture(good)", good, SC, EL, results)
    results.append(("selftest: clean fixture passes", all(ok for _, ok, _ in results[n0:]), ""))
    results.append(("selftest: beat_hash is stable and prefixed",
                    beat_hash(good["beats"][0]) == beat_hash(json.loads(json.dumps(good["beats"][0])))
                    and beat_hash(good["beats"][0]).startswith("sha256:"), ""))
    results.append(("selftest: beat_hash moves when placement moves",
                    beat_hash(good["beats"][0]) != beat_hash({**good["beats"][0],
                        "placement": {"type": "lesson_end"}}), ""))

    def red(label, mutate):
        cat = json.loads(json.dumps(good)); mutate(cat)
        scratch = []
        gate_catalog("fixture(red)", cat, SC, EL, scratch)
        caught = any(not ok for _, ok, _ in scratch)
        results.append((label, caught, "" if caught else "mutation was NOT caught"))

    red("selftest: ungoverned intent is caught",
        lambda c: c["beats"][0]["intent"].update(pedagogical="delight"))
    red("selftest: new beat 'type' outside intent is caught (schema)",
        lambda c: c["beats"][0].update(beat_type="callout"))
    red("selftest: dangling scene ref is caught",
        lambda c: c["beats"][0].update(placement={"type": "scene_end", "scene_id": "sc_missing"}))
    red("selftest: after_element without element_id is caught",
        lambda c: c["beats"][1].update(placement={"type": "after_element"}))
    red("selftest: lesson beat carrying a scene_id is caught",
        lambda c: c["beats"][0].update(placement={"type": "lesson_start", "scene_id": "sc_a"}))
    red("selftest: duplicate beat_id is caught",
        lambda c: c["beats"].append(json.loads(json.dumps(c["beats"][0]))))
    red("selftest: copy smuggled onto a beat is caught (schema — beats carry no text)",
        lambda c: c["beats"][0].update(text="Welcome to the course!"))
    sys.exit(0 if report(results) else 1)

if __name__ == "__main__":
    PP = harness_paths.resolve()
    proj = PP["project_dir"]
    beats_p = proj / "occurrences" / "beats.json"
    results = []
    if not beats_p.exists():
        results.append(("no beat catalog in project — nothing to gate", True, f"looked at {beats_p}"))
        sys.exit(0 if report(results) else 1)
    cat = json.loads(beats_p.read_text(encoding="utf-8"))
    scenes_p = proj / "occurrences" / "scenes.json"
    scenes = json.loads(scenes_p.read_text(encoding="utf-8")) if scenes_p.exists() else {"scenes": []}
    scene_ids = {s["id"] for s in scenes.get("scenes", [])}
    els_p = proj / "occurrences" / "elements.json"
    els = json.loads(els_p.read_text(encoding="utf-8")) if els_p.exists() else []
    el_list = els["elements"] if isinstance(els, dict) and "elements" in els else els
    element_ids = {e["element_id"] for e in el_list}
    gate_catalog(beats_p.name, cat, scene_ids, element_ids, results)
    for b in cat.get("beats", []):
        print(f"   {b['beat_id']:<28} {b['status']:<9} {beat_hash(b)[:23]}…")
    sys.exit(0 if report(results) else 1)
