#!/usr/bin/env python3
"""
verify_agent_output.py — prove the agent's output plugs into the QE gate and the locale pack.

Takes a FILLED agent output (mocked here — a plausible draft), runs the deterministic
QE-gate checks the harness would run before a human sees it, then maps a passing draft
into a locales/ja.json entry exactly as element.schema / locales/README specify.
"""
import json, hashlib

SRC = "You must report product safety information to your Drug Safety Officer as soon as you become aware of it."
SOURCE_HASH = "sha256:" + hashlib.sha256(SRC.encode()).hexdigest()

# ── a MOCK of what the LLM returns given the assembled context (build_agent_call.py) ──
AGENT_OUTPUT = {
    "element_id": "ele_ast009_s04_stmt_012",
    "source_hash": SOURCE_HASH,
    "source_locale": "en",
    "target_locale": "ja",
    "target": "安全管理情報を認識した場合は、速やかに医薬品安全管理責任者に報告しなければなりません。",
    "status": "draft",
    "confidence": 0.78,
    "term_compliance": [
        {"concept": "product safety information", "required": "安全管理情報", "used": True}
    ],
    "flags": [
        {"span": "医薬品安全管理責任者", "category": "terminology-uncertain", "severity": "med",
         "note": "Rendering of 'Drug Safety Officer' — confirm the official Astellas-JP title."}
    ],
    "rationale": "Used locked 安全管理情報; kept formal ます register; flagged the DSO title as needing the official term.",
    "provenance": {"glossary_version": "astellas-pv.glossary.v0.1", "prompt_version": "loc-agent.v0.1",
                   "exemplars_used": ["ex_256dd4"], "tm_used": ["tm_001"]},
}

# what the assembled context said was locked for this string
LOCKED = [{"required": "安全管理情報", "forbidden": ["製品安全情報", "製品安全に関する情報"]}]

def qe_gate(out, locked, source_hash):
    """Deterministic pre-human checks. Returns (findings, passed)."""
    f = []
    # 1. the bright line — agent may never self-validate
    if out.get("status") != "draft":
        f.append(("ERROR", "status", f'status must be "draft", got {out.get("status")!r}'))
    # 2. provenance join — draft must be tied to the exact source meaning
    if out.get("source_hash") != source_hash:
        f.append(("ERROR", "source_hash", "source_hash does not match the source string (stale/mismatched draft)"))
    # 3. termbase compliance — the ~40% mechanical class, enforced not hoped
    tgt = out.get("target", "")
    for lk in locked:
        if lk["required"] not in tgt:
            f.append(("ERROR", "termbase", f'required term {lk["required"]} missing from target'))
        for bad in lk["forbidden"]:
            if bad in tgt:
                f.append(("ERROR", "termbase", f'forbidden calque {bad} present in target'))
    # 4. term_compliance self-report must not lie
    for tc in out.get("term_compliance", []):
        if tc.get("used") and tc["required"] not in tgt:
            f.append(("ERROR", "term-selfreport", f'claims used {tc["required"]} but it is absent'))
    # 5. register spot-check — bare 患者 without the honorific
    import re
    if re.search(r"患者(?!さん)", tgt):
        f.append(("WARN", "register", "bare 患者 without honorific さん"))
    # 6. output must be target-language only (no leftover source ascii sentences)
    if re.search(r"[A-Za-z]{4,}\s+[A-Za-z]{4,}", tgt.replace("Product Safety Awareness", "")):
        f.append(("WARN", "purity", "target contains untranslated English runs (check defined-name exceptions)"))
    passed = not any(lv == "ERROR" for lv, _, _ in f)
    return f, passed

def to_locale_entry(out, reviewer=None):
    """Map a reviewer-approved draft into a locales/ja.json entry (element.schema contract)."""
    return {out["element_id"]: {
        "target": out["target"],
        "status": "validated" if reviewer else "draft",
        "reviewer": reviewer,
        "source_hash": out["source_hash"],
    }}

def main():
    print("QE GATE  (deterministic, before any human sees the draft)")
    print("-" * 70)
    findings, passed = qe_gate(AGENT_OUTPUT, LOCKED, SOURCE_HASH)
    if findings:
        for lv, chk, msg in findings:
            print(f"  {'✗' if lv=='ERROR' else '⚠'} {lv:5s} [{chk}] {msg}")
    else:
        print("  ✓ clean — no mechanical defects")
    print(f"\n  → gate result: {'PASS → route to human review' if passed else 'FAIL → back to agent'}")
    print(f"  → {len(AGENT_OUTPUT['flags'])} judgment flag(s) forwarded to the reviewer\n")

    print("LOCALE-PACK MAPPING  (locales/ja.json)")
    print("-" * 70)
    print("  before reviewer sign-off (status=draft):")
    print("   ", json.dumps(to_locale_entry(AGENT_OUTPUT), ensure_ascii=False))
    print("  after reviewer confers validated:")
    entry = to_locale_entry(AGENT_OUTPUT, reviewer="jp_sme_reviewer")
    print("   ", json.dumps(entry, ensure_ascii=False))

    # schema-shape assertion (matches locales/README contract)
    v = next(iter(entry.values()))
    assert set(v) == {"target", "status", "reviewer", "source_hash"}, "locale entry shape drift"
    assert v["source_hash"].startswith("sha256:"), "source_hash join broken"
    print("\n  ✓ locale entry matches element.schema / locales contract (keyed by element_id, source_hash join intact)")

if __name__ == "__main__":
    main()
