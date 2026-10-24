# Memory schema — aidebug

Episode envelope (validated by `memory.py append`; fields marked * are required):

```json
{
  "ts*": "UTC ISO-8601", "domain*": "aidebug", "mode*": "debug",
  "difficulty*": 1,
  "item*": {"ref*": "aidebug-<bugclass>-<short-repo-slug>", "title": "", "tags": []},
  "outcome*": "pass | partial | fail",
  "time_s": 0, "hints": [],
  "flaws*": [],
  "workflow": "how the user worked, one sentence",
  "remark*": "one actionable sentence",
  "x": {"bugs_total": "", "bugs_fixed": "", "tests_failed_first_run": "", "first_repro_s": "", "ai_prompts": "", "prompt_quality": "", "ai_trap_outcome": "", "techniques_used": "", "techniques_new": "", "strategy": "", "diff_lines": "", "reference_diff_lines": "", "regressions": "", "time_s_to_first_fix": "", "variant": ""}
}
```

## Domain extension block `x`
| Field | Meaning |
|-------|---------|
| `bugs_total` | Number of seeded bugs in the repo. |
| `bugs_fixed` | Number fixed at the final submission. |
| `tests_failed_first_run` | How many public tests failed on the first run, and whether the user ran them before editing. |
| `first_repro_s` | Seconds until the user first reproduced the failure. |
| `ai_prompts` | Number of times the user consulted the AI helper. |
| `prompt_quality` | 1-3: 1 vague, 2 has the symptom, 3 has the symptom, a hypothesis and the minimal context. |
| `ai_trap_outcome` | caught | fell | not-triggered | not-applicable (planted wrong AI claim). |
| `techniques_used` | Technique names the user actually applied (matches the playbook). |
| `techniques_new` | Techniques or methodologies new to the playbook this session. |
| `strategy` | One sentence: order of steps the user followed. |
| `diff_lines` | Changed lines in the user's fix. |
| `reference_diff_lines` | Changed lines in the reference fix, for the minimal-diff comparison. |
| `regressions` | Public or hidden tests that passed before and failed after the user's change. |
| `time_s_to_first_fix` | Seconds until the first bug was fixed. |
| `variant` | Review mode only: how the repo differs from the original. |

## Derived files
- `profile.md` (≤40 lines): recommended_level, last-5 success + hints, weak/strong tags, rolling-20 flaw watch list, last 3 workflow lines.
- `notes.md` (≤30 lines): short takeaways, newest kept.
- `items/<ref>/`: stored material for review and spaced repetition (the whole repo dir: repo/ (buggy), fixed/ (reference), tests_public/, tests_hidden/, meta.json, plus the user's final tree).
