# Taxonomy — lld

## Topic tags
- `oop-principles`
- `solid`
- `creational-patterns`
- `structural-patterns`
- `behavioral-patterns`
- `state-machines`
- `concurrency-design`
- `api-design`
- `extensibility`
- `error-handling`
- `testing-design`
- `classic-problems`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-MISSING-REQ` | Did not clarify requirements/actors/scale before designing. |
| `F-GOD-CLASS` | One class owns too many responsibilities (SRP). |
| `F-NO-ABSTRACTION` | Concrete types everywhere; no seam for variation (OCP/DIP). |
| `F-OVER-ENGINEERING` | Patterns or layers with no requirement behind them. |
| `F-PATTERN-MISUSE` | Pattern applied to the wrong problem or implemented incorrectly. |
| `F-LSP-VIOLATION` | Subtype breaks base-class contract. |
| `F-TIGHT-COUPLING` | Classes reach into each other's internals; hard to test or replace. |
| `F-NO-CONCURRENCY` | Shared state with no thread-safety story when the requirements imply it. |
| `F-STATE-LEAK` | Invariants can be broken from outside (public mutable state, no validation). |
| `F-NO-ERROR-HANDLING` | Failure cases/invalid transitions unhandled. |
| `F-EXTENSIBILITY-FAIL` | Changed-requirement probe required rewriting, not extending. |
| `F-NOT-COMPILABLE` | C++ skeleton does not compile (g++ -fsyntax-only). |
| `F-RESOURCE-MGMT` | C++ ownership issues: raw new/delete, missing virtual destructor, copy/move mistakes. |
