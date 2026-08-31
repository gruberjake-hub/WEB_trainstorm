#!/usr/bin/env python3
"""
voice_accept — the ONLY writer into a voice pack.

The acceptance half of the voice authoring loop (the accept_value.py pattern): Dragoman's voice
mode proposes into voice/proposals/<register>.json; a human runs THIS script; this script is what
acceptance *is*, mechanically. The agent writes nothing into the pack — it has no path to it — and
that is enforced by there being exactly one script, run by a person, that can put an entry in.

    # accept specific drafts
    voice_accept.py --project ../brunswick/projects/paytrans --register warm_direct \
        --ids atom_bw_guide_base_pay,atom_bw_guide_base_pay_grades --by jake

    # accept every draft that passes the gate (review the gate report + flags FIRST)
    voice_accept.py --project ../brunswick/projects/paytrans --register warm_direct --all --by jake

    # accept with an edited text (your words, your authorship — recorded as accepted-with-edit)
    voice_accept.py --project ... --register warm_direct --ids <atom_id> --by jake \
        --edit "Your edited rendering."

Every acceptance re-runs the deterministic invent-guard on the entry at acceptance time (stale or
invariant-violating drafts are refused — re-propose instead), then writes the pack entry
{text, status: "accepted", reviewer, source_hash} and validates the pack against
schemas/voice.pack.schema.json before saving. A failed validation writes nothing.
"""
import argparse, json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import harness_paths
from voice_gate import (invariant_findings, inverse_findings, build_arc_allowlist,
                        gate_track_proposals, GOVERNED, sha)  # one guard, one home — never copied
from validate_arc import beat_hash
from jsonschema import Draft202012Validator

ap = argparse.ArgumentParser()
ap.add_argument("--core"); ap.add_argument("--project", required=False)
ap.add_argument("--register", required=True)
ap.add_argument("--ids", help="comma-separated atom_ids (or bt_ beat ids) to accept")
ap.add_argument("--tracks", help="comma-separated scene ids: accept narration tracks (voice/proposals/narration.<register>.json → voice/narration/<register>.json)")
ap.add_argument("--all", action="store_true", help="accept every gate-passing draft")
ap.add_argument("--by", required=True, help="reviewer of record — acceptance is a person's act")
ap.add_argument("--edit", help="replacement text (single --ids entry only): accept your edit of the draft")
a = ap.parse_args()

if sum(map(bool, (a.ids, a.all, a.tracks))) != 1:
    raise SystemExit("choose exactly one of --ids, --all, or --tracks")
if a.edit and (a.all or len((a.ids or a.tracks).split(",")) != 1):
    raise SystemExit("--edit accepts exactly one --ids/--tracks entry")

P = harness_paths.resolve_core(a.core)
PP = harness_paths.resolve()
proj = PP["project_dir"]
reg = a.register
if reg not in GOVERNED:
    raise SystemExit(f"register '{reg}' is not governed (vocab/register.enum.json)")
if GOVERNED[reg].get("status") != "specified":
    raise SystemExit(f"register '{reg}' is status '{GOVERNED[reg].get('status')}' — "
                     "a draft register may be drafted against, never accepted (register.v0.1 rule)")

if a.tracks:
    import json as _json
    tprops_p = proj / "voice" / "proposals" / f"narration.{reg}.json"
    if not tprops_p.exists():
        raise SystemExit(f"no narration proposals store: {tprops_p}")
    tstore = _json.loads(tprops_p.read_text(encoding="utf-8"))
    atoms_l = _json.loads((proj / "atoms.json").read_text(encoding="utf-8"))
    atoms_by_id = {x["atom_id"]: x for x in (atoms_l["atoms"] if isinstance(atoms_l, dict) else atoms_l)}
    beats_pth = proj / "occurrences" / "beats.json"
    b_by_id = {b["beat_id"]: b for b in _json.loads(beats_pth.read_text(encoding="utf-8")).get("beats", [])}               if beats_pth.exists() else {}
    vpack_p = proj / "voice" / f"{reg}.json"
    vpack = _json.loads(vpack_p.read_text(encoding="utf-8")) if vpack_p.exists() else {}
    corpus_t = " ".join(x["meaning"]["source_text"] for x in atoms_by_id.values())
    from jsonschema import Draft202012Validator as _V
    nschema = _json.loads((P["schemas_dir"] / "narration.pack.schema.json").read_text(encoding="utf-8"))
    npack_p = proj / "voice" / "narration" / f"{reg}.json"
    npack = _json.loads(npack_p.read_text(encoding="utf-8")) if npack_p.exists() else             {"narration_version": "narration.v0.1", "register": reg, "tracks": {}}
    acc, ref = [], []
    for sid in [s.strip() for s in a.tracks.split(",")]:
        tr = (tstore.get("track_proposals") or {}).get(sid)
        if tr is None:
            ref.append((sid, "no such track proposal")); continue
        scratch = []
        gate_track_proposals("acceptance", {"register": reg, "track_proposals": {sid: tr}},
                             atoms_by_id, b_by_id, vpack, corpus_t, scratch)
        bad = [r for r in scratch if not r[1]]
        if bad:
            ref.append((sid, "; ".join(f"{n}: {d}" for n, _, d in bad)[:160])); continue
        text = a.edit if a.edit else tr["text"]
        npack["tracks"][sid] = {"text": text, "status": "accepted", "reviewer": a.by,
                                 "sources": tr["sources"]}
        acc.append((sid, "accepted" + (" (with edit)" if a.edit else "")))
    errs = sorted(_V(nschema).iter_errors(npack), key=lambda e: list(e.path))
    if errs:
        print("NARRATION PACK INVALID — nothing written:")
        for e in errs[:5]:
            print(" ", e.message)
        sys.exit(1)
    if acc:
        npack_p.parent.mkdir(parents=True, exist_ok=True)
        npack_p.write_text(_json.dumps(npack, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for sid, msg in acc:
        print(f"  + track {sid}: {msg}")
    for sid, msg in ref:
        print(f"  ! track {sid}: REFUSED — {msg}")
    print(f"\n{len(acc)} track(s) accepted by {a.by} → {npack_p if acc else '(nothing written)'}; {len(ref)} refused.")
    sys.exit(0 if not ref else (0 if acc else 1))

atoms_list = json.loads((proj / "atoms.json").read_text(encoding="utf-8"))
atoms = {x["atom_id"]: x for x in (atoms_list["atoms"] if isinstance(atoms_list, dict) else atoms_list)}
corpus = " ".join(x["meaning"]["source_text"] for x in atoms.values())

props_p = proj / "voice" / "proposals" / f"{reg}.json"
if not props_p.exists():
    raise SystemExit(f"no proposals store: {props_p}")
_props_store = json.loads(props_p.read_text(encoding="utf-8"))
props = _props_store["proposals"]
beat_props = _props_store.get("beat_proposals") or {}
beats_p = proj / "occurrences" / "beats.json"
beats_by_id = {}
if beats_p.exists():
    beats_by_id = {b["beat_id"]: b for b in
                   json.loads(beats_p.read_text(encoding="utf-8")).get("beats", [])}
allow_text = build_arc_allowlist(proj)

pack_p = proj / "voice" / f"{reg}.json"
pack = json.loads(pack_p.read_text(encoding="utf-8")) if pack_p.exists() else \
       {"pack_version": "voice.v0.1", "register": reg, "entries": {}}

schema = json.loads((P["schemas_dir"] / "voice.pack.schema.json").read_text(encoding="utf-8"))
V = Draft202012Validator(schema)

wanted = (list(props) + list(beat_props)) if a.all else [i.strip() for i in a.ids.split(",")]
accepted, refused = [], []
for aid in wanted:
    if aid.startswith("bt_"):
        bp = beat_props.get(aid)
        if bp is None:
            refused.append((aid, "no such beat proposal")); continue
        beat = beats_by_id.get(aid)
        if beat is None:
            refused.append((aid, "no such beat in occurrences/beats.json")); continue
        if beat.get("status") != "accepted":
            refused.append((aid, f"beat is status {beat.get('status')!r} — ratify the beat in the "
                                  "catalog first; copy cannot outrun its beat")); continue
        if bp.get("status") != "draft":
            refused.append((aid, f"proposal status is {bp.get('status')!r}, not draft")); continue
        if bp["source_hash"] != beat_hash(beat):
            refused.append((aid, "STALE — placement/intent moved since the draft; re-propose")); continue
        btext = a.edit if a.edit else bp["text"]
        bfails = inverse_findings(btext, corpus, allow_text)
        if bfails:
            refused.append((aid, "inverse guard: " + "; ".join(bfails))); continue
        pack.setdefault("beats", {})[aid] = {"text": btext, "status": "accepted", "reviewer": a.by,
                                              "source_hash": beat_hash(beat)}
        accepted.append((aid, "accepted" + (" (with edit)" if a.edit else "")))
        continue
    p = props.get(aid)
    if p is None:
        refused.append((aid, "no such proposal")); continue
    atom = atoms.get(aid)
    if atom is None:
        refused.append((aid, "no such atom")); continue
    if p.get("status") != "draft":
        refused.append((aid, f"proposal status is {p.get('status')!r}, not draft")); continue
    if p["source_hash"] != atom["content_hash"]:
        refused.append((aid, "STALE — meaning moved since the draft; re-propose")); continue
    text = a.edit if a.edit else p["text"]
    fails, notes = invariant_findings(text, atom["meaning"]["source_text"], corpus)
    if fails:
        refused.append((aid, "invent-guard: " + "; ".join(fails))); continue
    pack["entries"][aid] = {"text": text, "status": "accepted", "reviewer": a.by,
                             "source_hash": atom["content_hash"]}
    accepted.append((aid, "accepted" + (" (with edit)" if a.edit else "")
                          + (f"  [sibling-atom: {'; '.join(notes)}]" if notes else "")))

errs = sorted(V.iter_errors(pack), key=lambda e: list(e.path))
if errs:
    print("PACK INVALID — nothing written:")
    for e in errs[:5]:
        print(" ", e.message)
    sys.exit(1)

if accepted:
    pack_p.write_text(json.dumps(pack, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

for aid, msg in accepted:
    print(f"  + {aid}: {msg}")
for aid, msg in refused:
    print(f"  ! {aid}: REFUSED — {msg}")
print(f"\n{len(accepted)} accepted by {a.by} → {pack_p if accepted else '(nothing written)'}; "
      f"{len(refused)} refused. Pack validates. Run tools/validate_voice.py to re-gate the store.")
sys.exit(0 if not refused else (0 if accepted else 1))
