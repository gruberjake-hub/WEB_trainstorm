# Orchestrator – L&D Track

This repository contains the L&D-facing assets for the Orchestrator Program:
- Decision-maker briefs and whitepapers
- Pitch decks and sales collateral
- Narrative arcs and beats tailored for L&D audiences
- The Orchestrator AI Coach context layer (v0.1)
- Implementation and measurement frameworks

The core design assumption:
> Every learner-facing artifact should also function as structured context
> for a future AI Coach that co-evolves with the learner.

Folders:
- `docs/` – reference docs, briefs, whitepapers, concept vaults
- `deck/` – outlines and slide decks
- `sales/` – outbound email templates, call scripts, one-pagers
- `narrative/` – arcs, beats, and temperature-scaled messaging
- `coach/` – API skeletons, persona definitions, coach prompt blocks
- `ops/` – implementation and metrics frameworks

orchestrator-ld/
├─ README.md
├─ docs/
│  ├─ briefs/
│  │  └─ LD_Decision_Maker_Brief.md
│  ├─ whitepaper/
│  │  └─ Orchestrator_LD_Whitepaper.md
│  ├─ coach-context/
│  │  └─ Orchestrator_Coach_Context_Layer_v0.1.md
│  ├─ concept-vault/
│  │  └─ Orchestrator_Concept_Vault_v1.0.md
│  └─ meta/
│     └─ Design_Principles_For_AI_Native_ID.md
├─ deck/
│  ├─ outline/
│  │  └─ Orchestrator_LD_Pitch_Deck_Outline.md
│  └─ slides/
│     └─ Orchestrator_LD_Pitch_Deck_v1.pptx   (or .key / .pdf)
├─ sales/
│  ├─ email/
│  │  └─ LD_Prospect_Email_Template.md
│  ├─ call-scripts/
│  │  └─ LD_Discovery_Call_Script.md
│  └─ one-pagers/
│     └─ Orchestrator_LD_OnePager.pdf
├─ narrative/
│  ├─ arcs/
│  │  └─ LD_Specific_Narrative_Arc.md
│  ├─ beats/
│  │  └─ LD_Audience_Beats_Menu.md
│  └─ temperatures/
│     └─ Temperature_Spectrum_Guide_for_LD.md
├─ coach/
│  ├─ api/
│  │  └─ Coach_Wrapper_APISkeleton.md
│  ├─ personas/
│  │  └─ LD_Persona_Profiles.md
│  └─ prompts/
│     └─ Coach_Prompt_Blocks_For_LD_Use.md
└─ ops/
   ├─ packaging/
   │  └─ Orchestrator_LD_Implementation_Plan.md
   └─ metrics/
      └─ Orchestrator_LD_Measurement_Framework.md