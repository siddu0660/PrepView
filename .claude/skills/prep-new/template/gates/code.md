**Kind: code-checkable.** Nothing is shown until it is machine-verified.
1. Author: statement, reference solution, an *independent* brute force (different algorithm), input generator, constraints.
2. Execute in the scratchpad (never the repo): reference must equal brute force on ≥200 random small cases plus hand-written edge cases (empty/min/max, duplicates, negatives, overflow range).
3. Difficulty anchor: the intended solution meets the limit at max constraints and the brute force does **not**; otherwise raise constraints or regenerate.
4. Grade user answers by **executing** them on the same harness — never by reading and judging.
5. Reject ambiguity: input format, constraints, tie-breaks and output format are all stated.
