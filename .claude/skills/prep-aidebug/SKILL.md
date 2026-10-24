---
name: prep-aidebug
description: AI-assisted code comprehension and debugging practice for /prep: debug a seeded-bug codebase with an AI helper under a time box, learn techniques (repro-first, hypothesis prompting, bisecting, verifying AI output), and keep a playbook of techniques. Invoked by the prep orchestrator via --aidebug, --ai, --comprehension.
---

# AI-Assisted Code Comprehension & Debugging (`aidebug`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `aidebug` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init aidebug --default-level 2`, `MEM profile aidebug`, mode = `debug`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** The skill of fixing unfamiliar code fast and correctly while using an AI assistant: framing context, hypothesis-driven prompting, reproducing first, localising (bisect, tracing, logging), reading unfamiliar code, verifying and critiquing AI suggestions, minimal test-driven fixes, regression guarding, time management; runnable Python codebases with seeded bugs.
**Out:** Algorithm puzzles (prep-dsa), building features from scratch, model/prompt-engineering theory, non-debugging code review style, languages other than Python for the practice repos.

Topics (taxonomy tags, see `references/taxonomy.md`): repro-first, context-framing, hypothesis-prompting, localisation-bisect, reading-unfamiliar-code, verifying-ai-output, test-driven-fix, minimal-diff, root-cause-vs-symptom, regression-guarding, tooling-logging-debugger, time-management

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `debug` | difficulty, optional topic, time box → one verified runnable repo with seeded bugs; fix it in the time box using the AI helper; hidden tests grade it |
| `learn` | technique name or weakest technique → short lesson (when/why/how, anti-pattern) plus a 5-minute drill on a tiny repo that forces that technique |
| `critique` | difficulty, optional topic → an AI-style diagnosis or patch for a repo, partly wrong; you decide what to trust and prove it with tests |
| `review` | none or technique → spaced repetition: a fresh repo for techniques or bug classes you missed |
| `mock` | time box, default 45m → interview simulation: terse interviewer, AI helper allowed, no hints, process and result both scored |

Default mode: `debug` · default difficulty: `2`. `--timed`: enforce the expected time per item and log `time_s`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | One file, one bug, a failing test names it: off-by-one, wrong operator, swapped arguments. 15 min. |
| 2 | 3-5 files, one bug whose symptom is one call away from the cause: wrong unit, bad default, missed None case. 20 min. |
| 3 | 6-8 files, two independent bugs, misleading symptoms: mutable default argument, aliasing, stale cache, sort stability. The helper may be wrong. 30 min. |
| 4 | Multi-module, three bugs where one masks another: timezone/rounding, encoding, cache invalidation, ordering assumptions, retry/idempotency logic. 40 min. |
| 5 | Realistic service, 10+ files, four interacting bugs plus a suspicious-looking but correct red herring and a plausible wrong AI claim; a naive fix breaks hidden tests. 50 min. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `aidebug-<bugclass>-<short-repo-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### aidebug specifics
All paths relative to this skill's directory. Work in the scratchpad: `P=<scratchpad>/aidebug/<ref>`. `MEM` as above; `PB` = `python3 scripts/playbook.py` (the technique ledger, see below).

**Technique ledger (the point of this skill).** `PB` keeps `playbook.md` in the memory dir (`$(MEM path aidebug)/playbook.md`, never capped): every technique or methodology the user learned or invented, with a name, a one-line how/when, the evidence (item ref + date), and status `taught` / `tried` / `owned` (owned = used correctly unprompted in 2 sessions). Before any session: `PB show` (what they already own; do not re-teach it). At Remember: `PB add "<name>" --how "<one line>" --when "<trigger>" --ref <item ref> --status taught|tried|owned [--origin user|skill]`; `--origin user` for something the user invented or adapted; re-adding a name updates it and its status instead of duplicating. `PB catalog` lists the curated techniques in `references/techniques.md` that are not yet in the playbook.

**Generate (debug/mock/review)** — write `$P/{repo/,fixed/,tests_public/,tests_hidden/,meta.json}` per `harness/judge.py` docstring: a small realistic Python app (inventory, billing, rate limiter, scheduler, parser, cache layer...) with clear module boundaries, a `README.md` of 5-10 lines, and a `run_tests.sh`-free layout (`python3 -m unittest`). Seed bugs by editing a correct tree (`fixed/`) into `repo/`; record every bug in `meta.json`. Level = number of bugs, file count, how far the symptom is from the cause, masking, red herrings, traps (see ladder).
**Verify** — `python3 harness/judge.py verify $P`. Exit 0 required; on failure read `stage`/`detail`, fix, retry (max 3), else tell the user and pick another repo.
**Present** — copy `repo/` and `tests_public/` to `<workdir>/aidebug-work/` (the user's working tree; tell them the path), print the README, the test command (`python3 -m unittest discover -s tests_public -v`, run from that folder), the time box (L1 15m, L2 20m, L3 30m, L4 40m, L5 50m; `mock` as given), the rules, and that `/prep` can be asked as the AI helper. Never show `fixed/`, `tests_hidden/` or `meta.json`.
**Interact — AI helper protocol.** The user may ask the helper anything, prefixed `ask:` (or in plain words). Log each consultation (time, prompt summary, quality 1-3). Answer like a competent but fallible coding assistant: use only what was actually pasted or described plus what the helper can read in the working tree when asked; give hypotheses, not the fix, unless the user explicitly asks for a patch. At level 3+ the helper may deliver the planted trap from `meta.json` when the user asks the relevant question; otherwise it stays accurate. Never reveal hidden tests, `meta.json` or the reference. If asked to just fix it, comply but tag the item with the F-AI-BLIND-TRUST risk and make the user verify. Hints use the shared tiers (1 nudge, 2 pattern/where to look, 3 skeleton, 4 patch) and cost outcome as the rubric says.
**Submit** — when the user says done (or time ends): `python3 harness/judge.py judge $P <workdir>/aidebug-work` returns per-bug status, public/hidden results, regressions, test tampering, diff size, flaws. Report counts and the first failing hidden test name plus its message; do NOT reveal the reference.
**Debrief** — per bug: root cause, the technique that exposes it, whether the user got it. Reveal the trap and how it could have been caught. Show diff vs reference. Map process flaws from the transcript to taxonomy codes and `x` fields.
**Remember** — `save-item` the whole `$P` (not `__pycache__`), `append` one episode with `x`, then ledger updates via `PB add` for every technique used, taught or invented (one call each), and at most 3 `MEM note` lines.

**learn mode** — pick the user's weakest technique (profile tags, else the first not in the playbook per `PB catalog`). Teach in ≤12 lines from `references/techniques.md`: when to use, how, an anti-pattern, an example prompt (bad vs good). Then a 5-minute drill on a tiny verified repo (level 1-2) that is only fixable efficiently using that technique. Record it as `--status taught`; it becomes `tried` after a correct use, `owned` after correct unprompted use in 2 sessions.
**critique mode** — present a repo, a failing symptom and an AI-written diagnosis plus patch where some claims are false (kept in `meta.json`). The user must decide which claims to accept and prove each verdict by running something. Graded on claims correctly accepted/rejected with evidence, not on speed.
**mock mode** — no hints, interviewer tone, helper allowed but not coached, ask 'walk me through your approach' at the start and 'what would you do differently' at the end; both score process and result.

## 5. Accuracy gates (hard — run before presenting anything)
**Kind: code-checkable.** Nothing is shown until it is machine-verified.
1. Author: statement, reference solution, an *independent* brute force (different algorithm), input generator, constraints.
2. Execute in the scratchpad (never the repo): reference must equal brute force on ≥200 random small cases plus hand-written edge cases (empty/min/max, duplicates, negatives, overflow range).
3. Difficulty anchor: the intended solution meets the limit at max constraints and the brute force does **not**; otherwise raise constraints or regenerate.
4. Grade user answers by **executing** them on the same harness — never by reading and judging.
5. Reject ambiguity: input format, constraints, tie-breaks and output format are all stated.
6. Harness is mandatory: `python3 harness/judge.py verify <dir>` must exit 0 before the repo is shown. It proves, with the Python stdlib only: the buggy tree fails the public and hidden tests; the reference tree passes everything; each seeded bug, applied alone to the fixed tree, makes at least one hidden test fail; and no hidden test fails for a bug that is not listed. `python3 harness/judge.py selftest` proves the harness itself.
7. Seeded bugs must be realistic, one root cause each, and described in `meta.json` as a patch (file, buggy snippet, fixed snippet, bug class, technique that exposes it). Public tests must expose at least one bug; hidden tests must cover all of them plus regression behaviour.
8. Planted AI traps (levels 3+) are fixed in `meta.json` in advance: a plausible claim, why it is wrong, and the test that proves it. The user is told up front that the helper can be wrong; the trap is revealed in the debrief, never earlier.
9. Dedupe: skip any `item.ref` already in memory (`MEM seen aidebug <ref>`) unless in review mode; refs follow `aidebug-<bugclass>-<slug>`.
10. Ground truth for every claim the helper makes comes from running the code, not from reading it.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path aidebug)` — outside the repo, never committed.
- **Read at start:** `MEM profile aidebug` (already loaded by orchestrator). In `review` mode also `MEM due aidebug` and `MEM tail aidebug 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild aidebug`.

## 8. Output format
Terse. Repo path and rules first, nothing else. The helper answers briefly and says what it is unsure about. Debrief ≤10 lines. Code in fenced blocks. No praise padding.
