#!/usr/bin/env python3
"""Ground-truth runner for prep-cpp. Every predict/debug/"does it compile" item is executed here first.

  cppcheck.py run <file.cpp> [--std c++20]
      Compiles at -O0 AND -O2 with -Wall -Wextra and ASan+UBSan, runs all, prints JSON:
      {"compiles":bool,"diagnostics":"...","stdout":"...","deterministic":bool,"ub":[...],"warnings":[...],
       "verdict":"OK|COMPILE_ERROR|UB|UNSPECIFIED"}
  cppcheck.py fails <file.cpp> [--std c++20]     expect a compile error; prints the first diagnostic
Only use items with verdict OK (clean, deterministic) for "what does this print"; use UB items only when the
question is explicitly "is this UB / what goes wrong"; discard UNSPECIFIED items for output questions.
(g++ 13: coroutines/concepts/ranges are fine; modules are unreliable, so never verify modules with this tool.)
"""
import json, os, re, subprocess, sys, tempfile


def sh(cmd, timeout=20):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return None, "", "timeout"


def run(src, std):
    td = tempfile.mkdtemp(); outs, warns = [], []
    base = ["g++", f"-std={std}", "-Wall", "-Wextra", "-pipe"]
    cfgs = {"O0": ["-O0"], "O2": ["-O2"], "san": ["-O1", "-g", "-fsanitize=address,undefined", "-fno-sanitize-recover=undefined"]}
    res = {}
    for name, fl in cfgs.items():
        exe = os.path.join(td, name)
        rc, _, err = sh(base + fl + [src, "-o", exe], 120)
        if rc != 0:
            return {"compiles": False, "diagnostics": err[:1500], "verdict": "COMPILE_ERROR"}
        if name == "O0":
            warns = sorted(set(re.findall(r"\[(-W[\w-]+)\]", err)))
        rc, out, e = sh([exe])
        res[name] = (rc, out, e)
    ub = sorted({m for m in ("signed integer overflow", "out of bounds", "heap-buffer-overflow", "stack-buffer-overflow", "use-after-free",
                             "use-after-scope", "null pointer", "misaligned", "dereference of null", "shift exponent", "double-free",
                             "invalid vptr", "stack-use-after-return", "heap-use-after-free", "division by zero") if m in res["san"][2]})
    det = res["O0"][1] == res["O2"][1] == res["san"][1] and res["O0"][0] == res["O2"][0]
    verdict = "UB" if ub else "OK" if det else "UNSPECIFIED"
    return {"compiles": True, "stdout": res["O0"][1][:2000], "exit_code": res["O0"][0], "deterministic": det, "ub": ub,
            "warnings": warns, "sanitizer_report": res["san"][2][:600] if ub else "", "verdict": verdict}


def main(a):
    if len(a) < 2 or a[0] not in ("run", "fails"):
        print(__doc__); return 2
    std = a[a.index("--std") + 1] if "--std" in a else "c++20"
    if a[0] == "fails":
        rc, _, err = sh(["g++", f"-std={std}", "-fsyntax-only", a[1]], 60)
        first = next((l for l in err.splitlines() if "error" in l), "")
        print(json.dumps({"compile_error": rc != 0, "first_diagnostic": first})); return 0 if rc != 0 else 1
    r = run(a[1], std); print(json.dumps(r, indent=1)); return 0 if r["verdict"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
