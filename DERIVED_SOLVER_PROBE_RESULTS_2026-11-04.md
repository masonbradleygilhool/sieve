# SIEVE — derived solver, pre-registered probe results (2026-11-04)

Program name: **SIEVE** (renamed from APEX-2 by user order
2026-11-04, applied to this document on landing; directory and
file paths retain their build-time names by the same order).

**Verdict: WEAK-ALIVE** (architecture derivation §6.4: 1–3 certified
solves on A+B). The identification loop fires on real fresh tasks
over the derived grammar — the first certified solve any SIEVE lane
has posted on a fresh gauntlet draw — and earns exactly one
iteration, aimed at the taxonomy's largest class (§7 below). No
scale, no confirmation draw (that is conditioned on ALIVE), no
approval exam (untouched, per orders).

Strength labels: the census bound (98.2%) is a paper ceiling; the
numbers below are the measurement. Nothing here is a capability
claim beyond them.

## 1. Protocol as executed

- Instrument: `gauntlet/gauntlet.py`, **unmodified**. Lane:
  `derived_solver/ds_lane.py:lane`. Budget 25 s/task. Draw
  A:12, B:36, C:12, single draw.
- Seed **20261164** — smallest seed ≥ 20261110 whose B-draw and
  C-draw are disjoint from the draws of 20261103 / 20261104 /
  20261109, verified by replicating the gauntlet's sampling offline
  before the lane ran; the replication reproduces all three prior
  run records' drawn id sets exactly. Pool A overlap with prior
  draws: 8–9 of 12 (pool A has 18 tasks; unavoidable, per §6.1).
  Drawn A ids: e66aafb8, 1e97544e, 3ed85e70, ca8f78db, 08573cc6,
  c663677b, 67b4a34d, 929ab4e9, 477d2879, 604001fa, f4081712,
  79fb03f4.
- Run record: `gauntlet/runs/run_1793829053_seed20261164_derived.json`
  — complete (not partial), wall **972.1 s** for 60 tasks, $0, CPU
  only.
- Controls (§6.3): **all five PASS before the run** —
  `derived_solver/controls_ds.py`: (1) split-by-color and grow
  synthetics solved and certified; (2) periodic-extension task
  solved and certified through the field binding itself
  ({("field",): ("field", 0)}, phase 0, LOO pass); (3) cross-pair
  copy task solved and certified, the certified schema family
  exactly {copy_other, preserve, preserve}; (4) abstention control:
  novel-creation task produced no certified schema
  (creation_novel); (5) shuffled-output negative: rejected
  (inconsistent_delta).
- Coverage expectation (§6.2), recorded in the build's design note
  before the probe: census bound **921/938 = 98.2%** on pool B
  (census/param_bound.json), vs the v2 grammar's 69.7% recomputed
  by the same tool.

## 2. Raw counts

| Pool | n | Certified solves | Train-fit-only | No-fit |
|---|---|---|---|---|
| A | 12 | 0 | 0 | 12 |
| B | 36 | **1** | 0 | 35 |
| C | 12 | 0 | 0 | 12 |
| **A+B** | **48** | **1** | 0 | 47 |
| All | 60 | 1 | 0 | 59 |

`fits=1` is reported only for certified schemas (§6.1), so
train-fit-only is 0 by construction; full-fit accounting is in §3.

**Solve rate A+B: 1/48 = 2.1%, Wilson 95% [0.4%, 10.9%].**
Pool B: 1/36, Wilson [0.5%, 14.2%]. Pool A: 0/12, Wilson [0%, 24.3%].
All 60: 1/60, Wilson [0.3%, 8.9%].

The solve: **ad38a9d0** (pool B) — account primary/modal/modal,
background rule const, pre-transform id|x1, canvas delta, 6
bindings, mechanism tag object_schema (not a lookup kind),
determinacy 1.0, solved in 0.22 s. It reproduced identically in the
diagnostic re-run (0 record/re-run mismatches on solved tasks).

## 3. Fit → certified conversion (A+B)

- Full-fit coverage: **10/48 = 20.8%**, Wilson [11.7%, 34.3%]
  (v1: 4.2%, v2: 8.3% on their draws; the derived grammar reaches
  2.5× v2's fit rate, against a 98.2% paper bound — the bound→fit
  gap is the derivation's own L5 warning priced: content
  identification is not placement identification, and §4 shows
  search economics taking a further cut).
- Of the 10 full fits: certified **1**; LOO-rejected 3;
  shape-LOO-rejected 3 (the new certification's own kill count,
  reported separately per §6.5); nondeterminate_test_class 2
  (2-pair tasks); 1 found a full fit and exhausted the budget
  inside certification.
- Conversion: 1/10 full fits certified (10%).

## 4. Death taxonomy (A+B, §6.5 — every non-solved task, one sub-reason)

From the diagnostic re-run (`derived_solver/diag_ds.py`, which also
reproduced the record's solve):

| Sub-reason | Count | Share |
|---|---|---|
| search_cap — lane "budget" (25 s exhausted in the attempt sweep) | 20 | 41.7% |
| search_cap — enumeration caps hit | 7 | 14.6% |
| inconsistent_segmentation (canonical account: no consistent background rule) | 7 | 14.6% |
| creation_unexplained | 3 | 6.3% |
| loo_rejected | 3 | 6.3% |
| shape_loo_rejected | 3 | 6.3% |
| nondeterminate_test_class | 2 | 4.2% |
| inconsistent_delta | 1 | 2.1% |
| cover_failed | 1 | 2.1% |
| (full fit, budget exhausted inside certification) | 1 | 2.1% |
| **solved** | **1** | 2.1% |

**The largest class is search economics: 27/48 (56%)** die as
search_cap/budget before the grammar's identification stage can
return a structural verdict — the derived grammar's attempt space
(40 pre-transforms × searched accounts × base-component attempts)
at a fixed 25 s/task. This, not a grammar class, is what the one
earned iteration is aimed at (§7). Second is background
identification at the canonical account (7) — the v2 probe's
largest class (17/48 there) reduced but not eliminated, and partly
masked by the budget class above it: tasks whose canonical account
dies at the background stage may fit under later searched
accounts the sweep never reached.

Zero creation_novel deaths were recorded on this draw (the
abstention control proves the class is live machinery; the draw's
creation-bearing tasks died earlier in the pipeline). One
inconsistent_phi/tau/param death beyond the delta above: none.

Pool C (12): budget 8, search_cap 2, shape_loo_rejected 2 (the 2 C
full fits both died at the shape-diverse holdout); 0 solves.

## 5. Census-class tabulation of the draw (A+B, §6.5)

Size class: same 29, shrink 17, grow 1, mixed 1. Train pairs per
task: 2→5, 3→25, 4→13, 5→3, 6→1, 7→1.
Fates present (tasks, census staged matching): preserved 36,
deleted 28, recolored 27, grown 24, created 21, shrunk 15,
scaled 6, reshaped 2. Tasks with any creation: 21/48.
Creation instances under the modal account, by source class
(first-match, derivation order): ring/mirror 443, copy 45,
witness 34, glyph-eligible 20, novel/residual 5, field 1.
Determinacy (census LOO substrate): the 1 solve is fully
determinate (frac 1.0); of the 47 non-solves, 12 are fully
determinate and the mean determinate fraction is 0.396 — the
draw's identification substrate is thin, as the census said of
the population (LOO fully determinate 16.4%).

## 6. Gates, applied strictly (§6.4)

- KILL (0 solves): **no** — 1 certified solve.
- WEAK-ALIVE (1–3 solves): **yes — the verdict.**
- ALIVE (≥4 solves AND coverage ≥30% AND no override): no —
  solves 1 < 4, coverage 20.8% < 30%.
- F1 (coverage <15% caps at WEAK): not triggered (20.8% ≥ 15%).
- F5 (≥half of full fits LOO-rejected caps at WEAK): strict
  reading — ordinary LOO rejections are 3/10 (30%), not triggered;
  inclusive reading — counting shape-diverse holdout rejections,
  6/10 (60%), triggered. The verdict is WEAK-ALIVE under both
  readings (the solve count already places it there); recorded
  because the F5 signal is real: certification, not fitting, is
  the second-largest conversion loss.
- F4 (C solves with zero A+B solves = KILL): not triggered
  (C = 0 solves; A+B = 1).
- F3 (≥half of solves from a lookup kind caps at WEAK): not
  triggered (the solve is object_schema).

Consequence per §6.4: WEAK-ALIVE earns **exactly one iteration,
aimed at the §6.5 taxonomy's largest class — search economics
(search_cap/budget, 27/48)**. No scale claim, no grammar
extension, no budget change is licensed by this verdict; the
confirmation draw does not run; the sealed approval exam is not
touched.

## 7. Per-task record (from the gauntlet run record)

Wall: A+B sum 729.2 s; 22 of 48 A+B tasks consumed ≥20 s; max
43.7 s — one task overran the 25 s lane budget (the census
evaluation paths used by the table stage are not deadline-ticked;
recorded here as an instrument defect of the lane, priced into
the budget class above). Full per-task lines (tid, pool, class,
fits, pairs, elapsed) are in the run record
`run_1793829053_seed20261164_derived.json`; per-task sub-reasons,
mechanisms, accounts, determinacy and binding status are in
`derived_solver/diag_ds_rows.json`.

Solved: ad38a9d0 (B, 0.22 s). Everything else on A+B: no_fit,
with sub-reasons per §4.

## 8. Honest distance

The bound said 98.2% of pool B carries the grammar's necessary
conditions. The probe measured: full-fit reach 20.8% on this draw,
certified conversion 1/48. The distance decomposes, on this
evidence, as: search economics at the fixed budget (27/48 deaths —
the grammar's attempt space is wider than 25 s/task can sweep),
certification losses (6–9 of 10 fits), background identification
at the canonical account (7), and the remainder structural. The
one licensed iteration targets the first of these. This probe
does not measure, and this file does not claim, anything about
the sealed approval exam or the 90% requirement; the candidate
is not frozen and no exam was run.
