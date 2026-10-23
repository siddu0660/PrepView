# Rubric — lld

Score each 0-2 (0 missing, 1 partial, 2 solid):

| Dimension | Looks for |
|-----------|-----------|
| Requirements | actors, use-cases, constraints, out-of-scope stated |
| Entities & relations | right nouns, ownership, cardinality |
| Responsibilities | each class one reason to change |
| Patterns & abstraction | used where variation exists, not elsewhere |
| Correctness | invariants, state transitions, error paths |
| Concurrency | shared state protected / reasoned about |
| Extensibility | handled the changed requirement without rewrite |
| Code | compiles; sensible C++ (RAII, virtual dtor, const-correctness) |

## Outcome mapping
Weighted total /16 (Correctness and Extensibility count double): **pass** ≥ 75% with no 0 in Correctness; **partial** 40-75%; **fail** < 40% or Correctness = 0.

Hint penalty: a tier ≥3 hint (skeleton/solution) caps the outcome at `partial`. Giving up = `fail`.
