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
  --template / TRAINSTORM_TEMPLATE   (optional 4th anchor; None for a template store)

The template anchor exists because an INSTANCE store is a sparse overlay over a template that lives
in a different store, and bindings.instance.instantiates has to resolve somewhere. It is declared
once, in the instance project's manifest.json:

    "instantiates_template": {"store": "../alsap", "document": "doc_form_ast_34037", "version": "1.0"}

`store` is relative to the instance project dir. Keeping it in the manifest rather than hardcoding a
path is what makes the still-pending promotion of the ALSAP template UP into a client-shared content
tier a one-line change instead of a refactor. A project with no instantiates_template resolves
template_dir to None and every instance check is simply skipped — the four existing tools and both
existing stores are unaffected.
"""
import os, argparse, json, pathlib

def resolve():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--core", default=os.environ.get("TRAINSTORM_CORE"))
    ap.add_argument("--project", default=os.environ.get("TRAINSTORM_PROJECT"))
    ap.add_argument("--registry", default=os.environ.get("TRAINSTORM_REGISTRY"))
    ap.add_argument("--template", default=os.environ.get("TRAINSTORM_TEMPLATE"))
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

    # ---- template store (optional; only instance stores have one) ----
    if args.template:
        template = pathlib.Path(args.template).resolve()
    else:
        mf = project / "manifest.json"
        declared = None
        if mf.exists():
            try:
                declared = (json.loads(mf.read_text()).get("instantiates_template") or {}).get("store")
            except (ValueError, AttributeError):
                declared = None
        template = (project / declared).resolve() if declared else None
    if template is not None and not (template / "atoms.json").exists():
        raise SystemExit(f"Template store declared but has no atoms.json: {template}")

    return {
        "schemas_dir": schemas_dir, "vocab_dir": vocab_dir,
        "registry_dir": registry, "project_dir": project, "template_dir": template,
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
            f"registry={P['registry_dir']} project={P['project_dir']}"
            + (f" template={P['template_dir']}" if P.get("template_dir") else ""))
