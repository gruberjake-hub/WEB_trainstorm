# `_studio/` — the room's prompts

*Canonical home of the three generating prompts (studio-and-ledger, 2026-09-02). Not a seat.
Like `_shared/`, the leading underscore means "no `modes.json`, no system-prompt subtree, no
writer here." These files are run **verbatim, hot, in a fresh chat** and are never rewritten
into spine voice. A seat that wants one of them references it by path; it does not fold it in.*

## The three stopping points

| # | prompt | produces (saved whole) | harvested into | gate / promoter |
|---|---|---|---|---|
| 1 | `01_context_digest.md` | `<project>/dossier/context_digest.md` | `doss_*.json` → `context_digest` (verbatim excerpts, `document` ref) | `tools/validate_dossier.py` |
| 2 | `02_exploration.md` | `<project>/dossier/exploration.md` | `doss_*.json` → `argument` ref + `warrant` rationales, `roi`, `modality_recommendations`, `design_insights`, `outcomes` | `tools/validate_dossier.py` · `tools/dossier_accept.py --by` |
| 3 | `03_design_commitment.md` | the production script, saved whole | `schemas/committed-design.schema.json` (`cd_`) → Headwater | `tools/validate_committed_design.py` · `committed_design_accept.py` |

Input to each is the **document** from the stopping point before it — never the JSON. The JSON
is the index; the document is the meaning.

## Rules (from `architecture/studio-and-ledger.md`)

1. **The room writes nothing.** Running a prompt is not a facet write.
2. **Generating prompt ≠ harvest.** A harvester extracts verbatim; it never shortens or
   rewrites. The dossier gate checks substring identity against the saved document.
3. **Verdicts are never harvested.** The three warrant verdicts (pass / partial / fail) are a
   human's choice, recorded in `argument.verdicts_by`; the gate refuses an agent-shaped handle.
4. **Status is `proposed` until a human promotes.** Unchanged law.

## Naming

Numbers encode the order of the stopping points and nothing else. A file that is not a stage
of the room (a per-client inputs overlay, a worked example, a retired version) belongs beside
its prompt in a folder named for it — never as `04_`.

## Known carry

`02_exploration.md` names a client in its inputs list ("current Scope of Work document with
client Brunswick"). Kept verbatim (rule 2). The fix is a per-engagement inputs overlay, by its
own block — not an edit to the core prompt.

## Worked instance

`cgen/brunswick/projects/paytrans/dossier/` — the first pass through stopping points 1 and 2:
`context_digest.md`, `exploration.md`, `doss_paytrans.json`.
