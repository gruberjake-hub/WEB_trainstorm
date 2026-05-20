# Astellas — Local Language Voiceover Initiative
**Created:** March 2026  
**Status:** Concept — skunk works evaluation phase pending  
**Thread:** Separate from Brunswick. Pick up in dedicated session.

---

## The Problem Being Solved

Astellas has abandoned voiceover production entirely due to:
- High cost of per-language voice talent
- Studio scheduling friction
- MLR/legal review required per language variant
- Version fragility — any content update requires full re-production
- Localization complexity at scale across multiple markets

The result is text-only e-learning across the board. Not because VO isn't wanted — because the production model was unsustainable.

---

## The Proposed Solution

A local TTS pipeline that renders narrated content in multiple languages using cloned or synthetic voices, with zero data egress. Content never leaves the firewall.

```
Source script → translate → render in target language → localized audio file
```

Every language variant becomes a pipeline parameter, not a production engagement. Content updates trigger a re-render, not a re-hire.

---

## Why Local Inference Is Non-Negotiable for Astellas

- Pre-approval and investigational drug content cannot go to third-party APIs
- Japanese parent company has heightened data sovereignty expectations
- MLR implications of sending script content to cloud vendors
- Local = no vendor data agreements, no retention policy exposure, no legal review of TTS provider

**This is not a preference — it is likely a requirement.**

---

## The Japanese Problem

Astellas is a Japanese company. Japanese is the highest-stakes language in the portfolio and the hardest for Western TTS models to handle well.

**Specific challenges:**
- **Pitch accent** — mora-level pitch patterns that distinguish meaning. Getting this wrong changes what words mean, not just how they sound.
- **Prosody rhythm** — Japanese is mora-timed, not stress-timed. English-trained models impose the wrong cadence.
- **Honorific register (keigo)** — business Japanese has specific speech patterns. A voice natural in casual Japanese sounds wrong in professional training content.
- **Native speaker tolerance** — Japanese colleagues will hear every artifact. "Good enough for a demo" is not good enough if the demo room has native speakers.

---

## Candidate Models for Evaluation

| Model | Notes |
|-------|-------|
| Kokoro | Multi-language support, local, already in stack. Japanese quality untested. |
| Style-Bert-VITS2 | Japanese-first TTS, significantly better Japanese prosody than Western models. Local, open source. Primary candidate for Japanese. |
| RVC (local) | Voice conversion pipeline. Relevant if cloning a specific Astellas voice locally. |
| ElevenLabs | Best-in-class cloning quality but cloud-based. Not viable for sensitive Astellas content. |

---

## Skunk Works Evaluation Plan

**Format:** Small internal session — not a pitch, not a commitment. An experiment.

**You bring:**
- Short piece of existing Astellas content (something colleagues know well)
- 2-3 renders per language: Kokoro vs Style-Bert-VITS2 vs one other
- Cloned voice attempt alongside synthetic voice for comparison
- Local inference story as framing context

**Colleagues bring:**
- Native Japanese ears
- Honest feedback unconstrained by vendor politeness
- Institutional knowledge of what "good enough for our learners" means
- Potential co-inventor dynamic if they shape the evaluation criteria

**What the session answers:**
- Does any local model clear the Japanese quality bar?
- Which artifacts are dealbreakers vs acceptable?
- Does the no-data-egress story resonate as a value driver?
- Is this a real opportunity or a concept that doesn't survive native speaker scrutiny?

---

## Pre-Session Build Tasks

- [ ] Install and test Style-Bert-VITS2 locally
- [ ] Run Kokoro on Japanese test script — baseline quality check
- [ ] Source or generate a short Japanese training script (existing Astellas content preferred)
- [ ] Identify 1-2 native Japanese speaking colleagues willing to evaluate
- [ ] Test RVC locally for voice cloning viability
- [ ] Fix MP3 output in tts_module.py (ffmpeg PATH issue) before session

---

## The Pitch Architecture (When Ready)

**What they gave up:** Narrated content — more engaging, better retention, more human.  
**Why they gave it up:** Cost, speed, localization complexity, version fragility.  
**What you're bringing back:** All of that — with none of the reasons they stopped.

- No voice talent contracts
- No studio scheduling
- No per-language production cycle
- No MLR re-review when a word changes
- No data leaving the firewall
- Re-render on demand, any language, same voice

**This is not a feature pitch. It is the return of a capability they already wanted.**

---

## Strategic Notes

- Brunswick is the proving ground. Get the English pipeline clean first.
- Do not bring this to Astellas until a native speaker has cleared the Japanese quality bar.
- Coming in with a working demo beats a slide deck every time.
- If colleagues co-evaluate, they become co-inventors — internal advocacy follows naturally.
- Style-Bert-VITS2 is the primary Japanese research thread. Start there.

---

## Related Files
- `tts_notes.md` — TTS module build notes and wiring roadmap
- `cgen/scripts/tts_module.py` — current TTS module (Kokoro, English)
