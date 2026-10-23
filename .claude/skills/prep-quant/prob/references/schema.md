# Memory schema — quant/prob

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "quant/prob", "mode*": "problem",
  "difficulty*": 1,
  "item*": {"ref*": "prob-<topic>-<short-slug>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"method": "", "method_ideal": "", "answer_given": "", "answer_true": "", "sanity_checks_done": "", "time_s": "", "target_s": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `method` | Technique the user used. |
| `method_ideal` | Cleanest technique for this problem. |
| `answer_given` | User's final answer. |
| `answer_true` | Verified exact answer (fraction). |
| `sanity_checks_done` | Checks the user performed. |
| `time_s` | Seconds taken vs target. |
| `target_s` | Interview target for this level. |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (statement, exact answer, verification script, ideal solution).
