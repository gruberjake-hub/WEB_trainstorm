#!/usr/bin/env python3
"""
The audience-model gate — the Audience Agent's gate for the SEGMENT record.

The audience model is the sibling graph: populations, not persons, keyed to segments, joined to
content only through objective_ids. This gate enforces the contract layer that keeps it that way:

    SCHEMA        — every record validates against schemas/audience-model.schema.json (PII-blind by
                    construction: closed properties, governed ids, reason tokens — no prose about people).
    GOVERNANCE    — every disposition factor id and the affective_pattern resolve to
                    vocab/disposition.enum.json (closed list). An APPROVED record may not cite a `seed`
                    entry — seeds exist to make the contract testable, not to describe real audiences.
    HARM GATE     — every factor carries risk_of_overuse (schema-required); the gate additionally
                    refuses a record whose governance.status is approved while a `high`-risk factor
                    lacks an objective_ids scope — "high" means never amplified, so it must say where
                    it applies. (unification-map §2: a gate in the join, not a note in the margin.)
    BOUNDARY      — a `kind: learner` record (the Responsive Engine's reserved live shape) is NEVER
                    legal in a content project store. Learner data belongs to the separately governed
                    learner-data domain. Finding one here is a red result, not a warning.
    ANCHOR        — every mastery / factor objective_id resolves to ontology/objectives.json.
    JOIN          — a record's segment_id is unique within the project's audience/ dir.

What it does NOT check: whether the psychology is right. Stage 1 validates plumbing; Stage 1.5's
evidence flags and Stage 2's real evidence are where that gets tested (architecture/lre-stage1-synthetic-learner.md).

    python3 tools/validate_audience.py --project ../brunswick/projects/paytrans   # gate real records
    python3 tools/validate_audience.py --selftest                                  # fixtures, proves red

With --project and no audience/ dir present, the run is a contract-only pass (schema + vocab +
reference example) and says so — segment records are optional until the Audience Agent pass lands.
"""
import argparse, json, sys, pathlib
from jsonschema import Draft202012Validator, FormatChecker
import harness_paths

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--core"); ap.add_argument("--project"); ap.add_argument("--selftest", action="store_true")
args, _ = ap.parse_known_args()

P = harness_paths.resolve_core(args.core)
schema_p = P["schemas_dir"] / "audience-model.schema.json"
vocab_p = P["vocab_dir"] / "disposition.enum.json"
core_dir = P["schemas_dir"].parent
ontology_p = core_dir / "ontology" / "objectives.json"
example_p = core_dir / "reference" / "example_audience_segment.json"
for _p in (schema_p, vocab_p, ontology_p):
    if not _p.exists():
        raise SystemExit(f"not found: {_p}")
schema = json.loads(schema_p.read_text(encoding="utf-8"))
vocab = json.loads(vocab_p.read_text(encoding="utf-8"))
_ont = json.loads(ontology_p.read_text(encoding="utf-8"))
_objs = _ont.get("objectives", _ont)
OBJECTIVE_IDS = set(_objs.keys()) if isinstance(_objs, dict) else {o.get("id") or o.get("objective_id") for o in _objs}

results = []

# ---------------------------------------------------------------- contract layer (always runs)

try:
    Draft202012Validator.check_schema(schema)
    results.append(("audience-model.schema is valid Draft 2020-12", True, ""))
except Exception as e:
    results.append(("audience-model.schema is valid Draft 2020-12", False, str(e)))

V = Draft202012Validator(schema, format_checker=FormatChecker())

_vals = vocab.get("values", [])
_ids = [v["id"] for v in _vals]
results.append(("disposition vocab: ids unique", len(_ids) == len(set(_ids)), ""))
results.append(("disposition vocab: closed list declared", vocab.get("governance", {}).get("closed_list") is True, ""))
_fams = vocab.get("governance", {}).get("families", {})
_bad_fam = [v["id"] for v in _vals if not any(v["id"].startswith(f) for f in _fams)]
results.append(("disposition vocab: every id belongs to a declared family", not _bad_fam, ", ".join(_bad_fam)))
_bad_status = [v["id"] for v in _vals if v.get("status") not in ("seed", "specified")]
results.append(("disposition vocab: every status is seed|specified", not _bad_status, ", ".join(_bad_status)))
GOVERNED = set(_ids)
SEED = {v["id"] for v in _vals if v.get("status") == "seed"}

FACTOR_FAMILIES = ("inhibitors", "objections", "aligners", "identity_threats",
                   "belief_gaps", "meaning_anchors", "rationalization_patterns")

# ---------------------------------------------------------------- record gate (shared by both modes)

def gate_record(name, rec, in_project_store=True, objective_ids=None):
    """Append results for one audience record. in_project_store=True means the record was found in a
    content project's audience/ dir — where a learner-kind record is illegal."""
    objective_ids = OBJECTIVE_IDS if objective_ids is None else objective_ids
    errs = sorted(V.iter_errors(rec), key=lambda e: list(e.path))
    results.append((f"{name}: validates against schema", not errs,
                    "; ".join(e.message for e in errs)[:180]))
    if errs:
        return
    if in_project_store:
        results.append((f"{name}: is a segment record (no learner data in a content store)",
                        rec["kind"] == "segment",
                        "" if rec["kind"] == "segment" else
                        "kind=learner found in a CONTENT project store — learner data lives in the learner-data domain"))
    approved = rec["governance"]["status"] == "approved"
    disp = rec.get("disposition", {})
    factors = [f for fam in FACTOR_FAMILIES for f in disp.get(fam, [])]
    for f in factors:
        fid = f["id"]
        results.append((f"{name}: factor {fid} is governed", fid in GOVERNED, "not in disposition.enum.json"))
        if approved and fid in SEED:
            results.append((f"{name}: approved record cites no seed factor ({fid})", False,
                            "seed entries make the contract testable; they do not describe a real audience"))
        if approved and f["risk_of_overuse"]["level"] == "high" and not f.get("objective_ids"):
            results.append((f"{name}: high-risk factor {fid} is scoped to objectives", False,
                            "risk_of_overuse=high means never amplified — it must say where it applies"))
        for oid in f.get("objective_ids", []):
            results.append((f"{name}: factor {fid} → {oid} resolves in ontology", oid in objective_ids, ""))
    aff = disp.get("affective_pattern")
    if aff is not None:
        results.append((f"{name}: affective_pattern {aff} is governed", aff in GOVERNED, ""))
        if approved and aff in SEED:
            results.append((f"{name}: approved record cites no seed affect ({aff})", False, ""))
    for m in rec.get("standing", {}).get("mastery", []):
        results.append((f"{name}: mastery {m['objective_id']} resolves in ontology",
                        m["objective_id"] in objective_ids, ""))

# ---------------------------------------------------------------- selftest (fixtures; proves red)

if args.selftest:
    good = json.loads(example_p.read_text(encoding="utf-8"))
    n0 = len(results); gate_record("fixture(good)", good)
    results.append(("selftest: reference example passes every record check",
                    all(ok for _, ok, _ in results[n0:]), ""))

    def red(label, mutate, in_store=True):
        rec = json.loads(json.dumps(good))
        mutate(rec)
        hold = results[:]           # run the gate into a scratch window, then restore
        del results[:]
        gate_record("fixture(red)", rec, in_project_store=in_store)
        failed = any(not ok for _, ok, _ in results)
        del results[:]
        results.extend(hold)
        results.append((label, failed, "" if failed else "mutation was NOT caught"))

    def approve(r):
        r["governance"]["status"] = "approved"

    red("selftest: stray person field (name) is caught",
        lambda r: r.update(name="J. Gruber"))
    red("selftest: free-text factor id is caught",
        lambda r: r["disposition"]["inhibitors"][0].update(id="fear of being underpaid"))
    red("selftest: well-formed but ungoverned factor id is caught",
        lambda r: r["disposition"]["inhibitors"][0].update(id="inh_not_in_vocab"))
    red("selftest: factor without risk_of_overuse is caught",
        lambda r: r["disposition"]["aligners"][0].pop("risk_of_overuse"))
    red("selftest: prose basis (not a reason token) is caught",
        lambda r: r["baselines"]["trust"].update(basis="we think they probably don't trust HR much"))
    red("selftest: confidence-shaped basis (number) is caught",
        lambda r: r["baselines"]["trust"].update(basis=0.7))
    red("selftest: trajectory variable smuggled into baselines (clarity) is caught",
        lambda r: r["baselines"].update(clarity={"value": 0.3, "basis": "prior:segment_default"}))
    red("selftest: kind/record_id prefix mismatch is caught",
        lambda r: r.update(kind="learner"))
    red("selftest: learner-kind record in a content store is caught",
        lambda r: r.update(kind="learner", record_id="lrn_x"))
    red("selftest: unknown objective_id is caught",
        lambda r: r["standing"]["mastery"][0].update(objective_id="obj_does_not_exist"))
    red("selftest: approved record citing a seed factor is caught", approve)
    # isolate the harm gate: pretend every vocab entry is specified, so ONLY the unscoped high-risk
    # factor can trip the approved record
    _seed_hold = set(SEED); SEED.clear()
    red("selftest: approved record with unscoped high-risk factor is caught",
        lambda r: (approve(r), r["disposition"]["identity_threats"][0].pop("objective_ids")))
    rec = json.loads(json.dumps(good)); approve(rec)
    hold = results[:]; del results[:]
    gate_record("fixture(approved, all scoped)", rec)
    ok = all(o for _, o, _ in results)
    del results[:]; results.extend(hold)
    results.append(("selftest: approved record with every high-risk factor scoped passes", ok, ""))
    SEED.update(_seed_hold)
    # the learner shape is legal OUTSIDE a content store (the reserved Stage-2 contract):
    rec = json.loads(json.dumps(good)); rec.update(kind="learner", record_id="lrn_fx")
    hold = results[:]; del results[:]
    gate_record("fixture(learner, learner-domain)", rec, in_project_store=False)
    ok = all(o for _, o, _ in results)
    del results[:]; results.extend(hold)
    results.append(("selftest: learner-kind record is legal outside a content store (reserved contract)", ok, ""))

# ---------------------------------------------------------------- project mode (real records)

else:
    n0 = len(results)
    gate_record("reference/example_audience_segment.json",
                json.loads(example_p.read_text(encoding="utf-8")), in_project_store=False)
    PP = harness_paths.resolve()
    proj = PP["project_dir"]
    aud_dir = proj / "audience"
    recs = sorted(aud_dir.glob("*.json")) if aud_dir.exists() else []
    if not recs:
        results.append(("no audience records in project — contract-only pass", True, f"looked in {aud_dir}"))
    seen = {}
    for rp in recs:
        rec = json.loads(rp.read_text(encoding="utf-8"))
        gate_record(rp.name, rec)
        sid = rec.get("segment_id")
        if sid in seen:
            results.append((f"{rp.name}: segment_id {sid} unique in project", False, f"also in {seen[sid]}"))
        seen[sid] = rp.name

# ---------------------------------------------------------------- report

print(f"{'CHECK':<62} RESULT")
print("-" * 76)
bad = 0
for label, ok, note in results:
    print(f"{label[:62]:<62} {'PASS' if ok else 'FAIL'}" + (f"   {note}" if note and not ok else ""))
    bad += 0 if ok else 1
print("-" * 76)
print(f"{len(results) - bad} passed, {bad} failed")
sys.exit(1 if bad else 0)
