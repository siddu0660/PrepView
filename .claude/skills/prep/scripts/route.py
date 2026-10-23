#!/usr/bin/env python3
"""Deterministic router for /prep.

Usage: route.py "<raw arguments>"
Prints one JSON object:
  {"status": "ok"|"ask", "domain": {...}|null, "memory_key": "quant/prob",
   "mode": ..., "difficulty": int|null, "n": int, "timed": bool, "text": "...",
   "candidates": [...], "reason": "..."}
Flags beat free-text inference. Free text never guesses silently: low score or
a thin margin returns status "ask" with the top candidates.
"""
import json, os, re, shlex, sys

SKILLS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
MIN_SCORE = 2      # minimum trigger score to route without asking
MIN_MARGIN = 2     # lead over the runner-up required to route without asking

DIFF_WORDS = [("beginner", 1), ("very hard", 5), ("expert", 5), ("easy", 2),
              ("medium", 3), ("hard", 4)]
MODE_WORDS = [("quiz", ["quiz", "mcq", "test me", "questions on"]),
              ("mock", ["mock", "simulate interview", "interview me"]),
              ("review", ["review", "revise", "revision", "recap"]),
              ("explain", ["explain", "clear", "teach", "understand", "what is", "how does"]),
              ("drill", ["drill", "speed run"]),
              ("story", ["story", "stories", "star answer"]),
              ("design", ["design"]),
              ("problem", ["problem", "new question", "give me a"])]


def load(path):
    with open(os.path.join(SKILLS, path)) as f:
        return json.load(f)


def flatten(registry_path, parent=None):
    """Yield every domain node with its full memory key; children inlined."""
    out = []
    for d in load(registry_path)["domains"]:
        key = f"{parent}/{d['id']}" if parent else d["id"]
        node = dict(d, memory_key=key, parent=parent)
        out.append(node)
        if d.get("children"):
            out.extend(flatten(d["children"], key))
    return out


def tokenize(raw):
    try:
        return shlex.split(raw)
    except ValueError:
        return raw.split()


def parse(raw):
    toks, text, flags = tokenize(raw), [], []
    opts = {"difficulty": None, "n": 1, "mode": None, "timed": False}
    i = 0
    while i < len(toks):
        t = toks[i]
        if t in ("-d", "--difficulty", "--level") and i + 1 < len(toks):
            opts["difficulty"] = max(1, min(5, int(toks[i + 1]))); i += 2; continue
        if t in ("-n", "--count") and i + 1 < len(toks):
            opts["n"] = max(1, int(toks[i + 1])); i += 2; continue
        if t == "--mode" and i + 1 < len(toks):
            opts["mode"] = toks[i + 1].lower(); i += 2; continue
        if t == "--timed":
            opts["timed"] = True; i += 1; continue
        if t.startswith("--"):
            flags.append(t.lower())
        else:
            text.append(t)
        i += 1
    return opts, flags, " ".join(text)


def score(node, text):
    low = re.sub(r"[^a-z0-9+#\- ]", " ", text.lower())
    s = 0
    for trig in node.get("triggers", []):
        # whole-phrase match, tolerant of simple plurals ("deadlocks", "graphs")
        if re.search(rf"(?<![a-z0-9]){re.escape(trig.lower())}(?:e?s)?(?![a-z0-9])", low):
            s += 1 + len(trig.split())     # longer phrases are more specific
    return s


def infer_mode(text):
    low = text.lower()
    for mode, words in MODE_WORDS:
        if any(w in low for w in words):
            return mode
    return None


def infer_difficulty(text):
    low = text.lower()
    for w, v in DIFF_WORDS:
        if re.search(rf"\b{w}\b", low):
            return v
    m = re.search(r"\b(?:level|difficulty)\s*([1-5])\b", low)
    return int(m.group(1)) if m else None


def finish(status, node, opts, text, cands, reason, nodes):
    mode = opts["mode"] or infer_mode(text)
    diff = opts["difficulty"] or infer_difficulty(text)
    if node and mode and node.get("modes") and mode not in node["modes"]:
        reason += f" (mode '{mode}' not offered by {node['id']}; using default)"
        mode = None
    if node:
        mode = mode or node.get("default_mode")
    slim = None
    if node:
        slim = {k: node.get(k) for k in ("id", "skill", "path", "kind", "modes", "default_mode", "default_difficulty")}
    return {"status": status, "domain": slim, "memory_key": node["memory_key"] if node else None,
            "mode": mode, "difficulty": diff, "n": opts["n"], "timed": opts["timed"],
            "text": text, "candidates": [c["memory_key"] for c in cands], "reason": reason}


def route(raw):
    nodes = flatten("prep/registry.json")
    opts, flags, text = parse(raw)
    by_flag = {}
    for n in nodes:
        for f in n.get("flags", []):
            by_flag[f] = n
    hit = [by_flag[f] for f in flags if f in by_flag]
    unknown = [f for f in flags if f not in by_flag]
    if unknown and not hit:
        return finish("ask", None, opts, text, [], f"unknown flag(s) {unknown}", nodes)
    if hit:
        node = hit[0]
        if node.get("children"):                       # parent flag: pick a child
            kids = [n for n in nodes if n["parent"] == node["memory_key"]]
            ranked = sorted(kids, key=lambda k: -score(k, text))
            if len(ranked) == 1 or (score(ranked[0], text) - (score(ranked[1], text) if len(ranked) > 1 else 0)) >= 1 and score(ranked[0], text) > 0:
                return finish("ok", ranked[0], opts, text, ranked, f"flag {node['id']} + trigger match", nodes)
            return finish("ask", None, opts, text, ranked, f"--{node['id']} has sub-domains; which one?", nodes)
        return finish("ok", node, opts, text, [node], f"explicit flag {flags[0]}", nodes)
    leaves = [n for n in nodes if not n.get("children")]
    ranked = sorted(leaves, key=lambda n: -score(n, text))
    top = score(ranked[0], text) if ranked else 0
    second = score(ranked[1], text) if len(ranked) > 1 else 0
    parents = sorted((n for n in nodes if n.get("children")), key=lambda n: -score(n, text))
    if parents and score(parents[0], text) >= MIN_SCORE and score(parents[0], text) > top:
        kids = [n for n in nodes if n["parent"] == parents[0]["memory_key"]]
        return finish("ask", None, opts, text, kids, f"matched '{parents[0]['id']}' but not a sub-domain; which one?", nodes)
    if top >= MIN_SCORE and top - second >= MIN_MARGIN:
        return finish("ok", ranked[0], opts, text, ranked[:3], f"trigger score {top} vs {second}", nodes)
    return finish("ask", None, opts, text, ranked[:3], f"low confidence (top={top}, second={second})", nodes)


if __name__ == "__main__":
    print(json.dumps(route(" ".join(sys.argv[1:])), indent=2))
