# The Script / Generation Layer — Placement

### Where `script.primitives` sits in the architecture, and how it connects to elements

**What it is:** the **semantic generation layer** — the intermediate representation between raw source and presentation. A *script* is an ordered array of **didactic moves** (definition, distinction, process_flow, context_frame…), each a *typed knowledge structure*, emitted from source material before anything is laid out. It's the most content-pure layer in the stack: a `definition` is a definition regardless of how it's later drawn.

**Why it was the missing layer:** our unified `element.schema.json` models the *presentation* unit (Head/Statement/List + rhetorical intent + expression). The script primitive models the *knowledge* unit above it. Content-vs-expression separation, one level up.

---

## 1. The pipeline

```
 source material
      │  (generator agent)
      ▼
 SCRIPT PRIMITIVES        ← script.primitives.v1.json   · WHAT knowledge, structurally
   (definition, distinction, process_flow, …)
      │  (realizer agent — the realization table below)
      ▼
 ELEMENTS                 ← element.schema.json          · HOW it's presented
   (Head, Statement, List, … + rhetorical intent + expression keys)
      │  (render agents — AE/Lottie/HTML → Storyline)
      ▼
 RENDERED FORMS
```

Two agents live in that pipeline: a **generator** (source → primitives) and a **realizer** (primitives → elements). Both fit the hub-and-spoke — each reads the layer above and writes the layer below; neither talks to the other directly.

---

## 2. The derivation link (provenance all the way down)

A primitive realizes into **one or more** elements. Stamp each element with the primitive it came from, so the chain source → primitive → element → render is fully traceable:

```jsonc
// on the element (a small addition to element.schema.json)
"derivation": {
  "realizes_primitive": "p003",     // the script primitive's id
  "script_ref": "brunswick.script.v2"
}
```

This is the same `content_hash` discipline extended across layers: if a primitive changes, you can find and re-realize exactly the elements that derived from it — nothing else.

---

## 3. The intent lattice (this is a NEW axis, not a rival)

`script.primitives` fills the empty slot. Five independent descriptors, five different questions:

| Axis | Question | Source of truth |
|---|---|---|
| `type` | what shape on screen? | element.schema |
| rhetorical intent | what does it do communicatively? | intent.enum · rhetorical |
| pedagogical intent | its role in the learning sequence? | intent.enum · pedagogical (Gagné) |
| **content primitive** | **what knowledge-move is it?** | **script.primitives** |
| bloom | cognitive level? | element.schema |

Each primitive has a **natural default pedagogical intent** (the generator can set it automatically):

| Primitive | Default pedagogical intent |
|---|---|
| orientation | objective |
| context_frame | hook / activate |
| definition | present |
| decomposition | present |
| distinction | exemplify |
| process_flow | exemplify |
| role_relevance | activate / transfer |
| knowledge_check | practice / assess |
| boundary_statement | present |
| resource_pointer | transfer |
| closure | reinforce |

---

## 4. The realization table (the realizer's contract)

How each primitive becomes elements. This is a **starter** — refine against your primitive/layout registries. Where a primitive routes to `interaction_primitive`, its `delivery` is behavior-driven (Storyline); otherwise didactic (AE/Lottie), consistent with the pedagogical→delivery routing.

| Primitive | Realizes into (elements) | Layout / interaction primitive | delivery |
|---|---|---|---|
| orientation | `Head` (orient) [+ `SubHead`] | TitleCard / TopTitle | didactic |
| context_frame | `Statement` (problem) + `Impact` (risk) | CenterEmphasis | didactic |
| definition | `Head` (term) + `Statement` (meaning) | DefinitionCard | didactic |
| decomposition | `ListHead` + `List` + `ListItem`×n | Cards / PillarGrid | didactic |
| distinction | two `Statement`s (or `Impact`) | TwoColumn / Versus | didactic |
| process_flow | `List` + `ListItem`×n | ProcessFlow / Timeline | didactic |
| role_relevance | `Statement` / `Impact` | RelevanceCallout | didactic |
| knowledge_check | interaction node + options | ClickToReveal / MCQ | **interactive** |
| boundary_statement | `Statement` (callout style) | Callout | didactic |
| resource_pointer | `Statement` (system-callout style) | SystemCallout | didactic |
| closure | `Head` + `List` (recap) + `Impact` (takeaway) + CTA | RecapList + BottomCTA | didactic |

Note two things this encodes cleanly: a `decomposition`/`process_flow` produces the **decomposed list model** (container + `ListItem` children with parent refs — the representation your standalone scene file already evolved toward), and a `boundary_statement`/`resource_pointer` becomes a `Statement` rendered via a **callout** primitive — confirming "callout is a role, not a type."

---

## 5. Governance

`script.primitives` is a **governed, closed vocabulary**, like `intent.enum.json`. The 11 primitive types are the complete set; a new one requires a **version bump** and a typed `$def` — the schema rejects anything else (verified: it rejects an ungoverned `epiphany` type and an underspecified `distinction`). The linter should validate scripts against this schema, exactly as it validates courses against the element schema.

---

## 6. One optional upgrade

Today a script is a bare array of primitives (faithful to your v1). When you're ready, wrap it with light metadata so scripts are addressable and traceable:

```jsonc
{ "script_id": "brunswick.script.v2", "source_ref": "…", "course_id": "…",
  "primitives": [ /* the array */ ] }
```

Not required now — but it's the hook for source→script provenance, the same way `course_id` anchors the course.

---

## Where this leaves the stack
- **`script.primitives.v1.json`** — generation IR (WHAT knowledge). *New spoke, now complete.*
- **`element.schema.json`** — presentation unit (HOW shown). Add the `derivation` link.
- **`intent.enum.json`** — the governed rhetorical + pedagogical vocabularies.
- **render agents** — AE / Lottie / HTML → Storyline.

The generator emits primitives; the realizer turns them into elements; the render agents draw them. Three clean transforms over one traceable chain.
