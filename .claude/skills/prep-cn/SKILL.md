---
name: prep-cn
description: Computer Networks practice for /prep: computer network, networking, tcp, udp, dns, http. Invoked by the prep orchestrator via --cn, --networks, --net.
---

# Computer Networks (`cn`)

Invoked by `/prep` after routing. Follow `../prep/references/session-contract.md` (loop + exact memory-write procedure) and `../prep/references/difficulty.md`.
`MEM` = `python3 ../prep/scripts/memory.py` · memory key = `cn` · inputs from orchestrator: `mode, difficulty, n, timed, text, profile`.
If invoked directly (no orchestrator), set it up yourself: `MEM init cn --default-level 2`, `MEM profile cn`, mode = `quiz`, difficulty = profile `recommended_level`.

## 1. Scope
**In:** Interview-level networking: OSI/TCP-IP layers, Ethernet/ARP, IP addressing/subnetting/CIDR, routing (RIP/OSPF/BGP basics), TCP (handshake, flow/congestion control, retransmission), UDP, DNS, HTTP/1.1-2-3, TLS, NAT/firewalls, sockets, troubleshooting a request end to end.
**Out:** Vendor CLI configuration, distributed-system design (prep-hld), cryptography proofs.

Topics (taxonomy tags, see `references/taxonomy.md`): osi-tcpip, ethernet-arp, ip-subnetting, routing, tcp-handshake-teardown, tcp-flow-congestion, udp-quic, dns, http-versions, tls, nat-firewall, sockets, delay-throughput-calcs, troubleshooting

## 2. Modes
Open-ended: if the user asks for a task not listed, do it with the same loop and log it with `mode` set to the closest listed mode and the real task in `item.title`.

| Mode | Input → Output |
|------|----------------|
| `quiz` | difficulty, optional topic, n → n keyed questions incl. calculation items verified by script |
| `explain` | protocol/concept → what problem it solves, packet-level mechanism, failure modes, 2 follow-ups |
| `review` | none or topic → spaced repetition of missed questions with fresh variants |
| `mock` | time box → oral interviewer incl. the classic 'what happens when you type a URL' deep-dive |

Default mode: `quiz` · default difficulty: `2`.

## 3. Difficulty ladder (domain anchors)
| Lvl | Anchor |
|-----|--------|
| 1 | Recall: layers of OSI, TCP vs UDP, what DNS does, what a MAC address is. |
| 2 | Mechanism: three-way handshake states, ARP flow, subnet mask basics, HTTP methods/status codes, what NAT rewrites. |
| 3 | Applied: subnetting/VLSM calc, TCP sequence/ack trace, delay (transmission+propagation) calc, CORS/cookies vs sessions, DNS resolution path with caching. |
| 4 | Deep: TCP congestion control (slow start, AIMD, fast retransmit), window/BDP throughput limits, TLS 1.3 handshake, HTTP/2 vs HTTP/3 (head-of-line blocking), BGP path selection. |
| 5 | Expert: debugging from a packet trace, bufferbloat, TCP CUBIC/BBR trade-offs, anycast/ECMP effects, MTU/fragmentation black holes. |

## 4. Session loop
Implements the shared contract: Generate → Verify → Present → Interact → Grade → Debrief → Remember.
- Item ref format: `cn-<topic>-<short-slug>` (stable slug; used for dedupe and review).
- Bias ~40% of items to `weak_tags` from the profile; probe the `watch_list` flaws; respect `n`.

### Quiz specifics
- Batch: default `n=5` questions per round (mock: 8 chained oral-style questions with follow-ups). Present all, numbered, with *confidence 1-3* requested per answer (1 guess, 2 fairly sure, 3 certain).
- Grade each against its key; a correct answer at confidence 1 is `partial` (lucky), a wrong answer at confidence 3 is the most important flaw (record the misconception).
- Debrief per question: key, 1-line why, the misconception it targets. Then 2-line pattern summary.
- Remember: **one episode per question** (append a JSON list in a single call), `item.ref` = `<domain>-<topic>-<slug>`, plus one `note` for the weakest cluster.
- Subnetting, delay, BDP and throughput items: compute the key with `python3 scripts/netcalc.py ...` (relative to this skill's directory); show the user the given values with explicit units and ask for units in the answer.


## 5. Accuracy gates (hard — run before presenting anything)
**Kind: knowledge.** Every item carries: question · answer key · one-line justification · source tag (textbook chapter, RFC, man page, paper).
1. Independent re-derivation: answer the question again in a separate pass without looking at the key; any mismatch → discard the item.
2. MCQ: exactly one defensible option; distractors are real misconceptions (record each in `x.misconception`), never absurd; no "all/none of the above".
3. Reject opinion-based, version-dependent (unless the version is stated) and pure-trivia items.
4. Explanations: separate what is certain from what you are less than certain about; never invent numbers, citations or API behaviour.
5. Grade open answers per key points (must-have vs nice-to-have), not wording.
6. Protocol facts (header fields, default timers, port numbers) must match the RFC or standard cited in the source tag; if the value is implementation-specific (e.g. initial congestion window, RTO min), name the OS/RFC or avoid the item.
7. Packet-trace items: write the trace out fully (seq, ack, flags, window) and re-simulate it step by step before presenting.

## 6. Grading
Rubric and outcome thresholds: `references/rubric.md`. Flaw codes: `references/taxonomy.md`.

## 7. Memory
Location: `$(MEM path cn)` — outside the repo, never committed.
- **Read at start:** `MEM profile cn` (already loaded by orchestrator). In `review` mode also `MEM due cn` and `MEM tail cn 5`.
- **Write at end (always):** `MEM save-item`, `MEM append`, `MEM note` exactly as in the session contract.
- **Episode schema + domain extension `x`:** `references/schema.md`.
- Never edit `log.jsonl` by hand; `profile.md` is derived and safe to rebuild with `MEM rebuild cn`.

## 8. Output format
Terse. Statement/question first, nothing else. Debrief ≤8 lines using the contract. Code in fenced blocks. No praise padding.
