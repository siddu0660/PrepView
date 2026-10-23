# Rubric — cpp

| Format | Correct means |
|--------|---------------|
| mcq | exact option |
| short | all must-have key points present; nice-to-haves only affect the debrief |
| trace/calc | final value AND intermediate steps match the key (right answer from wrong steps = partial) |
| oral | each chained follow-up graded separately; outcome = worst of the core points |

Confidence modifies reporting: wrong@3 → record `F-OVERCONFIDENT` with the misconception; right@1 → `partial` + `F-LUCKY-GUESS`.

**predict / debug:** correctness is decided only by `scripts/cppcheck.py` output. predict = exact stdout or the exact verdict (compiles / which UB). debug = the user identifies the planted bug AND their fix compiles, runs clean under ASan/UBSan, and keeps the intended output.

## Outcome mapping
- **pass**: all must-have points correct, confidence ≥2.
- **partial**: some must-have points, or correct at confidence 1, or right answer from flawed steps.
- **fail**: wrong, or none of the must-haves.
- **predict:** pass = exact match at confidence ≥2.
- **debug:** pass = bug named + verified fix with ≤1 hint; partial = fix works but the cause was wrongly explained, or tier ≥3 hint; fail = bug not found/fix fails.

Hint penalty: a tier ≥3 hint (skeleton/solution) caps the outcome at `partial`. Giving up = `fail`.
