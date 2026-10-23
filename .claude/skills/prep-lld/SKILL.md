---
name: prep-lld
description: Low-Level Design (OOD) practice for /prep: lld, low level design, object oriented design, class design, design pattern, solid. Invoked by the prep orchestrator via --lld, --oop.
---

# Low-Level Design (OOD) (`lld`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `lld` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init lld --default-level 2`, `MEM profile lld`, mode = `design`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Object-oriented design interviews in C++: requirements, entities, relationships, patterns, SOLID, state machines, concurrency in design, extensibility, clean public APIs.
**Out:** Distributed architecture (prep-hld), algorithm optimisation (prep-dsa), language syntax drills.

Topics (taxonomy tags, see `references/taxonomy.md`): oop-principles, solid, creational-patterns, structural-patterns, behavioral-patterns, state-machines, concurrency-design, api-design, extensibility, error-handling, testing-design, classic-problems

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `design` | difficulty, optional system → one LLD problem: requirements dialogue, user's design + C++ skeleton, graded vs hidden rubric with an extensibility probe |
| `quiz` | difficulty, topic, n → pattern/principle questions (which pattern, spot the smell, fix the violation) |
| `explain` | pattern/principle → problem it solves, C++ minimal example, misuse cases, relation to neighbours |
| `review` | none or topic → revisit weak designs/smells from memory with a changed requirement |
| `mock` | time box (default 45m) → interviewer simulation: sparse prompt, clarifications on request, 1 mid-session requirement change |

Default mode: `design` · default difficulty: `2`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Tic-tac-toe, parking lot (single type), basic bank account: 3-5 classes, clear nouns/verbs. |
| 2 | Library system, vending machine (state), elevator (single car): one pattern needed (State/Strategy). |
| 3 | Splitwise, ATM, multi-elevator scheduler, chess: several patterns, invariants, validation rules. |
| 4 | Thread-safe LRU/cache, rate limiter, logger framework, pub-sub, task scheduler: concurrency and extensibility under change. |
| 5 | Plugin architecture, workflow engine, game engine core, text editor with undo/redo and collaboration hooks: layered design with strong trade-off defence. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `lld-<system>-<variant>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Design specifics
Present a one-line prompt only; answer clarifying questions tersely and in character. Let the user drive; interrupt only to enforce the time box. Pose the extensibility probe after their first full design.

## 5. Accuracy gates (hard — run before presenting anything)
**Kind: design.** Graded against a rubric, not intuition.
1. Before presenting, write the hidden rubric: requirements (functional + non-functional), key decisions with their trade-offs, failure modes, and where numbers are expected.
2. Every number you state or expect (QPS, storage, latency, memory) is computed with a script/arithmetic check, not recalled.
3. Accept any valid design; mark only violations of requirements, correctness bugs, or unjustified decisions. Do not grade on matching your own solution.
4. Each critique quotes the user's own words and says what to change; no generic advice.
5. Probe once: ask one follow-up that stress-tests their weakest decision (scale ×10, a node failure, a new requirement) and grade the reaction.
6. Any C++ skeleton you show (reference or critique) must pass `g++ -std=c++20 -fsyntax-only` first; run the user's skeleton through the same check and report compile errors as `F-NOT-COMPILABLE` rather than judging by eye.
7. Prepare the extensibility probe (a changed requirement) at generation time, together with the hidden rubric; do not invent it after seeing the user's design.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path lld)` — outside the repo, never committed.
- **Read at start:** `MEM profile lld` (already loaded by orchestrator). In `review` mode also `MEM due lld` and `MEM tail lld 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild lld`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
