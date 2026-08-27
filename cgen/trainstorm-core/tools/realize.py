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
**check** (`agents/realizer/check_v1.md`). Three closed shapes live on the
graph (`vocab/check-shape.enum.json`): `invert_definition` (sibling first
sentences), `sequence_order` (Procedure A `object.order`), `closed_choice`
(`reg_benefit_risk_profile` + instance `selected_value`). Realizer stamps
`ext.check` / `manifest.checks` (shape + operand refs). The projector
**reads** those records; it does not re-discover pedagogy by if-atom-id.
Sequence and closed-choice are projector-only: no extra `ele_`. Sequence
cannot honestly `composed_from` one A step; closed_choice cannot honestly
`composed_from` only the form field or only the instance fill (options live
on the field’s `options_ref`, key lives on the instance). No authored
`content.text`. Prefer keys/refs over copying option strings. Distractors,
if any, are sibling atoms or the field’s already-governed value set — never
an LLM writer.

Default HTML is a **short lesson spine** (`agents/realizer/spine_v1.md`): title
hook, a why-this callout of the purpose atom (`tp_callout`), a handful of
front-matter teaching cards, Procedure A’s real steps as a job sequence
(present only), a sequence practice of those four presents (`sequence_order`
read from `manifest.checks`), two form-field presents from the sibling form
store (the BR profile / rationale fields the instance examples fill —
`agents/realizer/form_field_present_v1.md`), one worked example from the
sibling instance store (two `exemplify` extras of existing ASP-9999 atoms —
`agents/realizer/instance_example_v1.md`), then a `closed_choice` of the BR
profile (projector-only, after the field+example), then the existing
definition checks (`invert_definition`). Scene membership and order are
first-class on the graph (`vocab/scene.enum.json`): Realizer stamps
`spine.scenes` / `ext.scene` (id, title heuristic, ordered `ele_` refs,
in-scene check-shape refs). A **lesson** record (`agents/realizer/lesson_v1.md`)
points at that list. The projector **reads the lesson node** (default, or
`--lesson`) then its scenes and checks; it does not hard-code “the ALSAP
lesson is these three headings.” Same three scenes (front-matter /
Procedure A / form BR), **one at a time** (Next/Back). Scene 3 includes
the BR closed-choice after the field+example. Definition/purpose checks
stay a final step after scene 3, not a fourth scene. Extra lesson records
are a subset of those same `spine.scenes`, read from the project catalog
(`occurrences/lessons.json`) and stamped onto `manifest.lessons`. The
projector writes HTML derived from `lesson_id`; it does not fork this
file for a lesson id. A one-scene lesson has the pager disabled (single
step). The full SOP dump is `realized_coverage.html` (a second
projection, not a lesson node).
Spine is a selection of existing `ele_` records — it mints none for membership
and drops none. Procedure-step atoms stay 1:1 (no extra `reinforce`): they are
imperatives, so they cannot host an honest copula-invert sibling check. Form
and instance extras `composed_from` those stores’ `atom_id`s; they do not copy
text onto the element or into SOP `atoms.json`.

**Atom → primitives** (`agents/realizer/primitives_v1.md`): Realizer binds a
closed compiler `text_primitive` on the occurrence from atom kind + occurrence
move (heading / body / step / callout / check). The spine projector renders
those primitives — why-this as a callout of purpose, Procedure A s1–s4 as one
job-aid step list then a sequence practice of the same four presents, the
form-field presents as body/`present` clothes, the instance example as
body/`exemplify` clothes (not a new SOP card), a closed-choice of the BR
profile fill after those presents/examples, front-matter as heading/body,
reinforce as the existing definition checks. Scene records group those
existing primitives; they do not mint `ele_`. The lesson record mints no
`ele_` either (not a `Course` occurrence — no honest `composed_from` for
a container). Player chrome shows one named scene at a time (Next/Back)
by reading the selected lesson’s scenes. Coverage stays card-like.
Couturier still owns `style_ref`. No authored `content.text`.

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
    python tools/realize.py --lesson ast_alsap_short
    python tools/realize.py --lesson ast_alsap_br
    python tools/realize.py --lesson ast_alsap_plan
    python tools/realize.py --selftest
    python tools/cartographer.py          # re-runnable on the mixed store
    python tools/couturier.py             # dresses existing ele_; mints nothing

Default `--project` is the live ALSAP SOP store (47 atoms). Writes (regenerated,
never hand-edited):

    <project>/occurrences/elements.json     occurrence store (does not touch atoms.json)
    <project>/occurrences/manifest.json     realized_from / source hashes + spine keys
    <project>/occurrences/lessons.json      closed project catalog (source of truth; not rewritten)
    <project>/realized_lesson.html          short lesson (default {project}_short). Open this.
    <project>/realized_lesson_br.html       BR subset (path derived from lesson_id)
    <project>/realized_lesson_plan.html     Procedure A subset (path derived from lesson_id)
    <project>/realized_coverage.html        full SOP dump in document order
"""
from __future__ import annotations

import argparse
import hashlib
import html
import inspect
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
CHECK_SHAPE_SPEC = "vocab/check-shape.enum.json"
CHECK_SHAPE_POLICY = "v1_check_shapes_on_graph"
SHAPE_INVERT = "invert_definition"
SHAPE_SEQUENCE = "sequence_order"
SHAPE_CLOSED = "closed_choice"
CHECK_SHAPES = (SHAPE_INVERT, SHAPE_SEQUENCE, SHAPE_CLOSED)
# Render of invert_definition when contrast_atom_ids is empty — not a fourth shape.
RENDER_CLOZE = "cloze"
SPINE_SPEC = "agents/realizer/spine_v1.md"
SPINE_POLICY = "v1_front_matter_callout_procedure_sequence_form_example_then_checks"
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
FORM_FIELD_SPEC = "agents/realizer/form_field_present_v1.md"
FORM_FIELD_POLICY = "v1_form_field_present_seed"
FORM_PROJECT_NAME = "alsap"
# Honest referent of INSTANCE_EXAMPLE_SEED: those instance atoms instantiate
# exactly these two FORM-AST-34037 fields. Not f_br_guidance, not phrasing
# examples. If they were missing, stop rather than stretch a cousin.
FORM_FIELD_SEED = (
    ("atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile", "present"),
    ("atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale", "present"),
)
# Closed-choice of the BR profile fill. Prompt is task clothes (same honesty
# as the sequence prompt). Options = the form field's options_ref value ids.
# Key = the instance selected_value. Do not invent a stem.
BR_CHECK_PROMPT = "Choose the closed value already shown."
BR_PROFILE_FORM_ATOM_ID = FORM_FIELD_SEED[0][0]
BR_PROFILE_INSTANCE_ATOM_ID = INSTANCE_EXAMPLE_SEED[0][0]
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
# First-class scene records: group existing spine ele_ into three scenes
# from SOP/form roles already used for membership. Not new beats. Not an
# LLM. Headings are the documented title heuristic, not invented outcomes.
# Spec: agents/realizer/scenes_v1.md. Projector reads spine.scenes.
SCENE_SPEC = "agents/realizer/scenes_v1.md"
SCENE_VOCAB = "vocab/scene.enum.json"
SCENE_GRAPH_POLICY = "v1_scenes_on_graph"
SCENE_POLICY = "v1_three_scenes_from_roles"
PAGING_POLICY = "v1_one_scene_at_a_time"
SCENE_FRONT_MATTER = "front_matter"
SCENE_PROCEDURE_A = "procedure_a"
SCENE_FORM_BR = "form_br"
SCENE_LESSON_END = "lesson_end"
SCENE_DEFS = (
    {
        "id": "what_an_alsap_is",
        "role": SCENE_FRONT_MATTER,
        "heading": "What an ALSAP is",
        "kicker": "Front matter",
        "from": (
            "Document-root opening, why-this callout of purpose, and teachable "
            "front-matter primaries (purpose / scope / general). Those atoms "
            "are the SOP’s definitional front-matter."
        ),
    },
    {
        "id": "how_an_alsap_starts",
        "role": SCENE_PROCEDURE_A,
        "heading": "How an ALSAP starts",
        "kicker": "Procedure A",
        "from": (
            "First Procedures-container branch in object.order (thin heading: "
            "A. Plan Development of ALSAP.). Job-aid presents plus the "
            "in-scene sequence practice of those presents."
        ),
    },
    {
        "id": "benefit_risk_on_the_form",
        "role": SCENE_FORM_BR,
        "heading": "Benefit-risk on the form",
        "kicker": "Form",
        "from": (
            "FORM-AST-34037 BR-field presents (Benefit-Risk profile + rationale) "
            "plus the instance examples that instantiate those fields, then an "
            "in-scene closed-choice of the profile fill (registry value ids; "
            "key = instance selected_value)."
        ),
    },
)
SCENE_DEFS_BY_ROLE = {d["role"]: d for d in SCENE_DEFS}
LESSON_SPEC = "agents/realizer/lesson_v1.md"
LESSON_POLICY = "v1_lesson_on_graph"
LESSON_CATALOG_FILENAME = "lessons.json"
LESSON_CATALOG_POLICY = "v1_lesson_catalog"
DEFAULT_LESSON_HTML_NAME = "realized_lesson.html"
DEFAULT_COVERAGE_HTML_NAME = "realized_coverage.html"

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


def load_options_registry(registry_dir) -> dict:
    """Client options registry keyed by reg_ id. Empty if the file is absent."""
    if not registry_dir:
        return {}
    p = pathlib.Path(registry_dir) / "options.registry.json"
    if not p.exists():
        return {}
    data = load(p)
    return {e["id"]: e for e in (data.get("options") or []) if isinstance(e, dict) and e.get("id")}


def load_check_shape_ids(vocab_dir) -> list:
    """Closed check-shape vocab. Missing file is a hard fail in main; selftest uses CHECK_SHAPES."""
    p = pathlib.Path(vocab_dir) / "check-shape.enum.json"
    if not p.exists():
        return list(CHECK_SHAPES)
    data = load(p)
    return [s["id"] for s in (data.get("shapes") or []) if s.get("id")]


SCENE_ROLES = (SCENE_FRONT_MATTER, SCENE_PROCEDURE_A, SCENE_FORM_BR)


def load_scene_role_ids(vocab_dir) -> list:
    """Closed scene-role vocab. Missing file is a hard fail in main; selftest uses SCENE_ROLES."""
    p = pathlib.Path(vocab_dir) / "scene.enum.json"
    if not p.exists():
        return list(SCENE_ROLES)
    data = load(p)
    return [s["id"] for s in (data.get("roles") or []) if s.get("id")]


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


def sibling_form_project(sop_project: pathlib.Path | None) -> pathlib.Path | None:
    """Lesson store is ast_alsap; form is sibling alsap (FORM-AST-34037). Not every project."""
    if sop_project is None or sop_project.name != "ast_alsap":
        return None
    sibling = sop_project.parent / FORM_PROJECT_NAME
    if (sibling / "atoms.json").exists():
        return sibling
    return None


def load_form_field_atoms(sop_project: pathlib.Path | None) -> list:
    """Join catalog only. Does not rewrite SOP or form atoms.json."""
    sibling = sibling_form_project(sop_project)
    if sibling is None:
        return []
    atoms = load(sibling / "atoms.json")
    if not isinstance(atoms, list):
        return []
    return [a for a in atoms if a.get("atom_id")]


def sibling_options_registry(sop_project: pathlib.Path | None) -> pathlib.Path | None:
    """Client options registry (reg_ ids). ALSAP lesson join only."""
    if sop_project is None or sop_project.name != "ast_alsap":
        return None
    reg = sop_project.parent.parent / "registry" / "options.registry.json"
    if reg.exists():
        return reg
    return None


def load_option_sets(sop_project: pathlib.Path | None) -> dict:
    """Governed value sets keyed by options_ref. Does not rewrite the registry."""
    path = sibling_options_registry(sop_project)
    if path is None:
        return {}
    data = load(path)
    if not isinstance(data, dict):
        return {}
    return {e["id"]: e for e in (data.get("options") or []) if e.get("id")}


def joined_guest_atoms(sop_project: pathlib.Path | None) -> list:
    """Form then instance. SOP atoms.json is not copied into."""
    return load_form_field_atoms(sop_project) + load_instance_example_atoms(sop_project)


def meaning_catalog(sop_atoms, extra_atoms=None) -> dict:
    """SOP atoms plus joined guest atoms, keyed by atom_id. SOP wins on collision."""
    by_id = {a["atom_id"]: a for a in sop_atoms if a.get("atom_id")}
    for a in extra_atoms or []:
        aid = a.get("atom_id")
        if aid and aid not in by_id:
            by_id[aid] = a
    return by_id


def mint_element(atom, move: str, *, role: str = "primary", guest: bool = False) -> dict:
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
    # Guest extras live in a store that is not their home. Do not point
    # parent_id at an ele_ that was never minted here.
    if obj.get("belongs_to") and not guest:
        structure["parent_id"] = mint_element_id(obj["belongs_to"])
    if "order" in obj:
        structure["sequence_index"] = obj["order"]
    if obj.get("prerequisites") and not guest:
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


def append_guest_extras(elements, claimed, prev, mint_extras, *, seed, atoms_by_id,
                        store_name, spec, policy, store_key, spec_key):
    """Mint guest extras whose composed_from is in a sibling atom store."""
    wanted = []
    seen = set()
    if mint_extras:
        for aid, move in seed:
            if aid not in atoms_by_id:
                continue
            eid = mint_extra_element_id(aid, move)
            wanted.append((eid, aid, move))
            seen.add(eid)
    for old in prev.values():
        cf = old.get("composed_from")
        if cf not in atoms_by_id or not is_extra_element(old):
            continue
        eid = old["element_id"]
        if eid in seen or eid in claimed:
            continue
        move = extra_move_of(old)
        if not move:
            continue
        wanted.append((eid, cf, move))
        seen.add(eid)
    for eid, aid, move in wanted:
        if eid in claimed:
            continue
        extra = mint_element(atoms_by_id[aid], move, role="extra", guest=True)
        extra["element_id"] = eid
        rf = extra.setdefault("ext", {}).setdefault("realized_from", {})
        rf[store_key] = store_name
        rf[spec_key] = spec
        rf["policy"] = policy
        preserve_cartographer_intent([extra], list(prev.values()))
        preserve_couturier_expression([extra], list(prev.values()))
        if not (extra.get("ext") or {}).get("cartographer"):
            extra["intent"]["move"] = move
        elements.append(extra)
        claimed.add(eid)
    return elements, claimed


EXT_KEY_ORDER = ("realized_from", "cartographer", "couturier", "realizer_primitive", "check", "scene")


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
                      instance_atoms=None, form_atoms=None, options_registry=None) -> list:
    """
    Mint one primary per SOP atom, then extra occurrences from the seed and from
    any extras already in the store. Never drop an existing extra. Preserve
    Cartographer intent on matching element_id values. Guest form-field presents
    (sibling alsap) and guest instance extras (sibling alsap_asp9999) mint into
    this occurrence store with composed_from pointing at those atom_ids — they
    are not copied into SOP atoms.json.
    """
    prev = {e.get("element_id"): e for e in (previous or []) if e.get("element_id")}
    instance_by_id = {a["atom_id"]: a for a in (instance_atoms or []) if a.get("atom_id")}
    form_by_id = {a["atom_id"]: a for a in (form_atoms or []) if a.get("atom_id")}
    atoms_by_id = meaning_catalog(atoms, list(form_by_id.values()) + list(instance_by_id.values()))
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

    append_guest_extras(
        elements, claimed, prev, mint_extras,
        seed=FORM_FIELD_SEED, atoms_by_id=form_by_id,
        store_name=FORM_PROJECT_NAME, spec=FORM_FIELD_SPEC, policy=FORM_FIELD_POLICY,
        store_key="form_store", spec_key="form_spec",
    )
    append_guest_extras(
        elements, claimed, prev, mint_extras,
        seed=INSTANCE_EXAMPLE_SEED, atoms_by_id=instance_by_id,
        store_name=INSTANCE_PROJECT_NAME, spec=INSTANCE_EXAMPLE_SPEC,
        policy=INSTANCE_EXAMPLE_POLICY,
        store_key="instance_store", spec_key="instance_spec",
    )

    for eid, old in prev.items():
        if eid in claimed:
            continue
        cf = old.get("composed_from")
        if cf in atoms_by_id and is_extra_element(old):
            elements.append(old)
            claimed.add(eid)

    apply_group_ids(elements)
    refresh_text_primitives(elements, atoms_by_id)
    bind_check_shapes(
        elements, atoms,
        meaning_atoms=list(form_by_id.values()) + list(instance_by_id.values()),
        options_registry=options_registry,
    )
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
    """True when this occurrence hosts a stamped check shape, or is the
    legacy reinforce/recall surface. Membership of lesson-end checks is
    still `move == reinforce` (closed_choice stays in the form scene)."""
    rec = hosted_check(el)
    if rec and rec.get("shape") in CHECK_SHAPES:
        return True
    move = (el.get("intent") or {}).get("move")
    expr = el.get("expression") or {}
    return (
        move == "reinforce"
        or expr.get("style_ref") == "brand.recall"
        or expr.get("text_primitive") == PRIMITIVE_CHECK
        or expr.get("layout_hint") == "check"
    )


def hosted_check(el) -> dict | None:
    rec = (el.get("ext") or {}).get("check")
    if isinstance(rec, dict) and rec.get("shape") in CHECK_SHAPES:
        return rec
    return None


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


def invert_operands(atom, atoms) -> dict | None:
    """Operand refs for invert_definition. Contrast ids only — no copied strings."""
    src = (atom.get("meaning") or {}).get("source_text") or ""
    sentence = first_sentence(src)
    if not sentence or not copula_parts(sentence):
        return None
    contrast = []
    for sib in sibling_atoms(atom, atoms):
        sib_sent = first_sentence((sib.get("meaning") or {}).get("source_text") or "")
        if not sib_sent:
            continue
        if strip_period(sib_sent).lower() == strip_period(sentence).lower():
            continue
        if not phrase_in_atom(sib_sent, sib):
            continue
        contrast.append(sib["atom_id"])
        if len(contrast) >= 2:
            break
    return {
        "key_atom_id": atom["atom_id"],
        "contrast_atom_ids": contrast,
    }


def supports_honest_sibling_check(atom, atoms) -> bool:
    """True only for a copula invert plus two sibling first-sentences.

    Procedure steps are imperatives — no `{subject} is {complement}` — so this
    is False and we do not mint an extra `reinforce` of one step. Cloze is not
    sibling contrast. Sequence practice of a procedure_step *group* is a
    different shape (`sequence_order`); it mints no extra `ele_`.
    """
    sentence = first_sentence((atom.get("meaning") or {}).get("source_text") or "")
    if not copula_parts(sentence):
        return False
    ops = invert_operands(atom, atoms)
    return bool(ops and ops.get("contrast_atom_ids"))


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


def form_field_spine_ids(elements) -> list:
    """Seed order. Guest extras whose composed_from is a cited form field atom."""
    by_eid = {e["element_id"]: e for e in elements}
    out = []
    for aid, move in FORM_FIELD_SEED:
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
    presents (job sequence) → form-field presents → instance-example extras
    → reinforce extras of spine atoms. Spec: agents/realizer/spine_v1.md
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
                (el.get("intent") or {}).get("move") == "reinforce"
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
    form_fields = form_field_spine_ids(elements)
    examples = instance_example_spine_ids(elements)
    return opening + presents + form_fields + examples + checks


def apply_spine(manifest, atoms, elements, *, meaning_atoms=None, option_sets=None,
                lesson_catalog=None) -> dict:
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
                 "not B/C), then the two FORM-AST-34037 BR-field presents those instance "
                 "examples fill (alsap atoms via composed_from), then a small "
                 "instance-example seed (alsap_asp9999 atoms via composed_from — "
                 "Procedure A has no honest match; these illustrate the ALSAP generally), "
                 "then existing reinforce extras. Spine projector "
                 "renders compiler primitives (callout / step list / heading / body / "
                 "check) plus a sequence practice of the Procedure A presents "
                 "(projector-only; no extra ele_) plus a closed-choice of the BR "
                 "profile fill after the form presents and instance examples "
                 "(projector-only; options_ref value ids; no extra ele_) plus "
                 "present clothes on the form-field beats and exemplify clothes "
                 "on the instance beats; coverage dump stays card-like. Scene "
                 "records (spine.scenes / ext.scene) group those existing beats "
                 "from SOP/form roles — first-class on the graph, not chrome "
                 "rediscovery. A lesson record (manifest.lessons) points at that "
                 "list; the projector reads the lesson node, not a hard-coded "
                 "ALSAP trio. Lesson records come from the project catalog "
                 "(occurrences/lessons.json) when present. Player chrome pages "
                 "that list one named scene at a time (Next/Back); lesson-end "
                 "checks are a final step, not a fourth scene. Not an LLM path "
                 "and not a full object-tree walk."),
    }
    seq_atoms = procedure_sequence_atoms(atoms)
    seq = derive_sequence_check(seq_atoms)
    if seq:
        assert_sequence_check_honest(seq, atoms)
        by_cf = {e.get("composed_from"): e for e in elements if is_primary_element(e)}
        from_eids = [by_cf[aid]["element_id"] for aid in seq["correct_ids"] if aid in by_cf]
        manifest["spine"]["sequence_check"] = {
            "shape": SHAPE_SEQUENCE,
            "spec": CHECK_SPEC,
            "policy": CHECK_POLICY,
            "from_atom_ids": seq["correct_ids"],
            "from_element_ids": from_eids,
            "see": "checks",
            "note": ("Projector-only practice of the Procedure A presents already on "
                     "the spine. Items are those atoms’ first sentences. Correct order "
                     "is bindings.object.order (already taught). No extra ele_ — "
                     "composing this check from one atom would be a lie. Lives in the "
                     "Procedure A scene. First-class record is manifest.checks "
                     f"shape {SHAPE_SEQUENCE}."),
        }
    catalog = meaning_catalog(atoms, meaning_atoms)
    registry = option_sets or {}
    cc = closed_choice_record(elements, catalog, registry)
    has_br = False
    if cc:
        ops = cc["operands"]
        form_atom = catalog.get(ops.get("form_atom_id"))
        inst_atom = catalog.get(ops.get("instance_atom_id"))
        br = derive_br_profile_check(form_atom, inst_atom, registry)
        if br:
            has_br = True
            assert_br_profile_check_honest(br, catalog, registry)
            from_eids = [eid for eid in (
                ops.get("form_element_id"), ops.get("instance_element_id"),
            ) if eid]
            manifest["spine"]["br_profile_check"] = {
                "shape": SHAPE_CLOSED,
                "spec": CHECK_SPEC,
                "policy": CHECK_SHAPE_POLICY,
                "see": "checks",
                "options_ref": ops.get("options_ref"),
                "key": br["key"],
                "from_atom_ids": [ops.get("form_atom_id"), ops.get("instance_atom_id")],
                "from_element_ids": from_eids,
                "note": ("Projector-only closed-choice of the BR profile fill already "
                         "shown. Options are the form field’s options_ref value ids "
                         "(verbatim). Key is the instance selected_value. Prompt is "
                         "task clothes, not an SOP stem. No extra ele_ — composing "
                         "from only the form field or only the instance would hide "
                         "the other half. Lives in the form BR scene. First-class "
                         f"record is manifest.checks shape {SHAPE_CLOSED}."),
            }
    by_eid = {e["element_id"]: e for e in elements}
    by_atom = {a["atom_id"]: a for a in atoms}
    scenes, lesson_end = group_spine_scenes(ids, by_eid, by_atom)
    manifest["spine"]["scenes"] = stamp_spine_scenes(
        scenes, lesson_end,
        sequence_check=bool(seq),
        closed_choice=has_br,
    )
    bind_scene_membership(elements, manifest["spine"]["scenes"])
    stamp_lessons(manifest, atoms, elements, lesson_catalog=lesson_catalog)
    return manifest["spine"]


def sibling_coverage_path(lesson_path: pathlib.Path) -> pathlib.Path:
    if lesson_path.name == DEFAULT_LESSON_HTML_NAME or lesson_path.name.startswith("realized_lesson_"):
        return lesson_path.with_name(DEFAULT_COVERAGE_HTML_NAME)
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


def spine_scene_role(el, atoms_by_id) -> str:
    """Which scene cluster this existing spine occurrence belongs to.

    Pure function of SOP/form/instance roles already on the graph (atom kind,
    guest stamps, extra reinforce). Not an LLM. Not a new ele_. Definition /
    purpose reinforce extras stay lesson-end unless they are the Procedure A
    sequence practice or the form-BR closed-choice (those practices are
    projector-only and have no ele_).
    """
    if is_extra_element(el) and (el.get("intent") or {}).get("move") == "reinforce":
        return SCENE_LESSON_END
    atom = atoms_by_id.get(el.get("composed_from")) or {}
    kind = (atom.get("meaning") or {}).get("kind") or ""
    realized = (el.get("ext") or {}).get("realized_from") or {}
    if realized.get("form_store") or realized.get("instance_store"):
        return SCENE_FORM_BR
    if kind in ("form_field", "form_section", "form", "instance_value"):
        return SCENE_FORM_BR
    if kind == "procedure_step" or is_step_primitive(el):
        return SCENE_PROCEDURE_A
    return SCENE_FRONT_MATTER


def group_spine_scenes(spine_ids, by_eid, atoms_by_id):
    """Consecutive same-role spine ids → scene runs. Lesson-end checks trail."""
    scenes = []
    lesson_end = []
    current = None
    for eid in spine_ids:
        el = by_eid.get(eid)
        if el is None:
            continue
        role = spine_scene_role(el, atoms_by_id)
        if role == SCENE_LESSON_END:
            if current is not None:
                scenes.append(current)
                current = None
            lesson_end.append(eid)
            continue
        if current is not None and current["role"] == role:
            current["element_ids"].append(eid)
        else:
            if current is not None:
                scenes.append(current)
            current = {"role": role, "element_ids": [eid]}
    if current is not None:
        scenes.append(current)
    return scenes, lesson_end


def stamp_spine_scenes(scenes, lesson_end, *, sequence_check=False,
                       closed_choice=False) -> dict:
    """First-class scene records. Membership is unchanged. Projector reads these."""
    out = []
    for s in scenes:
        d = SCENE_DEFS_BY_ROLE.get(s["role"]) or {}
        checks = []
        if s["role"] == SCENE_PROCEDURE_A and sequence_check:
            checks.append({"shape": SHAPE_SEQUENCE, "see": "checks"})
        if s["role"] == SCENE_FORM_BR and closed_choice:
            checks.append({"shape": SHAPE_CLOSED, "see": "checks"})
        out.append({
            "id": d.get("id") or s["role"],
            "role": s["role"],
            "heading": d.get("heading") or s["role"],
            "kicker": d.get("kicker") or "",
            "element_ids": list(s["element_ids"]),
            "checks": checks,
            "from": d.get("from") or "",
        })
    return {
        "policy": SCENE_GRAPH_POLICY,
        "heuristic": SCENE_POLICY,
        "spec": SCENE_SPEC,
        "vocab": SCENE_VOCAB,
        "scenes": out,
        "lesson_end_checks": list(lesson_end),
        "paging": {
            "policy": PAGING_POLICY,
            "spec": SCENE_SPEC,
            "scene_count": len(out),
            "step_count": len(out) + (1 if lesson_end else 0),
            "lesson_end_is_final_step": bool(lesson_end),
            "note": ("Player UX on the first-class scene list: one named scene "
                     "at a time, Next/Back. Definition/purpose checks are a "
                     "final step after the last scene, not a fourth named scene. "
                     "Hash is optional. Same membership. Coverage dump stays unpaged."),
        },
        "note": ("First-class scene records: ordered ele_ refs plus in-scene "
                 "check-shape refs. Projector reads this list to wrap/page; it "
                 "does not re-discover scenes by if-atom-id. Sequence practice "
                 "stays in Procedure A. Form-BR closed-choice stays in "
                 "Benefit-risk on the form. Definition/purpose checks stay at "
                 "lesson end. Not an LLM. Not outcome language. "
                 "Coverage dump stays ungrouped."),
    }


def bind_scene_membership(elements, scenes_stamp):
    """Stamp ext.scene on member ele_ records. Clears stale stamps. Idempotent."""
    by_eid = {e["element_id"]: e for e in elements}
    claimed = set()
    for sc in (scenes_stamp or {}).get("scenes") or []:
        sid = sc.get("id") or ""
        role = sc.get("role") or ""
        if role and role not in SCENE_ROLES:
            raise SystemExit(f"scene {sid!r} role {role!r} is not in {SCENE_VOCAB}")
        rec = {
            "id": sid,
            "role": role,
            "spec": SCENE_SPEC,
            "policy": SCENE_GRAPH_POLICY,
        }
        for eid in sc.get("element_ids") or []:
            el = by_eid.get(eid)
            if el is None:
                raise SystemExit(f"scene {sid} element {eid} is not on the graph")
            el.setdefault("ext", {})["scene"] = dict(rec)
            claimed.add(eid)
    for el in elements:
        if el.get("element_id") not in claimed:
            ext = el.get("ext")
            if isinstance(ext, dict):
                ext.pop("scene", None)


def hosted_scene(el) -> dict | None:
    rec = (el.get("ext") or {}).get("scene")
    if isinstance(rec, dict) and rec.get("id") and rec.get("role") in SCENE_ROLES:
        return rec
    return None


def resolve_scene(record, by_eid) -> dict:
    """Membership from stamped element_ids. Refuses if a ref does not resolve."""
    if not record:
        raise SystemExit("scene record is missing")
    sid = record.get("id") or ""
    role = record.get("role") or ""
    if role not in SCENE_ROLES:
        raise SystemExit(f"scene {sid!r} role {role!r} is not in {SCENE_VOCAB}")
    ids = list(record.get("element_ids") or [])
    if not ids:
        raise SystemExit(f"scene {sid} has no element_ids")
    els = []
    for eid in ids:
        el = by_eid.get(eid)
        if el is None:
            raise SystemExit(f"scene {sid} element {eid} is not on the graph")
        els.append(el)
    heading = record.get("heading") or ""
    if not heading:
        raise SystemExit(f"scene {sid} has no heading (title heuristic)")
    return {
        "id": sid,
        "role": role,
        "heading": heading,
        "kicker": record.get("kicker") or "",
        "element_ids": ids,
        "elements": els,
        "checks": list(record.get("checks") or []),
        "from": record.get("from") or "",
    }


def scene_check_refs(scene) -> list:
    """In-scene check-shape refs from the stamped scene record."""
    refs = []
    for cref in scene.get("checks") or []:
        if isinstance(cref, dict) and cref.get("shape"):
            refs.append(cref["shape"])
        elif isinstance(cref, str):
            refs.append(cref)
    return refs


def project_slug(manifest) -> str:
    """Stable project slug used in default lesson_id and derived HTML names."""
    proj = (manifest.get("project") or "").strip() or "course"
    return re.sub(r"[^A-Za-z0-9_-]+", "_", proj).strip("_") or "course"


def default_lesson_id(manifest) -> str:
    """Stable default lesson_id. Project-specific, not a closed enum."""
    return f"{project_slug(manifest)}_short"


def lesson_title_heuristic(atoms, elements, spine_ids):
    """Title from the document-root atom already on the spine. Ref, not invented copy."""
    by_eid = {e["element_id"]: e for e in elements}
    by_atom = {a["atom_id"]: a for a in atoms}
    if not spine_ids:
        return "", None
    el = by_eid.get(spine_ids[0])
    if not el:
        return "", None
    aid = el.get("composed_from")
    atom = by_atom.get(aid) if aid else None
    if not atom:
        return "", None
    text = clean_meaning((atom.get("meaning") or {}).get("source_text") or "")
    sent = first_sentence(text) or text
    return sent, aid


def build_default_lesson(manifest, atoms, elements) -> dict:
    """Pure function of spine.scenes + document-root title. Mints no ele_."""
    spine = manifest.get("spine") or {}
    scenes_stamp = spine.get("scenes") or {}
    scene_ids = [s["id"] for s in scenes_stamp.get("scenes") or [] if s.get("id")]
    end_ids = list(scenes_stamp.get("lesson_end_checks") or [])
    spine_ids = list(spine.get("element_ids") or [])
    title, title_from = lesson_title_heuristic(atoms, elements, spine_ids)
    lid = default_lesson_id(manifest)
    if not title:
        title = lid
    return {
        "lesson_id": lid,
        "title": title,
        "title_from": title_from,
        "scenes": {"see": "spine.scenes"},
        "scene_ids": scene_ids,
        "lesson_end_checks": {"see": "spine.scenes.lesson_end_checks"},
        "lesson_end_check_ids": end_ids,
        "paging": {"see": "spine.scenes.paging"},
        "default": True,
        "from": (
            "Document-root atom first sentence (title heuristic) plus the "
            "first-class scene list already on spine.scenes. Not an LLM. "
            "Not outcome language. Not a Course ele_ — no honest composed_from "
            "for a container."
        ),
    }


def lesson_catalog_path(store_dir) -> pathlib.Path:
    return pathlib.Path(store_dir) / LESSON_CATALOG_FILENAME


def load_lesson_catalog(store_dir) -> dict | None:
    """Read the closed project catalog. None if the file is absent (fixtures)."""
    path = lesson_catalog_path(store_dir)
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise SystemExit(f"{path} is not a lesson catalog object")
    lessons = [L for L in (data.get("lessons") or []) if isinstance(L, dict) and L.get("lesson_id")]
    if not lessons:
        raise SystemExit(f"{path} has no lesson records")
    seen = set()
    for rec in lessons:
        lid = rec["lesson_id"]
        if lid in seen:
            raise SystemExit(f"{path} has duplicate lesson_id {lid}")
        seen.add(lid)
    return data


def derive_lesson_paging(scene_ids, end_ids, _scenes_stamp=None, *, is_full=False) -> dict:
    """Paging for one lesson record. Full default follows spine.scenes.paging."""
    if is_full:
        return {"see": "spine.scenes.paging"}
    scene_count = len(scene_ids)
    has_end = bool(end_ids)
    step_count = scene_count + (1 if has_end else 0)
    paging = {
        "policy": PAGING_POLICY,
        "scene_count": scene_count,
        "step_count": step_count,
        "lesson_end_is_final_step": has_end,
    }
    if step_count <= 1:
        paging["chrome"] = "suppressed"
        paging["note"] = (
            "Same paging policy as the default lesson. This record has one "
            "scene and no lesson-end invert_definition checks, so Next/Back "
            "is not shown. In-scene checks stay on the scene record."
        )
    return paging


def hydrate_lesson_record(raw, manifest, atoms, elements, computed_default, *, is_default) -> dict:
    """Stamp one catalog row onto a runtime lesson record. Mints no ele_."""
    lid = raw.get("lesson_id") or ""
    if not lid:
        raise SystemExit("lesson catalog record is missing lesson_id")
    spine = manifest.get("spine") or {}
    scenes_stamp = spine.get("scenes") or {}
    scene_ids = list(raw.get("scene_ids") or [])
    if not scene_ids:
        if is_default:
            scene_ids = list(computed_default.get("scene_ids") or [])
        else:
            raise SystemExit(f"lesson catalog {lid} has no scene_ids")
    if "lesson_end_check_ids" in raw:
        end_ids = list(raw.get("lesson_end_check_ids") or [])
    elif is_default:
        end_ids = list(computed_default.get("lesson_end_check_ids") or [])
    else:
        end_ids = []
    title = raw.get("title") or ""
    title_from = raw.get("title_from") or computed_default.get("title_from")
    if not title:
        title = computed_default.get("title") or lid
    full = (
        scene_ids == list(computed_default.get("scene_ids") or [])
        and end_ids == list(computed_default.get("lesson_end_check_ids") or [])
    )
    paging = raw.get("paging")
    if isinstance(paging, dict) and (paging.get("see") or paging.get("policy")):
        paging = dict(paging)
    else:
        paging = derive_lesson_paging(scene_ids, end_ids, scenes_stamp, is_full=full)
    rec = {
        "lesson_id": lid,
        "title": title,
        "title_from": title_from,
        "scenes": {"see": "spine.scenes"},
        "scene_ids": scene_ids,
        "lesson_end_check_ids": end_ids,
        "paging": paging,
        "default": bool(is_default),
        "from": raw.get("from") or (
            computed_default.get("from") if is_default else (
                "Catalog record: ordered scene id refs into spine.scenes. "
                "Title heuristic is the document-root atom. Not a Course ele_."
            )
        ),
    }
    if is_default:
        rec["lesson_end_checks"] = {"see": "spine.scenes.lesson_end_checks"}
    return rec


def stamp_lessons_from_catalog(manifest, atoms, elements, lesson_catalog) -> dict:
    """Catalog is the source of truth. Stamps runtime view onto manifest.lessons."""
    computed = build_default_lesson(manifest, atoms, elements)
    raw_lessons = [
        L for L in (lesson_catalog.get("lessons") or [])
        if isinstance(L, dict) and L.get("lesson_id")
    ]
    default_id = lesson_catalog.get("default")
    if not default_id:
        for rec in raw_lessons:
            if rec.get("default"):
                default_id = rec["lesson_id"]
                break
    if not default_id:
        default_id = computed["lesson_id"]
    default_rec = None
    extras = []
    seen = set()
    for raw in raw_lessons:
        lid = raw["lesson_id"]
        if lid in seen:
            raise SystemExit(f"lesson catalog has duplicate lesson_id {lid}")
        seen.add(lid)
        is_default = lid == default_id
        rec = hydrate_lesson_record(
            raw, manifest, atoms, elements, computed, is_default=is_default,
        )
        if is_default:
            default_rec = rec
        else:
            extras.append(rec)
    if default_rec is None:
        default_rec = computed
    return _lessons_block(
        default_rec, extras, catalog=True,
        catalog_policy=lesson_catalog.get("policy") or LESSON_CATALOG_POLICY,
    )


def _lessons_block(default, extras, *, catalog=False, catalog_policy=None) -> dict:
    note = (
        "First-class lesson records: id, title heuristic, ordered scene "
        "id refs into spine.scenes, lesson-end ele_ refs, paging pointer. "
        "Projector reads the selected lesson (default or --lesson) to "
        "wrap/page; it does not assume the ALSAP trio. "
    )
    if catalog:
        note += (
            "Source of truth is the project catalog (occurrences/lessons.json); "
            "this block is the stamped runtime view. Adding a lesson is "
            "appending a catalog record. "
        )
    else:
        note += (
            "No project catalog; extra lesson records already on the stamp "
            "are preserved and project to a sibling HTML derived from "
            "lesson_id (not a fork of this file). "
        )
    note += (
        "Not a LMS. Not SCORM. Not a Course ele_. Coverage dump stays a "
        "second projection, not a lesson node."
    )
    block = {
        "policy": LESSON_POLICY,
        "spec": LESSON_SPEC,
        "default": default["lesson_id"],
        "lessons": [default] + extras,
        "note": note,
    }
    if catalog:
        block["catalog"] = {
            "see": f"occurrences/{LESSON_CATALOG_FILENAME}",
            "policy": catalog_policy or LESSON_CATALOG_POLICY,
        }
    return block


def stamp_lessons(manifest, atoms, elements, *, lesson_catalog=None) -> dict:
    """First-class lesson records. Catalog wins; else recompute default and keep extras."""
    if lesson_catalog:
        manifest["lessons"] = stamp_lessons_from_catalog(
            manifest, atoms, elements, lesson_catalog,
        )
        return manifest["lessons"]
    default = build_default_lesson(manifest, atoms, elements)
    block = manifest.get("lessons") if isinstance(manifest.get("lessons"), dict) else {}
    existing = list(block.get("lessons") or [])
    extras = [
        L for L in existing
        if isinstance(L, dict) and L.get("lesson_id") and L["lesson_id"] != default["lesson_id"]
    ]
    manifest["lessons"] = _lessons_block(default, extras, catalog=False)
    return manifest["lessons"]


def select_lesson_record(manifest, lesson_id=None) -> dict:
    block = manifest.get("lessons") if isinstance(manifest.get("lessons"), dict) else {}
    lessons = [L for L in (block.get("lessons") or []) if isinstance(L, dict)]
    if not lessons:
        raise SystemExit("no lesson record on the graph (manifest.lessons)")
    if lesson_id:
        for rec in lessons:
            if rec.get("lesson_id") == lesson_id:
                return rec
        raise SystemExit(f"lesson {lesson_id!r} is not on the graph")
    default_id = block.get("default")
    if default_id:
        for rec in lessons:
            if rec.get("lesson_id") == default_id:
                return rec
    for rec in lessons:
        if rec.get("default"):
            return rec
    return lessons[0]


def carry_previous_lesson_records(occ_manifest, prev_mf) -> None:
    """Fallback when no project catalog exists.

    Realize rebuilds the occurrence manifest from scratch. Fixtures plant extra
    lesson records on the previous stamp; this carry keeps them so stamp_lessons
    can preserve extras. A live catalog is the source of truth and skips this.
    """
    prev = prev_mf.get("lessons") if isinstance((prev_mf or {}).get("lessons"), dict) else {}
    prev_lessons = [
        L for L in (prev.get("lessons") or [])
        if isinstance(L, dict) and L.get("lesson_id")
    ]
    if not prev_lessons:
        return
    occ_manifest["lessons"] = {
        "policy": prev.get("policy") or LESSON_POLICY,
        "spec": prev.get("spec") or LESSON_SPEC,
        "default": prev.get("default"),
        "lessons": prev_lessons,
        "note": prev.get("note"),
    }


def lesson_html_filename(manifest, lesson_id=None) -> str:
    """Default lesson → realized_lesson.html; extras → realized_lesson_{suffix}.html.

    Suffix is the lesson_id with the project slug prefix stripped
    (`{project}_{suffix}` → `realized_lesson_{suffix}.html`). Not a per-id fork.
    """
    rec = select_lesson_record(manifest, lesson_id)
    lid = rec.get("lesson_id") or ""
    default_id = (manifest.get("lessons") or {}).get("default") or default_lesson_id(manifest)
    if rec.get("default") or lid == default_id:
        return DEFAULT_LESSON_HTML_NAME
    slug = project_slug(manifest)
    suffix = lid
    prefix = f"{slug}_"
    if lid.startswith(prefix):
        suffix = lid[len(prefix):]
    suffix = re.sub(r"[^A-Za-z0-9_-]+", "_", suffix).strip("_") or lid
    return f"realized_lesson_{suffix}.html"


def lesson_html_path(project, manifest, lesson_id=None, *, out=None) -> pathlib.Path:
    if out:
        return pathlib.Path(out).resolve()
    return pathlib.Path(project) / lesson_html_filename(manifest, lesson_id)


def iter_lesson_ids(manifest) -> list:
    block = manifest.get("lessons") if isinstance(manifest.get("lessons"), dict) else {}
    ids = []
    seen = set()
    for L in block.get("lessons") or []:
        if not isinstance(L, dict):
            continue
        lid = L.get("lesson_id")
        if not lid or lid in seen:
            continue
        seen.add(lid)
        ids.append(lid)
    return ids


def project_lesson_htmls(atoms, elements, manifest, project, *, meaning_atoms=None,
                         option_sets=None, options_registry=None, lesson_id=None,
                         out=None, lesson_catalog=None):
    """Write lesson HTML. Default pass emits every catalog/stamp record.

    `--lesson` regenerates that one file. `--out` writes one path.
    Coverage dump is written once (default lesson) and is not a lesson node.
    Extra records project to a path derived from `lesson_id`.
    """
    html_kw = dict(
        meaning_atoms=meaning_atoms, option_sets=option_sets,
        options_registry=options_registry, lesson_catalog=lesson_catalog,
    )
    if out:
        path = pathlib.Path(out).resolve()
        rec = select_lesson_record(manifest, lesson_id)
        default_id = (manifest.get("lessons") or {}).get("default")
        write_coverage = (
            path.name == DEFAULT_LESSON_HTML_NAME
            or rec.get("default")
            or rec.get("lesson_id") == default_id
        )
        coverage = project_html(
            atoms, elements, manifest, path,
            lesson_id=lesson_id, write_coverage=write_coverage, **html_kw,
        )
        return coverage, path, []

    ids = iter_lesson_ids(manifest)
    if lesson_id and lesson_id not in ids:
        select_lesson_record(manifest, lesson_id)
    if not ids:
        path = pathlib.Path(project) / DEFAULT_LESSON_HTML_NAME
        coverage = project_html(
            atoms, elements, manifest, path,
            lesson_id=lesson_id, **html_kw,
        )
        return coverage, path, []

    default_id = (manifest.get("lessons") or {}).get("default") or default_lesson_id(manifest)
    if lesson_id:
        ordered = [lesson_id]
    else:
        ordered = []
        if default_id:
            ordered.append(default_id)
        for lid in ids:
            if lid not in ordered:
                ordered.append(lid)

    coverage_path = None
    selected_path = None
    extra_paths = []
    for lid in ordered:
        path = pathlib.Path(project) / lesson_html_filename(manifest, lid)
        is_default = lid == default_id
        cov = project_html(
            atoms, elements, manifest, path,
            lesson_id=lid, write_coverage=is_default, **html_kw,
        )
        if is_default:
            coverage_path = cov
        if selected_path is None:
            selected_path = path
        elif path != selected_path:
            extra_paths.append(path)
    return coverage_path, selected_path, extra_paths


def _follow_paging(rec, scenes_stamp) -> dict:
    paging = rec.get("paging")
    if isinstance(paging, dict) and paging.get("see"):
        return dict(scenes_stamp.get("paging") or {})
    if isinstance(paging, dict) and paging.get("policy"):
        return dict(paging)
    return dict(scenes_stamp.get("paging") or {})


def resolve_lesson(manifest, by_eid, *, lesson_id=None, atoms_by_id=None) -> dict:
    """Lesson → scenes → element_ids. Refuses if a ref does not resolve."""
    rec = select_lesson_record(manifest, lesson_id)
    lid = rec.get("lesson_id") or ""
    if not lid:
        raise SystemExit("lesson record has no lesson_id")
    scenes_stamp = (manifest.get("spine") or {}).get("scenes") or {}
    by_sid = {s.get("id"): s for s in scenes_stamp.get("scenes") or [] if s.get("id")}
    scene_ids = list(rec.get("scene_ids") or [])
    if not scene_ids:
        scene_ids = [s.get("id") for s in scenes_stamp.get("scenes") or [] if s.get("id")]
    resolved_scenes = []
    for sid in scene_ids:
        sc = by_sid.get(sid)
        if sc is None:
            raise SystemExit(f"lesson {lid} scene {sid} is not on spine.scenes")
        resolved_scenes.append(resolve_scene(sc, by_eid))
    if "lesson_end_check_ids" in rec:
        end_ids = list(rec.get("lesson_end_check_ids") or [])
    else:
        end_ids = list(scenes_stamp.get("lesson_end_checks") or [])
    for eid in end_ids:
        if eid not in by_eid:
            raise SystemExit(f"lesson {lid} lesson_end_check {eid} is not on the graph")
    title = rec.get("title") or ""
    title_from = rec.get("title_from")
    if not title and atoms_by_id and title_from:
        atom = atoms_by_id.get(title_from)
        if atom:
            text = clean_meaning((atom.get("meaning") or {}).get("source_text") or "")
            title = first_sentence(text) or text
    if not title:
        raise SystemExit(f"lesson {lid} has no title (heuristic or ref)")
    if "will be able" in title.lower() or "learning outcome" in title.lower():
        raise SystemExit(f"lesson {lid} title is outcome language: {title!r}")
    return {
        "lesson_id": lid,
        "title": title,
        "title_from": title_from,
        "scenes": resolved_scenes,
        "lesson_end_checks": end_ids,
        "paging": _follow_paging(rec, scenes_stamp),
        "record": rec,
    }


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
        render = "mcq" if distractors else RENDER_CLOZE
        cloze_lead = cloze_blank = cloze_tail = None
        if render == RENDER_CLOZE:
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
        render = "mcq" if distractors else RENDER_CLOZE

    ops = invert_operands(atom, atoms) or {
        "key_atom_id": atom["atom_id"],
        "contrast_atom_ids": [d["from_atom_id"] for d in distractors],
    }
    check = {
        "shape": SHAPE_INVERT,
        "render": render,
        "spec": CHECK_SPEC,
        "policy": CHECK_POLICY,
        "stem": stem,
        "key": key,
        "key_atom_id": atom["atom_id"],
        "sentence": sentence,
        "choices": [],
        "cloze_lead": cloze_lead if render == RENDER_CLOZE else None,
        "cloze_tail": cloze_tail if render == RENDER_CLOZE else None,
        "operands": ops,
    }
    if render == "mcq":
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


def derive_sequence_check(step_atoms) -> dict | None:
    """Order-the-siblings check for a procedure_step group.

    Items = verbatim first sentences of the given atoms. Correct order =
    bindings.object.order (already taught on the job aid). Not a copula invert
    and not an MCQ stem. Composing this from one atom would be a lie — the
    check *is* the siblings — so the projector emits it without minting an
    extra ele_.
    """
    items = []
    for atom in step_atoms or []:
        if (atom.get("meaning") or {}).get("kind") != "procedure_step":
            return None
        sent = first_sentence((atom.get("meaning") or {}).get("source_text") or "")
        if not sent or not phrase_in_atom(sent, atom):
            return None
        items.append({
            "atom_id": atom["atom_id"],
            "text": sent,
            "order": atom_order(atom),
        })
    if len(items) < 2:
        return None
    items.sort(key=lambda it: it["order"])
    orders = [it["order"] for it in items]
    if len(set(orders)) != len(orders):
        return None
    return {
        "shape": SHAPE_SEQUENCE,
        "spec": CHECK_SPEC,
        "policy": CHECK_POLICY,
        "prompt": "Put these in the order already taught.",
        "items": items,
        "correct_ids": [it["atom_id"] for it in items],
        "operands": {
            "atom_ids": [it["atom_id"] for it in items],
            "order_from": "bindings.object.order",
        },
    }


def assert_sequence_check_honest(check, atoms):
    """Refuse a sequence projection that invented wording or order."""
    if not check or check.get("shape") != SHAPE_SEQUENCE:
        raise SystemExit("sequence check derivation returned nothing")
    if check.get("prompt") != "Put these in the order already taught.":
        raise SystemExit("sequence prompt is clothes, not an SOP stem — refusing a new fact")
    by_id = {a["atom_id"]: a for a in atoms}
    prev = None
    for it in check.get("items") or []:
        src = by_id.get(it["atom_id"])
        if src is None:
            raise SystemExit(f"sequence item cites unknown atom {it['atom_id']}")
        if (src.get("meaning") or {}).get("kind") != "procedure_step":
            raise SystemExit(f"{it['atom_id']}: sequence item is not a procedure_step")
        if not phrase_in_atom(it["text"], src):
            raise SystemExit(
                f"{it['atom_id']}: sequence item is not in the atom — refusing to invent"
            )
        expected = first_sentence((src.get("meaning") or {}).get("source_text") or "")
        if it["text"] != expected:
            raise SystemExit(f"{it['atom_id']}: sequence item is not the atom’s first sentence")
        o = atom_order(src)
        if it["order"] != o:
            raise SystemExit(f"{it['atom_id']}: sequence order is not bindings.object.order")
        if prev is not None and o <= prev:
            raise SystemExit("sequence items are not strictly object.order")
        prev = o
    if check.get("correct_ids") != [it["atom_id"] for it in check["items"]]:
        raise SystemExit("sequence correct_ids must follow the sorted items")


def option_values(entry) -> list:
    if not isinstance(entry, dict):
        return []
    return [v for v in (entry.get("values") or []) if isinstance(v, dict) and v.get("id")]


def closed_choice_operands(el, catalog, options_registry) -> dict | None:
    """Operand refs for closed_choice. Registry id + atom ids — no copied labels."""
    atom = catalog.get(el.get("composed_from"))
    if not atom:
        return None
    inst = (atom.get("bindings") or {}).get("instance") or {}
    sv = inst.get("selected_value")
    form_id = inst.get("instantiates")
    if not sv or not form_id:
        return None
    form = catalog.get(form_id)
    if not form:
        return None
    options_ref = ((form.get("bindings") or {}).get("form") or {}).get("options_ref")
    if not options_ref:
        return None
    entry = (options_registry or {}).get(options_ref)
    values = option_values(entry)
    if not any(v.get("id") == sv for v in values):
        return None
    return {
        "options_ref": options_ref,
        "instance_atom_id": atom["atom_id"],
        "form_atom_id": form_id,
        "key_from": "bindings.instance.selected_value",
        "instance_element_id": el["element_id"],
    }


def closed_choice_record(elements, catalog, options_registry) -> dict | None:
    """Projector-only closed_choice from graph refs. No extra ele_, no ext.check host."""
    rec = None
    for el in elements:
        realized = (el.get("ext") or {}).get("realized_from") or {}
        if not realized.get("instance_store"):
            continue
        ops = closed_choice_operands(el, catalog, options_registry or {})
        if not ops:
            continue
        form_eid = None
        for e in elements:
            if e.get("composed_from") == ops["form_atom_id"] and is_extra_element(e):
                if (e.get("intent") or {}).get("move") == "present":
                    form_eid = e["element_id"]
                    break
        ops = dict(ops)
        ops["form_element_id"] = form_eid
        rec = {
            "shape": SHAPE_CLOSED,
            "host_element_id": None,
            "placement": "after_form_br",
            "operands": ops,
        }
        break
    return rec


def ext_check_stamp(shape, operands) -> dict:
    return {
        "shape": shape,
        "spec": CHECK_SPEC,
        "policy": CHECK_SHAPE_POLICY,
        "operands": operands,
    }


def bind_check_shapes(elements, atoms, *, meaning_atoms=None, options_registry=None) -> list:
    """Stamp ext.check on host ele_ records. Returns the manifest checks index.

    Operand refs only. Projector resolves wording from the graph.
    """
    extra = list(meaning_atoms or [])
    catalog = meaning_catalog(list(atoms), extra)
    records = []

    for el in elements:
        if not is_extra_element(el):
            continue
        if (el.get("intent") or {}).get("move") != "reinforce":
            continue
        atom = catalog.get(el.get("composed_from"))
        if atom is None:
            continue
        ops = invert_operands(atom, atoms)
        if not ops:
            el.get("ext", {}).pop("check", None)
            continue
        ops = dict(ops)
        ops["host_element_id"] = el["element_id"]
        el.setdefault("ext", {})["check"] = ext_check_stamp(SHAPE_INVERT, ops)
        records.append({
            "shape": SHAPE_INVERT,
            "host_element_id": el["element_id"],
            "operands": ops,
        })

    seq_atoms = procedure_sequence_atoms(atoms)
    seq = derive_sequence_check(seq_atoms)
    if seq:
        by_primary = {e.get("composed_from"): e for e in elements if is_primary_element(e)}
        from_eids = [by_primary[aid]["element_id"]
                     for aid in seq["correct_ids"] if aid in by_primary]
        ops = {
            "atom_ids": list(seq["correct_ids"]),
            "element_ids": from_eids,
            "order_from": "bindings.object.order",
        }
        records.append({
            "shape": SHAPE_SEQUENCE,
            "host_element_id": None,
            "placement": "after_job_aid",
            "operands": ops,
        })

    rec = closed_choice_record(elements, catalog, options_registry or {})
    if rec:
        records.append(rec)
    for el in elements:
        host = hosted_check(el)
        if host and host.get("shape") == SHAPE_CLOSED:
            el.get("ext", {}).pop("check", None)

    return records


def stamp_checks(manifest, atoms, elements, *, meaning_atoms=None, options_registry=None) -> list:
    """Write manifest.checks and bind ext.check. Idempotent."""
    records = bind_check_shapes(
        elements, atoms, meaning_atoms=meaning_atoms, options_registry=options_registry
    )
    manifest["checks"] = {
        "policy": CHECK_SHAPE_POLICY,
        "spec": CHECK_SPEC,
        "vocab": CHECK_SHAPE_SPEC,
        "checks": records,
        "note": ("Closed shapes on the graph. Projector reads these records "
                 "(and ext.check on host ele_ records). Operands are refs — "
                 "atoms, ele_, options_ref, object.order — not copied option "
                 "strings. invert_definition hosts on extra reinforce; "
                 "sequence_order is projector-only of the Procedure A presents; "
                 "closed_choice is projector-only of the form present + instance "
                 "fill (options_ref value ids; key = selected_value)."),
    }
    return records


def manifest_check(manifest, shape, *, host_element_id=None) -> dict | None:
    for rec in ((manifest.get("checks") or {}).get("checks") or []):
        if rec.get("shape") != shape:
            continue
        if host_element_id is not None and rec.get("host_element_id") != host_element_id:
            continue
        return rec
    return None


def resolve_invert_definition(operands, catalog) -> dict | None:
    """Wording from operand atom_ids. Refuses if a ref does not resolve."""
    key_id = (operands or {}).get("key_atom_id")
    atom = catalog.get(key_id)
    if atom is None:
        return None
    atoms = [atom]
    for sid in operands.get("contrast_atom_ids") or []:
        sib = catalog.get(sid)
        if sib is None:
            raise SystemExit(f"invert_definition contrast {sid} is not on the graph")
        atoms.append(sib)
    # derive_check hunts siblings in `atoms`; pass the full catalog values so
    # belongs_to still finds them, but the stamped contrast ids are the source
    # of truth for which distractors land.
    chk = derive_check(atom, list(catalog.values()))
    if not chk or chk.get("shape") != SHAPE_INVERT:
        return None
    want = list(operands.get("contrast_atom_ids") or [])
    if want:
        got = [c["from_atom_id"] for c in chk.get("choices") or [] if not c.get("correct")]
        if got != want:
            # Rebuild choices strictly from stamped contrast ids.
            key = chk["key"]
            choices = [{"text": key, "correct": True, "from_atom_id": key_id}]
            for sid in want:
                sib = catalog[sid]
                sent = first_sentence((sib.get("meaning") or {}).get("source_text") or "")
                if not sent or not phrase_in_atom(sent, sib):
                    raise SystemExit(f"invert_definition contrast {sid} has no honest first sentence")
                choices.append({"text": sent, "correct": False, "from_atom_id": sid})
            chk = dict(chk)
            chk["choices"] = choices
            chk["render"] = "mcq"
    chk["operands"] = operands
    return chk


def resolve_sequence_order(operands, catalog) -> dict | None:
    ids = list((operands or {}).get("atom_ids") or [])
    step_atoms = []
    for aid in ids:
        src = catalog.get(aid)
        if src is None:
            raise SystemExit(f"sequence_order atom {aid} is not on the graph")
        step_atoms.append(src)
    chk = derive_sequence_check(step_atoms)
    if chk:
        chk["operands"] = operands
    return chk


def resolve_closed_choice(operands, catalog, options_registry) -> dict | None:
    inst = catalog.get((operands or {}).get("instance_atom_id"))
    form = catalog.get((operands or {}).get("form_atom_id"))
    options_ref = (operands or {}).get("options_ref")
    if not inst or not form or not options_ref:
        return None
    chk = derive_br_profile_check(form, inst, options_registry or {})
    if not chk:
        return None
    form_ref = ((form.get("bindings") or {}).get("form") or {}).get("options_ref")
    if form_ref != options_ref:
        raise SystemExit(
            f"closed_choice options_ref {options_ref} is not the form atom’s options_ref {form_ref}"
        )
    if (operands or {}).get("key_from") == "bindings.instance.selected_value":
        sv = ((inst.get("bindings") or {}).get("instance") or {}).get("selected_value")
        if not sv:
            raise SystemExit("closed_choice key_from selected_value is missing on the instance atom")
        if chk.get("key") != sv:
            raise SystemExit("closed_choice selected_value drifted from the instance atom")
    chk = dict(chk)
    chk["operands"] = operands
    return chk


def resolve_check(record, catalog, options_registry=None) -> dict | None:
    """Resolved render payload from a stamped check record. Graph only."""
    if not record:
        return None
    shape = record.get("shape")
    ops = record.get("operands") or {}
    if shape == SHAPE_INVERT:
        return resolve_invert_definition(ops, catalog)
    if shape == SHAPE_SEQUENCE:
        return resolve_sequence_order(ops, catalog)
    if shape == SHAPE_CLOSED:
        return resolve_closed_choice(ops, catalog, options_registry or {})
    raise SystemExit(f"unknown check shape {shape!r} — not in {CHECK_SHAPE_SPEC}")


def shuffled_sequence_items(items, seed: str) -> list:
    """Stable non-identity permutation so the learner can be wrong, then right."""
    rotated = stable_rotate(list(items), seed)
    ids = [it["atom_id"] for it in rotated]
    correct = [it["atom_id"] for it in items]
    if ids == correct and len(items) > 1:
        rotated = list(items[1:]) + list(items[:1])
    return rotated


def option_value_ids(form_atom, option_sets) -> list | None:
    """Verbatim closed value ids from the form field's options_ref. None if no set."""
    ref = ((form_atom.get("bindings") or {}).get("form") or {}).get("options_ref")
    if not ref:
        return None
    entry = (option_sets or {}).get(ref)
    if not entry:
        return None
    ids = []
    seen = set()
    for v in entry.get("values") or []:
        vid = v.get("id")
        if not vid or vid in seen:
            continue
        seen.add(vid)
        ids.append(vid)
    if len(ids) < 2:
        return None
    return ids


def derive_br_profile_check(form_atom, instance_atom, option_sets) -> dict | None:
    """Closed-choice of the instance fill against the form field's options_ref.

    Options = verbatim value ids from the governed set. Key = instance
    selected_value (must be a member, and must be the atom's source_text).
    Prompt is task clothes, not an SOP stem. If there is no honest closed
    set, return None — do not invent options or a fact-asserting stem.
    """
    if not form_atom or not instance_atom:
        return None
    if (form_atom.get("meaning") or {}).get("kind") != "form_field":
        return None
    if (instance_atom.get("meaning") or {}).get("kind") != "instance_value":
        return None
    inst = (instance_atom.get("bindings") or {}).get("instance") or {}
    if inst.get("instantiates") != form_atom.get("atom_id"):
        return None
    values = option_value_ids(form_atom, option_sets)
    if not values:
        return None
    key = inst.get("selected_value")
    src = (instance_atom.get("meaning") or {}).get("source_text") or ""
    if not key or key != src:
        return None
    if key not in values:
        return None
    if not phrase_in_atom(key, instance_atom):
        return None
    ref = ((form_atom.get("bindings") or {}).get("form") or {}).get("options_ref")
    return {
        "shape": "closed_choice",
        "spec": CHECK_SPEC,
        "policy": CHECK_POLICY,
        "prompt": BR_CHECK_PROMPT,
        "key": key,
        "key_atom_id": instance_atom["atom_id"],
        "form_atom_id": form_atom["atom_id"],
        "options_ref": ref,
        "choices": [
            {"text": vid, "correct": vid == key, "from": ref} for vid in values
        ],
    }


def assert_br_profile_check_honest(check, catalog, option_sets):
    """Refuse a closed-choice that invented a key, an option, or an SOP stem."""
    if not check or check.get("shape") != "closed_choice":
        raise SystemExit("BR profile check derivation returned nothing")
    if check.get("prompt") != BR_CHECK_PROMPT:
        raise SystemExit("BR prompt is clothes, not an SOP stem — refusing a new fact")
    form_atom = catalog.get(check.get("form_atom_id"))
    inst_atom = catalog.get(check.get("key_atom_id"))
    if form_atom is None or inst_atom is None:
        raise SystemExit("BR profile check cites unknown form or instance atom")
    values = option_value_ids(form_atom, option_sets)
    if not values:
        raise SystemExit("BR profile check has no honest closed set — refusing to invent options")
    if check.get("options_ref") != ((form_atom.get("bindings") or {}).get("form") or {}).get("options_ref"):
        raise SystemExit("BR profile check options_ref is not the form field’s")
    if check.get("key") != ((inst_atom.get("bindings") or {}).get("instance") or {}).get("selected_value"):
        raise SystemExit("BR profile check key is not the instance selected_value")
    if not phrase_in_atom(check["key"], inst_atom):
        raise SystemExit("BR profile check key is not in the instance atom — refusing to invent")
    if check["key"] not in values:
        raise SystemExit("BR profile check key is not in the form field’s closed set")
    choice_texts = [c["text"] for c in (check.get("choices") or [])]
    if choice_texts != values:
        raise SystemExit("BR profile check options are not the verbatim closed value ids")
    for c in check.get("choices") or []:
        if c["text"] not in values:
            raise SystemExit(f"BR choice {c['text']!r} is not in the closed set")
        if c.get("from") != check.get("options_ref"):
            raise SystemExit("BR choice must cite the form field’s options_ref")
        if c["correct"] and c["text"] != check["key"]:
            raise SystemExit("BR key choice must be the instance selected_value")
        if not c["correct"] and c["text"] == check["key"]:
            raise SystemExit("BR distractor must not be the instance fill")


def shuffled_closed_choices(choices, seed: str) -> list:
    """Stable non-identity permutation so the learner can be wrong, then right."""
    rotated = stable_rotate(list(choices), seed)
    original = [c["text"] for c in choices]
    shown = [c["text"] for c in rotated]
    if shown == original and len(rotated) > 1:
        rotated = list(rotated[1:]) + list(rotated[:1])
    if rotated and rotated[0].get("correct") and len(rotated) > 1:
        rotated = list(rotated[1:]) + list(rotated[:1])
    return rotated


def stable_rotate(items, seed: str) -> list:
    if not items:
        return []
    n = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % len(items)
    return items[n:] + items[:n]


def check_body_html(el, catalog, options_registry, esc) -> str | None:
    """Occurrence body from a stamped check shape. None if this ele_ hosts none."""
    rec = hosted_check(el)
    if not rec:
        return None
    chk = resolve_check(rec, catalog, options_registry)
    if not chk:
        return None
    eid = el["element_id"]
    shape = chk["shape"]
    if shape == SHAPE_INVERT:
        atom = catalog.get(chk.get("key_atom_id") or rec["operands"]["key_atom_id"])
        if atom:
            assert_check_honest(chk, atom, list(catalog.values()))
        return invert_check_html(el, chk, esc)
    if shape == SHAPE_CLOSED:
        return closed_choice_html(el, chk, esc)
    return None


def invert_check_html(el, chk, esc) -> str:
    eid = el["element_id"]
    reveal = esc(chk.get("sentence") or chk.get("key") or "")
    ops = chk.get("operands") or {}
    contrast = ops.get("contrast_atom_ids") or []
    src_note = (
        f'<p class="check-note">Key is atom '
        f'<span class="mono">{esc(chk.get("key_atom_id") or ops.get("key_atom_id") or "")}</span>. '
        f'Contrast, if any, is sibling atoms '
        f'({", ".join(esc(a) for a in contrast) or "none"}). '
        f'Shape <span class="mono">{esc(SHAPE_INVERT)}</span> — '
        f'read from <span class="mono">ext.check</span>, not authored '
        f'<span class="mono">content.text</span>.</p>'
    )
    if chk.get("render") == "mcq" or chk.get("choices"):
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
            f'<form class="check" data-shape="{esc(SHAPE_INVERT)}" data-key="key" '
            f'data-eid="{esc(eid)}">'
            f'<p class="stem">{esc(chk["stem"])}</p>'
            f'{"".join(labels)}'
            f'<div class="check-actions"><button type="submit">Check</button></div>'
            f'<p class="feedback" hidden></p>'
            f'<p class="reveal" hidden>{reveal}</p>'
            f"{src_note}"
            f"</form>"
        )
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
        f'<form class="check" data-shape="{esc(SHAPE_INVERT)}" data-render="{esc(RENDER_CLOZE)}" '
        f'data-key="{esc(chk["key"])}" data-eid="{esc(eid)}">'
        f"{stem_block}"
        f'<input type="text" class="cloze-in" autocomplete="off" aria-label="Your recall">'
        f'<div class="check-actions"><button type="submit">Check</button></div>'
        f'<p class="feedback" hidden></p>'
        f'<p class="reveal" hidden>{reveal}</p>'
        f"{src_note}"
        f"</form>"
    )


def closed_choice_html(el, chk, esc) -> str:
    eid = el["element_id"]
    ops = chk.get("operands") or {}
    choices = stable_rotate(list(chk["choices"]), eid)
    if [c.get("id") or c.get("text") for c in choices] == [
        c.get("id") or c.get("text") for c in chk["choices"]
    ] and len(choices) > 1:
        choices = list(choices[1:]) + list(choices[:1])
    labels = []
    for c in choices:
        vid = c.get("id") or c["text"]
        labels.append(
            f'<label class="choice">'
            f'<input type="radio" name="{esc(eid)}" value="{esc(vid)}">'
            f'<span class="mono">{esc(c["text"])}</span>'
            f"</label>"
        )
    src_note = (
        f'<p class="check-note">Key is <span class="mono">selected_value</span> '
        f'<span class="mono">{esc(chk["key"])}</span> on '
        f'<span class="mono">{esc(ops.get("instance_atom_id") or chk.get("key_atom_id") or "")}</span>. '
        f'Choices resolve from <span class="mono">{esc(ops.get("options_ref") or chk.get("options_ref") or "")}</span> '
        f'(form atom <span class="mono">{esc(ops.get("form_atom_id") or chk.get("form_atom_id") or "")}</span>). '
        f'Shape <span class="mono">{esc(SHAPE_CLOSED)}</span> — labels are not on the element.</p>'
    )
    return (
        f'<form class="check" data-shape="{esc(SHAPE_CLOSED)}" '
        f'data-key="{esc(chk["key"])}" data-eid="{esc(eid)}">'
        f'<p class="stem">{esc(chk.get("prompt") or chk.get("stem") or "")}</p>'
        f'{"".join(labels)}'
        f'<div class="check-actions"><button type="submit">Check</button></div>'
        f'<p class="feedback" hidden></p>'
        f'<p class="reveal" hidden><span class="mono">{esc(chk["key"])}</span></p>'
        f"{src_note}"
        f"</form>"
    )


def project_html(atoms, elements, manifest, out_path: pathlib.Path, *, meaning_atoms=None,
                 option_sets=None, options_registry=None, lesson_id=None,
                 write_coverage=True, lesson_catalog=None):
    """Write the short lesson (selected lesson node) and the full SOP dump (coverage).

    `atoms` is the SOP tree (coverage walk / spine SOP membership).
    `meaning_atoms` is an optional join catalog (form-field and instance
    citations) so composed_from can resolve across stores without copying
    into SOP atoms.json.
    `option_sets` / `options_registry` are the governed value sets keyed by
    options_ref (for closed_choice). Pass explicitly — do not silently invent
    options. Projector reads the selected lesson node, then its stamped
    scenes and check shapes; it does not re-discover pedagogy or assume
    “the ALSAP lesson is these three headings.”
    `lesson_id` selects `manifest.lessons` (default lesson if omitted).
    Extra lesson records write a sibling HTML derived from `lesson_id`;
    this function does not fork for a lesson id. Coverage dump is not a
    lesson node.
    `write_coverage` is false when projecting an extra lesson onto a derived path.
    """
    registry = options_registry if options_registry is not None else (option_sets or {})
    options_registry = registry
    option_sets = option_sets if option_sets is not None else registry
    stamp_checks(manifest, atoms, elements,
                 meaning_atoms=meaning_atoms, options_registry=options_registry)
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
    spine = apply_spine(
        manifest, atoms, elements,
        meaning_atoms=meaning_atoms, option_sets=option_sets,
        lesson_catalog=lesson_catalog,
    )
    coverage_path = sibling_coverage_path(out_path)
    derived_lesson_html = (
        out_path.name == DEFAULT_LESSON_HTML_NAME
        or out_path.name.startswith("realized_lesson_")
    )
    coverage_href = esc(coverage_path.name)
    # Coverage dump links to the default short lesson, not a catalog of extras.
    lesson_href = esc(DEFAULT_LESSON_HTML_NAME if derived_lesson_html else out_path.name)
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
        form = bool((el.get("ext") or {}).get("realized_from", {}).get("form_store"))
        out = [f'<span class="pill move-{esc(move)}{ " low" if low else ""}">{esc(move)}</span>']
        if extra:
            out.append('<span class="pill extra-occ">extra</span>')
        if form:
            out.append('<span class="pill form-occ">form</span>')
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
        rec = hosted_check(el)
        if rec:
            kicker = "Check"
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
        rec = hosted_check(el)
        if rec:
            join_bits.append(
                f'check <span class="mono">{esc(rec.get("shape") or "")}</span> · '
                f'operands on the graph'
            )
            body = check_body_html(el, by_atom, options_registry, esc)
            if not body:
                body = f'<{meaning_tag} class="meaning">{esc(meaning)}</{meaning_tag}>'
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

    def sequence_check_html(step_els, chk):
        """Projector-only order practice of the job-aid presents. No extra ele_."""
        seed = "sequence:" + ",".join(chk["correct_ids"])
        shown = shuffled_sequence_items(chk["items"], seed)
        rows = []
        for it in shown:
            rows.append(
                f'<li data-atom="{esc(it["atom_id"])}">'
                f'<div class="seq-move">'
                f'<button type="button" class="seq-up" aria-label="Move up">Up</button>'
                f'<button type="button" class="seq-down" aria-label="Move down">Down</button>'
                f'</div>'
                f'<span class="seq-text">{esc(it["text"])}</span>'
                f'</li>'
            )
        reveal = "".join(f'<li>{esc(it["text"])}</li>' for it in chk["items"])
        from_ids = ", ".join(esc(el["element_id"]) for el in step_els)
        from_atoms = ", ".join(f'<span class="mono">{esc(i)}</span>' for i in chk["correct_ids"])
        return (
            f'<section class="prim prim-check sequence-check">'
            f'<div class="kicker">Practice</div>'
            f'<form class="check" data-shape="{esc(SHAPE_SEQUENCE)}" '
            f'data-order="{esc(",".join(chk["correct_ids"]))}" '
            f'data-eid="sequence:{esc(chk["correct_ids"][0])}">'
            f'<p class="stem">{esc(chk["prompt"])}</p>'
            f'<ol class="sequence-items">{"".join(rows)}</ol>'
            f'<div class="check-actions"><button type="submit">Check</button></div>'
            f'<p class="feedback" hidden></p>'
            f'<ol class="reveal" hidden>{reveal}</ol>'
            f'<p class="check-note">Items are the first sentences of {from_atoms}. '
            f'Correct order is <span class="mono">bindings.object.order</span> '
            f'(already taught). Projects the present '
            f'<span class="mono">ele_</span> records ({from_ids}) — no extra '
            f'occurrence, not authored <span class="mono">content.text</span>. '
            f'Shape <span class="mono">{esc(SHAPE_SEQUENCE)}</span> read from '
            f'<span class="mono">manifest.checks</span>.</p>'
            f'</form>'
            f'</section>'
        )

    def br_profile_check_html(chk):
        """Projector-only closed-choice of the instance fill. No extra ele_."""
        seed = "closed_choice:" + chk["options_ref"] + ":" + chk["key"]
        shown = shuffled_closed_choices(chk["choices"], seed)
        labels = []
        for c in shown:
            labels.append(
                f'<label class="choice">'
                f'<input type="radio" name="br_profile" value="{esc(c["text"])}">'
                f'<span class="mono">{esc(c["text"])}</span>'
                f"</label>"
            )
        form_eid = mint_extra_element_id(chk["form_atom_id"], "present")
        inst_eid = mint_extra_element_id(chk["key_atom_id"], "exemplify")
        return (
            f'<section class="prim prim-check closed-choice-check">'
            f'<div class="kicker">Practice</div>'
            f'<form class="check" data-shape="closed_choice" '
            f'data-key="{esc(chk["key"])}" '
            f'data-eid="closed_choice:{esc(chk["key_atom_id"])}">'
            f'<p class="stem">{esc(chk["prompt"])}</p>'
            f'{"".join(labels)}'
            f'<div class="check-actions"><button type="submit">Check</button></div>'
            f'<p class="feedback" hidden></p>'
            f'<p class="reveal" hidden><span class="mono">{esc(chk["key"])}</span></p>'
            f'<p class="check-note">Options are the value ids of '
            f'<span class="mono">{esc(chk["options_ref"])}</span> on '
            f'<span class="mono">{esc(chk["form_atom_id"])}</span>. '
            f'Key is the instance fill '
            f'(<span class="mono">{esc(chk["key_atom_id"])}</span> '
            f'<span class="mono">selected_value</span>). Projects the existing '
            f'<span class="mono">ele_</span> records '
            f'(<span class="mono">{esc(form_eid)}</span>, '
            f'<span class="mono">{esc(inst_eid)}</span>) — no extra occurrence, '
            f'not authored <span class="mono">content.text</span>. '
            f'Shape <span class="mono">{esc(SHAPE_CLOSED)}</span> read from '
            f'<span class="mono">manifest.checks</span>.</p>'
            f'</form>'
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
    lesson = resolve_lesson(manifest, by_eid, lesson_id=lesson_id, atoms_by_id=by_atom)
    scene_list = list(lesson["scenes"])
    lesson_end_ids = list(lesson["lesson_end_checks"])
    lesson_title = lesson["title"]
    lesson_key = lesson["lesson_id"]

    def render_beat_groups(ids):
        chunks = []
        for kind, els in group_spine_for_project(ids, by_eid):
            if kind == "job_aid":
                chunks.append(job_aid_block_html(els))
                continue
            el = els[0]
            atom = by_atom[el["composed_from"]]
            extra_cls = " extra" if is_extra_element(el) else ""
            chunks.append(card_html(el, atom, extra_cls))
        return chunks

    def render_scene_checks(scene):
        """In-scene projector-only checks from the stamped scene record."""
        chunks = []
        for shape in scene_check_refs(scene):
            rec = manifest_check(manifest, shape)
            if not rec:
                continue
            chk = resolve_check(rec, by_atom, options_registry)
            if not chk:
                continue
            if shape == SHAPE_SEQUENCE:
                assert_sequence_check_honest(chk, catalog)
                want = list((rec.get("operands") or {}).get("element_ids") or [])
                step_els = [by_eid[eid] for eid in want if eid in by_eid]
                if step_els:
                    chunks.append(sequence_check_html(step_els, chk))
            elif shape == SHAPE_CLOSED:
                assert_br_profile_check_honest(chk, by_atom, options_registry or {})
                chunks.append(br_profile_check_html(chk))
        return chunks

    eid_to_scene = {}
    for sc in scene_list:
        for eid in sc.get("element_ids") or []:
            eid_to_scene[eid] = sc.get("heading") or sc.get("role") or ""
    for eid in lesson_end_ids:
        eid_to_scene[eid] = "lesson-end"

    spine_body = []
    step_n = 0
    scene_n = 0
    if scene_list:
        for idx, sc in enumerate(scene_list):
            resolved = resolve_scene(sc, by_eid)
            inner = render_beat_groups(resolved["element_ids"])
            inner.extend(render_scene_checks(resolved))
            hidden = "" if idx == 0 else " hidden"
            spine_body.append(
                f'<section class="scene" data-scene="{esc(resolved["id"])}" '
                f'data-role="{esc(resolved["role"])}" '
                f'data-player-step="{idx}"{hidden}>'
                f'<header class="scene-head">'
                f'<p class="scene-kicker">{esc(resolved["kicker"])}</p>'
                f'<h2 class="scene-heading">{esc(resolved["heading"])}</h2>'
                f'</header>'
                f'{"".join(inner)}'
                f'</section>'
            )
        if lesson_end_ids:
            end_step = len(scene_list)
            spine_body.append(
                f'<section class="lesson-end-checks" data-player-step="{end_step}" '
                f'data-player-kind="lesson-end" hidden>'
                f'{"".join(render_beat_groups(lesson_end_ids))}'
                f'</section>'
            )
        scene_n = len(scene_list)
        step_n = scene_n + (1 if lesson_end_ids else 0)
        first_heading = scene_list[0].get("heading") or ""
        paging_id = ((lesson.get("paging") or {}).get("policy") or PAGING_POLICY)
        chrome = "suppressed" if step_n <= 1 else "next_back"
        if step_n <= 1:
            player_nav = ""
        else:
            player_nav = (
                f'<nav class="player-nav" aria-label="Scenes">'
                f'<button type="button" class="player-back" disabled>Back</button>'
                f'<p class="player-status" aria-live="polite">'
                f'{esc(first_heading)} · 1 of {scene_n}</p>'
                f'<button type="button" class="player-next">Next</button>'
                f'</nav>'
            )
        spine_main = (
            f'<div class="player" data-lesson="{esc(lesson_key)}" '
            f'data-paging="{esc(paging_id)}" '
            f'data-paging-chrome="{esc(chrome)}" '
            f'data-scene-count="{scene_n}" data-step-count="{step_n}">'
            f'{player_nav}'
            f'{"".join(spine_body)}'
            f'</div>'
        )
    else:
        spine_main = "".join(render_beat_groups(spine_ids))
    spine_rows = []
    for n, eid in enumerate(spine_ids, 1):
        el = by_eid.get(eid)
        if el is None:
            continue
        a = by_atom[el["composed_from"]]
        teaches = ", ".join((el.get("intent") or {}).get("teaches") or []) or "—"
        look = (el.get("expression") or {}).get("style_ref") or "—"
        prim = (el.get("expression") or {}).get("text_primitive") or "—"
        scene_label = eid_to_scene.get(eid, "—")
        spine_rows.append(
            f"<tr><td>{n}</td>"
            f"<td class=mono>{esc(el['element_id'])}</td>"
            f"<td class=mono>{esc(el['composed_from'])}</td>"
            f"<td>{esc((el.get('intent') or {}).get('move', ''))}</td>"
            f"<td class=mono>{esc(prim)}</td>"
            f"<td class=mono>{esc(look)}</td>"
            f"<td class=mono>{esc(teaches)}</td>"
            f"<td>{esc(a['meaning'].get('kind', ''))}</td>"
            f"<td>{esc(scene_label)}</td></tr>"
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
        "Procedure A’s job-aid presents also project a sequence practice "
        "(order those first sentences; object.order; no extra ele_). "
        "The form BR presents and instance fill also project a closed-choice "
        "(options_ref value ids; key = selected_value; no extra ele_). "
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
        "Procedure A as a job-aid step list then a sequence practice of those "
        "presents, a form-field present as body/`present` clothes then a worked "
        "example as body/`exemplify` clothes (form then instance atom via "
        "composed_from), a closed-choice of the BR profile fill in that scene, "
        "front-matter as heading/body, "
        "reinforce as the existing definition checks. Scene records on "
        "<span class=mono>spine.scenes</span> group those existing beats "
        "(front-matter / Procedure A / form BR); player chrome pages that "
        "list one named scene at a time. Coverage stays card-like. "
        if prim_counts else
        " The atom → primitives hop is owed so beats are clothes, not SOP cards. "
    )
    spine_note = (
        f" Default HTML is the short lesson spine "
        f"(<span class=mono>{esc(spine.get('policy', SPINE_POLICY))}</span>): "
        f"{spine.get('count', 0)} of {len(elements)} occurrences — document-root opening, "
        "why-this callout of purpose, teachable front-matter primaries, Procedure A as "
        "a job sequence then a sequence practice of those presents, the form "
        "fields those examples fill, a small instance example, a closed-choice "
        "of that BR profile fill, then the existing "
        "definition checks. A lesson record on <span class=mono>manifest.lessons</span> "
        "(stamped from the project catalog when present) "
        "points at <span class=mono>spine.scenes</span>; the player shows that "
        "lesson’s named scenes"
        + (" one at a time (Next/Back). " if step_n > 1 else
           " (this lesson is a single step; pager disabled). ")
        + "The object tree walk "
        "is coverage, not a second lesson node. "
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
.pill.form-occ{background:#0369a1;text-transform:none}
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
.player{margin:4px 0 24px}
.player-nav{display:flex;align-items:center;justify-content:space-between;gap:12px;
 position:sticky;top:0;background:#fff;border-bottom:1px solid var(--line);padding:10px 0 12px;
 margin:0 0 8px;z-index:2}
.player[data-paging-chrome="suppressed"] .player-nav{display:none}
.player-nav button{background:#1e3a8a;color:#fff;border:0;border-radius:6px;padding:8px 14px;
 font:inherit;font-weight:600;cursor:pointer}
.player-nav button:disabled{background:#e2e8f0;color:#94a3b8;cursor:not-allowed}
.player-status{margin:0;font-size:13px;color:var(--mut);text-align:center;flex:1}
.scene{margin:12px 0 8px;padding:4px 0 8px;border-top:3px solid var(--accent)}
.scene-head{margin:10px 0 16px}
.scene-kicker{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
 color:var(--accent);margin:0 0 4px}
.scene-heading{font-size:22px;margin:0;letter-spacing:-.02em;color:var(--ink)}
.lesson-end-checks{margin:12px 0 8px;padding-top:10px;border-top:1px dashed var(--line)}
.scene[hidden],.lesson-end-checks[hidden]{display:none !important}
.sequence-check{border:2px solid #334155;border-radius:8px;padding:16px 18px 10px;margin:16px 0;
 background:#f1f5f9}
.sequence-check .kicker{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
 color:#1e293b;margin:0 0 6px}
.sequence-check form.check .stem{font-size:16px;font-weight:650;margin:4px 0 12px}
.sequence-check ol.sequence-items{margin:0;padding:0;list-style:none}
.sequence-check ol.sequence-items li{display:grid;grid-template-columns:auto 1fr;gap:10px;
 align-items:start;padding:10px 12px;margin:8px 0;background:#fff;border:1px solid var(--line);
 border-radius:6px}
.sequence-check .seq-move{display:flex;flex-direction:column;gap:4px}
.sequence-check .seq-move button{background:#e2e8f0;color:#0f172a;border:0;border-radius:4px;
 padding:4px 8px;font:inherit;font-size:12px;font-weight:600;cursor:pointer}
.sequence-check .seq-move button:hover{background:#cbd5e1}
.sequence-check .seq-text{font-size:14.5px;line-height:1.45}
.sequence-check ol.reveal{margin:10px 0 0;padding:8px 10px 8px 28px;background:#fff;
 border-left:3px solid #1e3a8a;font-size:13.5px}
.closed-choice-check{border:2px solid #334155;border-radius:8px;padding:16px 18px 10px;margin:16px 0;
 background:#f1f5f9}
.closed-choice-check .kicker{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
 color:#1e293b;margin:0 0 6px}
.closed-choice-check form.check .stem{font-size:16px;font-weight:650;margin:4px 0 12px}
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

    CHECK_SCRIPT = r"""
(function () {
  function norm(s) {
    return (s || "").replace(/\s+/g, " ").trim().toLowerCase();
  }
  document.querySelectorAll("form.check").forEach(function (form) {
    form.querySelectorAll(".seq-up").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var li = btn.closest("li");
        if (li && li.previousElementSibling) {
          li.parentNode.insertBefore(li, li.previousElementSibling);
        }
      });
    });
    form.querySelectorAll(".seq-down").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var li = btn.closest("li");
        if (li && li.nextElementSibling) {
          li.parentNode.insertBefore(li.nextElementSibling, li);
        }
      });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fb = form.querySelector(".feedback");
      var reveal = form.querySelector(".reveal");
      var shape = form.getAttribute("data-shape");
      var key = form.getAttribute("data-key");
      var ok = false;
      if (shape === "invert_definition" && !form.querySelector(".cloze-in")) {
        var picked = form.querySelector("input[type=radio]:checked");
        if (!picked) {
          fb.hidden = false;
          fb.className = "feedback";
          fb.textContent = "Pick an answer to check.";
          return;
        }
        ok = picked.value === "key";
        fb.hidden = false;
        fb.className = "feedback " + (ok ? "ok" : "no");
        fb.textContent = ok
          ? "Correct — that wording is this atom."
          : "Not yet. Distractors (if any) are sibling atoms in this store; the key is this atom’s own wording.";
      } else if (shape === "closed_choice") {
        var pickedChoice = form.querySelector("input[type=radio]:checked");
        if (!pickedChoice) {
          fb.hidden = false;
          fb.className = "feedback";
          fb.textContent = "Pick an answer to check.";
          return;
        }
        ok = pickedChoice.value === key;
        fb.hidden = false;
        fb.className = "feedback " + (ok ? "ok" : "no");
        fb.textContent = ok
          ? "Correct — that is the fill already shown."
          : "Not yet. Options are the form field’s closed value set; the key is the instance fill already shown.";
      } else if (shape === "sequence_order") {
        var want = (form.getAttribute("data-order") || "").split(",");
        var got = [];
        form.querySelectorAll(".sequence-items li").forEach(function (li) {
          got.push(li.getAttribute("data-atom"));
        });
        ok = got.join(",") === want.join(",");
        fb.hidden = false;
        fb.className = "feedback " + (ok ? "ok" : "no");
        fb.textContent = ok
          ? "Correct — that is the order of these atoms."
          : "Not yet. The order is the sequence already taught (these atoms’ object.order).";
      } else {
        var typed = form.querySelector("input[type=text]");
        ok = typed && norm(typed.value) === norm(key);
        fb.hidden = false;
        fb.className = "feedback " + (ok ? "ok" : "no");
        fb.textContent = ok
          ? "Correct — that wording is this atom."
          : "Not yet. Distractors (if any) are sibling atoms in this store; the key is this atom’s own wording.";
      }
      if (reveal) reveal.hidden = false;
    });
  });
})();
""".strip()

    PLAYER_SCRIPT = r"""
(function () {
  var player = document.querySelector(".player");
  if (!player) return;
  var steps = Array.prototype.slice.call(player.querySelectorAll("[data-player-step]"));
  if (!steps.length) return;
  steps.sort(function (a, b) {
    return Number(a.getAttribute("data-player-step")) - Number(b.getAttribute("data-player-step"));
  });
  var back = player.querySelector(".player-back");
  var next = player.querySelector(".player-next");
  var status = player.querySelector(".player-status");
  var sceneCount = Number(player.getAttribute("data-scene-count") || 0);
  var i = 0;
  function sceneNumber(idx) {
    var n = 0;
    for (var k = 0; k <= idx; k++) {
      if (steps[k].classList.contains("scene")) n++;
    }
    return n;
  }
  function headingOf(el) {
    var h = el.querySelector(".scene-heading");
    return h ? (h.textContent || "").trim() : "";
  }
  function hashOf(el) {
    if (el.classList.contains("scene")) return el.getAttribute("data-scene") || "";
    if (el.getAttribute("data-player-kind") === "lesson-end") return "lesson-end";
    return "";
  }
  function show(n, writeHash) {
    if (n < 0) n = 0;
    if (n > steps.length - 1) n = steps.length - 1;
    i = n;
    steps.forEach(function (el, idx) {
      if (idx === i) el.removeAttribute("hidden");
      else el.setAttribute("hidden", "");
    });
    if (back) back.disabled = i === 0;
    if (next) next.disabled = i === steps.length - 1;
    var cur = steps[i];
    var isScene = cur.classList.contains("scene");
    if (status) {
      status.textContent = isScene
        ? headingOf(cur) + " · " + sceneNumber(i) + " of " + sceneCount
        : "";
    }
    if (writeHash && history.replaceState) {
      var hash = hashOf(cur);
      history.replaceState(null, "", hash ? "#" + hash : location.pathname + location.search);
    }
  }
  function stepFromHash() {
    var hash = (location.hash || "").replace(/^#/, "");
    if (!hash) return 0;
    for (var k = 0; k < steps.length; k++) {
      if (hashOf(steps[k]) === hash) return k;
    }
    return 0;
  }
  if (back) back.addEventListener("click", function () { show(i - 1, true); });
  if (next) next.addEventListener("click", function () { show(i + 1, true); });
  window.addEventListener("hashchange", function () { show(stepFromHash(), false); });
  show(stepFromHash(), false);
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
        f"{' Procedure A presents also project a sequence practice (same spec; no extra ele_).' if check_n else ''} "
        f"{' Form BR presents + instance fill also project a closed-choice (same spec; no extra ele_).' if (spine.get('br_profile_check')) else ''} "
        f"{' Compiler primitives: ' + prim_bits + '.' if prim_bits else ''} "
        f"Spine heuristic: <span class=mono>{esc(SPINE_SPEC)}</span>."
        f"{' Lesson: ' + esc(LESSON_POLICY) + ' (' + esc(LESSON_SPEC) + ').' if lesson_key else ''}"
        f"{' Scenes: ' + esc(SCENE_GRAPH_POLICY) + ' (' + esc(SCENE_SPEC) + ').' if scene_list else ''}"
        f"{' Player: ' + esc(PAGING_POLICY) + '.' if scene_list else ''}"
    )

    def render_page(page_title, heading, nav, path_line, main, details_html, extra_script=""):
        script = CHECK_SCRIPT + (("\n" + extra_script) if extra_script else "")
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
            f"</div><script>{script}</script></body></html>"
        )

    project_name = esc(manifest.get("project", "course"))
    spine_n = spine.get("count", 0)
    store_n = len(elements)
    lesson_details = (
        f"<details open><summary>Spine membership — {spine_n} ele_ records "
        f"(heuristic <span class=mono>{esc(SPINE_POLICY)}</span>)</summary>"
        "<table><thead><tr><th>#</th><th>element_id</th><th>composed_from</th>"
        "<th>move</th><th>primitive</th><th>style_ref</th><th>teaches</th><th>atom kind</th>"
        "<th>scene</th></tr></thead>"
        f"<tbody>{''.join(spine_rows)}</tbody></table></details>"
    )
    coverage_details = (
        f"<details><summary>Occurrence index — {store_n} ele_ records (click to expand)</summary>"
        "<table><thead><tr><th>element_id</th><th>composed_from</th><th>move</th>"
        "<th>style_ref</th><th>teaches</th><th>type</th><th>atom kind</th><th>arity</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></details>"
    )
    scene_headings = [sc.get("heading") for sc in scene_list if sc.get("heading")]
    scene_path = (
        (f"{len(scene_list)} scene" + ("s" if len(scene_list) != 1 else "")
         + (" (" + ", ".join(esc(h) for h in scene_headings) + ")" if scene_headings else "")
         + " grouping the same beats. ")
        if scene_list else ""
    )
    end_bit = " Lesson-end checks are a final step." if lesson_end_ids else ""
    if step_n <= 1:
        page_bit = "One named scene (pager disabled — this lesson is a single step)."
    else:
        page_bit = "One named scene at a time (Next/Back)."
    lesson_heading = esc(lesson_title)
    lesson_html = render_page(
        f"{lesson_heading} — {project_name}",
        lesson_heading,
        f'<a href="{coverage_href}">Full SOP / coverage ({store_n} occurrences)</a>',
        (f"{spine_n} of {store_n} occurrences · lesson <span class=mono>{esc(lesson_key)}</span> · "
         f"{scene_path}"
         f"{page_bit}"
         f"{end_bit} "
         "Read from the lesson node and its scenes — not a hard-coded ALSAP trio. "
         "Not B/C and not the SOP dump. Heuristic is documented, not an LLM."),
        spine_main,
        lesson_details,
        extra_script=PLAYER_SCRIPT,
    )
    coverage_html = render_page(
        f"Coverage dump — {project_name}",
        "Full SOP / coverage",
        f'<a href="{lesson_href}">{lesson_heading}</a>',
        (f"Every occurrence in document order ({store_n} ele_ records). "
         "This is coverage, not a second lesson node. The short path is the other file."),
        "".join(body),
        coverage_details,
    )
    out_path.write_text(lesson_html)
    if write_coverage:
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
    results.append(("general check shape is invert_definition",
                    chk_g and chk_g["shape"] == SHAPE_INVERT, chk_g and chk_g.get("shape")))
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
    results.append(("purpose check shape is invert_definition",
                    chk_p and chk_p["shape"] == SHAPE_INVERT, chk_p and chk_p.get("shape")))
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
    results.append(("procedure A steps have no copula invert — skip sibling MCQ",
                    all(not supports_honest_sibling_check(s, store)
                        for s in (step, step2, step3, step4)),
                    [copula_parts(first_sentence(s["meaning"]["source_text"]))
                     for s in (step, step2, step3, step4)]))
    seq_chk = derive_sequence_check([step, step2, step3, step4])
    assert_sequence_check_honest(seq_chk, store)
    results.append(("procedure A sequence shape is sequence_order not invert",
                    seq_chk and seq_chk["shape"] == SHAPE_SEQUENCE, seq_chk and seq_chk.get("shape")))
    results.append(("sequence items are first sentences of the four A atoms",
                    seq_chk and [it["atom_id"] for it in seq_chk["items"]] == [
                        "atom_sop_ast29080_proc_a_s1",
                        "atom_sop_ast29080_proc_a_s2",
                        "atom_sop_ast29080_proc_a_s3",
                        "atom_sop_ast29080_proc_a_s4",
                    ]
                    and all(phrase_in_atom(it["text"], by)
                            for it, by in zip(seq_chk["items"], (step, step2, step3, step4))),
                    seq_chk and [it["text"][:40] for it in seq_chk["items"]]))
    results.append(("sequence order is object.order",
                    seq_chk and seq_chk["correct_ids"] == [
                        "atom_sop_ast29080_proc_a_s1",
                        "atom_sop_ast29080_proc_a_s2",
                        "atom_sop_ast29080_proc_a_s3",
                        "atom_sop_ast29080_proc_a_s4",
                    ]
                    and [it["order"] for it in seq_chk["items"]] == [0, 1, 2, 3],
                    seq_chk and seq_chk.get("correct_ids")))
    results.append(("sequence prompt is task clothes not an SOP stem",
                    seq_chk and seq_chk["prompt"] == "Put these in the order already taught."
                    and "first planning" not in seq_chk["prompt"].lower(),
                    seq_chk and seq_chk.get("prompt")))
    results.append(("sequence check of one atom is refused",
                    derive_sequence_check([step]) is None, ""))
    shuffled = shuffled_sequence_items(seq_chk["items"], "sequence:" + ",".join(seq_chk["correct_ids"]))
    results.append(("sequence shuffle is not identity so the learner can be wrong",
                    [it["atom_id"] for it in shuffled] != seq_chk["correct_ids"],
                    [it["atom_id"] for it in shuffled]))

    fixture_br_options = {
        "reg_benefit_risk_profile": {
            "id": "reg_benefit_risk_profile",
            "values": [
                {"id": "favorable"},
                {"id": "unfavorable"},
                {"id": "uncertain_inconclusive"},
                {"id": "conditional_favorable"},
                {"id": "contextual"},
                {"id": "other_smt_defined"},
            ],
        }
    }
    br_form = {
        "atom_id": BR_PROFILE_FORM_ATOM_ID,
        "meaning": {
            "source_locale": "en",
            "source_text": "SMT assessment of the overall Benefit-Risk profile of the asset.",
            "kind": "form_field",
        },
        "bindings": {"form": {"options_ref": "reg_benefit_risk_profile", "field_type": "select_one"}},
    }
    br_inst = {
        "atom_id": BR_PROFILE_INSTANCE_ATOM_ID,
        "meaning": {
            "source_locale": "en",
            "source_text": "conditional_favorable",
            "kind": "instance_value",
        },
        "bindings": {
            "instance": {
                "instantiates": BR_PROFILE_FORM_ATOM_ID,
                "selected_value": "conditional_favorable",
            }
        },
    }
    br_chk = derive_br_profile_check(br_form, br_inst, fixture_br_options)
    assert_br_profile_check_honest(
        br_chk, {br_form["atom_id"]: br_form, br_inst["atom_id"]: br_inst}, fixture_br_options
    )
    results.append(("BR check shape is closed_choice not mcq_siblings",
                    br_chk and br_chk["shape"] == "closed_choice", br_chk and br_chk.get("shape")))
    results.append(("BR prompt is task clothes not an SOP stem",
                    br_chk and br_chk["prompt"] == BR_CHECK_PROMPT
                    and "first planning" not in br_chk["prompt"].lower()
                    and "should" not in br_chk["prompt"].lower()
                    and "required" not in br_chk["prompt"].lower(),
                    br_chk and br_chk.get("prompt")))
    results.append(("BR key is the instance selected_value already in the atom",
                    br_chk and br_chk["key"] == "conditional_favorable"
                    and phrase_in_atom(br_chk["key"], br_inst), br_chk and br_chk.get("key")))
    results.append(("BR options are the verbatim registry value ids",
                    br_chk and [c["text"] for c in br_chk["choices"]] == [
                        "favorable", "unfavorable", "uncertain_inconclusive",
                        "conditional_favorable", "contextual", "other_smt_defined",
                    ], br_chk and [c["text"] for c in br_chk["choices"]]))
    results.append(("BR check of a field with no options_ref is refused",
                    derive_br_profile_check(
                        {**br_form, "bindings": {"form": {"field_type": "text_long"}}},
                        br_inst, fixture_br_options,
                    ) is None, ""))
    results.append(("BR check of rationale (no closed set) is refused",
                    derive_br_profile_check(
                        {
                            "atom_id": FORM_FIELD_SEED[1][0],
                            "meaning": {"kind": "form_field", "source_text": "Rationale."},
                            "bindings": {"form": {"field_type": "text_long"}},
                        },
                        {
                            "atom_id": INSTANCE_EXAMPLE_SEED[1][0],
                            "meaning": {"kind": "instance_value", "source_text": "authored judgment"},
                            "bindings": {"instance": {"instantiates": FORM_FIELD_SEED[1][0]}},
                        },
                        fixture_br_options,
                    ) is None, ""))
    results.append(("BR check whose key is not in the closed set is refused",
                    derive_br_profile_check(
                        br_form,
                        {**br_inst, "meaning": {**br_inst["meaning"], "source_text": "invented_seventh"},
                         "bindings": {"instance": {
                             "instantiates": BR_PROFILE_FORM_ATOM_ID,
                             "selected_value": "invented_seventh",
                         }}},
                        fixture_br_options,
                    ) is None, ""))
    br_shown = shuffled_closed_choices(br_chk["choices"], "closed_choice:" + br_chk["options_ref"] + ":" + br_chk["key"])
    results.append(("BR shuffle is not identity so the learner can be wrong",
                    [c["text"] for c in br_shown] != [c["text"] for c in br_chk["choices"]]
                    and not br_shown[0]["correct"],
                    [c["text"] for c in br_shown]))
    results.append(("spine is a subset of existing ele_ ids", set(got_spine) <= seeded_ids, ""))
    mf_spine = {}
    apply_spine(mf_spine, store, seeded)
    apply_spine(mf_spine, store, seeded)
    stamp_checks(mf_spine, store, seeded)
    results.append(("spine recompute is stable",
                    mf_spine["spine"]["element_ids"] == want_spine, mf_spine["spine"]["element_ids"]))
    scenes0 = (mf_spine.get("spine") or {}).get("scenes") or {}
    scene_roles0 = [s["role"] for s in scenes0.get("scenes") or []]
    results.append(("spine scenes are front-matter then Procedure A (no form in fixture)",
                    scene_roles0 == [SCENE_FRONT_MATTER, SCENE_PROCEDURE_A], scene_roles0))
    results.append(("scene headings are role labels not outcome language",
                    [s["heading"] for s in scenes0.get("scenes") or []]
                    == ["What an ALSAP is", "How an ALSAP starts"]
                    and all("will be able" not in (s.get("heading") or "").lower()
                            and "learning outcome" not in (s.get("from") or "").lower()
                            for s in scenes0.get("scenes") or []),
                    [s.get("heading") for s in scenes0.get("scenes") or []]))
    results.append(("definition checks stay lesson-end not in a fourth scene",
                    scenes0.get("lesson_end_checks") == [
                        "ele_sop_ast29080_purpose__reinforce",
                        "ele_sop_ast29080_general__reinforce",
                    ], scenes0.get("lesson_end_checks")))
    results.append(("Procedure A scene lists sequence_order and the four presents",
                    any(s["role"] == SCENE_PROCEDURE_A
                        and SHAPE_SEQUENCE in scene_check_refs(s)
                        and s["element_ids"] == [
                            "ele_sop_ast29080_proc_a_s1",
                            "ele_sop_ast29080_proc_a_s2",
                            "ele_sop_ast29080_proc_a_s3",
                            "ele_sop_ast29080_proc_a_s4",
                        ]
                        for s in scenes0.get("scenes") or []),
                    [s for s in scenes0.get("scenes") or [] if s["role"] == SCENE_PROCEDURE_A]))
    results.append(("scene grouping does not change spine membership",
                    scenes0.get("policy") == SCENE_GRAPH_POLICY
                    and scenes0.get("heuristic") == SCENE_POLICY
                    and set(sum((s["element_ids"] for s in scenes0.get("scenes") or []), [])
                            + list(scenes0.get("lesson_end_checks") or []))
                    == set(want_spine), ""))
    paging0 = scenes0.get("paging") or {}
    results.append(("paging still pages the first-class scene list",
                    paging0.get("policy") == PAGING_POLICY
                    and paging0.get("scene_count") == 2
                    and paging0.get("step_count") == 3
                    and paging0.get("lesson_end_is_final_step") is True
                    and scenes0.get("policy") == SCENE_GRAPH_POLICY, paging0))
    seeded_by_eid = {e["element_id"]: e for e in seeded}
    resolved_scenes0 = [resolve_scene(s, seeded_by_eid) for s in scenes0.get("scenes") or []]
    results.append(("scene operands resolve from the graph (not hardcoded HTML)",
                    resolved_scenes0
                    and all(el["element_id"] in seeded_by_eid for sc in resolved_scenes0
                            for el in sc["elements"])
                    and [el["element_id"] for el in resolved_scenes0[0]["elements"]]
                    == scenes0["scenes"][0]["element_ids"],
                    [sc["element_ids"] for sc in resolved_scenes0]))
    fm_host = next(e for e in seeded if e["element_id"] == "ele_sop_ast29080")
    proc_host = next(e for e in seeded if e["element_id"] == "ele_sop_ast29080_proc_a_s1")
    end_host = next(e for e in seeded if e["element_id"] == "ele_sop_ast29080_purpose__reinforce")
    results.append(("ext.scene is stamped on scene members not lesson-end checks",
                    hosted_scene(fm_host)
                    and hosted_scene(fm_host).get("id") == "what_an_alsap_is"
                    and hosted_scene(proc_host)
                    and hosted_scene(proc_host).get("id") == "how_an_alsap_starts"
                    and hosted_scene(end_host) is None,
                    (hosted_scene(fm_host), hosted_scene(end_host))))
    lessons0 = mf_spine.get("lessons") or {}
    default0 = (lessons0.get("lessons") or [{}])[0]
    store_atoms = {a["atom_id"]: a for a in store}
    resolved_lesson0 = resolve_lesson(mf_spine, seeded_by_eid, atoms_by_id=store_atoms)
    flat0 = [eid for sc in resolved_lesson0["scenes"] for eid in sc["element_ids"]] + list(
        resolved_lesson0["lesson_end_checks"]
    )
    results.append(("default lesson record points at spine.scenes",
                    lessons0.get("policy") == LESSON_POLICY
                    and lessons0.get("spec") == LESSON_SPEC
                    and lessons0.get("default") == "course_short"
                    and default0.get("lesson_id") == "course_short"
                    and default0.get("scene_ids") == [s["id"] for s in scenes0.get("scenes") or []]
                    and default0.get("scenes") == {"see": "spine.scenes"}
                    and default0.get("title_from") == "atom_sop_ast29080"
                    and "will be able" not in (default0.get("title") or "").lower(),
                    default0))
    results.append(("lesson → scenes → element_ids resolve from the graph",
                    resolved_lesson0["lesson_id"] == "course_short"
                    and [sc["id"] for sc in resolved_lesson0["scenes"]]
                    == [s["id"] for s in scenes0.get("scenes") or []]
                    and flat0 == want_spine
                    and all(eid in seeded_by_eid for eid in flat0),
                    {"scene_ids": [sc["id"] for sc in resolved_lesson0["scenes"]], "flat": flat0}))
    results.append(("lesson title heuristic is the document-root atom not outcome language",
                    resolved_lesson0["title_from"] == "atom_sop_ast29080"
                    and "SOP-X" not in resolved_lesson0["title"]
                    and "Plan, Develop, Execute" in resolved_lesson0["title"]
                    and "will be able" not in resolved_lesson0["title"].lower(),
                    resolved_lesson0["title"]))
    mf_spine.setdefault("lessons", {}).setdefault("lessons", []).append({
        "lesson_id": "front_only",
        "title": "Front matter only",
        "title_from": "atom_sop_ast29080",
        "scene_ids": ["what_an_alsap_is"],
        "lesson_end_check_ids": [],
    })
    apply_spine(mf_spine, store, seeded)
    kept_ids = [L.get("lesson_id") for L in (mf_spine.get("lessons") or {}).get("lessons") or []]
    results.append(("re-stamp preserves extra lesson records and recomputes the default",
                    "front_only" in kept_ids
                    and kept_ids[0] == "course_short"
                    and (mf_spine.get("lessons") or {}).get("default") == "course_short",
                    kept_ids))
    resolved_front = resolve_lesson(
        mf_spine, seeded_by_eid, lesson_id="front_only", atoms_by_id=store_atoms
    )
    results.append(("extra lesson resolves a subset of scenes not the hard-coded trio",
                    resolved_front["lesson_id"] == "front_only"
                    and [sc["id"] for sc in resolved_front["scenes"]] == ["what_an_alsap_is"]
                    and not resolved_front["lesson_end_checks"]
                    and resolved_front["title"] == "Front matter only",
                    [sc["id"] for sc in resolved_front["scenes"]]))
    rebuilt = {"project": "course"}
    carry_previous_lesson_records(rebuilt, mf_spine)
    apply_spine(rebuilt, store, seeded)
    rebuilt_ids = [L.get("lesson_id") for L in (rebuilt.get("lessons") or {}).get("lessons") or []]
    results.append(("realize-style rebuild carries extra lesson records from previous manifest",
                    "front_only" in rebuilt_ids
                    and rebuilt_ids[0] == "course_short"
                    and (rebuilt.get("lessons") or {}).get("default") == "course_short",
                    rebuilt_ids))
    named = {
        "project": "ast_alsap",
        "lessons": {
            "default": "ast_alsap_short",
            "lessons": [
                {"lesson_id": "ast_alsap_short", "default": True, "scene_ids": ["what_an_alsap_is"]},
                {"lesson_id": "ast_alsap_br", "scene_ids": ["benefit_risk_on_the_form"]},
                {"lesson_id": "ast_alsap_plan", "scene_ids": ["how_an_alsap_starts"]},
            ],
        },
    }
    results.append(("extra lesson html filename is derived from lesson_id not a fork",
                    lesson_html_filename(named, "ast_alsap_short") == DEFAULT_LESSON_HTML_NAME
                    and lesson_html_filename(named, "ast_alsap_br") == "realized_lesson_br.html"
                    and lesson_html_filename(named, "ast_alsap_plan") == "realized_lesson_plan.html"
                    and lesson_html_filename(named) == DEFAULT_LESSON_HTML_NAME, ""))
    cat_small = {
        "policy": LESSON_CATALOG_POLICY,
        "default": "course_short",
        "lessons": [
            {"lesson_id": "course_short", "default": True},
            {"lesson_id": "course_plan", "scene_ids": ["how_an_alsap_starts"]},
        ],
    }
    mf_cat = {"project": "course"}
    mf_cat.setdefault("lessons", {}).setdefault("lessons", []).append({
        "lesson_id": "stale_extra",
        "title": "stale",
        "scene_ids": ["what_an_alsap_is"],
        "lesson_end_check_ids": [],
    })
    apply_spine(mf_cat, store, seeded, lesson_catalog=cat_small)
    cat_ids = [L.get("lesson_id") for L in (mf_cat.get("lessons") or {}).get("lessons") or []]
    results.append(("catalog stamps default plus extras and drops stale stamp-only records",
                    cat_ids == ["course_short", "course_plan"]
                    and (mf_cat.get("lessons") or {}).get("catalog", {}).get("see")
                    == f"occurrences/{LESSON_CATALOG_FILENAME}"
                    and (mf_cat.get("lessons") or {}).get("default") == "course_short",
                    cat_ids))
    resolved_plan0 = resolve_lesson(
        mf_cat, seeded_by_eid, lesson_id="course_plan", atoms_by_id=store_atoms
    )
    results.append(("catalog plan record resolves Procedure A scene from the graph",
                    resolved_plan0["lesson_id"] == "course_plan"
                    and [sc["id"] for sc in resolved_plan0["scenes"]] == ["how_an_alsap_starts"]
                    and not resolved_plan0["lesson_end_checks"]
                    and SHAPE_SEQUENCE in scene_check_refs(resolved_plan0["scenes"][0])
                    and (resolved_plan0["paging"] or {}).get("chrome") == "suppressed",
                    [sc["id"] for sc in resolved_plan0["scenes"]]))
    with tempfile.TemporaryDirectory() as td_cat:
        cat_path = pathlib.Path(td_cat) / LESSON_CATALOG_FILENAME
        cat_path.write_text(json.dumps(cat_small, indent=2) + "\n")
        loaded = load_lesson_catalog(td_cat)
    results.append(("catalog file loads as project data",
                    loaded is not None
                    and loaded.get("default") == "course_short"
                    and [L["lesson_id"] for L in loaded["lessons"]]
                    == ["course_short", "course_plan"],
                    loaded))
    projector_fns = (
        stamp_lessons, stamp_lessons_from_catalog, hydrate_lesson_record,
        derive_lesson_paging, project_html, project_lesson_htmls,
        lesson_html_filename, select_lesson_record, resolve_lesson,
    )
    projector_src = "\n".join(inspect.getsource(fn) for fn in projector_fns)
    results.append(("projector does not special-case extra lesson ids",
                    "ast_alsap_br" not in projector_src
                    and "ast_alsap_plan" not in projector_src,
                    ""))

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
    results.append(("lesson has two definition checks plus one sequence practice",
                    page.count('form class="check"') == 3
                    and page.count('data-shape="sequence_order"') == 1
                    and page.count(f'data-shape="{SHAPE_INVERT}"') == 2, page.count('form class="check"')))
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
    results.append(("callout is not a check",
                    page.split("ele_sop_ast29080_purpose__activate", 1)[-1]
                    .split("</article>", 1)[0].count('form class="check"') == 0, ""))
    results.append(("coverage dump stays card-like (no job-aid grouping)",
                    "class=\"prim prim-step job-aid\"" not in cov_page
                    and "ele_sop_ast29080_proc_a_s1" in cov_page, ""))
    results.append(("coverage dump has no sequence practice (lesson-only projection)",
                    'data-shape="sequence_order"' not in cov_page
                    and 'data-shape="closed_choice"' not in cov_page, ""))
    results.append(("lesson HTML names two scenes from SOP roles (no form in fixture)",
                    page.count('class="scene-heading">What an ALSAP is</h2>') == 1
                    and page.count('class="scene-heading">How an ALSAP starts</h2>') == 1
                    and "Benefit-risk on the form" not in page, ""))
    results.append(("lesson scene kickers are graph roles not outcomes",
                    ">Front matter</p>" in page
                    and ">Procedure A</p>" in page
                    and "will be able" not in page.lower(), ""))
    results.append(("lesson HTML is a read of the default lesson node",
                    'data-lesson="selftest_short"' in page
                    and "Plan, Develop, Execute" in page
                    and page.find("<h1>") != -1
                    and "will be able" not in page[page.find("<h1>"):page.find("</h1>") + 5].lower(),
                    ""))
    mf_front = {"project": "selftest"}
    apply_spine(mf_front, store, seeded)
    mf_front["lessons"]["lessons"].append({
        "lesson_id": "front_only",
        "title": "Front matter only",
        "title_from": "atom_sop_ast29080",
        "scene_ids": ["what_an_alsap_is"],
        "lesson_end_check_ids": [],
    })
    with tempfile.TemporaryDirectory() as td_front:
        front_path = pathlib.Path(td_front) / "realized_lesson.html"
        project_html(store, seeded, mf_front, front_path, lesson_id="front_only")
        page_front = front_path.read_text()
    results.append(("projector reads --lesson scene_ids not a hard-coded ALSAP trio",
                    'data-lesson="front_only"' in page_front
                    and page_front.count('class="scene"') == 1
                    and 'data-scene="what_an_alsap_is"' in page_front
                    and 'data-scene="how_an_alsap_starts"' not in page_front
                    and "Benefit-risk on the form" not in page_front
                    and "<h1>Front matter only</h1>" in page_front
                    and 'class="lesson-end-checks"' not in page_front, ""))
    results.append(("single-scene extra lesson suppresses the pager",
                    'data-paging-chrome="suppressed"' in page_front
                    and 'data-scene-count="1"' in page_front
                    and 'data-step-count="1"' in page_front
                    and 'class="player-nav"' not in page_front
                    and 'class="player-next"' not in page_front
                    and "pager disabled" in page_front, ""))
    fm_start = page.find('data-scene="what_an_alsap_is"')
    proc_start = page.find('data-scene="how_an_alsap_starts"')
    end_start = page.find('class="lesson-end-checks"')
    fm_chunk = page[fm_start:proc_start] if fm_start != -1 and proc_start != -1 else ""
    proc_chunk = page[proc_start:end_start] if proc_start != -1 and end_start != -1 else ""
    end_chunk = page[end_start:] if end_start != -1 else ""
    results.append(("front-matter scene holds title, callout, purpose, scope, general",
                    all(eid in fm_chunk for eid in (
                        "ele_sop_ast29080",
                        "ele_sop_ast29080__present",
                        "ele_sop_ast29080_purpose__activate",
                        "ele_sop_ast29080_purpose",
                        "ele_sop_ast29080_scope",
                        "ele_sop_ast29080_general",
                    ))
                    and "ele_sop_ast29080_proc_a_s1" not in fm_chunk
                    and "ele_sop_ast29080_purpose__reinforce" not in fm_chunk, ""))
    results.append(("Procedure A scene holds the job-aid and the sequence practice",
                    "ele_sop_ast29080_proc_a_s1" in proc_chunk
                    and "ele_sop_ast29080_proc_a_s4" in proc_chunk
                    and 'data-shape="sequence_order"' in proc_chunk
                    and "ele_sop_ast29080_purpose__reinforce" not in proc_chunk, ""))
    results.append(("definition checks sit after the scenes at lesson end",
                    "ele_sop_ast29080_purpose__reinforce" in end_chunk
                    and "ele_sop_ast29080_general__reinforce" in end_chunk
                    and page.find('data-scene="how_an_alsap_starts"')
                    < page.find('class="lesson-end-checks"')
                    < page.find("ele_sop_ast29080_purpose__reinforce"), ""))
    results.append(("coverage dump has no scene chrome",
                    'class="scene-heading"' not in cov_page
                    and 'class="scene"' not in cov_page, ""))
    fm_tag = re.search(r'<section class="scene" data-scene="what_an_alsap_is"[^>]*>', page)
    proc_tag = re.search(r'<section class="scene" data-scene="how_an_alsap_starts"[^>]*>', page)
    end_tag = re.search(r'<section class="lesson-end-checks"[^>]*>', page)
    results.append(("lesson HTML has player chrome Next/Back",
                    'class="player"' in page
                    and f'data-paging="{PAGING_POLICY}"' in page
                    and 'class="player-next"' in page
                    and 'class="player-back"' in page
                    and 'data-scene-count="2"' in page
                    and 'data-step-count="3"' in page, ""))
    results.append(("first scene is the visible player step",
                    bool(fm_tag) and "hidden" not in fm_tag.group(0)
                    and fm_tag.group(0).find('data-player-step="0"') != -1,
                    fm_tag.group(0) if fm_tag else ""))
    results.append(("later scenes and lesson-end start hidden",
                    bool(proc_tag) and "hidden" in proc_tag.group(0)
                    and proc_tag.group(0).find('data-player-step="1"') != -1
                    and bool(end_tag) and "hidden" in end_tag.group(0)
                    and end_tag.group(0).find('data-player-kind="lesson-end"') != -1,
                    (proc_tag.group(0) if proc_tag else "", end_tag.group(0) if end_tag else "")))
    results.append(("coverage dump has no player chrome",
                    'class="player"' not in cov_page
                    and 'class="player-nav"' not in cov_page
                    and 'class="player-next"' not in cov_page, ""))
    results.append(("player chrome does not invent a fourth scene heading",
                    page.count('class="scene-heading">') == 2
                    and "will be able" not in page.lower(), page.count('class="scene-heading">')))
    results.append(("HTML scene headings are a read of spine.scenes not a hardcoded string",
                    all(f'data-scene="{s["id"]}"' in page
                        and f'class="scene-heading">{s["heading"]}</h2>' in page
                        for s in scenes0.get("scenes") or [])
                    and all(eid in page for s in scenes0.get("scenes") or []
                            for eid in s["element_ids"]),
                    [s.get("id") for s in scenes0.get("scenes") or []]))
    results.append(("lesson sequence practice sits after the job aid",
                    page.find('class="prim prim-step job-aid"')
                    < page.find('data-shape="sequence_order"')
                    < page.find("ele_sop_ast29080_purpose__reinforce"), ""))
    results.append(("lesson sequence items are the four A first sentences",
                    'data-atom="atom_sop_ast29080_proc_a_s1"' in page
                    and 'data-atom="atom_sop_ast29080_proc_a_s2"' in page
                    and 'data-atom="atom_sop_ast29080_proc_a_s3"' in page
                    and 'data-atom="atom_sop_ast29080_proc_a_s4"' in page
                    and "Notify a member of Safety Data Science" in page
                    and "Schedule and conduct the ALSAP Kick-Off Meeting" in page, ""))
    results.append(("lesson sequence does not invent a planning-step MCQ stem",
                    "first planning step" not in page.lower()
                    and "Which is the first" not in page
                    and "Put these in the order already taught." in page, ""))
    results.append(("lesson sequence kicker is Practice not a new retrieve enum",
                    ">Practice</div>" in page
                    and "retrieve" not in page, ""))
    seq_section = page.split('data-shape="sequence_order"', 1)[-1].split("</form>", 1)[0]
    shown_ids = re.findall(r'data-atom="([^"]+)"', seq_section)
    results.append(("lesson sequence initial order is shuffled",
                    shown_ids != [
                        "atom_sop_ast29080_proc_a_s1",
                        "atom_sop_ast29080_proc_a_s2",
                        "atom_sop_ast29080_proc_a_s3",
                        "atom_sop_ast29080_proc_a_s4",
                    ]
                    and set(shown_ids) == {
                        "atom_sop_ast29080_proc_a_s1",
                        "atom_sop_ast29080_proc_a_s2",
                        "atom_sop_ast29080_proc_a_s3",
                        "atom_sop_ast29080_proc_a_s4",
                    }, shown_ids))
    results.append(("spine sequence_check stamp names the four presents",
                    (mf_spine.get("spine") or {}).get("sequence_check", {}).get("from_atom_ids")
                    == [
                        "atom_sop_ast29080_proc_a_s1",
                        "atom_sop_ast29080_proc_a_s2",
                        "atom_sop_ast29080_proc_a_s3",
                        "atom_sop_ast29080_proc_a_s4",
                    ], (mf_spine.get("spine") or {}).get("sequence_check")))

    profile_inst = {
        "atom_id": INSTANCE_EXAMPLE_SEED[0][0],
        "content_hash": "sha256:" + ("c" * 64),
        "meaning": {
            "source_locale": "en",
            "source_text": "conditional_favorable",
            "kind": "instance_value",
        },
        "bindings": {
            "instance": {
                "instantiates": FORM_FIELD_SEED[0][0],
                "selected_value": "conditional_favorable",
                "authored_by": "role_smt",
            }
        },
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
    results.append(("instance example is not a fourth job-aid card",
                    page_inst.count('class="prim prim-step job-aid"') == 1, ""))
    results.append(("instance example sits after sequence practice and before definition checks",
                    page_inst.find("ele_sop_ast29080_proc_a_s4")
                    < page_inst.find('data-shape="sequence_order"')
                    < page_inst.find(inst_eids[0])
                    < page_inst.find("ele_sop_ast29080_purpose__reinforce"), ""))
    results.append(("instance lesson has sequence practice plus two definition checks",
                    page_inst.count('form class="check"') == 3
                    and page_inst.count('data-shape="sequence_order"') == 1, page_inst.count('form class="check"')))

    profile_form = {
        "atom_id": FORM_FIELD_SEED[0][0],
        "content_hash": "sha256:" + ("f" * 64),
        "meaning": {
            "source_locale": "en",
            "source_text": "SMT assessment of the overall Benefit-Risk profile of the asset.",
            "kind": "form_field",
        },
        "bindings": {
            "object": {"belongs_to": "atom_form_ast34037_sec_purpose_sec_safety_profile", "order": 3},
            "form": {"field_type": "select_one", "options_ref": "reg_benefit_risk_profile"},
        },
        "governance": {"version": 1, "status": "draft"},
    }
    rationale_form = {
        "atom_id": FORM_FIELD_SEED[1][0],
        "content_hash": "sha256:" + ("b" * 64),
        "meaning": {
            "source_locale": "en",
            "source_text": "Rationale and phrasing for the selected Benefit-Risk profile.",
            "kind": "form_field",
        },
        "bindings": {
            "object": {"belongs_to": "atom_form_ast34037_sec_purpose_sec_safety_profile", "order": 4},
            "form": {"field_type": "text_long"},
        },
        "governance": {"version": 1, "status": "draft"},
    }
    unused_form = {
        "atom_id": "atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_guidance",
        "content_hash": "sha256:" + ("a" * 64),
        "meaning": {
            "source_locale": "en",
            "source_text": (
                "Choose from the options below to document the SMT's assessment of the "
                "overall Benefit-Risk profile of the asset."
            ),
            "kind": "form_field",
        },
        "bindings": {"object": {"belongs_to": "atom_form_ast34037_sec_purpose_sec_safety_profile", "order": 2}},
        "governance": {"version": 1, "status": "draft"},
    }
    form_store = [profile_form, rationale_form, unused_form]
    options_fixture = {
        "reg_benefit_risk_profile": {
            "id": "reg_benefit_risk_profile",
            "values": [
                {"id": "favorable", "label": "Favorable Benefit-Risk Profile"},
                {"id": "unfavorable", "label": "Unfavorable Benefit-Risk Profile"},
                {"id": "conditional_favorable", "label": "Conditional Favorable Benefit-Risk Profile"},
                {"id": "uncertain_inconclusive", "label": "Uncertain or Inconclusive Benefit-Risk Profile"},
            ],
        }
    }
    seeded_form = assemble_elements(
        store, [], DEFAULT_MOVE, mint_extras=True,
        instance_atoms=instance_store, form_atoms=form_store,
        options_registry=options_fixture,
    )
    form_eids = [
        mint_extra_element_id(FORM_FIELD_SEED[0][0], "present"),
        mint_extra_element_id(FORM_FIELD_SEED[1][0], "present"),
    ]
    unused_form_eid = mint_element_id(unused_form["atom_id"])
    unused_form_extra = mint_extra_element_id(unused_form["atom_id"], "present")
    got_spine_form = select_spine(store, seeded_form)
    results.append(("form seed mints two present extras",
                    all(eid in {e["element_id"] for e in seeded_form} for eid in form_eids),
                    sorted(e["element_id"] for e in seeded_form if "form_ast34037" in e["element_id"]
                           and "asp9999" not in e["element_id"])))
    results.append(("form extras composed_from form atom_ids",
                    all(next(e for e in seeded_form if e["element_id"] == eid)["composed_from"]
                        == aid for eid, (aid, _) in zip(form_eids, FORM_FIELD_SEED)), ""))
    results.append(("form extras stamp present not exemplify",
                    all(next(e for e in seeded_form if e["element_id"] == eid)["intent"]["move"]
                        == "present" for eid in form_eids), ""))
    results.append(("form extras carry no authored content.text",
                    all("content" not in next(e for e in seeded_form if e["element_id"] == eid)
                        for eid in form_eids), ""))
    results.append(("form extras do not stamp a parent ele_ never minted here",
                    all("parent_id" not in (next(e for e in seeded_form if e["element_id"] == eid)
                                            .get("structure") or {})
                        for eid in form_eids), ""))
    results.append(("unused form guidance atom is not minted onto the store",
                    unused_form_eid not in {e["element_id"] for e in seeded_form}
                    and unused_form_extra not in {e["element_id"] for e in seeded_form}, ""))
    results.append(("SOP atoms.json fixture is unchanged by form join",
                    all(a["atom_id"].startswith("atom_sop_") for a in store), ""))
    results.append(("spine places form presents after Procedure A and before instance examples",
                    got_spine_form[-6:] == form_eids + inst_eids + [
                        "ele_sop_ast29080_purpose__reinforce",
                        "ele_sop_ast29080_general__reinforce",
                    ]
                    and got_spine_form.index("ele_sop_ast29080_proc_a_s4")
                    < got_spine_form.index(form_eids[0])
                    < got_spine_form.index(inst_eids[0])
                    < got_spine_form.index("ele_sop_ast29080_purpose__reinforce"),
                    got_spine_form))
    results.append(("spine without form or instance store stays the original 12",
                    got_spine == want_spine and len(got_spine) == 12, len(got_spine)))
    results.append(("form_field + present is tp_body not a new primitive",
                    classify_text_primitive(profile_form, {"intent": {"move": "present"}})
                    == PRIMITIVE_BODY, ""))
    for eid in form_eids:
        el = next(e for e in seeded_form if e["element_id"] == eid)
        el["expression"] = {
            "style_ref": "brand.instructional",
            "text_primitive": "tp_body",
            "content_role": "body",
            "layout_hint": "card",
        }
    for eid in inst_eids:
        el = next(e for e in seeded_form if e["element_id"] == eid)
        el["expression"] = {
            "style_ref": "brand.example",
            "text_primitive": "tp_body",
            "content_role": "example",
            "layout_hint": "cite",
        }
    with tempfile.TemporaryDirectory() as td:
        html_path = pathlib.Path(td) / "realized_lesson.html"
        project_html(
            store, seeded_form,
            {"project": "selftest", "one_to_many": {"seeded_atom_count": 3}},
            html_path, meaning_atoms=form_store + instance_store,
            option_sets=fixture_br_options,
            options_registry=fixture_br_options,
        )
        page_form = html_path.read_text()
        cov_page_form = pathlib.Path(html_path).with_name("realized_coverage.html").read_text()
    results.append(("lesson HTML shows Present kicker on form-field beats",
                    page_form.count(">Present</div>") >= 2
                    and "style-instructional" in page_form
                    and FORM_FIELD_SEED[0][0] in page_form, page_form.count(">Present</div>")))
    results.append(("lesson HTML form meaning is the form atoms not invented text",
                    "SMT assessment of the overall Benefit-Risk profile of the asset." in page_form
                    and "Rationale and phrasing for the selected Benefit-Risk profile." in page_form, ""))
    results.append(("lesson HTML does not dump the unused form guidance atom",
                    unused_form["atom_id"] not in page_form
                    and unused_form_eid not in page_form, ""))
    results.append(("form present sits after sequence practice and before instance examples",
                    page_form.find("ele_sop_ast29080_proc_a_s4")
                    < page_form.find('data-shape="sequence_order"')
                    < page_form.find(form_eids[0])
                    < page_form.find(inst_eids[0])
                    < page_form.find("ele_sop_ast29080_purpose__reinforce"), ""))
    results.append(("form present is not example clothes",
                    page_form.split(form_eids[0], 1)[-1].split("</article>", 1)[0]
                    .find("style-example") == -1, ""))
    results.append(("form present is not a second job-aid",
                    page_form.count('class="prim prim-step job-aid"') == 1, ""))
    mf_form = {}
    apply_spine(mf_form, store, seeded_form)
    results.append(("form spine without option_sets does not invent a BR check",
                    "br_profile_check" not in (mf_form.get("spine") or {}),
                    (mf_form.get("spine") or {}).get("br_profile_check")))
    apply_spine(
        mf_form, store, seeded_form,
        meaning_atoms=form_store + instance_store, option_sets=fixture_br_options,
    )
    stamp_checks(mf_form, store, seeded_form,
                 meaning_atoms=form_store + instance_store,
                 options_registry=fixture_br_options)
    form_scenes = (mf_form.get("spine") or {}).get("scenes") or {}
    form_roles = [s["role"] for s in form_scenes.get("scenes") or []]
    results.append(("form fixture yields three scenes from SOP/form roles",
                    form_roles == [SCENE_FRONT_MATTER, SCENE_PROCEDURE_A, SCENE_FORM_BR],
                    form_roles))
    results.append(("third scene heading is Benefit-risk on the form",
                    any(s["role"] == SCENE_FORM_BR
                        and s["heading"] == "Benefit-risk on the form"
                        and s["element_ids"] == form_eids + inst_eids
                        for s in form_scenes.get("scenes") or []),
                    [s for s in form_scenes.get("scenes") or [] if s["role"] == SCENE_FORM_BR]))
    results.append(("three-scene membership still equals the spine",
                    set(sum((s["element_ids"] for s in form_scenes.get("scenes") or []), [])
                        + list(form_scenes.get("lesson_end_checks") or []))
                    == set(got_spine_form), ""))
    br_start = page_form.find('data-scene="benefit_risk_on_the_form"')
    end_form = page_form.find('class="lesson-end-checks"')
    br_chunk = page_form[br_start:end_form] if br_start != -1 and end_form != -1 else ""
    results.append(("lesson HTML names all three scenes when form+instance extras exist",
                    page_form.count('class="scene-heading">What an ALSAP is</h2>') == 1
                    and page_form.count('class="scene-heading">How an ALSAP starts</h2>') == 1
                    and page_form.count('class="scene-heading">Benefit-risk on the form</h2>') == 1, ""))
    results.append(("form BR scene holds the two presents then the two examples",
                    all(eid in br_chunk for eid in form_eids + inst_eids)
                    and br_chunk.find(form_eids[0]) < br_chunk.find(inst_eids[0])
                    and "ele_sop_ast29080_purpose__reinforce" not in br_chunk
                    and "ele_sop_ast29080_proc_a_s1" not in br_chunk, ""))
    results.append(("form lesson still parks definition checks at lesson end",
                    'class="lesson-end-checks"' in page_form
                    and page_form.find('data-scene="benefit_risk_on_the_form"')
                    < page_form.find('class="lesson-end-checks"')
                    < page_form.find("ele_sop_ast29080_purpose__reinforce"), ""))
    form_paging = form_scenes.get("paging") or {}
    results.append(("three-scene paging still leaves checks as the final step",
                    form_paging.get("policy") == PAGING_POLICY
                    and form_paging.get("scene_count") == 3
                    and form_paging.get("step_count") == 4
                    and form_paging.get("lesson_end_is_final_step") is True, form_paging))
    br_tag = re.search(r'<section class="scene" data-scene="benefit_risk_on_the_form"[^>]*>', page_form)
    end_form_tag = re.search(r'<section class="lesson-end-checks"[^>]*>', page_form)
    results.append(("form lesson pages three scenes then lesson-end",
                    f'data-paging="{PAGING_POLICY}"' in page_form
                    and 'data-scene-count="3"' in page_form
                    and 'data-step-count="4"' in page_form
                    and bool(br_tag) and "hidden" in br_tag.group(0)
                    and br_tag.group(0).find('data-player-step="2"') != -1
                    and bool(end_form_tag) and "hidden" in end_form_tag.group(0)
                    and end_form_tag.group(0).find('data-player-step="3"') != -1, ""))
    results.append(("form lesson player does not name a fourth scene",
                    page_form.count('class="scene-heading">What an ALSAP is</h2>') == 1
                    and page_form.count('class="scene-heading">How an ALSAP starts</h2>') == 1
                    and page_form.count('class="scene-heading">Benefit-risk on the form</h2>') == 1
                    and page_form.count('class="scene-heading">') == 3, page_form.count('class="scene-heading">')))
    results.append(("form BR scene lists closed_choice of the instance fill",
                    any(s["role"] == SCENE_FORM_BR
                        and SHAPE_CLOSED in scene_check_refs(s)
                        for s in form_scenes.get("scenes") or [])
                    and (mf_form.get("spine") or {}).get("br_profile_check", {}).get("key")
                    == "conditional_favorable"
                    and (mf_form.get("spine") or {}).get("br_profile_check", {}).get("options_ref")
                    == "reg_benefit_risk_profile",
                    (mf_form.get("spine") or {}).get("br_profile_check")))
    results.append(("form lesson HTML puts BR closed-choice in scene 3 after examples",
                    'data-shape="closed_choice"' in br_chunk
                    and br_chunk.find(inst_eids[0]) < br_chunk.find('data-shape="closed_choice"')
                    and "ele_sop_ast29080_purpose__reinforce" not in br_chunk
                    and 'data-shape="closed_choice"' not in page_form[end_form:], ""))
    results.append(("form lesson has sequence + BR closed-choice + two definition checks",
                    page_form.count('form class="check"') == 4
                    and page_form.count('data-shape="sequence_order"') == 1
                    and page_form.count('data-shape="closed_choice"') == 1
                    and page_form.count(f'data-shape="{SHAPE_INVERT}"') == 2,
                    page_form.count('form class="check"')))
    results.append(("BR closed-choice options are the registry ids not invented stems",
                    "Choose the closed value already shown." in br_chunk
                    and 'value="conditional_favorable"' in br_chunk
                    and 'value="favorable"' in br_chunk
                    and 'value="unfavorable"' in br_chunk
                    and 'value="uncertain_inconclusive"' in br_chunk
                    and 'value="contextual"' in br_chunk
                    and 'value="other_smt_defined"' in br_chunk
                    and "first planning step" not in page_form.lower()
                    and "which benefit-risk profile is required" not in page_form.lower()
                    and "The benefits of the investigational drug outweigh" not in page_form, ""))
    results.append(("BR closed-choice initial order is shuffled",
                    (lambda shown: shown != [
                        "favorable", "unfavorable", "uncertain_inconclusive",
                        "conditional_favorable", "contextual", "other_smt_defined",
                    ] and set(shown) == {
                        "favorable", "unfavorable", "uncertain_inconclusive",
                        "conditional_favorable", "contextual", "other_smt_defined",
                    })(re.findall(
                        r'name="br_profile" value="([^"]+)"',
                        br_chunk.split('data-shape="closed_choice"', 1)[-1].split("</form>", 1)[0]
                        if 'data-shape="closed_choice"' in br_chunk else "",
                    )),
                    re.findall(r'name="br_profile" value="([^"]+)"', br_chunk)))
    results.append(("BR feedback does not invent SOP facts",
                    "Correct — that is the fill already shown." in page_form
                    and "the instance fill already shown" in page_form
                    and "SMT should" not in page_form
                    and "hepatic monitoring" not in page_form.split('data-shape="closed_choice"', 1)[-1]
                    .split("</form>", 1)[0], ""))
    results.append(("coverage dump has no BR closed-choice",
                    'data-shape="closed_choice"' not in cov_page_form
                    and 'data-shape="sequence_order"' not in cov_page_form, ""))

    # Check shapes are first-class on the graph; projector reads operands, not if-atom-id.
    gen_host = next(e for e in seeded if e["element_id"] == "ele_sop_ast29080_general__reinforce")
    gen_stamp = hosted_check(gen_host)
    results.append(("invert_definition is stamped on the general reinforce extra",
                    gen_stamp and gen_stamp.get("shape") == SHAPE_INVERT
                    and gen_stamp.get("operands", {}).get("key_atom_id")
                    == "atom_sop_ast29080_general", gen_stamp))
    results.append(("invert operands are atom_ids not copied option strings",
                    gen_stamp and "contrast_atom_ids" in (gen_stamp.get("operands") or {})
                    and "central cross-functional framework"
                    not in json.dumps(gen_stamp.get("operands") or {}),
                    gen_stamp and gen_stamp.get("operands")))
    resolved_inv = resolve_check(gen_stamp, store_by_id)
    results.append(("invert operands resolve from the graph",
                    resolved_inv and resolved_inv["stem"] == "What is the ALSAP?"
                    and "central cross-functional framework" in resolved_inv["key"]
                    and {c["from_atom_id"] for c in resolved_inv["choices"] if not c["correct"]}
                    == set(gen_stamp["operands"]["contrast_atom_ids"]),
                    resolved_inv and resolved_inv.get("key", "")[:40]))
    results.append(("HTML invert stem is the resolved graph wording not a hardcoded string on the element",
                    resolved_inv and resolved_inv["stem"] in page
                    and "content" not in gen_host, ""))

    seq_stamp = manifest_check(mf_spine, SHAPE_SEQUENCE) or manifest_check(mf_form, SHAPE_SEQUENCE)
    results.append(("sequence_order is on the manifest checks index",
                    seq_stamp and seq_stamp.get("shape") == SHAPE_SEQUENCE
                    and seq_stamp.get("operands", {}).get("atom_ids") == [
                        "atom_sop_ast29080_proc_a_s1",
                        "atom_sop_ast29080_proc_a_s2",
                        "atom_sop_ast29080_proc_a_s3",
                        "atom_sop_ast29080_proc_a_s4",
                    ]
                    and seq_stamp.get("operands", {}).get("order_from") == "bindings.object.order",
                    seq_stamp))
    resolved_seq = resolve_check(seq_stamp, store_by_id)
    results.append(("sequence operands resolve first sentences from the graph",
                    resolved_seq and resolved_seq["items"][0]["text"].startswith("Notify a member")
                    and all(it["text"] in page for it in resolved_seq["items"]),
                    resolved_seq and [it["text"][:30] for it in (resolved_seq or {}).get("items") or []]))

    cc_host = next(e for e in seeded_form if e["element_id"] == inst_eids[0])
    cc_stamp = manifest_check(mf_form, SHAPE_CLOSED)
    results.append(("closed_choice is on the manifest checks index (projector-only)",
                    cc_stamp and cc_stamp.get("shape") == SHAPE_CLOSED
                    and cc_stamp.get("host_element_id") is None
                    and cc_stamp.get("operands", {}).get("options_ref") == "reg_benefit_risk_profile"
                    and cc_stamp.get("operands", {}).get("key_from")
                    == "bindings.instance.selected_value"
                    and cc_stamp.get("operands", {}).get("instance_atom_id")
                    == INSTANCE_EXAMPLE_SEED[0][0]
                    and hosted_check(cc_host) is None, cc_stamp))
    results.append(("closed_choice operands do not copy option labels onto the element",
                    cc_stamp and "Conditional Favorable" not in json.dumps(cc_stamp)
                    and "content" not in cc_host
                    and "assessment" not in cc_host, cc_stamp))
    form_catalog = {a["atom_id"]: a for a in store + form_store + instance_store}
    resolved_cc = resolve_check(cc_stamp, form_catalog, fixture_br_options)
    results.append(("closed_choice operands resolve selected_value + registry from the graph",
                    resolved_cc and resolved_cc["key"] == "conditional_favorable"
                    and resolved_cc["prompt"] == BR_CHECK_PROMPT
                    and {c["text"] for c in resolved_cc["choices"]}
                    == {
                        "favorable", "unfavorable", "conditional_favorable",
                        "uncertain_inconclusive", "contextual", "other_smt_defined",
                    },
                    resolved_cc and resolved_cc.get("key")))
    results.append(("HTML closed_choice is a read of those resolved operands",
                    resolved_cc and f'data-shape="{SHAPE_CLOSED}"' in page_form
                    and resolved_cc["prompt"] in page_form
                    and 'value="conditional_favorable"' in page_form
                    and 'value="unfavorable"' in page_form
                    and br_chunk.find(f'data-shape="{SHAPE_CLOSED}"') != -1, ""))
    results.append(("form lesson has invert + sequence_order + closed_choice",
                    page_form.count('form class="check"') == 4
                    and page_form.count(f'data-shape="{SHAPE_INVERT}"') == 2
                    and page_form.count(f'data-shape="{SHAPE_SEQUENCE}"') == 1
                    and page_form.count(f'data-shape="{SHAPE_CLOSED}"') == 1,
                    page_form.count('form class="check"')))
    results.append(("closed_choice stays in the form BR scene not lesson end",
                    f'data-shape="{SHAPE_CLOSED}"' in br_chunk
                    and inst_eids[0] in br_chunk
                    and f'data-shape="{SHAPE_CLOSED}"' not in page_form[end_form:], ""))
    form_by_eid = {e["element_id"]: e for e in seeded_form}
    resolved_form_scenes = [resolve_scene(s, form_by_eid) for s in form_scenes.get("scenes") or []]
    results.append(("three-scene operands resolve from the graph",
                    len(resolved_form_scenes) == 3
                    and resolved_form_scenes[2]["id"] == "benefit_risk_on_the_form"
                    and resolved_form_scenes[2]["element_ids"] == form_eids + inst_eids
                    and SHAPE_CLOSED in scene_check_refs(resolved_form_scenes[2])
                    and SHAPE_SEQUENCE in scene_check_refs(resolved_form_scenes[1]),
                    [sc["id"] for sc in resolved_form_scenes]))
    results.append(("HTML three-scene wrap is a read of those resolved records",
                    all(f'data-scene="{sc["id"]}"' in page_form
                        and f'class="scene-heading">{sc["heading"]}</h2>' in page_form
                        for sc in resolved_form_scenes)
                    and all(eid in page_form for eid in resolved_form_scenes[2]["element_ids"]),
                    [sc["heading"] for sc in resolved_form_scenes]))
    br_member = next(e for e in seeded_form if e["element_id"] == form_eids[0])
    results.append(("form BR members carry ext.scene",
                    hosted_scene(br_member)
                    and hosted_scene(br_member).get("id") == "benefit_risk_on_the_form"
                    and hosted_scene(br_member).get("role") == SCENE_FORM_BR,
                    hosted_scene(br_member)))
    results.append(("rationale extra stays an example (not a fourth check host)",
                    hosted_check(next(e for e in seeded_form if e["element_id"] == inst_eids[1]))
                    is None, ""))
    results.append(("closed vocab of shapes is invert_definition / sequence_order / closed_choice",
                    set(CHECK_SHAPES) == {SHAPE_INVERT, SHAPE_SEQUENCE, SHAPE_CLOSED}
                    and all(r.get("shape") in CHECK_SHAPES
                            for r in (mf_form.get("checks") or {}).get("checks") or []),
                    (mf_form.get("checks") or {}).get("checks")))
    results.append(("closed vocab of scene roles is front_matter / procedure_a / form_br",
                    set(SCENE_ROLES) == {SCENE_FRONT_MATTER, SCENE_PROCEDURE_A, SCENE_FORM_BR}
                    and all(s.get("role") in SCENE_ROLES
                            for s in form_scenes.get("scenes") or []),
                    [s.get("role") for s in form_scenes.get("scenes") or []]))
    results.append(("spine membership is still 16 with form+instance",
                    len(got_spine_form) == 16, got_spine_form))
    resolved_form_lesson = resolve_lesson(
        mf_form, form_by_eid, atoms_by_id=form_catalog
    )
    form_flat = [
        eid for sc in resolved_form_lesson["scenes"] for eid in sc["element_ids"]
    ] + list(resolved_form_lesson["lesson_end_checks"])
    results.append(("form lesson → three scenes → 16 element_ids resolve from the graph",
                    resolved_form_lesson["lesson_id"] == "course_short"
                    and [sc["id"] for sc in resolved_form_lesson["scenes"]]
                    == ["what_an_alsap_is", "how_an_alsap_starts", "benefit_risk_on_the_form"]
                    and form_flat == got_spine_form
                    and len(form_flat) == 16, form_flat))
    results.append(("form lesson HTML is a read of that lesson node",
                    'data-lesson="selftest_short"' in page_form
                    and page_form.count('class="scene"') == 3
                    and 'data-scene="benefit_risk_on_the_form"' in page_form, ""))
    mf_form["lessons"]["lessons"].append({
        "lesson_id": "course_br",
        "title": resolved_form_lesson["title"],
        "title_from": resolved_form_lesson["title_from"],
        "scene_ids": ["benefit_risk_on_the_form"],
        "lesson_end_check_ids": [],
        "paging": {
            "policy": PAGING_POLICY,
            "scene_count": 1,
            "step_count": 1,
            "lesson_end_is_final_step": False,
            "chrome": "suppressed",
        },
    })
    resolved_br = resolve_lesson(
        mf_form, form_by_eid, lesson_id="course_br", atoms_by_id=form_catalog
    )
    results.append(("BR subset lesson_id resolves only the form_br scene from the graph",
                    resolved_br["lesson_id"] == "course_br"
                    and [sc["id"] for sc in resolved_br["scenes"]] == ["benefit_risk_on_the_form"]
                    and not resolved_br["lesson_end_checks"]
                    and SHAPE_CLOSED in scene_check_refs(resolved_br["scenes"][0]),
                    [sc["id"] for sc in resolved_br["scenes"]]))
    results.append(("BR subset lesson html filename is derived from lesson_id",
                    lesson_html_filename(mf_form, "course_br") == "realized_lesson_br.html"
                    and lesson_html_filename(mf_form, "course_short") == DEFAULT_LESSON_HTML_NAME,
                    lesson_html_filename(mf_form, "course_br")))
    with tempfile.TemporaryDirectory() as td_br:
        br_path = pathlib.Path(td_br) / "realized_lesson_br.html"
        project_html(
            store, seeded_form, mf_form, br_path, lesson_id="course_br",
            meaning_atoms=form_store + instance_store,
            option_sets=fixture_br_options, options_registry=fixture_br_options,
            write_coverage=False,
        )
        page_br = br_path.read_text()
        br_cov = pathlib.Path(td_br) / DEFAULT_COVERAGE_HTML_NAME
    results.append(("BR subset HTML is a read of that lesson node",
                    'data-lesson="course_br"' in page_br
                    and page_br.count('class="scene"') == 1
                    and 'data-scene="benefit_risk_on_the_form"' in page_br
                    and 'data-scene="what_an_alsap_is"' not in page_br
                    and 'data-scene="how_an_alsap_starts"' not in page_br
                    and 'class="lesson-end-checks"' not in page_br
                    and 'data-shape="closed_choice"' in page_br
                    and 'data-shape="sequence_order"' not in page_br
                    and f'data-shape="{SHAPE_INVERT}"' not in page_br
                    and 'data-paging-chrome="suppressed"' in page_br
                    and 'class="player-nav"' not in page_br
                    and 'data-scene-count="1"' in page_br
                    and 'data-step-count="1"' in page_br
                    and not br_cov.exists(), ""))
    apply_spine(
        mf_form, store, seeded_form,
        meaning_atoms=form_store + instance_store, option_sets=fixture_br_options,
    )
    kept_form_ids = [L.get("lesson_id") for L in (mf_form.get("lessons") or {}).get("lessons") or []]
    results.append(("re-stamp keeps the BR subset lesson and does not force lesson-end onto it",
                    "course_br" in kept_form_ids
                    and kept_form_ids[0] == "course_short"
                    and (mf_form.get("lessons") or {}).get("default") == "course_short"
                    and not resolve_lesson(
                        mf_form, form_by_eid, lesson_id="course_br", atoms_by_id=form_catalog
                    )["lesson_end_checks"],
                    kept_form_ids))

    cat_form = {
        "policy": LESSON_CATALOG_POLICY,
        "default": "course_short",
        "lessons": [
            {"lesson_id": "course_short", "default": True},
            {"lesson_id": "course_br", "scene_ids": ["benefit_risk_on_the_form"]},
            {"lesson_id": "course_plan", "scene_ids": ["how_an_alsap_starts"]},
        ],
    }
    mf_form_cat = {"project": "course"}
    apply_spine(
        mf_form_cat, store, seeded_form,
        meaning_atoms=form_store + instance_store, option_sets=fixture_br_options,
        lesson_catalog=cat_form,
    )
    cat_form_ids = [
        L.get("lesson_id") for L in (mf_form_cat.get("lessons") or {}).get("lessons") or []
    ]
    results.append(("form catalog stamps three lesson records from the file",
                    cat_form_ids == ["course_short", "course_br", "course_plan"]
                    and (mf_form_cat.get("lessons") or {}).get("catalog", {}).get("see")
                    == f"occurrences/{LESSON_CATALOG_FILENAME}",
                    cat_form_ids))
    resolved_plan_form = resolve_lesson(
        mf_form_cat, form_by_eid, lesson_id="course_plan", atoms_by_id=form_catalog
    )
    results.append(("catalog plan lesson_id resolves only the procedure_a scene from the graph",
                    resolved_plan_form["lesson_id"] == "course_plan"
                    and [sc["id"] for sc in resolved_plan_form["scenes"]]
                    == ["how_an_alsap_starts"]
                    and not resolved_plan_form["lesson_end_checks"]
                    and SHAPE_SEQUENCE in scene_check_refs(resolved_plan_form["scenes"][0])
                    and SHAPE_CLOSED not in scene_check_refs(resolved_plan_form["scenes"][0]),
                    [sc["id"] for sc in resolved_plan_form["scenes"]]))
    results.append(("plan subset lesson html filename is derived from lesson_id",
                    lesson_html_filename(mf_form_cat, "course_plan")
                    == "realized_lesson_plan.html"
                    and lesson_html_filename(mf_form_cat, "course_br")
                    == "realized_lesson_br.html",
                    lesson_html_filename(mf_form_cat, "course_plan")))
    with tempfile.TemporaryDirectory() as td_plan:
        plan_path = pathlib.Path(td_plan) / "realized_lesson_plan.html"
        project_html(
            store, seeded_form, mf_form_cat, plan_path, lesson_id="course_plan",
            meaning_atoms=form_store + instance_store,
            option_sets=fixture_br_options, options_registry=fixture_br_options,
            write_coverage=False, lesson_catalog=cat_form,
        )
        page_plan = plan_path.read_text()
        plan_cov = pathlib.Path(td_plan) / DEFAULT_COVERAGE_HTML_NAME
    results.append(("plan subset HTML is a read of that lesson node",
                    'data-lesson="course_plan"' in page_plan
                    and page_plan.count('class="scene"') == 1
                    and 'data-scene="how_an_alsap_starts"' in page_plan
                    and 'data-scene="what_an_alsap_is"' not in page_plan
                    and 'data-scene="benefit_risk_on_the_form"' not in page_plan
                    and 'class="lesson-end-checks"' not in page_plan
                    and 'data-shape="sequence_order"' in page_plan
                    and 'data-shape="closed_choice"' not in page_plan
                    and f'data-shape="{SHAPE_INVERT}"' not in page_plan
                    and 'data-paging-chrome="suppressed"' in page_plan
                    and 'class="player-nav"' not in page_plan
                    and 'data-scene-count="1"' in page_plan
                    and 'data-step-count="1"' in page_plan
                    and not plan_cov.exists(), ""))
    with tempfile.TemporaryDirectory() as td_one:
        _, selected_one, extra_one = project_lesson_htmls(
            store, seeded_form, mf_form_cat, td_one,
            meaning_atoms=form_store + instance_store,
            option_sets=fixture_br_options, options_registry=fixture_br_options,
            lesson_id="course_plan", lesson_catalog=cat_form,
        )
        names_one = {p.name for p in pathlib.Path(td_one).iterdir()}
    results.append(("--lesson regenerates only that catalog file",
                    selected_one.name == "realized_lesson_plan.html"
                    and not extra_one
                    and names_one == {"realized_lesson_plan.html"},
                    names_one))
    with tempfile.TemporaryDirectory() as td_all:
        _, selected_all, extra_all = project_lesson_htmls(
            store, seeded_form, mf_form_cat, td_all,
            meaning_atoms=form_store + instance_store,
            option_sets=fixture_br_options, options_registry=fixture_br_options,
            lesson_catalog=cat_form,
        )
        names_all = {p.name for p in pathlib.Path(td_all).iterdir()}
    results.append(("default pass emits all catalog lessons",
                    selected_all.name == DEFAULT_LESSON_HTML_NAME
                    and {p.name for p in extra_all} == {
                        "realized_lesson_br.html", "realized_lesson_plan.html",
                    }
                    and DEFAULT_COVERAGE_HTML_NAME in names_all
                    and "realized_lesson.html" in names_all
                    and "realized_lesson_br.html" in names_all
                    and "realized_lesson_plan.html" in names_all,
                    names_all))

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
        for _aid, mv in FORM_FIELD_SEED:
            if mv not in closed_moves:
                raise SystemExit(f"form-field move {mv!r} is not in the closed vocab")
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
               "  python3 tools/realize.py --lesson ast_alsap_short\n"
               "  python3 tools/realize.py --lesson ast_alsap_br\n"
               "  python3 tools/realize.py --lesson ast_alsap_plan\n"
               "  python3 tools/cartographer.py\n"
               "  python3 tools/couturier.py\n"
               "Open <project>/realized_lesson.html (short spine), "
               "realized_lesson_br.html (BR subset), "
               "realized_lesson_plan.html (Procedure A subset), "
               "or realized_coverage.html (full dump).\n",
    )
    ap.add_argument("--project", default=None,
                    help=f"Atom store directory containing atoms.json (default: {default_shown})")
    ap.add_argument("--core", default=None, help="trainstorm-core (schemas + vocab); usually auto-detected")
    ap.add_argument("--registry", default=None, help="Client registry; usually auto-derived from --project")
    ap.add_argument("--out", help="HTML output path (default: derived from --lesson; default lesson is <project>/realized_lesson.html)")
    ap.add_argument("--lesson", default=None,
                    help="Lesson id from the project catalog (occurrences/lessons.json), stamped onto manifest.lessons. Default pass emits all catalog lessons; --lesson regenerates that file.")
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
    closed_check_shapes = load_check_shape_ids(P["vocab_dir"])
    if set(closed_check_shapes) != set(CHECK_SHAPES):
        raise SystemExit(
            f"vocab/check-shape.enum.json {closed_check_shapes} does not match "
            f"realize.py {list(CHECK_SHAPES)}"
        )
    closed_scene_roles = load_scene_role_ids(P["vocab_dir"])
    if set(closed_scene_roles) != set(SCENE_ROLES):
        raise SystemExit(
            f"vocab/scene.enum.json {closed_scene_roles} does not match "
            f"realize.py {list(SCENE_ROLES)}"
        )
    options_registry = load_options_registry(P["registry_dir"])
    move = args.move
    if move not in closed_moves:
        raise SystemExit(f"--move {move!r} is not in the closed vocab: {closed_moves}")
    for _aid, mv in ONE_TO_MANY_SEED:
        if mv not in closed_moves:
            raise SystemExit(f"seed move {mv!r} is not in the closed vocab: {closed_moves}")
    for _aid, mv in INSTANCE_EXAMPLE_SEED:
        if mv not in closed_moves:
            raise SystemExit(f"instance-example move {mv!r} is not in the closed vocab: {closed_moves}")
    for _aid, mv in FORM_FIELD_SEED:
        if mv not in closed_moves:
            raise SystemExit(f"form-field move {mv!r} is not in the closed vocab: {closed_moves}")

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
    form_atoms = load_form_field_atoms(project)
    form_path = sibling_form_project(project)
    form_hash_before = (
        sha256_bytes((form_path / "atoms.json").read_bytes()) if form_path else None
    )
    form_by_id = {a["atom_id"]: a for a in form_atoms}
    missing_form = [aid for aid, _mv in FORM_FIELD_SEED if aid not in form_by_id]
    if form_atoms and missing_form:
        raise SystemExit(
            f"form-field seed atom_id(s) missing from {FORM_PROJECT_NAME}: {missing_form}. "
            "Do not stretch a cousin field."
        )
    elements = assemble_elements(
        atoms, previous, move, mint_extras=mint_extras,
        instance_atoms=instance_atoms, form_atoms=form_atoms,
        options_registry=options_registry,
    )
    atoms_by_id = meaning_catalog(atoms, form_atoms + instance_atoms)
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
        rec = hosted_check(e)
        if rec and rec.get("shape") == SHAPE_INVERT:
            atom = atoms_by_id[e["composed_from"]]
            chk = resolve_check(rec, atoms_by_id)
            assert_check_honest(chk, atom, atoms)
        elif (e.get("intent") or {}).get("move") == "reinforce":
            atom = atoms_by_id[e["composed_from"]]
            chk = derive_check(atom, atoms)
            assert_check_honest(chk, atom, atoms)
    seq_live = derive_sequence_check(procedure_sequence_atoms(atoms))
    if seq_live:
        assert_sequence_check_honest(seq_live, atoms)
    option_sets = load_option_sets(project)
    if not options_registry:
        options_registry = option_sets
    if form_atoms and instance_atoms:
        br_live = derive_br_profile_check(
            form_by_id.get(BR_PROFILE_FORM_ATOM_ID),
            instance_by_id.get(BR_PROFILE_INSTANCE_ATOM_ID),
            option_sets,
        )
        if not br_live:
            raise SystemExit(
                "No honest closed set for a FORM-AST-34037 BR profile check "
                "(need form options_ref values + instance selected_value in that set). "
                "Refusing to invent options or a stem."
            )
        assert_br_profile_check_honest(br_live, atoms_by_id, option_sets)

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
        "form_field_present": {
            "spec": FORM_FIELD_SPEC,
            "policy": FORM_FIELD_POLICY,
            "store": FORM_PROJECT_NAME,
            "seed": [
                {"atom_id": aid, "extra_element_id": mint_extra_element_id(aid, mv), "move": mv}
                for aid, mv in FORM_FIELD_SEED if aid in form_by_id
            ],
            "note": ("The two instance examples instantiate exactly these FORM-AST-34037 "
                     "fields (BR profile + rationale). Guest ele_ records composed_from "
                     "the form atom_id. Not a form dump. Not f_br_guidance or phrasing "
                     "cousins. Meaning catalog joins the sibling alsap store; SOP and "
                     "form atoms.json are not copied into."),
        },
        "note": ("Primary: one ele_ per atom. 1:many seed mints extra occurrences of a couple "
                 "of teaching-worthy atoms (same composed_from, distinct move, no authored "
                 "content.text). A small form-field present seed mints guest ele_ records "
                 f"whose composed_from is an alsap form atom_id ({FORM_FIELD_SPEC}). "
                 "A small instance-example seed mints guest ele_ records "
                 f"whose composed_from is an alsap_asp9999 atom_id "
                 f"({INSTANCE_EXAMPLE_SPEC}). Cartographer owns occurrence intent; Couturier owns expression "
                 "style. Realizer binds compiler primitives (text_primitive) from atom kind + "
                 f"move ({PRIMITIVE_SPEC}). Spine is a documented selection of existing ele_ records "
                 f"({SPINE_SPEC}); the full dump is coverage. Check shapes "
                 f"({SHAPE_INVERT}, {SHAPE_SEQUENCE}, {SHAPE_CLOSED}) live on "
                 "ext.check / manifest.checks (vocab/check-shape.enum.json). "
                 "Scene records (id, title heuristic, ordered ele_ refs) live on "
                 "spine.scenes / ext.scene (vocab/scene.enum.json). "
                 "The lesson record (id, title heuristic, scene id refs) lives on "
                 "manifest.lessons (agents/realizer/lesson_v1.md), stamped from "
                 "the project catalog (occurrences/lessons.json) when present, "
                 "and points at spine.scenes — not a Course ele_, not a LMS. "
                 "Procedure A sequence_order is projector-only of those four "
                 "presents; composing it from one atom would be a lie. "
                 "closed_choice is projector-only of the form present + instance "
                 "fill (options_ref ids; key = selected_value); composing from "
                 "only one of those two atoms would hide the other half. "
                 "A re-realize preserves extras, intent, style, and recomputes "
                 "the same spine, primitives, check shapes, scenes, and stamps "
                 "lesson records from the catalog (HTML derived from lesson_id)."),
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
    lesson_catalog = load_lesson_catalog(store_dir)
    if lesson_catalog is None:
        carry_previous_lesson_records(occ_manifest, prev_mf)
    apply_spine(
        occ_manifest, atoms, elements,
        meaning_atoms=form_atoms + instance_atoms, option_sets=option_sets,
        lesson_catalog=lesson_catalog,
    )
    stamp_checks(
        occ_manifest, atoms, elements,
        meaning_atoms=form_atoms + instance_atoms,
        options_registry=options_registry or option_sets,
    )
    stamp_primitives(occ_manifest, elements)
    normalize_elements_ext(elements)
    elements_path.write_text(json.dumps(elements, indent=2) + "\n")
    (store_dir / "manifest.json").write_text(json.dumps(occ_manifest, indent=2) + "\n")

    coverage_path, html_path, extra_htmls = project_lesson_htmls(
        atoms, elements, occ_manifest, project,
        meaning_atoms=form_atoms + instance_atoms,
        option_sets=option_sets, options_registry=options_registry or option_sets,
        lesson_id=args.lesson, out=args.out, lesson_catalog=lesson_catalog,
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
    if form_path and form_hash_before:
        if sha256_bytes((form_path / "atoms.json").read_bytes()) != form_hash_before:
            raise SystemExit(
                f"{FORM_PROJECT_NAME}/atoms.json changed during realize — abort. "
                "Realizer must not rewrite form atoms."
            )

    spine_n = (occ_manifest.get("spine") or {}).get("count", 0)
    print(f"Realizer v1 → {len(elements)} elements ({occ_manifest['policy']}, default_move={move})")
    print(f"  atoms      : {atoms_path} ({len(atoms)} records, unchanged)")
    print(f"  primaries  : {len(primaries)}")
    print(f"  extras     : {len(extras)} ({', '.join(e['element_id'] + '=' + (e.get('intent') or {}).get('move', '?') for e in extras) or 'none'})")
    print(f"  occurrences: {elements_path}")
    print(f"  manifest   : {store_dir / 'manifest.json'}")
    print(f"  spine      : {spine_n} of {len(elements)} ({SPINE_POLICY})")
    scenes_n = len(((occ_manifest.get("spine") or {}).get("scenes") or {}).get("scenes") or [])
    print(f"  scenes     : {scenes_n} ({SCENE_GRAPH_POLICY})")
    print(f"  form       : {FORM_PROJECT_NAME} ({len(form_atoms)} atoms joined for meaning; "
          f"{sum(1 for e in extras if (e.get('ext') or {}).get('realized_from', {}).get('form_store'))} guest ele_)")
    print(f"  instance   : {INSTANCE_PROJECT_NAME} ({len(instance_atoms)} atoms joined for meaning; "
          f"{sum(1 for e in extras if (e.get('ext') or {}).get('realized_from', {}).get('instance_store'))} guest ele_)")
    print(f"  primitives : {dict(sorted(primitive_counts(elements).items()))}")
    print(f"  lesson HTML: {html_path}  ← open this")
    for extra_html in extra_htmls:
        print(f"  extra HTML : {extra_html}")
    print(f"  coverage   : {coverage_path}  (full SOP dump)")
    print("  schema     : element.schema.json ALL PASS (no authored content.text)")


if __name__ == "__main__":
    main()
