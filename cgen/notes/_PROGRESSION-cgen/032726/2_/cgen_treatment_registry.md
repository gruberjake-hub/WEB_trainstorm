# CGEN Treatment Registry

## Purpose

This registry keeps the planning vocabulary legible across layers so the schema can be read later as a record of system reasoning.

The key distinction is:

- **semanticRole** = what the unit *is*
- **rhetoricalTreatment** = how the unit is rhetorically shaped
- **sceneTreatment** = the dominant experiential mode of the scene
- **unitTreatment** = the experiential role the unit plays inside the scene
- **treatmentHint** = a visual or modality hint for downstream rendering

---

## Layer Map

| Layer | Field | Question it answers | Typical Scope |
|---|---|---|---|
| Semantic | `semanticRole` | What kind of content object is this? | Unit |
| Rhetorical planning | `rhetoricalTreatment` | How is this content being rhetorically handled? | Unit |
| Experience direction | `sceneTreatment` | What is the dominant staged mode of the scene? | Scene |
| Experience direction | `unitTreatment` | What role does this unit play in the staged moment? | Unit |
| Visual intent | `treatmentHint` | What downstream visual treatment might fit? | Unit |

---

## Scene Treatments

| Name | Meaning | Use when | Common signals |
|---|---|---|---|
| `didactic-flow` | Standard instructional delivery with balanced pacing | General explanation scenes | Mixed content, no special emphasis pattern |
| `emphasis-frame` | Sparse scene built around one dominant idea | Key principle, anchor statement, policy takeaway | Sparse scene, strong `Impact`, low element count |
| `progressive-reveal` | Information unfolds step-by-step | Process, sequence, layered concept | Lists, multiple steps, ordered progression |
| `contrast-frame` | Scene organized around tension, comparison, or before/after | Misconception correction, right/wrong, before/after | Paired assertions, dual statements, comparison logic |
| `assessment-beat` | Learner must pause and act | MCQ, check-your-understanding, decision point | Presence of MCQ or explicit learner action |

---

## Unit Treatments

| Name | Meaning | Typical mapped roles |
|---|---|---|
| `primary-assertion` | Core idea of the scene, usually visually dominant | Heading, central claim |
| `supporting-context` | Explanatory or secondary information | Paragraph, statement, support text |
| `emphasis-beat` | A highlighted line meant to land with force | Impact statement, strong takeaway |
| `progressive-step` | One step in a sequence or unfolding explanation | List item, paragraph in progressive reveal scene |
| `contrast-pair` | One side of a comparison or tension | Statement, paragraph, impact in contrast frame |
| `interaction-prompt` | Cue for learner action | MCQ, prompt, action cue |

---

## Rhetorical Treatments

These are lower-level than scene direction. They describe how a semantic unit is rhetorically handled, not how the whole scene is staged.

| Name | Meaning | Typical semantic sources |
|---|---|---|
| `summary-highlight` | Distilled orientation or headline-style framing | Head |
| `supporting-detail` | Secondary elaboration or explanatory detail | Paragraph, List |
| `emphasized-assertion` | Strong, high-salience statement | Impact, Statement |
| `plain-exposition` | Neutral instructional explanation | Paragraph, Statement |
| `knowledge-check` | Assessment-oriented rhetorical handling | MCQ |

---

## How the layers combine

A single unit may carry all of the following without redundancy:

| Field | Example | Meaning |
|---|---|---|
| `semanticRole` | `Impact` | The unit is an impact-style semantic object |
| `rhetoricalTreatment` | `emphasized-assertion` | It is rhetorically framed as a forceful statement |
| `unitTreatment` | `emphasis-beat` | In this scene, it functions as the emphatic landing moment |
| `treatmentHint` | `spotlight` | Downstream visual logic may choose a spotlight-like treatment |

---

## Example Readings

### Example 1

```json
{
  "semanticRole": "Head",
  "rhetoricalTreatment": "summary-highlight",
  "unitTreatment": "primary-assertion"
}
```

Interpretation:
- This is a heading.
- It is rhetorically handled as the orienting summary.
- In the scene, it is the main assertion the learner should anchor on.

### Example 2

```json
{
  "semanticRole": "Impact",
  "rhetoricalTreatment": "emphasized-assertion",
  "unitTreatment": "emphasis-beat"
}
```

Interpretation:
- This is an impact statement.
- It is rhetorically framed as a strong assertion.
- In the scene, it is the main landing beat.

### Example 3

```json
{
  "sceneTreatment": "progressive-reveal",
  "semanticRole": "List",
  "rhetoricalTreatment": "supporting-detail",
  "unitTreatment": "progressive-step"
}
```

Interpretation:
- The scene is staged as an unfolding sequence.
- This list carries supporting detail rhetorically.
- But experientially, it functions as a step in the reveal.

---

## Registry Template for Growth

Use this section as the pattern whenever you add new vocabulary.

| Field Family | Name | Definition | Trigger signals | Runtime implications | Notes |
|---|---|---|---|---|---|
| rhetoricalTreatment |  |  |  |  |  |
| sceneTreatment |  |  |  |  |  |
| unitTreatment |  |  |  |  |  |
| treatmentHint |  |  |  |  |  |

---

## Suggested Governance Rule

When adding a new planning term, decide first which family it belongs to:

1. **Is it describing what the content is?** → `semanticRole`
2. **Is it describing rhetorical framing?** → `rhetoricalTreatment`
3. **Is it describing the dominant experiential mode of the scene?** → `sceneTreatment`
4. **Is it describing the experiential role of a unit inside a scene?** → `unitTreatment`
5. **Is it only a downstream visual/render suggestion?** → `treatmentHint`

If a term seems to fit more than one family, that is usually a sign the definition needs sharpening.

---

## Current Working Principle

The system should be readable later as a chain of thought encoded in schema:

**what it is → how it is framed → how it should land → how it might render**
