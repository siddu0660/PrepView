---
name: prep-db
description: Databases (DBMS) practice for /prep: dbms, database, sql, normalization, acid, isolation level. Invoked by the prep orchestrator via --db, --dbms.
---

# Databases (DBMS) (`db`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `db` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init db --default-level 2`, `MEM profile db`, mode = `quiz`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Interview-level DBMS: relational model, SQL (queries, joins, windows, aggregation), normalization, indexing and B+ trees, query planning, transactions/ACID, isolation levels and anomalies, locking/MVCC, recovery (WAL), storage engines, replication/partitioning basics, SQL vs NoSQL trade-offs.
**Out:** Vendor administration, distributed-systems design at scale (prep-hld), ORM specifics.

Topics (taxonomy tags, see `references/taxonomy.md`): relational-model, sql-queries, joins-aggregation, window-functions, normalization, indexing-btree, query-optimization, transactions-acid, isolation-anomalies, locking-2pl, mvcc, recovery-wal, storage-engines, replication-partitioning, nosql-vs-sql

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `quiz` | difficulty, optional topic, n → n keyed questions (MCQ/short/trace/calc) with confidence capture |
| `sql` | difficulty, optional topic → a schema + task; your SQL is executed on SQLite and compared with the reference result set |
| `explain` | concept → definition, mechanism, anomalies/trade-offs, 2 interview follow-ups with answers |
| `review` | none or topic → spaced repetition of missed questions/queries as fresh variants |
| `mock` | time box → oral interviewer: chained DBMS questions that drill into each answer |

Default mode: `quiz` · default difficulty: `2`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Recall: PK vs unique, what ACID stands for, inner vs left join, what an index is. |
| 2 | Mechanism: 1NF-3NF with a given table, GROUP BY/HAVING, why indexes slow writes, dirty vs non-repeatable read. |
| 3 | Applied: BCNF decomposition with FDs, window functions, composite index column order, deadlock between two transactions, choose isolation level for a scenario. |
| 4 | Deep: B+ tree height/IO calc, MVCC visibility and write skew, WAL/ARIES redo-undo, query plan reading (nested loop vs hash join), covering indexes. |
| 5 | Expert: serializable snapshot isolation, phantom prevention, optimizer cardinality estimation errors, designing indexes for a workload, replication lag anomalies. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `db-<topic>-<short-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Quiz specifics
- Batch: default `n=5` questions per round (mock: 8 chained oral-style questions with follow-ups). Present all, numbered, with *confidence 1-3* requested per answer (1 guess, 2 fairly sure, 3 certain).
- Grade each against its key; a correct answer at confidence 1 is `partial` (lucky), a wrong answer at confidence 3 is the most important flaw (record the misconception).
- Debrief per question: key, 1-line why, the misconception it targets. Then 2-line pattern summary.
- Remember: **one episode per question** (append a JSON list in a single call), `item.ref` = `<domain>-<topic>-<slug>`, plus one `note` for the weakest cluster.

### SQL mode
All paths relative to this skill's directory; work in the scratchpad `P`.
1. Write `$P/schema.sql` (CREATE + INSERT; ≥8 rows with NULLs, ties, duplicates and an empty-group case) and `$P/ref.sql`. Run `python3 scripts/sqlcheck.py run $P/schema.sql $P/ref.sql` and confirm the result matches your own reasoning for the hardest row.
2. Present schema + task text only.
3. Save the user's query to `$P/user.sql`; run `python3 scripts/sqlcheck.py compare $P/schema.sql $P/ref.sql $P/user.sql [--ordered]`. Show verdict, a few expected-vs-got rows and flaws; never show `ref.sql` before AC or give-up.
4. Debrief with `python3 scripts/sqlcheck.py plan ...` for both queries when performance is a point.


## 5. Accuracy gates (hard — run before presenting anything)
**Kind: knowledge.** Every item carries: question · answer key · one-line justification · source tag (textbook chapter, RFC, man page, paper).
1. Independent re-derivation: answer the question again in a separate pass without looking at the key; any mismatch → discard the item.
2. MCQ: exactly one defensible option; distractors are real misconceptions (record each in `x.misconception`), never absurd; no "all/none of the above".
3. Reject opinion-based, version-dependent (unless the version is stated) and pure-trivia items.
4. Explanations: separate what is certain from what you are less than certain about; never invent numbers, citations or API behaviour.
5. Grade open answers per key points (must-have vs nice-to-have), not wording.
6. SQL items: the reference query is executed with `scripts/sqlcheck.py` on SQLite and its result checked against a hand-derived expectation for the trickiest row before presenting. SQLite lacks some features (e.g. no RIGHT JOIN before 3.39, no stored procedures, weak types): state the dialect and avoid items that depend on engine-specific behaviour.
7. Isolation/locking questions must state the engine behaviour assumed (textbook definition vs PostgreSQL vs MySQL InnoDB) because real engines deviate from the SQL standard; never mix them silently.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path db)` — outside the repo, never committed.
- **Read at start:** `MEM profile db` (already loaded by orchestrator). In `review` mode also `MEM due db` and `MEM tail db 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild db`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
