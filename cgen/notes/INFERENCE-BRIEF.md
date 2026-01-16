INFERENCE BRIEF

Project: WEB_TRAINSTORM (AI-driven learning runtime)

What this is:
- Native HTML/CSS/JS learning runtime
- Deterministic course.json compiler
- Brand + theme system separated from content
- Multi-client, multi-course architecture

Current focus:
- Runtime / branding / theme orchestration
- Not changing compiler behavior
- Not changing course.json schema

Key design decisions already made:
- Brand = identity + rules + assets (JSON)
- Theme = CSS expression of brand
- Compiler is brand-agnostic
- Runtime applies branding before init()

What I need help with right now:
- [1–2 concrete goals, e.g. “stabilize branding pipeline”]

Constraints:
- Avoid re-architecting unless strictly necessary
- Preserve existing brand/theme separation
