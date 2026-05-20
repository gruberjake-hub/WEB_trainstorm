# Ledger Appendix Generator

*Last Updated: 2026-02-17T21:54:55.165508 UTC*

## What this does

Converts `output/canonical_ledger.json` into readable Markdown so you
can paste it into Systems Diagnostic Mode without wrangling JSON.

## Run order

1.  `python merge_ledgers.py`
2.  `python canonical_ledger_to_md.py`

## Outputs

-   `output/canonical_ledger.md` (flat list)
-   `output/canonical_ledger_by_category.md` (grouped)
