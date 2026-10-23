# Routing rules (implemented in scripts/route.py)

1. Flags first. A flag may be a domain (`--dsa`), an alias (`--sd`, `--mm`) or a dotted path (`--quant.prob`).
2. A parent flag (`--quant`) resolves to a child by trigger score; if no clear child, ask.
3. Free text: each trigger phrase present adds `1 + words` points. Route only if top ≥ 2 and lead over #2 ≥ 2. Otherwise `status: ask`.
4. Mode words: quiz/mcq → quiz · mock/interview me → mock · review/revise → review · explain/clear/teach → explain · drill → drill · design → design · problem/give me a → problem. A mode the domain doesn't offer is dropped and the default is used.
5. Difficulty words: beginner=1 easy=2 medium=3 hard=4 expert/very hard=5; `-d N` overrides.
6. Ambiguity examples that MUST ask: "give me something", "practice", "design" (lld vs hld), "probability or DSA?".
7. Add triggers for a new domain only via `/prep-new`; keep phrases specific (≥1 distinctive word) to avoid collisions — `scripts/lint.py` flags collisions.
