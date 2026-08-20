#!/usr/bin/env python3
"""
Headwater ingest (form specialisation) — FORM-AST-34037 v1.0, the ALSAP Template -> content atoms.

Sibling of headwater_ingest.py: same agent, same three written facets (meaning, bindings.object,
source-type facet), routed to `form` instead of `procedure`. As there, the semantic acts — what is a
section, what is a field, its field_type, its content_disposition — are the agent's authored
decomposition; this script serialises and stamps them. It is NOT a docx parser.

SCOPE — one section vertical, end to end (2026-08-20). Cover block, approval block, version history,
and PURPOSE AND STAKEHOLDER REVIEW > Safety Profile Summary > Benefit-Risk. The remaining eight
Heading-1 sections are deliberately not decomposed yet; see source_silent.

DISPOSITION IS READ FROM THE TEMPLATE'S OWN MARKERS, not guessed. The convention is stated in
"Instructions for Use / Understanding Template Text Types" AND encoded in the colour of the three
legend entries themselves, which is the proof that it holds document-wide:

    <STANDARD TEXT>        black / auto,  upright   (97 paras)  -> controlled_standard
    <EXAMPLE TEXT>         green 00B050,  upright   (23 paras)  -> example
    <INSTRUCTIONAL TEXT>   blue  5B9BD5,  ITALIC    (89 paras)  -> instructional_transient
    [placeholder text]     blue  5B9BD5,  upright, inside [ ]   -> authorable

Blue does TWO jobs, disambiguated by italics and bracketing: an italic blue block is instructional
prose to delete; upright blue inside square brackets is a fill-in slot. Verified by checking every
run colour in the document — the legend entry for <EXAMPLE TEXT> is itself green, <INSTRUCTIONAL
TEXT> is itself blue italic, <STANDARD TEXT> is itself black.
"""
import json, pathlib, sys
import harness_paths
import store_merge

STORE = harness_paths.resolve()["project_dir"]
CORPUS = "FORM-AST-34037 v1.0 — ALSAP Template (docx, Final)"
DOC = "doc_form_ast_34037"

atoms = []
R = "atom_form_ast34037"


def atom(aid, kind, text, belongs_to=None, order=None, form=None):
    a = {"atom_id": aid,
         "meaning": {"source_locale": "en", "source_text": text, "kind": kind},
         "bindings": {},
         "governance": {"version": 1, "status": "draft",
                        "regulatory_binding": "regulatory",
                        "owner": "team_qseg_safety_data_science"}}
    obj = {}
    if belongs_to: obj["belongs_to"] = belongs_to
    if order is not None: obj["order"] = order
    if obj: a["bindings"]["object"] = obj
    if form is not None: a["bindings"]["form"] = form
    atoms.append(a)
    return aid


def section(aid, text, parent, order, **form):
    return atom(aid, "form_section", text, parent, order, form=form or {})


def field(aid, text, parent, order, field_type, content_disposition, **form):
    form.update(field_type=field_type, content_disposition=content_disposition)
    return atom(aid, "form_field", text, parent, order, form=form)


# ---------------- the form container ----------------
atom(R, "form", "Asset Level Safety Assessment Plan (ALSAP).",
     form={"captures_record": "rec_alsap", "performed_by": ["role_alsap_lead"]})

# ---------------- Instructions for Use (deleted when authoring) ----------------
# Held as a container so a projection knows it exists and must go. Its bullets are a list and are
# NOT decomposed in this pass — flagged, not smashed (see source_silent).
section(f"{R}_sec_instructions", "Instructions for Use.", R, 0,
        content_disposition="instructional_transient")

# ---------------- Cover block (TABLE 2) — labelled fields, [bracketed] slots ----------------
SC = section(f"{R}_sec_cover", "Cover.", R, 1)
field(f"{SC}_f_asset_code",
      "Asset Development Code or International Non-proprietary Name.", SC, 0,
      "text_short", "authorable", constraints={"required": True})
field(f"{SC}_f_version_date", "Version Date.", SC, 1,
      "date", "authorable", constraints={"required": True, "format": "DD-MMM-YYYY"})
# "Final signed versions are X.0. The first final approved version is version 1.0."
field(f"{SC}_f_version_number", "Version Number.", SC, 2,
      "text_short", "authorable", constraints={"required": True, "format": "X.0"})
field(f"{SC}_f_author", "Author.", SC, 3,
      "person", "authorable", constraints={"required": True},
      performed_by=["role_alsap_lead"])

# ---------------- Approval block (TABLE 3) ----------------
# Signature SLOTS only. A signed block is a submission (PII) held under separate governance — the
# template text itself is retained unchanged, hence controlled_standard.
SA = section(f"{R}_sec_approval", "Reviewed and approved by.", R, 2)
field(f"{SA}_f_prepared_by", "Prepared by (name, degree, title) and date.", SA, 0,
      "signature", "controlled_standard", constraints={"required": True},
      performed_by=["role_alsap_lead"])
field(f"{SA}_f_approved_by_1", "Approved by (name, degree, title) and date.", SA, 1,
      "signature", "controlled_standard", constraints={"required": True},
      performed_by=["role_gso", "role_medical_lead", "role_alsap_approver"])
field(f"{SA}_f_approved_by_2", "Approved by (name, degree, title) and date.", SA, 2,
      "signature", "controlled_standard", constraints={"required": True},
      performed_by=["role_gso", "role_medical_lead", "role_alsap_approver"])

# ---------------- Version History (TABLE 4) ----------------
SV = section(f"{R}_sec_version_history", "Version History.", R, 3)
field(f"{SV}_f_history_table",
      "ALSAP Version History Summary: the changes from the prior approved ALSAP that impact "
      "analyses, listed with the rationale (ALSAP Version, Approval Date, ALSAP Section(s), "
      "Change, Rationale).", SV, 0,
      "table", "example", constraints={"repeatable": True})

# ---------------- 1. PURPOSE AND STAKEHOLDER REVIEW > Safety Profile Summary ----------------
SP = section(f"{R}_sec_purpose", "Purpose and Stakeholder Review.", R, 4)
SS = section(f"{SP}_sec_safety_profile", "Safety Profile Summary.", SP, 0)

field(f"{SS}_f_guidance",
      "Describe in a concise way the comprehensive information about the preclinical, "
      "toxicological, pharmacokinetics, pharmacodynamics and clinical safety data for this asset "
      "which may be found in the SFDG and/or IB. The DRMP offers valuable insights, including "
      "patient population epidemiology, identified and potential risks, and risk mitigation "
      "strategies. Maintain consistency of safety information described in the DRMP and ALSAP.",
      SS, 0, "text_long", "instructional_transient")

# CORRECTED 2026-08-20: first modelled `example` from a partial reading. Run-level colour shows the
# sentence is BLACK standard text carrying four upright-blue [ ] placeholder slots — it is retained,
# not optional, and only the bracketed spans are the author's. See source_silent: a standard
# sentence with embedded authorable slots has genuinely mixed disposition and no way to say so.
field(f"{SS}_f_narrative",
      "The overall safety profile for this asset as of the signing of this ALSAP draws upon data "
      "obtained from [Include # here] participants who participated in clinical trials. The most "
      "frequently encountered adverse events associated with [ASPXXXX] include [list of the most "
      "prevalent adverse events] of which the most common that were considered serious include "
      "[list of the most common serious adverse events].",
      SS, 1, "text_long", "controlled_standard",
      # form.facet v0.3: each slot names the exact bracketed literal it fills. Naming the slots
      # (v0.2) removed positional references from the INSTANCE key; the marker removes them from
      # RENDERING too, which is where they had quietly survived.
      constraints={"slots": [
          {"id": "participant_count", "marker": "[Include # here]",
           "expects": "Number of participants across clinical trials contributing to the safety profile."},
          {"id": "asset_code", "marker": "[ASPXXXX]",
           "expects": "Asset development code or INN, matching the cover block."},
          {"id": "prevalent_adverse_events", "marker": "[list of the most prevalent adverse events]",
           "expects": "The most frequently encountered adverse events associated with the asset."},
          {"id": "serious_adverse_events", "marker": "[list of the most common serious adverse events]",
           "expects": "Those among the prevalent events that were considered serious."}]})

field(f"{SS}_f_br_guidance",
      "Choose from the options below to document the SMT's assessment of the overall Benefit-Risk "
      "profile of the asset. Each option carries a definition and an implication for development.",
      SS, 2, "text_long", "instructional_transient")

# The controlled choice and its rationale are TWO atoms — never a smashed
# controlled_choice_plus_rationale. The option set is REFERENCED, never embedded.
BR = field(f"{SS}_f_br_profile",
           "SMT assessment of the overall Benefit-Risk profile of the asset.", SS, 3,
           "select_one", "authorable",
           options_ref="reg_benefit_risk_profile",
           constraints={"required": True},
           performed_by=["role_smt", "role_gso"])

field(f"{SS}_f_br_rationale",
      "Rationale and phrasing for the selected Benefit-Risk profile.", SS, 4,
      "text_long", "authorable", conditional_on=[{"field": BR}])

# ---- Example phrasing, per Benefit-Risk option ----
# A SECTION WRAPPER, not loose siblings: the association "these belong to the rationale field" needs
# to be explicit in structure, and it cannot be expressed by parenting them under br_rationale
# (a form_field leaf with children would break the containers-vs-leaves rule the gate enforces).
#
# DISPOSITION CORRECTED 2026-08-20: labelled "Example phrasing" in the source, but the run-colour
# audit puts the whole option block in blue ITALIC inside one <...> span — so by the template's own
# convention these are instructional_transient (guidance that is deleted), not `example` (candidate
# text the author may retain). The label says example; the colour says instructional; the colour is
# the governed signal. They are still atoms so the agent can surface exactly the phrasings for the
# option actually chosen — conditional_on carries that.
SBP = section(f"{SS}_sec_br_phrasing",
              "Example phrasing for the selected Benefit-Risk profile.", SS, 5,
              content_disposition="instructional_transient")

PHRASING = [
  ("favorable", ["The benefit-risk profile is favorable for the proposed indication.",
                 "Supports continued development and/or marketing authorization."]),
  ("unfavorable", ["The benefit-risk profile is not favorable at this time.",
                   "Further data are needed to support a positive conclusion."]),
  ("uncertain_inconclusive", ["The benefit-risk profile cannot be determined based on current evidence.",
                              "Additional studies are required to clarify the benefit-risk balance."]),
  ("conditional_favorable", ["The benefit-risk profile is favorable under the proposed risk management plan.",
                             "Approval is recommended contingent upon additional safety monitoring."]),
  ("contextual", ["The benefit-risk profile is acceptable in the context of unmet medical need.",
                  "Use is justified in patients with no alternative treatment options."]),
  # other_smt_defined carries no phrasing in the source — the SMT defines it. Absence is not a gap.
]
_o = 0
for opt, lines in PHRASING:
    for i, line in enumerate(lines):
        field(f"{SBP}_{opt}_{i}", line, SBP, _o, "text_long", "instructional_transient",
              conditional_on=[{"field": BR, "equals": opt}])
        _o += 1

# ---------------- provenance / proposals / flags ----------------
store_merge.stamp(atoms)

proposed = {
  "_note": "Flagged, not invented. Every value below resolves to a PROPOSED registry entry; adopt "
           "by entry + version bump before these atoms can pass a governed-vocab gate above draft.",
  "corpus": CORPUS,
  "roles": [], "records": [], "docs": [],
  "options": [{
    "id": "reg_benefit_risk_profile",
    "label": "Benefit-Risk Profile",
    "description": "SMT assessment of an asset's overall Benefit-Risk profile. RESOLVED from the "
                   "source (2026-08-20): FORM-AST-34037 says 'Choose from the options below', so "
                   "this is a CONTROLLED value set, not example wording — closing the "
                   "controlled-vs-example question open since 2026-08-10.",
    "values": [
      {"id": "favorable", "label": "Favorable Benefit-Risk Profile",
       "description": "The benefits of the investigational drug outweigh the known and potential "
                      "risks. Implication: supports progression to the next phase of development "
                      "or regulatory approval."},
      {"id": "unfavorable", "label": "Unfavorable Benefit-Risk Profile",
       "description": "The risks outweigh the benefits, or the benefits are not sufficiently "
                      "demonstrated. Implication: may lead to discontinuation, redesign of the "
                      "trial, or additional data requirements."},
      {"id": "uncertain_inconclusive", "label": "Uncertain or Inconclusive Benefit-Risk Profile",
       "description": "Insufficient data to make a definitive conclusion. Implication: often used "
                      "in early-phase trials or when data are conflicting."},
      {"id": "conditional_favorable", "label": "Conditional Favorable Benefit-Risk Profile",
       "description": "Benefits may outweigh risks if certain conditions are met, such as risk "
                      "mitigation strategies, long-term follow-up, additional data, or data "
                      "maturity. Implication: may support conditional approval or restricted use."},
      {"id": "contextual", "label": "Contextual Benefit-Risk Profile",
       "description": "Benefit-risk is favorable in specific populations or settings, such as rare "
                      "diseases or life-threatening conditions. Implication: may justify approval "
                      "despite limited data or higher risk."},
      {"id": "other_smt_defined", "label": "Other as defined by the SMT",
       "description": "An open option the template permits; the SMT defines the assessment. Pairs "
                      "with the conditional rationale field."},
    ]}]
}

source_silent = {
  "_note": "Gaps, ambiguities and deferred scope surfaced by this ingest. Named, not invented.",
  "corpus": CORPUS,
  "flags": [
    "APPROVER COUNT — the approval table provides one 'Prepared by' and TWO 'Approved by' blocks, "
    "but SOP-AST-29080 names THREE approver roles (GSO, Medical Lead, ALSAP Lead). Whether the "
    "block is fixed at two or repeatable is not stated. Modelled as two fixed slots, each carrying "
    "all three candidate roles in performed_by. Open question for the SME.",

    "BLUE TEXT — RESOLVED 2026-08-20, no SME needed. A full run-colour audit shows a consistent "
    "three-colour convention, self-evidenced by the legend entries' own colours: black upright = "
    "standard (97 paras), green 00B050 upright = example (23 paras), blue 5B9BD5 ITALIC = "
    "instructional (89 paras). Blue does two jobs, split by italics: italic blue is an "
    "instructional block; upright blue inside [ ] is a fill-in slot (authorable). The template is "
    "internally consistent; the earlier ambiguity was a sampling error on our side.",

    "MIXED-DISPOSITION SENTENCE (new, real gap) — the Safety Profile narrative is one sentence of "
    "black standard text containing four upright-blue [ ] authorable slots. Its disposition is "
    "genuinely mixed and the facet can only carry one value per field. Modelled "
    "controlled_standard (the sentence is retained; only the brackets are the author's), but "
    "nothing records that it HAS slots, how many, or what each expects. Options: leave implicit; "
    "add a `slots` array to form.constraints; or decompose the sentence, which would destroy its "
    "readability as a rendered clause. Not resolved — flagged for a deliberate pass.",

    "PER-OPTION EXAMPLE PHRASING — each Benefit-Risk option carries 'Example phrasing' lines. "
    "Registry entries are {id,label,description}, which has no home for them, and they are not "
    "content atoms either. Captured in the proposal description where possible; the phrasings "
    "themselves are NOT yet modelled. Candidate: a richer options-registry entry shape, or "
    "`example`-disposition child atoms under the rationale field.",

    "INSTRUCTIONS FOR USE — held as a single instructional_transient container. Its bullets are a "
    "list and should decompose into List + ListItem (shared-core structure.enum kinds). Flagged, "
    "not smashed; deferred with the rest of the template.",

    "DEFERRED SCOPE — eight Heading-1 sections are not decomposed in this pass: Source of "
    "Aggregated Data and Pooling Strategies; Safety Topics of Interest; Data Analysis Approaches; "
    "Ongoing Safety Surveillance of Clinical Trials; Background Incidence of Anticipated SAEs; "
    "Communication of Safety Information; Supporting Documentation (Appendices 1-4); References. "
    "Thirteen of the seventeen tables are likewise untouched.",

    "SIGNATURE SLOTS — modelled controlled_standard: the template text is retained unchanged and "
    "what gets filled in is a SUBMISSION (PII) under separate governance, never template content.",
  ]
}

manifest = {
  "project": "alsap",
  "corpus_derived_from": CORPUS,
  "source_document": DOC,
  "headwater_mode": "direct",
  "scope": "vertical slice — cover, approval, version history, purpose > safety profile summary > "
           "benefit-risk (see source_silent for deferred sections)",
  "written_facets": ["meaning", "bindings.object", "bindings.form"],
  "read_only_facets": ["intent", "expression", "audience", "render"],
  "approval_roles": ["role_alsap_approver", "role_gso", "role_medical_lead", "role_alsap_lead"],
  "generated_by": "tools/headwater_ingest_form.py",
}

atoms, rep, ingest_log, bootstrap = store_merge.merge(
    STORE, atoms, corpus=CORPUS, project=manifest["project"], owns=("object", "form"), prune="--prune" in sys.argv)
manifest["atom_count"] = len(atoms)
store_merge.write(STORE, atoms, ingest_log, files={
    "proposed_registry_extensions.json": proposed,
    "source_silent.json": source_silent,
    "manifest.json": manifest,
})
store_merge.report(atoms, STORE, rep, bootstrap)
import collections
print("  kinds:", dict(collections.Counter(a["meaning"]["kind"] for a in atoms)))
