# Taxonomy — db

## Topic tags
- `relational-model`
- `sql-queries`
- `joins-aggregation`
- `window-functions`
- `normalization`
- `indexing-btree`
- `query-optimization`
- `transactions-acid`
- `isolation-anomalies`
- `locking-2pl`
- `mvcc`
- `recovery-wal`
- `storage-engines`
- `replication-partitioning`
- `nosql-vs-sql`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-CONCEPT-CONFUSION` | Mixed up two related concepts. |
| `F-DEF-WRONG` | Incorrect or imprecise definition. |
| `F-CALC-ERROR` | Arithmetic or formula error in a calculation. |
| `F-TRADEOFF-MISSING` | Gave a mechanism without its cost/benefit trade-off. |
| `F-OVERCONFIDENT` | Wrong at confidence 3. |
| `F-LUCKY-GUESS` | Right at confidence 1 (unreliable knowledge). |
| `F-SCOPE-SHALLOW` | Right headline, missed the key mechanism when asked to go deeper. |
| `F-NORMAL-FORM-ERROR` | Wrong normal form, missed functional dependency, or bad decomposition. |
| `F-ANOMALY-CONFUSION` | Confused isolation anomalies (dirty/non-repeatable/phantom/write skew) or what each level prevents. |
| `F-INDEX-MISUSE` | Index choice/order wrong; ignored selectivity, write cost or covering. |
| `F-SQL-SYNTAX` | Query does not parse/run (harness-detected). |
| `F-SQL-WRONG-LOGIC` | Query runs but returns wrong rows (harness-detected). |
| `F-SQL-MISSING-ROWS` | Fewer rows than expected (e.g. inner join dropping NULL side, wrong filter). |
| `F-SQL-DUPLICATES-OR-JOIN-FANOUT` | Too many rows: join fan-out, missing DISTINCT/GROUP BY. |
| `F-SQL-WRONG-COLUMNS` | Right rows, wrong columns/aggregation. |
| `F-SQL-NULL-SEMANTICS` | NULL handling error (= NULL, NOT IN with NULL, COUNT(col) vs COUNT(*)). |
| `F-ACID-CONFUSION` | Misstated what A/C/I/D guarantee. |
| `F-PLAN-MISREAD` | Misread a query plan (scan vs seek, join type). |
