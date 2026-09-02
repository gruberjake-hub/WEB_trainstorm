#!/usr/bin/env python3
"""
Headwater ingest — CCI Public Disclosure QD-nucleus (Case-Author stage 2).

Sibling of headwater_ingest.py (ALSAP SOP) and headwater_ingest_form.py
(FORM-AST-34037). Same agent, same written facets (meaning, bindings.object,
source-type facet). Authored semantic acts, NOT a PDF parser.

Wakes only through tools/headwater_case_author_mint.py on validated cd_ast_cci_pd.
Three in-scope QDs only, v2.0 (April 2026, supersede v1.0):

    SOP-AST-29658  → procedure / procedure_step / list / list_item
    GUIDE-AST-6011 → procedure containers + MAY-BE / Not-CCI leaves (collapsed; not 80 atoms)
    FORM-AST-35734 → form / form_section / form_field (FORM-AST-34037 specialisation)

Remainder inventory (tracking tool, Helix trigger, WS3, comms, SH training-guide)
is NOT minted. No ele_. No bindings.intent. No approval-page PII/emails.
Ungoverned roles/records/docs go to proposed_registry_extensions.json;
cgen/astellas/registry/docs.registry.json is not grown.

Living-connection: SOP B/C NOTES (already public is not confidential). Do not
invent Health Canada/CTIS incident atoms. E names a Tracking Tool in source_text
and does not lock an obj_ or pretend the tool is live. Helix Project ID is a
FORM field, not a trigger.
"""
import json, pathlib, sys
import store_merge

STORE = pathlib.Path(__file__).resolve().parent.parent.parent / "astellas" / "projects" / "cci_public_disclosure"
CORPUS = (
    "SOP-AST-29658 / GUIDE-AST-6011 / FORM-AST-35734 v2.0 (April 2026; supersede v1.0) "
    "— Astellas CCI Public Disclosure QD-nucleus. Authored Headwater decomposition "
    "from jake-handed v2.0 QDs, not the Feb 2025 v1 pile. Case-Author stage 2 of "
    "validated cd_ast_cci_pd. Remainder inventory not minted."
)

LEFTOVER_DOC_IDS = frozenset({
    "doc_cci_pd_tracking_tool",
    "doc_cci_pd_helix_kachi_trigger",
    "doc_cci_pd_ws3_ri",
    "doc_cci_pd_connections_note",
    "doc_cci_pd_sh_training_guide",
})

atoms = []
OWNER = "team_public_disclosure"  # inferred from PD Lead owning the GUIDE; flagged


def atom(aid, kind, text, belongs_to=None, order=None, prereqs=None,
         procedure=None, form=None):
    if aid.startswith("ele_"):
        raise SystemExit(f"refused ele_ id: {aid}")
    a = {
        "atom_id": aid,
        "meaning": {"source_locale": "en", "source_text": text, "kind": kind},
        "bindings": {},
        "governance": {
            "version": 1,
            "status": "draft",
            "regulatory_binding": "regulatory",
            "owner": OWNER,
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
    if procedure is not None and form is not None:
        raise SystemExit(f"{aid}: both procedure and form facets (exactly one allowed)")
    if procedure is not None:
        a["bindings"]["procedure"] = procedure
    if form is not None:
        a["bindings"]["form"] = form
    if "intent" in a["bindings"]:
        raise SystemExit(f"{aid}: bindings.intent is closed")
    atoms.append(a)
    return aid


def listnode(aid, text, parent, order):
    return atom(aid, "list", text, belongs_to=parent, order=order)


def item(aid, text, parent, order):
    return atom(aid, "list_item", text, belongs_to=parent, order=order)


def step(aid, text, parent, order, step_type, roles, produces=None, refs=None,
         prereqs=None, branches=None):
    proc = {"step_type": step_type, "performed_by": roles}
    if produces:
        proc["produces_records"] = produces
    if refs:
        proc["references"] = refs
    if branches:
        proc["branches"] = branches
    return atom(aid, "procedure_step", text, belongs_to=parent, order=order,
                prereqs=prereqs, procedure=proc)


def section(aid, text, parent, order, **form):
    return atom(aid, "form_section", text, parent, order, form=form or {})


def field(aid, text, parent, order, field_type, content_disposition, **form):
    form.update(field_type=field_type, content_disposition=content_disposition)
    return atom(aid, "form_field", text, parent, order, form=form)


def docid(n):
    return "doc_" + n.lower().replace("-", "_")


DOC_SOP = docid("SOP-AST-29658")
DOC_GUIDE = docid("GUIDE-AST-6011")
DOC_FORM = docid("FORM-AST-35734")

# =====================================================================
# SOP-AST-29658 v2.0 — procedure tree (ALSAP kinds)
# Skip history/approvals. No approval-page PII/emails.
# =====================================================================
R = "atom_sop_ast29658"

atom(R, "procedure",
     "SOP-AST-29658 v2.0 (April 2026; supersedes v1.0) — define Astellas CCI for "
     "disclosure of Astellas information in the public domain, and outline tracking.")

atom(f"{R}_purpose", "procedure",
     "Define Astellas CCI for disclosure of Astellas information in the public domain, and outline tracking.",
     belongs_to=R, order=0)

atom(f"{R}_scope", "procedure",
     "This SOP applies to disclosure of Astellas information in the public domain.",
     belongs_to=R, order=1)

SDOM = f"{R}_scope_domains"
listnode(SDOM, "Public domains include:", f"{R}_scope", 0)
for i, name in enumerate([
    "ClinicaTrials.gov",  # PDF spelling; keep if quoting
    "CTIS",
    "EU CTR/EudraCT",
    "jRCT",
    "national registries",
    "company website",
    "TrialSummaries.com",
    "journals",
    "events",
    "HMA-EMA RWD catalogue",
    "HA clinical-data sites",
    "HTA sites",
    "EMA Policy 0043",
]):
    item(f"{SDOM}_{i}", name, SDOM, i)

SORG = f"{R}_scope_orgs"
listnode(SORG, "Organizations in scope of this SOP.", f"{R}_scope", 1)
for i, name in enumerate([
    "Alliance Management",
    "BOD",
    "COQS",
    "Communications & IR",
    "PPM",
    "EDTS",
    "Legal & IP",
    "Market Access & Pricing",
    "Global Medical Affairs",
    "OD",
    "RAPV",
    "Oncology Research",
    "Cell & Gene Therapy Research",
    "Innovation Lab",
    "Product Development & Manufacturing",
]):
    item(f"{SORG}_{i}", name, SORG, i)

SOOS = f"{R}_scope_oos"
listnode(SOOS, "Out of scope.", f"{R}_scope", 2)
item(f"{SOOS}_0", "corporate/media/IR", SOOS, 0)
item(f"{SOOS}_1",
     "third-party under contract (POL-1048, POL-317)",
     SOOS, 1)

atom(f"{R}_definitions", "procedure",
     "Document-specific terms used in this SOP: CCI, Public Disclosure, Public Domain.",
     belongs_to=R, order=2)
atom(f"{R}_def_cci", "procedure",
     "CCI: non-public technical/scientific/business know-how, trade secrets, proprietary; "
     "also info useful to competitors or harmful if disclosed.",
     belongs_to=f"{R}_definitions", order=0)
atom(f"{R}_def_public_disclosure", "procedure",
     "Public Disclosure: disclosure of Astellas information in the public domain.",
     belongs_to=f"{R}_definitions", order=1)
atom(f"{R}_def_public_domain", "procedure",
     "Public Domain: ClinicaTrials.gov, CTIS, EU CTR/EudraCT, jRCT, national registries, "
     "company website, TrialSummaries.com, journals, events, HMA-EMA RWD catalogue, "
     "HA clinical-data sites, HTA sites, EMA Policy 0043.",
     belongs_to=f"{R}_definitions", order=2)

atom(f"{R}_overview", "procedure",
     "Packages can contain company secrets AND/OR participant/personnel PI/PPD. "
     "GUIDE for classification; FORM is the asset-specific library.",
     belongs_to=R, order=3,
     procedure={"references": [DOC_GUIDE, DOC_FORM]})
GOV = f"{R}_overview_objects"
listnode(GOV, "GUIDE+FORM as objects.", f"{R}_overview", 0)
item(f"{GOV}_0", "GUIDE-AST-6011 for classification.", GOV, 0)
item(f"{GOV}_1", "FORM-AST-35734 is the asset-specific library.", GOV, 1)

atom(f"{R}_roles", "procedure",
     "Roles and Responsibilities.",
     belongs_to=R, order=4)
atom(f"{R}_role_asset_lead", "procedure",
     "Asset Lead completes FORM with GUIDE + AMT/SMEs; revises on phase/CCI change; consults PD Lead.",
     belongs_to=f"{R}_roles", order=0)
atom(f"{R}_role_ddc", "procedure",
     "Disclosure Document Coordinator prepares docs, uses FORM, escalates if not followed.",
     belongs_to=f"{R}_roles", order=1)
atom(f"{R}_role_disclosing_party", "procedure",
     "Disclosing Party posts/uploads, same.",
     belongs_to=f"{R}_roles", order=2)
atom(f"{R}_role_pd_lead", "procedure",
     "PD Lead maintains GUIDE, facilitates FORM, collects/reports, escalation.",
     belongs_to=f"{R}_roles", order=3)

atom(f"{R}_procedures", "procedure",
     "Procedures.", belongs_to=R, order=5)
atom(f"{R}_proc_intro", "procedure",
     "CN-to-IND.",
     belongs_to=f"{R}_procedures", order=0)

PA = atom(f"{R}_proc_a", "procedure", "A.",
          belongs_to=f"{R}_procedures", order=1)
PB = atom(f"{R}_proc_b", "procedure", "B. Phase-change.",
          belongs_to=f"{R}_procedures", order=2)
PC = atom(f"{R}_proc_c", "procedure", "C. Ad hoc.",
          belongs_to=f"{R}_procedures", order=3)
PD = atom(f"{R}_proc_d", "procedure", "D. Follow FORM or escalate before ship.",
          belongs_to=f"{R}_procedures", order=4)
PE = atom(f"{R}_proc_e", "procedure", "E. Tracking.",
          belongs_to=f"{R}_procedures", order=5)

# A steps 1-6
A1 = step(f"{PA}_s1", "PD Lead initiate.", PA, 0, "action", ["role_pd_lead"])
A2 = step(f"{PA}_s2",
          "Asset Lead classify with GUIDE (may-be consult SME/Dept Head/Legal).",
          PA, 1, "action", ["role_asset_lead"],
          refs=[DOC_GUIDE], prereqs=[A1])
A3 = step(f"{PA}_s3", "Document on FORM.", PA, 2, "action", ["role_asset_lead"],
          produces=["rec_cci_library"], refs=[DOC_FORM], prereqs=[A2])
A4 = step(f"{PA}_s4", "Inform PD Lead.", PA, 3, "action", ["role_asset_lead"],
          prereqs=[A3])
A5 = step(f"{PA}_s5", "Archive.", PA, 4, "action", ["role_asset_lead"],
          produces=["rec_cci_library"], refs=[DOC_FORM], prereqs=[A4])
A6 = step(f"{PA}_s6", "Inform Disclosing Parties.", PA, 5, "action",
          ["role_asset_lead", "role_pd_lead"], prereqs=[A5])

# B: phase-change + public-domain-check NOTE (living-connection). Not an incident atom.
B1 = step(f"{PB}_s1", "Reassess.", PB, 0, "action", ["role_asset_lead"],
          refs=[DOC_GUIDE, DOC_FORM])
NOTE = atom(f"{PB}_note_already_public", "procedure",
            "Check public domain — already public is not confidential.",
            belongs_to=PB, order=1)

# C: ad hoc + same NOTE (referenced, not a second Health Canada/CTIS invention)
C1 = step(f"{PC}_s1", "Ad hoc reassess.", PC, 0, "action", ["role_asset_lead"],
          refs=[NOTE, DOC_GUIDE, DOC_FORM])
# B also cites the NOTE as the living-connection on the phase-change path
atoms_by_id = {a["atom_id"]: a for a in atoms}
atoms_by_id[B1]["bindings"]["procedure"].setdefault("references", []).append(NOTE)

# D: follow FORM CCI or escalate mailbox before ship (not leftover Helix/tracker)
D1 = step(f"{PD}_s1", "Prepare/post without FORM CCI.", PD, 0, "action",
          ["role_disclosure_document_coordinator", "role_disclosing_party"],
          refs=[DOC_FORM])
D2 = step(f"{PD}_s2",
          "If deviation, contact Asset Lead and PD Lead via publicdisclosure-sm@astellas.com before ship.",
          PD, 1, "action",
          ["role_disclosure_document_coordinator", "role_disclosing_party",
           "role_asset_lead", "role_pd_lead"],
          prereqs=[D1], refs=[DOC_FORM])

# E: tracking steps 1-4 as SOP procedure. Names a Tracking Tool — do not lock
# an obj_ or pretend it is live. No leftover doc_ id, no produces_records.
E1 = step(f"{PE}_s1", "Quarterly request.", PE, 0, "action", ["role_pd_lead"])
E2 = step(f"{PE}_s2", "Parties provide.", PE, 1, "action",
          ["role_disclosing_party", "role_disclosure_document_coordinator"],
          prereqs=[E1])
E3 = step(f"{PE}_s3", "PD Lead reconcile.", PE, 2, "action", ["role_pd_lead"],
          prereqs=[E2])
E4 = step(f"{PE}_s4", "Verify in Public Disclosure Tracking Tool.", PE, 3,
          "verification", ["role_pd_lead"], prereqs=[E3])

# =====================================================================
# GUIDE-AST-6011 v2.0 — classification companion (procedure kinds, not 80 atoms)
# Four type containers, each with MAY-BE vs Not-CCI leaves. Bullets collapsed.
# =====================================================================
G = "atom_guide_ast6011"
atom(G, "procedure",
     "GUIDE-AST-6011 v2.0 (April 2026; supersedes v1.0) — CCI / may-be-CCI / not-CCI including phase.")
atom(f"{G}_purpose", "procedure",
     "Standards apply all phases, decreasing later/after MA.",
     belongs_to=G, order=0)
atom(f"{G}_companion", "procedure",
     "Companion of SOP-AST-29658.",
     belongs_to=G, order=1,
     procedure={"references": [DOC_SOP]})
atom(f"{G}_phase_decay", "procedure",
     "Phase-decay: preclinical through Ph4, decreases later/after MA.",
     belongs_to=G, order=2)

GCMC = atom(f"{G}_cmc", "procedure", "CMC.", belongs_to=G, order=3)
atom(f"{GCMC}_maybe", "procedure",
     "MAY-BE: DS names/structure early; quantitative composition; metabolite formulae/pathways "
     "that reveal manufacture; polymorphism/sequence; impurities; DS/DP manufacturing methods, "
     "sites, CMOs, specs, batch size, unpublished in-house cells; DP packaging technical specs; "
     "AAV fact of synthesis/formulation change.",
     belongs_to=GCMC, order=0)
atom(f"{GCMC}_not", "procedure",
     "Not-CCI: published/commercial cell-line names; general characterization; excipient names; "
     "standard storage; batch numbers; common techniques; fact of process change except AAV.",
     belongs_to=GCMC, order=1)

GNC = atom(f"{G}_nonclinical", "procedure", "Nonclinical.", belongs_to=G, order=4)
atom(f"{GNC}_maybe", "procedure",
     "MAY-BE: unpublished novel MoA/concepts; metabolites until NDA/BLA; special substrate; "
     "exclusive assays; early results; CRO/site names; future plans; study dates; detailed HA "
     "advice; contractual strategy.",
     belongs_to=GNC, order=0)
atom(f"{GNC}_not", "procedure",
     "Not-CCI: ELISA/Biacore/common assays; published techniques; country names.",
     belongs_to=GNC, order=1)

GCL = atom(f"{G}_clinical", "procedure", "Clinical.", belongs_to=G, order=5)
atom(f"{GCL}_maybe", "procedure",
     "MAY-BE: unpublished patentable unit/daily/max dose (typ. Ph1); novel unqualified "
     "biomarkers; exclusive assays; non-label endpoints; third-party questionnaires when "
     "contract forbids disclosure.",
     belongs_to=GCL, order=0)
atom(f"{GCL}_not", "procedure",
     "Not-CCI: route/frequency/setting; design; results; CRO names; fact of HA consult.",
     belongs_to=GCL, order=1)

GOT = atom(f"{G}_other", "procedure", "Other.", belongs_to=G, order=6)
atom(f"{GOT}_maybe", "procedure",
     "MAY-BE: exposure calc, exposure/sales by country, projected exposure, product cost, net pricing.",
     belongs_to=GOT, order=0)
atom(f"{GOT}_not", "procedure",
     "Not-CCI: list pricing.",
     belongs_to=GOT, order=1)

# =====================================================================
# FORM-AST-35734 v2.0 — form specialisation like FORM-AST-34037
# One-tab-per-phase is an instruction atom, not 12 empty workbooks.
# Project ID (Helix) is a FIELD, not a trigger.
# =====================================================================
F = "atom_form_ast35734"
atom(F, "form",
     "FORM-AST-35734 v2.0 (April 2026; supersedes v1.0) — CCI library.",
     form={"captures_record": "rec_cci_library", "performed_by": ["role_asset_lead"]})

SC = section(f"{F}_sec_cover", "Development Phase X.", F, 0)

field(f"{SC}_f_version_date", "Version Date.", SC, 0,
      "date", "authorable", constraints={"required": True},
      evidence_kind="date", supplied_by="authoring_context")

# Cover label retains [ASPXXXX] as the fill-in; sentence is controlled, slot is the demand.
field(f"{SC}_f_asset_code", "Asset code/INN [ASPXXXX].", SC, 1,
      "text_short", "controlled_standard", constraints={
          "required": True,
          "slots": [{
              "id": "asset_code",
              "marker": "[ASPXXXX]",
              "expects": "Asset development code or International Non-proprietary Name.",
              "evidence_kind": "identifier",
              "supplied_by": "asset_evidence",
          }],
      })

field(f"{SC}_f_project_id", "Project ID (Helix).", SC, 2,
      "text_short", "authorable", constraints={"required": True},
      evidence_kind="identifier", supplied_by="asset_evidence")

field(f"{SC}_f_dev_phase", "Development Phase.", SC, 3,
      "text_short", "authorable", constraints={"required": True},
      evidence_kind="identifier", supplied_by="asset_evidence")

field(f"{F}_f_escalate",
      "If deviation, contact Asset Lead and PD Lead via publicdisclosure-sm@astellas.com before ship.",
      F, 1, "text_long", "instructional_transient")

SL = section(f"{F}_sec_library", "CCI library.", F, 2)
field(f"{SL}_f_columns",
      "Type/Subtype/CCI exact text/Notes.",
      SL, 0, "table", "authorable",
      constraints={"required": True, "repeatable": True},
      captures_record="rec_cci_library",
      performed_by=["role_asset_lead"],
      evidence_kind="structured_set", supplied_by="asset_evidence")

SI = section(f"{F}_sec_instructions", "Instructions-Examples.", F, 3,
             content_disposition="instructional_transient")
field(f"{SI}_f_examples",
      "Exact-text examples; complete revision history.",
      SI, 0, "text_long", "instructional_transient")
field(f"{SI}_f_one_tab_per_phase",
      "One tab per phase.",
      SI, 1, "text_long", "instructional_transient")

SV = section(f"{F}_sec_revision_history", "Revision History.", F, 4)
field(f"{SV}_f_history_table",
      "Phase, Asset Lead, PD Lead, description, version date.",
      SV, 0, "table", "example", constraints={"repeatable": True})


def _assert_no_remainder():
    for a in atoms:
        aid = a["atom_id"]
        if aid.startswith("ele_"):
            raise SystemExit(f"ele_ minted: {aid}")
        if a.get("bindings", {}).get("intent"):
            raise SystemExit(f"bindings.intent on {aid}")
        proc = a.get("bindings", {}).get("procedure") or {}
        for ref in proc.get("references") or []:
            if ref in LEFTOVER_DOC_IDS:
                raise SystemExit(f"{aid} references leftover {ref}")


def proposed_extensions():
    return {
        "_note": "Headwater flagged these: every value resolves to a PROPOSED registry entry "
                 "because none exist in the current governed ALSAP-era seeds. Adopt into the "
                 "repo registries by entry + version bump before status>draft. Do not silently "
                 "grow cgen/astellas/registry/docs.registry.json this hop. Remainder-bin docs "
                 "(tracking tool, Helix trigger, WS3, comms, SH training-guide) are NOT proposed.",
        "corpus": CORPUS,
        "roles": [
            {"id": "role_asset_lead", "label": "Asset Lead",
             "note": "Completes FORM-AST-35734 with GUIDE-AST-6011 + AMT/SMEs; revises on phase/CCI change; consults PD Lead."},
            {"id": "role_disclosure_document_coordinator",
             "label": "Disclosure Document Coordinator",
             "note": "Prepares disclosure documents, uses the FORM, escalates if not followed."},
            {"id": "role_disclosing_party", "label": "Disclosing Party",
             "note": "Posts/uploads public disclosures; follows FORM or escalates before ship."},
            {"id": "role_pd_lead", "label": "PD Lead",
             "note": "Maintains GUIDE, facilitates FORM, collects/reports, escalation. Already named as goal_ast_cci_library_used owner; not in governed roles.registry."},
        ],
        "records": [
            {"id": "rec_cci_library",
             "label": "FORM-AST-35734 CCI library",
             "note": "Asset-specific CCI library the Asset Lead completes before IND. Template FORM-AST-35734. Not the Public Disclosure Tracking Tool."},
        ],
        "docs": [
            {"id": DOC_SOP, "source_number": "SOP-AST-29658",
             "label": "Public Disclosure of Astellas CCI (v2.0)"},
            {"id": DOC_GUIDE, "source_number": "GUIDE-AST-6011",
             "label": "CCI / may-be-CCI / not-CCI including phase (v2.0)"},
            {"id": DOC_FORM, "source_number": "FORM-AST-35734",
             "label": "CCI library Asset Leads complete before IND (v2.0)"},
            {"id": docid("POL-1048"), "source_number": "POL-1048",
             "label": "Third-party under contract (cited in SOP out of scope)"},
            {"id": docid("POL-317"), "source_number": "POL-317",
             "label": "Third-party under contract (cited in SOP out of scope)"},
        ],
        "docs_note": "Proposed, not invented into the governed ALSAP-era docs.registry. "
                     "Remainder inventory ids are not listed here and are not minted.",
    }


def source_silent_doc():
    return {
        "_note": "Gaps where the source is silent or this hop deliberately does not mint. Named, not invented.",
        "corpus": CORPUS,
        "gaps": [
            "governance.owner — inferred team_public_disclosure from PD Lead maintaining the GUIDE; flagged, not a person.",
            "SOP history/approvals — skipped. No approval-page PII/emails.",
            "Feb 2025 v1 pile — superseded; v2.0 (April 2026) is what jake handed; v1 not minted.",
            "Public Disclosure Tracking Tool — named in SOP E source_text as a procedure step. Not in production. Not an obj_. Not leftover doc_cci_pd_tracking_tool. No rec_ minted for it.",
            "Helix/Kachi start-trigger — remainder. Project ID (Helix) is a FORM field, not a trigger atom.",
            "WS3 RI, connections/comms, SH parking-lot training-guide — leftover; not minted.",
            "Health Canada / CTIS incident examples — not in the v2.0 QDs; not invented. Living-connection is the B/C NOTE: already public is not confidential.",
            "AMT/SMEs, SME/Dept Head/Legal — named as consults in source_text; not proposed as extra roles this hop.",
            "One-tab-per-phase — instruction atom, not 12 empty Development Phase workbooks.",
            "GUIDE bullets collapsed into MAY-BE vs Not-CCI leaves per type (CMC, Nonclinical, Clinical, Other); not 80 atoms.",
            "D.s2 embedded conditional ('if deviation') — candidate decision step; kept as action + flagged, same as ALSAP B.s2.",
        ],
    }


def manifest_doc(n):
    return {
        "project": "cci_public_disclosure",
        "corpus_derived_from": CORPUS,
        "headwater_mode": "case_author",
        "committed_design": "cd_ast_cci_pd",
        "in_scope": sorted(IN_SCOPE := ["doc_sop_ast_29658", "doc_guide_ast_6011", "doc_form_ast_35734"]),
        "left_unminted": sorted(LEFTOVER_DOC_IDS),
        "atom_count": n,
        "written_facets": ["meaning", "bindings.object", "bindings.procedure", "bindings.form"],
        "read_only_facets": ["intent", "expression", "audience", "render"],
        "approval_roles": ["role_pd_lead", "role_asset_lead"],
        "generated_by": "tools/headwater_ingest_cci_pd.py",
        "source_versions": {
            "SOP-AST-29658": "2.0",
            "GUIDE-AST-6011": "2.0",
            "FORM-AST-35734": "2.0",
        },
    }


def ingest(store, prune=False):
    """Serialise the authored decomposition into `store`. Does not touch committed-design.json."""
    _assert_no_remainder()
    store_merge.stamp(atoms)
    proposed = proposed_extensions()
    source_silent = source_silent_doc()
    manifest = manifest_doc(len(atoms))
    merged, rep, ingest_log, bootstrap = store_merge.merge(
        store, atoms, corpus=CORPUS, project=manifest["project"],
        owns=("object", "procedure", "form"), prune=prune)
    manifest["atom_count"] = len(merged)
    store_merge.write(store, merged, ingest_log, files={
        "proposed_registry_extensions.json": proposed,
        "source_silent.json": source_silent,
        "manifest.json": manifest,
    })
    store_merge.report(merged, store, rep, bootstrap)
    kinds = {}
    for a in merged:
        k = a["meaning"]["kind"]
        kinds[k] = kinds.get(k, 0) + 1
    print("  kinds:", kinds)
    print("  remainder not minted:", sorted(LEFTOVER_DOC_IDS))
    return merged


if __name__ == "__main__":
    ingest(STORE, prune="--prune" in sys.argv)
