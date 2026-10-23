---
name: prep-quant-mental-math
description: Quant Mental Math practice for /prep: mental math, mental arithmetic, arithmetic speed, zetamac, quick calculation, estimate quickly. Invoked by the prep orchestrator via --mental-math, --mm, --quant.mm.
---

# Quant Mental Math (`quant/mental-math`)

Invoked by `/prep` after routing. Follow `../../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../../prep/references/difficulty.md`.
`MEM` = `python3 ../../prep/scripts/memory.py` · memory key = `quant/mental-math` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init quant/mental-math --default-level 2`, `MEM profile quant/mental-math`, mode = `drill`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Speed arithmetic for quant interviews: add/subtract, multiplication, squares, percentages, fractions-decimals, division, estimation, compound growth, logs/roots approximation.
**Out:** Probability reasoning (quant/prob), written-calculation tutoring.

Topics (taxonomy tags, see `references/taxonomy.md`): add-sub, mul-2digit, mul-3x2, squares, percent, fractions-decimals, division, powers-roots, compound-growth, estimation-logs, ratios-odds

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `drill` | difficulty, n, categories → batch of generated questions (answers hidden), graded by script, per-category accuracy and time |
| `quiz` | technique → short set that forces one trick (e.g. squares near 50, x*11, percent flips) |
| `explain` | operation → fastest mental method, 3 examples, common slip |
| `review` | none → targeted drill on categories with worst error rate |

Default mode: `drill` · default difficulty: `2`. `--timed`: enforce the expected time per item and log `time_s`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | 2-digit add/subtract, x2/x5/x10/x11, simple percents (10%, 50%). |
| 2 | 2x2 digit multiplication, squares to 30, division with clean results, 15%/25% tips. |
| 3 | 3x2 multiplication, decimals, percent chains, fractions to decimals (1/7, 1/9, 1/12). |
| 4 | Estimation within 1-2%: compound interest, sqrt/cube estimates, ratios, products of 3 numbers. |
| 5 | Zetamac-hard pace with mixed operations, logs/exponent estimation, 4-digit by 2-digit within a tolerance. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `mm-<cat>-L<level>-s<seed>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Drill specifics
1. `python3 scripts/drill.py gen --level L --n N --seed S [--cats a,b] > $P/drill.json` (seed = unix time unless replaying a stored item).
2. Show only the `q` fields, numbered. User replies with answers (comma/newline separated) and total time (e.g. `... | 95s`).
3. `python3 scripts/drill.py grade $P/drill.json "<answers>" --time <seconds>` → JSON with per-question result, per-category accuracy, avg time, flaws.
4. Debrief: misses with correct answer + the fastest method for each; one `episode` per drill (not per question), `item.tags` = categories drilled.

## 5. Accuracy gates (hard — run before presenting anything)
**Kind: code-checkable.** Nothing is shown until it is machine-verified.
1. Author: statement, reference solution, an *independent* brute force (different algorithm), input generator, constraints.
2. Execute in the scratchpad (never the repo): reference must equal brute force on ≥200 random small cases plus hand-written edge cases (empty/min/max, duplicates, negatives, overflow range).
3. Difficulty anchor: the intended solution meets the limit at max constraints and the brute force does **not**; otherwise raise constraints or regenerate.
4. Grade user answers by **executing** them on the same harness — never by reading and judging.
5. Reject ambiguity: input format, constraints, tie-breaks and output format are all stated.
6. All questions and answers come from `python3 scripts/drill.py gen` (exact arithmetic with Python integers/Fractions) — never compute answers yourself.
7. Grade with `python3 scripts/drill.py grade <file> <answers>`; do not eyeball.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path quant/mental-math)` — outside the repo, never committed.
- **Read at start:** `MEM profile quant/mental-math` (already loaded by orchestrator). In `review` mode also `MEM due quant/mental-math` and `MEM tail quant/mental-math 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild quant/mental-math`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
