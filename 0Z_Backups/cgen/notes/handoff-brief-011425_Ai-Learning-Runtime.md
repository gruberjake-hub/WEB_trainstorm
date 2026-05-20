# AI‑Driven Native Web Course Engine

## Handoff Brief (Authoritative)

### Purpose

Provide a complete context transfer so another AI instance can continue building the system without loss of architectural, philosophical, or tactical intent.

---

## Identity (Non‑Negotiable)

**This is NOT:**

* A Storyline clone
* A slide authoring tool
* A front‑end tutorial
* Timeline‑based animation software

**This IS:**

* A native HTML/CSS/JS learning runtime
* Courses defined as data (JSON)
* AI as primary author/compiler
* Human as intent, constraint, and ethics authority

---

## Core Philosophy

**Unit of design = learner state transition**

Design focuses on:

* Psychological state
* Emotional posture
* Cognitive clarity
* Agency and trust

Content is an *expression* of intent, not the intent itself.

---

## Architecture (Already Implemented)

### Player / Runtime

* Native web (HTML/CSS/JS)
* Single `.app` container
* Player‑owned header, stage, nav, footer
* Scene‑based rendering
* Central state store
* Declarative rules engine
* Audio + WebVTT captions
* Thin SCORM adapter (compatibility only)

### Implemented Components

* Heading
* Body
* RevealCards
* MCQ

---

## Course Schema (v1 – Stable)

```json
{
  "meta": { "id": "", "title": "", "theme": "", "client": "" },
  "nav": { "startSceneId": "" },
  "scenes": [ { "id": "", "title": "", "components": [] } ],
  "rules": []
}
```

Additive extensions only. No breaking changes.

---

## Time, Video, and Overlays

* No timelines
* Time is observable *state*, not UI
* Video is the authoritative clock
* Synchronization via WebVTT cue IDs
* VTT contains **semantic IDs only**, never learner‑facing text

Meaning lives in JSON; timing lives in VTT.

---

## Asset Strategy

* Central asset library
* Each asset has a matching `.json` manifest
* Manifests encode intent, constraints, and allowed usage
* Assets are referenced, not copied
* Client restrictions are metadata‑based, not folder‑based

---

## AI Role

AI acts as:

* Course architect
* Instructional compiler
* Structure generator
* Script and caption generator

AI does **not** decide goals or values.

---

## Human Role

Human provides:

* Desired learner state (from → to)
* Psychological and emotional intent
* Ethical and brand constraints
* Final approval

Human does **not** hand‑wire interactions.

---

## Long‑Term Vision (Not Yet Marketed)

* Probabilistic learner state model
* Bayesian belief updates
* Adaptive generation via evolving prompt context
* Fixed goals, adaptive paths

---

## Immediate Next Steps

1. Lock v1 course schema
2. Add components: ImageWithCaption, Video (static), ScenarioPrompt, KnowledgeCheck
3. Implement script → audio + WebVTT pipeline
4. Create “Course Compiler” prompt (human‑in‑loop)
5. Generate one real course end‑to‑end

---

## Guardrails

* No timelines
* No slide metaphors
* No animation required for comprehension
* No opaque AI persuasion

---

## North Star

> If the system optimizes for output instead of learner state, refactor.
