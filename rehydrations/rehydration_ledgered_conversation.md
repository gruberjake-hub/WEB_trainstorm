# Rehydration Handoff — Dual-Channel "Ledgered" LLM Conversation

## What this is
A self-contained handoff to carry one conversational thread into a fresh (general-profile) Claude session. The thread is **not** about the project it originated in — it's a conceptual discussion of LLM failure modes plus a concrete architecture for a "ledgered" high-temperature conversation. Goal in the next session: continue the design discussion and/or build a working prototype.

**Provenance note:** this thread started inside a domain-specific (tax-prep) project but has been deliberately scrubbed of all personal/domain data — none should travel with it. The only residue of the origin worth keeping is that the whole line of thinking began from a real-world *ambiguous bureaucratic instruction*.

## Interaction register (match this)
- User is highly technical and numerate. No simplification, no hand-holding, no sycophancy.
- Peer-level, dry, honest. Push back when warranted; concede the half that's right and hold the half that isn't.
- Be precise about ML internals and hedge appropriately. **Do not fabricate citations or specific results** — stay at the level of "probing research has found…" unless you can ground specifics.

## The conceptual thread (compressed, in order)
1. **Origin.** A badly-drafted instruction line was *resolvable on careful parse* but tripped the reader because a polysemous word was disambiguated only by a buried clause. Lesson: resolvable ≠ well-written. The misread was driven by a **prior** — an active goal biased sense-selection before the disambiguating tokens got a vote (top-down expectation front-running bottom-up parse). The ambiguity was therefore *reader-relative*.
2. **Two failure classes.**
   - *Navigation / control-flow* failures (cross-reference goose chases) fail **loud** — you get lost, you notice. Deterministic, stable, and *compressible*: serialize the traversal once (e.g., a process flow) and amortize it to ~zero marginal cost.
   - *Semantic / leaf* failures (ambiguous wording resolved wrongly) fail **silent** — you confidently encode the wrong meaning and it surfaces much later. Not compressible the same way, because what you'd encode is an *interpretation*, not a fact.
3. **Unifying frame:** *well-formedness is decoupled from correctness.* A garbled output is loud; a fluent, confident, wrong output is silent — no surface signal. Silent failure is what you get when **generation and verification are the same pass.** A compiler separates them (loud, line-numbered errors); ambiguous prose and LLMs fold interpretation and output into one motion. The only fix is a verification layer *outside* the system (human-in-the-loop, tests, grounding).
4. **LLMs are that class, generalized.** They don't even need upstream ambiguity — they can be confidently, fluently wrong about a perfectly clear input, because the failure originates in *generation*.
5. **Statelessness / the "hidden ledger" question.**
   - No durable state across turns except the **token stream** (context window). Weights are frozen; nothing persists between forward passes unless written into tokens. This is *why* chain-of-thought / scratchpads work — externalizing would-be hidden state into the one medium that survives.
   - Within a single forward pass there *are* rich intermediate activations encoding far more than the emitted token ("knows more than it says") — but they're ephemeral, recomputed each pass, discarded, and never *in* the context. The KV cache is just memoized arithmetic over visible tokens, not a secret ledger.
   - The model **cannot read its own activations**; external probes can. That's precisely *why* the failure is silent to the reader: the uncertainty exists in activations but there's no reliable wire from internal doubt → tokens that express doubt.
   - Architecture note: this is a *transformer* property. Recurrent / state-space models do carry a compressed hidden state forward. External memory / RAG is the only practical "ledger" — and it works by writing into the visible context, which proves the rule.

## The design idea
A high-temperature conversation where the model emits **two channels every turn**:
1. **Vernacular channel** — the conversational reply, run *hot* for exploration/creativity.
2. **Ledger channel** — a JSON of things to track / build / revisit, which must **not** be hot or self-authoritative.

This is a deliberate, hand-built externalization of the hidden ledger that doesn't otherwise exist — forcing would-be hidden state into tokens so it persists.

## Three design levers / gotchas
1. **Temperature fights itself.** Hot is right for the prose channel and *poison* for JSON (drifting schema, invented fields, broken syntax). Don't run both at one temperature.
   - **Option A — two calls:** generate prose hot, then a second call at temp ~0 that takes the conversation + prose and emits/updates the JSON.
   - **Option B — one call, structured output:** route the JSON through a tool / structured-output schema so constrained decoding guarantees valid syntax even while sampling hot. *Caveat:* the constraint fixes **form**, not **judgment** — heat can still make it track the wrong things; it just won't hand you broken JSON.
2. **Who owns the ledger is the real hazard.** If the model re-derives and re-emits the whole structure each hot turn, it will silently mutate prior entries (drop, reword, renumber) — the silent-failure mode turned inward on its own bookkeeping. At high temp that's a guarantee, not a risk.
   - **Robust pattern:** the *application* is source of truth. The model proposes **deltas** only; deterministic code applies + stores the canonical JSON; you re-inject the relevant slice next turn. Generation proposes; a separate deterministic pass commits. Never let the hot channel be authority on its own state.
3. **Uncertainty field — partial cure, with a catch.** Add a per-entry `confidence` / `assumptions` / `needs_verification`. This forces doubt into tokens, a partial fix for the silence problem. *Catch:* a self-reported confidence is still a *generated* token, not a probe readout — the model's narrative about its certainty, which can be as miscalibrated as anything else. Useful, but don't mistake a written `0.6` for the internal one.

## Starter schema sketch (template, not prescriptive)
```json
{
  "established_facts": [],
  "open_questions": [],
  "build_targets": [],
  "decisions": [],
  "entities": {},
  "assumptions": [
    { "claim": "", "confidence": 0.0, "needs_verification": false }
  ],
  "threads_to_revisit": []
}
```
Fix the top-level keys up front so the consuming app can program against them; don't let the model invent keys.

## Open questions / next steps
- **Full re-emit vs. delta-only** updates (delta is more efficient but needs deterministic apply outside the model).
- **Ledger growth:** how to summarize/slice when it gets large (re-inject relevant slice vs. whole thing each turn).
- **Drift eval:** a cheap check that prior entries weren't silently mutated turn-over-turn.
- **Offer on the table:** build a working prototype as an artifact using the Anthropic API in-artifact — dual-channel output, fixed schema, app-applied deltas, two-temperature wiring — so you can drive a hot conversation and watch the ledger accrete.
