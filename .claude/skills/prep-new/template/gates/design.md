**Kind: design.** Graded against a rubric, not intuition.
1. Before presenting, write the hidden rubric: requirements (functional + non-functional), key decisions with their trade-offs, failure modes, and where numbers are expected.
2. Every number you state or expect (QPS, storage, latency, memory) is computed with a script/arithmetic check, not recalled.
3. Accept any valid design; mark only violations of requirements, correctness bugs, or unjustified decisions. Do not grade on matching your own solution.
4. Each critique quotes the user's own words and says what to change; no generic advice.
5. Probe once: ask one follow-up that stress-tests their weakest decision (scale ×10, a node failure, a new requirement) and grade the reaction.
