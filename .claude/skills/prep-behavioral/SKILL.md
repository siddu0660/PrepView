---
name: prep-behavioral
description: Behavioral & HR Rounds practice for /prep: behavioral, behavioural, star method, tell me about a time, leadership principles, conflict with. Invoked by the prep orchestrator via --behavioral, --hr, --bq.
---

# Behavioral & HR Rounds (`behavioral`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `behavioral` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init behavioral --default-level 2`, `MEM profile behavioral`, mode = `mock`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Behavioral interview rounds: STAR stories, competencies (ownership, conflict, failure, ambiguity, leadership, influence), 'tell me about yourself', motivation, questions for the interviewer.
**Out:** Technical correctness (other domains), salary negotiation scripts (separate domain if wanted).

Topics (taxonomy tags, see `references/taxonomy.md`): ownership, conflict, failure-learning, leadership, ambiguity, influence, deadline-pressure, mentoring, customer-focus, motivation, strengths-weaknesses, intro-pitch, questions-for-interviewer

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `mock` | n questions, optional competency → interviewer questions one at a time with realistic follow-ups, graded at the end |
| `story` | an experience the user describes → shape it into a STAR story: gaps flagged, questions to extract metrics; saved to the story bank |
| `drill` | one competency → a single question, rapid scoring, sharper rewrite of the weakest sentence |
| `review` | none → re-test saved stories against new questions to check they flex across competencies |

Default mode: `mock` · default difficulty: `2`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Simple prompts: tell me about yourself, why this company, a strength. |
| 2 | Standard STAR: a conflict, a deadline you met, a time you learned something. |
| 3 | Probing: failure with real consequences, disagreeing with a manager, ambiguity, with 2 follow-ups. |
| 4 | Senior-level: influence without authority, a decision with incomplete data, org-level impact, trade-offs between people and delivery. |
| 5 | Hostile/ambiguous interviewer: challenges your claims, asks 'what would you do differently?', probes ownership vs team credit. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `beh-<competency>-<short-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Behavioral specifics
`story` mode: ask at most 3 extraction questions at a time (what exactly did YOU do, what was the number, what would you change); then produce the STAR draft in the user's voice and `save-item` it as the story bank entry (item.ref `beh-<competency>-<slug>`). `mock`: one question, wait for the answer, one follow-up, move on.

## 5. Accuracy gates (hard — run before presenting anything)
**Kind: design.** Graded against a rubric, not intuition.
1. Before presenting, write the hidden rubric: requirements (functional + non-functional), key decisions with their trade-offs, failure modes, and where numbers are expected.
2. Every number you state or expect (QPS, storage, latency, memory) is computed with a script/arithmetic check, not recalled.
3. Accept any valid design; mark only violations of requirements, correctness bugs, or unjustified decisions. Do not grade on matching your own solution.
4. Each critique quotes the user's own words and says what to change; no generic advice.
5. Probe once: ask one follow-up that stress-tests their weakest decision (scale ×10, a node failure, a new requirement) and grade the reaction.
6. Never invent or embellish the user's experiences. Stories come only from the user; you coach structure, extract specifics, and rewrite their own words more sharply.
7. Do not 'grade' honesty away: if a claim sounds implausible, probe it as an interviewer would instead of silently accepting it.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path behavioral)` — outside the repo, never committed.
- **Read at start:** `MEM profile behavioral` (already loaded by orchestrator). In `review` mode also `MEM due behavioral` and `MEM tail behavioral 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild behavioral`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
