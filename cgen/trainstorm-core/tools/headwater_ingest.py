#!/usr/bin/env python3
"""
Headwater ingest — SOP-AST-29080 (ALSAP) -> content atoms.

This encodes the Headwater agent's *authored decomposition* as data and serialises it
to the git-native atom store. The semantic acts (what is a step, its step_type, which role
performs it, which record it produces) are the agent's; this script only serialises + stamps.

Headwater writes exactly three facets: meaning, bindings.object, bindings.procedure.
It resolves every enum to a governed member OR flags it as a proposed registry extension
(flag, never invent). Ungoverned roles/records are emitted to proposed_registry_extensions.json,
NOT silently added to the governed lists.
"""
import json, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
STORE = ROOT / "store" / "projects" / "ast_alsap"
CORPUS = "SOP-AST-29080 v1 — ALSAP SOP (docx)"

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
            "owner": "team_qseg_safety_data_science"  # inferred from doc; see source_silent flags
        },
    }
    obj = {}
    if belongs_to: obj["belongs_to"] = belongs_to
    if order is not None: obj["order"] = order
    if prereqs: obj["prerequisites"] = prereqs
    if obj: a["bindings"]["object"] = obj
    if procedure is not None: a["bindings"]["procedure"] = procedure
    atoms.append(a)
    return aid

# controlled-doc references are governed doc_ ids (real procedure facet requires ^(doc|atom)_),
# NOT raw document numbers. Map number -> doc_ id + keep a human label for projection.
DOC_LABELS = {
    "FORM-AST-34037": "ALSAP Template", "SOP-1798": "Plan and Implement a Safety Management Team",
    "SOP-1683": "Development of Safe First Dosing Guidance", "SOP-1450": "Creation of Development Risk Management Plan",
    "SOP-1773": "Develop, Update, and Distribute Investigator's Brochure", "SOP-480": "Astellas Good Documentation Practices",
    "SOP-AST-28304": "Plan and Implement a Safety Assessment Committee", "STL-4899": "Medical Monitoring Plan Template",
    "WPD-981": "Tables, Listings, and Figures Specifications", "WPD-970": "Specify, Create and Review Statistical Output",
    "WPD-982": "Performing Statistical Analysis", "STL-3884": "Creating Analysis Plans, TLF Specifications and Data Derivations",
    "STL-969": "Data Element and Data Presentation Table",
}
def docid(n): return "doc_" + n.lower().replace("-", "_")

R = "atom_sop_ast29080"  # root

# ---- root + front-matter sections (containers; kind=procedure) ----
atom(R, "procedure",
     "SOP-AST-29080 — Plan, Develop, Execute, Maintain, and Archive the Asset Level Safety "
     "Assessment Plan (ALSAP).")
atom(f"{R}_purpose", "procedure",
     "The purpose of this SOP is to define the process for planning, developing, executing, "
     "maintaining, and archiving the Asset Level Safety Assessment Plan (ALSAP) for use in "
     "asset-level safety monitoring during clinical development.",
     belongs_to=R, order=0)
atom(f"{R}_scope", "procedure",
     "This SOP applies to all Astellas and non-Astellas employees responsible for supporting "
     "ALSAP throughout its lifecycle. In-scope organizations: BOD, COQS, EDTS, MA, OD, RAPV. "
     "[Headwater flag: the in-scope-organizations list is currently embedded prose; it should be "
     "decomposed into a List container + ListItem children, but procedure.enum has no 'list'/"
     "'list_item' kind — surfaced as an open vocab question, not smashed and not invented.]",
     belongs_to=R, order=1)
atom(f"{R}_definitions", "procedure",
     "For definitions, refer to Vault Quality Glossary, or directly in Vault Quality. "
     "[Headwater note: definitions are an external reference; no embedded meaning to atomise here.]",
     belongs_to=R, order=2)
atom(f"{R}_general", "procedure",
     "The ALSAP is the central cross-functional framework for ongoing identification, evaluation, "
     "and communication of emerging safety risks at the asset level. It operationalizes existing "
     "safety governance documents (SFDG, DRMP, IB, SMT minutes), integrating them into an "
     "actionable, data-driven plan for aggregate monitoring across all relevant clinical trials. "
     "Only one ALSAP exists per asset. It must meet ALCOA+ standards and is reviewed annually by "
     "the SMT, with ad hoc updates triggered by emerging signals, regulatory changes, milestones, "
     "data-quality concerns, or external safety events. "
     "[Headwater flag: the governing-documents bullet list (SFDG/DRMP/IB/SMT) is embedded prose; "
     "same open List/ListItem vocab question as scope.]",
     belongs_to=R, order=3)
atom(f"{R}_roles", "procedure",
     "Roles and Responsibilities. [Headwater note: the roles table defines the actors referenced "
     "by performed_by throughout Section VI. Every role resolves to a PROPOSED registry entry — "
     "none are in the current governed roles.registry seed.]",
     belongs_to=R, order=4)
atom(f"{R}_procedures", "procedure",
     "Procedures.", belongs_to=R, order=5)

# ---- sub-section containers ----
PA = atom(f"{R}_proc_a", "procedure", "A. Plan Development of ALSAP.",
          belongs_to=f"{R}_procedures", order=0)
PB = atom(f"{R}_proc_b", "procedure", "B. Develop and Maintain ALSAP.",
          belongs_to=f"{R}_procedures", order=1)
PC = atom(f"{R}_proc_c", "procedure", "C. Develop Analysis Datasets and TLFs.",
          belongs_to=f"{R}_procedures", order=2)

def step(aid, text, parent, order, step_type, roles, produces=None, refs=None,
         prereqs=None, branches=None):
    proc = {"step_type": step_type, "performed_by": roles}
    if produces: proc["produces_records"] = produces
    if refs: proc["references"] = refs
    if branches: proc["branches"] = branches
    atom(aid, "procedure_step", text, belongs_to=parent, order=order,
         prereqs=prereqs, procedure=proc)

# ---- Section A steps ----
step(f"{PA}_s1", "Notify a member of Safety Data Science in QSEG of the need for an ALSAP and "
     "request an ALSAP Lead.", PA, 0, "action", ["role_gso"])
step(f"{PA}_s2", "Collaborate with SMT to identify contributing authors and reviewers.", PA, 1,
     "action", ["role_alsap_lead"], prereqs=[f"{PA}_s1"])
step(f"{PA}_s3", "Schedule and conduct ALSAP Kick-Off Meeting.", PA, 2, "action",
     ["role_alsap_lead"], prereqs=[f"{PA}_s2"])
step(f"{PA}_s4", "Collaborate with contributing authors and confirm alignment on section "
     "deliverables and target dates.", PA, 3, "action", ["role_alsap_lead"], prereqs=[f"{PA}_s3"])

# ---- Section B steps ----
step(f"{PB}_s1", "Provide the ALSAP Lead with contributions to the ALSAP within the agreed-upon "
     "timeframe.", PB, 0, "action", ["role_alsap_contributing_author"])
step(f"{PB}_s2", "Draft the ALSAP using FORM-AST-34037 (ALSAP Template), with the support of the "
     "Contributing Authors. If the asset already has an approved ALSAP, obtain the most current "
     "version from the EDMS to make the updates. [Headwater flag: embedded conditional — candidate "
     "to split into a decision step; kept atomic for the beta and flagged.]",
     PB, 1, "action", ["role_alsap_lead"], produces=["rec_alsap"], refs=[docid("FORM-AST-34037")],
     prereqs=[f"{PB}_s1"])
step(f"{PB}_s3", "Distribute the draft ALSAP for review to the ALSAP Reviewers.", PB, 2, "action",
     ["role_alsap_lead"], prereqs=[f"{PB}_s2"])
step(f"{PB}_s4", "Review draft ALSAP to ensure alignment in approach for the asset and provide "
     "feedback to the ALSAP Lead.", PB, 3, "verification", ["role_alsap_reviewer"],
     prereqs=[f"{PB}_s3"])
step(f"{PB}_s5", "Reconcile comments/edits in consultation with the ALSAP Contributing Authors, "
     "follow up on any comments/edits, and repeat steps 2-4 until all comments/edits are "
     "addressed.", PB, 4, "decision", ["role_alsap_lead"], prereqs=[f"{PB}_s4"],
     branches=[{"on": "comments_or_edits_remaining", "leads_to": f"{PB}_s3"}])
step(f"{PB}_s6", "Finalize the ALSAP and route for approvals in the EDMS.", PB, 5, "action",
     ["role_alsap_lead"], prereqs=[f"{PB}_s5"])
step(f"{PB}_s7", "Review and approve the ALSAP in EDMS.", PB, 6, "verification",
     ["role_alsap_approver"], produces=["rec_alsap"], prereqs=[f"{PB}_s6"])
step(f"{PB}_s8", "Notify the ALSAP Contributing Authors, Reviewers, Approvers, and the SAC Chair "
     "of the approval of the ALSAP.", PB, 7, "action", ["role_alsap_lead"], prereqs=[f"{PB}_s7"])

# ---- Section C steps ----
step(f"{PC}_s1", "Develop the Tables, Listings, and Figures (TLF) Table of Contents (TOC) and "
     "Shells per the asset's ALSAP.", PC, 0, "action", ["role_alsap_lead"],
     produces=["rec_tlf_toc_shells"], refs=[docid("WPD-981"), docid("STL-3884"), docid("STL-969")])
step(f"{PC}_s2", "Distribute the TLF TOC and Shells to the SMT Co-Chairs.", PC, 1, "action",
     ["role_alsap_lead"], prereqs=[f"{PC}_s1"])
step(f"{PC}_s3", "Reach alignment with SMT Co-Chairs on TLF TOC and Shells.", PC, 2, "action",
     ["role_alsap_lead"], prereqs=[f"{PC}_s2"])
step(f"{PC}_s4", "File the ALSAP TLF TOC and Shells in the assigned asset folder in the "
     "Statistical Computing Environment (SCE).", PC, 3, "action", ["role_alsap_lead"],
     prereqs=[f"{PC}_s3"])
step(f"{PC}_s5", "In collaboration with the Safety Programmer, prepare the plan for development of "
     "statistical outputs based on the asset's SMT schedule.", PC, 4, "action",
     ["role_alsap_lead", "role_safety_programmer"], prereqs=[f"{PC}_s4"])
step(f"{PC}_s6", "Develop Dataset and TLF programming specifications.", PC, 5, "action",
     ["role_safety_programmer"], prereqs=[f"{PC}_s5"])
step(f"{PC}_s7", "Review Dataset and TLF programming specifications and provide feedback.", PC, 6,
     "verification", ["role_alsap_lead"], prereqs=[f"{PC}_s6"])
step(f"{PC}_s8", "Develop the datasets (SDTM, ADaM, and non-CDISC derived) and specifications. "
     "Note: development programs and output must reside in the PV restricted-access folder of the "
     "SCE to protect the blind.", PC, 7, "action", ["role_safety_programmer"],
     produces=["rec_analysis_datasets"], refs=[docid("WPD-970")], prereqs=[f"{PC}_s7"])
step(f"{PC}_s9", "Create TLF programs and outputs.", PC, 8, "action", ["role_safety_programmer"],
     produces=["rec_tlf_outputs"], refs=[docid("WPD-982")], prereqs=[f"{PC}_s8"])
step(f"{PC}_s10", "Validate TLF programs and outputs.", PC, 9, "verification",
     ["role_safety_programmer"], prereqs=[f"{PC}_s9"])
step(f"{PC}_s11", "Review the TLF outputs.", PC, 10, "verification", ["role_alsap_lead"],
     prereqs=[f"{PC}_s10"])
step(f"{PC}_s12", "Provide TLF outputs to the SMT per the agreed-upon cycles and timeframes. "
     "Note: unblinded data must not be provided to the members of the SMT to protect the blind.",
     PC, 11, "action", ["role_alsap_lead"], prereqs=[f"{PC}_s11"])
step(f"{PC}_s13", "Review ALSAP outputs per SOP-1798.", PC, 12, "verification", ["role_smt"],
     refs=[docid("SOP-1798")], prereqs=[f"{PC}_s12"])

# ---- stamp content_hash on every atom (hash of meaning) ----
for a in atoms:
    payload = json.dumps(a["meaning"], sort_keys=True, ensure_ascii=False).encode("utf-8")
    a["content_hash"] = "sha256:" + hashlib.sha256(payload).hexdigest()
    # order keys for a clean, diffable store
    a_ordered = {k: a[k] for k in ["atom_id", "content_hash", "meaning", "bindings", "governance"]}
    a.clear(); a.update(a_ordered)

# ---- proposed registry extensions (FLAGGED — not governed) ----
proposed = {
  "_note": "Headwater flagged these: every value resolves to a PROPOSED registry entry because none "
           "exist in the current governed seeds. Adopt into the repo registries by entry + version "
           "bump before this SOP's atoms can pass a governed-vocab gate at status>draft.",
  "corpus": CORPUS,
  "roles": [
    {"id": "role_alsap_lead", "label": "ALSAP Lead",
     "note": "Safety Statistician (QSEG) responsible for ALSAP development & maintenance. OWED SEED (2026-08-10)."},
    {"id": "role_alsap_reviewer", "label": "ALSAP Reviewer",
     "note": "Cross-functional reviewer group (incl. Contributing Authors, SMT Co-chairs, BRT Chair, Asset/Research Lead, GCPL, GSTATL, RAPV Epidemiologist, Safety Programmer, EDTS Safety Rep). Group role — see open question on committee vs individual roles."},
    {"id": "role_alsap_approver", "label": "ALSAP Approver",
     "note": "Minimum: GSO, Medical Lead, ALSAP Lead."},
    {"id": "role_alsap_contributing_author", "label": "ALSAP Contributing Author"},
    {"id": "role_sac_chair", "label": "SAC Chair",
     "note": "Leads the Safety Assessment Committee; typically Global Medical Safety Head (or designee) per SOP-AST-28304."},
    {"id": "role_safety_programmer", "label": "Safety Programmer",
     "note": "QSEG. Doc splits Developer vs Validator (segregation of duties). OPEN: two roles vs a duty attribute? Modeled as one role for the beta."},
    {"id": "role_gso", "label": "Global Safety Officer (GSO)"},
    {"id": "role_medical_lead", "label": "Medical Lead (ML)"},
    {"id": "role_smt", "label": "Safety Management Team (SMT)",
     "note": "A committee/body, not an individual. Same committee-vs-individual open question."},
    {"id": "role_smt_cochair", "label": "SMT Co-Chair"}
  ],
  "records": [
    {"id": "rec_alsap", "label": "Asset Level Safety Assessment Plan (ALSAP)",
     "note": "The controlled plan itself; template FORM-AST-34037. OWED SEED (2026-08-10)."},
    {"id": "rec_tlf_toc_shells", "label": "TLF Table of Contents and Shells"},
    {"id": "rec_analysis_datasets", "label": "Analysis Datasets (SDTM / ADaM / non-CDISC derived)"},
    {"id": "rec_tlf_outputs", "label": "TLF Programs and Outputs"}
  ],
  "docs": [
    {"id": docid(n), "source_number": n, "label": DOC_LABELS[n]}
    for n in ["FORM-AST-34037", "SOP-1798", "SOP-1683", "SOP-1450", "SOP-1773", "SOP-480",
              "SOP-AST-28304", "STL-4899", "WPD-981", "WPD-970", "WPD-982", "STL-3884", "STL-969"]
  ],
  "docs_note": "The real procedure facet requires references to be doc_/atom_ ids (not raw numbers). "
      "These are PROPOSED doc_ entries for a controlled-doc registry (doc_). Classic client-level "
      "vocab — the same doc_sop_1798 is cited across many Astellas SOPs, so it should be governed "
      "once in the Astellas namespace, not per-project.",
  "still_owed_not_instantiated_by_this_sop": {
    "reg_benefit_risk_profile": "Owed controlled value set (2026-08-10). The BRT (Benefit Risk Team) "
        "appears here only as a reviewer role, not as a value set, so this SOP does not force it. "
        "Left owed; do not invent."
  }
}

source_silent = {
  "_note": "Gaps where the source is silent or defers elsewhere. Named, not invented.",
  "corpus": CORPUS,
  "gaps": [
    "governance.owner — no accountable content owner id stated in the doc; inferred 'team_qseg_safety_data_science' and flagged.",
    "governance.effective_date — v1 'New SOP', no effective date in extracted text; omitted (optional).",
    "governance.approved_by — approver roles are named but no signatory ids; left empty.",
    "DEFINITIONS — deferred to external Vault Quality Glossary; no embedded meaning atomised.",
    "Safety Programmer Developer/Validator — segregation of duties present in the table but modeled as one role; open.",
    "Embedded conditional in B.s2 ('if an approved ALSAP exists') — candidate decision step; kept atomic + flagged.",
    "Narrative lists (in-scope orgs; governing docs; notify recipients) — want List/ListItem decomposition, but procedure.enum lacks those kinds."
  ]
}

manifest = {
  "project": "ast_alsap",
  "corpus_derived_from": CORPUS,
  "headwater_mode": "direct",
  "atom_count": len(atoms),
  "written_facets": ["meaning", "bindings.object", "bindings.procedure"],
  "read_only_facets": ["intent", "expression", "audience", "render"],
  "generated_by": "tools/headwater_ingest.py"
}

STORE.mkdir(parents=True, exist_ok=True)
(STORE / "atoms.json").write_text(json.dumps(atoms, indent=2, ensure_ascii=False))
(STORE / "proposed_registry_extensions.json").write_text(json.dumps(proposed, indent=2, ensure_ascii=False))
(STORE / "source_silent.json").write_text(json.dumps(source_silent, indent=2, ensure_ascii=False))
(STORE / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
print(f"Wrote {len(atoms)} atoms to {STORE/'atoms.json'}")
print(f"  {sum(1 for a in atoms if a['meaning']['kind']=='procedure')} containers, "
      f"{sum(1 for a in atoms if a['meaning']['kind']=='procedure_step')} steps")
