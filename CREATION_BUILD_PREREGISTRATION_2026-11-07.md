# CREATION BUILD — PREREGISTRATION (2026-11-07)

Filed BEFORE the build, per commission. Governing texts:
`CREATION_MACHINERY_SPEC_2026-11-07.md` (the build),
`CREATION_WALL_ANATOMY_2026-11-07.md` (the 19-task table, M-U finding,
not-creation verdicts, killed hypotheses), `BG_GATE_RESULTS_2026-11-07.md`
(lane state being extended), `NOVEMBER_CONVERSION_PACKET` kill-criteria
language. Lane extended: `nextgen_probe/ng2_lane_bg.py` (bg deaths 2/48,
fits 4/4 preserved, budget deaths 15/48 at the frozen 25 s cap).

**Filing defect disclosed up front:** the anatomy file on disk is
truncated mid-§2-S (12,969 chars, ends with a literal `[truncated 8182
chars]` marker). §1 (the full 19-task table), §2-Q/L/R and part of §2-S
are on disk; §§3–5 and §2 detail for M/F/C/T/P/G are not. The build
proceeds from the spec (complete on disk), the §1 table, §2-Q/L/R, and
direct measurement of the task grids (performed at filing: all 19 tasks
inspected pair by pair). No killed hypothesis for 67b4a34d / 9110e3c5 /
5d2a5c43 (block-modal, kaleidoscope fold-majority, mod-4 orbit-majority,
stride sampling; (3,2,2)-block majority + four predicates; block
any/all/majority + row-period compression) is re-tried anywhere below.

## The build

New file `nextgen_probe/ng2_lane_creation.py`, a copy of
`ng2_lane_bg.py` plus the creation component. `ng2_lane_bg.py` and
`ng2_lane.py` are not modified.

**Byte-identical core (diff-verified after the build, function by
function, against `ng2_lane_bg.py`):** `pair_assignments`,
`combine_iter`, `loo_check`, and the `determinate()` closure inside
`lane()`. Everything else is generation/rendering surface the spec's
mechanisms necessarily extend: `gen_candidates`, `render_body`,
`_fate_of`, `_consuming_classes`, `_fates_from_bindings`,
`_group_needs`, `_class_has_fate`, `FIELD_NAMES`,
`_induce_under_account` (scene hook), `induce` (program fallback pass),
`predict` (program branch), `_mechanism_tag` (program tag only).

**Build order:** M-U first (the anatomy's load-bearing mechanism), then
the strata in spec order as integrated below.

### Integration architecture (narrower choices, disclosed)

1. **Object-level mechanisms (Strata 2–3)** integrate inside
   `gen_candidates`, which gains a `scene` argument (the pair's own
   input grid, its identified bg_in/bg_out, its shape) from
   `_induce_under_account`. Creation candidates are appended AFTER all
   existing kinds for each output object, under the same dedup and the
   same per-object candidate cap (existing kinds keep search priority).
2. **Whole-grid mechanisms (Stratum 1: M-Q, M-S, and the lattice half
   of M-R for 85fa5666)** integrate as *program accounts*: a program is
   validated by exact reproduction of every train pair of the task
   (rule(input) == output, shape included — the spec's M-Q soundness
   cap). Programs are tried ONLY after the object pipeline has failed
   on every attempt of `induce()` (fallback pass on the raw pairs,
   identity pretransform), so no currently-fitting task's schema can be
   shadowed by a program (kill criterion 1 safety). A validating
   program yields a program schema (bindings empty; `predict` applies
   the rule; `loo_check` revalidates per fold through the unchanged
   `induce`/`predict`). Program rules are total scene functions of the
   input grid alone.
3. **M-P instance colors** are realized as the spec's color slot in
   effect: a creation derivation's key identifies its instance context
   (anchor class / source class) and its value carries the ink color;
   `combine_iter`'s unchanged key→value agreement binds the color per
   instance across pairs. No color is ever taken from global φ.
4. **M-U union parts** are drawn from: whole input objects (the
   existing merge pool), split parts as pattern sources are EXCLUDED
   (narrower; group semantics stay inside the split machinery), and
   virtual pattern sources generated from the scene (gather patterns,
   stroke rasters, stamp copy-unions, ring sets). Unions are capped at
   3 parts, MERGE_CAND_CAP results per output object, exact tiling only
   (the merge recursion's discipline).
5. **Budget is frozen**: 25 s/task everywhere; no cap, node, or
   deadline change anywhere in the lane. Budget deaths are reported,
   not repaired.

### Mechanisms

- **M-U union** — generalized merge: parts pool = input objects +
  virtual sources; per-part phi, per-part ink for None-colored cells.
- **M-G gather** — non-consuming derivation, ins=(); pattern = all
  cells of one input color (≥ 8 cells), reconstructed from the grid at
  generation and at render; matched under tau/phi like copy.
- **M-L stroke** — virtual patterns rasterized on the input grid:
  (a) axis cross through an anchor object's bbox center (lines only,
  and anchor-inclusive variant); anchor set = all objects of the
  anchor's class for the cross; (b) rays from an anchor in the 8
  lattice directions, extent to-edge or to-obstacle, from bbox corner
  or center; (c) rays from an anchor toward a second anchor (diagonal
  sign vector). Ink = None-colored cells, single observed color bound
  in the value. Stroke patterns serve as standalone derivations
  (ins=()) and as M-U parts.
- **M-R stamp** — consuming derivation: pattern = source object ∪ its
  copies. Modes: (i) lattice — translates by a bound period vector
  (period read off the scene by autocorrelation; placements = all
  lattice translates of the source origin inside the canvas);
  (ii) markers — placements putting the source's reference cell on
  each object of a marker class; (iii) enumerated — placements read
  off the output object at generation (occurrence tiling of the output
  object by source translates), recorded in the value; (iv) reflected
  — source ∪ its mirror across the bbox edge axis, both sides.
  Copies-only variants serve as M-U parts.
- **M-F frame** — (i) iterated rings: non-consuming derivation whose
  pattern = concentric square rings centered on a unique marker
  object's center, radii a consecutive run, colors cycling the color
  sequence of a marker object read in reading order; count and radii
  bound in the value. (ii) inset: consuming derivation, pattern =
  solid object ∪ the border of its margin-1 interior rectangle,
  interior cells None-colored (instance ink in the value).
  (iii) center-as-content is the (i) centering rule.
- **M-C count-shape** — non-consuming derivation: Π count query =
  number of cells of a scene color; canonical filled triangle (row
  widths 1, 3, 5, …, final row partial to spend the count exactly),
  anchored with its base on the canvas bottom row, centered on the
  counted color's modal column; colors = the counted color.
- **M-T texture** — binding-level derivation for single-cell outputs:
  value = checkerboard parity p; the two colors are scene-resolved
  (the input grid's exactly-two colors, even-parity color = the input
  grid's (0,0) color), drawn over the full canvas in `render_body`
  before object rendering. Family closed: checkerboard only.
- **M-P split-and-discard** — (i) the split-group prune in
  `gen_candidates` no longer strips a group's surviving parts when a
  sibling part has no candidate, and `_group_needs` computes a
  split_color group's needs as the parts that HAVE candidates in this
  pair (the kept set); dropped parts are recorded implicitly by
  absence and remain visible in the group accounting. (ii) instance
  colors per item 3 above (also serving M-L/M-F inks).
- **M-Q quotient (program)** — partition × classifier accounts.
  Partitions: uniform b×b blocks (b from in/out shape ratio when
  integral; also b from the scene period structure), row/column strip
  compositions (consecutive groups; count from the output shape), each
  admissible only if the emitted shape equals every pair's output
  shape. Classifiers (Π functions, closed family): modal color;
  presence-of-color c → ink else bg (per c); count of c ≥ t (per c,
  t); the block's unique non-bg color mapped through a color map;
  dihedral-canonical pattern-key → color (functional across all
  blocks of all pairs, or the account dies). Validation = exact
  reproduction of all pairs.
- **M-Q(iii) domain extraction (program)** — smallest (0,0)-anchored
  rectangle whose mirrored dihedral tiling reproduces the input on all
  cells except a designated occlusion color; emitted as the output.
- **M-S symmetry completion (program)** — close the input under a
  subgroup of the grid's dihedral group (generators measured from the
  grid: a generator is admitted only if it maps every non-occlusion
  cell to a cell of the same color or an occlusion cell); occlusion
  cells take the unique non-occlusion color of their orbit; orbit
  conflict = account death.
- **Lattice extension (program, for 85fa5666's R form)** — output =
  input ∪ all in-canvas translates of the input's non-bg pattern by a
  period vector (dx, dy) (and its negative), period identified by
  intersection across pairs; exact reproduction required.

## Gates, in order

### G0 — census re-measurement (a measurement, not a pass/fail)

Protocol = `SURVIVOR_SET_CENSUS_2026-11-04.md`'s own: for every
full-fit task of the lane on the spent 48 A+B draw, enumerate the
version space — ALL verified schemas across all attempt families and
background accounts (the lane's schema cap does not apply; caps
20,000 combinations / 512 schemas / 120 s per task, cap hit =
undetermined, never absorbed) — render each on the task's test input
via the lane's `predict`; unanimous iff exactly one distinct rendered
grid AND enumeration completed; test outputs used only to flag
correct/incorrect. Report, per the census's treatments: determined
count, unanimous count, unanimous∧correct, U conservative (undetermined
against), U determined-only, U absolute ceiling; F measured on the
draw (fits/48) and the ceiling products F_measured × U and
0.982 × U_ceiling (the 0.982 supply bound is the census's bg-binding
bound — the creation extension does not alter bg accounts, so that
component stands as measured; the lane-level supply is re-measured
directly). The same enumeration is run for the OLD lane
(`ng2_lane_bg.py`) on its 4 banked fits, as kill criterion 4's
comparison population.

If the re-measured ceiling still binds below 0.90, the verdict says so
at full strength.

### G1 — fit preservation (kill criterion 1 governs)

The 4 banked fits — 7d1f7ee8 (full fit / loo_rejected), a61f2674
(full fit / nondeterminate_test_class), 4acc7107 (full fit /
loo_rejected), 8dae5dfc (full fit / loo_rejected), all pool B, account
(agnostic, modal, modal), map 0→0 per `diag2_bg_rows.json` — are run
through the extended lane at 25 s and must re-certify identically
(same full_fit, same reason, same certification outcome).

### G2 — spent-draw re-run

The extended lane over the spent 48 A+B draw (run record
`gauntlet/runs/run_1793817846_seed20261109_nextgen_v2.json`, the
`diag2_bg.py` harness mirrored on the new lane; rows to
`nextgen_probe/diag2_creation_rows.json`, the bg rows file untouched).
Full re-charged taxonomy against the bg lane's, the 19 creation rows'
migration (leaving the zero-candidate state; labeled SPENT-DRAW
DIAGNOSTIC everywhere it appears), certified solves, fit-bearing
count, budget deaths.

### The five build kill criteria (spec §4, quoted; adjudicated one by one in the results)

1. **Fits lost:** any of the 4 banked fits stops fitting or changes
   certification.
2. **Unblocking floor:** fewer than 10 of the 19 creation rows leave
   the zero-candidate state in their designated attempts.
3. **Budget ceiling:** budget deaths on the spent 48 exceed the bg
   lane's 15/48.
4. **U band:** the survivor-census re-measurement on the extended
   grammar, over the spent draw's fits, must show unanimous∧correct
   among determinate fits no worse than the old grammar's spent-draw
   reading (the 4 banked fits, determinacy as recorded).
   Operationalization filed here: the census enumeration of G0 is run
   on the 4 banked fits under BOTH lanes; criterion 4 fails if the
   extended lane's unanimous∧correct count among determined spaces on
   those 4 tasks drops below the old lane's, or if any of the 4 flips
   from non-unanimous to unanimous∧wrong. New fits' unanimity is
   reported in G0 as the extended grammar's own reading.
5. **Per-class cut:** any single mechanism (M-Q…M-P) unblocking 0 of
   its class's tasks on the spent draw is cut from the build (named
   in the results; a cut is not by itself a build kill).

Passing all five earns the §3 fresh-draw probe (separate filing; it
does NOT fire in this lane). Passing certifies nothing about
conversion. Nothing in G0–G2 projects spent-draw numbers to 240.

## Registered fresh-draw probe bars (spec §3 — context, NOT run here)

48 untouched tasks from the 890 remaining pool tasks, 12 A + 36 B,
seed fixed in its own preregistration. Seat bar: conversion ≥ 10 ×
1/28 guarded to ≥ 10 fits, OR the unanimity clause (≥ 8
sample-unanimous judgeable with ≥ 3/4 correct, Fisher p printed);
secondary diagnostic: creation_unexplained deaths vs the spent 19/48.
A probe pass approves no solver; the sealed exam is the only 216/240
instrument.

## Contention discipline

Local CPU only. /proc is censused before every heavy batch; other
lanes are live (NS SA70 instrument chain, SA37 fine driver) and are
never disturbed. All runs thread-capped
(OMP_NUM_THREADS / OPENBLAS_NUM_THREADS / MKL_NUM_THREADS = 1) and
nice'd. The 25 s/task cap is frozen machinery.
