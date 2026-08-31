# beats_v1 — the beat model (arc pass, 2026-08-31)

A **beat** is a content-free rhetorical/pedagogical move keyed by PLACEMENT, not by atom: the
species the voice hop-two finding surfaced (the artisan control's "a solid, positive place to
be" — evaluative warmth NO atom carries, correctly withheld by the invent-guard, homeless until
now). Scene-record `heading`/`kicker` fields were this species in embryo — designer-authored,
learner-facing, atom-free — grown a governed home instead of more ungated fields.

## The model

- **Store:** `occurrences/beats.json` per project — authored project data beside `scenes.json`
  (`schemas/beats.catalog.schema.json`). Dramaturge proposes (`status:"proposed"`); the designer
  ratifies by flipping to `accepted` in the file; merge makes it durable.
- **Placement:** `lesson_start` | `lesson_end` | `scene_start`/`scene_end` (+`scene_id`) |
  `after_element` (+`element_id`).
- **Intent:** governed, from `intent.enum.json` — a beat is EXPRESSED intent, which is why it
  needs no meaning. Welcome = pedagogical `hook`; closure = pedagogical `transfer`; gloss =
  rhetorical `persuade`; interlude = rhetorical `transition`. No new types, ever — a beat kind
  is an intent, not a taxonomy.
- **beat_hash:** `sha256:` over the canonical JSON of `{beat_id, placement, intent}` (sorted
  keys, compact separators). This is the beat's staleness anchor.

## The copy flow (hop two of the arc — mirrors the voice arc exactly)

Words are NOT Dramaturge's. For each ACCEPTED beat: Dragoman voice mode proposes copy into the
register pack's `beats` section (proposals first, `voice/proposals/`), pinned to `beat_hash` as
its `source_hash`; the **INVERSE guard** gates it — claim-free proven: NO figures at all, no
names beyond the governed course allowlist (client/theme name + lesson-title words) — because a
sentence that claims nothing can't lie; `voice_accept` stays the pack's only writer. Twin stakes
sentence: *let words with no meaning anchor exist, while proving they carry none.*

## The renderer (hop three of the arc)

Realize injects accepted-beat copy at its placement — and ONLY beats whose copy is accepted and
fresh render at all; a beat without accepted copy renders nothing (a placed beat is a plan, not
a promise). Projects with no beat catalog stay byte-identical, same fallback discipline as the
voice overlay.
