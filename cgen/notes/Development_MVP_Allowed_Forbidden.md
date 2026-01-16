# WEB_TRAINSTORM  
## Development MVP: Allowed / Forbidden List

**Purpose:**  
Deliver Storyline-level *felt completeness* **without** locking the system into legacy interface assumptions.

**Prime Directive:**  
> *Nothing built in Development may encode pedagogy, sequencing, or authorial intent into UI or layout.*

---

## ✅ ALLOWED (Safe to Build)

### 1. Navigation as Runtime Policy
- Central navigation state (`canNext`, `canBack`, `position`)
- Runtime-owned enable/disable logic
- Stateless nav UI bound to runtime state

### 2. Player Chrome as a Theme Surface
- Fixed player shell
- Nav bar / footer / header containers
- Theme-controlled sizing, color, typography

### 3. Fixed Player Geometry
- Locked viewport dimensions
- Stable nav positioning
- Content scroll inside a fixed frame

### 4. Declarative Component States
- Components exposing states: idle, hover, active, feedback
- CSS-driven visuals for each state

### 5. Visual Hierarchy Tokens
- Theme tokens for spacing, rhythm, hierarchy
- Consistent vertical flow rules

### 6. Micro-Transitions as Presentation
- CSS/runtime-controlled transitions
- Uniform scene easing
- Globally adjustable timing

### 7. Progress as Orientation (Not Truth)
- Step indicators
- Section markers
- Approximate learner orientation cues

### 8. Brand Validation Gates
- Brand completeness checks
- Asset resolution validation
- Runtime refusal to init if brand invalid

---

## ❌ FORBIDDEN (Do Not Build)

### 1. Timeline-Based Anything
- Time-encoded scenes
- Instructional delays or choreography

### 2. Slide-Type Logic
- Quiz slides
- Content slides
- Summary slides

### 3. Course-Authored Navigation Rules
- Per-scene nav overrides
- Content deciding nav availability

### 4. Completion-as-Progress
- Slide counts as truth
- Completion derived from traversal

### 5. Interaction-Specific Layout Templates
- Hardcoded quiz layouts
- Fixed answer grids

### 6. Inline Styling in Content
- Per-course CSS
- Content-driven visual overrides

### 7. Logic Hidden in UI
- Buttons making decisions
- UI-bound pedagogy logic

---

## Litmus Test

Before adding anything, ask:

> *Can I replace this UI, change sequencing logic, or reinterpret progress without touching course.json?*

If **yes** → Allowed  
If **no** → Forbidden
