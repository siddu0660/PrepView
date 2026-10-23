# Taxonomy — arch

## Topic tags
- `isa-risc-cisc`
- `pipelining-hazards`
- `branch-prediction`
- `ooo-superscalar`
- `cache-organization`
- `cache-replacement-write-policy`
- `cache-coherence`
- `memory-consistency`
- `virtual-memory-hardware`
- `performance-equations`
- `simd-vector`
- `multicore-numa`
- `gpu-basics`

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
| `F-HAZARD-ERROR` | Misidentified a pipeline hazard or wrong stall/forwarding count. |
| `F-CACHE-ADDR-ERROR` | Wrong tag/index/offset split or set count (verified by archcalc). |
| `F-AMAT-ERROR` | AMAT/CPI formula misuse (e.g. forgot miss-rate global vs local, or hit time). |
| `F-AMDAHL-ERROR` | Amdahl's law misapplied. |
| `F-COHERENCE-STATE-ERROR` | Wrong MESI state transition or bus action. |
| `F-CONSISTENCY-CONFUSION` | Confused coherence with consistency or misjudged a litmus outcome. |
| `F-PREDICTOR-TRACE-ERROR` | Wrong branch-predictor state trace. |
| `F-LOCALITY-MISSED` | Missed spatial/temporal locality effect in a code example. |
| `F-UNITS-ERROR` | Cycles vs seconds / bytes vs bits / KB vs KiB slip. |
