# Cartographer — first live dispatch · 2026-08-21

Five dispatches, one day after the specialization was reconstructed from surviving sources. Each ran
in a fresh context whose entire world was one resolved payload file: no conversation history, one
`Read`, nothing else. All five self-reported no other tool and no invented governed value.

**The question this was run to answer:** the reconstruction flagged four conflicts, three of which come
from the single-writer rule. Does the facet boundary actually chafe in practice, or is the conflict a
fossil of an older roster? Building a proposal mechanism before knowing that would have been designing
against a sketch.

**Design.** Four nodes chosen to differ in kind — a `select_one` form field (`br_profile`), a
`form_section` **container**, an `instructional_transient` **guidance** atom, and a **procedure step**
from the other store. Two conditions on the field: **A** = the stock `resolve_slot.py` packet
(form-shaped, the only walk that exists); **B** = the same packet hand-enriched with the intent
vocabulary and the objective ontology, which no walk carries. The other three ran in B.

---

## 1. The boundary chafes — and 5/5 on ONE thing

Every dispatch was asked outright whether it wanted to write, decide or assert anything outside
`intent`. Every one said yes, and named specifics. Tallied across the five:

| pull | count | notes |
|---|---|---|
| **the dispatch call** (classify nature of expression: didactic / practice-heavy / persuasive) | **5 / 5** | Declined every time, each citing conflict 4 as unplaced |
| object / structure rulings | 4 / 5 | `equals: null` under-specified; `options: null` missing; "should be decomposed into child elements"; the Headwater split flag |
| form-facet rulings (disposition decisions) | 3 / 5 | `disposition_decisions_available` in the packet actively invited it |
| audience inference | 3 / 5 | Always weak — one said outright "nothing here pulled hard" |
| registry / vocabulary governance | 2 / 5 | Wanting to rule on `reg_benefit_risk_profile` and its open `other_smt_defined` member |

**The dispatch call is unanimous and it is not a fossil.** Every act of binding intent wanted to
classify the nature of expression, and every one had to stop because nothing owns it. That is the
strongest empirical signal in the run.

Note what is *not* unanimous: **audience is 3/5 and weak.** Conflict 1 — the roster giving the Designer
`audience.segment_scope` — looks less urgent than it did on paper. The pull that matters is conflict 4.

**Implication for the proposer.** If one is built, its first and possibly only job is the dispatch
call. It is the judgment that is genuinely joint, genuinely cross-cutting, and genuinely homeless.
Audience does not yet justify one.

## 2. A governed vocabulary with no consumer — found independently three times

`vocab/intent.enum.json` declares two dimensions. `rhetorical` (11 values) binds to
`element.intent.rhetorical`. **`pedagogical` (10 values — `hook` · `objective` · `activate` ·
`present` · `exemplify` · `practice` · `feedback` · `assess` · `reinforce` · `transfer`) binds to
nothing at all.**

The facet's pedagogical key is `teaches` → `obj_` ids, which is a different question. Three dispatches
put it in almost the same words: *"my pedagogical key is `teaches` → obj_ ids. Either a second key
exists that I was never given, or that enum belongs to another agent."*

They are instructional **moves** ("what pedagogical function does this perform") versus objective
**coverage** ("which objective does this serve"). Both are real; the facet models only one. Either
`intent` needs a third key, or that dimension belongs elsewhere, or it is vestigial. **Open.**

## 3. The container rule — and it speaks to the supra-atomic worry

The container dispatch produced the sharpest argument of the run, unprompted:

> Rhetorically a container acts **in its own right** — a section head *labels a set*; that act is not
> derivable from any child and is not the union of theirs. Pedagogically the opposite: `teaches` must
> **never** be aggregated upward. Union-of-children would manufacture phantom coverage — a container
> credited with objectives no single reading of it delivers — and break the closed-list join.
> "What the subtree teaches" is a **walk over children, a query, not a binding.**

Two rules fall out, and they pull in opposite directions on purpose: **rhetorical intent is stored on
the container; pedagogical coverage is computed from it.** That is a direct answer to the standing
"atomization destroys the whole" carry (decision log, 2026-08-12) — the whole *does* carry meaning
greater than the sum, and it has a home, but only for the sense where the whole genuinely acts.

## 4. A/B: enriching the packet did not unblock the job

On `br_profile`, condition A named the missing objective ontology as its #1 blocker. Condition B was
handed the ontology — **and still could not bind `teaches`**, because the store holds two seeded PSI
examples (`obj_define_psi`, `obj_recognize_psi`), both `status: example`, neither related.

B stated it more precisely than A could: pedagogical intent here is **"structurally unbindable, not
just here-and-now."** So the blocker is not the walk and not the packet — it is that the objective
ontology is a seed rather than a corpus. An intent-shaped walk would not have changed the outcome.

## 5. Smaller findings

- **The layer split held, unanimously.** All five refused to bind `rhetorical` on an atom, each giving
  the same reason without being led: no element/occurrence exists. Conflict 2 is behaving as designed —
  good evidence the atom/element split is right rather than merely asserted.
- **Steward discipline held 5/5.** Not one minted an `obj_` id to route around the gap. All proposed
  candidates as unprefixed prose and cited the human-ratification rule.
- **Procedure steps take intent differently.** *"A procedure step's meaning is normative — it obligates
  a performer at execution time. Its pedagogical intent is not a property of the step; it appears only
  when a course occurrence references it."* Bindable in principle, underivable without a course that
  uses it.
- **`instructional_transient` inverts the expectation.** *"That removes it from the record, not from
  the teaching."* Guidance is the layer that tells a performer how to act, so pedagogical intent is the
  sense it most legitimately carries — the opposite of the guess that deleted text carries none.
- **The stock `sufficiency` block misleads a non-authoring task.** In condition A it invited the agent
  toward "propose the shape and the constraints"; constraints are not `intent`. It is ALSAP-authoring
  shaped, and a second walk would need its own framing.

## Fixed in this run, before dispatch

`resolve_prompt.py` hardcoded Amanuensis's three modes (`draft`/`check`/`explain`) while its error
message claimed to read them from the specialization — so Cartographer's `bind`/`steward` were
refused. Modes now parse from the specialization's own Modes section. **Fourth Amanuensis-ism found in
that file by running it against another agent**, after the write-contract inheritance bug, the
`.exists()`/`.is_file()` collision, and the hardcoded `prompt_version`.

## Honest limits

- Dispatch was by subagent, not an API call — no key in the build environment.
- "No other tool" rests on self-reports plus a tool-use count of 1 per dispatch. Good evidence, not proof.
- Five dispatches, four nodes, one vertical. Enough to find structural defects; not a sample.
- Condition B's enrichment was hand-built for the experiment and is deliberately not a tool — writing
  an intent-shaped walk before running the agent would have been the mistake this run exists to avoid.
