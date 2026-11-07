#!/usr/bin/env python3
"""Post-run diagnostic for the next-gen v2 probe: per-task sub-reason
and full-fit accounting on the exact drawn tasks, from the lane's own
info dict (design §6 taxonomy). Diagnostic only — the scored verdict
comes from the gauntlet run record. Also cross-checks that re-running
the lane reproduces the run record's classes task by task."""
import json
import sys
from collections import Counter
sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
import ng2_lane as ng2

RUN = "/home/hatch/workspace/arc_apex2/gauntlet/runs/" \
      "run_1793817846_seed20261109_nextgen_v2.json"
POOLS = "/home/hatch/workspace/arc_apex2/gauntlet/pools.json"
POOL_KEYS = {"A": "A_agi1_eval_fresh", "B": "B_agi2_train_fresh",
             "C": "C_compose_fresh"}


def main():
    rec = json.load(open(RUN))
    pools = json.load(open(POOLS))
    by_id = {}
    for pk, key in POOL_KEYS.items():
        for e in pools[key]:
            by_id[e["tid"]] = (pk, e["task"])
    rows = []
    tally = Counter()
    tally_ab = Counter()
    fit_ab = fit_all = 0
    loo_rej_ab = 0
    mismatch = 0
    for t in rec["tasks"]:
        pk, task = by_id[t["tid"]]
        preds, info = ng2.lane(task, 25.0)
        reason = info.get("reason") or ("accepted" if info["accepted"]
                                        else "?")
        solved = bool(preds) and info["accepted"]
        cls = ("solved" if solved else
               "train_fit_only" if info.get("fits") else "no_fit")
        if cls != t["class"]:
            mismatch += 1
        rows.append({"tid": t["tid"], "pool": pk, "class": t["class"],
                     "lane_reason": reason,
                     "full_fit": bool(info.get("full_fit")),
                     "mechanism": info.get("mechanism")})
        tally[reason] += 1
        if pk in ("A", "B"):
            tally_ab[reason] += 1
            fit_ab += bool(info.get("full_fit"))
            loo_rej_ab += reason == "loo_rejected"
        fit_all += bool(info.get("full_fit"))
    print("class mismatches vs run record:", mismatch)
    print("full-fit coverage A+B:", f"{fit_ab}/48", " all:", f"{fit_all}/60")
    print("loo-rejected among A+B full-fits:", loo_rej_ab)
    print("ALL:", dict(tally))
    print("A+B:", dict(tally_ab))
    json.dump(rows, open("/home/hatch/workspace/arc_apex2/nextgen_probe/"
                         "diag2_rows.json", "w"), indent=1)


if __name__ == "__main__":
    main()
