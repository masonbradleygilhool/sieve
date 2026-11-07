#!/usr/bin/env python3
"""APEX-2 NEXT-GEN PROBE v2 — derivation-based correspondence induction.

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
import ng_lane as ng

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


def gen_candidates(in_objs, out_objs, out_shape, deadline):
    """-> (cand_by_out, group_sizes) or (None, zero_out_indices).
    cand_by_out: oi -> [derivation]. group_sizes: split group id ->
    number of parts the group must produce."""
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
    zero = [oi for oi in range(len(out_objs)) if not cand[oi]]
    if zero:
        return None, zero
    # prune split groups that cannot complete: every part index present
    present = {}
    for oi, lst in cand.items():
        for d in lst:
            if d["group"] is not None:
                present.setdefault(d["group"], set()).add(d["key"][-1])
    dead_groups = set()
    for grp, size in group_sizes.items():
        have = present.get(grp, set())
        if grp[1] == "split_color":
            need = {c for c, _ in
                    color_parts(in_objs[grp[0]].pattern)}
        else:
            need = set(range(size))
        if not need.issubset(have):
            dead_groups.add(grp)
    if dead_groups:
        for oi in cand:
            cand[oi] = [d for d in cand[oi] if d["group"] not in dead_groups]
        zero = [oi for oi in range(len(out_objs)) if not cand[oi]]
        if zero:
            return None, zero
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
    return []


def _group_needs(in_objs, cand):
    needs = {}
    for lst in cand.values():
        for d in lst:
            g = d["group"]
            if g is None or g in needs:
                continue
            io = in_objs[g[0]]
            if g[1] == "split_color":
                needs[g] = {("split_color", io.cls, c)
                            for c, _ in color_parts(io.pattern)}
            else:
                idxs = {dd["key"][2] for l2 in cand.values()
                        for dd in l2 if dd["group"] == g}
                needs[g] = {("split_sep", io.cls, i)
                            for i in range(max(idxs) + 1)}
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
    objs = segment(gi, bg_in)
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
    bg_out = sch["bg"][1]
    if all(gshape(gi) == gshape(o) for gi, o in tpairs):
        if all(render_body(sch, gi) == o for gi, o in tpairs):
            sch["canvas"] = "same"
            return True
    if all(gshape(o)[0] <= gshape(gi)[0]
           and gshape(o)[1] <= gshape(gi)[1] for gi, o in tpairs):
        if all(_crop_grid(render_body(sch, gi), bg_out) == o
               for gi, o in tpairs):
            sch["canvas"] = "crop"
            return True
    totals = {(gshape(o)[0] - gshape(gi)[0],
               gshape(o)[1] - gshape(gi)[1]) for gi, o in tpairs}
    if len(totals) == 1:
        th, tw = next(iter(totals))
        if th >= 0 and tw >= 0 and (th, tw) != (0, 0):
            if all(render_body(sch, gi, gshape(o)) == o
                   for gi, o in tpairs):
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


def _induce_under(tpairs, deadline):
    """-> (schema_core, None) or (None, (stage, field)). Core lacks
    pre-transform/canvas fields."""
    bg_pairs = {(modal_color(gi), modal_color(o)) for gi, o in tpairs}
    if len(bg_pairs) != 1:
        return None, ("inconsistent", "phi")
    bg = next(iter(bg_pairs))
    per_pair = []
    capped_any = False
    for gi, outp in tpairs:
        in_objs = segment(gi, bg[0])
        out_objs = segment(outp, bg[1])
        if len(in_objs) > MAX_OBJECTS or len(out_objs) > MAX_OBJECTS:
            return None, ("search_cap", None)
        cand, zero = gen_candidates(in_objs, out_objs, gshape(outp),
                                    deadline)
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
            sch_j = {"bg": bg, "bindings": b, "deletions": d}
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
        sch = {"bg": bg, "bindings": bindings, "deletions": deletions}
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
        cands, fail = _induce_under(tpairs, deadline)
        if cands is not None:
            for sch in cands:
                sch["pre_name"] = pname
                sch["pre_fn"] = pfn
            return cands, {"attempts": attempts, "full_fit": True}
        if designated is None:
            designated = fail
    if designated is None:
        return None, {"attempts": attempts, "stage": "canvas",
                      "field": None}
    return None, {"attempts": attempts, "stage": designated[0],
                  "field": designated[1]}


def predict(sch, grid_in):
    gi = sch["pre_fn"](grid_in)
    if gi is None:
        return grid_in
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
    return False


# ---------------------------------------------------------------- lane

def lane(task, budget_s):
    t0 = time.time()
    deadline = t0 + budget_s
    train = [(p["input"], p["output"]) for p in task["train"]]
    test_inputs = [p["input"] for p in task["test"]]  # outputs stripped
    info = {"fits": 0, "tried": 0, "programs": [], "mechanism": None,
            "loo": None, "accepted": False, "full_fit": False}
    try:
        cands, meta = induce(train, deadline)
    except Timeout:
        info["reason"] = "budget"
        return [], info
    info["tried"] = meta.get("attempts", 0)
    if not cands:
        stage = meta.get("stage", "canvas")
        if stage == "inconsistent":
            info["reason"] = f"inconsistent_{meta.get('field') or 'param'}"
        else:
            info["reason"] = stage
        return [], info
    info["full_fit"] = True
    sch = cands[0]
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
