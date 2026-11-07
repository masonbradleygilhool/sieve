#!/usr/bin/env python3
"""EXEC-SYNTH supply canary — draw by the registered seed rule
(SIEVE_REDESIGN_COMMISSION_2026-11-07.md, Candidate 1 canary +
constraint C1/C7, extending FRESH_PROBE_PREREGISTRATION_2026-11-07.md
section 4's method one draw further).

Rule: the smallest seed > 22988303 (the fresh probe's seed, the last
spent seed) whose B-draw (canary sampling: draw spec B:24 only;
gauntlet.py's exact rng consumption) is disjoint from the union of
ALL spent B draws — the seven gauntlet run records, the Friday draw,
AND the fresh probe draw (seed 22988303), which is now itself a spent
run record. Gate FIRST: replicate all nine spent draws exactly (id
sets and order); if replication fails, refuse to pick a seed.
gauntlet.py is NOT modified and NOT run here; this script only
computes the draw the same way gauntlet.py does and writes
exec_synth_draw.json beside this file. Nothing is sampled against
any model here.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARC = HERE.parent
GAUNTLET = ARC / "gauntlet"
POOLS_FILE = GAUNTLET / "pools.json"
RUNS_DIR = GAUNTLET / "runs"
FRIDAY_DRAW = ARC / "friday_bigmodel_kit" / "harness" / "friday_draw.json"
FRESH_DRAW = HERE / "fresh_probe_draw.json"
POOL_KEYS = {"A": "A_agi1_eval_fresh", "B": "B_agi2_train_fresh",
             "C": "C_compose_fresh"}
CANARY_SPEC = {"B": 24}
SPENT_RUN_FILES = {
    999: "run_1793752808_seed999_smoke.json",
    20261103: "run_1793752881_seed20261103_baseline.json",
    20261104: "run_1793816913_seed20261104_nextgen_v1.json",
    20261109: "run_1793817846_seed20261109_nextgen_v2.json",
    20261164: "run_1793829053_seed20261164_derived.json",
    20271132: "run_1793832491_seed20271132_sieve_iter2.json",
    20365108: "run_1793837074_seed20365108_sieve_intersection.json",
}
FRIDAY_SEED = 22979062
FRESH_SEED = 22988303
FLOOR = FRESH_SEED  # search strictly above the last spent seed


def replicate_draw(pools, seed, draw_spec):
    """Byte-for-byte gauntlet.py's sampling (same rng consumption)."""
    rng = random.Random(seed)
    drawn = []
    for pk, count in draw_spec.items():
        entries = pools[POOL_KEYS[pk]]
        take = min(count, len(entries))
        for e in rng.sample(entries, take):
            drawn.append((pk, e))
    rng.shuffle(drawn)
    return drawn


def sample_b_ids(pools, seed, draw_spec):
    """B-id set for a seed under a draw spec, without the shuffle
    (the shuffle consumes rng but cannot change set membership)."""
    rng = random.Random(seed)
    out = set()
    for pk, count in draw_spec.items():
        entries = pools[POOL_KEYS[pk]]
        take = min(count, len(entries))
        got = {e["tid"] for e in rng.sample(entries, take)}
        if pk == "B":
            out = got
    return out


def main():
    pools = json.loads(POOLS_FILE.read_text())

    # --- step 1: replicate every spent draw exactly ----------------
    spent_b = set()
    for seed, fname in SPENT_RUN_FILES.items():
        rec = json.loads((RUNS_DIR / fname).read_text())
        assert rec["seed"] == seed, (fname, rec["seed"])
        drawn = replicate_draw(pools, seed, rec["draw_spec"])
        mine = [(pk, e["tid"]) for pk, e in drawn]
        theirs = [(t["pool"], t["tid"]) for t in rec["tasks"]]
        assert sorted(mine) == sorted(theirs), \
            f"REPLICATION FAILED (set) for seed {seed}"
        assert [m[1] for m in mine] == [t[1] for t in theirs], \
            f"REPLICATION FAILED (order) for seed {seed}"
        spent_b |= {tid for pk, tid in mine if pk == "B"}
        print(f"replicated run seed {seed}: {len(mine)} tasks, "
              f"id set + order exact vs {fname}", flush=True)
    fd = json.loads(FRIDAY_DRAW.read_text())
    assert fd["seed"] == FRIDAY_SEED
    drawn = replicate_draw(pools, FRIDAY_SEED, fd["draw_spec"])
    mine_ids = [e["tid"] for _, e in drawn]
    assert mine_ids == fd["task_ids_in_draw_order"], \
        "REPLICATION FAILED for the Friday draw"
    spent_b |= {e["tid"] for pk, e in drawn if pk == "B"}
    print(f"replicated Friday seed {FRIDAY_SEED}: {len(mine_ids)} "
          f"tasks, order exact vs friday_draw.json", flush=True)
    fp = json.loads(FRESH_DRAW.read_text())
    assert fp["seed"] == FRESH_SEED
    drawn = replicate_draw(pools, FRESH_SEED, fp["draw_spec"])
    mine = [(pk, e["tid"]) for pk, e in drawn]
    assert [m[1] for m in mine] == fp["task_ids_in_draw_order"], \
        "REPLICATION FAILED for the fresh probe draw"
    assert sorted(m[1] for m in mine) == \
        sorted(t["tid"] for t in fp["tasks"]), \
        "REPLICATION FAILED (set) for the fresh probe draw"
    fresh_b = {tid for pk, tid in mine if pk == "B"}
    assert len(fresh_b) == 36
    spent_b |= fresh_b
    print(f"replicated fresh-probe seed {FRESH_SEED}: {len(mine)} "
          f"tasks, id set + order exact vs fresh_probe_draw.json",
          flush=True)
    print(f"spent B union: {len(spent_b)} distinct ids "
          f"({len(pools[POOL_KEYS['B']]) - len(spent_b)} untouched)",
          flush=True)
    assert len(spent_b) == 288, len(spent_b)

    # --- step 2: smallest seed above the floor, B-disjoint ---------
    seed = FLOOR + 1
    while True:
        b = sample_b_ids(pools, seed, CANARY_SPEC)
        if not (b & spent_b):
            break
        seed += 1
    drawn = replicate_draw(pools, seed, CANARY_SPEC)
    b_ids = {e["tid"] for _, e in drawn}
    assert not (b_ids & spent_b)
    assert len(b_ids) == 24
    print(f"CANARY SEED: {seed} (B:24 disjoint from all 288 spent "
          f"B ids across nine spent draws)", flush=True)

    out = {
        "kind": "exec_synth_canary_draw",
        "seed": seed,
        "draw_spec": CANARY_SPEC,
        "rule": "smallest seed > 22988303 (fresh probe seed, last "
                "spent) whose B-draw (canary sampling B:24, "
                "gauntlet.py rng consumption) is disjoint from the "
                "union of all spent B draws (run seeds 999, "
                "20261103, 20261104, 20261109, 20261164, 20271132, "
                "20365108 + Friday seed 22979062 + fresh-probe seed "
                "22988303); replication of all nine spent draws "
                "verified exact (id sets and order) before "
                "selection",
        "pool_sizes": {k: len(v) for k, v in pools.items()},
        "spent_b_union_size": len(spent_b),
        "tasks": [{"tid": e["tid"], "pool": pk, "task": e["task"]}
                  for pk, e in drawn],
        "task_ids_in_draw_order": [e["tid"] for _, e in drawn],
    }
    out_path = HERE / "exec_synth_draw.json"
    out_path.write_text(json.dumps(out, indent=1))
    print(f"draw written: {out_path} ({len(drawn)} tasks, all B)",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
