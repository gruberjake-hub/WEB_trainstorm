#!/usr/bin/env python3
"""
Realizer v1 — atoms → occurrence elements + a double-clickable HTML lesson.

The Realizer is the typesetter of meaning (`architecture/agents-roster.md`). It
does not invent authored text. Display HTML reads meaning from the atom via
`composed_from`. Default is still **one occurrence per atom** (move placeholder
`present`). A small documented 1:many seed then mints extra `ele_` records for
a couple of teaching-worthy atoms — same `composed_from`, distinct `move`,
stable extra ids. The rest of the store stays 1:1. Not a full ID treatment of
the SOP.

`reinforce` extras (Gagné 9a; closed vocab has no `retrieve`) project as a
**check** derived from the atom's existing meaning (`agents/realizer/check_v1.md`)
— a stem + choices or a cloze, not an italic reprint. No authored
`content.text`. Distractors, if any, are sibling atoms in the same store.

Default HTML is a **short lesson spine** (`agents/realizer/spine_v1.md`): title
hook, a why-this callout of the purpose atom (`tp_callout`), a handful of
front-matter teaching cards, Procedure A’s real steps as a job sequence
(present only), one worked example from the sibling instance store (two
`exemplify` extras of existing ASP-9999 atoms — `agents/realizer/instance_example_v1.md`),
then the existing checks. The full SOP dump is
`realized_coverage.html`. Spine is a selection of existing `ele_` records —
it mints none for membership and drops none. Procedure-step atoms stay 1:1
(no extra `reinforce`): they are imperatives, so they cannot host an honest
copula-invert sibling check. Instance extras `composed_from` instance
`atom_id`s; they do not copy text onto the element or into SOP `atoms.json`.

**Atom → primitives** (`agents/realizer/primitives_v1.md`): Realizer binds a
closed compiler `text_primitive` on the occurrence from atom kind + occurrence
move (heading / body / step / callout / check). The spine projector renders
those primitives — why-this as a callout of purpose, Procedure A s1–s4 as one
job-aid step list, the instance example as body/`exemplify` clothes (not a
new SOP card), front-matter as heading/body, reinforce as the existing
check. Coverage stays card-like. Couturier still owns `style_ref`. No authored
`content.text`.

Idempotency: extra ids are `(primary ele_) + "__" + move`. A re-run accretes
missing extras and never drops existing extras or Cartographer bindings.
Primitive keys recompute from kind + move.

Not this tool: Dragoman (locale packs), Storyline, .potx, PNG pipelines,
`tools/render/`, Netlify / `/cgen/alsap` hosting. Couturier (`tools/couturier.py`)
owns style keys on the occurrence; a re-realize preserves them and rebinds
`text_primitive`. Does not rewrite SOP/form atoms into elements — `atoms.json`
is read-only. Cartographer still binds `teaches` / rest of intent.

Usage (from `cgen/trainstorm-core`):

    python tools/realize.py
    python tools/realize.py --project ../astellas/projects/ast_alsap
    python tools/realize.py --selftest
    python tools/cartographer.py          # re-runnable on the mixed store
    python tools/couturier.py             # dresses existing ele_; mints nothing

Default `--project` is the live ALSAP SOP store (47 atoms). Writes (regenerated,
never hand-edited):

    <project>/occurrences/elements.json     occurrence store (does not touch atoms.json)
    <project>/occurrences/manifest.json     realized_from / source hashes + spine keys
    <project>/realized_lesson.html          short lesson (spine). Open this.
    <project>/realized_coverage.html        full SOP dump in document order
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import pathlib
import re
import sys
from collections import Counter, defaultdict

import harness_paths
from jsonschema import Draft202012Validator

POLICY = "v1_one_occurrence_per_atom"
EXTRA_POLICY = "v1_extra_occurrence"
STORE_POLICY = "v1_one_to_many_seed"
REALIZER = "tools/realize.py"
DEFAULT_MOVE = "present"
ELE_ID_RE = re.compile(r"^ele_[A-Za-z0-9_-]+$")

# Honest 1:many seed — a couple of teaching-worthy ALSAP atoms, not the whole SOP.
# Primary occurrence keeps Cartographer's bound move; Realizer stamps `move` only
# on the extra. Closed pedagogical vocab has no `retrieve`; `reinforce` is Gagné
# 9a (enhance retention), the legal name for a later placement of the same meaning.
# Purpose also mints `activate` so the spine can wear tp_callout (why this).
# Spec: agents/realizer/one_to_many_v1.md
ONE_TO_MANY_SEED = (
    ("atom_sop_ast29080", "present"),            # title: hook (primary) + present
    ("atom_sop_ast29080_general", "reinforce"),  # what ALSAP is: present + check
    ("atom_sop_ast29080_purpose", "activate"),   # SOP purpose: why-this callout
    ("atom_sop_ast29080_purpose", "reinforce"),  # SOP purpose: objective + check
)
CHECK_SPEC = "agents/realizer/check_v1.md"
CHECK_POLICY = "v1_check_from_atom"
SPINE_SPEC = "agents/realizer/spine_v1.md"
SPINE_POLICY = "v1_front_matter_callout_procedure_sequence_example_then_checks"
INSTANCE_EXAMPLE_SPEC = "agents/realizer/instance_example_v1.md"
INSTANCE_EXAMPLE_POLICY = "v1_instance_example_seed"
INSTANCE_PROJECT_NAME = "alsap_asp9999"
# Procedure A has no honest match in the instance store (plan-development
# acts vs filled AST-34037 values). These two illustrate the ALSAP generally:
# the SMT's selected BR conclusion + the authored rationale. Not the other 8.
INSTANCE_EXAMPLE_SEED = (
    ("atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_profile", "exemplify"),
    ("atom_alsap_asp9999__form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale", "exemplify"),
)
PRIMITIVE_SPEC = "agents/realizer/primitives_v1.md"
PRIMITIVE_POLICY = "v1_atom_to_primitive"
# Closed compiler vocabulary. Keys must exist in primitives.registry.json.
# heading/body/check reuse Couturier v1 look keys; step + callout are this hop.
PRIMITIVE_HEADING = "tp_display"
PRIMITIVE_BODY = "tp_body"
PRIMITIVE_STEP = "tp_step"
PRIMITIVE_CHECK = "tp_recall"
PRIMITIVE_CALLOUT = "tp_callout"
PRIMITIVE_PURPOSE = "tp_purpose"
# First Procedures-container branch’s non-thin procedure_step children, in
# object.order. Live ALSAP Procedure A is a handful (4) — all land. Cap only
# if that branch is huge. Not B/C, not thin A/B/C headings.
PROCEDURE_SEQUENCE_CAP = 8

KIND_TO_TYPE = {
    "procedure": "Section",
    "procedure_step": "Statement",
    "list": "List",
    "list_item": "Bullet",
    "form": "Section",
    "form_section": "Section",
    "form_field": "Statement",
    "instance_value": "Statement",
}
TYPE_TO_RHETORICAL = {
    "Course": "orient",
    "Section": "structure",
    "Head": "orient",
    "ListHead": "organize",
    "List": "organize",
    "Bullet": "specify",
    "Statement": "assert",
    "Paragraph": "explain",
    "Impact": "persuade",
    "Quote": "contextualize",
    "Callout": "support",
}


def repo_default_project():
    """Sibling live ALSAP SOP store: cgen/astellas/projects/ast_alsap."""
    p = pathlib.Path(__file__).resolve().parent.parent.parent / "astellas" / "projects" / "ast_alsap"
    return p if (p / "atoms.json").exists() else None


def argv_has_flag(name):
    prefix = name + "="
    for a in sys.argv[1:]:
        if a == name or a.startswith(prefix):
            return True
    return False


def inject_default_project():
    """Other harness tools require --project. Realizer v1 has a known first hop."""
    if argv_has_flag("--project") or os.environ.get("TRAINSTORM_PROJECT"):
        return
    d = repo_default_project()
    if d is not None:
        os.environ["TRAINSTORM_PROJECT"] = str(d)


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def mint_element_id(atom_id: str) -> str:
    if not atom_id.startswith("atom_"):
        raise SystemExit(f"cannot mint ele_ from {atom_id!r}: not an atom_ id")
    eid = "ele_" + atom_id[len("atom_"):]
    if not ELE_ID_RE.match(eid):
        raise SystemExit(f"minted id fails ele_ pattern: {eid}")
    return eid


def mint_extra_element_id(atom_id: str, move: str) -> str:
    """Stable extra occurrence id: primary ele_ + '__' + closed-vocab move."""
    if not re.match(r"^[a-z]+$", move):
        raise SystemExit(f"cannot mint extra ele_ for ungoverned move {move!r}")
    eid = mint_element_id(atom_id) + "__" + move
    if not ELE_ID_RE.match(eid):
        raise SystemExit(f"minted extra id fails ele_ pattern: {eid}")
    return eid


def is_primary_element(el) -> bool:
    cf = el.get("composed_from")
    return bool(cf) and el.get("element_id") == mint_element_id(cf)


def is_extra_element(el) -> bool:
    rf = (el.get("ext") or {}).get("realized_from") or {}
    if rf.get("role") == "extra":
        return True
    cf = el.get("composed_from")
    return bool(cf) and el.get("element_id") != mint_element_id(cf)


def element_type(atom) -> str:
    kind = (atom.get("meaning") or {}).get("kind")
    belongs = (atom.get("bindings") or {}).get("object", {}).get("belongs_to")
    if not belongs:
        return "Course"
    return KIND_TO_TYPE.get(kind, "Statement")


def clean_meaning(text: str) -> str:
    i = text.find("[Headwater")
    return text[:i].strip() if i != -1 else text.strip()


def kids(atoms, parent_id):
    ch = [a for a in atoms
          if (a.get("bindings") or {}).get("object", {}).get("belongs_to") == parent_id]
    return sorted(ch, key=lambda a: (a.get("bindings") or {}).get("object", {}).get("order", 0))


def roots(atoms):
    r = [a for a in atoms
         if not (a.get("bindings") or {}).get("object", {}).get("belongs_to")]
    if r:
        return r
    return list(atoms)


def portable_atom_store_path(atoms_path: pathlib.Path) -> str:
    """Repo-relative path when possible — never a machine-local absolute."""
    repo = pathlib.Path(__file__).resolve().parents[3]  # …/cgen/trainstorm-core/tools → repo
    try:
        return str(atoms_path.resolve().relative_to(repo))
    except ValueError:
        return "atoms.json"


def sibling_instance_project(sop_project: pathlib.Path | None) -> pathlib.Path | None:
    """Lesson store is ast_alsap; instance is sibling alsap_asp9999. Not every project."""
    if sop_project is None or sop_project.name != "ast_alsap":
        return None
    sibling = sop_project.parent / INSTANCE_PROJECT_NAME
    if (sibling / "atoms.json").exists():
        return sibling
    return None


def load_instance_example_atoms(sop_project: pathlib.Path | None) -> list:
    """Join catalog only. Does not rewrite SOP or instance atoms.json."""
    sibling = sibling_instance_project(sop_project)
    if sibling is None:
        return []
    atoms = load(sibling / "atoms.json")
    if not isinstance(atoms, list):
        return []
    return [a for a in atoms if a.get("atom_id")]


def meaning_catalog(sop_atoms, extra_atoms=None) -> dict:
    """SOP atoms plus joined instance atoms, keyed by atom_id. SOP wins on collision."""
    by_id = {a["atom_id"]: a for a in sop_atoms if a.get("atom_id")}
    for a in extra_atoms or []:
        aid = a.get("atom_id")
        if aid and aid not in by_id:
            by_id[aid] = a
    return by_id


def mint_element(atom, move: str, *, role: str = "primary") -> dict:
    aid = atom["atom_id"]
    obj = (atom.get("bindings") or {}).get("object") or {}
    typ = element_type(atom)
    extra = role == "extra"
    realized_from = {
        "atom_id": aid,
        "realizer": REALIZER,
        "policy": EXTRA_POLICY if extra else POLICY,
        "role": "extra" if extra else "primary",
    }
    if extra:
        realized_from["target_move"] = move
    ch = atom.get("content_hash")
    if ch:
        realized_from["content_hash"] = ch
    structure = {}
    if obj.get("belongs_to"):
        structure["parent_id"] = mint_element_id(obj["belongs_to"])
    if "order" in obj:
        structure["sequence_index"] = obj["order"]
    if obj.get("prerequisites"):
        structure["prerequisites"] = [mint_element_id(p) for p in obj["prerequisites"]]
    gov = {
        "version": 1,
        "status": "draft",
        "owner": "realizer",
    }
    rb = (atom.get("governance") or {}).get("regulatory_binding")
    if rb:
        gov["regulatory_binding"] = rb
    el = {
        "element_id": mint_extra_element_id(aid, move) if extra else mint_element_id(aid),
        "composed_from": aid,
    }
    if ch:
        el["source_hash"] = ch
    el["type"] = typ
    if structure:
        el["structure"] = structure
    el["intent"] = {
        "rhetorical": TYPE_TO_RHETORICAL.get(typ, "assert"),
        "move": move,
    }
    el["governance"] = gov
    el["ext"] = {"realized_from": realized_from}
    return el


def apply_group_ids(elements):
    """Pair 1:many members via structure.group_id = composed_from (atom_id)."""
    from collections import defaultdict
    by_atom = defaultdict(list)
    for el in elements:
        by_atom[el["composed_from"]].append(el)
    for aid, group in by_atom.items():
        if len(group) < 2:
            continue
        for el in group:
            el.setdefault("structure", {})["group_id"] = aid


def extra_move_of(el) -> str | None:
    intent_move = (el.get("intent") or {}).get("move")
    rf = (el.get("ext") or {}).get("realized_from") or {}
    return rf.get("target_move") or intent_move


EXT_KEY_ORDER = ("realized_from", "cartographer", "couturier", "realizer_primitive")


def normalize_element_ext(el):
    """Stable ext key order so re-runs do not reshuffle JSON."""
    ext = el.get("ext")
    if not isinstance(ext, dict) or not ext:
        return
    ordered = {}
    for k in EXT_KEY_ORDER:
        if k in ext:
            ordered[k] = ext[k]
    for k, v in ext.items():
        if k not in ordered:
            ordered[k] = v
    el["ext"] = ordered


def normalize_elements_ext(elements):
    for el in elements:
        normalize_element_ext(el)
    return elements


def assemble_elements(atoms, previous, default_move: str, *, mint_extras: bool = True,
                      instance_atoms=None) -> list:
    """
    Mint one primary per SOP atom, then extra occurrences from the seed and from
    any extras already in the store. Never drop an existing extra. Preserve
    Cartographer intent on matching element_id values. Guest instance extras
    (sibling alsap_asp9999) mint into this occurrence store with composed_from
    pointing at the instance atom_id — they are not copied into SOP atoms.json.
    """
    prev = {e.get("element_id"): e for e in (previous or []) if e.get("element_id")}
    instance_by_id = {a["atom_id"]: a for a in (instance_atoms or []) if a.get("atom_id")}
    atoms_by_id = meaning_catalog(atoms, instance_atoms)
    seed_moves = {}
    if mint_extras:
        for aid, move in ONE_TO_MANY_SEED:
            seed_moves.setdefault(aid, []).append(move)

    elements = []
    claimed = set()

    for atom in atoms:
        aid = atom["atom_id"]
        primary = mint_element(atom, default_move, role="primary")
        preserve_cartographer_intent([primary], previous)
        preserve_couturier_expression([primary], previous)
        elements.append(primary)
        claimed.add(primary["element_id"])

        wanted = []  # (element_id, move)
        seen_eids = set()
        for move in seed_moves.get(aid, []):
            eid = mint_extra_element_id(aid, move)
            wanted.append((eid, move))
            seen_eids.add(eid)
        for old in prev.values():
            if old.get("composed_from") != aid or not is_extra_element(old):
                continue
            eid = old["element_id"]
            if eid in seen_eids:
                continue
            move = extra_move_of(old)
            if not move:
                continue
            wanted.append((eid, move))
            seen_eids.add(eid)

        for eid, move in wanted:
            extra = mint_element(atom, move, role="extra")
            extra["element_id"] = eid
            preserve_cartographer_intent([extra], previous)
            preserve_couturier_expression([extra], previous)
            if not (extra.get("ext") or {}).get("cartographer"):
                extra["intent"]["move"] = move
            elements.append(extra)
            claimed.add(eid)

    wanted_inst = []
    seen_inst = set()
    if mint_extras:
        for aid, move in INSTANCE_EXAMPLE_SEED:
            if aid not in instance_by_id:
                continue
            eid = mint_extra_element_id(aid, move)
            wanted_inst.append((eid, aid, move))
            seen_inst.add(eid)
    for old in prev.values():
        cf = old.get("composed_from")
        if cf not in instance_by_id or not is_extra_element(old):
            continue
        eid = old["element_id"]
        if eid in seen_inst or eid in claimed:
            continue
        move = extra_move_of(old)
        if not move:
            continue
        wanted_inst.append((eid, cf, move))
        seen_inst.add(eid)
    for eid, aid, move in wanted_inst:
        if eid in claimed:
            continue
        extra = mint_element(instance_by_id[aid], move, role="extra")
        extra["element_id"] = eid
        rf = extra.setdefault("ext", {}).setdefault("realized_from", {})
        rf["instance_store"] = INSTANCE_PROJECT_NAME
        rf["instance_spec"] = INSTANCE_EXAMPLE_SPEC
        rf["policy"] = INSTANCE_EXAMPLE_POLICY
        preserve_cartographer_intent([extra], previous)
        preserve_couturier_expression([extra], previous)
        if not (extra.get("ext") or {}).get("cartographer"):
            extra["intent"]["move"] = move
        elements.append(extra)
        claimed.add(eid)

    for eid, old in prev.items():
        if eid in claimed:
            continue
        cf = old.get("composed_from")
        if cf in atoms_by_id and is_extra_element(old):
            elements.append(old)
            claimed.add(eid)

    apply_group_ids(elements)
    refresh_text_primitives(elements, atoms_by_id)
    normalize_elements_ext(elements)
    return elements


def validate_elements(elements, schema, atoms_by_id):
    v = Draft202012Validator(schema)
    hard = []
    seen = set()
    for el in elements:
        for err in sorted(v.iter_errors(el), key=lambda e: list(e.path)):
            hard.append(f"{el.get('element_id', '?')}: {err.message}")
        eid = el.get("element_id")
        if eid in seen:
            hard.append(f"duplicate element_id {eid}")
        seen.add(eid)
        if "content" in el:
            hard.append(f"{eid}: authored content is forbidden on v1 occurrences "
                        "(meaning lives on the atom)")
        cf = el.get("composed_from")
        if cf not in atoms_by_id:
            hard.append(f"{eid}: composed_from {cf} is not in the atom store")
        if el.get("intent", {}).get("move") is None:
            hard.append(f"{eid}: missing intent.move")
        if is_extra_element(el):
            rf = (el.get("ext") or {}).get("realized_from") or {}
            if rf.get("role") and rf.get("role") != "extra":
                hard.append(f"{eid}: extra occurrence realized_from.role is {rf.get('role')!r}")
    if hard:
        print("REALIZER VALIDATION FAILURES:", file=sys.stderr)
        for m in hard:
            print("  x", m, file=sys.stderr)
        raise SystemExit(1)


def move_counts(elements):
    counts = {}
    for el in elements:
        m = (el.get("intent") or {}).get("move") or "?"
        counts[m] = counts.get(m, 0) + 1
    return counts


def preserve_cartographer_intent(elements, previous):
    """Single-writer: Cartographer owns occurrence intent. A re-realize must not clobber it.

    Extra occurrences also keep their Cartographer binding. Their `move` exists
    because Realizer minted a second teaching act; Realizer must not wipe it on re-run.
    """
    if not previous:
        return
    prev = {e.get("element_id"): e for e in previous if e.get("element_id")}
    for el in elements:
        old = prev.get(el.get("element_id"))
        if not old:
            continue
        cart = (old.get("ext") or {}).get("cartographer")
        if not cart:
            # Extra without Cartographer yet: keep Realizer-stamped move.
            if is_extra_element(el) and (old.get("intent") or {}).get("move"):
                el.setdefault("intent", {})["move"] = old["intent"]["move"]
            continue
        if "intent" in old:
            el["intent"] = old["intent"]
        el.setdefault("ext", {})["cartographer"] = cart


def preserve_couturier_expression(elements, previous):
    """Single-writer: Couturier owns occurrence style. A re-realize must not clobber it."""
    if not previous:
        return
    prev = {e.get("element_id"): e for e in previous if e.get("element_id")}
    for el in elements:
        old = prev.get(el.get("element_id"))
        if not old:
            continue
        cout = (old.get("ext") or {}).get("couturier")
        if not cout and "expression" not in old:
            continue
        if "expression" in old:
            el["expression"] = old["expression"]
        if cout:
            el.setdefault("ext", {})["couturier"] = cout


def atom_kind_of(atom) -> str:
    return (atom.get("meaning") or {}).get("kind") or ""


def classify_text_primitive(atom, el) -> str:
    """Closed compiler form from atom object-role + occurrence move.

    Spec: agents/realizer/primitives_v1.md. Not a design system. First match wins.
    """
    move = (el.get("intent") or {}).get("move") or ""
    kind = atom_kind_of(atom)
    if move == "reinforce":
        return PRIMITIVE_CHECK
    if move == "hook":
        return PRIMITIVE_HEADING
    if kind == "procedure_step":
        return PRIMITIVE_STEP
    if move == "activate":
        return PRIMITIVE_CALLOUT
    if move == "objective":
        return PRIMITIVE_PURPOSE
    return PRIMITIVE_BODY


def bind_text_primitive(el, atom) -> str:
    """Write Realizer-owned compiler key. Do not wipe Couturier style_ref."""
    key = classify_text_primitive(atom, el)
    expr = dict(el.get("expression") or {})
    expr["text_primitive"] = key
    el["expression"] = expr
    ext = el.setdefault("ext", {})
    ext["realizer_primitive"] = {
        "policy": PRIMITIVE_POLICY,
        "tool": REALIZER,
        "spec": PRIMITIVE_SPEC,
        "from_kind": atom_kind_of(atom),
        "from_move": (el.get("intent") or {}).get("move") or "",
        "text_primitive": key,
    }
    return key


def refresh_text_primitives(elements, atoms_by_id):
    """Recompute text_primitive on every occurrence. Pure function of kind + move."""
    for el in elements:
        cf = el.get("composed_from")
        atom = atoms_by_id.get(cf)
        if atom is None:
            raise SystemExit(f"{el.get('element_id')}: composed_from {cf} is not in the atom store")
        bind_text_primitive(el, atom)


def primitive_counts(elements):
    counts = {}
    for el in elements:
        tp = (el.get("expression") or {}).get("text_primitive") or "?"
        counts[tp] = counts.get(tp, 0) + 1
    return counts


def is_step_primitive(el) -> bool:
    return (el.get("expression") or {}).get("text_primitive") == PRIMITIVE_STEP


def stamp_primitives(manifest, elements) -> dict:
    """Stamp compiler-primitive provenance on the occurrence manifest."""
    manifest["primitives"] = {
        "policy": PRIMITIVE_POLICY,
        "spec": PRIMITIVE_SPEC,
        "owner": "realizer",
        "counts": dict(sorted(primitive_counts(elements).items())),
        "note": ("Closed compiler form on the occurrence (heading/body/step/"
                 "callout/check). Realizer binds text_primitive from atom kind "
                 "+ occurrence move. Couturier still owns style_ref."),
    }
    return manifest["primitives"]


def assert_primitives_registered(elements, closed_text_primitives):
    hard = []
    for el in elements:
        eid = el.get("element_id")
        tp = (el.get("expression") or {}).get("text_primitive")
        if not tp:
            hard.append(f"{eid}: missing text_primitive after Realizer bind")
        elif tp not in closed_text_primitives:
            hard.append(f"{eid}: text_primitive {tp!r} is not in primitives.registry.json")
        stamp = (el.get("ext") or {}).get("realizer_primitive") or {}
        if stamp.get("policy") != PRIMITIVE_POLICY:
            hard.append(f"{eid}: missing ext.realizer_primitive.policy={PRIMITIVE_POLICY}")
    if hard:
        print("PRIMITIVE VALIDATION FAILURES:", file=sys.stderr)
        for m in hard:
            print("  x", m, file=sys.stderr)
        raise SystemExit(1)


CLOTHES_CLASS = {
    "brand.opening": "style-opening",
    "brand.instructional": "style-instructional",
    "brand.recall": "style-recall",
    "brand.purpose": "style-purpose",
    "brand.prior": "style-prior",
    "brand.example": "style-example",
    "brand.job": "style-job",
}

KICKER = {
    "title": "Opening",
    "body": "Present",
    "retrieval": "Check",
    "purpose": "Purpose",
    "prior": "Already known",
    "callout": "Why this",
    "example": "Example",
    "handoff": "On the job",
    "step": "Job aid",
}

THIN_HEADING_RE = re.compile(
    r"^(roles and responsibilities|procedures|organizations in scope of this sop)\.?$",
    re.I,
)
GLOSSARY_POINTER_RE = re.compile(r"^for definitions,\s+refer\b", re.I)


def first_sentence(text: str) -> str:
    t = clean_meaning(text or "")
    if not t:
        return ""
    if ". " in t:
        return t.split(". ", 1)[0].strip().rstrip(".") + "."
    return t if t.endswith(".") else t + "."


def strip_period(s: str) -> str:
    s = (s or "").strip()
    return s[:-1] if s.endswith(".") else s


def copula_parts(sentence: str) -> tuple[str, str] | None:
    """Split '{subject} is {complement}'. Complement must be substantial."""
    body = strip_period(sentence)
    m = re.match(r"^(?P<sub>.+?)\s+is\s+(?P<comp>.+)$", body, re.I)
    if not m:
        return None
    sub, comp = m.group("sub").strip(), m.group("comp").strip()
    if len(sub) < 3 or len(comp) < 8:
        return None
    return sub, comp


def question_stem(subject: str) -> str:
    """Grammatical invert of '{subject} is …' — a question form, not a new fact."""
    s = (subject or "").strip()
    low = s[:4].lower()
    if low == "the ":
        s = "the " + s[4:]
    elif s[:3].lower() == "an ":
        s = "an " + s[3:]
    elif s[:2].lower() == "a ":
        s = "a " + s[2:]
    return f"What is {s}?"


def atom_belongs_to(atom):
    return (atom.get("bindings") or {}).get("object", {}).get("belongs_to")


def atom_order(atom) -> int:
    return int((atom.get("bindings") or {}).get("object", {}).get("order", 0) or 0)


def is_usable_sibling(atom) -> bool:
    text = clean_meaning((atom.get("meaning") or {}).get("source_text") or "")
    if len(text) < 50:
        return False
    if THIN_HEADING_RE.match(text):
        return False
    if GLOSSARY_POINTER_RE.match(text):
        return False
    return True


def sibling_atoms(atom, atoms) -> list:
    """Same parent in the store — closed contrast, not invented misconceptions."""
    parent = atom_belongs_to(atom)
    out = []
    for a in atoms:
        if a.get("atom_id") == atom.get("atom_id"):
            continue
        if atom_belongs_to(a) != parent:
            continue
        if is_usable_sibling(a):
            out.append(a)
    return sorted(out, key=atom_order)


def phrase_in_atom(phrase: str, atom) -> bool:
    src = clean_meaning((atom.get("meaning") or {}).get("source_text") or "")
    p = (phrase or "").strip()
    if not p or not src:
        return False
    return p in src or strip_period(p) in src


def is_check_occurrence(el) -> bool:
    move = (el.get("intent") or {}).get("move")
    expr = el.get("expression") or {}
    return (
        move == "reinforce"
        or expr.get("style_ref") == "brand.recall"
        or expr.get("text_primitive") == "tp_recall"
        or expr.get("layout_hint") == "check"
    )


def is_callout_occurrence(el) -> bool:
    """Activate / tp_callout extra — why-this clothes, not a check."""
    if is_check_occurrence(el):
        return False
    move = (el.get("intent") or {}).get("move")
    expr = el.get("expression") or {}
    return (
        move == "activate"
        or expr.get("text_primitive") == PRIMITIVE_CALLOUT
        or expr.get("layout_hint") == "callout"
    )


def is_thin_teaching_atom(atom) -> bool:
    """Heading-only or glossary pointer — not a paragraph an ID would teach."""
    text = clean_meaning((atom.get("meaning") or {}).get("source_text") or "")
    if len(text) < 50:
        return True
    if THIN_HEADING_RE.match(text):
        return True
    if GLOSSARY_POINTER_RE.match(text):
        return True
    return False


def is_front_matter_section(atom, root_id) -> bool:
    """Direct child of the document root with a teachable procedure/form paragraph."""
    if not root_id or atom.get("atom_id") == root_id:
        return False
    if atom_belongs_to(atom) != root_id:
        return False
    kind = (atom.get("meaning") or {}).get("kind")
    if kind not in ("procedure", "form"):
        return False
    return not is_thin_teaching_atom(atom)


def is_procedures_heading(atom) -> bool:
    text = clean_meaning((atom.get("meaning") or {}).get("source_text") or "")
    return bool(re.match(r"^procedures\.?$", text, re.I))


def descendants_of(atoms, parent_id) -> list:
    """All belongs_to descendants of parent_id, not including the parent."""
    by_parent = defaultdict(list)
    for a in atoms:
        pid = atom_belongs_to(a)
        if pid:
            by_parent[pid].append(a)
    out = []
    stack = list(by_parent.get(parent_id) or [])
    while stack:
        cur = stack.pop()
        out.append(cur)
        stack.extend(by_parent.get(cur["atom_id"]) or [])
    return out


def procedure_container(atoms, root_id):
    """SOP Procedures heading — parent of A/B/C branches. Not a walk of the steps."""
    if not root_id:
        return None
    direct = kids(atoms, root_id)
    for a in direct:
        if is_procedures_heading(a):
            return a
    for a in direct:
        if any((d.get("meaning") or {}).get("kind") == "procedure_step"
               for d in descendants_of(atoms, a["atom_id"])):
            return a
    return None


def procedure_sequence_atoms(atoms) -> list:
    """First real procedure’s job-sequence steps. Skip thin A/B/C headings.

    Object tree: Procedures. → A/B/C (thin) → steps. Walking that *is* the dump.
    This selector takes the first branch in object.order, then every non-thin
    procedure_step child in that order — on ALSAP, Plan Development’s four
    real A steps (notify Lead → identify authors → 15-day kick-off → confirm
    deliverables). Cap only if that branch is huge. Branches B/C stay coverage.
    """
    rs = roots(atoms)
    if not rs:
        return []
    rid = rs[0]["atom_id"]
    container = procedure_container(atoms, rid)
    if not container:
        return []
    branches = kids(atoms, container["atom_id"])
    if not branches:
        return []
    branch = branches[0]
    steps = [
        a for a in kids(atoms, branch["atom_id"])
        if (a.get("meaning") or {}).get("kind") == "procedure_step"
        and not is_thin_teaching_atom(a)
    ]
    if steps:
        return steps[:PROCEDURE_SEQUENCE_CAP]
    if not is_thin_teaching_atom(branch):
        kind = (branch.get("meaning") or {}).get("kind")
        if kind in ("procedure", "procedure_step"):
            return [branch]
    return []


def supports_honest_sibling_check(atom, atoms) -> bool:
    """True only for a copula invert plus two sibling first-sentences.

    Procedure steps are imperatives — no `{subject} is {complement}` — so this
    is False and we do not mint an extra `reinforce`. Cloze is not sibling
    contrast; do not treat it as an honest check for this hop.
    """
    sentence = first_sentence((atom.get("meaning") or {}).get("source_text") or "")
    if not copula_parts(sentence):
        return False
    chk = derive_check(atom, atoms)
    return bool(chk and chk.get("shape") == "mcq_siblings")


def spine_atom_ids(atoms) -> list:
    """Root, teachable front-matter, then Procedure A’s real steps. Not a tree walk."""
    rs = roots(atoms)
    if not rs:
        return []
    root = rs[0]
    rid = root["atom_id"]
    kids_teaching = [a for a in atoms if is_front_matter_section(a, rid)]
    kids_teaching.sort(key=atom_order)
    seen = {rid} | {a["atom_id"] for a in kids_teaching}
    seq_ids = [a["atom_id"] for a in procedure_sequence_atoms(atoms) if a["atom_id"] not in seen]
    return [rid] + [a["atom_id"] for a in kids_teaching] + seq_ids


def instance_example_spine_ids(elements) -> list:
    """Seed order. Guest extras whose composed_from is a cited instance atom."""
    by_eid = {e["element_id"]: e for e in elements}
    out = []
    for aid, move in INSTANCE_EXAMPLE_SEED:
        eid = mint_extra_element_id(aid, move)
        el = by_eid.get(eid)
        if el is None:
            continue
        if el.get("composed_from") != aid:
            continue
        if (el.get("intent") or {}).get("move") != move:
            continue
        out.append(eid)
    return out


def select_spine(atoms, elements) -> list:
    """Stable ele_ ids in teachable order. Selection of existing occurrences; mints nothing.

    Opening (root primary + non-check extras) → why-this activate extras of
    spine atoms → front-matter primaries → first real procedure’s step
    presents (job sequence) → instance-example extras → reinforce extras of
    spine atoms. Spec: agents/realizer/spine_v1.md
    """
    by_id = {e["element_id"]: e for e in elements}
    by_cf = defaultdict(list)
    for e in elements:
        by_cf[e["composed_from"]].append(e)

    def occs_for(atom_id):
        occs = list(by_cf.get(atom_id) or [])
        occs.sort(key=lambda e: (0 if is_primary_element(e) else 1, e["element_id"]))
        return occs

    opening = []
    presents = []
    checks = []
    for i, aid in enumerate(spine_atom_ids(atoms)):
        callouts = []
        primaries = []
        atom_checks = []
        for el in occs_for(aid):
            eid = el["element_id"]
            if eid not in by_id:
                continue
            extra_check = is_extra_element(el) and (
                (el.get("intent") or {}).get("move") == "reinforce" or is_check_occurrence(el)
            )
            extra_callout = is_extra_element(el) and is_callout_occurrence(el)
            if extra_check:
                atom_checks.append(eid)
            elif i == 0:
                opening.append(eid)
            elif extra_callout:
                callouts.append(eid)
            elif is_primary_element(el):
                primaries.append(eid)
        if i != 0:
            presents.extend(callouts + primaries)
        checks.extend(atom_checks)
    examples = instance_example_spine_ids(elements)
    return opening + presents + examples + checks


def apply_spine(manifest, atoms, elements) -> dict:
    """Stamp spine keys on the occurrence manifest. Pure projection; mints/drops no ele_."""
    ids = select_spine(atoms, elements)
    manifest["spine"] = {
        "policy": SPINE_POLICY,
        "spec": SPINE_SPEC,
        "element_ids": ids,
        "count": len(ids),
        "store_count": len(elements),
        "note": ("Selection of existing ele_ records in teachable order: document-root "
                 "opening, why-this activate callout of purpose, teachable front-matter "
                 "primaries (object.order), the first real procedure’s non-thin "
                 "procedure_step children as a job sequence (not thin A/B/C headings, "
                 "not B/C), then a small instance-example seed (alsap_asp9999 atoms via "
                 "composed_from — Procedure A has no honest match; these illustrate the "
                 "ALSAP generally), then existing reinforce extras. Spine projector "
                 "renders compiler primitives (callout / step list / heading / body / "
                 "check) plus exemplify clothes on the instance beats; coverage dump "
                 "stays card-like. Not an LLM path and not a full object-tree walk."),
    }
    return manifest["spine"]


def sibling_coverage_path(lesson_path: pathlib.Path) -> pathlib.Path:
    if lesson_path.name == "realized_lesson.html":
        return lesson_path.with_name("realized_coverage.html")
    return lesson_path.with_name(lesson_path.stem + "_coverage.html")


def job_aid_title(first_el, atoms_by_id) -> str:
    """Parent atom meaning — the thin A/B/C heading skipped as a teaching card."""
    atom = atoms_by_id.get(first_el.get("composed_from"))
    if not atom:
        return ""
    parent_id = atom_belongs_to(atom)
    parent = atoms_by_id.get(parent_id) if parent_id else None
    if not parent:
        return ""
    return clean_meaning((parent.get("meaning") or {}).get("source_text") or "")


def primitive_class(el) -> str:
    tp = (el.get("expression") or {}).get("text_primitive") or ""
    return {
        PRIMITIVE_HEADING: "prim-heading",
        PRIMITIVE_BODY: "prim-body",
        PRIMITIVE_PURPOSE: "prim-body",
        PRIMITIVE_STEP: "prim-step",
        PRIMITIVE_CHECK: "prim-check",
        PRIMITIVE_CALLOUT: "prim-callout",
    }.get(tp, "")


def group_spine_for_project(spine_ids, by_eid):
    """Consecutive tp_step occurrences become one job-aid run. Other beats stay singles."""
    groups = []
    i = 0
    n = len(spine_ids)
    while i < n:
        el = by_eid.get(spine_ids[i])
        if el is None:
            i += 1
            continue
        if is_step_primitive(el):
            run = []
            while i < n:
                nxt = by_eid.get(spine_ids[i])
                if nxt is None or not is_step_primitive(nxt):
                    break
                run.append(nxt)
                i += 1
            groups.append(("job_aid", run))
        else:
            groups.append(("card", [el]))
            i += 1
    return groups


def derive_check(atom, atoms) -> dict | None:
    """Project a check from this atom's meaning. Shape is a key, not a second meaning.

    Honesty: key ⊆ this atom; distractors ⊆ sibling atoms in the same store.
    """
    src = (atom.get("meaning") or {}).get("source_text") or ""
    sentence = first_sentence(src)
    if not sentence:
        return None
    src_clean = clean_meaning(src)
    parts = copula_parts(sentence)
    distractors = []
    for sib in sibling_atoms(atom, atoms):
        sib_sent = first_sentence((sib.get("meaning") or {}).get("source_text") or "")
        if not sib_sent:
            continue
        if strip_period(sib_sent).lower() == strip_period(sentence).lower():
            continue
        if not phrase_in_atom(sib_sent, sib):
            continue
        distractors.append({"text": sib_sent, "from_atom_id": sib["atom_id"]})
        if len(distractors) >= 2:
            break

    if parts:
        subject, complement = parts
        key = complement
        if key not in src_clean:
            return None
        stem = question_stem(subject)
        shape = "mcq_siblings" if distractors else "cloze"
        cloze_lead = cloze_blank = cloze_tail = None
        if shape == "cloze":
            # Type-in of the complement; stem still the question invert.
            cloze_lead, cloze_blank, cloze_tail = "", key, ""
    else:
        body = strip_period(sentence)
        words = body.split()
        if len(words) < 6:
            return None
        cloze_lead = " ".join(words[:3]) + " "
        cloze_blank = " ".join(words[3:-1])
        cloze_tail = " " + words[-1]
        key = cloze_blank
        if key not in src_clean:
            return None
        stem = f"{cloze_lead}______{cloze_tail}."
        shape = "mcq_siblings" if distractors else "cloze"

    check = {
        "shape": shape,
        "spec": CHECK_SPEC,
        "policy": CHECK_POLICY,
        "stem": stem,
        "key": key,
        "key_atom_id": atom["atom_id"],
        "sentence": sentence,
        "choices": [],
        "cloze_lead": cloze_lead if shape == "cloze" else None,
        "cloze_tail": cloze_tail if shape == "cloze" else None,
    }
    if shape == "mcq_siblings":
        check["choices"] = (
            [{"text": key, "correct": True, "from_atom_id": atom["atom_id"]}]
            + [{"text": d["text"], "correct": False, "from_atom_id": d["from_atom_id"]} for d in distractors]
        )
    return check


def assert_check_honest(check, atom, atoms):
    """Refuse a projection that invented a key or a distractor."""
    if not check:
        raise SystemExit(f"{atom.get('atom_id')}: check derivation returned nothing")
    if not phrase_in_atom(check["key"], atom):
        raise SystemExit(
            f"{atom.get('atom_id')}: check key is not in the atom — refusing to invent"
        )
    atoms_by_id = {a["atom_id"]: a for a in atoms}
    for c in check.get("choices") or []:
        src = atoms_by_id.get(c["from_atom_id"])
        if src is None:
            raise SystemExit(f"check choice cites unknown atom {c['from_atom_id']}")
        if not phrase_in_atom(c["text"], src):
            raise SystemExit(
                f"{atom.get('atom_id')}: choice from {c['from_atom_id']} is not in that atom"
            )
        if c["correct"] and c["from_atom_id"] != atom["atom_id"]:
            raise SystemExit(f"{atom.get('atom_id')}: key choice must cite this atom")
        if not c["correct"] and c["from_atom_id"] == atom["atom_id"]:
            raise SystemExit(f"{atom.get('atom_id')}: distractor must be a sibling, not this atom")


def stable_rotate(items, seed: str) -> list:
    if not items:
        return []
    n = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % len(items)
    return items[n:] + items[:n]


def check_body_html(el, atom, atoms, esc) -> str:
    """Occurrence body for reinforce: a check the reader can attempt."""
    chk = derive_check(atom, atoms)
    if chk:
        assert_check_honest(chk, atom, atoms)
    eid = el["element_id"]
    if not chk:
        # Last-resort cloze of whatever text exists — still from this atom.
        meaning = clean_meaning(atom["meaning"]["source_text"])
        return (
            f'<form class="check" data-shape="cloze" data-key="{esc(meaning)}" data-eid="{esc(eid)}">'
            f'<p class="stem">Recall this atom’s wording.</p>'
            f'<input type="text" class="cloze-in" autocomplete="off" aria-label="Your recall">'
            f'<div class="check-actions"><button type="submit">Check</button></div>'
            f'<p class="feedback" hidden></p>'
            f'<p class="reveal" hidden>{esc(meaning)}</p>'
            f"</form>"
        )
    reveal = esc(chk["sentence"])
    src_note = (
        f'<p class="check-note">Key is this atom '
        f'(<span class="mono">{esc(chk["key_atom_id"])}</span>). '
        f'Distractors, if any, are sibling atoms in this store. '
        f'Shape <span class="mono">{esc(chk["shape"])}</span> — '
        f'not authored <span class="mono">content.text</span>.</p>'
    )
    if chk["shape"] == "mcq_siblings":
        choices = stable_rotate(list(chk["choices"]), eid)
        labels = []
        for c in choices:
            val = "key" if c["correct"] else "d:" + c["from_atom_id"]
            labels.append(
                f'<label class="choice">'
                f'<input type="radio" name="{esc(eid)}" value="{esc(val)}">'
                f'<span>{esc(c["text"])}</span>'
                f"</label>"
            )
        return (
            f'<form class="check" data-shape="mcq_siblings" data-key="key" data-eid="{esc(eid)}">'
            f'<p class="stem">{esc(chk["stem"])}</p>'
            f'{"".join(labels)}'
            f'<div class="check-actions"><button type="submit">Check</button></div>'
            f'<p class="feedback" hidden></p>'
            f'<p class="reveal" hidden>{reveal}</p>'
            f"{src_note}"
            f"</form>"
        )
    # cloze
    lead = esc(chk.get("cloze_lead") or "")
    tail = esc(chk.get("cloze_tail") or "")
    stem = chk["stem"]
    if chk.get("cloze_lead") is not None and "______" in stem:
        stem_html = f"{lead}<span class=\"blank\">______</span>{tail}".rstrip(".")
        if stem.endswith("."):
            stem_html += "."
        stem_block = f'<p class="stem">{stem_html}</p>'
    else:
        stem_block = f'<p class="stem">{esc(stem)}</p>'
    return (
        f'<form class="check" data-shape="cloze" data-key="{esc(chk["key"])}" data-eid="{esc(eid)}">'
        f"{stem_block}"
        f'<input type="text" class="cloze-in" autocomplete="off" aria-label="Your recall">'
        f'<div class="check-actions"><button type="submit">Check</button></div>'
        f'<p class="feedback" hidden></p>'
        f'<p class="reveal" hidden>{reveal}</p>'
        f"{src_note}"
        f"</form>"
    )


def project_html(atoms, elements, manifest, out_path: pathlib.Path, *, meaning_atoms=None):
    """Write the short lesson (spine) and the full SOP dump (coverage).

    `atoms` is the SOP tree (coverage walk / spine SOP membership).
    `meaning_atoms` is an optional join catalog (instance citations) so
    composed_from can resolve across stores without copying into SOP atoms.json.
    """
    catalog = list(atoms)
    if meaning_atoms:
        seen = {a["atom_id"] for a in catalog}
        for a in meaning_atoms:
            if a.get("atom_id") and a["atom_id"] not in seen:
                catalog.append(a)
    by_atom = {a["atom_id"]: a for a in catalog}
    esc = html.escape
    cart = manifest.get("cartographer") or {}
    counts = cart.get("move_counts") or move_counts(elements)
    mixed = len([k for k in counts if k != "?"]) > 1
    cf_counts = Counter(e["composed_from"] for e in elements)
    spine = apply_spine(manifest, atoms, elements)
    coverage_path = sibling_coverage_path(out_path)
    lesson_href = esc(out_path.name)
    coverage_href = esc(coverage_path.name)
    by_cf = defaultdict(list)
    for e in elements:
        by_cf[e["composed_from"]].append(e)
    extra_n = sum(1 for e in elements if is_extra_element(e))

    def occs_for(atom_id):
        occs = list(by_cf.get(atom_id) or [])
        occs.sort(key=lambda e: (0 if is_primary_element(e) else 1, e["element_id"]))
        return occs

    def pills_for(el):
        intent = el.get("intent") or {}
        expr = el.get("expression") or {}
        move = intent.get("move", DEFAULT_MOVE)
        low = (el.get("ext") or {}).get("cartographer", {}).get("confidence") == "low"
        extra = is_extra_element(el)
        instance = bool((el.get("ext") or {}).get("realized_from", {}).get("instance_store"))
        out = [f'<span class="pill move-{esc(move)}{ " low" if low else ""}">{esc(move)}</span>']
        if extra:
            out.append('<span class="pill extra-occ">extra</span>')
        if instance:
            out.append('<span class="pill instance-occ">instance</span>')
        if is_check_occurrence(el):
            out.append('<span class="pill check-occ">check</span>')
        tp = expr.get("text_primitive")
        if tp:
            out.append(f'<span class="pill primitive" title="expression.text_primitive">{esc(tp)}</span>')
        if expr.get("style_ref"):
            out.append(f'<span class="pill style" title="expression.style_ref">{esc(expr["style_ref"])}</span>')
        for oid in intent.get("teaches") or []:
            short = oid[4:] if oid.startswith("obj_") else oid
            out.append(f'<span class="pill teaches" title="{esc(oid)}">{esc(short)}</span>')
        if low:
            out.append('<span class="pill dim">low-conf</span>')
        return "".join(out)

    def card_html(el, atom, extra_cls):
        meaning = clean_meaning(atom["meaning"]["source_text"])
        kind = atom["meaning"].get("kind", "")
        sh = (el.get("source_hash") or "")[:19]
        expr = el.get("expression") or {}
        clothes = CLOTHES_CLASS.get(expr.get("style_ref"), "")
        clothes_cls = f" {clothes}" if clothes else ""
        prim = primitive_class(el)
        prim_cls = f" {prim}" if prim else ""
        kicker = KICKER.get(expr.get("content_role"), "")
        if expr.get("text_primitive") == PRIMITIVE_CALLOUT:
            kicker = KICKER.get("callout", "Why this")
        kicker_html = f'<div class="kicker">{esc(kicker)}</div>' if kicker else ""
        meaning_tag = "h2" if expr.get("text_primitive") == PRIMITIVE_HEADING else "p"
        tp = expr.get("text_primitive") or ""
        hint = expr.get("layout_hint") or ""
        join_bits = [
            f'composed_from <span class="mono">{esc(el["composed_from"])}</span>',
            f'source_hash <span class="mono">{esc(sh)}…</span>',
        ]
        if expr:
            join_bits.append(
                f'primitive <span class="mono">{esc(tp)}</span> · '
                f'clothes <span class="mono">{esc(expr.get("style_ref", ""))}'
                f' · {esc(expr.get("content_role", ""))}'
                f' · {esc(hint)}</span>'
            )
        if is_check_occurrence(el):
            chk = derive_check(atom, atoms)
            if chk:
                join_bits.append(
                    f'check <span class="mono">{esc(chk["shape"])}</span> · '
                    f'key from this atom · distractors from siblings'
                )
            body = check_body_html(el, atom, atoms, esc)
        else:
            body = f'<{meaning_tag} class="meaning">{esc(meaning)}</{meaning_tag}>'
        return (
            f'<article class="occ{extra_cls}{clothes_cls}{prim_cls}">'
            f'{kicker_html}'
            f'<div class="meta">'
            f'<span class="id">{esc(el["element_id"])}</span>'
            f'{pills_for(el)}'
            f'<span class="pill dim">{esc(el["type"])}</span>'
            f'<span class="pill dim">{esc(kind)}</span>'
            f'</div>'
            f'{body}'
            f'<div class="join">{" · ".join(join_bits)}</div>'
            f'</article>'
        )

    def step_item_html(el, atom):
        meaning = clean_meaning(atom["meaning"]["source_text"])
        sh = (el.get("source_hash") or "")[:19]
        expr = el.get("expression") or {}
        tp = expr.get("text_primitive") or ""
        join = (
            f'composed_from <span class="mono">{esc(el["composed_from"])}</span>'
            f' · source_hash <span class="mono">{esc(sh)}…</span>'
            f' · primitive <span class="mono">{esc(tp)}</span>'
        )
        return (
            f'<li class="step" data-eid="{esc(el["element_id"])}">'
            f'<div class="meta">'
            f'<span class="id">{esc(el["element_id"])}</span>'
            f'{pills_for(el)}'
            f'</div>'
            f'<p class="meaning">{esc(meaning)}</p>'
            f'<div class="join">{join}</div>'
            f'</li>'
        )

    def job_aid_block_html(step_els):
        title = job_aid_title(step_els[0], by_atom)
        title_html = f'<h2 class="job-title">{esc(title)}</h2>' if title else ""
        items = []
        for el in step_els:
            items.append(step_item_html(el, by_atom[el["composed_from"]]))
        return (
            f'<section class="prim prim-step job-aid">'
            f'<div class="kicker">Job aid</div>'
            f'{title_html}'
            f'<ol class="steps">{"".join(items)}</ol>'
            f'<p class="join">primitive <span class="mono">{esc(PRIMITIVE_STEP)}</span> · '
            f'{len(step_els)} steps · meaning from each atom via '
            f'<span class="mono">composed_from</span> · not authored '
            f'<span class="mono">content.text</span></p>'
            f'</section>'
        )

    def walk(atom, depth, acc):
        occs = occs_for(atom["atom_id"])
        if not occs:
            raise SystemExit(f"no occurrence for atom {atom['atom_id']}")
        if len(occs) > 1:
            moves = " + ".join((o.get("intent") or {}).get("move", "?") for o in occs)
            acc.append(
                f'<section class="pair d{depth}">'
                f'<div class="pair-label">1:many pair · same atom · {len(occs)} occurrences · '
                f'composed_from <span class="mono">{esc(atom["atom_id"])}</span> · '
                f'moves <span class="mono">{esc(moves)}</span></div>'
            )
            for el in occs:
                extra_cls = " extra" if is_extra_element(el) else ""
                acc.append(card_html(el, atom, extra_cls))
            acc.append("</section>")
        else:
            acc.append(card_html(occs[0], atom, f" d{depth}"))
        for ch in kids(atoms, atom["atom_id"]):
            walk(ch, depth + 1, acc)

    body = []
    for r in roots(atoms):
        walk(r, 0, body)

    by_eid = {e["element_id"]: e for e in elements}
    spine_ids = list(spine.get("element_ids") or [])
    spine_body = []
    for kind, els in group_spine_for_project(spine_ids, by_eid):
        if kind == "job_aid":
            spine_body.append(job_aid_block_html(els))
            continue
        el = els[0]
        atom = by_atom[el["composed_from"]]
        extra_cls = " extra" if is_extra_element(el) else ""
        spine_body.append(card_html(el, atom, extra_cls))
    spine_rows = []
    for n, eid in enumerate(spine_ids, 1):
        el = by_eid.get(eid)
        if el is None:
            continue
        a = by_atom[el["composed_from"]]
        teaches = ", ".join((el.get("intent") or {}).get("teaches") or []) or "—"
        look = (el.get("expression") or {}).get("style_ref") or "—"
        prim = (el.get("expression") or {}).get("text_primitive") or "—"
        spine_rows.append(
            f"<tr><td>{n}</td>"
            f"<td class=mono>{esc(el['element_id'])}</td>"
            f"<td class=mono>{esc(el['composed_from'])}</td>"
            f"<td>{esc((el.get('intent') or {}).get('move', ''))}</td>"
            f"<td class=mono>{esc(prim)}</td>"
            f"<td class=mono>{esc(look)}</td>"
            f"<td class=mono>{esc(teaches)}</td>"
            f"<td>{esc(a['meaning'].get('kind', ''))}</td></tr>"
        )

    rows = []
    for el in elements:
        a = by_atom[el["composed_from"]]
        teaches = ", ".join((el.get("intent") or {}).get("teaches") or []) or "—"
        pair = cf_counts[el["composed_from"]] > 1
        row_cls = " class=pair-row" if pair else ""
        many = "1:many" if pair else "1:1"
        look = (el.get("expression") or {}).get("style_ref") or "—"
        rows.append(
            f"<tr{row_cls}><td class=mono>{esc(el['element_id'])}</td>"
            f"<td class=mono>{esc(el['composed_from'])}</td>"
            f"<td>{esc((el.get('intent') or {}).get('move', ''))}</td>"
            f"<td class=mono>{esc(look)}</td>"
            f"<td class=mono>{esc(teaches)}</td>"
            f"<td>{esc(el['type'])}</td>"
            f"<td>{esc(a['meaning'].get('kind', ''))}</td>"
            f"<td>{many}</td></tr>"
        )

    rf = manifest.get("realized_from") or {}
    otm = manifest.get("one_to_many") or {}
    cout = manifest.get("couturier") or {}
    count_bits = " · ".join(f"{esc(k)} {v}" for k, v in sorted(counts.items()))
    look_counts = cout.get("look_counts") or {}
    look_bits = " · ".join(f"{esc(k)} {v}" for k, v in sorted(look_counts.items()))
    check_n = sum(1 for e in elements if is_check_occurrence(e))
    pair_n = sum(1 for n in cf_counts.values() if n > 1)
    extras_bit = (f" · {extra_n} extra" + ("s" if extra_n != 1 else "")
                  + f" on {otm.get('seeded_atom_count', pair_n)} atoms"
                  + (f" · {check_n} check" + ("s" if check_n != 1 else "") if check_n else "")
                  if extra_n else "")
    many_note = (
        f" {pair_n} atom"
        + ("s" if pair_n != 1 else "")
        + " carry a second <span class=mono>ele_</span> (same "
        f"<span class=mono>composed_from</span>, distinct <span class=mono>move</span>). "
        if extra_n else
        " Later 1:many can mint additional elements without changing atom ids. "
    )
    check_note = (
        " Extra <span class=mono>reinforce</span> occurrences render as a check "
        "(stem + choices or cloze) derived from the atom — not an italic reprint. "
        if check_n else ""
    )
    clothes_note = (
        " Couturier dressed each occurrence from its <span class=mono>move</span> "
        "(<span class=mono>style_ref</span>) — "
        "hook vs present vs reinforce must not look like the same card. "
        if cout else
        " Couturier (style keys) is the next hop so different moves look like different clothes. "
    )
    prim_manifest = manifest.get("primitives") or {}
    prim_counts = prim_manifest.get("counts") or primitive_counts(elements)
    prim_bits = " · ".join(f"{esc(k)} {v}" for k, v in sorted(prim_counts.items()))
    primitives_note = (
        " Realizer bound a closed compiler primitive "
        "(<span class=mono>text_primitive</span>: heading / body / step / callout / check) "
        "from atom kind + occurrence move. The short lesson renders those primitives — "
        "why-this as a <span class=mono>tp_callout</span> of purpose, "
        "Procedure A as a job-aid step list, a worked example as body/`exemplify` "
        "clothes (instance atom via composed_from), front-matter as heading/body, "
        "reinforce as the existing check. Coverage stays card-like. "
        if prim_counts else
        " The atom → primitives hop is owed so beats are clothes, not SOP cards. "
    )
    spine_note = (
        f" Default HTML is the short lesson spine "
        f"(<span class=mono>{esc(spine.get('policy', SPINE_POLICY))}</span>): "
        f"{spine.get('count', 0)} of {len(elements)} occurrences — document-root opening, "
        "why-this callout of purpose, teachable front-matter primaries, Procedure A as "
        "a job sequence, a small instance example, then the existing checks. The object "
        "tree walk is coverage, not the path. "
    )
    if cout:
        ctrl_doc = "Couturier v1"
        ctrl_sub = f'{esc(manifest.get("project", ""))} · occurrence style bound'
        ctrl_meta = (f"{len(elements)} occurrences{extras_bit} · {look_bits or count_bits}<br>"
                     f"policy {esc(cout.get('policy', ''))}")
        banner = (
            "<b>Meaning lives on the atom.</b> Clothes come from <span class=mono>element.expression</span> "
            "(Couturier). Intent (<span class=mono>move</span>, <span class=mono>teaches</span>) is "
            "Cartographer’s. The Realizer minted the <span class=mono>ele_</span> ids and copied no authored "
            f"<span class=mono>content.text</span>.{many_note}{check_note}{clothes_note}{primitives_note}{spine_note}"
            "Dragoman / Storyline / PNG render are not this hop."
        )
        projector = (f"{esc(REALIZER)} + {esc(cart.get('tool', 'tools/cartographer.py'))} + "
                     f"{esc(cout.get('tool', 'tools/couturier.py'))}")
    elif cart:
        ctrl_doc = "Cartographer v1"
        ctrl_sub = f'{esc(manifest.get("project", ""))} · occurrence intent bound'
        ctrl_meta = (f"{len(elements)} occurrences{extras_bit} · {count_bits}<br>"
                     f"policy {esc(cart.get('policy', ''))}")
        banner = (
            "<b>Meaning lives on the atom.</b> Occurrence intent "
            "(<span class=mono>move</span>, <span class=mono>teaches</span>) is Cartographer’s. "
            "v1 is a documented heuristic compiler, not ID genius — low-confidence pills are flagged. "
            "The Realizer minted the <span class=mono>ele_</span> ids and copied no authored "
            f"<span class=mono>content.text</span>.{many_note}{check_note}{clothes_note}{primitives_note}{spine_note}"
            "Dragoman / PNG render are not this hop."
        )
        projector = f"{esc(REALIZER)} + {esc(cart.get('tool', 'tools/cartographer.py'))}"
    else:
        ctrl_doc = "Realizer v1"
        ctrl_sub = f'{esc(manifest.get("project", ""))} · occurrence hop'
        ctrl_meta = (f"{len(elements)} occurrences{extras_bit} · default move "
                     f"<b>{esc(manifest.get('default_move', DEFAULT_MOVE))}</b><br>"
                     f"policy {esc(manifest.get('policy', POLICY))}")
        banner = (
            "<b>Meaning lives on the atom.</b> Each card is one occurrence "
            "(<span class=mono>ele_</span>), linked by <span class=mono>composed_from</span>. "
            "The Realizer copied no authored <span class=mono>content.text</span>. Ugly typography "
            f"is v1.{many_note}{check_note}{clothes_note}{primitives_note}{spine_note}"
            "Dragoman / PNG render are not this hop."
        )
        projector = esc(REALIZER)

    STYLE = """
:root{--ink:#0f172a;--mut:#64748b;--line:#e2e8f0;--bg:#f8fafc;--accent:#1e3a8a}
*{box-sizing:border-box}
body{font:15px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);
 margin:0;background:var(--bg)}
.page{max-width:920px;margin:0 auto;background:#fff;padding:40px 48px;
 box-shadow:0 1px 3px rgba(0,0,0,.08)}
.ctrl{display:flex;justify-content:space-between;align-items:flex-start;
 border-bottom:2px solid var(--accent);padding-bottom:14px;margin-bottom:8px}
.ctrl .doc{font-weight:700;font-size:19px;color:var(--accent)}
.ctrl .meta{text-align:right;font-size:12.5px;color:var(--mut)}
.banner{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:10px 14px;
 font-size:12.5px;color:#1e3a8a;margin:14px 0 22px}
h1{font-size:20px;margin:8px 0 4px}
.nav{font-size:13px;margin:6px 0 10px}
.nav a{color:var(--accent)}
.path{font-size:12.5px;color:var(--mut);margin:0 0 14px}
.occ{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:8px 0}
.d1{margin-left:18px}.d2{margin-left:36px}.d3{margin-left:54px}.d4{margin-left:72px}
.occ .meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:6px}
.id{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;font-weight:600}
.pill{background:#1e3a8a;color:#fff;border-radius:999px;padding:1px 8px;font-size:11px;
 text-transform:uppercase;letter-spacing:.03em}
.pill.dim{background:#e2e8f0;color:#334155}
.pill.teaches{background:#e0e7ff;color:#3730a3;text-transform:none;letter-spacing:0}
.pill.low{box-shadow:0 0 0 2px #f59e0b inset}
.pill.move-hook{background:#b45309}
.pill.move-objective{background:#047857}
.pill.move-activate{background:#0f766e}
.pill.move-present{background:#1e3a8a}
.pill.move-exemplify{background:#6d28d9}
.pill.move-practice{background:#be123c}
.pill.move-feedback{background:#9f1239}
.pill.move-assess{background:#7f1d1d}
.pill.move-reinforce{background:#334155}
.pill.move-transfer{background:#c2410c}
.pill.extra-occ{background:#0f766e;text-transform:none}
.pill.instance-occ{background:#6d28d9;text-transform:none}
.pill.check-occ{background:#1e3a8a;text-transform:none}
.pair{border:2px solid #1e3a8a;border-radius:10px;padding:10px 12px 6px;margin:12px 0;
 background:#f1f5f9}
.pair-label{font-size:12px;color:#1e3a8a;font-weight:600;margin:0 0 8px}
.pair .occ{background:#fff}
.occ.extra{background:#fffbeb;border-color:#f59e0b}
.pill.style{background:#fef3c7;color:#92400e;text-transform:none;letter-spacing:0}
.pill.primitive{background:#e0e7ff;color:#3730a3;text-transform:none;letter-spacing:0}
.kicker{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
 margin:0 0 8px;color:inherit;opacity:.85}
.occ.style-opening{background:linear-gradient(135deg,#b45309,#d97706);color:#fff;border:none;
 border-radius:4px;padding:28px 24px 22px;text-align:center}
.occ.style-opening .id,.occ.style-opening .join,.occ.style-opening .pill.dim{color:#fde68a}
.occ.style-opening .meaning{font-size:22px;font-weight:700;line-height:1.25;letter-spacing:-.02em;
 margin:8px 0 10px}
.occ.style-opening .kicker{color:#fffbeb;opacity:1}
.occ.style-instructional{background:#fff;border:1px solid #cbd5e1;border-left:5px solid #1e3a8a;
 border-radius:6px;padding:14px 16px}
.occ.style-instructional .meaning{font-size:15px;line-height:1.55}
.occ.style-recall{background:#f1f5f9;border:2px solid #334155;border-radius:6px;padding:16px 18px}
.occ.style-recall .kicker{color:#1e293b;opacity:1}
.occ.style-recall form.check .stem{font-size:16px;font-weight:650;font-style:normal;margin:8px 0 12px;color:var(--ink)}
.occ.style-recall form.check .blank{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
 letter-spacing:.12em;color:#334155}
form.check .choice{display:flex;gap:10px;align-items:flex-start;margin:8px 0;padding:10px 12px;
 border:1px solid var(--line);border-radius:6px;background:#fff;cursor:pointer}
form.check .choice:hover{border-color:#334155}
form.check .choice span{flex:1}
form.check .cloze-in{width:100%;font:inherit;padding:8px 10px;border:1px solid #94a3b8;border-radius:6px}
form.check .check-actions{margin:12px 0 6px}
form.check button{background:#1e3a8a;color:#fff;border:0;border-radius:6px;padding:8px 14px;
 font:inherit;font-weight:600;cursor:pointer}
form.check .feedback{font-size:13px;margin:8px 0 0}
form.check .feedback.ok{color:#047857;font-weight:650}
form.check .feedback.no{color:#9f1239;font-weight:650}
form.check .reveal{margin:10px 0 0;padding:8px 10px;background:#fff;border-left:3px solid #1e3a8a;
 font-size:13.5px}
form.check .check-note{font-size:11.5px;color:var(--mut);margin:10px 0 0}
.occ.style-purpose{background:#ecfdf5;border:1px solid #059669;border-left:6px solid #047857;
 border-radius:6px}
.occ.style-purpose .meaning{font-weight:600}
.occ.style-purpose .kicker{color:#047857}
.occ.style-prior,.occ.prim-callout{background:#f0fdfa;border:1px solid #0f766e;
 border-left:6px solid #0f766e;border-radius:6px;padding:14px 16px 12px;font-size:14.5px}
.occ.style-prior .kicker,.occ.prim-callout .kicker{color:#0f766e;opacity:1}
.occ.prim-callout .meaning{font-size:15.5px;line-height:1.45;margin:4px 0 8px}
.occ.style-example{background:#faf5ff;border:1px solid #c4b5fd;border-radius:6px;padding:12px 14px 12px 18px}
.occ.style-example .meaning{font-family:Georgia,Times,serif;font-size:14px}
.occ.style-example .kicker{color:#6d28d9}
.occ.style-job{background:#fff7ed;border:1px solid #c2410c;border-left:6px solid #c2410c;border-radius:6px}
.occ.style-job .kicker{color:#c2410c}
.job-aid{border:2px solid #1e3a8a;border-radius:8px;padding:16px 18px 10px;margin:16px 0;
 background:#fff}
.job-aid .kicker{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
 color:#1e3a8a;margin:0 0 6px}
.job-aid .job-title{font-size:18px;margin:0 0 12px;letter-spacing:-.02em}
.job-aid ol.steps{margin:0;padding:0;list-style:none;counter-reset:step}
.job-aid li.step{display:grid;grid-template-columns:2.4rem 1fr;gap:10px;padding:12px 0;
 border-top:1px solid var(--line);counter-increment:step}
.job-aid li.step::before{content:counter(step);font-weight:700;color:#1e3a8a;font-size:20px;
 line-height:1.2}
.job-aid li.step .meta{grid-column:2;display:flex;flex-wrap:wrap;gap:6px;align-items:center;
 margin:0 0 4px}
.job-aid li.step .meaning{grid-column:2;margin:0 0 4px;font-size:15.5px;line-height:1.45}
.job-aid li.step .join{grid-column:2}
.job-aid > .join{margin:10px 0 4px}
.occ.prim-heading .meaning,.occ.prim-body .meaning{margin:4px 0 6px}
tr.pair-row td{background:#eff6ff}
.meaning{margin:4px 0 6px}
.join{font-size:12px;color:var(--mut)}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:12.5px}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:#f1f5f9;font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:#475569}
details{margin-top:28px;border-top:1px dashed var(--line);padding-top:14px}
summary{cursor:pointer;color:var(--mut);font-size:12.5px}
.foot{margin-top:28px;font-size:11.5px;color:var(--mut);border-top:1px solid var(--line);
 padding-top:12px}
""".strip()

    SCRIPT = r"""
(function () {
  function norm(s) {
    return (s || "").replace(/\s+/g, " ").trim().toLowerCase();
  }
  document.querySelectorAll("form.check").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fb = form.querySelector(".feedback");
      var reveal = form.querySelector(".reveal");
      var shape = form.getAttribute("data-shape");
      var key = form.getAttribute("data-key");
      var ok = false;
      if (shape === "mcq_siblings") {
        var picked = form.querySelector("input[type=radio]:checked");
        if (!picked) {
          fb.hidden = false;
          fb.className = "feedback";
          fb.textContent = "Pick an answer to check.";
          return;
        }
        ok = picked.value === "key";
      } else {
        var typed = form.querySelector("input[type=text]");
        ok = typed && norm(typed.value) === norm(key);
      }
      fb.hidden = false;
      fb.className = "feedback " + (ok ? "ok" : "no");
      fb.textContent = ok
        ? "Correct — that wording is this atom."
        : "Not yet. Distractors (if any) are sibling atoms in this store; the key is this atom’s own wording.";
      if (reveal) reveal.hidden = false;
    });
  });
})();
""".strip()

    foot_common = (
        f"Atom store: {esc(str(rf.get('atom_store', '')))} · "
        f"atoms_sha256 {esc(str(rf.get('atoms_sha256', ''))[:19])}…<br>"
        f"Projector: {projector} · this HTML is regenerated, never hand-edited. "
        "Meaning is read from atoms.json. Occurrence intent is Cartographer’s when bound. "
        "Clothes are Couturier’s when bound (expression keys, not authored text). "
        f"{'Moves are mixed.' if mixed else 'All moves still share one value — run tools/cartographer.py.'}"
        f"{' 1:many pairs share composed_from.' if extra_n else ''}"
        f"{' Clothes are mixed.' if cout and len(look_counts) > 1 else (' Run tools/couturier.py to dress occurrences.' if not cout else '')}"
        f"{' Extra reinforce occurrences project as a check from the atom (agents/realizer/check_v1.md).' if check_n else ''} "
        f"{' Compiler primitives: ' + prim_bits + '.' if prim_bits else ''} "
        f"Spine heuristic: <span class=mono>{esc(SPINE_SPEC)}</span>."
    )

    def render_page(page_title, heading, nav, path_line, main, details_html):
        return (
            "<!doctype html><html lang=en><head><meta charset=utf-8>"
            "<meta name=viewport content=\"width=device-width,initial-scale=1\">"
            f"<title>{page_title}</title>"
            f"<style>{STYLE}</style></head><body><div class=page>"
            "<div class=ctrl>"
            f" <div><div class=doc>{ctrl_doc}</div>"
            f" <div style=\"font-size:12.5px;color:var(--mut)\">{ctrl_sub}</div></div>"
            f" <div class=meta>{ctrl_meta}</div>"
            "</div>"
            f"<h1>{heading}</h1>"
            f'<p class="nav">{nav}</p>'
            f'<p class="path">{path_line}</p>'
            f"<div class=banner>{banner}</div>"
            f"{main}"
            f"{details_html}"
            f"<div class=foot>{foot_common}</div>"
            f"</div><script>{SCRIPT}</script></body></html>"
        )

    project_name = esc(manifest.get("project", "course"))
    spine_n = spine.get("count", 0)
    store_n = len(elements)
    lesson_details = (
        f"<details open><summary>Spine membership — {spine_n} ele_ records "
        f"(heuristic <span class=mono>{esc(SPINE_POLICY)}</span>)</summary>"
        "<table><thead><tr><th>#</th><th>element_id</th><th>composed_from</th>"
        "<th>move</th><th>primitive</th><th>style_ref</th><th>teaches</th><th>atom kind</th></tr></thead>"
        f"<tbody>{''.join(spine_rows)}</tbody></table></details>"
    )
    coverage_details = (
        f"<details><summary>Occurrence index — {store_n} ele_ records (click to expand)</summary>"
        "<table><thead><tr><th>element_id</th><th>composed_from</th><th>move</th>"
        "<th>style_ref</th><th>teaches</th><th>type</th><th>atom kind</th><th>arity</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></details>"
    )
    lesson_html = render_page(
        f"Short lesson — {project_name}",
        "Short lesson",
        f'<a href="{coverage_href}">Full SOP / coverage ({store_n} occurrences)</a>',
        (f"{spine_n} of {store_n} occurrences · why-this callout of purpose, "
         "front-matter as heading/body, Procedure A as a job-aid step sequence, "
         "then a worked example from the instance store, then the existing checks. "
         "Not B/C and not the SOP dump. Heuristic is documented, not an LLM."),
        "".join(spine_body),
        lesson_details,
    )
    coverage_html = render_page(
        f"Coverage dump — {project_name}",
        "Full SOP / coverage",
        f'<a href="{lesson_href}">Short lesson (spine)</a>',
        (f"Every occurrence in document order ({store_n} ele_ records). "
         "This is coverage, not the course. The short path is the other file."),
        "".join(body),
        coverage_details,
    )
    out_path.write_text(lesson_html)
    coverage_path.write_text(coverage_html)
    return coverage_path


def selftest(closed_moves):
    """Tiny fixture: extra ids are stable, 1:many shares composed_from, re-run keeps extras."""
    results = []

    def atom(aid, kind, text, parent=None, order=0):
        a = {
            "atom_id": aid,
            "content_hash": "sha256:" + ("a" * 64),
            "meaning": {"source_locale": "en", "source_text": text, "kind": kind},
            "bindings": {},
            "governance": {"version": 1, "status": "draft"},
        }
        if parent:
            a["bindings"]["object"] = {"belongs_to": parent, "order": order}
        return a

    title = atom("atom_sop_x", "procedure", "SOP-X — Do the thing.")
    general = atom("atom_sop_x_general", "procedure", "X is the framework.", "atom_sop_x", 0)
    other = atom("atom_sop_x_other", "procedure", "A 1:1 leftover.", "atom_sop_x", 1)

    primary = mint_element(title, DEFAULT_MOVE, role="primary")
    extra = mint_element(title, "reinforce", role="extra")
    results.append(("primary id is ele_ + suffix",
                    primary["element_id"] == "ele_sop_x", primary["element_id"]))
    results.append(("extra id is primary + __move",
                    extra["element_id"] == "ele_sop_x__reinforce", extra["element_id"]))
    results.append(("same composed_from", extra["composed_from"] == primary["composed_from"] == "atom_sop_x",
                    extra["composed_from"]))
    results.append(("distinct moves", extra["intent"]["move"] != primary["intent"]["move"]
                    and extra["intent"]["move"] == "reinforce", extra["intent"]["move"]))
    results.append(("no authored content on extra", "content" not in extra, ""))
    results.append(("extra role stamped", extra["ext"]["realized_from"]["role"] == "extra", ""))
    results.append(("reinforce is closed vocab", extra["intent"]["move"] in closed_moves, extra["intent"]["move"]))

    # assemble with a local seed override via previous extras + seed atoms that exist
    orig_seed = ONE_TO_MANY_SEED
    try:
        # Can't mutate the tuple in place; assemble reads the module-level seed.
        # Drive extras via a previous extra + seed atoms that match the real seed ids? Those
        # atoms are not in this fixture. Instead, plant a previous extra and rely on preserve.
        prev_extra = mint_element(general, "reinforce", role="extra")
        prev_primary_g = mint_element(general, DEFAULT_MOVE, role="primary")
        previous = [primary, extra, prev_primary_g, prev_extra]
        assembled = assemble_elements([title, general, other], previous, DEFAULT_MOVE, mint_extras=False)
        ids = [e["element_id"] for e in assembled]
        results.append(("re-run without seed keeps planted extras",
                        "ele_sop_x__reinforce" in ids and "ele_sop_x_general__reinforce" in ids, ids))
        results.append(("1:1 atom stays singleton",
                        sum(1 for e in assembled if e["composed_from"] == "atom_sop_x_other") == 1, ""))
        results.append(("title has two occs",
                        sum(1 for e in assembled if e["composed_from"] == "atom_sop_x") == 2, ""))
        # Cartographer stamp survives re-realize
        extra["ext"]["cartographer"] = {"policy": "v1_heuristic_compiler", "tool": "tools/cartographer.py",
                                        "confidence": "high", "flags": ["extra_occurrence_move_preserved"]}
        extra["intent"]["teaches"] = ["obj_explain_alsap_purpose"]
        extra["intent"]["move"] = "reinforce"
        extra["expression"] = {
            "style_ref": "brand.recall",
            "text_primitive": "tp_recall",
            "content_role": "retrieval",
            "layout_hint": "check",
        }
        extra["ext"]["couturier"] = {
            "policy": "v1_move_to_look",
            "tool": "tools/couturier.py",
            "from_move": "reinforce",
        }
        assembled2 = assemble_elements([title, general, other], [primary, extra, prev_primary_g, prev_extra],
                                       DEFAULT_MOVE, mint_extras=False)
        kept = next(e for e in assembled2 if e["element_id"] == "ele_sop_x__reinforce")
        results.append(("re-realize preserves extra move", kept["intent"]["move"] == "reinforce",
                        kept["intent"].get("move")))
        results.append(("re-realize preserves extra teaches",
                        kept["intent"].get("teaches") == ["obj_explain_alsap_purpose"],
                        kept["intent"].get("teaches")))
        results.append(("re-realize preserves cartographer stamp",
                        "cartographer" in kept.get("ext", {}), ""))
        results.append(("re-realize preserves couturier stamp",
                        "couturier" in kept.get("ext", {}), ""))
        results.append(("re-realize preserves expression style_ref",
                        (kept.get("expression") or {}).get("style_ref") == "brand.recall",
                        (kept.get("expression") or {}).get("style_ref")))
        results.append(("ids stable across re-run",
                        {e["element_id"] for e in assembled} == {e["element_id"] for e in assembled2}, ""))
        results.append(("re-realize preserves layout_hint check",
                        (kept.get("expression") or {}).get("layout_hint") == "check",
                        (kept.get("expression") or {}).get("layout_hint")))
    finally:
        assert ONE_TO_MANY_SEED is orig_seed

    # Honesty bar: check is derived from this atom; distractors from siblings.
    general_live = atom(
        "atom_sop_ast29080_general", "procedure",
        "The ALSAP is the central cross-functional framework for ongoing identification, "
        "evaluation, and communication of emerging safety risks at the asset level. "
        "Only one ALSAP exists per asset.",
        "atom_sop_ast29080", 3,
    )
    purpose_live = atom(
        "atom_sop_ast29080_purpose", "procedure",
        "The purpose of this SOP is to define the process for planning, developing, executing, "
        "maintaining, and archiving the Asset Level Safety Assessment Plan (ALSAP) for use in "
        "asset-level safety monitoring during clinical development.",
        "atom_sop_ast29080", 0,
    )
    scope_live = atom(
        "atom_sop_ast29080_scope", "procedure",
        "This SOP applies to all Astellas and non-Astellas employees responsible for supporting "
        "ALSAP throughout its lifecycle. The in-scope organizations are listed below.",
        "atom_sop_ast29080", 1,
    )
    title_live = atom(
        "atom_sop_ast29080", "procedure",
        "SOP-AST-29080 — Plan, Develop, Execute, Maintain, and Archive the Asset Level Safety "
        "Assessment Plan (ALSAP).",
    )
    thin = atom("atom_sop_ast29080_roles", "procedure",
                "Roles and Responsibilities.", "atom_sop_ast29080", 4)
    definitions = atom(
        "atom_sop_ast29080_definitions", "procedure",
        "For definitions, refer to Vault Quality Glossary, or directly in Vault Quality.",
        "atom_sop_ast29080", 2,
    )
    procedures = atom("atom_sop_ast29080_procedures", "procedure",
                      "Procedures.", "atom_sop_ast29080", 5)
    proc_a = atom("atom_sop_ast29080_proc_a", "procedure",
                  "A. Plan Development of ALSAP.", "atom_sop_ast29080_procedures", 0)
    proc_b = atom("atom_sop_ast29080_proc_b", "procedure",
                  "B. Develop and Maintain ALSAP.", "atom_sop_ast29080_procedures", 1)
    step = atom(
        "atom_sop_ast29080_proc_a_s1", "procedure_step",
        "Notify a member of Safety Data Science in QSEG of the need for an ALSAP "
        "and request an ALSAP Lead.",
        "atom_sop_ast29080_proc_a", 0,
    )
    step2 = atom(
        "atom_sop_ast29080_proc_a_s2", "procedure_step",
        "Collaborate with SMT to identify contributing authors and reviewers for the ALSAP.",
        "atom_sop_ast29080_proc_a", 1,
    )
    step3 = atom(
        "atom_sop_ast29080_proc_a_s3", "procedure_step",
        "Schedule and conduct the ALSAP Kick-Off Meeting within 15 business days of "
        "ALSAP Lead assignment.",
        "atom_sop_ast29080_proc_a", 2,
    )
    step4 = atom(
        "atom_sop_ast29080_proc_a_s4", "procedure_step",
        "Collaborate with contributing authors and confirm alignment on section "
        "deliverables and target dates.",
        "atom_sop_ast29080_proc_a", 3,
    )
    step_b = atom(
        "atom_sop_ast29080_proc_b_s1", "procedure_step",
        "Provide the ALSAP Lead with contributions to the ALSAP within the agreed-upon timeframe.",
        "atom_sop_ast29080_proc_b", 0,
    )
    store = [title_live, purpose_live, scope_live, general_live, thin, definitions,
             procedures, proc_a, proc_b, step, step2, step3, step4, step_b]

    chk_g = derive_check(general_live, store)
    assert_check_honest(chk_g, general_live, store)
    results.append(("general check shape is mcq_siblings",
                    chk_g and chk_g["shape"] == "mcq_siblings", chk_g and chk_g.get("shape")))
    results.append(("general stem is question invert of this atom",
                    chk_g and chk_g["stem"] == "What is the ALSAP?", chk_g and chk_g.get("stem")))
    results.append(("general key is the complement in this atom",
                    chk_g and "central cross-functional framework" in chk_g["key"]
                    and phrase_in_atom(chk_g["key"], general_live), chk_g and chk_g.get("key")))
    d_from = sorted({c["from_atom_id"] for c in chk_g["choices"] if not c["correct"]}) if chk_g else []
    results.append(("general distractors are purpose + scope siblings",
                    d_from == ["atom_sop_ast29080_purpose", "atom_sop_ast29080_scope"], d_from))
    results.append(("roles heading is not a distractor",
                    chk_g and all(c["from_atom_id"] != "atom_sop_ast29080_roles" for c in chk_g["choices"]),
                    ""))
    results.append(("no authored content field on a check", "content" not in extra, ""))

    chk_p = derive_check(purpose_live, store)
    assert_check_honest(chk_p, purpose_live, store)
    results.append(("purpose check shape is mcq_siblings",
                    chk_p and chk_p["shape"] == "mcq_siblings", chk_p and chk_p.get("shape")))
    results.append(("purpose stem is question invert of this atom",
                    chk_p and chk_p["stem"] == "What is the purpose of this SOP?",
                    chk_p and chk_p.get("stem")))
    results.append(("purpose key is the complement in this atom",
                    chk_p and chk_p["key"].startswith("to define the process for planning")
                    and phrase_in_atom(chk_p["key"], purpose_live), chk_p and chk_p.get("key", "")[:40]))

    # Seed mints both reinforce extras when those atom ids are in the store.
    seeded = assemble_elements(store, [], DEFAULT_MOVE, mint_extras=True)
    seeded_ids = {e["element_id"] for e in seeded}
    results.append(("seed mints general reinforce extra",
                    "ele_sop_ast29080_general__reinforce" in seeded_ids, sorted(seeded_ids)))
    results.append(("seed mints purpose reinforce extra",
                    "ele_sop_ast29080_purpose__reinforce" in seeded_ids, ""))
    results.append(("seed mints purpose activate callout extra",
                    "ele_sop_ast29080_purpose__activate" in seeded_ids, ""))
    results.append(("purpose activate extra is activate not reinforce",
                    any(e["element_id"] == "ele_sop_ast29080_purpose__activate"
                        and e["intent"]["move"] == "activate" for e in seeded), ""))
    results.append(("title extra is present not reinforce",
                    any(e["element_id"] == "ele_sop_ast29080__present"
                        and e["intent"]["move"] == "present" for e in seeded), ""))
    results.append(("roles stay 1:1",
                    sum(1 for e in seeded if e["composed_from"] == "atom_sop_ast29080_roles") == 1, ""))

    # HTML: reinforce extra is a form the reader can attempt, not an italic reprint.
    # Lesson default is the short spine; coverage dump keeps the rest.
    import tempfile
    gen_extra = next(e for e in seeded if e["element_id"] == "ele_sop_ast29080_general__reinforce")
    gen_extra["expression"] = {
        "style_ref": "brand.recall",
        "text_primitive": "tp_recall",
        "content_role": "retrieval",
        "layout_hint": "check",
    }
    purp_extra = next(e for e in seeded if e["element_id"] == "ele_sop_ast29080_purpose__reinforce")
    purp_extra["expression"] = {
        "style_ref": "brand.recall",
        "text_primitive": "tp_recall",
        "content_role": "retrieval",
        "layout_hint": "check",
    }
    purp_callout = next(e for e in seeded if e["element_id"] == "ele_sop_ast29080_purpose__activate")
    purp_callout["expression"] = {
        "style_ref": "brand.prior",
        "text_primitive": "tp_callout",
        "content_role": "callout",
        "layout_hint": "callout",
    }
    want_spine = [
        "ele_sop_ast29080",
        "ele_sop_ast29080__present",
        "ele_sop_ast29080_purpose__activate",
        "ele_sop_ast29080_purpose",
        "ele_sop_ast29080_scope",
        "ele_sop_ast29080_general",
        "ele_sop_ast29080_proc_a_s1",
        "ele_sop_ast29080_proc_a_s2",
        "ele_sop_ast29080_proc_a_s3",
        "ele_sop_ast29080_proc_a_s4",
        "ele_sop_ast29080_purpose__reinforce",
        "ele_sop_ast29080_general__reinforce",
    ]
    got_spine = select_spine(store, seeded)
    results.append(("spine is the short ALSAP path", got_spine == want_spine, got_spine))
    results.append(("spine skips thin roles heading", "ele_sop_ast29080_roles" not in got_spine, ""))
    results.append(("spine skips glossary pointer", "ele_sop_ast29080_definitions" not in got_spine, ""))
    results.append(("spine skips thin procedures heading",
                    "ele_sop_ast29080_procedures" not in got_spine, ""))
    results.append(("spine skips thin A heading", "ele_sop_ast29080_proc_a" not in got_spine, ""))
    results.append(("spine includes all Procedure A real steps",
                    all(eid in got_spine for eid in (
                        "ele_sop_ast29080_proc_a_s1",
                        "ele_sop_ast29080_proc_a_s2",
                        "ele_sop_ast29080_proc_a_s3",
                        "ele_sop_ast29080_proc_a_s4",
                    )), got_spine))
    results.append(("spine A steps keep object.order",
                    got_spine.index("ele_sop_ast29080_proc_a_s1")
                    < got_spine.index("ele_sop_ast29080_proc_a_s2")
                    < got_spine.index("ele_sop_ast29080_proc_a_s3")
                    < got_spine.index("ele_sop_ast29080_proc_a_s4"), got_spine))
    results.append(("spine skips branch B",
                    "ele_sop_ast29080_proc_b_s1" not in got_spine, ""))
    results.append(("procedure A steps stay 1:1 (no extra reinforce)",
                    all(sum(1 for e in seeded if e["composed_from"] == aid) == 1
                        for aid in (
                            "atom_sop_ast29080_proc_a_s1",
                            "atom_sop_ast29080_proc_a_s2",
                            "atom_sop_ast29080_proc_a_s3",
                            "atom_sop_ast29080_proc_a_s4",
                        )),
                    ""))
    results.append(("procedure A steps have no copula invert — skip check",
                    all(not supports_honest_sibling_check(s, store)
                        for s in (step, step2, step3, step4)),
                    [copula_parts(first_sentence(s["meaning"]["source_text"]))
                     for s in (step, step2, step3, step4)]))
    results.append(("spine is a subset of existing ele_ ids", set(got_spine) <= seeded_ids, ""))
    mf_spine = {}
    apply_spine(mf_spine, store, seeded)
    apply_spine(mf_spine, store, seeded)
    results.append(("spine recompute is stable",
                    mf_spine["spine"]["element_ids"] == want_spine, mf_spine["spine"]["element_ids"]))

    # Compiler primitives from atom kind + occurrence move.
    results.append(("procedure_step present is tp_step",
                    classify_text_primitive(step, {"intent": {"move": "present"}}) == PRIMITIVE_STEP, ""))
    results.append(("procedure_step transfer is still tp_step (atom role wins)",
                    classify_text_primitive(step, {"intent": {"move": "transfer"}}) == PRIMITIVE_STEP, ""))
    results.append(("hook is heading tp_display",
                    classify_text_primitive(title_live, {"intent": {"move": "hook"}}) == PRIMITIVE_HEADING, ""))
    results.append(("reinforce is check tp_recall",
                    classify_text_primitive(general_live, {"intent": {"move": "reinforce"}}) == PRIMITIVE_CHECK, ""))
    results.append(("front-matter present is body tp_body",
                    classify_text_primitive(general_live, {"intent": {"move": "present"}}) == PRIMITIVE_BODY, ""))
    results.append(("activate is callout tp_callout",
                    classify_text_primitive(thin, {"intent": {"move": "activate"}}) == PRIMITIVE_CALLOUT, ""))
    results.append(("purpose atom + activate is tp_callout (why-this clothes)",
                    classify_text_primitive(purpose_live, {"intent": {"move": "activate"}}) == PRIMITIVE_CALLOUT, ""))
    results.append(("objective keeps tp_purpose",
                    classify_text_primitive(purpose_live, {"intent": {"move": "objective"}}) == PRIMITIVE_PURPOSE, ""))

    store_by_id = {a["atom_id"]: a for a in store}
    title_el = next(e for e in seeded if e["element_id"] == "ele_sop_ast29080")
    title_el["intent"]["move"] = "hook"
    refresh_text_primitives(seeded, store_by_id)
    results.append(("refresh binds heading on hook",
                    (title_el.get("expression") or {}).get("text_primitive") == PRIMITIVE_HEADING, ""))
    results.append(("refresh binds tp_step on all Procedure A presents",
                    all((next(e for e in seeded if e["element_id"] == eid).get("expression") or {})
                        .get("text_primitive") == PRIMITIVE_STEP
                        for eid in (
                            "ele_sop_ast29080_proc_a_s1",
                            "ele_sop_ast29080_proc_a_s2",
                            "ele_sop_ast29080_proc_a_s3",
                            "ele_sop_ast29080_proc_a_s4",
                        )), ""))
    results.append(("refresh binds tp_callout on purpose activate extra",
                    (next(e for e in seeded if e["element_id"] == "ele_sop_ast29080_purpose__activate")
                     .get("expression") or {}).get("text_primitive") == PRIMITIVE_CALLOUT, ""))
    results.append(("refresh does not author content.text",
                    all("content" not in e for e in seeded), ""))
    results.append(("job-aid title is the parent atom (thin A heading)",
                    job_aid_title(next(e for e in seeded if e["element_id"] == "ele_sop_ast29080_proc_a_s1"),
                                  store_by_id) == "A. Plan Development of ALSAP.", ""))

    with tempfile.TemporaryDirectory() as td:
        html_path = pathlib.Path(td) / "realized_lesson.html"
        cov_path = project_html(
            store, seeded, {"project": "selftest", "one_to_many": {"seeded_atom_count": 3}}, html_path
        )
        page = html_path.read_text()
        cov_page = pathlib.Path(cov_path).read_text()
    results.append(("HTML check form present for general reinforce",
                    'form class="check"' in page and "ele_sop_ast29080_general__reinforce" in page, ""))
    results.append(("HTML stem is the question invert", "What is the ALSAP?" in page, ""))
    results.append(("HTML does not italic-reprint the general paragraph as .meaning on the extra",
                    page.split("ele_sop_ast29080_general__reinforce", 1)[-1]
                    .split("</article>", 1)[0].count('class="meaning"') == 0, ""))
    results.append(("HTML kicker is Check not Remember",
                    ">Check</div>" in page and "Remember" not in page, ""))
    results.append(("HTML choices include sibling purpose sentence",
                    "The purpose of this SOP is to define the process" in page, ""))
    results.append(("HTML choices include sibling scope sentence",
                    "This SOP applies to all Astellas and non-Astellas employees" in page, ""))
    results.append(("closed vocab still has no retrieve on extras",
                    all((e.get("intent") or {}).get("move") != "retrieve" for e in seeded), ""))
    results.append(("lesson HTML is the spine not the dump",
                    "ele_sop_ast29080_roles" not in page
                    and '<span class="id">ele_sop_ast29080_proc_a_s1</span>' in page
                    and '<span class="id">ele_sop_ast29080_proc_a_s2</span>' in page
                    and '<span class="id">ele_sop_ast29080_proc_a_s3</span>' in page
                    and '<span class="id">ele_sop_ast29080_proc_a_s4</span>' in page
                    and '<span class="id">ele_sop_ast29080_proc_b_s1</span>' not in page
                    and '<span class="id">ele_sop_ast29080_procedures</span>' not in page
                    and '<span class="id">ele_sop_ast29080_proc_a</span>' not in page, ""))
    results.append(("lesson puts Procedure A sequence before the checks",
                    page.find("ele_sop_ast29080_proc_a_s1")
                    < page.find("ele_sop_ast29080_proc_a_s4")
                    < page.find("ele_sop_ast29080_purpose__reinforce"), ""))
    results.append(("lesson links to coverage",
                    "realized_coverage.html" in page and "Full SOP / coverage" in page, ""))
    results.append(("lesson has both existing checks (no new procedure check)",
                    page.count('form class="check"') == 2, page.count('form class="check"')))
    results.append(("coverage dump keeps roles and later steps",
                    "ele_sop_ast29080_roles" in cov_page
                    and "ele_sop_ast29080_proc_a_s1" in cov_page
                    and "ele_sop_ast29080_proc_a_s2" in cov_page
                    and "ele_sop_ast29080_proc_b_s1" in cov_page, ""))
    results.append(("coverage links back to the lesson", "realized_lesson.html" in cov_page, ""))
    results.append(("lesson groups Procedure A as one job-aid not four cards",
                    page.count('class="prim prim-step job-aid"') == 1
                    and page.count('<li class="step"') == 4
                    and "A. Plan Development of ALSAP." in page, page.count('<li class="step"')))
    results.append(("job-aid lists the four A step ids",
                    all(f'data-eid="{eid}"' in page for eid in (
                        "ele_sop_ast29080_proc_a_s1",
                        "ele_sop_ast29080_proc_a_s2",
                        "ele_sop_ast29080_proc_a_s3",
                        "ele_sop_ast29080_proc_a_s4",
                    )), ""))
    results.append(("job-aid meaning is from the atoms",
                    "Notify a member of Safety Data Science" in page
                    and "Collaborate with SMT to identify contributing authors" in page, ""))
    results.append(("hook occurrence carries heading primitive",
                    "prim-heading" in page and "tp_display" in page, ""))
    results.append(("front-matter body primitive is present",
                    "prim-body" in page and "tp_body" in page, ""))
    results.append(("spine includes purpose activate callout before purpose primary",
                    "ele_sop_ast29080_purpose__activate" in got_spine
                    and got_spine.index("ele_sop_ast29080_purpose__activate")
                    < got_spine.index("ele_sop_ast29080_purpose"), got_spine))
    results.append(("lesson HTML has why-this callout of the purpose atom",
                    "ele_sop_ast29080_purpose__activate" in page
                    and "Why this" in page
                    and "prim-callout" in page
                    and "tp_callout" in page, ""))
    results.append(("callout clothes the purpose atom meaning (not invented text)",
                    page.split("ele_sop_ast29080_purpose__activate", 1)[-1]
                    .split("</article>", 1)[0]
                    .find("The purpose of this SOP is to define the process") != -1, ""))
    results.append(("callout is not a third check",
                    page.count('form class="check"') == 2, page.count('form class="check"')))
    results.append(("coverage dump stays card-like (no job-aid grouping)",
                    "class=\"prim prim-step job-aid\"" not in cov_page
                    and "ele_sop_ast29080_proc_a_s1" in cov_page, ""))

    profile_inst = {
        "atom_id": INSTANCE_EXAMPLE_SEED[0][0],
        "content_hash": "sha256:" + ("c" * 64),
        "meaning": {
            "source_locale": "en",
            "source_text": "conditional_favorable",
            "kind": "instance_value",
        },
        "bindings": {"instance": {"instantiates": "atom_form_x", "authored_by": "role_smt"}},
        "governance": {"version": 1, "status": "draft", "owner": "role_smt"},
    }
    rationale_inst = {
        "atom_id": INSTANCE_EXAMPLE_SEED[1][0],
        "content_hash": "sha256:" + ("d" * 64),
        "meaning": {
            "source_locale": "en",
            "source_text": (
                "The benefit-risk profile of ASP9999 is favorable provided the additional "
                "hepatic monitoring described in the risk management plan is in place."
            ),
            "kind": "instance_value",
        },
        "bindings": {"instance": {"instantiates": "atom_form_y", "authored_by": "role_alsap_lead"}},
        "governance": {"version": 1, "status": "draft", "owner": "role_alsap_lead"},
    }
    unused_inst = {
        "atom_id": "atom_alsap_asp9999__form_ast34037_sec_cover_f_asset_code",
        "content_hash": "sha256:" + ("e" * 64),
        "meaning": {"source_locale": "en", "source_text": "ASP9999", "kind": "instance_value"},
        "bindings": {"instance": {}},
        "governance": {"version": 1, "status": "draft"},
    }
    instance_store = [profile_inst, rationale_inst, unused_inst]
    seeded_inst = assemble_elements(
        store, [], DEFAULT_MOVE, mint_extras=True, instance_atoms=instance_store
    )
    inst_eids = [
        mint_extra_element_id(INSTANCE_EXAMPLE_SEED[0][0], "exemplify"),
        mint_extra_element_id(INSTANCE_EXAMPLE_SEED[1][0], "exemplify"),
    ]
    unused_eid = mint_element_id(unused_inst["atom_id"])
    unused_extra = mint_extra_element_id(unused_inst["atom_id"], "exemplify")
    got_spine_inst = select_spine(store, seeded_inst)
    results.append(("instance seed mints two exemplify extras",
                    all(eid in {e["element_id"] for e in seeded_inst} for eid in inst_eids),
                    sorted(e["element_id"] for e in seeded_inst if "asp9999" in e["element_id"])))
    results.append(("instance extras composed_from instance atom_ids",
                    all(next(e for e in seeded_inst if e["element_id"] == eid)["composed_from"]
                        == aid for eid, (aid, _) in zip(inst_eids, INSTANCE_EXAMPLE_SEED)), ""))
    results.append(("instance extras stamp exemplify not present",
                    all(next(e for e in seeded_inst if e["element_id"] == eid)["intent"]["move"]
                        == "exemplify" for eid in inst_eids), ""))
    results.append(("instance extras carry no authored content.text",
                    all("content" not in next(e for e in seeded_inst if e["element_id"] == eid)
                        for eid in inst_eids), ""))
    results.append(("unused instance atom is not minted onto the store",
                    unused_eid not in {e["element_id"] for e in seeded_inst}
                    and unused_extra not in {e["element_id"] for e in seeded_inst}, ""))
    results.append(("SOP atoms.json fixture is unchanged by instance join",
                    all(a["atom_id"].startswith("atom_sop_") for a in store), ""))
    results.append(("spine places instance example after Procedure A and before checks",
                    got_spine_inst[-4:] == inst_eids + [
                        "ele_sop_ast29080_purpose__reinforce",
                        "ele_sop_ast29080_general__reinforce",
                    ]
                    and got_spine_inst.index("ele_sop_ast29080_proc_a_s4")
                    < got_spine_inst.index(inst_eids[0])
                    < got_spine_inst.index("ele_sop_ast29080_purpose__reinforce"),
                    got_spine_inst))
    results.append(("spine without instance store stays the original 12",
                    got_spine == want_spine and len(got_spine) == 12, len(got_spine)))
    results.append(("instance_value + exemplify is tp_body not a new primitive",
                    classify_text_primitive(rationale_inst, {"intent": {"move": "exemplify"}})
                    == PRIMITIVE_BODY, ""))
    for eid in inst_eids:
        el = next(e for e in seeded_inst if e["element_id"] == eid)
        el["expression"] = {
            "style_ref": "brand.example",
            "text_primitive": "tp_body",
            "content_role": "example",
            "layout_hint": "cite",
        }
    with tempfile.TemporaryDirectory() as td:
        html_path = pathlib.Path(td) / "realized_lesson.html"
        project_html(
            store, seeded_inst,
            {"project": "selftest", "one_to_many": {"seeded_atom_count": 3}},
            html_path, meaning_atoms=instance_store,
        )
        page_inst = html_path.read_text()
    results.append(("lesson HTML shows Example kicker on instance beats",
                    page_inst.count(">Example</div>") == 2
                    and "style-example" in page_inst
                    and "brand.example" in page_inst, page_inst.count(">Example</div>")))
    results.append(("lesson HTML meaning is the instance atoms not invented text",
                    "conditional_favorable" in page_inst
                    and "The benefit-risk profile of ASP9999 is favorable provided" in page_inst, ""))
    results.append(("lesson HTML composed_from is the instance atom_id",
                    INSTANCE_EXAMPLE_SEED[0][0] in page_inst
                    and INSTANCE_EXAMPLE_SEED[1][0] in page_inst, ""))
    results.append(("lesson HTML does not dump the unused instance atom",
                    unused_inst["atom_id"] not in page_inst
                    and unused_eid not in page_inst, ""))
    results.append(("instance example is not a third check or a job-aid card",
                    page_inst.count('form class="check"') == 2
                    and page_inst.count('class="prim prim-step job-aid"') == 1, ""))
    results.append(("instance example sits after the job aid and before checks in HTML",
                    page_inst.find("ele_sop_ast29080_proc_a_s4")
                    < page_inst.find(inst_eids[0])
                    < page_inst.find("ele_sop_ast29080_purpose__reinforce"), ""))

    huge_steps = [
        atom(
            f"atom_sop_ast29080_proc_a_s{i}", "procedure_step",
            f"Do Plan Development work item number {i:02d} with enough text to not be a thin heading.",
            "atom_sop_ast29080_proc_a", i - 1,
        )
        for i in range(1, PROCEDURE_SEQUENCE_CAP + 5)
    ]
    huge_store = [title_live, purpose_live, scope_live, general_live,
                  procedures, proc_a] + huge_steps
    huge_els = assemble_elements(huge_store, [], DEFAULT_MOVE, mint_extras=True)
    huge_spine = select_spine(huge_store, huge_els)
    a_on_huge = [eid for eid in huge_spine if "_proc_a_s" in eid]
    results.append(("huge Procedure A is capped",
                    len(a_on_huge) == PROCEDURE_SEQUENCE_CAP, len(a_on_huge)))
    results.append(("huge A cap keeps object.order prefix",
                    a_on_huge == [f"ele_sop_ast29080_proc_a_s{i}"
                                  for i in range(1, PROCEDURE_SEQUENCE_CAP + 1)],
                    a_on_huge))

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
    # --selftest must not require a project store.
    if "--selftest" in sys.argv[1:]:
        inject_default_project()
        P = harness_paths.resolve_core(None)
        element_schema = load(P["schemas_dir"] / "element.schema.json")
        closed_moves = list(element_schema["properties"]["intent"]["properties"]["move"]["enum"])
        for _aid, mv in ONE_TO_MANY_SEED:
            if mv not in closed_moves:
                raise SystemExit(f"seed move {mv!r} is not in the closed vocab")
        for _aid, mv in INSTANCE_EXAMPLE_SEED:
            if mv not in closed_moves:
                raise SystemExit(f"instance-example move {mv!r} is not in the closed vocab")
        selftest(closed_moves)
        return

    inject_default_project()
    default_shown = os.environ.get("TRAINSTORM_PROJECT") or (
        str(repo_default_project()) if repo_default_project() else "(pass --project)"
    )
    ap = argparse.ArgumentParser(
        description="Realizer v1 — mint occurrence elements (1:1 default + small 1:many seed) and project a lesson HTML.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="From cgen/trainstorm-core:\n"
               "  python tools/realize.py\n"
               "  python3 tools/realize.py --project ../astellas/projects/ast_alsap\n"
               "  python3 tools/realize.py --selftest\n"
               "  python3 tools/cartographer.py\n"
               "  python3 tools/couturier.py\n"
               "Open <project>/realized_lesson.html (short spine) or realized_coverage.html (full dump).\n",
    )
    ap.add_argument("--project", default=None,
                    help=f"Atom store directory containing atoms.json (default: {default_shown})")
    ap.add_argument("--core", default=None, help="trainstorm-core (schemas + vocab); usually auto-detected")
    ap.add_argument("--registry", default=None, help="Client registry; usually auto-derived from --project")
    ap.add_argument("--out", help="HTML output path (default: <project>/realized_lesson.html)")
    ap.add_argument("--store", help="Occurrence store directory (default: <project>/occurrences)")
    ap.add_argument("--move", default=DEFAULT_MOVE,
                    help=f"Closed pedagogical move for every v1 primary occurrence (default: {DEFAULT_MOVE})")
    ap.add_argument("--selftest", action="store_true", help="Run the 1:many minting fixture and exit")
    ap.add_argument("--no-one-to-many", action="store_true",
                    help="Do not mint new extras from the seed; still preserve extras already in the store")
    args = ap.parse_args()  # harness_paths re-reads --project/--core/--registry from argv

    P = harness_paths.resolve()
    print(harness_paths.announce(P))
    project = P["project_dir"]
    schemas = P["schemas_dir"]
    atoms_path = project / "atoms.json"
    if not atoms_path.exists():
        raise SystemExit(f"No atoms.json in project store: {project}")

    atoms_bytes = atoms_path.read_bytes()
    atoms_hash_before = sha256_bytes(atoms_bytes)
    atoms = json.loads(atoms_bytes)
    if not isinstance(atoms, list) or not atoms:
        raise SystemExit(f"{atoms_path} is not a non-empty atom list")
    atoms_by_id = {a["atom_id"]: a for a in atoms if "atom_id" in a}
    if len(atoms_by_id) != len(atoms):
        raise SystemExit("atom store has missing or duplicate atom_id values")

    element_schema = load(schemas / "element.schema.json")
    closed_moves = list(element_schema["properties"]["intent"]["properties"]["move"]["enum"])
    registry = load(P["vocab_dir"] / "primitives.registry.json")
    closed_text_primitives = {e["key"] for e in (registry.get("text_primitive") or []) if "key" in e}
    move = args.move
    if move not in closed_moves:
        raise SystemExit(f"--move {move!r} is not in the closed vocab: {closed_moves}")
    for _aid, mv in ONE_TO_MANY_SEED:
        if mv not in closed_moves:
            raise SystemExit(f"seed move {mv!r} is not in the closed vocab: {closed_moves}")
    for _aid, mv in INSTANCE_EXAMPLE_SEED:
        if mv not in closed_moves:
            raise SystemExit(f"instance-example move {mv!r} is not in the closed vocab: {closed_moves}")

    store_dir = pathlib.Path(args.store).resolve() if args.store else project / "occurrences"
    previous = []
    prev_path = store_dir / "elements.json"
    prev_mf = {}
    if prev_path.exists() and prev_path.resolve() != atoms_path.resolve():
        previous = load(prev_path)
        if not isinstance(previous, list):
            previous = []
        mf_prev_path = store_dir / "manifest.json"
        if mf_prev_path.exists():
            prev_mf = load(mf_prev_path)

    mint_extras = not args.no_one_to_many
    instance_atoms = load_instance_example_atoms(project)
    instance_path = sibling_instance_project(project)
    instance_hash_before = (
        sha256_bytes((instance_path / "atoms.json").read_bytes()) if instance_path else None
    )
    instance_by_id = {a["atom_id"]: a for a in instance_atoms}
    missing_seed = [aid for aid, _mv in INSTANCE_EXAMPLE_SEED if aid not in instance_by_id]
    if instance_atoms and missing_seed:
        raise SystemExit(
            f"instance-example seed atom_id(s) missing from {INSTANCE_PROJECT_NAME}: {missing_seed}"
        )
    elements = assemble_elements(
        atoms, previous, move, mint_extras=mint_extras, instance_atoms=instance_atoms
    )
    atoms_by_id = meaning_catalog(atoms, instance_atoms)
    validate_elements(elements, element_schema, atoms_by_id)
    assert_primitives_registered(elements, closed_text_primitives)

    primaries = [e for e in elements if is_primary_element(e)]
    extras = [e for e in elements if is_extra_element(e)]
    if len(primaries) != len(atoms):
        raise SystemExit(f"every atom needs one primary occurrence; got {len(primaries)} vs {len(atoms)}")
    from collections import defaultdict
    moves_by_atom = defaultdict(set)
    for e in elements:
        moves_by_atom[e["composed_from"]].add((e.get("intent") or {}).get("move"))
    for aid, mvset in moves_by_atom.items():
        if len([e for e in elements if e["composed_from"] == aid]) > 1 and len(mvset) < 2:
            raise SystemExit(f"{aid}: 1:many occurrences must have distinct moves; got {sorted(mvset)}")

    for e in extras:
        if (e.get("intent") or {}).get("move") != "reinforce":
            continue
        atom = atoms_by_id[e["composed_from"]]
        chk = derive_check(atom, atoms)
        assert_check_honest(chk, atom, atoms)

    store_dir.mkdir(parents=True, exist_ok=True)
    elements_path = store_dir / "elements.json"
    if elements_path.resolve() == atoms_path.resolve():
        raise SystemExit("refusing to overwrite atoms.json")

    mf_path = project / "manifest.json"
    project_name = load(mf_path).get("project", project.name) if mf_path.exists() else project.name
    seeded_present = [
        {"atom_id": aid, "extra_element_id": mint_extra_element_id(aid, mv), "move": mv}
        for aid, mv in ONE_TO_MANY_SEED if aid in atoms_by_id
    ]
    occ_manifest = {
        "store": "occurrences",
        "project": project_name,
        "policy": STORE_POLICY if extras else POLICY,
        "default_move": move,
        "element_count": len(elements),
        "generated_by": REALIZER,
        "realized_from": {
            "atom_store": portable_atom_store_path(atoms_path),
            "atom_count": len(atoms),
            "atoms_sha256": atoms_hash_before,
        },
        "one_to_many": {
            "spec": "agents/realizer/one_to_many_v1.md",
            "seeded_atom_count": len({s["atom_id"] for s in seeded_present}),
            "extra_count": len(extras),
            "seed": seeded_present,
            "note": ("Small honest seed, not the whole SOP. Extra ele_ ids are stable. "
                     "Re-run accretes missing extras and never drops existing extras, "
                     "Cartographer bindings, or Couturier style. Extra reinforce "
                     "occurrences project as a check from the atom "
                     "(agents/realizer/check_v1.md)."),
        },
        "instance_example": {
            "spec": INSTANCE_EXAMPLE_SPEC,
            "policy": INSTANCE_EXAMPLE_POLICY,
            "store": INSTANCE_PROJECT_NAME,
            "seed": [
                {"atom_id": aid, "extra_element_id": mint_extra_element_id(aid, mv), "move": mv}
                for aid, mv in INSTANCE_EXAMPLE_SEED if aid in instance_by_id
            ],
            "note": ("Procedure A has no honest match in the instance store (plan-"
                     "development acts vs filled AST-34037 values). Two cited atoms "
                     "illustrate the ALSAP generally: BR profile + rationale. "
                     "composed_from points at the instance atom_id. Meaning catalog "
                     "joins the sibling store; SOP atoms.json is not copied into."),
        },
        "note": ("Primary: one ele_ per atom. 1:many seed mints extra occurrences of a couple "
                 "of teaching-worthy atoms (same composed_from, distinct move, no authored "
                 "content.text). A small instance-example seed mints guest ele_ records "
                 f"in this occurrence store whose composed_from is an alsap_asp9999 atom_id "
                 f"({INSTANCE_EXAMPLE_SPEC}). Cartographer owns occurrence intent; Couturier owns expression "
                 "style. Realizer binds compiler primitives (text_primitive) from atom kind + "
                 f"move ({PRIMITIVE_SPEC}). Spine is a documented selection of existing ele_ records "
                 f"({SPINE_SPEC}); the full dump is coverage. A re-realize preserves extras, "
                 "intent, style, and recomputes the same spine and primitives."),
    }
    if any((e.get("ext") or {}).get("cartographer") for e in elements):
        cart = dict(prev_mf.get("cartographer") or {})
        cart["move_counts"] = move_counts(elements)
        cart["teaches_bound"] = sum(1 for e in elements if (e.get("intent") or {}).get("teaches"))
        cart["low_confidence"] = sum(
            1 for e in elements
            if (e.get("ext") or {}).get("cartographer", {}).get("confidence") == "low"
        )
        cart["element_count"] = len(elements)
        occ_manifest["cartographer"] = cart
    if any((e.get("ext") or {}).get("couturier") for e in elements):
        from collections import Counter
        cout = dict(prev_mf.get("couturier") or {})
        cout["look_counts"] = dict(sorted(Counter(
            (e.get("expression") or {}).get("style_ref") or "undressed" for e in elements
        ).items()))
        cout["dressed"] = sum(1 for e in elements if e.get("expression"))
        cout["element_count"] = len(elements)
        occ_manifest["couturier"] = cout
    apply_spine(occ_manifest, atoms, elements)
    stamp_primitives(occ_manifest, elements)
    normalize_elements_ext(elements)
    elements_path.write_text(json.dumps(elements, indent=2) + "\n")
    (store_dir / "manifest.json").write_text(json.dumps(occ_manifest, indent=2) + "\n")

    html_path = pathlib.Path(args.out).resolve() if args.out else project / "realized_lesson.html"
    coverage_path = project_html(
        atoms, elements, occ_manifest, html_path, meaning_atoms=instance_atoms
    )
    (store_dir / "manifest.json").write_text(json.dumps(occ_manifest, indent=2) + "\n")

    atoms_hash_after = sha256_bytes(atoms_path.read_bytes())
    if atoms_hash_after != atoms_hash_before:
        raise SystemExit("atoms.json changed during realize — abort. Realizer must not rewrite atoms.")
    if instance_path and instance_hash_before:
        if sha256_bytes((instance_path / "atoms.json").read_bytes()) != instance_hash_before:
            raise SystemExit(
                f"{INSTANCE_PROJECT_NAME}/atoms.json changed during realize — abort. "
                "Realizer must not rewrite instance atoms."
            )

    spine_n = (occ_manifest.get("spine") or {}).get("count", 0)
    print(f"Realizer v1 → {len(elements)} elements ({occ_manifest['policy']}, default_move={move})")
    print(f"  atoms      : {atoms_path} ({len(atoms)} records, unchanged)")
    print(f"  primaries  : {len(primaries)}")
    print(f"  extras     : {len(extras)} ({', '.join(e['element_id'] + '=' + (e.get('intent') or {}).get('move', '?') for e in extras) or 'none'})")
    print(f"  occurrences: {elements_path}")
    print(f"  manifest   : {store_dir / 'manifest.json'}")
    print(f"  spine      : {spine_n} of {len(elements)} ({SPINE_POLICY})")
    print(f"  instance   : {INSTANCE_PROJECT_NAME} ({len(instance_atoms)} atoms joined for meaning; "
          f"{sum(1 for e in extras if (e.get('ext') or {}).get('realized_from', {}).get('instance_store'))} guest ele_)")
    print(f"  primitives : {dict(sorted(primitive_counts(elements).items()))}")
    print(f"  lesson HTML: {html_path}  ← open this (short lesson)")
    print(f"  coverage   : {coverage_path}  (full SOP dump)")
    print("  schema     : element.schema.json ALL PASS (no authored content.text)")


if __name__ == "__main__":
    main()
