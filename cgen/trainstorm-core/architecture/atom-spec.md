# The Content Atom — Schema Spec

### The smallest buildable thing under the manifold

**What this is:** the concrete shape of a single content atom — the node everything else in the architecture hangs off. An engineer can start typing from this today.
**Files in this package:**
- `atom.schema.json` — the formal JSON Schema (draft 2020-12), validatable.
- `example_atom.json` — a worked instance (the AST009 "Recognize product safety information" atom), which **validates against the schema**.
- this spec — the annotated reading.

**Date:** 20 July 2026

---

## 1. The one rule

**The atom is thin. It owns its *meaning* and nothing else — every rendering is a reference.**

- The atom holds the **canonical source meaning** (one string, audience-agnostic) plus **keys** into the sub-models.
- It does **not** hold: translations, visual styles, objectives, or learner data. Those live in external stores keyed by `atom_id`.
- **One agent writes each binding** (single-writer). Everyone else reads. That is what keeps the whole system decoupled and lets ownership map straight to governance.

If you remember only one thing: **change a rendering in its own store, and every atom that references it updates — because the atom never held a copy.**

---

## 2. The atom, annotated

```jsonc
{
  "atom_id": "atom_ast009_recognize_psi",   // stable, opaque, durable — the join key everywhere
  "content_hash": "sha256:3b7e9a…",         // hash of meaning; detects real change vs. a moved id

  "meaning": {                              // THE ONLY EMBEDDED PAYLOAD — the invariant truth
    "source_locale": "en",
    "source_text": "Recognize product safety information",
    "kind": "objective_statement"           // semantic kind (NOT a visual type)
  },

  "bindings": {                             // keyed references into the sub-models
    "object": {                             // owner: Content Architecture — structure
      "belongs_to": "atom_ast009_slide_1_3",
      "order": 4,
      "prerequisites": ["atom_ast009_def_psi"]
    },
    "intent": {                             // owner: L&D / ID — meaning/purpose
      "teaches": ["obj_recognize_psi"],     // → objective node in the intent ontology
      "intended_response": "discriminate reportable from non-reportable",
      "bloom": "analyze"
    },
    "expression": {                         // owner: Brand + Localization — KEYS into registries
      "content_type": "instructional.objective",   // → visual registry → motion/type/brand tokens
      "register": "formal",
      "term_refs": ["term_safety_mgmt_info"]        // → glossary registry (locked terminology)
    },
    "audience": {                           // owner: L&D Adaptivity — FIT HOOKS only (no PII)
      "segment_scope": ["tier1_field", "tier1_psp", "tier2_msl"],  // design-time RBT targeting
      "difficulty": 0.3,
      "variant_group": "vg_recognize_psi"   // engine picks one variant per learner
    }
  },

  "governance": {                           // owner: Governance / Quality — provenance
    "version": 3,
    "status": "approved",
    "regulatory_binding": "regulatory",     // drives controlled-translation + review lane
    "owner": "pv_content",
    "approved_by": ["qa_jsmith"],
    "effective_date": "2026-07-15"
  }
}
```

That is the entire atom. Notice how little it is: one real sentence of content, and the rest is pointers.

---

## 3. The bindings, and who owns each

| Binding | Answers | Holds (references, not copies) | Single writer |
|---|---|---|---|
| **object** | *what / where* | `belongs_to`, `order`, `prerequisites[]` (atom_ids) | Content Architecture |
| **intent** | *why* | `teaches[]` (objective_ids), `intended_response`, `bloom` | L&D / Instructional Design |
| **expression** | *how* | `content_type`, `register`, `term_refs[]` — keys into registries | Brand + Localization |
| **audience** | *for whom* | `segment_scope[]`, `difficulty`, `variant_group` — fit hooks | L&D Adaptivity |
| *(governance)* | *is it trustworthy* | version, status, approvals, regulatory flag | Governance / Quality |

`bindings` is **extensible** (`additionalProperties` allowed): when a new agent needs a new facet, it adds a new named binding — it does not modify the existing ones. That is the "facets accrete, the spine stays small" principle, enforced by the schema.

---

## 4. What lives OUTSIDE the atom (the reference targets)

The atom is a hub of keys. Here is what those keys point at — each a separate store, each keyed by `atom_id` or by the ref id:

**Locale pack** — `locales/ja.json` (owner: Localization; the localization facet):
```json
{
  "atom_ast009_recognize_psi": {
    "target": "製品の安全管理情報を見分ける",
    "status": "validated",
    "reviewer": "jp_incountry",
    "source_hash": "sha256:3b7e9a…"      // ties this translation to the meaning it was made for
  }
}
```

**Glossary registry** — `registry/glossary.json` (owner: Localization + PV):
```json
{ "term_safety_mgmt_info": { "en": "product safety information", "ja": "安全管理情報", "locked": true } }
```

**Visual registry** — `registry/visual.json` (owner: Brand):
```json
{ "instructional.objective": { "type_scale": "h3", "motion": "fade-in", "brand_token": "surface.instructional" } }
```

**Intent ontology** — `ontology/objectives.json` (owner: L&D):
```json
{ "obj_recognize_psi": { "label": "Recognize PSI", "requires": ["obj_define_psi"], "framework": "CASE" } }
```

**Learner model** — `learners/*` (owner: Data Privacy / DPO — **separate governance, holds PII**):
```json
{ "learner_2841": { "segment": "tier1_field", "mastery": { "obj_recognize_psi": 0.4 } } }
```

The atom touches none of these directly — it just carries the keys. Swap a locale, relock a term, restyle a `content_type`, revise an objective: the atom is untouched and every atom that references the changed thing updates at once.

---

## 5. How it all resolves at render time

To render this atom **for a specific learner**, the responsive engine walks the keys:

1. **meaning** → take `source_text`; if the learner's locale ≠ source, resolve `locales/<locale>[atom_id].target` (fall back to source if not validated).
2. **expression** → resolve `content_type` in the visual registry → tokens; enforce `term_refs` against the glossary (locked terms win).
3. **intent** → look up `teaches[]` in the ontology to know what this atom is *for* (used for sequencing and for scoring).
4. **audience (the join)** → match `segment_scope` + `difficulty` against the **learner model** (`learners[id]`); pick the right `variant_group` member for this learner's mastery.
5. **govern** → only render atoms whose `status = approved`; log which versions/refs were used (provenance).

Steps 1–3 are audience-agnostic (the same for everyone). **Step 4 is the join** — the one place the content graph meets the learner model. Resolve it at authoring time and you have a static course; resolve it here, per learner, and you have a responsive one.

---

## 6. Invariants (enforce these or it rots)

- **Stable id, forever.** `atom_id` is opaque and never reused or edited. It is the join key for the entire system; if it drifts, everything downstream (translations, mastery, provenance) orphans. (This is the exact failure we reverse-engineered in the JP harvest.)
- **`content_hash` guards meaning.** When `source_text` changes, the hash changes → downstream renderings (translations especially) are flagged stale for re-validation. When only structure moves, the hash is unchanged → renderings stay valid. This is how you re-import a re-exported course without re-translating everything.
- **Single-writer per binding.** No agent writes another's binding. The `atom_id` is the only shared contract.
- **Reference, never embed** — except the one canonical `meaning`. Everything else is a key.
- **No PII in the atom.** Learner data lives in a separately-governed store. The content atom stays clean, which is what keeps the content side easy on Legal.

---

## 7. Where this sits

This atom is the node in the **object graph** (system map → the hub → the content graph). Its four bindings are the wires to the **object / intent / expression** sub-models and to the **learner model** via the audience hooks. The localization agent (AST009, proven) is simply the writer of the locale packs in §4, keyed by these `atom_id`s. Everything you've drawn this session terminates here — this is the row of JSON an engineer types first, and the rest of the tower stands on it.

**Suggested first build step:** stand up the `atom_id` + `meaning` + `object` binding (the spine) and the locale-pack store — that alone reproduces, cleanly, what AST009 does today, and gives you the join key that ends the reconstruction tax for good. Intent, expression registries, and the audience/adaptivity binding accrete after, as their agents come online.
