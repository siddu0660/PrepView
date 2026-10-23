#!/usr/bin/env python3
"""Lint the PrepView skill tree. Exit 1 on any error.

Checks: registry well-formed; ids/flags unique across the whole tree; every path
exists with SKILL.md + references/{taxonomy,rubric,schema}.md (leaf domains);
SKILL.md has the 8 required sections and frontmatter name matches registry;
no unresolved {{placeholders}}; triggers do not collide across domains (warn).
"""
import json, os, re, sys

SKILLS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SECTIONS = ["## 1. Scope", "## 2. Modes", "## 3. Difficulty ladder", "## 4. Session loop",
            "## 5. Accuracy gates", "## 6. Grading", "## 7. Memory", "## 8. Output format"]
errors, warns = [], []


def walk(reg_rel, parent=None, seen=None):
    seen = seen if seen is not None else {"ids": {}, "flags": {}, "trig": {}}
    with open(os.path.join(SKILLS, reg_rel)) as f:
        reg = json.load(f)
    for d in reg["domains"]:
        key = f"{parent}/{d['id']}" if parent else d["id"]
        for need in ("id", "skill", "path", "flags", "triggers", "kind"):
            if need not in d:
                errors.append(f"{key}: registry missing '{need}'")
        if key in seen["ids"]:
            errors.append(f"duplicate id {key}")
        seen["ids"][key] = d
        for fl in d.get("flags", []):
            if not fl.startswith("--"):
                errors.append(f"{key}: flag {fl} must start with --")
            if fl in seen["flags"]:
                errors.append(f"flag {fl} used by {seen['flags'][fl]} and {key}")
            seen["flags"][fl] = key
        for t in d.get("triggers", []):
            other = seen["trig"].get(t.lower())
            if other and other != key:
                warns.append(f"trigger '{t}' shared by {other} and {key}")
            seen["trig"][t.lower()] = key
        base = os.path.join(SKILLS, d.get("path", ""))
        if not os.path.isfile(os.path.join(base, "SKILL.md")):
            errors.append(f"{key}: {d.get('path')}/SKILL.md missing")
            continue
        text = open(os.path.join(base, "SKILL.md")).read()
        m = re.match(r"---\nname: (.+)\ndescription: (.+)\n(?:.*\n)*?---", text)
        if not m:
            errors.append(f"{key}: bad frontmatter")
        elif m.group(1).strip() != d["skill"]:
            errors.append(f"{key}: frontmatter name '{m.group(1).strip()}' != registry skill '{d['skill']}'")
        if re.search(r"\{\{\w+\}\}", text):
            errors.append(f"{key}: unresolved placeholder in SKILL.md")
        if d["kind"] != "router":
            for s in SECTIONS:
                if s not in text:
                    errors.append(f"{key}: SKILL.md missing '{s}'")
            for r in ("taxonomy", "rubric", "schema"):
                if not os.path.isfile(os.path.join(base, "references", r + ".md")):
                    errors.append(f"{key}: references/{r}.md missing")
            if d.get("default_mode") not in d.get("modes", []):
                errors.append(f"{key}: default_mode not in modes")
        if d.get("children"):
            if not os.path.isfile(os.path.join(SKILLS, d["children"])):
                errors.append(f"{key}: children registry {d['children']} missing")
            else:
                walk(d["children"], key, seen)
    return seen


seen = walk("prep/registry.json")
for w in warns:
    print("warn:", w)
for e in errors:
    print("ERROR:", e)
print(f"{len(seen['ids'])} domains, {len(seen['flags'])} flags, {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
