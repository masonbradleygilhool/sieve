#!/usr/bin/env python3
"""Post-run diagnostic for the next-gen probe: where does induction
die on the exact drawn tasks? Uses ng_lane primitives; classifies each
no_schema task by the first failing stage under the first
shape-compatible grid transform. Diagnostic only — the scored verdict
comes from the gauntlet run record."""
import json
import sys
from collections import Counter
sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
import ng_lane as ng

RUN = "/home/hatch/workspace/arc_apex2/gauntlet/runs/run_1793816913_seed20261104_nextgen_v1.json"
POOLS = "/home/hatch/workspace/arc_apex2/gauntlet/pools.json"
POOL_KEYS = {"A": "A_agi1_eval_fresh", "B": "B_agi2_train_fresh",
             "C": "C_compose_fresh"}

def stage_diag(task):
    train = [(p["input"], p["output"]) for p in task["train"]]
    for gname, gfn in ng.GRID_TRANSFORMS:
        norm = []
        ok = True
        for inp, outp in train:
            gi = gfn(inp)
            if ng.gshape(gi) != ng.gshape(outp):
                ok = False; break
            norm.append((gi, outp))
        if not ok:
            continue
        # first shape-compatible transform: analyze pair accounting
        creations = splits = 0
        accounted_pairs = 0
        class_actions = {}
        inconsistent = None
        for gi, outp in norm:
            bg_in = ng.modal_color(gi); bg_out = ng.modal_color(outp)
            in_objs = ng.segment(gi, bg_in)
            out_objs = ng.segment(outp, bg_out)
            used = set(); matched = 0
            pair_class = {}
            for oo in out_objs:
                hit = None
                for ii, io in enumerate(in_objs):
                    if ii in used:
                        continue
                    m = ng.match_candidate(io, oo)
                    if m is not None:
                        hit = (ii, io, m); break
                if hit is None:
                    creations += 1
                    if sum(len(o.pattern) for o in out_objs) != \
                       sum(len(o.pattern) for o in in_objs):
                        splits += 1
                    continue
                ii, io, (tau, phi) = hit
                used.add(ii); matched += 1
                delta = (oo.origin[0] - io.origin[0],
                         oo.origin[1] - io.origin[1])
                act = (tau, tuple(sorted(phi.items())), delta)
                if io.cls in pair_class and pair_class[io.cls] != act:
                    inconsistent = "within_pair_class_conflict"
                pair_class[io.cls] = act
            if matched == len(out_objs):
                accounted_pairs += 1
            for cls, act in pair_class.items():
                if cls in class_actions and class_actions[cls] != act \
                        and inconsistent is None:
                    # separate displacement vs tau/phi conflicts
                    prev = class_actions[cls]
                    if prev[0] == act[0] and prev[1] == act[1]:
                        inconsistent = "displacement_nonconstant"
                    elif prev[1] != act[1]:
                        inconsistent = "phi_conflict"
                    else:
                        inconsistent = "tau_conflict"
                class_actions[cls] = act
        if creations > 0:
            return f"creation_or_splitmerge(cre={creations})"
        if accounted_pairs < len(norm):
            return "unmatched_objects"
        if inconsistent:
            return inconsistent
        return "accounted_consistent(fit failed at reconstruction/bg/loo)"
    return "no_shape_compatible_transform"

def main():
    rec = json.load(open(RUN))
    pools = json.load(open(POOLS))
    by_id = {}
    for pk, key in POOL_KEYS.items():
        for e in pools[key]:
            by_id[e["tid"]] = (pk, e["task"])
    rows = []
    tally = Counter(); tally_ab = Counter()
    for t in rec["tasks"]:
        pk, task = by_id[t["tid"]]
        preds, info = ng.lane(task, 25.0)
        reason = info.get("reason") or ("accepted" if info["accepted"]
                                        else "?")
        stage = stage_diag(task) if reason == "no_schema" else reason
        rows.append({"tid": t["tid"], "pool": pk, "class": t["class"],
                     "lane_reason": reason, "stage": stage})
        tally[stage] += 1
        if pk in ("A", "B"):
            tally_ab[stage] += 1
    print("ALL:", dict(tally))
    print("A+B:", dict(tally_ab))
    json.dump(rows, open("/home/hatch/workspace/arc_apex2/nextgen_probe/"
                         "diag_rows.json", "w"), indent=1)

if __name__ == "__main__":
    main()
