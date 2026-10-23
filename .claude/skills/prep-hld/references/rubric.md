# Rubric — hld

Score each 0-2:

| Dimension | Looks for |
|-----------|-----------|
| Requirements | functional + non-functional (latency, availability, consistency, scale), scope cut |
| Estimation | QPS, storage, bandwidth within ~2x of verified numbers, and *used* to decide |
| API & data model | endpoints/entities before boxes |
| Architecture | coherent flow, right components for the load |
| Trade-offs | alternatives named, costs explicit |
| Scalability | partitioning, caching, hotspots, queues where warranted |
| Reliability | failure modes, replication, degradation, SPOFs |
| Depth | convincing deep dive on one component |

## Outcome mapping
Weighted /16 (Trade-offs, Scalability, Reliability double): **pass** ≥ 70% with no 0 in Requirements or Trade-offs; **partial** 40-70%; **fail** < 40%.

Hint penalty: a tier ≥3 hint (skeleton/solution) caps the outcome at `partial`. Giving up = `fail`.
