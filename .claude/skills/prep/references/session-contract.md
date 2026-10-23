# Session contract — every domain skill implements this loop

```
Generate → Verify → Present → Interact → Grade → Debrief → Remember
```

| Step | Rule |
|------|------|
| Generate | Respect `difficulty`, `mode`, `n`. Skip any `item.ref` where `$MEM seen <key> <ref>` exits 0 (unless the mode is review). Bias ~40% to `weak_tags`, and address `watch_list` flaws. In review mode start from `$MEM due <key>`. |
| Verify | Run the domain's accuracy gate (§5 of its SKILL.md). An item that fails the gate is discarded silently and regenerated (max 3 tries, then tell the user). |
| Present | Statement only. No answer, no hint, no complexity. Show expected time if `--timed`. |
| Interact | Hints are tiered: 1 nudge → 2 pattern → 3 skeleton → 4 solution. Log each tier used in `hints: [1,2]`. Say nothing true-but-unasked. |
| Grade | Use `references/rubric.md` of the domain. Outcome ∈ pass / partial / fail. `pass` requires correctness AND no tier ≥3 hint. |
| Debrief | ≤8 lines: verdict, what was good, top 1–3 flaws with codes, the key insight, one next step. Cite the user's own words/code. |
| Remember | Always, even on give-up (outcome fail). See below. |

## Remember (exact procedure)

1. `$MEM save-item <key> <ref> <path>` — store the statement/key (and harness dir for code domains) so the item can be revisited.
2. Pipe ONE episode JSON to `$MEM append <key>`:

```json
{"ts":"<UTC ISO, e.g. 2026-10-23T14:02:00Z>","domain":"<key>","mode":"problem",
 "difficulty":3,
 "item":{"ref":"<stable-slug>","title":"...","tags":["sliding-window"]},
 "outcome":"pass|partial|fail","time_s":1420,"hints":[1,2],
 "flaws":["F-EDGE-EMPTY"],
 "workflow":"one sentence on HOW they worked (order of steps, habits)",
 "remark":"one actionable sentence to carry forward",
 "x":{ }}
```

   `x` follows the domain's `references/schema.md`. Flaw codes come from the domain's `references/taxonomy.md`; propose a new code only if none fits (format `F-<AREA>-<WHAT>`), and add it to taxonomy.md.
3. `$MEM note <key> "<≤140-char takeaway>"` — at most 3 per session, only things worth re-reading.
4. A non-zero exit from `$MEM append` → print the stderr once, continue. Never retry in a loop.

## Style
Terse. No praise padding. Accuracy over friendliness: if the user is wrong, say so with the counter-example.
