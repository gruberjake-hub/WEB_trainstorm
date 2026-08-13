# Chameleon — Audience / Adaptivity Agent · **STUB (do not build yet)**

> **This is a placeholder, not an operating prompt.** It exists to hold the seat, document the wall, and
> stop anyone (including a future us) from building this agent prematurely. It does **not** fill the spine's
> slots as a working agent. When the frontier project is stood up, replace this file with a real spine
> specialization — until then, Chameleon writes nothing.

Lives at `agents/chameleon/02_system_prompts/core_agent/system_prompt.md` (as a stub).

---

## Why this is walled off

Chameleon would own the **`audience` facet** — the adaptivity hooks: `segment_scope[]`, `difficulty`,
`variant_group` (per `atom-spec` §3, owner: L&D Adaptivity). But the thing that gives that facet meaning
— an engine that **reads those hooks live and adapts the content per learner** — is the **Response Engine
/ Orchestrator**, which canon explicitly keeps as a **separate project on the frontier**, not on the
near-term production pipeline. Building an operating Chameleon now would drag that frontier into the beta.

So the near-term posture is deliberate: the atom may still **carry** the `audience` facet as *inert keys*
(authored variants, difficulty tags), but **no agent adapts on them** in the production pipeline. The
hooks sit in the graph, dormant, waiting for the engine that reads them.

## The one invariant that must hold even here

**No PII — ever.** The `audience` facet holds *segment / difficulty / variant* hooks, never learner data.
Real learner state (mastery, motivation, identity) lives in the **learner model** — a separate,
separately-governed store that holds PII. Chameleon, whenever it becomes real, reads audience hooks and
learner *segments*; it never writes a person into a content atom. This is also where the deferred
**authored affective/narrative arc** carry stays cleanly distinct: the *authored* arc is content
(near-term, its own facet); *per-learner* adaptation is this frontier seat.

## When it activates (the hand-off to a real prompt)

Replace this stub with a spine specialization only when the Response Engine project is live. At that point
the slots would fill roughly:

| Slot | (frontier) value |
|---|---|
| `{{FACET}}` / keys | `audience` — `segment_scope[]`, `difficulty`, `variant_group` |
| `{{WAKE_ON}}` | a learner-context event **in the Response Engine runtime** — not a content-pipeline graph write |
| `{{MODES}}` | — (runtime adaptation; out of scope for the authoring pipeline) |
| owner | L&D Adaptivity (runtime) |

Until then: **stub. Do not build.** Frontier lives in its own repo/project; it imports these schemas but
keeps its own build context.
