# DAILY LOG --- TRAINSTORM CGEN

## METADATA

-   Date: 2026-03-29
-   Session Focus: Experience Treatment Layer
-   Primary Goal: Move from structure → staged experience

## WHERE I STARTED

-   System works but feels flat
-   No staging, pacing, or hierarchy
-   Question: where does experience live?

## WHAT I WORKED ON

### Planner Layer

-   Added sceneTreatment + unitTreatment
-   Introduced sceneSignals → classification pipeline

### Schema

-   Renamed treatment → rhetoricalTreatment
-   Separated rhetorical vs experiential layers

### Knowledge Layer

-   Created treatment-registry.md
-   Established canonical vocabulary

## WHAT WORKS NOW

-   Planner encodes experience intent
-   render-plan is readable as reasoning
-   Clear separation of roles

## WHAT FEELS OFF

-   Some scenes over-default to didactic-flow
-   unitTreatment slightly coarse
-   contrast detection weak

## DIAGNOSIS

Planner sees experience but not precisely enough yet.

## KEY INSIGHT

Experience must be encoded before runtime.

## CURRENT SYSTEM STATE

Planner encodes rhetorical + experiential intent but runtime does not
express it.

## CURRENT GAP

Need to validate and tune planner classifications.

## NEXT STEP

1.  Review render-plan.json
2.  Tune classification logic
3.  Then map to runtime lightly

## NOTE TO FUTURE SELF

Do not jump to visuals. Fix planner first.

## SUMMARY

-   Added experience layer
-   Improved interpretability
-   Next: refine + express
