# Survivor-Set Census — the §1.4 measurement of the Conversion Derivation

**Date:** 2026-11-04 (run completed 2026-11-05 ~03:55 UTC)
**Instrument:** `derived_solver/survivor_census.py` (analysis-only; no lane changed)
**Rows:** `SURVIVOR_SET_CENSUS_ROWS_2026-11-04.json` (28 per-task records; working file `derived_solver/survivor_census_rows.json`)
**Population:** the 28 spent A+B full-fit tasks of the three derived-grammar probes (iter1 10, iter2 8, iter3 10). Spent draws only; the sealed approval exam was never read, run, or touched. Cost $0.

## Verdict

**The version-space (Stage-V) conversion mechanism is closed as a path to the criterion — under every treatment of the cases this census could not decide.** The registered falsifier F-unanimity (U < 0.50) fires on the conservative all-fits reading (U = 0.321) and is denominator-sensitive on the determined-only reading (U = 0.692, CI straddling 0.50); the closure does not depend on that choice, because the criterion arithmetic fails under *every* completion of the undecided cases: even granting all 15 undetermined tasks as unanimous, U ≤ 24/28 = 0.857 and F·U ≤ 0.982 × 0.857 = **0.842 < 0.90**. The U ≥ ~0.85 reopen threshold is not met by any measurement — 0.857 is an unexcluded bound, not a measured value, and it still loses. Separately, the solve-relevant rate is measured outright: **unanimous ∧ correct = 1/28** — eight of the nine unanimous version spaces are unanimously *wrong*, the systematic-shared-binding species the derivation named in §2. A Stage-V solver over this grammar would convert this fit population at the same 1/28 the frozen certification achieved, not because certification was too strict, but because the survivor sets that do speak with one voice are usually wrong together.

The (b)/(c) split the derivation left unmeasured is now measured, and it reverses the derivation's center of gravity: **fold rejections are overwhelmingly (b) certification dynamics — 17 of 19 tasks, 58 of 64 rejecting folds — including all four census-fully-witnessed tasks (14/14 folds).** Fit quality (c) accounts for 2 of 19 tasks. Charge (b) was real and large; removing it (Stage V's design goal) still does not reach the criterion, because the surviving constraint is (a): the version spaces themselves, wrong or plural, on test inputs the train pairs do not govern.

## (i) Parent-schema re-judgment — the (b)/(c) split

Method: each probe's own frozen induction was re-run under its own conditions; the recovered parent schema was judged directly on every held pair through the lane's own predict path. A rejecting fold whose parent prediction set is exactly the held output is class **(b)** (the fold's re-induction, not the parent, failed); a fold whose parent set excludes the held output is class **(c)**; a plural parent set containing the held output is recorded as its own sub-class (none occurred). Fold verdicts were taken from the lane's `loo_eval` given a fresh 25 s deadline of its own (the lanes' shared-deadline slicing starves LOO on re-run; the judgment rule is unchanged — deviation and reason recorded per task as `loo_deadline_mode`).

Results, over the 19 fold-rejection fits (11 LOO + 8 shape-LOO):

| Level | (b) certification dynamics | (c) fit quality |
|---|---|---|
| Tasks | **17 / 19** | **2 / 19** |
| Rejecting folds | **58 / 64 (90.6%)** singleton-correct | 6 / 64 excludes-correct |

- The two (c) tasks are both iter3: **c909285e** and **67b4a34d** — all three rejecting folds exclude-correct in each. Both are also unanimous-and-wrong in part (ii): genuinely wrong rules whose version spaces agree with them.
- **Fully-witnessed tasks (census fraction 1.0) — all four named tasks are class (b), 14/14 folds:** ce4f8723 (4 folds), caa06a1f (3), d9fac9be (4), e4888269 (3). On tasks where the census says every binding is witnessed, the parents were right on every held pair and certification still killed them. The derivation's firm-(b) floor of 0 with an unseparated band is resolved: on fully-witnessed tasks the band is entirely (b).
- e4888269 disclosure: its parent is recoverable and was measured class (b) in the clean pre-run validation (all 3 folds singleton-correct, loo fail). In the full run and in one standalone rerun, its `loo_eval` starved under VM contention and returned timeout with empty folds; those two artifacts are recorded in its row and are not evidence against the validation measurement.
- Not applicable, stated plainly: the 9 non-fold-rejection fits (5 nondeterminate, 2 fit-then-budget, 1 canvas-ambiguous, 1 certified) have no fold rejections to split; parent re-judgment is defined on LOO folds and was not forced onto them. No parent schema was unrecoverable among the 19; none was reconstructed.

As shares of all 27 fit deaths (the derivation's §1.1 ledger): (b) 17/27 = 63%, (c) 2/27 = 7%, the remaining 8/27 are the nondeterminate/canvas/budget deaths outside the (b)/(c) question.

## (ii) Survivor-set width and unanimity

Method: for each task, the intersection lane's frame sweep was replicated; at the winning frame, Stage-A per-key survivor sets (fate + witness bindings intersected across all pairs) were retained, and **all** cover-feasible schemas of that frame were enumerated across all three attempt families and all background rules (the lane's 8-schema cap does not apply to the version space). Caps: 20,000 combinations, 512 schemas (one task re-run at 4,096 — see below), 120 s wall per task. A cap hit is recorded as **undetermined**, never silently absorbed. Unanimity: enumerated schemas rendered on the task's actual test input via the lane's predict path; unanimous iff exactly one distinct rendered grid *and* enumeration completed. Test outputs were used only to flag whether a unanimous rendering is correct; they entered no identification. The survivor set is the derivation's specified instrument — the factored set of the intersection lane's Stage-A/B machinery, within the winning frame; 26/28 rows' winning accounts match the original probes' diag accounts (flags in the rows).

**Determination:** 13 of 28 tasks determined — **9 unanimous, 4 non-unanimous** (e4888269, 1fad071e, 1d61978c, bd283c4a; each produced ≥2 distinct test renderings within its completed enumeration). **15 undetermined:** enumeration hit the schema/combo caps (spaces of 594–7,917+ enumerated cores) with exactly 1 distinct rendering in the enumerated prefix in every case. One undetermined task, e45ef808, was re-run at raised caps (4,096 schemas / 60,000 combos) and exhausted: 2,196 schemas, unanimous (wrong). The remaining 14 spaces are not exhaustible at any cap this budget buys.

**U, all treatments:**

| Treatment | U | Wilson 95% |
|---|---|---|
| Conservative (undetermined count against unanimity), n=28 | **9/28 = 0.321** | [0.179, 0.507] |
| Determined-only, n=13 | **9/13 = 0.692** | [0.424, 0.873] |
| Absolute ceiling (all 15 undetermined unanimous) | 24/28 = 0.857 | — (bound, not a measurement) |

**Wilson arithmetic check:** the derivation stated n=28 gives ~±18 pts. Confirmed as the worst case: at p̂ = 0.5 the Wilson half-width is ±17.4 pts; at the measured p̂ = 0.321 it is ±16.4 pts.

**Unanimous ∧ correct = 1/28 = 0.036, Wilson [0.006, 0.177]** — ad38a9d0, the program's one certified solve. The other eight unanimous sets (caa06a1f, aabf363d, ecaa0ec1, d9fac9be, c909285e, 67b4a34d, be03b35f, e45ef808) force a unique test prediction that is wrong. Two of them (d9fac9be, c909285e) are single-schema version spaces: complete determinacy, wrong answer.

**Width distribution:** Stage-A plural (unresolved) keys per task: median 8, mean 9.29, range 0–35 (4 tasks fully determined at Stage A). Widest single key per task: median width 16, range 0–40. Realized version-space sizes (determined tasks): median 112 schemas, range 1–2,196. Across all 28 tasks, distinct test renderings never exceeded **2** — the spaces are wide in binding space but the test input discriminates at most one binary split wherever enumeration completed.

**U by census witnessing fraction** (unanimous / n, undetermined in parentheses): fraction 0.0 → 4/15 (10 undet.); 0 < frac < 1 → 1/5 (3 undet.); fraction 1.0 → 3/7 (2 undet.); pool A (no census row) → 1/1. No witnessing band rescues U: the fully-witnessed band's determined rate is 3/5, and its ceiling is 5/7 = 0.714. The schema-level measurement lands *above* the derivation's proxy band (0.27–0.36) on the determined subset and *inside* it on the conservative reading — the proxy-vs-schema comparison the derivation asked for is therefore: the proxies priced the conservative number, not the determined one, and the difference is entirely the 15 undecided spaces.

**By probe:** iter1 2/10 unanimous (8 undet.), iter2 2/8 (5 undet.), iter3 5/10 (2 undet.).

## (iii) The verdict arithmetic

Against the criterion F·U ≥ 0.90, using the derivation's own supply rows:

| Supply F | × U = 0.321 (cons.) | × U = 0.692 (det.) | × U = 0.857 (ceiling) |
|---|---|---|---|
| Measured 0.208 | 0.067 | 0.144 | 0.178 |
| Bound 0.982 | 0.316 | 0.680 | **0.842** |

- **Reopen (U ≥ ~0.85): does not occur.** No measured treatment reaches it; the only figure above 0.85 is the unexcluded ceiling, and at bound supply it still yields 0.842 < 0.90. The build decision does not return with a live path.
- **F-unanimity (U < 0.50): fires on the conservative reading** (0.321; the Wilson upper bound 0.507 sits at the line, the point estimate does not). On the determined-only reading it does not fire (0.692 [0.424, 0.873]). The falsifier's letter is denominator-sensitive and is reported as such.
- **The closure is not denominator-sensitive.** F·U < 0.90 under every completion of the undetermined cases and every supply row the derivation offers. The version-space mechanism, as the path to 216/240 over this grammar, is closed on this measurement — by the ceiling argument where the falsifier's letter is ambiguous, and by the falsifier where it is not.
- **What the number leaves open, exactly:** (1) U itself is not pinned — the determined-only interval reaches 0.873, so a future instrument that exhausts wide version spaces (or decides unanimity by test-relevant-key projection rather than enumeration) could move the estimate; it cannot move the ceiling enough to reopen the criterion arithmetic unless it also overturns determined cases. (2) The binding constraint has moved, measurably, to charge (a): of the determined fits, the dominant failure is no longer certification dynamics but the version spaces' content — plural where they should force (4/13), unanimously wrong where they do force (8/9). Any future mechanism must attack grammar expressiveness / shared-wrong bindings, not conversion. (3) Nothing here touches fit supply: F at measured 0.208 caps the product at 0.208 regardless of U.

## Cost and integrity

Total compute ≈ 28 CPU-minutes (smoke + validation ~6 min, one VM-reboot-killed partial run ~5 min, full run 1,100 s, raised-cap redo ~1 min) — inside the task's ~1 CPU-hour stop line, above the derivation's ≤12 CPU-min re-run sketch; the difference is the collect-all survivor enumeration, which the sketch priced as retention during a lane re-run. Disclosed, not expanded: no further caps were raised after e45ef808, whose space proved exhaustible; the other 14 undetermined spaces (≥2,880 cores, up to 7,917 enumerated without exhaustion) were left undetermined rather than chased. The VM rebooted mid-run once; rows are checkpointed per task and the run resumed — every re-run task reproduced its pre-reboot prefix. Census instrumentation: `derived_solver/survivor_census.py`; per-task rows in the JSON beside this file, including cap details, account-match flags, redo notes, and the e4888269 contention artifacts.

## Per-task rows (summary; full records in the JSON)

| task | probe | death | frac | plural keys | max width | schemas | distinct | unanimous | correct | parent |
|---|---|---|---|---|---|---|---|---|---|---|
| 29c11459 | iter1 | nondeterminate | 0.0 | 8 | 16 | 512* | 1 | undet. | — | — |
| 6430c8c4 | iter1 | loo_rejected | 0.75 | 9 | 18 | 512* | 1 | undet. | — | b |
| 67636eac | iter1 | shape_loo_rejected | 0.667 | 3 | 16 | 512* | 1 | undet. | — | b |
| ce4f8723 | iter1 | loo_rejected | 1.0 | 7 | 24 | 512* | 1 | undet. | — | b |
| caa06a1f | iter1 | shape_loo_rejected | 1.0 | 3 | 8 | 512 | 1 | **yes** | no | b |
| b2bc3ffd | iter1 | loo_rejected | 0.0 | 17 | 16 | 512* | 1 | undet. | — | b |
| 66e6c45b | iter1 | nondeterminate | 1.0 | 4 | 32 | 512* | 1 | undet. | — | — |
| 5a719d11 | iter1 | budget | 0.0 | 35 | 22 | 512* | 1 | undet. | — | — |
| ad38a9d0 | iter1 | accepted | 1.0 | 7 | 16 | 48 | 1 | **yes** | **yes** | — |
| 20818e16 | iter1 | shape_loo_rejected | 0.0 | 8 | 16 | 512* | 1 | undet. | — | b |
| 45737921 | iter2 | shape_loo_rejected | 0.0 | 8 | 2 | 512* | 1 | undet. | — | b |
| e4888269 | iter2 | loo_rejected | 1.0 | 9 | 24 | 384 | 2 | no | — | b† |
| e45ef808 | iter2 | nondeterminate | 0.0 | 5 | 13 | 2196‡ | 1 | **yes** | no | — |
| 320afe60 | iter2 | shape_loo_rejected | 0.0 | 14 | 8 | 512* | 1 | undet. | — | b |
| ac6f9922 | iter2 | loo_rejected | 0.0 | 10 | 40 | 512* | 1 | undet. | — | b |
| 8e301a54 | iter2 | loo_rejected | 0.0 | 15 | 16 | 512* | 1 | undet. | — | b |
| b0c4d837 | iter2 | loo_rejected | 0.333 | 14 | 8 | 512* | 1 | undet. | — | b |
| aabf363d | iter2 | nondeterminate | 0.0 | 0 | 1 | 16 | 1 | **yes** | no | — |
| 1fad071e | iter3 | loo_rejected | 0.667 | 4 | 16 | 512 | 2 | no | — | b |
| c6e1b8da | iter3 | budget | 0.0 | 17 | 36 | 512* | 1 | undet. | — | — |
| ecaa0ec1 | iter3 | shape_loo_rejected | 0.25 | 0 | 1 | 64 | 1 | **yes** | no | b |
| d9fac9be | iter3 | shape_loo_rejected | 1.0 | 0 | 0 | 1 | 1 | **yes** | no | b |
| c909285e | iter3 | shape_loo_rejected | 0.0 | 0 | 0 | 1 | 1 | **yes** | no | c |
| 67b4a34d | iter3 | loo_rejected | — (pool A) | 2 | 16 | 68 | 1 | **yes** | no | c |
| be03b35f | iter3 | loo_rejected | 0.0 | 4 | 8 | 112 | 1 | **yes** | no | b |
| 1d61978c | iter3 | canvas_ambiguous | 1.0 | 19 | 16 | 512 | 2 | no | — | — |
| bd283c4a | iter3 | nondeterminate | 0.0 | 13 | 20 | 256 | 2 | no | — | — |
| e21a174a | iter3 | loo_rejected | 0.0 | 25 | 12 | 512* | 1 | undet. | — | b |

\* enumeration capped (undetermined). ‡ raised-cap re-run, exhausted. † validation-run measurement; full-run re-judgment starved under contention (disclosed in §i).
