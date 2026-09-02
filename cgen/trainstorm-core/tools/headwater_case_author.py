#!/usr/bin/env python3
"""
headwater_case_author — Case-Author stage 1, propose-only (Dramaturge pattern).

Reads a corpus inventory / source listing and EMITS a committed-design document
(status "proposed", always). It never mints atoms, never writes validated, never
sets reviewer. A human-run tools/committed_design_accept.py --by is the only
promoter. Stage-2 mint is tools/headwater_case_author_mint.py (does not live here).

Idempotent and deferential: a designer's existing design at --out (whatever its
status) is never re-proposed — a claimed placement is not re-litigated by a
re-run. The document is gated by validate_committed_design.gate_doc before
writing; a failed gate writes nothing.

    python3 tools/headwater_case_author.py --selftest
    python3 tools/headwater_case_author.py \
        --inventory reference/example_corpus_inventory.json \
        --out reference/example_committed_design.json
    python3 tools/headwater_case_author.py --inventory ... --out ... --dry-run

Do not point --out at a live client store (paytrans, ALSAP, artwork) this hop.
The fixture lives under reference/. Direct-mode headwater_ingest*.py scripts are
untouched.
"""
import argparse, json, sys, pathlib, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate_committed_design import (
    gate_doc, gate_passes, report, walk_values, ATOM_PREFIX,
)

# Teachable source-types: these may become canon. Everything else stays in the
# source store (FAQ, decks, SOW, stakeholder comments, talking points, …).
# Under-claim unknown kinds — never smash the whole corpus into in_scope.
# 2026-09-01 named bump: "guide" (GUIDE-AST-* is a teachable object; lying that
# a GUIDE is an SOP is refused). Do not add deck/faq/sow. Version-note in
# architecture/DECISIONS.md — do not silently extend.
IN_SCOPE_KINDS = frozenset({
    "work_instruction", "sop", "procedure", "form", "template", "guide",
})

PROPOSED_BY_DEFAULT = "headwater.case_author"


class Refuse(SystemExit):
    """Proposal refused — nothing written."""


def load_inventory(path):
    p = pathlib.Path(path)
    if not p.exists():
        raise Refuse(f"not found: {p}")
    inv = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(inv, dict):
        raise Refuse("inventory must be an object")
    return inv


def inventory_ref(entry):
    ref = {"id": entry["id"], "registry": entry.get("registry") or "docs"}
    return ref


def classify_selection(entries):
    """Partition inventory entries: in-scope kinds vs left in the source store."""
    in_scope, left = [], []
    for e in entries:
        ref = inventory_ref(e)
        if e.get("kind") in IN_SCOPE_KINDS:
            in_scope.append(ref)
        else:
            left.append(ref)
    return in_scope, left


def selection_honest(entries, selection):
    """False if out-of-scope docs exist but were smashed into in_scope / empty left."""
    out = [e for e in entries if e.get("kind") not in IN_SCOPE_KINDS]
    in_ids = {r["id"] for r in (selection.get("in_scope") or [])}
    left_ids = {r["id"] for r in (selection.get("left_in_source_store") or [])}
    if not (selection.get("in_scope") or []):
        return False
    if out:
        if not (selection.get("left_in_source_store") or []):
            return False
        for e in out:
            if e["id"] not in left_ids or e["id"] in in_ids:
                return False
    return True


def would_mint_atoms(doc):
    """True if this node is smuggling atom identity or meaning (stage 2, not this hop)."""
    did = str(doc.get("design_id") or "")
    if did.startswith("atom_") or ATOM_PREFIX.match(did):
        return True
    if "atom_id" in doc or "meaning" in doc or "content_hash" in doc:
        return True
    for val in walk_values(doc):
        if isinstance(val, str) and val.startswith("atom_"):
            return True
    return False


def audit_proposal(doc, inventory=None):
    """Violations the writer must never emit. Empty list = honest proposal."""
    v = []
    if doc.get("status") != "proposed":
        v.append("set validated")
    if "reviewer" in doc:
        v.append("set reviewer (agent never validates)")
    if would_mint_atoms(doc):
        v.append("mint atoms")
    wj = doc.get("warrant_join")
    if not wj:
        v.append("omit warrant_join")
    else:
        kind = wj.get("kind")
        has_w = kind == "held_warrant" and bool(wj.get("goal_id"))
        has_e = kind == "direct_escape" and bool(wj.get("escape_kind"))
        if not (has_w ^ has_e):
            v.append("omit warrant_join")
    did = str(doc.get("design_id") or "")
    if did.startswith("atom_") or not did.startswith("cd_"):
        v.append("atom_ as design_id")
    if inventory is not None:
        entries = inventory.get("entries") or []
        if not selection_honest(entries, doc.get("selection") or {}):
            v.append("smash corpus into in_scope")
    return v


def propose(inventory, proposed_by=None):
    """Pure: inventory dict → committed-design dict (status proposed). Writes nothing."""
    client = inventory.get("client")
    project = inventory.get("project")
    source_store = inventory.get("source_store")
    entries = inventory.get("entries") or []
    if not client or not project or not source_store:
        raise Refuse("inventory must name client, project, and source_store")
    if not entries:
        raise Refuse("inventory has no entries")

    in_scope, left = classify_selection(entries)
    if not in_scope:
        raise Refuse("nothing in-scope — no work_instruction/sop/procedure/form/template/guide in the listing")

    wj = inventory.get("warrant_join")
    if not wj:
        raise Refuse("inventory omits warrant_join (held_warrant XOR direct_escape is required)")

    framing = inventory.get("framing") or {}
    shape = framing.get("shape")
    if not shape:
        labels = [e.get("label") or e["id"] for e in entries if e.get("kind") in IN_SCOPE_KINDS]
        shape = "Bounded teachable object from: " + "; ".join(labels)
        shape = shape[:500]

    design_id = inventory.get("design_id") or f"cd_{client}_{project}_scope"
    proposed_by = proposed_by or inventory.get("proposed_by") or PROPOSED_BY_DEFAULT

    doc = {
        "_note": inventory.get("design_note") or (
            f"proposed committed-design for {client}/{project} — status proposed, not a mint."
        ),
        "schema_version": "committed-design.v0.1",
        "store": "committed-design",
        "design_id": design_id,
        "version": 1,
        "status": "proposed",
        "client": client,
        "project": project,
        "proposed_by": proposed_by,
        "derived_from": {
            "source_store": source_store,
            "inventory_refs": [inventory_ref(e) for e in entries],
        },
        "selection": {
            "in_scope": in_scope,
            "left_in_source_store": left,
        },
        "framing": {"shape": shape},
        "warrant_join": json.loads(json.dumps(wj)),
    }
    if framing.get("goal_ref"):
        doc["framing"]["goal_ref"] = framing["goal_ref"]
    if framing.get("objective_refs"):
        doc["framing"]["objective_refs"] = list(framing["objective_refs"])

    bad = audit_proposal(doc, inventory)
    if bad:
        raise Refuse("proposal refused: " + "; ".join(bad))
    return doc


def claimed_placement(existing):
    """Dramaturge: any existing design (proposed or validated) is already claimed."""
    if not isinstance(existing, dict):
        return False
    return existing.get("store") == "committed-design" and bool(existing.get("design_id"))


def dump(doc):
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def write_if_clean(doc, out_p, dry_run=False):
    """Gate, then write. Returns ('wrote'|'deferred'|'dry-run'|'refused', detail)."""
    if out_p.exists():
        try:
            existing = json.loads(out_p.read_text(encoding="utf-8"))
        except Exception:
            existing = None
        if claimed_placement(existing):
            return ("deferred",
                    f"{out_p} already holds {existing.get('design_id')} "
                    f"status={existing.get('status')!r} — not re-litigating")

    ok, rows = gate_passes(doc)
    if not ok:
        bad = [f"{n}: {d}" for n, p, d in rows if not p]
        return ("refused", "gate failed — nothing written: " + "; ".join(bad)[:240])

    if dry_run:
        return ("dry-run", f"{len(dump(doc))} bytes would be proposed → {out_p}")
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(dump(doc), encoding="utf-8")
    return ("wrote", str(out_p))


def selftest():
    results = []
    inv_p = HERE.parent / "reference" / "example_corpus_inventory.json"
    inv = json.loads(inv_p.read_text(encoding="utf-8"))

    doc = propose(inv)
    n0 = len(results)
    gate_doc("propose(fixture)", doc, results)
    results.append(("selftest: fixture proposal passes the committed-design gate",
                    all(ok for _, ok, _ in results[n0:]), ""))

    results.append(("selftest: status is proposed, never validated",
                    doc.get("status") == "proposed" and "reviewer" not in doc, ""))
    results.append(("selftest: proposed_by stamped (agent is not reviewer)",
                    doc.get("proposed_by") == "headwater.case_author",
                    f"proposed_by={doc.get('proposed_by')!r}"))
    results.append(("selftest: warrant_join present (held_warrant XOR direct_escape)",
                    (doc.get("warrant_join") or {}).get("kind") in ("held_warrant", "direct_escape"),
                    ""))
    results.append(("selftest: design_id is cd_, not atom_",
                    str(doc.get("design_id", "")).startswith("cd_")
                    and not str(doc.get("design_id", "")).startswith("atom_"),
                    f"design_id={doc.get('design_id')!r}"))
    results.append(("selftest: would not mint atoms",
                    not would_mint_atoms(doc), ""))
    left = doc["selection"]["left_in_source_store"]
    in_scope = doc["selection"]["in_scope"]
    results.append(("selftest: out-of-scope docs left in source store (not smashed)",
                    bool(left) and {r["id"] for r in left} == {
                        "doc_fx_related_faq", "doc_fx_out_of_scope_deck"}
                    and {r["id"] for r in in_scope} == {"doc_fx_work_instruction"},
                    f"in_scope={in_scope!r} left={left!r}"))
    results.append(("selftest: audit_proposal is clean on the real proposal",
                    audit_proposal(doc, inv) == [],
                    str(audit_proposal(doc, inv))))

    # Named bump: kind "guide" is in-scope. A GUIDE is not recast as an SOP.
    # deck/faq/sow stay leftover. A parking-lot "training guide" with a leftover
    # kind stays left — classify by kind, not by the word "guide" in the label.
    ginv = json.loads(json.dumps(inv))
    ginv["entries"] = [
        {"id": "doc_fx_sop", "registry": "docs", "kind": "sop",
         "label": "SOP — durable procedure"},
        {"id": "doc_fx_guide", "registry": "docs", "kind": "guide",
         "label": "GUIDE — classify with this"},
        {"id": "doc_fx_parking_guide", "registry": "docs", "kind": "stakeholder",
         "label": "Parking-lot training guide — would launder FORM location"},
        {"id": "doc_fx_deck", "registry": "docs", "kind": "deck", "label": "Deck"},
        {"id": "doc_fx_faq", "registry": "docs", "kind": "faq", "label": "FAQ"},
        {"id": "doc_fx_sow", "registry": "docs", "kind": "sow", "label": "SOW"},
    ]
    gdoc = propose(ginv)
    g_in = {r["id"] for r in gdoc["selection"]["in_scope"]}
    g_left = {r["id"] for r in gdoc["selection"]["left_in_source_store"]}
    results.append(("selftest: kind guide is in_scope (not recast as sop)",
                    g_in == {"doc_fx_sop", "doc_fx_guide"},
                    f"in_scope={g_in!r}"))
    results.append(("selftest: deck/faq/sow and parking-lot training-guide stay left",
                    g_left == {"doc_fx_parking_guide", "doc_fx_deck",
                               "doc_fx_faq", "doc_fx_sow"},
                    f"left={g_left!r}"))
    results.append(("selftest: deck/faq/sow are not IN_SCOPE_KINDS",
                    not ({"deck", "faq", "sow"} & IN_SCOPE_KINDS),
                    f"IN_SCOPE_KINDS={sorted(IN_SCOPE_KINDS)!r}"))

    # Direct-escape inventory path (recorded_by already a human; writer copies, does not invent)
    esc = json.loads(json.dumps(inv))
    esc["warrant_join"] = {
        "kind": "direct_escape",
        "escape_kind": "sop_course",
        "recorded_by": "jake",
        "rationale": "This pile is one bounded work instruction; the document is the syllabus.",
    }
    esc_doc = propose(esc)
    results.append(("selftest: Direct-escape proposal stays proposed and gated",
                    esc_doc["status"] == "proposed"
                    and esc_doc["warrant_join"]["kind"] == "direct_escape"
                    and gate_passes(esc_doc)[0], ""))

    # Red: mutations the writer must catch
    def red(label, mutate):
        mutated = json.loads(json.dumps(doc))
        mutate(mutated)
        caught = bool(audit_proposal(mutated, inv))
        results.append((label, caught, "" if caught else "mutation was NOT caught"))

    red("selftest: would-set-validated is caught",
        lambda d: d.update(status="validated", reviewer="headwater.case_author"))
    red("selftest: omit-warrant_join is caught",
        lambda d: d.pop("warrant_join"))
    red("selftest: atom_ as design_id is caught",
        lambda d: d.update(design_id="atom_fx_smuggled"))
    red("selftest: mint-atoms (smuggled meaning) is caught",
        lambda d: d.update(meaning={"source_text": "the whole corpus dumped here"}))
    red("selftest: smash-whole-corpus-into-in_scope is caught",
        lambda d: d.update(selection={
            "in_scope": [inventory_ref(e) for e in inv["entries"]],
            "left_in_source_store": [],
        }))

    # Missing warrant on the inventory itself refuses to propose
    try:
        bare = json.loads(json.dumps(inv))
        bare.pop("warrant_join")
        propose(bare)
        refused_missing = False
    except Refuse:
        refused_missing = True
    results.append(("selftest: inventory without warrant_join is refused",
                    refused_missing, ""))

    # Idempotency: a validated design at --out is not overwritten; no atoms.json appears
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        out = td / "committed-design.json"
        st, detail = write_if_clean(doc, out)
        results.append(("selftest: first write lands a proposed design",
                        st == "wrote" and out.exists()
                        and json.loads(out.read_text())["status"] == "proposed",
                        f"{st}: {detail}"))
        results.append(("selftest: write does not mint atoms.json",
                        not (td / "atoms.json").exists(),
                        "atoms.json appeared beside the design"))
        # re-run against the proposed file — claimed, not re-litigated
        st2, _ = write_if_clean(doc, out)
        results.append(("selftest: re-run defers to claimed placement (proposed)",
                        st2 == "deferred", f"action={st2}"))
        validated = json.loads(json.dumps(doc))
        validated["status"] = "validated"
        validated["reviewer"] = "jake"
        out.write_text(dump(validated), encoding="utf-8")
        before = out.read_text(encoding="utf-8")
        st3, _ = write_if_clean(doc, out)
        after = out.read_text(encoding="utf-8")
        results.append(("selftest: existing validated design is not re-litigated",
                        st3 == "deferred" and before == after
                        and json.loads(after)["status"] == "validated",
                        f"action={st3}"))

    # Schema example still matches the fixture proposal's selection (same corpus)
    ex_p = HERE.parent / "schemas" / "committed-design.example.json"
    ex = json.loads(ex_p.read_text(encoding="utf-8"))
    results.append(("selftest: schema example is proposed (not a live client design)",
                    ex.get("status") == "proposed" and ex.get("client") == "fx", ""))
    ok_ex, _ = gate_passes(ex)
    results.append(("selftest: schemas/committed-design.example.json still gates",
                    ok_ex, ""))

    sys.exit(0 if report(results) else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--core")
    ap.add_argument("--inventory", help="corpus inventory / source listing (JSON)")
    ap.add_argument("--out", help="path to write the proposed committed-design")
    ap.add_argument("--proposed-by", default=PROPOSED_BY_DEFAULT,
                    help="provenance stamp (not a ratification). Default: headwater.case_author")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        selftest()

    if not a.inventory:
        raise SystemExit("pass --inventory <corpus listing> (or --selftest)")
    if not a.out and not a.dry_run:
        raise SystemExit("pass --out <path> (or --dry-run / --selftest)")

    inv = load_inventory(a.inventory)
    doc = propose(inv, proposed_by=a.proposed_by)
    out_p = pathlib.Path(a.out) if a.out else pathlib.Path("-")
    if a.dry_run and not a.out:
        print(dump(doc), end="")
        print("(dry run) proposed committed-design — status proposed; not written.")
        return

    st, detail = write_if_clean(doc, out_p, dry_run=a.dry_run)
    if st == "wrote":
        print(f"  + {doc['design_id']}: status proposed · "
              f"in_scope={len(doc['selection']['in_scope'])} "
              f"left_in_source_store={len(doc['selection']['left_in_source_store'])} "
              f"warrant={doc['warrant_join']['kind']}")
        print(f"\nproposed → {detail}. Ratify with "
              "tools/committed_design_accept.py --file … --by <human>. "
              "Stage-2 mint is tools/headwater_case_author_mint.py.")
    elif st == "deferred":
        print(f"  · skipped — {detail}")
    elif st == "dry-run":
        print(f"  + {doc['design_id']}: status proposed · {doc['warrant_join']['kind']}")
        print(f"\n(dry run) {detail}")
    else:
        print(f"REFUSED — {detail}")
        sys.exit(1)


if __name__ == "__main__":
    main()
