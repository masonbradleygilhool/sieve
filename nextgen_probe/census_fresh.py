#!/usr/bin/env python3
"""Fresh-probe sample-U — the census protocol of census_g0.py,
unchanged, over the fresh draw's full fits (extended lane).

Protocol (CREATION_BUILD_PREREGISTRATION_2026-11-07.md / census_g0):
for every full-fit task of the creation lane on the fresh draw,
enumerate the version space — ALL verified schemas across all
attempt families (pretransforms) and background accounts; the
lane's SCHEMA_CAP does not apply. Enumeration caps: 20,000
combinations / 512 schemas / 120 s per task; a cap hit marks the
task UNDETERMINED, never absorbed. Each enumerated schema is
rendered on the task's (first) test input via the lane's predict;
a space is unanimous iff exactly one distinct rendered grid AND
enumeration completed. Test outputs are used only to flag
correct/incorrect. Writes census_fresh_rows.json."""
import json
import sys
import time

sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
import census_g0
import ng2_lane_creation as CR

DRAW = "/home/hatch/workspace/arc_apex2/nextgen_probe/" \
       "fresh_probe_draw.json"
ROWS = "/home/hatch/workspace/arc_apex2/nextgen_probe/" \
       "diag_fresh_probe_rows.json"
OUT = "/home/hatch/workspace/arc_apex2/nextgen_probe/" \
      "census_fresh_rows.json"


def main():
    draw = json.load(open(DRAW))
    by_id = {e["tid"]: (e["pool"], e["task"]) for e in draw["tasks"]}
    rows_in = json.load(open(ROWS))
    fits = sorted({r["tid"] for r in rows_in if r["full_fit"]})
    print("fresh-draw full fits to enumerate:", fits, flush=True)
    rows = []
    for tid in fits:
        pk, task = by_id[tid]
        t0 = time.time()
        n, comp, nr, un, cor = census_g0.enumerate_task(CR, task)
        rows.append({"lane": "creation", "tid": tid, "pool": pk,
                     "schemas": n, "completed": comp,
                     "distinct_renders": nr, "unanimous": un,
                     "correct": cor})
        print("creation", tid, pk, "schemas:", n, "completed:", comp,
              "renders:", nr, "unanimous:", un, "correct:", cor,
              f"{time.time()-t0:.1f}s", flush=True)
    json.dump(rows, open(OUT, "w"), indent=1)
    det = [r for r in rows if r["completed"]]
    un = [r for r in det if r["unanimous"]]
    uc = [r for r in un if r["correct"]]
    print("fits:", len(rows), "determined:", len(det),
          "unanimous:", len(un), "unanimous&correct:", len(uc),
          "U_cons:", f"{len(uc)}/{len(rows)}",
          "U_det:", f"{len(uc)}/{len(det)}" if det else "n/a",
          "U_ceiling:", f"{len(uc) + len(rows) - len(det)}/"
          f"{len(rows)}")


if __name__ == "__main__":
    main()
