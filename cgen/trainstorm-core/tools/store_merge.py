#!/usr/bin/env python3
"""
Shared, idempotent merge of an authored decomposition into a project atom store.

Every headwater ingest script is a SERIALISER of an authored decomposition, and every one of them
must be re-runnable without destroying what reconcile/approval wrote afterwards. That rule lived
inside headwater_ingest.py; the moment a second ingest script existed it would have been copied,
and a copied rule is a rule that drifts. So it lives here once and both scripts import it.

The rule (see decision-log 2026-08-19):
  authored text unchanged since last ingest -> STORE WINS   (a downstream mode advanced it)
  authored text changed                     -> INGEST WINS  (corpus/authoring moved): new meaning,
                                               version bumped from the store, status -> draft,
                                               approvals cleared
  atom_id absent from the store             -> MINT at v1/draft
  in the store but no longer authored       -> ORPHAN: kept and reported (prune=True to remove)

"What the last ingest authored" is external, atom_id-keyed provenance in ingest_log.json — the same
reference-don't-embed move as reconciliation_log.json, and for the same reason: atom.schema.json is
additionalProperties:false at the top level and inside governance, so there is no field for it.
"""
import json, hashlib

ORDER = ["atom_id", "content_hash", "meaning", "bindings", "governance"]


def stamp(atoms):
    """content_hash every atom from its meaning, and order keys for a clean, diffable store."""
    for a in atoms:
        payload = json.dumps(a["meaning"], sort_keys=True, ensure_ascii=False).encode("utf-8")
        a["content_hash"] = "sha256:" + hashlib.sha256(payload).hexdigest()
        ordered = {k: a[k] for k in ORDER if k in a}
        a.clear(); a.update(ordered)
    return atoms


def merge(store, authored, corpus, project, owns=("object",), prune=False):
    """Merge `authored` into store/atoms.json. Returns (atoms, report, ingest_log, bootstrap).

    `owns` names the binding keys THIS writer owns (single-writer). Bindings are merged key by key:
    owned keys are taken from the authored decomposition, every other key is preserved from the
    store. Without that, a re-ingest would silently erase another facet owner's work (Cartographer's
    `intent`, Couturier's `expression`) — a single-writer violation committed by the merge itself.

    Note the two independent axes. `content_hash` covers MEANING only, so a facet re-binding with
    unchanged text produces an identical hash; keying the whole merge on it would silently drop
    every binding correction. Meaning divergence is ambiguous (SME or corpus?) and needs the log to
    resolve; a binding change is not ambiguous, because exactly one writer owns each key.
    """
    ap = store / "atoms.json"
    prior = {a["atom_id"]: a for a in json.loads(ap.read_text())} if ap.exists() else {}

    il = store / "ingest_log.json"
    if il.exists():
        prev = json.loads(il.read_text()).get("authored", {})
        bootstrap = False
    else:
        # First run under the merge rule: no record of what the last ingest authored. Assume the
        # store IS the last ingest's output (true wherever nothing has advanced it yet). The caller
        # is expected to say so on stdout — stated loudly rather than assumed silently.
        prev = {aid: a.get("content_hash") for aid, a in prior.items()}
        bootstrap = True

    merged, rep = [], {"minted": [], "preserved": [], "updated": [], "rebound": [], "orphan": []}
    now = {}
    for a in authored:
        aid, h = a["atom_id"], a["content_hash"]
        now[aid] = h
        was = prior.get(aid)
        if was is None:
            merged.append(a); rep["minted"].append(aid); continue
        if prev.get(aid) == h:
            # meaning: this run authored what the last run authored, so any divergence in the store
            # came from downstream — keep the store's meaning/hash.
            keep = dict(was)
            newb = dict(was.get("bindings", {}))
            for k in owns:
                if k in a.get("bindings", {}):
                    newb[k] = a["bindings"][k]
                else:
                    newb.pop(k, None)
            rebound = newb != was.get("bindings", {})
            if rebound:
                keep["bindings"] = newb
                g = dict(keep.get("governance", {}))
                g["version"] = int(g.get("version", 1)) + 1
                g["status"] = "draft"        # a facet re-binding on a controlled doc needs re-review
                g.pop("approved_by", None); g.pop("effective_date", None)
                keep["governance"] = g
                rep["rebound"].append(aid)
            merged.append(keep)
            if was.get("content_hash") != h and not rebound:
                rep["preserved"].append(aid)
            elif was.get("content_hash") != h:
                rep["preserved"].append(aid)
            continue
        newb = dict(was.get("bindings", {}))
        for k in list(newb):
            if k in owns and k not in a.get("bindings", {}):
                newb.pop(k)
        newb.update({k: v for k, v in a.get("bindings", {}).items() if k in owns})
        a["bindings"] = newb
        g = was.get("governance", {})
        a["governance"]["version"] = int(g.get("version", 1)) + 1
        a["governance"]["status"] = "draft"          # meaning moved; re-approval required
        a["governance"].pop("approved_by", None)
        a["governance"].pop("effective_date", None)
        merged.append(a); rep["updated"].append(aid)

    for aid, was in prior.items():
        if aid not in now:
            rep["orphan"].append(aid)
            if not prune:
                merged.append(was)
                now[aid] = prev.get(aid, was.get("content_hash"))

    pos = {aid: i for i, aid in enumerate(now)}
    merged.sort(key=lambda a: pos.get(a["atom_id"], 10 ** 6))

    log = {
        "_note": "External ingest-provenance store, keyed by atom_id: the content_hash this ingest "
                 "AUTHORED on its last run. Lets a re-ingest tell 'the corpus changed' (authored "
                 "hash moved) from 'a downstream mode advanced this atom' (authored hash steady, "
                 "store hash moved) and preserve the latter. Reference, don't embed.",
        "project": project, "corpus": corpus, "authored": now,
    }
    return merged, rep, log, bootstrap


def write(store, atoms, log, files=None):
    store.mkdir(parents=True, exist_ok=True)
    (store / "atoms.json").write_text(json.dumps(atoms, indent=2, ensure_ascii=False))
    (store / "ingest_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False))
    for name, payload in (files or {}).items():
        (store / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def report(atoms, store, rep, bootstrap):
    if bootstrap:
        print("NOTE: no ingest_log.json — bootstrapping from the existing store "
              "(assuming it is the last ingest's output).")
    print(f"Wrote {len(atoms)} atoms to {store/'atoms.json'}")
    print(f"  merge: {len(rep['minted'])} minted, {len(rep['updated'])} updated (source changed), "
          f"{len(rep['rebound'])} rebound (facet changed, meaning intact), "
          f"{len(rep['preserved'])} preserved (downstream advanced), {len(rep['orphan'])} orphan")
    for k in ("updated", "rebound", "preserved", "orphan"):
        for aid in rep[k]:
            print(f"    {k.upper():9} {aid}")
