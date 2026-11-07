# SIEVE — Intersection-First Identification Probe Results (2026-11-04)

The build of the mechanism derived in
`NEXT_IDENTIFICATION_DERIVATION_2026-11-04.md` (intersection-first
identification over cached signature tables), over the frozen
derived grammar. Lane: `derived_solver/ds_lane3.py`; design note:
`derived_solver/DESIGN_NOTE3.md` (implementation deviations only).

## Verdict: KILL — and F6 falsified

**0/48 certified solves A+B** (A 0/12, B 0/36), Wilson 95%
[0.0%, 7.4%]. Pre-registered bands (derivation §5): KILL = 0;
WEAK = 1–3; ALIVE = ≥4 solves AND coverage ≥30% AND no override.
The measured point is 0, so the band is KILL.

**F6 (this mechanism's own economics falsifier) fires on both
clauses.** Search-economics deaths charged exactly as iterations
1–2 charged them: **30/48 = 62.5%** (budget 17 + search_cap 12 +
fit-then-budget 1), against the registered limit of 6/48. Median
A+B per-task wall **12.25 s**, against the registered limit of
2.5 s. Under §5, F6 caps the verdict at WEAK regardless of solves
(moot under KILL), the mechanism is closed as designed, and **no
economics iteration is permitted on it**. Registered consequence
(§5): KILL, or F6 falsification, closes this species; the desk
redraws from the three-probe record. Both fired. The sealed
approval exam was not read, run, or touched; it remains unspent.

Full-fit coverage: **10/48 = 20.8%**, Wilson [11.7%, 34.3%]
(iteration 1: 20.8%; iteration 2: 16.7%) — the fit supply of the
first probe, recovered without iteration 2's reordering, and
converted at 0/10.

## 1. Protocol as run

- Instrument: `gauntlet/gauntlet.py`, **unmodified**. Lane:
  `derived_solver/ds_lane3.py:lane`. Budget 25 s/task. Draw
  A:12, B:36, C:12, single draw, CPU only, $0.
- Seed **20365108** — the smallest seed ≥ 20271133 whose B-draw
  and C-draw are disjoint from the draws of seeds 20261103,
  20261104, 20261109, 20261164, 20271132 and smoke 999, per §5's
  seed rule. Verified by replicating the gauntlet's sampling
  offline: the replication reproduces all six prior run records'
  drawn id sets exactly before the lane ran. Pool A has 18 tasks;
  A-overlap with prior draws is unavoidable and the drawn A ids
  are recorded in the run record.
- Controls: **all five PASS before the run**
  (`derived_solver/controls_ds3.py`), including §5's
  strengthened assertions: control 2's certified schema carries
  the field binding itself; control 3's certified schema family
  is exactly {copy_other, preserve}; control 4 (abstention)
  produces no certified schema; control 5 (shuffled negative)
  none.
- Engineering pre-checks (§5), all PASS
  (`derived_solver/prechecks_ds3.py`, spent tasks only):
  (i) deadline discipline on iteration 1's overrun tasks —
  ac0c5833: 43.7 s under ds_lane → **25.00 s**; 2c0b0aff:
  28.0 s → **25.00 s**, both charged budget; (ii) iteration 1's
  solve ad38a9d0 solves and certifies (identical program:
  primary/modal/modal, const, id|x1, delta, 6 bindings,
  object_schema, 0.27 s); (iii) candidate completeness — the
  frozen certified schema's bindings survive Stage A intact on
  its winning frame, and on all 21 spent tasks where a frozen
  lane recorded a full fit, this lane retains a full fit on
  **21/21** (19 of 21 complete induction + certification in
  ≤ 8.7 s; 2 are fit-then-budget deaths inside certification);
  (iv) fold integrity — loo folds and a direct Stages T/0/A/B
  run on the same pair subsets are the identical code path
  (induce3) and produce identical held-pair judgments on both
  sampled controls.
- Run record: `gauntlet/runs/run_1793837074_seed20365108_
  sieve_intersection.json` — complete (not partial), wall
  **809.0 s** of the 1,200 s protocol parameter.
  Diagnostic: `derived_solver/diag_ds3.py` — 0 record/re-run
  mismatches on solved tasks (none solved; acceptance flags
  reproduce).

## 2. Raw counts

| Pool | n | Certified solves | Train-fit-only | No-fit |
|---|---|---|---|---|
| A | 12 | 0 | 0 | 12 |
| B | 36 | 0 | 0 | 36 |
| C | 12 | 0 | 0 | 12 |
| **A+B** | **48** | **0** | 0 | 48 |
| All | 60 | 0 | 0 | 60 |

Solve rate A+B: 0/48, Wilson [0.0%, 7.4%]. Pool B: 0/36
[0.0%, 9.6%]. Pool A: 0/12 [0.0%, 24.3%]. All 60: 0/60
[0.0%, 6.0%]. (`fits=1` is reported only for certified schemas,
so train-fit-only is 0 by construction; full-fit accounting is
in §3.)

## 3. Fit → certified conversion (A+B)

- Full-fit coverage: **10/48 = 20.8%**, Wilson [11.7%, 34.3%].
- Of the 10 full fits: certified **0**; LOO-rejected 4;
  shape-LOO-rejected 3; nondeterminate test class 1;
  canvas-ambiguous 1; 1 found a full fit and exhausted the
  budget inside certification (fit-then-budget).
- Conversion: 0/10. Every full fit died at the frozen
  certification or at determinacy — stages this mechanism, by
  its own derivation (§7.1), does not claim to improve.

## 4. Death taxonomy (A+B, charged exactly as iterations 1–2)

| Sub-reason | Iter 3 | Iter 1 | Iter 2 |
|---|---|---|---|
| budget (lane deadline) | 17 | 20 | 24 |
| search_cap (enumeration caps) | 12 | 7 | 4 |
| fit-then-budget in certification | 1 | 1 | 0 |
| inconsistent_segmentation | 7 | 7 | 8 |
| loo_rejected | 4 | 3 | 4 |
| shape_loo_rejected | 3 | 3 | 2 |
| nondeterminate_test_class | 1 | 2 | 2 |
| inconsistent_param | 0 | 0 | 2 |
| creation_novel | 2 | 0 | 0 |
| creation_unexplained | 0 | 3 | 2 |
| inconsistent_delta | 1 | 1 | 0 |
| canvas_ambiguous | 1 | 0 | 0 |
| cover_failed | 0 | 1 | 0 |
| **certified solve** | **0** | **1** | **0** |
| total | 48 | 48 | 48 |

**Search economics did not shrink.** Charged on the derivation
§3 convention (budget + search_cap + fit-then-budget):
**30/48 = 62.5%**, against iteration 1's 28/48 and iteration 2's
28/48. The class total is invariant across all three
organizations of the same grammar — sweep, reordered sweep, and
intersection-first. The composition moved (cap deaths rose
4 → 12 as pruned covers reach their caps inside Stage B's
residual enumeration; budget deaths fell 24 → 17), the total did
not.

Pool C (control only): budget 4, search_cap 5,
inconsistent_segmentation 2, shape_loo_rejected 1 (its single
full fit); 0 solves.

## 5. Wall distribution and the cost model, measured against it

Per-task wall, A+B (run record): **median 12.25 s, mean
13.18 s, p90 25.0 s (the cap), max 25.03 s, sum 632.5 s.**
Distribution: <1 s: 12 tasks; 1–5 s: 6; 5–20 s: 9; ≥20 s: 21.
Deadline discipline holds: **0 tasks above 25.5 s on any pool**
(max anywhere 25.03 s) — iteration 1's overrun class stays dead.
The distribution is bimodal: tasks whose frames fit (or die
structurally) finish in seconds; the rest burn the frame sweep
to the deadline.

| Quantity | Modeled (§4, α=1) | Measured | Ratio |
|---|---|---|---|
| Median task (A+B) | 0.28 s | 12.25 s | ~44× |
| Mean task (A+B) | 1.40 s | 13.18 s | ~9× |
| p90 task | 3.1 s | 25.0 s (cap) | — |
| Worst task | 20.8 s (construction) | 25.03 s (cap, deadline-held) | — |
| 48-task wall (A+B sum) | ≈ 67 s | 632.5 s | ~9× |
| 60-task run wall | — | 809.0 s (≤ 1,200 protocol) | — |

The model is falsified on measurement, on the median clause by
~44×. Where the separation sits, on the evidence available (the
lane does not instrument stages inside the probe; this is the
reading the pre-checks and walls support, stated as such):
Stages A/B/C are cheap where they are reached — pre-check
(iii-b) shows induction + certification completing in ≤ 8.7 s
on 19 of 21 spent fit tasks, and the probe's own fits were
found in 0.16–2.8 s of their tasks' walls. The residual cost is
the frame sweep itself: Stage T candidacy is paid per
(pre-transform × account) frame — up to ~10³ frames — where
§4's T_cand priced the candidacy envelope once per task. The
derivation's §7.2 named this risk in advance (α=1 is an
envelope argument, not a measurement of new code); F6 exists
to close the mechanism on exactly this event, and it has.

## 6. Census-class tabulation of the draw (A+B, diagnostic)

Size class: same 33, shrink 10, grow 5. Train pairs per task:
2→5, 3→24, 4→12, 5→5, 6→2. Fates present (tasks): preserved
39, created 31, grown 21, deleted 19, recolored 18, shrunk 16,
scaled 9, reshaped 1. Tasks with any creation: 31/48.
Creation instances under the modal account, by source class
(first-match, derivation order): ring/mirror 945, copy 73,
witness 55, novel/residual 32, const 23, glyph-eligible 13,
symunion 6, field 4. Determinacy (census LOO substrate): 9/48
tasks fully determinate; mean determinate fraction 0.310 —
there are no solves whose profile could be contrasted.

## 7. Gates, applied strictly (§5)

- KILL (0 solves): **yes — the verdict.**
- WEAK (1–3): no. ALIVE (≥4 AND coverage ≥30% AND no
  override): no (solves 0, coverage 20.8%).
- F1 (coverage <15% caps at WEAK): not triggered (20.8%).
- F5 (≥half of full fits LOO-rejected caps at WEAK): strict
  reading — 4/10 (40%), not triggered; inclusive reading —
  counting shape-diverse holdout rejections, 7/10 (70%),
  triggered. Recorded; the verdict is KILL under both.
- F4 (C solves with zero A+B solves = KILL): not triggered
  (C = 0 solves).
- F3 (≥half of solves from a single lookup kind): not
  applicable (no solves).
- **F6 (economics): TRIGGERED on both clauses** — economics
  deaths 30/48 > 6/48; median A+B wall 12.25 s > 2.5 s. The
  mechanism's central claim is falsified on measurement; it
  is closed as designed and no economics iteration is
  permitted on it.

Consequence per §5: KILL and F6 falsification each close this
species. Three probes of the derived grammar now stand at 1/48,
0/48, 0/48 certified solves, with coverage 20.8%, 16.7%, 20.8%
and an economics class of 28, 28, 30 deaths — invariant under
sweep order and under intersection-first factoring alike. What
this probe banks, per the derivation's own §8: the failure is
clean in a way the two-probe record was not. Fit supply at
iteration 1's level was recovered with certification losses
fully exposed (10 fits, 0 conversions, every death charged),
fit retention against both frozen lanes is 21/21 on spent
tasks, and the economics wall is now measured at the candidacy
stage, not entangled with cover enumeration. The next
derivation starts from that discrimination. The sealed approval
exam remains unspent, and no solver is approved.

Ledger tag: `sieve_intersection_probe`. Files: solver
`derived_solver/ds_lane3.py`; design
`derived_solver/DESIGN_NOTE3.md`; controls
`derived_solver/controls_ds3.py` (ALL CONTROLS: PASS);
pre-checks `derived_solver/prechecks_ds3.py` (ALL PRE-CHECKS:
PASS, log `prechecks_ds3.log`); run
`gauntlet/runs/run_1793837074_seed20365108_sieve_intersection.json`;
diagnostic `derived_solver/diag_ds3.py`, rows
`derived_solver/diag_ds3_rows.json`; logs
`derived_solver/probe3_run.log`, `derived_solver/diag3_run.log`.
