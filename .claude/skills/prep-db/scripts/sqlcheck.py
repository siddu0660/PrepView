#!/usr/bin/env python3
"""SQL verifier on in-memory SQLite (stdlib). Used by prep-db `sql` mode.

  sqlcheck.py run     <schema.sql> <query.sql>                 print result rows as JSON
  sqlcheck.py compare <schema.sql> <ref.sql> <user.sql> [--ordered]
        -> {"verdict":"AC|WA|ERR","detail":...,"expected":[...],"got":[...],"flaws":[...]}
  sqlcheck.py plan    <schema.sql> <query.sql>                 EXPLAIN QUERY PLAN rows (index use / scans)

Result sets compare as multisets unless --ordered (use it when the task demands ORDER BY).
Floats compare to 6 dp. Exit 0 iff AC / success.
"""
import json, sqlite3, sys
from collections import Counter


def conn(schema):
    c = sqlite3.connect(":memory:")
    c.executescript(open(schema).read())
    return c


def norm(v):
    return round(v, 6) if isinstance(v, float) else v


def rows(c, sql):
    cur = c.execute(sql)
    return [tuple(norm(v) for v in r) for r in cur.fetchall()]


def main(a):
    if len(a) < 3:
        print(__doc__); return 2
    cmd = a[0]
    c = conn(a[1])
    if cmd == "run":
        print(json.dumps(rows(c, open(a[2]).read()))); return 0
    if cmd == "plan":
        print(json.dumps([r[3] for r in c.execute("EXPLAIN QUERY PLAN " + open(a[2]).read())])); return 0
    if cmd == "compare" and len(a) >= 4:
        ordered = "--ordered" in a
        exp = rows(c, open(a[2]).read())
        try:
            got = rows(c, open(a[3]).read())
        except sqlite3.Error as e:
            print(json.dumps({"verdict": "ERR", "detail": str(e), "flaws": ["F-SQL-SYNTAX"]})); return 1
        ok = got == exp if ordered else Counter(got) == Counter(exp)
        flaws = []
        if not ok:
            if Counter(r[0] if r else None for r in got) == Counter(r[0] if r else None for r in exp) and got != exp:
                flaws.append("F-SQL-WRONG-COLUMNS")
            elif len(got) > len(exp):
                flaws.append("F-SQL-DUPLICATES-OR-JOIN-FANOUT")
            elif len(got) < len(exp):
                flaws.append("F-SQL-MISSING-ROWS")
            else:
                flaws.append("F-SQL-WRONG-LOGIC")
            if set(got) == set(exp) and Counter(got) != Counter(exp):
                flaws = ["F-SQL-DUPLICATES-OR-JOIN-FANOUT"]
            if ordered is False and sorted(map(str, got)) == sorted(map(str, exp)):
                flaws = []
        print(json.dumps({"verdict": "AC" if ok else "WA", "flaws": flaws,
                          "expected": exp[:10], "got": got[:10], "rows_expected": len(exp), "rows_got": len(got)}))
        return 0 if ok else 1
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
