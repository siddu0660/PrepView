---
name: prep-arch
description: Computer Architecture practice for /prep: computer architecture, cpu pipeline, pipelining, hazard, branch prediction, out of order execution. Invoked by the prep orchestrator via --arch.
---

# Computer Architecture (`arch`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `arch` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init arch --default-level 2`, `MEM profile arch`, mode = `quiz`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Interview-level computer architecture: ISA (RISC/CISC), pipelining and hazards, branch prediction, out-of-order/superscalar execution, cache organization and replacement, cache coherence (MESI), memory consistency models, hardware side of virtual memory, performance equations (CPI, Amdahl), SIMD, multicore/NUMA, GPU basics.
**Out:** Digital logic design/Verilog, OS algorithms (prep-os), microarchitecture of one specific vendor chip.

Topics (taxonomy tags, see `references/taxonomy.md`): isa-risc-cisc, pipelining-hazards, branch-prediction, ooo-superscalar, cache-organization, cache-replacement-write-policy, cache-coherence, memory-consistency, virtual-memory-hardware, performance-equations, simd-vector, multicore-numa, gpu-basics

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `quiz` | difficulty, optional topic, n → n keyed questions incl. calculations verified by script |
| `explain` | concept → mechanism with a small worked example, hazards/trade-offs, 2 follow-ups |
| `review` | none or topic → spaced repetition of missed items with new numbers |
| `mock` | time box → oral interviewer: chained questions from ISA down to cache behaviour of a code snippet |

Default mode: `quiz` · default difficulty: `2`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Recall: RISC vs CISC, what a pipeline stage is, what a cache line is, definition of CPI. |
| 2 | Mechanism: 5-stage pipeline, RAW/WAR/WAW hazards, direct-mapped vs set-associative, write-through vs write-back. |
| 3 | Applied: AMAT with two levels, CPI with instruction mix, tag/index/offset split, Amdahl speedup, stall counting with forwarding. |
| 4 | Deep: Tomasulo/reorder buffer, 2-bit predictor traces, MESI transitions for a sequence of accesses, false sharing, store buffers and TSO vs SC. |
| 5 | Expert: reasoning about cache-miss behaviour of loop nests, memory-ordering litmus tests, prefetching trade-offs, NUMA effects, designing a cache for a workload. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `arch-<topic>-<short-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Quiz specifics
- Batch: default `n=5` questions per round (mock: 8 chained oral-style questions with follow-ups). Present all, numbered, with *confidence 1-3* requested per answer (1 guess, 2 fairly sure, 3 certain).
- Grade each against its key; a correct answer at confidence 1 is `partial` (lucky), a wrong answer at confidence 3 is the most important flaw (record the misconception).
- Debrief per question: key, 1-line why, the misconception it targets. Then 2-line pattern summary.
- Remember: **one episode per question** (append a JSON list in a single call), `item.ref` = `<domain>-<topic>-<slug>`, plus one `note` for the weakest cluster.
- Numeric items (AMAT, CPI, cache address split, Amdahl, pipeline timing, branch penalty): compute the key with `python3 scripts/archcalc.py ...` (relative to this skill's directory) and state all assumptions (forwarding, perfect/real prediction, inclusive/exclusive caches) in the question.


## 5. Accuracy gates (hard — run before presenting anything)
**Kind: knowledge.** Every item carries: question · answer key · one-line justification · source tag (textbook chapter, RFC, man page, paper).
1. Independent re-derivation: answer the question again in a separate pass without looking at the key; any mismatch → discard the item.
2. MCQ: exactly one defensible option; distractors are real misconceptions (record each in `x.misconception`), never absurd; no "all/none of the above".
3. Reject opinion-based, version-dependent (unless the version is stated) and pure-trivia items.
4. Explanations: separate what is certain from what you are less than certain about; never invent numbers, citations or API behaviour.
5. Grade open answers per key points (must-have vs nice-to-have), not wording.
6. Pipeline and coherence traces: simulate the sequence cycle by cycle (or state by state) in a script or table before presenting; state ISA/pipeline assumptions explicitly.
7. Memory-model litmus tests: name the model (SC, x86-TSO, ARMv8) and the allowed/forbidden outcome per its published definition; skip the item if unsure.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path arch)` — outside the repo, never committed.
- **Read at start:** `MEM profile arch` (already loaded by orchestrator). In `review` mode also `MEM due arch` and `MEM tail arch 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild arch`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
