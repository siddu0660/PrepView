---
name: {{skill_name}}
description: {{description}}
---

# {{title}} (`{{memory_key}}`)

Invoked by `/prep` after routing. Follow `{{prep_rel}}/references/session-contract.md` (loop + exact memory-write procedure) and `{{prep_rel}}/references/difficulty.md`.
`MEM` = `python3 {{mem_cmd}}` · memory key = `{{memory_key}}` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.

## 1. Scope
**In:** {{scope_in}}
**Out:** {{scope_out}}

Topics (taxonomy tags, see `references/taxonomy.md`): {{topics_csv}}

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
{{modes_table}}

Default mode: `{{default_mode}}` · default difficulty: `{{default_difficulty}}`.{{timed_note}}

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
{{ladder_table}}

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `{{item_ref_format}}` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.
{{loop_extra}}

## 5. Accuracy gates (hard — run before presenting anything)
{{gate_block}}

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path {{memory_key}})` — outside the repo, never committed.
- **Read at start:** `MEM profile {{memory_key}}` (already loaded by orchestrator). In `review` mode also `MEM due {{memory_key}}` and `MEM tail {{memory_key}} 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild {{memory_key}}`.

## 8. Output format
{{output_format}}
