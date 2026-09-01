#!/usr/bin/env python3
"""
responsive_engine — the direction facet owner's runtime (responsive_engine.v0.1, policy direction_v1).

THE SEAT. The roster's Responsive Engine, born in its design-time mode. It owns ONE facet —
`direction` — and writes it to exactly one place: `direction/<segment_id>.json` per project.
It holds no PII in either mode; the learner-state half (transcript, posteriors) is a SEPARATE
future seat (see capability_horizon/learner-response-intelligence).

TWO MODES, one of which runs:

    resolve  (live)        design-time batch. Walk every element × one segment record, resolve the
                           audience join, and materialize a reviewable pack of proposed bindings.
    serve    (live:false)  runtime, per learner, materializing nothing. DECLARED, NOT BUILT — it
                           waits on the horizon's activation signals. Asking for it is refused,
                           loudly, with the reason.

The core is a PURE FUNCTION — `propose()` + `clamp()` take dicts and return dicts: no I/O, no
clock, no notion of who is asking. That is the whole promotion path: `resolve` runs it under a
batch harness, `serve` will run the same function under a serve-one harness. Only the harness
swaps.

WHAT IT WRITES, AND WHAT IT REFUSES TO WRITE. An entry is emitted only when at least one
AUDIENCE-DERIVED rule fired. The `rule:intent_default` mapping alone would be identical for every
segment — and by direction's own governing test, a value that does not vary by segment is not
direction, it is tone, arc or expression. So the pack is exactly the audience delta, and the
invariance test is structural rather than aspirational.

THE HARM CLAMP (D10, the roster's one hard ethical rule). A binding that cites an audience factor
is constrained by that factor's `risk_of_overuse`: high — never `lead`, never `dwell`, cited at
most once per pack; moderate — cited at most once per pack; low — free. The clamp records what it
did (`harm:` tokens) rather than silently declining.

    python3 tools/responsive_engine.py --project ../brunswick/projects/paytrans
    python3 tools/responsive_engine.py --project ... --audience reference/example_audience_segment.json --dry-run
    python3 tools/responsive_engine.py --selftest
"""
import argparse, json, sys, datetime
import harness_paths

POLICY = "direction_v1"
TOOL = "tools/responsive_engine.py"

# ---------------------------------------------------------------- the pure core

# rule:intent_default — the audience-blind baseline every element starts from. NOT written on its
# own: it is the floor the audience rules move away from.
WEIGHT_BY_RHETORICAL = {
    "orient": "anchor", "refine": "anchor", "organize": "anchor",
    "assert": "lead", "persuade": "lead",
    "explain": "support", "specify": "support", "structure": "support", "contextualize": "support",
    "transition": "aside", "support": "aside",
}

def _factors(audience):
    """Every disposition factor, flattened, in a deterministic order."""
    disp = audience.get("disposition", {})
    out = []
    for fam in ("inhibitors", "objections", "aligners", "identity_threats",
                "belief_gaps", "meaning_anchors", "rationalization_patterns"):
        for f in disp.get(fam, []):
            out.append(f)
    return out

def _scene_of(element):
    sc = (element.get("ext") or {}).get("scene")
    return (sc or {}).get("id") if isinstance(sc, dict) else sc

def baseline(element):
    """PURE, AUDIENCE-BLIND. What this element's delivery would be for ANY segment: weight from
    rhetorical intent, tempo measured. This is the floor direction is measured against — and the
    reason a pack is a DELTA. A binding equal to the baseline reads the same for every segment,
    which by direction's own governing test makes it tone, arc or expression, not direction."""
    intent = element.get("intent") or {}
    return WEIGHT_BY_RHETORICAL.get(intent.get("rhetorical"), "support"), "measured"

def _budget(factor, risk, spent):
    """(ok_to_cite, level). high and moderate factors may be cited ONCE per pack."""
    level = risk.get(factor, "low")
    return (not (level in ("high", "moderate") and spent.get(factor))), level

def propose(element, audience, state=None):
    """PURE. (element, segment record, state) -> (weight, tempo, reason[], cites[], state').

    `state` carries the two budgets the pack-level rules need — the harm budget (a high/moderate
    factor is cited once per pack) and the scene lead budget (an audience rule may promote at most
    ONE element per scene to `lead`). Budgets are checked BEFORE a rule fires, never after: a rule
    whose factor is spent does not apply its effect at all. (An earlier draft dropped the citation
    but kept the effect — which is how "never repeat" quietly becomes "repeat without saying so".)

    Rule order is fixed and stated, because a reviewer must be able to replay it:
      1 intent_default     weight from rhetorical intent; tempo measured        (the baseline)
      2 belief_gap_lead    an element teaching a gap-targeted objective becomes load-bearing
      3 threat_anchor      ... unless a threat targets it and identity_safety is low — safety
                           before correction, so this OVERRIDES rule 2 (stated precedence)
      4 cadence_chunk      a set larger than the segment's chunk tolerance arrives in parts
      5 density_shed       unteaching support drops to aside when density tolerance is sparse
      6 low_efficacy_dwell new AND consequential material gets time when self-efficacy is low
      7 known_brisk        material the segment already holds moves fast
    v1 acts on gap_ and thr_ factors, the four baselines, cadence and mastery. The other factor
    families (inh_, obj_x_, aln_, mng_, rat_) are READ but unused here — later rule sets, not
    silent behavior.

    Direction never re-emphasises what the content already emphasises: it makes at most one
    segment-specific promotion per scene and leaves the content's own weighting alone.
    """
    state = {"spent": {}, "scene_lead": {}} if state is None else \
            {"spent": dict(state.get("spent", {})), "scene_lead": dict(state.get("scene_lead", {}))}
    intent = element.get("intent") or {}
    teaches = set(intent.get("teaches") or [])
    base = audience.get("baselines", {})
    cad = audience.get("cadence", {})
    mastery = {m["objective_id"]: m["level"] for m in audience.get("standing", {}).get("mastery", [])}
    risk = {f["id"]: f["risk_of_overuse"]["level"] for f in _factors(audience)}
    scene = _scene_of(element)

    weight, tempo = baseline(element)
    reason = ["rule:intent_default"]
    cites = []

    # 2 · belief_gap_lead — at most one audience-promoted lead per scene, and the factor's budget
    gap_hit = next((f for f in _factors(audience)
                    if f["id"].startswith("gap_") and teaches & set(f.get("objective_ids") or [])), None)
    if gap_hit:
        ok, level = _budget(gap_hit["id"], risk, state["spent"])
        if not ok:
            reason.append(f"harm:budget_spent:{level}")
        elif state["scene_lead"].get(scene):
            reason.append("rule:lead_taken")
        else:
            weight = "lead"
            reason += ["rule:belief_gap_lead", f"factor:{gap_hit['id']}"]
            cites.append(gap_hit["id"])
            state["scene_lead"][scene] = True
            if level in ("high", "moderate"):
                state["spent"][gap_hit["id"]] = {"level": level, "spent_on": element["element_id"]}

    # 3 · threat_anchor (overrides 2 — safety before correction)
    if base.get("identity_safety", {}).get("value", 1.0) < 0.5:
        thr_hit = next((f for f in _factors(audience)
                        if f["id"].startswith("thr_") and teaches & set(f.get("objective_ids") or [])), None)
        if thr_hit:
            ok, level = _budget(thr_hit["id"], risk, state["spent"])
            if not ok:
                reason.append(f"harm:budget_spent:{level}")
            else:
                weight = "anchor"
                reason += ["rule:threat_anchor", f"factor:{thr_hit['id']}", "baseline:identity_safety<0.5"]
                cites.append(thr_hit["id"])
                if level in ("high", "moderate"):
                    state["spent"][thr_hit["id"]] = {"level": level, "spent_on": element["element_id"]}

    # 4 · cadence_chunk
    if cad.get("chunk_tolerance") == "short" and element.get("type") == "List":
        tempo = "progressive"
        reason += ["rule:cadence_chunk", "cadence:chunk_tolerance=short"]

    # 5 · density_shed
    if cad.get("density_tolerance") == "sparse" and weight == "support" and not teaches:
        weight = "aside"
        reason += ["rule:density_shed", "cadence:density_tolerance=sparse"]

    # 6 · low_efficacy_dwell
    if tempo == "measured" and base.get("self_efficacy", {}).get("value", 1.0) < 0.5:
        weak = sorted(o for o in teaches if mastery.get(o, 1.0) < 0.3)
        if weak:
            tempo = "dwell"
            reason += ["rule:low_efficacy_dwell", f"mastery:{weak[0]}<0.3"]

    # 7 · known_brisk
    if tempo == "measured" and teaches and all(mastery.get(o, 0.0) >= 0.6 for o in teaches):
        tempo = "brisk"
        reason += ["rule:known_brisk", f"mastery:{sorted(teaches)[0]}>=0.6"]

    return weight, tempo, reason, cites, state

def clamp(weight, tempo, reason, cites, audience):
    """PURE. The high-risk restriction: a binding citing a high-risk factor may be an
    acknowledgement but never an amplification — no `lead`, no `dwell`. (The once-per-pack half of
    the rule is enforced in propose(), before the effect is applied.) The clamp records what it
    did rather than silently declining."""
    risk = {f["id"]: f["risk_of_overuse"]["level"] for f in _factors(audience)}
    reason = list(reason)
    if any(risk.get(f) == "high" for f in cites):
        if weight == "lead":
            weight = "support"
            reason.append("harm:high\u2192no_lead")
        if tempo == "dwell":
            tempo = "measured"
            reason.append("harm:high\u2192no_dwell")
    return weight, tempo, reason, cites

AUDIENCE_TOKENS = ("factor:", "baseline:", "cadence:", "mastery:")

def resolve(elements, audience, resolved_at=None):
    """PURE. The batch harness: (elements, one segment record) -> a direction pack dict.
    Deterministic — same inputs, same bytes.

    Emits an entry ONLY where the resolved binding DIFFERS from the audience-blind baseline. That
    is the invariance test made structural: a pack contains the audience delta and nothing else,
    so it cannot silently accumulate decisions that belong to tone, arc or expression."""
    entries, state = {}, {"spent": {}, "scene_lead": {}}
    for el in elements:
        w, t, reason, cites, state = propose(el, audience, state)
        w, t, reason, cites = clamp(w, t, reason, cites, audience)
        if (w, t) == baseline(el):
            continue
        entry = {"weight": w, "tempo": t, "reason": reason,
                 "source_hash": el["source_hash"], "status": "proposed"}
        if cites:
            entry["cites"] = cites
        entries[el["element_id"]] = entry
    pack = {
        "pack_version": "direction.v0.1",
        "segment_id": audience["segment_id"],
        "audience_ref": {"record_id": audience["record_id"],
                          "source_hash": audience["governance"]["source_hash"]},
        "resolved_by": {"tool": TOOL, "policy": POLICY, "mode": "resolve"},
        "entries": entries,
    }
    # The harm budget is recorded at pack level because it can be spent on an element that
    # produces NO entry (the audience rule agreed with the content's own weighting, so there was
    # no delta to write). Without this, a reader sees `harm:budget_spent` tokens and no record of
    # where the one permitted acknowledgement went — the restraint would be invisible.
    if state["spent"]:
        pack["harm_budget"] = dict(sorted(state["spent"].items()))
    if resolved_at:
        pack["resolved_by"]["resolved_at"] = resolved_at
    return pack

# ---------------------------------------------------------------- harness

def _load_elements(proj):
    p = proj / "occurrences" / "elements.json"
    if not p.exists():
        raise SystemExit(f"not found: {p}")
    d = json.loads(p.read_text(encoding="utf-8"))
    return d["elements"] if isinstance(d, dict) and "elements" in d else d

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--core"); ap.add_argument("--project")
    ap.add_argument("--mode", default="resolve", choices=["resolve", "serve"])
    ap.add_argument("--audience", help="path to ONE segment record; default: every record in <project>/audience/")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a, _ = ap.parse_known_args()

    P = harness_paths.resolve_core(a.core)
    core = P["schemas_dir"].parent
    modes = json.loads((core / "agents" / "responsive_engine" / "modes.json").read_text(encoding="utf-8"))
    live = {m["id"]: m.get("live", False) for m in modes["modes"]}

    if a.selftest:
        return selftest(core)

    if not live.get(a.mode):
        why = next(m.get("why_not_live", "") for m in modes["modes"] if m["id"] == a.mode)
        print(f"mode '{a.mode}' is DECLARED, not live — refusing to run.\n  {why}")
        return 2

    PP = harness_paths.resolve()
    proj = PP["project_dir"]
    elements = _load_elements(proj)
    if a.audience:
        recs = [core / a.audience if not str(a.audience).startswith("/") else a.audience]
    else:
        d = proj / "audience"
        recs = sorted(d.glob("*.json")) if d.exists() else []
    if not recs:
        print(f"no segment records in {proj / 'audience'} — nothing to resolve. "
              f"(Pass --audience <record> to dry-run against one.)")
        return 0

    for rp in recs:
        aud = json.loads(open(rp, encoding="utf-8").read())
        pack = resolve(elements, aud,
                       resolved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
        out = proj / "direction" / f"{aud['segment_id']}.json"
        n = len(pack["entries"])
        if a.dry_run:
            print(f"[dry-run] {rp.name} → {out}  ({n} of {len(elements)} elements directed)")
            for eid, e in list(pack["entries"].items())[:6]:
                print(f"    {eid:<44} {e['weight']:<8} {e['tempo']:<12} {' '.join(e['reason'])}")
            if n > 6:
                print(f"    … {n - 6} more")
        else:
            out.parent.mkdir(exist_ok=True)
            out.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"wrote {out}  ({n} of {len(elements)} elements directed)")
    return 0

# ---------------------------------------------------------------- selftest

def selftest(core):
    aud = json.loads((core / "reference" / "example_audience_segment.json").read_text(encoding="utf-8"))
    H = "sha256:" + "a" * 64
    def el(eid, rhet, teaches=(), typ="Statement"):
        return {"element_id": eid, "type": typ, "source_hash": H,
                "intent": {"rhetorical": rhet, "teaches": list(teaches)}}
    results = []
    def check(label, ok, note=""):
        results.append((label, ok, note))

    els = [
        el("ele_fx_orient", "orient"),
        el("ele_fx_gap", "assert", ["obj_bw_emp_pay_factors"]),
        el("ele_fx_gap2", "assert", ["obj_bw_emp_pay_factors"]),
        el("ele_fx_known", "assert", ["obj_bw_emp_total_rewards"]),
        el("ele_fx_list", "structure", [], "List"),
        el("ele_fx_bridge", "transition"),
    ]
    pack = resolve(els, aud)
    ent = pack["entries"]

    check("selftest: resolver is deterministic (same inputs, same bytes)",
          json.dumps(resolve(els, aud), sort_keys=True) == json.dumps(pack, sort_keys=True))
    check("selftest: a binding equal to the audience-blind baseline is NOT written",
          "ele_fx_bridge" not in ent,
          "an entry that reads the same for every segment is tone/arc/expression, not direction")
    check("selftest: every emitted entry differs from baseline",
          all((e["weight"], e["tempo"]) != baseline(x)
              for x in els for e in [ent.get(x["element_id"])] if e))
    check("selftest: every emitted entry cites audience evidence",
          all(any(t.startswith(AUDIENCE_TOKENS) for t in e["reason"]) for e in ent.values()))
    e = ent.get("ele_fx_gap")
    check("selftest: threat_anchor overrides belief_gap_lead (safety before correction)",
          e is not None and e["weight"] == "anchor" and "rule:threat_anchor" in e["reason"],
          json.dumps(e) if e else "no entry")
    check("selftest: chunk tolerance turns a set progressive",
          ent.get("ele_fx_list", {}).get("tempo") == "progressive")
    check("selftest: a high-risk factor is cited at most once per pack",
          sum(1 for x in ent.values() if "thr_seniority_not_valued" in (x.get("cites") or [])) == 1)
    check("selftest: a spent budget withholds the EFFECT, not just the citation",
          "ele_fx_gap2" not in ent or ent["ele_fx_gap2"]["weight"] != "anchor",
          "the second match must not silently inherit the first's promotion")
    fluent = json.loads(json.dumps(aud))          # the reference segment holds no objective at 0.6+
    for m in fluent["standing"]["mastery"]:
        if m["objective_id"] == "obj_bw_emp_total_rewards":
            m["level"] = 0.7
    check("selftest: mastery the segment already holds moves brisk",
          resolve([el("ele_fx_known", "assert", ["obj_bw_emp_total_rewards"])],
                  fluent)["entries"].get("ele_fx_known", {}).get("tempo") == "brisk")

    # scene lead scarcity — an audience rule may promote ONE element per scene
    def sc(eid, teaches, scene):
        e2 = el(eid, "explain", teaches); e2["ext"] = {"scene": {"id": scene}}; return e2
    calm = json.loads(json.dumps(aud))
    calm["baselines"]["identity_safety"]["value"] = 0.9        # disable threat_anchor
    twopack = resolve([sc("ele_fx_a", ["obj_bw_emp_pay_factors"], "s1"),
                       sc("ele_fx_b", ["obj_bw_emp_pay_factors"], "s1")], calm)
    check("selftest: at most one audience-promoted lead per scene",
          sum(1 for x in twopack["entries"].values() if x["weight"] == "lead") == 1,
          json.dumps({k: v["weight"] for k, v in twopack["entries"].items()}))

    # the clamp: a HIGH-risk belief gap must not become the lead
    hot = json.loads(json.dumps(calm))
    hot["disposition"]["belief_gaps"][0]["risk_of_overuse"]["level"] = "high"
    g = resolve([el("ele_fx_gap", "assert", ["obj_bw_emp_pay_factors"])], hot)["entries"].get("ele_fx_gap", {})
    check("selftest: harm clamp refuses `lead` for a high-risk factor",
          g.get("weight") == "support" and "harm:high\u2192no_lead" in g.get("reason", []),
          json.dumps(g))
    hot2 = json.loads(json.dumps(hot))
    hot2["baselines"]["self_efficacy"]["value"] = 0.2
    # `orient` so the clamped result still differs from baseline and is therefore written;
    # with an `explain` element the clamp lands exactly back on baseline and — correctly —
    # nothing is written at all, which is the right behavior but proves nothing here.
    g2 = resolve([el("ele_fx_gap", "orient", ["obj_bw_emp_pay_factors"])], hot2)["entries"]["ele_fx_gap"]
    check("selftest: harm clamp refuses `dwell` for a high-risk factor",
          g2["tempo"] != "dwell" and "harm:high\u2192no_dwell" in g2["reason"], json.dumps(g2))

    # modes
    modes = json.loads((core / "agents" / "responsive_engine" / "modes.json").read_text(encoding="utf-8"))
    by = {m["id"]: m for m in modes["modes"]}
    check("selftest: mode `resolve` is live", by["resolve"]["live"] is True)
    check("selftest: mode `serve` is declared and NOT live", by["serve"]["live"] is False,
          "the aspiration is declared; only the design-time half runs")

    print(f"{'CHECK':<62} RESULT")
    print("-" * 76)
    bad = 0
    for label, ok, note in results:
        print(f"{label[:62]:<62} {'PASS' if ok else 'FAIL'}" + (f"   {note}" if note and not ok else ""))
        bad += 0 if ok else 1
    print("-" * 76)
    print(f"{len(results) - bad} passed, {bad} failed")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
