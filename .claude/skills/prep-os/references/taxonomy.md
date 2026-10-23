# Taxonomy — os

## Topic tags
- `processes-threads`
- `scheduling`
- `synchronization`
- `deadlock`
- `memory-management`
- `virtual-memory-paging`
- `page-replacement`
- `tlb-caching`
- `file-systems`
- `io-disk`
- `ipc`
- `syscalls-kernel`
- `concurrency-bugs`
- `virtualization-containers`
- `linux-practical`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-CONCEPT-CONFUSION` | Mixed up two related concepts (e.g. mutex/semaphore, process/thread, paging/segmentation). |
| `F-DEF-WRONG` | Incorrect or imprecise definition. |
| `F-CALC-ERROR` | Arithmetic or formula error in a calculation (EAT, page table size, address split). |
| `F-TRACE-ERROR` | Wrong execution trace (scheduling Gantt, page-replacement, semaphore ordering). |
| `F-RACE-MISSED` | Failed to see a race condition or missing memory barrier/atomicity. |
| `F-DEADLOCK-CONDITIONS` | Wrong Coffman conditions or wrong prevention/avoidance/detection reasoning. |
| `F-TRADEOFF-MISSING` | Gave a mechanism without its cost/benefit trade-off. |
| `F-OVERCONFIDENT` | Wrong at confidence 3. |
| `F-LUCKY-GUESS` | Right at confidence 1 (unreliable knowledge). |
| `F-SCOPE-SHALLOW` | Right headline, missed the key mechanism when asked to go deeper. |
