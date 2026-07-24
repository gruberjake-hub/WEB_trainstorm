#!/usr/bin/env python3
"""
Promote staging records -> real registry entries.

CONFIRMED RULE (Jake, 2026-07-23), overriding the ingest script's proposal:
    A client token in the filename means DO NOT TRAVEL — full stop.
    Category is irrelevant to scope. "stock_brunswick" is as locked as
    "Logo_Brunswick", because much of that imagery is derived from or pulled
    out of the client's own database, not generic stock.

    -> client token present  => scope.clients = [client]
    -> "general" / no token  => scope universal, EXCEPT where held back below.

Category still drives ROLE (what kind of asset it is), just not scope.

HELD BACK (not promoted; land in unresolved.json instead):
    - third-party regulatory marks (FDA/EMA/PMDA) — not ours, not the client's,
      and usable only on a legal call nobody has made yet
    - the E2E project mark — ownership unknown to me

Everything promoted enters at governance.status = "draft". The compiler's
approval gate means nothing here is servable until a human signs it off.
"""
import json
import re
from collections import Counter
from pathlib import Path

KNOWN_CLIENTS = {"brunswick", "astellas", "abbvie"}

# Program / project codenames that identify a client without naming them.
# These carry the SAME locking force as an explicit client token — a codename is
# still a client tie, it just isn't spelled out. Extend as more surface.
CLIENT_ALIASES = {
    "e2e": "astellas",      # E2E Operating Model / Asset Maximization — Astellas program
    "alsap": "astellas",
}

# category token -> role. Ordered: first match wins.
ROLE_RULES = [
    (("logo", "brand", "logos"),                                  "signature"),
    (("button", "nav"),                                           "chrome"),
    (("background", "abstract"),                                  "chrome"),
    (("icon",),                                                   "motif"),
    (("stock", "people", "contextual", "misc",
      "computer-perspective", "computer-monitor", "dualmonitor",
      "eu", "lifecycle-management-image", "magnifying-glass"),     "motif"),
]

# filename fragments that must NOT be auto-promoted
HOLD_BACK: dict[str, str] = {}

# filename fragment -> industry scope. Not client-owned, but not universal either:
# usable across any client in the industry, invisible to clients outside it.
INDUSTRY_RULES = {
    "icon_health-authority_logo": ["pharma"],
}

# third-party marks: neither ours nor the client's. Recorded explicitly so whoever
# approves them knows what they are signing off on.
THIRD_PARTY_MARKS = {
    "icon_health-authority_logo": (
        "Third-party regulatory agency mark. Scoped to pharma by Jake's decision "
        "(2026-07-23); the regulatory/endorsement question is deliberately left to "
        "human review at approval time, not resolved here. Status stays draft until then."
    ),
}

# specific agency identifications, where established. Left absent where not —
# these are NOT guessed, because a mislabelled agency mark is worse than an unlabelled one.
AGENCY_IDENTIFIED = {
    "icon_health-authority_logo (1).png": "PMDA — Pharmaceuticals and Medical Devices Agency (Japan)",
    "icon_health-authority_logo (2).png": "EMA — European Medicines Agency",
}

NOISE_TOKENS = {"png", "jpg", "jpeg", "jfif", "svg", "v2", "1", "2", "3", "flat",
                "transparent", "transback", "logoonly", "primary"}


# --- mark_class -------------------------------------------------------------
# `role: signature` says "this is a high-specificity mark". It does NOT say
# whose authority it carries. Without this, a program logo is indistinguishable
# from the client's corporate identity — ask for "the Astellas logo" and E2E is
# an equally valid answer.
#
# DERIVED where the filename genuinely carries the signal; OVERRIDDEN by an
# explicit table where it took OCR or a human to tell. Rules for the mechanical
# part, a table for the judgment part — the same split as role and scope.

MARK_CLASS_RULES = [
    # (filename predicate, mark_class)
    (lambda f: f.startswith("icon_health-authority"),            "third_party"),
    (lambda f: any(p in f.lower() for p in ("e2e", "alsap")),     "program"),
    # Capital-L "Logo_<Client>_..." is the deliberately-named corporate mark;
    # the harvested "logo_brand_<client> (N)" pile is not.
    (lambda f: re.match(r"^Logo_(Brunswick|Astellas|AbbVie)_", f) is not None, "identity"),
]

# Established by OCR of the image itself — the filename gave no signal.
MARK_CLASS_OVERRIDES = {
    "logo_brand_brunswick (1).jpg":  "program",   # "BRUNSWICK Achieve — Performance Management"
    "logo_brand_brunswick (15).png": "program",   # same Achieve program lockup
    "logo_brand_brunswick (16).png": "program",   # "BRUNSWICK Performance Management for Success"
}

# Safe default for the remaining harvested pile. Deliberately sub_brand, not
# identity: several are confirmed Brunswick subsidiaries (Mercury, Simrad,
# Attwood, Boateka, Veer, ProMariner, Boston Whaler, Spartan), and the two real
# corporate marks carry different filenames. Under-claiming authority is the
# safe direction of error; over-claiming is the failure this field prevents.
MARK_CLASS_DEFAULT_FOR_HARVESTED = "sub_brand"


# --- asset roots ------------------------------------------------------------
# Two stores, because the two kinds of asset genuinely differ:
#   library — 404 MB of churning content on Dropbox. Absolute path, machine-
#             specific, overridable via TRAINSTORM_ASSET_ROOT.
#   brand   — a few hundred KB of corporate identity marks, in the repo beside
#             tokens/fonts. RELATIVE, and therefore portable with no env var:
#             it travels with the clone. That portability is a direct payoff of
#             keeping them in git rather than in the bulk store.
ASSET_ROOTS = {
    "library": "F:/Dropbox/3a-Brainstorm/_TRAINSTORM-local/__ASSETS/",
    "brand": "../../brands/",
}
DEFAULT_ROOT = "library"

# Only mark_class == "identity" earns a place in the brand folders. sub_brand,
# program and third_party marks stay in the library — they are engagement
# ephemera or somebody else's IP, not the client's standing brand contract.
BRAND_FOLDER = "{client}/assets/"


def decide_mark_class(fname: str, role: str) -> str | None:
    if role != "signature":
        return None
    if fname in MARK_CLASS_OVERRIDES:
        return MARK_CLASS_OVERRIDES[fname]
    for predicate, value in MARK_CLASS_RULES:
        if predicate(fname):
            return value
    if fname.lower().startswith("logo_brand_"):
        return MARK_CLASS_DEFAULT_FOR_HARVESTED
    return None


def tokens_of(stem: str) -> list[str]:
    stem = re.sub(r"\s*\(\d+\)\s*$", "", stem)
    return [t for t in re.split(r"[_\s.]+", stem.lower()) if t]


def decide_role(toks: set[str]) -> str | None:
    for names, role in ROLE_RULES:
        if toks & set(names):
            return role
    return None


def promote(staging_path: str, registry_out: str, unresolved_out: str) -> None:
    staging = json.loads(Path(staging_path).read_text())

    # Carry forward governance from an existing registry. A human approval is a
    # decision, not derived data — regenerating must never silently revoke one.
    prior_governance: dict[str, dict] = {}
    prior_registry_status = "draft"
    prior_approval_record = None
    if Path(registry_out).exists():
        prior = json.loads(Path(registry_out).read_text())
        prior_governance = {a["asset_id"]: a["governance"] for a in prior.get("assets", [])}
        prior_registry_status = prior.get("status", "draft")
        prior_approval_record = prior.get("_approval_record")

    seen_ids: set[str] = set()
    entries, unresolved = [], []

    for rec in staging["records"]:
        fname = rec["original_filename"]

        held = next((note for frag, note in HOLD_BACK.items() if fname.startswith(frag)), None)
        if held:
            unresolved.append({"original_filename": fname, "asset_id": rec["asset_id"],
                               "reason": held})
            continue

        if rec["asset_id"] in seen_ids:      # byte-identical twin, already promoted
            continue
        if rec.get("error"):
            unresolved.append({"original_filename": fname, "asset_id": rec["asset_id"],
                               "reason": rec["error"]})
            continue

        toks = set(tokens_of(Path(fname).stem))
        explicit = toks & KNOWN_CLIENTS
        via_alias = {CLIENT_ALIASES[t] for t in toks if t in CLIENT_ALIASES}
        clients = sorted(explicit | via_alias)
        alias_hits = sorted(t for t in toks if t in CLIENT_ALIASES)
        role = decide_role(toks)

        if role is None:
            unresolved.append({"original_filename": fname, "asset_id": rec["asset_id"],
                               "reason": "No recognized category token — role undeterminable."})
            continue

        # THE CONFIRMED RULE — client token locks. Industry scope applies only where
        # an asset is nobody's client property but still belongs to a vertical.
        industries = next((v for frag, v in INDUSTRY_RULES.items() if fname.startswith(frag)), [])
        scope = {"industries": industries, "clients": clients}

        third_party = next((n for frag, n in THIRD_PARTY_MARKS.items() if fname.startswith(frag)), None)
        agency = AGENCY_IDENTIFIED.get(fname)

        tags = sorted(toks - KNOWN_CLIENTS - NOISE_TOKENS - {"general"})

        if third_party:
            usage_rights = "third-party-mark"
        elif clients:
            usage_rights = "client-associated"
        else:
            usage_rights = "unverified"

        provenance = (f"Ingested 2026-07-23 from asset-pack_visual-registry-build_072326. "
                      f"Original filename: {fname}.")
        if clients:
            basis = (f"program alias '{alias_hits[0]}'" if alias_hits and not explicit
                     else "naming convention")
            provenance += (f" Client-locked per {basis} ({clients[0]}); imagery may be "
                           f"client-derived.")
        if third_party:
            provenance += " " + third_party
        if agency:
            provenance += f" Identified: {agency}."
        elif third_party:
            provenance += (" Specific issuing agency NOT identified — confirm before use, "
                           "do not assume.")

        mark_class = decide_mark_class(fname, role)

        # Identity marks live in the repo alongside the client's tokens/fonts;
        # everything else resolves against the bulk library.
        if mark_class == "identity" and clients:
            root = "brand"
            file_value = BRAND_FOLDER.format(client=clients[0]) + fname
        else:
            root = DEFAULT_ROOT
            file_value = fname

        entry = {
            "asset_id": rec["asset_id"],
            "file": file_value,
            "root": root,
            "media_type": rec["media_type"],
            "role": role,
            "mark_class": mark_class,
            "scope": scope,
            "tags": tags + (["regulatory-authority"] if third_party else []),
            "content_type_hints": [],
            "content_hash": rec["content_hash"],
            "metadata": {
                "native_dimensions_px": rec["metadata"]["native_dimensions_px"],
                "aspect_ratio": rec["metadata"]["aspect_ratio"],
                "alt_text": agency or "",   # only where established; never guessed
                "caption": "",
            },
            "usage_rights": usage_rights,
            "provenance": provenance,
            "governance": prior_governance.get(rec["asset_id"], {
                "version": 1, "status": "draft", "owner": "jake",
                "approved_by": [], "effective_date": "2026-07-23"}),
        }
        if mark_class is None:
            entry.pop("mark_class", None)   # absent, not null — the schema has no null member
        entries.append(entry)
        seen_ids.add(rec["asset_id"])

    registry = {
        "registry_version": "visual-assets.v0.4",
        "entry_schema": "https://trainstorm.ai/schemas/visual-asset.schema.json",
        "_entry_schema_note": ("Each item in `assets` validates against this schema — NOT the file "
                               "as a whole (the container has no schema of its own). Schema lives "
                               "in trainstorm-core/schemas/, this registry in trainstorm-core/"
                               "registry/; the $id above is the durable link between them."),
        # Registry-level approval is a human act, same as per-entry governance:
        # carried forward, never silently reset by regeneration.
        "status": prior_registry_status,
        "asset_roots": ASSET_ROOTS,
        "_asset_roots_note": ("TWO stores, because the two kinds of asset differ in kind. "
                              "`library` is ABSOLUTE by necessity — the registry lives in git on C:, "
                              "the bulk images in Dropbox on F:, and Windows cannot express a "
                              "relative path across volumes; it is machine-specific, so the resolver "
                              "prefers the TRAINSTORM_ASSET_ROOT env var and falls back to this "
                              "value. `brand` is RELATIVE to this registry and therefore portable "
                              "with no env var at all — it travels with the clone, which is the "
                              "direct payoff of keeping identity marks in the repo. An entry's "
                              "`root` names which one; absent means 'library'."),
        "_default_root": "library",
        "role_definitions": {
            "signature": "Rare, high-specificity brand asset — logo marks, primary illustrations. Reserve for hero placements, not general reuse.",
            "motif": "General-purpose illustrative asset tied to a recurring content concept. Swappable within a family; referenced via content_type_hints.",
            "chrome": "Decorative background, divider, or texture. No semantic specificity. Freely swappable per theme.",
        },
        "assets": entries,
    }
    if prior_approval_record:
        registry["_approval_record"] = prior_approval_record

    Path(registry_out).write_text(json.dumps(registry, indent=2, ensure_ascii=False))
    Path(unresolved_out).write_text(json.dumps(
        {"note": "Deliberately NOT promoted. Each needs a human decision before it can be scoped.",
         "items": unresolved}, indent=2, ensure_ascii=False))

    print(f"promoted:   {len(entries)}")
    print(f"unresolved: {len(unresolved)}")
    print()
    print("role split:  ", dict(Counter(e["role"] for e in entries)))
    lock = Counter(e["scope"]["clients"][0] if e["scope"]["clients"] else "UNIVERSAL"
                   for e in entries)
    print("scope split: ", dict(lock))


if __name__ == "__main__":
    promote("staging.json", "visual-assets.registry.json", "unresolved.json")
