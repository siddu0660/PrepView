#!/usr/bin/env python3
"""Per-domain memory manager for PrepView. Stdlib only.

Memory lives OUTSIDE the repo: $PREP_MEMORY_DIR or ~/.claude/prep-memory.
Layout per domain key (e.g. "dsa", "quant/prob"):
  meta.json    {"default_level": 2}
  log.jsonl    append-only episodes (source of truth)
  profile.md   derived, <=40 lines, ALWAYS rebuildable from log.jsonl
  notes.md     curated short remarks
  items/<ref>  stored problem/question material for review & spaced repetition

Commands:
  init <key> [--default-level N]     create files if missing
  profile <key>                      print profile.md (rebuilds if stale)
  rebuild <key>                      recompute profile.md from log.jsonl
  append <key>                       read one episode JSON on stdin, validate, append, rebuild
  tail <key> [n]                     last n log entries (default 5)
  seen <key> <ref>                   exit 0 if ref already in log (dedupe)
  note <key> "text"                  append a remark to notes.md (compacts past 30 lines)
  save-item <key> <ref> <path>       copy file/dir into items/<ref>
  due <key> [--now ISO]              refs due for spaced-repetition review
  path <key>                         print the resolved directory
"""
import datetime as dt, json, os, shutil, sys
from collections import Counter, defaultdict

REQUIRED = {"ts": str, "domain": str, "mode": str, "difficulty": int,
            "item": dict, "outcome": str, "flaws": list, "remark": str}
OUTCOMES = {"pass", "partial", "fail"}
INTERVAL_DAYS = [1, 3, 7, 14]          # spaced-repetition ladder
NOTES_MAX = 30
PROFILE_MAX = 40


def root():
    return os.path.expanduser(os.environ.get("PREP_MEMORY_DIR") or "~/.claude/prep-memory")


def d(key, create=False):
    p = os.path.join(root(), *key.split("/"))
    if create:
        os.makedirs(os.path.join(p, "items"), exist_ok=True)
    return p


def read_log(key):
    p = os.path.join(d(key), "log.jsonl")
    if not os.path.exists(p):
        return []
    out = []
    with open(p) as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                try:
                    out.append(json.loads(ln))
                except json.JSONDecodeError:
                    pass                       # a torn line must never block a session
    return out


def meta(key):
    try:
        with open(os.path.join(d(key), "meta.json")) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"default_level": 2}


def init(key, default_level=None):
    p = d(key, create=True)
    mp = os.path.join(p, "meta.json")
    if not os.path.exists(mp):
        with open(mp, "w") as f:
            json.dump({"default_level": default_level or 2}, f)
    for name, head in (("log.jsonl", ""), ("notes.md", f"# Notes: {key}\n")):
        fp = os.path.join(p, name)
        if not os.path.exists(fp):
            with open(fp, "w") as f:
                f.write(head)
    if not os.path.exists(os.path.join(p, "profile.md")):
        rebuild(key)
    return p


def validate(ep):
    for k, t in REQUIRED.items():
        if k not in ep or not isinstance(ep[k], t):
            raise ValueError(f"episode field '{k}' missing or not {t.__name__}")
    if ep["outcome"] not in OUTCOMES:
        raise ValueError(f"outcome must be one of {sorted(OUTCOMES)}")
    if not 1 <= ep["difficulty"] <= 5:
        raise ValueError("difficulty must be 1..5")
    if "ref" not in ep["item"]:
        raise ValueError("item.ref required")


def level_state(log, default):
    """Deterministic level rule: +1 after 2 consecutive clean passes at/above the
    level, -1 after 2 consecutive failures at/below it. Resets on any change."""
    lvl, clean, bad = default, 0, 0
    for e in log:
        ok = e["outcome"] == "pass" and len(e.get("hints", [])) <= 1
        if ok and e["difficulty"] >= lvl:
            clean, bad = clean + 1, 0
        elif e["outcome"] == "fail" and e["difficulty"] <= lvl:
            bad, clean = bad + 1, 0
        elif e["outcome"] != "pass":
            clean = 0
        if clean >= 2 and lvl < 5:
            lvl, clean, bad = lvl + 1, 0, 0
        elif bad >= 2 and lvl > 1:
            lvl, clean, bad = lvl - 1, 0, 0
    return lvl


def tag_stats(log):
    st = defaultdict(lambda: [0.0, 0])
    for e in log:
        score = {"pass": 1.0, "partial": 0.5, "fail": 0.0}[e["outcome"]]
        for t in e["item"].get("tags", []):
            st[t][0] += score
            st[t][1] += 1
    return st


def rebuild(key):
    log = read_log(key)
    lvl = level_state(log, meta(key).get("default_level", 2))
    st = tag_stats(log)
    ranked = sorted(((s / n, n, t) for t, (s, n) in st.items() if n >= 2))
    weak = [f"{t} ({r:.0%} over {n})" for r, n, t in ranked if r < 0.7][:3]
    strong = [f"{t} ({r:.0%})" for r, n, t in reversed(ranked) if r >= 0.85][:3]
    flaws = Counter(f for e in log[-20:] for f in e.get("flaws", []))
    watch = [f"{c} x{n}" for c, n in flaws.most_common(3)]
    habits = [e["workflow"] for e in log[-3:] if e.get("workflow")]
    last5 = log[-5:]
    rate = (sum({"pass": 1, "partial": .5, "fail": 0}[e["outcome"]] for e in last5) / len(last5)) if last5 else None
    hints = sum(len(e.get("hints", [])) for e in last5)
    lines = [f"# Profile: {key}",
             f"recommended_level: {lvl}",
             f"sessions: {len(log)}   last5_success: {'n/a' if rate is None else f'{rate:.0%}'}   last5_hints: {hints}",
             f"weak_tags: {', '.join(weak) or 'none yet'}",
             f"strong_tags: {', '.join(strong) or 'none yet'}",
             f"watch_list (rolling 20): {', '.join(watch) or 'none yet'}",
             "recent_workflow:"] + [f"- {h}" for h in habits] + \
            [f"updated: {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}"]
    with open(os.path.join(d(key, create=True), "profile.md"), "w") as f:
        f.write("\n".join(lines[:PROFILE_MAX]) + "\n")
    return lvl


def append(key, ep):
    validate(ep)
    init(key)
    ep.setdefault("id", f"{ep['ts']}-{key.replace('/', '-')}-{len(read_log(key)) + 1:03d}")
    with open(os.path.join(d(key), "log.jsonl"), "a") as f:
        f.write(json.dumps(ep, separators=(",", ":")) + "\n")
    return rebuild(key)


def note(key, text):
    init(key)
    p = os.path.join(d(key), "notes.md")
    with open(p, "a") as f:
        f.write(f"- {dt.date.today()}: {text.strip()}\n")
    with open(p) as f:
        lines = f.read().splitlines()
    if len(lines) > NOTES_MAX + 1:            # keep header + newest NOTES_MAX
        with open(p, "w") as f:
            f.write("\n".join([lines[0]] + lines[-NOTES_MAX:]) + "\n")


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def due(key, now=None):
    now = parse_ts(now) if now else dt.datetime.now(dt.timezone.utc)
    seq = defaultdict(list)
    for e in read_log(key):
        seq[e["item"]["ref"]].append(e)
    out = []
    for ref, eps in seq.items():
        if all(e["outcome"] == "pass" for e in eps):
            continue                            # never struggled: not tracked
        stage = 0
        for e in eps:
            stage = stage + 1 if e["outcome"] == "pass" else 0
        if stage >= len(INTERVAL_DAYS):
            continue                            # mastered: retired
        when = parse_ts(eps[-1]["ts"]) + dt.timedelta(days=INTERVAL_DAYS[stage])
        if when <= now:
            out.append({"ref": ref, "stage": stage, "due": when.isoformat(timespec="minutes"),
                        "last_flaws": eps[-1].get("flaws", []),
                        "stored": os.path.exists(os.path.join(d(key), "items", ref))})
    return sorted(out, key=lambda x: x["due"])


def main(a):
    if len(a) < 2:
        print(__doc__); return 2
    cmd, key = a[0], a[1]
    if cmd == "init":
        lvl = int(a[a.index("--default-level") + 1]) if "--default-level" in a else None
        print(init(key, lvl))
    elif cmd == "path":
        print(d(key))
    elif cmd == "profile":
        init(key)
        print(open(os.path.join(d(key), "profile.md")).read(), end="")
    elif cmd == "rebuild":
        print(rebuild(key))
    elif cmd == "append":
        try:
            print(append(key, json.load(sys.stdin)))
        except (ValueError, json.JSONDecodeError) as e:
            print(f"memory: not saved: {e}", file=sys.stderr); return 1
    elif cmd == "tail":
        for e in read_log(key)[-(int(a[2]) if len(a) > 2 else 5):]:
            print(json.dumps(e))
    elif cmd == "seen":
        return 0 if any(e["item"]["ref"] == a[2] for e in read_log(key)) else 1
    elif cmd == "note":
        note(key, a[2])
    elif cmd == "save-item":
        init(key)
        dst = os.path.join(d(key), "items", a[2])
        shutil.rmtree(dst, ignore_errors=True)
        if os.path.isdir(a[3]):
            shutil.copytree(a[3], dst)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(a[3], dst)
    elif cmd == "due":
        print(json.dumps(due(key, a[a.index("--now") + 1] if "--now" in a else None), indent=1))
    else:
        print(__doc__); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
