---
name: prep-hld
description: High-Level System Design practice for /prep: hld, high level design, system design, design twitter, design a url shortener, scalability. Invoked by the prep orchestrator via --hld, --sd.
---

# High-Level System Design (`hld`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `hld` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init hld --default-level 3`, `MEM profile hld`, mode = `design`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Distributed system design interviews: requirements, estimation, APIs, data models, storage choice, caching, partitioning, replication/consistency, queues/streams, failure modes, observability.
**Out:** Class-level design (prep-lld), implementation code, vendor marketing comparisons.

Topics (taxonomy tags, see `references/taxonomy.md`): requirements, estimation, api-design, data-modeling, sql-vs-nosql, caching, sharding-partitioning, replication-consistency, queues-streams, load-balancing-cdn, rate-limiting, search-indexing, realtime-push, failure-modes, observability, security-privacy, cost

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `design` | difficulty, optional system → one HLD problem walked through the standard stages, graded vs hidden rubric with one stress probe |
| `quiz` | difficulty, topic, n → rapid trade-off and numbers questions (e.g. quorum maths, when to shard, cache invalidation) |
| `explain` | concept → clear a concept: problem, mechanism, trade-offs, when NOT to use it, numbers |
| `review` | none or topic → re-run weak areas from memory with a harder variant |
| `mock` | time box (default 45m) → full interviewer simulation with deep-dive requested on the weakest decision |

Default mode: `design` · default difficulty: `3`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | URL shortener, pastebin: single DB, simple cache, ID generation. |
| 2 | Rate limiter, notification service, news feed (small), key-value store single node: one scaling idea each. |
| 3 | Twitter timeline, WhatsApp chat, Uber-lite, web crawler: fan-out choices, sharding, queues, hot keys. |
| 4 | Distributed KV store, ticket booking with strong consistency, YouTube, distributed cache: replication, consensus-adjacent trade-offs, failure handling. |
| 5 | Ad click aggregation with exactly-once, global strongly-consistent store, collaborative editor (CRDT/OT), Spanner-like design: deep consistency/time/failure reasoning. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `hld-<system>-<variant>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Stages (user may reorder; you grade coverage)
Requirements → estimation → API → data model → high-level architecture → deep dive → bottlenecks/failures → stress probe. Do not volunteer the next stage; ask 'what next?' only after silence.

## 5. Accuracy gates (hard — run before presenting anything)
**Kind: design.** Graded against a rubric, not intuition.
1. Before presenting, write the hidden rubric: requirements (functional + non-functional), key decisions with their trade-offs, failure modes, and where numbers are expected.
2. Every number you state or expect (QPS, storage, latency, memory) is computed with a script/arithmetic check, not recalled.
3. Accept any valid design; mark only violations of requirements, correctness bugs, or unjustified decisions. Do not grade on matching your own solution.
4. Each critique quotes the user's own words and says what to change; no generic advice.
5. Probe once: ask one follow-up that stress-tests their weakest decision (scale ×10, a node failure, a new requirement) and grade the reaction.
6. Verify every number (QPS, storage, bandwidth, cache size) with a script; keep the table in the hidden rubric and compare the user's estimates against it, not against intuition.
7. State consistency/availability claims precisely (e.g. quorum R+W>N reasoning, CAP vs PACELC); if unsure of a protocol detail, say so rather than assert it.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path hld)` — outside the repo, never committed.
- **Read at start:** `MEM profile hld` (already loaded by orchestrator). In `review` mode also `MEM due hld` and `MEM tail hld 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild hld`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
