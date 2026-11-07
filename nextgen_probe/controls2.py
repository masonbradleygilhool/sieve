#!/usr/bin/env python3
"""Controls for the next-gen v2 probe lane (pre-registered in
NEXTGEN_V2_DESIGN_2026-11-04.md §8).

Positive A — v2-only transformation: a two-color 2x2 block SPLITS by
color; the color-1 slice moves by (+4,+2) and recolors 1->6, the
color-2 slice moves by (+1,+7) and recolors 2->7; a color-3 2x2
square is preserved, moves by (+3,-4), recolors 3->4.
Positive B — v2-only size change: a color-1 2x2 square GROWS a
color-5 ring (origin shifts by (-1,-1)); the canvas PADS by totals
(2,2) at constant offset (1,1).
Negative — control A's inputs with train outputs shuffled across
pairs; the lane must not accept a schema.

Expected outputs are placed by hand from the stated rules,
independently of the lane's machinery.
"""
import sys
sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
from ng2_lane import lane

# ---------------------------------------------------------------- control A

D1 = (4, 2)    # color-1 slice displacement
D2 = (1, 7)    # color-2 slice displacement
D3 = (3, -4)   # preserver displacement


def blank(h, w):
    return [[0] * w for _ in range(h)]


def pair_a(sp, pr):
    gi = blank(12, 16)
    go = blank(12, 16)
    r, c = sp
    gi[r][c] = 1; gi[r][c + 1] = 1
    gi[r + 1][c] = 2; gi[r + 1][c + 1] = 2
    r, c = pr
    for dr in (0, 1):
        for dc in (0, 1):
            gi[r + dr][c + dc] = 3
    r, c = sp
    go[r + D1[0]][c + D1[1]] = 6; go[r + D1[0]][c + D1[1] + 1] = 6
    go[r + D2[0]][c + D2[1]] = 7; go[r + D2[0]][c + D2[1] + 1] = 7
    r, c = pr
    for dr in (0, 1):
        for dc in (0, 1):
            go[r + D3[0] + dr][c + D3[1] + dc] = 4
    return {"input": gi, "output": go}


def build_a(shuffle=False):
    train = [pair_a((1, 1), (1, 11)),
             pair_a((2, 5), (7, 12)),
             pair_a((7, 2), (2, 12))]
    test = [pair_a((4, 3), (7, 11))]
    if shuffle:
        outs = [p["output"] for p in train]
        for p, o in zip(train, [outs[1], outs[2], outs[0]]):
            p["output"] = o
    return {"train": train, "test": test}


# ---------------------------------------------------------------- control B

def pair_b(sq):
    gi = blank(6, 7)
    go = blank(8, 9)
    r, c = sq
    for dr in (0, 1):
        for dc in (0, 1):
            gi[r + dr][c + dc] = 1
    # grown block in rendered coords: origin (r-1, c-1), 4x4; canvas pad
    # offset (1,1) -> output origin (r, c), inner 2x2 at (r+1, c+1)
    for dr in range(4):
        for dc in range(4):
            inner = dr in (1, 2) and dc in (1, 2)
            go[r + dr][c + dc] = 1 if inner else 5
    return {"input": gi, "output": go}


def build_b():
    train = [pair_b((2, 2)), pair_b((1, 4)), pair_b((3, 1))]
    test = [pair_b((2, 4))]
    return {"train": train, "test": test}


# ---------------------------------------------------------------- run

def main():
    ok = True
    task = build_a()
    preds, info = lane(task, 25.0)
    want = task["test"][0]["output"]
    a_ok = bool(preds) and preds[0] and preds[0][0] == want \
        and info.get("accepted")
    print("POSITIVE A (split_color):", "PASS" if a_ok else "FAIL", info)
    ok = ok and a_ok

    task = build_b()
    preds, info = lane(task, 25.0)
    want = task["test"][0]["output"]
    b_ok = bool(preds) and preds[0] and preds[0][0] == want \
        and info.get("accepted")
    print("POSITIVE B (grow+pad):", "PASS" if b_ok else "FAIL", info)
    ok = ok and b_ok

    task = build_a(shuffle=True)
    preds, info = lane(task, 25.0)
    want = task["test"][0]["output"]
    neg_bad = bool(preds) and preds[0] and preds[0][0] == want
    neg_ok = not neg_bad and not info.get("accepted")
    print("NEGATIVE (shuffled):", "PASS" if neg_ok else "FAIL", info)
    ok = ok and neg_ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
