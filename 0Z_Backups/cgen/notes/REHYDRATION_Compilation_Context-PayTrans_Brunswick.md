# REHYDRATION PACKAGE: Pay Transparency Course Compilation
## Technical Context for Learning Cognition System Implementation

**Date:** 2026-01-19  
**Purpose:** Bring a new Claude instance up to speed on the compilation challenge  
**Context:** This is ONE path of a forked conversation—other path continues instructional design work

---

## SYSTEM ARCHITECTURE OVERVIEW

### What We're Building

A **Learning Cognition System** that auto-generates courses from instructional scripts through a compilation process:

```
Instructional Script (markdown)
    ↓ [soft-compiler prompt]
course.json (structured format)
    ↓ [runtime engine]
Deployed course on website
```

### The Challenge

We have a production-ready instructional script (~15,000 words, highly structured) that was designed through a rigorous process:
1. Context ingestion (7-file corpus, ~2,800 lines)
2. Sense-making analysis (Context Digest)
3. Strategic exploration (high-temperature design thinking)
4. Design commitment (production script authoring)

**The script contains instructional sophistication that may not map cleanly to available course.json primitives.**

Question: How do we compile this without losing instructional integrity?

---

## WHAT WE'VE BUILT (Summary)

### The Script
**File:** `Brunswick_Pay_Transparency_Script_v1.md`  
**Length:** ~15,000 words  
**Duration:** 40-45 minutes estimated  
**Audience:** Brunswick managers and HR professionals  
**Topic:** Pay transparency and compensation conversations

### Structure
```
Introduction (~3 min)
Module 1: How Pay Works at Brunswick (~8 min)
  ├─ Compensation Philosophy
  ├─ Pay Ranges
  ├─ Individual Pay Factors
  └─ Base Pay vs Total Rewards

Module 2: What's Changing (~5 min)
  ├─ Transparency Landscape
  ├─ Impact on Managers
  └─ Opportunity Beyond Compliance

Module 3: Conversation Framework (~7 min)
  ├─ Success Definition
  └─ 5-Step Framework (Pause → Ask → Explain → Partner → Close)

Module 4: Scenarios (~12 min)
  ├─ Scenario 1: "Why am I at midpoint?"
  ├─ Scenario 2: "Why does my colleague make more?"
  ├─ Scenario 3: "External market shows higher pay"
  ├─ Scenario 4: "Frustrated despite high performance"
  ├─ Scenario 5: "When to escalate"
  └─ Scenario 6: "Redirecting to development"

Module 5: Escalation & Resources (~4 min)
  ├─ Green/Yellow/Red Framework
  ├─ How to Escalate Professionally
  └─ Available Resources

Module 6: Preparation (~3 min)
  ├─ Before First Conversations
  ├─ Proactive vs Reactive
  └─ Managing Expectations

Optional Practice Assignment (~5 min if completed)

Knowledge Checks (~5 min total, distributed throughout)
  ├─ 10 questions total
  ├─ Mixture of MC, multi-select, true/false, scenario-based
  └─ Placed strategically, not all at end

Conclusion (~2 min)

Plus 3 Downloadable Job Aids:
  ├─ Conversation Framework (1-page reference)
  ├─ Escalation Decision Tree (visual)
  └─ Practice Scenario Worksheet
```

### Key Design Characteristics

1. **Honest About Limitations:** Explicitly states training is foundation, not complete solution
2. **Scenario-Heavy:** 6 full scenarios with dialogue + debrief
3. **Tool-Focused:** Job aids may deliver more value than eLearning content itself
4. **Spaced Repetition:** "Pause skill" appears in framework, all scenarios, multiple checks
5. **Realistic Success Criteria:** "Employee understands" not "employee is happy"
6. **Brunswick Voice:** 2nd person, empowering without preaching, research-backed

---

## COMPILATION CHALLENGE: WHERE PRIMITIVES MAY NOT MAP

### Complex Elements That May Lose Fidelity

#### 1. **Scenario Structure**
Each scenario has:
- Setup text (context)
- Multi-turn dialogue (manager/employee back-and-forth)
- Debrief with bullet points (what worked)
- Narrator commentary threading through

**Potential mapping issue:** If course.json primitives expect simple "stimulus → response" interactions, multi-turn dialogue with running commentary doesn't fit cleanly.

**What could be lost:** The rhythm of realistic conversation (employee pushes back, manager responds, conversation evolves). If flattened to single-turn Q&A, loses instructional value.

#### 2. **Job Aids as First-Class Deliverables**
Three substantial job aids are specified:
- Conversation Framework (1-page, front/back, specific content provided)
- Escalation Decision Tree (visual flowchart, structure described)
- Practice Worksheet (template with 10 questions)

**Potential mapping issue:** If course.json treats downloads as metadata/links rather than content objects, the detailed specifications could be lost.

**What could be lost:** The job aids ARE the deliverable for many managers (more useful than eLearning). If compilation treats them as "attach PDF" afterthoughts, misses design intent.

#### 3. **Distributed Knowledge Checks**
10 knowledge checks placed throughout (not all at end):
- Check 1 after Module 1 (comp philosophy)
- Check 2 after conversation framework
- Check 3 after scenarios
- Checks 4-10 after remaining modules and at end

**Potential mapping issue:** If course.json expects assessment as separate module, strategic placement is lost.

**What could be lost:** Spaced practice effect. Checks are teaching moments, not just evaluation.

#### 4. **Optional vs Required Pathways**
Practice assignment is explicitly optional:
- Core path: Introduction → Modules 1-6 → Knowledge Checks → Conclusion
- Optional branch: Practice Assignment (can be skipped)

**Potential mapping issue:** If primitives don't support conditional/optional content elegantly, becomes forced or hidden.

**What could be lost:** The "soft optional" positioning—framed as enhancement, used to gauge interest for Phase 2.

#### 5. **Layered Narration + On-Screen Text**
Throughout script, pattern is:
```
**On-screen:** [Text that appears visually]
**Narration:** [Audio voiceover, often different from on-screen]
```

Sometimes these are complementary, sometimes on-screen is bullet points while narration is full sentences.

**Potential mapping issue:** If primitives expect single "content" field, the audio/visual layering gets flattened.

**What could be lost:** Cognitive load management—on-screen provides structure, narration provides detail and tone.

#### 6. **Framework as Persistent Reference**
The 5-step conversation framework is:
- Introduced in Module 3
- Applied in all 6 scenarios
- Referenced in knowledge checks
- Provided as downloadable job aid

**Potential mapping issue:** If each module compiles independently, the framework's recurrence as persistent mental model gets lost.

**What could be lost:** The instructional throughline—framework taught once, seen in action repeatedly.

#### 7. **Tone and Voice**
Script uses specific linguistic patterns:
- 2nd person direct ("you")
- Empathy without apology ("This will be awkward" not "We're sorry this is hard")
- Research citations where credible
- Permission-giving language ("It's okay if employee is still frustrated")

**Potential mapping issue:** If compilation strips to bare content, voice gets neutralized.

**What could be lost:** The Brunswick cultural fit. This was designed to match their style from example script analysis.

#### 8. **Design Commitment Notes**
Extensive metadata at end:
- 10 key instructional decisions explained
- Exclusions/deferrals with rationale
- 7 known limitations/risks
- 10 assumptions for future revision

**Potential mapping issue:** This isn't course content—it's designer-to-stakeholder communication. But it's essential context.

**What could be lost:** The "why" behind every choice. Future maintainers won't understand intent.

---

## PRIMITIVE MAPPING QUESTIONS FOR NEW CLAUDE

Here are the specific technical questions the compilation process needs to resolve:

### Content Structure

**Q1:** Does course.json support nested modules with time estimates?
- Script has 6 modules, some with 3-4 sub-scenes
- Each has estimated duration (~3 min, ~8 min, etc.)
- Need to preserve hierarchy: Module → Scene → Content

**Q2:** How are scenarios represented?
- Multi-turn dialogue (not simple Q&A)
- Includes setup, back-and-forth conversation, debrief
- Some have 10+ turns of realistic dialogue
- Need to maintain conversational flow

**Q3:** What's the primitive for "demonstration" vs "practice"?
- These scenarios are observation + reflection, not simulation
- Learner watches, doesn't interact beyond "what did manager do well?"
- Not branching scenario, not quiz—it's modeled behavior

### Assessment & Interaction

**Q4:** How are distributed knowledge checks handled?
- Not a single assessment block at end
- 10 checks spread throughout, each contextually placed
- Some are MC, some multi-select, one true/false
- Each has correct/incorrect feedback (teaching, not just scoring)

**Q5:** Can feedback be instructional vs just "right/wrong"?
- Script provides substantial feedback for each answer
- Feedback explains the reasoning, doesn't just confirm choice
- This is spaced learning, not testing

**Q6:** How are optional activities marked?
- Practice assignment is skippable but valuable
- Should be framed as enhancement, not requirement
- Need to track completion (data for Phase 2) but not block progress

### Media & Downloads

**Q7:** How are downloadable job aids specified?
- Three substantial documents, each with detailed content
- Not just "provide link to PDF"—the content is architected
- Conversation Framework has specific front/back layout
- Practice Worksheet has 10 scaffolded questions

**Q8:** Are visuals/diagrams first-class objects?
- Script calls for:
  - Pay range diagram (visual showing min/mid/max zones)
  - 3-pillar philosophy graphic
  - Escalation decision tree (flowchart)
  - 5-step framework visual
- These aren't decorative—they're instructional

**Q9:** How is audio narration vs on-screen text distinguished?
- Pattern throughout: **On-screen:** X, **Narration:** Y
- Sometimes complementary, sometimes different content
- Audio provides detail/tone, visual provides structure

### Metadata & Context

**Q10:** Where does design rationale live?
- Design Commitment Notes section has extensive context
- Not course content, but essential for maintenance
- Explains decisions, flags risks, documents assumptions
- Without this, future updates break design intent

**Q11:** How are learning objectives mapped to content?
- 10 LOs at start
- Each module addresses specific LOs
- Knowledge checks tied to specific LOs
- Need traceability for accreditation/reporting

**Q12:** Are dependencies/prerequisites supported?
- Module 4 (scenarios) assumes Modules 1-3 taught framework
- Practice assignment assumes main content complete
- Can't randomize or skip ahead

---

## WHAT THE NEW CLAUDE NEEDS TO SOLVE

### Primary Task
**Given:**
- A production-ready instructional script (provided)
- A soft-compiler prompt that converts scripts to course.json (need to see this)
- A set of available primitives in course.json (need to understand this)

**Produce:**
- A compiled course.json that preserves instructional integrity
- Documentation of what was preserved vs approximated vs lost
- Recommendations for primitive additions if needed

### Success Criteria

**Minimum viable:** Course builds and runs without errors

**Good:** Course preserves:
- Module structure and flow
- Knowledge check placement and feedback
- Scenario content (even if simplified)
- Job aid specifications
- Key instructional decisions

**Excellent:** Course preserves:
- Multi-turn scenario dialogue rhythm
- Distributed assessment strategy
- Audio/visual layering
- Optional pathway positioning
- Design rationale for future maintenance

### Known Risks

1. **Over-simplification:** Flattening scenarios to simple Q&A loses realism
2. **Orphaned content:** Job aids specified but not compiled into deliverables
3. **Lost context:** Design Commitment Notes not captured, future updates break intent
4. **Neutralized voice:** Tone stripped, becomes generic corporate speak
5. **Broken throughline:** Framework taught once, not reinforced throughout
6. **Assessment as afterthought:** Checks treated as quiz-block, not teaching moments

---

## ARTIFACTS AVAILABLE TO NEW CLAUDE

### Must-Have Context
1. **This rehydration document** (you're reading it)
2. **Brunswick_Pay_Transparency_Script_v1.md** (the script to compile)
3. **Learning Objectives (revised)** (10 LOs, explicit mapping needed)
4. **Assessment items document** (structure for knowledge checks)

### Helpful Context
5. **Context Digest** (why this project exists, organizational reality)
6. **Exploratory Design Analysis** (strategic thinking behind script)
7. **SOW/Proposal** (constraints, audience, scope)
8. **Example Brunswick script** (tone/style reference)

### For Deep Dive (if needed)
9. **Project context corpus** (7-file source, 2800 lines)
10. **Revision summaries** (what changed and why)

---

## COMPILATION STRATEGY RECOMMENDATIONS

### Approach 1: Faithful Translation
Compile exactly what's in the script, even if it exposes primitive limitations.

**Pros:** 
- Preserves instructional integrity
- Reveals what primitives are missing
- Provides clear requirements for system improvement

**Cons:** 
- May not compile cleanly
- Could require primitive additions
- Might delay deployment

### Approach 2: Graceful Degradation
Where primitives don't map perfectly, approximate with closest available option.

**Example:**
- Multi-turn scenario → Single "stimulus + response" interaction with longer text
- Layered narration → Combined into single content block
- Optional practice → Hidden module that learner can skip

**Pros:**
- Compiles immediately
- Deploys faster
- Proves concept

**Cons:**
- Loses some instructional value
- May disappoint stakeholders
- Creates technical debt

### Approach 3: Hybrid - Core + Extensions
Compile core content faithfully, mark advanced features as "extension needed."

**Example:**
- Core modules compile cleanly
- Complex scenarios flagged as "requires dialogue primitive"
- Job aids compiled as structured objects, flagged as "requires download primitive"
- Design notes exported as separate metadata file

**Pros:**
- Balanced pragmatism
- Clear roadmap for enhancement
- Incremental improvement path

**Cons:**
- Requires judgment calls on what's core vs extension
- May still require some approximation

---

## IMMEDIATE NEXT STEPS FOR NEW CLAUDE

1. **Examine the soft-compiler prompt:** Understand how it expects to transform scripts
2. **Review course.json schema:** What primitives actually exist?
3. **Identify mapping gaps:** Where does script structure not match available primitives?
4. **Propose solution:** Faithful translation, graceful degradation, or hybrid?
5. **Compile or specify:** Either produce course.json or document what's needed to produce it

---

## CRITICAL CONTEXT: WHY THIS MATTERS

This isn't just a technical exercise. The script represents:
- Rigorous analysis of organizational reality (Context Digest)
- Strategic design decisions (Exploratory Analysis)
- Honest reckoning with constraints (no facilitators, eLearning doing heavy lifting)
- Careful attention to Brunswick's culture and voice

**If compilation loses instructional integrity, we've wasted that work.**

The Learning Cognition System's value proposition is:
> "Auto-generate courses that are as good as human-designed ones."

This script is a test case. If we can compile it without meaningful loss, the system works. If we can't, we've identified what needs to be built.

---

## QUESTIONS FOR THE NEW CLAUDE TO ASK

Before diving into compilation, you should understand:

1. **What does the soft-compiler prompt actually look like?** (Critical input)
2. **What's the course.json schema?** (What primitives exist?)
3. **What's the runtime environment?** (What can the player actually render?)
4. **Is there a course.json example to reference?** (Existing courses as patterns)
5. **What's the priority: ship fast or ship right?** (Informs strategy choice)
6. **Are primitive additions feasible?** (Can we extend the system if needed?)
7. **What's the tolerance for degradation?** (How much approximation is acceptable?)

---

## HANDOFF TO INSTRUCTIONAL DESIGN CONVERSATION

Meanwhile, the **other fork of this conversation** (the one you're not joining) will continue working on:
- Client presentation materials (executive summary, visual mock-ups)
- Facilitator guide (if optional ILT happens)
- Job aid design specifications (taking content to visual design)
- Phase 2 planning (enhanced support, pilot evaluation)

That conversation has the instructional design expertise and client relationship context. Your conversation has the technical/compilation expertise.

**Both are necessary. Neither is sufficient alone.**

---

## FINAL NOTE

The user (learning architect) describes this as:
> "Auto-generating these courses as part of a larger Learning Cognition System"

You're not just compiling one course. You're helping prove (or disprove) that:
- Complex instructional design can be systematically generated
- Scripts can be compiled without instructional loss
- The Learning Cognition System can produce professional-grade outputs

**High stakes, fascinating challenge, important work.**

Good luck. The script is excellent. Don't let compilation ruin it.

---

**END OF REHYDRATION PACKAGE**

**Status:** Ready for technical conversation fork  
**Next Step:** New Claude examines soft-compiler prompt and course.json schema  
**Success Metric:** Compiled course preserves instructional integrity
