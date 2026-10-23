---
name: prep-os
description: Operating Systems practice for /prep: operating system, os quiz, process, thread, deadlock, scheduling. Invoked by the prep orchestrator via --os.
---

# Operating Systems (`os`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `os` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init os --default-level 2`, `MEM profile os`, mode = `quiz`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Interview-level OS: processes/threads, scheduling, synchronization, deadlocks, memory management and paging, TLB, file systems, I/O, IPC, syscalls, Linux practicalities, virtualization/containers basics.
**Out:** Kernel source-level trivia, vendor-specific behaviour without a stated version, networking (prep-net if added), distributed systems (prep-hld).

Topics (taxonomy tags, see `references/taxonomy.md`): processes-threads, scheduling, synchronization, deadlock, memory-management, virtual-memory-paging, page-replacement, tlb-caching, file-systems, io-disk, ipc, syscalls-kernel, concurrency-bugs, virtualization-containers, linux-practical

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `quiz` | difficulty, optional topic, n → n keyed questions (MCQ/short/trace/calc) with confidence capture and per-question debrief |
| `explain` | concept → tight explanation: definition, why it exists, mechanism, trade-offs, 2 interview-style follow-ups with answers |
| `review` | none or topic → resurface missed/low-confidence questions via spaced repetition with fresh variants |
| `mock` | time box → oral-style interviewer: chained questions that dig deeper on each answer |

Default mode: `quiz` · default difficulty: `2`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Recall: process vs thread, what a syscall is, stack vs heap, definition of deadlock. |
| 2 | Mechanism: round-robin trace, mutex vs semaphore, what a page fault does, why context switches cost. |
| 3 | Applied: Banker's algorithm step, page-replacement trace (FIFO/LRU/Belady), effective access time with TLB, priority inversion, producer-consumer correctness. |
| 4 | Deep: copy-on-write/fork internals, TLB shootdowns, memory-ordering/atomics reasoning, lock-free pitfalls, scheduler fairness (CFS), I/O scheduling. |
| 5 | Expert: design questions on kernel mechanisms (build a user-space scheduler, debug a livelock from a trace, NUMA/huge pages trade-offs, io_uring vs epoll). |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `os-<topic>-<short-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Quiz specifics
- Batch: default `n=5` questions per round (mock: 8 chained oral-style questions with follow-ups). Present all, numbered, with *confidence 1-3* requested per answer (1 guess, 2 fairly sure, 3 certain).
- Grade each against its key; a correct answer at confidence 1 is `partial` (lucky), a wrong answer at confidence 3 is the most important flaw (record the misconception).
- Debrief per question: key, 1-line why, the misconception it targets. Then 2-line pattern summary.
- Remember: **one episode per question** (append a JSON list in a single call), `item.ref` = `<domain>-<topic>-<slug>`, plus one `note` for the weakest cluster.
- Calc/trace questions: compute the key with a short script/arithmetic before presenting (never mentally).


## 5. Accuracy gates (hard — run before presenting anything)
**Kind: knowledge.** Every item carries: question · answer key · one-line justification · source tag (textbook chapter, RFC, man page, paper).
1. Independent re-derivation: answer the question again in a separate pass without looking at the key; any mismatch → discard the item.
2. MCQ: exactly one defensible option; distractors are real misconceptions (record each in `x.misconception`), never absurd; no "all/none of the above".
3. Reject opinion-based, version-dependent (unless the version is stated) and pure-trivia items.
4. Explanations: separate what is certain from what you are less than certain about; never invent numbers, citations or API behaviour.
5. Grade open answers per key points (must-have vs nice-to-have), not wording.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path os)` — outside the repo, never committed.
- **Read at start:** `MEM profile os` (already loaded by orchestrator). In `review` mode also `MEM due os` and `MEM tail os 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild os`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
