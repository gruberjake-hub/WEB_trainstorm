Procedure / SOP object model — the canonical procedural source (2026-07-31)

Captured with Jake. How procedural / quality content (SOPs) enters the manifold as the literal source of truth, without a rival schema. Companion to layout-engine-reconciliation.md and promptpack-manifold-map.md. Files: procedure.facet.schema.json, example_procedure.json, vocab/procedure.enum.json, registry/roles.registry.json, registry/records.registry.json.

The decision, in one line

A procedure IS the content atom — plus one new accreted binding facet (procedure). No second schema, no rival source of truth. SOP source, instructional elements, and translations all sit on the same spine and the same IDs.

The confusion it dissolves ("derived" ≠ "not canonical")

The object model being derived worried Jake for the SOP case, where the JSON must be the source of truth. The word "derived" was doing two jobs:

derived-into — the live, downward dependency (a translation derives into from meaning; change meaning → it goes stale). Real, but only for expression (pedagogy, localization, renderings).
derived-from — a backward provenance pointer, not a dependency ("distilled from that corpus"). The corpus is a quarry, not a parent; once the stone is cut it doesn't depend on it.

An SOP object model is derived-from the SharePoint corpus (a one-time distillation — the prompt pack's Thinker) and is the thing everything else is derived-into. It sits at the headwater. It is not a derived artifact pretending to be truth — it is the meaning layer, which the manifold already defines as the one authored, embedded, canonical payload. So making it the source of truth is the architecture doing what it already says, not a fight with it. The derived_from provenance is a feature: it makes the canonical claim stronger (traceable to meeting / decision / resolved question), which is exactly what a controlled document needs.

What's new vs. what's reused

The only new thing is one binding facet, single-writer-owned by the authoring/headwater agent:

jsonc
"procedure": {                              // NEW facet (bindings accrete; spine untouched)
  "step_type":       "action|decision|verification",   // GOVERNED closed list
  "performed_by":    ["role_qa_intake"],    // WHO — role refs, never people (no PII)
  "produces_records":["rec_complaint_form"],// GxP evidence the step happened
  "references":      ["doc_gvp_module_vi"], // cited controlled docs / regs
  "acceptance_ref":  "atom_...",            // verification steps → a criterion atom (its own meaning)
  "branches": [ { "on": "safety_signal_present", "leads_to": "atom_sop_pci_s3_escalate" } ]
}

Everything else is the atom as-is: the action instruction is meaning.source_text (meaning.kind = procedure for the container, procedure_step for a leaf); linear order and gating are object.order / object.prerequisites; branching beyond a DAG is a decision step whose branches route to other step atoms; and governance (version / status / owner / approved_by / regulatory_binding / effective_date) is what makes it a controlled document — already present, SOPs just lean on it hard.

The agent (placement matters)

This is a new agent, and it sits upstream, not beside pedagogy/translation. Those are downstream facet-writers operating on content that's already canon. This one is the generator specialized for procedural source — the headwater agent that mints canon from a raw corpus. Single-writer: it owns the procedural meaning, the object/structure facet, and the new procedure facet; everyone else reads. It "wakes on" a new SOP project / corpus drop (mirrors the course-generator waking on a new course request).

The SME surface = the localization agent reapplied

The SME never edits JSON. They edit a projection (Word doc / web form / table), marked up as usual. A reconciliation step — structurally identical to the localization agent's human-in-the-loop — folds approved edits back into the canonical atoms: version bump, provenance stamped (who / when / why), status → validated by their sign-off, content_hash recomputed. Human edits a surface; validated change flows back to canon with provenance. Proven already on JP regulatory translation (the hardest case); SOP curation is the easier cousin.

Regulatory reality (the honest caveat)

A GxP stakeholder will not accept raw JSON as the controlled SOP (controlled docs, approvals, Part 11 signatures). Don't fight that. The object model is the engineering source of truth; the controlled Word/PDF is a deterministic projection of it. You show them the controlled document they trust; the model earns its status invisibly by being the single thing every projection and every downstream training/translation is generated from and traces back to.

Invariant check (fragment passes)

Stable opaque IDs ✓ · single-writer (authoring agent owns procedure) ✓ · reference-don't-embed (roles/records/refs are pointers; only the action text is embedded) ✓ · one canonical source (additive to atom.schema.json, no rival) ✓ · content_hash guards meaning (a changed step flags exactly the stale downstream training/translations) ✓ · no PII (roles, not people) ✓.

Validation performed: procedure.facet.schema.json is valid Draft 2020-12; all three example atoms pass the unmodified atom spine (proving accretion); the procedure bindings validate against the facet; an ungoverned step_type is rejected; intra-fragment parent/prereq refs resolve.

Governance vocabularies — minted 2026-07-31 (gate cleared)

The closed lists the facet depends on now exist as real, conformance-checked files:

vocab/procedure.enum.json — governs meaning.kind procedural values (procedure, procedure_step) and the fully-closed step_type enum (action / decision / verification).
registry/roles.registry.json — the role_ roles for performed_by. Roles, never people (no PII). Seed: role_qa_intake, role_pv_reviewer, role_qa_reviewer, role_sme_author.
registry/records.registry.json — the rec_ record/evidence types for produces_records. Seed: rec_complaint_form.

All three declare closed_list: true with the same governance pattern as intent.enum.json. The facet schema's inline step_type enum is marked a mirror of the vocab (vocab wins); a conformance check asserts schema enum == vocab ids, so there is no drifting second copy. The SOP fragment's every value (kinds, step_type, roles, records) was verified to resolve to a governed member. Registries are seeded/draft — extend by entry + version bump, never by using an ungoverned key.

Next: the SME reconciliation loop

Gate cleared, so the next build is the projection + human-in-the-loop round-trip (Word/web surface → SME edits → reconcile back to canon with provenance + version bump + hash recompute). Localization pattern reapplied.

Production vs. frontier

Near-term / buildable: the headwater authoring agent + the SME reconciliation round-trip — the localization pattern reapplied. Genuinely productizable (structured-SOP-as-data as a premium cognition-engineering offering, not ID support). Frontier (keep walled off): "the organizational mind reasons against this grounding" — Response-Engine / Orchestrator territory, a separate project.