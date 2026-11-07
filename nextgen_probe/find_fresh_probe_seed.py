#!/usr/bin/env python3
"""SIEVE fresh-draw conversion probe — draw by the registered seed
rule (FRESH_PROBE_PREREGISTRATION_2026-11-07.md section 4, extending
friday_bigmodel_kit/harness/find_friday_seed.py's rule by the Friday
seed itself).

Rule: the smallest seed > 22979062 whose B-draw (probe sampling:
draw spec A:12, B:36; gauntlet.py's exact rng consumption) is
disjoint from the union of all spent B draws (seven gauntlet run
records + the Friday draw). Gate FIRST: replicate all eight spent
draws exactly (id sets and order); if replication fails, refuse to
pick a seed. gauntlet.py is NOT modified and NOT run here; this
script only computes the draw the same way gauntlet.py does and
writes fresh_probe_draw.json beside this file. The draw is NOT run
against any lane here.
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
POOL_KEYS = {"A": "A_agi1_eval_fresh", "B": "B_agi2_train_fresh",
             "C": "C_compose_fresh"}
PROBE_SPEC = {"A": 12, "B": 36}
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
FLOOR = FRIDAY_SEED  # search strictly above the last spent seed


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


def sample_ids(pools, seed, draw_spec):
    """(A-id set, B-id set) for a seed, without the shuffle (the
    shuffle consumes rng but cannot change set membership)."""
    rng = random.Random(seed)
    out = {}
    for pk, count in draw_spec.items():
        entries = pools[POOL_KEYS[pk]]
        take = min(count, len(entries))
        out[pk] = {e["tid"] for e in rng.sample(entries, take)}
    return out.get("A", set()), out.get("B", set())


def main():
    pools = json.loads(POOLS_FILE.read_text())

    # --- step 1: replicate every spent draw exactly ----------------
    spent_b = set()
    spent_all = {}
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
        spent_all[seed] = [tid for _, tid in mine]
        spent_b |= {tid for pk, tid in mine if pk == "B"}
        print(f"replicated run seed {seed}: {len(mine)} tasks, "
              f"id set + order exact vs {fname}", flush=True)
    fd = json.loads(FRIDAY_DRAW.read_text())
    assert fd["seed"] == FRIDAY_SEED
    drawn = replicate_draw(pools, FRIDAY_SEED, fd["draw_spec"])
    mine_ids = [e["tid"] for _, e in drawn]
    assert mine_ids == fd["task_ids_in_draw_order"], \
        "REPLICATION FAILED for the Friday draw"
    spent_all[FRIDAY_SEED] = mine_ids
    spent_b |= {e["tid"] for pk, e in drawn if pk == "B"}
    print(f"replicated Friday seed {FRIDAY_SEED}: {len(mine_ids)} "
          f"tasks, order exact vs friday_draw.json", flush=True)
    print(f"spent B union: {len(spent_b)} distinct ids "
          f"({len(pools[POOL_KEYS['B']]) - len(spent_b)} untouched)",
          flush=True)

    # --- step 2: smallest seed above the floor, B-disjoint ---------
    seed = FLOOR + 1
    while True:
        _a, b = sample_ids(pools, seed, PROBE_SPEC)
        if not (b & spent_b):
            break
        seed += 1
    drawn = replicate_draw(pools, seed, PROBE_SPEC)
    a_ids = {e["tid"] for pk, e in drawn if pk == "A"}
    b_ids = {e["tid"] for pk, e in drawn if pk == "B"}
    assert not (b_ids & spent_b)
    a_overlap = {str(s): sorted(set(ids) & a_ids)
                 for s, ids in spent_all.items()}
    a_overlap = {s: v for s, v in a_overlap.items() if v}
    print(f"PROBE SEED: {seed} (B disjoint from all 8 spent draws; "
          f"A-overlap unavoidable with pool A=18, reported below)",
          flush=True)

    out = {
        "kind": "fresh_probe_draw",
        "seed": seed,
        "draw_spec": PROBE_SPEC,
        "rule": "smallest seed > 22979062 whose B-draw (probe "
                "sampling A:12,B:36, gauntlet.py rng consumption) "
                "is disjoint from the union of all spent B draws "
                "(run seeds 999, 20261103, 20261104, 20261109, "
                "20261164, 20271132, 20365108 + Friday seed "
                "22979062); replication of all eight spent draws "
                "verified exact (id sets and order) before "
                "selection; A-overlap unavoidable (pool A = 18, all "
                "drawn historically) and recorded per spent draw",
        "pool_sizes": {k: len(v) for k, v in pools.items()},
        "spent_b_union_size": len(spent_b),
        "a_overlap_with_spent_draws": a_overlap,
        "tasks": [{"tid": e["tid"], "pool": pk, "task": e["task"]}
                  for pk, e in drawn],
        "task_ids_in_draw_order": [e["tid"] for _, e in drawn],
    }
    out_path = HERE / "fresh_probe_draw.json"
    out_path.write_text(json.dumps(out, indent=1))
    print(f"draw written: {out_path} ({len(drawn)} tasks: "
          f"A={len(a_ids)} B={len(b_ids)})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
