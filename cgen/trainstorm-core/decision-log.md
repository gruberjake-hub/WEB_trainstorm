# Decision log — Course Engine / Manifold

*Running log of settled architectural decisions. Newest first. One entry = one decision that is
closed enough to build on; if it reopens, add a new dated entry rather than editing history.*

## 2026-08-10 — Ingest/headwater agent architecture is settled; next rung is the prompt pass

The ingest/decomposition agent is **not** greenfield — it is the **headwater authoring agent**
(`procedure-object-model.md`), now extended to a second source type via the **`form` facet**
(`form-object-model.md`, gated 11/11). Procedure and form are duals on one spine; the object-model
(process_model / form_model) is an **ingest view**, not the output-of-record (the atoms are). Facet
ownership is single-writer: this agent owns `meaning`, `object`, and the source-type facet
(`procedure` | `form`); intent / expression / audience / render are downstream readers. **Next real
rung: the prompt pass** — write the headwater agent's system + intake prompts against this settled
architecture, harvesting the bundle's prompts as raw material. Open items carried: mint 3 registry
seeds (`role_alsap_lead`, `rec_alsap`, `reg_benefit_risk_profile`); resolve the Benefit-Risk
controlled-vs-example SME question.
