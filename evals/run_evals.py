#!/usr/bin/env python3
"""PrepView eval suite. Stdlib only. Usage: python3 evals/run_evals.py [--quick] [--only routing|memory|scaffold|drill|harness|mutation]

routing   deterministic router cases (incl. ambiguous ones that MUST ask)
memory    level state machine, dedupe, spaced repetition, batch/atomic append, notes cap
scaffold  new domain from spec in a throw-away copy of the skill tree; collision + lint checks
drill     mental-math generator/grader sanity
helpers   sqlcheck / netcalc / archcalc ground truth (+ cppcheck unless --quick)
harness   C++ judge selftest (compiles; ~25s)           [skipped with --quick]
mutation  seeded-wrong problems the verifier MUST reject [skipped with --quick]
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SK = os.path.join(ROOT, ".claude", "skills")
PY = sys.executable
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    if not cond:
        print(f"  FAIL {name} {detail}")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# ----------------------------------------------------------------------------- routing
ROUTING = [  # (args, expected memory_key | "ASK", expected mode or None, expected difficulty or None)
    ("--dsa", "dsa", "problem", None), ("--algo -d 3", "dsa", None, 3), ("--dsa hard", "dsa", None, 4),
    ("give me a leetcode medium on sliding window", "dsa", None, 3),
    ("binary search on a graph problem", "dsa", None, None),
    ("--dsa --mode review", "dsa", "review", None), ("--dsa --mode quiz -n 5", "dsa", "quiz", None),
    ("quiz me on deadlocks", "os", "quiz", None), ("explain virtual memory and paging", "os", "explain", None),
    ("mutex vs semaphore", "os", None, None), ("--os --mode problem", "os", "quiz", None),
    ("design a url shortener", "hld", None, None), ("caching and sharding trade-offs", "hld", None, None),
    ("--sd", "hld", "design", None), ("--hld --mode mock", "hld", "mock", None),
    ("parking lot design with solid principles", "lld", None, None), ("--oop", "lld", None, None),
    ("tell me about a time I had a conflict with a teammate", "behavioral", None, None),
    ("--hr -d 4", "behavioral", None, 4), ("star method practice", "behavioral", None, None),
    ("--behavioral story", "behavioral", "story", None),
    ("--quant expected value of dice", "quant/prob", None, None), ("--prob", "quant/prob", None, None),
    ("--quant.prob -d 5", "quant/prob", None, 5), ("bayes and conditional probability", "quant/prob", None, None),
    ("--mm -d 3 -n 20", "quant/mental-math", "drill", 3), ("mental math drill", "quant/mental-math", "drill", None),
    ("--quant.mm", "quant/mental-math", None, None),
    ("--db", "db", "quiz", None), ("--dbms -d 4", "db", None, 4), ("explain mvcc and isolation levels", "db", "explain", None),
    ("write a query with a window function and a join", "db", "sql", None), ("normalization to bcnf", "db", None, None),
    ("--cn", "cn", "quiz", None), ("--net -d 3", "cn", None, 3), ("explain the tcp three way handshake", "cn", "explain", None),
    ("subnetting and cidr practice", "cn", None, None), ("quiz me on dns and http", "cn", "quiz", None),
    ("--arch", "arch", "quiz", None), ("cache coherence mesi quiz", "arch", "quiz", None), ("branch prediction and pipeline hazards", "arch", None, None),
    ("amat and set associative cache", "arch", None, None),
    ("--cpp", "cpp", "quiz", None), ("--cpp --mode predict", "cpp", "predict", None), ("move semantics and rvalue references", "cpp", None, None),
    ("spot the bug in this c++ raii code", "cpp", "debug", None), ("explain c++20 concepts", "cpp", "explain", None),
    ("what does this print undefined behavior vtable", "cpp", "predict", None),
    # must ask
    ("", "ASK", None, None), ("give me something", "ASK", None, None), ("practice", "ASK", None, None),
    ("design", "ASK", None, None), ("--quant", "ASK", None, None), ("--foo", "ASK", None, None),
    ("jane street interview prep", "ASK", None, None), ("probability or dsa?", "ASK", None, None),
]


def t_routing():
    for args, key, mode, diff in ROUTING:
        p = run([PY, os.path.join(SK, "prep/scripts/route.py"), *args.split()])
        try:
            r = json.loads(p.stdout)
        except json.JSONDecodeError:
            check(f"route[{args}]", False, p.stderr[:200]); continue
        if key == "ASK":
            check(f"route[{args}] asks", r["status"] == "ask", f"got {r['memory_key']}")
        else:
            check(f"route[{args}] -> {key}", r["status"] == "ok" and r["memory_key"] == key, f"got {r['status']}/{r['memory_key']} ({r['reason']})")
            if mode:
                check(f"route[{args}] mode={mode}", r["mode"] == mode, f"got {r['mode']}")
            if diff:
                check(f"route[{args}] diff={diff}", r["difficulty"] == diff, f"got {r['difficulty']}")
    r = json.loads(run([PY, os.path.join(SK, "prep/scripts/route.py"), "--quant"]).stdout)
    check("route[--quant] offers both children", set(r["candidates"]) == {"quant/prob", "quant/mental-math"}, str(r["candidates"]))
    r = json.loads(run([PY, os.path.join(SK, "prep/scripts/route.py"), "--dsa", "--os"]).stdout)
    check("route: first flag wins", r["memory_key"] == "dsa")


# ----------------------------------------------------------------------------- memory
def ep(ref, outcome, diff=2, ts="2026-10-01T00:00:00Z", tags=("t",), hints=(), flaws=()):
    return {"ts": ts, "domain": "x", "mode": "problem", "difficulty": diff, "item": {"ref": ref, "tags": list(tags)},
            "outcome": outcome, "flaws": list(flaws), "remark": "r", "hints": list(hints)}


def mem(env, *args, inp=None):
    return run([PY, os.path.join(SK, "prep/scripts/memory.py"), *args], input=inp, env=env)


def level(env, key):
    for ln in mem(env, "profile", key).stdout.splitlines():
        if ln.startswith("recommended_level"):
            return int(ln.split(":")[1])


def t_memory():
    tmp = tempfile.mkdtemp(); env = dict(os.environ, PREP_MEMORY_DIR=tmp)
    try:
        mem(env, "init", "a", "--default-level", "2")
        check("mem: default level", level(env, "a") == 2)
        for i in range(2):
            mem(env, "append", "a", inp=json.dumps(ep(f"p{i}", "pass", 2)))
        check("mem: 2 clean passes -> +1", level(env, "a") == 3)
        mem(env, "append", "a", inp=json.dumps(ep("p2", "pass", 3, hints=[1, 2, 3])))  # not clean (3 hints)
        mem(env, "append", "a", inp=json.dumps(ep("p3", "pass", 3)))
        check("mem: hinted pass does not count as clean", level(env, "a") == 3)
        for i in (4, 5):
            mem(env, "append", "a", inp=json.dumps(ep(f"p{i}", "fail", 3)))
        check("mem: 2 fails -> -1", level(env, "a") == 2)
        mem(env, "init", "b", "--default-level", "5")
        mem(env, "append", "b", inp=json.dumps([ep("q1", "pass", 5), ep("q2", "pass", 5)]))
        check("mem: level capped at 5", level(env, "b") == 5)
        mem(env, "init", "c", "--default-level", "1")
        mem(env, "append", "c", inp=json.dumps([ep("q1", "fail", 1), ep("q2", "fail", 1)]))
        check("mem: level floored at 1", level(env, "c") == 1)
        check("mem: seen true", mem(env, "seen", "a", "p0").returncode == 0)
        check("mem: seen false", mem(env, "seen", "a", "nope").returncode == 1)
        bad = mem(env, "append", "a", inp=json.dumps([ep("ok1", "pass"), {"ts": "x"}]))
        check("mem: invalid batch rejected atomically", bad.returncode == 1 and mem(env, "seen", "a", "ok1").returncode == 1)
        check("mem: bad outcome rejected", mem(env, "append", "a", inp=json.dumps(ep("z", "great"))).returncode == 1)
        # spaced repetition
        mem(env, "init", "d")
        mem(env, "append", "d", inp=json.dumps([ep("s1", "fail", ts="2026-10-01T00:00:00Z"), ep("s2", "pass", ts="2026-10-01T00:00:00Z")]))
        due = json.loads(mem(env, "due", "d", "--now", "2026-10-03T00:00:00Z").stdout)
        check("sr: failed item due after 1 day, clean pass never", [x["ref"] for x in due] == ["s1"], str(due))
        check("sr: not due early", json.loads(mem(env, "due", "d", "--now", "2026-10-01T12:00:00Z").stdout) == [])
        mem(env, "append", "d", inp=json.dumps(ep("s1", "pass", ts="2026-10-03T00:00:00Z")))
        due = json.loads(mem(env, "due", "d", "--now", "2026-10-05T00:00:00Z").stdout)
        check("sr: stage 1 interval is 3 days", due == [], str(due))
        due = json.loads(mem(env, "due", "d", "--now", "2026-10-07T00:00:00Z").stdout)
        check("sr: due after 3 days", [x["ref"] for x in due] == ["s1"] and due[0]["stage"] == 1)
        for ts in ("2026-10-07", "2026-10-15", "2026-10-30"):
            mem(env, "append", "d", inp=json.dumps(ep("s1", "pass", ts=ts + "T00:00:00Z")))
        check("sr: retired after 4 consecutive passes", json.loads(mem(env, "due", "d", "--now", "2027-01-01T00:00:00Z").stdout) == [])
        for i in range(40):
            mem(env, "note", "d", f"note {i}")
        lines = open(os.path.join(tmp, "d", "notes.md")).read().splitlines()
        check("mem: notes capped at 30 + header", len(lines) == 31 and lines[-1].endswith("note 39"), str(len(lines)))
        # corrupt line tolerance + profile size
        with open(os.path.join(tmp, "d", "log.jsonl"), "a") as f:
            f.write("{torn\n")
        check("mem: torn log line tolerated", mem(env, "profile", "d").returncode == 0)
        check("mem: profile <= 40 lines", len(mem(env, "profile", "d").stdout.splitlines()) <= 40)
        mem(env, "save-item", "d", "s9", SK + "/prep-dsa/harness/example")
        check("mem: save-item skips .build", os.path.isdir(os.path.join(tmp, "d/items/s9")) and not os.path.exists(os.path.join(tmp, "d/items/s9/.build")))
        check("mem: nested key path", mem(env, "path", "quant/prob").stdout.strip() == os.path.join(tmp, "quant", "prob"))
        check("mem: nothing written into repo", not os.path.exists(os.path.join(ROOT, "prep-memory")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ----------------------------------------------------------------------------- scaffold
def t_scaffold():
    tmp = tempfile.mkdtemp()
    try:
        sk = os.path.join(tmp, "skills"); shutil.copytree(SK, sk, ignore=shutil.ignore_patterns(".build", ".pch", "__pycache__"))
        spec = json.load(open(os.path.join(SK, "prep-new/specs/os.json")))
        spec.update(id="netw", title="Warp Physics", flags=["--zznet"], triggers=["flux capacitor", "warp drive", "dilithium", "tachyon", "quark soup", "antimatter"])
        spec["topics"] = ["tcp", "dns"]; sp = os.path.join(tmp, "netw.json"); json.dump(spec, open(sp, "w"))
        sc = [PY, os.path.join(sk, "prep-new/scripts/scaffold.py")]
        lint = [PY, os.path.join(sk, "prep/scripts/lint.py")]
        r = run(sc + [sp, "--skills-root", sk]); check("scaffold: creates domain", r.returncode == 0, r.stderr)
        check("scaffold: files exist", all(os.path.exists(os.path.join(sk, "prep-netw", f)) for f in
              ("SKILL.md", "references/taxonomy.md", "references/rubric.md", "references/schema.md")))
        check("scaffold: no placeholders left", "{{" not in open(os.path.join(sk, "prep-netw/SKILL.md")).read())
        check("scaffold: lint passes after add", run(lint).returncode == 0, run(lint).stdout)
        check("scaffold: memory not created in repo tree", not os.path.exists(os.path.join(sk, "prep-netw", "memory")))
        r = json.loads(run([PY, os.path.join(sk, "prep/scripts/route.py"), "--zznet"]).stdout)
        check("scaffold: new flag routes", r["memory_key"] == "netw", str(r))
        r = json.loads(run([PY, os.path.join(sk, "prep/scripts/route.py"), "explain flux capacitor and warp drive"]).stdout)
        check("scaffold: new triggers route", r["memory_key"] == "netw", str(r["reason"]))
        check("scaffold: duplicate id refused", run(sc + [sp, "--skills-root", sk]).returncode == 1)
        spec2 = dict(spec, id="other"); json.dump(spec2, open(sp, "w"))
        r = run(sc + [sp, "--skills-root", sk]); check("scaffold: flag collision refused", r.returncode == 1 and "collision" in r.stderr, r.stderr)
        bad = dict(spec, id="bad2", flags=["--bad2"], ladder=["x"]); json.dump(bad, open(sp, "w"))
        check("scaffold: invalid spec refused", run(sc + [sp, "--skills-root", sk]).returncode == 1)
        nested = dict(spec, id="stoch", parent="quant", flags=["--stoch"], kind="knowledge"); json.dump(nested, open(sp, "w"))
        r = run(sc + [sp, "--skills-root", sk]); check("scaffold: nested child created", r.returncode == 0, r.stderr)
        check("scaffold: nested lint passes", run(lint).returncode == 0, run(lint).stdout)
        r = json.loads(run([PY, os.path.join(sk, "prep/scripts/route.py"), "--quant.prob"]).stdout)
        check("scaffold: existing nested still routes", r["memory_key"] == "quant/prob")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    check("repo: lint clean", run([PY, os.path.join(SK, "prep/scripts/lint.py")]).returncode == 0, run([PY, os.path.join(SK, "prep/scripts/lint.py")]).stdout)


# ----------------------------------------------------------------------------- drill
def t_drill():
    d = os.path.join(SK, "prep-quant/mental-math/scripts/drill.py"); tmp = tempfile.mkdtemp()
    try:
        for L in range(1, 6):
            g = json.loads(run([PY, d, "gen", "--level", str(L), "--n", "12", "--seed", "3"]).stdout)
            g2 = json.loads(run([PY, d, "gen", "--level", str(L), "--n", "12", "--seed", "3"]).stdout)
            check(f"drill L{L}: deterministic by seed", g == g2)
            check(f"drill L{L}: 12 questions", len(g["questions"]) == 12)
        p = os.path.join(tmp, "d.json"); open(p, "w").write(run([PY, d, "gen", "--level", "2", "--n", "8", "--seed", "5"]).stdout)
        qs = json.load(open(p))["questions"]
        r = json.loads(run([PY, d, "grade", p, "\n".join(q["a"] for q in qs), "--time", "40"]).stdout)
        check("drill: perfect answers pass", r["outcome"] == "pass" and r["accuracy"] == 1.0, str(r["outcome"]))
        r = json.loads(run([PY, d, "grade", p, "\n".join(q["a"] for q in qs), "--time", "400"]).stdout)
        check("drill: slow -> partial + F-MM-SLOW", r["outcome"] == "partial" and "F-MM-SLOW" in r["flaws"])
        wrong = [q["a"] for q in qs]; wrong[0] = "123456789"
        r = json.loads(run([PY, d, "grade", p, ",".join(wrong), "--time", "40"]).stdout)
        check("drill: one wrong detected", r["accuracy"] == 0.875 and r["results"][0]["ok"] is False and r["flaws"])
        r = json.loads(run([PY, d, "grade", p, "", "--time", "40"]).stdout)
        check("drill: blank answers fail", r["outcome"] == "fail")
        est = json.loads(run([PY, d, "gen", "--level", "4", "--n", "6", "--seed", "9", "--cats", "est,comp,pow"]).stdout)
        open(p, "w").write(json.dumps(est))
        near = []
        for q in est["questions"]:
            from fractions import Fraction
            near.append(str(float(Fraction(q["a"]) * Fraction(1005, 1000))))
        r = json.loads(run([PY, d, "grade", p, ",".join(near)]).stdout)
        check("drill: estimation tolerance accepts 0.5% error", r["accuracy"] == 1.0, str(r["accuracy"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)



# ----------------------------------------------------------------------------- helpers (db / cn / arch / cpp)
def t_helpers(quick=False):
    tmp = tempfile.mkdtemp()
    try:
        w = lambda n, t: (open(os.path.join(tmp, n), "w").write(t), os.path.join(tmp, n))[1]
        sk = lambda *p: os.path.join(SK, *p)
        schema = w("s.sql", "CREATE TABLE e(id INTEGER PRIMARY KEY,d TEXT,s INT); INSERT INTO e VALUES(1,'x',100),(2,'x',200),(3,'y',150),(4,'y',150);")
        ref = w("ref.sql", "SELECT d, MAX(s) FROM e GROUP BY d"); ok = w("ok.sql", "SELECT d, MAX(s) AS m FROM e GROUP BY 1")
        bad = w("bad.sql", "SELECT d, s FROM e"); syn = w("syn.sql", "SELEC")
        sq = [PY, sk("prep-db/scripts/sqlcheck.py")]
        check("sql: equivalent query AC", json.loads(run(sq + ["compare", schema, ref, ok]).stdout)["verdict"] == "AC")
        r = run(sq + ["compare", schema, ref, bad]); check("sql: wrong query WA, nonzero exit", json.loads(r.stdout)["verdict"] == "WA" and r.returncode == 1)
        check("sql: syntax error ERR", json.loads(run(sq + ["compare", schema, ref, syn]).stdout)["verdict"] == "ERR")
        ordq = w("o1.sql", "SELECT id FROM e ORDER BY id"); ordr = w("o2.sql", "SELECT id FROM e ORDER BY id DESC")
        check("sql: --ordered distinguishes order", json.loads(run(sq + ["compare", schema, ordq, ordr, "--ordered"]).stdout)["verdict"] == "WA"
              and json.loads(run(sq + ["compare", schema, ordq, ordr]).stdout)["verdict"] == "AC")
        nc = [PY, sk("prep-cn/scripts/netcalc.py")]
        s = json.loads(run(nc + ["subnet", "192.168.10.77/26"]).stdout)
        check("cn: subnet math", s["network"] == "192.168.10.64" and s["broadcast"] == "192.168.10.127" and s["usable_hosts"] == 62, str(s))
        v = json.loads(run(nc + ["vlsm", "10.0.0.0/24", "10", "50", "20"]).stdout)
        check("cn: vlsm largest first", [x["subnet"] for x in v] == ["10.0.0.0/26", "10.0.0.64/27", "10.0.0.96/28"], str(v))
        check("cn: contains", json.loads(run(nc + ["contains", "10.0.0.0/8", "10.200.1.1"]).stdout) is True)
        d = json.loads(run(nc + ["delay", "--size-bytes", "1500", "--bw-bps", "1e7", "--dist-m", "2e6"]).stdout)
        check("cn: delay", abs(d["transmission_s"] - 0.0012) < 1e-12 and abs(d["propagation_s"] - 0.01) < 1e-12)
        check("cn: bdp", json.loads(run(nc + ["window", "--bw-bps", "1e9", "--rtt-s", "0.1"]).stdout)["bdp_bytes"] == 12500000.0)
        ac = [PY, sk("prep-arch/scripts/archcalc.py")]
        c = json.loads(run(ac + ["cache-addr", "--addr", "0x12345678", "--size-bytes", "32768", "--block-bytes", "64", "--ways", "4"]).stdout)
        check("arch: cache split", (c["sets"], c["offset_bits"], c["index_bits"], c["tag_bits"]) == (128, 6, 7, 19) and c["offset"] == 56, str(c))
        check("arch: amat 2-level", json.loads(run(ac + ["amat", "--hit-s", "1", "--miss-rate", "0.05", "--penalty-s", "20", "--l2-miss-rate", "0.2", "--l2-penalty-s", "100"]).stdout)["amat_s"] == 3.0)
        check("arch: amdahl", abs(json.loads(run(ac + ["amdahl", "--p", "0.8", "--s", "4"]).stdout)["speedup"] - 2.5) < 1e-9)
        check("arch: cpi mix", abs(json.loads(run(ac + ["cpi", "--mix", "0.5:1,0.3:2,0.2:4"]).stdout)["cpi"] - 1.9) < 1e-9)
        if quick:
            return
        cc = [PY, sk("prep-cpp/scripts/cppcheck.py")]
        ok_ = w("ok.cpp", '#include <iostream>\n#include <utility>\nstruct A{A(){std::cout<<"c ";}A(A&&){std::cout<<"m ";}A(const A&){std::cout<<"cp ";}};\nint main(){A a;A b=std::move(a);A c=b;std::cout<<"\\n";}\n')
        r = json.loads(run(cc + ["run", ok_]).stdout); check("cpp: clean item OK + exact output", r["verdict"] == "OK" and r["stdout"] == "c m cp \n", str(r))
        ub = w("ub.cpp", "#include <vector>\n#include <iostream>\nint main(){std::vector<int> v{1,2,3};int&r=v[0];v.push_back(4);std::cout<<r<<'\\n';}\n")
        r = json.loads(run(cc + ["run", ub]).stdout); check("cpp: dangling reference flagged UB", r["verdict"] == "UB" and r["ub"], str(r.get("ub")))
        ce = w("ce.cpp", 'int main(){ int x = "s"; }\n')
        r = run(cc + ["fails", ce]); check("cpp: compile failure detected", r.returncode == 0 and json.loads(r.stdout)["compile_error"])
        un = w("un.cpp", '#include <iostream>\nint f(){std::cout<<"f";return 1;} int g(){std::cout<<"g";return 2;}\nint h(int a,int b){return a+b;}\nint main(){std::cout<<h(f(),g())<<"\\n";}\n')
        r = json.loads(run(cc + ["run", un]).stdout); check("cpp: runs deterministic item without false UB", r["verdict"] in ("OK", "UNSPECIFIED"), str(r["verdict"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

# ----------------------------------------------------------------------------- harness + mutation
def t_harness():
    r = run([PY, os.path.join(SK, "prep-dsa/harness/judge.py"), "selftest"])
    check("harness: selftest", r.returncode == 0, r.stdout[-400:])


MUTATIONS = [  # (name, file, old, new, expected stage(s))
    ("int instead of long long", "ref.cpp", "long long best=LLONG_MIN, cur=0", "int best=INT_MIN, cur=0", {"ref-crash", "mismatch"}),
    ("allows empty subarray", "ref.cpp", "cur=max(x,cur+x)", "cur=max(0LL,cur+x)", {"mismatch"}),
    ("best starts at 0", "ref.cpp", "best=LLONG_MIN, cur=0", "best=0, cur=0", {"mismatch"}),
    ("never resets running sum", "ref.cpp", "cur=max(x,cur+x)", "cur=cur+x", {"mismatch"}),
    ("skips last element", "ref.cpp", "for(int i=0;i<n;i++)", "for(int i=0;i<n-1;i++)", {"mismatch", "ref-crash"}),
    ("answer off by one", "ref.cpp", 'printf("%lld\\n",best)', 'printf("%lld\\n",best+1)', {"mismatch"}),
    ("ref reads past array (n=1 crash)", "ref.cpp", "long long best=LLONG_MIN, cur=0;", "long long best=LLONG_MIN, cur=0; vector<long long> v(n); v[n]=1;", {"ref-crash"}),
    ("ref is O(n^2) (too slow)", "ref.cpp", None, None, {"ref-too-slow"}),
    ("brute is as fast as ref", "brute.cpp", None, None, {"brute-passes-limit"}),
    ("no edge cases", None, None, None, {"no-edge-cases"}),
    ("brute has a bug", "brute.cpp", "long long s=0;", "long long s=1;", {"mismatch"}),
    ("generator breaks", "gen.cpp", 'printf("%d\\n",n);', 'printf("%d\\n",n); return 1;', {"gen", "mismatch", "ref-crash"}),
]


def t_mutation():
    ex = os.path.join(SK, "prep-dsa/harness/example"); judge = os.path.join(SK, "prep-dsa/harness/judge.py")
    for name, f, old, new, stages in MUTATIONS:
        tmp = tempfile.mkdtemp()
        try:
            d = os.path.join(tmp, "p"); shutil.copytree(ex, d, ignore=shutil.ignore_patterns(".build", "sols"))
            if name.startswith("ref is O(n^2)"):
                shutil.copy(os.path.join(ex, "brute.cpp"), os.path.join(d, "ref.cpp"))
            elif name.startswith("brute is as fast"):
                shutil.copy(os.path.join(ex, "ref.cpp"), os.path.join(d, "brute.cpp"))
            elif name == "no edge cases":
                shutil.rmtree(os.path.join(d, "edge"))
            else:
                src = open(os.path.join(d, f)).read(); assert old in src, (name, old)
                open(os.path.join(d, f), "w").write(src.replace(old, new, 1))
            r = run([PY, judge, "verify", d]); out = json.loads(r.stdout) if r.stdout.strip() else {}
            check(f"mutation rejected: {name}", r.returncode != 0 and not out.get("ok") and out.get("stage") in stages,
                  f"stage={out.get('stage')} detail={str(out.get('detail'))[:120]}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    r = run([PY, judge, "verify", ex]); check("mutation control: the unmutated example is accepted", r.returncode == 0, r.stdout[-300:])


SUITES = {"routing": t_routing, "memory": t_memory, "scaffold": t_scaffold, "drill": t_drill, "helpers": lambda: t_helpers("--quick" in sys.argv), "harness": t_harness, "mutation": t_mutation}

if __name__ == "__main__":
    a = sys.argv[1:]
    only = a[a.index("--only") + 1] if "--only" in a else None
    names = [only] if only else [n for n in SUITES if not (("--quick" in a) and n in ("harness", "mutation"))]
    for n in names:
        before = len(results); print(f"[{n}]", end=" ", flush=True); SUITES[n]()
        ok = sum(1 for r in results[before:] if r[1]); print(f"{ok}/{len(results) - before}")
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    sys.exit(1 if failed else 0)
