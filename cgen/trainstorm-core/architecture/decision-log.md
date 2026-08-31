# Decision log — Course Engine / Manifold (narrative record)

*Migrated into the repo 2026-08-25 from the Claude Project doc `claude/decision-log.md`, where it had
lived since 2026-08-10. From this commit forward **this file is the only copy**; the Project copy is a
one-way snapshot from git and is not edited by hand.*

**How this file relates to `architecture/DECISIONS.md`.** `DECISIONS.md` is the short-block canon —
one dated block per settled call, and the file that wins when a chat disagrees. This file is the
**reasoning record** behind those calls: what was tried, what was found, what was retracted and why.
The two are different genres of one history, not two copies. When they disagree, `DECISIONS.md` wins,
and the fix is a new dated block there plus a dated entry here — never a silent edit to either.

*Running log of settled architectural decisions. Newest first. One entry = one decision that is
closed enough to build on; if it reopens, add a new dated entry rather than editing history.*

## 2026-08-31 (arc hop three) — The course greets and closes. Three acceptances join at the choke point; the closure lands after the checks; the arc's first pass is COMPLETE.

*Anchor: branch `drive/arc-renderer` off `41878e6` (Jake's beat-copy acceptance commit; the
beats themselves ratified in `394655e` — both direct-to-main human writes, per the acceptance
precedent). No design forks — this executes the arc-pass plan end to end.*

### What landed

Beat loading joined to the voice overlay at the same choke point (`project_lesson_htmls` — the
voice hop-three lesson, applied not relearned): a beat renders only when catalog-accepted AND
copy-accepted AND `beat_hash`-fresh; stale copy is loud; everything else renders NOTHING — a
placed beat is a plan, not a promise. `_inject_beat_components` is pure and selftested: welcome
opens scene one; the closure appends to the LAST scene — after the lesson-end checks, the
artisan control's shape (you close once the work is done); scene and element placements land
exactly; an unplaceable beat is skipped and reported, never guessed. Manifest stamps
`beats_applied`; beat components carry beat_id/intent/placement in meta. Scope line named: the
engine projection (the played course) renders beats; the dev HTML sidecar does not yet — carry.

### Verified live

Headless Chromium: the course OPENS on "Welcome — this is about your pay: what's changing, how
it's set, and what it means for you." — closure absent until the end — pages through the
warm_direct teaching copy — and LANDS on "You're informed. You know how your pay is set and
what's behind it — and that knowledge is yours to use." after the checks. ast_alsap and
ast_artwork regenerate byte-identical; every gate and selftest green.

### Where this leaves the machine

The artisan side-by-side (hop five of the paytrans drive) named four gaps. Two are now CLOSED
at v1 — voice (rewritten learner copy) and arc frame (welcome/closure) — through five governed
stores, two agent modes, one new seat, and eleven human acceptance acts, with every rendering
provably anchored or provably empty. Remaining: narration (Griot — whose "words before voice"
wake now has accepted words and an authored arc), player expression (+ acceptance front-end
carry), motion (parked). The withheld midpoint gloss is the ready-made demo for flipping
Dramaturge's `withheld_gloss` wake live. One session, 2026-08-31, corpus to a course that
greets, teaches, checks, and closes — in words the machine can prove it was allowed to say.

## 2026-08-31 (arc hop two) — The inverse guard lands and the frame gets its words: welcome and closure proposed, gate-green, refused-until-ratified. Copy cannot outrun its beat.

*Anchor: branch `drive/arc-beat-copy` off `0558f96` (PR #54). No new design forks — this hop
executes the arc-pass design already ratified (hop one block): beat copy through the voice
machinery, inverse-guarded, beats-section acceptance.*

### The inverse guard, mechanically

`inverse_findings` (voice_gate.py): ZERO digits anywhere; capitalized content words pass only if
sentence-initial, exempt, in the project corpus, or in the data-derived ARC ALLOWLIST (lesson
titles + scene headings/kickers + project/client names). Anchor = `beat_hash`, imported from
validate_arc — one definition, three importers, zero copies. The selftest proves red five ways
(figure, invented mid-sentence name, stale hash, missing beat, self-acceptance) and — worth
noting as a first — DEMONSTRATES its own documented limit as a passing check: a sentence-initial
name slips the deterministic net, on purpose, in the record, so nobody mistakes the guard for a
proof. Human acceptance remains the meaning gate.

### Copy cannot outrun its beat

`voice_accept` routes `bt_` ids: refuses while the beat is `proposed` (proven on a project copy
— the refusal message names the fix), refuses stale `beat_hash`, re-guards at acceptance,
supports `--edit`; `validate_voice` gates the pack's `beats` section identically. The subtle
call that makes the workflow humane: `beat_hash` EXCLUDES status — so the copy authored today,
while the beats sit `proposed`, survives Jake's ratification edit untouched; only a placement or
intent change stales it. Sequencing freedom without staleness holes.

### The words (Dragoman voice mode, in-session, warm_direct — both draft, both gate-green)

Welcome (hook): "Welcome — this is about your pay: what's changing, how it's set, and what it
means for you." — flagged invented-risk low ("what's changing" presupposes change; contextually
anchored by scene one's atoms, but the welcome itself claims it). Closure (transfer): "You're
informed. You know how your pay is set and what's behind it — and that knowledge is yours to
use." — flagged invented-risk low (assures the LEARNER, the artisan control's closure stance;
claim-free about content, but an assurance). Both flags are the guard doing its job on the
species it was built for: the residue the deterministic net can't judge, handed to the human
with the reasoning attached.

### What did NOT happen

No beat was accepted (the beats themselves are still `proposed` — Jake's ratification edit
comes first, then copy acceptance). No realize change (arc hop three). All stores regenerate
byte-identical; every selftest and gate green.

## 2026-08-31 (arc hop one) — Dramaturge takes the seat: beats as governed project data, one live wake, welcome + closure proposed for paytrans. The intangibles get their home.

*Anchor: branch `drive/arc-dramaturge` off `569dc18` (PR #53). The design conversation ran in
two sittings: the intangibles exchange after the withheld-reassurance finding (species
distinction — affective claim-free copy vs. actual invention; the INVERSE guard — claim-free is
a checkable property; placement-keyed store; never via Headwater), and the fork resolution
before this build. Jake's calls: a REAL agent seat now, not just a catalog — he wants to tune
wake conditions and watch how beats arrive differently — split as one live wake + declared
placeholders; beat copy inside the register's voice pack; full v1 placement granularity
(lesson + scene + element-adjacent, so the motivating midpoint case has a home).*

### The grounding find that reframed the design

Scene records ALREADY carry authored, learner-facing, atom-free copy — `"heading": "Why you're
seeing pay ranges"` renders on screen and no atom anchors it. The honesty line was crossed in
miniature when scene.v2 landed, governed only by authorship and merge. So the arc pass is not
introducing a foreign species; it is giving the species scene headings already are a first-class
home with governed intent and a gate, instead of letting it grow one ungated field at a time.
(Migrating heading/kicker INTO beats is a candidate later hop — named, not assumed.)

### What landed

`schemas/beats.catalog.schema.json` (beats carry placement + governed intent + status + NO text
— schema-enforced; `beat_hash` anchors future copy) · `agents/dramaturge/` — the seat: README
(spine slots; write contract narrowed to status:"proposed" only), `beats_v1.md` (the model and
the three-hop arc), `wakes.json` — THE PLAY SURFACE: `missing_arc_frame` live with tunable
`min_scenes`; `withheld_gloss` (voice proposals' invented-risk withheld flags → after_element
persuade beats — the finding become a wake condition), `hook_persuade`, `pacing_interlude` all
declared live:false · `tools/dramaturge.py` (runs live wakes; defers to claimed placements —
re-runs never re-litigate designer decisions, proven; validates before writing; --dry-run) ·
`tools/validate_arc.py` (schema + governance + reference resolution; selftest red seven ways,
including copy smuggled onto a beat) · voice.pack.schema `beats` section (bt_* keyed, copy
pins beat_hash).

No vocab bump was needed — welcome/closure/gloss/interlude resolve to hook/transfer/persuade/
transition. The design validating itself: a beat kind is an intent, not a new type.

### First run

`bt_paytrans_welcome` (lesson_start, hook) and `bt_paytrans_closure` (lesson_end, transfer)
proposed for the employee course — the exact frame the January artisan control has and the
pipeline course lacks. Both status "proposed"; Jake ratifies by flipping to "accepted" in
beats.json. Idempotent re-run skips both ("placement already claimed — not re-litigating").
All stores regenerate byte-identical (realize does not read beats yet); every gate green.

### Next

Arc hop two: the INVERSE guard in voice_gate (beat entries: NO figures, no names beyond the
governed course allowlist), Dragoman voice mode proposes copy for accepted beats pinned to
beat_hash, voice_accept extended to the beats section. Arc hop three: realize injects
accepted-and-fresh beat copy at placement; a beat without accepted copy renders nothing. Then
Griot has both words AND arc to narrate.

## 2026-08-31 (voice hop three) — The course SPEAKS: realize's voice overlay, one choke point, loud stale fallback. Checks stay meaning-anchored, and the played lesson proves both sides of that line.

*Anchor: branch `drive/voice-renderer` off `2c96259` (Jake's acceptance commit — the pack itself,
50 entries, `--all --by jake`; acceptance data goes straight to main as the human's own write, no
PR). Before this hop: Jake's acceptance run failed on Windows (cp1252 vs UTF-8 — my missing
`encoding=` in the voice tools; unblocked with `$env:PYTHONUTF8=1`, hardened properly here; the
WIDER toolset still reads locale-default — named carry, one sweep, not silent fixes).*

### The instructive failure

First implementation loaded the overlay in realize's `main()`. Regen looked right — manifest
stamped `applied: 50` — but the projection still spoke verbatim: cartographer and couturier
IMPORT realize and call `project_lesson_htmls` directly, so the last writer in the pipeline had
an empty overlay. The fix is the architectural point: the overlay loads inside
`project_lesson_htmls` itself — one choke point every caller shares. Worth remembering as the
pattern for any future projection-time store: wire it into the shared entry, not the CLI path.

### What landed

`load_voice_overlay` + `voice_text`/`voice_atom_text` in realize; interceptions at the four
learner-facing text accessors (`_engine_atom_text`, `list_item_display`,
`instance_fill_display`, `step_item_html`). Accepted-and-fresh entries apply; element overrides
(chain-hash checked) beat atom entries; STALE accepted entries fall back to verbatim LOUDLY
(console + manifest `voice.stale_fallbacks`) — the brand-fallback lesson applied. Two packs
refuse rather than guess (authored register choice = future, deliberate). Stamps only when a
pack applies: manifest `voice` block, projection `meta.voice_register` — so ast_alsap and
ast_artwork regenerate BYTE-IDENTICAL, proven. Realize selftest +6 voice checks. UTF-8 explicit
in the three voice tools.

### Verified live (the hop-4b bar)

Headless Chromium against a local serve, paged through all five scenes:
`/cgen/?project=brunswick/paytrans` in Brunswick chrome renders "Your base salary pays for the
core expectations of your specific role", "You have the right to ask your employer…", the EU
line with 27/June 2026 intact — and the withheld reassurance ABSENT on-screen, exactly as
accepted. One probe deliberately still verbatim: a lesson-end check choice quotes the atom
("Base salary is paid to perform…") — **checks derive from meaning, not voice**, because
`assert_check_honest` proves choices against atoms. That register seam (warm teaching copy,
verbatim check language) is now VISIBLE in the played course — the concrete exhibit for the
check-voicing decision, to be taken or declined deliberately, not drifted into.

### The arc, after this hop

Voice pack v1 is COMPLETE end-to-end: vocab → schema → writer → guard → acceptance → renderer →
played. Next: the ARC PASS design conversation (intangibles/beats — hop-two log has the sketch:
species distinction, inverse guard, placement-keyed store) BEFORE Griot builds, since narration
hits the same missing-welcome problem. Then Griot, then player expression. Carries: acceptance
front-end (review surface — pairs with player expression); toolkit-wide UTF-8 sweep; check
voicing (above).

## 2026-08-31 (voice hop two) — Dragoman speaks: 50 warm_direct drafts proposed, gate-green, none accepted. The invent-guard is two-speed; the pack's only writer is a human-run script; the withheld reassurance is the finding.

*Anchor: branch `drive/voice-writer` off `c505f5e` (PR #51). Design beat held with Jake before
building; three calls, all his: two-speed invent-guard (deterministic + flags, human acceptance as
the meaning gate) over adding an LLM checker now; in-session execution of the mode (implementation
varies behind the contract — the contract, not the executor, is what's governed); scope = the 50
course-played atoms, not the full 68.*

### What the seat read surfaced

Dragoman's `system.md` was READIER than the handoff suggested: config header (with a free-prose
`register` field the vocab now formalizes), the two-speed principle, the flag discipline, the
draft-only bright line — voice mode is that frame re-instantiated, not new machinery. Tone is not
wired into paytrans (the tone.enum field is proposed, no data) — the mode's contract reads tone
where present and proceeds without. No Brunswick termbase exists; defined names are constrained by
the atoms themselves plus the `defined-name` flag (carry, not blocker).

### What landed

`agents/localize/voice.system.md` (voice-agent.v0.1) — the mode contract; README reframed:
agents/localize is DRAGOMAN, one seat, two mode instantiations, each with its own gate profile.
`tools/localize/voice_gate.py` — the deterministic invent-guard: bright line, anchor freshness,
invariant import (atom → pass; sibling atom → pass WITH NOTE; nowhere → fail), flag/confidence
discipline; selftest proves red seven ways; honest limit stated (catches countable surface forms,
not paraphrased invention). `tools/localize/voice_accept.py` — the accept_value pattern: the
pack's ONLY writer, human-run, re-guards at acceptance time, refuses non-`specified` registers,
`--edit` records accepted-with-edit, schema-validates before writing. Whole loop proven on a
project copy: accept 2 → accept `--all` (50/50) → store gate green; refusal paths demonstrated
(draft register, missing proposal).

### The proposals (the actual copy)

50 drafts in `voice/proposals/warm_direct.json`, all gate-green. Register moves per the spec:
second person re-addressing where the atom grants the learner something; compression that sheds
words, not claims; verbatim-kept declared on labels and pillar names; the high-or-low merit
symmetry KEPT (de-threatening by honesty, not softening). One sibling-atom note (U.S. for the
atom's USA). **The finding of the hop: the withheld reassurance.** The artisan control appends "a
solid, positive place to be" to the midpoint scenario — an evaluative claim NO atom carries. The
mode withheld it and flagged `invented-risk` instead. That is the stakes sentence enforced against
the exact copy that motivated the arc — and it hands the closure/persuade design question its
first concrete case: warm copy the client plausibly wants, with no meaning anchor to hang it on.
Resolution paths when that conversation opens: mint the atom (Headwater), or accept-with-edit
(human authorship, recorded).

### What did NOT happen

No pack entry exists — acceptance is Jake's act, per-id or `--all`, after reading the flags. No
realize change (hop three: "accepted voice if present, else verbatim atom"). No closure/persuade
copy. All stores regenerate byte-identical; every existing gate green.

## 2026-08-31 (voice hop one) — The voice-pack CONTRACT lands: Dragoman voice MODE, two pins, register.v0.1 with the January register reverse-specified. Contract before writer.

*Anchor: branch `drive/voice-pack-contract` off `a9b73eb` (PR #50). The design conversation the
hop-five block called for was held with Jake in full before any file was written; this entry is
the reasoning record behind the DECISIONS block of the same date.*

### The design conversation (what was argued, not just what was decided)

**Mode, not agent — Jake's opening call, tested and kept.** Register-shift and translation share
the deep contract: re-render meaning at a target coordinate, prove the meaning didn't move. The
frame that survived scrutiny: Dragoman owns the meaning-rendering SPACE; language and register are
coordinates. The composition payoff decided it — when locale × register combine (Spanish AND
conversational), ordering becomes one seat's internal concern instead of inter-agent
coordination, which the choreography model forbids. The strain named honestly: the modes differ
in LICENSE (translation ≈ fidelity, near-zero authorial freedom; voice = authorship —
compression, person, rhythm) and their failure modes INVERT (a failing translator garbles; a
failing copywriter invents). Handled by contract, not by a second agent: each mode declares its
own gate profile, and voice's invent-guard is the stricter one.

**"What does localization localize?" dissolved into two pins.** Jake's question, and the split
that answered it: the ATOM anchors meaning always (every rendering gated against `content_hash`,
never transitively — no telephone chains), while the WRITER works from the accepted voice
rendering where one exists (`derived_from`, hash pinned). Localization localizes the expression,
judged against the atom. Jake's articulation, kept as the canonical rationale: three protections
with three scopes — the atom guards what must be TRUE; Dragoman's libraries guard what the client
ALWAYS SAYS; the chained source transmits what the voice writer CHOSE HERE, the one kind of
contextual meaning no library can hold. And register does not translate: specs are abstract
(person/stance/formality), realized natively per locale — conversational Japanese is not
translated conversational English.

**The Chameleon boundary, drawn before it could blur.** Voice mode READS a register spec — a
governed coordinate chosen for the course. It never reasons about who the learners are; the
moment it does, it is writing the audience facet and single-writer has broken. Which segment gets
which register is Chameleon's join, downstream. **Named carry (Jake, this session): Chameleon is
the faster→better pivot.** Correctly a stub today — until the voice pack it had nothing to choose
between; every pack axis built widens its decision space for free, because packs key on exactly
the coordinates it selects on. The decided build order IS the Chameleon-preparation sequence.
Revisit after player expression; do not open its design mid-arc.

**Taxonomy-up-front with an honest counterweight.** Jake chose four registers now over
one-register-minimalism. Mitigation built into the vocab: per-register `status` — only
`warm_direct`, reverse-specified from the January artisan control's actual copy (direct address,
contractions, de-threatening reassurance, rights-affirming persuade beats, heavy compression), is
`specified`; the other three are `draft` and the gate flags any rendering authored against them.

### What the repo read surfaced (two flags, both resolved with Jake)

**`tone.enum.json` already existed** — governed affective tone, per-element, at the intent layer.
Unflagged overlap here would have been vocabulary drift of the exact kind the constitution exists
to prevent. Resolution: TONE MODULATES WITHIN REGISTER — register is the course-level voice
coordinate, constant per rendering; tone varies element to element and the voice writer reads it
as an input. Boundary stated in `register.enum.json` itself. **The hop-five block's parenthetical
said "keyed by element id"** while deferring pack shape to this pass; refined per the 08-25
occurrence-identity precedent to atom_id + element overrides, named as a supersession rather than
letting canon and schema quietly disagree.

### What landed

`vocab/register.enum.json` (register.v0.1) · `schemas/voice.pack.schema.json` (two pins;
propose→accept statuses; element_overrides chain via `derived_from`) · `locales/README.md` gains
the sibling-family note and the optional `derived_from` (backward-compatible; no pack instances
existed to migrate) · `tools/validate_voice.py` — schema, governance, anchor freshness, chain
freshness; selftest proves red EIGHT ways (ungoverned register, accepted-against-draft, missing
reviewer, malformed hash, stale anchor, missing atom, stale chain, embedded-shape entry); project
mode is a contract-only pass until packs exist. All existing gates re-run green; paytrans,
ast_alsap, ast_artwork regenerated byte-identical (no pipeline code touched). What this gate does
NOT check, deliberately: meaning preservation itself — that is voice mode's review gate (the
invent-guard, `prompt_purity.py` as prior art), which is hop two's problem, alongside the
Dragoman voice-mode prompt. Hop three: realize learns "accepted voice if present, else verbatim
atom."

## 2026-08-31 (hop five) — RATIFIED: the paytrans employee course is `brunswick.reference.course` v1 (structural). The July `_todo` is closed by the pipe, not by hand. The artisan side-by-side names four gaps, each with an architectural home; the voice pack is the next build.

*Jake's two calls, made in conversation after playing the branded course live: ratify now as the
STRUCTURAL reference with v2 scope named, and build the voice pack next. Anchor: branch
`drive/reference-course-v1` off `cb2e32d` (PR #49). The reference file is a validated POINTER
record — copying the projection into reference/ would mint the drifting second source this repo
exists to prevent.*

### The side-by-side (pipeline v1 vs. the January artisan control)

Control: `cgen/courses/brunswick_pay_transparency_employee/course.json` — 10 AE-rendered scenes,
10 VO tracks (~977 narration words), rewritten learner-facing on-screen copy, two mid-course
interactions, a `persuade` Impact beat ("You have every right to understand your pay"), a closure
scene ("You're Informed"). Pipeline v1: 5 scenes + 2 checks, verbatim atom text, branded chrome,
no narration, no arc. Jake's read: content is very close; aesthetics and the less tangible pieces
are not there yet. The decomposition of "less tangible":

| gap | what the artisan has | architectural home | status |
|---|---|---|---|
| **Voice** | compressed, warm, learner-facing copy — almost never verbatim source | a RENDERING of meaning, external store keyed by element id — a locale pack shifted in REGISTER, not language; Dragoman machinery generalized. First natural seat for a dispatched LLM writer under propose→accept, with meaning-preservation as the review gate; content_hash staleness covers it for free | **NEXT BUILD** |
| **Narration** | 10 VO mp3s | Griot — seat and wake ("words before voice") defined 08-12, never run; player audio chrome already built | after voice pack |
| **Arc** | welcome, persuade beat, closure, interaction placement | the 08-12 authored-affect carry + the lineage audit's exploratory seat; closure/persuade COPY waits on the voice pack, placement is catalog work | partially catalog-now |
| **Motion/visuals** | AE mp4 per scene, motion primitives | parked (Lottie-first per conventions); meanwhile the HTML player has unused RevealCards/StepList components, and the PayTrans icon set + 255-asset visual registry have never been consumed | expression hop, parallel |

The consolidating finding: **every gap already has a home in the architecture** — nothing the
artisan course does is architecturally homeless. The manifold anticipated its own v2.

### Order decided

Voice pack → Griot (words, then audio) → player expression (components + icons, parallelizable).
Motion/AE and Storyline/.potx stay parked. Ratification does not wait on any of it: the reference's
job is to prove corpus→course under gates, which v1 does; the record names what v2 will claim.

## 2026-08-31 (hop 4b) — Brunswick brand pack conformed to the Course Engine pack contract; the branded player verified in a real browser

*Anchor: branch `drive/brunswick-brand-pack` off `c53b2e6` (PR #48). Verified headless-Chromium
against a local serve of the repo: catalog, projection, all four pack files and the logo fetch 200;
`#app` carries `brand-brunswick`; `--color-accent` resolves `#026AFE`; the lesson pages through to
both checks rendering with sibling distractors under Brunswick chrome.*

Jake's live report after landing hop four: the lesson plays, no Brunswick chrome. Cause: the
January brand folder predates the pack contract the engine's loaders established (astellas pack,
PR #35) — `loadBrand` fetches `<theme>-brand.json` and `loadTheme` links
`<theme>-{tokens,layout,components}.css`; the folder held `brand.json` + `brunswick.css`. The 404
was silent chrome-fallback by design (a course must play unbranded rather than not at all), which
made it invisible until a human looked. Fix at the data layer: the pack now carries the four
contract files. `brunswick-tokens.css` maps the January distillation onto the SAME semantic
variable contract as the astellas tokens; two status colors the guidelines do not define (warning,
danger) are neutral values flagged as non-brand in the file, not invented brand colors.
`brand.json` and `brunswick.css` stay — they are the distillation source, a different genre.

**Named carry (real debt, taken knowingly):** `brunswick-{layout,components}.css` are copies of the
astellas files with brand spots swapped, because the engine has no shared base layer — the astellas
pack IS the de-facto base. Two copies of component CSS will drift exactly the way two copies of a
schema drift. The right shape is an engine base stylesheet + thin per-brand token/override packs;
until that hop, every component/layout edit must land in BOTH packs, and each copied file says so
in its header. Second smaller carry: `loadBrand`'s silent fallback deserves a visible dev-mode
notice — silence cost this drive a round trip.

Hop five remains: Jake's design review of the played lesson, then reference-course ratification and
the artisan side-by-side.

## 2026-08-31 (hop four) — `?project=` refs are client-qualified: `/cgen/?project=brunswick/paytrans`. The astellas prefix was an assumption the second client namespace exposed.

*Anchor: branch `drive/cgen-client-qualified-project` off `7e25d55` (PR #47). One file,
`cgen/src/lessonCatalog.js`. Node tests on the resolver: bare slug → astellas (both existing URLs
byte-identical in behavior), `brunswick/paytrans` → `./brunswick/projects/paytrans/…`, and the
unsafe shapes (`../evil`, `a/b/c`, `brunswick/../x`) all resolve to "" and fail in the stage.*

The hop-three plan assumed `/cgen/?project=paytrans` would play with no work because the loader
"already takes ?project=". Half true: it takes a project, but bakes `./astellas/` into the path —
fine when astellas was the only client, an assumption the moment brunswick existed. Fix is
data-free: a project ref may be `<client>/<slug>`; a bare slug keeps meaning astellas, so
`/cgen` and `?project=ast_artwork` are untouched. Deliberately NOT a client registry and not a
catalog UI — the ref names the store path the same way the store names itself.

Verification after Jake lands this: fetch
`https://trainstorm.ai/cgen/brunswick/projects/paytrans/occurrences/lessons.json` (the catalog) and
play `/cgen/?project=brunswick/paytrans` — Brunswick chrome via `meta.theme`. Then hop five:
Jake's design review of the lesson, ratify the projection as `brunswick.reference.course`, run the
artisan side-by-side. Carry from hop three unchanged: manifest `move_counts` key order is
insertion-dependent across rerun sequences (diff noise, not meaning — sort it in a later tidy).

## 2026-08-31 (hop three) — The employee course EXISTS: five scenes, two checks, played from the graph. Cartographer heuristic v2 (expository kinds + intent_map as project data); scene.v2 adds `topic`; existing stores proven byte-identical.

*Anchor: branch `drive/brunswick-paytrans-course` off `0832c53` (PR #46). Verification at delivery:
paytrans GATE/PROMOTE PASS (68 atoms), elements 70/70 vs element.schema.json, validate_objectives
ALL PASS, realize/cartographer/couturier selftests ALL PASS on default AND both astellas projects,
lint 0 errors, form/instance/socket 17/17·17/17·21/21 — and the decisive one: regenerating
ast_alsap and ast_artwork under the new code produced a 0-line diff (no intent_map file = v1
behavior, byte for byte).*

### What ran

`realize → cartographer → couturier` on the first expository store. 70 occurrences (68 primaries +
2 reinforce extras), spine 52 of 70 across five authored scenes, moves
{hook 1 · objective 1 · present 61 · activate 5 · reinforce 2}, teaches bound on 56, all five
looks dressed, two lesson-end `invert_definition` checks with real sibling contrasts, and
`realized_lesson.json` carrying `meta.theme: brunswick` — the brand pack the repo has held since
January finally has a consumer. The course design itself lives entirely in FOUR project-data files:
`scenes.json` (five scenes, ordered refs), `lessons.json` (authored title — a four-root corpus has
no single document root to name it), `one_to_many_seed.json` (two extras), and the new
`intent_map.json`.

### Heuristic v2 — the two v1 assumptions the corpus broke

**"No belongs_to → hook" assumed one root.** Four document roots here; which one opens the lesson
is course design, not structure. New rule: `kind document → present/low`, and the **intent_map
elects at most one hook** (loader rejects two — a lesson opens once). First election taught its own
lesson: the guide root's title is *manager-facing* copy ("Manager's Guide to…"), wrong as an
employee course opening; the commitment sentence is the honest hook. The heuristic could never have
known that. That is exactly the designer/compiler boundary working.

**`bind_teaches` was ALSAP-hardcoded Python.** The same shape the 08-27 catalog decisions retired
for scenes and lessons, now retired for intent: `occurrences/intent_map.json` carries the
designer's objective bindings (55 entries here, each validated against the ontology and the closed
move vocab on load). Cartographer remains the intent facet's single writer; the map is its governed
input. Confidence subtlety worth keeping: the v1 walk demoted every off-ALSAP atom to `low` purely
for `teaches_unbound`; when the map binds teaches, the classifier's own confidence is restored —
low-confidence dropped 69 → 13, and the 13 that remain are honest (document roots, definitions,
deliberately unbound orientation atoms). Spec: `agents/cartographer/heuristic_v2_expository.md`.

### scene.v2 and the selftest that rotted on schedule

`vocab/scene.enum.json` v2 adds one role, `topic` (authored expository grouping; heading/kicker are
designer copy from the record, like every scene heading). realize's role mirror caught the bump
exactly as built — and its selftest then FAILED because the case asserted the three SOP roles as
the whole list. **Third recurrence of the 08-20 rot** (reg_benefit_risk_profile, then `serves`,
now scene roles): a governed-list bump breaks the test that pinned the list's contents. Repaired to
assert the rule (SOP trio still governed ⊆ SCENE_ROLES; every used role governed), with the
recurrence noted in the test comment itself.

### Checks — what was refused

Only two atoms carry honest copulas ("Base salary is…", "The BPP is…"); both became lesson-end
invert-definition checks retrieving from the performance scene. The colon-form definitions
(Pay Equity / Pay Transparency / Pay Gap Reporting) were **not** seeded: `copula_parts` cannot
invert "X: Y" and a rewritten stem would be invented copy. If those checks are wanted, the honest
path is extending `copula_parts` to colon definitions as its own decided hop — flagged, not done.

### Open / next

Jake reacts to `realized_lesson.html` (nothing is locked — scenes, order, membership, title are all
project data he can redraft in review). Then hop four: `/cgen?project=paytrans` needs only the
landed store — the loader already takes `?project=`, and `meta.theme: brunswick` resolves the
existing brand pack; verify live and score. Hop five: ratify the projection as
`brunswick.reference.course` and run the artisan-control side-by-side. Carries: colon-copula
extension; the `objective` move on `atom_bw_framework_total_rewards_purpose` (heuristic
purpose-frame match on a coverage atom — harmless, flagged here rather than special-cased); the
manager course as drive two.

## 2026-08-31 (objective lock) — RATIFIED: goal_bw_pay_understood and all five obj_bw_emp_* go `validated`. The promotion gate is exercised by live nodes for the first time.

*Jake's ratification, given in conversation after reading the goal, the four not_trainable causes,
and the five objectives as written; this entry and the status flips are the durable record, and his
merge lands them. Anchor: branch `drive/brunswick-objective-lock` off `34b9700` (PR #45). Goals v4,
objectives v5. `validate_objectives` ALL PASS; negative control proven red in the same session — a
validated objective with `serves` stripped fails on two checks (schema conditional + the warrant
walk), then green on restore.*

The meaning of `validated` was put to Jake explicitly before he chose: it asserts the warrant holds
for building, not that Brunswick has signed off — client sign-off is a separate, later event, and
the goal's rationale now says so in the file. He ratified on that reading.

These are the first `validated` nodes the ontology has ever held. Every prior goal and objective is
`example` or `draft` — the 08-21 warrant chain was built and gated against seeds, and the
"conditionally required once status: validated" promotion gate had never had a live node to bite.
It now guards six.

Unlocked: hop three — the course itself. Scenes/lessons/checks as project data for the employee
awareness course, then realize → cartographer → couturier on the paytrans store. Two heuristic
touches are expected and will be taken as their own decisions, not smuggled: Cartographer's move
walk has never seen `statement`/`section`/`document` kinds, and the spine/sequence heuristics walk
procedure shapes that this store does not have.

## 2026-08-31 — Brunswick paytrans hop one: first non-Astellas client namespace, first EXPOSITORY corpus through Headwater (structure.v0.2: document/section/statement), warrant chain drafted from client documents. 68 atoms, all gates green.

*Anchor: branch `drive/brunswick-paytrans-hop1` off `bc53065`. Proposed by Claude as a patch series;
repo state once Jake lands it — and his merge RATIFIES the structure.v0.2 vocab bump and the drafted
warrant chain (see the DECISIONS block). Verification at delivery: `validate_atoms --project
../brunswick/projects/paytrans` GATE PASS / PROMOTE PASS (68 atoms, 0 hard, 0 soft);
`validate_objectives` ALL PASS with the new nodes; every pre-existing gate re-run green.*

### What this drive is

The full-course arc, decided with Jake this session: take the messy Brunswick pay-transparency
corpus (the real BPS engagement corpus, Jan 2025–Jan 2026, from the folder that predates the
manifold) and drive it through the whole pipe to a played lesson — the validated projection then
BECOMES `reference/brunswick.reference.course`, closing the July `_todo` instead of hand-authoring
it (a hand-written reference now would be fake evidence). Scope call: the **employee awareness
course** first (~10 min, five LOs) — it is the proven drive scale, and Jake's hand-built
`cgen/courses/brunswick_pay_transparency_employee` is an exact artisan CONTROL to compare against.
The manager course (10 LOs, scenario-heavy) is drive two on the same store.

### The vocabulary finding — the headline decision

**The manifold had no meaning-kind for expository content.** Every governed `meaning.kind` was
procedure-, form-, or list-shaped, because only SOPs and forms had ever been ingested. A deck that
*states how compensation works* has nothing to DO and nothing to fill in. Per govern-the-vocabularies
this is a version bump, not a silent addition: **`structure.enum.json` → v0.2**, adding `document`
(source-document root), `section` (titled subdivision), `statement` (one meaning-bearing assertion —
the didactic dual of `procedure_step`: a step says DO THIS, a statement says THIS IS SO). The gate
unions vocab files, so the three kinds became governed with no validator change — the 08-13 `govset`
design paying off exactly as intended.

### The store — first non-Astellas client

`cgen/brunswick/{registry,projects/paytrans}`, sibling to `cgen/astellas`, same shape;
`harness_paths` derived the registry anchor with zero changes. Registries seeded v1 as the
namespace-creation act (8 docs, 5 roles, records/options empty) — there was no prior Brunswick
registry to propose INTO; growth from here follows propose→adopt. `tools/headwater_ingest_paytrans.py`
is the authored decomposition (headwater_mode: direct, owns `object` only — no procedure/form facet
anywhere, which the source-type rule permits: at most one, not exactly one): **68 atoms** — 4
document roots (Manager's Guide deck, Comp Philosophy & Framework v3, EOC update, FAQs), 10
sections, 24 statements, 6 lists, 24 list_items. Everything verbatim from the structured extractions
Jake's own Jan-2026 pipeline produced from the pptx sources (`file_to_structured_all_md.py`) — that
derivation is named in the manifest corpus string, the docs registry, and the ingest header, not
hidden. Deliberately NOT decomposed, each named in a Headwater note: the manager-course slides
(practice sessions, reflection guidance, talking points) and the FAQ's per-jurisdiction compliance
table (reference material the course points TO — obj_bw_emp_find_resources — not taught meaning).

### The warrant chain — drafted from documents, not invented

The 08-21 structure gets its first real, non-Astellas exercise, and the client had already written
most of it: the SOW states outcome, audiences, timing, and measurement; the client-ready LO document
IS the objective list; and Jake's own LO-revision analysis contains a reachability judgment made in
the wild — "confidence builds through practice over time" is `not_trainable` reasoning written seven
months before the schema required the field. Minted: **`goal_bw_pay_understood`** (goals v3) with a
four-item `not_trainable` (pay outcomes and pay equity itself; trust; manager conversation quality —
that is drive two's goal; compliance itself) and **five `obj_bw_emp_*` nodes** (objectives v4),
verbatim from the LO doc's employee section, `serves` the goal, Bloom-classified
(3×understand, 2×remember). All `status: draft` — the objective-lock conversation with Jake is the
next hop's first beat, and Brunswick has not ratified the goal statement; the note says both out
loud. The ten manager LOs are deliberately unminted until drive two.

### Lineage woven — Jake's directive

The three Jan-2026 proto-agent prompts in the corpus folder are the pipeline's ancestors, and
`architecture/lineage/2026-01-proto-agent-prompts.md` (+ the three prompts frozen beside it) now
records the mapping: the sense-making prompt → Headwater case_author + the objective derivation
(its "training compensating for structural issues" clause → `reachability.not_trainable` — the
strongest single line of lineage); the design-commitment prompt → the script-primitives IR. The
audit's structural finding: **the exploratory ("high-temperature, non-binding") phase has no agent
seat** — stages 1 and 3 of the proto-pipeline were industrialized, stage 2 was not. Already parked
(Designer/Strategist); the lineage file now says what that seat inherits. Three smaller carries:
signal-vs-noise annotation on ingest scope; open-questions-to-the-project-team for a corpus; a
course-level DESIGN COMMITMENT NOTES analog.

### Open / next (the drive's remaining hops)

Hop two: **objective lock** — Jake ratifies or amends the five draft objectives and the goal, they
go `validated` (the schema's promotion gate makes `serves` binding there). Hop three: catalogs as
project data — scenes/lessons/checks for the employee course, drafted by Claude, ratified by Jake;
realize → cartographer → couturier (heuristics may need their first non-SOP touches — e.g.
`procedure_sequence_atoms` has nothing to walk here, and move classification has never seen
`statement`). Hop four: Brunswick brand pack (`cgen/brands/brunswick` exists) as `/cgen?project=`
chrome. Hop five: ratify the projection as `brunswick.reference.course`, strike the `_todo`, and
run the side-by-side against the artisan control. Standing carries touched, not closed: per-project
ontology store (instances still in core seed); the atom.schema `$id` namespace; Claude push access.

## 2026-08-30 (cleanup) — Two gates that could not run now run and go red: `lint.py` classifier repaired (254 false errors → 0), `layout-engine/ci/validate_sidecar.py` repointed (3 real violations found and closed at the data layer), drifted `_schema/` copies removed

*Anchor: branch `cleanup/tooling-lint-layout-engine` off `24b594c`, 8 files. Proposed by Claude as a
patch series (no push access yet); repo state only once Jake lands it. Verification at delivery:
`lint.py reference schemas vocab ontology ../astellas` → 71 files, **0 errors**; negative controls
(ungoverned `pedagogical_intent`, ungoverned `move`, missing `composed_from`, malformed v2 script)
all go red, exit 1. `validate_sidecar.py` → **OK, 0 violations** out of the box; negative control
(bad sha pin + `ListItem`) fails, exit 1. Every other gate unchanged and green: `validate_atoms` on
all four stores, form 17/17, instance 17/17, socket 21/21, objectives 45/45, realize 266/266,
cartographer 27/27, couturier 35/35.*

**Two gates were recording a state they could not check.** The 2026-08-30 survey that scored the
course half found both in the same condition the 08-21 entry describes for `validate_objectives`
before `77d5d57`: listed ✅ in `STRUCTURE.md`, and unable to execute against the repo as it is.

**`tools/lint.py` — the classifier predated the stores.** It decided kind by shape, and "is a JSON
array" meant "is a script." That was true in July. Since 2026-08-25 the repo holds two more arrays —
`atoms.json` (items keyed `atom_id`) and `occurrences/elements.json` (items keyed `element_id` +
`composed_from`) — and the linter was validating all 248 of their items against
`script.primitives.v1.json`, producing 254 errors, every one false. Nobody had run it since the stores
existed; nothing announced that. Repair: classify by the key the items carry. An **atom store** is
recognised and **deferred** to `validate_atoms.py` with an INFO line — the gate already exists and
does far more than schema; a thinner second copy here would be the drift the 08-13 vendored-schema
entry warns about. An **element store** is schema-validated against `element.schema.json` (same file
realize / cartographer / couturier already validate against on their own runs, so it cannot drift;
this catches a hand-edited store between runs). A **script** is validated against v1 unless it uses a
property only v2 declares — derived from the two schemas at run time, not hardcoded, so
`sample_script.v2.json` stops failing against the wrong version. One incidental fix in the same tool:
the `item_count` check looked for children typed `ListItem`; the element schema and
`cgen/schema/scene.schema.json` both spell it `Bullet`, so the check could never fire. It accepts both.

**`layout-engine/ci/validate_sidecar.py` — a default path from before the move.** Its defaults were
`../../trainstorm-core/{schemas,}`, written when `layout-engine/` sat *beside* `trainstorm-core`.
It now sits *inside*, so the default resolved to `trainstorm-core/trainstorm-core/…` and the gate
crashed before its first check. Repair: auto-detect core as the nearest ancestor holding
`schemas/atom.schema.json` — the same rule as `harness_paths.resolve_core()`, restated because this
gate lives outside `tools/` and must run alone. Once it ran, it found **three real violations**, both
closed at the **data** layer (the sidecar is per-brand data; the schema and the vocab are canon):

| violation | resolution | why there and not in canon |
|---|---|---|
| rule `scenario_to_sort` fires on `script_primitive: scenario` | rule **removed**; the governed `requested_interaction: scenario_select` rule that already routed the same layout is now the only path | no version of `script.primitives` declares a `scenario` type (11 governed types, v1 and v2). The rule's own note says it was added to "close a gap" — i.e. it invented a value. A 12th primitive is a vocabulary decision for `DECISIONS.md`, not a sidecar edit. **Flagged, not made.** |
| `STATIC_CARDS_3` / `REVEAL_GRID` repeat over `where.type: ListItem` | → `Bullet` | `element.schema.json`'s type enum has `List` + `Bullet`; the live Realizer emits `Bullet` for every `list_item` atom (10 of 55 in `ast_alsap`); `cgen/schema/scene.schema.json` agrees. `ListItem` is the prose spelling from July's conventions and survives only in `project/custom_instructions.md` line 28 and the Claude Project instructions — **prose drift, one line, not fixed here** because that file is a one-way snapshot Jake regenerates. |

**`layout-engine/_schema/` — the second copy, again.** Two files, `intent_sidecar.schema.json` and
`template_manifest.schema.json`, drifted from their canonical twins in `schemas/` (old `cgen.local`
`$id`s, pre-Manifold descriptions; 169 and 13 diff lines). The layout-engine README had *already
declared* the adoption into `schemas/` on 2026-07-31 and then kept the copies. Nothing read them —
the validator took `--schema-dir` — so they were pure hazard: the next person to `cp` one back would
re-run the 08-13 incident. Deleted; both docs repointed. Same standing rule, third instance:
*schemas have exactly one home.*

**Standing rule, sharpened.** The 08-21 entry made "a worked example must be gated" a rule. This
adds its mirror: **a gate must be run by something.** A ✅ on a tool that no self-test, CI step or
log entry has executed against the current repo is a claim, not a check. The two tools here had been
✅ since July and August respectively; neither could run. Candidate follow-up (not done): a
`tools/selftest_all.py` or CI job that executes every gate so a broken one announces itself.

**Deliberately not in this pass** (Jake scoped it to broken tooling): the two committed virtualenvs
under `cgen/Trainstorm_Toolkit_v2*/` (2,382 tracked `.pyc`); `atom.schema.json`'s `$id` still on
`astellas.example`; the vestiges `STRUCTURE.md` already names; the cross-store `composed_from` rule
that the 08-26 worked-example block executes but the 08-20 sideways-reference rule forbids — that one
needs a `DECISIONS.md` block with Jake's signature; `ast_artwork`'s six proposed registry entries
awaiting `adopt_registries.py`.

## 2026-08-30 — Artwork store **and** `?project=` loader on main via #42

Same-day correction to the STRUCTURE score hop. PR #42 merged onto
origin (`f9642bc` and later). Store
(`cgen/astellas/projects/ast_artwork/`,
`tools/headwater_ingest_artwork.py`) **and** the Course Engine
`?project=` stand-in (`catalogUrlForProject` in `lessonCatalog.js`;
`main.js` selects the catalog) are on main. Live
`/cgen/?project=ast_artwork` plays SOP-2290; `/cgen` stays ALSAP. A
loader restore PR was not needed and was not opened. The earlier
“do not claim `?project=` plays until the loader PR lands” line was
false — a raw.githubusercontent.com read was still at #41. No new
product. Working-process block untouched. Claude remains a
co-builder.

---

## 2026-08-30 — STRUCTURE reconciled against this main (log refresh)

Score hop only. `STRUCTURE.md` tree + First moves brought to 2026-08-30
against `cgen/trainstorm-core`, not wider `cgen/` vestiges. Course-half
hops after 2026-08-26 (checks, scenes, lessons, `/cgen` player, brand
chrome, learner labels, hide-VO, `?lesson=`) marked done; cite the
dated `DECISIONS.md` blocks. Item 7 brunswick gold course stays open.
Hop-start snapshot had `ast_artwork` on PR #42 Draft (a #41 read);
same-day correction above: store **and** `?project=` loader are on
main via #42.
No new product. Working-process block untouched. Claude remains a
co-builder.

---

## 2026-08-27 — Astellas brand pack is player chrome at `/cgen`

Couturier v1 already wrote pedagogical look keys on occurrences
(`style_ref`: `brand.opening` / `brand.instructional` / `brand.recall`
/ …). Those are **roles**, not hex or fonts. `style_map_v1.md` already
said brand token resolution (`brands/<client>/`) is later. This hop is
that later — **as player chrome**, not as occurrence 1:many.

The pack was already on main (`cgen/brands/astellas/`: tokens, layout,
components, constraints, logos). Course Engine already had loaders
(`brandLoader.js` / `themeLoader.js` / `applyBrand`) and they were
unwired: lesson JSON `meta` had id/title only, fetch paths
`../../brands/` 404 from `/cgen`, no `#brandLogo`. Engine chrome used
`--bg/--panel/--text` (grey system-ui); Astellas tokens use
`--color-bg` etc.

**What `/cgen` reads.** Realize copies the overlay client name
(`cgen/astellas/projects/…`, same axis as the client registry) onto
every `realized_lesson*.json` as `meta.theme`. Runtime loads
`cgen/brands/<theme>/` from that field. Logo from
`astellas-brand.json` `logos.primary`. Engine vars alias the pack
tokens. Unused `runtimeConfig.js` hardcoded astellas is gone —
projection meta wins. Sidecar HTML keeps stand-in clothes. Lumina
untouched. Brunswick not this hop. Couturier map untouched.

Hypothesis verified: the socket was unwired + `meta.theme` missing.
The overlay folder was already the client constitution; no parallel
theme field on `lessons.json`.

---

## 2026-08-27 — `/cgen` plays the ALSAP lesson node (engine projection)

The Course Engine at `/cgen` (`index.html` + `engine/`) did not load a
course: `src/main.js` was missing, and `courses/demo/course.json` is a
parallel authored ALSAP, not the occurrence graph. This hop **points
that existing player at the lesson record**. Same 16 spine
occurrences. Same three scenes. Same three lessons. Same 55 / 47.

**What `/cgen` reads.** The engine cannot honestly consume occurrence
files as-is (Heading / Body / RevealCards / MCQ; linear `scenes[]`).
The minimum adapter is a JSON **projection of the lesson node**,
rebuilt by `realize.py` (`realized_lesson.json`, sibling of the HTML
sidecar). Documented as a projection of the graph, not a hand-authored
SCORM package, not `course.schema.json` as a third constitution.
`/cgen/src/main.js` fetches that file. Sequence practice is a new
`SequenceOrder` component (mapping it to MCQ would be a lie). Job-aid
presents are `StepList`. Invert-definition and closed-choice stay MCQ.
Lesson-end invert_definition is a final pager step, not a fourth named
scene on the graph. Meaning still from atoms via `composed_from`. No
authored `content.text`.

**Unchanged.** `/cgen/lumina`. Tabled `/cgen/alsap` rewrite
(`netlify.toml` not revived). One site-wide CSP. Sidecar HTML still
emitted. `atoms.json` untouched. No catalog UI, chameleon, Headwater
outcomes-mode, Procedure B, quiz engine, LLM distractors, new agent.
Cartographer owns intent. Couturier owns style. Idempotent realize →
cartographer → couturier emits sidecars **and** the JSON `/cgen` reads.

Hypothesis verified: `cgen/` had a course JSON shape (the engine
runtime, not `course.schema.json`). Mapping `manifest.lessons` into
that shape via Realize was enough; loading `elements.json` in the
browser would have duplicated the honesty bar.

---

## 2026-08-27 — Scene catalog is project data

PR #32 lifted lesson records into `occurrences/lessons.json`. Scene
membership was still a spine heuristic inside Realizer (`SCENE_DEFS`,
three ALSAP headings). This hop **lifts scenes into a closed project
file**. Same 16 spine occurrences. Same three scenes. Same three
lessons. Same 55 / 47.

**Where it lives.** `occurrences/scenes.json` is the source of truth
(policy `v1_scene_catalog`). Realizer reads it and stamps
`spine.scenes` (runtime view, policy `v1_scenes_on_graph`). Adding a
scene is appending a record: `id`, title heuristic/ref, ordered
`element_ids`, in-scene checks. Realize does not special-case the
three ALSAP headings beyond reading the catalog. Lessons keep pointing
at `scene_ids` only. Membership is the list PR #29 already stamped —
not a rival grouping. Heuristic `v1_three_scenes_from_roles` may still
propose a default when the file is absent (fixtures / first mint).
Live path is read-the-file. Coverage dump stays a dump. Not a catalog
UI.

**Unchanged.** 16 spine `ele_` ids. 55 / 47. Same three scenes. Same
three lessons. HTML should feel unchanged (short pages 1–2–3; br and
plan single-scene). `atoms.json` untouched. No authored `content.text`.
No Procedure B. No chameleon.py, no Headwater outcomes-mode, no
`/cgen/alsap` hosting, no quiz engine, no LLM distractors, no new
agent. Cartographer owns intent. Couturier owns style. Idempotent
realize → cartographer → couturier.

Hypothesis verified: a closed catalog file was enough; forking
`realize.py` for a fourth ALSAP scene heading would have been a lie.

---

## 2026-08-27 — Lesson catalog is project data; third lesson is Procedure A

PR #31 proved two lesson records on one store (`ast_alsap_short`,
`ast_alsap_br`). Extras still lived as carry-across on the generated
occurrence manifest — adding a third would have been a Python branch
or a hand-edit of a regenerated file. This hop **lifts the catalog
into a closed project file**. Same 16 spine occurrences. Same three
scenes. Same 55 / 47.

**Where it lives.** `occurrences/lessons.json` is the source of truth
(policy `v1_lesson_catalog`). Realizer reads it and stamps
`manifest.lessons` (runtime view, policy `v1_lesson_on_graph`). Adding
a lesson is appending a record: `lesson_id`, `scene_ids`, optional
`lesson_end_check_ids`, optional `paging`. Realize does not
special-case extra lesson ids. Third id `ast_alsap_plan` points at
`how_an_alsap_starts` (job-aid + in-scene `sequence_order`). One scene
→ pager disabled. HTML derived from lesson_id:
`realized_lesson_plan.html`. Default pass emits all catalog lessons.
`--lesson <id>` regenerates that file. Coverage dump stays a dump, not
a fourth lesson. Not a catalog UI.

**Unchanged.** 16 spine `ele_` ids. 55 / 47. Same three scenes.
`atoms.json` untouched. No authored `content.text`. No Procedure B. No
chameleon.py, no Headwater outcomes-mode, no `/cgen/alsap` hosting, no
quiz engine, no LLM distractors, no new agent. Cartographer owns
intent. Couturier owns style. Idempotent realize → cartographer →
couturier.

Hypothesis verified: a closed catalog file was enough; forking
`realize.py` for a third ALSAP lesson would have been a lie.

---

## 2026-08-27 — Second lesson record: BR-only from the same store

PR #30 named one lesson on the graph (`ast_alsap_short`) so a later
agent could emit another by writing a record, not forking HTML. This
hop writes that second record. Same 16 spine occurrences. Same three
scenes on `spine.scenes`. Same 55 / 47.

**Where it lives.** `manifest.lessons` now has two objects.
`ast_alsap_short` (default) still lists all three scene ids and the
invert-definition extras. `ast_alsap_br` lists only
`benefit_risk_on_the_form`. Those invert-definition extras do **not**
belong on the BR lesson (they close front-matter, not the form
cluster); the in-scene `closed_choice` does. Projector derives
`realized_lesson_br.html` from the lesson_id. One scene → pager
disabled (same `v1_one_scene_at_a_time` policy). Realize carries extra
lesson records across a fresh manifest rebuild. Coverage dump stays a
second projection, not a third lesson. Not a catalog UI.

**Unchanged.** 16 spine `ele_` ids. 55 / 47. Same three scenes.
`atoms.json` untouched. No authored `content.text`. No Procedure B. No
chameleon.py, no Headwater outcomes-mode, no `/cgen/alsap` hosting, no
quiz engine, no LLM distractors, no new agent. Cartographer owns
intent. Couturier owns style. Idempotent realize → cartographer →
couturier.

Hypothesis verified: a second lesson record on the same occurrence
store was enough; forking `realize.py` for ALSAP would have been a lie.

---

## 2026-08-27 — Lesson is a graph object that points at `spine.scenes`

After PR #29 scene membership lived on `spine.scenes` / `ext.scene`.
The short ALSAP lesson was still a projector convention:
`realized_lesson.html` was “the” lesson because `realize.py` knew this
project. This hop **names the lesson on the graph**. Same 16 spine
occurrences. Same three scenes. Same paging UX. Same checks.

**Where it lives.** `manifest.lessons` is the index — `lesson_id`,
title heuristic (`title_from` = document-root atom), ordered `scene_ids`
into `spine.scenes`, `lesson_end_check_ids`, paging pointer. Analogous
to `manifest.checks`. No `Course` `ele_` (no honest `composed_from` for
a container; `element.schema.json` already names the type; the SOP root
occurrence is already `type: Course`). Not a rival `course.schema.json`.
Not a LMS. Not SCORM. Not a catalog UI. Projector reads the selected
lesson (`--lesson` or default `{project}_short`) then its scenes. It
does not assume the ALSAP trio. Extra lesson records are preserved on
re-stamp. Coverage dump stays a second projection, not a second lesson
node.

**Unchanged.** 16 spine `ele_` ids. 55 / 47. Same paging
(`v1_one_scene_at_a_time`). Same three scenes. `atoms.json` untouched.
No authored `content.text`. No Procedure B. No chameleon.py, no
Headwater outcomes-mode, no `/cgen/alsap` hosting, no quiz engine, no
LLM distractors, no new agent. Cartographer owns intent. Couturier
owns style. Idempotent realize → cartographer → couturier. Sequence
check in scene 2; BR closed-choice in scene 3; invert_definition at
end.

Hypothesis verified: a sibling lesson record on the occurrence
manifest was enough; minting a Course `ele_` would have been a lie.

---

## 2026-08-27 — Scene membership and order first-class on the graph

After PR #28 the three check kinds lived on `ext.check` /
`manifest.checks`. Scenes and one-at-a-time paging were still projector
chrome: three named ALSAP headings plus a pager, membership recomputed
from SOP/form roles at project time. This hop **names them on the
graph**. Same 16 spine occurrences. Same three scenes. Same paging UX.

**Where they live.** `spine.scenes` is the source of truth — ordered
scene objects with `element_ids` — analogous to `manifest.checks`.
Closed roles `vocab/scene.enum.json`: `front_matter` / `procedure_a` /
`form_br`. Member occurrences carry `ext.scene`. In-scene checks are
shape refs into `manifest.checks` (`sequence_order` in scene 2,
`closed_choice` in scene 3). Invert-definition extras stay lesson-end,
not a fourth scene. Projector reads the stamp to wrap/page. It does
not re-discover scenes by if-atom-id. Headings stay the documented
title heuristic, not outcome language.

**Unchanged.** 16 spine `ele_` ids. 55 / 47. Same paging
(`v1_one_scene_at_a_time`). Same three scenes. `atoms.json` untouched.
No authored `content.text`. No Procedure B. No chameleon.py, no
Headwater outcomes-mode, no `/cgen/alsap` hosting, no quiz engine, no
LLM distractors, no new agent. Cartographer owns intent. Couturier
owns style. Idempotent realize → cartographer → couturier. Sequence
check in scene 2; BR closed-choice in scene 3; invert_definition at
end.

Hypothesis verified: `spine.scenes` was enough; no parallel scene
meaning store.

---

## 2026-08-27 — Check shapes first-class on the graph

After PR #27 the short ALSAP lesson already had three honest check
kinds in the projector: invert-definition MCQ from sibling first
sentences, Procedure A sequence from `object.order`, and a BR
closed-choice from `reg_benefit_risk_profile` + instance
`selected_value`. They lived as Python/HTML branches
(`mcq_siblings` / `sequence` / `derive_br_profile_check` by atom id).
This hop **names them on the graph**. Main had moved (PR #26 paging,
PR #27 projector-only closed-choice); this rebase keeps that newer
behavior and stops special-casing HTML by atom id.

**Where they live.** Closed vocab `vocab/check-shape.enum.json`:
`invert_definition`, `sequence_order`, `closed_choice`. Host records
on `ext.check` (definition extras). Projector-only `sequence_order`
and `closed_choice` on `manifest.checks` (minting an extra `ele_` from
one A step, or from only the form field / only the instance, is still
a lie). Operands are refs — atom ids, `ele_` ids, `options_ref`,
`order_from` — not copied option strings. Projector reads the stamp
and resolves wording. Cloze is a render of `invert_definition` when
contrast is empty. Closed-choice options stay verbatim value ids;
prompt stays task clothes (*Choose the closed value already shown.*).

**Unchanged.** 16 spine `ele_` ids. 55 / 47. Same paging
(`v1_one_scene_at_a_time`). Same three scenes. `atoms.json` untouched.
No authored `content.text`. No Procedure B. No chameleon.py, no
Headwater outcomes-mode, no `/cgen/alsap` hosting, no quiz engine, no
LLM distractors, no new agent. Cartographer owns intent. Couturier
owns style. Idempotent realize → cartographer → couturier. Wrong then
right on all three kinds.

Hypothesis verified: `ext` was enough; `element.assessment` stays
empty of option labels.

---

## 2026-08-26 — Scene 3 BR closed-choice (the fill already shown)

After PR #26 scene 3 taught the FORM-AST-34037 BR fields and showed the
ASP-9999 fills, then jumped to lesson-end definition checks. An ID would
practice that fill near the example. This entry records that hop.

**Shape.** `agents/realizer/check_v1.md` gains `closed_choice` beside invert-
definition `mcq_siblings` / `cloze` and Procedure A `sequence`. Options =
verbatim value ids of `reg_benefit_risk_profile` (the form field’s
`options_ref`; full set). Key = instance `selected_value`
`conditional_favorable` (also `source_text`). Prompt is task clothes:
*Choose the closed value already shown.* Not “which BR profile is
required?” Feedback does not invent SOP facts. Stable shuffle so the
learner can be wrong, then right. Rationale has no `options_ref` — no
honest closed set; not this check.

**Mint nothing.** Composing from the instance alone hides the options set.
Composing from the form field alone hides the key. Project from the two
existing guest `ele_` records (form present + instance exemplify). Store
stays 55 / 47. `atoms.json` untouched. Spine `element_ids` still 16.
`spine.br_profile_check` documents the projection. Placement: in-scene 3,
after field+example, before lesson-end definition checks. Paging from
PR #26 stays.

Closed vocab: no `retrieve`. Did not stamp `practice` on a fake extra.
No chameleon.py, no Headwater outcomes-mode, no `/cgen/alsap` hosting,
no Procedure B, no extra form dump, no 1:many of the SOP, no
distractor-writer. Idempotent with realize → cartographer → couturier.

---

## 2026-08-26 — ALSAP short lesson pages one named scene at a time (player chrome)

After PR #25 the short lesson read as three named scenes (front-matter,
Procedure A, form BR) but still *scrolled* as one long page. This hop is
**player chrome only**. Same 16 spine occurrences. Same headings.

**Paging.** Projector shows one named scene at a time (`spine.scenes.paging`,
policy `v1_one_scene_at_a_time`). Next / Back moves between the three
scenes. Sequence practice stays in scene 2. Definition/purpose checks stay
at lesson end — a final player step after Next from scene 3, not a fourth
scene. Hash is optional. Not an LLM. Not outcome language.

Same 16 `ele_` ids. Same `composed_from`. `atoms.json` untouched. No
authored `content.text`. No new `ele_`. Coverage dump stays ungrouped and
unpaged. Couturier still dresses occurrences; Realizer pages the existing
scene sections.

Store 55 / 47. Membership policy unchanged. No chameleon.py, no Headwater
outcomes-mode, no LLM distractors, no `/cgen/alsap` hosting, no Procedure
B, no extra form dump, no extra beats. Idempotent with realize →
cartographer → couturier.

---

## 2026-08-26 — ALSAP short lesson reads as three scenes (layout chrome)

After PR #24 the short lesson was a coherent SOP-course seed: front-matter,
Procedure A job-aid + sequence check, form BR presents + ASP-9999 examples,
definition/purpose checks. It still *looked* like sixteen stacked cards.
This hop is **layout only**.

**Scenes.** Documented heuristic from SOP/form roles already in the graph
(`spine.scenes`, policy `v1_three_scenes_from_roles`), not an LLM and not
outcome language:

1. **What an ALSAP is** — front-matter cluster (title, why-this callout,
   purpose, scope, general).
2. **How an ALSAP starts** — Procedure A job-aid. Sequence practice stays
   in-scene.
3. **Benefit-risk on the form** — FORM-AST-34037 BR-field presents then
   the instance examples that fill them.

Definition/purpose checks stay at lesson end (not a fourth scene). Same
16 `ele_` ids. Same `composed_from`. `atoms.json` untouched. No authored
`content.text`. No new `ele_`. Coverage dump stays ungrouped. Couturier
still dresses occurrences; Realizer groups them.

Store 55 / 47. Membership policy unchanged. No chameleon.py, no Headwater
outcomes-mode, no LLM distractors, no `/cgen/alsap` hosting, no Procedure
B, no extra form dump. Idempotent with realize → cartographer → couturier.

---

## 2026-08-26 — Form BR-field present before the instance examples

After PR #23 the short lesson walked Procedure A as a job-aid, practiced
that order, then showed two ASP-9999 filled FORM-AST-34037 values that
do **not** illustrate A. An ID would show the field those values fill
before the filled example. This entry records that hop.

**Which atoms.** The instance examples `instantiates` exactly
`atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_profile` and
`atom_form_ast34037_sec_purpose_sec_safety_profile_f_br_rationale`.
Meaning join, not a cousin. Not `f_br_guidance`. Not phrasing examples.
If those field atoms were missing, stop.

**Cross-store.** Guest `ele_` records in the ALSAP occurrence store
`composed_from` the form `atom_id`. Catalog joins SOP + `alsap` +
`alsap_asp9999`. No copy into `ast_alsap/atoms.json`. Clothes: `present`
→ `brand.instructional` / kicker Present / `tp_body`. Placement: both
form presents, then both instance examples (do not split the example
pair). Spine policy
`v1_front_matter_callout_procedure_sequence_form_example_then_checks`.
Store 55 / 47. Spine 16. Form and instance stores untouched. No
chameleon.py, no Headwater outcomes-mode, no LLM distractors, no
procedure-step MCQ, no `/cgen/alsap` hosting.

Idempotent with realize → cartographer → couturier.

---
## 2026-08-26 — Procedure A sequence practice (order the four existing step atoms)

After PR #22 the short lesson walked Procedure A as a job-aid, then showed
an instance example, then two definition checks. An ID would practice the
**order** of those steps near the job aid. This entry records that hop.

**Shape.** `agents/realizer/check_v1.md` gains `sequence` beside invert-
definition `mcq_siblings` / `cloze`. Items = first sentences of
`atom_sop_ast29080_proc_a_s1` … `_s4` (verbatim). Correct order =
`bindings.object.order` (already taught). Prompt is task clothes: *Put
these in the order already taught.* Not “which is the first planning
step?” (PR #16 refused that invented fact). Feedback does not invent SOP
facts. Stable shuffle so the learner can be wrong, then right.

**Mint nothing.** Composing from one A step is a lie (the check is the
four siblings). Composing from the thin A heading is a lie. Project from
the four existing present `ele_` records. Store stays 53 / 47.
`atoms.json` untouched. Spine `element_ids` still 14.
`spine.sequence_check` documents the projection. Placement: after the
job aid, before the instance example (`exemplify` stays). Definition
checks stay at the end.

Closed vocab: no `retrieve`. Did not stamp `practice` on a fake extra.
No chameleon.py, no Headwater outcomes-mode, no `/cgen/alsap` hosting,
no 1:many of the SOP, no distractor-writer. Idempotent with realize →
cartographer → couturier.

---
## 2026-08-26 — One worked example on the ALSAP spine (instance atoms via composed_from)

The short lesson already had opening, why-this callout of purpose, front-matter,
Procedure A as a job-aid, then two checks. This hop puts **that it happened**
on the path: one worked example after the job aid, before the checks.

**Heuristic (small seed, not all ten).** Procedure A has no honest match in
`alsap_asp9999` — those atoms are filled AST-34037 values, not notify / kick-off
/ authors / dates. They illustrate the ALSAP generally. Cited:

- BR profile `conditional_favorable`
- BR rationale (authored SMT judgment; names ASP9999)

Not cited: cover metadata, slot fills (412, AE lists, duplicate ASP9999).

**Cross-store.** Lesson store is `ast_alsap`. Instance is `alsap_asp9999`.
Realizer mints guest `ele_` records in the ALSAP occurrence store whose
`composed_from` is the instance `atom_id`. Meaning catalog joins the sibling
store. No copy into `ast_alsap/atoms.json`. No parallel meaning atom. Clothes:
`exemplify` → Couturier `brand.example` / kicker Example / `tp_body`. Spine
policy `v1_front_matter_callout_procedure_sequence_example_then_checks`. Store
53 / 47. Instance store untouched. No chameleon.py, no audience variants, no
LLM distractors, no procedure-step MCQ, no `/cgen/alsap` hosting.

Idempotent with realize → cartographer → couturier.

---
## 2026-08-26 — Authoring Chameleon vs runtime Chameleon; `tp_callout` on the spine

Two jobs were mixed in the Chameleon stub (“writes nothing / do not
build”). Jake agreed they split: **runtime** Chameleon (wake on a live
learner, pick a variant) is Learner Response Engine / frontier.
**Authoring** Chameleon is in-scope for a static course — assumed
audience, write `audience` facets onto **occurrences** (not atoms’
meaning, not PII) so the course is generated around that impression.
Same keys the engine would later read (`segment_scope`, `difficulty`,
`variant_group`). Without LRE the impression is a documented
hypothesis, like Cartographer’s heuristic. The wake differs
(content-pipeline write vs learner-context event); the facet contract
does not.

Chameleon does not mint `ele_` (Realizer mints). Headwater owns
meaning. Couturier owns style. Audience 1:many is another occurrence
of the same atom, not a variant SOP. This hop does **not** stand up
the agent: no `chameleon.py`, no SOP variants, no live `audience`
bind. v1, when it happens, is one documented assumed segment on the
ALSAP lesson. Stub + system-prompt stub amended so authoring is no
longer “do not build”; runtime / LRE still is. No PII. Working-process
block untouched.

Same PR, original build (not Chameleon): PR #20 paid atom → primitives
but left `tp_callout` unused on the spine. Verified
`atom_sop_ast29080_purpose` is the why-this sentence; title is the SOP
name (already hook + present). Realizer mints
`ele_sop_ast29080_purpose__activate` (`move: activate` → `tp_callout`).
Spine policy `v1_front_matter_callout_procedure_sequence_then_checks`
puts that extra after the title opening and before the purpose
primary. Meaning via `composed_from`. No authored `content.text`. No
procedure-step MCQ. `atoms.json` untouched. Store 51 / 47. Projector
kicker **Why this**. Hosting / `/cgen/alsap` stays tabled. Demo remains
`realized_lesson.html`. Idempotent with realize → cartographer →
couturier.

---
## 2026-08-26 — Atom → primitives (closed compiler form on the occurrence)

The course chain already minted occurrences, bound move/teaches, dressed
style, and projected a short spine with Procedure A as four presents plus
two checks. Every beat was still atom text in a styled HTML card. This
entry records the owed **atom → primitives** hop.

`tools/realize.py` binds a closed five-role compiler vocabulary onto
`expression.text_primitive` (`agents/realizer/primitives_v1.md`, policy
`v1_atom_to_primitive`): heading `tp_display`, body `tp_body`, step
`tp_step`, callout `tp_callout`, check `tp_recall`. Selection is atom
`meaning.kind` + occurrence `move` — procedure_step → step even when the
move is present/transfer; reinforce → check; hook → heading. Registry
`primitives.v0.4` adds `tp_step` and `tp_callout`; the other three keys
already existed from Couturier v1. Not a design system. Not an LLM call.

Realizer owns the hop. Cartographer refreshes the key after writing move.
Couturier still owns `style_ref` and preserves `text_primitive`; a step
gets `layout_hint: job_aid`. The short-lesson projector groups consecutive
`tp_step` spine beats into one numbered job-aid (Procedure A s1–s4).
Front-matter is heading/body. Reinforce stays the existing check.
Coverage dump stays card-like. Meaning via `composed_from`. No authored
`content.text`. `atoms.json` untouched. Store stays 50.

Idempotent with realize → cartographer → couturier.

Not this hop: Netlify / `/cgen/alsap` hosting (Jake tabled the redirect
loop; buried projector path stays the demo URL), distractor-writer,
procedure-step MCQs, 1:many of the SOP, Dragoman, Storyline, `.potx`,
motion, PNG pipelines.

---
## 2026-08-26 — `/cgen/alsap/` rewrite needs `force = true` (Pretty URLs)

PR #18 rewrote `/cgen/alsap/` to the projector file without `force`.
On production Pretty URLs treated that slash path as a directory and
301’d `/cgen/alsap/` → `/cgen/alsap/` (self). `/cgen/alsap` 301’d to
the slash, then looped. Jake got `ERR_TOO_MANY_REDIRECTS`. Buried
`realized_lesson.html` stayed 200. `/cgen/alsap/coverage` self-301’d
the same way.

Fix: `force = true` on the ALSAP 200 rewrites (and the one-hop 301s)
in `netlify.toml`. Canonical URL remains `/cgen/alsap/` so relative
coverage hrefs stay siblings. No parallel HTML store. No second CSP.
`/cgen` and `/cgen/lumina` untouched.

---
## 2026-08-26 — ALSAP short lesson public URL (`/cgen/alsap`)

After PR #17 the short lesson lived at the buried static path
`cgen/astellas/projects/ast_alsap/realized_lesson.html`. Jake needed a
URL he can send. This hop is hosting, not a new projector.

`netlify.toml` rewrites `/cgen/alsap/` (and `/cgen/alsap` → that slash)
to the projector file Realizer already writes. `/cgen/alsap/coverage`
rewrites to `realized_coverage.html`. Sibling names
(`realized_lesson.html` / `realized_coverage.html`) are also rewritten
under `/cgen/alsap/` so the HTML’s relative `href`s keep working on the
short URL and as `file://` locally. Not a third lesson store. Not a
hand-copied HTML. After realize → cartographer → couturier, the public
entry is current because it *is* that file.

`/cgen` and `/cgen/lumina` untouched. `_headers` untouched — one
site-wide CSP (PR #6 stacking). `/cgen` is the Course Engine player, not
a lesson index; no new app shell. `atoms.json` unchanged. Python tools
unchanged.

Not this hop: Dragoman, Storyline, motion, PNG render, a manifold GUI,
path-specific CSP, replacing the `/cgen` player.

---
## 2026-08-26 — Procedure A as a job sequence on the ALSAP lesson spine

The previous 2026-08-26 hop (PR #16) put one Plan Development present
(`atom_sop_ast29080_proc_a_s1`) on the short path. An ID teaching *Plan
Development of ALSAP* would walk the real A steps, not stop at the GSO
notify. This entry records that hop.

`tools/realize.py` extends `agents/realizer/spine_v1.md` (policy
`v1_front_matter_procedure_sequence_then_checks`): after teachable
front-matter, take the first Procedures-container branch in `object.order`,
skip the thin A/B/C heading, take every non-thin `procedure_step` child in
that order. Live ALSAP Procedure A is a handful (s1 notify Lead, s2 identify
authors, s3 15-day kick-off, s4 confirm deliverables). Cap 8; 4 is under it,
so all four land as presents. Branches B/C stay coverage.

No extra `reinforce`. Procedure steps are imperatives; sibling first
sentences exist but there is no honest copula invert. Cloze is not sibling
contrast. Distractor-writer stays parked. Store stays 50. `atoms.json`
untouched. Checks still at the end. Idempotent with realize → cartographer
→ couturier.

Not this hop: distractor-writer, Dragoman, Storyline, `.potx`, motion, PNG
pipelines, rewriting SOP/form atoms into elements, 1:many of the procedure
tree, inventing a `retrieve` enum, procedure B/C on the spine.

---
## 2026-08-26 — One real procedure on the ALSAP lesson spine

Spine v1 (PR #15) projected front-matter then the two existing checks.
Procedure steps lived only in `realized_coverage.html`. An ID would teach
doing the work. This entry records putting **one** teaching-worthy
procedure present on the short path.

`tools/realize.py` extends `agents/realizer/spine_v1.md` (policy
`v1_front_matter_one_procedure_then_checks`): after teachable front-matter,
take the first Procedures-container branch in `object.order`, skip the thin
A/B/C heading, take its first non-thin `procedure_step`. Live ALSAP: Procedure
A (Plan Development) lead `atom_sop_ast29080_proc_a_s1` — GSO notifies SDS
and requests an ALSAP Lead. First real work; B and C cannot start without
it. Cap 1. Later A steps and branches B/C stay coverage.

No extra `reinforce`. Procedure steps are imperatives; sibling first
sentences exist but there is no honest copula invert. Cloze is not sibling
contrast. Distractor-writer stays parked. Store stays 50. `atoms.json`
untouched. Checks still at the end. Idempotent with realize → cartographer
→ couturier.

Not this hop: distractor-writer, Dragoman, Storyline, `.potx`, motion, PNG
pipelines, rewriting SOP/form atoms into elements, 1:many of the procedure
tree, inventing a `retrieve` enum.

---
## 2026-08-25 — Lesson spine v1 (short path; dump is coverage)

The course hop was proven through extra `reinforce` as a check (PR #14), but
`realized_lesson.html` still walked every SOP atom in document order — 47
cards plus extras. That is a dressed SOP, not a course. This entry records
the first **short lesson path**.

`tools/realize.py` projects a documented heuristic
(`agents/realizer/spine_v1.md`, policy `v1_front_matter_then_checks`):
document-root opening (title hook + seeded present extra), then teachable
front-matter primaries (purpose, scope, general — skip thin headings and
the glossary pointer), then the two existing reinforce checks. Cartographer's
object tree is reused as *input* (root vs child vs descendant, sibling
`order`); walking it remains coverage, not the path. No new 1:many. No
`retrieve` enum. No LLM path-picker. No distractor-writer (parked).

Default HTML is the spine. `realized_coverage.html` keeps the full dump.
Manifest stamps `spine.element_ids`. 50 `ele_` records stay. `atoms.json`
untouched. Idempotent with realize → cartographer → couturier.

Not this hop: Dragoman, Storyline, `.potx`, motion, PNG pipelines, rewriting
SOP/form atoms into elements, inventing distractors with a model.

---
## 2026-08-25 — Extra `reinforce` is a check (render of move + atom meaning)

Couturier v1 (PR #13) dressed `reinforce` as `brand.recall` / `tp_recall`, but
the extra occurrence on the ALSAP definition was still the same SOP paragraph
in a Remember recap. Traditional ID’s third move is a check. This entry
records that the extra `reinforce` now *instructs*.

The HTML projector in `tools/realize.py` branches on `intent.move ==
reinforce` (and Couturier `brand.recall` / `tp_recall`) and emits a check UI
from the atom (`agents/realizer/check_v1.md`). No new agent. No authored
`content.text`. No new `retrieve` enum. Shape is `mcq_siblings` or `cloze` —
a key, not a second meaning. Key ⊆ this atom; distractors ⊆ sibling atoms
in the same store (definition vs purpose vs scope as closed contrast). Couturier
`layout_hint` for `reinforce` is `check`.

Seed: keep `ele_sop_ast29080_general__reinforce`; mint one more teaching-worthy
extra, `ele_sop_ast29080_purpose__reinforce`. Not the whole SOP. Idempotent
with realize → cartographer → couturier. `atoms.json` untouched.

Not this hop: Dragoman, Storyline, `.potx`, motion, PNG pipelines, rewriting
SOP/form atoms into elements, inventing a `retrieve` move.

---
## 2026-08-25 — Couturier v1: first writer of style on the occurrence

Realizer minted `ele_` records (PR #10, 1:many seed PR #12) and Cartographer bound
`move` / `teaches` (PR #11), but every occurrence still *looked* like the same SOP
card. This entry records the first writer of occurrence style.

`tools/couturier.py` is a **documented move→look map**
(`agents/couturier/style_map_v1.md`), not a design system. It writes
`element.expression` style keys (`style_ref`, `text_primitive`, `content_role`,
`layout_hint`) onto existing `ele_` records, stamps `ext.couturier`, re-projects
`realized_lesson.html`, and mints no ids. `atoms.json` and `element.intent`
untouched. Locale packs stay on `atom_id`; style is on `element_id`.

The map is from `intent.move`. The 1:many pairs must not wear the same clothes:
title `hook` → `brand.opening` / `tp_display`; title extra `present` →
`brand.instructional` / `tp_body`; definition `present` vs extra `reinforce` →
instructional vs `brand.recall` / `tp_recall`. Other live moves get a distinct
look. Unmapped `practice` / `feedback` / `assess` stay undressed. Motion /
`.potx` layout_primitive / Storyline interaction_primitive are not this hop.

`vocab/primitives.registry.json` bumped to v0.3 for the handful of look keys.
HTML projector reads expression keys, not authored `content.text`.

Not this hop: Dragoman, Storyline, `.potx`, motion primitives, PNG pipelines,
rewriting SOP/form atoms into elements.

---
## 2026-08-25 — Realizer 1:many seed lands in the live ALSAP store (two atoms, not the SOP)

The store was still 1:1 after Realizer v1 (one `ele_` per atom) and Cartographer v1 (intent on
those records). This entry records the first extra occurrences: the same atom, twice, with
distinct `move`, no duplicated meaning.

`tools/realize.py` mints a documented seed (`agents/realizer/one_to_many_v1.md`):

- `atom_sop_ast29080` → extra `ele_sop_ast29080__present` (`present`; primary stays `hook`)
- `atom_sop_ast29080_general` → extra `ele_sop_ast29080_general__reinforce` (`reinforce` as
  the closed-vocab name for retrieve/retention; primary stays `present`)

The other 45 atoms stay 1:1. Extra ids are stable (`primary ele_ + "__" + move`). Re-run of
realize accretes missing extras and does not drop extras or Cartographer bindings. Cartographer
is re-runnable on the mixed store: it still writes `teaches` / `rhetorical` /
`intended_response`, and it **preserves** the extra's stamped `move` (flag
`extra_occurrence_move_preserved`). HTML groups cards that share `composed_from`.
`atoms.json` untouched; no `content.text` on occurrences.

Not this hop: Couturier, Dragoman, Storyline, a full ID treatment of the SOP, a new `retrieve`
enum value.

---
## 2026-08-25 — Cartographer v1: first occurrence-intent write. Heuristic compiler; small ALSAP ontology.

Previous Cartographer dispatches (2026-08-21) wrote nothing: `teaches` was unbindable because the
ontology was two `status: example` PSI nodes. Realizer v1 then minted 47 ALSAP occurrences, all
`move: present`. This entry records the first writer of the intent facet on that store.

`tools/cartographer.py` is a **documented heuristic compiler** (`agents/cartographer/heuristic_v1.md`),
not a model call and not fake ID genius. It reads atoms for meaning, writes `element.intent`
(`move`, `teaches`, `rhetorical`, `intended_response`) onto existing `ele_` records, stamps
`ext.cartographer` (including low-confidence flags), re-projects `realized_lesson.html`, and does
not touch `atoms.json`. It never mints ids.

Ontology seed, small and honest: `goal_alsap_asset_safety_monitored` (`status: draft`) plus five
draft `obj_` nodes distilled from SOP-AST-29080. The AST009 PSI example goal/objectives stay.
Draft is not validated — no human lock. `teaches` binds sparsely; container labels stay empty
(coverage is a walk over children).

Next: Couturier, or Realizer minting a second occurrence of 1–2 atoms (1:many in the store).
Cartographer does not do that.

---
## 2026-08-25 — Realizer v1: first course hop. One occurrence per atom; HTML reads meaning from the atom.

Schemas already enforced 1:many (PR #9). Nothing had yet *written* an occurrence. `tools/realize.py`
is that writer: it walks a live atom store (default `ast_alsap`, 47 SOP atoms), mints one `ele_` per
atom with `composed_from` and `move: present`, copies no authored `content.text`, writes
`<project>/occurrences/` (atoms.json untouched), and projects `realized_lesson.html` so Jake can
open it in a browser. Provenance is `realized_from` / source hashes.

v1 is 1:1 on purpose. Preview → teach → retrieve as three elements of the same atom can accrete
later without changing atom ids; Cartographer is not a v1 gate. Couturier, Dragoman, Storyline,
`.potx`, and PNG render pipelines are not this hop. Live SOP/form stores stay atoms.

---

## 2026-08-25 — Schemas now enforce occurrence identity; 2026-08-21 Fable-run restitch LANDED

The 2026-08-25 occurrence-identity block in `DECISIONS.md` was ratified in prose (PR #8) while
`element.schema.json` still treated `element_id` as the locale-pack join key and required `content`
as source meaning, and `atom.schema.json` still carried a populated `bindings.intent`. This entry
records that the schemas, gates, and worked examples now match that block:

- `element.schema.json` requires `composed_from` (an `atom_id`); `element_id` is the `ele_`
  occurrence key, minted at realization; locale packs are not keyed by `element_id`.
- Authored meaning does not live on the element. `content` / `content.text` is not required as the
  source-meaning store; remaining `content` is optional presentation-constraint copy only (default
  omit).
- `atom.bindings.intent` is empty and closed. `teaches` + `intended_response` live on the
  occurrence (`element.intent`), with `rhetorical` and `move`.
- `validate_atoms.py` / `validate_objectives.py` enforce the closed binding and the occurrence
  link. `reference/example_atom.json` has no intent fields; `reference/example_element.json` has
  `composed_from` and no authored `content`.

Live Astellas stores (`ast_alsap`, `alsap`, `alsap_asp9999`) were already atoms with zero intent
bindings — no SOP/form rewrite into elements. Not in this landing: `realize.py`, Dragoman, renderer.

The PENDING banner on the 2026-08-21 Fable-run entry below is struck.

---

## 2026-08-21 (Fable run) — LANDED 2026-08-25: objectives are INTERVENTION-SCOPED. The restitch executes: `teaches` + `intended_response` off the atom; `atom.intent` is empty and closed. Supersedes the "teaches on the atom" clause of the earlier 2026-08-21 layer-split entry.

> **STATUS (2026-08-25): LANDED.** `atom.schema.json` now has `bindings.intent` empty and closed;
> `teaches` + `intended_response` live on the occurrence (`element.intent`). Banner struck when the
> schema PR landed. The body below is the decision as written on 2026-08-21; treat the schema on
> this branch as the contract, not a target.
>
> ~~STATUS AT MIGRATION (2026-08-25): DECIDED by Jake, NOT YET IN THE REPO. The patch this entry
> describes was produced against an uploaded snapshot and has not been applied to `main`.
> `atom.schema.json` on `main` still carries a populated `bindings.intent`. Treat the schema state
> described below as the target, not the current file. Land the patch, then strike this banner.~~

*Jake's ratification, made in the independent Fable-run session after the spec-vs-log collision was
surfaced. Anchor honesty (08-20 sharpened rule): this work ran on an uploaded snapshot, NOT on
origin/main — it is delivered as a reviewed patch + changed files and is repo state only once Jake
lands it. Verification at delivery: objectives gate ALL PASS (extended, negatives proven red),
Fixture A 22/22 incl. 3 negative controls, form 17/17, instance 17/17, socket 21/21, all three
astellas stores GATE/PROMOTE PASS, lint 0 errors, layout sidecar contract OK.*

### The decision, and what decided it

The spec (v0.1, ATOM-001/ALIGN-001) and this log's earlier 2026-08-21 entry contradicted each other
on where `teaches` lives — and the contradiction reduced to one prior question: **are objectives
intervention-scoped or capability-scoped?** Jake: intervention-scoped. An intervention-scoped
objective does not outlive the course that minted it, so `teaches` on the atom binds canonical
meaning to particular interventions. The golden fixture measured the cost before the decision was
made: under teaches-on-atom, the atom must carry the UNION of every course's objectives, so a new
course serving a new objective REBINDS the canonical atom — version bump, status reset, approvals
cleared — i.e. course design work re-triggers Quality re-review of unchanged regulatory meaning.
That cost is now gone: a third course touches only its own occurrences.

### What was built

- **`atom.schema.json`** — `bindings.intent` is **empty and closed** (`additionalProperties: false`,
  no properties): any intent field on an atom is a schema failure, not silent drift. The ATOM-001
  forbidden-field posture, enforced at the schema layer.
- **`validate_objectives.py` extended** — the bloom-placement check now asserts the full forbidden
  set (`bloom`, `teaches`, `intended_response`, `rhetorical`, `move`) is absent from `atom.intent`,
  that the binding is empty-and-closed, and (negative control, proven red) that an atom *instance*
  still carrying `intent.teaches` is rejected at runtime.
- **ATOM-002 migration ledger** — `migration/2026-08-21-atom-intent-restitch.candidates.json`.
  Audit: all three astellas stores carry **zero** intent bindings; populated values existed only on
  `reference/example_atom.json` and the Fixture A atom, and both relocate losslessly to occurrence
  records that already carried the same values verbatim. Nothing silently deleted.
- **Cartographer → v0.3** — one writer at ONE layer: all intent fields (`rhetorical`, `move`,
  `teaches`, `intended_response`) are element-side; atoms are read for grounding, never written.
  Reconstruction conflict 2 re-closed the other way; the dispatch's 5/5 "won't bind rhetorical to an
  atom" behaviour generalizes to all intent.
- **Fixture A updated** — now *enforces* the restitched contract (atom carries no intent fields;
  every occurrence carries its own scoped `teaches`), 22/22.

The chain now reads:

```
goal_  --(reachability)-->  obj_ (intervention-scoped; serves, bloom)
element.intent  → rhetorical, move, teaches, intended_response   (occurrence-level, all of it)
atom            → meaning + content_hash only                     (no intent binding)
```

### What this deliberately does NOT settle

**The grounding direction.** "Which atoms ground this objective?" still needs a home now that atoms
no longer point at objectives: a `grounded_in` field on the objective node, or the spec §8.6 scoped
alignment record (which also carries competency/observables). Per the standing rule, not resolved by
casually adding a field — it is the next decision, and the alignment record only earns its keep if
competency modeling arrives with it. Unchanged carries: `composed_from` promotion to first-class
(Fixture A rides `ext` until then), element `content` de-authoring under 1:many, locale identity.

## 2026-08-21 (build) — The warrant chain BUILT and gated 27/27: `goal_` node, reachability as a schema constraint, `serves`, `bloom` moved, `move` added. GAP-05 closed.

*Anchor: `origin/main` at `5d8983a`, 10 files, +346/−50. Three gates PASS/PASS,
`selftest_form_gate` 17/17, `selftest_instance_gate` 17/17, `validate_objectives` 27/27,
`project_alsap` clean (0 owed, 0 stale), all six specializations resolve with purity PASS.
This is the build of the four items the 2026-08-21 (later) entry listed as buildable, in that order.*

### What was built

**1 · `schemas/goal.schema.json` — the business-outcome node.** Owner is the CLIENT's business, not
L&D: if L&D owns the outcome, it is not a business outcome. `label` (what should be different),
`measure` (how anyone would know it moved — required, and it is what separates an outcome from a
wish), and `reachability` — **required**, so a goal cannot exist without one.

**The reachability gate is a schema constraint, not a lint rule.** That was the one design choice
made during the build rather than before it, and it is the right one: the unification map asked for
"a hard gate", and a required object is unavoidable in a way a checked convention is not.

| field | why it is required |
|---|---|
| `trainable` | the part instruction can actually move. If nothing here is true, the project should not exist |
| `not_trainable` | the causes training will NOT fix, named out loud. **May be empty, but the field is required** — an empty array is a claim, not a default |
| `assessed_by` | attribution. This is the highest-leverage judgment in the chain and it must be someone's |

`not_trainable` is the instructional designer's protection, and that is worth stating plainly: it is
what keeps a later audit from reading a flat metric as a training failure.

**2 · `ontology/goals.json`** — seeded with the one goal the existing objective seeds actually imply
(PSI recognised and reported inside the window). Recognition is trainable; channel friction, workload
and incentive structure are named as not. `status: example`, because no client has ratified it. The
schema is shared core; these instances are per-project client content, exactly as 2026-08-12 decided.

**3 · `objectives.schema.json` → v2** — the anticipated additive bump, now triggered. Objectives
already pointed SIDEWAYS (`requires`) and OUTWARD (`framework`); they now point UPWARD:

- **`serves: [goal_id]`** — the WARRANT. An objective with no `serves` is an assertion, not a
  derivation. **Conditionally required once `status: validated`** — draft and example may precede
  their goal; validated may not. That conditional *is* the promotion gate, and it is the shape this
  log has reached for repeatedly: allowed at draft, blocking at promotion.
- **`bloom`** — moved here off both intent bindings.

**4 · `bloom` off the content, `move` onto the element.** Bloom grades a CAPABILITY, not a piece of
content: an atom teaching several objectives has no single level, so a content-level bloom is a walk
over `teaches[]` rather than a stored value. Content inherits its level by reference.

In its place on the element: **`move`**, ten values mirroring `vocab/intent.enum.json`'s
`pedagogical` dimension — **the orphaned vocabulary from the Cartographer dispatch now has a
consumer.** Occurrence-level, sibling to `rhetorical`, per the layer split decided in the earlier
2026-08-21 entry.

```
atom.intent     → teaches                        (meaning-level, stable)
element.intent  → rhetorical, move               (occurrence-level, per-placement)
objective node  → serves, bloom                  (capability-level)
goal node       → reachability                   (warrant-level)
```

The chain now reads **`goal_` --(reachability)--> `obj_` --(teaches)--> content**, with `move` naming
the teaching act and `bloom` the level, each on the node that owns it.

### The gate: `validate_objectives.py`, 7 checks → 27

It now gates the whole chain rather than the objective store alone. Negative controls proven to go
red: a goal with no reachability judgment; a goal that never says what training will not fix; an
ungoverned `goal_` prefix; a dangling `serves[]`; a validated objective with no warrant; a drifted
`element.intent.move` mirror against the vocab; and `bloom` reappearing on `atom.intent`.

*(It was made runnable in `77d5d57`, which repointed it off a hardcoded absolute path via
`harness_paths.resolve_core()`. Before that, the 2026-08-12 entry recording it as "gated 7/7" was
recording a tool that could not execute — a small instance of the 08-19 standing rule, and the reason
that rule exists.)*

### Two findings from the build, both ours

**A worked example that does not validate is worse than none.** Removing `bloom` silently invalidated
`reference/example_atom.json` and `reference/example_element.json`, and **nothing caught it** — no
gate had ever validated the reference examples. Found only by checking on purpose. They are now
checks #16 and #17, proven to go red. **New standing rule: a worked example is a governed artifact
and must be gated.** An invalid one teaches the wrong shape with authority, which is worse than
having no example at all.

**A negative control rotted, for the second time, in exactly the same way.** The "a premature
`serves` is rejected" case correctly began failing the moment `serves` became governed — the same
failure as `reg_benefit_risk_profile` on 08-20, and repaired the same way: assert the RULE (an
unknown field is rejected) using a field name that will never be governed, plus a companion asserting
the now-governed field passes. The 08-20 standing rule — *self-tests assert rules, never the current
contents of a governed list* — held up, but it did not prevent recurrence, because the rot is
introduced by the change that governs the value, not by the test. Worth noticing: **when a decision
governs a previously-ungoverned value, grep the self-tests for it as part of that change.**

### Housekeeping worth one line

Both schemas were edited **surgically** rather than re-serialised. A `json.dumps` round-trip produced
a semantically identical file with a 485-line diff; the surgical edits produce 8 and 5. On a
canonical artifact a diff is the review surface, so reformatting noise is a real cost — it hides the
meaning change inside whitespace churn.

### Cartographer → v0.2

`move` added, `bloom` removed, the warrant chain wired in. Its reconstruction conflicts **2, 3 and 4
close as answered**; conflict 1 (audience) remains downgraded, not urgent. Resolves as
`cartographer.v0.2+spine.v0.2`, purity PASS.

### Still open

The objective ontology holds two example objectives serving one example goal, so **`teaches` remains
largely unbindable**. That is a content gap, not an architectural one, and the structure is now in
place to receive a real corpus. Unchanged carries from the prior entries: bulk decomposition of
FORM-AST-34037; the intake socket spec; the `person` field vs no-PII collision; `element` needs
`composed_from` under 1:many; what `content_hash` means on an element; the spine's atom-centric
"bound to an atom by its `atom_id`" language, which the 1:many decision has made imprecise.

## 2026-08-21 (later) — DECIDED: objectives are DERIVED, not supplied — from reachable business outcomes, classified by Bloom. Closes the last open question of the intent arc and re-opens GAP-05 as buildable.

*Jake's answer to the question left open by the earlier 2026-08-21 entry. It re-derives, from practice,
the `goal_` node that three separate architectural analyses had found missing.*

### The reframe

The question had been posed as **who supplies objectives** — the client's SME, or an agent drafting
from the corpus for ratification. Jake answered a different and better question: **what determines
them.**

> *"Objectives are derived from Bloom's Taxonomy + the reachable business outcomes at which the
> training intervention is aimed."*

Objectives are neither handed over nor invented. They are **derived**. That changes what has to be
built: not an intake path for a list, but a derivation with a source node and a filter.

### 1. The business-outcome half IS the missing `goal_` node

This is the same node three prior analyses found absent, arriving from the practitioner side rather
than the architectural one:

- `architecture/unification-map.md` files it as **GAP-05** and states it flatly: *"The intervention
  warrant IS the business-outcome node: no `goal_`, no project."* It also calls for **a hard gate**
  in the Strategist.
- `architecture/agents-roster.md` has the Designer *reading* `goal_` nodes and *"converting what must
  change into what must be learned."*
- The 2026-08-11 log carries the ROI/goal node as a standing deferral.

Three independent findings that it is missing, and now an independent statement that it is *needed*,
from the person who does the work. Treat GAP-05 as **buildable** rather than deferred.

### 2. Bloom is a CLASSIFIER, not a source — which resolves the `bloom` loose thread

The derivation is asymmetric, and the asymmetry is load-bearing:

- **The reachable outcome** determines *what capability is needed* — the **generative** half.
- **Bloom** grades that capability once you have it — the **classifying** half. It never tells you
  what to teach; it tells you at what cognitive level a capability sits, and therefore what
  instruction and assessment it demands.

**Consequence:** `bloom` belongs on the **objective node**, not on `atom.intent` and not on
`element.intent`, where it currently sits on both. The earlier 2026-08-21 entry flagged this as a
loose thread; Jake's answer is the argument that settles it. An objective carries its own Bloom level;
content inherits it by reference through `teaches`.

### 3. "Reachable" is the hard word, and it names a filter

Not every business outcome is reachable by training. *"Reduce complaints 20%"* may be a process
problem, a staffing problem, or an incentive problem. An instructional designer who accepts an
unreachable outcome ships a course that cannot work, however well built.

So the derivation has three terms, not two:

```
goal_  →  the part of it training can actually move  →  objectives
              ↑ the REACHABILITY FILTER — a judgment, and the highest-value one an ID makes
```

That middle term is what `unification-map.md` meant by a **hard gate** on the warrant band. It is also
what makes an objective *defensible* rather than asserted — the same move as reading disposition off
the template's own colour convention instead of guessing it.

### 4. Two things this unlocks

**Objectives get provenance and staleness.** An objective derived from a goal carries
`derived_from: goal_id`. Change the business outcome and every objective resting on it goes stale, and
every atom that `teaches` those objectives goes stale with it. **This is the two-hop staleness walk for
the third time** — instance-over-template, expression-over-corpus, and now objective-over-goal. The
pattern is now firmly the manifold's main structural idiom.

**The schema already left the door open.** `objectives.schema.json` deliberately **rejects** a `serves`
field, and the 2026-08-12 entry recorded why: adding the ROI/goal upward link later should be *"a
deliberate version bump, not accidental drift."* `tools/validate_objectives.py` still tests that a
premature `serves` is rejected. **That anticipated version bump is now triggerable** — this decision is
what triggers it.

### 5. Core vs per-project answers itself

Goals belong to a client, so objectives derived from them are **per-project content**. The *schema*
stays shared core. That is exactly what the 2026-08-12 entry already decided — *"the objective schema
is shared core; an objective instance is per-project content"* — so no new decision is needed, only
the confirmation that the earlier one survives contact with the derivation.

### What is now buildable, in order

1. **`goal_` node + schema** — the warrant. Nothing above it; everything else here depends on it.
2. **The reachability gate** — a recorded judgment turning a goal into the trainable delta. Human-made;
   an agent may propose.
3. **`serves` on `objectives.schema.json`** — the version bump the schema was built to expect, linking
   objective → goal.
4. **Move `bloom` onto the objective node**, off both intent bindings.

### The intent arc, closed

With this, every question opened by the 2026-08-21 Cartographer dispatch is answered:
the orphaned `pedagogical` vocabulary has a home (`element.intent.move`); the layer split is settled
(`teaches` on the atom, `rhetorical` + `move` on the element); the dispatch call is a project field
rather than a facet; and objectives have a derivation. **Cartographer's four reconstruction conflicts
are now three closed and one downgraded** — conflict 1 (audience) measured only 3/5 in dispatch and
always weakly, and is not urgent.

## 2026-08-21 — DECIDED: teaching MOVES and OBJECTIVES are different things, at different layers. Closes the orphaned vocabulary and the intent layer question; dissolves the dispatch call.

*Jake's calls, made after the 2026-08-21 Cartographer dispatch surfaced all three. Record:
`agents/cartographer/07_examples/dispatch_2026-08-21/findings.md`. No code written yet — these are
decisions with consequences listed, not a build.*

### The problem the dispatch found

`vocab/intent.enum.json` declares two governed dimensions. `rhetorical` (11 values) binds to
`element.intent.rhetorical`. **`pedagogical` (10 values) bound to nothing at all** — three of five
dispatches noticed independently and asked, in nearly the same words, whether a key was missing or the
enum belonged to another agent. Meanwhile `teaches` → `obj_` ids was unbindable for a different reason:
the objective ontology holds two seeded PSI examples and nothing real.

**The orphan is not a vestige.** Read the values in order —
`hook` · `objective` · `activate` · `present` · `exemplify` · `practice` · `feedback` · `assess` ·
`reinforce` · `transfer` — and it is **Gagné's nine events**, with retention and transfer split.
Someone encoded a canonical instructional sequence and never wired it up.

### 1. Moves and objectives are different kinds of thing

- An **objective** is a claim about the learner's future capability. Falsifiable, assessable, and it
  **outlives any particular course**. Jake: *"a much more structured measure of learning."*
- A **move** is a choice about *this moment of delivery* — what teaching act is being performed here.

**The relation is one-to-many:** a hook, a worked example, a practice item and an assessment may all
serve one objective. Moves are the means; the objective is the end. They are not two names for one
idea and must not be collapsed.

### 2. Closed names, unbounded realization — and why the freedom goes where it does

Jake's first framing was that moves should be "a lot more free and creative" than objectives. The
refinement he accepted: **the freedom is in realization, not in naming.**

An open move vocabulary — anyone may invent a move type — would destroy the queries that are the whole
point of having the dimension: *"does this module contain any retrieval practice?"*, *"does every
objective have an `assess` move somewhere?"* Those are coverage walks, and they are exactly the
"sophisticated teaching nuance at render time" the dimension is being adopted for. **An open list would
cost the capability it was opened to buy.**

So: `move` is a **governed closed list**; how a `practice` move is actually built — the scenario, the
interaction, the feedback design — is wide open. Same pattern as `style_ref`: closed key, rich content
behind it.

### 3. The layer split — which also settles the question left open on 2026-08-20

Ask where each belongs and it falls out of the 1:many decision:

- **A move is a property of the OCCURRENCE.** The same atom is a `hook` in module 1 and `reinforce` in
  module 5 — that is spaced repetition, which is the argument that decided 1:many in the first place.
- **`teaches` is a property of the MEANING.** The content serves that objective wherever it appears.

```
atom.intent     → teaches            (meaning-level, stable)
element.intent  → rhetorical, move   (occurrence-level, per-placement)
```

`rhetorical` and `move` are siblings — both answer *"what is this doing here"* — which is why they
live together and why the atom carries neither. **This closes conflict 2 from the Cartographer
reconstruction** (whether `rhetorical` being element-only was oversight or design): design, and the
same reasoning places `move` beside it.

It also delivers the render-cycle goal directly. Render agents read elements; `move` is the key that
tells one a hook is treated differently from an assessment.

### 4. The dispatch call is a PROJECT setting, not a facet binding — conflict 4 dissolved

All five dispatches wanted to classify the nature of expression (persuasive / didactic /
practice-heavy) and all five stopped because nothing owns it. The resolution is not a new facet:

**A project-level field, set by the instructional designer or SME, which an agent may PROPOSE to
change** on the evidence of intent, objectives, audience and corpus. Human sets it; the agent may
argue.

Consequences: it needs no facet, so it **breaks no single-writer rule**; it is per-project, not
per-node, so nothing tags it onto every paragraph; and the proposer it requires is small. The roster's
own phrasing supports this — the dispatch call gates *"which strategy dominates downstream"*, which is
a project-scoped statement.

**This substantially shrinks the proposer question** raised on 2026-08-20. The 5/5 pull was for this
one judgment, and it turns out not to need a cross-facet proposer at all.

### Consequences to build (not built)

- `element.schema.json` gains `intent.move`, enum-mirrored to `intent.enum.json`'s `pedagogical`
  dimension. The mirror-conformance check in `validate_atoms.py` already exists for exactly this shape.
- The Cartographer specialization's `{{FACET_KEYS}}` and its layer note need updating; its flagged
  conflicts 2 and 4 can be struck.
- Coverage walks become writable once real elements exist: per-objective move coverage, and
  "objectives with no `assess`".

### Still open — the one Jake has NOT answered

**Where do real objectives come from?** `ontology/objectives.json` holds two `status: example`
entries. The 2026-08-21 A/B showed this is the true blocker: handing the agent the ontology did not
help, because the ontology is a seed. Unanswered: does the client's SME supply objectives, or does an
agent draft them from the corpus for human ratification — and do they live in core or per-project (an
Astellas objective is not a Brunswick objective)?

**Loose thread:** `bloom` currently appears on both `atom.intent` and `element.intent`. It is arguably
a property of the **objective** rather than of the content, in which case it belongs on the objective
node and on neither. Not examined.

## 2026-08-20 (eighth) — DECIDED: atom→element is 1:many. Two stable ids, and an explicit link. Closes the element/atom question; supersedes the sixth and seventh entries.

*Jake's decision, made on instructional-design grounds rather than on schema archaeology — which is
the correct ground, because the archaeology cannot answer it. **Read this entry instead of the sixth
and seventh; they are the working-out, not the answer.***

> **Re-affirmed 2026-08-25** after PR #7's identity-freeze block re-derived the seventh entry's
> "same node, two costumes" reading from the same archaeology this entry says cannot settle the
> question. See `DECISIONS.md` 2026-08-25 (occurrence identity). This entry stands.

### Why the archaeology could not settle it

- **git is no help.** Every architecture doc and schema shares one first-commit date — the repo was
  seeded in a single commit, so version control preserves no ordering. Internal dates are all there is.
- **No document states the cardinality.** The nearest is `reconciliation.md` hedging that
  course-primitives maps "*almost* 1:1 to an atom."
- **The docs actively conflict, and one of them is out-of-tier.** `reconciliation.md` says
  `element_id` **=** `atom_id`; `STRUCTURE.md` lists `ele_` and `atom_` as **two** stable prefixes;
  `promptpack_manifold.md` §8 says element ids are minted at realization and joined by a
  `derivation` stamp. **Jake's provenance note is decisive here: `promptpack_manifold.md` came from a
  tangential, parallel workstream aimed at a different purpose** — the manifold is meant to take what
  is useful from several builds. It is a crosswalk, not core canon, and was being weighted as canon.

So this was never a recovery job. **It was a live design decision that had not been made.**

### The decision, and the argument that made it

**One atom may become MANY elements. Two stable ids. An explicit link between them.**

The argument is Jake's and it is stronger than the efficiency case that had been offered:

> Reuse is not a convenience here — **repetition is the instrument.** Preview → teach → retrieve is
> spaced repetition of *the same atom* at three positions. A persuasive piece plants a claim,
> develops it, lands it. Every render type does this.

Therefore **a 1:1 model is semantically incapable of instructional design.** Expressing spaced
retrieval would require minting three atoms carrying identical meaning — which then drift apart, so
the architecture would *cause* the failure it exists to prevent. That is not a trade-off; it is a
disqualification.

**Governing picture: atoms are the LEXICON, elements are the UTTERANCES.** A word appears many times
in a text; each occurrence has its own position, emphasis and styling, and none of that duplicates
the dictionary entry. You do not fork the lexicon to say a word twice.

### What follows immediately

- **Two ids, both stable, both real.** `atom_id` = the headword. `element_id` = this occurrence.
  `STRUCTURE.md`'s two-prefix convention is **correct**.
- **`reconciliation.md` §4/§6 is WRONG** where it says "make `element_id` the stable `atom_id`" and
  "`element_id` … = atom_id (the join key)". A real error to correct in that file, not a stale
  phrasing to tolerate.
- **An element must NOT carry its own authored text.** `element.content` as written today is an
  embedded copy — under 1:many that forks the lexicon and means paying for the same translation once
  per occurrence.
- **An explicit atom→element link is REQUIRED** (`composed_from`, or the `derivation` stamp of
  `promptpack` §8). The seventh entry withdrew it; that withdrawal is itself withdrawn.

### What survives, and what dies, from the sixth and seventh entries

Stated explicitly so the next window does not relitigate this:

| claim | verdict |
|---|---|
| sixth: atom / primitives / element are three **layers** | **dead** — the pipeline is source → primitives → elements; atom is the meaning layer feeding it, not a pipeline stage |
| sixth: element needs `composed_from: [atom_id]` | **ALIVE** — required under 1:many, for exactly the reason the sixth entry could not articulate |
| sixth: "Decision (Jake): atom is content canon" | **struck** — a decision Jake never made; see that entry's header |
| seventh: the July docs say "you validate against the element" | **alive**, but it is a statement about the *course chain*, and it comes from the out-of-tier doc |
| seventh: atom and element are **the same node** | **dead** — 1:many makes them different node kinds |
| seventh: `composed_from` "manufactures a split the architecture rejected" | **dead** — the split is real and required |
| seventh: shape does not carry intent; read the document of record | **alive, and reinforced** — with the added rule below |

**New standing rule, from the failure mode this whole sequence exposed:** *a document of record has a
tier.* Reading the declaration instead of inferring from schema shape is necessary but not
sufficient — you must also know **which workstream a document came from and what it was for.** A
crosswalk from a parallel effort was quoted as canon and drove two reversals. Before citing an
architecture doc as authority, establish its tier. Ideally, stamp tier in the docs themselves.

### Re-opened by this decision — flagged, not decided

1. **Locale packs are keyed by `element_id`.** Under 1:many that is the expensive choice: translate
   the meaning **once at `atom_id`**, with element-level overrides only where presentation genuinely
   constrains the rendering (length limits, heading vs sentence). Material cost on AST009-scale work.
2. **Can one element compose MANY atoms?** A paragraph fusing two facts. If yes, `composed_from` is
   an array and the relation is many:many.
3. **What does `content_hash` mean on an element with no content of its own?** It becomes a hash of
   the *composition* — which atoms, which expression choices — not of text. This is what the
   staleness walk will key on, so it needs settling before that walk is built.

### Process note

Three readings of this relationship were produced in one session — two layers, one node, two nodes —
and only the third was decided by the person who owns the architecture, on grounds from his own
discipline. The two wrong ones were both produced by inference from file shapes. **The tell that
inference is happening: the reading changes when a new file is read, rather than when a new argument
is made.**

## 2026-08-20 (seventh) — [SUPERSEDED — see 2026-08-20 (eighth)] `element` and `atom` read as one node

> **SUPERSEDED.** Its central claim — that atom and element are the *same node* — does not survive
> the 1:many decision in the eighth entry. Its process lesson does survive, and is reinforced there.
> This entry is the working-out; the eighth is the answer. Read that first.

*Read before the sixth, which this retracts. Sources, all primary and all July:
`architecture/promptpack_manifold.md` (07-21), `architecture/reconciliation.md`,
`architecture/atom-spec.md` (07-20), `architecture/unification-map.md` (07-24). No code has been
written against either reading; nothing to unwind.*

**Jake declined to ratify the sixth entry's reversal and asked for the July design instead. He was
right to.** The documents are explicit, consistent on the relationship, and say the opposite of what
that entry claimed.

### The relationship, from the source

`promptpack_manifold.md` §1 exists to correct an earlier misreading that was *structurally identical
to the sixth entry's*:

> The conversational map had the pack cooling from hot ideation into a single **atom → element
> promotion**, "where identity is born." **That does not survive the files:** `atom.schema.json` and
> `element.schema.json` are **not two temperatures of one node.** The atom is the *conceptual* node
> (meaning + keyed bindings); the element is the *reconciled production* node that
> `reconciliation.md` builds by unifying the three legacy schemas. **You validate against the
> element. There is no runtime atom→element promotion.**

So:

- **`atom` is the design.** The model of what a node is — thin, owns its meaning, everything else
  keyed, single-writer per binding. `atom-spec.md`: "the node everything else in the architecture
  hangs off." `atom.schema.json` is its minimal reference implementation.
- **`element` is the contract.** The reconciled *production* schema that implements that model,
  unifying three legacy schemas (`course` authoring / `scene` render / `course-primitives`
  substrate).
- **They are one node.** `reconciliation.md` §4: *"`course-primitives`' flat, ID-keyed element array
  → **this is the atom store.** Make `element_id` the stable `atom_id`."* Its convergence sketch
  carries the comment `"element_id": "ele_…",  // = atom_id (stable, the join key)`.

The pipeline (from `script-generation-layer.md`, quoted in `promptpack_manifold.md` §2) contains **no
atom layer at all**:

```
source material → generator → SCRIPT PRIMITIVES → realizer → ELEMENTS → render agents → RENDERED FORMS
```

Three layers, two named transforms. The atom is not a stage; **the atom is what an element *is*.**

### Consequences for the sixth entry's "evidence"

- `ele_ast009_recognize_psi` and `atom_ast009_recognize_psi` carrying the same sentence is the
  **intended correspondence** — one node in its conceptual and production forms — not a fossil of an
  unbuilt join. `element.governance` being byte-identical to `atom.governance` is evidence *for* that.
- The proposed `composed_from: [atom_id]` would have **manufactured the two-layer split the
  architecture explicitly rejected**, turning one node into two. It is withdrawn.

### Where the ambiguity genuinely is: IDENTITY, not relationship

Three July sources disagree, and this is the narrow thing actually left open:

| source | says |
|---|---|
| `reconciliation.md` §4, §6 | `element_id` **=** `atom_id` — one stable join key |
| `STRUCTURE.md` naming conventions | lists `ele_` **and** `atom_` as two separate stable-ID prefixes |
| `promptpack_manifold.md` §8 | "IDs are minted where each layer creates nodes: primitive ids at generation, **`element_id`s at realization**, joined by the `derivation` stamp" |

The first says one id; the third implies element ids are minted downstream and joined by a
`derivation` stamp. Unresolved, and it is the real question underneath all of this.

### What the August harness did, and why it diverged

Everything built from 2026-08-10 validates against `atom.schema.json`, added
`bindings.procedure` / `form` / `instance`, and never touched `element` — against a doc of record
saying "you validate against the element." **There is a defensible reason:** `element` is
course-shaped (`slide_id`, `narration`, `assessment`, motion primitives), and validating an SOP step
against it would be strange. But the divergence was silent, and a silent divergence is how you get
two schemas nobody can choose between.

### The live hypothesis (Jake's, this session — PROPOSED, not decided)

*"Element might simply be a step in the course chain."* That fits the pipeline diagram exactly, and
suggests a reconciliation that costs no new concepts:

**`element` is not a layer above the atom — it is the atom specialized for the COURSE chain, exactly
as `form.facet` and `procedure.facet` specialize it for the document chain.**

The evidence is that element's top-level fields *are* the facets, merely unnested — element predates
the `bindings` convention:

| `element.schema.json` top level | atom equivalent |
|---|---|
| `element_id` · `source_hash` · `content` · `governance` | `atom_id` · `content_hash` · `meaning` · `governance` |
| `structure` | `bindings.object` |
| `intent` · `audience` | `bindings.intent` · `bindings.audience` |
| `expression` (primitive keys) | `bindings.expression` — **element's is the richer, correct one** |
| `narration` | Griot's facet — already has an owner in the roster |
| `render` · `assessment` | no atom equivalent yet |

If that reading holds, the move is `element.facet.schema.json` — a fourth source-type facet beside
procedure / form / instance — one `atom_id`, and the gate already knows how to validate this shape
because it does it three times already. It would honour July (element is the production contract for
courses) *and* August (atom is what you validate) without reversing either.

**Not decided.** It needs testing against `element.schema.json` field by field, and the identity
question above settled first.

### Process note worth keeping

Two confident structural readings in one session were wrong — the sixth entry's, and the
conversational map's that `promptpack_manifold.md` §1 was written to correct. Both invented an
`atom → element` promotion that the files do not support. **When a schema comparison and a document
of record disagree, read the document first.** Schema shapes carry no record of intent, and inferring
intent from them reproduces exactly the error the intent was written down to prevent.

## 2026-08-20 (sixth) — [RETRACTED — see 2026-08-20 (seventh)] element / atom / script-primitives read as three layers

> **RETRACTED 2026-08-20. The central reading in this entry is wrong**, and the July documents say
> the opposite. `element` and `atom` are not two layers awaiting a join; they are one node — the atom
> is the *concept*, the element is its *reconciled production contract*. The proposed
> `composed_from: [atom_id]` fix would have manufactured a split the architecture explicitly
> rejected. Kept for the survey findings in its later sections, which stand. **Read
> 2026-08-20 (seventh) first.**
>
> A line reading *"Decision (Jake, this session): `atom` is the ultimate content canon"* has been
> **struck** rather than corrected in place: Jake gave a hedged recollection, not a decision, and
> recording a decision he did not make is a factual error about him rather than a superseded
> judgment. The log's don't-edit-history convention covers the second, not the first.

*Anchor: `STRUCTURE.md` (uploaded and verified byte-identical to the repo copy),
`architecture/unification-map.md`, `schemas/{element,atom}.schema.json`,
`reference/example_{element,atom}.json`. No code changed — this is a settled reading plus one
reversal, and it names the next rung of the generalized core.*

**The question.** `element.schema.json` and `atom.schema.json` carry the same six facet names, a
byte-for-byte identical `governance` block, and two descriptions each claiming to be *the* canonical
unit. Nothing in the harness reads `element`; nothing in the layout engine or the localize runtime
reads `atom`. Two live lineages that never meet.

### The design was three layers, and it is written down

`STRUCTURE.md` is unambiguous:

| schema | role | question it answers |
|---|---|---|
| `atom.schema.json` | conceptual node (the manifold) | what it **means** |
| `script.primitives.v1.json` | generation IR | what **knowledge** |
| `element.schema.json` | presentation unit | **how shown** |

So the layering Jake recalled is real and documented. **One correction to the recollection, and it
matters:** a Japanese translation is *not* an element. `element.content`'s own description reads
"SOURCE LOCALE ONLY. Do not embed other languages here; translations live in `locales/<lang>.json`
keyed by `element_id`. (This is the fix for the AST009 drift.)" There are three distinct things — the
atom (the concept), the element (this text, shown this way, on this slide), and a locale-pack entry
(that element's text in another language). Modelling a translation as an element would give one
element per language, make `locales/` redundant, and re-embed language in the node — precisely the
drift `element` exists to prevent.

### Why the overlap exists: nobody designed it. `element` predates `atom`.

- `element.schema.json` is titled *"Trainstorm Element (**Unified**)"* — the name of a node that was
  once the only one.
- `STRUCTURE.md` lists exactly one agent, `localize/`. It is the earliest scaffold; six agents now
  exist on disk.
- `atom.schema.json` and `architecture/atom-spec.md` arrived later, slid in *beneath* element, and
  **nothing went back to connect them.**

The worked examples encode the duplication rather than merely permitting it:

```
reference/example_element.json   ele_ast009_recognize_psi
   content.text        = "Recognize product safety information"
reference/example_atom.json      atom_ast009_recognize_psi
   meaning.source_text = "Recognize product safety information"

element -> atom reference: NONE      atom -> element reference: NONE
```

Same sentence, two nodes, ids differing only by prefix, no link either way. The overlap is a fossil
of the sequence, not a decision.

### The reversal, stated plainly

`architecture/unification-map.md` (2026-07-24) rejected a proposal on the grounds that it "would mint
a second canonical source beside **`element.schema.json`**", and describes the content graph as
"**elements** + script primitives + intent ontology". **As of July, element was canon.** The
project's Custom Instructions still say so.

Every harness artifact built since 2026-08-10 — `validate_atoms.py`, `store_merge.py`,
`harness_paths.py`, both ingests, all three project stores, the gate, the self-tests — validates
against **atom**, and nothing validates against element.

**[STRUCK 2026-08-20 — a decision was recorded here that Jake did not make. He offered a hedged
recollection; this entry firmed it into a decision. No reversal was decided. See the seventh entry.]** `architecture/unification-map.md` and
`project/custom_instructions.md` both need correcting to match; until they are, they are the most
authoritative wrong statements in the repo.

### What is actually missing — and it is machinery we have already built twice

`element` needs to become an overlay on atoms:

- **`composed_from: [atom_id]`** — required, non-empty. Does not exist in any form.
- **`content` stops being authored** and is resolved from its atoms at render time. Today it is an
  embedded copy of `atom.meaning`, with `additionalProperties: false` and the same `{locale, text}`
  payload.
- **`source_hash` becomes the hash(es) it bound against**, not a hash of its own embedded content —
  so "which elements went stale when this atom changed?" is one walk.

**This is the third instance of one pattern in a single session:** instance-over-template (built and
gated today), expression-over-corpus (the socket), element-over-atoms. Pin + hash + staleness walk,
three times. The gate logic in `validate_atoms.py` already implements it once; the third instance is
cheap because of that.

**Collision to resolve with it.** `element_id` is described as "**the single** join key across the
object graph, every locale pack, the registries, and the learner model" — which is verbatim the job
`atom_id` performs in the harness. Two ids cannot both be *the* join key. Most likely resolution:
`atom_id` joins meaning, structure and governance; `element_id` joins presentation, locale packs and
the learner model; `composed_from` is the bridge. Not settled.

Note also that `expression` means **different things** in the two schemas — element's is the
primitive registry keys (`text_primitive`, `motion_primitive`, `layout_primitive`,
`interaction_primitive`, `style_ref`); atom's is `content_type` / `register` / `term_refs`. Once the
layers are declared this stops being a conflict and becomes correct: element's is expression-layer,
atom's is source-side. Until then it is a live ambiguity.

### What "complete the generalized core" now means, concretely

Not vague. `STRUCTURE.md` already names the unbuilt transforms, and the survey confirms them:

- `tools/realize.py` — primitives → elements. **Absent.**
- `tools/render/` — element → HTML → PNG. **Directory exists and is empty.**
- **atom → primitives has no listed transform at all** — the first hop of the chain is not scaffolded.
- plus the `composed_from` join above.

Also confirmed by survey: **no store anywhere carries an `intent`, `expression`, `audience` or
`render` binding** — only `object`, `procedure`, `form`, `instance`. Four of six facets have never
been exercised, only Headwater has ever written, `agents/cartographer/` does not exist, and
`reference/brunswick.reference.course.json` is `{"_todo": ...}` — the gold-standard course cited by
the project's own pointers has never existed. **The ALSAP vertical is deep and green; the course half
of the machine has never run.**

### Smaller drift found in the same survey

- `trainstorm-core/registry/` holds `roles.registry.json` (4 entries) and `records.registry.json`
  (1) while `astellas/registry/` holds 14 and 5. The 2026-08-13 tiering decision put the *pattern* in
  shared core and the *entries* at the client tier; core carrying entries is either seed data or
  drift, and is not labelled either way.
- `trainstorm-core/project/ast_alsap/review_matrix.csv` is a stray store fragment inside the folder
  reserved for Claude Project setup. Misfiled by `STRUCTURE.md`'s own one rule.
- `cgen/astellas/` is a **third sibling** under `cgen/` that `STRUCTURE.md` does not acknowledge, and
  it sits in tension with that doc's "a client's actual course → not here." The 2026-08-19 entry
  chose the namespace deliberately; the structure doc never caught up. Client *courses* go to a
  separate repo; client *document stores and registries* apparently live here. Worth stating
  explicitly rather than leaving as an undocumented exception.

## 2026-08-20 (fifth) — ID intake vs STAKEHOLDER intake: the manifold serves two orders, and today's "blocked" finding belongs to the second

*Jake's distinction, drawn after the dispatch. It corrects the framing of the 08-20 (fourth) entry
rather than its facts, and per this log's convention that entry is left standing — the correction is
here. No code changed; this is a scoping decision, and it moves a large piece of work off the build
queue entirely.*

**Two orders of intake, which had been collapsed into one.**

1. **ID intake (first order).** An instructional designer takes a client corpus — SOP-AST-29080,
   FORM-AST-34037 — and converts it into an expression layer. Here the expression is an *agent*
   rather than a course, but the shape is ordinary ID work. **Everything in the manifold today is
   this.**
2. **Stakeholder intake (second order).** The artefact produced by the first order is *itself an
   intake surface*. Amanuensis, operated by the ALSAP Lead, consumes asset evidence — IB, DRMP,
   SFDG — which is **theirs, not the ID's**, and which arrives at **their runtime**, not at the
   engine's design time.

**Why this had to be named: the arc was bolted on.** Jake's account is that the ALSAP work became an
ambitious stretch goal around a live need, and it is not native to the manifold's design. That is why
it kept not-quite-fitting. The manifold had no concept of *an expression that is itself an intake
surface for someone else*, so second-order requirements kept presenting as first-order gaps.

### What this reclassifies

**The 08-20 (fourth) finding is a success, not a blocker.** Seven agents were handed a slot with no
asset evidence and every one refused to fabricate. That is precisely the state the delivered product
is in *before its operator loads their data*. The engine was behaving correctly in its shipping
state; it was not failing to work. "Draft mode is **blocked**" was the wrong word — the correct one
is "draft mode **awaits stakeholder intake**." The facts of that entry stand; only the diagnosis of
whose problem it is changes.

**A hard constraint follows, and it is a good one.** Unblinded safety data is not an instructional
designer's to hold, and Jake may never be permitted to have the asset corpus. **The engine must
therefore be deliverable, demonstrable and testable without it — permanently.** That is not a
temporary state of the beta. It is a property the architecture has to keep.

**A large piece of work leaves the build queue.** The two-layer source-atoms-plus-claims design
sketched earlier this session is *second-order*. It is not Jake's to build; at most it is a reference
implementation a stakeholder could adopt. This also removes the ontology-project risk flagged
against it — the datum-versus-interpretation line does not have to be drawn by us.

### The real design object is the SOCKET, not the corpus

What ships is a self-contained authoring apparatus — template atoms, procedure atoms, the agent
prompt, `resolve_slot.py`, `resolve_prompt.py`, the gate, `accept_value.py`, `project_alsap.py` —
plus a **declared intake contract**: *to author this document you must supply these kinds of
evidence.*

**That contract is fully specifiable from what we already hold, with no asset data at all**, because
the template's slots enumerate the demand: `[Include # here]` demands a participant count,
`[list of the most prevalent adverse events]` demands an AE list, `reg_benefit_risk_profile` demands
an SMT position. The `sufficiency` block added to the packet earlier today is a crude first version
of exactly this — it currently *warns* that evidence is absent. Promoted to a **specification** it
becomes the artefact handed to the stakeholder, and the thing their own ingest is validated against.
This is buildable now and needs nothing we do not have.

### The recursion generalizes

Not an ALSAP quirk. Every agent produced by ID intake has its own stakeholder intake — a
course-authoring agent needs the SME's content; a localization agent needs the TM and glossary. So
**"an agent render declares its runtime intake requirements" belongs in the agent operating-package
as a first-class part**, not as an ALSAP special case. *Candidate home:* the 2026-08-10 entry left
`06` and `10` unassigned in the package layout, to be normalized "when their contents are known."
An intake contract is a plausible occupant. Not decided.

### Open — the commercial fork, held deliberately

**How rich is the socket?** A thin contract ("supply these values") ships fast and works, but
maintenance degrades to re-checking everything on every revision. A rich one (evidence arrives as
governed, hash-bearing atoms) buys the two-hop staleness walk — source moves → claims citing it go
stale → expressions citing those claims go stale — but imposes structure on a stakeholder who may
simply hand over a spreadsheet. **The gradient is a product decision more than a technical one**, and
it is where the question of whether Trainstorm sells the engine or operates it gets answered. Held,
not settled.

### Correction to carry forward

`derived_from` does **not** exist in `atom.schema.json`. `governance` is `additionalProperties: false`
with exactly `version`, `status`, `regulatory_binding`, `owner`, `approved_by`, `effective_date`.
The 08-20 and 08-20 (later) entries both assert provenance lives in "`governance` (owner,
`derived_from`)"; that is wrong and was checked rather than assumed. It matters the moment citation
becomes load-bearing, because a citation is a **live graph edge** a maintenance walk traverses — not
audit provenance — so it belongs in a binding, not in `governance` and not in an external sidecar.

## 2026-08-20 (fourth) — Prompt resolver built; Amanuensis DISPATCHED for the first time. Finding: the packet grounds a slot but carries no asset evidence, so the agent can review but cannot draft

*Anchor: branch `instance-facet`, commit `7d1a5e1`. Three gates PASS/PASS, both self-tests 17/17,
purity PASS, all 7 open slots resolve to a payload. Full dispatch record:
`agents/alsap_builder/07_examples/dispatch_2026-08-20/findings.md`.*

**The rung we had been faking.** The 08-20 (third) entry claimed the slice ran end to end: template
slot → packet → *Amanuensis proposal* → acceptance → instance atom → gate → projection. Every rung
was real except that one — a human read the packet, chose `conditional_favorable` and wrote the
rationale. Amanuensis existed as a prompt and had never been run. Naming that is the point of this
entry: **an unrun agent is a design, not a component**, and the same "the log describes what was
designed, the repo records what ran" rule applies to our own claims about the loop.

### `tools/resolve_prompt.py` — the carry from 2026-08-11, closed

Spine + specialization + walk result → a dispatchable `{system, messages, meta}` payload. Three
things in it are load-bearing:

**It refuses to emit a leaking payload.** `--verify-prompt` *reports*; the resolver *refuses*. Purity
is enforced where the prompt is constructed rather than checked afterwards, which is the difference
between a lint and a gate. The rule itself moved to `tools/prompt_purity.py` and both tools import
it — a second copy of the leak scan would have drifted exactly like a second copy of a schema
(`store_merge.py` precedent).

**Substitution is single-pass, and the reason is a small trap worth remembering.** Amanuensis's
write-contract block *quotes its own slot*: "the spine gained an optional eighth slot,
`{{WRITE_CONTRACT}}`." Sequential `str.replace()` therefore re-injected the token it had just
filled, and the resolver refused its own output. A specialization documenting its own slots is
normal and good; the resolver must not read token names inside a *value* as instructions to
substitute again. One regex pass with a lookup function; slot values are never rescanned.

**Dispatch is deliberately not its job.** The payload is a file, so it is reproducible, diffable, and
something the purity check can run against. How it reaches a model is environment-specific.

### The dispatch, and the finding

Seven runs, each in a fresh context whose entire world was one payload file — no conversation
history, no repo access, one `Read` each, self-reported and corroborated by a tool-use count of 1.

**All five first-round dispatches refused to draft, and converged on one root cause.** The packet
carries template structure, drafting guidance and governing procedure — grounding for *what a slot
requires and who owns it* — and **no evidence at all about the asset being documented.** No safety
data, no adverse-event terms, no participant counts, no asset identity. Every `authorable` slot in an
ALSAP is authored *from asset evidence*, and no asset-dossier corpus exists in the manifold.

**The consequence, which the agent surfaced itself and which is the most useful thing to come out of
this session:**

> **Amanuensis is usable today as a reviewer, not as a drafter.** `check` mode works on template
> grounding alone — dispatched against the real `br_rationale` draft it verified disposition,
> instructional-text leakage, and consistency with the governed `conditional_favorable` selection,
> and returned *pass-with-questions* with the honest caveat that it could confirm form but not
> accuracy. `draft` mode is blocked until an evidence corpus exists.

That asymmetry reframes the near-term product. The reviewer is shippable against what we already
have; the drafter is a corpus away.

**"Flag, never invent" held 7/7.** Not one dispatch papered a gap with plausible prose. The `author`
dispatch declined the tempting inference — refusing to answer "ALSAP Lead" from `accountable` +
`performed_by`, on the grounds that *accountable for a field* is not *the value of the field*. The
`example` dispatch refused to import the `controlled_standard` "Not Applicable" fallback across
dispositions. The `person` field was refused on **PII** grounds, not merely on absent data — and that
one is a real open question: a required `person` field on the ALSAP cover sits directly against
"no PII in a content atom," and needs a governance answer (key into an identity registry, or declare
instance facets a separately-governed tier).

### What the dispatches broke, and what got fixed

**`gaps: []` was answering the wrong question.** It reports whether the *walk resolved everything it
referenced* — an assembly question — and every agent read the empty array as licence to proceed, then
had to work out for itself that the decisive input was missing. Adequacy is a different question and
now has its own field: a `sufficiency` block that states in plain words what the packet carries, what
it does not, and a per-slot verdict. **General lesson: a completeness signal that answers a narrower
question than its name suggests is worse than no signal**, because a downstream reader trusts it.

**A conditional slot was handed its dependency's identity but nothing else** — no field type, no
governed value set, no predicate. "The selected Benefit-Risk profile" had no referent, and the slot
was undraftable no matter how complete its own entry was. Now resolved: the controlling field's type,
its options, and its predicate (with an absent predicate *named* rather than passed as a silent
`null`). This would have hit every conditional slot in the template.

**Nothing showed what had already been authored.** `--instance` adds `instance_so_far` — this slot,
the fields it depends on, the decisions, governance and staleness. **This is what makes `check` mode
work at all**, and it is the packet's first read across the template/instance boundary.

Smaller, all fixed: roles and records arrived as display labels, so the agent could not run the
ungoverned-value drift check its own contract demands (`idlabel()` now carries `{id, label,
governed}`); the governed `disposition_decision` set was absent from the packet, and one agent duly
invented the token `as_is` and flagged it as ungoverned — exactly the right behaviour, and exactly
the input it should not have had to invent; `governance`/version now travel with the slot, so a
binding can record which version of a value set it resolved against.

**Two prompt defects that only running it could expose.** `{{FACET}}` was declared
`*(none — see the write-contract deviation below)*`, which substituted mid-sentence throughout the
spine — "Always: write only *(none — see the write-contract deviation below)*". Two agents flagged it
independently. Fixed to `instance`, plus an explicit clause: **read every "write" in the spine as
"propose"**. And the disposition table had **no row for `controlled_standard` with
`constraints.slots`**, so the agent read the v0.2 named-slot feature as a flat contradiction and
refused the slot entirely. Row added, and the wake condition now covers it. *The v0.2 feature was
unusable by the agent it was built for, and only a dispatch could have shown that.*

**The fixes moved behaviour, measurably.** Re-dispatched on `narrative`, the agent went from *"I may
not touch this at all"* to correctly stating it may draft **only the four named spans** and must
quote the sentence unchanged — then stopped, citing the packet's own `sufficiency` verdict. Its
feedback: *"Unusually good. The `sufficiency` block stated its own insufficiency plainly and
pre-empted the failure mode."*

### Open

- **The asset-evidence corpus.** The next real rung, and now ahead of bulk template decomposition in
  the ordering: decomposing 300 more template atoms does not make one more slot draftable. Shape is
  unsettled — SFDG / IB / DRMP extracts as atoms in a per-asset store, read into the packet the way
  the SOP already is. Whether it is a Headwater ingest, a reference tier, or something else is open.
- **Bulk decomposition** remains unblocked and still wanted; it just no longer looks like the thing
  that unblocks authoring.
- **The `person` field vs no-PII collision** (SME + governance).
- **The ten phrasing atoms** are `instructional_transient` yet appear in the conditional graph as
  `fields_conditional_on_this_slot`, i.e. presented as document content. Two agents flagged the
  contradiction. Guidance that is deleted before final probably should not present as a conditional
  *field*.
- **`f_br_rationale`'s `conditional_on` carries no `equals`** where its ten siblings do. The packet
  now says so out loud; the decomposition still needs the answer.
- Honest limits, restated: dispatch was by subagent, not by API call (no key in the build
  environment); "used no other tool" rests on self-report plus a tool-use count; seven dispatches on
  one vertical is enough to find structural defects and is not a sample.


## 2026-08-20 (third) — `instance` facet built, gated 17/17, proven end to end; four open questions settled; `form.facet` v0.3 closes the positional-slot hole

*Anchor: branch `instance-facet`, commit `44dd1c8`. Three gates PASS/PASS
(`alsap` 31 template atoms · `ast_alsap` 47 · `alsap_asp9999` 10 authored values + 19 decisions),
`selftest_form_gate.py` 17/17, `selftest_instance_gate.py` 17/17, prompt purity PASS.*

**Before anything else — a drift finding that cost this window its first hour.** The hand-off told the
new window to verify against the repo. `origin/main` at `d6cfbd7` had **none** of 08-19-afternoon or
08-20: no `projects/alsap`, no `options.registry.json`, no `resolve_slot`/`store_merge`/
`selftest_form_gate`/`headwater_ingest_form`, no `agents/alsap_builder/`, spine at v0.1, `form.enum`
still in the pre-v0.2 flat shape, and `ast_alsap/atoms.json` still the **2026-08-13 15:50 clobbered
file** (35 atoms, all v1/draft). All four verification commands would have failed. Jake pushed
(`cb0c48c`) and the staged working copy then matched origin **byte-for-byte across all 48 files**.
The 08-19 standing rule said *when the log and the repo disagree, the repo wins* — but the repo can be
**behind**, not just ahead. Sharpened rule: **the working tree is the state; the repo is the state
only once pushed.** A hand-off that says "verify against the repo" must name the commit it expects,
so a stale remote is caught in one step instead of read as "the work was never done."

### The four open questions, settled

**1 · Named slots key ONE ATOM per `(instantiates, fills_slot)`** — not a sub-map on one instance
atom. A sub-map would put several independently authored values under a single `content_hash`, so
revising one blank would stale the others, and per-slot approval would be impossible. `fills_slot` is
omitted when the value fills a whole field. The gate enforces uniqueness on the compound key.

**2 · Instance atoms live in their own PER-ASSET store.** The decisive argument is not "an ALSAP is
per-asset" (true but weak) — it is that **the approval boundary is per-asset**. `approve.py`,
`approvals.json` and `manifest.approval_roles` are all per-store, and template atoms answer to
Astellas document control, a different regime entirely; one store spanning both would run one gate
across two governance regimes. `manifest.instantiates_template` declares `{store, document, version}`
and `harness_paths` gained an optional fourth anchor (`--template` / `TRAINSTORM_TEMPLATE` /
manifest). A project without the key resolves it to `None` and every instance check is skipped, so
both existing stores are untouched.

**The cross-store `instantiates` reference is legal, and this needs saying precisely** because
08-20 (later) recorded "persisting an `atom_id` across a store boundary is forbidden." That rule is
about **direction**, not about boundaries: `instantiates` points **UP** into a shared, governed tier —
the same direction as `role_` / `rec_` / `doc_` / `reg_` ids already point. Sideways (peer project →
peer project) and downward (shared → instance) remain forbidden. *Honest gap:* the ALSAP template has
**not** physically moved into a `shared/` tier yet, because `harness_paths` derives the registry from
`project.parent.parent`, which that move breaks. The manifest indirection makes it a one-line change
later; today the pin points at the sibling `projects/alsap`. **Declared, not done.**

**3 · `disposition_decision` — a governed closed list of four**, in `vocab/instance.enum.json`
(canonical `dimensions.<name>.values[]` shape, mirrored into the facet schema and checked):
`retained` · `modified` · `marked_not_applicable` · `deleted`. What makes it defensible is that the
**legality matrix is read off the template's own rules**, exactly as `content_disposition` was:

| template disposition | legal decisions | atom? |
|---|---|---|
| `controlled_standard` | `retained` · `marked_not_applicable` (FORM_RULE_005) | forbidden |
| `example` | `retained` · `modified` · `deleted` (FORM_RULE_006) | required iff `modified` |
| `instructional_transient` | `deleted` only (FORM_RULE_007) | forbidden |
| `authorable` | **none** — it is *filled*, not *decided* | required |

**Where a decision lives follows from whether it has meaning.** `modified` produces new text, so it
must be carried by an atom; the other three produce none, so they go in an external, atom_id-keyed
`instance_decisions.json` — the same reference-don't-embed move as `reconciliation_log.json` and the
locale packs. One vocabulary, one carrier per case, no ambiguity about which wins.

**4 · Gate extended + `selftest_instance_gate.py` (17/17).** Hard: unresolvable `instantiates`;
`fills_slot` not declared on the template atom; two values on one compound key; a second
`template_version` in one store; an illegal or ungoverned decision; `modified` naming no atom; an atom
and a contradicting decision; wrong `meaning.kind`; an instance atom also carrying a source-type
facet. Soft (hold promotion, allow drafting): `[instance/stale]` and `[instance/incomplete]`.

**A correction the hand-off's own proposal needed.** It specified "an instance atom over a
`controlled_standard` slot is a hard failure." That is right *except* for a declared named slot —
which is the entire reason `constraints.slots` exists. The Safety Profile narrative is
`controlled_standard` and carries four authorable spans. The rule is therefore: **hard failure over
`controlled_standard` UNLESS `fills_slot` names a declared slot.** Left as written, the gate would
have made v0.2's headline feature unusable. *(Still open for the SME: FORM_RULE_005 permits changing
standard text "unless absolutely necessary," and we currently allow no path for that at all —
deviation is modelled as impossible rather than as governed. Deliberate for v0.1; flagged.)*

### `form.facet` v0.3 — naming the slots was necessary but not sufficient

Found while building the projector, and worth recording as a class of error. v0.2 declared slots
"**named, never positional**" and made `(atom_id, slot_id)` the instance key — but a slot carried only
`{id, expects}`, so a *renderer* still had to match the four `[bracketed]` spans to the four declared
ids **by position**. The positional reference had been removed from the key and left in the
rendering. v0.3 adds **`slots[].marker`** — the exact bracketed literal — making substitution a
literal match; the gate requires each marker to occur **exactly once** in `source_text` (hard).
Lesson: *eliminating a positional dependency from the data model does not eliminate it from every
consumer; check where else the ordering was doing work.*

### The property the whole overlay rests on, now asserted

Re-ingesting the template after adding markers reported **REBOUND on exactly one atom** — bindings
changed, meaning intact — so `content_hash` was untouched (`sha256:8aa65df1…` before and after),
`template_source_hash` still matched, and **no instance value went stale** even though the template
atom went v3 → v4. This is the 08-20 two-axes lesson (meaning divergence vs binding divergence)
paying off across the template/instance boundary, and `selftest_instance_gate.py` now asserts it
directly: if it ever fails, every facet correction on a template silently invalidates every ALSAP
written against it.

### The slice, proven

`tools/accept_value.py` is the **only** writer into an instance store — the single-writer contract as
a script a human runs, which is what "the agent proposes, a human accepts" means mechanically. It
refuses in plain words before the write (authoring over retained standard text; authoring into
guidance; an illegal decision), with the gate remaining the authority for hand-edited stores.
`tools/project_alsap.py` resolves the overlay back into a document: 10 authored values over 31 pinned
template atoms render a whole ALSAP in which every word of standard text was resolved at render time
and **exists nowhere in the instance store**. That is the proof the sparse overlay was the right
call — the alternative was N drifting copies of controlled boilerplate.

Worked example: `cgen/astellas/projects/alsap_asp9999` (**ASP9999 is a deliberately fictional asset
code**; the store exists to prove the loop, not to hold a real ALSAP). Benefit-Risk ran the full path:
template slot → `resolve_slot.py` packet (6 governed values, each with its own phrasing guidance,
plus the governing SOP step across the store boundary) → selection of `conditional_favorable` →
`accept_value.py` → gate → projection. The acceptance test has moved as the hand-off predicted: the
old criterion was *"must flag the ungoverned Benefit-Risk vocabulary"*; the gate now enforces
**"select one of the six governed values and never invent a seventh"**, and additionally that the
atom's `meaning.source_text` **is** the chosen id — the option's label and definition live once, in
the options registry, and are resolved live by the projector.

**A side effect worth keeping:** because completeness is computed against the pinned template, the
gate now prints **STILL OWED** — every slot lacking a value and every template atom lacking a
decision. "What does this ALSAP still need?" became a gate output rather than a meeting.

**Open / next.** Physically promote the template into a client-shared tier (needs a `harness_paths`
registry-derivation change). The FORM_RULE_005 deviation path (SME). Then, against a now-validated
loop, **bulk-decompose the remaining template** — eight Heading-1 sections, thirteen of seventeen
tables, the Instructions-for-Use bullets. Unchanged carries: approver count (SME), the
`procedure.facet` duty-attribute bump, the prompt resolver (Amanuensis needs one that inlines a
*walk result*), `agents/cartographer/` still absent, `agents/localize/system.md` still un-`git rm`'d.
New minor: `__pycache__` is neither gitignored nor tracked — one line in `.gitignore`.

## 2026-08-20 (later) — Render target = AGENT: Amanuensis built; spine v0.2; the colour convention resolves disposition; `form.facet` v0.2 named slots

**The arc's actual object now exists.** `agents/alsap_builder/02_system_prompts/core_agent/amanuensis_system_prompt.md`
— a seven-slot specialization on the shared spine, named for a secretary who writes at another's
dictation, which is exactly the relationship. Every prior render projected atoms into a *document*.
This projects atoms into an *agent*: the ALSAP Lead authors, Amanuensis drafts and checks, the gate
and the approval gate govern. Same machine, new render kind.

**Spine v0.2 — an optional eighth slot, `{{WRITE_CONTRACT}}`.** Building Amanuensis exposed that the
spine had been fusing two separable things: the universal **graph discipline** (wake on state, never
call, govern the vocabularies, flag never invent, surface uncertainty, no PII) and the facet-owner
**write contract** ("you are the sole writer of `{{FACET}}`"). Amanuensis needs the first and not the
second — it writes nothing; it proposes, and a human's acceptance plus the gates make it canon. A
specialization that omits the slot inherits the single-writer default verbatim, so all six facet
owners written against v0.1 are byte-for-byte unaffected. The deviation stopped being an exception
and became a slot. *(Pattern worth keeping: when an agent doesn't fit the spine, the question to ask
is "which part of the spine was doing two jobs?", not "what exception does this agent get?")*

**The rule that defines the agent: it does not know the ALSAP — it reads it.** Every fact about the
template arrives in a grounding packet assembled at run time by `tools/resolve_slot.py`. Nothing about
the ALSAP is in the prompt, and nothing may come from the model's training. This is not style: content
in a prompt is a second source of truth that drifts the instant the template is revised, and a
drifting copy of a controlled document is the failure this whole architecture exists to prevent.

**`tools/resolve_slot.py` — the walk.** For one slot it assembles: the field atom (text, `field_type`,
`content_disposition`, `constraints`, `content_hash`); its ancestry via `object.belongs_to`; the
instructional/example guidance under its section; the governed value set behind `options_ref`, with
**each value carrying its own conditional guidance**; `performed_by` resolved to registry labels; the
conditional graph in both directions; and the SOP steps that reference this template. That last one is
the marriage the hand-off was after — *the procedure that governs the build and the template that
shapes the output, meeting in one packet*, joined by `doc_form_ast_34037` across two stores. Empty
sections are reported as `gaps` rather than filled.

**Reading vs persisting across a store boundary.** The packet reads from two project stores. That is
allowed and needs saying once: a packet is **ephemeral context**, so reading across the boundary costs
nothing. *Persisting* an `atom_id` across it is still forbidden. Per-project isolation governs what is
stored, not what may be read into a prompt.

**Acceptance criterion, made runnable.** `resolve_slot.py --verify-prompt <files>` asserts that no
atom's `source_text` appears in the agent's prompt; a hit means the prompt has become a second copy of
the controlled document. Spine + specialization: PASS. Negative control — one template atom pasted
into a copy of the prompt — FAIL, exit 1. Honest limit: it catches verbatim copying, not paraphrase.
Verbatim is the realistic failure (someone pastes template text in "to help the agent"); this is not a
proof of purity.

### The colour convention — an SME question closed by evidence instead of escalation

Jake's read: blue is instructive, green is example. A full run-colour audit confirms it, and the
template proves the convention **against itself** — the three legend entries are written in the
colours they describe:

| legend entry | rendering | paragraphs | governed value |
|---|---|---|---|
| `<STANDARD TEXT>` | black / auto, upright | 97 | `controlled_standard` |
| `<EXAMPLE TEXT>` | green `00B050`, upright | 23 | `example` |
| `<INSTRUCTIONAL TEXT>` | blue `5B9BD5`, **italic** | 89 | `instructional_transient` |
| `[placeholder text]` | blue `5B9BD5`, upright, in brackets | inline | `authorable` |

**Blue does two jobs, split by italics and bracketing:** an italic blue block is instructional prose
to delete; upright blue inside square brackets is a fill-in slot. The template is internally
consistent — the earlier "blue is a fourth ambiguous signal" flag was a **sampling error on our
side**: the Benefit-Risk block is 100% blue italic, and the convention was generalised from it.
The open SME question is withdrawn, not answered.

**Two corrections the audit forced.** (1) The Safety Profile narrative is black standard text carrying
four upright-blue `[ ]` slots — `controlled_standard`, not `example`. (2) The Benefit-Risk "Example
phrasing" lines sit inside the one angle-bracketed blue-italic span, so they are
`instructional_transient` (guidance that is deleted), not `example` (candidate text the author may
retain). **The label says example; the colour says instructional; the colour is the governed signal.**
Standing rule: where a template's prose label and its own typographic convention disagree, the
convention wins, because it is the machine-checkable one.

**Example phrasings — section wrapper.** Ten phrasing atoms under a `form_section` wrapper,
`conditional_on` the specific Benefit-Risk value each serves. They are siblings-in-a-section rather
than children of `br_rationale` because a `form_field` leaf with children would break the
containers-vs-leaves rule the gate enforces. `other_smt_defined` carries none — the SMT defines it;
absence is information, not a gap. Store: **31 atoms**.

### The merge was committing the violation it was built to prevent

Correcting one `content_disposition` should have been a one-line change. It was not, and the reason is
load-bearing: **`content_hash` covers MEANING only**, so a facet re-binding with unchanged text
produces an identical hash — and the merge keyed its entire decision on that hash. *Every binding
correction would have been silently dropped on re-ingest.* Worse, the naive fix (always take the
authored bindings) would have erased other facet owners' work the moment Cartographer wrote `intent`.

Fixed: bindings merge **key by key**, and each ingest script declares what it owns
(`owns=("object","procedure")` / `owns=("object","form")`). Owned keys come from the authored
decomposition; every other key is preserved from the store. A binding-only change is reported as
**REBOUND**, bumps `version`, resets `status` to `draft` and clears approvals — a facet change on a
controlled document needs re-review. Proven with an atom seeded with a foreign `intent` binding and
`approved` status: the foreign binding survived, the owned binding updated, v1→v2, approvals cleared.

**The general lesson: meaning divergence and binding divergence are different axes.** Meaning
divergence is *ambiguous* (SME or corpus?) and needs `ingest_log.json` to resolve. A binding change is
*unambiguous*, because exactly one writer owns each key. One hash cannot arbitrate both.

### `form.facet` v0.2 — named slots for mixed disposition

A sentence of retained standard text containing `[bracketed]` authorable spans has genuinely mixed
disposition, and the facet carries one value per field. Resolved with `constraints.slots`:
`[{id, expects, options_ref?}]`.

**Named, never positional.** Under the instance overlay each blank is filled per asset; anonymous
blanks would force the overlay to say "slot 2 of atom X", a positional reference into a string that
shifts the moment anyone edits the sentence — precisely what stable ids exist to eliminate. Naming
them makes `(atom_id, slot_id)` a compound stable key while the sentence stays whole and renderable.
**Deliberately no `field_type` on a slot:** repeating that closed list inside the facet would spawn
the drifting second copy the mirror check exists to catch. `options_ref` is fine — a pattern, not an
enum.

Both facet schemas now carry a **`facet_version`** field (`form.v0.2`, `procedure.v0.1`), so the
"version bump" language the log has used since 2026-08-13 finally denotes something in the file.
`procedure.facet` is stamped and ready for its pending duty-attribute bump.

**Gate + self-test.** New soft flag `[form/slots]`: a field with bracketed spans and no matching
declared slots reports and **holds promotion** without blocking draft (square brackets have other
uses). Self-test now **16/16**, adding a slot with no `expects`, a slot id that is not a stable name,
and the soft-flag case. Also fixed while demoing: option-scoped guidance was leaking into sibling
slots as ambient section noise; it now rides only with its own option (narrative slot: 13 guidance
atoms → 3).

### Sequencing decision — `instance` facet BEFORE bulk template decomposition

Jake's preference was to shore everything up; the dependency ordering argues otherwise and he took
the recommendation. **Template completeness unblocks nothing until the `instance` facet exists** —
all 229 paragraphs and 17 tables could be decomposed and still not permit a single authored ALSAP,
because authored content would have nowhere to live. And the cost of bulk work ahead of a validated
loop is already evidenced: the 9-atom fragment modelled `br_profile` as `controlled_standard` and the
real document overturned it. The same class of error across 300 atoms is expensive.

Order: **`instance` facet → prove one slot end to end (template slot → Amanuensis proposal → human
acceptance → instance atom → gate → projection) → then bulk-decompose against a known-good loop.** A
cheap middle path if shoring up is wanted sooner: decompose *structure only* for the remaining
sections (containers and hierarchy, no `form_field` leaves) — roughly 30 atoms, almost no judgment
calls, deferring every field-level decision.

**Open.** The `instance` facet itself (proposed, not gated — and it is what Amanuensis proposes
*into*). The approver-count discrepancy (still genuinely SME: two signature blocks vs three named
approver roles). Eight Heading-1 sections and thirteen of seventeen tables. The Instructions-for-Use
bullets, flagged as a list, not smashed.

## 2026-08-20 — Form side of the gate closed (13/13 self-test); FORM-AST-34037 vertical ingested into `projects/alsap`; options registry tier added

**The gate now covers both source types.** `validate_atoms.py` loads `form.facet.schema.json` and
validates `bindings.form`, which previously passed **unchecked** — silent, and therefore worse than
failing. Added with it: `form_field` leaves must carry a `field_type` and containers must not;
`conditional_on` must resolve to a real atom; `options_ref` / `captures_record` / `performed_by` run
through the same invent-guard as the procedure side; and an atom must carry **exactly one**
source-type facet, since a procedure *produces* a record and a form *is* that record's template —
merging them into one atom collapses the duality. A `form_field` with no `content_disposition` is a
HARD failure, not a flag: it is the line between reused controlled text and asset-specific authored
text, so an atom that cannot state which it is leaves an authoring agent unable to tell what it may
touch. A container may declare a disposition (an instructional block that must be deleted); optional
there, but governed if present.

**Two anti-drift checks that had no owner.** (1) **Mirror conformance** — both facet schemas inline
enums their vocab files *declare* to be mirrors, and nothing was asserting it. The gate now checks
`schema enum == vocab ids` for `step_type`, `field_type`, `content_disposition`. This is the
2026-08-13 vendored-schema incident converted from an accident into a check. (2) **Vocab shape** — a
vocab file that is present but is NOT in the canonical `dimensions.<name>.values[]` shape is now a
hard failure rather than a silent skip: govern-the-vocabularies applied reflexively to the
vocabulary files themselves.

**`form.enum.json` normalised (form.v0.1 → v0.2).** It used a top-level
`{kinds, field_type, content_disposition}` layout — it predates the 08-13 lesson that established
the canonical shape, and because nothing read it, nothing had noticed. The `structure.enum` union
code would have `KeyError`'d on it. Ids, labels and definitions unchanged; three ad-hoc loaders
replaced by one `govset()` helper, so a new vocab file is one line rather than a new parser.

**A gate is only worth its green light if it is known to go red.** `tools/selftest_form_gate.py`
drives the gate against deliberately broken copies of the worked fragment and asserts each is
rejected with the expected verdict tag — 13 cases including a positive control, the invent-guard,
and two that mutate a **copy** of core to prove the mirror and shape checks bite. Run it with
`python3 tools/selftest_form_gate.py`.

**Load-bearing finding — the template declares its own disposition convention.** FORM-AST-34037's
"Understanding Template Text Types" spells out four markers, and they land *exactly* on the four
governed `content_disposition` ids that were derived independently from FORM_RULE_005/006/007:

| Template marker | governed value |
|---|---|
| `<STANDARD TEXT>` — "remain unchanged unless absolutely necessary" | `controlled_standard` |
| `<EXAMPLE TEXT>` — "used as-is, modified, or deleted" | `example` |
| `<instructional text>` — italic, angle brackets, "delete once complete" | `instructional_transient` |
| `[placeholder text]` — "customize for the specific study or asset" | `authorable` |

Disposition is therefore **read off the source, not guessed at** — the markers are typographic and
checkable. This is the strongest validation the form facet has received, and it is what makes an
authored decomposition defensible to a GxP reviewer rather than a matter of taste.

**Benefit-Risk resolved from source — closes the 2026-08-10 carry.** The template says *"Choose from
the options below to document the SMT's assessment"* — a **controlled value set**, not example
wording. Six values, each with a Definition and an Implication: `favorable` · `unfavorable` ·
`uncertain_inconclusive` · `conditional_favorable` · `contextual` · `other_smt_defined`. Exactly the
six the form object model guessed a fortnight ago, now sourced. `other_smt_defined` being an open
escape is precisely why the decomposed `select_one` + conditional `text_long` rationale is correct.

**New registry tier — controlled value sets.** `cgen/astellas/registry/options.registry.json`, same
client tier and governance pattern as roles/records/docs, holding the `reg_` ids behind
`form.options_ref`. Its entries carry a nested `values` array the others don't, because an options
entry is a **set**, not an item — a deliberate shape difference, documented in the file. Seeded
empty at v1, then `reg_benefit_risk_profile` adopted into it (v2). `adopt_registries.py` now (a)
handles `options`, (b) **refuses to conjure a governed registry as a side effect** — establishing a
vocabulary is its own deliberate act — and (c) promotes `description` and `values` when the proposal
supplies them. (c) was a latent bug: adoption promoted only `id` + `label`, so every role or record
adopted from here on would have landed without the `description` the v3 shape requires.

**`tools/store_merge.py` — the merge rule extracted before it could be copied.** A second ingest
script would have meant copy-pasting the idempotent-merge rule, and a copied rule drifts. Both
`headwater_ingest.py` and `headwater_ingest_form.py` now import it. Regression: re-running the SOP
ingest produced a **byte-identical** `atoms.json` (same md5), `0 minted / 0 updated / 2 preserved`.

**Store state.** `cgen/astellas/projects/alsap` — 20 atoms (1 `form`, 6 `form_section`,
13 `form_field`): cover block, approval block, version history, and Purpose → Safety Profile Summary
→ Benefit-Risk. **GATE PASS / PROMOTE PASS**, no flags. `ast_alsap` unchanged at 47 atoms, green.
Both halves of the builder's grounding — SOP procedure atoms and FORM template atoms — are now in
the store, joined by shared `role_` / `rec_` / `doc_` ids.

**Correction the real document forced.** The worked fragment had `br_profile` as
`controlled_standard`; the template disagrees — the SMT's assessment is chosen and written by the
author, so it is `authorable`. The fragment was built from a bundle summary, not the controlled doc.
General lesson: a fragment authored from a summary is a *hypothesis*, and the source is the test.

**A test pinned to a real id rots when governance moves.** Immediately after adoption the self-test
went 12/13: the invent-guard case asserted `reg_benefit_risk_profile` is rejected when unproposed,
which stopped being true the moment it was governed. Fixed by testing the RULE with a synthetic
`reg_selftest_never_governed`, plus a companion case asserting the adopted set passes with no
proposal. Back to 13/13. Standing rule: **self-tests assert rules, never the current contents of a
governed list.**

### The three lifecycles (conceptual clarification, worked out with Jake this session)

A near-miss worth recording because it will recur. `content_disposition` is **permission**, not
provenance: every one of its four values describes text that came from the uploaded corpus, and
`authorable` means "a slot an author may fill", not "an SME wrote this". Provenance lives elsewhere
— `governance` (owner, `derived_from`), `ingest_log.json`, `reconciliation_log.json`. And agent
scope is neither: it is **single-writer per facet**.

Nor does authored content ever graduate into `controlled_standard`. Three lifecycles run in
parallel and interact only by reference and by evidence, never by one turning into another:

1. **Template** — FORM-AST-34037, versioned and approved by Astellas document control.
2. **Instance** — the ALSAP for a given asset; drafted, reviewed, approved per asset. Points at the
   template; never becomes it.
3. **Vocabulary** — propose in the project store → adopt UP into the governed client registry, with
   the gate blocking promotion in between. This *is* a genuine pre-prod → prod promotion, and it is
   the one Jake's "enforced versioning" instinct was correctly reaching for.

The manifold's contribution to (1): because instance atoms are keyed to template slots, "every ALSAP
authors near-identical text into slot 4.2" becomes a **queryable** signal that slot 4.2 should be
`controlled_standard` in the next template revision. That is a promotion, but a deliberate act of
document control informed by evidence — not an automatic graduation.

**Open from this pass.** For the SME: the approval table provides one *Prepared by* and TWO
*Approved by* blocks while SOP-AST-29080 names THREE approver roles (GSO, Medical Lead, ALSAP Lead —
and `role_alsap_approver`'s own registry description reads "Minimum: GSO, Medical Lead, ALSAP Lead");
fixed-at-two or repeatable is not stated, and is modelled as two fixed slots each carrying all three
candidate roles. Also for the SME: **blue text** (`5B9BD5`) is a fourth signal the template describes
as "optional or placeholder content" but which does not map cleanly onto one governed disposition;
the Safety Profile narrative is blue, non-italic, with `[placeholders]`, modelled as `example`.
Design-side: **per-option example phrasing** has no governed home (registry entries are
`{id,label,description}`; the phrasings are not content atoms either). Deferred scope: eight
Heading-1 sections, thirteen of seventeen tables, and the Instructions-for-Use bullets (flagged as a
list, not smashed). Then the arc's actual object: the **ALSAP-builder specialization**.

## 2026-08-19 — Re-ingest made idempotent (the 08-13 clobber, diagnosed and fixed); ALSAP store restored to 47 atoms with lifecycle intact

**The defect.** `tools/headwater_ingest.py` rewrote `atoms.json` unconditionally — every atom minted
fresh at `version: 1`, `status: draft`. Any downstream lifecycle state (reconcile's version bump +
`in_review`, approval's `approved_by`/`effective_date`) was destroyed on re-run. This is not
hypothetical: `reconciliation_log.json` was written **2026-08-13 15:00** with two real SME events;
`atoms.json` was rewritten **15:50**, fifty minutes later, resetting all 35 atoms to v1/draft. The
external audit log survived only because it is external — reference-don't-embed paying off in a way
nobody designed for, while simultaneously demonstrating the hazard (an audit trail pointing at hashes
no longer in the store).

**Why hashes alone can't fix it.** "The SME advanced this atom" and "the source corpus changed" both
present as `store_hash != authored_hash`. The script cannot distinguish them from the store. So ingest
now records what **it** authored each run in an external, atom_id-keyed sidecar
`ingest_log.json` — same move as `reconciliation_log.json`, and for the same reason: `atom.schema.json`
is `additionalProperties: false` at the top level *and* inside `governance`, so there is no native home
for an ingest-provenance field. (Contrast: approval DOES have a native governance home. The pattern
holds — provenance that governance has no field for goes external and keyed.)

**The merge rule (now in `headwater_ingest.py`):**

| condition | outcome |
|---|---|
| authored text unchanged since last ingest | **STORE WINS** — divergence came from downstream; atom untouched |
| authored text changed | **INGEST WINS** — corpus/authoring moved: new meaning, version bumped from the store, status reset to `draft`, approvals cleared (meaning changed, so prior sign-off no longer covers this content) |
| `atom_id` absent from the store | **MINT** at v1/draft |
| in the store but no longer authored | **ORPHAN** — kept and reported; `--prune` to remove (never silent) |

Bootstrap (no `ingest_log.json` yet) seeds the authored map from the existing store and says so on
stdout — stated loudly rather than assumed silently.

**Restoration, in order.** (1) Ingest re-run: 12 minted (the `list`/`list_item` decomposition), 2
updated (`_scope`, `_general` — their embedded lists were extracted, so meaning genuinely changed →
v2/draft), 0 removed. (2) The two 2026-08-13 reconcile events replayed from the log's `text_after`
through the real `reconcile.py` via `review_matrix.replay.csv`; **both landed on the exact recorded
`to_hash`** (`b24f0616…`, `584a252b…`). The original events are retained and the replay appended — an
audit trail is added to, never rewritten. (3) Gate green.

**Acceptance test — the fix proven, not asserted.** Ingest re-run *over the reconciled store*:
`0 minted, 0 updated, 2 preserved (downstream advanced), 0 orphan`. Both SME edits survived at
v2/`in_review` with hashes matching the log. That is the property the ALSAP builder depends on.

**Store state now:** 47 atoms — 10 `procedure` + 2 `list` + 10 `list_item` + 25 `procedure_step`;
versions {v1: 45, v2: 2}; statuses `draft` + `in_review`. GATE PASS / PROMOTE PASS, 0 hard failures,
0 soft flags. `manifest.json` now carries `approval_roles`, so `approve.py` can run against this store
for the first time. **This is also the first time `structure.enum.json` is load-bearing** — the
validator's vocab union now governs kinds the store actually uses.

**Standing rule — files over log.** The 08-13 entries described what was *designed*; the repo records
what *ran*. Reconcile and approval were built and demonstrated, but not against this store; the
"47 atoms, gate green" claim was never true of `cgen/astellas`. When the log and the repo disagree, the
repo wins. Log entries that assert a file's state must cite the anchor (path + commit or mtime, hashes
where they matter) so the next window verifies in one step instead of trusting prose. Same instinct as
`source_hash` on a facet, applied to our own working memory.

### ALSAP-builder decisions taken this session (the new arc)

- **Canonical source: the manifold atoms.** The ad-hoc Copilot-assisted ALSAP becomes a feeder corpus,
  not a rival truth. Document-of-record cutover is **deferred** until the projection is trusted by GxP
  reviewers — atoms are the engineering source of truth immediately, the controlled doc flips later.
- **Namespace: `cgen/astellas/projects/alsap`**, sibling to `ast_alsap`, sharing the client registries.
- **SOP-AST-29080 promotes UP to Astellas client-shared content**, referenced by both projects. Note
  this is a *new* use of the promote-UP path: it has carried registry entries before, never content.
- **Template → instance (PROPOSED, not gated).** An authored ALSAP instance is a **sparse overlay of
  authored atoms over a pinned template**, never a filled-in copy. `content_disposition` becomes the
  structural rule: `controlled_standard` stays in the template and resolves at render time;
  `authorable` mints a real instance atom (it carries *new* meaning, and meaning only ever embeds in
  atoms); `example`/`instructional_transient` become a governed per-instance keep/delete decision, never
  copied text. Structurally this is the locale-pack move on a third axis — the difference being that a
  translation carries the *same* meaning (so it lives outside the store) while an authored slot carries
  new meaning (so it must be an atom). Proposed binding: a small new **`instance` facet**
  (`instantiates`, `template_version`, `template_source_hash`, `disposition_decision`) rather than
  extending `form` — **the writer boundary forces the facet boundary** (`form` is Headwater's on a
  template drop; the instance is the ALSAP Lead's, and two writers on one facet breaks single-writer).
  Staleness then comes free: a template revision changes its `content_hash`, and one walk over
  `template_source_hash` names every stale instance.
- **The acceptance criterion for render-as-agent.** If ALSAP content ends up *in the builder's prompt*,
  we have spawned a second source of truth that drifts the moment the form is revised. The prompt stays
  thin and stable (spine + seven slots); the grounding is a walk resolved per slot at run time. The
  agent does not know the ALSAP — it reads it. Checkable, not aspirational.

**Open / next.** The gate is still procedure-only in two places: `gov_kinds` unions procedure ∪
structure but **not `form.enum.json`** (so `form`/`form_section`/`form_field` hard-fail), and only
`procedure.facet.schema.json` is loaded — there is **no validator for `bindings.form`**, which would
pass unchecked (worse than failing, because it is silent). So the "prove wide (a form)" carry is a
validator extension, not just a vocab addition, and it blocks step 2 of the builder slice. Also:
`_core_adds/` is a second potential home for canon-shaped vocab (precedence protects reads, but a stale
copy there is the next drift — delete any `structure.enum.json` sitting in one); `cgen/trainstorm-core/decision-log.md`
is a stale duplicated accretion of this log (repeated whole-document appends, missing the newest
entries) and should be deleted or replaced by a one-way export; `agents/cartographer/` does not exist
despite the 08-12 entry listing it as built; `agents/localize/system.md` is still un-`git rm`'d.

## 2026-08-13 — Harness is repo-native (shared path resolver) + `list`/`list_item` shared-core vocab (carry closed)

**Repo-native tools.** All harness tools now resolve paths through `tools/harness_paths.py` instead of
hardcoding them. Three anchors — **core** (schemas+vocab), the **client registry**, the **project store** —
each via flag / env var / auto-detect. In the repo (tools in `cgen/trainstorm-core/tools/`): core is
auto-detected (tools' parent), the registry auto-derives from the project (`astellas/projects/<proj>` →
`astellas/registry`), so you pass only `--project`. Standalone: zero-config (fenced `_core_mirror` + package
store, with the mirror warning). Verified green against a simulated three-home repo tree *and* standalone.
`approve.py` forwards the anchors to its gate subprocess.

**`list` / `list_item` — shared-core structural vocab (the flagged carry, now done).** New
`cgen/trainstorm-core/vocab/structure.enum.json` governs the universal `meaning.kind`s `list` + `list_item`
— **source-agnostic**, so NOT in `procedure.enum` (forms and courses have lists too). Same
`dimensions.<name>.values[].id` shape + governance as `procedure.enum.json`. The validator now **unions**
governed kinds across vocab files (procedure ∪ structure), gracefully if `structure.enum.json` is absent.
The two ALSAP front-matter lists (6 in-scope orgs; 4 governing docs) are **decomposed** into a List
container + ListItem children (was flagged-not-smashed); `project_sop.py` renders them as `<ul>`. Store is
now **47 atoms** (10 procedure containers + 2 `list` + 10 `list_item` + 25 steps); gate green.

**Frontend kicked off (separate window):** `claude/handoff-frontend.md` — a basic frontend as a
concept-cementing lens over the same store (read-only atom-graph viewer first). **Remaining near-term
carries:** the **duty-attribute** facet bump (needs a `procedure.facet` version bump); prove **wide** (a
form through the same machine).

## 2026-08-13 — Drift caught + fixed: vendored schema copies overwrote core canon; recurrence guard added

**What happened.** The beta harness package carried convenience *copies* of three core-canon files.
When the package landed in the repo (commit `c6ad256`), a thin `atom.schema.json` (missing the `intent`
and `expression` binding definitions) and a flat `procedure.enum.json` overwrote the canonical originals
— the exact "second copy of a canonical source" drift the manifold exists to kill, hit for real. Caught
during the "verify vendored schemas vs live" carry, when the files Jake pulled back turned out to be my
own vendored copies (circular check), so the true canon was pulled from the synced-repo knowledge instead.

**Fixed in the repo** by per-file `git restore`: `atom.schema.json` from `0bc0097` (its original canonical
commit — a clean two-commit history, so a pristine revert), `procedure.enum.json` from `05211ed` (its
birth commit; it didn't exist at `0bc0097`, hence separate sources). Live files are canonical again.

**What the real files taught us:** the canonical `procedure.enum.json` is NOT a flat
`{meaning_kinds, step_type}` — it nests governed values under `dimensions.<name>.values[].id` as
`{id, label, definition}` objects, with `vocabulary_version` + `governance` metadata. The harness validator
now parses that shape. And the canonical `atom.schema.json` defines all four bindings — `object`, `intent`,
`expression`, `audience` — with real constraints (`bloom` enum, `^obj_`/`^term_` patterns) my copy had dropped.

**Recurrence guard (harness package).** No committable copy of core canon sits next to the tools anymore.
The core files live in a fenced `_core_mirror/` (byte-identical, marked `DO_NOT_COMMIT_TO_CORE.md`), used
only for standalone runs. `validate_atoms.py` reads canon via `--core-dir`/resolver; without it, warns and
uses the mirror. Structural fix — nothing canon-shaped next to the tools to clobber.

**Standing rule:** schemas/vocab have exactly one home (`cgen/trainstorm-core`); tools read them from
there; any mirror syncs **one-way** (core → mirror), never the reverse.

## 2026-08-13 — Approval / publish gate built — controlled-document lifecycle complete (draft → in_review → approved)

`tools/approve.py` — the pre-publish QA gate, the one place canon says sequencing MUST be enforced.
Two hard preconditions: **(1) authorized approver** — the approver id must be a governed member of the
project's `approval_roles` (new field in `manifest.json`; for ALSAP = `role_alsap_approver` / `role_gso`
/ `role_medical_lead` / `role_alsap_lead`); **(2) publishable state** — the standing gate must read GATE
PASS *and* PROMOTE PASS (no hard failures, no pending vocab). Teeth demonstrated: `role_safety_programmer`
sign-off REFUSED; `role_alsap_approver` APPROVED.

**Clean architectural contrast with reconcile.** The approval *outcome* has a **native home in
`governance`** — `status: approved`, `approved_by`, `effective_date` are exactly those fields — so it
writes into the atom, no side-store needed. (Reconcile's provenance was homeless → external log; approval
is the opposite case.) Approval does **not** change `meaning`, so `content_hash`/`version` are untouched:
an unchanged hash proves the approved content is the same content that was validated.

**Signed snapshot (Part-11 flavor).** An external `approvals.json` binds approver + `effective_date` to
the exact `content_hash` of every atom approved. External + keyed, same pattern as `reconciliation_log.json`.
The projection header now renders `Status: APPROVED · effective <date> · Approved by <role label>` from the
store + approvals.json. **This closes the vertical:** corpus → atoms → gate → projection → reconcile →
approval, end to end.

## 2026-08-13 — Carry (FRONTIER): the tutor learner-profile loop is a working prototype of the Response-Engine per-learner join

Surfaced by Jake mid-harness as a "side note." The pattern used to maintain *his own* tutor
learner-profile is structurally the **Response Engine's core loop**, run on a population of one (him,
fully consented). Content side: thin atoms, meaning embedded, everything else referenced, resolved
per-learner at render time. Learner side: a thin, living profile, updated by a growth loop, loaded into
context at course start — which **is** atom-spec §5 step 4 (the join, where `audience` fit-hooks meet the
learner model at render time). The tutor is **Chameleon-for-one**.

**Invariant lines this tests hardest:** *reference, don't embed* (profile lives in the separately-governed
learner model, keyed by employee id, joined at load — never embedded in content); *no PII in content*.
**New boundary — the PII governance TIER:** a profile rich enough to be useful is heavy PII; split into
(a) fit-hooks + learning prefs (lighter) and (b) deep affective modeling (consent/scope/access control).

**Status: carry, FRONTIER.** Response Engine / Orchestrator = a separate project, walled off. Sibling to
the Chameleon `audience` stub and the affective/narrative-arc carry. Seed captured; not to build near-term.

## 2026-08-13 — Reconcile round-trip built (loop now bidirectional) + registries enriched to v3

The one-directional loop (atoms → projection) is now a **round-trip**: projection → SME markup → back to
canon. Projection #2 = a **review matrix** (`review_matrix.csv`, one row per step, empty
`proposed_source_text` column). The SME fills it; `reconcile.py` folds edits back into canon **matched by
`atom_id`** — updates `meaning.source_text`, recomputes `content_hash`, bumps `version`, sets status
`in_review`. Deterministic, id-matched. Answers the open v1 HITL question.

**Honest finding — governance has no home for review provenance** (`additionalProperties:false`). So the
audit trail lives in an **external `reconciliation_log.json`, keyed by atom_id** — the same reference-don't-
embed move as locale packs. (Contrast: approval DOES have a native governance home.) **Cross-check:**
`reconcile.py` recomputes `content_hash` independently of `validate_atoms.py` and they agree.

**Registries enriched to v3 — `{id, label, description}`** (docs also `source_number`). The `label` is
load-bearing: the projection **VLOOKUPs the id → label**. The projector reads labels from the **governed
registry** (the law), not the staging pen; `adopt_registries.py` **promotes `id` + `label`** and drops the
review-only `note`; `registry_adds/*.add.json` emit FULL entries. Loaders: `set(reg["roles"])` →
`{e["id"] for e in reg["roles"]}`.

## 2026-08-13 — Piece 2 beta harness: thinnest end-to-end slice built + validated (SOP-AST-29080 / ALSAP)

**raw corpus → atoms → validation gate → deterministic projection**, run end to end on a live Astellas
SOP. Gate green; a controlled HTML doc a GxP reviewer can react to, every clause tracing to `atom_id` +
`content_hash`.

**Settled:** atom store = git-native JSON in a per-project namespace; a *walk* is a filter over the store
(no DB for beta). Gate policy = schema + drift + vocab-conformance; HARD failures block at any status,
PROPOSED-pending pass at draft but block promotion until adopted; **"flag, never invent" is a gate verdict.**
Router run by hand for v1.

**Load-bearing finding — cited controlled docs are GOVERNED references, not free text** (`^(doc|atom)_`);
raw doc numbers → `doc_` ids governed by a client-level **`doc_` registry**. **Registry tiers:** governance
*pattern* = shared core; *entries* at the lowest level still reused without forking (universal vocab →
core; client roles/records/docs → Astellas namespace). Proposals **stage** in the project store then
**promote UP** into the client registry; staging pen **dropped** (no shadow copy).

**Decision — Safety Programmer Developer vs. Validator → ONE role + a per-step `duty` attribute** (needs a
`procedure.facet` version bump). **Carries:** duty-attribute bump; prove wide (a form); `list`/`list_item`
(now DONE — see top entry); schema verification vs live (DONE — see drift-fix entry).

## 2026-08-12 — Facet-owner batch COMPLETE (spine + 6 owners; Dragoman runtime reconciled)

The full facet-owner set is built on the spine — one shared contract + six specializations (five
operating, one frontier stub). The spine held across every archetype with **no loop override for any
reader**; the single documented exception is Headwater (origin writer, three facets). Each agent surfaced
exactly one honest architectural note:

- **Headwater** (`meaning` + `object` + source-type) — origin-writer exception; modes `direct` / `case_author`.
- **Cartographer** (`intent`) — read-then-bind; also maintains the objective ontology as its governed vocabulary.
- **Couturier** (`expression` · *style*) — single-writer holds at *key* granularity (the sub-facet split).
- **Dragoman** (`expression` · *locale* — AST009) — retrieval memory (RAG) lives outside the graph-contract
  cleanly; `reconcile` mode = the SME human-in-the-loop template. **The `localize` runtime
  (`tools/localize/build_agent_call.py`) was reconciled** to load spine + specialization from the numbered
  path (interim "poor-man's resolver": concatenate the two files, spine first; `prompt_version` bumped to
  `loc-agent.v0.2-spine`, pending Jake's confirm). Folder stays `agents/localize/`; "Dragoman" is the
  display name.
- **Griot** (`narration`) — first agent with a real ordering dependency (words before voice), expressed as
  a *richer wake condition* (reads Dragoman's **validated** locale), not an agent-to-agent call.
- **Chameleon** (`audience`) — **stub only**, frontier (Response Engine / Orchestrator). Holds the seat,
  documents the wall, enforces no-PII even as a placeholder.

Files: `agents/{headwater_ingest,cartographer,couturier,localize,griot,chameleon}/02_system_prompts/core_agent/…`
+ `agents/_shared/facet_owner_spine.md`.

**Threads carried into the harness phase (Piece 2):** registries several agents are scaffolded ahead of
(`primitives.registry.json` partial; voice/prosody registries absent); the draft pedagogical-intent vocab;
the flat→numbered migration + `git rm agents/localize/system.md`; the `prompt_version` stamp to confirm.

## 2026-08-12 — Carry: no owner yet for the authored affective / narrative arc (supra-atomic composition)

Surfaced by Jake's "is this too atomic?" check. Verdict: the design is **atomic, not atomist** — atoms
carry relations (graph, not chain), *containers are atoms too* so group-level properties bind to the
container node, and shared **closed registries** keep independent per-atom choices coherent.

**The gap:** psychological/narrative structure emergent across **non-containment** relations — a callback
(scene 2 → scene 40), a fear planted early / resolved late, a difficulty ramp spanning modules — has *no
facet and no owner*. The clarifying split: **authored arc** (designer-built, content, supra-atomic,
homeless — wants its own single-writer facet `affect`/`narrative_arc` on container atoms + typed edges)
vs **per-learner adaptation** (`audience` + Response Engine, frontier, PII-free on content side).
**Anti-pattern:** letting the arc live only in a render agent's runtime — that smuggles a supra-atomic
truth outside the graph. Status: **carry**, sibling to the deferred ROI/goal node.

## 2026-08-11 — Facet-owner spine adopted; Headwater re-expressed on it

Agent system prompts are built as **spine + specialization**. `agents/_shared/facet_owner_spine.md` holds
the shared ~70% of every facet owner's contract. Each agent is a small specialization filling **seven
slots**: name, one-line role, facet+keys, wake condition, governed vocab refs, modes, schema refs. The
spine is canonical and referenced, never pasted (reference-don't-embed, applied to the prompts).

- **Load-bearing generalization:** Headwater owns `content_hash`; every other facet owner records the
  `source_hash` it bound against, so "is this facet stale?" is one graph walk.
- **The one exception, documented not smuggled:** Headwater is the *origin writer* — three facets at birth.
- **Headwater modes:** `direct` (bounded → mint) and `case_author` (large corpus → scope-commit →
  committed-design artifact → mint). A haiku-class **router** picks the mode.

### Agent batch progress (under this spine)
- **Cartographer** (intent) — built; maintains the objective ontology. **Couturier** (expression·style) —
  built; proves the sub-facet single-writer split (style keys vs locale keys). **Dragoman / Griot /
  Chameleon** — built (see 2026-08-12).

## 2026-08-12 — Objectives ontology instantiated + STRUCTURE.md reconciled

`schemas/objectives.schema.json` (governed closed list, `obj_` prefix, rejects a premature `serves` field)
+ `ontology/objectives.json` (seeded `obj_recognize_psi`, `obj_define_psi`, both `status: example`). Gated
7/7 (schema valid; refs resolve; prereq graph acyclic; negative controls rejected). STRUCTURE.md reconciled
(`ontology/` added). Per-project note: objective *schema* = shared core; an *instance* = per-project content.

## 2026-08-11 — Deferred: prompt resolver + plain-language explainer (explainer = auto-dogfood candidate)

Two human-facing **projections** of the spine+specialization, both deferred. (1) **Prompt resolver** — a
deterministic script that inlines each agent's slots into the spine → `resolved_prompt.md`. Pick up
whenever. (2) **Plain-language explainer** — a simplified projection into SME English, best built as
**auto-dogfood** once the render path exists (feed the manifold's own architecture in as a corpus).

## 2026-08-10 — Agent package folder structure locked (v0.1, "for now")

The numbered scaffold from the bundle's `Manifold_Rendering_Agent` is the standard agent operating-package
layout (`01_operating_model/` … `09_team_guidance/`). **Caveat (invariant guard):** canonical schemas and
vocabularies do **not** get copied into an agent's `04_schemas/` — they have one home
(`cgen/trainstorm-core/schemas/` + `/vocab/`); the folder holds *references* only. *(This is exactly the
invariant the 2026-08-13 drift-fix re-proved the hard way.)*

## 2026-08-10 — Ingest/headwater agent architecture is settled; next rung is the prompt pass

The ingest/decomposition agent is **not** greenfield — it is the **headwater authoring agent**
(`procedure-object-model.md`), extended to a second source type via the **`form` facet**
(`form-object-model.md`, gated 11/11). Procedure and form are duals on one spine; the object-model is an
**ingest view**, not the output-of-record (the atoms are). Single-writer: owns `meaning`, `object`, and
the source-type facet; intent / expression / audience / render are downstream readers. Open items carried:
mint 3 registry seeds (`role_alsap_lead`, `rec_alsap`, `reg_benefit_risk_profile`); resolve the
Benefit-Risk controlled-vs-example SME question.
