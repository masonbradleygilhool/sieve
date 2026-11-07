#!/usr/bin/env python3
"""CREATION BUILD G2 diagnostic: diag2_bg.py re-run on the creation
lane (ng2_lane_creation). Same spent 48 A+B draw, same 25 s/task
budget, same taxonomy and class computation as diag2_bg.py; the
before-record is diag2_bg_rows.json (the bg-fixed lane). Rows
additionally carry the solution check against the pool's test
outputs (the lane itself never sees them). Writes
diag2_creation_rows.json. Preregistration:
../CREATION_BUILD_PREREGISTRATION_2026-11-07.md."""
import json
import sys
import time
from collections import Counter
sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
import ng2_lane_creation as ng2

RUN = "/home/hatch/workspace/arc_apex2/gauntlet/runs/" \
      "run_1793817846_seed20261109_nextgen_v2.json"
POOLS = "/home/hatch/workspace/arc_apex2/gauntlet/pools.json"
BEFORE = "/home/hatch/workspace/arc_apex2/nextgen_probe/diag2_bg_rows.json"
POOL_KEYS = {"A": "A_agi1_eval_fresh", "B": "B_agi2_train_fresh",
             "C": "C_compose_fresh"}


def main():
    rec = json.load(open(RUN))
    pools = json.load(open(POOLS))
    before = {r["tid"]: r for r in json.load(open(BEFORE))}
    by_id = {}
    for pk, key in POOL_KEYS.items():
        for e in pools[key]:
            by_id[e["tid"]] = (pk, e["task"])
    rows = []
    tally_ab = Counter()
    for t in rec["tasks"]:
        pk, task = by_id[t["tid"]]
        if pk not in ("A", "B"):
            continue
        t0 = time.time()
        preds, info = ng2.lane(task, 25.0)
        wall = time.time() - t0
        reason = info.get("reason") or ("accepted" if info["accepted"]
                                        else "?")
        solved = bool(preds) and info["accepted"]
        # certified-solve check against the held test outputs
        test_ok = None
        if solved:
            test_ok = all(
                preds[i][0] == task["test"][i]["output"]
                for i in range(len(task["test"])))
        cls = ("solved" if solved else
               "train_fit_only" if info.get("fits") else "no_fit")
        b = before[t["tid"]]
        rows.append({
            "tid": t["tid"], "pool": pk,
            "before_class": b["class"], "before_reason": b["lane_reason"],
            "before_full_fit": b["full_fit"],
            "class": cls, "lane_reason": reason,
            "full_fit": bool(info.get("full_fit")),
            "accepted": bool(info.get("accepted")),
            "test_ok": test_ok,
            "mechanism": info.get("mechanism"),
            "programs": info.get("programs"),
            "bg_stage_passed": info.get("bg_stage_passed"),
            "bg_functional_count": info.get("bg_functional_count"),
            "bg_account": info.get("bg_account"),
            "bg_map": info.get("bg_map"),
            "wall_s": round(wall, 2)})
        tally_ab[reason] += 1
        print(t["tid"], pk, b["lane_reason"], "->", reason,
              "fit:", bool(info.get("full_fit")),
              "acc:", bool(info.get("accepted")), "test_ok:", test_ok,
              "mech:", info.get("mechanism"),
              f"{wall:.1f}s", flush=True)
    print("A+B new tally:", dict(tally_ab))
    json.dump(rows, open("/home/hatch/workspace/arc_apex2/nextgen_probe/"
                         "diag2_creation_rows.json", "w"), indent=1)


if __name__ == "__main__":
    main()
