#!/usr/bin/env python3
"""APEX-2 NEXT-GEN PROBE v1 — correspondence-first schema induction.

Mechanism (design: ../NEXTGEN_SOLVER_DESIGN_2026-11-04.md):
  1. Factor out a grid-level dihedral transform by cross-pair
     shape-consistency intersection.
  2. Segment input/output into objects (8-connected non-background
     components); match output objects to input objects by cell count,
     dihedral shape equality, and a functional cellwise color map.
  3. Induce a schema: one action (tau, phi, displacement) per object
     feature class, required consistent across ALL train pairs;
     unmatched input classes must be deletions in every pair;
     creations are outside the v1 language (no full schema).
  4. Accept only on within-task held-out certification:
     >=3 pairs -> leave-one-out re-induction must predict every held
     pair exactly; 2 pairs -> full fit + test determinacy.
     On rejection the lane ABSTAINS (no candidates).

Contract: lane(task, budget_s) -> (predictions, info). Reads train
pairs and test INPUTS only; test outputs are stripped on entry.
"""
import time
from collections import Counter

# ---------------------------------------------------------------- grids

def gshape(g):
    return (len(g), len(g[0]) if g else 0)

def t_id(g): return [row[:] for row in g]
def t_flipud(g): return [row[:] for row in g[::-1]]
def t_fliplr(g): return [row[::-1] for row in g]
def t_rot180(g): return [row[::-1] for row in g[::-1]]
def t_rot90(g):  # clockwise
    return [list(r) for r in zip(*g[::-1])]
def t_rot270(g):
    return [list(r) for r in zip(*g)][::-1]
def t_transpose(g):
    return [list(r) for r in zip(*g)]
def t_anti(g):  # anti-diagonal transpose
    return [list(r) for r in zip(*[row[::-1] for row in g])][::-1]

GRID_TRANSFORMS = [("id", t_id), ("flipud", t_flipud), ("fliplr", t_fliplr),
                   ("rot180", t_rot180), ("rot90", t_rot90),
                   ("rot270", t_rot270), ("transpose", t_transpose),
                   ("anti", t_anti)]

# dihedral transforms on relative cell coords (r, c), applied then
# renormalized by the pattern routine below.
def _d_all(cells):
    outs = []
    for f in (lambda r, c: (r, c), lambda r, c: (r, -c),
              lambda r, c: (-r, c), lambda r, c: (-r, -c),
              lambda r, c: (c, r), lambda r, c: (c, -r),
              lambda r, c: (-c, r), lambda r, c: (-c, -r)):
        outs.append(tuple(sorted(f(r, c) for r, c in cells)))
    return outs

def norm_cells(cells):
    """Translate so min r = min c = 0; return (cells_tuple, origin)."""
    mr = min(r for r, _ in cells); mc = min(c for _, c in cells)
    return tuple(sorted((r - mr, c - mc) for r, c in cells)), (mr, mc)

def canon_shape(cells):
    return min(norm_cells(list(v))[0] for v in _d_all(list(cells)))

# ---------------------------------------------------------------- objects

class Obj:
    __slots__ = ("cells", "pattern", "origin", "shape", "colors", "cls")

    def __init__(self, cells_with_color):
        # cells_with_color: list of (r, c, color) absolute
        rs = [r for r, _, _ in cells_with_color]
        cs = [c for _, c, _ in cells_with_color]
        self.origin = (min(rs), min(cs))
        self.pattern = tuple(sorted(
            (r - self.origin[0], c - self.origin[1], col)
            for r, c, col in cells_with_color))
        self.cells = tuple(sorted((r, c) for r, c, _ in cells_with_color))
        self.shape = tuple(sorted((r, c) for r, c, _ in self.pattern))
        self.colors = tuple(sorted({col for _, _, col in self.pattern}))
        self.cls = (self.colors, len(self.pattern),
                    canon_shape([(r, c) for r, c, _ in self.pattern]))

def segment(grid, bg):
    """8-connected components of non-bg cells."""
    H, W = gshape(grid)
    seen = [[False] * W for _ in range(H)]
    objs = []
    for r in range(H):
        for c in range(W):
            if grid[r][c] == bg or seen[r][c]:
                continue
            stack = [(r, c)]; seen[r][c] = True; comp = []
            while stack:
                cr, cc = stack.pop()
                comp.append((cr, cc, grid[cr][cc]))
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = cr + dr, cc + dc
                        if (0 <= nr < H and 0 <= nc < W
                                and not seen[nr][nc]
                                and grid[nr][nc] != bg):
                            seen[nr][nc] = True
                            stack.append((nr, nc))
            objs.append(Obj(comp))
    objs.sort(key=lambda o: o.origin)
    return objs

def modal_color(grid):
    return Counter(v for row in grid for v in row).most_common(1)[0][0]

def transform_pattern(pattern, tau_idx):
    """Apply dihedral tau_idx to a pattern; return normalized pattern."""
    cells = [(r, c) for r, c, _ in pattern]
    cols = {(r, c): col for r, c, col in pattern}
    f = (lambda r, c: (r, c), lambda r, c: (r, -c),
         lambda r, c: (-r, c), lambda r, c: (-r, -c),
         lambda r, c: (c, r), lambda r, c: (c, -r),
         lambda r, c: (-c, r), lambda r, c: (-c, -r))[tau_idx]
    moved = [f(r, c) for r, c in cells]
    norm, _ = norm_cells(moved)
    # colors ride along with their cells
    src = {f(r, c): cols[(r, c)] for r, c in cells}
    mr = min(r for r, _ in moved); mc = min(c for _, c in moved)
    return tuple(sorted((r - mr, c - mc, src[(r + mr, c + mc)])
                        for r, c in norm))

def match_candidate(inp, outp):
    """If outp can be inp under some dihedral tau with a functional
    cellwise color map, return (tau_idx, phi_dict); else None.
    Deterministic tau preference: identity first."""
    if len(inp.pattern) != len(outp.pattern):
        return None
    order = list(range(8))
    order.sort(key=lambda i: 0 if i == 0 else 1)
    for tau in order:
        tp = transform_pattern(inp.pattern, tau)
        if tuple(sorted((r, c) for r, c, _ in tp)) != outp.shape:
            continue
        phi = {}
        ok = True
        tmap = {(r, c): col for r, c, col in tp}
        for r, c, col in outp.pattern:
            src = tmap.get((r, c))
            if src is None:
                ok = False; break
            if src in phi and phi[src] != col:
                ok = False; break
            phi[src] = col
        if ok:
            return tau, phi
    return None

# ---------------------------------------------------------------- schema

class Schema:
    def __init__(self):
        self.gname = "id"
        self.actions = {}      # cls -> (tau, phi_tuple, (dr, dc))
        self.deletions = set() # classes deleted everywhere
        self.bg_map = None     # (bg_in, bg_out)
        self.canvas = "same"   # or "crop"
        self.tag = "object_schema"

def _induce_for_transform(pairs, gname, gfn):
    """pairs: list of (input, output) raw. Returns Schema or None."""
    norm = []
    for inp, outp in pairs:
        gi = gfn(inp)
        if gshape(gi) != gshape(outp):
            return None
        norm.append((gi, outp))
    sch = Schema(); sch.gname = gname
    bg_pairs = []
    class_seen = {}   # cls -> action or "deleted"
    for gi, outp in norm:
        bg_in = modal_color(gi); bg_out = modal_color(outp)
        bg_pairs.append((bg_in, bg_out))
        in_objs = segment(gi, bg_in)
        out_objs = segment(outp, bg_out)
        # candidate matches
        cand = {}
        for oi, oo in enumerate(out_objs):
            lst = []
            for ii, io in enumerate(in_objs):
                m = match_candidate(io, oo)
                if m is not None:
                    lst.append((ii, m))
            cand[oi] = lst
        # greedy assignment, fewest candidates first
        used_in = set(); assign = {}
        for oi in sorted(cand, key=lambda k: (len(cand[k]), k)):
            for ii, m in cand[oi]:
                if ii not in used_in:
                    used_in.add(ii); assign[oi] = (ii, m); break
            else:
                return None  # an output object has no source: creation
        matched_cls_actions = {}
        for oi, (ii, (tau, phi)) in assign.items():
            io = in_objs[ii]
            delta = (out_objs[oi].origin[0] - io.origin[0],
                     out_objs[oi].origin[1] - io.origin[1])
            act = (tau, tuple(sorted(phi.items())), delta)
            if io.cls in matched_cls_actions and \
                    matched_cls_actions[io.cls] != act:
                return None  # same class, two actions, one pair
            matched_cls_actions[io.cls] = act
        # cross-pair consistency + deletion bookkeeping
        for cls, act in matched_cls_actions.items():
            if cls in sch.deletions:
                return None
            if cls in sch.actions and sch.actions[cls] != act:
                return None
            sch.actions[cls] = act
        for ii, io in enumerate(in_objs):
            if ii in used_in:
                continue
            if io.cls in sch.actions:
                return None  # matched elsewhere, deleted here
            if any(o.cls == io.cls for o in
                   [in_objs[j] for j in used_in]):
                return None  # partial match within the pair
            sch.deletions.add(io.cls)
            class_seen[io.cls] = "deleted"
    if len(set(bg_pairs)) != 1:
        return None  # background mapping inconsistent across pairs
    sch.bg_map = bg_pairs[0]
    # verify by reconstruction on both canvas rules
    for canvas in ("same", "crop"):
        sch.canvas = canvas
        if all(_apply(sch, gi, gname) == outp for gi, outp in norm):
            return sch
    return None

def _apply(sch, grid_in_raw, gname):
    gfn = dict(GRID_TRANSFORMS)[gname]
    gi = gfn(grid_in_raw)
    H, W = gshape(gi)
    bg_in, bg_out = sch.bg_map
    canvas = [[bg_out] * W for _ in range(H)]
    objs = segment(gi, bg_in)
    single_action = None
    if len({a for a in sch.actions.values()}) == 1:
        single_action = next(iter(sch.actions.values()))
    for o in objs:
        if o.cls in sch.deletions:
            continue
        act = sch.actions.get(o.cls, single_action)
        if act is None:
            # unseen class: leave unchanged
            for r, c, col in o.pattern:
                canvas[o.origin[0] + r][o.origin[1] + c] = col
            continue
        tau, phi_items, (dr, dc) = act
        phi = dict(phi_items)
        tp = transform_pattern(o.pattern, tau)
        for r, c, col in tp:
            nr, nc = o.origin[0] + dr + r, o.origin[1] + dc + c
            if 0 <= nr < H and 0 <= nc < W:
                canvas[nr][nc] = phi.get(col, col)
    if sch.canvas == "crop":
        cells = [(r, c) for r in range(H) for c in range(W)
                 if canvas[r][c] != bg_out]
        if not cells:
            return canvas
        mr = min(r for r, _ in cells); Mr = max(r for r, _ in cells)
        mc = min(c for _, c in cells); Mc = max(c for _, c in cells)
        canvas = [row[mc:Mc + 1] for row in canvas[mr:Mr + 1]]
    return canvas

def induce(pairs):
    """pairs: list of (input, output). Returns (schema, transforms_tried)
    or (None, transforms_tried)."""
    tried = 0
    for gname, gfn in GRID_TRANSFORMS:
        tried += 1
        sch = _induce_for_transform(pairs, gname, gfn)
        if sch is not None:
            sch.tag = _mechanism_tag(sch, pairs)
            return sch, tried
    return None, tried

def _mechanism_tag(sch, pairs):
    if sch.gname != "id" and all(
            a[0] == 0 and a[2] == (0, 0) for a in sch.actions.values()):
        return "grid_transform"
    # degenerate: every pair segments to a single object covering >=90%
    for inp, _ in pairs:
        gfn = dict(GRID_TRANSFORMS)[sch.gname]
        gi = gfn(inp)
        objs = segment(gi, modal_color(gi))
        total = gshape(gi)[0] * gshape(gi)[1]
        if not (len(objs) == 1 and len(objs[0].pattern) >= 0.9 * total):
            return "object_schema"
    if all(a[0] == 0 and a[2] == (0, 0) for a in sch.actions.values()):
        return "colormap_only"
    return "object_schema"

def predict(sch, grid_in):
    return _apply(sch, grid_in, sch.gname)

def loo_check(pairs):
    """True iff re-induction from any k-1 pairs predicts the held pair."""
    for j in range(len(pairs)):
        sub = [p for i, p in enumerate(pairs) if i != j]
        sch, _ = induce(sub)
        if sch is None:
            return False
        if predict(sch, pairs[j][0]) != pairs[j][1]:
            return False
    return True

# ---------------------------------------------------------------- lane

def lane(task, budget_s):
    t0 = time.time()
    train = [(p["input"], p["output"]) for p in task["train"]]
    test_inputs = [p["input"] for p in task["test"]]  # outputs stripped
    info = {"fits": 0, "tried": 0, "programs": [],
            "mechanism": None, "loo": None, "accepted": False}
    sch, tried = induce(train)
    info["tried"] = tried
    if sch is None:
        info["reason"] = "no_schema"
        return [], info
    info["mechanism"] = sch.tag
    info["programs"] = [
        f"g={sch.gname} classes={len(sch.actions)} "
        f"del={len(sch.deletions)} canvas={sch.canvas} tag={sch.tag}"]
    if len(train) >= 3:
        ok = loo_check(train)
        info["loo"] = ok
        if not ok:
            info["reason"] = "loo_rejected"
            return [], info
    else:  # exactly 2 (or 1) train pairs: determinacy gate
        info["loo"] = loo_check(train) if len(train) == 2 else None
        gfn = dict(GRID_TRANSFORMS)[sch.gname]
        for ti in test_inputs:
            gi = gfn(ti)
            for o in segment(gi, modal_color(gi)):
                if o.cls not in sch.actions and o.cls not in sch.deletions \
                        and len(sch.actions) != 1:
                    info["reason"] = "nondeterminate_test_class"
                    return [], info
    if time.time() - t0 > budget_s:
        info["reason"] = "budget"
        return [], info
    info["fits"] = 1
    info["accepted"] = True
    preds = [[predict(sch, ti)] for ti in test_inputs]
    return preds, info
