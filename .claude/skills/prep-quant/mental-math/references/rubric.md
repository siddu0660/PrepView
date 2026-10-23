# Rubric — quant/mental-math

Graded by `scripts/drill.py grade` (exact for integers, tolerance for estimation categories).

| Dimension | Evidence |
|-----------|----------|
| Accuracy | fraction correct overall and per category |
| Speed | average seconds/question vs `target_time_s` (user-reported total time) |
| Method | noted from the explanations the user gives when asked how they got a miss |

## Outcome mapping
Per drill: **pass** accuracy ≥ 90% and avg time ≤ target; **partial** accuracy 70-90% or over time; **fail** < 70%.
Targets (s/question): L1 6, L2 10, L3 15, L4 20, L5 25.

Hint penalty: a tier ≥3 hint (skeleton/solution) caps the outcome at `partial`. Giving up = `fail`.
