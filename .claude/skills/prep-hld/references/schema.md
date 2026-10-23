# Memory schema — hld

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "hld", "mode*": "design",
  "difficulty*": 1,
  "item*": {"ref*": "hld-<system>-<variant>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"system": "", "requirements_missed": "", "numbers_estimated": "", "estimation_error_pct": "", "bottleneck_identified": "", "tradeoffs_named": "", "deep_dive_topic": "", "stress_probe": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `system` | What was designed. |
| `requirements_missed` | Requirements (esp. non-functional) the user never raised. |
| `numbers_estimated` | true/false |
| `estimation_error_pct` | Largest estimation error vs your verified numbers. |
| `bottleneck_identified` | true/false plus which. |
| `tradeoffs_named` | Count of explicit trade-offs. |
| `deep_dive_topic` | Component drilled into and outcome. |
| `stress_probe` | The probe posed (10x scale, node loss, etc.) and pass/fail. |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (prompt, hidden rubric, verified numbers, reference sketch).
