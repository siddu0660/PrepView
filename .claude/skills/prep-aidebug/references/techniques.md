# Technique catalog (curated). Each `##` heading is a ledger entry name for `playbook.py`.

## Repro first
When: before any edit or prompt. How: run the failing test, read the exact assertion and traceback, write down expected vs actual. Anti-pattern: asking the AI "why is my code broken" with no failure attached.

## Minimal repro prompt
When: consulting the AI. How: give the failing test name, the traceback, expected vs actual, and only the 1-2 functions on the stack. Bad: "fix this repo" + 3000 lines. Good: "test_refund fails: expected 90.0 got 100.0; code below; I suspect the discount is applied twice - what else would explain it?"

## Hypothesis ledger
When: more than one plausible cause. How: write 2-3 hypotheses with the observation that would falsify each, test the cheapest first, cross it off. Anti-pattern: editing until green.

## Bisect the call path
When: symptom is far from cause. How: print/assert at the boundaries of the pipeline (input, after parse, after transform, before output) to find the first wrong value; `git bisect` if history exists.

## Read the contract, not the body
When: unfamiliar module. How: read tests, public signatures, docstrings and call sites first; open function bodies only on the suspect path. Ask the AI for a call graph or data-flow summary, then verify two edges by grep.

## Verify before apply
When: the AI proposes a cause or patch. How: turn the claim into a prediction ("if that is the cause, input X must give Y"), run it, then apply. Reject claims you cannot test. Planted wrong claims are part of this skill.

## Falsify with a new test
When: you have a fix idea. How: write or extend a failing test that captures the bug before fixing; it must fail for the right reason and pass after.

## One change at a time
When: any fix. How: single edit, rerun tests, keep or revert. Anti-pattern: three edits and a prayer.

## Minimal diff
When: finalising. How: revert incidental edits; the diff should read like the root-cause sentence. Large diffs hide regressions.

## Root cause sentence
When: before declaring a bug fixed. How: say in one sentence why the bug happened and why the fix removes it, not just that tests pass. Check whether the same pattern exists elsewhere (grep).

## Invariants and boundaries
When: numeric, time or ordering code. How: check units, off-by-one, empty/one/many, None, ties, timezone, rounding, stable sort, mutation of shared defaults/aliases.

## Regression sweep
When: after the last fix. How: run the whole suite, not just the failing test; then ask what else the touched code feeds.

## Time-box checkpoints
When: any timed round. How: 20% reproduce and map, 50% localise and fix, 20% verify, 10% write-up; if stuck for 5 minutes, change the question (smaller repro, different layer, ask the AI for hypotheses not fixes).

## Tool leverage
When: stuck on state. How: `python -m pdb`/breakpoint, targeted prints with labels, `grep -rn`, `git log -p`/`git blame` on the suspect lines, `python -X dev` for warnings.

## Critique the AI's diagnosis
When: reviewing an AI answer. How: split into atomic claims, mark each as checkable, test the cheapest checkable ones, and check whether the diagnosis explains all symptoms rather than just the first.
