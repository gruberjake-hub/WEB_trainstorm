#!/usr/bin/env python3
"""
griot — the narration facet's runtime (griot.v0.1). Read-then-bind, per the seat's contract.

Wake: an ACCEPTED narration track lacking a narration binding. Griot reads the accepted script
(voice/narration/<register>.json) and the per-brand voice registry, and BINDS the performance:
voice_ref, register, locale, narration_source, script_hash. He writes NO words (the script is
Dragoman's, already accepted), produces NO audio (voiceover_ref stays null until a render step
fills it — "you choose, they produce"), and never re-litigates an existing binding.

Staleness, two ways per the contract: `script_hash` pins the accepted track's text — the track
re-accepted with new words → binding stale; the track itself multi-pins its sources — meaning
moved → track stale → binding transitively stale. Realize refuses to project either.

    python3 tools/griot.py --project ../brunswick/projects/paytrans [--register warm_direct]
    python3 tools/griot.py --selftest
"""
import argparse, hashlib, json, sys, pathlib
import harness_paths

ap = argparse.ArgumentParser()
ap.add_argument("--core"); ap.add_argument("--project")
ap.add_argument("--register", default="warm_direct")
ap.add_argument("--locale", default="en")
ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()


def sha(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_voice_registry(client_brand_dir: pathlib.Path):
    hits = sorted(client_brand_dir.glob("*-voice.registry.json"))
    if not hits:
        return None, None
    reg = json.loads(hits[0].read_text(encoding="utf-8"))
    return {v["id"]: v for v in reg.get("voices", [])}, hits[0].name


def bind(npack, bindings, voices, register, locale, default_voice):
    """Pure: returns (new_bindings_dict, bound_ids, skipped). Never touches existing bindings."""
    out = dict(bindings)
    bound, skipped = [], []
    for sid, tr in (npack.get("tracks") or {}).items():
        if tr.get("status") != "accepted":
            skipped.append((sid, "track not accepted — words before voice"))
            continue
        if sid in out:
            skipped.append((sid, "already bound — not re-litigating"))
            continue
        if default_voice not in voices:
            skipped.append((sid, f"voice_ref '{default_voice}' not in the brand voice registry — flag, don't invent"))
            continue
        out[sid] = {
            "voice_ref": default_voice,
            "register": register,
            "locale": locale,
            "narration_source": f"voice/narration/{register}.json",
            "script_hash": sha(tr["text"]),
            "voiceover_ref": None,
        }
        bound.append(sid)
    return out, bound, skipped


if a.selftest:
    VOICES = {"voice_fx": {"id": "voice_fx"}}
    NP = {"tracks": {
        "s_ok": {"text": "Spoken words.", "status": "accepted", "reviewer": "t", "sources": {}},
        "s_draft": {"text": "Not yet.", "status": "draft", "sources": {}},
    }}
    results = []
    b, bound, skipped = bind(NP, {}, VOICES, "warm_direct", "en", "voice_fx")
    results.append(("accepted track binds; draft track waits (words before voice)",
                    bound == ["s_ok"] and any("not accepted" in s[1] for s in skipped), str(skipped)))
    results.append(("binding pins script_hash and leaves voiceover_ref null (choose, don't produce)",
                    b["s_ok"]["script_hash"] == sha("Spoken words.") and b["s_ok"]["voiceover_ref"] is None, ""))
    b2, bound2, skipped2 = bind(NP, b, VOICES, "warm_direct", "en", "voice_fx")
    results.append(("re-run never re-litigates an existing binding",
                    bound2 == [] and any("already bound" in s[1] for s in skipped2), ""))
    _, bound3, skipped3 = bind(NP, {}, VOICES, "warm_direct", "en", "voice_ghost")
    results.append(("ungoverned voice_ref refuses (flag, don't invent)",
                    bound3 == [] and any("not in the brand voice registry" in s[1] for s in skipped3), ""))
    print(f"{'CHECK':<70} RESULT")
    print("-" * 84)
    ok = True
    for nm, passed, detail in results:
        ok = ok and passed
        print(f"{nm:<70} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
    print("-" * 84)
    print("ALL PASS" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)

P = harness_paths.resolve_core(a.core)
PP = harness_paths.resolve()
proj = PP["project_dir"]
npack_p = proj / "voice" / "narration" / f"{a.register}.json"
if not npack_p.exists():
    raise SystemExit(f"no accepted narration pack: {npack_p} — words before voice.")
npack = json.loads(npack_p.read_text(encoding="utf-8"))

client = proj.parent.parent.name
brand_dir = proj.parent.parent.parent / "brands" / client
voices, reg_name = load_voice_registry(brand_dir)
if voices is None:
    raise SystemExit(f"no voice registry in {brand_dir} — seed <brand>-voice.registry.json first.")
default_voice = sorted(voices)[0] if len(voices) == 1 else None
if default_voice is None:
    raise SystemExit(f"{len(voices)} voices in {reg_name} — choosing needs an authored voice per "
                     "track/lesson; add that deliberately when a second voice exists.")

nb_p = proj / "occurrences" / "narration.json"
store = json.loads(nb_p.read_text(encoding="utf-8")) if nb_p.exists() else {
    "store": "narration", "project": proj.name, "policy": "v1_narration_bindings",
    "spec": "agents/griot/02_system_prompts/core_agent/griot_system_prompt.md",
    "registry": f"brands/{client}/{reg_name}", "bindings": {}}

new_bindings, bound, skipped = bind(npack, store["bindings"], voices, a.register, a.locale, default_voice)
store["bindings"] = new_bindings
for sid in bound:
    print(f"  + {sid}: bound → {default_voice} · {a.register}/{a.locale} · script_hash pinned · voiceover_ref null")
for sid, why in skipped:
    print(f"  · {sid}: skipped — {why}")
if bound:
    nb_p.write_text(json.dumps(store, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{len(bound)} binding(s) → {nb_p}. Audio is a render step; captions can carry the "
          "script now (realize projects scene.voiceover from accepted-and-fresh bindings).")
else:
    print("\nnothing to bind.")
