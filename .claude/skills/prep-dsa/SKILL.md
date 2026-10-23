---
name: prep-dsa
description: Data Structures & Algorithms (C++) practice for /prep: dsa, leetcode, algorithm, data structure, array, string problem. Invoked by the prep orchestrator via --dsa, --algo.
---

# Data Structures & Algorithms (C++) (`dsa`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `dsa` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init dsa --default-level 2`, `MEM profile dsa`, mode = `problem`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Coding-interview algorithm problems solved in C++20: arrays, strings, hashing, trees, graphs, DP, greedy, heaps, intervals, bit tricks, number theory; complexity analysis; STL pitfalls.
**Out:** System design (prep-hld/prep-lld), language trivia unrelated to solving problems, non-C++ solutions (translate on request but judge only C++).

Topics (taxonomy tags, see `references/taxonomy.md`): arrays, hashing, two-pointers, sliding-window, binary-search, prefix-sums, stack-monotonic, linked-list, trees, bst, heap, graph-bfs-dfs, shortest-path, dsu, topo-sort, dp-1d, dp-2d, dp-knapsack, dp-bitmask, greedy, intervals, backtracking, strings, trie, bit-manipulation, number-theory, segment-tree-fenwick, recursion

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `problem` | difficulty, optional topic → one verified problem; judge the user's C++ against the harness |
| `quiz` | difficulty, topic → rapid conceptual questions (complexity, invariants, STL behaviour), each checked by a runnable snippet when behavioural |
| `explain` | pattern/algorithm name → concise explanation: invariant, template code in C++, when it fails, 2 canonical problems |
| `review` | none or topic → resurface due/failed items from memory (spaced repetition), re-judge a fresh attempt |
| `mock` | number of problems (default 2), time box → interviewer simulation: statement only, clarifying questions answered tersely, time tracked, full debrief at end |

Default mode: `problem` · default difficulty: `2`. `--timed`: enforce the expected time per item and log `time_s`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Warm-up, one idea: Two Sum, Valid Parentheses, Reverse Linked List, Best Time to Buy/Sell Stock. |
| 2 | Standard screen: sliding window (fixed/variable), BFS on grid, binary search on sorted array, prefix sums, hash-map counting, simple tree DFS. |
| 3 | On-site medium: LRU cache, topological sort, binary search on answer, 2D/knapsack DP, union-find, monotonic stack, Dijkstra on small graphs. |
| 4 | Strong on-site / top firm: segment tree or Fenwick, bitmask DP, DP optimisation, trie+DFS, graph with state (BFS on states), tricky greedy with proof. |
| 5 | Elite: Codeforces ~1900-2300 style, multi-insight (offline queries, divide and conquer, SCC/bridges, convex-hull trick, heavy edge-case design). |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `dsa-<topic>-<short-title-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### DSA specifics
All paths relative to this skill's directory. Work in the scratchpad, e.g. `P=<scratchpad>/dsa/<ref>`.
1. **Generate** — write `$P/{statement.md,ref.cpp,brute.cpp,gen.cpp,edge/*.in,meta.json}` per `harness/judge.py` docstring. `gen.cpp <seed> <n>` must be deterministic; use tiny value ranges on small cases to force ties/negatives and full range on large cases. Choose `large_n`/`tl_s` so the intended solution passes and the brute force does not.
2. **Verify** — `python3 harness/judge.py verify $P`. Exit 0 required (it checks ref==brute on edge+200 small cases under sanitizers, ref speed, and that brute fails the limit). On failure read `stage`/`detail`, fix, retry (max 3), else tell the user and fall back to a different problem. Pass `--allow-fast-brute` only at level 1.
3. **Present** — print `statement.md` only (plus time box if `--timed`: L1 15m, L2 25m, L3 35m, L4 45m, L5 60m).
4. **Interact** — before accepting code, ask once (unprompted only if they jump straight to code): approach + complexity. When the user submits code, save to `$P/sol.cpp` and run `python3 harness/judge.py judge $P $P/sol.cpp`. Report verdict + `case` + the minimal failing `input` + `flaws`; do NOT reveal the reference solution. Resubmissions count as `attempts`.
5. **Debrief** — show a clean reference approach (from `ref.cpp`), the key insight, and map every harness `flaws` entry plus process flaws to taxonomy codes.
6. **Remember** — `save-item` the whole `$P` (exclude `.build`), then `append` with `x` per schema.

**Quiz/explain** items about behaviour (complexity, iterator invalidation, UB) must be confirmed by compiling and running a tiny C++ snippet before they are asked.
**Mock**: no hints unless the user asks; clarify requirements tersely like an interviewer; evaluate both process and code; fan-out generation for the n problems may use parallel subagents.

## 5. Accuracy gates (hard — run before presenting anything)
**Kind: code-checkable.** Nothing is shown until it is machine-verified.
1. Author: statement, reference solution, an *independent* brute force (different algorithm), input generator, constraints.
2. Execute in the scratchpad (never the repo): reference must equal brute force on ≥200 random small cases plus hand-written edge cases (empty/min/max, duplicates, negatives, overflow range).
3. Difficulty anchor: the intended solution meets the limit at max constraints and the brute force does **not**; otherwise raise constraints or regenerate.
4. Grade user answers by **executing** them on the same harness — never by reading and judging.
5. Reject ambiguity: input format, constraints, tie-breaks and output format are all stated.
6. Harness is mandatory: `python3 harness/judge.py verify <dir>` must exit 0 before the statement is shown. `python3 harness/judge.py selftest` proves the harness itself (run it if a verdict looks suspicious).
7. Language is C++20 (`g++ -std=c++20 -O2`); the same solution is also built with `-fsanitize=address,undefined` — UB that 'works' still counts as a flaw.
8. Dedupe: skip any `item.ref` already in memory (`MEM seen dsa <ref>`) unless in review mode; refs follow `dsa-<topic>-<slug>`.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path dsa)` — outside the repo, never committed.
- **Read at start:** `MEM profile dsa` (already loaded by orchestrator). In `review` mode also `MEM due dsa` and `MEM tail dsa 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild dsa`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
