# Memory schema — {{memory_key}}

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "{{memory_key}}", "mode*": "{{default_mode}}",
  "difficulty*": 1,
  "item*": {"ref*": "{{item_ref_format}}", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {{x_example}}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
{{x_table}}

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition ({{items_note}}).
