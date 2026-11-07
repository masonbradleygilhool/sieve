# Next-Gen Solver v2 — Probe Results (2026-11-04)

Status labels: every number below is **measured** by the run or the
diagnostic named, unless marked otherwise. Gates were pre-registered in
`NEXTGEN_V2_DESIGN_2026-11-04.md` §8 before the lane was run.

## Verdict

**KILL** — per the pre-registered gates: F2 fired (0 accepted solves on
A+B) and F1 fired (full-fit coverage 8.3% < the 15% floor). F5 also
fired (75% of full-fit schemas LOO-rejected). The design is dead as a
solver. What it leaves behind is a taxonomy that re-diagnoses v1's
deaths on identical tasks and names the wall that actually binds first:
**background identification** (see §4–§5).

## 1. The run

- Lane: `nextgen_probe/ng2_lane.py` (design: `NEXTGEN_V2_DESIGN_2026-11-04.md`).
- Instrument: **unmodified** gauntlet (`arc_apex2/gauntlet/gauntlet.py`),
  `--draw A:12,B:36,C:12 --seeds 20261109 --budget 25`.
- Run record:
  `gauntlet/runs/run_1793817846_seed20261109_nextgen_v2.json`
  (60 tasks, partial = false, wall 59.5 s total, CPU only, $0, zero API
  calls).
- Seed rule (fixed in the design before the run): smallest seed
  ≥ 20261105 whose B and C draws are both disjoint from v1's draw.
  Verified against the run record after the fact: the drawn task ids
  match the pre-computed expectation exactly; **B overlap 0/36,
  C overlap 0/12**; A overlap 9/12 (unavoidable — pool A holds 18 tasks).
- Per-task diagnostic (sub-reasons, full-fit flags):
  `nextgen_probe/diag2.py` → `nextgen_probe/diag2_rows.json`.
  Re-running the lane reproduced the run record's class on **60/60**
  tasks (0 mismatches) — the lane is deterministic.

## 2. Controls (run before the probe; gate §8)

`nextgen_probe/controls2.py` — all hand-built, expected outputs placed
independently of the lane:

| control | result |
|---|---|
| Positive A — split-by-color + preserve, 3 pairs | **PASS** — solved, LOO-certified, tag `object_transform` |
| Positive B — grow-by-ring on a padded canvas, 3 pairs | **PASS** — solved, LOO-certified, canvas `pad` identified |
| Negative — A's outputs shuffled across pairs | **PASS** — no schema accepted (`inconsistent_delta`) |

## 3. Raw numbers (measured)

Primary metric = accepted solves on A+B (the fresh real pool), with the
gauntlet's Wilson 95% intervals:

| pool | n | solved | train_fit_only | no_fit | Wilson 95% |
|---|---|---|---|---|---|
| A (AGI-1 eval, record-fresh) | 12 | 0 | 0 | 12 | [0.000, 0.242] |
| B (AGI-2 train, record-fresh) | 36 | 0 | 0 | 36 | [0.000, 0.096] |
| **A+B** | **48** | **0** | **0** | **48** | **[0.000, 0.074]** |
| C (compositional, control) | 12 | 0 | 0 | 12 | [0.000, 0.242] |
| all | 60 | 0 | 0 | 60 | [0.000, 0.060] |

Accounting note (same as v1): `fits = 1` is reported only for
certified schemas, so tasks whose full-fit schema was LOO-rejected or
failed test determinacy appear as `no_fit` in the gauntlet. Their count
comes from the diagnostic: **full-fit coverage on A+B = 4/48 = 8.3%**
(Wilson [0.033, 0.196]); v1 measured 2/48 = 4.2% on its draw.

Gate-by-gate (§8 of the design):

| gate | outcome |
|---|---|
| F1 — coverage floor 15% | **TRIGGERED** (8.3%) |
| F2 — 0 solves ⇒ KILL | **TRIGGERED** |
| F3 — colormap-shadow cap | not applicable (no solves) |
| F4 — pool-C shadow | not triggered (C solves = 0) |
| F5 — ≥half of full fits LOO-rejected ⇒ over-generation | **TRIGGERED** (3/4 = 75%) |
| ALIVE (≥4 solves ∧ coverage ≥15%) | not met on either conjunct |
| WEAK-ALIVE (1–3 solves) | not met (0 solves) |

## 4. Death taxonomy for THIS design (A+B, n = 48, measured)

| sub-reason | n | what it means here |
|---|---|---|
| `inconsistent_phi` | **17** | the modal-background map is not a function across pairs — the lane dies **before object accounting starts** (decomposed below) |
| `creation_unexplained` | 16 | an output object has no derivation in the grammar (design §5.2's named class, now measured) |
| `search_cap` | 5 | candidate/assignment/combination caps exhausted |
| `cover_failed` | 4 | candidates exist but no exact cover with uniform class fates |
| `loo_rejected` | 3 | full fit, killed by LOO re-induction |
| `budget` | 1 | 25 s budget exhausted |
| `nondeterminate_test_class` | 1 | full fit (2 pairs); a test class has no fate and no single-unary fallback |
| `canvas` | 1 | bindings consistent, no canvas mode reconstructs the outputs |

Pool C (n = 12): `inconsistent_phi` 11, `creation_unexplained` 1.

### 4.1 The 17 background deaths, decomposed (measured)

All 17 are the **background-map check**, none are object-level φ
conflicts: for every one, the (modal input color → modal output color)
pairs across the task's train pairs fail to form a function. The pairs
themselves show three visible patterns (tids are from
`diag2_rows.json`; pair lists are (bg_in → bg_out) per train pair):

- **Output background is context-dependent**: same input background,
  different output backgrounds — e.g. `3194b014`: 0→3, 0→4, 0→8;
  `c803e39c`: 0→3, 0→8, 0→8. The output's dominant color is plausibly
  set by scene content (or is a drawn panel, not background).
- **Input modal color is not the background**: input modals vary while
  the output background is constant — e.g. `27f8ce4f`: 5→0, 7→0, 9→0,
  8→0. A large colored region out-counts the true background in the
  input, so segmentation itself is built on the wrong background.
- **Single-pair modal flips**: the map is functional except one pair
  where an object outgrows the background — e.g. `9110e3c5`: six pairs
  0→0 and one 3→0; `5d2a5c43`: four pairs 4→8 and one 0→8.

Only 4 of the 17 involve a tied modal color in some pair, so tie
-breaking is a minor contributor. The failure is the identification
assumption itself: **background = modal color, mapped by one
function** — stated in the design as a primitive, now measured as the
single largest death class (17/48 = 35%).

### 4.2 Full-fit autopsy (the 4 tasks that fit, all pool B)

| tid | mechanism tag | fate |
|---|---|---|
| `7d1f7ee8` | `object_schema` | LOO-rejected |
| `8dae5dfc` | `object_schema` | LOO-rejected |
| `4acc7107` | `object_transform` | LOO-rejected |
| `a61f2674` | `object_schema` | determinacy-rejected (2 pairs) |

The transformation grammar produced exactly **one**
transformation-tagged full fit on 48 tasks, and certification killed
it. Coverage doubled over v1 (4.2% → 8.3%, cross-draw — see §5 caveat)
while the fit→certified conversion stayed at 0/4.

## 5. Paired comparison with v1 (the 9 pool-A tasks both probes drew)

v1 and v2 drew different B and C tasks by design, so cross-probe count
comparisons are indicative only. The 9 shared pool-A tasks are a true
paired sample — same tasks, both lanes (v1 stages from
`diag.py`/`diag_rows.json`, v2 from `diag2_rows.json`):

| tid | v1 death | v2 death |
|---|---|---|
| 08573cc6 | creation_or_splitmerge | creation_unexplained |
| 1e97544e | creation_or_splitmerge | **inconsistent_phi (bg map)** |
| 55783887 | creation_or_splitmerge | **inconsistent_phi (bg map)** |
| 604001fa | creation_or_splitmerge | creation_unexplained |
| 67b4a34d | no_shape_compatible_transform | **inconsistent_phi (bg map)** |
| 79fb03f4 | creation_or_splitmerge | search_cap |
| af22c60d | creation_or_splitmerge | **inconsistent_phi (bg map)** |
| e66aafb8 | no_shape_compatible_transform | **inconsistent_phi (bg map)** |
| f4081712 | no_shape_compatible_transform | **inconsistent_phi (bg map)** |

On identical tasks, **6 of v1's 9 "creation/split-merge" and "size"
deaths were background-identification failures** that v1's taxonomy
could not see (its diagnostic attributed deaths by object accounting
without isolating the background gate). v1's headline — "creation
killed 35/48" — was, in substantial part, a segmentation artifact.

## 6. What the measurement says (strength-labeled)

1. **(measured)** The first wall is no longer the rule grammar. It is
   background/segmentation identification: 17/48 die there, before any
   rule is induced. Any successor that keeps "background = modal
   color" inherits this ceiling regardless of grammar.
2. **(measured)** Widening the grammar to first-class transformation
   doubled full-fit coverage and still converted 0/4 through
   certification (F5 fired: 75% LOO-rejected). Fit rate is not the
   scarce quantity; **certified generalization is**.
3. **(measured)** Unexplained creation remains the second wall
   (16/48): output content the derivation grammar cannot reach —
   design §5.2's class (parameter-object/drawing rules), now sized.
4. **(measured)** The machinery's own caps bind on 6/48 (5 search_cap
   + 1 budget) — third-order, but nonzero at 25 s/task.
5. **(inference)** The cheapest decisive next experiment is not a
   wider grammar: it is **background identification as a first-class
   identified object** — per-pair background candidates (not just the
   modal color) carried through the same intersection discipline, with
   the background rule allowed to be a function of an identified scene
   feature. The 17-task class is directly re-testable: a bg-fixed lane
   variant on this same draw would show within an hour whether those
   tasks then die at cover, creation, or certification.
6. **(inference)** v1+v2 jointly bound the object-schema family:
   two grammars, two fresh draws, zero certified solves, and the
   deaths concentrate at identification stages (background, creation)
   that precede rule choice. A third grammar in the same family,
   without solving background identification and parameter-object
   semantics, is pre-registered here as expected-dead on arrival.

## 7. Implementation corrections recorded (transparency)

Two points where implementation completed or corrected the design as
written; both are recorded here, the design doc stands as written
pre-run, and neither changes any gate:

1. **Schema selection order.** The design says identified schemas are
   certified by LOO but does not fix *which* verified schema the lane
   commits to when several fit. As first built, the lane committed to
   the first found — and control A demonstrated the failure: a
   spurious copy-based schema that fit a 2-pair sub-problem through a
   clipping accident was selected and LOO rejected the *rule*, when
   the true schema was also in the space. The lane now commits to the
   lexicographic minimum under (creations, deletions, bindings), all
   tied minima are carried, LOO is set-valued (candidate minima must
   unanimously predict each held pair), and test predictions must be
   unanimous across minima (else abstain: `ambiguous`). This is an
   Occam order over the constructed space, fixed in code before the
   run, not tuned per task.
2. **Pad parameterization.** The design's §4 pad rules (constant
   offset / centered / bottom-right) are unidentifiable distinctions
   once binding deltas are measured in output coordinates: with a
   uniform background, the input frame's position inside the output
   canvas is observable only through object deltas, which the
   bindings already carry. The implemented canvas model is therefore
   unified — render on the output-shaped canvas — and pad is
   parameterized by its totals only, which are identified exactly.
   Nothing identifiable was lost; §4's three rules collapse to one
   because they were never three rules.

## 8. Files

- Design + pre-registered gates: `NEXTGEN_V2_DESIGN_2026-11-04.md`
- Lane: `nextgen_probe/ng2_lane.py`
- Controls: `nextgen_probe/controls2.py` (3/3 PASS)
- Run record: `gauntlet/runs/run_1793817846_seed20261109_nextgen_v2.json`
- Diagnostic: `nextgen_probe/diag2.py`, `nextgen_probe/diag2_rows.json`
- Ledger: `PROBE_LEDGER.jsonl` (record appended, tag `nextgen_v2_probe`)
