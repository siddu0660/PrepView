# Rubric — db

| Format | Correct means |
|--------|---------------|
| mcq | exact option |
| short | all must-have key points present; nice-to-haves only affect the debrief |
| trace/calc | final value AND intermediate steps match the key (right answer from wrong steps = partial) |
| oral | each chained follow-up graded separately; outcome = worst of the core points |

Confidence modifies reporting: wrong@3 → record `F-OVERCONFIDENT` with the misconception; right@1 → `partial` + `F-LUCKY-GUESS`.

**sql mode:** correctness is decided only by `scripts/sqlcheck.py compare` (multiset equality of result rows; `--ordered` when ORDER BY is part of the task). Style (readability, avoiding SELECT *, sargable predicates) is commented on but never changes the verdict.

## Outcome mapping
- **pass**: all must-have points correct, confidence ≥2.
- **partial**: some must-have points, or correct at confidence 1, or right answer from flawed steps.
- **fail**: wrong, or none of the must-haves.
- **sql mode:** pass = AC with ≤1 hint; partial = AC after a tier ≥3 hint or after 3+ attempts; fail = ERR/WA at the end.

Hint penalty: a tier ≥3 hint (skeleton/solution) caps the outcome at `partial`. Giving up = `fail`.
