# Rubric — quant/prob

| Dimension | Evidence |
|-----------|----------|
| Answer | exactly equals the verified fraction/value (not 'about') |
| Method | valid derivation, ideally the clean technique |
| Checks | boundary or limiting-case sanity checks |
| Speed | within `target_s` when timed |

Answer correctness is decided by the verified value, never by plausibility.

## Outcome mapping
- **pass**: exact answer, valid method, ≤1 hint (tier ≤2), within time if timed.
- **partial**: right answer with weak/absent derivation, tier ≥3 hint, over time; or right method with an arithmetic slip.
- **fail**: wrong answer with wrong method, or gave up.

Time targets (timed): L1 1m, L2 3m, L3 5m, L4 8m, L5 12m.

Hint penalty: a tier ≥3 hint (skeleton/solution) caps the outcome at `partial`. Giving up = `fail`.
