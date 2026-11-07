# BG-GATE — preregistration (filed 2026-11-07, BEFORE the build and the run)

## Why this gate fires

The Friday seat test closed FLAT NULL at full pre-registered draw
width (C1a-med 0/24 fits + C1b-med 0/24 fits = 0/48 fit-bearing,
0 certified; instrument healthy — 287/288 medium completions
finished 'stop'). Under NOVEMBER_CONVERSION_PACKET.md the FAIL
branch fires: the gpt-oss-120b proposer species is closed as a
standalone, and BG-GATE (packet §2.3) is the successor species'
first gate. It decides whether the v2-line lane with the §2.2
searched-background-identification component earns the successor
seat. Groundwork: BG_GATE_RUN_PREP_2026-11-07.md (extraction
verified from source).

## Instrument

`nextgen_probe/ng2_lane_bg.py` — a copy of `nextgen_probe/ng2_lane.py`
with ONLY the background stage replaced by the §2.2 component.
Everything else is byte-identical: grammar (derivation candidates,
exact cover, combination), caps (MAX_OBJECTS 20, CAND_CAP_PER_OUT 64,
MERGE_CAND_CAP 16, ASSIGN_CAP 16, ASSIGN_NODES 3000,
COMBINE_NODES 4000, SCHEMA_CAP 24), pretransform set and order,
Occam selection order, canvas rules, and the lane's frozen
certification (LOO re-induction for ≥3 pairs; 2-pair determinacy;
prediction unanimity). The Friday proposer certification
(sample_version_space.py / certify.py) is not part of this lane and
is not touched.

The replaced stage, exactly:

1. **Candidate generation.** Per train pair (after the attempt's
   pretransform, as in the original), background values are produced
   by the generator set {modal, border-modal, corner-color, sea}
   applied independently to the input grid and to the output grid.
   Generator definitions are imported unchanged from the census
   operationalization (`census/census_param_bound.py:bg_generators`,
   `GENS`) so the definitions cannot diverge from the banked bound.
2. **Accounts.** An account is (segmentation, input-generator,
   output-generator): segmentations {agnostic = the lane's own
   `ng.segment` (8-connected, color-mixed), primary = per-color
   4-connected components returning the same `ng.Obj` type} × 4 × 4
   generator pairs = 32 accounts. Declared trial order: agnostic
   accounts first (the lane's native segmentation), primary second;
   within a segmentation, generators in census GENS order — so
   (agnostic, modal, modal), the original lane's configuration, is
   tried first, and the first account (in this order) that yields
   verified schemas supplies the candidates, mirroring the original
   pretransform order discipline.
3. **Identification by cross-pair intersection.** An account
   survives the background stage iff the generated
   input-background → output-background values across the attempt's
   pairs form a FUNCTION (the census `functional` rule; packet
   §2.2 step 2). Accounts whose intersection is empty die in set
   arithmetic before any content candidate is generated under them.
   Scope note, declared in advance: this build implements the
   plain functional rule — the census's operationalization. The
   packet's further allowance (a map that is a function of an
   identified scene feature, for the context-dependent subtype) is
   NOT implemented; a task rescuable only by a feature-dependent
   map will still charge to the background class, and the readout
   will say so where the subtype pattern shows it.
4. **Account-relative segmentation.** Each surviving account runs
   the unchanged downstream pipeline with segmentation performed
   under that account (its segmentation mode; per-pair generated
   backgrounds). Bindings never leave their account.
5. **Per-pair backgrounds in schemas.** A schema carries its
   account and the identified map; rendering/verification resolve
   the background per pair. For a constant map this reduces exactly
   to the original lane's constant-pair behavior. Prediction on a
   new grid: output background = the identified map applied to the
   grid's generated input background (a constant map applies to any
   input, as in the original lane; an unseen key under a
   non-constant map abstains — the schema cannot render that grid).
6. **LOO discipline.** The background binding is re-identified
   inside every certification fold from the fold's pairs alone:
   `loo_check` calls `induce` unchanged, and `induce` re-runs the
   account search per fold. No full-task background verdict is
   imported into a fold.
7. **Failure designation.** Across pretransform attempts the
   original rule is kept (first failure is designated if no attempt
   succeeds). Within an attempt: if NO account is functional, the
   attempt dies at the background stage — ("inconsistent", "phi"),
   a background-class death. If ≥1 account is functional but none
   yields verified schemas, the designated failure is the first
   functional account's downstream failure — the task has passed
   the background gate and is charged downstream.

## Draw

The v2 probe's own spent A+B draw (n=48), from
`gauntlet/runs/run_1793817846_seed20261109_nextgen_v2.json` /
`nextgen_probe/diag2_rows.json`, task bodies from
`gauntlet/pools.json`. Component diagnostic on known tasks — it
claims no capability measurement. Budget: `lane(task, 25.0)` per
task, identical to diag2.py. Local CPU only; no GPU, no Kaggle, no
network.

The 17 background-death tasks, extracted by rule
(`lane_reason == "inconsistent_phi"` over A+B in diag2_rows.json;
verified: all 17 have non-singleton modal background pairs under
the identity pretransform, and all other 31 A+B tasks have
singleton modal pairs — the before-class is exactly the
background stage):
f4081712, 5833af48, af22c60d, 3194b014, 5d2a5c43, 27f8ce4f,
edcc2ff0, 9110e3c5, e9afcf9a, e66aafb8, 55783887, 67b4a34d,
1e97544e, c803e39c, b7f8a4d8, 47996f11, a2d730bd

The 4 banked full fits that must still fit (all pool B, from
diag2_rows.json `full_fit` over A+B): 7d1f7ee8, a61f2674,
4acc7107, 8dae5dfc.

## Readout

Per task over the full 48 (diag2_bg.py, a diag2.py copy on the
variant lane): pool, before class / lane_reason / full_fit, new
lane_reason, new class, new full_fit, background-stage passage in
the designated attempt, the carrying account (segmentation,
generator pair), and the identified background map where it differs
from the old constant modal pair. The 17-task migration table is
the primary row set; the full 48-task taxonomy is re-charged with
the identical taxonomy.

Definitions, fixed before the run:

- **Migrated** (packet: "migrate past the background gate — they
  solve, or die at cover, creation, or certification instead"):
  the task's designated attempt has ≥1 functional account. Its new
  charge is then its downstream outcome (solved / full fit / cover
  / creation / certification sub-reason / cap / budget), never the
  background class.
- **Background deaths after**: tasks among the 48 whose designated
  attempt has no functional account. (The lane_reason string count
  of "inconsistent_phi" is also reported for comparability; it can
  in principle include a downstream phi-binding conflict, and any
  such case will be named.)
- **Fits preserved**: the 4 banked tids with `full_fit` true under
  the variant.

## Bars (packet §2.3, quoted, fixed before the run)

- **PASS:** ≥ **13/17** of the bg-death tasks migrate past the
  background gate **AND** background-class deaths on the full 48
  fall to ≤ **5/48** **AND** all 4 of the v2 probe's full fits
  still fit under the new background stage.
- **WEAK:** 7–12/17 migrate, or background deaths land at 6–11/48
  → exactly one refinement iteration, aimed at the largest
  surviving subtype among the three in packet §2.1, re-tested on
  the same draw under the same bars. A second WEAK closes the
  component as designed. (This run reports a WEAK if it lands; the
  refinement iteration is the packet's prescribed next step, not
  part of this run.)
- **KILL:** ≤ **6/17** migrate, **OR** background deaths remain
  ≥ **12/48**, **OR** ≥ 2 of the 4 banked full fits are lost.

## Consequence, pre-stated (packet §2.3, §3)

- A PASS is a component verdict on a spent draw — measured
  component evidence, countable as the successor species' first
  gate record at its registered bars. It is NOT a conversion
  measurement, does NOT approve a solver, and does NOT move the
  SIEVE axis; the axis moves only when a successor lane converts
  on a fresh draw under the gauntlet protocol.
- A KILL is a clean result: the modal-assumption diagnosis was
  right about the v2 lane's accounting but the searched-account
  component does not reach the class at lane level, and the
  successor redraws from the re-charged taxonomy's largest class
  with the 17-task migration table as its starting evidence.
- Nothing in this gate projects 48-task numbers to the 240-task
  scale. The sealed exam, the Friday pack, and friday_tasks.json
  are untouched; the proposer is not re-run.
