# Rubric — aidebug

Score the process and the result separately.

**Result (from the harness):** bugs fixed / total, regressions, test tampering, diff size vs reference.

**Process (from the transcript, all must-haves):**
- Reproduced first: ran the tests and read the failure before editing or prompting.
- Prompts carried the symptom, the evidence and a hypothesis; context was narrowed, not dumped.
- Each AI claim was verified (run, test, or code read) before it became an edit.
- One change at a time, re-running tests after each; diff close to the reference.
- Kept going after the first green public test: looked for the remaining bugs.

Nice-to-have: wrote a regression test, stated a root cause in one sentence, used bisect/logging/debugger deliberately.

## Outcome mapping
- **pass**: all bugs fixed (hidden tests green), no regression, no test tampering, within the time box, and at most one of F-AI-BLIND-TRUST / F-AI-NO-REPRO.
- **partial**: more than half of the bugs fixed, OR all fixed but over time, with regressions or a major process flaw.
- **fail**: half or fewer fixed, tests tampered with, or gave up.

Hint penalty: a tier ≥3 hint (skeleton/solution) caps the outcome at `partial`. Giving up = `fail`.
