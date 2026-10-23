# Taxonomy — cn

## Topic tags
- `osi-tcpip`
- `ethernet-arp`
- `ip-subnetting`
- `routing`
- `tcp-handshake-teardown`
- `tcp-flow-congestion`
- `udp-quic`
- `dns`
- `http-versions`
- `tls`
- `nat-firewall`
- `sockets`
- `delay-throughput-calcs`
- `troubleshooting`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-CONCEPT-CONFUSION` | Mixed up two related concepts. |
| `F-DEF-WRONG` | Incorrect or imprecise definition. |
| `F-CALC-ERROR` | Arithmetic or formula error in a calculation. |
| `F-TRADEOFF-MISSING` | Gave a mechanism without its cost/benefit trade-off. |
| `F-OVERCONFIDENT` | Wrong at confidence 3. |
| `F-LUCKY-GUESS` | Right at confidence 1 (unreliable knowledge). |
| `F-SCOPE-SHALLOW` | Right headline, missed the key mechanism when asked to go deeper. |
| `F-LAYER-CONFUSION` | Placed a protocol/function at the wrong layer. |
| `F-SUBNET-ERROR` | Subnetting/CIDR/VLSM mistake (verified by netcalc). |
| `F-TCP-STATE-ERROR` | Wrong TCP state/sequence/ack/window reasoning. |
| `F-CONGESTION-CONFUSION` | Confused flow control with congestion control or misdescribed AIMD/slow start. |
| `F-DELAY-UNITS` | Bits vs bytes or unit mismatch in delay/throughput calculation. |
| `F-DNS-PATH-ERROR` | Wrong resolution path (recursive vs iterative, caching, authoritative). |
| `F-TLS-HANDSHAKE-ERROR` | Wrong handshake order, key exchange or certificate role. |
| `F-HTTP-VERSION-CONFUSION` | Attributed a feature to the wrong HTTP version. |
| `F-TRACE-ERROR` | Misread a packet trace or sequence diagram. |
