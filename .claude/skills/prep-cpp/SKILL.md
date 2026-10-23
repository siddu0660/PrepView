---
name: prep-cpp
description: C++ Language (C++11 to C++20) practice for /prep: c++, cpp, c++20, c++17, c++11, raii. Invoked by the prep orchestrator via --cpp.
---

# C++ Language (C++11 to C++20) (`cpp`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `cpp` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init cpp --default-level 2`, `MEM profile cpp`, mode = `quiz`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** C++ language and standard library from C++11 through C++20: value categories and move semantics, RAII and smart pointers, object lifetime and UB, templates/concepts/constexpr, STL containers/iterators/algorithms/ranges, lambdas, OOP and vtables, exceptions, concurrency and the memory model, coroutines, three-way comparison, C++20 features.
**Out:** Algorithm problems (prep-dsa), modules and build systems (not verifiable here), C++23 and later, compiler-specific extensions.

Topics (taxonomy tags, see `references/taxonomy.md`): value-categories-move, raii-smart-pointers, rule-of-five, object-lifetime-ub, templates-deduction, concepts-constraints, constexpr-consteval, stl-containers-iterators, algorithms-ranges, lambdas-callables, oop-virtual-vtable, exceptions-safety, concurrency-memory-model, coroutines, cpp20-features

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `quiz` | difficulty, optional topic, n → n keyed questions; any behavioural claim is confirmed by compiling and running |
| `predict` | difficulty, optional topic → a snippet: what does it print / does it compile / is it UB? ground truth from the compiler |
| `debug` | difficulty, optional topic → a snippet with a planted bug; you find and fix it; fix is compiled and checked under sanitizers |
| `explain` | feature → motivation, mechanism, minimal example, pitfalls, C++20 changes |
| `review` | none or topic → spaced repetition of missed items with modified snippets |
| `mock` | time box → language-lawyer style interview: chained questions, each probing one level deeper |

Default mode: `quiz` · default difficulty: `2`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Basics: references vs pointers, const, stack vs heap, auto, range-for, struct vs class. |
| 2 | Core: RAII, unique_ptr/shared_ptr ownership, rule of 3/5/0, virtual destructor, std::vector growth and iterator invalidation. |
| 3 | Applied: move semantics and value categories, templates and deduction, lambdas captures (dangling), copy elision, exception safety, constexpr basics. |
| 4 | Deep: perfect forwarding, SFINAE vs concepts, ADL, vtable layout and slicing, memory_order and data races, coroutines basics, ranges views laziness, three-way comparison. |
| 5 | Expert: strict aliasing, sequence points/unspecified order, lifetime extension corner cases, ODR violations, designing a coroutine task type, constexpr evaluation limits. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `cpp-<topic>-<short-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Quiz specifics
- Batch: default `n=5` questions per round (mock: 8 chained oral-style questions with follow-ups). Present all, numbered, with *confidence 1-3* requested per answer (1 guess, 2 fairly sure, 3 certain).
- Grade each against its key; a correct answer at confidence 1 is `partial` (lucky), a wrong answer at confidence 3 is the most important flaw (record the misconception).
- Debrief per question: key, 1-line why, the misconception it targets. Then 2-line pattern summary.
- Remember: **one episode per question** (append a JSON list in a single call), `item.ref` = `<domain>-<topic>-<slug>`, plus one `note` for the weakest cluster.

### predict / debug
All paths relative to this skill's directory; work in the scratchpad `P`.
1. Write `$P/item.cpp` (≤30 lines, self-contained, `#include`s explicit). Run `python3 scripts/cppcheck.py run $P/item.cpp`. For "does it compile?" items run `python3 scripts/cppcheck.py fails $P/item.cpp`.
2. Use the result as the key: verdict `OK` → ask for the exact output; `UB` → ask 'what is wrong / what can happen' (never ask for the output); `UNSPECIFIED` or differing between -O0/-O2 → discard and regenerate.
3. Present only the snippet plus the standard (C++11/14/17/20) and compiler assumption (g++ 13, `-std=c++20` unless the item says otherwise).
4. debug mode: save the user's fixed file as `$P/fix.cpp` and run `cppcheck.py run` on it; compare stdout with the intended output you recorded.


## 5. Accuracy gates (hard — run before presenting anything)
**Kind: knowledge.** Every item carries: question · answer key · one-line justification · source tag (textbook chapter, RFC, man page, paper).
1. Independent re-derivation: answer the question again in a separate pass without looking at the key; any mismatch → discard the item.
2. MCQ: exactly one defensible option; distractors are real misconceptions (record each in `x.misconception`), never absurd; no "all/none of the above".
3. Reject opinion-based, version-dependent (unless the version is stated) and pure-trivia items.
4. Explanations: separate what is certain from what you are less than certain about; never invent numbers, citations or API behaviour.
5. Grade open answers per key points (must-have vs nice-to-have), not wording.
6. Every behavioural claim (output, compiles, UB, complexity guarantee) is confirmed by `python3 scripts/cppcheck.py` before it is asked or used as a key; recalled 'facts' about the standard must cite the clause/cppreference page in `source` and be marked 'standard says' vs 'g++ 13 does'.
7. Never verify modules with the tool (unreliable on g++ 13); mark such items 'conceptual only' and keep them out of predict/debug.
8. Implementation-defined results (e.g. sizeof(long), name mangling, string literal addresses) are asked only with the platform stated.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path cpp)` — outside the repo, never committed.
- **Read at start:** `MEM profile cpp` (already loaded by orchestrator). In `review` mode also `MEM due cpp` and `MEM tail cpp 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild cpp`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
