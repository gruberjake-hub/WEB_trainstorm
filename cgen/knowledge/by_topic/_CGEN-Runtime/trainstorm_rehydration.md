# 🧠 REHYDRATION SCRIPT  
**Trainstorm Course Generator — Semantic → Planning → Runtime Pipeline (Checkpoint v1.2)**

---

## CONTEXT

I am building a system called **Trainstorm Course Generator (CGEN)**.

The goal is to:

> Fully automate high-quality eLearning course creation by separating:
- meaning
- instructional intent
- experience design
- runtime rendering

This is NOT a simple content generator.

It is a **multi-stage compiler pipeline for learning experiences**.

---

## CORE ARCHITECTURE

The system is composed of staged transformations:

```
PROJECT CORPUS
→ SCRIPT
→ SEMANTIC MODEL (course.semantic.json)
→ RENDER PLAN (render-plan.json)
→ RUNTIME COURSE (course.json)
→ BROWSER EXPERIENCE
```

---

## LLM vs DETERMINISTIC SPLIT

### LLM is used for:
- interpreting source material
- generating instructional scripts
- structuring semantic meaning
- defining learner outcomes and intent

### Deterministic system is used for:
- schema validation
- structural transformation
- pedagogic rule application
- runtime compilation
- rendering

### Critical boundary:

> The **semantic model is the handoff point**  
Before it = interpretation  
After it = compilation

---

## CURRENT IMPLEMENTATION (WORKING)

### 1. Semantic Layer
File:
```
courses/demo/course.semantic.json
```

Contains:
- scenes
- sceneIntent
- learnerOutcome
- semantic elements:
  - Head
  - Paragraph
  - Impact
  - List
  - Statement
  - MCQ

Optional:
- `modalityHint` (light hint only, not binding)

---

### 2. Planning Layer (DETERMINISTIC)
File:
```
planner/planCourse.js
```

Output:
```
courses/demo/render-plan.json
```

Planner determines:

- renderUnits
- instructionalIntent
- rhetoricalWeight
- treatment
- learnerAction
- renderType
- primitive
- styleRef
- completionPlan
- narrationPlan
- motionPlan

Recently added:
- **visualIntent** (light modality planning, not asset binding)

---

### 3. Runtime Compilation Layer
File:
```
compiler/renderPlanToCourse.js
```

Output:
```
courses/demo/course.json
```

Transforms:
- renderUnits → runtime components
- scenePlans → runtime scenes
- narrationPlan → voiceover
- completionPlan → completion config

---

### 4. Runtime
Files:
```
courses/demo/index.html
courses/demo/main.js
engine/*
```

Handles:
- rendering components
- navigation
- interactions (RevealCards, MCQ)
- basic course flow

---

## CURRENT STATE OF THE SYSTEM

### What works

- End-to-end pipeline from semantic → runtime
- Scenes render correctly
- Interactions function (RevealCards, MCQ)
- Navigation works
- Planner correctly interprets semantic structure
- MCQ correctly treated as knowledge-check
- Visual intent scaffolding exists

---

### What it feels like

> “Clear, structured, but flat”

The course:
- is legible
- is organized
- is technically correct

But:
- lacks energy
- lacks staging
- lacks visual hierarchy
- lacks emotional weight
- lacks pacing and rhythm

---

## ROOT DIAGNOSIS

The system currently models:

> **meaning and structure**

But does NOT yet model:

> **experience and staging**

---

## WHAT IS MISSING

A new planning dimension:

> **Experience Treatment Layer**

The system currently answers:
- what something is
- how it should be structured

It does NOT yet sufficiently answer:

- how this moment should feel
- how information should be staged
- when to be sparse vs dense
- when to emphasize vs explain
- when to shift modality
- how to create rhythm and contrast

---

## NEXT EVOLUTION

We need to introduce:

### **Scene-Level Experience Treatment**
Examples:

- didactic-standard
- emphasis-sparse
- structured-reveal
- contrast-frame
- knowledge-check
- summary-land

### **Unit-Level Treatment Enhancements**
Examples:

- emphasis-beat
- supporting-text
- contrast-assertion
- progressive-build
- reflective-pause

---

## KEY PRINCIPLE

> The system must evolve from:
>
> **content generator**
>
> to:
>
> **experience director**

---

## DESIGN PHILOSOPHY

### Layer responsibilities

| Layer | Responsibility |
|------|------|
| Semantic | meaning |
| Planning | pedagogic strategy |
| Treatment (NEW) | experience design |
| Runtime | execution |

---

## IMPORTANT CONSTRAINTS

- Do NOT collapse layers
- Do NOT push runtime concerns upstream
- Do NOT bind assets at semantic level
- Keep system deterministic after semantic stage
- Maintain auditability and consistency

---

## CURRENT FILE STRUCTURE (RELEVANT)

```
cgen/
├── planner/
│   └── planCourse.js
├── compiler/
│   └── renderPlanToCourse.js
├── courses/demo/
│   ├── course.semantic.json
│   ├── render-plan.json
│   ├── course.json
│   ├── index.html
│   └── main.js
├── engine/
│   ├── runtime.js
│   ├── components/
│   └── store.js
```

---

## CURRENT DEVELOPMENT WORKFLOW

```bash
node planner/planCourse.js courses/demo/course.semantic.json
node compiler/renderPlanToCourse.js courses/demo/render-plan.json
python -m http.server 8000
```

Then open:

```
http://localhost:8000/courses/demo/
```

---

## CURRENT GOAL

Transition from:

> working structured demo

to:

> **compelling, staged, living learning experience**

---

## NEXT TASK

Define and implement:

> **Experience Treatment System**

This includes:

1. Define scene-level treatment vocabulary
2. Extend planner to assign treatments
3. Modify render-plan to include treatment signals
4. Eventually adapt runtime behavior and styling based on treatment

---

## WHAT I WANT FROM YOU (NEXT INFERENCE)

Help me:

1. Define a **minimal but powerful set of experience treatments**
2. Integrate them into the planning layer
3. Keep the system clean, scalable, and deterministic
4. Avoid premature visual/asset complexity
5. Move toward a system that can replicate high-quality instructional design decisions

---

## FINAL SUMMARY

> The pipeline works.  
> The system understands meaning.  
> Now it must learn how to *stage experience*.
