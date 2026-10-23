#!/usr/bin/env python3
"""Instantiate a new PrepView domain from template/ using a JSON spec.

Usage: scaffold.py <spec.json> [--force] [--skills-root DIR]

Creates <skills>/prep-<id>/ (or <skills>/prep-<parent>/<id>/ when spec.parent is set):
  SKILL.md, references/{taxonomy,rubric,schema}.md
and registers the domain in prep/registry.json (or the parent's registry.json).
Memory files are NOT created here: they live outside the repo and are created
lazily by prep/scripts/memory.py on first use.
Exits non-zero (and writes nothing) on any validation error.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "template")
REQUIRED = ["id", "title", "kind", "flags", "triggers", "scope_in", "scope_out", "modes",
            "default_mode", "default_difficulty", "ladder", "topics", "flaws", "x_fields",
            "item_ref_format", "rubric_body", "outcome_rule"]
KINDS = {"code", "knowledge", "design"}


def read(*p):
    with open(os.path.join(TEMPLATE, *p)) as f:
        return f.read()


def render(tpl, ctx):
    missing = set(re.findall(r"\{\{(\w+)\}\}", tpl)) - set(ctx)
    if missing:
        raise SystemExit(f"template placeholders without values: {sorted(missing)}")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(ctx[m.group(1)]), tpl)


def flat_flags(reg_path, skills):
    flags, ids = set(), set()
    def walk(p):
        with open(os.path.join(skills, p)) as f:
            for dom in json.load(f)["domains"]:
                flags.update(dom.get("flags", [])); ids.add(dom["id"])
                if dom.get("children"):
                    walk(dom["children"])
    walk(reg_path)
    return flags, ids


def validate(spec):
    errs = [f"missing key '{k}'" for k in REQUIRED if k not in spec]
    if errs:
        return errs
    if not re.fullmatch(r"[a-z][a-z0-9-]*", spec["id"]):
        errs.append("id must be kebab-case")
    if spec["kind"] not in KINDS:
        errs.append(f"kind must be one of {sorted(KINDS)}")
    if len(spec["ladder"]) != 5:
        errs.append("ladder needs exactly 5 anchors (levels 1..5)")
    if spec["default_mode"] not in [m["id"] for m in spec["modes"]]:
        errs.append("default_mode must be one of modes[].id")
    if not 1 <= spec["default_difficulty"] <= 5:
        errs.append("default_difficulty must be 1..5")
    if not all(f.startswith("--") for f in spec["flags"]):
        errs.append("flags must start with --")
    if len(spec["triggers"]) < 5:
        errs.append("give at least 5 trigger phrases")
    for m in spec["modes"]:
        if not {"id", "input", "output"} <= set(m):
            errs.append(f"mode {m} needs id,input,output")
    return errs


def build(spec, parent):
    key = f"{parent}/{spec['id']}" if parent else spec["id"]
    skill_name = f"prep-{parent}-{spec['id']}" if parent else f"prep-{spec['id']}"
    depth_up = "../.." if parent else ".."
    gate = read("gates", spec["kind"] + ".md").rstrip()
    if spec.get("gate_extra"):
        gate += "\n" + "\n".join(f"{i}. {t}" for i, t in enumerate(spec["gate_extra"], 6))
    x = spec["x_fields"]
    ctx = {
        "skill_name": skill_name, "title": spec["title"], "id": spec["id"], "memory_key": key,
        "description": spec.get("description") or
            f"{spec['title']} practice for /prep: {', '.join(spec['triggers'][:6])}. Invoked by the prep orchestrator via {', '.join(spec['flags'])}.",
        "prep_rel": f"{depth_up}/prep", "mem_cmd": f"{depth_up}/prep/scripts/memory.py",
        "scope_in": spec["scope_in"], "scope_out": spec["scope_out"],
        "topics_csv": ", ".join(spec["topics"]), "topics_list": "\n".join(f"- `{t}`" for t in spec["topics"]),
        "modes_table": "\n".join(f"| `{m['id']}` | {m['input']} → {m['output']} |" for m in spec["modes"]),
        "default_mode": spec["default_mode"], "default_difficulty": spec["default_difficulty"],
        "timed_note": " `--timed`: enforce the expected time per item and log `time_s`." if spec.get("timed") else "",
        "ladder_table": "\n".join(f"| {i} | {a} |" for i, a in enumerate(spec["ladder"], 1)),
        "item_ref_format": spec["item_ref_format"],
        "loop_extra": spec.get("loop_extra", ""),
        "gate_block": gate,
        "output_format": spec.get("output_format",
            "Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding."),
        "x_table": "\n".join(f"| `{k}` | {v} |" for k, v in x.items()),
        "x_example": json.dumps({k: "" for k in x}),
        "items_note": spec.get("items_note", "statement, key and any harness files"),
        "flaws_table": "\n".join(f"| `{c}` | {m} |" for c, m in spec["flaws"].items()),
        "rubric_body": spec["rubric_body"], "outcome_rule": spec["outcome_rule"],
    }
    files = {
        "SKILL.md": render(read("SKILL.md.tpl"), ctx),
        "references/taxonomy.md": render(read("references", "taxonomy.md.tpl"), ctx),
        "references/rubric.md": render(read("references", "rubric.md.tpl"), ctx),
        "references/schema.md": render(read("memory", "schema.md.tpl"), ctx),
    }
    entry = {"id": spec["id"], "skill": skill_name,
             "path": f"prep-{parent}/{spec['id']}" if parent else f"prep-{spec['id']}",
             "kind": spec["kind"], "flags": spec["flags"], "triggers": spec["triggers"],
             "modes": [m["id"] for m in spec["modes"]], "default_mode": spec["default_mode"],
             "default_difficulty": spec["default_difficulty"]}
    return files, entry


def main(argv):
    if not argv:
        print(__doc__); return 2
    force = "--force" in argv
    skills = os.path.abspath(argv[argv.index("--skills-root") + 1]) if "--skills-root" in argv \
        else os.path.abspath(os.path.join(HERE, "..", ".."))
    with open(argv[0]) as f:
        spec = json.load(f)
    errs = validate(spec)
    if errs:
        print("spec invalid:\n- " + "\n- ".join(errs), file=sys.stderr); return 1
    parent = spec.get("parent")
    reg_rel = f"prep-{parent}/registry.json" if parent else "prep/registry.json"
    reg_path = os.path.join(skills, reg_rel)
    if parent and not os.path.exists(reg_path):
        print(f"parent '{parent}' has no {reg_rel}; create the parent router first", file=sys.stderr); return 1
    files, entry = build(spec, parent)
    root_dir = os.path.join(skills, entry["path"])
    flags, ids = flat_flags("prep/registry.json", skills)
    with open(reg_path) as f:
        reg = json.load(f)
    existing = next((d for d in reg["domains"] if d["id"] == spec["id"]), None)
    if (existing or os.path.exists(root_dir)) and not force:
        print(f"'{spec['id']}' already exists (use --force to regenerate)", file=sys.stderr); return 1
    mine = set(existing["flags"]) if existing else set()
    clash = (set(spec["flags"]) & flags) - mine
    if clash:
        print(f"flag collision: {sorted(clash)}", file=sys.stderr); return 1
    for rel, body in files.items():
        p = os.path.join(root_dir, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(body)
    reg["domains"] = [d for d in reg["domains"] if d["id"] != spec["id"]] + [entry]
    with open(reg_path, "w") as f:
        json.dump(reg, f, indent=2); f.write("\n")
    print(f"created {entry['path']} ({len(files)} files); registered in {reg_rel}")
    print(f"next: python3 {os.path.relpath(os.path.join(skills, 'prep/scripts/lint.py'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
