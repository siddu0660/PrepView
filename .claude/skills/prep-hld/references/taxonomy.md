# Taxonomy — hld

## Topic tags
- `requirements`
- `estimation`
- `api-design`
- `data-modeling`
- `sql-vs-nosql`
- `caching`
- `sharding-partitioning`
- `replication-consistency`
- `queues-streams`
- `load-balancing-cdn`
- `rate-limiting`
- `search-indexing`
- `realtime-push`
- `failure-modes`
- `observability`
- `security-privacy`
- `cost`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-NO-REQUIREMENTS` | Jumped to boxes without functional/non-functional requirements. |
| `F-NO-ESTIMATION` | No back-of-envelope numbers where scale decides the design. |
| `F-ESTIMATION-ERROR` | Arithmetic or order-of-magnitude error in estimates. |
| `F-NO-TRADEOFFS` | Chose a component without naming alternatives and costs. |
| `F-WRONG-STORE` | Storage choice inconsistent with access pattern or consistency need. |
| `F-CONSISTENCY-IGNORED` | No stance on consistency/staleness/ordering where it matters. |
| `F-SPOF` | Single point of failure left in the design. |
| `F-HOTSPOT-IGNORED` | Skew / hot key / thundering herd not considered. |
| `F-NO-FAILURE-MODES` | Did not discuss what fails and how it recovers. |
| `F-BUZZWORD-DROPPING` | Named technologies without explaining the mechanism or why. |
| `F-OVERCOMPLICATED` | Microservices/queues/caches added with no requirement. |
| `F-API-DATA-MISSING` | No API or data model before architecture. |
| `F-DEPTH-LACK` | Could not go deep when the interviewer drilled into a component. |
