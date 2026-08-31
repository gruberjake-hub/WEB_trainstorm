#!/usr/bin/env python3
"""
dramaturge — the arc facet owner's runtime (dramaturge.v0.1).

Runs the LIVE wakes in agents/dramaturge/wakes.json against a project and PROPOSES beats into
occurrences/beats.json (status "proposed", always — the designer ratifies by flipping to
"accepted" in the catalog; merge makes it durable). Dramaturge writes placement + intent, never
copy: words are Dragoman voice-mode work against a beat, inverse-guarded, a later hop.

Idempotent and deferential: a placement already claimed by ANY existing beat (whatever its
status) is never re-proposed — a designer's decision, including a deletion-by-edit, is not
re-litigated by a re-run. The catalog is schema-validated before writing; a failed validation
writes nothing.

    python3 tools/dramaturge.py --project ../brunswick/projects/paytrans
    python3 tools/dramaturge.py --project ... --dry-run
"""
import argparse, json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness_paths
from validate_arc import gate_catalog, beat_hash  # one gate, one home — never copied

ap = argparse.ArgumentParser()
ap.add_argument("--core"); ap.add_argument("--project")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

P = harness_paths.resolve_core(a.core)
PP = harness_paths.resolve()
proj = PP["project_dir"]
wakes_p = P["core_dir"] / "agents" / "dramaturge" / "wakes.json" if "core_dir" in P else \
          P["schemas_dir"].parent / "agents" / "dramaturge" / "wakes.json"
wakes = json.loads(wakes_p.read_text(encoding="utf-8"))

scenes_p = proj / "occurrences" / "scenes.json"
scenes = json.loads(scenes_p.read_text(encoding="utf-8")) if scenes_p.exists() else {"scenes": []}
scene_ids = {s["id"] for s in scenes.get("scenes", [])}
els_p = proj / "occurrences" / "elements.json"
els = json.loads(els_p.read_text(encoding="utf-8")) if els_p.exists() else []
el_list = els["elements"] if isinstance(els, dict) and "elements" in els else els
element_ids = {e["element_id"] for e in el_list}

beats_p = proj / "occurrences" / "beats.json"
cat = json.loads(beats_p.read_text(encoding="utf-8")) if beats_p.exists() else {
    "store": "beats", "project": proj.name, "policy": "v1_beat_catalog",
    "spec": "agents/dramaturge/beats_v1.md", "vocab": "vocab/intent.enum.json", "beats": []}

claimed = {json.dumps(b["placement"], sort_keys=True) for b in cat["beats"]}
slug = proj.name
proposed, skipped = [], []


def propose(beat):
    key = json.dumps(beat["placement"], sort_keys=True)
    if key in claimed:
        skipped.append((beat["beat_id"], "placement already claimed — not re-litigating"))
        return
    cat["beats"].append(beat)
    claimed.add(key)
    proposed.append(beat)


for wake in wakes["wakes"]:
    if not wake.get("live"):
        continue
    if wake["id"] == "missing_arc_frame":
        n = len(scenes.get("scenes", []))
        if n < int(wake["params"].get("min_scenes", 3)):
            skipped.append((wake["id"], f"lesson has {n} scenes < min_scenes"))
            continue
        propose({"beat_id": f"bt_{slug}_welcome",
                  "placement": {"type": "lesson_start"},
                  "intent": {"pedagogical": "hook"},
                  "status": "proposed",
                  "from": f"missing_arc_frame: {n} scenes, no lesson_start beat — a course that "
                           "opens on its first topic never told the learner why they're here.",
                  "proposed_by": "dramaturge.v0.1/missing_arc_frame"})
        propose({"beat_id": f"bt_{slug}_closure",
                  "placement": {"type": "lesson_end"},
                  "intent": {"pedagogical": "transfer"},
                  "status": "proposed",
                  "from": f"missing_arc_frame: {n} scenes, no lesson_end beat — the artisan "
                           "control closes ('You're Informed'); the pipeline course just stops.",
                  "proposed_by": "dramaturge.v0.1/missing_arc_frame"})
    else:
        skipped.append((wake["id"], "live but unimplemented — placeholder wakes must stay live:false"))

results = []
gate_catalog(beats_p.name, cat, scene_ids, element_ids, results)
bad = [r for r in results if not r[1]]
if bad:
    print("CATALOG INVALID — nothing written:")
    for nm, _, detail in bad[:5]:
        print(f"  {nm}: {detail}")
    sys.exit(1)

for b in proposed:
    print(f"  + {b['beat_id']}: {b['placement']['type']} · {json.dumps(b['intent'])} · {beat_hash(b)[:23]}…")
for bid, why in skipped:
    print(f"  · {bid}: skipped — {why}")

if a.dry_run:
    print(f"\n(dry run) {len(proposed)} beat(s) would be proposed → {beats_p}")
elif proposed:
    beats_p.write_text(json.dumps(cat, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{len(proposed)} beat(s) proposed → {beats_p}. Ratify by flipping status to "
          "\"accepted\" in the catalog; copy comes later via Dragoman voice mode.")
else:
    print("\nnothing to propose — the arc frame is already claimed.")
