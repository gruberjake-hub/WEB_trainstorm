#!/usr/bin/env python3
"""
Shared path resolver for the harness tools.

The harness runs in two layouts, and the tools must not care which:

  REPO (tools live in cgen/trainstorm-core/tools/):
    core     = cgen/trainstorm-core            (schemas/ + vocab/)  — auto-detected
    project  = cgen/astellas/projects/<proj>   — pass --project
    registry = cgen/astellas/registry          — auto-derived from project (client = project/../..)

  STANDALONE package (tools live in beta_harness/tools/):
    core     = beta_harness/_core_mirror       (NON-canonical mirror; prints a warning)
    project  = beta_harness/store/projects/ast_alsap
    registry = beta_harness/schemas

Resolution priority for each anchor: explicit flag > env var > auto-detect > standalone default.
  --core     / TRAINSTORM_CORE
  --project  / TRAINSTORM_PROJECT
  --registry / TRAINSTORM_REGISTRY
"""
import os, argparse, pathlib

def resolve():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--core", default=os.environ.get("TRAINSTORM_CORE"))
    ap.add_argument("--project", default=os.environ.get("TRAINSTORM_PROJECT"))
    ap.add_argument("--registry", default=os.environ.get("TRAINSTORM_REGISTRY"))
    args, _ = ap.parse_known_args()

    tools_dir = pathlib.Path(__file__).resolve().parent
    base = tools_dir.parent  # trainstorm-core in the repo; the package root when standalone
    warnings = []

    # ---- core (schemas + vocab) ----
    if args.core:
        core = pathlib.Path(args.core).resolve()
        core_is_mirror = False
    elif (base / "schemas" / "atom.schema.json").exists() and (base / "vocab" / "procedure.enum.json").exists():
        core = base                       # tools sit inside a real core dir → canon is right here
        core_is_mirror = False
    elif (base / "_core_mirror" / "atom.schema.json").exists():
        core = base / "_core_mirror"      # standalone fallback
        core_is_mirror = True
        warnings.append("core: using bundled _core_mirror (NOT canonical). "
                        "In the repo pass --core <path>/cgen/trainstorm-core.")
    else:
        raise SystemExit("Cannot locate core schemas. Pass --core <path to cgen/trainstorm-core>.")

    if core_is_mirror:
        schemas_dir = vocab_dir = core   # mirror keeps all three files flat
    else:
        schemas_dir, vocab_dir = core / "schemas", core / "vocab"

    # ---- project store ----
    if args.project:
        project = pathlib.Path(args.project).resolve()
    elif (base / "store" / "projects" / "ast_alsap").exists():
        project = base / "store" / "projects" / "ast_alsap"
    else:
        raise SystemExit("Cannot locate a project store. Pass --project <path to .../projects/<proj>>.")

    # ---- client registry ----
    if args.registry:
        registry = pathlib.Path(args.registry).resolve()
    elif (project.parent.parent / "registry").exists():
        registry = project.parent.parent / "registry"   # repo: astellas/projects/<proj> → astellas/registry
    elif (base / "schemas").exists():
        registry = base / "schemas"                      # standalone: registries live in schemas/
    else:
        raise SystemExit("Cannot locate the client registry. Pass --registry <path>.")

    return {
        "schemas_dir": schemas_dir, "vocab_dir": vocab_dir,
        "registry_dir": registry, "project_dir": project,
        # new-to-core vocab (e.g. structure.enum.json) not yet in a real core checkout;
        # only present standalone. In the repo, such files live in vocab_dir once committed.
        "core_adds_dir": base / "_core_adds",
        "core_is_mirror": core_is_mirror, "warnings": warnings,
    }

def announce(P):
    """Print any resolution warnings + a one-line summary of where things resolved."""
    for w in P["warnings"]:
        print("WARNING:", w)
    src = "MIRROR (non-canonical)" if P["core_is_mirror"] else "canonical"
    return (f"core[{src}]={P['schemas_dir'].parent if not P['core_is_mirror'] else P['schemas_dir']} "
            f"registry={P['registry_dir']} project={P['project_dir']}")
