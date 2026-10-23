# PrepView

A Claude Code skill set for SWE and quant interview prep. One entry point, `/prep`, routes to domain skills, runs the task at a chosen difficulty, and keeps per-domain memory of what you were asked, where you went wrong and how you work.

Design: [`docs/ADR-001-prepview-skill-architecture.md`](docs/ADR-001-prepview-skill-architecture.md)

## Use

```
/prep --dsa -d 3                 # a verified C++ problem, level 3
/prep quiz me on deadlocks       # inferred: os / quiz
/prep --hld --mode mock          # system-design mock round
/prep --lld                      # OOD problem with an extensibility probe
/prep --quant.prob -n 5 --timed  # probability set, timed
/prep --mm -d 3 -n 20            # mental-math drill
/prep --behavioral --mode story  # build a STAR story bank entry
/prep --db --mode sql            # SQL task, your query is executed on SQLite and compared
/prep --cn -d 3                  # networks quiz (subnetting/TCP numbers computed by script)
/prep --arch                     # computer-architecture quiz (AMAT, caches, pipelines, MESI)
/prep --cpp --mode predict       # "what does this print / is this UB", ground truth from g++
/prep --cpp --mode debug         # find and fix a planted bug; fix is checked under sanitizers
/prep --dsa --mode review        # spaced-repetition of items you missed
/prep                            # dashboard: level, weakest tag, items due
/prep-new db --kind knowledge    # add a new domain from the template
```

Flags: `--dsa|--algo` `--os` `--db|--dbms` `--cn|--networks|--net` `--arch` `--cpp` `--lld|--oop` `--hld|--sd` `--behavioral|--hr|--bq` `--quant` → `--prob|--quant.prob`, `--mm|--mental-math|--quant.mm`.
(`--arch` = computer architecture: ISA, pipelines, caches, coherence, performance equations.)
Options: `-d 1..5` (or words easy/medium/hard/expert), `-n N`, `--mode problem|quiz|explain|review|mock|design|drill|story|sql|predict|debug`, `--timed`.
No flag → free-text routing; when unsure it asks one question, never guesses.

## Layout

```
.claude/skills/
  prep/            orchestrator: SKILL.md, registry.json, scripts/{route,memory,lint}.py, references/
  prep-new/        scaffolder: template/, specs/*.json (one per domain), scripts/scaffold.py
  prep-dsa/        C++ harness (verify + judge under ASan/UBSan) + example problem
  prep-os/ prep-lld/ prep-hld/ prep-behavioral/
  prep-db/ (scripts/sqlcheck.py)  prep-cn/ (scripts/netcalc.py)  prep-arch/ (scripts/archcalc.py)  prep-cpp/ (scripts/cppcheck.py)
  prep-quant/      router → prob/, mental-math/ (own registry.json, scripts/drill.py)
evals/run_evals.py routing, memory, scaffold, drill, harness and seeded-bad-problem tests
```

Domain skills are generated from `prep-new/specs/<id>.json` — edit the spec and re-run `python3 .claude/skills/prep-new/scripts/scaffold.py <spec> --force`, don't hand-edit generated SKILL.md files.

## Memory (never in this repo)

Stored per domain in `$PREP_MEMORY_DIR` (default `~/.claude/prep-memory`):
`log.jsonl` (append-only episodes), `profile.md` (derived: level, weak tags, flaw watch list), `notes.md` (short takeaways), `items/` (stored problems for review).
The repo only holds each domain's schema (`references/schema.md`). `~/.claude` persists on local installs; cloud sessions are ephemeral, so run locally (or point `PREP_MEMORY_DIR` at a persistent path) if you want your history to survive.

## Requirements

`python3` (stdlib only), `g++` 13+ with C++20 and sanitizers (for `--dsa` and `--cpp`).

## Verify

```
python3 evals/run_evals.py --quick   # ~15 s: routing, memory, scaffold, drill, helpers
python3 evals/run_evals.py           # + cppcheck, C++ harness selftest and 12 seeded-bad-problem mutations (~100 s)
python3 .claude/skills/prep/scripts/lint.py
```
