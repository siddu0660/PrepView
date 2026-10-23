# Taxonomy — quant/prob

## Topic tags
- `counting-combinatorics`
- `conditional-bayes`
- `linearity-of-expectation`
- `indicator-variables`
- `symmetry`
- `first-step-recursion`
- `markov-chains`
- `random-walks`
- `martingales-stopping`
- `order-statistics`
- `geometric-probability`
- `distributions-moments`
- `dice-coins-cards`
- `games-optimal-stopping`
- `bounds-inequalities`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-PROB-DOUBLE-COUNT` | Counted outcomes twice or ignored ordering/indistinguishability. |
| `F-PROB-INDEPENDENCE-ASSUMED` | Assumed independence that is not given. |
| `F-PROB-CONDITIONING-SLIP` | Conditioned on the wrong event (boy-girl, Monty Hall style). |
| `F-PROB-MISSED-LINEARITY` | Used a hard route when linearity of expectation sufficed. |
| `F-PROB-MISSED-SYMMETRY` | Failed to exploit a symmetry argument. |
| `F-PROB-BAD-STATE-SPACE` | Wrong or bloated state definition for a recursion/Markov chain. |
| `F-PROB-NO-BOUNDARY` | Boundary/absorbing conditions wrong or missing. |
| `F-PROB-NO-SANITY-CHECK` | No limiting-case / probabilities-sum-to-1 sanity check. |
| `F-PROB-ARITH-ERROR` | Right method, arithmetic slip. |
| `F-PROB-SLOW` | Correct but beyond the time target (when --timed). |
| `F-PROB-NO-METHOD` | Guessed an answer with no derivation. |
