# ADR-001: PrepView — Orchestrated, Memory-Backed Skill Set for Job Prep

**Status:** Accepted (decisions on language, roles, memory location resolved 2026-10-23)
**Date:** 2026-10-23
**Deciders:** Repo owner

## Context

Goal: one entry point (`/prep`) that serves SWE / quant / other interview prep. It must:

1. Route a request to the right domain skill, via explicit flag (`--dsa`, `--lld`) or inference from free text.
2. Run any task type at a set difficulty: new problem, quiz, concept clearing, mock round, review.
3. Let new domains be added cheaply from a single template, with a domain-specific memory draft included.
4. Persist per-domain memory: what was asked, flaws in the user's approach, workflow summary, short takeaways.
5. Be fast (small context, no needless fan-out) and accurate (verified problems, keyed answers, rubric grading).

Platform: Claude Code skills (`.claude/skills/<name>/SKILL.md`, progressive disclosure, Bash/Read/Write available).

## Decision

A **three-layer design**: Orchestrator → Domain skills (nestable) → Per-domain memory, all generated from one Template and one Scaffolder.

### 1. Repository layout

```
.claude/skills/
  prep/                         # ORCHESTRATOR (user-facing: /prep)
    SKILL.md                    # ≤120 lines: parse → route → delegate → persist
    registry.yaml               # single source of truth for routing (flags, aliases, triggers)
    references/
      routing.md                # tie-break + ambiguity rules
      difficulty.md             # shared 1–5 scale + adaptive rules
      session-contract.md       # the loop every domain must implement
  prep-new/                     # SCAFFOLDER (/prep-new <domain>): template → new domain
    SKILL.md
    template/                   # THE TEMPLATE
      SKILL.md.tpl
      memory/
        schema.md.tpl           # domain memory draft (see §4)
        profile.md.tpl
        notes.md.tpl
      references/
        taxonomy.md.tpl         # topic tags + flaw codes for this domain
        rubric.md.tpl           # grading rubric / answer-key format
  prep-dsa/                     # DOMAIN (leaf)
    SKILL.md
    references/ taxonomy.md rubric.md
  prep-lld/  prep-hld/  prep-os/  prep-db/  prep-net/  prep-behavioral/
  prep-quant/                   # DOMAIN (nested: has its own registry.yaml)
    SKILL.md
    registry.yaml               # probability, mental-math, brainteasers, stochastic, markets
    prob/ SKILL.md              # sub-skill, same template, own memory
    mental-math/ SKILL.md
~/.claude/prep-memory/          # USER DATA — NOT in the repo (override with $PREP_MEMORY_DIR)
  dsa/   { profile.md  log.jsonl  notes.md }
  quant/prob/ { ... }
```

The repo holds only skills, templates and memory **schemas** (`schema.md` lives with the skill under
`references/`). Actual memory is created lazily on first use in the user-level Claude directory, never
under the repo and never pushed to GitHub. Skills read/write it only through that resolved path.

**Durability caveat:** `~/.claude` persists on a local CLI/desktop install, but cloud sessions run in an
ephemeral container that is reclaimed after inactivity, so memory written there is lost. For durable
memory, run PrepView locally (or point `$PREP_MEMORY_DIR` at a persistent mount). Claude.ai's built-in
chat memory is not writable from skills, so it is not used.

### 2. Orchestrator flow

```
/prep [--<domain>[.<sub>]] [-d 1..5] [-n N] [--mode <task>] [free text]
  │
  ├─ 1 PARSE      flags win. Aliases from registry.yaml (--sd → hld, --os, --prob → quant.prob).
  ├─ 2 ROUTE      no flag → match free text against registry `triggers`.
  │                 score ≥ threshold, margin over #2 ≥ gap → proceed, state "Routing: dsa".
  │                 else → ONE question (top 3 candidates as options). Never guess silently.
  ├─ 3 LOAD       read ONLY: domain SKILL.md + <memory-dir>/<d>/profile.md (+ last 5 log lines).
  ├─ 4 RESOLVE    difficulty: explicit -d > profile.recommended_level > domain default (2).
  │               mode: explicit > inferred from text (quiz/new/explain/review/mock) > domain default.
  ├─ 5 DELEGATE   hand domain skill {domain, mode, difficulty, n, profile-summary}.
  └─ 6 CLOSE      domain skill writes memory (§4); orchestrator prints 3-line recap + next suggestion.
```

Nested domains: orchestrator resolves `quant.prob` by walking `registry.yaml` files; a parent `registry.yaml` only
lists its children. Depth is unbounded but each level only loads its own registry.

`registry.yaml` entry:

```yaml
- id: dsa
  skill: prep-dsa
  flags: [--dsa, --algo]
  triggers: [leetcode, array, graph, dp, two pointers, complexity, "give me a problem"]
  modes: [problem, quiz, explain, review, mock]
  default_mode: problem
  default_difficulty: 2
  memory: ${PREP_MEMORY_DIR:-~/.claude/prep-memory}/dsa
```

### 3. Template contract (what every domain skill contains)

`SKILL.md.tpl` sections, fixed order so the orchestrator and scaffolder can rely on them:

| # | Section | Content |
|---|---------|---------|
| 0 | Frontmatter | `name`, `description` (trigger phrases), `argument-hint` |
| 1 | Scope | what is / isn't in the domain |
| 2 | Modes | the task types, each with input → output shape (open-ended list; add freely) |
| 3 | Difficulty ladder | 1–5 anchored with concrete examples *for this domain* |
| 4 | Session loop | Generate → Verify → Present → Interact → Grade → Debrief → Remember |
| 5 | Accuracy gates | domain-specific hard checks before anything is shown (see below) |
| 6 | Grading rubric | scored dimensions + flaw codes → `references/rubric.md` |
| 7 | Memory | schema pointer, read rules, write rules (§4) |
| 8 | Output format | terse, spoiler-safe, hints in tiers |

Hints are tiered (nudge → pattern → skeleton → solution) and each tier used is logged.

**Accuracy gates (the "deadly accurate" part).** Models must not rely on recall for correctness:

- *Code-checkable* domains (DSA, quant calc): generate problem + reference solution + brute force + tests; run them with Bash; present only if reference == brute force on random tests. **Language is C++** (`g++ -std=c++20 -O2`, also compiled with `-fsanitize=address,undefined` for UB/OOB catches). User code is graded against the same harness (random + edge + max-size stress tests with a time limit for complexity), and compiler/sanitizer output is mapped to flaw codes (e.g. `F-OOB`, `F-INT-OVERFLOW`, `F-UNINIT`). Harness lives in `prep-dsa/harness/` (runner script + testlib-style generators); work happens in the scratchpad, not the repo.
- *Knowledge* domains (OS, DB, networking): every question carries an answer key, a one-line justification and a source tag; a second-pass "adversarial check" re-derives the answer independently and the item is dropped if the two disagree. No ambiguous or opinion-based MCQs.
- *Design* domains (LLD, HLD): graded against a rubric of requirements, trade-offs, failure modes and numbers; feedback must cite the user's own words.
- Always: the difficulty claimed must match the ladder anchors; unseen = not in `log.jsonl` (dedupe by problem/question id).

**Speed.** Progressive disclosure (orchestrator ≈ registry + one domain loaded); profile file capped ~40 lines; log read by tail only; no subagents by default (only `--mock` or batch generation may fan out); single routing question at most.

### 4. Memory design

Three files per domain, split by access pattern:

| File | Role | Write | Read |
|------|------|-------|------|
| `log.jsonl` | Append-only episodes — raw truth | every session | tail / dedupe lookups |
| `profile.md` | Derived aggregate: level, weak/strong tags, recurring flaws, workflow habits | rewritten at session close | **always** (small) |
| `notes.md` | Curated short remarks / "take these with you" | append ≤3 lines per session; compact when >30 | on `--mode review` |

**Common envelope** (all domains):

```json
{"id":"2026-10-23T14:02Z-dsa-017","ts":"...","domain":"dsa","mode":"problem",
 "difficulty":3,"item":{"ref":"...","title":"...","tags":["sliding-window"]},
 "outcome":"partial","time_s":1420,"hints":[1,2],
 "flaws":["F-EDGE-EMPTY","F-COMPLEXITY-NOT-ANALYSED"],
 "workflow":"jumped to code before examples; fixed after test 2",
 "remark":"Write 3 edge cases before coding.",
 "x":{ }}
```

`x` is the **domain extension block**, defined by the template's `memory/schema.md.tpl` — this is the "draft memory for the domain" produced at creation:

| Domain | `x` fields |
|--------|-----------|
| dsa | `pattern`, `complexity_claimed/actual`, `brute_to_optimal_path`, `lang`, `tests_failed` |
| quiz (os/db/net) | `qid`, `topic`, `misconception`, `confidence`(1–3) |
| lld | `entities`, `patterns_used`, `smells`, `extensibility_probe_result` |
| hld | `requirements_missed`, `numbers_estimated`, `bottleneck_identified`, `tradeoffs_named` |
| quant | `method`, `calc_errors`, `time_vs_target`, `distribution_traps` |

**Profile update rule (deterministic):** `recommended_level` = last-5 weighted success; ±1 only after 2 consecutive clean outcomes at the level (up) or 2 failures (down). Flaw codes counted over a rolling 20 → top 3 become "Watch list" the domain skill actively probes next session. Tag with the lowest success rate gets 40% of generated items.

**Memory invariants:** never delete `log.jsonl`; `profile.md` is always reconstructible from it; a failed write must not block the session (warn once).

### 5. Scaffolder flow (`/prep-new <domain>`)

1. Ask ≤4 questions: flag/aliases, task types, code-checkable vs knowledge vs design, difficulty anchors.
2. Instantiate `template/` → `.claude/skills/prep-<domain>/` with taxonomy + flaw codes seeded.
3. Write `.claude/skills/prep-<domain>/references/schema.md` (the domain's `x` block) in the repo; the empty `profile.md`/`log.jsonl`/`notes.md` are created in the user-level memory dir on first session, not in the repo.
4. Append an entry to `registry.yaml` (or a parent registry for nested).
5. Run a lint: required sections present, registry id unique, flag not colliding, schema valid JSON example.

## Options Considered

### Option A: One monolithic "prep" skill
| Dimension | Assessment |
|-----------|------------|
| Complexity | Low initially, High over time |
| Scalability | Poor — context bloat per domain added |
| Memory | Entangled |

**Pros:** trivial to start. **Cons:** slow (loads everything), fragile edits, no per-domain accuracy gates.

### Option B: Flat independent skills, rely on description auto-triggering
| Dimension | Assessment |
|-----------|------------|
| Complexity | Low |
| Scalability | Good |
| Routing reliability | Medium — implicit, no `--flag`, collisions |

**Pros:** idiomatic. **Cons:** no deterministic flags, no shared difficulty/memory contract, template drift.

### Option C (chosen): Orchestrator + registry + template + per-domain memory
| Dimension | Assessment |
|-----------|------------|
| Complexity | Medium (one-time) |
| Scalability | High — new domain = scaffolder run |
| Speed | High — progressive disclosure |
| Accuracy | High — per-domain gates |

**Pros:** deterministic flags + inference fallback, uniform contract, nestable. **Cons:** more files; registry must stay in sync (mitigated by scaffolder + lint).

### Memory sub-decision
- Single shared memory file — rejected: no schema fit across domains.
- SQLite — rejected for v1: opaque to the user, tooling overhead.
- **Per-domain md + jsonl — chosen:** human-readable, diffable, greppable, zero dependencies.

## Trade-off Analysis

- **Flags vs inference:** flags are zero-ambiguity; inference is convenience. Flags always win, inference never guesses silently.
- **Verification vs speed:** running reference+brute-force adds seconds for DSA/quant but removes wrong problems — the dominant failure mode of LLM-generated practice. Knowledge quizzes use a cheaper double-derivation check.
- **Derived profile vs raw log only:** the profile costs a write per session but keeps the per-session read tiny.

## Consequences

- Easier: adding domains, tuning difficulty globally, auditing progress (`git log` on memory).
- Harder: keeping registry/triggers/flag names collision-free as domains grow (lint covers it).
- Revisit: spaced repetition scheduling (resurface failed items by due date) once `log.jsonl` has volume; cross-domain "readiness dashboard"; whether memory should be a private repo.

## Action Items (build order)

1. [ ] `prep/SKILL.md`, `registry.yaml`, `references/{routing,difficulty,session-contract}.md`
2. [ ] `prep-new/template/*` (the template + memory drafts) and `prep-new/SKILL.md` scaffolder with lint
3. [ ] Reference domain #1: `prep-dsa` (hardest, exercises the verification harness + all memory fields)
4. [ ] Domain #2 as a quiz type: `prep-os` (validates the knowledge-domain gate)
5. [ ] Domain #3 nested: `prep-quant` → `prob`, `mental-math` (validates nested routing)
6. [ ] `prep-lld`, `prep-hld`, `prep-behavioral` via scaffolder (validates the template)
7. [ ] Eval set: 20 routing prompts (incl. ambiguous) + 10 seeded wrong problems the verifier must reject
8. [ ] Spaced-repetition mode using `log.jsonl`

## Open Questions

None blocking. Resolved:

1. DSA language: **C++** (harness above).
2. Roles: **both SWE and quant** — build order keeps `prep-quant` (prob, mental-math) alongside the SWE domains rather than deferring it; quant gets timed modes (`--timed`) since speed is scored there.
3. Memory: **outside the repo**, user-level Claude directory (see Layout and durability caveat). Repo = skills + schemas only.

Still open: whether you want a persistent location for cloud sessions (e.g. mounted volume) or are fine running locally.
