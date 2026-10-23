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
/prep --dsa --mode review        # spaced-repetition of items you missed
/prep                            # dashboard: level, weakest tag, items due
/prep-new db --kind knowledge    # add a new domain from the template
```

Flags: `--dsa|--algo` `--os` `--lld|--oop` `--hld|--sd` `--behavioral|--hr|--bq` `--quant` → `--prob|--quant.prob`, `--mm|--mental-math|--quant.mm`.
Options: `-d 1..5` (or words easy/medium/hard/expert), `-n N`, `--mode problem|quiz|explain|review|mock|design|drill|story`, `--timed`.
No flag → free-text routing; when unsure it asks one question, never guesses.

## Layout

```
.claude/skills/
  prep/            orchestrator: SKILL.md, registry.json, scripts/{route,memory,lint}.py, references/
  prep-new/        scaffolder: template/, specs/*.json (one per domain), scripts/scaffold.py
  prep-dsa/        C++ harness (verify + judge under ASan/UBSan) + example problem
  prep-os/ prep-lld/ prep-hld/ prep-behavioral/
  prep-quant/      router → prob/, mental-math/ (own registry.json, scripts/drill.py)
evals/run_evals.py routing, memory, scaffold, drill, harness and seeded-bad-problem tests
```

Domain skills are generated from `prep-new/specs/<id>.json` — edit the spec and re-run `python3 .claude/skills/prep-new/scripts/scaffold.py <spec> --force`, don't hand-edit generated SKILL.md files.

## Memory (never in this repo)

Stored per domain in `$PREP_MEMORY_DIR` (default `~/.claude/prep-memory`):
`log.jsonl` (append-only episodes), `profile.md` (derived: level, weak tags, flaw watch list), `notes.md` (short takeaways), `items/` (stored problems for review).
The repo only holds each domain's schema (`references/schema.md`). `~/.claude` persists on local installs; cloud sessions are ephemeral, so run locally (or point `PREP_MEMORY_DIR` at a persistent path) if you want your history to survive.

## Requirements

`python3` (stdlib only), `g++` with C++20 and sanitizers (for `--dsa`).

## Verify

```
python3 evals/run_evals.py --quick   # ~10 s: routing, memory, scaffold, drill
python3 evals/run_evals.py           # + C++ harness selftest and 12 seeded-bad-problem mutations (~75 s)
python3 .claude/skills/prep/scripts/lint.py
```
