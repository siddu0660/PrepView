#!/usr/bin/env python3
"""C++ problem verifier + solution judge for prep-dsa. Stdlib only.

  judge.py verify <problem_dir> [--allow-fast-brute]
  judge.py judge  <problem_dir> <solution.cpp>
  judge.py selftest                     run the bundled example end to end

Problem dir (all authored by Claude into the scratchpad, never the repo):
  statement.md   shown to the user (verify never reads it; present it only after verify passes)
  ref.cpp        intended solution          brute.cpp   independent brute force
  gen.cpp        ./gen <seed> <n>  -> one input on stdout (deterministic in seed,n)
  checker.cpp    optional; ./checker <input> <expected> <actual>, exit 0 = accept
                 (use when several outputs are valid)
  edge/*.in      hand-written edge inputs (empty/min/max/duplicates/extremes)
  meta.json      {"small_max_n":8,"small_cases":200,"large_n":200000,"large_cases":2,
                  "tl_s":2.0,"checker":false}

Output: one JSON object on stdout. verify -> {"ok":bool,"stage":...,"detail":...}.
judge -> {"verdict":"AC|CE|WA|RE|TLE|SAN","flaws":[...],"time_s":..,"case":..,"detail":..}.
Exit code 0 iff ok / AC.
"""
import glob, hashlib, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = ThreadPoolExecutor(max_workers=os.cpu_count() or 4)

STD = ["g++", "-std=c++20", "-O2", "-pipe"]
SAN = ["g++", "-std=c++20", "-O1", "-g", "-fsanitize=address,undefined", "-fno-sanitize-recover=undefined", "-pipe"]
WARN = ["-Wall", "-Wextra"]
SAN_MAP = [
    (r"heap-buffer-overflow|stack-buffer-overflow|global-buffer-overflow|index .* out of bounds", "F-OOB"),
    (r"signed integer overflow", "F-INT-OVERFLOW"),
    (r"use-after-free|use-after-scope|use-after-return", "F-LIFETIME"),
    (r"null pointer|SEGV on unknown address 0x0000000000", "F-NULL"),
    (r"division by zero", "F-DIV-ZERO"),
    (r"shift exponent|shift of negative", "F-UB-SHIFT"),
    (r"stack-overflow", "F-RECURSION-DEPTH"),
    (r"container-overflow", "F-STL-MISUSE"),
]


def sh(cmd, inp=None, timeout=10, cwd=None):
    t = time.perf_counter()
    try:
        p = subprocess.run(cmd, input=inp, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return p.returncode, p.stdout, p.stderr, time.perf_counter() - t
    except subprocess.TimeoutExpired:
        return None, "", "timeout", time.perf_counter() - t


def ensure_pch(san):
    """Precompiled <bits/stdc++.h> per flag-set (first use ~5s, then every compile is ~4x faster)."""
    root = os.path.join(HERE, ".pch", "san" if san else "std")
    gch = os.path.join(root, "bits", "stdc++.h.gch")
    if os.path.exists(gch):
        return ["-I", root]
    try:
        _, _, err, _ = sh(["g++", "-std=c++20", "-H", "-E", "-x", "c++", "-"], "#include <bits/stdc++.h>\n", 30)
        real = next(l.split()[-1] for l in err.splitlines() if l.startswith(". ") and l.endswith("bits/stdc++.h"))
        os.makedirs(os.path.join(root, "bits"), exist_ok=True)
        hdr = os.path.join(root, "bits", "stdc++.h")
        open(hdr, "w").write(f'#include "{real}"\n')
        rc, _, _, _ = sh((SAN if san else STD) + ["-x", "c++-header", hdr, "-o", gch], timeout=120)
        return ["-I", root] if rc == 0 else []
    except Exception:
        return []


def compile_(src, out, san=False, warn=False):
    flags = (SAN if san else STD) + (WARN if warn else [])
    key = hashlib.sha1((open(src).read() + " ".join(flags)).encode()).hexdigest()
    if os.path.exists(out) and os.path.exists(out + ".key") and open(out + ".key").read() == key + "|ok":
        return True, ""
    rc, _, err, _ = sh(flags + ensure_pch(san) + [src, "-o", out], timeout=120)
    if rc == 0:
        open(out + ".key", "w").write(key + "|ok")
    return rc == 0, err


def load_meta(d):
    m = {"small_max_n": 8, "small_cases": 200, "large_n": 200000, "large_cases": 2, "tl_s": 2.0, "checker": False}
    p = os.path.join(d, "meta.json")
    if os.path.exists(p):
        m.update(json.load(open(p)))
    return m


def same(meta, d, inp_path, exp, act):
    if not meta["checker"]:
        return exp.split() == act.split()
    ep, ap = inp_path + ".exp", inp_path + ".act"
    open(ep, "w").write(exp); open(ap, "w").write(act)
    rc, *_ = sh([os.path.join(d, ".build", "checker"), inp_path, ep, ap], timeout=10)
    return rc == 0


def build_common(d, names, san_names=()):
    b = os.path.join(d, ".build"); os.makedirs(b, exist_ok=True)
    list(POOL.map(ensure_pch, (False, True)))          # build both PCHs before fan-out
    jobs = []
    for n in names:
        src = os.path.join(d, n + ".cpp")
        if not os.path.exists(src):
            return None, f"missing {n}.cpp"
        jobs.append((n, POOL.submit(compile_, src, os.path.join(b, n), n in san_names)))
    for n, fut in jobs:
        ok, err = fut.result()
        if not ok:
            return None, f"{n}.cpp does not compile:\n{err[:800]}"
    return b, None


def gen_input(b, seed, n):
    rc, out, err, _ = sh([os.path.join(b, "gen"), str(seed), str(n)], timeout=10)
    return (out, None) if rc == 0 else (None, f"gen failed seed={seed} n={n}: {err[:200]}")


def test_inputs(d, meta, b, small_only=False):
    """Yield (label, input_text): edge files, then small random with ascending n."""
    for p in sorted(glob.glob(os.path.join(d, "edge", "*.in"))):
        yield "edge/" + os.path.basename(p), open(p).read()
    cases, mx = meta["small_cases"], meta["small_max_n"]
    for i in range(cases):
        n = 1 + (i * mx) // max(cases, 1)
        inp, err = gen_input(b, i + 1, n)
        yield f"small seed={i + 1} n={n}", inp if inp is not None else err
    if small_only:
        return


def _verify_case(meta, d, b, idx, label, inp):
    ip = os.path.join(b, f"v{idx}.in"); open(ip, "w").write(inp)
    rr, ro, re_, _ = sh([os.path.join(b, "ref_san")], inp, 10)
    if rr != 0:
        return {"ok": False, "stage": "ref-crash", "detail": f"{label}: ref failed under sanitizers: {re_[:400]}"}
    br, bo, be, _ = sh([os.path.join(b, "brute")], inp, 20)
    if br != 0:
        return {"ok": False, "stage": "brute-crash", "detail": f"{label}: {be[:300]}"}
    if not same(meta, d, ip, ro, bo):
        return {"ok": False, "stage": "mismatch", "detail": f"ref != brute on {label}\ninput:\n{inp[:300]}\nref: {ro[:100]}\nbrute: {bo[:100]}"}
    return None


def verify(d, allow_fast_brute=False):
    meta = load_meta(d)
    names = ["ref", "brute", "gen"] + (["checker"] if meta["checker"] else [])
    b, err = build_common(d, names)
    if err:
        return {"ok": False, "stage": "compile", "detail": err}
    ok, serr = compile_(os.path.join(d, "ref.cpp"), os.path.join(b, "ref_san"), san=True)
    if not ok:
        return {"ok": False, "stage": "compile-san", "detail": serr[:800]}
    cases = list(test_inputs(d, meta, b))
    for label, inp in cases:
        if inp is None or inp.startswith("gen failed"):
            return {"ok": False, "stage": "gen", "detail": inp}
    res = list(POOL.map(lambda t: _verify_case(meta, d, b, t[0], *t[1]), enumerate(cases)))
    bad = next((r for r in res if r), None)
    if bad:
        return bad
    nedge = sum(l.startswith("edge") for l, _ in cases); nsmall = len(cases) - nedge
    if nedge == 0:
        return {"ok": False, "stage": "no-edge-cases", "detail": "add at least one edge/*.in (empty/min/max)"}
    worst = 0.0
    for c in range(meta["large_cases"]):
        inp, e = gen_input(b, 1000 + c, meta["large_n"])
        if inp is None:
            return {"ok": False, "stage": "gen-large", "detail": e}
        brute_f = None if (allow_fast_brute or c) else POOL.submit(sh, [os.path.join(b, "brute")], inp, meta["tl_s"] * 1.2)
        rr, _, re_, t = sh([os.path.join(b, "ref")], inp, meta["tl_s"] * 3)
        worst = max(worst, t)
        if rr != 0 or t > meta["tl_s"]:
            return {"ok": False, "stage": "ref-too-slow", "detail": f"ref took {t:.2f}s (limit {meta['tl_s']}s) rc={rr}"}
        if brute_f:
            br, _, _, bt = brute_f.result()
            if br == 0 and bt <= meta["tl_s"]:
                return {"ok": False, "stage": "brute-passes-limit",
                        "detail": f"brute finished in {bt:.2f}s at max constraints; raise large_n or pass --allow-fast-brute for level-1 items"}
    return {"ok": True, "stage": "verified", "detail": f"{nedge} edge + {nsmall} small cases agree under ASan/UBSan; ref max {worst:.2f}s / {meta['tl_s']}s"}


def classify(err):
    return sorted({code for pat, code in SAN_MAP if re.search(pat, err)})


def _judge_case(meta, d, b, idx, label, inp):
    ip = os.path.join(b, f"j{idx}.in"); open(ip, "w").write(inp)
    _, exp, _, _ = sh([os.path.join(b, "ref")], inp, 10)
    rc, out, e, t = sh([os.path.join(b, "sol_san")], inp, meta["tl_s"] * 10)
    case = {"case": label, "input": inp if len(inp) <= 400 else inp[:200] + "..."}
    edge = label.startswith("edge") or inp.split()[:1] in (["0"], ["1"])
    if rc is None:
        return {"verdict": "TLE", "flaws": ["F-TLE-COMPLEXITY"], **case, "detail": "hangs on a tiny input (infinite loop?)"}
    if rc != 0 or "runtime error" in e or "Sanitizer" in e:
        return {"verdict": "SAN" if classify(e) else "RE", "flaws": (classify(e) or ["F-RE-CRASH"]) + (["F-EDGE-CASE"] if edge else []),
                **case, "detail": e[:500]}
    if not same(meta, d, ip, exp, out):
        return {"verdict": "WA", "flaws": ["F-WA-LOGIC"] + (["F-EDGE-CASE"] if edge else []),
                **case, "expected": exp[:150], "got": out[:150], "detail": "wrong answer on smallest failing case"}
    return None


def judge(d, sol):
    meta = load_meta(d)
    names = ["ref", "gen"] + (["checker"] if meta["checker"] else [])
    b, err = build_common(d, names)
    if err:
        return {"verdict": "ERR", "flaws": [], "detail": "problem harness broken: " + err}
    f_plain = POOL.submit(compile_, sol, os.path.join(b, "sol"), False, True)
    f_san = POOL.submit(compile_, sol, os.path.join(b, "sol_san"), True, False)
    ok, cerr = f_plain.result()
    if not ok:
        return {"verdict": "CE", "flaws": [], "detail": cerr[:1200]}
    warn_flaws = ["F-UNINIT"] if re.search(r"may be used uninitiali[sz]ed|is used uninitiali[sz]ed", cerr) else []
    ok, serr = f_san.result()
    if not ok:
        return {"verdict": "CE", "flaws": [], "detail": serr[:1200]}
    cases = list(test_inputs(d, meta, b))
    res = list(POOL.map(lambda t: _judge_case(meta, d, b, t[0], *t[1]), enumerate(cases)))
    bad = next((r for r in res if r), None)
    if bad:
        bad["flaws"] = list(dict.fromkeys(bad["flaws"] + warn_flaws))
        return bad
    worst = 0.0
    src_text = open(sol).read()
    for c in range(meta["large_cases"]):
        inp, e = gen_input(b, 1000 + c, meta["large_n"])
        _, exp, _, _ = sh([os.path.join(b, "ref")], inp, meta["tl_s"] * 3)
        rc, out, e, t = sh([os.path.join(b, "sol")], inp, meta["tl_s"] * 1.5)
        worst = max(worst, t)
        case = {"case": f"large seed={1000 + c} n={meta['large_n']}"}
        if rc is None or t > meta["tl_s"]:
            return {"verdict": "TLE", "flaws": ["F-TLE-COMPLEXITY"] + warn_flaws, **case, "time_s": round(t, 2),
                    "detail": f"limit {meta['tl_s']}s at n={meta['large_n']}: complexity too high"}
        if rc != 0:
            return {"verdict": "RE", "flaws": (classify(e) or ["F-RE-CRASH"]) + warn_flaws, **case, "detail": e[:300]}
        ip = os.path.join(b, "jl.in"); open(ip, "w").write(inp)
        if not same(meta, d, ip, exp, out):
            fl = ["F-WA-LOGIC"] + (["F-INT-OVERFLOW"] if "long long" not in src_text and "int64" not in src_text else [])
            return {"verdict": "WA", "flaws": fl + warn_flaws, **case, "detail":
                    "passes small cases, fails at scale: overflow (int vs long long) or a bug that only triggers for large n"}
    return {"verdict": "AC", "flaws": warn_flaws, "time_s": round(worst, 2), "detail": f"all tests passed; max {worst:.2f}s / {meta['tl_s']}s"}


def selftest():
    here = os.path.dirname(os.path.abspath(__file__))
    ex = os.path.join(here, "example")
    v = verify(ex)
    fails = [] if v["ok"] else [f"example failed verify: {v}"]
    want = {"good.cpp": "AC", "wrong.cpp": "WA", "overflow.cpp": None, "slow.cpp": "TLE", "crash.cpp": None, "broken.cpp": "CE"}
    for name, exp in want.items():
        r = judge(ex, os.path.join(ex, "sols", name))
        got = r["verdict"]
        if exp is None:
            if got not in ("SAN", "WA", "RE"):
                fails.append(f"{name}: expected SAN/WA/RE got {got}")
        elif got != exp:
            fails.append(f"{name}: expected {exp} got {got} ({r.get('detail')})")
        print(f"  {name:13s} -> {got:4s} {r.get('flaws', [])}")
    print("selftest:", "OK" if not fails else "FAILED\n" + "\n".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["selftest"]:
        sys.exit(selftest())
    if len(a) >= 2 and a[0] == "verify":
        r = verify(a[1], "--allow-fast-brute" in a); print(json.dumps(r, indent=1)); sys.exit(0 if r["ok"] else 1)
    if len(a) >= 3 and a[0] == "judge":
        r = judge(a[1], a[2]); print(json.dumps(r, indent=1)); sys.exit(0 if r["verdict"] == "AC" else 1)
    print(__doc__); sys.exit(2)
