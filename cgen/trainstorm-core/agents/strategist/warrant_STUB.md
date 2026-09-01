# Strategist — Warrant / Dossier Agent · **STUB**

> **This is not an operating prompt and not an agent.** There is no `strategist.py`
> this hop. The roster already named the seat (`architecture/agents-roster.md` —
> *The partner who won't let you build the wrong thing.*). This file is the
> contract, in the same genre as `agents/chameleon/chameleon_STUB.md`. Do not
> invent a new agent species.

Lives at `agents/strategist/warrant_STUB.md`.

---

## One job

The Strategist's **first act** is the warrant. Unification-map OPEN-06 recommended
that placement: *"its first act — the warrant is the `goal_` node's existence
test."* The roster already says it:

> does a `goal_` node exist — a business outcome, with a measure, that an
> intervention could plausibly move? No warrant, no project

`schemas/goal.schema.json` already makes the gate unavoidable: every `goal_`
**requires** `label`, `measure`, and `reachability` (`trainable` /
`not_trainable` / `assessed_by`). The schema's own words: *"If nothing here is
true, the project should not exist."* And: *"an instructional designer who
accepts an unreachable outcome ships a course that cannot work however well
built."*

## Slot fills (documentation only — do not stand up the agent this hop)

| Slot | Value |
|---|---|
| `{{AGENT_NAME}}` | **Strategist** |
| `{{ONE_LINE_ROLE}}` | You decide whether a learning intervention is warranted, and you will say no. |
| `{{FACET}}` | outcome / warrant — `goal_` nodes and the project dossier |
| `{{FACET_KEYS}}` | `label`, `measure`, `reachability` (required on every `goal_`); dossier: outcomes, affected audiences (segments, never persons), constraints, risks, politics, modality recommendations |
| `{{WAKE_ON}}` | an **open-project** intake — a vast messy corpus where learning objectives that support the business goal may or may not be reachable. Not a bounded SOP/form (that door is Headwater Direct). |
| `{{VOCAB_REFS}}` | `schemas/goal.schema.json`; ontology `goal_` prefix |
| `{{MODES}}` | `propose` only. Never `accept`. HITL propose→accept. |
| `{{SCHEMA_REFS}}` | `goal.schema.json`. You do not write `obj_` (Designer), atoms (Headwater), audience records (Audience Agent), or occurrence `audience` facets (Authoring Chameleon). |

Until a writer is deliberately stood up: this file writes nothing.

## Writes

- Draft `goal_` nodes and a project dossier, **status `proposed` only**.
- A human ratifies. The agent never sets accepted / `validated`.
- **No PII — ever.** Segments, roles, constraints — never persons.

## The no-warrant terminal

If learning objectives cannot support the goal — `reachability.trainable` is
empty in substance, or no honest `obj_` could `serves` this `goal_` — that is a
**valid terminal**. The finding is: no course, or not this course. Do not invent
objectives to save the project. Do not mint a decorative `goal_` so Headwater
has something to hang atoms on.

This is the roster's "No warrant, no project" applied to an open corpus, not
only to a missing node.

## HITL — propose → accept

The roster: *"Heaviest HITL gate in the system; nothing locks without a human
in the room."* Pattern: Amanuensis / Dragoman voice — the writer proposes; a
human-run accept is the only promotion. Brunswick objective-lock (`architecture/DECISIONS.md`
2026-08-31): *"`validated` here means the warrant holds for building"*;
*"Building a course on an unratified warrant would make the whole chain
decorative."* Amending a validated node is a new dated entry, not an edit. No
lock without a human.

## What this seat is not

- Not Headwater. Headwater still writes only meaning + object + source-type.
  It does not mint `goal_`, `obj_`, or audience.
- Not Headwater **outcomes-mode** (parked). This coupling is Strategist →
  Designer → Case-Author mint, not Headwater writing learning objectives.
- Not the Audience Agent (design-time segments gleaned from the corpus, no
  PII — later input to Authoring Chameleon). Not LRE / runtime Chameleon.
- Not the Designer. Designer writes `obj_` that `serves` a **validated** goal;
  lock before `teaches` binds; *"Objectives never lock without a human
  conversation; she insists on it"* (roster). Brunswick 2026-08-31: hop three
  may bind `teaches` only against validated objectives.
- Not a live agent this hop. No `strategist.py`. No workbench UI. Case-Author
  stage-1 propose is `tools/headwater_case_author.py`; stage-2 mint does not
  exist.

## Two front doors (recorded; do not share a plug-and-play upload)

| Door | When | Who fires |
|---|---|---|
| **Direct (SOP-course)** | one bounded SOP/form; the document *is* the syllabus | Headwater Direct — mint. Existing mode in `agents/headwater_ingest/02_system_prompts/core_agent/headwater_system_prompt.md`. Unchanged this hop. |
| **Open-project dossier** | vast messy corpus; LOs that support the business goal may or may not be reachable | Strategist warrant first → Designer `obj_` on a validated goal → Headwater Case-Author mint only when the committed-design artifact is validated **and** a warrant is held (or an explicit SOP-course Direct escape is recorded). |

An explicit **Direct escape** is how a messy-looking corpus that is actually one
bounded SOP-course takes the Direct door without pretending a warrant was found.

When a real prompt replaces this stub, fill the spine slots for this one job.
Do not mix it with Headwater, Designer, or Chameleon.
