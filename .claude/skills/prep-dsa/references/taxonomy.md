# Taxonomy — dsa

## Topic tags
- `arrays`
- `hashing`
- `two-pointers`
- `sliding-window`
- `binary-search`
- `prefix-sums`
- `stack-monotonic`
- `linked-list`
- `trees`
- `bst`
- `heap`
- `graph-bfs-dfs`
- `shortest-path`
- `dsu`
- `topo-sort`
- `dp-1d`
- `dp-2d`
- `dp-knapsack`
- `dp-bitmask`
- `greedy`
- `intervals`
- `backtracking`
- `strings`
- `trie`
- `bit-manipulation`
- `number-theory`
- `segment-tree-fenwick`
- `recursion`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-NO-PLAN` | Started coding before restating the problem / working an example / choosing an approach. |
| `F-BRUTE-SKIPPED` | Did not state a brute force and its complexity before optimising. |
| `F-WRONG-PATTERN` | Chose a technique that does not fit the constraints or structure. |
| `F-GREEDY-UNPROVEN` | Greedy choice without exchange argument or counter-example search. |
| `F-COMPLEXITY-NOT-ANALYSED` | Did not state time/space complexity or got it wrong. |
| `F-EDGE-CASE` | Failed an empty/single/extreme input (harness-detected on edge or n<=1 case). |
| `F-OFF-BY-ONE` | Boundary/index off by one (loop bounds, half-open ranges). |
| `F-DUP-HANDLING` | Duplicates / ties mishandled. |
| `F-STATE-NOT-RESET` | Global or loop state carried across test cases / iterations. |
| `F-WA-LOGIC` | Wrong answer from a logic error (harness-detected). |
| `F-TLE-COMPLEXITY` | Correct but too slow at max constraints (harness-detected). |
| `F-INT-OVERFLOW` | int overflow where long long needed (UBSan-detected). |
| `F-OOB` | Out-of-bounds access (ASan/UBSan-detected). |
| `F-UNINIT` | Uninitialised variable (-Wall warning). |
| `F-NULL` | Null dereference. |
| `F-LIFETIME` | Use-after-free / dangling reference (e.g. invalidated iterator or reference). |
| `F-DIV-ZERO` | Division or modulo by zero. |
| `F-UB-SHIFT` | Undefined shift (width, negative). |
| `F-RECURSION-DEPTH` | Stack overflow from deep recursion (needs iteration or explicit stack). |
| `F-RE-CRASH` | Runtime crash not otherwise classified. |
| `F-STL-MISUSE` | STL pitfall: map::operator[] inserting, erase-while-iterating, comparator not strict weak order, vector<bool> quirks. |
| `F-DEBUG-FLAIL` | Changed code at random after a failure instead of reproducing on a minimal case. |
