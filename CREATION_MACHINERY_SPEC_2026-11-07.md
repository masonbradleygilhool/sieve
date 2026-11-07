# CREATION MACHINERY SPEC — the successor lane's creation component

**Date:** 2026-11-07 · **Status:** SPEC ONLY — nothing in this document is built.
**Anatomy:** `CREATION_WALL_ANATOMY_2026-11-07.md` (the 19 tasks, classes Q/L/R/S/M/F/C/T/P/G, all counts and verdicts live there).
**Base lane:** `nextgen_probe/ng2_lane_bg.py` (the bg-fixed lane; its background component is integrated, not replaced).
**Governing discipline:** §3.1 of `SHARED_WRONG_BINDING_DERIVATION_2026-11-04.md` — a build on an extended grammar is authorized by a **measured U on spent draws against a pre-registered band**, not by a bound and not by this spec; and the packet's seat-standard language for any fresh-draw claim.

## 1. Architecture — three strata, one threading discipline

The creation component integrates at exactly the points where the bg component
did, and changes nothing else. The lane's solver core — `pair_assignments`,
`combine_iter`, `loo_check`, determinacy — stays byte-identical, as it did for
the BG-GATE build. All new machinery speaks the existing idiom: `_deriv` records
(kind / outs / ins / key / value / group), fate keys, Π bindings identified by
cross-pair intersection, survival = functional consistency across all pairs of
the task.

**Stratum 1 — scene stage** (inside `_induce_under_account`, beside the bg
account enumeration; candidates here are *whole-grid programs*, threaded exactly
like bg accounts — enumerated per pair, surviving by cross-pair functional
intersection, charged to the same per-task deadline):
- **M-Q: quotient accounts** (class Q). A quotient account is a pair
  (partition rule, classifier binding). Partition rules, in declared order:
  (i) uniform b×b blocks, b read from the scene's period structure (the Π period
  binding the bg/census machinery already computes — never a free constant);
  (ii) row/column strip partitions (bands from the same period structure);
  (iii) symmetry-domain extraction (the fundamental domain of the grid's
  dihedral/translation symmetry group, for e66aafb8-type emissions).
  The classifier is a Π function from the existing kinds — a pattern/parameter
  function over the block (modal color, presence-of-color predicate,
  odd-one-out, block pattern key) — bound exactly like existing scalars, by
  intersection across pairs. The quotient grid is emitted as the output (or as
  the scene on which object induction then runs, when the quotient is an
  intermediate — the §3.1 form). **Soundness cap:** a quotient account is
  admissible only if it reproduces every train pair's output grid *shape*
  exactly; shape failure kills the account before classification is bound.
- **M-S: symmetry-completion pretransform** (class S). A new pretransform
  family beside `id|x1` & friends: given a bound symmetry group G (a subgroup
  of the grid's dihedral × period-translation group, enumerated from the
  scene's measured symmetries — not hypothesized freely), emit the grid closed
  under G: every cell whose G-orbit contains a non-background mate takes the
  mate's color (orbit conflicts = account death, exactly like a bg account
  failing a pair). Object induction then runs on the completed grid unchanged,
  where the completed mass is an ordinary input object and `preserve` fires.

**Stratum 2 — pattern sources** (the `in_objs` list handed to
`gen_candidates` gains pseudo-objects with reserved class tags; everything
downstream is untouched):
- **M-G: color-class gather source** (class G). For each color present in the
  input, the pseudo-object whose pattern is *all cells of that color* in the
  input grid. Derivations over it use the existing kinds (preserve first).
  Cap: gather sources are offered only when the color's cells number ≥ 8
  (below that, components already cover the territory) — the cap is a
  candidate-count discipline, stated here so the build does not tune it.

**Stratum 3 — derivation kinds** (new `_deriv` kinds inside `gen_candidates`,
same record format, same dedup and per-object candidate caps):
- **M-U: union derivations (cross-cutting; build first).** If an output
  object's cells partition into ≥ 2 parts, each part independently derivable
  (by any kind, including the creation kinds below), emit one composite
  candidate whose ins/keys are the union of the parts' and whose value records
  the partition. Search discipline: partitions are proposed only from the cell
  sets of candidates already generated for sub-patterns of the object and from
  creation-kind proposals (strokes, stamps, frames) — never by subset
  enumeration. This is the mechanism that lets created content that *touches*
  preserved content (the majority of L/R/M/F cases) be derived at all.
- **M-L: stroke kind** (class L). Parameters: anchor (a Π region-query —
  object center, unique dot, marker pair), direction (8 lattice directions),
  extent (to-edge / to-second-anchor / to-obstacle), ink (an existing color
  under φ, or an instance color per M-P). Rasterization is exact lattice
  geometry (Bresenham-free: ARC strokes are axis/diagonal — direction vectors
  in {(0,±1),(±1,0),(±1,±1)} only).
- **M-R: stamp kind** (class R, and M via placement mode). One source pattern,
  one binding, a **placement set**. Placement modes in declared order:
  (i) lattice — translates of a bound period vector (covers 363442ee pair 2,
  85fa5666); (ii) marker set — positions read by a Π region-query over marker
  objects (covers 363442ee pairs 0–1); (iii) enumerated — a placement set bound
  as an explicit scene parameter, identified across pairs by intersection
  (covers 27f8ce4f); (iv) reflected — placements may include the pattern under
  a reflection composed with a translation (covers 760b3cac, class M). The
  stamp emits the union of its placements as one pattern (merged components
  are the normal case, not an exception).
- **M-F: frame generalization** (class F). The existing frame kind gains:
  (i) an **iteration count** binding (rings emitted concentrically until the
  count is spent or the region is), with the **color sequence** bound from
  marker objects via Π region-queries (08573cc6); (ii) an **inset mode** —
  the ring drawn at negative margin inside a source object's bbox, consuming
  the object's interior border (694f12f3); (iii) the center as an
  addressed-content parameter (unique marker position) rather than only
  canvas / unique-object anchors.
- **M-C: count-shape kind** (class C). A Π region-query supplies a count (and
  optionally a color multiset) of a source class; a canonical shape family —
  filled triangle first, row-gathers behind it — is generated at exactly that
  count, anchored at a bound position, colors assigned from the multiset in
  reading order. The family list is closed at build time; adding a family is
  a new commission, not a tuning knob.
- **M-T: texture kind** (class T). Periodic fill of a bound region: checkerboard
  (two bound colors + phase) first; the region is the canvas or a bound
  object's bbox. Closed family list, same rule as M-C.
- **M-P: split-and-discard + instance colors** (class P; the color half also
  serves M-L/M-F). (i) In the split-group prune, a group may complete on a
  **subset** of parts if the unkept parts are recorded as dropped in the
  derivation value — the prune's condition changes from "every part index
  present" to "every *kept* part index present, kept-set identical across all
  pairs of the task". (ii) A derivation may carry an **instance color**: a
  color slot in the derivation key, bound per derivation instance by
  cross-pair intersection (the same key must take the same color in every
  pair), never through the global φ. Instance colors are the only sanctioned
  route to colors absent from the input.

**What is NOT in this spec:** no change to segmentation (the 5d2a5c43
diagonal-pair footnote in the anatomy is recorded, not engineered around); no
new pretransform geometries beyond M-S; no budget change (the 25 s/task frozen
budget stands — candidate growth is controlled by the caps above and by the
kill criteria below, not by more time); no free constants anywhere — every new
parameter is a Π binding in the lane's existing sense.

## 2. Expected migration on the spent 19 — SPENT-DRAW DIAGNOSTIC

"Unblocked" = in the designated attempt, every previously-zero output object
gains ≥ 1 surviving candidate (split-and-discard: post-prune) under the
mechanism as specified. This is a candidate-generation diagnostic on a spent
draw. It is not a fit count, not a solve count, and not a conversion reading;
realized migration is whatever the build's spent-draw re-run (§4) measures,
and the fresh draw (§3) is the only conversion instrument. Nothing here
projects to 240 tasks.

| Class | Mechanism | Tasks | Unblocked if mechanism performs as analyzed |
|---|---|---|---|
| Q | M-Q | 67b4a34d, e66aafb8, 9110e3c5, 5d2a5c43, e3497940 | ≤ 5 — partition side is mechanical; the classifier binding is unidentified for 3 of 5 (anatomy §2-Q), so realized unblocking for those 3 is the build's open problem, not this spec's promise |
| L | M-L (+M-U, M-P ink) | 55783887, 5c0a986e, 41e4d17e | ≤ 3 |
| R | M-R (+M-U) | 27f8ce4f, 363442ee, 85fa5666 | ≤ 3 (27f8ce4f verified content-exact; the other two rest on the tiling readings in the anatomy) |
| S | M-S | af22c60d | ≤ 1 (group identification is the risk: no single involution completes it) |
| M | M-R mode (iv) | 760b3cac | ≤ 1 |
| F | M-F (+M-P ink) | 08573cc6, 694f12f3 | ≤ 2 |
| C | M-C | 3d6c6e23 | ≤ 1 (count/multiset readings verified exactly) |
| T | M-T | e9afcf9a | ≤ 1 |
| P | M-P | 604001fa | ≤ 1 (shape side verified exactly; the fresh colors must bind by intersection) |
| G | M-G (+M-U) | 6d0160f0 | ≤ 1 |
| **Total** | | **19** | **≤ 19 — an upper bound on leaving the zero-candidate state, nothing more** |

## 3. Fresh-draw conversion probe (design only — not run, not authorized by this spec)

- **Draw source:** untouched tasks from the 938-task gauntlet pool, excluding
  the 48 spent A+B tasks (890 remain). Same composition as the spent draw:
  12 A + 36 B, sampled by a seed fixed in the probe's preregistration *before*
  sampling. No task used by the Friday pack beyond the spent 48, and no task
  from the sealed exam (disjoint by construction).
- **Protocol:** the extended lane (bg component + this creation component)
  runs the gauntlet protocol unchanged — frozen 25 s/task budget, LOO
  determinacy as the lane's certification, rows published in the diag format.
- **Pre-registered bars, in the packet's language** (filed in the probe's own
  preregistration before the draw is sampled):
  - fits and certified solves reported with denominators; conversion read
    against the grammar's **1/28** (unanimous∧correct) and the fit-supply
    reading **1/18**;
  - **sample-U with denominators**, measured on the *extended* grammar (the
    old U = 0.321 does not apply — anatomy §4);
  - **unanimous∧correct with its Fisher p against the grammar's 1/9**,
    printed with the line;
  - the seat-standard bar mirrors the packet's: conversion ≥ 10 × 1/28
    guarded to ≥ 10 fits, **or** the unanimity clause (≥ 8 sample-unanimous
    judgeable tasks with ≥ 3/4 correct, Fisher p printed);
  - secondary diagnostic (never the seat criterion): `creation_unexplained`
    deaths on the fresh draw, against the spent draw's 19/48 with
    denominators stated.
- A PASS on this probe is a component-to-lane verdict in the packet's sense.
  It approves no solver. The sealed in-house exam remains the only 216/240
  instrument.

## 4. Kill criteria for the build itself (spent draw first — no fresh draw is spent before these pass)

The build's first run is a re-diagnosis of the **spent 48** under the extended
lane, same protocol as the BG-GATE run. The design ends — before any fresh
draw is sampled — if any of the following holds:

1. **Fits lost.** Any of the 4 banked fits (7d1f7ee8, a61f2674, 4acc7107,
   8dae5dfc) stops fitting or changes certification. (Enlarged candidate sets
   can move determinacy; a creation component that costs the lane its banked
   fits is a regression, whatever it unblocks.)
2. **Unblocking floor.** Fewer than **10 of the 19** tasks leave the
   zero-candidate state in their designated attempts. (The mechanisms were
   specified against verified readings of these tasks; unblocking under half
   of them means the readings or the mechanisms are wrong, and the correct
   move is back to anatomy, not forward to a fresh draw.)
3. **Budget ceiling.** `budget` deaths on the spent 48 exceed the bg lane's
   **15/48** — the disclosed cost the bg component already paid. Candidate
   growth beyond that is controlled by cutting kinds, never by raising the
   frozen budget.
4. **U band (§3.1's first gate).** The survivor-census re-measurement on the
   extended grammar, over the spent draw's fits, must show
   unanimous∧correct among determinate fits **no worse than the old
   grammar's spent-draw reading** (the 4 banked fits, determinacy as
   recorded). A creation grammar that buys fits with wrong unanimity fails
   the commission's own gate, per §3.1: the build is authorized by a
   measured U on spent draws, or it is not authorized.
5. **Per-class cut.** Any single mechanism (M-Q … M-P) that unblocks **0** of
   its class's tasks on the spent draw is cut from the build — not carried
   into the fresh draw as dead candidate mass.

Passing all five does not certify anything about conversion; it earns the
fresh-draw probe of §3, whose preregistration is a separate filing.

## 5. Fence consequences (summary; full treatment in the anatomy §4)

Every mechanism here enlarges or alters the old grammar's candidate system.
Consequences, stated once: the **F × U ≤ 0.842 ceiling and census U are void
as bounds on the extended grammar** and must be re-measured (kill criterion 4
is that measurement's first instance); the census bound 921/938 = 98.2% is
recomputed, not inherited; **M-P is the one deliberate weakening of a banked
soundness fence** (split-group completeness) and its cost lands in the same
U re-measurement. What survives untouched: the bg component and its PASS as a
component record, the Friday flat-null verdict, the 4 banked fits as
re-verification targets (kill criterion 1), and every per-task death record
as history.
