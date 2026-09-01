#!/usr/bin/env python3
"""
The direction-pack gate — the Responsive Engine's gate for the AUDIENCE coordinate.

Direction packs are the third coordinate of the rendering space: locale packs key a rendering by
LANGUAGE, voice packs by REGISTER, direction packs by AUDIENCE SEGMENT. This gate enforces the
contract layer that keeps that coordinate honest:

    SCHEMA        — every pack validates against schemas/direction.pack.schema.json.
    GOVERNANCE    — weight and tempo resolve to vocab/direction.enum.json (closed lists), and every
                    cited factor resolves to vocab/disposition.enum.json.
    DELTA         — every entry carries audience evidence (a factor:/baseline:/cadence:/mastery:
                    token, or a rule:lead_taken displacement). An entry justified only by
                    rule:intent_default would read the same for EVERY segment — which by direction's
                    own governing test makes it tone, arc or expression, not direction. This is the
                    check that stops a direction pack becoming a dumping ground.
    HARM          — D10, the roster's one hard ethical rule: a binding citing a HIGH-risk factor may
                    not carry weight `lead` or tempo `dwell` (acknowledge, never amplify), and a
                    high or moderate factor may be cited at most ONCE per pack (never repeat). Every
                    spent budget is recorded in pack.harm_budget.
    ANCHOR        — TWO PINS. Each entry's source_hash matches its element's CURRENT source_hash
                    (meaning moved ⇒ the direction decision is stale), and the pack's
                    audience_ref.source_hash matches the segment record's governance.source_hash
                    (the analysis moved ⇒ every binding in the pack is stale).
    JOIN          — every entry keys a real element; the pack's segment_id matches its record.
    BOUNDARY      — audience_ref.record_id is a seg_ record. A lrn_ record is learner data and has
                    no place in a design-time pack (schema-enforced; re-checked here for the message).

What it does NOT check: whether the direction is GOOD. That is what the proposed/accepted flip is
for — and the accepted corpus is what will later license accepting a policy.

    python3 tools/validate_direction.py --project ../brunswick/projects/paytrans
    python3 tools/validate_direction.py --selftest
"""
import argparse, json, sys
from jsonschema import Draft202012Validator, FormatChecker
import harness_paths

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--core"); ap.add_argument("--project"); ap.add_argument("--selftest", action="store_true")
args, _ = ap.parse_known_args()

P = harness_paths.resolve_core(args.core)
core = P["schemas_dir"].parent
schema_p = P["schemas_dir"] / "direction.pack.schema.json"
dir_vocab_p = P["vocab_dir"] / "direction.enum.json"
disp_vocab_p = P["vocab_dir"] / "disposition.enum.json"
for _p in (schema_p, dir_vocab_p, disp_vocab_p):
    if not _p.exists():
        raise SystemExit(f"not found: {_p}")
schema = json.loads(schema_p.read_text(encoding="utf-8"))
dvocab = json.loads(dir_vocab_p.read_text(encoding="utf-8"))
disp = json.loads(disp_vocab_p.read_text(encoding="utf-8"))

results = []
try:
    Draft202012Validator.check_schema(schema)
    results.append(("direction.pack.schema is valid Draft 2020-12", True, ""))
except Exception as e:
    results.append(("direction.pack.schema is valid Draft 2020-12", False, str(e)))
V = Draft202012Validator(schema, format_checker=FormatChecker())

WEIGHTS = {v["id"] for v in dvocab["dimensions"]["weight"]["values"]}
TEMPOS = {v["id"] for v in dvocab["dimensions"]["tempo"]["values"]}
DISPOSITIONS = {v["id"] for v in disp["values"]}
results.append(("direction vocab: closed list declared", dvocab["governance"].get("closed_list") is True, ""))
results.append(("direction vocab: every value names a producing rule",
                all(v.get("produced_by") for d in ("weight", "tempo")
                    for v in dvocab["dimensions"][d]["values"]),
                "a value no rule can write is dead vocabulary"))
results.append(("direction vocab: schema enums match the vocabulary",
                set(schema["$defs"]["entry"]["properties"]["weight"]["enum"]) == WEIGHTS and
                set(schema["$defs"]["entry"]["properties"]["tempo"]["enum"]) == TEMPOS, ""))

AUDIENCE_TOKENS = ("factor:", "baseline:", "cadence:", "mastery:")

def gate_pack(name, pack, elements_by_id, audience=None):
    """elements_by_id: {element_id: source_hash}. audience: the segment record, when resolvable."""
    errs = sorted(V.iter_errors(pack), key=lambda e: list(e.path))
    results.append((f"{name}: validates against schema", not errs,
                    "; ".join(e.message for e in errs)[:180]))
    if errs:
        return
    results.append((f"{name}: audience_ref is a segment record, not learner data",
                    pack["audience_ref"]["record_id"].startswith("seg_"), ""))
    if audience is not None:
        results.append((f"{name}: segment_id matches its record",
                        pack["segment_id"] == audience.get("segment_id"), ""))
        fresh = pack["audience_ref"]["source_hash"] == audience.get("governance", {}).get("source_hash")
        results.append((f"{name}: audience_ref.source_hash is fresh", fresh,
                        "" if fresh else "the audience analysis moved — EVERY binding in this pack is STALE"))
        risk = {f["id"]: f["risk_of_overuse"]["level"]
                for fam in ("inhibitors", "objections", "aligners", "identity_threats",
                             "belief_gaps", "meaning_anchors", "rationalization_patterns")
                for f in audience.get("disposition", {}).get(fam, [])}
    else:
        risk = {}

    seen = {}
    for eid, e in pack["entries"].items():
        results.append((f"{name}: {eid} weight/tempo governed",
                        e["weight"] in WEIGHTS and e["tempo"] in TEMPOS, ""))
        if eid not in elements_by_id:
            results.append((f"{name}: {eid} keys a real element", False, "no such element in the store"))
        else:
            fresh = e["source_hash"] == elements_by_id[eid]
            results.append((f"{name}: {eid} source_hash is fresh", fresh,
                            "" if fresh else "the element's meaning moved — this direction is STALE"))
        evidence = any(t.startswith(AUDIENCE_TOKENS) for t in e["reason"]) or \
                   any(t == "rule:lead_taken" for t in e["reason"])
        results.append((f"{name}: {eid} carries audience evidence", evidence,
                        "justified only by rule:intent_default — that is not direction, it reads "
                        "the same for every segment"))
        for f in e.get("cites", []):
            results.append((f"{name}: {eid} cites governed factor {f}", f in DISPOSITIONS, ""))
            seen.setdefault(f, []).append(eid)
            if risk.get(f) == "high":
                results.append((f"{name}: {eid} does not amplify high-risk {f}",
                                e["weight"] != "lead" and e["tempo"] != "dwell",
                                "risk_of_overuse=high means acknowledge, never amplify"))
    for f, where in seen.items():
        if risk.get(f) in ("high", "moderate"):
            results.append((f"{name}: {f} ({risk[f]}) cited at most once per pack", len(where) == 1,
                            "cited on: " + ", ".join(where)))
    budget = pack.get("harm_budget", {})
    for f, where in seen.items():
        if risk.get(f) in ("high", "moderate"):
            results.append((f"{name}: {f} spend is recorded in harm_budget", f in budget,
                            "the one permitted acknowledgement must be traceable"))
    if any("harm:budget_spent" in t for e in pack["entries"].values() for t in e["reason"]):
        results.append((f"{name}: budget_spent tokens have a recorded spend", bool(budget),
                        "restraint claimed but no harm_budget to point at"))

if args.selftest:
    sys.path.insert(0, str(P["schemas_dir"].parent / "tools"))
    import responsive_engine as RE
    aud = json.loads((core / "reference" / "example_audience_segment.json").read_text(encoding="utf-8"))
    H = "sha256:" + "b" * 64
    els = [{"element_id": "ele_fx_gap", "type": "Statement", "source_hash": H,
            "intent": {"rhetorical": "assert", "teaches": ["obj_bw_emp_pay_factors"]}},
           {"element_id": "ele_fx_list", "type": "List", "source_hash": H,
            "intent": {"rhetorical": "structure", "teaches": []}}]
    good = RE.resolve(els, aud)
    ebi = {e["element_id"]: e["source_hash"] for e in els}
    n0 = len(results); gate_pack("fixture(good)", good, ebi, aud)
    results.append(("selftest: a freshly resolved pack passes every check",
                    all(ok for _, ok, _ in results[n0:]), ""))

    def red(label, mutate):
        pack = json.loads(json.dumps(good)); a = json.loads(json.dumps(aud)); e = dict(ebi)
        mutate(pack, a, e)
        hold = results[:]; del results[:]
        gate_pack("fixture(red)", pack, e, a)
        failed = any(not ok for _, ok, _ in results)
        del results[:]; results.extend(hold)
        results.append((label, failed, "" if failed else "mutation was NOT caught"))

    first = next(iter(good["entries"]))
    red("selftest: ungoverned weight is caught",
        lambda p, a, e: p["entries"][first].update(weight="hero"))
    red("selftest: ungoverned tempo is caught",
        lambda p, a, e: p["entries"][first].update(tempo="glacial"))
    red("selftest: empty reason trace is caught",
        lambda p, a, e: p["entries"][first].update(reason=[]))
    red("selftest: intent_default-only entry is caught (not direction)",
        lambda p, a, e: p["entries"][first].update(reason=["rule:intent_default"]))
    red("selftest: prose reason token is caught",
        lambda p, a, e: p["entries"][first].update(reason=["because the audience is defensive"]))
    red("selftest: stale element source_hash (meaning moved) is caught",
        lambda p, a, e: e.update({first: "sha256:" + "c" * 64}))
    red("selftest: stale audience pin (analysis moved) is caught",
        lambda p, a, e: a["governance"].update(source_hash="sha256:" + "d" * 64))
    red("selftest: entry keying a missing element is caught",
        lambda p, a, e: e.pop(first))
    red("selftest: ungoverned cited factor is caught",
        lambda p, a, e: p["entries"][first].update(cites=["gap_not_in_vocab"],
                                                   reason=p["entries"][first]["reason"] + ["factor:gap_not_in_vocab"]))
    red("selftest: learner record in a design-time pack is caught",
        lambda p, a, e: p["audience_ref"].update(record_id="lrn_someone"))
    red("selftest: accepted binding without a reviewer is caught",
        lambda p, a, e: p["entries"][first].update(status="accepted"))
    def _amplify(p, a, e):
        for f in a["disposition"]["belief_gaps"] + a["disposition"]["identity_threats"]:
            f["risk_of_overuse"]["level"] = "high"
        p["entries"][first].update(weight="lead", tempo="dwell",
                                    cites=["gap_midpoint_means_average"],
                                    reason=p["entries"][first]["reason"] + ["factor:gap_midpoint_means_average"])
    red("selftest: amplifying a high-risk factor (lead/dwell) is caught", _amplify)
    def _repeat(p, a, e):
        for f in a["disposition"]["belief_gaps"]:
            f["risk_of_overuse"]["level"] = "high"
        for k in p["entries"]:
            p["entries"][k]["cites"] = ["gap_midpoint_means_average"]
            p["entries"][k]["weight"] = "support"; p["entries"][k]["tempo"] = "measured"
            p["entries"][k]["reason"] = ["rule:intent_default", "factor:gap_midpoint_means_average"]
        e.update({k: p["entries"][k]["source_hash"] for k in p["entries"]})
    red("selftest: repeating a high-risk factor across entries is caught", _repeat)
    red("selftest: budget_spent claimed with no recorded spend is caught",
        lambda p, a, e: (p.pop("harm_budget", None),
                         p["entries"][first].__setitem__("reason",
                             p["entries"][first]["reason"] + ["harm:budget_spent:high"])))
else:
    PP = harness_paths.resolve()
    proj = PP["project_dir"]
    els_p = proj / "occurrences" / "elements.json"
    if not els_p.exists():
        raise SystemExit(f"not found: {els_p}")
    _e = json.loads(els_p.read_text(encoding="utf-8"))
    _elist = _e["elements"] if isinstance(_e, dict) and "elements" in _e else _e
    ebi = {e["element_id"]: e["source_hash"] for e in _elist}
    aud_by_seg = {}
    ad = proj / "audience"
    if ad.exists():
        for rp in sorted(ad.glob("*.json")):
            r = json.loads(rp.read_text(encoding="utf-8"))
            aud_by_seg[r.get("segment_id")] = r
    dd = proj / "direction"
    packs = sorted(dd.glob("*.json")) if dd.exists() else []
    if not packs:
        results.append(("no direction packs in project — contract-only pass", True, f"looked in {dd}"))
    for pk in packs:
        pack = json.loads(pk.read_text(encoding="utf-8"))
        gate_pack(pk.name, pack, ebi, aud_by_seg.get(pack.get("segment_id")))

print(f"{'CHECK':<62} RESULT")
print("-" * 76)
bad = 0
for label, ok, note in results:
    print(f"{label[:62]:<62} {'PASS' if ok else 'FAIL'}" + (f"   {note}" if note and not ok else ""))
    bad += 0 if ok else 1
print("-" * 76)
print(f"{len(results) - bad} passed, {bad} failed")
sys.exit(1 if bad else 0)
