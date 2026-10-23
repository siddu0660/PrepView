#!/usr/bin/env python3
"""Networking calculator for prep-cn answer keys (stdlib). Never compute these by hand.

  netcalc.py subnet <cidr>                       network, broadcast, mask, first/last host, usable hosts
  netcalc.py split  <cidr> <new_prefix>          list the subnets
  netcalc.py contains <cidr> <ip>                true/false
  netcalc.py vlsm   <cidr> <hosts> [<hosts>...]  allocate subnets for host counts (largest first)
  netcalc.py delay  --size-bytes N --bw-bps B [--dist-m D] [--speed 2e8]   transmission/propagation/total (s)
  netcalc.py window --bw-bps B --rtt-s R [--mss 1460]    BDP bytes and window needed to fill the pipe
  netcalc.py tcp-throughput --window-bytes W --rtt-s R   max throughput bits/s for a window-limited flow
"""
import ipaddress, json, math, sys


def opt(a, name, default=None, cast=float):
    return cast(a[a.index(name) + 1]) if name in a else default


def main(a):
    if not a:
        print(__doc__); return 2
    c = a[0]
    if c == "subnet":
        n = ipaddress.ip_network(a[1], strict=False); hosts = list(n.hosts()) if n.num_addresses <= 2 ** 16 else None
        out = {"network": str(n.network_address), "broadcast": str(n.broadcast_address), "mask": str(n.netmask), "prefix": n.prefixlen,
               "addresses": n.num_addresses, "usable_hosts": max(n.num_addresses - 2, 0) if n.prefixlen < 31 else n.num_addresses,
               "first_host": str(hosts[0]) if hosts else str(n.network_address + 1), "last_host": str(hosts[-1]) if hosts else str(n.broadcast_address - 1)}
    elif c == "split":
        out = [str(s) for s in ipaddress.ip_network(a[1], strict=False).subnets(new_prefix=int(a[2]))]
    elif c == "contains":
        out = ipaddress.ip_address(a[2]) in ipaddress.ip_network(a[1], strict=False)
    elif c == "vlsm":
        net = ipaddress.ip_network(a[1], strict=False); cur = int(net.network_address); out = []
        for h in sorted(map(int, a[2:]), reverse=True):
            pre = 32 - math.ceil(math.log2(h + 2))
            sub = ipaddress.ip_network((cur, pre))
            if sub.broadcast_address > net.broadcast_address:
                out.append({"hosts": h, "error": "does not fit"}); break
            out.append({"hosts": h, "subnet": str(sub), "usable": sub.num_addresses - 2}); cur = int(sub.broadcast_address) + 1
    elif c == "delay":
        size, bw = opt(a, "--size-bytes"), opt(a, "--bw-bps"); tx = size * 8 / bw
        pr = opt(a, "--dist-m", 0) / opt(a, "--speed", 2e8)
        out = {"transmission_s": tx, "propagation_s": pr, "total_s": tx + pr}
    elif c == "window":
        bdp = opt(a, "--bw-bps") * opt(a, "--rtt-s") / 8; mss = opt(a, "--mss", 1460)
        out = {"bdp_bytes": bdp, "segments": math.ceil(bdp / mss)}
    elif c == "tcp-throughput":
        out = {"max_bps": opt(a, "--window-bytes") * 8 / opt(a, "--rtt-s")}
    else:
        print(__doc__); return 2
    print(json.dumps(out)); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
