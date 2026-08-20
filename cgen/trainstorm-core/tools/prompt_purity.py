#!/usr/bin/env python3
"""
Shared purity rule: no atom's source text may appear in an agent's prompt.

Acceptance criterion #1 for render-as-agent (decision log 2026-08-19 / 08-20). If controlled content
reaches a prompt, the prompt has become a second copy of the controlled document, and it drifts the
moment the template is revised.

This lived inside resolve_slot.py. The moment a second tool needed it — resolve_prompt.py, which must
refuse to EMIT a leaking payload rather than merely report one — it would have been copy-pasted, and a
copied rule drifts. Same reasoning as store_merge.py.

Honest limit, restated wherever this is used: it catches VERBATIM copying, not paraphrase. Verbatim is
the realistic failure (someone pastes template text in "to help the agent"). This is not a proof.
"""

MIN_LEN = 25   # short labels ("Cover.", "Author.") are not content


def scan(atoms, texts):
    """texts: {label: text}. Returns [(label, atom_id, excerpt)] — empty means clean."""
    leaks = []
    for label, text in texts.items():
        for a in atoms:
            src = a["meaning"]["source_text"].strip().rstrip(".")
            if len(src) < MIN_LEN:
                continue
            if src in text:
                leaks.append((label, a["atom_id"], src[:70]))
    return leaks


def report(atoms, texts, leaks, what="prompt file(s)"):
    print("=" * 70)
    print(f"PROMPT PURITY — {len(atoms)} atoms vs {len(texts)} {what}")
    print("=" * 70)
    for label in texts:
        print(f"  checked: {label}")
    if leaks:
        for label, aid, s in leaks:
            print(f"  x LEAK {label}: contains {aid} — \"{s}...\"")
        print("VERDICT: FAIL — the prompt carries ALSAP content; it is a second source of truth.")
        return False
    print("VERDICT: PASS — no atom content found in the prompt. Grounding is a walk, not a paste.")
    return True
