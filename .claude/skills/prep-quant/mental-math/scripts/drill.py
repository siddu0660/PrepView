#!/usr/bin/env python3
"""Mental-math drill generator + grader. Exact arithmetic (ints/Fractions); stdlib only.

  drill.py gen   --level 1..5 --n N [--seed S] [--cats add,mul,sq,pct,div,frac,est,comp,pow]
  drill.py grade <drill.json> "<a1>,<a2>,..." [--time TOTAL_SECONDS]

gen prints JSON {"level","seed","target_s","questions":[{"id","cat","tag","q","a","tol"}]}.
Answers are comma/newline separated plain numbers (no thousands separators). Show the user ONLY the "q" fields. grade prints per-question results, per-category
accuracy, avg time, the episode-ready flaw codes and outcome.
"""
import json, math, random, re, sys
from fractions import Fraction

TARGET_S = {1: 6, 2: 10, 3: 15, 4: 20, 5: 25}
TAG = {"add": "add-sub", "mul": "mul-2digit", "sq": "squares", "pct": "percent", "div": "division",
       "frac": "fractions-decimals", "est": "estimation-logs", "comp": "compound-growth", "pow": "powers-roots"}
LEVEL_CATS = {1: ["add", "mul", "sq", "pct"], 2: ["add", "mul", "sq", "pct", "div"],
              3: ["add", "mul", "sq", "pct", "div", "frac"], 4: ["mul", "sq", "pct", "frac", "est", "comp", "pow"],
              5: ["mul", "sq", "pct", "frac", "est", "comp", "pow", "add"]}


def q_add(r, L):
    d = {1: 2, 2: 3, 3: 4, 4: 4, 5: 5}[L]
    a, b = r.randint(10 ** (d - 1), 10 ** d - 1), r.randint(10 ** (d - 1), 10 ** d - 1)
    if r.random() < .5:
        return f"{a} + {b}", Fraction(a + b), 0, "add"
    return f"{a} - {b}", Fraction(a - b), 0, "add"


def q_mul(r, L):
    if L == 1:
        a, b = r.randint(12, 99), r.choice([2, 5, 10, 11, 4])
    elif L == 2:
        a, b = r.randint(12, 99), r.randint(12, 99)
    elif L == 3:
        a, b = r.randint(101, 999), r.randint(12, 99)
    elif L == 4:
        a, b = r.randint(101, 999), r.randint(101, 999)
    else:
        a, b = r.randint(1001, 9999), r.randint(12, 99)
    return f"{a} × {b}", Fraction(a * b), 0, "mul"


def q_sq(r, L):
    hi = {1: 15, 2: 30, 3: 100, 4: 200, 5: 400}[L]
    a = r.randint(11, hi)
    return f"{a}²", Fraction(a * a), 0, "sq"


def q_pct(r, L):
    p = r.choice([10, 50, 25, 5, 20] if L == 1 else [15, 12, 35, 7, 18, 45, 65, 8, 2.5] if L < 4 else [17, 13, 37, 8.5, 6.25, 112, 87])
    base = r.choice([40, 80, 120, 240, 360, 500, 600, 840, 1200]) if L < 4 else r.randint(100, 9999)
    ans = Fraction(str(p)) * base / 100
    return f"{p}% of {base}", ans, 0 if L < 4 else Fraction(1, 100), "pct"


def q_div(r, L):
    b = r.randint(3, 9 if L < 3 else 19)
    a = b * r.randint(12, 99 if L < 3 else 999)
    return f"{a} ÷ {b}", Fraction(a, b), 0, "div"


def q_frac(r, L):
    n = r.choice([1, 2, 3, 5]) if L < 5 else r.randint(1, 12)
    d = r.choice([7, 9, 11, 12, 13] if L < 5 else [13, 14, 17, 19, 23])
    return f"{n}/{d} as a decimal (3 dp)", Fraction(n, d), Fraction(1, 1000) / (Fraction(n, d)), "frac"


def q_est(r, L):
    a, b, c = r.randint(11, 99), r.randint(11, 99), r.randint(11, 99)
    return f"{a} × {b} × {c} (within 1%)", Fraction(a * b * c), Fraction(1, 100), "est"


def q_comp(r, L):
    rate, yrs = r.choice([3, 5, 6, 7, 8, 10, 12]), r.choice([5, 8, 10, 12, 15, 20])
    return f"1.{rate:02d}^{yrs} (within 1%)", Fraction(round((1 + rate / 100) ** yrs * 10 ** 9), 10 ** 9), Fraction(1, 100), "comp"


def q_pow(r, L):
    n = r.randint(200, 9999)
    return f"√{n} (within 1%)", Fraction(round(math.sqrt(n) * 10 ** 9), 10 ** 9), Fraction(1, 100), "pow"


GEN = {"add": q_add, "mul": q_mul, "sq": q_sq, "pct": q_pct, "div": q_div, "frac": q_frac, "est": q_est, "comp": q_comp, "pow": q_pow}


def gen(level, n, seed, cats):
    r = random.Random(seed)
    cats = cats or LEVEL_CATS[level]
    qs = []
    for i in range(n):
        cat = cats[i % len(cats)] if len(cats) > 1 else cats[0]
        q, a, tol, c = GEN[cat](r, level)
        qs.append({"id": i + 1, "cat": cat, "tag": TAG[cat], "q": q, "a": str(a), "tol": str(tol)})
    r.shuffle(qs)
    for i, x in enumerate(qs):
        x["id"] = i + 1
    return {"level": level, "seed": seed, "target_s": TARGET_S[level], "questions": qs}


def parse(s):
    s = s.strip().replace("−", "-").replace("_", "")
    try:
        return Fraction(s)
    except (ValueError, ZeroDivisionError):
        m = re.search(r"-?\d+(?:\.\d+)?(?:/\d+)?", s)
        return Fraction(m.group(0)) if m else None


def grade(path, answers, total_time=None):
    d = json.load(open(path))
    given = [x for x in re.split(r"[\n;|,]+", answers) if x.strip()]
    res, by = [], {}
    for q, g in zip(d["questions"], given + [""] * len(d["questions"])):
        a, tol, u = Fraction(q["a"]), Fraction(q["tol"]), parse(g)
        ok = u is not None and (abs(u - a) <= tol * abs(a) if tol else u == a)
        flaw = None
        if not ok:
            if u is None:
                flaw = "F-MM-GUESS"
            elif a != 0 and abs(u - a) > abs(a) / 2:
                flaw = "F-MM-GUESS"
                if u != 0 and abs(math.log10(abs(float(u / a)))) % 1 < 1e-9:
                    flaw = "F-MM-DECIMAL-PLACE"
            elif q["cat"] in ("est", "comp", "pow"):
                flaw = "F-MM-ESTIMATION-DRIFT"
            elif q["cat"] == "frac":
                flaw = "F-MM-FRACTION-CONV"
            elif q["cat"] == "add" and u is not None and (u < 0) != (a < 0):
                flaw = "F-MM-SIGN"
            else:
                flaw = "F-MM-CARRY"
        res.append({"id": q["id"], "q": q["q"], "correct_answer": str(float(a)) if a.denominator != 1 else str(a),
                    "given": g.strip(), "ok": ok, "flaw": flaw})
        c = by.setdefault(q["cat"], [0, 0]); c[1] += 1; c[0] += ok
    n, right = len(res), sum(r["ok"] for r in res)
    acc = right / n if n else 0
    avg = (total_time / n) if total_time else None
    flaws = sorted({r["flaw"] for r in res if r["flaw"]})
    if avg and avg > d["target_s"]:
        flaws.append("F-MM-SLOW")
    outcome = "pass" if acc >= .9 and (avg is None or avg <= d["target_s"]) else "partial" if acc >= .7 else "fail"
    worst = min(by, key=lambda k: by[k][0] / by[k][1]) if by else None
    return {"outcome": outcome, "accuracy": round(acc, 3), "avg_time_s": round(avg, 1) if avg else None,
            "target_time_s": d["target_s"], "flaws": flaws, "worst_category": worst,
            "category_stats": {k: {"n": v[1], "correct": v[0]} for k, v in by.items()},
            "tags": sorted({TAG[k] for k in by}), "results": res}


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["gen"]:
        g = lambda f, dflt: a[a.index(f) + 1] if f in a else dflt
        lvl = int(g("--level", 2)); seed = int(g("--seed", random.randrange(10 ** 6)))
        cats = g("--cats", "").split(",") if g("--cats", "") else None
        print(json.dumps(gen(lvl, int(g("--n", 10)), seed, cats), indent=1))
    elif a[:1] == ["grade"] and len(a) >= 3:
        t = float(a[a.index("--time") + 1]) if "--time" in a else None
        print(json.dumps(grade(a[1], a[2], t), indent=1))
    else:
        print(__doc__); sys.exit(2)
