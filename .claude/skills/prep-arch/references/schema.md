# Memory schema — arch

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "arch", "mode*": "quiz",
  "difficulty*": 1,
  "item*": {"ref*": "arch-<topic>-<short-slug>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"qid": "", "topic": "", "format": "", "misconception": "", "confidence": "", "key_points_hit": "", "key_points_total": "", "source": "", "calc_verified": "", "level_of_stack": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `qid` | Stable question id (matches item.ref). |
| `topic` | Primary taxonomy tag. |
| `format` | mcq | short | trace | calc | oral |
| `misconception` | The specific wrong belief revealed (empty if correct). |
| `confidence` | 1-3 self-reported. |
| `key_points_hit` | Number of must-have points matched. |
| `key_points_total` | Number of must-have points in the key. |
| `source` | Source tag of the key. |
| `calc_verified` | true/false: key computed with scripts/archcalc.py. |
| `level_of_stack` | ISA | microarchitecture | memory-system | multicore. |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (question text, key, justification, archcalc commands used).
