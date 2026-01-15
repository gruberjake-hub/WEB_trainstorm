# AI Learning Runtime

A native web learning system designed to replace legacy slide‑based authoring tools and enable AI‑authored, intent‑driven learning experiences.

---

## Overview

This project provides:

* A lightweight HTML/CSS/JS learning player
* Declarative, JSON‑defined courses
* AI‑assisted authoring workflows
* Accessibility‑first design
* A future path to adaptive, belief‑aware learning

---

## Core Concepts

### Course as Data

Courses are defined in JSON, not slides. The player renders structure and behavior at runtime.

### Intent‑First Design

Learning is designed as a sequence of learner state transitions (psychological, emotional, cognitive).

### No Timelines

Time is observable state (e.g., video playback), not an authoring surface.

### Semantic Video Sync

Video overlays are synchronized using WebVTT cue IDs. Meaning lives in JSON; timing lives in VTT.

---

## Architecture

* `/engine` – core runtime, components, rules, SCORM adapter
* `/courses` – individual course folders
* `/assets` – shared asset library with JSON manifests
* `/brands` – brand themes and tokens

---

## Authoring Workflow

1. Provide design intent or script
2. AI generates `course.json`
3. Human reviews intent and flow
4. Player renders instantly
5. Iterate without re‑authoring

---

## Accessibility

* Native HTML semantics
* Keyboard‑first navigation
* WebVTT captions
* Motion optional and respectful of user preferences

---

## Roadmap

* Expand component library
* Automate script → audio + captions
* Introduce intent metadata
* Enable adaptive generation (internal)

---

## Philosophy

> This system optimizes for learning effect, not slide polish.

AI accelerates execution. Humans retain responsibility for intent, ethics, and outcomes.
