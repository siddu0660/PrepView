# Memory schema — behavioral

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "behavioral", "mode*": "mock",
  "difficulty*": 1,
  "item*": {"ref*": "beh-<competency>-<short-slug>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"competency": "", "story_ref": "", "star_complete": "", "quantified": "", "i_vs_we": "", "length_s": "", "followup_handling": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `competency` | Primary competency tested. |
| `story_ref` | Story-bank id of the story used. |
| `star_complete` | Which of S/T/A/R were present. |
| `quantified` | true/false: a metric in the result. |
| `i_vs_we` | Rough ratio or 'clear' / 'unclear' personal ownership. |
| `length_s` | Approx spoken length (word count / 2.5). |
| `followup_handling` | Held / wobbled / defensive. |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (the user's story text (the story bank) and the rewritten version).
