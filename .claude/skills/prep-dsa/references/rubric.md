# Rubric — dsa

## Verdict-driven (the harness decides correctness; never judge by reading)

| Dimension | Evidence |
|-----------|----------|
| Correctness | `judge.py judge` verdict AC (also passes ASan/UBSan) |
| Efficiency | passes large cases within `tl_s`; stated complexity matches `complexity_actual` |
| Process | restated problem, worked an example, named brute force then optimised, tested edge cases before submitting |
| Code quality | readable, no UB warnings, sensible STL use |

Process flaws (F-NO-PLAN, F-BRUTE-SKIPPED, F-COMPLEXITY-NOT-ANALYSED, F-DEBUG-FLAIL) are judged from the conversation transcript and logged even when the verdict is AC.

## Outcome mapping
- **pass**: verdict AC AND ≤1 hint (tier ≤2) AND stated complexity correct.
- **partial**: AC with a tier ≥3 hint or wrong/missing complexity analysis, OR a correct-but-slow solution (TLE) with the right idea.
- **fail**: WA/RE/SAN/CE not fixed by session end, wrong approach, or gave up.

Hint penalty: a tier ≥3 hint (skeleton/solution) caps the outcome at `partial`. Giving up = `fail`.
