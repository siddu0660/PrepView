#!/usr/bin/env python3
"""Computer-architecture calculator for prep-arch answer keys (stdlib). Never compute these by hand.

  archcalc.py amat --hit-s T --miss-rate M --penalty-s P [--l2-miss-rate M2 --l2-penalty-s P2]
  archcalc.py cache-addr --addr A --size-bytes S --block-bytes B --ways W [--addr-bits 32]   (W=0: fully assoc)
  archcalc.py cpi --base-cpi C --mix "frac:cpi,frac:cpi,..." [--freq-hz F --instr N]
  archcalc.py amdahl --p P --s S            speedup when fraction P is sped up by S
  archcalc.py pipeline --stages K --instr N --cycle-s T [--stall-cycles X]   time, speedup vs unpipelined
  archcalc.py branch --freq F --mispredict M --penalty C                      extra CPI from mispredictions
"""
import json, math, sys


def o(a, k, d=None):
    return float(a[a.index(k) + 1]) if k in a else d


def main(a):
    if not a:
        print(__doc__); return 2
    c = a[0]
    if c == "amat":
        l2m = o(a, "--l2-miss-rate")
        out = {"amat_s": o(a, "--hit-s") + o(a, "--miss-rate") * (o(a, "--penalty-s") + (l2m * o(a, "--l2-penalty-s") if l2m is not None else 0))}
    elif c == "cache-addr":
        s, b, w, bits = int(o(a, "--size-bytes")), int(o(a, "--block-bytes")), int(o(a, "--ways")), int(o(a, "--addr-bits", 32))
        blocks = s // b; sets = 1 if w == 0 else blocks // w; off = int(math.log2(b)); idx = int(math.log2(sets)) if sets > 1 else 0
        addr = int(a[a.index("--addr") + 1], 0)
        out = {"sets": sets, "offset_bits": off, "index_bits": idx, "tag_bits": bits - off - idx,
               "offset": addr & (b - 1), "index": (addr >> off) & (sets - 1), "tag": addr >> (off + idx)}
    elif c == "cpi":
        mix = [tuple(map(float, x.split(":"))) for x in a[a.index("--mix") + 1].split(",")]
        cpi = sum(f * k for f, k in mix); out = {"cpi": cpi, "fractions_sum": sum(f for f, _ in mix)}
        if o(a, "--freq-hz") and o(a, "--instr"):
            out["time_s"] = o(a, "--instr") * cpi / o(a, "--freq-hz")
    elif c == "amdahl":
        p, s = o(a, "--p"), o(a, "--s"); out = {"speedup": 1 / ((1 - p) + p / s), "limit_as_s_inf": 1 / (1 - p)}
    elif c == "pipeline":
        k, n, t, st = o(a, "--stages"), o(a, "--instr"), o(a, "--cycle-s"), o(a, "--stall-cycles", 0)
        piped = (k + n - 1 + st) * t; un = n * k * t; out = {"pipelined_s": piped, "unpipelined_s": un, "speedup": un / piped}
    elif c == "branch":
        out = {"extra_cpi": o(a, "--freq") * o(a, "--mispredict") * o(a, "--penalty")}
    else:
        print(__doc__); return 2
    print(json.dumps(out)); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
