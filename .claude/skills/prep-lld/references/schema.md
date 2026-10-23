# Memory schema — lld

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "lld", "mode*": "design",
  "difficulty*": 1,
  "item*": {"ref*": "lld-<system>-<variant>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"system": "", "entities": "", "patterns_used": "", "smells": "", "extensibility_probe": "", "concurrency_considered": "", "compiles": "", "requirements_clarified": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `system` | What was designed (e.g. 'parking lot'). |
| `entities` | Core classes/interfaces identified. |
| `patterns_used` | Patterns applied and whether justified. |
| `smells` | Design smells observed in the user's design. |
| `extensibility_probe` | The changed requirement posed and pass/fail. |
| `concurrency_considered` | true/false |
| `compiles` | true/false for user's C++ skeleton |
| `requirements_clarified` | number of clarifying questions asked |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (prompt, hidden rubric, reference class sketch, user's last design).
