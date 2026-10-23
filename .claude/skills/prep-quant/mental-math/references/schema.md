# Memory schema — quant/mental-math

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "quant/mental-math", "mode*": "drill",
  "difficulty*": 1,
  "item*": {"ref*": "mm-<cat>-L<level>-s<seed>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"category_stats": "", "n": "", "accuracy": "", "avg_time_s": "", "target_time_s": "", "worst_category": "", "seed": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `category_stats` | Per category {n, correct, avg_time_s}. |
| `n` | Questions in the drill. |
| `accuracy` | Overall fraction correct. |
| `avg_time_s` | Mean seconds per question. |
| `target_time_s` | Target per question at this level. |
| `worst_category` | Category with lowest accuracy. |
| `seed` | Generator seed (replayable). |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (the generated question file with answers and the user's answers).
