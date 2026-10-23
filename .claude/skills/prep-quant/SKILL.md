---
name: prep-quant
description: Quant-interview prep router for /prep (--quant). Dispatches to child domains - probability and expectation (--prob / --quant.prob) and mental math (--mm / --quant.mm). Use for quant, market-making, Jane Street / Citadel / HRT / Optiver style interview practice.
argument-hint: "[--prob|--mm] [-d 1-5] [-n N] [--mode ...] [--timed]"
---

# Quant (router)

This node holds no tasks of its own. The orchestrator's `scripts/route.py` already resolved a child via `registry.json` in this folder; if it returned `ask`, ask which child (list the ones below) and re-route with the answer.

| Child | Flags | Skill file | Memory key |
|-------|-------|-----------|-----------|
| Probability & expectation | `--prob`, `--quant.prob` | `prob/SKILL.md` | `quant/prob` |
| Mental math | `--mm`, `--mental-math`, `--quant.mm` | `mental-math/SKILL.md` | `quant/mental-math` |

Children are not auto-discovered by Claude Code (only top-level skill folders are): the orchestrator `Read`s the child's SKILL.md by the `path` in the registry and follows it. Each child has its own memory, profile and level.

Quant interviews are scored on **speed and exactness**: default every child session to `--timed` unless the user says otherwise.

Add a child (e.g. stochastic calculus, brainteasers, options pricing) with `/prep-new <id> --parent quant`.
