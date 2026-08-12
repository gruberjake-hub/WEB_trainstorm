# Form / template object model — the `form` facet (2026-08-10)

*Captured with Jake. How form/template source (the ALSAP `FORM-AST-34037`) enters the manifold —
as canonical atoms carrying one new accreted binding facet (`form`), sibling to `procedure`. No rival
schema, no second source of truth. Companion to `procedure-object-model.md`. Files:
`schemas/form.facet.schema.json`, `vocab/form.enum.json`, `reference/example_form_fragment.json`,
`validate.py`.*

## The decision, in one line

**A form IS the content atom — plus one new accreted binding facet (`form`) for the irreducibly
form-specific part (input primitive, constraints, options, authoring lifecycle).** Everything else
reuses the spine and the *same registries* `procedure` already uses. Overlap with `procedure` is
accepted for now; a shared `workflow` facet is noted as a later refactor if the duplication bites.

## Why a facet at all (and why a small one)

A procedure and a form are **duals**: the procedure is the *doing*; the form is the *record the doing
produces*. The canon already wires this — a procedure step's `produces_records: ["rec_complaint_form"]`
names a *form* as its output — and ALSAP is exactly the pair (SOP + form + crosswalk). So most of what a
form needs already exists: label text is `meaning.source_text`; sections/order are the `object` facet;
who-fills-and-signs are `role_` refs (**same `roles.registry`**); what-record-it-becomes is a `rec_`
ref (**same `records.registry`**); versioning/approvals/regulatory flag are `governance`. The facet
holds *only* what none of those cover.

## What's new vs. what's reused

```jsonc
"form": {                                 // NEW facet (bindings accrete; spine untouched)
  "field_type":      "date",              // GOVERNED closed list (leaves only)
  "content_disposition": "controlled_standard", // GOVERNED — the template authoring lifecycle
  "constraints":     { "required": true, "format": "DD-MMM-YYYY" },
  "options_ref":     "reg_benefit_risk_profile", // controlled values — reference, don't embed
  "captures_record": "rec_alsap",         // SAME records.registry as procedure
  "performed_by":    ["role_gso"],        // SAME roles.registry as procedure (roles, never people)
  "conditional_on":  [{ "field": "atom_...", "equals": "true" }] // show/require logic (field-level branches)
}
```

Reused as-is: `meaning` (the field label / standard text), `object` (`belongs_to`/`order` — a Form is a
`kind:form` container, sections are `kind:form_section`, fields are `kind:form_field` leaves), and
`governance` (what makes it a *controlled* template).

## The real drift this closes — an open `field_type` vocabulary

The raw ALSAP `form_model` used **21 un-governed `field_type` strings** (`text_version`,
`person_signature_block`, `controlled_choice_plus_rationale`, `narrative_formula`, `boolean_plus_note`,
`repeating_table`, `matrix`, `rule_list`, `structured_method`, …). That is precisely the ungoverned-
vocabulary drift the manifold forbids. The `form` facet closes it to **13 governed input primitives**;
specializations move to `constraints.format` or `meaning.kind`, not to new types. Crosswalk:

| Raw ALSAP `field_type` | Governed → | Note |
|---|---|---|
| text | `text_short` | |
| text_version, version | `text_short` | + `constraints.format: "X.0"` |
| date | `date` | + `constraints.format` |
| person | `person` | blank slot only (filled = PII → submission) |
| person_signature_block | `signature` | Part-11 slot |
| narrative, structured_text, text_schedule, method_narrative, narrative_formula, structured_method | `text_long` | prose specializations collapse |
| repeating_table | `table` | `constraints.repeatable: true` |
| repeating_group, narrative_list | `group` | |
| rule | `rule` | |
| rule_list | `group` of `rule` | **decompose** |
| matrix | `matrix` | |
| controlled_choice_plus_rationale | `select_one` **+** `text_long` | **decompose** into two atoms |
| controlled_choice_plus_narrative | `select_one` **+** `text_long` | **decompose** |
| boolean_plus_note | `boolean` **+** `text_long` | **decompose** |

**The decompose-composite finding.** The bundle's `*_plus_*` types smashed two fields into one — the
same anti-pattern as a `\n`-delimited list. Canon decomposes: a controlled choice and its rationale are
*two* field-atoms, the rationale `conditional_on` the choice. The worked fragment proves this on
Benefit-Risk Profile (choice + rationale) and Event Adjudication (boolean + note).

## `content_disposition` — the template's authoring lifecycle, governed

The FORM's own global rules encode a lifecycle for standard text: retain-unchanged (FORM_RULE_005),
example-may-delete (006), instructional-remove-before-final (007). That is form-specific and had no
home, so it becomes a governed closed list: `controlled_standard | authorable | example |
instructional_transient`. This is what lets a projection know what an author may touch.

## Template vs. submission (protects no-PII)

The `form` facet models the **blank template** — fields, types, rules, roles. A **filled-in form** is a
*submission* (real data, potential PII); it is a record/learner-model object under separate governance
and is never modeled here. `person`/`signature` declare a *slot*, not a person.

## Agent placement

No new agent. This extends the **headwater authoring agent** (`procedure-object-model.md`) to a second
source type. Single-writer over the form `meaning`, the `object` facet, and the new `form` facet;
everyone downstream reads. It wakes on a form/template drop, exactly as the procedural variant wakes on
an SOP.

## Invariant check (fragment passes)

Stable opaque IDs ✓ · single-writer (headwater agent owns `form`) ✓ · reference-don't-embed
(options/roles/records are pointers; only label + constraints embed) ✓ · one canonical source (additive
to `atom.schema.json`; no rival) ✓ · govern-the-vocabularies (`field_type`/`content_disposition` closed,
mirror-checked) ✓ · `content_hash` guards meaning ✓ · no PII (template only; roles, not people) ✓.

## Validation performed (gate cleared — 11/11)

`form.facet.schema.json` is valid Draft 2020-12; all 9 example atoms pass the **unmodified** atom spine;
every `form` binding validates against the facet; the ungoverned `controlled_choice_plus_rationale` is
**rejected**; schema `field_type`/`content_disposition` enums **==** vocab ids (no drifting copy); every
kind/type/disposition used resolves to a governed member; leaves carry `field_type` and containers do
not; all intra-fragment refs resolve; registry-ref ids are well-formed. Run `python3 validate.py` to
reproduce. *(Validation ran against a faithful local mirror of `atom.schema.json`; re-run against the
authoritative in-repo file before merge.)*

## Registry extensions this fragment requires (propose, don't silently invent)

Seeds to add by entry + version bump — NOT ungoverned keys:
- `roles.registry`: `role_alsap_lead`, `role_gso`, `role_medical_lead`.
- `records.registry`: `rec_alsap`.
- a controlled-value registry entry `reg_benefit_risk_profile` (Favorable / Unfavorable /
  Uncertain-Inconclusive / Conditional-Favorable / Contextual / Other — currently ambiguous in source;
  an open SME question: controlled values vs. examples).

## Overlap accepted; `workflow` unification deferred

`performed_by`, `captures_record`, and `conditional_on` also exist on `procedure`. Accepted. If the
duplication ever confuses, lift the shared trio into a `workflow` facet both procedures and forms bind
to — more elegant, more work, and a refactor of an already-validated doc. Not now.

## Next

- Mint the three registry extensions above (gate them like `procedure`'s).
- Resolve the Benefit-Risk `select_one` SME question (controlled vs. example values).
- Then the deferred **prompt pass**: write the headwater agent's form-intake prompt against this facet,
  drawing on the bundle's system/intake prompts as raw material.
- SME surface = the localization/reconciliation loop reapplied (blank-template projection → SME markup →
  reconcile to canon with provenance + version bump + hash recompute).
