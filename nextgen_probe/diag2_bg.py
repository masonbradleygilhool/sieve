#!/usr/bin/env python3
"""BG-GATE diagnostic: diag2.py re-run on the bg-fixed lane variant
(ng2_lane_bg). Same draw, same 25 s/task budget, same taxonomy and
class computation as diag2.py; rows additionally carry the
background-stage readout (stage passage, carrying account,
identified map) and the before-record from diag2_rows.json.
Writes diag2_bg_rows.json."""
import json
import sys
import time
from collections import Counter
sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
import ng2_lane_bg as ng2

RUN = "/home/hatch/workspace/arc_apex2/gauntlet/runs/" \
      "run_1793817846_seed20261109_nextgen_v2.json"
POOLS = "/home/hatch/workspace/arc_apex2/gauntlet/pools.json"
BEFORE = "/home/hatch/workspace/arc_apex2/nextgen_probe/diag2_rows.json"
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
    tally = Counter()
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
        cls = ("solved" if solved else
               "train_fit_only" if info.get("fits") else "no_fit")
        b = before[t["tid"]]
        rows.append({
            "tid": t["tid"], "pool": pk,
            "before_class": b["class"], "before_reason": b["lane_reason"],
            "before_full_fit": b["full_fit"],
            "class": cls, "lane_reason": reason,
            "full_fit": bool(info.get("full_fit")),
            "mechanism": info.get("mechanism"),
            "bg_stage_passed": info.get("bg_stage_passed"),
            "bg_functional_count": info.get("bg_functional_count"),
            "bg_account": info.get("bg_account"),
            "bg_map": info.get("bg_map"),
            "wall_s": round(wall, 2)})
        tally[reason] += 1
        tally_ab[reason] += 1
        print(t["tid"], pk, b["lane_reason"], "->", reason,
              "fit:", bool(info.get("full_fit")),
              "bgpass:", info.get("bg_stage_passed"),
              "acct:", info.get("bg_account"),
              f"{wall:.1f}s", flush=True)
    print("A+B new tally:", dict(tally_ab))
    json.dump(rows, open("/home/hatch/workspace/arc_apex2/nextgen_probe/"
                         "diag2_bg_rows.json", "w"), indent=1)


if __name__ == "__main__":
    main()
