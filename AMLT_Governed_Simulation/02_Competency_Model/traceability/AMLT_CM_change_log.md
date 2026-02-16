# AMLT Competency Model Change Log

This document records all structural and definitional changes to AMLT competency models.

Purpose:
- Maintain audit traceability
- Preserve historical versions
- Document SME approval
- Provide governance transparency

LOCKED models must never be overwritten.
All changes require version increment and log entry.

---

# Version History

---

## Version: AMLT_CM_v1.0
Status: LOCKED  
Date Locked: YYYY-MM-DD  
Approved By: SME_NAME_PLACEHOLDER  
Compiler Version: CM_COMPILER_LOCK_v0.1  

### Source Corpus
- AMLT_Deck_v3.md
- Asset_Maximization_Framework_v2.pdf
- Risk_Governance_SOP_v5.docx

### Summary of Changes
- Initial competency model derived from corpus.
- 6 competencies defined.
- Behavioral indicators normalized.
- Traceability anchors added for all competencies.
- Evidence keyword lists refined for simulation use.

### Structural Changes
- N/A (initial version)

### Rationale
This model reflects observed recurring behavioral and strategic patterns across AMLT documentation and aligns with enterprise-level decision expectations for Asset Maximization Teams.

### Simulation Impact
- Referenced by AMLT_SIM_v4.2
- Competency evaluation enabled.
- Maximum 2 flips per round enforced.

### Known Limitations
- Traceability anchors are section-level approximations.
- Regulatory clause mapping not yet implemented.

---

## Version: AMLT_CM_v1.1
Status: LOCKED  
Date Locked: YYYY-MM-DD  
Approved By: SME_NAME_PLACEHOLDER  
Compiler Version: CM_COMPILER_LOCK_v0.1  

### Source Corpus
- AMLT_Deck_v4.md (updated)
- Safety_Addendum_2026.pdf

### Summary of Changes
- Clarified definition of AMLT-C2_RISK_SYNTHESIS.
- Added 1 behavioral indicator to AMLT-C4_CROSS_FUNCTIONAL_LEADERSHIP.
- Expanded evidence keyword set for AMLT-C3_ENTERPRISE_THINKING.

### Structural Changes
- No competencies added or removed.
- No ID changes.

### Rationale
Updates reflect clarified expectations regarding risk communication in Phase 2 transition decisions.

### Simulation Impact
- No change to pass criteria.
- Minor adjustment in evidence detection sensitivity.

### Known Limitations
- Competitive positioning behaviors may require further granularity in next major revision.

---

# Versioning Guidelines

MAJOR (v2.0, v3.0, etc.)
- Competency added or removed
- Competency renamed
- Structural ID changes
- Core behavioral framing altered

MINOR (v1.1, v1.2, etc.)
- Definition clarified
- Behavioral indicators added/refined
- Keyword adjustments
- Traceability refined

---

# Governance Safeguards

- LOCKED models are immutable.
- Runtime must reference explicit version.
- Simulation and governance validator must log model version used.
- LMS completion records should include model version in metadata (if supported).

---

# Future Enhancements (Optional)

- Regulatory clause mapping layer
- Quantitative signal weighting
- Cross-functional density analysis
- Audit-ready traceability matrix export

---

# Architectural Note

Competency drift is one of the largest hidden risks in AI-driven evaluation systems.

This log exists to prevent:
- Silent competency mutation
- Untracked evaluation changes
- Misalignment between training and governance

If you are unsure whether a change requires MAJOR or MINOR versioning, default to MAJOR.
