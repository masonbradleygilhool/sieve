# BG-GATE — results (run 2026-11-07)

**VERDICT: PASS — migrated 15/17, background deaths 2/48, fits
preserved 4/4.** All three packet §2.3 PASS conditions hold.

Preregistration: BG_GATE_PREREGISTRATION_2026-11-07.md (filed
before the build and the run; bars, draw, definitions unchanged).
Groundwork: BG_GATE_RUN_PREP_2026-11-07.md. Rows:
`nextgen_probe/diag2_bg_rows.json`; run log:
`nextgen_probe/bg_gate_run.log` (48 tasks, 670.5 s total wall,
local CPU only).

## The three gate quantities, against the bars

| Quantity | Bar (PASS) | Measured |
|---|---|---|
| Bg-death tasks migrated past the background gate | ≥ 13/17 | **15/17** |
| Background-class deaths on the full 48 | ≤ 5/48 | **2/48** (17 before) |
| Banked full fits still fitting | 4/4 | **4/4** |

KILL conditions (≤6/17, ≥12/48, ≥2 fits lost): none approached.
The background-death count is by stage (designated attempt has no
functional account); the lane_reason string count of
`inconsistent_phi` over the 48 is also 2 — the same two tasks, so
no downstream phi-binding conflict inflates either count.

## The 17-task migration table

Before: every row `inconsistent_phi` (background stage). Subtypes
are the operational form of packet §2.1's patterns, read off the
modal pair sequence (the census's `subtype_of`; "other nonconstant
pattern" is its residue class beyond §2.1's three named patterns).
The identified map is the carrying account's generated
input-bg → output-bg map.

| Task | Pool | §2.1 subtype | After | Carrying account (seg, in-gen, out-gen) | Identified map |
|---|---|---|---|---|---|
| f4081712 | A | other nonconstant | **inconsistent_phi — still a background death** | none (0/32 functional) | — |
| 5833af48 | B | other nonconstant | cover_failed | agnostic, modal, modal | 0→4, 1→1, 3→3 |
| af22c60d | A | other nonconstant | creation_unexplained | agnostic, modal, sea | 4→4, 8→8 |
| 3194b014 | B | context-dependent output bg | canvas | agnostic, corner, modal | 0→8, 6→4, 8→3 |
| 5d2a5c43 | B | single-pair flip | creation_unexplained | agnostic, modal, modal | 0→8, 4→8 |
| 27f8ce4f | B | input modal not background | creation_unexplained | agnostic, modal, modal | 5→0, 7→0, 8→0, 9→0 |
| edcc2ff0 | B | other nonconstant | budget | agnostic, modal, modal | 1→1, 3→3, 8→8 |
| 9110e3c5 | B | single-pair flip | creation_unexplained | agnostic, modal, modal | 0→0, 3→0 |
| e9afcf9a | B | other nonconstant | creation_unexplained | agnostic, modal, modal | 3→3, 4→4 |
| e66aafb8 | A | other nonconstant | creation_unexplained | agnostic, modal, border_modal | 2→1, 5→5, 6→4, 9→9 |
| 55783887 | A | other nonconstant | creation_unexplained | agnostic, modal, modal | 4→4, 5→5, 8→8 |
| 67b4a34d | A | other nonconstant | creation_unexplained | agnostic, modal, modal | 2→2, 6→8, 7→7 |
| 1e97544e | A | other nonconstant | budget | agnostic, modal, modal | 4→4, 6→1 |
| c803e39c | B | context-dependent output bg | **inconsistent_phi — still a background death** | none (0/32 functional) | — |
| b7f8a4d8 | B | other nonconstant | budget | agnostic, modal, modal | 0→0, 3→3 |
| 47996f11 | A | other nonconstant | budget | agnostic, modal, modal | 3→3, 5→5, 7→7, 8→8 |
| a2d730bd | B | other nonconstant | budget | agnostic, modal, modal | 1→1, 3→3, 8→8 |

Where the migrated 15 now die: creation_unexplained 8, budget 5,
cover_failed 1, canvas 1. None reached certification and none fit —
the v2 probe §6 question (do they then die at cover, creation, or
certification) is answered on this draw: creation first, then the
search budget, cover, canvas; certification is not where they die.

Subtype readout: single-pair flip 2/2 migrated; input-modal-not-
background 1/1; context-dependent output background 1/2 (3194b014
is bound by the corner→modal account — the input's corner color
tracks the output background pair by pair; c803e39c is bound by no
generator account); other nonconstant 11/12 (f4081712 is bound by
no account in the family).

## Fit preservation (the 4 banked full fits)

| Task | Before | After | Account | Map |
|---|---|---|---|---|
| 7d1f7ee8 | full fit, loo_rejected | full fit, loo_rejected | agnostic, modal, modal | 0→0 |
| a61f2674 | full fit, nondeterminate_test_class | full fit, nondeterminate_test_class | agnostic, modal, modal | 0→0 |
| 4acc7107 | full fit, loo_rejected | full fit, loo_rejected | agnostic, modal, modal | 0→0 |
| 8dae5dfc | full fit, loo_rejected | full fit, loo_rejected | agnostic, modal, modal | 0→0 |

Fit-for-fit identical, certification outcome identical. Full-fit
coverage on the 48 is unchanged at 4/48; solved 0 before, 0 after.

## Re-charged taxonomy, full 48 (identical taxonomy)

| Class | Before | After |
|---|---|---|
| inconsistent_phi (background) | 17 | 2 |
| creation_unexplained | 16 | 19 |
| budget | 1 | 15 |
| search_cap | 5 | 4 |
| cover_failed | 4 | 2 |
| canvas | 1 | 2 |
| loo_rejected | 3 | 3 |
| nondeterminate_test_class | 1 | 1 |

The largest class in the re-charged taxonomy is now
creation_unexplained (19/48) — the wall the successor lane faces
after the background stage.

## Costs and limits, at full strength

- **Budget cost is real.** The account search multiplies per-task
  work; inside the frozen 25 s/task budget, budget deaths over the
  48 rose 1 → 15. Five of the 15 migrated tasks die at budget, and
  9 tasks outside the 17 were re-charged from a named downstream
  class (creation_unexplained / cover_failed / search_cap) to
  budget. They passed the background gate on generator arithmetic
  alone (stage passage is computed before any search and is not a
  budget artifact), but the lane resolves fewer of them to a named
  class at this budget. The three gate quantities are unaffected
  (fits 4/4, bg deaths counted by stage per the preregistration);
  the cost is inherited by any successor running this component at
  25 s/task.
- **Segmentation.** Every carrying account was agnostic (the
  lane's native segmentation, first in the declared order).
  Primary-segmentation accounts were in the searched space and
  functional on some tasks, but no task's passage was carried by
  one; whether primary segmentation is needed at lane level is not
  decided by this run.
- **Feature-dependent maps were not built** (preregistered scope:
  the census's plain functional rule). c803e39c is the visible
  residue — a context-dependent task bound by no generator
  account. A map that is a function of an identified scene feature
  (packet §2.2's further allowance) remains unbuilt and untested.
- **Component diagnostic on a spent draw.** Nothing here is a
  capability or conversion measurement; nothing projects to the
  240-task scale.

## The built component (diff surface)

New files only; the original lane and diagnostic are untouched.

- `nextgen_probe/ng2_lane_bg.py` — copy of `ng2_lane.py` with only
  the background stage replaced: generator import from the census
  operationalization (`census_param_bound.bg_generators`, so the
  definitions cannot diverge from the banked bound); the account
  search (`_accounts`, `_induce_under` → `_induce_under_account`);
  `segment_primary`; per-pair background resolution in
  `verify_schema` / `predict`; gate readout fields in `lane`.
  Verified by diff: `gen_candidates`, `_merge_candidates`,
  `pair_assignments`, `combine_iter`, `loo_check`,
  `_mechanism_tag`, and the 2-pair determinacy check are
  byte-identical to the original; caps, pretransforms, Occam
  order, and canvas rules unchanged. LOO re-identification is
  structural: `loo_check` calls the variant's `induce`, which
  re-runs the account search from each fold's pairs alone.
- `nextgen_probe/diag2_bg.py` — `diag2.py` on the variant lane
  (same run record, pools, budget, taxonomy), writing
  `diag2_bg_rows.json` with the before-record and the
  background-stage readout per task.

## Consequence (packet §2.3, §3, as registered)

A BG-GATE PASS is a component verdict on a spent draw: measured
component evidence, countable as the successor species' first gate
record at its registered bars. It is **not** a conversion
measurement, it does **not** approve a solver, and it does **not**
move the SIEVE axis — the axis moves only when a successor lane
converts on a fresh draw under the gauntlet protocol. What the
PASS establishes: the searched-background-identification component
clears the wall it was built against at lane level — the
modal-assumption death class falls from 17/48 to 2/48 with all
banked fits intact — so the bg-fixed v2-line lane holds the
successor seat as a component, and its next measured wall is
creation (19/48 in the re-charged taxonomy). The two tasks no
account binds (f4081712, c803e39c) stay charged to the background
class as the family's measured residue.

Repository note: `~/workspace/arc_apex2` is not a git repository —
nothing was committed; all artifacts are on disk at the paths
above.
