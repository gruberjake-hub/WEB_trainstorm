#!/usr/bin/env python3
"""
Headwater ingest — SOP-2290 (working id) artwork approval SOP -> content atoms.

Sibling of headwater_ingest.py (ALSAP). Same agent, same three written facets
(meaning, bindings.object, bindings.procedure). This is an *authored
decomposition*, not a generic docx parser. Do not overwrite the ALSAP ingest.

Working id SOP-2290: the Vault export used for this hop does not print its own
SOP number on the face (common). The face says it supersedes SOP-2290 v 4.0.
That gap is named in the corpus string, source_silent, and DECISIONS — not
silently treated as a printed document number.
"""
import json, pathlib, sys
import store_merge

STORE = pathlib.Path(__file__).resolve().parent.parent.parent / "astellas" / "projects" / "ast_artwork"
CORPUS = (
    "SOP-2290 (working id; Vault export does not print its own SOP number on "
    "the face; supersedes SOP-2290 v 4.0) — Artwork approval process and "
    "artwork text management for new or revised Printed Packaging Component "
    "(Astellas Pharma Europe B.V. Leiden; Pharmaceutical Technology / Supply "
    "Chain Management; status Effective). Authored extract, not a generic docx parse."
)

atoms = []


def atom(aid, kind, text, belongs_to=None, order=None, prereqs=None, procedure=None):
    a = {
        "atom_id": aid,
        "meaning": {"source_locale": "en", "source_text": text, "kind": kind},
        "bindings": {},
        "governance": {
            "version": 1,
            "status": "draft",
            "regulatory_binding": "regulatory",
            "owner": "team_pt_scm_emea",  # inferred from owning division; flagged
        },
    }
    obj = {}
    if belongs_to:
        obj["belongs_to"] = belongs_to
    if order is not None:
        obj["order"] = order
    if prereqs:
        obj["prerequisites"] = prereqs
    if obj:
        a["bindings"]["object"] = obj
    if procedure is not None:
        a["bindings"]["procedure"] = procedure
    atoms.append(a)
    return aid


DOC_LABELS = {
    "SOP-2290": "Artwork approval process and artwork text management for new or revised Printed Packaging Component",
    "SOP-2293": "Artwork Development with AMS BLUE",
    "WPD-1172": "Change Control of Text and/or Artwork",
    "SOP-2502": "Management of the UID",
    "SOP-3184": "Repackaging of Commercial Products within Affiliates",
    "STL-4269": "STL-4269 (title not in this extract)",
    "STL-4270": "STL-4270 (title not in this extract)",
    "WPD-1055": "WPD-1055 (title not in this extract)",
    "WPD-1056": "WPD-1056 (title not in this extract)",
    "WPD-1002": "WPD-1002 (title not in this extract)",
    "WPD-1003": "WPD-1003 (title not in this extract)",
    "WPD-1004": "WPD-1004 (title not in this extract)",
    "WPD-991": "LMG Start of a BLUE Project",
    "WI-AST-10187": "WI-AST-10187 (Implementation Report / IR; title not fully in this extract)",
}


def docid(n):
    return "doc_" + n.lower().replace("-", "_")


R = "atom_sop_2290"

# ---- root + front-matter ----
atom(R, "procedure",
     "SOP-2290 — Artwork approval process and artwork text management for new "
     "or revised Printed Packaging Component.")
atom(f"{R}_purpose", "procedure",
     "The purpose of this Standard Operating Procedure (SOP) is to:",
     belongs_to=R, order=0)
atom(f"{R}_scope", "procedure",
     "This SOP applies to:",
     belongs_to=R, order=1)
atom(f"{R}_definitions", "procedure",
     "Document-specific terms used in this SOP. [Headwater note: Artwork, CID, "
     "UID-related, and ASD are named in the source; glossary prose for those "
     "terms was not in the supplied extract. BLUE and BLUE Project below are "
     "verbatim. Not a Vault glossary dump as the short lesson.]",
     belongs_to=R, order=2)
atom(f"{R}_roles", "procedure",
     "Roles and Responsibilities. [Headwater note: actors named in this SOP "
     "(ACM, RA Representative, LMG EU, Manufacturing Plant, SPD, Affiliate, …) "
     "are not in the governed roles.registry. Proposed in "
     "proposed_registry_extensions.json; not a taught RACI course.]",
     belongs_to=R, order=3)
atom(f"{R}_procedures", "procedure",
     "Procedures.", belongs_to=R, order=4)


def listnode(aid, text, parent, order):
    atom(aid, "list", text, belongs_to=parent, order=order)


def item(aid, text, parent, order):
    atom(aid, "list_item", text, belongs_to=parent, order=order)


# ---- purpose bullets (verbatim) ----
PPUR = f"{R}_purpose_items"
listnode(PPUR, "The purpose of this Standard Operating Procedure (SOP) is to:",
         f"{R}_purpose", 0)
for i, txt in enumerate([
    "manage new or revised artwork in cooperation between Regulatory Affairs (RA) and relevant stakeholders to ensure that for each batch of product delivered under responsibility of an Astellas entity, the text of all Printed Packaging Components (PPC) (e.g. folding cartons, patient leaflets etc.) is verified to comply with the registered Product Information (PI), therefore the batch with compliant artwork meets (local) regulatory requirements and is suitable for distribution release",
    "ensure that artwork, part of the Marketing Authorisation (MA) in compliance with the regulatory regulations and directives, created, managed, and provided for production by Astellas is controlled in Astellas Artwork Management System BLUE (hereafter BLUE) as per “SOP-2293 Artwork Development with AMS BLUE”",
    "define an implementation schedule for new or revised artwork",
    "describe the role and responsibilities for each different step in the artwork process",
]):
    item(f"{PPUR}_{i}", txt, PPUR, i)

# ---- scope: who + products + related-process notes + out of scope ----
SWHO = f"{R}_scope_who"
listnode(SWHO, "This SOP applies to:", f"{R}_scope", 0)
item(f"{SWHO}_0",
     "Labeling Management Group Europe (LMG EU) fulfilling the role of (Associate) Artwork Coordination Managers (ACM)",
     SWHO, 0)
item(f"{SWHO}_1",
     "RA organisation of the Established and Emerging Markets of the region Europe, Middle East and Africa (EMEA) involved in Artwork Management consisting of: (Senior) Directors; RA Representatives",
     SWHO, 1)

atom(f"{R}_scope_products", "procedure",
     "The procedure is applicable for all products where an Astellas entity is "
     "the Marketing Authorization Holder (MAH) or where Astellas has legal or "
     "regulatory responsibilities (i.e., business partners and license partners).",
     belongs_to=f"{R}_scope", order=1)
atom(f"{R}_scope_applicable", "procedure",
     "This procedure is applicable for: specimen before approval; when a product "
     "will be launched after approval of the MA; after approval of a change (in "
     "a Centralized Procedure (CP), a Mutual Recognition Procedure (MRP) / "
     "Decentralized Procedure (DCP) or National Procedure (NP)) in the "
     "regulatory file requiring new or revised artwork",
     belongs_to=f"{R}_scope", order=2)

SREL = f"{R}_scope_related"
listnode(SREL, "Related controlled processes named in the scope of this SOP.",
         f"{R}_scope", 3)
item(f"{SREL}_0",
     "The global process for managing and tracking the implementation of a change to Product Information (PI) text and/or artwork, is part of “WPD-1172 Change Control of Text and/or Artwork”.",
     SREL, 0)
item(f"{SREL}_1",
     "Timelines mentioned for the various process steps in this SOP, indicate the standard lead time in BLUE to perform an activity. Any delays in BLUE will be monitored as per “SOP-2502 Management of the UID”.",
     SREL, 1)
item(f"{SREL}_2",
     "Repackaging, co-packaging, bundling, labeling and relabeling are part of “SOP-3184 Repackaging of Commercial Products within Affiliates”.",
     SREL, 2)

atom(f"{R}_scope_oos", "procedure",
     "Out of scope of this SOP is dispatch/shipment of PPC.",
     belongs_to=f"{R}_scope", order=4)

# ---- definitions: verbatim BLUE / BLUE Project; named terms without glossary prose ----
atom(f"{R}_def_blue", "procedure",
     "BLUE is a software application for managing the artwork change control "
     "process within Astellas.",
     belongs_to=f"{R}_definitions", order=0)
atom(f"{R}_def_blue_project", "procedure",
     "A BLUE Project contains 16 BLUE Tasks which must be performed in a "
     "predefined sequence in order to produce a desired outcome, such as an "
     "approved piece of artwork.",
     belongs_to=f"{R}_definitions", order=1)
# Artwork / CID / UID / ASD are named on the definitions atom (Headwater note)
# and in source_silent. Do not mint a sibling list heading — that would become
# an invert-definition distractor that is not SOP prose.

# ---- procedures intro + A–L ----
atom(f"{R}_procedures_intro", "procedure",
     "The management of artwork for products where an Astellas entity is the "
     "MAH: RA Representative ensures that the text of all the PPC complies "
     "with the registered PI and approves all artworks of products sold "
     "within their territory in BLUE. …",
     belongs_to=f"{R}_procedures", order=0)
atom(f"{R}_procedures_start", "procedure",
     "For new artwork start with Section A. For existing artwork start with Section C.",
     belongs_to=f"{R}_procedures", order=1)

PA = atom(f"{R}_proc_a", "procedure",
          "A. BLUE: Initiate Project for new artwork",
          belongs_to=f"{R}_procedures", order=2)


def step(aid, text, parent, order, step_type, roles, produces=None, refs=None,
         prereqs=None, branches=None):
    proc = {"step_type": step_type, "performed_by": roles}
    if produces:
        proc["produces_records"] = produces
    if refs:
        proc["references"] = refs
    if branches:
        proc["branches"] = branches
    atom(aid, "procedure_step", text, belongs_to=parent, order=order,
         prereqs=prereqs, procedure=proc)


step(f"{PA}_s1",
     "If new artwork is applicable: ACM initiates the BLUE Project for new "
     "artwork based on the information in the signed Implementation Report "
     "(IR) according to WI-AST-10187, by using BLUE and the committed base "
     "design.",
     PA, 0, "action", ["role_acm"],
     produces=["rec_blue_project"],
     refs=[docid("WI-AST-10187")])
step(f"{PA}_s2",
     "If Mock-up is required to be submitted to HA, ACM starts a BLUE Project "
     "as per “WPD-991 LMG Start of a BLUE Project“ when requested by the "
     "concerned Affiliate. This Mock-Up contains artwork that is for "
     "submission purposes.",
     PA, 1, "action", ["role_acm"],
     produces=["rec_blue_project", "rec_mock_up"],
     refs=[docid("WPD-991")],
     prereqs=[f"{PA}_s1"])
step(f"{PA}_s3",
     "If an immediate implementation of the Mock-Up artwork is required after "
     "HA approval, the concerned ACM shall follow the Mock-Up Implementation "
     "steps described in SOP-2293.",
     PA, 2, "action", ["role_acm"],
     refs=[docid("SOP-2293")],
     prereqs=[f"{PA}_s2"])

# B–L: section titles only. Step actions were not in the supplied extract —
# do not invent them. Containers keep the graph from being an A-only stub.
# Coverage dump shows these headings; short lesson does not.
for order, (letter, title) in enumerate([
    ("b", "B. Give instructions."),
    ("c", "C. Assess impact."),
    ("d", "D. Determine implementation overlap."),
    ("e", "E. Initiate artwork change."),
    ("f", "F. Additional BLUE start info."),
    ("g", "G. Development of Artwork."),
    ("h", "H. Review."),
    ("i", "I. Cancellation."),
    ("j", "J. Approve."),
    ("k", "K. Defining the CID."),
    ("l", "L. Artwork Implementation."),
], start=3):
    parent = atom(f"{R}_proc_{letter}", "procedure", title,
                  belongs_to=f"{R}_procedures", order=order)
    # One thin procedure_step so coverage is a procedure_step group, not a
    # heading-only stub. Text is the section title (verbatim). No invented
    # ACM actions. No performed_by guess.
    atom(f"{R}_proc_{letter}_s1", "procedure_step", title,
         belongs_to=parent, order=0,
         procedure={"step_type": "action"})

store_merge.stamp(atoms)

proposed = {
    "_note": "Headwater flagged these: values resolve to PROPOSED registry "
             "entries because they are not in the current governed seeds. "
             "Do not silently extend roles.registry / docs.registry / "
             "records.registry. Adopt by entry + version bump before status>draft.",
    "corpus": CORPUS,
    "roles": [
        {"id": "role_acm", "label": "(Associate) Artwork Coordination Manager (ACM)",
         "note": "LMG EU fulfills this role. Named throughout Procedure A. Not in governed roles.registry."},
        {"id": "role_ra_representative", "label": "RA Representative",
         "note": "RA organisation of Established and Emerging Markets EMEA. Approves artworks in BLUE for their territory."},
        {"id": "role_lmg_eu", "label": "Labeling Management Group Europe (LMG EU)",
         "note": "Group fulfilling the ACM role. A body, not an individual."},
        {"id": "role_manufacturing_plant", "label": "Manufacturing Plant",
         "note": "Named among sibling-process actors; not in the supplied Procedure A extract. Flagged so it is not silently added."},
        {"id": "role_spd", "label": "SPD",
         "note": "Named among sibling-process actors; expansion not in this extract. Flagged, not invented."},
        {"id": "role_affiliate", "label": "Affiliate",
         "note": "Requests Mock-Up BLUE Project (Procedure A step 2)."},
    ],
    "records": [
        {"id": "rec_blue_project", "label": "BLUE Project",
         "note": "A BLUE Project contains 16 BLUE Tasks in a predefined sequence."},
        {"id": "rec_implementation_report", "label": "Implementation Report (IR)",
         "note": "Signed IR; Procedure A starts from it per WI-AST-10187."},
        {"id": "rec_mock_up", "label": "Mock-Up",
         "note": "Artwork for HA submission purposes."},
        {"id": "rec_printed_packaging_component",
         "label": "Printed Packaging Component (PPC)",
         "note": "e.g. folding cartons, patient leaflets."},
        {"id": "rec_cid", "label": "CID",
         "note": "Named (Defining the CID). Glossary prose not in this extract."},
        {"id": "rec_uid", "label": "UID",
         "note": "Named via SOP-2502 Management of the UID. Glossary prose not in this extract."},
    ],
    "docs": [
        {"id": docid(n), "source_number": n, "label": DOC_LABELS[n]}
        for n in [
            "SOP-2290", "SOP-2293", "WPD-1172", "SOP-2502", "SOP-3184",
            "STL-4269", "STL-4270", "WPD-1055", "WPD-1056", "WPD-1002",
            "WPD-1003", "WPD-1004", "WPD-991", "WI-AST-10187",
        ]
    ],
    "docs_note": "None of these numbers are in the governed docs.registry "
                 "(ALSAP-era seed). Proposed, not invented into the governed list. "
                 "STL-4269/4270 and WPD-1055/1056/1002/1003/1004 are sibling "
                 "citations from the face/header; titles were not in the supplied extract.",
}

source_silent = {
    "_note": "Gaps where the source is silent or this extract is incomplete. Named, not invented.",
    "corpus": CORPUS,
    "gaps": [
        "SOP number on the face — Vault export used for this hop does not print its own SOP number. Working id SOP-2290 from supersedes SOP-2290 v 4.0. Not treated as a printed document number.",
        "governance.owner — owning division is Pharmaceutical Technology / Supply Chain Management / Astellas Pharma Europe B.V. Leiden; inferred 'team_pt_scm_emea' and flagged.",
        "DEFINITIONS — Artwork, CID, UID-related, ASD named; glossary prose not in the supplied extract. BLUE and BLUE Project are verbatim. Not a whole-glossary short lesson.",
        "Roles table — actors are not in governed roles.registry; Headwater note on the roles atom; not a taught RACI course.",
        "Procedure B–L — section titles only in this extract (Give instructions; Assess impact; Determine implementation overlap; Initiate artwork change; Additional BLUE start info; Development of Artwork; Review; Cancellation; Approve; Defining the CID; Artwork Implementation). Step actions not invented. Each letter is a procedure container plus one thin title-only procedure_step for coverage.",
        "Procedures intro — extract ends the RA Representative sentence with an ellipsis; kept verbatim. Not completed.",
        "Embedded conditionals in A.s1–s3 ('If new artwork…', 'If Mock-up…', 'If an immediate implementation…') — candidate decision steps; kept atomic + flagged, same as ALSAP B.s2.",
        "FORM-AST — this SOP has no honest closed form fill. No form/instance scene.",
        "ISO 14971 — not this document. Not ingested.",
    ],
}

manifest = {
    "project": "ast_artwork",
    "corpus_derived_from": CORPUS,
    "headwater_mode": "direct",
    "atom_count": len(atoms),
    "written_facets": ["meaning", "bindings.object", "bindings.procedure"],
    "read_only_facets": ["intent", "expression", "audience", "render"],
    "approval_roles": ["role_acm", "role_ra_representative"],
    "generated_by": "tools/headwater_ingest_artwork.py",
}

atoms, rep, ingest_log, bootstrap = store_merge.merge(
    STORE, atoms, corpus=CORPUS, project=manifest["project"],
    owns=("object", "procedure"), prune="--prune" in sys.argv)
manifest["atom_count"] = len(atoms)
store_merge.write(STORE, atoms, ingest_log, files={
    "proposed_registry_extensions.json": proposed,
    "source_silent.json": source_silent,
    "manifest.json": manifest,
})
store_merge.report(atoms, STORE, rep, bootstrap)
print(f"  {sum(1 for a in atoms if a['meaning']['kind']=='procedure')} containers, "
      f"{sum(1 for a in atoms if a['meaning']['kind']=='procedure_step')} steps")
