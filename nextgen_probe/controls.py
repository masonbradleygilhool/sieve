#!/usr/bin/env python3
"""Controls for the next-gen probe lane (pre-registered in the design doc).

Positive: known object rule (color-1 2x2 squares move right 2 and
recolor to 3; color-2 L-trominoes are deleted). The lane must solve it.
Negative: identical inputs, train outputs shuffled across pairs. The
lane must NOT produce an accepted schema / solve.
Expected outputs below are constructed by hand from the stated rule,
independently of the lane's machinery.
"""
import sys
sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
from ng_lane import lane

def blank(h=10, w=12):
    return [[0] * w for _ in range(h)]

def square(g, r, c, col):
    for dr in (0, 1):
        for dc in (0, 1):
            g[r + dr][c + dc] = col

def ell(g, r, c, col):
    g[r][c] = col; g[r + 1][c] = col; g[r + 1][c + 1] = col

def make_pair(sq_pos, el_pos):
    gi = blank(); go = blank()
    for (r, c) in sq_pos:
        square(gi, r, c, 1)
        square(go, r, c + 2, 3)   # the rule, applied by hand
    for (r, c) in el_pos:
        ell(gi, r, c, 2)         # deleted in the output
    return {"input": gi, "output": go}

def build(shuffle=False):
    train = [make_pair([(1, 1)], [(6, 8)]),
             make_pair([(2, 6), (7, 1)], [(1, 9)]),
             make_pair([(5, 3)], [(8, 5), (0, 8)])]
    test = [make_pair([(3, 4)], [(7, 9)])]
    if shuffle:
        outs = [p["output"] for p in train]
        for p, o in zip(train, [outs[1], outs[2], outs[0]]):
            p["output"] = o
    return {"train": train, "test": test}

def main():
    task = build()
    preds, info = lane(task, 25.0)
    want = task["test"][0]["output"]
    pos_ok = bool(preds) and preds[0] and preds[0][0] == want
    print("POSITIVE control:", "PASS" if pos_ok else "FAIL", info)

    task2 = build(shuffle=True)
    preds2, info2 = lane(task2, 25.0)
    want2 = task2["test"][0]["output"]
    neg_bad = bool(preds2) and preds2[0] and preds2[0][0] == want2
    neg_ok = not neg_bad and not info2.get("accepted")
    print("NEGATIVE control:", "PASS" if neg_ok else "FAIL", info2)
    return 0 if (pos_ok and neg_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
