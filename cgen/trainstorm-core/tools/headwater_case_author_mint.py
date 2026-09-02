#!/usr/bin/env python3
"""
headwater_case_author_mint — Case-Author stage 2, the mint gate.

Wakes on a validated committed-design (`cd_`). Gates first; writes nothing on refuse.
Does not mutate the `cd_`. Does not mint `ele_`. Does not write `bindings.intent`.
The sibling ingest (`headwater_ingest_cci_pd.py`) is the authored decomposition;
this script is the wake condition that is allowed to run it.

    python3 tools/headwater_case_author_mint.py --selftest
    python3 tools/headwater_case_author_mint.py \
        --file ../astellas/projects/cci_public_disclosure/committed-design.json

REFUSE unless: status validated + human-shaped reviewer + held_warrant XOR
direct_escape + (when held) the goal_ in ontology/goals.json is validated with a
non-empty trainable slice. REFUSE leftover smash, atom_ design_id, unvalidated
cd_, agent-shaped reviewer. First live mint is cd_ast_cci_pd (three in-scope QDs
only). Remainder inventory is not minted.
"""
import argparse, json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate_committed_design import (
    human_shaped, trainable_substance, report, walk_values, ATOM_PREFIX,
)

CGEN = HERE.parent.parent  # cgen/
ONTOLOGY_GOALS = HERE.parent / "ontology" / "goals.json"

# Remainder-bin ids from the live CCI PD inventory. Minting any of these is leftover smash.
LEFTOVER_IDS = frozenset({
    "doc_cci_pd_tracking_tool",
    "doc_cci_pd_helix_kachi_trigger",
    "doc_cci_pd_ws3_ri",
    "doc_cci_pd_connections_note",
    "doc_cci_pd_sh_training_guide",
})
# Locked in_scope QDs for cd_ast_cci_pd. Remainder stays in the source store.
IN_SCOPE_QDS = frozenset({
    "doc_sop_ast_29658",
    "doc_guide_ast_6011",
    "doc_form_ast_35734",
})
LIVE_DESIGN_ID = "cd_ast_cci_pd"


class Refuse(SystemExit):
    """Mint refused — nothing written; the cd_ is untouched."""


def load_json(path):
    p = pathlib.Path(path)
    if not p.exists():
        raise Refuse(f"not found: {p}")
    doc = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise Refuse("committed-design must be an object")
    return doc


def load_ontology_goals():
    if not ONTOLOGY_GOALS.exists():
        return {}
    store = json.loads(ONTOLOGY_GOALS.read_text(encoding="utf-8"))
    return store.get("goals") or {}


def in_scope_ids(doc):
    return {r["id"] for r in ((doc.get("selection") or {}).get("in_scope") or []) if "id" in r}


def leftover_ids_in_scope(doc):
    return in_scope_ids(doc) & LEFTOVER_IDS


def would_mint_ele_or_intent(doc):
    """True if the cd_ is smuggling occurrence identity (stage 2 still does not mint ele_)."""
    did = str(doc.get("design_id") or "")
    if did.startswith("ele_") or "element_id" in doc or "ele_id" in doc:
        return True
    for val in walk_values(doc):
        if isinstance(val, str) and val.startswith("ele_"):
            return True
    return False


def audit_mint(doc, goals_by_id=None):
    """Violations that refuse the mint. Empty list = wake is legal. Writes nothing."""
    v = []
    did = str(doc.get("design_id") or "")
    if did.startswith("atom_") or ATOM_PREFIX.match(did) or not did.startswith("cd_"):
        v.append("atom_ design_id")
    if would_mint_ele_or_intent(doc):
        v.append("ele_")
    if doc.get("status") != "validated":
        v.append("unvalidated")
    if not human_shaped(doc.get("reviewer")):
        v.append("agent-shaped reviewer")

    wj = doc.get("warrant_join") or {}
    kind = wj.get("kind")
    has_w = kind == "held_warrant" and bool(wj.get("goal_id"))
    has_e = kind == "direct_escape" and bool(wj.get("escape_kind"))
    if not (has_w ^ has_e):
        v.append("warrant_join")
    if has_w:
        gid = wj["goal_id"]
        goal = (goals_by_id or {}).get(gid) if goals_by_id is not None else None
        if goals_by_id is not None and goal is None:
            v.append("held goal_ missing")
        if goal is not None:
            if goal.get("status") != "validated":
                v.append("held goal_ not validated")
            if not trainable_substance(goal):
                v.append("unreachable-LO")
    if has_e and not human_shaped(wj.get("recorded_by")):
        v.append("agent-shaped reviewer")

    in_ids = in_scope_ids(doc)
    if leftover_ids_in_scope(doc):
        v.append("leftover")
    if did == LIVE_DESIGN_ID:
        if in_ids != IN_SCOPE_QDS:
            # extra remainder in in_scope, or a QD dropped so leftover could be smuggled
            v.append("leftover")
    elif did.startswith("cd_") and did != LIVE_DESIGN_ID:
        # this hop's sibling ingest is the CCI PD decomposition only
        v.append("not cd_ast_cci_pd")
    return v


def project_store(doc):
    client, project = doc.get("client"), doc.get("project")
    if not client or not project:
        raise Refuse("cd_ must name client and project")
    store = CGEN / client / "projects" / project
    if not store.is_dir():
        raise Refuse(f"project atom store not found: {store}")
    return store


def run_ingest(store):
    from headwater_ingest_cci_pd import ingest
    ingest(store)


def mint(doc, goals_by_id=None, dry_run=False):
    """Pure gate then sibling ingest. Never mutates doc. Returns ('minted'|'dry-run', store)."""
    bad = audit_mint(doc, goals_by_id)
    if bad:
        raise Refuse("mint refused: " + "; ".join(bad))
    store = project_store(doc)
    cd_p = store / "committed-design.json"
    before = cd_p.read_text(encoding="utf-8") if cd_p.exists() else None
    if dry_run:
        return ("dry-run", store)
    run_ingest(store)
    after = cd_p.read_text(encoding="utf-8") if cd_p.exists() else None
    if before is not None and after != before:
        raise Refuse("ingest mutated the cd_ — mint does not mutate committed-design.json")
    return ("minted", store)


def selftest():
    results = []
    live_p = CGEN / "astellas" / "projects" / "cci_public_disclosure" / "committed-design.json"
    live = json.loads(live_p.read_text(encoding="utf-8"))
    goals = load_ontology_goals()

    clean = audit_mint(live, goals)
    results.append(("selftest: live cd_ast_cci_pd is mint-ready (validated + jake + held_warrant)",
                    clean == [], str(clean)))
    results.append(("selftest: in_scope is the three QDs only",
                    in_scope_ids(live) == IN_SCOPE_QDS,
                    f"in_scope={sorted(in_scope_ids(live))!r}"))
    results.append(("selftest: leftover inventory is not in in_scope",
                    not leftover_ids_in_scope(live),
                    f"leftover-in-scope={sorted(leftover_ids_in_scope(live))!r}"))

    before_cd = live_p.read_text(encoding="utf-8")
    atoms_p = live_p.parent / "atoms.json"
    before_atoms = atoms_p.read_text(encoding="utf-8") if atoms_p.exists() else None

    def caught(label, mutate, expect_token):
        mutated = json.loads(json.dumps(live))
        mutate(mutated)
        bad = audit_mint(mutated, goals)
        ok = expect_token in bad
        results.append((label, ok,
                        "" if ok else f"expected {expect_token!r} in {bad!r}"))

    caught("selftest: refuse proposed",
           lambda d: (d.update(status="proposed"), d.pop("reviewer", None)),
           "unvalidated")
    caught("selftest: leftover smash is refused",
           lambda d: d.update(selection={
               "in_scope": list(d["selection"]["in_scope"]) + list(d["selection"]["left_in_source_store"]),
               "left_in_source_store": [],
           }),
           "leftover")
    terminal_goals = json.loads(json.dumps(goals))
    terminal_goals["goal_ast_cci_library_used"] = {
        "label": terminal_goals["goal_ast_cci_library_used"]["label"],
        "status": "validated",
        "reachability": {
            "trainable": "",
            "not_trainable": ["everything"],
            "assessed_by": "role_pd_lead",
        },
    }

    mutated = json.loads(json.dumps(live))
    bad_lo = audit_mint(mutated, terminal_goals)
    results.append(("selftest: unreachable-LO is refused",
                    "unreachable-LO" in bad_lo,
                    "" if "unreachable-LO" in bad_lo else f"got {bad_lo!r}"))

    caught("selftest: atom_ design_id is refused",
           lambda d: d.update(design_id="atom_ast_smuggled"),
           "atom_ design_id")
    caught("selftest: agent-shaped reviewer is refused",
           lambda d: d.update(reviewer="headwater.case_author"),
           "agent-shaped reviewer")

    after_cd = live_p.read_text(encoding="utf-8")
    results.append(("selftest: refuse paths do not mutate the live cd_",
                    before_cd == after_cd, "committed-design.json changed during selftest"))
    after_atoms = atoms_p.read_text(encoding="utf-8") if atoms_p.exists() else None
    results.append(("selftest: refuse paths do not write atoms.json",
                    before_atoms == after_atoms,
                    "atoms.json changed during refuse selftest"))

    sys.exit(0 if report(results) else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--core")
    ap.add_argument("--file", help="validated committed-design JSON to mint from")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        selftest()

    if not a.file:
        raise SystemExit("pass --file <validated committed-design.json> (or --selftest)")

    path = pathlib.Path(a.file)
    before = path.read_text(encoding="utf-8")
    doc = json.loads(before)
    goals = load_ontology_goals()
    try:
        st, store = mint(doc, goals, dry_run=a.dry_run)
    except Refuse as e:
        print(f"REFUSED — {e}")
        sys.exit(1)

    after = path.read_text(encoding="utf-8")
    if after != before:
        print("REFUSED — mint mutated the cd_; restoring is the caller's problem — this is a bug")
        sys.exit(1)

    n_scope = len(doc["selection"]["in_scope"])
    n_left = len(doc["selection"]["left_in_source_store"])
    if st == "minted":
        print(f"  + {doc['design_id']}: minted · in_scope={n_scope} "
              f"left_in_source_store={n_left} warrant={doc['warrant_join']['kind']} "
              f"reviewer={doc.get('reviewer')}")
        print(f"\nminted → {store / 'atoms.json'}. cd_ untouched. Remainder not minted.")
    else:
        print(f"  + {doc['design_id']}: dry-run · in_scope={n_scope} "
              f"left_in_source_store={n_left}")
        print(f"\n(dry run) would ingest three QDs → {store / 'atoms.json'}; cd_ untouched")


if __name__ == "__main__":
    main()
