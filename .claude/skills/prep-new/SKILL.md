---
name: prep-new
description: Scaffold a new PrepView domain skill (a new topic for /prep such as db, networking, ml-system-design, stochastic-calculus) from the shared template, including its memory schema, taxonomy, rubric and registry entry. Use for "/prep-new <topic>", "add a skill for X to prep", or "create a new prep domain".
argument-hint: "<domain-id> [--parent quant] [--kind code|knowledge|design]"
---

# /prep-new — domain scaffolder

Turns a topic into a complete domain skill in under a minute. Everything is generated from `template/`; do not hand-write SKILL.md structure.

## Steps

1. **Interview (≤4 questions, skip any the user already answered).**
   1. Flag + aliases and nesting: `--db`, parent (e.g. `quant`) or top-level?
   2. Kind → decides the accuracy gate: **code** (answers machine-checkable) · **knowledge** (quiz/explain, keyed facts) · **design** (rubric-graded open answers).
   3. Task types wanted (problem / quiz / explain / review / mock / drill / design / anything else) and the default.
   4. Difficulty anchors: one concrete example for each level 1–5 (propose them yourself and ask only for corrections).
2. **Draft the spec** → write `specs/<id>.json` (schema below). Propose, don't interrogate: fill topics, flaw codes, `x_fields` and rubric yourself from domain expertise, then show a 10-line summary for approval.
3. **Scaffold:** `python3 scripts/scaffold.py specs/<id>.json` (add `--force` only to regenerate). It validates the spec, refuses flag collisions, writes the skill folder (SKILL.md, references/taxonomy|rubric|schema) and registers it.
4. **Lint:** `python3 ../prep/scripts/lint.py` must print `0 errors`.
5. **Smoke test:** `python3 ../prep/scripts/route.py "--<flag> -d 2"` must return `status: ok` with the new memory key; one trigger phrase without a flag should also route (or intentionally ask).
6. **Enrich if needed:** domain-specific harness/scripts go in the new skill folder (see `prep-dsa/harness` as the model) — never in `template/`.

The domain's memory draft **is** `references/schema.md` (generated from `x_fields`). Actual memory files appear in `${PREP_MEMORY_DIR:-~/.claude/prep-memory}/<key>/` on first use; nothing is created in the repo.

## Spec schema (`specs/<id>.json`)

| Key | Type | Notes |
|-----|------|-------|
| `id`, `title` | str | kebab-case id |
| `parent` | str? | id of a `kind: router` domain (e.g. `quant`) |
| `kind` | `code\|knowledge\|design` | selects `template/gates/<kind>.md` |
| `flags` | [str] | each starts `--`; must be globally unique |
| `triggers` | [str] ≥5 | specific phrases used by free-text routing |
| `scope_in`, `scope_out` | str | one sentence each |
| `modes` | [{id,input,output}] | `default_mode` must be one of them |
| `default_mode`, `default_difficulty` | str, 1–5 | |
| `ladder` | [5 str] | concrete anchors for levels 1..5 |
| `topics` | [str] | taxonomy tags (what weak_tags will be made of) |
| `flaws` | {code: meaning} | codes `F-<AREA>-<WHAT>` |
| `x_fields` | {name: meaning} | **domain memory extension** (episode `x` block) |
| `item_ref_format` | str | stable slug pattern for dedupe |
| `rubric_body`, `outcome_rule` | str | markdown |
| optional | | `description`, `timed`, `gate_extra` [str], `loop_extra`, `output_format`, `items_note` |

## Rules
- Triggers must be domain-distinctive; if lint warns of a shared trigger, remove it from the less specific domain.
- A new domain must define at least 4 flaw codes and an `x_fields` block that captures *how the user went wrong*, not just whether.
- Never edit `prep/registry.json` by hand for new domains; the scaffolder keeps it consistent.
