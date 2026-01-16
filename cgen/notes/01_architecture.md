# Architecture Overview

## What This System Is

A native HTML / CSS / JS learning runtime where:

* Courses are defined as data (JSON)
* AI is the primary author and compiler
* Humans define intent, constraints, and ethics
* The player renders declaratively at runtime
* Brand and presentation are applied *outside* course content

This is not a slide engine.
This is a **runtime system**.

---

## Core Architectural Principles

### 1. Course-as-Data (Instructional Purity)

* No baked layouts
* No authoring timelines
* No embedded branding
* All instructional structure defined in `course.json`
* Runtime interprets meaning; never hardcodes content

Courses express **intent**, not appearance.

---

### 2. Scene-Based Model

* Slides → scenes
* Layers → overlays
* Timeline → state transitions

Scenes are semantic units, not visual ones.

---

### 3. Declarative Rules Engine

* `event → condition → action`
* No imperative JS wiring per course
* AI-readable and human-auditable
* Deterministic and testable

Rules express *behavioral logic*, not UI logic.

---

### 4. Central State Store

Tracks:

* navigation
* completion
* variables
* decisions
* (future) learner state inference

State is:

* serializable
* inspectable
* portable across runtimes

---

### 5. Media as First-Class Citizens

* Audio per scene
* Captions via WebVTT
* Video is authoritative clock when present
* No trapped or opaque media state

Media never dictates structure — only timing.

---

### 6. SCORM as Adapter, Not Core

* LocalStorage first
* SCORM only for LMS compatibility
* Architecture does not depend on LMS quirks

Learning logic must survive outside the LMS.

---

## Runtime Layering Model (Critical)

The system is intentionally layered to allow **reconstruction, not recall**.

### Layer 1: Instructional Content (Compiler Output)

* `course.json`
* Brand-agnostic
* Deterministic
* AI-generated, human-reviewed
* No styling, no identity, no assets

This layer answers:
**“What should happen?”**

---

### Layer 2: Runtime Engine

* Component rendering
* State management
* Navigation
* Media orchestration
* Rule execution

This layer answers:
**“How does it function?”**

---

### Layer 3: Brand Identity (Who We Are)

* Brand metadata (`*-brand.json`)
* Logos and variants
* Identity rules and constraints
* Non-visual semantics

Loaded at runtime via `brandLoader`.

This layer answers:
**“Who is speaking?”**

---

### Layer 4: Theme / Presentation (How It Looks)

* CSS tokens
* Layout rules
* Component styling
* Brand-scoped visual systems

Applied at runtime via `themeLoader`.

This layer answers:
**“How does it appear?”**

---

## Separation of Concerns (Non-Negotiable)

* Compiler **never** emits branding
* Course data **never** references CSS
* Runtime **orchestrates**, does not decide identity
* Brand defines constraints; theme defines expression
* Visual changes must not affect instructional meaning

---

## Non-Negotiables

* ❌ No timelines
* ❌ No slide metaphors
* ❌ No animation-dependent meaning
* ❌ No hardcoded interactions
* ❌ No branding inside `course.json`
* ❌ No runtime logic inside the compiler

---

## Design Philosophy (Implicit but Enforced)

* Memory is reconstructed, not replayed
* Context is rehydrated, not accumulated
* Structure beats history
* Explicit contracts beat hidden coupling
* Systems should survive cold starts

This architecture is designed to be **resilient to context loss** — human or machine.
