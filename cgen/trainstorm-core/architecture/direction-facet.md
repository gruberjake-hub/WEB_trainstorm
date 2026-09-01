# The direction facet — and the seat that owns it

*Canonical. Settled in the design beat of 2026-09-01 (after PR #62) and built the same day.
The Claude Project note `claude/design-beat-direction.md` was its draft and is now superseded by
this file. Companion: `lre-stage1-synthetic-learner.md` (the two-stage plan),
`capability_horizon/learner-response-intelligence.capability-horizon.md` (the horizon),
`agents/responsive_engine/` (the seat).*

---

## 1. The question

The audience model landed with a planner-shaped hole: something must read a segment record and
decide how content should LAND for those people. The rehydrated 2026-08 vocabulary called that
"treatment" and proposed eleven values across two levels. Before minting any of it, we tested it
against what the spine already owns.

## 2. The subtraction

Five of the eleven dissolved — they were facets that already exist, under another name:

| proposed "treatment" value | already owned by |
|---|---|
| `assessment-beat` | pedagogical intent (`practice` / `assess`) + `expression.interaction_primitive` |
| `contrast-frame` | the `distinction` script primitive realized through a two-column layout |
| `interaction-prompt` | `expression.interaction_primitive` |
| `emphasis-beat` | `tone.enum.json` (confident / urgent) + rhetorical `persuade` |
| scene-to-scene pacing | Dramaturge's arc — the `pacing_interlude` wake already exists |

What survived is two things the spine genuinely could not say:

- **weight** — within a scene, what is load-bearing and what is subordinate. Implicit in `type`
  today, and nowhere stated.
- **tempo** — dwell, and whether content discloses whole or in parts. The motion registry is where
  tempo is *rendered*; the decision that this should arrive slowly, in three parts, had no home.

## 3. The line (and the test that draws it)

> **Tone, arc and expression are audience-invariant. Direction is the one thing that varies per
> audience segment while meaning, tone and arc all stay fixed.**

An empathetic statement is empathetic for every segment; a closure beat falls in the same place for
everyone; Couturier dresses the occurrence blind to audience. So: *if a proposed field would be set
identically for every segment, it is not direction* — it belongs to tone, arc, or expression. That
test is what keeps a fourth overlapping vocabulary from being minted, and it is written into
`vocab/direction.enum.json` as the governing rule rather than left as an intention.

Two consequences worth stating:

- **Direction cannot live on the element.** The element is audience-invariant; direction is not.
  So it is an external store keyed by `element_id`, one per segment — `direction/<segment_id>.json`
  — pinned against `content_hash`, exactly as locale packs are keyed per language and voice packs
  per register. Dragoman's framing already calls language and register *coordinates in the
  rendering space*; **direction makes the audience segment the third coordinate.** Reason traces
  live per entry in the pack, which answers the long-open `plannerAssessment` question.
- **There is no scene-level direction vocabulary.** A scene's character is the aggregate of its
  elements' weight and tempo. A second enum describing the same thing one level up would drift
  against the first.

## 4. The pack is the audience delta

The resolver computes an audience-blind baseline (weight from rhetorical intent, tempo `measured`)
and writes an entry **only where the resolved binding differs from it**. So a pack contains the
audience delta and nothing else, and the invariance test above is structural rather than
aspirational: a binding that would read the same for every segment cannot get into a direction pack
even by accident. On the paytrans reference course, the reference segment record moves **7 of 70**
elements.

A second discipline follows the same instinct: **direction does not re-emphasise what the content
already emphasises.** An audience rule may promote at most one element per scene to `lead`. A scene
with twenty assertions has an authoring problem, not a direction problem.

## 5. The seat: the Responsive Engine, born in design-time mode

Not a new name. The roster already had the Responsive Engine as the ninth seat — *"designed, not
yet built."* Naming this work anything else would have created two seats destined to argue over the
same territory. So the seat is **activated**, not added, and the count stays nine.

**It owns `direction` and nothing else, and holds no PII in either mode.** The roster's old
one-line entry claimed it also writes "learner × objective runtime state (separate governance,
PII)"; that has been removed, because the horizon already separates the three jobs that line
compressed: **the LRE serves · the Bayesians infer · the Transcript stores.** This seat is the
*decision* half — which is precisely why it can exist before any learner data does.

**Two modes, and the seat declares which one runs** (`agents/responsive_engine/modes.json` — the
precedent is Dramaturge's `wakes.json` and the `seed`/`specified` vocab statuses):

- **`resolve` — live.** Design-time batch: every element × one segment record → a pack of
  `proposed` bindings. A human accepts **bindings**.
- **`serve` — declared, not live.** The same resolver, one element, one live learner, materializing
  nothing. Asking for it is refused with its reason. A human accepts the **policy**, and the
  runtime may serve only what that policy produces.

**The promotion path is not new wiring.** `baseline()`, `propose()` and `clamp()` are pure
functions — dicts in, dicts out, no I/O and no clock. `resolve` runs them under a batch harness;
`serve` will run the same functions under a serve-one harness. Only the harness swaps.

**And the thing that actually promotes it is not the wiring but the evidence.** The discipline
*nothing renders that a human didn't accept* has no runtime version — no one can accept a decision
made 40ms before it is served. So acceptance migrates up a level, from bindings to policy, and the
Stage-1 corpus of reviewed bindings is what licenses accepting a policy at all. That is why the
batch stage has to come first even though it could technically be skipped.

## 6. The harm clamp is now executable (D10)

`risk_of_overuse` was promoted from a metadata note to a gate when the audience model landed. Here
it becomes behavior:

- **high** — never `lead`, never `dwell` (acknowledge, never amplify); cited at most once per pack.
- **moderate** — cited at most once per pack.
- **low** — no constraint.

Two details that matter more than they look. The once-per-pack budget is checked **before** a rule
fires, so a spent factor withholds the **effect**, not merely the citation — an earlier draft
dropped the citation and kept the promotion, which is how *never repeat* quietly becomes *repeat
without saying so*. And the spend is recorded at pack level in `harm_budget`, because it can land
on an element that produces no entry (the rule agreed with the content's own weighting, so there
was no delta to write); without that record, `harm:budget_spent` tokens would point at nothing and
the restraint would be invisible to a reviewer.

## 7. What shipped

| artifact | what it is |
|---|---|
| `vocab/direction.enum.json` | weight (anchor · lead · support · aside) + tempo (brisk · measured · dwell · progressive), closed, versioned. Every value names a rule that can produce it; `pivot` was considered and withheld because nothing writes it. |
| `schemas/direction.pack.schema.json` | the pack: two pins (element meaning, audience analysis), non-empty reason traces, `proposed`/`accepted`, `harm_budget`. |
| `tools/responsive_engine.py` | the seat (policy `direction_v1`): pure core + batch harness + mode refusal. Selftest 14 ways. |
| `tools/validate_direction.py` | the gate: schema · governance · delta · harm · two pins · join · boundary. Selftest proves red 14 ways. |
| `agents/responsive_engine/` | README (spine card), `direction_v1.md` (the rule set), `modes.json` (the declaration). |

## 8. Deliberately not done

- **No direction pack was written into a client project.** paytrans has no segment record — the
  reference record's dispositions are seed values reverse-specified from the course, and planting
  it as project data would let an unearned audience analysis masquerade as a real one. The resolver
  was proven against the real 70-element store with `--dry-run` instead.
- **No renderer reads direction yet.** Couturier will read it as an upstream signal (like tone);
  that is a later hop, and it is why every projection in this hop is byte-identical.
- **`serve` is declared, not built** — see the horizon's activation signals.
