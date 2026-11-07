#!/usr/bin/env python3
"""FRESH-DRAW CONVERSION PROBE: diag2_creation.py's protocol on the
fresh draw (nextgen_probe/fresh_probe_draw.json, seed 22988303) with
the shipped creation lane (ng2_lane_creation, post-KC5 cuts). Same
25 s/task frozen budget, same taxonomy and class computation as
diag2_creation.py; rows additionally check the solution against the
pool's test outputs (the lane itself never sees them). A task that
raises is recorded as an error row and never replaced (no
re-sampling, per the preregistration). Writes
diag_fresh_probe_rows.json. Preregistration:
../FRESH_PROBE_PREREGISTRATION_2026-11-07.md."""
import json
import sys
import time
import traceback
from collections import Counter
sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
import ng2_lane_creation as ng2

DRAW = "/home/hatch/workspace/arc_apex2/nextgen_probe/" \
       "fresh_probe_draw.json"
OUT = "/home/hatch/workspace/arc_apex2/nextgen_probe/" \
      "diag_fresh_probe_rows.json"


def main():
    draw = json.load(open(DRAW))
    rows = []
    tally = Counter()
    for e in draw["tasks"]:
        tid, pk, task = e["tid"], e["pool"], e["task"]
        t0 = time.time()
        try:
            preds, info = ng2.lane(task, 25.0)
            wall = time.time() - t0
            reason = info.get("reason") or (
                "accepted" if info["accepted"] else "?")
            solved = bool(preds) and info["accepted"]
            test_ok = None
            if solved:
                test_ok = all(
                    preds[i][0] == task["test"][i]["output"]
                    for i in range(len(task["test"])))
            cls = ("solved" if solved else
                   "train_fit_only" if info.get("fits") else "no_fit")
            rows.append({
                "tid": tid, "pool": pk,
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
                "error": None,
                "wall_s": round(wall, 2)})
            print(tid, pk, "->", reason,
                  "fit:", bool(info.get("full_fit")),
                  "acc:", bool(info.get("accepted")),
                  "test_ok:", test_ok,
                  "mech:", info.get("mechanism"),
                  f"{wall:.1f}s", flush=True)
        except Exception as ex:
            wall = time.time() - t0
            traceback.print_exc()
            rows.append({
                "tid": tid, "pool": pk,
                "class": "error",
                "lane_reason": f"error:{type(ex).__name__}",
                "full_fit": False, "accepted": False,
                "test_ok": None, "mechanism": None, "programs": None,
                "bg_stage_passed": None, "bg_functional_count": None,
                "bg_account": None, "bg_map": None,
                "error": f"{type(ex).__name__}: {ex}",
                "wall_s": round(wall, 2)})
            print(tid, pk, "-> ERROR", type(ex).__name__, ex,
                  f"{wall:.1f}s", flush=True)
        tally[rows[-1]["lane_reason"]] += 1
    print("fresh-draw tally:", dict(tally))
    json.dump(rows, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
