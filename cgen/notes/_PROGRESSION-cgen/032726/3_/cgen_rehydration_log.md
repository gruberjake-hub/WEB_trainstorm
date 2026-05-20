# REHYDRATION --- CGEN Experience Layer Checkpoint

## CONTEXT

You are working on CGEN, a deterministic learning experience compiler.

Pipeline: semantic → planner → render-plan → runtime

## CURRENT STATE

-   Planner assigns:
    -   rhetoricalTreatment
    -   sceneTreatment
    -   unitTreatment
-   Registry exists in /knowledge

System understands: - what content is - how it is framed - how it should
land

But runtime does NOT yet express this.

## PROBLEM

Output feels flat because experience is not yet enacted.

## ARCHITECTURAL SHIFT

System must evolve from: content generator → experience director

## KEY PRINCIPLE

Do NOT move to runtime yet.

Validate planner first.

## WHAT TO DO NEXT

1.  Inspect render-plan.json
2.  Evaluate sceneTreatment correctness
3.  Evaluate unitTreatment correctness
4.  Refine classification logic

## SUCCESS CONDITION

Planner classifications feel obviously correct to a human reader.

## THEN

Map 1--2 treatments to light runtime behavior.

## REMINDER

Experience = planning layer, not rendering layer.
