---
name: prep-quant-prob
description: Quant Probability & Expectation practice for /prep: probability, expected value, conditional probability, bayes, random variable, variance. Invoked by the prep orchestrator via --prob, --quant.prob.
---

# Quant Probability & Expectation (`quant/prob`)

Invoked by `/prep` after routing. Follow `../../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../../prep/references/difficulty.md`.
`MEM` = `python3 ../../prep/scripts/memory.py` · memory key = `quant/prob` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init quant/prob --default-level 3`, `MEM profile quant/prob`, mode = `problem`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Quant-interview probability: counting, conditioning/Bayes, linearity of expectation, symmetry, first-step recursion, Markov chains, random walks, martingales, order statistics, geometric probability, simple games and optimal stopping.
**Out:** Advanced stochastic calculus (add a child domain), mental arithmetic (quant/mental-math), pure statistics/ML.

Topics (taxonomy tags, see `references/taxonomy.md`): counting-combinatorics, conditional-bayes, linearity-of-expectation, indicator-variables, symmetry, first-step-recursion, markov-chains, random-walks, martingales-stopping, order-statistics, geometric-probability, distributions-moments, dice-coins-cards, games-optimal-stopping, bounds-inequalities

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `problem` | difficulty, optional topic → one verified problem; user answers with reasoning; exact answer + method graded |
| `quiz` | difficulty, topic, n → n short numeric/fraction questions, all answers computed exactly |
| `explain` | technique → technique, when it applies, 2 worked examples, the classic trap |
| `review` | none or topic → spaced re-test of missed problems with changed parameters |
| `mock` | n problems, time box → rapid-fire interviewer: problem, probe 'why?', variation, next |

Default mode: `problem` · default difficulty: `3`. `--timed`: enforce the expected time per item and log `time_s`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Direct computation: P(two heads in 3 flips), E[die roll], P(sum of two dice = 7). |
| 2 | One technique: Bayes with two urns, linearity (expected fixed points), simple conditional probabilities. |
| 3 | Standard quant screen: expected flips to get HH, gambler's ruin, coupon collector, Monty-Hall variants, symmetry arguments. |
| 4 | Strong: martingale/optional stopping (ABRACADABRA), random-walk hitting times, optimal stopping games, order statistics of uniforms. |
| 5 | Elite: multi-step puzzle needing a non-obvious state space or exact-vs-asymptotic reasoning (100 prisoners, Poisson thinning/merging, continuous-time Markov). |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `prob-<topic>-<short-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Prob specifics
Present the problem, ask for answer + one-line method. Hints: nudge = name a technique family; pattern = state variable/event to define; skeleton = set up the equations; solution = full. For `quiz` batch items, no derivation required but record `method`.

## 5. Accuracy gates (hard — run before presenting anything)
**Kind: code-checkable.** Nothing is shown until it is machine-verified.
1. Author: statement, reference solution, an *independent* brute force (different algorithm), input generator, constraints.
2. Execute in the scratchpad (never the repo): reference must equal brute force on ≥200 random small cases plus hand-written edge cases (empty/min/max, duplicates, negatives, overflow range).
3. Difficulty anchor: the intended solution meets the limit at max constraints and the brute force does **not**; otherwise raise constraints or regenerate.
4. Grade user answers by **executing** them on the same harness — never by reading and judging.
5. Reject ambiguity: input format, constraints, tie-breaks and output format are all stated.
6. Compute the answer exactly with Python `fractions.Fraction` (enumeration, DP, or linear system) AND independently by Monte Carlo (≥1e6 trials, within 4 standard errors) before presenting; present only if they agree. Never trust a remembered 'known answer'.
7. Check the statement is unambiguous (independence, replacement, fairness, stopping rule, what 'expected' is over). Ambiguous → rewrite.
8. State the answer as an exact fraction/closed form plus decimal.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path quant/prob)` — outside the repo, never committed.
- **Read at start:** `MEM profile quant/prob` (already loaded by orchestrator). In `review` mode also `MEM due quant/prob` and `MEM tail quant/prob 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild quant/prob`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
