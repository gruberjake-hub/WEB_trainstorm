# Architecture Overview

## What This System Is

A native HTML/CSS/JS learning runtime where:
- Courses are defined as data (JSON)
- AI is the primary author/compiler
- Humans define intent, constraints, and ethics
- The player renders declaratively at runtime

This is not a slide engine.

---

## Core Architectural Principles

### 1. Course-as-Data
- No baked layouts
- No authoring timelines
- All structure defined in JSON
- Runtime interprets, never hardcodes

### 2. Scene-Based Model
- Slides → scenes
- Layers → overlays
- Timeline → state transitions

### 3. Declarative Rules
- `event → condition → action`
- No imperative JS wiring per course
- AI-readable and human-auditable

### 4. Central State Store
Tracks:
- navigation
- completion
- variables
- (future) learner state inference

Serializable and portable.

### 5. Media as First-Class Citizens
- Audio per scene
- Captions via WebVTT
- Video is authoritative clock
- No trapped data

### 6. SCORM as Adapter, Not Core
- LocalStorage first
- SCORM only for LMS compatibility
- Architecture does not depend on LMS quirks

---

## Non-Negotiables

- ❌ No timelines
- ❌ No slide metaphors
- ❌ No animation-dependent meaning
- ❌ No hardcoded interactions
