#!/usr/bin/env python3
"""
Cartographer v1 — bind occurrence intent on an existing Realizer store.

Cartographer owns occurrence intent: `move`, `teaches`, `intended_response`,
`rhetorical`. v1 is a documented heuristic compiler
(`agents/cartographer/heuristic_v1.md`), not an ID genius. It reads atoms for
meaning, writes only `element.intent` (+ `ext.cartographer` provenance) on
already-minted `ele_` records, and re-projects `realized_lesson.html`.

Never: mint `ele_` / `atom_` ids; copy meaning onto the element; write
`atoms.json`; put `teaches` back on atoms; invent `practice`/`assess` this SOP
does not contain; write Couturier style keys. Extra 1:many
occurrences keep their Realizer-stamped `move`; Cartographer still binds
`teaches` / `rhetorical` / `intended_response`. After writing `move` it
asks Realizer to refresh `text_primitive` (compiler form depends on move).
A re-run does not wipe Couturier style.

Usage (from `cgen/trainstorm-core`):

    python3 tools/cartographer.py
    python3 tools/cartographer.py --project ../astellas/projects/ast_alsap
    python3 tools/cartographer.py --selftest

Requires Realizer output at `<project>/occurrences/elements.json`. Re-runnable
on a mixed 1:1 + extra store; extra `ele_` ids are not dropped.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import sys
from collections import Counter

import harness_paths
from jsonschema import Draft202012Validator

import realize

POLICY = "v1_heuristic_compiler"
CARTOGRAPHER = "tools/cartographer.py"
CLOSED_INTENT_KEYS = ("rhetorical", "move", "teaches", "intended_response")

# ALSAP draft ontology — must exist in ontology/objectives.json. Never mint.
OBJ_EXPLAIN = "obj_explain_alsap_purpose"
OBJ_SCOPE = "obj_identify_alsap_scope"
OBJ_PLAN = "obj_execute_alsap_plan"
OBJ_DEVELOP = "obj_execute_alsap_develop_maintain"
OBJ_OUTPUTS = "obj_produce_alsap_analysis_outputs"

PURPOSE_TEXT_RE = re.compile(
    r"^(the )?purpose of (this )?(sop|procedure|document)\b", re.I
)
DEFINITIONS_TEXT_RE = re.compile(r"\b(definitions?|glossary)\b", re.I)
ROLES_TEXT_RE = re.compile(r"^roles and responsibilities\b", re.I)
TRANSFER_TEXT_RE = re.compile(
    r"(notify .+ of the approval)"
    r"|(provide tlf outputs to the smt)"
    r"|(review .+ per sop-)",
    re.I,
)


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def clean_meaning(text: str) -> str:
    return realize.clean_meaning(text)


def inject_default_project():
    realize.inject_default_project()


def atom_kind(atom) -> str:
    return (atom.get("meaning") or {}).get("kind") or ""


def belongs_to(atom):
    return (atom.get("bindings") or {}).get("object", {}).get("belongs_to")


def classify_move(atom) -> tuple[str, str, list[str]]:
    """Heuristic v1 `move`. Returns (move, confidence, flags). First match wins."""
    aid = atom["atom_id"]
    kind = atom_kind(atom)
    text = clean_meaning(atom.get("meaning", {}).get("source_text") or "")

    if kind == "document":
        # Heuristic v2 (expository): a multi-document corpus carries SEVERAL roots; which one
        # opens the lesson is course design, not structure. Default present; the project's
        # intent_map elevates exactly one to hook. SOP roots keep kind procedure → rule below.
        return "present", "low", ["document_root_expository"]
    if not belongs_to(atom):
        return "hook", "high", ["root_title"]
    if aid.endswith("_purpose") or PURPOSE_TEXT_RE.search(text):
        return "objective", "high", ["purpose_frame"]
    if "_definitions" in aid or (DEFINITIONS_TEXT_RE.search(text) and kind == "procedure"):
        return "activate", "low", ["definitions_as_prior_knowledge"]
    if aid.endswith("_roles") or ROLES_TEXT_RE.search(text):
        return "activate", "low", ["roles_as_prior_knowledge"]
    if "govdocs" in aid:
        return "exemplify", "low", ["governance_docs_as_examples"]
    if kind == "procedure_step" and TRANSFER_TEXT_RE.search(text):
        return "transfer", "low", ["handoff_as_transfer"]
    if kind in ("procedure_step", "list", "list_item", "statement"):
        return "present", "high", ["kind_present"]
    if kind == "form_field":
        return "present", "high", ["form_field_as_present"]
    return "present", "high", ["section_head_as_present"]


def classify_rhetorical(atom) -> str:
    """Heuristic v1 `rhetorical`. Structure/kind, not element.type → enum."""
    aid = atom["atom_id"]
    kind = atom_kind(atom)
    text = clean_meaning(atom.get("meaning", {}).get("source_text") or "")

    if kind == "document" or not belongs_to(atom):
        return "orient"
    if kind == "statement":
        return "assert"
    if aid.endswith("_purpose") or PURPOSE_TEXT_RE.search(text):
        return "assert"
    if aid.endswith("_scope") and kind == "procedure":
        return "contextualize"
    if "_definitions" in aid:
        return "support"
    if kind == "list":
        return "structure"
    if kind == "list_item":
        return "specify"
    if kind == "procedure_step":
        return "assert"
    if kind == "form_field":
        return "specify"
    if aid.endswith("_general"):
        return "explain"
    return "organize"


def is_container_label(atom) -> bool:
    """Section heads whose coverage is a walk over children, not a stored union."""
    aid = atom["atom_id"]
    return bool(re.search(r"_procedures$", aid) or re.search(r"_proc_[a-z]$", aid))


def bind_teaches(atom, project=None) -> list[str]:
    """Sparse objective binding. Empty is honest; never mint obj_ ids.

    ALSAP draft objectives stay on ALSAP (and selftest fixtures that omit
    a project name). A second SOP does not inherit obj_explain_alsap_*.
    """
    if project and project != "ast_alsap":
        return []
    aid = atom["atom_id"]
    if "_definitions" in aid or is_container_label(atom) or atom_kind(atom) == "form_field":
        return []
    if not belongs_to(atom) or aid.endswith("_purpose") or aid.endswith("_general") or "govdocs" in aid:
        return [OBJ_EXPLAIN]
    if "_scope" in aid or aid.endswith("_roles"):
        return [OBJ_SCOPE]
    if "_proc_a" in aid:
        return [OBJ_PLAN]
    if "_proc_b" in aid:
        return [OBJ_DEVELOP]
    if "_proc_c" in aid:
        return [OBJ_OUTPUTS]
    return []


def bind_intended_response(atom, move: str, project=None) -> str | None:
    if project and project != "ast_alsap":
        if move == "hook":
            return "attend to the document title this procedure governs"
        if move == "objective":
            return "state the process this SOP defines"
        if move == "reinforce":
            return "attempt a check that retrieves this atom's meaning, not as new information"
        if move == "activate":
            return "notice why this exists as a prior frame, not as a new fact"
        return None
    if move == "hook":
        return "attend to ALSAP as the asset-level safety plan this procedure governs"
    if move == "objective":
        return "state the process this SOP defines (plan, develop, execute, maintain, archive)"
    if move == "transfer":
        return "carry the named handoff into the job (notify, deliver outputs, or follow the cited SOP)"
    if move == "reinforce":
        return "attempt a check that retrieves this atom's meaning, not as new information"
    if move == "activate":
        return "notice why this exists as a prior frame, not as a new fact"
    if move == "exemplify":
        return "notice a filled ALSAP instance as evidence the job happened, not as a new SOP rule"
    return None


def bind_intent(atom, closed_moves, closed_rhetorical, objective_ids, project=None) -> tuple[dict, dict]:
    move, confidence, flags = classify_move(atom)
    if move not in closed_moves:
        raise SystemExit(f"heuristic emitted ungoverned move {move!r} for {atom['atom_id']}")
    rhetorical = classify_rhetorical(atom)
    if rhetorical not in closed_rhetorical:
        raise SystemExit(
            f"heuristic emitted ungoverned rhetorical {rhetorical!r} for {atom['atom_id']}"
        )
    teaches = bind_teaches(atom, project=project)
    unknown = [t for t in teaches if t not in objective_ids]
    if unknown:
        raise SystemExit(f"{atom['atom_id']}: teaches {unknown} not in ontology/objectives.json")
    if not teaches and not is_container_label(atom) and "_definitions" not in atom["atom_id"] \
            and atom_kind(atom) != "form_field":
        confidence = "low"
        flags = list(flags) + ["teaches_unbound"]
    intent = {"rhetorical": rhetorical, "move": move}
    if teaches:
        intent["teaches"] = teaches
    intended = bind_intended_response(atom, move, project=project)
    if intended:
        intent["intended_response"] = intended
    stamp = {
        "policy": POLICY,
        "tool": CARTOGRAPHER,
        "confidence": confidence,
        "flags": flags,
    }
    return intent, stamp


INTENT_MAP_FILENAME = "intent_map.json"
INTENT_MAP_POLICY = "v1_intent_map"


def load_intent_map(project_dir, objective_ids, closed_moves):
    """Project-data intent bindings: occurrences/intent_map.json, keyed by atom_id.

    Heuristic v2. The v1 teaches walk is ALSAP-hardcoded Python — the same shape the
    2026-08-27 catalog decisions retired for scenes and lessons. The map is the catalog
    move applied to Cartographer's inputs: the DESIGNER's objective bindings (and at most
    one hook election) live as project data; Cartographer stays the single writer of the
    intent facet and validates every value against the governed stores. Absent file = v1
    behavior, so ALSAP/artwork are byte-identical without it.
    Entry shape: {"teaches": [obj_ids], "move": optional governed move}.
    """
    p = pathlib.Path(project_dir) / "occurrences" / INTENT_MAP_FILENAME
    if not p.exists():
        return {}
    m = load(p)
    if m.get("policy") != INTENT_MAP_POLICY:
        raise SystemExit(f"{p}: policy {m.get('policy')!r} is not {INTENT_MAP_POLICY!r}")
    entries = m.get("map") or {}
    hooks = 0
    for aid, e in entries.items():
        for t in e.get("teaches") or []:
            if t not in objective_ids:
                raise SystemExit(f"intent_map {aid}: teaches {t!r} not in ontology/objectives.json")
        mv = e.get("move")
        if mv is not None:
            if mv not in closed_moves:
                raise SystemExit(f"intent_map {aid}: move {mv!r} not in the closed pedagogical vocab")
            if mv == "hook":
                hooks += 1
        extra = set(e) - {"teaches", "move", "why"}
        if extra:
            raise SystemExit(f"intent_map {aid}: unknown keys {sorted(extra)} (closed entry shape)")
    if hooks > 1:
        raise SystemExit("intent_map elects more than one hook — a lesson opens once")
    return entries


def apply_intent_map(el, atom, intent, stamp, entry, closed_moves, project=None):
    """Overlay one map entry on the heuristic result. Extras keep their Realizer move."""
    intent = dict(intent)
    stamp = dict(stamp)
    flags = [f for f in (stamp.get("flags") or [])]
    if entry.get("teaches") is not None:
        if entry["teaches"]:
            intent["teaches"] = list(entry["teaches"])
            if "teaches_unbound" in flags:
                # The heuristic demoted confidence ONLY because teaches was unbindable
                # (bind_teaches is empty off-ALSAP); the map has now bound it, so restore
                # the classifier's own confidence for the move.
                flags = [f for f in flags if f != "teaches_unbound"]
                if stamp.get("confidence") == "low":
                    stamp["confidence"] = classify_move(atom)[1]
        else:
            intent.pop("teaches", None)
    if entry.get("move") and not realize.is_extra_element(el):
        intent["move"] = entry["move"]
        stamp["confidence"] = "map"
        intended = bind_intended_response(atom, entry["move"], project=project)
        if intended:
            intent["intended_response"] = intended
        else:
            intent.pop("intended_response", None)
    if "intent_map" not in flags:
        flags.append("intent_map")
    stamp["flags"] = flags
    return intent, stamp


def bind_intent_for_occurrence(el, atom, closed_moves, closed_rhetorical, objective_ids,
                              project=None) -> tuple[dict, dict]:
    """Bind intent on one occurrence. Extra occurrences keep Realizer-stamped `move`."""
    intent, stamp = bind_intent(
        atom, closed_moves, closed_rhetorical, objective_ids, project=project,
    )
    if not realize.is_extra_element(el):
        return intent, stamp
    rf = (el.get("ext") or {}).get("realized_from") or {}
    move = (el.get("intent") or {}).get("move") or rf.get("target_move")
    if not move:
        raise SystemExit(
            f"{el.get('element_id')}: extra occurrence has no move to preserve "
            "(Realizer must stamp target_move when minting)"
        )
    if move not in closed_moves:
        raise SystemExit(f"{el.get('element_id')}: preserved extra move {move!r} is not in the closed vocab")
    intent = dict(intent)
    intent["move"] = move
    intended = bind_intended_response(atom, move, project=project)
    if intended:
        intent["intended_response"] = intended
    else:
        intent.pop("intended_response", None)
    stamp = dict(stamp)
    flags = list(stamp.get("flags") or [])
    if "extra_occurrence_move_preserved" not in flags:
        flags.append("extra_occurrence_move_preserved")
    stamp["flags"] = flags
    return intent, stamp


def apply_intent(el, intent, stamp):
    """Write only Cartographer-owned keys. Do not mint ids or copy meaning."""
    if "content" in el:
        raise SystemExit(f"{el.get('element_id')}: refusing to keep authored content on an occurrence")
    el["intent"] = intent
    ext = el.setdefault("ext", {})
    ext["cartographer"] = stamp
    return el


def validate_elements(elements, schema, atoms_by_id, objective_ids, closed_moves, closed_rhetorical):
    v = Draft202012Validator(schema)
    hard = []
    seen = set()
    for el in elements:
        eid = el.get("element_id")
        for err in sorted(v.iter_errors(el), key=lambda e: list(e.path)):
            hard.append(f"{eid}: {err.message}")
        if eid in seen:
            hard.append(f"duplicate element_id {eid}")
        seen.add(eid)
        if "content" in el:
            hard.append(f"{eid}: authored content is forbidden (meaning lives on the atom)")
        cf = el.get("composed_from")
        if cf not in atoms_by_id:
            hard.append(f"{eid}: composed_from {cf} is not in the atom store")
        intent = el.get("intent") or {}
        extra = set(intent) - set(CLOSED_INTENT_KEYS)
        if extra:
            hard.append(f"{eid}: intent has ungoverned keys {sorted(extra)}")
        move = intent.get("move")
        if move not in closed_moves:
            hard.append(f"{eid}: move {move!r} is not in the closed pedagogical vocab")
        rh = intent.get("rhetorical")
        if rh is not None and rh not in closed_rhetorical:
            hard.append(f"{eid}: rhetorical {rh!r} is not in the closed rhetorical vocab")
        for oid in intent.get("teaches") or []:
            if oid not in objective_ids:
                hard.append(f"{eid}: teaches {oid} is not in ontology/objectives.json")
            if not re.match(r"^obj_[a-z0-9_]+$", oid):
                hard.append(f"{eid}: teaches {oid} fails obj_ pattern")
        if (el.get("ext") or {}).get("cartographer", {}).get("policy") != POLICY:
            hard.append(f"{eid}: missing ext.cartographer.policy={POLICY}")
    if hard:
        print("CARTOGRAPHER VALIDATION FAILURES:", file=sys.stderr)
        for m in hard:
            print("  x", m, file=sys.stderr)
        raise SystemExit(1)


def assert_no_id_minting(before_ids, after_ids):
    if before_ids != after_ids:
        added = after_ids - before_ids
        removed = before_ids - after_ids
        raise SystemExit(
            f"Cartographer must not mint or drop ele_ ids. added={sorted(added)} removed={sorted(removed)}"
        )


def selftest(closed_moves, closed_rhetorical, objective_ids):
    """Tiny fixture: structure/kind → move, and the write contract."""
    results = []

    def atom(aid, kind, text, parent=None):
        a = {
            "atom_id": aid,
            "meaning": {"source_locale": "en", "source_text": text, "kind": kind},
            "bindings": {},
            "governance": {"version": 1, "status": "draft"},
        }
        if parent:
            a["bindings"]["object"] = {"belongs_to": parent, "order": 0}
        return a

    cases = [
        (atom("atom_sop_x", "procedure", "SOP-X — Do the thing."), "hook", "high", [OBJ_EXPLAIN]),
        (atom("atom_sop_x_purpose", "procedure", "The purpose of this SOP is to define the process.", "atom_sop_x"),
         "objective", "high", [OBJ_EXPLAIN]),
        (atom("atom_sop_x_definitions", "procedure", "For definitions, refer to the glossary.", "atom_sop_x"),
         "activate", "low", []),
        (atom("atom_sop_x_proc_a_s1", "procedure_step", "Notify QSEG and request an ALSAP Lead.", "atom_sop_x_proc_a"),
         "present", "high", [OBJ_PLAN]),
        (atom("atom_sop_x_proc_b_s8", "procedure_step",
              "Notify the ALSAP Contributing Authors, Reviewers, Approvers, and the SAC Chair of the approval of the ALSAP.",
              "atom_sop_x_proc_b"),
         "transfer", "low", [OBJ_DEVELOP]),
        (atom("atom_sop_x_proc_a", "procedure", "A. Plan Development of ALSAP.", "atom_sop_x_procedures"),
         "present", "high", []),
        (atom("atom_sop_x_general_govdocs_0", "list_item", "Investigator Brochure (IB): summarizes known risks.",
              "atom_sop_x_general_govdocs"),
         "exemplify", "low", [OBJ_EXPLAIN]),
        (atom("atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile", "form_field",
              "SMT assessment of the overall Benefit-Risk profile of the asset.",
              "atom_form_ast34037_sec_purpose_sec_safety_profile"),
         "present", "high", []),
    ]
    for a, want_move, want_conf, want_teach in cases:
        intent, stamp = bind_intent(a, closed_moves, closed_rhetorical, objective_ids)
        ok = (intent["move"] == want_move
              and stamp["confidence"] == want_conf
              and intent.get("teaches", []) == want_teach)
        results.append((f"{a['atom_id']} → {want_move}/{want_conf}/{want_teach}", ok,
                        f"got {intent.get('move')} / {stamp['confidence']} / {intent.get('teaches', [])}"))
    # ---- heuristic v2: expository kinds + intent_map (2026-08-31) ----
    doc_atom = atom("atom_x_doc", "document", "Guide to the Thing — a document title line.")
    doc_intent, doc_stamp = bind_intent(doc_atom, closed_moves, closed_rhetorical, objective_ids,
                                        project="not_alsap")
    results.append(("document root defaults present/low (multi-root corpus; hook is a map election)",
                    doc_intent["move"] == "present" and doc_stamp["confidence"] == "low"
                    and doc_intent.get("rhetorical") == "orient",
                    f"{doc_intent.get('move')}/{doc_stamp['confidence']}/{doc_intent.get('rhetorical')}"))
    st_atom = atom("atom_x_claim", "statement", "The framework balances market data with internal equity across grades.", "atom_x_doc")
    st_intent, st_stamp = bind_intent(st_atom, closed_moves, closed_rhetorical, objective_ids,
                                      project="not_alsap")
    results.append(("statement → present/high, rhetorical assert",
                    st_intent["move"] == "present" and st_intent.get("rhetorical") == "assert",
                    f"{st_intent.get('move')}/{st_intent.get('rhetorical')}"))
    any_obj = sorted(objective_ids)[0]
    prim_el = {"element_id": "ele_x_doc", "composed_from": "atom_x_doc"}
    m_intent, m_stamp = apply_intent_map(prim_el, doc_atom, doc_intent, doc_stamp,
                                         {"teaches": [any_obj], "move": "hook"}, closed_moves,
                                         project="not_alsap")
    results.append(("intent_map elects hook + binds teaches on a primary",
                    m_intent["move"] == "hook" and m_intent.get("teaches") == [any_obj]
                    and m_stamp["confidence"] == "map" and "intent_map" in m_stamp["flags"],
                    f"{m_intent.get('move')}/{m_intent.get('teaches')}/{m_stamp}"))
    extra_el = {"element_id": "ele_x_claim__reinforce", "composed_from": "atom_x_claim",
                "intent": {"move": "reinforce"},
                "ext": {"realized_from": {"target_move": "reinforce"}}}
    e_base, e_stamp0 = bind_intent_for_occurrence(extra_el, st_atom, closed_moves,
                                                  closed_rhetorical, objective_ids,
                                                  project="not_alsap")
    e_intent, e_stamp = apply_intent_map(extra_el, st_atom, e_base, e_stamp0,
                                         {"teaches": [any_obj], "move": "present"}, closed_moves,
                                         project="not_alsap")
    results.append(("intent_map move does NOT override a preserved extra move; teaches still binds",
                    e_intent["move"] == "reinforce" and e_intent.get("teaches") == [any_obj],
                    f"{e_intent.get('move')}/{e_intent.get('teaches')}"))
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        occ = pathlib.Path(td) / "occurrences"
        occ.mkdir()
        (occ / INTENT_MAP_FILENAME).write_text(json.dumps({
            "policy": INTENT_MAP_POLICY,
            "map": {"atom_x_doc": {"teaches": ["obj_never_governed_zzz"]}},
        }))
        try:
            load_intent_map(pathlib.Path(td), objective_ids, closed_moves)
            results.append(("load_intent_map rejects an ungoverned obj id", False, "did not raise"))
        except SystemExit:
            results.append(("load_intent_map rejects an ungoverned obj id", True, "raised"))
        (occ / INTENT_MAP_FILENAME).write_text(json.dumps({
            "policy": INTENT_MAP_POLICY,
            "map": {"a": {"move": "hook"}, "b": {"move": "hook"}},
        }))
        try:
            load_intent_map(pathlib.Path(td), objective_ids, closed_moves)
            results.append(("load_intent_map rejects two hook elections", False, "did not raise"))
        except SystemExit:
            results.append(("load_intent_map rejects two hook elections", True, "raised"))

    form_atom = cases[-1][0]
    form_intent, form_stamp = bind_intent(form_atom, closed_moves, closed_rhetorical, objective_ids)
    results.append(("form_field rhetorical is specify (a named slot)",
                    form_intent.get("rhetorical") == "specify", form_intent.get("rhetorical")))
    results.append(("form_field empty teaches is honest not low-conf",
                    form_stamp["confidence"] == "high"
                    and "teaches_unbound" not in (form_stamp.get("flags") or []),
                    form_stamp))

    # Write contract: existing ele_ kept; no content copied; atom store untouched.
    el = {
        "element_id": "ele_sop_x",
        "composed_from": "atom_sop_x",
        "type": "Course",
        "intent": {"rhetorical": "orient", "move": "present"},
        "governance": {"version": 1, "status": "draft", "owner": "realizer"},
        "ext": {"realized_from": {"atom_id": "atom_sop_x", "realizer": "tools/realize.py"}},
    }
    before_id = el["element_id"]
    intent, stamp = bind_intent(cases[0][0], closed_moves, closed_rhetorical, objective_ids)
    apply_intent(el, intent, stamp)
    results.append(("does not mint a new element_id", el["element_id"] == before_id, el["element_id"]))
    results.append(("does not copy meaning onto the element", "content" not in el, ""))
    results.append(("does not steal realized_from", "realized_from" in el["ext"], ""))
    results.append(("hook is not present", el["intent"]["move"] == "hook", el["intent"]["move"]))

    # 1:many extra: same atom, Realizer-stamped move survives Cartographer.
    extra = {
        "element_id": "ele_sop_x__present",
        "composed_from": "atom_sop_x",
        "type": "Course",
        "intent": {"rhetorical": "orient", "move": "present"},
        "governance": {"version": 1, "status": "draft", "owner": "realizer"},
        "ext": {
            "realized_from": {
                "atom_id": "atom_sop_x",
                "realizer": "tools/realize.py",
                "policy": "v1_extra_occurrence",
                "role": "extra",
                "target_move": "present",
            }
        },
    }
    extra_intent, extra_stamp = bind_intent_for_occurrence(
        extra, cases[0][0], closed_moves, closed_rhetorical, objective_ids
    )
    apply_intent(extra, extra_intent, extra_stamp)
    results.append(("extra keeps Realizer-stamped present (not atom heuristic hook)",
                    extra["intent"]["move"] == "present", extra["intent"]["move"]))
    results.append(("extra still binds teaches from the atom",
                    extra["intent"].get("teaches") == [OBJ_EXPLAIN], extra["intent"].get("teaches")))
    results.append(("extra does not mint a new element_id",
                    extra["element_id"] == "ele_sop_x__present", extra["element_id"]))
    results.append(("extra flagged move_preserved",
                    "extra_occurrence_move_preserved" in extra["ext"]["cartographer"]["flags"],
                    extra["ext"]["cartographer"]["flags"]))
    results.append(("primary and extra share composed_from",
                    el["composed_from"] == extra["composed_from"] == "atom_sop_x", ""))
    results.append(("primary and extra have distinct moves",
                    el["intent"]["move"] != extra["intent"]["move"],
                    f"{el['intent']['move']} vs {extra['intent']['move']}"))
    results.append(("does not copy meaning onto the extra", "content" not in extra, ""))

    extra_r = {
        "element_id": "ele_sop_x_general__reinforce",
        "composed_from": "atom_sop_x_general",
        "type": "Section",
        "intent": {"rhetorical": "explain", "move": "reinforce"},
        "governance": {"version": 1, "status": "draft", "owner": "realizer"},
        "ext": {
            "realized_from": {
                "atom_id": "atom_sop_x_general",
                "realizer": "tools/realize.py",
                "policy": "v1_extra_occurrence",
                "role": "extra",
                "target_move": "reinforce",
            }
        },
    }
    extra_r_atom = atom("atom_sop_x_general", "procedure", "The ALSAP is the framework.", "atom_sop_x")
    extra_r_intent, extra_r_stamp = bind_intent_for_occurrence(
        extra_r, extra_r_atom, closed_moves, closed_rhetorical, objective_ids
    )
    apply_intent(extra_r, extra_r_intent, extra_r_stamp)
    results.append(("extra reinforce keeps Realizer-stamped move",
                    extra_r["intent"]["move"] == "reinforce", extra_r["intent"]["move"]))
    results.append(("extra reinforce intended_response names a check",
                    "check" in (extra_r["intent"].get("intended_response") or ""),
                    extra_r["intent"].get("intended_response")))
    results.append(("extra reinforce does not invent retrieve",
                    extra_r["intent"]["move"] != "retrieve", extra_r["intent"]["move"]))

    # Couturier style on the extra must survive a Cartographer re-bind.
    extra["expression"] = {
        "style_ref": "brand.instructional",
        "text_primitive": "tp_body",
        "content_role": "body",
        "layout_hint": "card",
    }
    extra["ext"]["couturier"] = {"policy": "v1_move_to_look", "tool": "tools/couturier.py"}
    extra_intent2, extra_stamp2 = bind_intent_for_occurrence(
        extra, cases[0][0], closed_moves, closed_rhetorical, objective_ids
    )
    apply_intent(extra, extra_intent2, extra_stamp2)
    results.append(("re-bind does not wipe Couturier expression",
                    extra.get("expression", {}).get("style_ref") == "brand.instructional",
                    extra.get("expression")))
    results.append(("re-bind does not wipe ext.couturier",
                    "couturier" in extra.get("ext", {}), extra.get("ext", {}).keys()))

    print(f"{'CHECK':<72} RESULT")
    print("-" * 86)
    ok = True
    for name, passed, detail in results:
        ok = ok and passed
        print(f"{name:<72} {'PASS' if passed else 'FAIL'}   {detail if not passed else ''}")
    print("-" * 86)
    print("SELFTEST ALL PASS" if ok else "SELFTEST FAILED")
    if not ok:
        raise SystemExit(1)


def main():
    inject_default_project()
    default_shown = os.environ.get("TRAINSTORM_PROJECT") or (
        str(realize.repo_default_project()) if realize.repo_default_project() else "(pass --project)"
    )
    ap = argparse.ArgumentParser(
        description="Cartographer v1 — bind occurrence intent (heuristic compiler) and re-project the lesson HTML.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="From cgen/trainstorm-core:\n"
               "  python3 tools/cartographer.py\n"
               "  python3 tools/cartographer.py --project ../astellas/projects/ast_alsap\n"
               "  python3 tools/cartographer.py --selftest\n",
    )
    ap.add_argument("--project", default=None,
                    help=f"Atom + occurrence store directory (default: {default_shown})")
    ap.add_argument("--core", default=None, help="trainstorm-core (schemas + vocab + ontology)")
    ap.add_argument("--registry", default=None)
    ap.add_argument("--out", help="HTML output path (default: derived from --lesson; default lesson is <project>/realized_lesson.html)")
    ap.add_argument("--lesson", default=None,
                    help="Lesson id from the project catalog (occurrences/lessons.json), stamped onto manifest.lessons. Default pass emits all catalog lessons; --lesson regenerates that file.")
    ap.add_argument("--store", help="Occurrence store directory (default: <project>/occurrences)")
    ap.add_argument("--selftest", action="store_true", help="Run the heuristic fixture and exit")
    ap.add_argument("--dry-run", action="store_true", help="Bind and validate; do not write the store or HTML")
    args = ap.parse_args()

    P = harness_paths.resolve() if not args.selftest else harness_paths.resolve_core(args.core)
    if not args.selftest:
        print(harness_paths.announce(P))

    schemas = P["schemas_dir"]
    element_schema = load(schemas / "element.schema.json")
    closed_moves = list(element_schema["properties"]["intent"]["properties"]["move"]["enum"])
    closed_rhetorical = list(element_schema["properties"]["intent"]["properties"]["rhetorical"]["enum"])
    vocab = load(P["vocab_dir"] / "intent.enum.json")
    gov_moves = [v["id"] for v in vocab["dimensions"]["pedagogical"]["values"]]
    gov_rhetorical = [v["id"] for v in vocab["dimensions"]["rhetorical"]["values"]]
    if set(closed_moves) != set(gov_moves):
        raise SystemExit("element.intent.move does not mirror vocab/intent.enum.json pedagogical")
    if set(closed_rhetorical) != set(gov_rhetorical):
        raise SystemExit("element.intent.rhetorical does not mirror vocab/intent.enum.json rhetorical")

    obj_store = load(P["core_dir"] / "ontology" / "objectives.json")
    objective_ids = set(obj_store["objectives"])
    for required in (OBJ_EXPLAIN, OBJ_SCOPE, OBJ_PLAN, OBJ_DEVELOP, OBJ_OUTPUTS):
        if required not in objective_ids:
            raise SystemExit(f"ALSAP ontology missing {required} — Cartographer cannot bind teaches")

    if args.selftest:
        selftest(closed_moves, closed_rhetorical, objective_ids)
        return

    project = P["project_dir"]
    atoms_path = project / "atoms.json"
    if not atoms_path.exists():
        raise SystemExit(f"No atoms.json in project store: {project}")
    store_dir = pathlib.Path(args.store).resolve() if args.store else project / "occurrences"
    elements_path = store_dir / "elements.json"
    if not elements_path.exists():
        raise SystemExit(
            f"No occurrence store at {elements_path}. Run `python3 tools/realize.py` first."
        )
    if elements_path.resolve() == atoms_path.resolve():
        raise SystemExit("refusing to treat atoms.json as the occurrence store")

    atoms_bytes = atoms_path.read_bytes()
    atoms_hash_before = sha256_bytes(atoms_bytes)
    atoms = json.loads(atoms_bytes)
    mf_live = load(project / "manifest.json") if (project / "manifest.json").exists() else {}
    project_name = mf_live.get("project") or project.name
    instance_atoms = realize.load_instance_example_atoms(project)
    instance_path = realize.sibling_instance_project(project)
    instance_hash_before = (
        sha256_bytes((instance_path / "atoms.json").read_bytes()) if instance_path else None
    )
    form_atoms = realize.load_form_field_atoms(project)
    form_path = realize.sibling_form_project(project)
    form_hash_before = (
        sha256_bytes((form_path / "atoms.json").read_bytes()) if form_path else None
    )
    option_sets = realize.load_option_sets(project)
    atoms_by_id = realize.meaning_catalog(atoms, form_atoms + instance_atoms)
    if len({a["atom_id"] for a in atoms if "atom_id" in a}) != len(atoms):
        raise SystemExit("atom store has missing or duplicate atom_id values")

    elements = load(elements_path)
    if not isinstance(elements, list) or not elements:
        raise SystemExit(f"{elements_path} is not a non-empty element list")
    before_ids = {e["element_id"] for e in elements}
    before_expr = {
        e["element_id"]: (
            {k: v for k, v in e["expression"].items() if k != "text_primitive"} or None
            if isinstance(e.get("expression"), dict) else None
        )
        for e in elements
    }

    intent_map = load_intent_map(project, objective_ids, closed_moves)

    for el in elements:
        eid = el["element_id"]
        cf = el.get("composed_from")
        atom = atoms_by_id.get(cf)
        if atom is None:
            raise SystemExit(f"{eid}: composed_from {cf} is not in the atom store")
        intent, stamp = bind_intent_for_occurrence(
            el, atom, closed_moves, closed_rhetorical, objective_ids,
            project=project_name,
        )
        entry = intent_map.get(cf)
        if entry:
            intent, stamp = apply_intent_map(
                el, atom, intent, stamp, entry, closed_moves, project=project_name)
        apply_intent(el, intent, stamp)

    realize.refresh_text_primitives(elements, atoms_by_id)

    after_ids = {e["element_id"] for e in elements}
    assert_no_id_minting(before_ids, after_ids)
    for el in elements:
        old_expr = before_expr.get(el["element_id"])
        new_full = el.get("expression")
        new_expr = None
        if isinstance(new_full, dict):
            new_expr = {k: v for k, v in new_full.items() if k != "text_primitive"} or None
        if old_expr != new_expr:
            raise SystemExit(
                f"{el['element_id']}: Cartographer must not rewrite Couturier style "
                f"(was {old_expr}, now {new_expr})"
            )
    validate_elements(elements, element_schema, atoms_by_id, objective_ids, closed_moves, closed_rhetorical)

    move_counts = Counter(e["intent"]["move"] for e in elements)
    teaches_bound = sum(1 for e in elements if e["intent"].get("teaches"))
    low_n = sum(1 for e in elements if e.get("ext", {}).get("cartographer", {}).get("confidence") == "low")
    if len(move_counts) < 2:
        raise SystemExit(f"heuristic v1 produced only {dict(move_counts)} — expected mixed moves")
    if teaches_bound < 1 and project_name == "ast_alsap":
        raise SystemExit("heuristic v1 bound teaches on zero occurrences")

    mf_path = store_dir / "manifest.json"
    occ_manifest = load(mf_path) if mf_path.exists() else {}
    occ_manifest["cartographer"] = {
        "policy": POLICY,
        "tool": CARTOGRAPHER,
        "heuristic": "agents/cartographer/heuristic_v1.md",
        "move_counts": dict(sorted(move_counts.items())),
        "teaches_bound": teaches_bound,
        "low_confidence": low_n,
        "element_count": len(elements),
        "ontology": "ontology/objectives.json",
        "note": ("v1 compiler pass over Realizer occurrences, including extra 1:many "
                 "records. Cartographer writes intent only; it does not mint ele_ ids "
                 "or rewrite atoms. Extra occurrences keep Realizer-stamped move. "
                 "Couturier owns expression style; this tool does not wipe it. "
                 "After writing move, Realizer refreshes text_primitive (compiler form). "
                 "Lesson spine is Realizer projection (agents/realizer/spine_v1.md); "
                 "this tool does not own sequence. Does not wipe ext.check, ext.scene, "
                 "or manifest.lessons. Re-stamps scene records from the project "
                 "catalog (occurrences/scenes.json) when present. Re-stamps lesson "
                 "records from the project catalog (occurrences/lessons.json) when present."),
    }

    lesson_catalog = realize.load_lesson_catalog(store_dir)
    scene_catalog = realize.load_scene_catalog(store_dir)
    if lesson_catalog:
        realize.stamp_lessons(occ_manifest, atoms, elements, lesson_catalog=lesson_catalog)
    html_path = realize.lesson_html_path(
        project, occ_manifest, args.lesson, out=args.out
    )

    if args.dry_run:
        print(f"Cartographer v1 DRY-RUN → {len(elements)} elements ({POLICY})")
        print(f"  moves      : {dict(sorted(move_counts.items()))}")
        print(f"  teaches    : {teaches_bound} occurrences bound")
        print(f"  low-conf   : {low_n}")
        print("  no files written")
        return

    realize.apply_spine(
        occ_manifest, atoms, elements,
        meaning_atoms=form_atoms + instance_atoms, option_sets=option_sets,
        lesson_catalog=lesson_catalog, scene_catalog=scene_catalog,
    )
    realize.stamp_checks(
        occ_manifest, atoms, elements,
        meaning_atoms=form_atoms + instance_atoms,
        options_registry=option_sets,
    )
    realize.stamp_primitives(occ_manifest, elements)
    realize.normalize_elements_ext(elements)
    elements_path.write_text(json.dumps(elements, indent=2) + "\n")
    mf_path.write_text(json.dumps(occ_manifest, indent=2) + "\n")
    coverage_path, html_path, extra_htmls = realize.project_lesson_htmls(
        atoms, elements, occ_manifest, project,
        meaning_atoms=form_atoms + instance_atoms,
        option_sets=option_sets, options_registry=option_sets,
        lesson_id=args.lesson, out=args.out, lesson_catalog=lesson_catalog,
        scene_catalog=scene_catalog,
    )
    mf_path.write_text(json.dumps(occ_manifest, indent=2) + "\n")

    atoms_hash_after = sha256_bytes(atoms_path.read_bytes())
    if atoms_hash_after != atoms_hash_before:
        raise SystemExit("atoms.json changed during cartographer — abort. Cartographer must not rewrite atoms.")
    if instance_path and instance_hash_before:
        if sha256_bytes((instance_path / "atoms.json").read_bytes()) != instance_hash_before:
            raise SystemExit(
                "alsap_asp9999/atoms.json changed during cartographer — abort. "
                "Cartographer must not rewrite instance atoms."
            )
    if form_path and form_hash_before:
        if sha256_bytes((form_path / "atoms.json").read_bytes()) != form_hash_before:
            raise SystemExit(
                "alsap/atoms.json changed during cartographer — abort. "
                "Cartographer must not rewrite form atoms."
            )

    leftover_intent = [
        a["atom_id"] for a in atoms
        if isinstance((a.get("bindings") or {}).get("intent"), dict)
        and (a.get("bindings") or {}).get("intent")
    ]
    if leftover_intent:
        raise SystemExit(f"atom.intent is closed; leftover on {leftover_intent}")

    print(f"Cartographer v1 → {len(elements)} elements ({POLICY})")
    print(f"  atoms        : {atoms_path} ({len(atoms)} records, unchanged)")
    print(f"  occurrences  : {elements_path}")
    print(f"  manifest     : {mf_path}")
    print(f"  lesson HTML  : {html_path}")
    print(f"  lesson JSON  : {realize.lesson_player_json_path(html_path)}")
    for extra_html in extra_htmls:
        print(f"  extra HTML   : {extra_html}")
        print(f"  extra JSON   : {realize.lesson_player_json_path(extra_html)}")
    print(f"  coverage     : {coverage_path}")
    print(f"  moves        : {dict(sorted(move_counts.items()))}")
    print(f"  teaches bound: {teaches_bound}  ·  low-confidence: {low_n}")
    extras = [e for e in elements if realize.is_extra_element(e)]
    if extras:
        print(f"  extras kept  : {len(extras)} ({', '.join(e['element_id'] + '=' + e['intent']['move'] for e in extras)})")
    print("  schema       : element.schema.json ALL PASS (intent only; no authored content.text)")


if __name__ == "__main__":
    main()
