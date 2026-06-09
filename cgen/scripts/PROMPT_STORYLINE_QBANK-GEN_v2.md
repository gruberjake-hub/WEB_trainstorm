# PROMPT_QBANK-GEN v2.0
*(General-purpose Storyline-import question bank generator)*

---

## CONFIGURATION

```
COURSE_NAME:           {{COURSE_NAME}}
SOURCE_DOC:            project_context.md  ← always the grounding document
ROLE_PATH:             {{ROLE_PATH}}
NUM_QUESTIONS:         {{NUM_QUESTIONS}}
QUESTION_TYPES:        {{QUESTION_TYPES}}     ← e.g. "MC, TF" — default: MC only
CHOICES_PER_QUESTION:  {{CHOICES_PER_QUESTION}} ← default: 4
POINT_VALUE:           {{POINT_VALUE}}         ← default: 10
DISTRACTOR_DIFFICULTY: {{DISTRACTOR_DIFFICULTY}} ← easy | standard | mastery
```

### Distractor Difficulty Definitions

| Setting   | Distractor Mix (for 4-choice MC)                                                      |
|-----------|---------------------------------------------------------------------------------------|
| `easy`    | 1 near-miss + 2 obviously wrong                                                       |
| `standard`| 2 near-miss + 1 plausible misconception                                               |
| `mastery` | 2 hard near-misses + 1 plausible misconception (all three should trap a partial learner)|

---

## MODULE 1 — CORRECT ANSWER EXTRACTION (RUN FIRST)

You are a precise extraction engine. Your only job is to produce defensible, source-faithful correct answers from `SOURCE_DOC`.

### Source Format Handling

**If SOURCE_DOC is `.md` or `.txt`:**
Extract directly from prose and structured content. Preserve source wording where possible.

**If SOURCE_DOC is `.json`:**
- Ignore structural elements: keys, IDs, schema metadata, array indices, field names.
- Extract ONLY from value fields that carry semantic content: definitions, rules, procedural descriptions, policy statements, behavioral descriptions.
- If a value is a string that reads as a complete rule or definition, treat it as extractable.
- If a value is a numeric score, boolean flag, or internal reference ID, skip it.
- Preserve the wording of extracted values; do not rephrase to match JSON conventions.

### Rules (all formats)
- Output ONLY what the source directly supports.
- Preserve source wording where possible; rephrase only for grammatical completeness.
- Do NOT invent, infer beyond the text, or summarize.
- Do NOT create distractors here.

### Output (JSON only, no commentary)

```json
[
  {
    "concept": "",
    "correct_answer": "",
    "source_ref": ""
  }
]
```

---

## MODULE 2 — DISTRACTOR GENERATION

You are a distractor engineer. Your job is to construct wrong answers that are deliberately difficult to dismiss, using defined misconception types.

### Distractor Type Taxonomy

Assign ONE type to each distractor before writing it. The type controls the strategy:

| Type | Description | Example pattern |
|------|-------------|-----------------|
| `near-miss/sequence` | Correct elements, wrong order or wrong step | Steps 2 and 3 swapped |
| `near-miss/scope` | Correct concept but wrong level of application | Policy that applies to managers applied to all staff |
| `near-miss/condition` | Correct rule but wrong trigger condition | "When X happens" replaced with plausible-but-wrong "when Y happens" |
| `near-miss/attribution` | True fact from source, attributed to wrong context | Real definition, but belonging to a different term |
| `plausible-misconception` | Reflects a real, common learner error — not in source | Typical prior-knowledge assumption that this course corrects |
| `obvious-wrong` | Clearly incorrect for easy/padding purposes | Use sparingly; only permitted in `easy` mode |

### Length Parity Rule
All choices — correct AND distractor — must be within ±20% of the correct answer's word count.
If the correct answer is 12 words, every distractor must be 10–14 words.
Short distractors are a tell. Enforce this without exception.

### Grammatical Consistency Rule
All choices must use the same grammatical form as the correct answer: same tense, same sentence type, same level of specificity.

### Module 2 Output (JSON only)

```json
[
  {
    "concept": "",
    "correct_answer": "",
    "distractors": [
      { "type": "near-miss/sequence", "text": "" },
      { "type": "near-miss/condition", "text": "" },
      { "type": "plausible-misconception", "text": "" }
    ]
  }
]
```

---

## MODULE 3 — QUESTION ASSEMBLY + CSV EXPORT

Assemble Module 1 and Module 2 outputs into Storyline-importable CSV.

---

### QUESTION TYPE RULES (apply strictly)

| Type | Choice-level feedback? | Correct answer marker | Notes |
|------|------------------------|-----------------------|-------|
| `MC` | ✅ Yes — inline with `\|` | `*` prefix on correct choice | One correct answer only |
| `MR` | ❌ No — general feedback only | `*` prefix on ALL correct choices | Multiple correct answers allowed |
| `TF` | ❌ No — general feedback only | `*` prefix on correct choice | Choices must be exactly `True` and `False` |
| `FIB` | ❌ No | `*` prefix | List all acceptable answers as separate choices |
| `WB` | ❌ No | `*` prefix on correct placements | Word bank drag-drop |

---

### FIELD FORMATTING RULES

#### Correct Answer + Inline Feedback (MC only)
The correct choice field contains BOTH the answer text and its feedback, separated by `|`:
```
*Correct answer text here | This is correct because [reason grounded in source].
```

#### Distractor + Inline Feedback (MC only)
Each distractor field uses the same `|` pattern:
```
Distractor text here | This is incorrect because [specific correction grounded in source].
```

#### General Feedback (all types)
Two-part field separated by `|`:
```
Correct feedback text. | Incorrect feedback text.
```

#### Feedback Writing Rules
- Correct feedback: confirms *why* this is right; must cite source logic, not just "Correct!"
- Incorrect feedback: names the specific error (reference the misconception type if useful); does not reveal the correct answer directly.
- Both correct and incorrect feedback should be 1–2 sentences.

---

### CSV SCHEMA

```
QuestionID, QuestionType, Points, Question, ChoiceA, ChoiceB, ChoiceC, ChoiceD, Feedback, Topic, Tags
```

**Column notes:**

| Column | Notes |
|--------|-------|
| `QuestionID` | Stable ID: `{COURSE_CODE}-Q{n}` e.g. `ALSAP-Q01` |
| `QuestionType` | MC / MR / TF / FIB / WB |
| `Points` | Use POINT_VALUE from config |
| `Question` | Scenario-grounded stem. Must name a realistic situation requiring judgment. |
| `ChoiceA` | Always the correct answer. Format: `*text \| feedback` (MC) or `*text` (other) |
| `ChoiceB–D` | Distractors. Format: `text \| feedback` (MC) or `text` (other) |
| `Feedback` | General question-level feedback: `correct msg \| incorrect msg`. Required for MR and TF. |
| `Topic` | Section or objective area from source |
| `Tags` | Semicolon-delimited: `Apply;Judgment;{concept}` |

**CSV rules:**
- Quote any field containing commas or pipes.
- No blank rows.
- No trailing tabs or spaces.
- ChoiceA is always the correct answer (randomization handled by Storyline).

---

### QUESTION STEM REQUIREMENTS

Every question stem must:
1. Describe a realistic situation the learner could face in `ROLE_PATH`.
2. Embed the decision point — make the learner choose, not recall.
3. Avoid answer giveaways in the stem (no "which of the following is NOT").
4. Be answerable using only `project_context.md`.
5. Target application or judgment, not pure recall.

---

### EXAMPLE ROW (MC, 4 choices)

```csv
QuestionID,QuestionType,Points,Question,ChoiceA,ChoiceB,ChoiceC,ChoiceD,Feedback,Topic,Tags
ALSAP-Q01,MC,10,"A team lead notices a deviation during a batch review but the batch was released last shift. What is the correct first action?","*Submit a deviation report within 24 hours of discovery | Correct: source_context specifies a 24-hour reporting window from point of discovery, not release.","Notify QA and wait for verbal approval before documenting | Incorrect: verbal approval does not substitute for written documentation per source_context.","Document the deviation at the next scheduled review cycle | Incorrect: the reporting window begins at discovery, not at the next review cycle.","Escalate to the site head before any documentation is created | Incorrect: documentation precedes escalation in the source_context workflow.","Correct: the 24-hour window begins at discovery. | Incorrect: review the deviation reporting timeline in source_context.",Deviation Reporting,"Apply;Judgment;Compliance"
```

---

## PROCESS ORDER

1. Run **Module 1** against `project_context.md`. Output JSON.
2. Run **Module 2** using Module 1 output + `DISTRACTOR_DIFFICULTY` setting. Output JSON.
3. Run **Module 3** to assemble and export CSV.
4. Validate: every row must have all columns; correct answer must be `ChoiceA`; MC rows must use `|` in choice fields; MR/TF rows must NOT use `|` in choice fields.

Return CSV only. No commentary. No extra text.
