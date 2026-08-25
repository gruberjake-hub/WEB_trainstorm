# Conversation Insight Reconciliation

ChatGPT conversations are discovery evidence, not architectural authority. The canonical state is
the checked-out `trainstorm-core` repository. A remembered idea, chat summary, or exported message
changes the architecture only after it is reconciled against the repository and accepted in
`architecture/DECISIONS.md`. If a chat disagrees with that file, **the file wins.**

## Why this process exists

ChatGPT memory is useful for continuity but is not a complete, inspectable graph of prior sessions.
It can surface relevant details without preserving every detail or exposing a definitive list of
project memories. Therefore, memory can suggest where to look, but only conversation text can serve
as evidence for what a prior session actually proposed.

## Evidence ladder

Use the strongest available source and preserve its provenance:

1. **Canonical repo artifact** - current behavior and architecture; authoritative.
2. **Accepted `architecture/DECISIONS.md` entry** - rationale for a settled repo decision.
3. **Full conversation text** - evidence of a proposal, constraint, or unresolved question.
4. **Contemporaneous chat summary** - useful lead, but verify against the full chat when possible.
5. **Cross-chat memory or recollection** - discovery hint only; never merge directly.

Later timestamps do not automatically outrank earlier ones. The repo outranks every conversation,
and explicit user decisions outrank model-generated proposals.

## Capture workflow

### 1. Acquire

Prefer a ChatGPT data export containing `conversations.json`. Individual copied conversations also
work, but are less complete. Keep raw material under `.chat-capture/raw/`; that directory is ignored
because conversations may contain client information, personal data, or unrelated material.

### 2. Inventory

Run `tools/chat-capture/extract_chatgpt.py` to produce a filtered inventory. Begin broadly with terms
such as `CGEN`, `Trainstorm`, `course generation`, `manifold`, `schema`, and known agent names. Do not
assume titles alone are sufficient; the utility searches message text too.

### 3. Extract claims

For each relevant conversation, capture atomic claims rather than whole-chat summaries. Each claim
must retain:

- conversation ID and title;
- conversation and message timestamps when available;
- message ID and author role;
- a short source excerpt or faithful paraphrase;
- the repo artifact or architectural surface it may affect;
- confidence and unresolved ambiguity.

Separate user intent from assistant invention. An assistant suggestion is not a user decision merely
because it went unchallenged in the conversation.

### 4. Reconcile

Classify every claim into exactly one disposition:

- `already_present` - faithfully represented in the repo;
- `compatible_candidate` - additive and consistent, but not yet accepted;
- `conflict` - contradicts a current invariant, contract, or decision;
- `superseded` - a later accepted decision replaced it;
- `open_question` - important but insufficiently decided;
- `out_of_scope` - belongs to a client course, frontier system, or another repository.

For `already_present` and `superseded`, cite the proving repo path. For a conflict, name the exact
invariant or contract. Never resolve ambiguity by silently averaging two designs together.

### 5. Promote

Promotion is a separate, human-reviewed act:

1. Confirm the intended decision with Jake when the conversation does not contain an explicit choice.
2. Update the smallest canonical artifact that owns the behavior.
3. Validate affected schemas, examples, vocabularies, and tools.
4. Add a dated `architecture/DECISIONS.md` block with the conversation provenance and changed repo paths.
5. Keep the raw export and working candidate ledger outside git unless a sanitized evidence artifact
   is deliberately approved for the repository.

## Working artifacts

The default local layout is:

```text
.chat-capture/
  raw/                 # downloaded export or copied chat text
  inventory.jsonl      # filtered conversation/message index
  candidates.jsonl     # atomic claims awaiting reconciliation
  reports/             # generated summaries and crosswalks
```

These are working materials, not a second source of truth. The durable outputs are changes to the
canonical architecture plus their `architecture/DECISIONS.md` entries.

## First-pass review order

Review by architectural surface rather than by conversation date:

1. core invariants and the atom/element manifold;
2. course-generation stages and script primitives;
3. facet ownership and agent boundaries;
4. layout, rendering, and Storyline realization;
5. localization, audience, and objective ontology;
6. frontier systems and explicitly deferred ideas.

This makes duplicate proposals and cross-session drift visible before anything is promoted.
