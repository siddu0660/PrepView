# Shared difficulty scale (1–5)

Each domain anchors this scale with concrete examples in its own SKILL.md (§3). Generic meaning:

| Level | Meaning | Expected solve rate for target user |
|-------|---------|--------------------------------------|
| 1 | Warm-up / recall. One idea, no traps. | ≥90% |
| 2 | Standard screen-level. One technique, one edge case. | ~75% |
| 3 | On-site medium. Two ideas combined or a real trap. | ~55% |
| 4 | Strong on-site / top-firm. Non-obvious insight or heavy trade-offs. | ~35% |
| 5 | Elite. Research-flavoured, multi-insight, or tight constraints. | ≤20% |

## Selection order
explicit `-d`/words (`easy`=2, `medium`=3, `hard`=4, `expert`=5, `beginner`=1) > `recommended_level` in profile > domain `default_difficulty`.

## Adaptation (computed in `scripts/memory.py`, never by feel)
- +1 level after 2 consecutive clean passes (pass with ≤1 hint) at or above current level.
- −1 level after 2 consecutive failures at or below current level.
- Within a session, if the first item is solved in under a third of the expected time with no hints, the next item may go +1 (not persisted until logged).
- Weakest tag in `weak_tags` receives ~40% of generated items; the rest are spread over untouched topics (exploration) so weak spots are not over-fitted.

## Calibration rule
Before presenting an item, the domain skill states internally which anchor it resembles. If it cannot name one, regenerate. Never label an item with a level it does not match.
