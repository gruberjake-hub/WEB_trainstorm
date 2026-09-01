#!/usr/bin/env python3
"""
dossier_accept — the ONLY writer that can set a Strategist dossier status validated.

The acceptance half of the warrant snapshot (committed_design_accept / voice_accept
pattern): a human (or this chat) proposes status "proposed"; a human runs THIS script;
this script is what validation *is*, mechanically. The Strategist has no path to
validated — it cannot pass --by as itself (human-shaped reviewer required) and there
is no strategist.py compiler.

    python3 tools/dossier_accept.py --file reference/example_dossier.json --by jake
    python3 tools/dossier_accept.py --selftest

Every acceptance re-runs validate_dossier.gate_doc at acceptance time.
Refuses: missing --by, agent-shaped --by, already-validated, missing warrant
terminal (or missing Direct-escape record), smuggled atoms/obj_, example fixtures,
PII. Writes nothing on refuse. Does not mint atoms. Does not write
ontology/goals.json — accepting the dossier is not the goals-store hop.

The example file is refused on purpose (not a live engagement). Selftest promotes
a copy in a tempfile.
"""
import argparse, json, sys, pathlib, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate_dossier import (
    gate_doc, gate_passes, human_shaped, is_example_fixture, report, walk_values,
    strategist_py_absent,
)


class Refuse(SystemExit):
    """Acceptance refused — nothing written."""


def would_mint_atoms(doc):
    did = str(doc.get("dossier_id") or "")
    if did.startswith(("atom_", "obj_", "ele_")):
        return True
    if "atom_id" in doc or "meaning" in doc or "objectives" in doc:
        return True
    for val in walk_values(doc):
        if isinstance(val, str) and val.startswith("atom_"):
            return True
    return False


def would_write_goals_store(doc):
    """Accept promotes the dossier only. A nested ontology/goals shape is a smash."""
    if doc.get("store") == "ontology/goals":
        return True
    if isinstance(doc.get("goals"), dict):
        return True
    return False


def promote(doc, by):
    """Pure: proposed doc + human --by → validated copy, or Refuse. Writes nothing."""
    if not by:
        raise Refuse("--by is required (validation is a person's act)")
    if not human_shaped(by):
        raise Refuse(f"--by {by!r} is not a human-shaped reviewer (agent never validates)")
    if doc.get("status") != "proposed":
        raise Refuse(f"status is {doc.get('status')!r}, not proposed — nothing to accept")
    if "reviewer" in doc:
        raise Refuse("proposed document already carries reviewer — refuse rather than launder")
    if is_example_fixture(doc):
        raise Refuse("example fixtures stay proposed — not a live engagement")
    door = doc.get("door")
    if door == "open_project":
        w = doc.get("warrant") or {}
        qs = ("value_evidence", "adoption_legitimacy", "cynicism_audit")
        if any((w.get(q) or {}).get("verdict") not in ("pass", "partial", "fail") for q in qs):
            raise Refuse("missing warrant terminal — not validated")
        if w.get("outcome") not in ("full_pass", "partial_pass", "full_fail"):
            raise Refuse("missing warrant terminal — not validated")
    elif door == "direct_escape":
        de = doc.get("direct_escape") or {}
        if de.get("escape_kind") != "sop_course" or not str(de.get("rationale") or "").strip():
            raise Refuse("missing Direct-escape record — not validated")
        if "recorded_by" in de:
            raise Refuse("proposed Direct escape already carries recorded_by — refuse rather than launder")
    else:
        raise Refuse(f"door {door!r} is not a known terminal")
    if would_mint_atoms(doc):
        raise Refuse("document smuggles atom identity — accept does not mint atoms")
    if would_write_goals_store(doc):
        raise Refuse("accept does not write ontology/goals.json — dossier only")

    out = json.loads(json.dumps(doc))
    out["status"] = "validated"
    out["reviewer"] = by
    if door == "direct_escape":
        out.setdefault("direct_escape", {})
        out["direct_escape"]["recorded_by"] = by
    ok, rows = gate_passes(out)
    if not ok:
        bad = [f"{n}: {d}" for n, p, d in rows if not p]
        raise Refuse("gate failed after promote — nothing written: " + "; ".join(bad)[:240])
    return out


def dump(doc):
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def live_for_accept(example):
    """Strip the EXAMPLE marker so a tempfile copy can be promoted in selftest."""
    doc = json.loads(json.dumps(example))
    doc["_note"] = "selftest copy — not the reference fixture, not a live client dossier."
    doc["dossier_id"] = "doss_fx_selftest_accept"
    return doc


def selftest():
    results = []
    example_p = HERE.parent / "reference" / "example_dossier.json"
    example = json.loads(example_p.read_text(encoding="utf-8"))
    proposed = live_for_accept(example)

    results.append(("selftest: no tools/strategist.py compiler",
                    strategist_py_absent(), "strategist.py exists"))

    accepted = promote(proposed, "jake")
    n0 = len(results)
    gate_doc("accept(fixture)", accepted, results)
    results.append(("selftest: promote + gate is green with a human --by",
                    all(ok for _, ok, _ in results[n0:]), ""))
    results.append(("selftest: status is validated and reviewer is the --by handle",
                    accepted["status"] == "validated" and accepted["reviewer"] == "jake",
                    ""))
    results.append(("selftest: accept does not mint atoms",
                    not would_mint_atoms(accepted) and "meaning" not in accepted, ""))
    results.append(("selftest: accept does not write a goals store into the document",
                    not would_write_goals_store(accepted), ""))

    def caught(label, fn):
        try:
            fn()
            results.append((label, False, "mutation was NOT caught"))
        except Refuse:
            results.append((label, True, ""))

    caught("selftest: missing --by is refused",
           lambda: promote(proposed, ""))
    caught("selftest: agent-shaped --by is refused",
           lambda: promote(proposed, "strategist"))
    caught("selftest: agent-shaped --by (claude) is refused",
           lambda: promote(proposed, "claude"))
    caught("selftest: example fixture is refused (not a live engagement)",
           lambda: promote(example, "jake"))

    missing = json.loads(json.dumps(proposed))
    missing.pop("warrant")
    caught("selftest: missing warrant terminal is refused",
           lambda: promote(missing, "jake"))

    atoms = json.loads(json.dumps(proposed))
    atoms["meaning"] = {"source_text": "smuggled corpus"}
    caught("selftest: smuggled atoms are refused",
           lambda: promote(atoms, "jake"))

    already = json.loads(json.dumps(accepted))
    caught("selftest: already-validated is not re-litigated",
           lambda: promote(already, "jake"))

    # write path: tempfile only — never the reference fixture; no atoms.json; no goals.json
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        p = td / "dossier.json"
        before = dump(proposed)
        p.write_text(before, encoding="utf-8")
        # refuse path writes nothing
        try:
            promote(json.loads(p.read_text(encoding="utf-8")), "strategist")
            results.append(("selftest: agent --by refuse path unreachable", False, "did not refuse"))
        except Refuse:
            after = p.read_text(encoding="utf-8")
            results.append(("selftest: writes nothing on refuse",
                            after == before, "file changed after refuse"))
        promoted = promote(json.loads(p.read_text(encoding="utf-8")), "jake")
        p.write_text(dump(promoted), encoding="utf-8")
        landed = json.loads(p.read_text(encoding="utf-8"))
        results.append(("selftest: tempfile write is validated by jake, no atoms.json, no goals.json",
                        landed["status"] == "validated" and landed["reviewer"] == "jake"
                        and not (td / "atoms.json").exists()
                        and not (td / "goals.json").exists()
                        and not (td / "ontology" / "goals.json").exists(), ""))
        # reference fixture untouched
        still = json.loads(example_p.read_text(encoding="utf-8"))
        results.append(("selftest: reference example remains proposed",
                        still.get("status") == "proposed" and "reviewer" not in still, ""))

    sys.exit(0 if report(results) else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--core")
    ap.add_argument("--file", help="proposed dossier JSON to promote")
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
    original = path.read_text(encoding="utf-8")
    doc = json.loads(original)
    try:
        out = promote(doc, a.by)
    except Refuse as e:
        # Writes nothing on refuse — reaffirm the file is unchanged.
        now = path.read_text(encoding="utf-8")
        if now != original:
            path.write_text(original, encoding="utf-8")
        print(f"REFUSED — {e}")
        sys.exit(1)
    path.write_text(dump(out), encoding="utf-8")
    print(f"  + {out['dossier_id']}: validated by {a.by} → {path}")
    print("Dossier only. ontology/goals.json was not written. Next hop: copy proposed_goals "
          "into the live goals store if the warrant holds for building.")


if __name__ == "__main__":
    main()
