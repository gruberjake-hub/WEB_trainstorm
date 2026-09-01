# direction_v1 — the resolver's rule set (2026-09-01)

Direction is **what varies per audience segment while meaning, tone and arc stay fixed**. Two axes,
governed in `vocab/direction.enum.json`: **weight** (anchor · lead · support · aside) and **tempo**
(brisk · measured · dwell · progressive).

## Two structural disciplines

**1 · A pack is the audience delta, not a description.** The resolver computes an audience-blind
`baseline()` — weight from rhetorical intent, tempo measured — and writes an entry **only where the
resolved binding differs from it**. A binding that would read the same for every segment is tone,
arc or expression by direction's own test, so it cannot end up in a direction pack even by
accident. On the paytrans reference course, one segment record moves **7 of 70** elements.

**2 · Direction does not re-emphasise what the content already emphasises.** An audience rule may
promote at most **one element per scene** to `lead`. The content's own weighting is left alone; a
scene with twenty assertions has an authoring problem, not a direction problem.

## The rules, in fixed order (a reviewer must be able to replay them)

| # | rule | fires when | effect |
|---|---|---|---|
| 1 | `intent_default` | always | weight from `intent.rhetorical`; tempo `measured` — the baseline |
| 2 | `belief_gap_lead` | element teaches an objective a `gap_` factor targets | weight → `lead` |
| 3 | `threat_anchor` | a `thr_` factor targets it **and** `identity_safety < 0.5` | weight → `anchor`; **overrides 2 — safety before correction** |
| 4 | `cadence_chunk` | `chunk_tolerance = short` and the element is a `List` | tempo → `progressive` |
| 5 | `density_shed` | `density_tolerance = sparse`, weight `support`, teaches nothing | weight → `aside` |
| 6 | `low_efficacy_dwell` | `self_efficacy < 0.5` and it teaches an objective at mastery `< 0.3` | tempo → `dwell` |
| 7 | `known_brisk` | every objective it teaches is at mastery `>= 0.6` | tempo → `brisk` |

v1 acts on `gap_` and `thr_` factors, the four baselines, cadence and mastery. The other factor
families (`inh_`, `obj_x_`, `aln_`, `mng_`, `rat_`) are **read but unused** — later rule sets, not
silent behavior.

## The harm clamp (D10)

`risk_of_overuse` is the roster's one hard ethical rule, and here it is a gate rather than a note:

- **high** — never `lead`, never `dwell`, cited at most **once per pack**.
- **moderate** — cited at most **once per pack**.
- **low** — no constraint.

Two details that matter more than they look:

- The once-per-pack budget is checked **before** a rule fires, so a spent factor withholds the
  **effect**, not merely the citation. (An earlier draft dropped the citation and kept the
  promotion — which is how *never repeat* quietly becomes *repeat without saying so*.)
- The budget is recorded at pack level in `harm_budget`, because a spend can land on an element
  that produces no entry — the rule agreed with the content's own weighting, so there was no delta
  to write. Without that record, `harm:budget_spent` tokens would point at nothing.

## Reason traces

Every entry carries a non-empty `reason`: short governed tokens (`rule:` · `factor:` · `baseline:` ·
`cadence:` · `mastery:` · `harm:`), never prose and never a confidence value. A binding that cannot
say why it exists cannot be reviewed — and reviewed bindings are what will eventually license
accepting a **policy**, which is the only way the "nothing renders that a human didn't accept"
discipline survives a runtime with no human in it.
