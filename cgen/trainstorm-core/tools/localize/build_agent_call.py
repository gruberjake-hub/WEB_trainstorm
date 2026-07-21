#!/usr/bin/env python3
"""
build_agent_call.py — assemble the COMPLETE message payload for the Translation Agent.

This is the runnable bridge between the retrieval harness and the agent prompt:
it takes one source element, retrieves its grounded context from the REAL corpus,
and emits the exact [system, user] messages you would send to the enterprise LLM
(Azure OpenAI), plus the output shape the agent must return.

  element (source string)                → the unit of work
  + system prompt (translation_agent.system.md)
  + assembled context (glossary · TM · contrastive exemplars · register)
  = a ready-to-send chat payload.

Run:  python build_agent_call.py
Writes: agent_call_payload.json   (the payload you'd POST to the model)
"""
import json, re, hashlib, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))          # trainstorm-core/tools/localize/
ROOT = os.path.dirname(os.path.dirname(HERE))               # trainstorm-core/
CORPUS_PATH   = os.path.join(ROOT, "registry", "corpus", "astellas-pv.ja.jsonl")
GLOSSARY_CSV  = os.path.join(ROOT, "registry", "glossary", "astellas-pv.candidates.csv")
SYSTEM_PROMPT = os.path.join(ROOT, "agents", "localize", "system.md")

# ── load the governed memory (real files) ─────────────────────────────────────
def load_corpus():
    with open(CORPUS_PATH, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def load_glossary():
    """Parse the locked-term seed into constraint records (EN trigger is illustrative)."""
    import csv
    rows = []
    with open(GLOSSARY_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "good": r["preferred_term(good)"],
                "bad":  r["avoid(bad)"],
                "category": r["category"],
                "note": r["rule_note"],
            })
    return rows

# Illustrative EN concept → locked term triggers (until the termbase carries EN keys).
GLOSSARY_TRIGGERS = {
    "product safety information": "安全管理情報",
    "safety information":         "安全管理情報",
    "product safety awareness":   "Product Safety Awareness (keep English)",
    "astellas":                   "アステラス",
    "patient":                    "患者さん",
    "patients":                   "患者さん",
}

# ── retrieval (stand-ins for embedding similarity; deterministic + legible) ────
def words(s): return set(re.findall(r"[a-z]+", s.lower()))

def retrieve_glossary(query, glossary):
    ql = query.lower()
    hits = []
    for concept, good in GLOSSARY_TRIGGERS.items():
        if concept in ql:
            match = next((g for g in glossary if g["good"] == good or good.startswith(g["good"])), None)
            hits.append({
                "concept": concept,
                "required": good,
                "forbidden": match["bad"] if match else None,
                "note": match["note"] if match else None,
            })
    # de-dupe by required rendering, keep the most specific concept
    seen, out = set(), []
    for h in sorted(hits, key=lambda x: -len(x["concept"])):
        if h["required"] in seen: continue
        seen.add(h["required"]); out.append(h)
    return out

TM = [  # approved EN→JA pairs anchored in the worked example (stand-in TM store)
    {"id": "tm_001", "en": "Recognize product safety information",
     "ja": "製品の安全管理情報を見分ける"},
    {"id": "tm_002", "en": "Explain the importance of product safety awareness",
     "ja": "Product Safety Awarenessの重要性について説明する"},
    {"id": "tm_003", "en": "How can we inform our patients and healthcare professionals about potential risks?",
     "ja": "どうすれば私たちは患者さんや医療従事者に潜在的なリスクについて、知らせることができるでしょうか？"},
]

def retrieve_tm(query, k=2):
    qw = words(query)
    ranked = sorted(TM, key=lambda t: len(qw & words(t["en"])) / max(1, len(qw | words(t["en"]))), reverse=True)
    return [t for t in ranked if len(qw & words(t["en"])) >= 2][:k]

def retrieve_exemplars(query, corpus, k=3):
    """Metadata-filtered contrastive pairs that TEACH the terms relevant to this string."""
    ql = query.lower()
    want_term = "安全管理情報" if ("safety information" in ql or "product safety" in ql) else None
    pool = []
    for r in corpus:
        if r.get("primary_tag") == "terminology-regulatory" and want_term:
            if want_term in r.get("jp_corrected", "") and want_term not in r.get("jp_vendor", ""):
                pool.append(r)
    # fall back to any regulatory contrastive pairs if the term filter is empty
    if not pool:
        pool = [r for r in corpus if r.get("primary_tag") == "terminology-regulatory"]
    seen, out = set(), []
    for r in pool:
        key = r["jp_corrected"][:16]
        if key in seen: continue
        seen.add(key); out.append(r)
        if len(out) >= k: break
    return out

# ── assemble the user-message context block (matches the prompt's contract) ────
def build_user_message(element, glossary_hits, tm_hits, exemplars, register):
    L = []
    L.append("SOURCE STRING")
    L.append(f'  element_id : {element["element_id"]}')
    L.append(f'  source_hash: {element["source_hash"]}')
    L.append(f'  text       : {element["text"]}')
    L.append("")

    L.append("LOCKED TERMINOLOGY (hard constraints — use the required rendering verbatim):")
    if glossary_hits:
        for g in glossary_hits:
            forb = f'   (NEVER {g["forbidden"]})' if g["forbidden"] else ""
            note = f' — {g["note"]}' if g["note"] else ""
            L.append(f'  • "{g["concept"]}" → {g["required"]}{forb}{note}')
    else:
        L.append("  (none triggered for this string)")
    L.append("")

    L.append("APPROVED TRANSLATIONS (translation memory — mirror this voice):")
    for t in tm_hits:
        L.append(f'  • [{t["id"]}] EN: {t["en"]}')
        L.append(f'             JA: {t["ja"]}')
    if not tm_hits: L.append("  (no close matches)")
    L.append("")

    L.append("CONTRASTIVE EXEMPLARS (✗ vendor miss → ✓ correct — avoid the miss):")
    for r in exemplars:
        rid = r.get("id") or r.get("pair_id") or f'ex_{hashlib.sha1(r["jp_corrected"].encode()).hexdigest()[:6]}'
        L.append(f'  • [{rid}] ✗ {r["jp_vendor"][:44]}')
        L.append(f'           ✓ {r["jp_corrected"][:44]}   [{r["primary_tag"]}]')
    if not exemplars: L.append("  (none retrieved)")
    L.append("")

    L.append("REGISTER / TIER SPEC:")
    L.append(f"  {register}")
    L.append("")
    L.append("Translate the SOURCE STRING now. Return ONLY the JSON output contract.")
    return "\n".join(L)

# ── expected output shape (what the agent must return — shown for verification) ─
def expected_output_skeleton(element, glossary_hits):
    return {
        "element_id": element["element_id"],
        "source_hash": element["source_hash"],
        "source_locale": "en",
        "target_locale": "ja",
        "target": "<agent fills — Japanese only>",
        "status": "draft",
        "confidence": None,
        "term_compliance": [
            {"concept": g["concept"], "required": g["required"], "used": True} for g in glossary_hits
        ],
        "flags": [],
        "rationale": "<agent fills>",
        "provenance": {
            "glossary_version": "astellas-pv.glossary.v0.1",
            "prompt_version": "loc-agent.v0.1",
            "exemplars_used": [],
            "tm_used": [],
        },
    }

def main():
    corpus = load_corpus()
    glossary = load_glossary()
    with open(SYSTEM_PROMPT, encoding="utf-8") as f:
        # ship only the paste-ready instruction (below the marker), not the doc wrapper
        doc = f.read()
    marker = "everything below the line is the agent's instruction)"
    system_text = doc.split(marker, 1)[-1].split("## HOW THIS PLUGS INTO", 1)[0].strip()

    # ── the query element (as it would arrive from element.content.text) ──
    src = "You must report product safety information to your Drug Safety Officer as soon as you become aware of it."
    element = {
        "element_id": "ele_ast009_s04_stmt_012",
        "source_hash": "sha256:" + hashlib.sha256(src.encode()).hexdigest(),
        "text": src,
    }
    register = ("Formal です・ます; healthcare-professional audience; refer to patients as 患者さん; "
                "keep official English document/program names untranslated. Tier 1 (safety-critical) — full human review.")

    gloss = retrieve_glossary(element["text"], glossary)
    tm    = retrieve_tm(element["text"])
    ex    = retrieve_exemplars(element["text"], corpus)

    user_text = build_user_message(element, gloss, tm, ex, register)
    payload = {
        "model": "azure-openai:<deployment>",
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user",   "content": user_text},
        ],
    }

    with open(os.path.join(HERE, "agent_call_payload.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # ── trace so you can SEE the retrieval + the assembled call ──
    print("=" * 78)
    print("RETRIEVAL TRACE")
    print("=" * 78)
    print(f'query element : {element["element_id"]}')
    print(f'source_hash   : {element["source_hash"][:23]}…')
    print(f'[1] glossary  : {[g["concept"] for g in gloss]}  → {[g["required"] for g in gloss]}')
    print(f'[2] TM        : {[t["id"] for t in tm]}')
    print(f'[3] exemplars : {len(ex)} pulled  (corpus size {len(corpus)})')
    print()
    print("=" * 78)
    print("SYSTEM MESSAGE (first 400 chars of the paste-ready instruction)")
    print("=" * 78)
    print(system_text[:400] + " …")
    print()
    print("=" * 78)
    print("USER MESSAGE (the per-string assembled context)")
    print("=" * 78)
    print(user_text)
    print()
    print("=" * 78)
    print("EXPECTED OUTPUT SHAPE (what the agent must return)")
    print("=" * 78)
    print(json.dumps(expected_output_skeleton(element, gloss), ensure_ascii=False, indent=2))
    print()
    print(f'→ full payload written to agent_call_payload.json '
          f'({os.path.getsize(os.path.join(HERE, "agent_call_payload.json"))} bytes)')

if __name__ == "__main__":
    main()
