# Chameleon — Audience / Adaptivity Agent · **STUB**

> **This is not an operating prompt and not an agent.** There is no `chameleon.py`
> this hop. The old stub mixed two jobs. They share one facet contract; they do
> not share a wake, and they are not the same build.

Lives at `agents/chameleon/02_system_prompts/core_agent/system_prompt.md` (as a stub).

---

## Two jobs, one facet contract

Chameleon owns the **`audience` facet** — `segment_scope[]`, `difficulty`,
`variant_group` (per `atom-spec` §3). Those keys are the contract. The wake
differs:

| Half | Wake | Static ALSAP course |
|---|---|---|
| **Authoring** | a content-pipeline write — assumed audience, so the course is generated around that impression | **In-scope as a contract.** v1, when it happens, is one documented assumed segment on the ALSAP lesson. **Do not build the agent this hop.** |
| **Runtime** | a learner-context event in the Learner Response Engine / Orchestrator | **Walled. Do not build.** Frontier. |

Without LRE the authored impression is a documented hypothesis, like
Cartographer’s heuristic: honest, flagged, not fake genius. The wake differs
(content-pipeline write vs learner-context event); the facet contract does not.

## Authoring half (in-scope; do not stand up the agent this hop)

Authoring Chameleon would write `audience` facets onto **occurrences**
(`element.audience`), not onto atoms’ meaning, and never PII.

- Same keys the engine would later read: `segment_scope`, `difficulty`,
  `variant_group`.
- **Does not mint `ele_` ids** — Realizer mints occurrences.
- **Does not rewrite atom meaning** — Headwater owns meaning.
- **Does not own style** — Couturier owns `element.expression` style keys.
- **Audience 1:many** is another occurrence of the **same** atom (a second
  `ele_`, `composed_from` that atom) — not a variant SOP, not a parallel
  meaning node, not a rewrite of `atoms.json`.

Until an authoring writer exists, the keys may sit empty. Do not invent
segments. Do not mint SOP variants. Do not build `chameleon.py` this hop.

Runtime / LRE remains **do not build.** Authoring is no longer “writes nothing /
do not build” as a blanket — that wall applied to a mixed job. The authoring
half is allowed to *bind the facet* when a writer exists; this file is still
not that writer.

## Runtime half (walled — Learner Response Engine / frontier)

Runtime Chameleon would wake on a live learner, pick a variant, and join
`audience` hooks to the learner model. That engine is a **separate project
on the frontier**. Building it now would drag LRE into the beta.

Until the Response Engine project is live: **runtime / LRE — do not build.**

## The one invariant that must hold even here

**No PII — ever.** The `audience` facet holds *segment / difficulty / variant*
hooks, never learner data. Real learner state lives in the **learner model** —
a separate, separately-governed store that holds PII. Chameleon, whenever
either half becomes real, reads audience hooks and learner *segments*; it
never writes a person into a content atom or an occurrence. This is also
where the deferred **authored affective/narrative arc** carry stays cleanly
distinct: the *authored* arc is content (near-term, its own facet);
*per-learner* adaptation is the runtime seat.

## When a real prompt replaces this stub

Replace this stub with a spine specialization only for the half that is
actually being built. Slot fills would split:

| Slot | Authoring (static course) | Runtime (LRE — do not build) |
|---|---|---|
| `{{FACET}}` / keys | `audience` — `segment_scope[]`, `difficulty`, `variant_group` on the **occurrence** | same keys, read live |
| `{{WAKE_ON}}` | a content-pipeline graph write (assumed audience on the lesson) | a learner-context event in the Response Engine runtime |
| `{{MODES}}` | authoring bind; one assumed segment at v1 | runtime adaptation; out of scope |
| owner | L&D Adaptivity (authoring) | L&D Adaptivity (runtime) |

The facet contract does not change between halves. The wake does.
Frontier runtime lives in its own repo/project; it imports these schemas but
keeps its own build context.
