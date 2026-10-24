#!/usr/bin/env python3
"""Seeded-bug repo verifier + judge for prep-aidebug. Python stdlib only.

  judge.py verify <problem_dir>
  judge.py judge  <problem_dir> <work_tree>     work_tree = the user's edited copy of repo/ (+ tests_public/)
  judge.py selftest                             verify + judge the bundled example end to end

Problem dir (authored by Claude into the scratchpad, never the repo):
  repo/            buggy tree shown to the user (python packages at its root, README.md)
  fixed/           reference tree (same layout, all bugs fixed)
  tests_public/    test_*.py (unittest) given to the user, expose at least one bug
  tests_hidden/    test_*.py graded at the end; cover every bug plus regression behaviour
  meta.json        {"time_box_s":1800,
                    "bugs":[{"id":"b1","file":"pkg/mod.py","buggy":"<snippet in repo/>","fixed":"<same place in fixed/>",
                             "class":"off-by-one","technique":"Invariants and boundaries"}],
                    "ai_traps":[{"claim":"...","why_wrong":"...","proof":"how to disprove by running"}]}  (ai_traps optional, level 3+)

Trees run as: cwd=<tree>, tests copied to tests/public and tests/hidden, `python -m unittest` (tests import packages from the tree root).
verify -> {"ok":bool,"stage":..,"detail":..}; judge -> per-bug status, regressions, tampering, diff sizes, flaws.
Exit code 0 iff ok / (judge: all bugs fixed with no regression).
"""
import difflib, hashlib, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = r'''
import json, sys, unittest
res = {}
class R(unittest.TextTestResult):
    def _rec(self, t, s, e=None):
        m = ""
        if e is not None:
            m = str(e[1]).strip().splitlines()[-1][:300] if str(e[1]).strip() else e[0].__name__
        res[t.id()] = [s, m]
    def addSuccess(self, t): super().addSuccess(t); self._rec(t, "ok")
    def addFailure(self, t, e): super().addFailure(t, e); self._rec(t, "fail", e)
    def addError(self, t, e): super().addError(t, e); self._rec(t, "error", e)
    def addSubTest(self, t, st, e):
        super().addSubTest(t, st, e)
        if e is not None: self._rec(t, "fail", e)
suite = unittest.defaultTestLoader.discover("tests", pattern="test_*.py", top_level_dir=".")
unittest.TextTestRunner(stream=open("/dev/null", "w"), resultclass=R).run(suite)
print("@@" + json.dumps(res))
'''
SKIP = {"__pycache__", "tests_public", "tests_hidden", ".git", "tests"}


def copy_tree(src, dst):
    for r, ds, fs in os.walk(src):
        ds[:] = [d for d in ds if d not in SKIP and not d.endswith(".pyc")]
        for f in fs:
            if f.endswith(".pyc"): continue
            p = os.path.join(r, f); q = os.path.join(dst, os.path.relpath(p, src))
            os.makedirs(os.path.dirname(q), exist_ok=True); shutil.copy2(p, q)


def py_files(root):
    out = {}
    for r, ds, fs in os.walk(root):
        ds[:] = [d for d in ds if d not in SKIP]
        for f in fs:
            if f.endswith(".py"):
                p = os.path.join(r, f); out[os.path.relpath(p, root)] = open(p).read()
    return out


def digest(d):
    h = hashlib.sha256()
    for r, _, fs in sorted(os.walk(d)):
        for f in sorted(fs):
            if f.endswith(".pyc"): continue
            h.update(os.path.relpath(os.path.join(r, f), d).encode()); h.update(open(os.path.join(r, f), "rb").read())
    return h.hexdigest()


def run_tree(tree, pub, hid, timeout=60):
    """-> {test_id:[status,msg]} for public+hidden; raises RuntimeError on harness-level failure."""
    td = tempfile.mkdtemp(prefix="aidbg-")
    try:
        copy_tree(tree, td)
        for name, src in (("public", pub), ("hidden", hid)):
            dst = os.path.join(td, "tests", name); os.makedirs(dst, exist_ok=True)
            open(os.path.join(td, "tests", "__init__.py"), "a").close(); open(os.path.join(dst, "__init__.py"), "a").close()
            if src and os.path.isdir(src):
                for f in os.listdir(src):
                    if f.endswith(".py"): shutil.copy2(os.path.join(src, f), dst)
        try:
            p = subprocess.run([sys.executable, "-B", "-c", RUNNER], cwd=td, capture_output=True, text=True, timeout=timeout,
                               env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"})
        except subprocess.TimeoutExpired:
            raise RuntimeError("test run timed out")
        line = next((l for l in p.stdout.splitlines() if l.startswith("@@")), None)
        if line is None:
            raise RuntimeError("runner produced no result: " + (p.stderr or p.stdout)[-400:])
        return json.loads(line[2:])
    finally:
        shutil.rmtree(td, ignore_errors=True)


def failing(res):
    return {t for t, (s, _) in res.items() if s != "ok"}


def apply_bugs(fixed_dir, bugs, dst):
    """Copy fixed/ to dst and re-introduce the given bugs by replacing the 'fixed' snippet with 'buggy'."""
    copy_tree(fixed_dir, dst)
    for b in bugs:
        p = os.path.join(dst, b["file"]); s = open(p).read()
        if s.count(b["fixed"]) != 1:
            raise RuntimeError(f"bug {b['id']}: 'fixed' snippet must occur exactly once in fixed/{b['file']} (found {s.count(b['fixed'])})")
        open(p, "w").write(s.replace(b["fixed"], b["buggy"]))


def load(P):
    m = json.load(open(os.path.join(P, "meta.json")))
    if not m.get("bugs"): raise RuntimeError("meta.json needs a non-empty 'bugs' list")
    for b in m["bugs"]:
        for k in ("id", "file", "buggy", "fixed", "class", "technique"):
            if k not in b: raise RuntimeError(f"bug missing '{k}': {b.get('id')}")
    return m


def isolated_sets(P, m):
    pub, hid = os.path.join(P, "tests_public"), os.path.join(P, "tests_hidden")
    sets = {}
    for b in m["bugs"]:
        td = tempfile.mkdtemp(prefix="aidbg-iso-")
        try:
            apply_bugs(os.path.join(P, "fixed"), [b], td)
            sets[b["id"]] = failing(run_tree(td, pub, hid))
        finally:
            shutil.rmtree(td, ignore_errors=True)
    return sets


def verify(P):
    def out(ok, stage, detail): print(json.dumps({"ok": ok, "stage": stage, "detail": detail})); return 0 if ok else 1
    try:
        for d in ("repo", "fixed", "tests_public", "tests_hidden"):
            if not os.path.isdir(os.path.join(P, d)): return out(False, "structure", f"missing {d}/")
        m = load(P)
        pub, hid = os.path.join(P, "tests_public"), os.path.join(P, "tests_hidden")
        # 1. meta describes exactly the difference between fixed/ and repo/
        td = tempfile.mkdtemp(prefix="aidbg-all-")
        try:
            apply_bugs(os.path.join(P, "fixed"), m["bugs"], td)
            if digest(td) != digest_no_tests(os.path.join(P, "repo")):
                return out(False, "meta-mismatch", "fixed/ with all bugs re-applied does not equal repo/ (undocumented difference)")
        finally:
            shutil.rmtree(td, ignore_errors=True)
        # 2. reference passes everything, twice (determinism)
        r1 = run_tree(os.path.join(P, "fixed"), pub, hid); r2 = run_tree(os.path.join(P, "fixed"), pub, hid)
        if not r1: return out(False, "no-tests", "no tests discovered")
        if failing(r1): return out(False, "reference-fails", sorted(failing(r1))[:3])
        if r1.keys() != r2.keys(): return out(False, "nondeterministic", "test set differs between runs")
        # 3. buggy tree fails public and hidden
        rb = run_tree(os.path.join(P, "repo"), pub, hid)
        pf = [t for t in failing(rb) if ".public." in t]; hf = [t for t in failing(rb) if ".hidden." in t]
        if not pf: return out(False, "public-passes", "public tests must expose at least one bug")
        if not hf: return out(False, "hidden-passes", "hidden tests must fail on the buggy tree")
        # 4. every bug independently observable; every failing test in repo is explained by some bug
        sets = isolated_sets(P, m)
        for bid, s in sets.items():
            if not s: return out(False, "bug-unobservable", f"{bid}: no test fails when only this bug is present")
        explained = set().union(*sets.values())
        unexplained = failing(rb) - explained
        if unexplained: return out(False, "unexplained-failure", sorted(unexplained)[:3])
        if not any(s & set(pf) for s in sets.values()): return out(False, "public-useless", "no public failure maps to a bug")
        return out(True, "verified", f"{len(m['bugs'])} bugs, {len(r1)} tests ({len(pf)} public failing, {len(hf)} hidden failing on repo); each bug isolated-observable")
    except RuntimeError as e:
        return out(False, "error", str(e))


def digest_no_tests(d):
    return digest(d)


def diff_lines(a, b):
    fa, fb = py_files(a), py_files(b); n = 0
    for k in sorted(set(fa) | set(fb)):
        for l in difflib.unified_diff(fa.get(k, "").splitlines(), fb.get(k, "").splitlines(), lineterm="", n=0):
            if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---")): n += 1
    return n


def judge(P, W):
    try:
        m = load(P); pub, hid = os.path.join(P, "tests_public"), os.path.join(P, "tests_hidden")
        sets = isolated_sets(P, m)
        base = run_tree(os.path.join(P, "repo"), pub, hid)
        wp = os.path.join(W, "tests_public")
        tampered = os.path.isdir(wp) and digest(wp) != digest(pub)
        user = run_tree(W, pub, hid)                      # graded against the ORIGINAL tests, never the user's edited ones
        uf = failing(user)
        bugs = [{"id": b["id"], "class": b["class"], "technique": b["technique"], "fixed": not (sets[b["id"]] & uf)} for b in m["bugs"]]
        reg = sorted(t for t, (s, _) in base.items() if s == "ok" and user.get(t, ["error"])[0] != "ok")
        missing = sorted(t for t in base if t not in user)
        ud, rd = diff_lines(os.path.join(P, "repo"), W), diff_lines(os.path.join(P, "repo"), os.path.join(P, "fixed"))
        nfixed = sum(b["fixed"] for b in bugs); flaws = []
        if reg: flaws.append("F-AI-REGRESSION")
        if tampered: flaws.append("F-AI-TEST-TAMPER")
        if ud > 3 * max(rd, 1) + 10: flaws.append("F-AI-OVERSCOPE")
        if 0 < nfixed < len(bugs): flaws.append("F-AI-STOPPED-EARLY")
        first = next(((t, user[t][1]) for t in sorted(uf)), None)
        res = {"bugs": bugs, "bugs_fixed": nfixed, "bugs_total": len(bugs), "regressions": reg, "missing_tests": missing,
               "tests_tampered": tampered, "diff_lines": ud, "reference_diff_lines": rd,
               "hidden_failing": len([t for t in uf if ".hidden." in t]), "public_failing": len([t for t in uf if ".public." in t]),
               "first_failure": {"test": first[0], "message": first[1]} if first else None, "flaws": flaws}
        print(json.dumps(res, indent=1))
        return 0 if nfixed == len(bugs) and not reg and not tampered and not missing else 1
    except RuntimeError as e:
        print(json.dumps({"error": str(e)})); return 2


def selftest():
    P = os.path.join(HERE, "example"); fails = []
    if verify(P) != 0: fails.append("verify(example)")
    td = tempfile.mkdtemp(prefix="aidbg-st-")
    try:
        m = load(P)
        for name, bugs_left, want_rc in (("reference", [], 0), ("buggy", m["bugs"], 1), ("half", m["bugs"][1:], 1)):
            W = os.path.join(td, name); apply_bugs(os.path.join(P, "fixed"), bugs_left, W)
            shutil.copytree(os.path.join(P, "tests_public"), os.path.join(W, "tests_public"))
            print(f"-- judge {name}"); rc = judge(P, W)
            if rc != want_rc: fails.append(f"judge({name}) rc={rc} want {want_rc}")
        W = os.path.join(td, "tamper"); apply_bugs(os.path.join(P, "fixed"), m["bugs"], W)
        shutil.copytree(os.path.join(P, "tests_public"), os.path.join(W, "tests_public"))
        open(os.path.join(W, "tests_public", "test_tamper.py"), "w").write("# edited\n")
        print("-- judge tamper"); rc = judge(P, W)
        if rc == 0: fails.append("tamper not detected")
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print(json.dumps({"selftest": "FAIL" if fails else "PASS", "failures": fails}))
    return 1 if fails else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["verify"] and len(a) == 2: sys.exit(verify(a[1]))
    if a[:1] == ["judge"] and len(a) == 3: sys.exit(judge(a[1], a[2]))
    if a[:1] == ["selftest"]: sys.exit(selftest())
    print(__doc__); sys.exit(2)
