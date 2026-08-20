# Amanuensis — first live dispatch · 2026-08-20

Seven dispatches (five, then two after fixes). Each ran in a fresh context whose entire world was one
resolved payload file: no conversation history, no repo access, one `Read` and nothing else. Every
agent confirmed in its self-check that it used no other tool and invented no ALSAP content.

The point was not to produce ALSAP text. It was to answer a question the purity check cannot:
**`--verify-prompt` proves no ALSAP content is IN the prompt; it says nothing about whether the walk
result is ENOUGH.** So: is the grounding packet sufficient?

## Verdict

**No — and the reason is structural, not a bug.** All five first-round dispatches independently
refused to draft, and all five gave the same root cause: the packet carries template structure,
drafting guidance and governing procedure — grounding for *what a slot requires and who owns it* —
and **no evidence whatsoever about the asset being documented.** No safety data, no adverse-event
terms, no participant counts, no asset identity. Every `authorable` slot in an ALSAP is authored
*from asset evidence*, and there is no asset-dossier corpus in the manifold.

That is the finding. It cannot be fixed in the resolver, and it means:

> **Amanuensis is usable today as a reviewer, not as a drafter.** `check` mode works on template
> grounding alone — it verified disposition, instructional-text leakage and governed-value
> consistency against a real draft. `draft` mode is blocked until an evidence corpus exists.

The `check`/`draft` asymmetry was surfaced by the agent itself, unprompted, and is the most
actionable result of the exercise.

## What held

- **"Flag, never invent" held under pressure — 7/7.** Not one dispatch filled a gap with plausible
  prose, and several explicitly declined a tempting inference. The `author` dispatch refused to
  answer "ALSAP Lead" from `accountable` + `performed_by`, flagging that "accountable for the field"
  is not "the value of the field."
- **Disposition posture was correct in every case.** `controlled_standard` → refused to redraft.
  `example` → produced a decision, not prose, and refused to import the `controlled_standard`
  "Not Applicable" fallback across dispositions. `select_one` → consulted the governed set, selected
  nothing, proposed no seventh value.
- **The no-PII rule bit where it should.** The `person` field on the cover was refused on PII
  grounds, not just on absence of data.

## Defects found, and what was done

| # | Finding | Status |
|---|---|---|
| 1 | Packet carries no asset evidence — blocks all drafting | **OPEN — needs a new corpus.** Recorded as the next rung. |
| 2 | `gaps: []` reports *assembly* completeness; agents read it as licence to proceed | **FIXED** — new `sufficiency` block states plainly what the packet does and does not carry, and gives a per-slot verdict. |
| 3 | A conditional slot got the controlling field's *identity* but not its value set, its type, or the predicate — "the selected profile" had no referent | **FIXED** — `this_slot_applies_when` now resolves the controlling field, inlines its governed options, and names an absent predicate explicitly. |
| 4 | Nothing showed what had already been authored for the asset | **FIXED** — `--instance` adds `instance_so_far` (this slot, the fields it depends on, decisions, governance, staleness). This is what makes `check` mode work. |
| 5 | Roles/records arrived as display labels, so the agent could not run the ungoverned-value drift check its own contract demands | **FIXED** — `idlabel()` carries `{id, label, governed}`. |
| 6 | `disposition_decision` vocabulary absent from the packet; one agent invented the token `as_is` and flagged it | **FIXED** — governed set is handed over in `disposition_decisions_available`. |
| 7 | No `governance`/version on the slot or the options set, so a binding could not record what it resolved against | **FIXED** — `governance` on the slot; instance atoms carry theirs. |
| 8 | `{{FACET}}` rendered as `*(none — see the write-contract deviation below)*`, producing sentences like "Always: write only *(none …)*". Two agents flagged it independently. | **FIXED** — `{{FACET}}` is `instance`, plus an explicit "read every *write* in the spine as *propose*" clause. |
| 9 | The disposition table had no row for `controlled_standard` **with** `constraints.slots`, so the agent read the v0.2 named-slot feature as a contradiction and refused entirely | **FIXED** — row added; the wake condition now covers it too. |
| 10 | Specialization still cited `instance.facet.schema.json` as *(proposed)* | **FIXED** — it was built and gated the same day. |
| 11 | Agent expected a `retained_with_fills` decision for a slotted `controlled_standard` field | **CLARIFIED in packet** — a slot you *fill* owes no decision; the fills are the record. The gate already implemented this; only the packet was silent. |
| 12 | The ten phrasing atoms are `instructional_transient` yet appear in the conditional graph as `fields_conditional_on_this_slot`, i.e. as document content | **OPEN — modelling.** Two agents flagged it. Guidance that is deleted before final should probably not present as a conditional *field*. |
| 13 | `f_br_rationale`'s `conditional_on` carries no `equals`, unlike its ten siblings | **OPEN — decomposition.** The packet now says the predicate is unspecified rather than passing `null` silently. |

## Effect of the fixes

The second round drew a visibly different response. On the `narrative` slot the agent moved from
*"I may not touch this at all"* to correctly stating it may draft **only the four named spans** and
must quote the sentence unchanged — the v0.2 feature working as designed — and it cited the packet's
own `sufficiency` verdict as its reason for stopping. Its packet feedback: *"Unusually good. The
`sufficiency` block stated its own insufficiency plainly and pre-empted the failure mode."*

## Honest limits of this exercise

- Dispatch was by subagent, not by an API call — there is no `ANTHROPIC_API_KEY` in the build
  environment. `resolve_prompt.py` emits a complete `{system, messages, meta}` payload; what carries
  it to a model is environment-specific and deliberately outside the tool.
- "It used no other tool" rests on the agents' own self-reports plus a tool-use count of 1 per
  dispatch. That is good evidence, not proof.
- Seven dispatches on one template vertical. Enough to find structural defects; not a sample.
