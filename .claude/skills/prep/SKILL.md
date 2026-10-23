---
name: prep
description: Job-interview prep orchestrator for SWE and quant roles. Use for "/prep", flags like --dsa --lld --hld --os --quant --prob, or any request for a practice problem, quiz, mock round or concept explanation on DSA, system design, OS, probability, mental math or behavioral rounds. Routes to the right domain skill, sets difficulty, and keeps per-domain memory.
argument-hint: "[--dsa|--os|--lld|--hld|--behavioral|--quant.prob|--quant.mm] [-d 1-5] [-n N] [--mode problem|quiz|explain|review|mock|design|drill] [--timed] [free text]"
---

# /prep — orchestrator

You route, you do not teach. Domain skills do the work. Keep this layer fast: one script call to route, one to load memory, then hand off.

Paths below are relative to this skill's directory. `$MEM` = `python3 scripts/memory.py`.

## Flow

1. **Route** — run `python3 scripts/route.py "$ARGUMENTS"` and read the JSON.
   - `status: ok` → say `Routing: <memory_key> · mode <mode> · level <n>` in one line.
   - `status: ask` → ask ONE question listing `candidates` (max 3) plus "other"; never guess. If `reason` names an unknown flag, list the valid flags from `registry.json`.
2. **Load** — `$MEM init <memory_key> --default-level <domain.default_difficulty>` (idempotent; creates memory outside the repo on first use), then `$MEM profile <memory_key>`. Read only that profile and the chosen domain's SKILL.md (`../<domain.path>/SKILL.md`). Nothing else.
3. **Resolve** — difficulty: explicit flag/words > `recommended_level` in profile > `default_difficulty`. Mode: from router, else domain default. If `--mode review` or the user says "revise", also run `$MEM due <memory_key>` and let the domain skill prioritise those items.
4. **Delegate** — follow the domain SKILL.md, passing: `memory_key, mode, difficulty, n, timed, text, profile`. For `kind: router` domains (e.g. quant) the router has already resolved a child; if it returned `ask`, ask which child.
5. **Close** — the domain skill writes memory per `references/session-contract.md`. Finish with a 3-line recap: result · top flaw · next suggestion (e.g. `/prep --dsa -d 3`).

## Rules

- Flags always win over inference. Unknown flag → ask, don't reinterpret.
- Never load more than one domain. Never spawn subagents unless the domain skill says so (`mock` fan-out only).
- Never reveal answers/solutions unless the user asks or the session loop reaches Debrief.
- A failed memory write warns once and never blocks the session.
- Registry, shared scales and loop contract live in `registry.json`, `references/difficulty.md`, `references/session-contract.md`; add domains only via `/prep-new`.

## Quick reference

`/prep --dsa -d 3` · `/prep quiz me on deadlocks` (infers os/quiz) · `/prep --hld --mode mock` · `/prep --quant.prob -n 5 --timed` · `/prep --dsa --mode review` · `/prep` alone (no args) → run `$MEM summary`, print a compact table (domain · level · sessions · weakest tag · due), and suggest the next session: domain with most `due` items, else the one not practised longest, as a ready-to-run command. If no memory exists yet, list the available flags from `registry.json`.
