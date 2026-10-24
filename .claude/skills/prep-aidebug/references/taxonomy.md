# Taxonomy — aidebug

## Topic tags
- `repro-first`
- `context-framing`
- `hypothesis-prompting`
- `localisation-bisect`
- `reading-unfamiliar-code`
- `verifying-ai-output`
- `test-driven-fix`
- `minimal-diff`
- `root-cause-vs-symptom`
- `regression-guarding`
- `tooling-logging-debugger`
- `time-management`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-AI-NO-REPRO` | Asked the AI or edited code before reproducing the failure and reading the test output. |
| `F-AI-VAGUE-PROMPT` | Prompt lacked the failing test, error text, expected vs actual, or relevant code; got a generic answer. |
| `F-AI-CONTEXT-DUMP` | Pasted the whole repo or logs without narrowing; noise drowned the signal. |
| `F-AI-NO-HYPOTHESIS` | Changed things without a stated, falsifiable hypothesis about the cause. |
| `F-AI-BLIND-TRUST` | Applied or believed an AI suggestion without verifying it with a test, run or code read (including falling for a planted wrong claim). |
| `F-AI-SYMPTOM-FIX` | Patched the symptom (special-case, try/except, test-shaped hack) instead of the root cause. |
| `F-AI-SHOTGUN-EDIT` | Made several unrelated edits at once so the effect of each was unknowable. |
| `F-AI-OVERSCOPE` | Rewrote or refactored far beyond the bug; diff much larger than needed. |
| `F-AI-REGRESSION` | Fix broke a previously passing test or behaviour. |
| `F-AI-TEST-TAMPER` | Edited or weakened tests to make them pass. |
| `F-AI-NO-VERIFY` | Declared done without rerunning the test suite after the last change. |
| `F-AI-STOPPED-EARLY` | Fixed some bugs and stopped; remaining hidden failures were never searched for. |
| `F-AI-TIME-MISMANAGEMENT` | Spent most of the time box on one dead end or on reading before running anything. |
