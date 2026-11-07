#!/usr/bin/env python3
"""APEX-2 NEXT-GEN PROBE v2, CREATION VARIANT — the BG-GATE lane
(ng2_lane_bg.py) plus the creation machinery of
CREATION_MACHINERY_SPEC_2026-11-07.md (preregistration:
../CREATION_BUILD_PREREGISTRATION_2026-11-07.md). The solver core
(pair_assignments, combine_iter, loo_check, the determinate()
closure in lane()) is byte-identical to ng2_lane_bg.py; the
background stage is unchanged. What is added, per the spec's three
strata: (1) whole-grid PROGRAM accounts (M-Q quotient partitions,
M-Q(iii) symmetry-domain extraction, M-S symmetry completion,
lattice orbit completion) tried inside induce() only after the
object pipeline has failed on every attempt; (2) pattern sources
(M-G color-class gather, stamp copy-unions) and scene patterns
threaded through gen_candidates via a per-pair `scene` argument;
(3) derivation kinds M-U union, M-L stroke, M-R stamp, M-F iterated
rings + inset, M-C count-shape, M-T checkerboard texture, and M-P
split-and-discard (kept-set group needs; instance colors carried in
creation derivation values). Budget (25 s/task), caps, Occam order,
canvas rules and LOO certification are frozen.

APEX-2 NEXT-GEN PROBE v2, BG-GATE VARIANT — identical to ng2_lane.py
except the background stage is replaced by the NOVEMBER_CONVERSION_
PACKET §2.2 searched-background-identification component (BG-GATE,
preregistration: ../BG_GATE_PREREGISTRATION_2026-11-07.md). Grammar,
caps, pretransforms, Occam order, canvas rules, and the LOO
certification are unchanged. The stage replacement: background
values are generated per pair by {modal, border-modal, corner,
sea} (definitions imported from the census operationalization);
an account is (segmentation {agnostic, primary} x generator pair);
an account survives iff its generated input-bg -> output-bg map is
functional across the attempt's pairs (cross-pair intersection);
segmentation and induction run relative to the surviving account;
the binding is re-identified inside every LOO fold because
loo_check calls this module's induce().

APEX-2 NEXT-GEN PROBE v2 — derivation-based correspondence induction.

Mechanism (design: ../NEXTGEN_V2_DESIGN_2026-11-04.md):
  Objects are produced by DERIVATIONS (preserve / scale / grow / mirror /
  split_color / split_sep / merge / copy / frame), not only preserved or
  deleted as in v1. Per pair, identification is exact cover over objects:
  candidate derivations are measured geometric facts about the pair;
  assignments must consume every input exactly once and produce every
  output exactly once. Cross-pair intersection on key->value bindings
  identifies the schema. Grid size change is a dihedral+scale
  pre-transform plus a canvas rule (same / crop / pad). Acceptance is
  v1's LOO re-induction certification, unchanged in form; on rejection
  or ambiguity the lane ABSTAINS.

Contract: lane(task, budget_s) -> (predictions, info). Reads train
pairs and test INPUTS only; test outputs are stripped on entry.
"""
import sys
import time
from collections import Counter

sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")
sys.path.insert(0, "/home/hatch/workspace/arc_apex2/census")
import ng_lane as ng
from census_param_bound import bg_generators, GENS as _GENS

gshape = ng.gshape
GRID_TRANSFORMS = ng.GRID_TRANSFORMS
segment = ng.segment
modal_color = ng.modal_color
transform_pattern = ng.transform_pattern
match_candidate = ng.match_candidate

MAX_OBJECTS = 20
CAND_CAP_PER_OUT = 64
MERGE_CAND_CAP = 16
ASSIGN_CAP = 16
ASSIGN_NODES = 3000
COMBINE_NODES = 4000
SCHEMA_CAP = 24  # max combinations reconstruction-verified per attempt


class Timeout(Exception):
    pass


def _tick(deadline):
    if time.time() > deadline:
        raise Timeout()


# ------------------------------------------------- BG-GATE: bg stage

GEN_ORDER = list(_GENS)  # ['modal', 'border_modal', 'corner', 'sea']
SEG_ORDER = ("agnostic", "primary")


def segment_primary(grid, bg):
    """Per-color 4-connected components of non-bg cells (the census
    'primary' segmentation), returning ng.Obj objects sorted by
    origin — the same contract as ng.segment."""
    H, W = gshape(grid)
    seen = [[False] * W for _ in range(H)]
    objs = []
    for r in range(H):
        for c in range(W):
            if grid[r][c] == bg or seen[r][c]:
                continue
            col = grid[r][c]
            stack = [(r, c)]
            seen[r][c] = True
            comp = []
            while stack:
                cr, cc = stack.pop()
                comp.append((cr, cc, grid[cr][cc]))
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = cr + dr, cc + dc
                    if (0 <= nr < H and 0 <= nc < W
                            and not seen[nr][nc]
                            and grid[nr][nc] == col):
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            objs.append(ng.Obj(comp))
    objs.sort(key=lambda o: o.origin)
    return objs


SEG_FNS = {"agnostic": segment, "primary": segment_primary}

# Trace of the most recent _induce_under attempt's background stage,
# read by induce()/lane() for the gate readout. Keys: functional
# (list of (seg, gen_in, gen_out)), account (designated or winning
# (seg, gen_in, gen_out) or None).
_BG_TRACE = {}


def _accounts(tpairs):
    """All functional accounts for an attempt's pairs, in declared
    order: (seg_name, gen_in, gen_out, bg_pairs, bg_map). Generator
    values are computed once per grid; an account survives iff its
    generated input-bg -> output-bg values form a function across
    the pairs (cross-pair intersection, packet SS2.2 step 2)."""
    gen_in_vals = [bg_generators(gi) for gi, _ in tpairs]
    gen_out_vals = [bg_generators(o) for _, o in tpairs]
    out = []
    for seg_name in SEG_ORDER:
        for ga in GEN_ORDER:
            for gb in GEN_ORDER:
                bp = [(gen_in_vals[i][ga], gen_out_vals[i][gb])
                      for i in range(len(tpairs))]
                m = {}
                ok = True
                for a, b in bp:
                    if a in m and m[a] != b:
                        ok = False
                        break
                    m[a] = b
                if ok:
                    out.append((seg_name, ga, gb, bp, m))
    return out


# ---------------------------------------------------------------- patterns

def pat_map(pattern):
    return {(r, c): col for r, c, col in pattern}


def pat_from_map(cells):
    """dict (r,c)->color (color may be None = added cell) -> normalized
    pattern with None preserved, plus origin offset."""
    mr = min(r for r, _ in cells)
    mc = min(c for _, c in cells)
    pat = tuple(sorted((r - mr, c - mc, col) for (r, c), col in cells.items()))
    return pat, (mr, mc)


def phi_match(src_pattern, out_pattern):
    """Functional color map taking src_pattern cellwise onto
    out_pattern, or None. Patterns must occupy identical cell sets."""
    if len(src_pattern) != len(out_pattern):
        return None
    smap = pat_map(src_pattern)
    phi = {}
    for r, c, col in out_pattern:
        s = smap.get((r, c))
        if s is None:
            return None
        if phi.get(s, col) != col:
            return None
        phi[s] = col
    return phi


def phi_tuple(phi):
    return tuple(sorted(phi.items()))


def scale_up_pat(pattern, k):
    cells = {}
    for r, c, col in pattern:
        for dr in range(k):
            for dc in range(k):
                cells[(r * k + dr, c * k + dc)] = col
    return pat_from_map(cells)[0]


def scale_down_pat(pattern, k):
    cells = pat_map(pattern)
    H = max(r for r, _ in cells) + 1
    W = max(c for _, c in cells) + 1
    if H % k or W % k:
        return None
    out = {}
    for br in range(H // k):
        for bc in range(W // k):
            block = [cells.get((br * k + dr, bc * k + dc))
                     for dr in range(k) for dc in range(k)]
            if any(v is None for v in block) or len(set(block)) != 1:
                return None
            out[(br, bc)] = block[0]
    return pat_from_map(out)[0]


def _dilate(shape):
    out = set()
    for r, c in shape:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                out.add((r + dr, c + dc))
    return out


def _holes(shape):
    H = max(r for r, _ in shape) + 1
    W = max(c for _, c in shape) + 1
    seen = set()
    stack = [(r, c) for r in range(H) for c in range(W)
             if (r in (0, H - 1) or c in (0, W - 1)) and (r, c) not in shape]
    seen.update(stack)
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and (nr, nc) not in shape \
                    and (nr, nc) not in seen:
                seen.add((nr, nc))
                stack.append((nr, nc))
    return {(r, c) for r in range(H) for c in range(W)
            if (r, c) not in shape and (r, c) not in seen}


def grow_pat(pattern, mode):
    """Pattern with added cells marked color None, or None if the mode
    adds nothing. Geometry only; fill color is matched later."""
    cells = pat_map(pattern)
    shape = set(cells)
    if mode == "ring":
        target = _dilate(shape)
    elif mode == "holes":
        target = shape | _holes(shape)
    elif mode == "bbox":
        H = max(r for r, _ in shape) + 1
        W = max(c for _, c in shape) + 1
        target = {(r, c) for r in range(H) for c in range(W)}
    else:
        return None
    if target == shape:
        return None
    grown = {pos: cells.get(pos) for pos in target}
    return pat_from_map(grown)[0]


def grow_match(src_pattern, mode, out_pattern):
    """-> (phi, fill_color) or None."""
    grown = grow_pat(src_pattern, mode)
    if grown is None or len(grown) != len(out_pattern):
        return None
    omap = pat_map(out_pattern)
    phi = {}
    fills = set()
    for r, c, col in grown:
        oc = omap.get((r, c))
        if oc is None:
            return None
        if col is None:
            fills.add(oc)
        else:
            if phi.get(col, oc) != oc:
                return None
            phi[col] = oc
    if len(fills) != 1:
        return None
    return phi, fills.pop()


def mirror_pat(pattern, axis):
    cells = pat_map(pattern)
    H = max(r for r, _ in cells) + 1
    W = max(c for _, c in cells) + 1
    out = dict(cells)
    for (r, c), col in cells.items():
        pos = (r, W - 1 - c) if axis == "v" else (H - 1 - r, c)
        if pos in out and out[pos] != col:
            return None
        out[pos] = col
    if len(out) == len(cells):
        return None  # already symmetric: mirror adds nothing
    return pat_from_map(out)[0]


def sep_parts(pattern):
    """All single-separator-line splits of a pattern.
    -> list of (orientation, sep_color, [part_pattern, ...]) with parts
    in canonical order (top,bottom) / (left,right)."""
    cells = pat_map(pattern)
    H = max(r for r, _ in cells) + 1
    W = max(c for _, c in cells) + 1
    results = []
    for r in range(H):
        row = [cells.get((r, c)) for c in range(W)]
        if all(v is not None for v in row) and len(set(row)) == 1:
            top = {p: col for p, col in cells.items() if p[0] < r}
            bot = {p: col for p, col in cells.items() if p[0] > r}
            if top and bot:
                results.append(("row", row[0],
                                [pat_from_map(top)[0], pat_from_map(bot)[0]]))
    for c in range(W):
        col = [cells.get((r, c)) for r in range(H)]
        if all(v is not None for v in col) and len(set(col)) == 1:
            left = {p: v for p, v in cells.items() if p[1] < c}
            right = {p: v for p, v in cells.items() if p[1] > c}
            if left and right:
                results.append(("col", col[0],
                                [pat_from_map(left)[0], pat_from_map(right)[0]]))
    return results


def color_parts(pattern):
    """Per-color slices: list of (color, part_pattern), colors ascending.
    Only when >=2 colors are present."""
    cells = pat_map(pattern)
    colors = sorted({col for _, _, col in pattern})
    if len(colors) < 2:
        return []
    out = []
    for col in colors:
        sub = {p: v for p, v in cells.items() if v == col}
        out.append((col, pat_from_map(sub)[0]))
    return out


def is_ring(pattern):
    """Single color, cells exactly the border of the pattern's bbox."""
    cells = pat_map(pattern)
    if len({col for _, _, col in pattern}) != 1:
        return False
    H = max(r for r, _ in cells) + 1
    W = max(c for _, c in cells) + 1
    if H < 2 or W < 2:
        return False
    border = {(r, c) for r in range(H) for c in range(W)
              if r in (0, H - 1) or c in (0, W - 1)}
    return set(cells) == border


# ---------------------------------------------------------------- derivations

FIELD_NAMES = {
    "preserve": ["kind", "tau", "phi", "delta"],
    "scale": ["kind", "k", "tau", "phi", "delta"],
    "grow": ["kind", "mode", "tau", "phi", "fill", "delta"],
    "mirror": ["kind", "axis", "tau", "phi", "delta"],
    "split_color": ["kind", "tau", "phi", "delta"],
    "split_sep": ["kind", "tau", "phi", "delta"],
    "merge": ["kind", "parts", "delta"],
    "copy": ["kind", "mode", "tau", "phi", "delta"],
    "frame": ["kind", "margin", "color"],
    # CREATION kinds (diff_field classification only)
    "gather": ["kind", "tau", "phi", "delta"],
    "stroke": ["kind", "phi", "ink", "delta"],
    "stamp": ["kind", "phi", "delta"],
    "stampgrid": ["kind", "phi", "placements", "delta"],
    "rings": ["kind", "radii", "phi", "delta"],
    "inset": ["kind", "phi", "ink", "delta"],
    "count": ["kind", "delta"],
    "texture": ["kind", "phi", "delta"],
    "union": ["kind", "parts", "delta"],
}


def diff_field(va, vb):
    names = FIELD_NAMES.get(va[0], [])
    for i, (x, y) in enumerate(zip(va, vb)):
        if x != y:
            nm = names[i] if i < len(names) else "param"
            return nm if nm in ("tau", "phi", "delta") else "param"
    return "param"


def _deriv(kind, outs, ins, key, value, group=None):
    return {"kind": kind, "outs": outs, "ins": ins, "key": key,
            "value": value, "group": group}


def gen_candidates(in_objs, out_objs, out_shape, deadline, scene=None):
    """-> (cand_by_out, group_sizes) or (None, zero_out_indices).
    cand_by_out: oi -> [derivation]. group_sizes: split group id ->
    number of parts the group must produce. CREATION: `scene`
    ({"grid", "bg_in", "seg"}) enables the creation kinds; the
    original call contract is unchanged when scene is None."""
    cand = {oi: [] for oi in range(len(out_objs))}
    group_sizes = {}
    in_counts = Counter(len(o.pattern) for o in in_objs)

    for oi, oo in enumerate(out_objs):
        lst = cand[oi]
        o_cells = len(oo.pattern)
        for ii, io in enumerate(in_objs):
            delta = (oo.origin[0] - io.origin[0], oo.origin[1] - io.origin[1])
            key_u = None
            # preserve (all taus)
            if len(io.pattern) == o_cells:
                for tau in range(8):
                    tp = transform_pattern(io.pattern, tau)
                    phi = phi_match(tp, oo.pattern)
                    if phi is not None:
                        lst.append(_deriv(
                            "preserve", (oi,), (ii,), ("preserve", io.cls),
                            ("preserve", tau, phi_tuple(phi), delta)))
                # scale down (source bigger)
                for k in (2, 3):
                    dp = scale_down_pat(io.pattern, k)
                    if dp is not None and len(dp) == o_cells:
                        for tau in range(8):
                            tp = transform_pattern(dp, tau)
                            phi = phi_match(tp, oo.pattern)
                            if phi is not None:
                                lst.append(_deriv(
                                    "scale", (oi,), (ii,), ("scale", io.cls),
                                    ("scale", -k, tau, phi_tuple(phi), delta)))
            # scale up (source smaller)
            if o_cells > len(io.pattern):
                for k in (2, 3):
                    up = scale_up_pat(io.pattern, k)
                    if len(up) == o_cells:
                        for tau in range(8):
                            tp = transform_pattern(up, tau)
                            phi = phi_match(tp, oo.pattern)
                            if phi is not None:
                                lst.append(_deriv(
                                    "scale", (oi,), (ii,), ("scale", io.cls),
                                    ("scale", k, tau, phi_tuple(phi), delta)))
                # grow modes
                for mode in ("ring", "holes", "bbox"):
                    for tau in range(8):
                        tp = transform_pattern(io.pattern, tau)
                        m = grow_match(tp, mode, oo.pattern)
                        if m is not None:
                            phi, fill = m
                            lst.append(_deriv(
                                "grow", (oi,), (ii,), ("grow", io.cls),
                                ("grow", mode, tau, phi_tuple(phi), fill,
                                 delta)))
                # mirror completion
                for axis in ("v", "h"):
                    for tau in range(8):
                        tp = transform_pattern(io.pattern, tau)
                        mp = mirror_pat(tp, axis)
                        if mp is not None:
                            phi = phi_match(mp, oo.pattern)
                            if phi is not None:
                                lst.append(_deriv(
                                    "mirror", (oi,), (ii,), ("mirror", io.cls),
                                    ("mirror", axis, tau, phi_tuple(phi),
                                     delta)))
            # split parts (source bigger or equal)
            if len(io.pattern) >= o_cells:
                for c0, part in color_parts(io.pattern):
                    if len(part) == o_cells:
                        for tau in range(8):
                            tp = transform_pattern(part, tau)
                            phi = phi_match(tp, oo.pattern)
                            if phi is not None:
                                grp = (ii, "split_color")
                                group_sizes[grp] = len(color_parts(io.pattern))
                                lst.append(_deriv(
                                    "split_color", (oi,), (ii,),
                                    ("split_color", io.cls, c0),
                                    ("split_color", tau, phi_tuple(phi),
                                     delta), group=grp))
                for orient, scol, parts in sep_parts(io.pattern):
                    for pidx, part in enumerate(parts):
                        if len(part) == o_cells:
                            for tau in range(8):
                                tp = transform_pattern(part, tau)
                                phi = phi_match(tp, oo.pattern)
                                if phi is not None:
                                    grp = (ii, "split_sep", orient, scol)
                                    group_sizes[grp] = len(parts)
                                    lst.append(_deriv(
                                        "split_sep", (oi,), (ii,),
                                        ("split_sep", io.cls, pidx),
                                        ("split_sep", tau, phi_tuple(phi),
                                         delta), group=grp))
            # copy of an input object (non-consuming)
            if len(io.pattern) == o_cells:
                for tau in range(8):
                    tp = transform_pattern(io.pattern, tau)
                    phi = phi_match(tp, oo.pattern)
                    if phi is not None:
                        lst.append(_deriv(
                            "copy", (oi,), (), ("copy", io.cls),
                            ("copy", "in", tau, phi_tuple(phi), delta)))
            _tick(deadline)
        # merge: subsets of 2-3 inputs whose counts sum to o's count
        if 2 <= len(in_objs) <= 9 and o_cells >= 2:
            lst.extend(_merge_candidates(in_objs, out_objs, oi, in_counts,
                                         deadline))
        # copy of another output object (template resolved at extraction)
        for oj, oj_obj in enumerate(out_objs):
            if oj == oi or len(oj_obj.pattern) != o_cells:
                continue
            delta = (oo.origin[0] - oj_obj.origin[0],
                     oo.origin[1] - oj_obj.origin[1])
            for tau in range(8):
                tp = transform_pattern(oj_obj.pattern, tau)
                phi = phi_match(tp, oo.pattern)
                if phi is not None:
                    lst.append(_deriv(
                        "copy", (oi,), (), ("copy_out_ref", oj),
                        ("copy", "out", tau, phi_tuple(phi), delta)))
        # frame creations
        if is_ring(oo.pattern):
            color = oo.pattern[0][2]
            oh, ow = out_shape
            ph = max(r for r, _, _ in oo.pattern) + 1
            pw = max(c for _, c, _ in oo.pattern) + 1
            if oo.origin == (0, 0) and (ph, pw) == (oh, ow):
                lst.append(_deriv(
                    "frame", (oi,), (), ("frame", "canvas"),
                    ("frame", 0, color)))
            cls_count = Counter(o.cls for o in in_objs)
            for ii, io in enumerate(in_objs):
                if cls_count[io.cls] != 1:
                    continue
                ih = max(r for r, _, _ in io.pattern) + 1
                iw = max(c for _, c, _ in io.pattern) + 1
                for m in (0, 1):
                    if (ph, pw) == (ih + 2 * m, iw + 2 * m):
                        lst.append(_deriv(
                            "frame", (oi,), (), ("frame", io.cls),
                            ("frame", m, color)))
        # dedup + cap
        seen = set()
        ded = []
        for d in lst:
            sig = (d["kind"], d["outs"], d["ins"], str(d["key"]),
                   str(d["value"]), str(d["group"]))
            if sig not in seen:
                seen.add(sig)
                ded.append(d)
        cand[oi] = ded[:CAND_CAP_PER_OUT]
    # CREATION candidates (spec strata 2-3): generated ONLY for
    # output objects with zero standard candidates (the
    # creation_unexplained wall), appended after the existing kinds,
    # deduped against them, under the same cap. Outputs the standard
    # kinds already explain never pay creation cost — this keeps the
    # bg lane's per-pair timing (and its budget profile) intact on
    # every pair the creation machinery does not address.
    zero = [oi for oi in range(len(out_objs)) if not cand[oi]]
    if scene is not None and zero:
        ccand = _creation_candidates(in_objs, out_objs, out_shape,
                                     deadline, scene,
                                     only=frozenset(zero))
        for oi in zero:
            if not ccand[oi]:
                continue
            seen = {(d["kind"], d["outs"], d["ins"], str(d["key"]),
                     str(d["value"]), str(d["group"])) for d in cand[oi]}
            lst = list(cand[oi])
            for d in ccand[oi]:
                sig = (d["kind"], d["outs"], d["ins"], str(d["key"]),
                       str(d["value"]), str(d["group"]))
                if sig not in seen:
                    seen.add(sig)
                    lst.append(d)
            cand[oi] = lst[:CAND_CAP_PER_OUT]
        # copy_out_ref hazard: pair_assignments (byte-protected)
        # resolves a copy source through in_objs[src.ins[0]], which
        # an ins=() creation derivation has no anchor for. Drop any
        # copy_out_ref derivation whose TARGET output now carries a
        # creation (ins == (), non-copy/frame) candidate.
        creation_targets = set()
        for oi in zero:
            if any(d["ins"] == () and d["kind"] not in ("copy", "frame")
                   for d in cand[oi]):
                creation_targets.add(oi)
        if creation_targets:
            for oi2 in range(len(out_objs)):
                cand[oi2] = [d for d in cand[oi2]
                             if not (d["key"][0] == "copy_out_ref"
                                     and d["key"][1]
                                     in creation_targets)]
    zero = [oi for oi in range(len(out_objs)) if not cand[oi]]
    if zero:
        return None, zero
    # CREATION M-P(i): split groups are NOT pruned when a sibling part
    # has no candidate (split-and-discard). The kept set is the parts
    # with candidates, computed identically in _group_needs; a group
    # with no surviving part has no derivations left to strip.
    return cand, None


def _merge_candidates(in_objs, out_objs, oi, in_counts, deadline):
    oo = out_objs[oi]
    target = len(oo.pattern)
    omap = pat_map(oo.pattern)
    out = []
    idxs = list(range(len(in_objs)))
    subsets = []
    for a in range(len(idxs)):
        for b in range(a + 1, len(idxs)):
            s2 = (len(in_objs[idxs[a]].pattern)
                  + len(in_objs[idxs[b]].pattern))
            if s2 == target:
                subsets.append((idxs[a], idxs[b]))
            for c in range(b + 1, len(idxs)):
                s3 = s2 + len(in_objs[idxs[c]].pattern)
                if s3 == target:
                    subsets.append((idxs[a], idxs[b], idxs[c]))
    for S in subsets[:40]:
        _tick(deadline)
        parts = [in_objs[i] for i in S]
        placed = []  # (in_idx, tau, origin_offset, phi)

        def rec(pi, remaining):
            if len(out) >= MERGE_CAND_CAP:
                return
            if pi == len(parts):
                if not remaining:
                    raw = [(in_objs[i2].cls, tau, off, phi_tuple(phi), i2)
                           for (i2, tau, off, phi) in placed]
                    raw.sort(key=lambda e: (str(e[0]), e[2]))
                    anchor_cls, anch_i = raw[0][0], raw[0][4]
                    delta = (oo.origin[0] - in_objs[anch_i].origin[0],
                             oo.origin[1] - in_objs[anch_i].origin[1])
                    entries = tuple((c, t, o, p) for (c, t, o, p, _i)
                                    in raw)
                    key = ("merge",
                           tuple(sorted((in_objs[i].cls for i in S),
                                        key=str)), anchor_cls)
                    value = ("merge", entries, delta)
                    out.append(_deriv("merge", (oi,), tuple(S), key, value))
                return
            io = parts[pi]
            i_idx = S[pi]
            cells = [(r, c) for r, c, _ in io.pattern]
            for tau in range(8):
                tp = transform_pattern(io.pattern, tau)
                tmap = pat_map(tp)
                # candidate offsets: align a tp cell to a remaining cell
                anch = next(iter(tmap))
                offs = set()
                for (rr, cc) in remaining:
                    offs.add((rr - anch[0], cc - anch[1]))
                for off in offs:
                    ok = True
                    phi = {}
                    newrem = dict(remaining)
                    for (r, c), col in tmap.items():
                        pos = (r + off[0], c + off[1])
                        oc = remaining.get(pos)
                        if oc is None:
                            ok = False
                            break
                        if phi.get(col, oc) != oc:
                            ok = False
                            break
                        phi[col] = oc
                    if not ok:
                        continue
                    for (r, c) in tmap:
                        newrem.pop((r + off[0], c + off[1]), None)
                    placed.append((i_idx, tau, off, phi))
                    rec(pi + 1, newrem)
                    placed.pop()
                    if len(out) >= MERGE_CAND_CAP:
                        return
        rec(0, dict(omap))
    return out


# ------------------------------------------------------- CREATION machinery
# Per CREATION_MACHINERY_SPEC_2026-11-07.md. A creation pattern is a
# normalized tuple of (r, c, color|None) plus its absolute origin in
# the scene (input) grid, regenerated from any grid by descriptor:
# generation time and render time share the code path, so a binding's
# rendering is the same scene function that generated it. None marks
# an ink slot — cells taking a single observed color, bound in the
# derivation value (the spec's instance colors; never through the
# global phi).

def _sign(x):
    return (x > 0) - (x < 0)


def _obj_center_abs(o):
    rs = [o.origin[0] + r for r, _, _ in o.pattern]
    cs = [o.origin[1] + c for _, c, _ in o.pattern]
    return ((min(rs) + max(rs)) // 2, (min(cs) + max(cs)) // 2)


def _match_creation(pattern, oo):
    """-> (phi, ink) if pattern matches output object oo exactly:
    same normalized cell set, colored cells functional under phi,
    None cells a single ink color. Else None."""
    if len(pattern) != len(oo.pattern):
        return None
    omap = pat_map(oo.pattern)
    phi = {}
    ink = None
    for r, c, col in pattern:
        oc = omap.get((r, c))
        if oc is None:
            return None
        if col is None:
            if ink is None:
                ink = oc
            elif ink != oc:
                return None
        else:
            if phi.get(col, oc) != oc:
                return None
            phi[col] = oc
    return phi, ink


def _ray_cells(grid, bg_in, obj, drc, extent):
    """Lattice ray cells (absolute coords -> None) starting just
    outside obj's bbox in direction drc. extent 'edge' runs to the
    grid border; 'obstacle' stops before the first non-bg cell not
    belonging to obj. Exact lattice rasterization (8 directions)."""
    H, W = gshape(grid)
    dr, dc = drc
    rs = [obj.origin[0] + r for r, _, _ in obj.pattern]
    cs = [obj.origin[1] + c for _, c, _ in obj.pattern]
    sr = max(rs) if dr > 0 else (min(rs) if dr < 0
                                 else (min(rs) + max(rs)) // 2)
    sc = max(cs) if dc > 0 else (min(cs) if dc < 0
                                 else (min(cs) + max(cs)) // 2)
    own = {(obj.origin[0] + r, obj.origin[1] + c)
           for r, c, _ in obj.pattern}
    cells = {}
    r, c = sr + dr, sc + dc
    while 0 <= r < H and 0 <= c < W:
        if extent == "obstacle" and grid[r][c] != bg_in \
                and (r, c) not in own:
            break
        cells[(r, c)] = None
        r += dr
        c += dc
    return cells


def _scene_pattern(desc, grid, bg_in, objs):
    """Scene/class-level creation patterns -> (pattern, origin) or
    None. desc: ("gather", color) | ("crossA", cls) |
    ("rings", center_cls, _seq, radii) | ("count", color)."""
    kind = desc[0]
    H, W = gshape(grid)
    if kind == "gather":
        color = desc[1]
        cells = {}
        for r in range(H):
            row = grid[r]
            for c in range(W):
                if row[c] == color:
                    cells[(r, c)] = color
        if len(cells) < 8:  # spec M-G cap
            return None
        return pat_from_map(cells)
    if kind == "crossA":
        # Axis lines through the bbox centers of ALL instances of the
        # class, minus the anchor instances' own cells (those are the
        # union's object parts). M-L/M-U part source.
        cls = desc[1]
        own = set()
        centers = []
        for o in objs:
            if o.cls == cls:
                centers.append(_obj_center_abs(o))
                own.update((o.origin[0] + r, o.origin[1] + c)
                           for r, c, _ in o.pattern)
        if not centers:
            return None
        cells = {}
        for cr, cc in centers:
            for c in range(W):
                if (cr, c) not in own:
                    cells[(cr, c)] = None
            for r in range(H):
                if (r, cc) not in own:
                    cells[(r, cc)] = None
        if not cells:
            return None
        return pat_from_map(cells)
    if kind == "rings":
        _, center_cls, _seq, radii = desc
        insts = [o for o in objs if o.cls == center_cls]
        if len(insts) != 1:
            return None
        cr, cc = _obj_center_abs(insts[0])
        cells = {}
        for i, rad in enumerate(radii):
            for r in range(cr - rad, cr + rad + 1):
                for c in range(cc - rad, cc + rad + 1):
                    if max(abs(r - cr), abs(c - cc)) == rad \
                            and 0 <= r < H and 0 <= c < W:
                        cells[(r, c)] = ("ring", i)
        if not cells:
            return None
        return pat_from_map(cells)
    if kind == "countstack":
        # M-C: the count-shape family as measured on the spent draw:
        # the scene's total non-bg cell count T is a perfect odd
        # sum (T = m^2); the output is the staircase of horizontal
        # bars of widths 2m-1, ..., 3, 1 stacked at the canvas
        # bottom, widest at the bottom. A single scene color takes
        # every bar; with several colors, each color's count must
        # equal exactly one bar width and takes that bar, centered
        # on the color's modal column (ties: smallest column).
        # (The spec's one-color filled triangle is the m-bar case.)
        per_color = {}
        total = 0
        for color in sorted({v for row in grid for v in row}):
            if color == bg_in:
                continue
            pts = [(r, c) for r in range(H) for c in range(W)
                   if grid[r][c] == color]
            if not pts:
                continue
            colcount = Counter(c for _, c in pts)
            top = max(colcount.values())
            ccol = min(c for c, k in colcount.items() if k == top)
            per_color[color] = (len(pts), ccol)
            total += len(pts)
        if not per_color:
            return None
        m = int(total ** 0.5)
        if m * m != total:
            return None
        widths = [2 * i - 1 for i in range(m, 0, -1)]
        if len(per_color) == 1:
            only = next(iter(per_color))
            bar_color = {w: only for w in widths}
        else:
            if sorted(n for n, _ in per_color.values()) \
                    != sorted(widths):
                return None
            bar_color = {}
            for color, (n, _cc) in per_color.items():
                bar_color[n] = color
        cells = {}
        for j, w in enumerate(widths):
            color = bar_color[w]
            ccol = per_color[color][1]
            r = (H - 1) - j
            lo = ccol - (w - 1) // 2
            for c in range(lo, lo + w):
                if 0 <= r < H and 0 <= c < W:
                    cells[(r, c)] = color
        if len(cells) != total:
            return None
        return pat_from_map(cells)
    if kind == "checker":
        # M-T: the cells of one parity class of an exactly-two-color
        # grid, colored with desc's color (the (0,0) color owns the
        # even parity class).
        color = desc[1]
        cols = {v for row in grid for v in row}
        if len(cols) != 2 or color not in cols:
            return None
        par = 0 if color == grid[0][0] else 1
        cells = {(r, c): color for r in range(H) for c in range(W)
                 if (r + c) % 2 == par}
        if not cells:
            return None
        return pat_from_map(cells)
    if kind == "linesA":
        # M-L: full lines through the bbox centers of ALL instances
        # of the class, along the descriptor's axis set (cells are
        # ink slots; anchor cells on a line stay in the pattern).
        cls, axes = desc[1], desc[2]
        centers = [_obj_center_abs(o) for o in objs if o.cls == cls]
        if not centers:
            return None
        cells = {}
        for cr, cc in centers:
            for (dr, dc) in axes:
                r, c = cr, cc
                while 0 <= r < H and 0 <= c < W:
                    cells[(r, c)] = None
                    r += dr
                    c += dc
                r, c = cr - dr, cc - dc
                while 0 <= r < H and 0 <= c < W:
                    cells[(r, c)] = None
                    r -= dr
                    c -= dc
        if not cells:
            return None
        return pat_from_map(cells)
    if kind == "part":
        # A color part of the (unique) instance of a parent class,
        # as an absolute pattern. M-U part source.
        _, parent_cls, color = desc
        insts = [o for o in objs if o.cls == parent_cls]
        if len(insts) != 1:
            return None
        o = insts[0]
        cells = {(o.origin[0] + r, o.origin[1] + c): col
                 for r, c, col in o.pattern if col == color}
        if not cells:
            return None
        return pat_from_map(cells)
    if kind == "stamp":
        # Scene-level stamp of a color part (M-U part source):
        # only the reflected mode is offered at scene level.
        _, src_desc, mode, params = desc
        if src_desc[0] != "part" or mode != "reflect":
            return None
        r = _scene_pattern(src_desc, grid, bg_in, objs)
        if r is None:
            return None
        pat, org = r
        src = {(org[0] + rr, org[1] + cc): col
               for rr, cc, col in pat}
        cells = dict(src)
        rs = [x for x, _ in src]
        cs = [x for _, x in src]
        side = params
        for (x, y), col in src.items():
            if side == "right":
                pos = (x, 2 * max(cs) + 1 - y)
            elif side == "left":
                pos = (x, 2 * min(cs) - 1 - y)
            elif side == "bottom":
                pos = (2 * max(rs) + 1 - x, y)
            else:
                pos = (2 * min(rs) - 1 - x, y)
            if not (0 <= pos[0] < H and 0 <= pos[1] < W):
                return None
            if pos in cells and cells[pos] != col:
                return None
            cells[pos] = col
        if len(cells) == len(src):
            return None
        return pat_from_map(cells)
    return None


def _inst_pattern(desc, grid, bg_in, objs, inst):
    """Instance-level creation patterns anchored at objs[inst] ->
    (pattern, origin) or None. desc: ("cross1", cls, incl) |
    ("ray1", cls, drc, extent, incl) | ("ray2", clsA, clsB, incl) |
    ("inset", cls) | ("stamp", src_cls, mode, params)."""
    kind = desc[0]
    H, W = gshape(grid)
    o = objs[inst]
    if kind == "cross1":
        _, _cls, incl = desc
        cr, cc = _obj_center_abs(o)
        cells = {}
        for c in range(W):
            cells[(cr, c)] = None
        for r in range(H):
            cells[(r, cc)] = None
        if incl:
            for r, c, col in o.pattern:
                cells[(o.origin[0] + r, o.origin[1] + c)] = col
        return pat_from_map(cells)
    if kind == "ray1":
        _, _cls, drc, extent, incl = desc
        cells = _ray_cells(grid, bg_in, o, drc, extent)
        if incl:
            for r, c, col in o.pattern:
                cells[(o.origin[0] + r, o.origin[1] + c)] = col
        if not cells:
            return None
        return pat_from_map(cells)
    if kind == "ray2":
        _, _clsA, clsB, incl = desc
        B = [x for x in objs if x.cls == clsB]
        if len(B) != 1:
            return None
        ca = _obj_center_abs(o)
        cb = _obj_center_abs(B[0])
        drc = (_sign(cb[0] - ca[0]), _sign(cb[1] - ca[1]))
        if drc == (0, 0):
            return None
        cells = _ray_cells(grid, bg_in, o, drc, "edge")
        if incl:
            for r, c, col in o.pattern:
                cells[(o.origin[0] + r, o.origin[1] + c)] = col
        if not cells:
            return None
        return pat_from_map(cells)
    if kind == "inset":
        # M-F(ii): the object's cells with its whole margin-1
        # interior rectangle overwritten as ink slots (the inset
        # rectangle is recolored wholesale, as measured on the spent
        # draw: a 5x5 block's full 3x3 interior takes the ink).
        cells = pat_map(o.pattern)
        H2 = max(r for r, _ in cells) + 1
        W2 = max(c for _, c in cells) + 1
        if H2 < 3 or W2 < 3:
            return None
        out = {(o.origin[0] + r, o.origin[1] + c): col
               for (r, c), col in cells.items()}
        marked = 0
        for r in range(1, H2 - 1):
            for c in range(1, W2 - 1):
                pos = (o.origin[0] + r, o.origin[1] + c)
                out[pos] = None
                marked += 1
        if not marked:
            return None
        return pat_from_map(out)
    if kind == "line1":
        # M-L: the full line through the instance's bbox center
        # along drc (both directions, to the grid edge).
        _, _cls, drc, incl = desc
        cr, cc = _obj_center_abs(o)
        dr, dc = drc
        cells = {}
        r, c = cr, cc
        while 0 <= r < H and 0 <= c < W:
            cells[(r, c)] = None
            r += dr
            c += dc
        r, c = cr - dr, cc - dc
        while 0 <= r < H and 0 <= c < W:
            cells[(r, c)] = None
            r -= dr
            c -= dc
        if incl:
            for rr, cc2, col in o.pattern:
                cells[(o.origin[0] + rr, o.origin[1] + cc2)] = col
        if not cells:
            return None
        return pat_from_map(cells)
    if kind == "stamp":
        _, _src_cls, mode, params = desc
        src = {(o.origin[0] + r, o.origin[1] + c): col
               for r, c, col in o.pattern}
        cells = dict(src)
        if mode == "reflect":
            # M-R(iv): source + its mirror across a bbox edge axis.
            side = params
            rs = [r for r, _ in src]
            cs = [c for _, c in src]
            for (r, c), col in src.items():
                if side == "right":
                    pos = (r, 2 * max(cs) + 1 - c)
                elif side == "left":
                    pos = (r, 2 * min(cs) - 1 - c)
                elif side == "bottom":
                    pos = (2 * max(rs) + 1 - r, c)
                else:
                    pos = (2 * min(rs) - 1 - r, c)
                if not (0 <= pos[0] < H and 0 <= pos[1] < W):
                    return None
                if pos in cells and cells[pos] != col:
                    return None
                cells[pos] = col
            if len(cells) == len(src):
                return None
            return pat_from_map(cells)
        if mode == "lattice":
            # M-R(i): all in-canvas translates by the bound period
            # vector (both signs); a translate that would recolor a
            # placed cell differently is excluded.
            dr, dc = params
            if (dr, dc) == (0, 0):
                return None
            for sgn in (1, -1):
                k = 1
                while k <= 64:
                    sh = {(r + sgn * k * dr, c + sgn * k * dc): col
                          for (r, c), col in src.items()}
                    if any(not (0 <= r < H and 0 <= c < W)
                           for r, c in sh):
                        break
                    if any(pos in cells and cells[pos] != col
                           for pos, col in sh.items()):
                        k += 1
                        continue
                    cells.update(sh)
                    k += 1
            if len(cells) == len(src):
                return None
            return pat_from_map(cells)
        if mode == "markers":
            # M-R(ii): copies placed so the source's bbox cell `ref`
            # sits on each marker instance's origin; a copy is
            # suppressed when any of its cells would land on a non-bg
            # scene cell outside the source and marker cells.
            marker_cls, ref = params
            src_cells = set(src)
            marker_cells = set()
            for m in objs:
                if m.cls == marker_cls:
                    marker_cells.update(
                        (m.origin[0] + r, m.origin[1] + c)
                        for r, c, _ in m.pattern)
            for m in objs:
                if m.cls != marker_cls:
                    continue
                org = (m.origin[0] - ref[0], m.origin[1] - ref[1])
                sh = {(org[0] + r, org[1] + c): col
                      for r, c, col in o.pattern}
                if any(not (0 <= r < H and 0 <= c < W)
                       for r, c in sh):
                    continue
                if any(grid[r][c] != bg_in and (r, c) not in src_cells
                       and (r, c) not in marker_cells
                       for r, c in sh):
                    continue
                if any(pos in cells and cells[pos] != col
                       for pos, col in sh.items()):
                    continue
                cells.update(sh)
            if len(cells) == len(src):
                return None
            return pat_from_map(cells)
    return None


def _stampgrid_candidates(grid, oo, oi, deadline):
    """M-R(iii) enumerated: tilings of the output object by exact
    translates of the whole input grid (the grid-as-pattern stamp).
    Placements are recorded in the value, in output-object
    coordinates; the binding's delta is the object's origin."""
    H, W = gshape(grid)
    n = H * W
    total = len(oo.pattern)
    if total == 0 or total % n != 0:
        return []
    k = total // n
    if k > 4:
        return []
    target = pat_map(oo.pattern)
    src = {(r, c): grid[r][c] for r in range(H) for c in range(W)}
    out = []
    state = {"nodes": 0}

    def rec(remaining, phi, placed):
        if len(out) >= 4 or state["nodes"] > 2000:
            return
        state["nodes"] += 1
        if not remaining:
            if len(placed) == k:
                out.append(_deriv(
                    "stampgrid", (oi,), (), ("stampgrid",),
                    ("stampgrid", phi_tuple(phi),
                     tuple(sorted(placed)), oo.origin)))
            return
        if len(placed) == k:
            return
        _tick(deadline)
        fr, fc = next(iter(remaining))
        cand_orgs = {(fr - r, fc - c) for (r, c) in src}
        for org in sorted(cand_orgs):
            nphi = dict(phi)
            covered = []
            ok = True
            for (r, c), col in src.items():
                pos = (r + org[0], c + org[1])
                oc = remaining.get(pos)
                if oc is None or nphi.get(col, oc) != oc:
                    ok = False
                    break
                nphi[col] = oc
                covered.append(pos)
            if not ok:
                continue
            nrem = dict(remaining)
            for pos in covered:
                nrem.pop(pos, None)
            placed.append(org)
            rec(nrem, nphi, placed)
            placed.pop()
            if len(out) >= 4:
                return

    rec(dict(target), {}, [])
    return out


def _union_candidates(in_objs, out_objs, oi, virts, deadline):
    """M-U: exact tilings of out_objs[oi] by 2-3 parts with at least
    one virtual (creation) part; part proposals come only from input
    objects and scene-generated creation patterns (never subset
    enumeration of the output). Pure-object tilings are the merge
    kind's territory and are skipped. virts: (desc, pattern, origin,
    consume_idx_or_None).

    Search: exact-cover recursion anchored on a fixed uncovered
    cell (the row-major smallest), parts tried virtual-first then
    largest-first, an exactly-k subset-sum feasibility sieve over
    part counts, and a hard node cap — the first build's free
    subset/placement enumeration was the lane's whole budget on
    dense scenes (profiled 24.96 s of a 25 s task), so the search
    discipline is part of the machinery here."""
    oo = out_objs[oi]
    target = len(oo.pattern)
    if target < 2 or not virts:
        return []
    omap = pat_map(oo.pattern)
    parts = []  # (desc_key, pattern, scene_origin, consume, is_virt)
    for desc, pat, org, cons in virts:
        parts.append((("virt", desc), pat, org, cons, True))
    for ii, io in enumerate(in_objs):
        parts.append((("obj", io.cls), io.pattern, io.origin, ii,
                      False))
    # part-count sieve: sums formable by exactly k parts
    counts = [len(p[1]) for p in parts]
    A = [set() for _ in range(4)]
    A[0] = {0}
    for cn in counts:
        for k in (3, 2, 1):
            A[k] |= {s + cn for s in A[k - 1]}
    if target not in A[2] and target not in A[3]:
        return []
    order0 = sorted(range(len(parts)),
                    key=lambda pi: (not parts[pi][4],
                                    -len(parts[pi][1])))
    out = []
    used = [False] * len(parts)
    nodes = [0]
    NODE_CAP = 20000

    def emit(chosen):
        raw = sorted(chosen, key=lambda e: (str(e[0]), e[2]))
        anchor = raw[0]
        delta = (oo.origin[0] - anchor[5][0],
                 oo.origin[1] - anchor[5][1])
        entries = tuple((dk, tau, off, phi_tuple(phi), ink)
                        for (dk, tau, off, phi, ink, _o, _c) in raw)
        key = ("union", tuple(sorted((e[0] for e in raw), key=str)),
               anchor[0])
        ins = tuple(sorted({e[6] for e in raw if e[6] is not None}))
        out.append(_deriv("union", (oi,), ins, key,
                          ("union", entries, delta)))

    def rec(remaining, chosen, has_virt):
        if len(out) >= MERGE_CAND_CAP or nodes[0] > NODE_CAP:
            return
        nodes[0] += 1
        if nodes[0] % 2048 == 0:
            _tick(deadline)
        if not remaining:
            if len(chosen) >= 2 and has_virt:
                emit(chosen)
            return
        depth = len(chosen)
        if depth == 3:
            return
        rem = len(remaining)
        if not any(rem in A[k]
                   for k in range(max(1, 2 - depth), 4 - depth)):
            return
        q = min(remaining)
        for pi in order0:
            if used[pi]:
                continue
            dk, pat, org, cons, isv = parts[pi]
            if len(pat) > rem:
                continue
            if depth == 2 and len(pat) != rem:
                continue
            taus = (0,) if isv else range(8)
            for tau in taus:
                tp = pat if tau == 0 else transform_pattern(pat, tau)
                for (pr, pc, _col) in tp:
                    off = (q[0] - pr, q[1] - pc)
                    phi = {}
                    ink = None
                    ok = True
                    for (r, c, col) in tp:
                        oc = remaining.get((r + off[0], c + off[1]))
                        if oc is None:
                            ok = False
                            break
                        if col is None:
                            if ink is None:
                                ink = oc
                            elif ink != oc:
                                ok = False
                                break
                        elif phi.get(col, oc) != oc:
                            ok = False
                            break
                        else:
                            phi[col] = oc
                    if not ok:
                        continue
                    newrem = dict(remaining)
                    for (r, c, _col) in tp:
                        newrem.pop((r + off[0], c + off[1]), None)
                    used[pi] = True
                    chosen.append((dk, tau, off, phi, ink, org, cons))
                    rec(newrem, chosen, has_virt or isv)
                    chosen.pop()
                    used[pi] = False
                    if len(out) >= MERGE_CAND_CAP \
                            or nodes[0] > NODE_CAP:
                        return

    rec(dict(omap), [], False)
    return out


def _creation_candidates(in_objs, out_objs, out_shape, deadline,
                         scene, only=None):
    """Creation-kind candidate derivations per output object
    (strata 2-3), including M-U unions. Existing kinds are generated
    by the caller; these are appended after them. only: if given,
    candidates are matched only for those output indices (the
    zero-standard-candidate outputs)."""
    grid, bg_in = scene["grid"], scene["bg_in"]
    objs = in_objs
    cand = {oi: [] for oi in range(len(out_objs))}
    scache = {}
    icache = {}

    def scene_pat(desc):
        if desc not in scache:
            scache[desc] = _scene_pattern(desc, grid, bg_in, objs)
        return scache[desc]

    def inst_pat(desc, ii):
        kk = (desc, ii)
        if kk not in icache:
            icache[kk] = _inst_pattern(desc, grid, bg_in, objs, ii)
        return icache[kk]

    offers = []  # (pattern, origin, ins, key, valfn(phi, ink, delta))
    colors = sorted({v for row in grid for v in row})
    # M-G gather: CUT under kill criterion 5 after the spent-draw
    # run (unblocked 0 of its class's tasks; see
    # CREATION_BUILD_RESULTS_2026-11-07.md). The scene pattern
    # itself remains for the census instruments; it is offered
    # neither as a derivation nor as a union part.
    classes = []
    for o in objs:
        if o.cls not in classes:
            classes.append(o.cls)
    uniq = [c for c in classes
            if sum(1 for o in objs if o.cls == c) == 1]
    dirs8 = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1),
             (-1, 1), (-1, -1)]
    axes4 = [(1, 1), (1, -1), (1, 0), (0, 1)]
    # M-L strokes: instance crosses, rays and full lines
    # (deduplicated by (pattern, ins) — the first descriptor wins
    # deterministically). Cost cap: skip objects over 40 cells.
    seen_pat = set()
    for ii, o in enumerate(objs):
        if len(o.pattern) > 40:
            continue
        descs = [("cross1", o.cls, incl) for incl in (False, True)]
        for drc in dirs8:
            for extent in ("edge", "obstacle"):
                for incl in (False, True):
                    descs.append(("ray1", o.cls, drc, extent, incl))
        for drc in axes4:
            for incl in (False, True):
                descs.append(("line1", o.cls, drc, incl))
        for desc in descs:
            r = inst_pat(desc, ii)
            if r is None:
                continue
            pat, org = r
            incl = desc[-1]
            sig = (pat, (ii,) if incl else ())
            if sig in seen_pat:
                continue
            seen_pat.add(sig)
            offers.append((pat, org, (ii,) if incl else (),
                           ("stroke", o.cls if incl else None, desc),
                           lambda phi, ink, delta:
                           ("stroke", phi_tuple(phi), ink, delta)))
    # M-L rays toward a second anchor (unique-instance classes)
    for clsA in uniq:
        ii = next(i for i, o in enumerate(objs) if o.cls == clsA)
        for clsB in uniq:
            if clsB == clsA:
                continue
            for incl in (False, True):
                desc = ("ray2", clsA, clsB, incl)
                r = inst_pat(desc, ii)
                if r is None:
                    continue
                pat, org = r
                sig = (pat, (ii,) if incl else ())
                if sig in seen_pat:
                    continue
                seen_pat.add(sig)
                offers.append((pat, org, (ii,) if incl else (),
                               ("stroke", clsA if incl else None, desc),
                               lambda phi, ink, delta:
                               ("stroke", phi_tuple(phi), ink, delta)))
    # M-L scene lines through all instances of a class
    for cls in classes:
        for axes in [((1, 1),), ((1, -1),), ((1, 0),), ((0, 1),),
                     ((1, 1), (1, -1)), ((1, 0), (0, 1))]:
            desc = ("linesA", cls, axes)
            r = scene_pat(desc)
            if r is None:
                continue
            pat, org = r
            offers.append((pat, org, (), ("stroke", None, desc),
                           lambda phi, ink, delta:
                           ("stroke", phi_tuple(phi), ink, delta)))
    _tick(deadline)
    # M-R stamp (object sources). Cost caps: reflect/lattice skip
    # sources over 30 cells; the marker mode enumerates placements
    # only for small sources (bbox area <= 12, <= 12 cells) and only
    # on scenes with <= 10 objects.
    for ii, o in enumerate(objs):
        bh = max(r for r, _, _ in o.pattern) + 1
        bw = max(c for _, c, _ in o.pattern) + 1
        descs = []
        if len(o.pattern) <= 30:
            descs += [("stamp", o.cls, "reflect", side)
                      for side in ("right", "left", "bottom", "top")]
            periods = {(bh, 0), (0, bw), (bh, bw), (bh, -bw),
                       (-bh, bw)}
            for jj, o2 in enumerate(objs):
                if o2.cls == o.cls and jj != ii:
                    periods.add((o2.origin[0] - o.origin[0],
                                 o2.origin[1] - o.origin[1]))
            for per in sorted(periods):
                if per != (0, 0):
                    descs.append(("stamp", o.cls, "lattice", per))
        if bh * bw <= 12 and len(o.pattern) <= 12                 and len(objs) <= 10:
            refs = [(r, c) for r, c, _ in o.pattern]
            for mcls in classes:
                if mcls == o.cls:
                    continue
                for ref in refs:
                    descs.append(("stamp", o.cls, "markers",
                                  (mcls, ref)))
        for desc in descs:
            r = inst_pat(desc, ii)
            if r is None:
                continue
            pat, org = r
            if len(pat) <= len(o.pattern):
                continue
            offers.append((pat, org, (ii,), ("stamp", desc),
                           lambda phi, ink, delta:
                           ("stamp", phi_tuple(phi), delta)))
    _tick(deadline)
    # M-F(ii) inset
    for ii, o in enumerate(objs):
        r = inst_pat(("inset", o.cls), ii)
        if r is None:
            continue
        pat, org = r
        offers.append((pat, org, (ii,), ("inset", o.cls),
                       lambda phi, ink, delta:
                       ("inset", phi_tuple(phi), ink, delta)))
    # M-F(i) iterated rings (color sequence bound in the value)
    for ccls in uniq:
        for start in (1, 2, 3):
            for cnt in (1, 2, 3):
                radii = tuple(range(start, start + cnt))
                r = scene_pat(("rings", ccls, None, radii))
                if r is None:
                    continue
                pat, org = r
                offers.append((pat, org, (), ("rings", ccls),
                               lambda phi, ink, delta, radii=radii:
                               ("rings", radii,
                                tuple(phi[("ring", i)]
                                      for i in range(len(radii))),
                                delta)))
    # M-C count-shape (whole-scene bar stack)
    r = scene_pat(("countstack",))
    if r is not None:
        pat, org = r
        offers.append((pat, org, (), ("count", "stack"),
                       lambda phi, ink, delta:
                       ("count", delta)))
    # M-T checkerboard texture (pattern derivation over the parity
    # class of an exactly-two-color scene)
    if len(colors) == 2:
        for color in colors:
            if color == bg_in:
                continue
            r = scene_pat(("checker", color))
            if r is None:
                continue
            pat, org = r
            offers.append((pat, org, (), ("texture", color),
                           lambda phi, ink, delta:
                           ("texture", phi_tuple(phi), delta)))
    # match offers against output objects
    for oi, oo in enumerate(out_objs):
        if only is not None and oi not in only:
            continue
        lst = cand[oi]
        for pat, org, ins, key, valfn in offers:
            if len(pat) != len(oo.pattern):
                continue
            m = _match_creation(pat, oo)
            if m is None:
                continue
            phi, ink = m
            if key == ("count", "stack") and (
                    ink is not None
                    or any(a != b for a, b in phi.items())):
                # the count value carries no phi (the stack's colors
                # are the scene's own, bound by construction); a
                # recolored stack is a different derivation's work
                continue
            delta = (oo.origin[0] - org[0], oo.origin[1] - org[1])
            lst.append(_deriv(key[0], (oi,), ins, key,
                              valfn(phi, ink, delta)))
        lst.extend(_stampgrid_candidates(grid, oo, oi, deadline))
        _tick(deadline)
    # M-U unions over virtual part sources:
    # (desc, pattern, scene origin, consume index or None)
    virts = []
    for cls in classes:
        r = scene_pat(("crossA", cls))
        if r is not None:
            virts.append((("crossA", cls), r[0], r[1], None))
        for axes in [((1, 1),), ((1, -1),), ((1, 0),), ((0, 1),),
                     ((1, 1), (1, -1)), ((1, 0), (0, 1))]:
            desc = ("linesA", cls, axes)
            r = scene_pat(desc)
            if r is not None:
                virts.append((desc, r[0], r[1], None))
    # instance-anchored stroke parts: only the first instance (in
    # origin order) of each class supplies the recorded pattern, so
    # render-time pool selection reproduces it.
    first_of_cls = {}
    for ii, o in enumerate(objs):
        cur = first_of_cls.get(o.cls)
        if cur is None or o.origin < objs[cur].origin:
            first_of_cls[o.cls] = ii
    for cls, ii in first_of_cls.items():
        o = objs[ii]
        if len(o.pattern) > 40:
            continue
        descs = [("cross1", cls, incl) for incl in (False, True)]
        for drc in dirs8:
            for incl in (False, True):
                descs.append(("ray1", cls, drc, "edge", incl))
        for drc in axes4:
            for incl in (False, True):
                descs.append(("line1", cls, drc, incl))
        for clsB in uniq:
            if clsB != cls:
                for incl in (False, True):
                    descs.append(("ray2", cls, clsB, incl))
        for desc in descs:
            r = inst_pat(desc, ii)
            if r is None:
                continue
            incl = bool(desc[-1])
            virts.append((desc, r[0], r[1], ii if incl else None))
    # color parts of a unique parent instance, and their reflected
    # stamps (split-part sources)
    for cls in uniq:
        ii = next(i for i, o in enumerate(objs) if o.cls == cls)
        o = objs[ii]
        partcols = sorted({col for _, _, col in o.pattern})
        if len(partcols) < 2:
            continue
        for pc in partcols:
            desc = ("part", cls, pc)
            r = scene_pat(desc)
            if r is None:
                continue
            virts.append((desc, r[0], r[1], ii))
            for side in ("right", "left", "bottom", "top"):
                sdesc = ("stamp", desc, "reflect", side)
                r2 = scene_pat(sdesc)
                if r2 is not None:
                    virts.append((sdesc, r2[0], r2[1], ii))
    for oi in range(len(out_objs)):
        if only is not None and oi not in only:
            continue
        cand[oi].extend(_union_candidates(in_objs, out_objs, oi,
                                          virts, deadline))
    return cand


# ---------------------------------------------------------------- cover

def _fate_of(d, in_objs):
    """(cls, fate descriptor) pairs a derivation imposes by consuming."""
    k = d["kind"]
    if k in ("preserve", "scale", "grow", "mirror"):
        return [(in_objs[d["ins"][0]].cls, ("unary", k))]
    if k in ("split_color", "split_sep"):
        return [(in_objs[d["ins"][0]].cls, ("split", k))]
    if k == "merge":
        return [(in_objs[i].cls, ("merge", d["key"])) for i in d["ins"]]
    # CREATION consuming kinds
    if k in ("stroke", "stamp", "inset"):
        if d["ins"]:
            return [(in_objs[d["ins"][0]].cls, ("unary", k))]
        return []
    if k == "union":
        return [(in_objs[i].cls, ("union", d["key"])) for i in d["ins"]]
    return []


def _group_needs(in_objs, cand):
    # CREATION M-P(i): a split group's needs are the parts that HAVE
    # candidates in this pair (the kept set). A part with no candidate
    # is discarded, not a completeness failure; kept-set identity
    # across pairs is enforced by bindings + reconstruction, exactly
    # as the spec assigns the cost. (The original all-parts needs for
    # split_color and the range(max+1) needs for split_sep are the
    # pre-M-P semantics.)
    needs = {}
    for lst in cand.values():
        for d in lst:
            g = d["group"]
            if g is None:
                continue
            needs.setdefault(g, set()).add(d["key"])
    return needs


def pair_assignments(in_objs, out_objs, cand, deadline):
    """Enumerate exact covers. -> (assignments, capped) where an
    assignment is (bindings, deletions)."""
    needs = _group_needs(in_objs, cand)
    order = sorted(range(len(out_objs)), key=lambda oi: len(cand[oi]))
    results = []
    state = {"nodes": 0, "capped": False}

    def rec(pos, used, bindings, fates, groups, chosen):
        if len(results) >= ASSIGN_CAP:
            return
        state["nodes"] += 1
        if state["nodes"] > ASSIGN_NODES:
            state["capped"] = True
            return
        _tick(deadline)
        if pos == len(order):
            for grp, keys in groups.items():
                if keys != needs[grp]:
                    return  # split group touched but incomplete
            deletions = set()
            for ii, io in enumerate(in_objs):
                if ii not in used:
                    deletions.add(io.cls)
            if deletions & set(fates):
                return  # a class both deleted and ruled in this pair
            # resolve copy-of-output references
            prod = {}
            for d in chosen:
                prod[d["outs"][0]] = d
            final = dict(bindings)
            for d in chosen:
                if d["key"][0] != "copy_out_ref":
                    continue
                src = prod.get(d["key"][1])
                if src is None or src["kind"] in ("copy", "frame", "merge"):
                    return
                tcls = in_objs[src["ins"][0]].cls
                rk = ("copy", tcls)
                if rk in final and final[rk] != d["value"]:
                    return
                if tcls in deletions:
                    return
                final[rk] = d["value"]
            results.append((final, deletions))
            return
        oi = order[pos]
        for d in cand[oi]:
            key = d["key"]
            if key[0] != "copy_out_ref":
                if key in bindings and bindings[key] != d["value"]:
                    continue
            ok = True
            for ii in d["ins"]:
                u = used.get(ii)
                if d["group"] is not None:
                    if u is not None and u != d["group"]:
                        ok = False
                        break
                elif u is not None:
                    ok = False
                    break
            if not ok:
                continue
            nf = {}
            for cls, fd in _fate_of(d, in_objs):
                if cls in fates and fates[cls] != fd:
                    ok = False
                    break
                nf[cls] = fd
            if not ok:
                continue
            nused = dict(used)
            for ii in d["ins"]:
                nused[ii] = d["group"] if d["group"] is not None else "whole"
            nbind = dict(bindings)
            if key[0] != "copy_out_ref":
                nbind[key] = d["value"]
            nfates = dict(fates)
            nfates.update(nf)
            ngroups = {g: set(s) for g, s in groups.items()}
            if d["group"] is not None:
                ngroups.setdefault(d["group"], set()).add(key)
            chosen.append(d)
            rec(pos + 1, nused, nbind, nfates, ngroups, chosen)
            chosen.pop()
            if len(results) >= ASSIGN_CAP:
                return

    rec(0, {}, {}, {}, {}, [])
    return results, state["capped"]


def _consuming_classes(bindings):
    cons = set()
    for k in bindings:
        if k[0] in ("preserve", "scale", "grow", "mirror",
                    "split_color", "split_sep"):
            cons.add(k[1])
        elif k[0] == "merge":
            cons.update(k[1])
        # CREATION consuming kinds
        elif k[0] in ("stroke", "inset"):
            if k[1] is not None:
                cons.add(k[1])
        elif k[0] == "stamp":
            cons.add(k[1][1])
        elif k[0] == "union":
            cons.update(dk[1] for dk in k[1] if dk[0] == "obj")
    return cons


def _fates_from_bindings(bindings):
    fates = {}
    ok = True
    for k, v in bindings.items():
        if k[0] in ("preserve", "scale", "grow", "mirror"):
            fd = ("unary", k[0])
            if k[1] in fates and fates[k[1]] != fd:
                ok = False
            fates[k[1]] = fd
        elif k[0] in ("split_color", "split_sep"):
            fd = ("split", k[0])
            if k[1] in fates and fates[k[1]] != fd:
                ok = False
            fates[k[1]] = fd
        elif k[0] == "merge":
            for cls in k[1]:
                fd = ("merge", k)
                if cls in fates and fates[cls] != fd:
                    ok = False
                fates[cls] = fd
        # CREATION consuming kinds (mirrors _fate_of)
        elif k[0] in ("stroke", "inset"):
            if k[1] is not None:
                fd = ("unary", k[0])
                if k[1] in fates and fates[k[1]] != fd:
                    ok = False
                fates[k[1]] = fd
        elif k[0] == "stamp":
            fd = ("unary", "stamp")
            if k[1][1] in fates and fates[k[1][1]] != fd:
                ok = False
            fates[k[1][1]] = fd
        elif k[0] == "union":
            for dk in k[1]:
                if dk[0] == "obj":
                    fd = ("union", k)
                    if dk[1] in fates and fates[dk[1]] != fd:
                        ok = False
                    fates[dk[1]] = fd
    return fates, ok


def combine_iter(pair_assigns, deadline, holder):
    """Generator of consistent (bindings, deletions) combinations, in
    DFS order. Verification is the caller's job: bindings-consistent
    combinations can still fail reconstruction, so the caller pulls
    combinations one at a time and verifies each, instead of taking a
    capped batch up front. holder collects the first conflict field
    and the capped flag."""
    state = {"nodes": 0}

    def rec(pi, bindings, deletions):
        if state["nodes"] > COMBINE_NODES:
            holder["capped"] = True
            return
        state["nodes"] += 1
        _tick(deadline)
        if pi == len(pair_assigns):
            yield (dict(bindings), set(deletions))
            return
        for b2, d2 in pair_assigns[pi]:
            nb = dict(bindings)
            bad = None
            for k, v in b2.items():
                if k in nb and nb[k] != v:
                    bad = diff_field(nb[k], v)
                    break
                nb[k] = v
            if bad is None:
                nd = deletions | d2
                if nd & _consuming_classes(nb):
                    bad = "param"
                else:
                    for k, v in nb.items():
                        if k[0] == "copy" and v[1] == "out" \
                                and k[1] in nd:
                            bad = "param"
                            break
                if bad is None:
                    _, fok = _fates_from_bindings(nb)
                    if not fok:
                        bad = "param"
            if bad is not None:
                if holder.get("field") is None:
                    holder["field"] = bad
                continue
            yield from rec(pi + 1, nb, nd)
            if holder.get("capped"):
                return

    yield from rec(0, {}, set())


# ---------------------------------------------------------------- render

def _apply_phi(pattern, phi):
    return tuple(sorted((r, c, phi.get(col, col)) for r, c, col in pattern))


def render_body(sch, gi, out_shape=None):
    """Render onto a canvas of out_shape (default: the transformed
    input's shape). Object origins are placed by binding deltas
    measured in output coordinates; the canvas rule (verify_schema /
    predict) decides the canvas shape and any crop."""
    bg_in, bg_out = sch["bg"]
    H, W = out_shape if out_shape else gshape(gi)
    canvas = [[bg_out] * W for _ in range(H)]
    objs = SEG_FNS[sch.get("seg", "agnostic")](gi, bg_in)
    bindings = sch["bindings"]
    deletions = sch["deletions"]
    by_cls = {}
    for idx, o in enumerate(objs):
        by_cls.setdefault(o.cls, []).append(idx)
    consumed = set()
    prov = []  # (cls, origin, final pattern)

    def draw(pattern, origin, phi=None, fill=None):
        for r, c, col in pattern:
            nr, nc = origin[0] + r, origin[1] + c
            if 0 <= nr < H and 0 <= nc < W:
                if col is None:
                    canvas[nr][nc] = fill
                elif phi:
                    canvas[nr][nc] = phi.get(col, col)
                else:
                    canvas[nr][nc] = col

    # merges first (they consume several objects)
    for key in sorted((k for k in bindings if k[0] == "merge"), key=str):
        _, entries, delta = bindings[key]
        classes = key[1]
        anchor_cls = key[2]
        need = Counter(classes)
        anchors = sorted((i for i in by_cls.get(anchor_cls, [])
                          if i not in consumed),
                         key=lambda i: objs[i].origin)
        for ai in anchors:
            tmp = Counter(need)
            tmp[anchor_cls] -= 1
            chosen = {anchor_cls: [ai]}
            ok = True
            for cls, cnt in tmp.items():
                if cnt <= 0:
                    continue
                pool = sorted((i for i in by_cls.get(cls, [])
                               if i not in consumed and i != ai),
                              key=lambda i: objs[i].origin)
                if len(pool) < cnt:
                    ok = False
                    break
                chosen[cls] = pool[:cnt]
            if not ok:
                continue
            out_origin = (objs[ai].origin[0] + delta[0],
                          objs[ai].origin[1] + delta[1])
            for v in chosen.values():
                consumed.update(v)
            by_cls_entries = {}
            for e in entries:
                by_cls_entries.setdefault(e[0], []).append(e)
            for cls, es in by_cls_entries.items():
                insts = sorted(chosen[cls], key=lambda i: objs[i].origin)
                for e, inst in zip(sorted(es, key=lambda e: e[2]), insts):
                    _, tau, rel, phi_t = e
                    phi = dict(phi_t)
                    tp = transform_pattern(objs[inst].pattern, tau)
                    org = (out_origin[0] + rel[0], out_origin[1] + rel[1])
                    draw(tp, org, phi)
                    prov.append((cls, org, _apply_phi(tp, phi)))

    # CREATION M-U unions (parts: input objects + virtual sources;
    # instance assignment mirrors the merge discipline: entries in
    # key order, instances of a class by origin order; consuming
    # instance-anchored virtual parts pop from the same discipline)
    for key in sorted((k for k in bindings if k[0] == "union"),
                      key=str):
        _, entries, delta = bindings[key]
        need = Counter(dk[1] for (dk, _t, _r, _p, _i) in entries
                       if dk[0] == "obj")
        pools = {}
        ok = True
        for cls, cnt in need.items():
            pools[cls] = sorted(
                (i for i in by_cls.get(cls, []) if i not in consumed),
                key=lambda i: objs[i].origin)
            if len(pools[cls]) < cnt:
                ok = False
                break
        if not ok:
            continue
        vpools = {}
        for (dk, _t, _r, _p, _i) in entries:
            if dk[0] == "virt" and dk[1][0] in ("cross1", "ray1",
                                                "ray2", "line1") \
                    and dk[1][-1]:
                vpools.setdefault(
                    dk[1][1],
                    sorted((i for i in by_cls.get(dk[1][1], [])
                            if i not in consumed),
                           key=lambda i: objs[i].origin))
        assign = {}
        for ei, (dk, _tau, _rel, _phi_t, _ink) in enumerate(entries):
            if dk[0] == "obj":
                assign[ei] = pools[dk[1]].pop(0)
        pats = {}
        vcons = []
        for ei, (dk, tau, rel, phi_t, ink) in enumerate(entries):
            if dk[0] == "obj":
                o = objs[assign[ei]]
                pats[ei] = (o.pattern, o.origin)
            elif dk[1][0] in ("cross1", "ray1", "ray2", "line1"):
                if dk[1][-1]:
                    pool = vpools.get(dk[1][1]) or []
                    if not pool:
                        ok = False
                        break
                    idx = pool.pop(0)
                    vcons.append(idx)
                else:
                    cand = by_cls.get(dk[1][1]) or []
                    if not cand:
                        ok = False
                        break
                    idx = cand[0]
                r = _inst_pattern(dk[1], gi, bg_in, objs, idx)
                if r is None:
                    ok = False
                    break
                pats[ei] = r
            else:
                r = _scene_pattern(dk[1], gi, bg_in, objs)
                if r is None:
                    ok = False
                    break
                pats[ei] = r
        if not ok:
            continue
        aorg = pats[0][1]
        out_origin = (aorg[0] + delta[0], aorg[1] + delta[1])
        for inst in assign.values():
            consumed.add(inst)
        for idx in vcons:
            consumed.add(idx)
        for ei, (dk, tau, rel, phi_t, ink) in enumerate(entries):
            phi = dict(phi_t)
            org = (out_origin[0] + rel[0], out_origin[1] + rel[1])
            pat = pats[ei][0]
            if dk[0] == "obj":
                tp = transform_pattern(pat, tau)
                draw(tp, org, phi, fill=ink)
                prov.append((dk[1], org, _apply_phi(tp, phi)))
            else:
                draw(pat, org, phi, fill=ink)
                prov.append((str(dk), org, _apply_phi(pat, phi)))

    # CREATION consuming kinds (stroke / stamp / inset): one rule
    # per class, applied to every unconsumed instance of the class,
    # before the unary loop so instances are marked consumed.
    for key in sorted((k for k in bindings
                       if k[0] in ("stroke", "stamp", "inset")),
                      key=str):
        v = bindings[key]
        if key[0] == "stroke":
            cls, desc = key[1], key[2]
            if cls is None:
                continue  # non-consuming stroke: drawn below
            _, phi_t, ink, delta = v
            for idx in [i for i in by_cls.get(cls, [])
                        if i not in consumed]:
                r = _inst_pattern(desc, gi, bg_in, objs, idx)
                if r is None:
                    continue
                pat, org = r
                o2 = (org[0] + delta[0], org[1] + delta[1])
                draw(pat, o2, dict(phi_t), fill=ink)
                consumed.add(idx)
                prov.append((cls, o2, pat))
        elif key[0] == "stamp":
            desc = key[1]
            cls = desc[1]
            _, phi_t, delta = v
            for idx in [i for i in by_cls.get(cls, [])
                        if i not in consumed]:
                r = _inst_pattern(desc, gi, bg_in, objs, idx)
                if r is None:
                    continue
                pat, org = r
                o2 = (org[0] + delta[0], org[1] + delta[1])
                draw(pat, o2, dict(phi_t))
                consumed.add(idx)
                prov.append((cls, o2, pat))
        else:  # inset
            cls = key[1]
            _, phi_t, ink, delta = v
            for idx in [i for i in by_cls.get(cls, [])
                        if i not in consumed]:
                r = _inst_pattern(("inset", cls), gi, bg_in, objs, idx)
                if r is None:
                    continue
                pat, org = r
                o2 = (org[0] + delta[0], org[1] + delta[1])
                draw(pat, o2, dict(phi_t), fill=ink)
                consumed.add(idx)
                prov.append((cls, o2, pat))

    # unary and split fates
    for idx, o in enumerate(objs):
        if idx in consumed:
            continue
        cls = o.cls
        if cls in deletions:
            continue
        ukey = next((k for k in bindings
                     if k[0] in ("preserve", "scale", "grow", "mirror")
                     and k[1] == cls), None)
        if ukey is not None:
            v = bindings[ukey]
            kind = ukey[0]
            if kind == "preserve":
                _, tau, phi_t, delta = v
                phi = dict(phi_t)
                tp = transform_pattern(o.pattern, tau)
                draw(tp, (o.origin[0] + delta[0], o.origin[1] + delta[1]),
                     phi)
                prov.append((cls, (o.origin[0] + delta[0],
                                   o.origin[1] + delta[1]),
                             _apply_phi(tp, phi)))
            elif kind == "scale":
                _, k, tau, phi_t, delta = v
                phi = dict(phi_t)
                base = transform_pattern(o.pattern, tau)
                tp = scale_up_pat(base, k) if k > 0 else \
                    scale_down_pat(base, -k)
                if tp is not None:
                    org = (o.origin[0] + delta[0], o.origin[1] + delta[1])
                    draw(tp, org, phi)
                    prov.append((cls, org, _apply_phi(tp, phi)))
            elif kind == "grow":
                _, mode, tau, phi_t, fill, delta = v
                phi = dict(phi_t)
                base = transform_pattern(o.pattern, tau)
                gp = grow_pat(base, mode)
                if gp is not None:
                    org = (o.origin[0] + delta[0], o.origin[1] + delta[1])
                    draw(gp, org, phi, fill=fill)
                    fin = tuple(sorted(
                        (r, c, fill if col is None else phi.get(col, col))
                        for r, c, col in gp))
                    prov.append((cls, org, fin))
            elif kind == "mirror":
                _, axis, tau, phi_t, delta = v
                phi = dict(phi_t)
                base = transform_pattern(o.pattern, tau)
                mp = mirror_pat(base, axis)
                if mp is not None:
                    org = (o.origin[0] + delta[0], o.origin[1] + delta[1])
                    draw(mp, org, phi)
                    prov.append((cls, org, _apply_phi(mp, phi)))
            continue
        skeys = [k for k in bindings
                 if k[0] in ("split_color", "split_sep") and k[1] == cls]
        if skeys:
            kind = skeys[0][0]
            if kind == "split_color":
                parts = dict(color_parts(o.pattern))
                for k in skeys:
                    part = parts.get(k[2])
                    if part is None:
                        continue
                    _, tau, phi_t, delta = bindings[k]
                    phi = dict(phi_t)
                    tp = transform_pattern(part, tau)
                    org = (o.origin[0] + delta[0], o.origin[1] + delta[1])
                    draw(tp, org, phi)
                    prov.append((cls, org, _apply_phi(tp, phi)))
            else:
                nparts = len(skeys)
                chosen_parts = None
                for orient, scol, parts in sep_parts(o.pattern):
                    if len(parts) == nparts:
                        chosen_parts = parts
                        break
                if chosen_parts is not None:
                    for k in skeys:
                        if k[2] >= len(chosen_parts):
                            continue
                        _, tau, phi_t, delta = bindings[k]
                        phi = dict(phi_t)
                        tp = transform_pattern(chosen_parts[k[2]], tau)
                        org = (o.origin[0] + delta[0],
                               o.origin[1] + delta[1])
                        draw(tp, org, phi)
                        prov.append((cls, org, _apply_phi(tp, phi)))
            continue
        draw(o.pattern, o.origin)  # unseen class: unchanged

    # copy of input objects (non-consuming)
    for k, v in bindings.items():
        if k[0] == "copy" and v[1] == "in":
            _, _, tau, phi_t, delta = v
            phi = dict(phi_t)
            for idx in by_cls.get(k[1], []):
                tp = transform_pattern(objs[idx].pattern, tau)
                draw(tp, (objs[idx].origin[0] + delta[0],
                          objs[idx].origin[1] + delta[1]), phi)
    # copy of rendered objects
    for k, v in bindings.items():
        if k[0] == "copy" and v[1] == "out":
            _, _, tau, phi_t, delta = v
            phi = dict(phi_t)
            for (cls, porg, ppat) in list(prov):
                if cls == k[1]:
                    tp = transform_pattern(ppat, tau)
                    draw(tp, (porg[0] + delta[0], porg[1] + delta[1]), phi)
    # frames
    for k, v in bindings.items():
        if k[0] != "frame":
            continue
        _, margin, color = v
        if k[1] == "canvas":
            for r in range(H):
                for c in range(W):
                    if r in (0, H - 1) or c in (0, W - 1):
                        canvas[r][c] = color
        else:
            for (cls, porg, ppat) in prov:
                if cls == k[1]:
                    ph = max(r for r, _, _ in ppat) + 1
                    pw = max(c for _, c, _ in ppat) + 1
                    r0, c0 = porg[0] - margin, porg[1] - margin
                    r1, c1 = porg[0] + ph + margin - 1, \
                        porg[1] + pw + margin - 1
                    for r in range(r0, r1 + 1):
                        for c in range(c0, c1 + 1):
                            if r in (r0, r1) or c in (c0, c1):
                                if 0 <= r < H and 0 <= c < W:
                                    canvas[r][c] = color
                    break
    # CREATION non-consuming kinds (gather / stroke / rings /
    # count / stampgrid): scene patterns regenerated from this grid
    # and placed by the binding's delta.
    for k, v in bindings.items():
        if k[0] == "gather":
            _, tau, phi_t, delta = v
            r = _scene_pattern(("gather", k[1]), gi, bg_in, objs)
            if r is None:
                continue
            tp = transform_pattern(r[0], tau)
            draw(tp, (r[1][0] + delta[0], r[1][1] + delta[1]),
                 dict(phi_t))
        elif k[0] == "stroke" and k[1] is None:
            _, phi_t, ink, delta = v
            desc = k[2]
            rr = None
            if desc[0] == "linesA":
                rr = _scene_pattern(desc, gi, bg_in, objs)
            elif desc[0] in ("cross1", "ray1", "ray2", "line1"):
                for idx, o in enumerate(objs):
                    if o.cls == desc[1]:
                        rr = _inst_pattern(desc, gi, bg_in, objs, idx)
                        if rr is not None:
                            break
            if rr is None:
                continue
            pat, org = rr
            draw(pat, (org[0] + delta[0], org[1] + delta[1]),
                 dict(phi_t), fill=ink)
        elif k[0] == "rings":
            _, radii, seq, delta = v
            r = _scene_pattern(("rings", k[1], None, radii),
                               gi, bg_in, objs)
            if r is None:
                continue
            pat, org = r
            phi = {("ring", i): seq[i % len(seq)]
                   for i in range(len(radii))}
            draw(pat, (org[0] + delta[0], org[1] + delta[1]), phi)
        elif k[0] == "count":
            _, delta = v
            r = _scene_pattern(("countstack",), gi, bg_in, objs)
            if r is None:
                continue
            draw(r[0], (r[1][0] + delta[0], r[1][1] + delta[1]))
        elif k[0] == "texture":
            _, phi_t, delta = v
            r = _scene_pattern(("checker", k[1]), gi, bg_in, objs)
            if r is None:
                continue
            draw(r[0], (r[1][0] + delta[0], r[1][1] + delta[1]),
                 dict(phi_t))
        elif k[0] == "stampgrid":
            _, phi_t, placements, delta = v
            phi = dict(phi_t)
            gh, gw = gshape(gi)
            for (pr, pc) in placements:
                for r0 in range(gh):
                    for c0 in range(gw):
                        nr, nc = delta[0] + pr + r0, delta[1] + pc + c0
                        if 0 <= nr < H and 0 <= nc < W:
                            canvas[nr][nc] = phi.get(gi[r0][c0],
                                                      gi[r0][c0])
    return canvas


def _crop_grid(g, bg):
    cells = [(r, c) for r, row in enumerate(g)
             for c, v in enumerate(row) if v != bg]
    if not cells:
        return g
    mr = min(r for r, _ in cells)
    Mr = max(r for r, _ in cells)
    mc = min(c for _, c in cells)
    Mc = max(c for _, c in cells)
    return [row[mc:Mc + 1] for row in g[mr:Mr + 1]]


def apply_canvas(sch, rendered):
    """Canvas rules that act on an input-shaped render (pad renders
    directly onto the output-shaped canvas in predict/verify)."""
    if sch["canvas"] == "crop":
        return _crop_grid(rendered, sch["bg"][1])
    return rendered


def verify_schema(sch, tpairs):
    """Try canvas modes; on success set canvas fields, return True.
    Unified canvas model: objects are drawn at origin+delta in output
    coordinates on a canvas of the mode's shape (input shape for
    same/crop, output shape for pad), so pad is parameterized by its
    totals only — an embedding offset is unobservable once deltas are
    measured in output coordinates, because the background is uniform.
    """
    # BG-GATE: backgrounds resolve per pair from the schema's
    # account; for a constant account every entry is the original
    # lane's single pair and this is the original check verbatim.
    bg_pairs = sch.get("bg_pairs") or [sch["bg"]] * len(tpairs)
    if all(gshape(gi) == gshape(o) for gi, o in tpairs):
        ok = True
        for i, (gi, o) in enumerate(tpairs):
            sch["bg"] = bg_pairs[i]
            if render_body(sch, gi) != o:
                ok = False
                break
        if ok:
            sch["canvas"] = "same"
            return True
    if all(gshape(o)[0] <= gshape(gi)[0]
           and gshape(o)[1] <= gshape(gi)[1] for gi, o in tpairs):
        ok = True
        for i, (gi, o) in enumerate(tpairs):
            sch["bg"] = bg_pairs[i]
            if _crop_grid(render_body(sch, gi), bg_pairs[i][1]) != o:
                ok = False
                break
        if ok:
            sch["canvas"] = "crop"
            return True
    totals = {(gshape(o)[0] - gshape(gi)[0],
               gshape(o)[1] - gshape(gi)[1]) for gi, o in tpairs}
    if len(totals) == 1:
        th, tw = next(iter(totals))
        if th >= 0 and tw >= 0 and (th, tw) != (0, 0):
            ok = True
            for i, (gi, o) in enumerate(tpairs):
                sch["bg"] = bg_pairs[i]
                if render_body(sch, gi, gshape(o)) != o:
                    ok = False
                    break
            if ok:
                sch["canvas"] = "pad"
                sch["pad_totals"] = (th, tw)
                return True
    return False


# ---------------------------------------------------------------- induction

def _scale_up_grid(k):
    def f(g):
        out = []
        for row in g:
            exp = []
            for v in row:
                exp.extend([v] * k)
            for _ in range(k):
                out.append(list(exp))
        return out
    return f


def _scale_down_grid(k):
    def f(g):
        H, W = gshape(g)
        if H % k or W % k:
            return None
        out = []
        for br in range(H // k):
            row = []
            for bc in range(W // k):
                block = {g[br * k + dr][bc * k + dc]
                         for dr in range(k) for dc in range(k)}
                if len(block) != 1:
                    return None
                row.append(block.pop())
            out.append(row)
        return out
    return f


def _build_pretransforms():
    scales = [("x1", None), ("x2", _scale_up_grid(2)),
              ("x3", _scale_up_grid(3)), ("d2", _scale_down_grid(2)),
              ("d3", _scale_down_grid(3))]
    out = []
    for sname, sfn in scales:
        for gname, gfn in GRID_TRANSFORMS:
            def make(gfn=gfn, sfn=sfn):
                def f(g):
                    gi = gfn(g)
                    if sfn is not None:
                        gi = sfn(gi)
                    return gi
                return f
            out.append((f"{gname}|{sname}", make()))
    return out


PRETRANSFORMS = _build_pretransforms()


def _shape_compatible(tpairs):
    same = all(gshape(gi) == gshape(o) for gi, o in tpairs)
    crop = all(gshape(o)[0] <= gshape(gi)[0]
               and gshape(o)[1] <= gshape(gi)[1] for gi, o in tpairs)
    pad = all(gshape(o)[0] >= gshape(gi)[0]
              and gshape(o)[1] >= gshape(gi)[1] for gi, o in tpairs)
    return same or crop or pad


def _induce_under(tpairs, deadline, allow_creation=True):
    """-> (schema_core, None) or (None, (stage, field)). Core lacks
    pre-transform/canvas fields.

    BG-GATE: the background stage is the §2.2 account search. If no
    account is functional the attempt dies at the background stage,
    as the original died on a non-singleton modal pair set. If at
    least one account is functional, accounts are tried in declared
    order; the first that yields verified schemas supplies the
    candidates, and if none does, the first functional account's
    downstream failure is designated."""
    accts = _accounts(tpairs)
    _BG_TRACE.clear()
    _BG_TRACE["functional"] = [(s, a, b) for s, a, b, _, _ in accts]
    _BG_TRACE["account"] = None
    if not accts:
        return None, ("inconsistent", "phi")
    designated_fail = None
    for seg_name, ga, gb, bp, fmap in accts:
        cands, fail = _induce_under_account(tpairs, deadline,
                                            seg_name, ga, gb, bp, fmap,
                                            allow_creation)
        if cands is not None:
            _BG_TRACE["account"] = (seg_name, ga, gb)
            _BG_TRACE["bg_map"] = sorted(fmap.items())
            return cands, None
        if designated_fail is None:
            designated_fail = fail
            _BG_TRACE["account"] = (seg_name, ga, gb)
            _BG_TRACE["bg_map"] = sorted(fmap.items())
    return None, designated_fail


def _induce_under_account(tpairs, deadline, seg_name, ga, gb, bp,
                          fmap, allow_creation=True):
    """The original _induce_under body under one account: per-pair
    generated backgrounds bp, segmentation SEG_FNS[seg_name]."""
    segfn = SEG_FNS[seg_name]
    acct = {"seg": seg_name, "gen_in": ga, "gen_out": gb,
            "bg_map": dict(fmap), "bg_pairs": list(bp)}
    per_pair = []
    capped_any = False
    for pi, (gi, outp) in enumerate(tpairs):
        bg = bp[pi]
        in_objs = segfn(gi, bg[0])
        out_objs = segfn(outp, bg[1])
        if len(in_objs) > MAX_OBJECTS or len(out_objs) > MAX_OBJECTS:
            return None, ("search_cap", None)
        cand, zero = gen_candidates(
            in_objs, out_objs, gshape(outp), deadline,
            scene={"grid": gi, "bg_in": bg[0], "seg": seg_name}
            if allow_creation else None)
        if cand is None:
            return None, ("creation_unexplained", None)
        assigns, capped = pair_assignments(in_objs, out_objs, cand,
                                           deadline)
        capped_any = capped_any or capped
        if not assigns:
            return None, ("search_cap" if capped else "cover_failed",
                          None)
        # Per-pair reconstruction filter: an assignment whose own
        # bindings do not reproduce its own pair (under some canvas
        # mode) can never participate in a global schema — zombie
        # covers (frames around deleted templates, copies that only
        # work by borrowing another pair's bindings) die here instead
        # of multiplying through the combination search.
        filtered = []
        for b, d in assigns:
            sch_j = dict(acct, bg=bg, bg_pairs=[bg], bindings=b,
                         deletions=d)
            if verify_schema(sch_j, [(gi, outp)]):
                filtered.append((b, d))
        if not filtered:
            return None, ("canvas", None)
        per_pair.append(filtered)
    # Selection among verified schemas: the lane commits to the
    # minimum under the declared lexicographic order (creations,
    # deletions, bindings) — an Occam order over the constructed
    # space, fixed here in code, not tuned per task. All minima are
    # returned; the lane arbitrates ties by prediction unanimity.
    holder = {}
    tried = 0
    exhausted = True
    best = []  # list of (key, schema)
    for bindings, deletions in combine_iter(per_pair, deadline, holder):
        tried += 1
        if tried > SCHEMA_CAP:
            exhausted = False
            break
        sch = dict(acct, bg=bp[0], bindings=bindings,
                   deletions=deletions)
        if verify_schema(sch, tpairs):
            key = (sum(1 for v in bindings.values()
                       if v[0] in ("copy", "frame")),
                   len(deletions), len(bindings))
            if not best or key < best[0][0]:
                best = [(key, sch)]
            elif key == best[0][0] and len(best) < 4:
                best.append((key, sch))
    if best:
        return [s for _, s in best], None
    if holder.get("capped") or not exhausted:
        return None, ("search_cap", None)
    if tried == 0:
        return None, ("inconsistent", holder.get("field") or "param")
    return None, ("canvas", None)


def induce(pairs, deadline):
    """-> (schema, meta). meta: stage/field when schema is None;
    attempts count always."""
    designated = None
    designated_trace = None
    attempts = 0
    for pname, pfn in PRETRANSFORMS:
        tpairs = []
        ok = True
        for inp, outp in pairs:
            gi = pfn(inp)
            if gi is None:
                ok = False
                break
            tpairs.append((gi, outp))
        if not ok or not _shape_compatible(tpairs):
            continue
        attempts += 1
        # CREATION budget discipline: creation candidates are
        # generated only under the identity pretransform. The
        # creation machinery is scene construction on the presented
        # grid (as Stratum 1's programs are, below); the dihedral /
        # scale sweep remains the object grammar's search. Profiled
        # basis: with creation live in all 40 attempts, dense scenes
        # spent the whole 25 s task budget failing attempts instead
        # of reaching their designated failure (union search alone
        # profiled at 24.96 s of one 25 s task before its own
        # discipline was added). The frozen budget is part of the
        # machinery (kill criterion 3); this gate is the build's
        # compliance with it, disclosed in the build results.
        cands, fail = _induce_under(
            tpairs, deadline, allow_creation=(pname == "id|x1"))
        if cands is not None:
            for sch in cands:
                sch["pre_name"] = pname
                sch["pre_fn"] = pfn
            return cands, {"attempts": attempts, "full_fit": True}
        if designated is None:
            designated = fail
            designated_trace = dict(_BG_TRACE)
    # CREATION Stratum 1: whole-grid program accounts (M-Q / M-S /
    # lattice), tried only after the object pipeline has failed on
    # every attempt, on the raw pairs — so no currently-fitting
    # task's schema can be shadowed by a program.
    ps = _program_schemas(pairs, deadline)
    if ps:
        return ps, {"attempts": attempts, "full_fit": True,
                    "program": ps[0]["program"][0]}
    if designated is None:
        return None, {"attempts": attempts, "stage": "canvas",
                      "field": None}
    return None, {"attempts": attempts, "stage": designated[0],
                  "field": designated[1],
                  "bg_trace": designated_trace}


def predict(sch, grid_in):
    gi = sch["pre_fn"](grid_in)
    if gi is None:
        return grid_in
    # CREATION Stratum 1: program schemas apply their rule directly.
    if "program" in sch:
        res = _program_apply(sch["program"], gi)
        return res if res is not None else grid_in
    # BG-GATE: resolve this grid's background under the schema's
    # identified account. A constant map applies to any input (the
    # original lane's behavior); an unseen key under a non-constant
    # map abstains (returns the input, which cannot certify).
    fmap = sch["bg_map"]
    binv = bg_generators(gi)[sch["gen_in"]]
    if binv in fmap:
        bout = fmap[binv]
    elif len(fmap) == 1:
        bout = next(iter(fmap.values()))
    else:
        return grid_in
    sch["bg"] = (binv, bout)
    if sch["canvas"] == "pad":
        th, tw = sch["pad_totals"]
        H, W = gshape(gi)
        return render_body(sch, gi, (H + th, W + tw))
    return apply_canvas(sch, render_body(sch, gi))


def _grid_key(g):
    return tuple(tuple(row) for row in g)


def loo_check(pairs, deadline):
    """Set-valued LOO: re-induction from any k-1 pairs must yield a
    candidate set whose members AGREE on the held pair's input, and
    that agreed prediction must be exact. (With a unique induced
    schema this is exactly v1's gate.)"""
    for j in range(len(pairs)):
        sub = [p for i, p in enumerate(pairs) if i != j]
        cands, _ = induce(sub, deadline)
        if not cands:
            return False
        preds = {_grid_key(predict(s, pairs[j][0])) for s in cands}
        if len(preds) != 1:
            return False
        if predict(cands[0], pairs[j][0]) != pairs[j][1]:
            return False
    return True


def _mechanism_tag(sch, pairs):
    if "program" in sch:
        return "program:" + sch["program"][0]
    vals = list(sch["bindings"].values())
    kinds = {v[0] for v in vals}
    # colormap_only: v1 degeneracy test, on pre-transformed pairs
    def _colormap():
        if sch["pre_name"] != "id|x1" or sch["canvas"] != "same":
            return False
        for inp, _ in pairs:
            gi = sch["pre_fn"](inp)
            objs = segment(gi, modal_color(gi))
            total = gshape(gi)[0] * gshape(gi)[1]
            if not (len(objs) == 1
                    and len(objs[0].pattern) >= 0.9 * total):
                return False
        return all(v[0] == "preserve" and v[1] == 0 and v[3] == (0, 0)
                   for v in vals)
    if _colormap():
        return "colormap_only"
    if sch["pre_name"] != "id|x1" and kinds <= {"preserve"} and all(
            v[1] == 0 and v[3] == (0, 0) for v in vals):
        return "grid_transform"
    if kinds & {"copy", "frame"}:
        return "object_creation"
    if kinds & {"scale", "grow", "mirror", "split_color", "split_sep",
                "merge"}:
        return "object_transform"
    return "object_schema"


def _class_has_fate(sch, cls):
    if cls in sch["deletions"]:
        return True
    for k in sch["bindings"]:
        if k[0] in ("preserve", "scale", "grow", "mirror",
                    "split_color", "split_sep") and k[1] == cls:
            return True
        if k[0] == "merge" and cls in k[1]:
            return True
        if k[0] in ("copy", "frame") and k[1] == cls:
            return True
        # CREATION consuming kinds
        if k[0] in ("stroke", "inset") and k[1] == cls:
            return True
        if k[0] == "stamp" and k[1][1] == cls:
            return True
        if k[0] == "union" and any(dk[0] == "obj" and dk[1] == cls
                                   for dk in k[1]):
            return True
    return False


# ------------------------------------------------------- CREATION programs
# Stratum 1 whole-grid program accounts. A program is a total scene
# function of the input grid alone; it is identified by exact
# reproduction of every train pair (shape included — the spec's M-Q
# soundness cap) and re-identified inside every LOO fold through
# induce(). Programs run only after the object pipeline has failed
# on every attempt (see induce()).

def _compositions(n, k, cap):
    """Compositions of n into k positive parts, uniform first."""
    if k == 1:
        return [(n,)]
    if k == n:
        return [tuple([1] * n)]
    out = []
    if n % k == 0:
        out.append(tuple([n // k] * k))

    def rec(left, parts_left, cur):
        if len(out) >= cap:
            return
        if parts_left == 1:
            out.append(tuple(cur + [left]))
            return
        for v in range(1, left - parts_left + 2):
            cur.append(v)
            rec(left - v, parts_left - 1, cur)
            cur.pop()
            if len(out) >= cap:
                return

    rec(n, k, [])
    seen = set()
    res = []
    for t in out:
        if t not in seen:
            seen.add(t)
            res.append(t)
    return res


def _blocks_of(grid, rgroups, cgroups):
    rows = []
    r0 = 0
    for rh in rgroups:
        row = []
        c0 = 0
        for cw in cgroups:
            row.append([grid[r][c] for r in range(r0, r0 + rh)
                        for c in range(c0, c0 + cw)])
            c0 += cw
        rows.append(row)
        r0 += rh
    return rows


def _block_key(blk, bh, bw):
    """Dihedral-canonical key of a rectangular block of colors."""
    cells = tuple((r, c, blk[r * bw + c])
                  for r in range(bh) for c in range(bw))
    best = None
    for tau in range(8):
        tp = transform_pattern(cells, tau)
        if best is None or tp < best:
            best = tp
    return best


def _quotient_classify(clf, blk, modal_in):
    kind = clf[0]
    if kind == "modal":
        return Counter(blk).most_common(1)[0][0]
    if kind == "unique_map":
        umap = dict(clf[1])
        nonmodal = {x for x in blk if x != modal_in}
        if len(nonmodal) == 1:
            return umap.get(next(iter(nonmodal)),
                            Counter(blk).most_common(1)[0][0])
        return Counter(blk).most_common(1)[0][0]
    if kind == "presence":
        _, col, ink, absent = clf
        if col in blk:
            return ink
        return modal_in if absent[0] == "modal_in" else absent[1]
    if kind == "count_ge":
        _, col, t, ink, absent = clf
        if blk.count(col) >= t:
            return ink
        return modal_in if absent[0] == "modal_in" else absent[1]
    return modal_in


def _quotient_apply(params, grid):
    rg, cg, clf = params
    H, W = gshape(grid)
    if sum(rg) != H or sum(cg) != W:
        return None
    blocks = _blocks_of(grid, rg, cg)
    modal_in = modal_color(grid)
    keymap = dict(clf[1]) if clf[0] == "pattern_key" else None
    out = []
    for r, rowb in enumerate(blocks):
        orow = []
        for c, blk in enumerate(rowb):
            if clf[0] == "pattern_key":
                k = _block_key(blk, rg[r], cg[c])
                orow.append(keymap.get(
                    k, Counter(blk).most_common(1)[0][0]))
            else:
                orow.append(_quotient_classify(clf, blk, modal_in))
        out.append(orow)
    return out


def _quotient_identify(pairs, rg, cg, deadline):
    """Classifier identification over all pairs (a classifier is a
    Pi function: it must reproduce every pair; the pattern-key and
    unique-color maps must be functional across all blocks of all
    pairs). -> classifier params or None."""
    # the partition is fixed across pairs: every pair's input must
    # tile by (rg, cg) and every output must be exactly the block
    # grid's shape (pairs whose output shape varies — the partition
    # family does not apply — kill this partition, not the lane)
    if any(gshape(go) != (len(rg), len(cg)) for _, go in pairs):
        return None
    if any(gshape(gi) != (sum(rg), sum(cg)) for gi, _ in pairs):
        return None
    blocks = [_blocks_of(gi, rg, cg) for gi, _ in pairs]
    outs = [go for _, go in pairs]
    Ho, Wo = gshape(outs[0])
    modal_in = [modal_color(gi) for gi, _ in pairs]

    def run(clf):
        for pi in range(len(pairs)):
            for r in range(Ho):
                for c in range(Wo):
                    if _quotient_classify(clf, blocks[pi][r][c],
                                          modal_in[pi]) \
                            != outs[pi][r][c]:
                        return False
        return True

    if run(("modal",)):
        return ("modal",)
    # pattern-key map (functional across all pairs or death)
    keymap = {}
    ok = True
    for pi in range(len(pairs)):
        for r in range(Ho):
            for c in range(Wo):
                k = _block_key(blocks[pi][r][c], rg[r], cg[c])
                v = outs[pi][r][c]
                if k in keymap and keymap[k] != v:
                    ok = False
                    break
                keymap[k] = v
            if not ok:
                break
        if not ok:
            break
    if ok:
        return ("pattern_key", tuple(sorted(keymap.items(), key=str)))
    # unique-color map: identify while validating
    umap = {}
    ok = True
    for pi in range(len(pairs)):
        for r in range(Ho):
            for c in range(Wo):
                blk = blocks[pi][r][c]
                nonmodal = {x for x in blk if x != modal_in[pi]}
                v = outs[pi][r][c]
                if len(nonmodal) == 1:
                    col = next(iter(nonmodal))
                    if col in umap and umap[col] != v:
                        ok = False
                        break
                    umap[col] = v
                elif v != Counter(blk).most_common(1)[0][0]:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            break
    if ok:
        return ("unique_map", tuple(sorted(umap.items())))
    in_colors = sorted({v for row in pairs[0][0] for v in row})
    out_colors = sorted({v for row in pairs[0][1] for v in row})
    for col in in_colors:
        for ink in out_colors:
            for absent in (("modal_in",), ("const", None)):
                if absent[0] == "const":
                    av = {outs[0][r][c] for r in range(Ho)
                          for c in range(Wo)
                          if col not in blocks[0][r][c]}
                    if len(av) != 1:
                        continue
                    absent = ("const", next(iter(av)))
                if run(("presence", col, ink, absent)):
                    return ("presence", col, ink, absent)
                _tick(deadline)
            for t in (1, 2, 3):
                for absent in (("modal_in",), ("const", None)):
                    if absent[0] == "const":
                        av = {outs[0][r][c] for r in range(Ho)
                              for c in range(Wo)
                              if blocks[0][r][c].count(col) < t}
                        if len(av) != 1:
                            continue
                        absent = ("const", next(iter(av)))
                    if run(("count_ge", col, t, ink, absent)):
                        return ("count_ge", col, t, ink, absent)
                    _tick(deadline)
    return None


def _prog_quotient(pairs, deadline):
    gi0, go0 = pairs[0]
    H, W = gshape(gi0)
    Ho, Wo = gshape(go0)
    if Ho > H or Wo > W or (Ho == H and Wo == W):
        return None
    rparts = _compositions(H, Ho, 12)
    cparts = _compositions(W, Wo, 12)
    tried = 0
    for rg in rparts:
        for cg in cparts:
            tried += 1
            if tried > 300:
                return None
            _tick(deadline)
            params = _quotient_identify(pairs, rg, cg, deadline)
            if params is not None:
                return ("quotient", (rg, cg, params))
    return None


def _fold_idx(i, n):
    m = i % (2 * n)
    return m if m < n else 2 * n - 1 - m


def _domain_apply(grid, occ):
    """M-Q(iii): the smallest (0,0)-anchored rectangle whose mirrored
    dihedral tiling reproduces the grid on all non-occlusion cells;
    the rectangle is emitted. (h, w) derived from the grid itself."""
    H, W = gshape(grid)
    cands = [(h, w) for h in range(1, H + 1) for w in range(1, W + 1)
             if (h, w) != (H, W)]
    cands.sort(key=lambda t: (t[0] * t[1], t[0], t[1]))
    for h, w in cands:
        ok = True
        for r in range(H):
            for c in range(W):
                v = grid[r][c]
                if occ is not None and v == occ:
                    continue
                if grid[_fold_idx(r, h)][_fold_idx(c, w)] != v:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return [row[:w] for row in grid[:h]]
    return None


def _prog_domain(pairs, deadline):
    gi0, go0 = pairs[0]
    occs = [None] + sorted({v for row in gi0 for v in row})
    for occ in occs:
        _tick(deadline)
        if _domain_apply(gi0, occ) == go0:
            if all(_domain_apply(gi, occ) == go for gi, go in pairs):
                return ("domain", occ)
    return None


def _sym_apply(grid, occ):
    """M-S: close the grid under the group generated by its measured
    dihedral symmetries (a generator is measured iff it maps every
    non-occlusion cell to a cell of the same color or an occlusion
    cell). Occlusion cells take their orbit's unique non-occlusion
    color; an orbit with two is account death."""
    H, W = gshape(grid)
    gens = {"flipud": lambda r, c: (H - 1 - r, c),
            "fliplr": lambda r, c: (r, W - 1 - c),
            "rot180": lambda r, c: (H - 1 - r, W - 1 - c)}
    if H == W:
        gens["transpose"] = lambda r, c: (c, r)
        gens["rot90"] = lambda r, c: (c, H - 1 - r)

    def is_measured(g):
        for r in range(H):
            for c in range(W):
                v = grid[r][c]
                if occ is not None and v == occ:
                    continue
                gr, gc = g(r, c)
                w = grid[gr][gc]
                if w != v and not (occ is not None and w == occ):
                    return False
        return True

    measured = [g for g in gens.values() if is_measured(g)]
    idx = [(r, c) for r in range(H) for c in range(W)]
    pos = {p: i for i, p in enumerate(idx)}
    gen_perms = [tuple(pos[g(r, c)] for (r, c) in idx)
                 for g in measured]
    ident = tuple(range(len(idx)))
    group = {ident}
    frontier = [ident]
    while frontier and len(group) <= 16:
        cur = frontier.pop()
        for gp in gen_perms:
            comp = tuple(gp[cur[i]] for i in range(len(idx)))
            if comp not in group:
                group.add(comp)
                frontier.append(comp)
    out = [[None] * W for _ in range(H)]
    seen = [False] * len(idx)
    for i, (r, c) in enumerate(idx):
        if seen[i]:
            continue
        orbit = set()
        for t in group:
            orbit.add(t[i])
        for j in orbit:
            seen[j] = True
        colors = {grid[idx[j][0]][idx[j][1]] for j in orbit}
        nonocc = {v for v in colors if v != occ}
        if len(nonocc) > 1:
            return None
        fill = next(iter(nonocc)) if nonocc else occ
        for j in orbit:
            out[idx[j][0]][idx[j][1]] = fill
    return out


def _prog_symclose(pairs, deadline):
    gi0, go0 = pairs[0]
    occs = [None] + sorted({v for row in gi0 for v in row})
    for occ in occs:
        _tick(deadline)
        if _sym_apply(gi0, occ) == go0:
            if all(_sym_apply(gi, occ) == go for gi, go in pairs):
                return ("symclose", occ)
    return None


def _lattice_apply(grid, period):
    """M-R(i) at scene level: orbit completion under the translation
    lattice generated by one period vector. Each orbit takes its
    unique non-bg color (bg = the grid's modal color); a conflicted
    orbit is account death."""
    H, W = gshape(grid)
    dr, dc = period
    if (dr, dc) == (0, 0):
        return None
    bg = modal_color(grid)
    out = [[bg] * W for _ in range(H)]
    seen = [[False] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            if seen[r][c]:
                continue
            rr, cc = r, c
            while 0 <= rr - dr < H and 0 <= cc - dc < W:
                rr -= dr
                cc -= dc
            orb = []
            while 0 <= rr < H and 0 <= cc < W:
                orb.append((rr, cc))
                seen[rr][cc] = True
                rr += dr
                cc += dc
            colors = {grid[x][y] for (x, y) in orb
                      if grid[x][y] != bg}
            if len(colors) > 1:
                return None
            fill = next(iter(colors)) if colors else bg
            for (x, y) in orb:
                out[x][y] = fill
    return out


def _prog_lattice(pairs, deadline):
    gi0, go0 = pairs[0]
    H, W = gshape(gi0)
    if H * W > 1600:
        return None
    good = []
    for dr in range(-(H - 1), H):
        for dc in range(-(W - 1), W):
            if (dr, dc) == (0, 0):
                continue
            _tick(deadline)
            if _lattice_apply(gi0, (dr, dc)) == go0:
                good.append((dr, dc))
    for per in sorted(good, key=lambda t: (abs(t[0]) + abs(t[1]), t)):
        if all(_lattice_apply(gi, per) == go for gi, go in pairs):
            return ("lattice", per)
    return None


# M-S (symmetry completion, _prog_symclose): CUT under kill
# criterion 5 after the spent-draw run (unblocked 0 of its class's
# tasks). The function remains in the file for the record and the
# census instruments; it is not in the shipped registry.
_PROGRAMS = (_prog_quotient, _prog_domain, _prog_lattice)


def _program_schemas(pairs, deadline):
    if time.time() > deadline - 0.5:
        return None
    idfn = next(fn for name, fn in PRETRANSFORMS if name == "id|x1")
    for prog in _PROGRAMS:
        try:
            got = prog(pairs, deadline)
        except Timeout:
            return None
        except Exception:
            continue  # a program family's own defect kills the
            # family for this task, never the lane
        if got is None:
            continue
        name, params = got
        sch = {"program": (name, params),
               "pre_name": "id|x1", "pre_fn": idfn,
               "canvas": "same", "seg": "agnostic",
               "gen_in": "program", "gen_out": "program",
               "bg_map": {}, "bg_pairs": [], "bg": (0, 0),
               "bindings": {}, "deletions": set()}
        return [sch]
    return None


def _program_apply(program, grid):
    name, params = program
    if name == "quotient":
        return _quotient_apply(params, grid)
    if name == "domain":
        return _domain_apply(grid, params)
    if name == "symclose":
        return _sym_apply(grid, params)
    if name == "lattice":
        return _lattice_apply(grid, params)
    return grid


# ---------------------------------------------------------------- lane

def _bg_info_from_trace(info, trace):
    """Gate readout fields from a background-stage trace."""
    functional = trace.get("functional") or []
    info["bg_stage_passed"] = bool(functional)
    info["bg_functional_count"] = len(functional)
    acct = trace.get("account")
    info["bg_account"] = list(acct) if acct else None
    info["bg_map"] = trace.get("bg_map")


def lane(task, budget_s):
    t0 = time.time()
    deadline = t0 + budget_s
    train = [(p["input"], p["output"]) for p in task["train"]]
    test_inputs = [p["input"] for p in task["test"]]  # outputs stripped
    info = {"fits": 0, "tried": 0, "programs": [], "mechanism": None,
            "loo": None, "accepted": False, "full_fit": False}
    _BG_TRACE.clear()
    try:
        cands, meta = induce(train, deadline)
    except Timeout:
        info["reason"] = "budget"
        _bg_info_from_trace(info, dict(_BG_TRACE))
        return [], info
    info["tried"] = meta.get("attempts", 0)
    if not cands:
        _bg_info_from_trace(info, meta.get("bg_trace") or {})
    if not cands:
        stage = meta.get("stage", "canvas")
        if stage == "inconsistent":
            info["reason"] = f"inconsistent_{meta.get('field') or 'param'}"
        else:
            info["reason"] = stage
        return [], info
    info["full_fit"] = True
    sch = cands[0]
    info["bg_stage_passed"] = True
    info["bg_account"] = [sch["seg"], sch["gen_in"], sch["gen_out"]]
    info["bg_map"] = sorted(sch["bg_map"].items())
    info["mechanism"] = _mechanism_tag(sch, train)
    info["programs"] = [
        f"pre={sch['pre_name']} canvas={sch['canvas']} "
        f"bind={len(sch['bindings'])} del={len(sch['deletions'])} "
        f"tag={info['mechanism']}"]
    try:
        if len(train) >= 3:
            ok = loo_check(train, deadline)
            info["loo"] = ok
            if not ok:
                info["reason"] = "loo_rejected"
                return [], info
        else:
            if len(train) == 2:
                info["loo"] = loo_check(train, deadline)

            def determinate(s):
                unary = [k for k in s["bindings"]
                         if k[0] in ("preserve", "scale", "grow",
                                     "mirror")]
                consuming = [k for k in s["bindings"]
                             if k[0] in ("preserve", "scale", "grow",
                                         "mirror", "split_color",
                                         "split_sep", "merge")]
                single_fallback = len(unary) == 1 and len(consuming) == 1
                for ti in test_inputs:
                    gi = s["pre_fn"](ti)
                    if gi is None:
                        continue
                    for o in segment(gi, modal_color(gi)):
                        if not _class_has_fate(s, o.cls) \
                                and not single_fallback:
                            return False
                return True

            cands = [s for s in cands if determinate(s)]
            if not cands:
                info["reason"] = "nondeterminate_test_class"
                return [], info
    except Timeout:
        info["reason"] = "budget"
        return [], info
    if time.time() - t0 > budget_s:
        info["reason"] = "budget"
        return [], info
    # prediction unanimity across the tied minima: a tie that predicts
    # two different outputs is a rule the pairs did not identify.
    pred_sets = [[predict(s, ti) for ti in test_inputs] for s in cands]
    if any(ps != pred_sets[0] for ps in pred_sets[1:]):
        info["reason"] = "ambiguous"
        return [], info
    info["fits"] = 1
    info["accepted"] = True
    preds = [[g] for g in pred_sets[0]]
    return preds, info
