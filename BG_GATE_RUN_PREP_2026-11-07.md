# BG-GATE run prep — verified 2026-11-07 (proactive research run, ~6:40 AM ET)

Status: PREPARED, NOT RUN. No BG-GATE artifact exists on disk yet
(checked 2026-11-07: `nextgen_probe/` has no files newer than
2026-11-04; the §2.2 component is spec-only in the packet —
"spec only — no build in this packet"). This prep removes the
extraction and verification lag so the gate can fire the moment
the desk commissions it.

## Why now

- C1a seat verdict is one half from final: medium effort, first 24
  tasks, 143/144 completions finish cleanly, fits still **0/24**
  (main chat 2026-11-07T10:17:18Z). Remaining 24 of the
  pre-registered 48 are running; on current evidence the packet's
  fail branch is what waits (main chat, same message).
- Packet sequencing: BG-GATE "fires Nov 7 morning regardless of
  the census update" (NOVEMBER_CONVERSION_PACKET.md §2.3). The
  census update it needed is already banked
  (CENSUS_UPDATES_2026-11-06.md; `census/bg_census_2026-11.json`,
  2026-11-06 22:10) — rescue rate 113/130 = 86.9% of modal binding
  failures reachable by searched background identification,
  against the gate's 13/17 = 76.5% PASS bar (different
  denominators; ceiling arithmetic, not a prediction).

## Verified extraction (recomputed from source this run)

Source: `nextgen_probe/diag2_rows.json` (60 rows; A+B = 48).

- Background-death class = `lane_reason == "inconsistent_phi"`
  on pools A+B: **exactly 17 tasks** — matches
  NEXTGEN_V2_PROBE_RESULTS_2026-11-04.md §4 (17/48 = 35%, the
  largest death class) and the packet §2.3 extraction rule
  (by rule from diag2_rows, not hand-listed).
- The 17 tids, in file order:
  f4081712, 5833af48, af22c60d, 3194b014, 5d2a5c43, 27f8ce4f,
  edcc2ff0, 9110e3c5, e9afcf9a, e66aafb8, 55783887, 67b4a34d,
  1e97544e, c803e39c, b7f8a4d8, 47996f11, a2d730bd
- The 4 banked full fits that must still fit under the new
  background stage (PASS condition 3), all pool B:
  7d1f7ee8 (loo_rejected), a61f2674 (nondeterminate_test_class),
  4acc7107 (loo_rejected), 8dae5dfc (loo_rejected)

## Instrument and bars (packet §2.3, unchanged)

- Instrument: v2-line lane (`nextgen_probe/ng2_lane.py`, diagnostic
  `nextgen_probe/diag2.py`) with ONLY the background stage replaced
  by the §2.2 component: candidate backgrounds from generators
  {modal, border-modal, corner-color, sea} per pair/side;
  identification by cross-pair intersection over the 32 accounts
  (2 segmentations × 4×4 generator pairs); account-relative
  segmentation; LOO re-identification inside every fold.
  Grammar, caps, 25 s/task budget, frozen certification unchanged.
  Local CPU only; no GPU, no Kaggle quota.
- Draw: the v2 probe's own spent A+B draw (n=48). Component
  diagnostic on known tasks — claims no capability measurement.
- PASS: ≥13/17 migrate past the background gate AND background
  deaths on the full 48 fall to ≤5/48 AND all 4 full fits above
  still fit. WEAK: 7–12/17 migrate, or bg deaths 6–11/48 → exactly
  one refinement iteration at the largest surviving subtype.
  KILL: ≤6/17 migrate, OR bg deaths ≥12/48, OR ≥2 of the 4 fits lost.
- Readout: full 48-task taxonomy re-charged with the identical
  taxonomy; each of the 17 gets its new death class as the primary
  row set.

## What remains (desk-side, in order)

1. Build the §2.2 background component into a bg-fixed lane variant
   (the only unbuilt piece; ng2_lane.py lines ~1090–1093 still carry
   the modal-only check `bg_pairs = {(modal_color(gi), modal_color(o))}`).
2. Run the gate on the 48; write the 17-task migration table.
3. Report the verdict at the strength the table supports. A PASS is
   a component verdict on a spent draw — not a conversion
   measurement, and it does not move the SIEVE axis until a successor
   lane converts on a fresh draw (packet §3).
