#!/usr/bin/env python3
"""EXEC-SYNTH canary sandbox harness.

Reads {"pairs": [{"input": g, "output": g}, ...]} as JSON from stdin
(consumed before any candidate code runs), loads the candidate
program from the file named in argv[1], executes transform() on a
deep copy of each train input, and prints ONE JSON line of per-pair
results to stdout. Registered caps: RLIMIT_CPU 5 s, RLIMIT_AS 2 GB,
socket module disabled, stdin already consumed (candidate reads get
EOF). The parent enforces the 6 s wall timeout.
"""
import copy
import json
import resource
import sys


def _block_network():
    import socket

    class _Blocked(socket.socket):
        def __init__(self, *a, **k):
            raise OSError("network disabled in sandbox")

    socket.socket = _Blocked
    socket.create_connection = lambda *a, **k: (_ for _ in ()).throw(
        OSError("network disabled in sandbox"))
    socket.getaddrinfo = lambda *a, **k: (_ for _ in ()).throw(
        OSError("network disabled in sandbox"))


def main():
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    resource.setrlimit(resource.RLIMIT_AS,
                       (2_000_000_000, 2_000_000_000))
    _block_network()
    pairs = json.loads(sys.stdin.read())["pairs"]
    code = open(sys.argv[1]).read()
    ns = {}
    try:
        exec(compile(code, "<candidate>", "exec"), ns)
    except Exception as e:  # load/syntax error: every pair errors
        out = {"load_error": f"{type(e).__name__}: {e}",
               "results": [{"status": "load_error"} for _ in pairs]}
        print(json.dumps(out))
        return 0
    fn = ns.get("transform")
    if not callable(fn):
        out = {"load_error": "no callable transform defined",
               "results": [{"status": "load_error"} for _ in pairs]}
        print(json.dumps(out))
        return 0
    results = []
    for p in pairs:
        exp = p["output"]
        try:
            got = fn(copy.deepcopy(p["input"]))
        except Exception as e:
            results.append({"status": "exception",
                            "error": f"{type(e).__name__}: {e}"[:300]})
            continue
        ok_shape = (isinstance(got, list) and len(got) == len(exp)
                    and all(isinstance(r, list) and len(r) == len(er)
                            for r, er in zip(got, exp)))
        if not ok_shape:
            try:
                gs = [len(got), len(got[0]) if got else 0]
            except Exception:
                gs = [-1, -1]
            results.append({"status": "shape",
                            "got_shape": gs,
                            "exp_shape": [len(exp),
                                          len(exp[0]) if exp else 0]})
            continue
        diffs = []
        for r in range(len(exp)):
            for c in range(len(exp[0])):
                if got[r][c] != exp[r][c]:
                    diffs.append([r, c, exp[r][c], got[r][c]])
        if diffs:
            results.append({"status": "mismatch",
                            "diff_cells": len(diffs),
                            "diffs": diffs[:12]})
        else:
            results.append({"status": "ok"})
    print(json.dumps({"load_error": None, "results": results}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
