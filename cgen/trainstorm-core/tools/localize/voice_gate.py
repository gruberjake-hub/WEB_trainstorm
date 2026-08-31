#!/usr/bin/env python3
"""
voice_gate.py — the deterministic INVENT-GUARD for Dragoman's voice mode (voice-agent.v0.1).

Runs on a proposals store (voice/proposals/<register>.json) BEFORE a human reviews it: the
mechanical class of voice failures, enforced not hoped. Checks per draft:

    BRIGHT LINE   — status is "draft"; the writer never self-accepts.
    ANCHOR        — the echoed source_hash matches the atom's CURRENT content_hash (stale = red).
    INVARIANTS    — no number/date token in the rendering that this atom's text does not carry
                    (a figure found elsewhere in the project store passes with a NOTE — imported
                    from a sibling atom is governed meaning, but the human should see it moved).
    NAMES         — no capitalized content word absent from this atom (case-insensitive; sibling-
                    atom fallback notes, as above; second-person/function words are exempt).
    DISCIPLINE    — flags use the governed taxonomy; confidence is honest arithmetic (0–1).

Honest limit, stated wherever this gate is cited (the prompt_purity.py framing): this catches
imported facts with COUNTABLE SURFACE FORMS — figures, dates, names. It does not catch paraphrased
invention ("your pay will go up"). That residue is what human acceptance is for; the writer's
flags are its triage signal.

Beat copy (arc hop two) is gated by the INVERSE guard — gate_beat_proposals: beat copy is
content-free BY CONTRACT, so the check inverts: ZERO digits anywhere (a figure in a welcome is a
claim that belongs to an atom), and no capitalized content word that is not sentence-initial,
exempt, in the project corpus, or in the arc allowlist (lesson titles + scene headings/kickers +
client/project names). Its anchor is the beat's beat_hash (validate_arc.py), not an atom hash.
Honest limits, both guards, stated plainly: the atom guard catches imported facts with countable
surface forms, not paraphrased invention; the inverse guard cannot catch a claim built from
ordinary lowercase words ("your pay will rise") or a name at sentence start — human acceptance
remains the meaning gate, the writer's flags its triage.

    python3 tools/localize/voice_gate.py --project ../brunswick/projects/paytrans   # gate real proposals
    python3 tools/localize/voice_gate.py --selftest                                  # fixtures, proves red
"""
import argparse, hashlib, json, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))          # tools/ — for harness_paths
import harness_paths
from validate_arc import beat_hash  # one anchor definition — never copied

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--core"); ap.add_argument("--project"); ap.add_argument("--selftest", action="store_true")
args, _ = ap.parse_known_args()

P = harness_paths.resolve_core(args.core)
vocab = json.loads((P["vocab_dir"] / "register.enum.json").read_text(encoding="utf-8"))
GOVERNED = {v["id"]: v for v in vocab["values"]}
FLAG_CATEGORIES = {"invented-risk", "compression-loss", "register", "ambiguous-source",
                   "defined-name", "verbatim-kept"}
SEVERITIES = {"low", "med", "high"}

# Function/second-person words a warm_direct rendering legitimately capitalizes with no source.
EXEMPT = {"you", "your", "you're", "you'll", "yours", "we", "our", "ours", "it", "it's", "its",
          "what", "how", "why", "when", "where", "who", "this", "that", "these", "those", "the",
          "a", "an", "and", "or", "but", "if", "so", "not", "no", "yes", "here", "there", "is",
          "are", "was", "will", "can", "do", "does", "don't", "doesn't", "let's", "to", "of",
          "in", "on", "at", "for", "with", "from", "by", "as", "one", "gets", "get", "got", "means",
          "behind", "every", "everything", "more", "than", "just", "all", "have", "has", "had",
          "that's", "we're", "they're", "there's", "what's", "who's", "here's", "each", "both",
          "now", "then", "only", "also", "some", "most", "any"}

NUM_RE = re.compile(r"\d[\dKk,./()%-]*")
CAP_RE = re.compile(r"\b[A-Z][A-Za-z'()\-\d]*\b")


def sha(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def invariant_findings(text, atom_text, corpus_text, sentence_starters=False):
    """Returns (fails, notes): tokens absent from the atom; notes = found in a sibling atom.
    sentence_starters=True exempts sentence-initial capitals (track prose — the same documented
    limit the inverse guard carries; numbers are NEVER exempted)."""
    fails, notes = [], []
    starters = set(_SENT_START.findall(text)) if sentence_starters else set()
    def present(token, hay):        # whole-token, case-insensitive — substring matching once
        return bool(re.search(r"(?<![A-Za-z0-9])" + re.escape(token) + r"(?![A-Za-z0-9])", hay, re.I))
        # let 'one' hide inside 'zones'; never again
    for tok in NUM_RE.findall(text):
        t = tok.strip(",.()-")
        if not t or present(t, atom_text):
            continue
        (notes if present(t, corpus_text) else fails).append(f"number '{t}'")
    for tok in CAP_RE.findall(text):
        t = tok.strip("'")
        if t.lower() in EXEMPT or t in starters or any(c.isdigit() for c in t) or present(t, atom_text):
            continue
        (notes if present(t, corpus_text) else fails).append(f"name '{t}'")
    return sorted(set(fails)), sorted(set(notes))


def build_arc_allowlist(proj: "pathlib.Path") -> str:
    """Names beat copy may use without them being in the corpus: lesson titles, scene
    headings/kickers, project + client names. Data-derived — no hand-kept list to drift."""
    parts = [proj.name, proj.parent.parent.name if len(proj.parts) >= 3 else ""]
    occ = proj / "occurrences"
    try:
        lessons = json.loads((occ / "lessons.json").read_text(encoding="utf-8"))
        parts += [l.get("title", "") for l in lessons.get("lessons", [])]
    except FileNotFoundError:
        pass
    try:
        scenes = json.loads((occ / "scenes.json").read_text(encoding="utf-8"))
        parts += [f"{s.get('heading','')} {s.get('kicker','')}" for s in scenes.get("scenes", [])]
    except FileNotFoundError:
        pass
    return " ".join(parts)


_SENT_START = re.compile(r"(?:^|[.!?…]\s+|—\s+|:\s+|\n\s*)([A-Z][A-Za-z'\-]*)")


def inverse_findings(text, corpus_text, allow_text):
    """The inverse guard: beat copy proves it carries NOTHING. Zero digits; capitalized content
    words only if sentence-initial, exempt, in the corpus, or in the arc allowlist."""
    fails = []
    def present(token, hay):
        return bool(re.search(r"(?<![A-Za-z0-9])" + re.escape(token) + r"(?![A-Za-z0-9])", hay, re.I))
    for tok in NUM_RE.findall(text):
        fails.append(f"figure '{tok.strip(',.()-')}' — beat copy carries no figures, ever")
    starters = set(_SENT_START.findall(text))
    for tok in CAP_RE.findall(text):
        t2 = tok.strip("'")
        if t2.lower() in EXEMPT or t2 in starters:
            continue
        if present(t2, corpus_text) or present(t2, allow_text):
            continue
        fails.append(f"name '{t2}'")
    return sorted(set(fails))


def gate_beat_proposals(name, store, beats_by_id, corpus_text, allow_text, results):
    for bid, p in (store.get("beat_proposals") or {}).items():
        tag = f"{name}: {bid}"
        if p.get("status") != "draft":
            results.append((f"{tag} status is draft (bright line)", False,
                            f"writer emitted {p.get('status')!r}"))
            continue
        beat = beats_by_id.get(bid)
        if beat is None:
            results.append((f"{tag} keys a real beat", False, "no such beat in the catalog"))
            continue
        if p.get("source_hash") != beat_hash(beat):
            results.append((f"{tag} beat_hash anchor is fresh", False,
                            "placement/intent moved — copy is STALE"))
            continue
        fails = inverse_findings(p.get("text", ""), corpus_text, allow_text)
        results.append((f"{tag} inverse guard (claim-free proven)", not fails, "; ".join(fails)))
        bad_flags = [f for f in p.get("flags", [])
                     if f.get("category") not in FLAG_CATEGORIES or f.get("severity") not in SEVERITIES]
        conf = p.get("confidence")
        disciplined = not bad_flags and isinstance(conf, (int, float)) and 0.0 <= conf <= 1.0
        results.append((f"{tag} flag/confidence discipline", disciplined,
                        "" if disciplined else "ungoverned flag category/severity or bad confidence"))


def gate_track_proposals(name, store, atoms_by_id, beats_by_id, voice_pack, corpus_text, results):
    """Narration tracks (narrate-agent.v0.1): draft-only bright line; every pin fresh (atom
    content_hash / beat_hash); invariants checked against the UNION of pinned sources — atom
    text + its accepted voice rendering + woven beat copy. Connective-tissue claims built from
    ordinary words are the documented limit; the writer's flags carry them to the human."""
    entries = (voice_pack or {}).get("entries") or {}
    beat_copy = (voice_pack or {}).get("beats") or {}
    for sid, tr in (store.get("track_proposals") or {}).items():
        tag = f"{name}: track {sid}"
        if tr.get("status") != "draft":
            results.append((f"{tag} status is draft (bright line)", False,
                            f"writer emitted {tr.get('status')!r}"))
            continue
        union_parts, stale, missing = [], [], []
        for key, pinned in (tr.get("sources") or {}).items():
            if key.startswith("bt_"):
                beat = beats_by_id.get(key)
                if beat is None:
                    missing.append(key); continue
                if pinned != beat_hash(beat):
                    stale.append(key); continue
                bc = beat_copy.get(key)
                if bc:
                    union_parts.append(bc.get("text") or "")
            else:
                atom = atoms_by_id.get(key)
                if atom is None:
                    missing.append(key); continue
                if pinned != atom["content_hash"]:
                    stale.append(key); continue
                union_parts.append(atom["meaning"]["source_text"])
                ve = entries.get(key)
                if ve:
                    union_parts.append(ve.get("text") or "")
        results.append((f"{tag} pins resolve", not missing, ", ".join(missing)))
        results.append((f"{tag} pins are fresh", not stale,
                        "; ".join(f"{k} — source moved, track STALE" for k in stale)))
        if missing or stale:
            continue
        union = " ".join(union_parts)
        fails, notes = invariant_findings(tr.get("text", ""), union, corpus_text, sentence_starters=True)
        detail = ("; ".join(fails) + (f"  [corpus: {'; '.join(notes)}]" if notes else "")) if fails                  else (f"[corpus: {'; '.join(notes)}]" if notes else "")
        results.append((f"{tag} union invariants", not fails, detail))
        bad_flags = [f for f in tr.get("flags", [])
                     if f.get("category") not in FLAG_CATEGORIES or f.get("severity") not in SEVERITIES]
        conf = tr.get("confidence")
        disciplined = not bad_flags and isinstance(conf, (int, float)) and 0.0 <= conf <= 1.0
        results.append((f"{tag} flag/confidence discipline", disciplined,
                        "" if disciplined else "ungoverned flag category/severity or bad confidence"))


def gate_proposals(name, store, atoms_by_id, corpus_text, results):
    reg = store.get("register")
    results.append((f"{name}: register '{reg}' is governed", reg in GOVERNED, ""))
    for aid, p in store.get("proposals", {}).items():
        tag = f"{name}: {aid}"
        if p.get("status") != "draft":
            results.append((f"{tag} status is draft (bright line)", False,
                            f"writer emitted {p.get('status')!r}"))
            continue
        if aid not in atoms_by_id:
            results.append((f"{tag} keys a real atom", False, "no such atom"))
            continue
        atom = atoms_by_id[aid]
        if p.get("source_hash") != atom["content_hash"]:
            results.append((f"{tag} anchor is fresh", False, "meaning moved — draft is STALE"))
            continue
        fails, notes = invariant_findings(p.get("text", ""), atom["meaning"]["source_text"], corpus_text)
        detail = ("; ".join(fails) + (f"  [sibling-atom: {'; '.join(notes)}]" if notes else "")) if fails \
                 else (f"[sibling-atom: {'; '.join(notes)}]" if notes else "")
        results.append((f"{tag} invariants", not fails, detail))
        bad_flags = [f for f in p.get("flags", [])
                     if f.get("category") not in FLAG_CATEGORIES or f.get("severity") not in SEVERITIES]
        conf = p.get("confidence")
        disciplined = not bad_flags and isinstance(conf, (int, float)) and 0.0 <= conf <= 1.0
        results.append((f"{tag} flag/confidence discipline", disciplined,
                        "" if disciplined else "ungoverned flag category/severity or bad confidence"))


def report(results):
    print(f"{'CHECK':<74} RESULT")
    print("-" * 90)
    ok = True
    for nm, passed, detail in results:
        ok = ok and passed
        print(f"{nm:<74} {'PASS' if passed else 'FAIL'}   {detail}")
    print("-" * 90)
    print("ALL PASS" if ok else "SOME FAILED")
    return ok


# ---------------------------------------------------------------- selftest

if __name__ == "__main__" and args.selftest:
    A1 = {"atom_id": "atom_fx_grades", "content_hash": None,
          "meaning": {"source_text": "Brunswick uses a grade structure with 24 pay ranges tied to market rates."}}
    A1["content_hash"] = sha(A1["meaning"]["source_text"])
    A2 = {"atom_id": "atom_fx_zones", "content_hash": None,
          "meaning": {"source_text": "The structure has 3 geographic zones reflecting cost of labor."}}
    A2["content_hash"] = sha(A2["meaning"]["source_text"])
    ATOMS = {a["atom_id"]: a for a in (A1, A2)}
    CORPUS = " ".join(a["meaning"]["source_text"] for a in ATOMS.values())
    good = {"register": "warm_direct", "proposals": {
        "atom_fx_grades": {"text": "Your pay range is one of 24 — each tied to real market rates.",
                            "status": "draft", "source_hash": A1["content_hash"], "confidence": 0.8,
                            "flags": [{"span": "real", "category": "invented-risk", "severity": "low",
                                        "note": "'real' is emphasis, not a new claim — confirm"}],
                            "rationale": "re-addressed to second person"}}}
    results = []
    gate_proposals("fixture(good)", good, ATOMS, CORPUS, results)
    base_ok = all(ok for _, ok, _ in results)
    results.append(("selftest: clean fixture passes", base_ok, ""))

    def red(label, mutate):
        s = json.loads(json.dumps(good))
        atoms = {k: json.loads(json.dumps(v)) for k, v in ATOMS.items()}   # deep copy — reds must not bleed
        mutate(s, atoms)
        scratch = []
        gate_proposals("fixture(red)", s, atoms, CORPUS, scratch)
        caught = any(not ok for _, ok, _ in scratch)
        results.append((label, caught, "" if caught else "mutation was NOT caught"))

    red("selftest: invented number is caught",
        lambda s, a: s["proposals"]["atom_fx_grades"].update(text="Your pay range is one of 25 across the company."))
    red("selftest: invented name is caught",
        lambda s, a: s["proposals"]["atom_fx_grades"].update(text="Check Workday for your range — one of 24."))
    red("selftest: sibling-atom fact passes with a note, absent fact fails",
        lambda s, a: s["proposals"]["atom_fx_grades"].update(text="Your range sits in one of 3 zones, says Mercer."))
    red("selftest: self-accepted status is caught (bright line)",
        lambda s, a: s["proposals"]["atom_fx_grades"].update(status="accepted"))
    red("selftest: stale anchor is caught",
        lambda s, a: a["atom_fx_grades"].update(content_hash=sha("changed meaning")))
    red("selftest: ungoverned flag category is caught",
        lambda s, a: s["proposals"]["atom_fx_grades"]["flags"].append(
            {"span": "x", "category": "style-note", "severity": "low", "note": "n"}))
    # the sibling-atom NOTE path must also be visible on a passing entry
    s2 = json.loads(json.dumps(good))
    s2["proposals"]["atom_fx_grades"]["text"] = "One of 24 ranges, across 3 zones."
    scratch = []
    gate_proposals("fixture(note)", s2, ATOMS, CORPUS, scratch)
    inv = [r for r in scratch if "invariants" in r[0]][0]
    results.append(("selftest: sibling-atom import passes WITH a visible note",
                    inv[1] and "sibling-atom" in inv[2], inv[2]))

    # ── inverse guard (arc hop two): beat copy proves it carries nothing ──
    BEAT = {"beat_id": "bt_fx_welcome", "placement": {"type": "lesson_start"},
            "intent": {"pedagogical": "hook"}, "status": "accepted", "from": "fx"}
    BEATS = {"bt_fx_welcome": BEAT}
    ALLOW = "Pay Transparency at Fixture — How Your Pay Works fixture-client"
    bgood = {"register": "warm_direct", "beat_proposals": {
        "bt_fx_welcome": {"text": "Welcome — this is about your pay, and what it means for you.",
                           "status": "draft", "source_hash": beat_hash(BEAT), "confidence": 0.8,
                           "flags": [], "rationale": "hook; claim-free"}}}
    n1 = len(results)
    gate_beat_proposals("fixture(beat)", bgood, BEATS, CORPUS, ALLOW, results)
    results.append(("selftest(beat): claim-free welcome passes the inverse guard",
                    all(ok for _, ok, _ in results[n1:]), ""))

    def bred(label, mutate):
        s = json.loads(json.dumps(bgood)); beats = {"bt_fx_welcome": json.loads(json.dumps(BEAT))}
        mutate(s, beats)
        scratch = []
        gate_beat_proposals("fixture(beat-red)", s, beats, CORPUS, ALLOW, scratch)
        caught = any(not ok for _, ok, _ in scratch)
        results.append((label, caught, "" if caught else "mutation was NOT caught"))

    bred("selftest(beat): ANY figure in beat copy is caught",
         lambda s, b: s["beat_proposals"]["bt_fx_welcome"].update(
             text="Welcome — all 24 pay ranges explained, for you."))
    bred("selftest(beat): an invented mid-sentence name is caught",
         lambda s, b: s["beat_proposals"]["bt_fx_welcome"].update(
             text="Welcome — your pay, explained with data from Mercer."))
    bred("selftest(beat): stale beat_hash (placement moved) is caught",
         lambda s, b: b["bt_fx_welcome"].update(placement={"type": "lesson_end"}))
    bred("selftest(beat): copy for a beat not in the catalog is caught",
         lambda s, b: b.clear())
    bred("selftest(beat): self-accepted beat copy is caught (bright line)",
         lambda s, b: s["beat_proposals"]["bt_fx_welcome"].update(status="accepted"))
    # the documented limit, demonstrated honestly: sentence-initial name slips the name check
    slip = {"register": "warm_direct", "beat_proposals": {
        "bt_fx_welcome": {"text": "Mercer welcomes you to this course about your pay.",
                           "status": "draft", "source_hash": beat_hash(BEAT), "confidence": 0.5,
                           "flags": [], "rationale": ""}}}
    scratch = []
    gate_beat_proposals("fixture(limit)", slip, BEATS, CORPUS, ALLOW, scratch)
    results.append(("selftest(beat): sentence-initial name slips — the DOCUMENTED limit "
                    "(human acceptance is the meaning gate)",
                    all(ok for _, ok, _ in scratch), "limit unexpectedly caught — update the docs"))

    # ── track / union guard (Griot hop one) ──
    TB = {"beat_id": "bt_fx_welcome", "placement": {"type": "lesson_start"},
          "intent": {"pedagogical": "hook"}, "status": "accepted", "from": "fx"}
    TBEATS = {"bt_fx_welcome": TB}
    TVPACK = {"entries": {"atom_fx_grades": {"text": "Your pay range is one of 24.",
                                              "status": "accepted", "reviewer": "t",
                                              "source_hash": A1["content_hash"]}},
              "beats": {"bt_fx_welcome": {"text": "Welcome, this is for you.",
                                           "status": "accepted", "reviewer": "t",
                                           "source_hash": beat_hash(TB)}}}
    tgood = {"register": "warm_direct", "track_proposals": {
        "sc_one": {"text": "Welcome, this is for you. Your pay range is one of 24 — set against market rates, in one of 3 zones.",
                    "status": "draft", "confidence": 0.8, "flags": [],
                    "sources": {"atom_fx_grades": A1["content_hash"],
                                 "atom_fx_zones": A2["content_hash"],
                                 "bt_fx_welcome": beat_hash(TB)}}}}
    n2 = len(results)
    gate_track_proposals("fixture(track)", tgood, ATOMS, TBEATS, TVPACK, CORPUS, results)
    results.append(("selftest(track): union-anchored flowing track passes",
                    all(ok for _, ok, _ in results[n2:]), ""))

    def tred(label, mutate):
        s = json.loads(json.dumps(tgood))
        atoms = {k: json.loads(json.dumps(v)) for k, v in ATOMS.items()}
        beats = {k: json.loads(json.dumps(v)) for k, v in TBEATS.items()}
        mutate(s, atoms, beats)
        scratch = []
        gate_track_proposals("fixture(track-red)", s, atoms, beats, TVPACK, CORPUS, scratch)
        caught = any(not ok for _, ok, _ in scratch)
        results.append((label, caught, "" if caught else "mutation was NOT caught"))

    tred("selftest(track): a figure NO pinned source carries is caught",
         lambda s, a, b: s["track_proposals"]["sc_one"].update(
             text="Your pay range is one of 25, in one of 3 zones."))
    tred("selftest(track): a stale atom pin is caught",
         lambda s, a, b: a["atom_fx_grades"].update(content_hash=sha("moved meaning")))
    tred("selftest(track): a stale beat pin (placement moved) is caught",
         lambda s, a, b: b["bt_fx_welcome"].update(placement={"type": "lesson_end"}))
    tred("selftest(track): a pin naming nothing is caught",
         lambda s, a, b: s["track_proposals"]["sc_one"]["sources"].update(atom_fx_ghost="sha256:" + "0" * 64))
    tred("selftest(track): self-accepted track is caught (bright line)",
         lambda s, a, b: s["track_proposals"]["sc_one"].update(status="accepted"))
    sys.exit(0 if report(results) else 1)

# ---------------------------------------------------------------- project mode

if __name__ == "__main__":       # importers take invariant_findings/GOVERNED/sha; only the CLI runs
    PP = harness_paths.resolve()
    proj = PP["project_dir"]
    atoms_list = json.loads((proj / "atoms.json").read_text(encoding="utf-8"))
    atoms_by_id = {a["atom_id"]: a for a in (atoms_list["atoms"] if isinstance(atoms_list, dict) else atoms_list)}
    corpus_text = " ".join(a["meaning"]["source_text"] for a in atoms_by_id.values())
    props_dir = proj / "voice" / "proposals"
    files = sorted(props_dir.glob("*.json")) if props_dir.exists() else []
    results = []
    if not files:
        results.append(("no voice proposals in project — nothing to gate", True, f"looked in {props_dir}"))
    beats_p = proj / "occurrences" / "beats.json"
    beats_by_id = {}
    if beats_p.exists():
        beats_by_id = {b["beat_id"]: b for b in
                       json.loads(beats_p.read_text(encoding="utf-8")).get("beats", [])}
    allow_text = build_arc_allowlist(proj)
    vpack_p = proj / "voice" / f"{'warm_direct'}.json"
    voice_packs = {vp.stem: json.loads(vp.read_text(encoding="utf-8"))
                   for vp in (proj / "voice").glob("*.json")}
    for f in files:
        store = json.loads(f.read_text(encoding="utf-8"))
        gate_proposals(f.name, store, atoms_by_id, corpus_text, results)
        gate_beat_proposals(f.name, store, beats_by_id, corpus_text, allow_text, results)
        gate_track_proposals(f.name, store, atoms_by_id, beats_by_id,
                             voice_packs.get(store.get("register") or ""), corpus_text, results)
    sys.exit(0 if report(results) else 1)
