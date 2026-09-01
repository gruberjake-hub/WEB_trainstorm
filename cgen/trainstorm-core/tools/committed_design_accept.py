#!/usr/bin/env python3
"""
committed_design_accept — the ONLY writer that can set status validated.

The acceptance half of Case-Author stage 1 (voice_accept / accept_value pattern):
headwater_case_author.py proposes status "proposed"; a human runs THIS script;
this script is what validation *is*, mechanically. The agent has no path to
validated — it cannot pass --by as itself (human-shaped reviewer required) and
the propose tool never writes that status.

    python3 tools/committed_design_accept.py --file reference/example_committed_design.json --by jake
    python3 tools/committed_design_accept.py --selftest

Every acceptance re-runs validate_committed_design.gate_doc at acceptance time.
Refuses: missing --by, agent-shaped --by, missing warrant-and-escape,
unreachable-LO terminal, status already validated, gate failure.
Writes nothing on refuse. Does not mint atoms. Stage-2 mint still does not exist.
"""
import argparse, json, sys, pathlib, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate_committed_design import (
    gate_doc, gate_passes, human_shaped, trainable_substance, report, walk_values,
)


class Refuse(SystemExit):
    """Acceptance refused — nothing written."""


def would_mint_atoms(doc):
    did = str(doc.get("design_id") or "")
    if did.startswith("atom_"):
        return True
    if "atom_id" in doc or "meaning" in doc:
        return True
    for val in walk_values(doc):
        if isinstance(val, str) and val.startswith("atom_"):
            return True
    return False


def promote(doc, by, goals_by_id=None):
    """Pure: proposed doc + human --by → validated copy, or Refuse. Writes nothing."""
    if not by:
        raise Refuse("--by is required (validation is a person's act)")
    if not human_shaped(by):
        raise Refuse(f"--by {by!r} is not a human-shaped reviewer (agent never validates)")
    if doc.get("status") != "proposed":
        raise Refuse(f"status is {doc.get('status')!r}, not proposed — nothing to accept")
    if "reviewer" in doc:
        raise Refuse("proposed document already carries reviewer — refuse rather than launder")
    wj = doc.get("warrant_join") or {}
    kind = wj.get("kind")
    has_w = kind == "held_warrant" and bool(wj.get("goal_id"))
    has_e = kind == "direct_escape" and bool(wj.get("escape_kind"))
    if not (has_w ^ has_e):
        raise Refuse("missing warrant-and-escape — not validated for mint")
    if has_w:
        gid = wj["goal_id"]
        if goals_by_id is not None:
            goal = goals_by_id.get(gid)
            if goal is None:
                raise Refuse(f"held goal_ {gid} is not in the goal store — not validated for mint")
            if goal.get("status") != "validated":
                raise Refuse(f"held goal_ {gid} is status {goal.get('status')!r}, not validated")
            if not trainable_substance(goal):
                raise Refuse("unreachable-LO terminal — empty trainable slice; not validated for mint")
    if would_mint_atoms(doc):
        raise Refuse("document smuggles atom identity — accept does not mint atoms")

    out = json.loads(json.dumps(doc))
    out["status"] = "validated"
    out["reviewer"] = by
    ok, rows = gate_passes(out, goals_by_id)
    if not ok:
        bad = [f"{n}: {d}" for n, p, d in rows if not p]
        raise Refuse("gate failed after promote — nothing written: " + "; ".join(bad)[:240])
    return out


def load_ontology_goals():
    goals_p = HERE.parent / "ontology" / "goals.json"
    if not goals_p.exists():
        return None
    store = json.loads(goals_p.read_text(encoding="utf-8"))
    return store.get("goals") or {}


def dump(doc):
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def selftest():
    results = []
    inv_p = HERE.parent / "reference" / "example_corpus_inventory.json"
    sys.path.insert(0, str(HERE))
    from headwater_case_author import propose
    inv = json.loads(inv_p.read_text(encoding="utf-8"))
    proposed = propose(inv)

    GOALS = {
        "goal_fx_example_outcome": {
            "label": "Operators follow the work instruction without inventing steps.",
            "measure": "Audit count of skipped-step incidents on the procedure.",
            "reachability": {
                "trainable": "Knowing the steps and the verification gate.",
                "not_trainable": ["Staffing on the line."],
                "assessed_by": "role_ops_lead",
            },
            "status": "validated",
        },
        "goal_fx_terminal": {
            "label": "Reduce complaints 20%.",
            "measure": "Monthly complaint volume.",
            "reachability": {
                "trainable": "",
                "not_trainable": ["Process, staffing, incentives."],
                "assessed_by": "role_ops_lead",
            },
            "status": "validated",
        },
    }

    accepted = promote(proposed, "jake", GOALS)
    n0 = len(results)
    gate_doc("accept(fixture)", accepted, results, GOALS)
    results.append(("selftest: promote + gate is green with a human --by",
                    all(ok for _, ok, _ in results[n0:]), ""))
    results.append(("selftest: status is validated and reviewer is the --by handle",
                    accepted["status"] == "validated" and accepted["reviewer"] == "jake",
                    ""))
    results.append(("selftest: accept does not mint atoms",
                    not would_mint_atoms(accepted) and "meaning" not in accepted, ""))

    def caught(label, fn):
        try:
            fn()
            results.append((label, False, "mutation was NOT caught"))
        except Refuse:
            results.append((label, True, ""))

    caught("selftest: missing --by is refused",
           lambda: promote(proposed, "", GOALS))
    caught("selftest: agent-shaped --by is refused",
           lambda: promote(proposed, "headwater.case_author", GOALS))
    missing = json.loads(json.dumps(proposed))
    missing.pop("warrant_join")
    caught("selftest: missing warrant-and-escape is refused",
           lambda: promote(missing, "jake", GOALS))

    terminal = json.loads(json.dumps(proposed))
    terminal["warrant_join"] = {"kind": "held_warrant", "goal_id": "goal_fx_terminal"}
    caught("selftest: unreachable-LO terminal is refused",
           lambda: promote(terminal, "jake", GOALS))

    already = json.loads(json.dumps(accepted))
    caught("selftest: already-validated is not re-litigated",
           lambda: promote(already, "jake", GOALS))

    # write path: tempfile only — never a live client store; no atoms.json
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        p = td / "committed-design.json"
        p.write_text(dump(proposed), encoding="utf-8")
        promoted = promote(json.loads(p.read_text(encoding="utf-8")), "jake", GOALS)
        p.write_text(dump(promoted), encoding="utf-8")
        landed = json.loads(p.read_text(encoding="utf-8"))
        results.append(("selftest: tempfile write is validated by jake, no atoms.json",
                        landed["status"] == "validated" and landed["reviewer"] == "jake"
                        and not (td / "atoms.json").exists(), ""))

    sys.exit(0 if report(results) else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--core")
    ap.add_argument("--file", help="proposed committed-design JSON to promote")
    ap.add_argument("--by", help="reviewer of record — validation is a person's act")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        selftest()

    if not a.file or not a.by:
        raise SystemExit("--file and --by are required (validation is a person's act)")

    path = pathlib.Path(a.file)
    if not path.exists():
        raise SystemExit(f"not found: {path}")
    doc = json.loads(path.read_text(encoding="utf-8"))
    goals = load_ontology_goals()
    # fixture goal_ ids are not in the live ontology — only join when present;
    # if the join is held_warrant and the id is absent, refuse (cannot validate a ghost warrant)
    wj = doc.get("warrant_join") or {}
    if wj.get("kind") == "held_warrant":
        gid = wj.get("goal_id")
        if not goals or gid not in goals:
            raise SystemExit(
                f"held goal_ {gid} is not in ontology/goals.json — not validated for mint "
                "(fixture designs stay proposed; do not accept a ghost warrant)")
    try:
        out = promote(doc, a.by, goals)
    except Refuse as e:
        print(f"REFUSED — {e}")
        sys.exit(1)
    path.write_text(dump(out), encoding="utf-8")
    print(f"  + {out['design_id']}: validated by {a.by} → {path}")
    print("Mint still does not exist. Stage 2 is a later hop.")


if __name__ == "__main__":
    main()
