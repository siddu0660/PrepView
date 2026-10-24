#!/usr/bin/env python3
"""Technique ledger for prep-aidebug. Stdlib only. Lives in $(MEM path aidebug)/playbook.json (+ rendered playbook.md).

  playbook.py show                          the user's playbook (name, status, how/when, evidence)
  playbook.py add "<name>" --how "..." --when "..." --ref <item ref> --status taught|tried|owned [--origin user|skill]
                                            add, or update an existing name (status never moves backwards; evidence accumulates)
  playbook.py catalog                       curated techniques (references/techniques.md) not yet in the playbook
  playbook.py path                          print the playbook.md path
Memory dir: $PREP_MEMORY_DIR or ~/.claude/prep-memory (same as memory.py), key 'aidebug'.
"""
import argparse, datetime, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = {"taught": 0, "tried": 1, "owned": 2}


def mem_dir():
    root = os.environ.get("PREP_MEMORY_DIR") or os.path.expanduser("~/.claude/prep-memory")
    d = os.path.join(root, "aidebug"); os.makedirs(d, exist_ok=True); return d


def load():
    p = os.path.join(mem_dir(), "playbook.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def save(pb):
    d = mem_dir()
    with open(os.path.join(d, "playbook.json"), "w") as f:
        json.dump(pb, f, indent=1, sort_keys=True)
    with open(os.path.join(d, "playbook.md"), "w") as f:
        f.write("# Playbook: AI-assisted debugging\n\n")
        for n, t in sorted(pb.items(), key=lambda kv: (-ORDER[kv[1]["status"]], kv[0])):
            f.write(f"## {n}  [{t['status']}{', yours' if t['origin']=='user' else ''}]\n")
            f.write(f"- how: {t['how']}\n- when: {t['when']}\n- evidence: {', '.join(t['evidence'][-5:])}\n\n")


def catalog():
    names = []
    with open(os.path.join(HERE, "..", "references", "techniques.md")) as f:
        names = re.findall(r"^## (.+?)\s*$", f.read(), re.M)
    return names


def main():
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("show"); sp.add_parser("catalog"); sp.add_parser("path")
    a = sp.add_parser("add"); a.add_argument("name"); a.add_argument("--how", required=True)
    a.add_argument("--when", required=True); a.add_argument("--ref", required=True)
    a.add_argument("--status", choices=ORDER, default="tried"); a.add_argument("--origin", choices=["user", "skill"], default="skill")
    r = ap.parse_args(); pb = load()
    if r.cmd == "show":
        if not pb: print("(playbook empty)"); return 0
        for n, t in sorted(pb.items(), key=lambda kv: (-ORDER[kv[1]["status"]], kv[0])):
            print(f"- {n} [{t['status']}{', yours' if t['origin']=='user' else ''}] how: {t['how']} | when: {t['when']}")
    elif r.cmd == "catalog":
        print("\n".join(n for n in catalog() if n not in pb) or "(all catalog techniques are in the playbook)")
    elif r.cmd == "path":
        print(os.path.join(mem_dir(), "playbook.md"))
    else:
        t = pb.get(r.name) or {"how": r.how, "when": r.when, "status": r.status, "origin": r.origin, "evidence": [], "first_seen": datetime.date.today().isoformat()}
        if ORDER[r.status] > ORDER[t["status"]]: t["status"] = r.status
        t["how"], t["when"] = r.how, r.when
        if r.origin == "user": t["origin"] = "user"
        t["evidence"].append(f"{r.ref}@{datetime.date.today().isoformat()}")
        pb[r.name] = t; save(pb); print(f"{r.name}: {t['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
