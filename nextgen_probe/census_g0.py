#!/usr/bin/env python3
"""G0 — survivor-census re-measurement over the extended grammar.

Protocol: SURVIVOR_SET_CENSUS_2026-11-04.md's own, as registered in
CREATION_BUILD_PREREGISTRATION_2026-11-07.md. For every full-fit
task of the lane on the spent 48 A+B draw, enumerate the version
space — ALL verified schemas across all attempt families
(pretransforms) and background accounts; the lane's SCHEMA_CAP does
not apply. Enumeration caps: 20,000 combinations / 512 schemas /
120 s per task; a cap hit marks the task UNDETERMINED, never
absorbed. Each enumerated schema is rendered on the task's test
input via the lane's predict; a space is unanimous iff exactly one
distinct rendered grid AND enumeration completed. Test outputs are
used only to flag correct/incorrect.

Populations: (a) the OLD lane (ng2_lane_bg) on the 4 banked fits —
kill criterion 4's comparison population; (b) the EXTENDED lane
(ng2_lane_creation) on every task it full-fits on the spent draw
(from diag2_creation_rows.json). Writes census_g0_rows.json."""
import json
import sys
import time

sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
import ng2_lane_bg as BG
import ng2_lane_creation as CR

POOLS = "/home/hatch/workspace/arc_apex2/gauntlet/pools.json"
CRE_ROWS = "/home/hatch/workspace/arc_apex2/nextgen_probe/" \
           "diag2_creation_rows.json"
OUT = "/home/hatch/workspace/arc_apex2/nextgen_probe/census_g0_rows.json"
BANKED = ["7d1f7ee8", "a61f2674", "4acc7107", "8dae5dfc"]
SCHEMA_ENUM_CAP = 512
COMBO_CAP = 20000
WALL_CAP = 120.0


class CapHit(Exception):
    pass


def _schema_sig(sch):
    if "program" in sch:
        return ("program", str(sch["program"]))
    return (sch.get("seg"), sch.get("gen_in"), sch.get("gen_out"),
            tuple(sorted((str(k), str(v))
                         for k, v in sch["bindings"].items())),
            tuple(sorted(str(d) for d in sch["deletions"])))


def _enumerate_account(L, tpairs, seg_name, ga, gb, bp, fmap, t_end):
    segfn = L.SEG_FNS[seg_name]
    acct = {"seg": seg_name, "gen_in": ga, "gen_out": gb,
            "bg_map": dict(fmap), "bg_pairs": list(bp)}
    per_pair = []
    for pi, (gi, outp) in enumerate(tpairs):
        bg = bp[pi]
        in_objs = segfn(gi, bg[0])
        out_objs = segfn(outp, bg[1])
        if len(in_objs) > L.MAX_OBJECTS or len(out_objs) > L.MAX_OBJECTS:
            return []
        if L is CR:
            cand, _zero = L.gen_candidates(
                in_objs, out_objs, L.gshape(outp), t_end,
                scene={"grid": gi, "bg_in": bg[0], "seg": seg_name})
        else:
            cand, _zero = L.gen_candidates(in_objs, out_objs,
                                           L.gshape(outp), t_end)
        if cand is None:
            return []
        assigns, capped = L.pair_assignments(in_objs, out_objs, cand,
                                             t_end)
        if capped:
            raise CapHit()
        if not assigns:
            return []
        filtered = []
        for b, d in assigns:
            sch_j = dict(acct, bg=bg, bg_pairs=[bg], bindings=b,
                         deletions=d)
            if L.verify_schema(sch_j, [(gi, outp)]):
                filtered.append((b, d))
        if not filtered:
            return []
        per_pair.append(filtered)
    holder = {}
    schemas = []
    combos = 0
    for bindings, deletions in L.combine_iter(per_pair, t_end, holder):
        combos += 1
        if combos > COMBO_CAP:
            raise CapHit()
        sch = dict(acct, bg=bp[0], bindings=bindings,
                   deletions=deletions)
        if L.verify_schema(sch, tpairs):
            schemas.append(sch)
            if len(schemas) >= SCHEMA_ENUM_CAP:
                raise CapHit()
        if time.time() > t_end:
            raise CapHit()
    if holder.get("capped"):
        raise CapHit()
    return schemas


def _enumerate_programs(L, pairs, t_end):
    """All validating Stratum-1 programs (creation lane only)."""
    out = []
    idfn = next(fn for name, fn in L.PRETRANSFORMS if name == "id|x1")

    def mksch(name, params):
        return {"program": (name, params), "pre_name": "id|x1",
                "pre_fn": idfn, "canvas": "same", "seg": "agnostic",
                "gen_in": "program", "gen_out": "program",
                "bg_map": {}, "bg_pairs": [], "bg": (0, 0),
                "bindings": {}, "deletions": set()}

    gi0, go0 = pairs[0]
    H, W = L.gshape(gi0)
    Ho, Wo = L.gshape(go0)
    if not (Ho > H or Wo > W or (Ho == H and Wo == W)):
        tried = 0
        for rg in L._compositions(H, Ho, 12):
            for cg in L._compositions(W, Wo, 12):
                tried += 1
                if tried > 300:
                    break
                clf = L._quotient_identify(pairs, rg, cg, t_end)
                if clf is not None:
                    out.append(mksch("quotient", (rg, cg, clf)))
    occs = [None] + sorted({v for row in gi0 for v in row})
    for occ in occs:
        if all(L._domain_apply(gi, occ) == go for gi, go in pairs):
            out.append(mksch("domain", occ))
        if all(L._sym_apply(gi, occ) == go for gi, go in pairs):
            out.append(mksch("symclose", occ))
    if H * W <= 1600:
        for dr in range(-(H - 1), H):
            for dc in range(-(W - 1), W):
                if (dr, dc) == (0, 0):
                    continue
                if all(L._lattice_apply(gi, (dr, dc)) == go
                       for gi, go in pairs):
                    out.append(mksch("lattice", (dr, dc)))
    return out


def enumerate_task(L, task):
    """-> (n_schemas, completed, renders:set, correct:bool)"""
    pairs = [(p["input"], p["output"]) for p in task["train"]]
    test_in = task["test"][0]["input"]
    test_out = task["test"][0]["output"]
    t_end = time.time() + WALL_CAP
    schemas = []
    seen = set()
    completed = True
    try:
        for pname, pfn in L.PRETRANSFORMS:
            tpairs = []
            ok = True
            for inp, outp in pairs:
                gi = pfn(inp)
                if gi is None:
                    ok = False
                    break
                tpairs.append((gi, outp))
            if not ok or not L._shape_compatible(tpairs):
                continue
            for seg_name, ga, gb, bp, fmap in L._accounts(tpairs):
                got = _enumerate_account(L, tpairs, seg_name, ga, gb,
                                         bp, fmap, t_end)
                for sch in got:
                    sch["pre_name"] = pname
                    sch["pre_fn"] = pfn
                    sig = _schema_sig(sch)
                    if sig not in seen:
                        seen.add(sig)
                        schemas.append(sch)
                if len(schemas) >= SCHEMA_ENUM_CAP:
                    raise CapHit()
                if time.time() > t_end:
                    raise CapHit()
        if L is CR:
            for sch in _enumerate_programs(L, pairs, t_end):
                sig = _schema_sig(sch)
                if sig not in seen:
                    seen.add(sig)
                    schemas.append(sch)
    except (CapHit, L.Timeout):
        completed = False
    renders = set()
    for sch in schemas:
        try:
            renders.add(L._grid_key(L.predict(sch, test_in)))
        except Exception:
            renders.add(("__predict_error__",))
    unanimous = completed and len(renders) == 1
    correct = unanimous and renders == {L._grid_key(test_out)}
    return len(schemas), completed, len(renders), unanimous, correct


def main():
    pools = json.load(open(POOLS))
    by_id = {}
    for key in ("A_agi1_eval_fresh", "B_agi2_train_fresh",
                "C_compose_fresh"):
        for e in pools[key]:
            by_id[e["tid"]] = e["task"]
    cre_rows = json.load(open(CRE_ROWS))
    new_fits = sorted({r["tid"] for r in cre_rows if r["full_fit"]})
    rows = []
    print("== OLD lane (ng2_lane_bg) on the 4 banked fits", flush=True)
    for tid in BANKED:
        t0 = time.time()
        n, comp, nr, un, cor = enumerate_task(BG, by_id[tid])
        rows.append({"lane": "bg", "tid": tid, "schemas": n,
                     "completed": comp, "distinct_renders": nr,
                     "unanimous": un, "correct": cor})
        print("bg", tid, "schemas:", n, "completed:", comp,
              "renders:", nr, "unanimous:", un, "correct:", cor,
              f"{time.time()-t0:.1f}s", flush=True)
    print("== EXTENDED lane (ng2_lane_creation) on its spent-draw fits:",
          new_fits, flush=True)
    for tid in new_fits:
        t0 = time.time()
        n, comp, nr, un, cor = enumerate_task(CR, by_id[tid])
        rows.append({"lane": "creation", "tid": tid, "schemas": n,
                     "completed": comp, "distinct_renders": nr,
                     "unanimous": un, "correct": cor})
        print("creation", tid, "schemas:", n, "completed:", comp,
              "renders:", nr, "unanimous:", un, "correct:", cor,
              f"{time.time()-t0:.1f}s", flush=True)
    json.dump(rows, open(OUT, "w"), indent=1)
    for lane in ("bg", "creation"):
        sub = [r for r in rows if r["lane"] == lane]
        det = [r for r in sub if r["completed"]]
        un = [r for r in det if r["unanimous"]]
        uc = [r for r in un if r["correct"]]
        print(lane, "fits:", len(sub), "determined:", len(det),
              "unanimous:", len(un), "unanimous&correct:", len(uc),
              "U_cons:", f"{len(uc)}/{len(sub)}",
              "U_det:", f"{len(uc)}/{len(det)}" if det else "n/a")


if __name__ == "__main__":
    main()
