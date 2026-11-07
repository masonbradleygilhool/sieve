# SIEVE — Iteration 2 Probe Results (2026-11-04)

Search-economics iteration of the derived-grammar solver (iteration 1:
`DERIVED_SOLVER_PROBE_RESULTS_2026-11-04.md`, verdict WEAK-ALIVE, 1/48). The
grammar, the certification, the gauntlet, the census tooling, and the 25 s/task
budget are unchanged from iteration 1 — frozen by the commission. What changed
is ordering, budgeting, memoization, and deadline enforcement only
(`derived_solver/DESIGN_NOTE2.md`, `derived_solver/ds_lane2.py`).

## Verdict: KILL

**0/48 certified solves A+B** (A 0/12, B 0/36), Wilson 95% [0.0%, 7.4%].
Pre-registered bands: ALIVE = ≥4/48 solves AND coverage ≥30%; WEAK = 1–3
solves; KILL = 0. The measured point is 0, so the band is KILL.

Full-fit coverage: **8/48 = 16.7%**, Wilson 95% [8.7%, 29.6%] (A 0/12,
B 8/36 = 22.2% [11.7%, 38.1%]) — below iteration 1's 20.8% [11.7%, 34.3%] and
below the 30% ALIVE floor. The two coverage intervals overlap; the verdict
follows the pre-registered bands on the measured points, not a significance
claim.

**Mandatory statement, as commissioned:** this is the last iteration this
design receives on this evidence — a second WEAK or a KILL closes the
derived-grammar species and the desk redraws from the two-probe record; an
ALIVE starts the freeze-and-exam sequence by separate order. The measured
outcome is a KILL. The derived-grammar species is therefore closed by this
result. The sealed approval exam was not read, run, or touched; it remains
unspent.

## 1. Protocol as run

- Draw: seed **20271132** — the smallest seed ≥ 20261165 whose B and C draws
  are disjoint from the draws of seeds 20261103, 20261104, 20261109, 20261164
  and smoke 999 (sampling replicated exactly from the gauntlet; all five prior
  run records' drawn sets reproduced before scanning). Pool A has 18 tasks
  total, so the 12-task A draw necessarily overlaps prior A draws (12/12);
  B/C disjointness is the enforceable part, per iteration 1's §6.1 precedent.
  Draw spec A:12, B:36, C:12.
- Controls: all five re-run against `ds_lane2` and **PASS** before the draw
  (split-by-color, grow+pad, field-extension, cross-pair copy, abstention,
  negative) — the passing run is the one recorded in §5, after the correction
  described there.
- Run: `gauntlet/runs/run_1793832491_seed20271132_sieve_iter2.json`, complete
  (not partial), wall **952.6 s** of the exam protocol's 6,000 s parameter,
  CPU only, $0. Diagnostic: `derived_solver/diag_ds2.py` on the run record —
  0 record/re-run mismatches (record is uniformly no_fit; no re-run accepted).

## 2. Conversion

8 full fits, **0 certified** (iteration 1: 10 full fits, 1 certified). Of the
8: LOO-rejected 4, shape-LOO-rejected 2, nondeterminate test class 2. Every
full fit this probe found died at certification or determinacy — stages whose
strength is frozen and was not touched. No fit-then-budget death occurred
(iteration 1 had 1).

## 3. Death taxonomy A+B (charged exactly as iteration 1)

| class | iter 2 | iter 1 |
|---|---|---|
| budget (lane deadline) | 24 (50.0%) | 20 |
| search_cap (enumeration caps) | 4 (8.3%) | 7 |
| fit-then-budget in certification | 0 | 1 |
| inconsistent_segmentation | 8 (16.7%) | 7 |
| loo_rejected | 4 | 3 |
| shape_loo_rejected | 2 | 3 |
| nondeterminate_test_class | 2 | 2 |
| inconsistent_param | 2 (4.2%) | 0 |
| creation_unexplained | 2 (4.2%) | 3 |
| inconsistent_delta | 0 | 1 |
| cover_failed | 0 | 1 |
| **certified solve** | **0** | **1** |
| total | 48 | 48 |

Pool C (control only): budget 7, search_cap 2, inconsistent_segmentation 1,
creation_novel 1, creation_unexplained 1; 1 full fit (LOO-rejected); 0 solves.

**The search-economics class did not shrink.** Charged as iteration 1 charged
it (lane-budget + enumeration caps, fit-then-budget counted with them):
28/48 = 58.3% in iteration 2 vs 28/48 = 58.3% in iteration 1 (20 + 7 + 1).
The composition moved — enumeration-cap deaths fell 7 → 4 while budget deaths
rose 20 → 24 — but the total is identical. The prior ordering, staged
budgeting, and memoization changed *which* wall the same tasks hit, not how
many tasks the search closes inside 25 s. On this evidence the binding
constraint is the size of the account × pre-transform × candidate space
relative to per-node cost, not the order in which it is swept.

## 4. Wall time and deadline discipline

Per-task elapsed, A+B (run record): mean 14.29 s, median 19.86 s, max
**25.01 s**; 24/48 tasks ≥ 20 s; 23/48 reached the 25 s cap; **0 tasks above
25.5 s** on any pool. Iteration 1's recorded instrument defect — a task
overrunning to 43.7 s through unticked census paths in the table stage —
**does not recur**: the table build is now ticked between per-pair census
evaluations and a SIGALRM watchdog raises the lane's own Timeout at the task
budget on every path. Pre-probe verification on iteration 1's own overrun
tasks: ac0c5833 43.7 s → 25.02 s, 2c0b0aff 28.0 s → 25.01 s, both recorded as
budget deaths. Total wall 952.6 s (iteration 1: 972.1 s), inside the 6,000 s
protocol parameter. The probe ran under box contention (load ~2.5–3 from
unrelated lanes); elapsed values are wall-clock, as in iteration 1.

## 5. The one correction that mattered (certification integrity)

An early iteration-2 change — seeding each LOO fold with the parent
induction's winning (pre-transform, account) — was implemented, measured, and
**removed before the probe**. On control 2 (field-extension), the seeded fold
fit its subset under the parent's account but mispredicted the held pair,
where iteration 1 and the unseeded sweep both pass: `induce` returns the first
fit, so seeding changes *which schema a fold is judged on* — it reaches into
certification's judgment, not merely its speed, and it turned a passing
control into a rejection. The hint was removed from every path; folds sweep
exactly as the main induction does; the controls were re-run and pass 5/5.
Certification in this probe is iteration 1's certification, criterion for
criterion. Recorded in full in `DESIGN_NOTE2.md` item 5.

## 6. Equivalence evidence (engineering checks, spent-draw tasks only)

- Per-account candidate sets under `ds_lane2` are identical to `ds_lane` on
  five sampled pool-B tasks under the canonical account at id|x1, except on
  outputs that reach the 64-candidate cap, where the surviving 64 differ by
  the licensed prior order (7 such outputs on one task). Fit verdicts
  identical on all five.
- Table-build values identical where both lanes build; iteration 1's solve
  ad38a9d0 still solves and certifies under `ds_lane2`.
- Grammar/candidacy/selection-key code paths are byte-identical in effect:
  enumeration caps, the (binds, −determinacy) selection key, and every
  certification criterion are unchanged constants and code from iteration 1.

## 7. Draw tabulation (A+B, census classes, diagnostic §6.5)

Size: same 37, shrink 10, grow 1. Train pairs: 2→9, 3→23, 4→8, 5→3, 6→4,
7→1. Fate task counts: preserved 34, created 25, grown 22, deleted 21,
recolored 19, shrunk 16, scaled 12, reshaped 3. Creation instances (modal
account, first-match derivation order): ring/mirror 960, copy 31,
novel/residual 10, glyph-eligible 9, witness 3, const 2 — 25/48 tasks carry
some creation. Determinacy: mean LOO-determinate fraction 0.314; 9/48 tasks
fully determinate; the 8 full fits include the 2 nondeterminate test-class
deaths above.

## 8. Grammar gaps — reported, not patched (per the freeze)

No grammar change was made. The classes that name grammar-level absences on
this draw: creation_unexplained 2, inconsistent_param 2, and
inconsistent_segmentation 8 (no consistent background rule under the canonical
account — the diagnostic's charging convention, unchanged from iteration 1).
These are recorded for the redraw; nothing here proposes a mechanism.

## 9. Distance, stated plainly

Two probes of the derived grammar now stand at 1/48 and 0/48 certified solves
with coverage 20.8% and 16.7%, against a census fit-reach bound of 98.2% and
an approval bar of 216/240 on the sealed exam. Search economics — the largest
death class of iteration 1 — was given its one commissioned iteration and did
not convert: the class total is unchanged, coverage did not rise, and every
full fit found died at the frozen certification. What the iteration did bank:
hard deadline discipline (the 43.7 s overrun class is eliminated, verified on
the original offending tasks) and a demonstrated guard — a change that would
have quietly weakened certification was caught by the controls and removed
before it could touch a measurement. Per the pre-registered statement in the
verdict block, the derived-grammar species is closed on this evidence. The
sealed approval exam remains unspent, and no solver is approved.

Ledger tag: `sieve_iteration2_probe`. Files: solver
`derived_solver/ds_lane2.py`; design `derived_solver/DESIGN_NOTE2.md`;
controls `derived_solver/controls_ds2.py` (ALL CONTROLS: PASS, post-correction
run); run `gauntlet/runs/run_1793832491_seed20271132_sieve_iter2.json`;
diagnostic `derived_solver/diag_ds2.py`, rows
`derived_solver/diag_ds2_rows.json`; logs `derived_solver/probe2_run.log`,
`derived_solver/diag2_run.log`.
