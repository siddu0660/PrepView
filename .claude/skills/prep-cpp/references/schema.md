# Memory schema — cpp

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "cpp", "mode*": "quiz",
  "difficulty*": 1,
  "item*": {"ref*": "cpp-<topic>-<short-slug>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"qid": "", "topic": "", "format": "", "misconception": "", "confidence": "", "key_points_hit": "", "key_points_total": "", "source": "", "std_version": "", "verdict_tool": "", "bug_found": "", "fix_verified": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `qid` | Stable question id (matches item.ref). |
| `topic` | Primary taxonomy tag. |
| `format` | mcq | short | predict | debug | compile | oral |
| `misconception` | The specific wrong belief revealed (empty if correct). |
| `confidence` | 1-3 self-reported. |
| `key_points_hit` | Number of must-have points matched. |
| `key_points_total` | Number of must-have points in the key. |
| `source` | Source tag of the key. |
| `std_version` | Standard the item targets (11/14/17/20). |
| `verdict_tool` | OK | UB | COMPILE_ERROR from scripts/cppcheck.py. |
| `bug_found` | debug mode: true/false and which bug. |
| `fix_verified` | debug mode: fix compiled and ran clean under sanitizers. |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (question/snippet, key, and cppcheck output).
