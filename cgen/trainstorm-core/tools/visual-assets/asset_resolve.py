#!/usr/bin/env python3
"""
asset_resolve — the one place that turns an asset_id into a path on disk.

Everything upstream (elements, render.asset_ref, the compiler) deals in asset_id.
Only this module knows filenames, drive letters, or roots exist.

TWO ROOTS, resolved differently on purpose:

  library  404 MB of content on Dropbox (F:). The registry lives in git on C:,
           and Windows cannot express a relative path across volumes, so this
           root must be ABSOLUTE — which makes it machine-specific, so the
           TRAINSTORM_ASSET_ROOT env var overrides it. Set per machine.

  brand    A few hundred KB of client identity marks, in the repo beside their
           tokens and fonts. RELATIVE to this registry, therefore portable with
           no env var: it travels with the clone. The env var does NOT touch it —
           overriding a repo-relative path would break what makes it portable.

An entry's `root` names which store it belongs to; absent means "library".
"""
import hashlib
import json
import os
import re
from pathlib import Path

ENV_VAR = "TRAINSTORM_ASSET_ROOT"
OVERRIDABLE_ROOT = "library"   # the machine-specific one; brand is repo-relative
DEFAULT_ROOT = "library"


class AssetResolver:
    def __init__(self, registry_path: str | Path):
        self.registry_path = Path(registry_path).resolve()
        reg = json.loads(self.registry_path.read_text(encoding="utf-8"))
        self._index = {a["asset_id"]: a for a in reg["assets"]}
        self._roots = dict(reg.get("asset_roots", {}))
        self._env_override = os.environ.get(ENV_VAR)
        if self._env_override:
            self._roots[OVERRIDABLE_ROOT] = self._env_override

    def root_for(self, name: str) -> Path:
        try:
            raw = self._roots[name]
        except KeyError:
            raise KeyError(
                f"'{name}' is not a declared root. Declared: {sorted(self._roots)}") from None

        # A Windows drive path ("F:/...") is absolute on Windows but NOT on
        # POSIX, where Path would silently glue it onto the registry directory
        # and produce a plausible-looking wrong path. Fail loudly instead —
        # this is exactly the sandbox-machine case.
        if re.match(r"^[A-Za-z]:[\\/]", str(raw)) and os.name != "nt":
            raise RuntimeError(
                f"root '{name}' is a Windows path ({raw}) but this is not Windows. "
                f"Set {ENV_VAR} to the local location instead of resolving it blindly.")

        p = Path(raw)
        # Relative roots resolve against the registry's own directory — that is
        # what makes the brand root portable.
        return p if p.is_absolute() else (self.registry_path.parent / p).resolve()

    def record(self, asset_id: str) -> dict:
        try:
            return self._index[asset_id]
        except KeyError:
            raise KeyError(f"{asset_id} is not in {self.registry_path.name}") from None

    def path(self, asset_id: str) -> Path:
        """asset_id -> concrete path. The only place `file` and `root` are read."""
        rec = self.record(asset_id)
        return self.root_for(rec.get("root", DEFAULT_ROOT)) / rec["file"]

    def verify(self, asset_id: str) -> tuple[bool, str]:
        """Exists, and do the bytes still match content_hash? Dropbox smart-sync
        placeholders and conflicted copies both fail here loudly rather than at
        render time."""
        p = self.path(asset_id)
        if not p.exists():
            return False, f"missing: {p}"
        actual = "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != self.record(asset_id)["content_hash"]:
            return False, f"hash mismatch (file changed since ingest): {p.name}"
        return True, "ok"

    def audit(self) -> dict:
        """Check every entry, grouped by root so a whole unmounted or unsynced
        store is obvious at a glance instead of looking like 251 unrelated
        failures."""
        out: dict[str, dict] = {}
        for aid, rec in self._index.items():
            r = rec.get("root", DEFAULT_ROOT)
            bucket = out.setdefault(r, {"ok": 0, "missing": [], "hash_mismatch": []})
            good, msg = self.verify(aid)
            if good:
                bucket["ok"] += 1
            elif msg.startswith("missing"):
                bucket["missing"].append(aid)
            else:
                bucket["hash_mismatch"].append(aid)
        return out

    def check_roots(self) -> list[str]:
        """Lint: every entry's `root` must name a declared root. JSON Schema
        cannot check this (it is a cross-reference within the document), so it
        lives here."""
        declared = set(self._roots)
        return [aid for aid, rec in self._index.items()
                if rec.get("root", DEFAULT_ROOT) not in declared]


if __name__ == "__main__":
    import sys
    r = AssetResolver(sys.argv[1] if len(sys.argv) > 1 else "visual-assets.registry.json")
    print(f"registry : {r.registry_path}")
    print(f"env      : {ENV_VAR}={r._env_override or '(unset)'}")
    for name in sorted(r._roots):
        note = "  <- env override" if (name == OVERRIDABLE_ROOT and r._env_override) else ""
        print(f"root[{name}] : {r.root_for(name)}{note}")
    bad = r.check_roots()
    print(f"undeclared roots referenced: {bad or 'none'}")
