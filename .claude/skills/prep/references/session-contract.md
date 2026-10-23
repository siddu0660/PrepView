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

## Review mode (spaced repetition)

Triggered by `--mode review` or "revise". Source of truth: `$MEM due <key>` (ladder 1 → 3 → 7 → 14 days; an item retires after 4 consecutive passes; items passed first time are never tracked).

1. Take up to `n` due refs (oldest due first). None due → say so, offer a normal session or the weakest `weak_tags` instead.
2. For each, load `items/<ref>` (`$MEM path <key>`). Never re-show the old answer or the user's old solution first.
3. Present a **variant**, not the identical item, so memorising cannot pass it: code domains change constraints/parameters and re-run the Verify gate; knowledge domains ask the same concept from a new angle; design domains change one requirement; quant changes the numbers and recomputes the answer with the script.
4. Grade normally and log the episode under the **original `item.ref`** (that is what advances or resets its stage); put the variant description in `x.variant`.
5. Debrief compares with the earlier attempt using the stored `flaws`/`remark`: fixed, persistent or new.

## Style
Terse. No praise padding. Accuracy over friendliness: if the user is wrong, say so with the counter-example.
