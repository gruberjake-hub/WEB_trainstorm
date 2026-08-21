#!/usr/bin/env python3
"""
resolve_prompt — spine + specialization + walk result -> one dispatchable payload.

The prompt resolver deferred on 2026-08-11 and made load-bearing by Amanuensis. The earlier
`tools/localize/build_agent_call.py` concatenates two static files, which is enough for an agent whose
grounding is a corpus lookup. It is NOT enough here: Amanuensis's entire world for a slot is a walk
result assembled at call time, so the resolver has to inline a *packet*, not a second document.

    python3 tools/resolve_slot.py   --project <template store> --procedure <sop store> \
        --slot <atom_id> --out packet.json
    python3 tools/resolve_prompt.py --agent alsap_builder --packet packet.json --mode draft \
        --project <template store> --out payload.json

What it does, in order:
  1. Reads the spine and keeps only what is marked as spine (everything after the "Everything below
     is the spine." marker) — the preamble is documentation ABOUT the slots and must not reach the
     agent as instructions.
  2. Reads the specialization's slot table and substitutes `{{SLOT}}` tokens into the spine.
  3. If the specialization supplies `{{WRITE_CONTRACT}}`, its text REPLACES the spine's default
     write-contract body (spine v0.2). If not, the default is inherited verbatim.
  4. Appends the specialization's remaining sections — the ones that are genuinely additional rather
     than slot values.
  5. Refuses to emit if any `{{TOKEN}}` is still unfilled, or if the resolved prompt carries atom
     content (the shared rule in prompt_purity.py). **The resolver is the enforcement point**: a
     leaking payload is never written, rather than written and reported.

Dispatch is deliberately NOT this tool's job. It emits `{system, messages, meta}`; how that reaches a
model is environment-specific (an enterprise endpoint, a harness, a subagent). Keeping dispatch out
means the same payload is reproducible and diffable, and the purity check has a file to run against.
"""
import json, pathlib, argparse, re, sys
import harness_paths
import prompt_purity

P = harness_paths.resolve()
CORE, PROJ = P["core_dir"], P["project_dir"]
AGENTS = CORE / "agents"

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--agent", required=True,
                help="agent folder under agents/ (e.g. alsap_builder), or a path to a specialization .md")
ap.add_argument("--spine", default=None)
ap.add_argument("--packet", help="grounding packet JSON from resolve_slot.py --out")
ap.add_argument("--mode", default="draft")
ap.add_argument("--out")
ap.add_argument("--print-system", action="store_true")
A, _ = ap.parse_known_args()

# ---- locate the two prompt files -------------------------------------------------------------
spine_p = pathlib.Path(A.spine) if A.spine else AGENTS / "_shared" / "facet_owner_spine.md"
spec_p = pathlib.Path(A.agent)
# .is_file(), not .exists(): `--agent localize` run from tools/ matched the tools/localize/ DIRECTORY
# and then tried to read it. Found 2026-08-20 by running the resolver against all seven agents.
if not spec_p.is_file():
    hits = sorted((AGENTS / A.agent / "02_system_prompts" / "core_agent").glob("*.md"))
    if len(hits) != 1:
        raise SystemExit(f"expected exactly one specialization under agents/{A.agent}/"
                         f"02_system_prompts/core_agent/, found {len(hits)}")
    spec_p = hits[0]
spine_raw, spec_raw = spine_p.read_text(), spec_p.read_text()

# The version stamp was hardcoded to "amanuensis.v0.1+spine.v0.2" — so every agent's payload claimed
# to be Amanuensis. Harmless while one agent resolved; wrong the moment six do. Derive it instead.
def _ver(text, default="v?"):
    m = re.search(r"\bv(\d+\.\d+)\b", text[:1200])
    return f"v{m.group(1)}" if m else default
_agent_name = spec_p.stem.replace("_system_prompt", "")
PROMPT_VERSION = f"{_agent_name}.{_ver(spec_raw)}+spine.{_ver(spine_raw)}"

# ---- 1. keep only the spine proper ------------------------------------------------------------
MARK = "Everything below is the spine."
if MARK not in spine_raw:
    raise SystemExit(f"{spine_p} has no '{MARK}' marker — cannot tell documentation from prompt.")
spine = spine_raw.split(MARK, 1)[1].lstrip("\n").lstrip("-").lstrip("\n")

# ---- 2. read the slot table --------------------------------------------------------------------
# Rows look like:  | `{{AGENT_NAME}}` | **Amanuensis** |
slots = {}
for m in re.finditer(r"^\|\s*`\{\{(\w+)\}\}`\s*\|(.+?)\|\s*$", spec_raw, re.M):
    slots[m.group(1)] = m.group(2).strip()

# Fail loudly on a row that declares more than one token, e.g. `| {{FACET}} / {{FACET_KEYS}} | … |`.
# One value cannot fill two slots, and the old behaviour was to silently not match and then report
# the slots as "unfilled" — which reads like the specialization forgot them rather than that the
# table shape is wrong. Four of the seven specializations were in this state.
for line in spec_raw.splitlines():
    if line.startswith("|") and len(re.findall(r"`\{\{(\w+)\}\}`", line.split("|")[1] if line.count("|") > 1 else "")) > 1:
        raise SystemExit(
            f"{spec_p.name}: one table row declares several slots —\n  {line.strip()[:110]}\n"
            f"  Give each slot its own row; one value cannot fill two.")

# ---- 3/4. split the specialization's prose into sections ---------------------------------------
sections, cur, buf = {}, None, []
for line in spec_raw.splitlines():
    if line.startswith("## "):
        if cur: sections[cur] = "\n".join(buf).strip()
        cur, buf = line[3:].strip(), []
    elif cur:
        buf.append(line)
if cur: sections[cur] = "\n".join(buf).strip()

# The slot table's own section is metadata about the resolution, not instruction to the agent.
DROP = {"The seven slots"}
# A section whose title marks it as the write-contract override fills that slot instead of appending.
wc_title = next((t for t in sections if "write-contract" in t.lower() or "write contract" in t.lower()),
                None)
if wc_title:
    slots["WRITE_CONTRACT"] = sections[wc_title]
    DROP.add(wc_title)
# The spine has a `{{MODES}}` slot; the specialization's Modes section is its value, not an addendum.
if "Modes" in sections:
    slots["MODES"] = sections["Modes"]
    DROP.add("Modes")

# ---- substitute --------------------------------------------------------------------------------
# The write contract is a whole section in the spine, headed with the slot token. When the
# specialization overrides it, the spine's default body goes with the heading — otherwise the agent
# would receive both the override and the single-writer default it contradicts.
SENTINEL = "\x00WRITE_CONTRACT\x00"
wc_body = slots.pop("WRITE_CONTRACT", None)
if wc_body is not None:
    spine = re.sub(r"^## The write contract — `\{\{WRITE_CONTRACT\}\}`.*?(?=^## )",
                   "## The write contract\n\n" + SENTINEL + "\n\n",
                   spine, count=1, flags=re.S | re.M)
else:
    # No override: the agent inherits the spine's default write contract verbatim. The heading still
    # carries the slot token, so strip it — otherwise the token survives to the unfilled-slot check
    # and the resolver refuses every agent that does NOT override. That was six of seven; only
    # Amanuensis (the one this tool was built against) has an override, so only Amanuensis worked.
    spine = re.sub(r"^## The write contract — `\{\{WRITE_CONTRACT\}\}`\s*$",
                   "## The write contract", spine, count=1, flags=re.M)
    # The token appears TWICE in the spine body — the heading above, and the italic note beneath it
    # ("…unless the specialization supplies `{{WRITE_CONTRACT}}`"). Stripping only the heading left
    # the second one to trip the unfilled check. Resolve the remainder to the plain slot name so the
    # note still reads correctly as documentation of the slot system.
    slots.setdefault("WRITE_CONTRACT", "WRITE_CONTRACT")

# Substitution is SINGLE-PASS: a slot's value is inserted and never rescanned for further tokens.
# Sequential str.replace() looked equivalent and was not — Amanuensis's write-contract block quotes
# the spine ("the spine gained an optional eighth slot, `{{WRITE_CONTRACT}}`"), so a second pass
# re-injected the very token it had just filled. A specialization that documents its own slots is
# normal and good; the resolver must not treat their names as instructions to substitute again.
spine = re.sub(r"\{\{(\w+)\}\}", lambda m: slots.get(m.group(1), m.group(0)), spine)

# A `{{FACET}}` that the specialization declares as "(none)" is still a token the spine leans on in
# several sentences; leaving it half-filled would ship a prompt that reads as broken. Catch it.
left = sorted(set(re.findall(r"\{\{(\w+)\}\}", spine)))
if left:
    raise SystemExit(f"unfilled slot(s) after resolution: {left}\n"
                     f"  the specialization {spec_p.name} declares no value for them.")

# Restored after the check, so token names *quoted inside* a slot value stay literal text.
if wc_body is not None:
    spine = spine.replace(SENTINEL, wc_body)

addenda = "\n\n".join(f"## {t}\n\n{b}" for t, b in sections.items() if t not in DROP and b)
system = spine.rstrip() + ("\n\n---\n\n" + addenda if addenda else "") + "\n"

# ---- 5. refuse to emit a leaking payload -------------------------------------------------------
atoms = json.loads((PROJ / "atoms.json").read_text())
leaks = prompt_purity.scan(atoms, {"<resolved system prompt>": system})
ok = prompt_purity.report(atoms, {"<resolved system prompt>": system}, leaks, what="resolved prompt")
if not ok:
    raise SystemExit("refusing to write a payload whose prompt carries controlled content.")

# ---- the user message: the mode instruction, then the packet -----------------------------------
# Modes are DECLARED BY THE SPECIALIZATION, not by this tool. They used to be a hardcoded dict of
# Amanuensis's three (draft/check/explain) — and the error message claimed they came from the
# specialization, which made the lie hard to see. Cartographer declares `bind`/`steward` and was
# refused. Fourth Amanuensis-ism found in this file by running it against another agent.
_declared = re.findall(r"^-\s+\*\*`(\w+)`\*\*", slots.get("MODES", ""), re.M)
if _declared and A.mode not in _declared:
    raise SystemExit(f"unknown mode {A.mode!r} for {_agent_name}; "
                     f"its specialization declares {sorted(_declared)}")
if not _declared:
    print(f"  ! {spec_p.name} declares no parseable modes; accepting {A.mode!r} unchecked")

packet = json.loads(pathlib.Path(A.packet).read_text()) if A.packet else None
# The mode's SEMANTICS are in the specialization's own Modes section, which is already inlined in the
# system prompt. The user turn only has to name which one is in force.
user = f"Work in `{A.mode}` mode, as your specialization defines it."
if packet:
    user += ("\n\nThis is the grounding packet for the slot. It is your entire world for this task; "
             "nothing else about the ALSAP is available to you, and nothing may come from your "
             "training. If something you need is absent, say so and stop.\n\n"
             "```json\n" + json.dumps(packet, indent=2, ensure_ascii=False) + "\n```")
else:
    user += "\n\n(No grounding packet supplied — you cannot proceed; say so.)"

payload = {
    "meta": {
        "agent": A.agent,
        "mode": A.mode,
        "spine": str(spine_p.relative_to(CORE)),
        "specialization": str(spec_p.relative_to(CORE)),
        "prompt_version": PROMPT_VERSION,
        "slot": (packet or {}).get("slot", {}).get("atom_id"),
        "template_source_hash": (packet or {}).get("slot", {}).get("content_hash"),
        "purity": "PASS",
    },
    "system": system,
    "messages": [{"role": "user", "content": user}],
}

if A.print_system:
    print(system)
if A.out:
    pathlib.Path(A.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"payload -> {A.out}")
print(f"  agent   : {A.agent} · mode {A.mode} · {payload['meta']['prompt_version']}")
print(f"  system  : {len(system.splitlines())} lines, {len(system)} chars "
      f"({len(slots)} slot(s) filled, {len(DROP) - 1} section(s) consumed as slot values)")
print(f"  slot    : {payload['meta']['slot'] or '(none)'}")
