# Memory schema — dsa

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "dsa", "mode*": "problem",
  "difficulty*": 1,
  "item*": {"ref*": "dsa-<topic>-<short-title-slug>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"pattern": "", "pattern_chosen": "", "complexity_claimed": "", "complexity_actual": "", "brute_to_optimal": "", "verdict": "", "attempts": "", "tests_failed": "", "ai_hint_tier_max": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `pattern` | Technique that actually solves it (e.g. 'sliding-window/variable'). |
| `pattern_chosen` | Technique the user first attempted, if different. |
| `complexity_claimed` | User's stated time/space, e.g. 'O(n log n) / O(n)'. |
| `complexity_actual` | Actual complexity of their final solution. |
| `brute_to_optimal` | One line: how (or whether) they moved from brute force to the optimal idea. |
| `verdict` | Harness verdict of final submission: AC/WA/TLE/RE/SAN/CE. |
| `attempts` | Number of submissions before AC or give-up. |
| `tests_failed` | First failing case label (e.g. 'edge/single_negative.in'). |
| `ai_hint_tier_max` | Highest hint tier used (0-4). |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (the whole problem dir: statement.md, ref/brute/gen/edge/meta, plus the user's last solution).
