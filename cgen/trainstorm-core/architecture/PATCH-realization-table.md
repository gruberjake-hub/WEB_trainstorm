# PATCH — realization table (§4 of script-generation-layer.md)

*2026-07-31. Refines the *starter* realization table so its Layout / interaction column references
**registered** `layout_primitive` / `interaction_primitive` keys (from the now-seeded
`vocab/primitives.registry.json`) instead of the placeholder names (`TitleCard`, `PillarGrid`,
`ClickToReveal`, …). Decision: layout-engine ids are canonical, so the keys below are the real
registry keys. This is the realizer's contract expressed against the same six layouts the
layout-engine `astellas.awareness` sidecar selects from — the two are now one mapping at two
altitudes (architecture doc ↔ brand-specific sidecar data).*

Replace the table in §4 with:

| Script primitive | Realizes into (elements) | layout_primitive | interaction_primitive | delivery |
|---|---|---|---|---|
| orientation | `Head` (orient) [+ `SubHead`] | `TITLE_BODY` | — | didactic |
| context_frame | `Statement` (problem) + `Impact` (risk) | `TITLE_BODY` | — | didactic |
| definition | `Head` (term) + `Statement` (meaning) | `TITLE_BODY` | — | didactic |
| decomposition (static) | `ListHead` + `List` + `ListItem`×3 | `STATIC_CARDS_3` | — | didactic |
| decomposition (explorable) | `ListHead` + `List` + `ListItem`×2–4 | `REVEAL_GRID` | `click_reveal` | interactive |
| distinction (diagrammatic) | two+ `Statement`s + callouts | `DIAGRAM_VENN` | — | didactic |
| distinction (prose) | two `Statement`s (or `Impact`) | `TITLE_BODY` | — | didactic |
| process_flow | `List` + `ListItem`×n | `TITLE_BODY` *(gap — see below)* | — | didactic |
| role_relevance | `Statement` / `Impact` | `TITLE_BODY` | — | didactic |
| knowledge_check | interaction node + option elements | `KC_SINGLE` | `mcq_single` | interactive |
| boundary_statement | `Statement` (callout style via `style_ref`) | `TITLE_BODY` | — | didactic |
| resource_pointer | `Statement` (system-callout style) | `TITLE_BODY` | — | didactic |
| closure | `Head` + `List` (recap) + `Impact` (CTA) | `TITLE_BODY` | — | didactic |

## Gaps the six-layout basis surfaces (add to the .potx + registry when a course needs them)

The reconciliation makes three real gaps explicit rather than hiding them behind placeholder names:

1. **No dedicated `process_flow` / timeline layout.** Routes to `TITLE_BODY` today. Add an
   `AST_ProcessFlow` layout → register `PROCESS_FLOW`.
2. **`SCENARIO_SORT` / `scenario_select` has no owning script primitive.** It's reachable in the
   sidecar only via `requested_interaction`, not from one of the 11 governed primitives. Either add
   a `scenario` / `application` primitive to `script.primitives.v1.json` (governed, version bump), or
   treat scenario_select as a realization *variant* of `knowledge_check` / `distinction`. Worth a
   decision — right now it's an interaction with no upstream knowledge-move.
3. **Callout / versus / center-emphasis** are handled as `TITLE_BODY` + `style_ref` today, which is
   consistent with "callout is a role, not a type," but if any deserves a distinct geometry, add the
   layout and register the key.
