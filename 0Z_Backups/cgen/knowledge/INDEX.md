# Knowledge Base Index
**Last Updated:** 2026-01-19  
**Purpose:** Curated AI-generated insights reusable across projects

---

## What Goes Here

**✅ Include:**
- Reusable insights (apply to future projects)
- Significant thinking (changed my approach)
- Non-obvious wisdom (not easily recreated)
- Design patterns that worked
- Strategic frameworks

**❌ Exclude:**
- Project-specific details (goes in `courses/[project]/notes/`)
- Basic best practices (already know these)
- Temporary experiments (not yet proven)

---

## By Topic

### Instructional Design
- [Rehydration Packages](by_topic/instructional_design/rehydration_packages.md) - Context transfer for AI conversations
- [Design Commitment Notes](by_topic/instructional_design/design_commitment_notes.md) - Capturing design decisions and rationale
- *More to come...*

### Compensation & Pay Transparency
- *Coming soon...*

### Conversation Frameworks
- *Coming soon...*

### Prompt Engineering
- *Coming soon...*

### Course Development
- *Coming soon...*

---

## By Project

- [Brunswick Pay Transparency 2026](by_project/brunswick_2026_learnings.md) - First full prompt-based course development
- *More projects to come...*

---

## Quick Reference

### Most Referenced
- [Rehydration Packages](by_topic/instructional_design/rehydration_packages.md) - Use whenever forking AI conversations

### Recently Added
- **2026-01-19:** [Rehydration Packages](by_topic/instructional_design/rehydration_packages.md)
- **2026-01-19:** Created knowledge base structure

---

## How to Use This Index

### Adding New Knowledge

1. **During AI conversation:** Note reusable insights mentally
2. **Within 24 hours:** Extract to files
3. **File location:** 
   - `knowledge/by_topic/[category]/[topic_name].md` for concepts
   - `knowledge/by_project/[project_name]_learnings.md` for project-specific
4. **Update this INDEX:** Add link in appropriate section
5. **Commit:** `git add knowledge/ && git commit -m "Add [topic] to knowledge base"`

### Finding Knowledge

**Method 1 - Scan this INDEX:**
- Browse by topic or project
- Click links

**Method 2 - VS Code Search:**
- `Cmd+Shift+F` (Mac) or `Ctrl+Shift+F` (Windows)
- Search across `knowledge/` folder

**Method 3 - Terminal Search:**
```bash
# Find files mentioning "escalation"
grep -r "escalation" knowledge/

# See what was added recently
git log --oneline knowledge/
```

---

## Maintenance

**Weekly (15 min):**
- Review this week's AI conversations
- Extract 2-3 best insights
- Update this INDEX
- Commit changes

**Monthly (30 min):**
- Review last month's additions
- Consolidate related insights
- Archive outdated patterns
- Update "Most Referenced" section

---

## Categories to Expand

As your knowledge base grows, consider adding:
- Scenario Design Patterns
- Assessment Strategies
- Client Management
- Technical Architecture
- Automation Scripts
- Localization Approaches

Create new topic folders as needed:
```bash
mkdir -p knowledge/by_topic/[new_category]
```

---

## Stats

**Total insights:** 1  
**Topics covered:** 1  
**Projects documented:** 1  
**Last update:** 2026-01-19

---

**This is your intellectual capital. Grow it consistently.**