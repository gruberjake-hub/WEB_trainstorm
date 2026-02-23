# Rehydration Packages for Context Transfer

**Source:** Learning system architecture conversation, Jan 2026  
**Context:** Building prompt-based instructional design workflow  
**Related Conversation:** AI content management and Git integration

---

## The Problem

When working across multiple AI conversations or handing off to another Claude instance, you lose context. A fresh conversation has no memory of:
- What you've already built
- Design decisions you've made and why
- Technical constraints you're working within
- What's complete vs what's pending

**This creates:**
- Repetitive explanations (wasting time)
- Lost context (inferior outputs)
- Inconsistent approach (new Claude doesn't know your patterns)
- Difficulty resuming work after time away

---

## The Solution

Create a comprehensive **rehydration package** - a state dump document that brings a fresh AI conversation up to full speed.

Think of it as: "Everything a new Claude instance needs to know to continue this work as if we'd been working together all along."

---

## What to Include

### 1. Executive Summary
- **Current phase:** Where are we in the project?
- **What's complete:** Deliverables finished
- **What's next:** Immediate next steps
- **Critical context:** Key facts the AI must know

### 2. All Key Artifacts
For each major output:
- **Description:** What it is
- **Location:** Exact file path
- **Purpose:** Why it exists
- **Status:** Draft / Complete / In-Review

Example:
```markdown
**Production Script:** 
- Location: `/mnt/user-data/outputs/Brunswick_Pay_Transparency_Script_v1.md`
- Purpose: 40-45 min eLearning script for managers
- Status: Complete, client-approved
```

### 3. Design Decisions Log
For each significant decision:
- **Decision:** What you chose
- **Rationale:** Why you chose it
- **Alternatives considered:** What you didn't choose and why
- **Trade-offs:** What you gave up / what you got
- **Reversibility:** Easy to change / Difficult / Locked in

### 4. Technical Considerations
- **Compilation challenges:** Where primitives may not map
- **Known limitations:** What won't work
- **Open questions:** What needs to be solved
- **Dependencies:** What requires what

### 5. Instructional Patterns Catalog
If relevant to the work:
- What component types exist in the design
- How they're structured
- Why they're structured that way

### 6. Next Steps for New Instance
Explicit tasks:
```markdown
## What the New Claude Should Do

1. Review the production script
2. Map content to available primitives
3. Identify gaps where primitives don't exist
4. Propose compilation approach
```

---

## Structure Template

```markdown
# REHYDRATION PACKAGE: [Project Name]
## State Dump for [Purpose - e.g., Compilation Phase]

**Generated:** YYYY-MM-DD  
**Purpose:** [One sentence - what this enables]  
**Current Phase:** [Where we are]  
**Target:** [Who/what this is for]

---

## EXECUTIVE SUMMARY: WHERE WE ARE

### Project Status
- Client: [Name]
- Deliverable: [What]
- Current State: [Phase complete]
- Next Step: [What needs to happen]

### What Has Been Completed
✅ [Item 1]
✅ [Item 2]
✅ [Item 3]

### What Needs to Happen Next
- [ ] [Task 1]
- [ ] [Task 2]

---

## KEY ARTIFACTS (Full Content)

### Artifact 1: [Name]
**Location:** `/path/to/file.md`
**Purpose:** [Why it exists]
**Status:** [Complete/Draft/Review]

[Include relevant excerpts or full content if needed]

---

## DESIGN DECISIONS LOG

### Decision: [Title]
**Date:** YYYY-MM-DD  
**Decision:** [What]  
**Rationale:** [Why]  
**Alternatives:** [What else considered]  
**Trade-offs:** [Gave up / Got]  
**Impact:** [What this affects]

---

## TECHNICAL CONSIDERATIONS

### Challenge 1: [Name]
**Problem:** [Description]
**Impact:** [What breaks or doesn't work]
**Mitigation:** [How to handle]

---

## INSTRUCTIONAL PATTERNS USED

### Pattern 1: [Name]
**What it is:** [Description]
**How it's structured:** [Format]
**Why it matters:** [Purpose]
**Frequency:** [How often used]

---

## OPEN QUESTIONS FOR NEW CLAUDE

**Q1:** [Question]  
**Context:** [Why this matters]  
**To resolve:** [What needs to happen]

---

## RECOMMENDED APPROACH

[Specific guidance on how to tackle the next phase]

---

**END OF REHYDRATION PACKAGE**

This document contains everything needed to continue work without context loss.
```

---

## When to Create Rehydration Packages

### Use Cases

**1. Forking Conversations**
- You want to work on two parallel aspects of a project
- One Claude works on design, another on implementation
- Both need full context

**2. Team Handoffs**
- You need to pass work to colleague
- They need to understand your thinking, not just see outputs
- Rehydration package = comprehensive briefing

**3. Resuming After Time Away**
- You pause work for weeks/months
- Fresh Claude instance needs context
- Rehydration package = your memory aid

**4. Documentation for Stakeholders**
- Client asks "where are we?"
- Rehydration package doubles as status report
- Shows thinking, not just deliverables

**5. Methodology Documentation**
- You want to capture "how we did this"
- For future similar projects
- Rehydration package = case study template

---

## Tips for Effective Rehydration

### 1. Create BEFORE Forking
Don't try to reconstruct context after the fact. Create while context is fresh.

### 2. Include File Paths
Always specify exact locations. "The script" is ambiguous. "`/outputs/script_v3.md`" is precise.

### 3. Be Explicit About Assumptions
State what you believe vs what you've proven. Prevents new Claude from assuming incorrectly.

### 4. Document Both Successes and Limitations
Not just "what worked" - also "what we tried that didn't work" and "what we haven't solved yet."

### 5. Write for Someone Who Wasn't There
Assume zero prior knowledge. If you had to brief a smart colleague who knows nothing about this project, what would you tell them?

### 6. Test It
After creating rehydration package, start fresh conversation. Upload package. Ask Claude: "What are we working on?" If answer is accurate and complete, package works.

---

## Example: Brunswick Project Rehydration

**Good rehydration opening:**
> We're building a 40-45 min eLearning script for Brunswick Corporation on pay transparency. Production script is complete at `/outputs/Brunswick_Pay_Transparency_Script_v1.md`. Key design decision: eLearning must carry heavy lifting because client has no trained facilitators for ILT. Next step: compile script to course.json, but scenario dialogue format may not map cleanly to available primitives.

**Poor rehydration opening:**
> Working on a training thing. Script is done. Need to compile it.

---

## Integration with Other Systems

**Rehydration packages complement:**
- **Project notes/DECISIONS.md:** Rehydration is comprehensive snapshot; decisions log is ongoing
- **Git commit history:** Rehydration explains "why"; commits show "what changed when"
- **README files:** Rehydration is state dump; README is orientation

**Think of it as:** Rehydration = save game file. Contains everything needed to resume exactly where you left off.

---

## Related Patterns

- [Project Template Structure](../project_template.md) - Standard organization
- [Design Commitment Notes](./design_commitment_notes.md) - Capturing rationale
- [Context Digests](./context_digests.md) - Initial sense-making

---

## Real-World Impact

**Without rehydration:** "I spent 30 minutes re-explaining context to new Claude before we could do actual work."

**With rehydration:** "I uploaded the package. Claude immediately understood everything and started solving the problem."

**Time saved per context transfer:** 20-30 minutes  
**Quality improvement:** New Claude has full context, not partial memory  
**Continuity:** Work flows seamlessly across conversation boundaries

---

**This pattern is especially valuable when AI generates content faster than you can organize it. Rehydration packages are how you preserve that velocity across sessions.**
