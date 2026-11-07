# Fresh-Draw Conversion Probe — Preregistration (2026-11-07)

**Status: FILED BEFORE SAMPLING.** This document fixes the draw rule,
the seed rule, the definitions, and the verdict bands before the draw
exists. The execution addendum (§8) records the computed seed and the
48 task IDs after the seed rule fires and before the lane runs.

**Governing design:** `CREATION_MACHINERY_SPEC_2026-11-07.md` §3
(fresh-draw conversion probe). **Lane under test:**
`nextgen_probe/ng2_lane_creation.py` **as shipped by the creation
build, post-KC5 cuts** (M-G color-class gather and M-S symmetry
completion are OUT of the shipped lane; M-Q/M-U/M-L/M-R/M-F/M-C/M-T/
M-P and the §2.2 bg component are in; solver core byte-identical to
the bg lane). **Build record:** `CREATION_BUILD_RESULTS_2026-11-07.md`
(BUILD PASS; all five kill criteria adjudicated there). **Protocol
precedents:** `BG_GATE_RESULTS_2026-11-07.md` (the gauntlet protocol
as run), `gauntlet/GAUNTLET.md` (pool definitions and the repeat-draw
doctrine), `friday_bigmodel_kit/harness/find_friday_seed.py` (the
campaign's registered seed rule for repeat draws).

## 1. The registered bars — spec §3, quoted verbatim

From `CREATION_MACHINERY_SPEC_2026-11-07.md` §3:

> - fits and certified solves reported with denominators; conversion
>   read against the grammar's **1/28** (unanimous∧correct) and the
>   fit-supply reading **1/18**;
> - **sample-U with denominators**, measured on the *extended*
>   grammar (the old U = 0.321 does not apply — anatomy §4);
> - **unanimous∧correct with its Fisher p against the grammar's
>   1/9**, printed with the line;
> - the seat-standard bar mirrors the packet's: conversion ≥ 10 ×
>   1/28 guarded to ≥ 10 fits, **or** the unanimity clause (≥ 8
>   sample-unanimous judgeable tasks with ≥ 3/4 correct, Fisher p
>   printed);
> - secondary diagnostic (never the seat criterion):
>   `creation_unexplained` deaths on the fresh draw, against the
>   spent draw's 19/48 with denominators stated.
>
> A PASS on this probe is a component-to-lane verdict in the
> packet's sense. It approves no solver. The sealed in-house exam
> remains the only 216/240 instrument.

## 2. Pools — the census/bg definitions, exactly

Pools are `gauntlet/pools.json` as built by `gauntlet/build_pools.py`
(definitions in `gauntlet/GAUNTLET.md`):

- **Pool A** — `A_agi1_eval_fresh`: ARC-AGI-1 evaluation tasks that
  no APEX-2 record has ever touched, strictly (id absent from every
  harvested use-record AND test-input content hash absent from every
  used/mined AGI-2 task). **Size: 18.**
- **Pool B** — `B_agi2_train_fresh`: ARC-AGI-2 training tasks minus
  every task recorded as a library donor, compose-seed source,
  registry donor, or probe subject (62 excluded). **Size: 938.**
- Pool C is not drawn by this probe (spec §3 composition is A+B).

## 3. Disclosure: the spec's pool arithmetic, and the rule this probe follows instead

Spec §3 describes the draw source as "untouched tasks from the
938-task gauntlet pool, excluding the 48 spent A+B tasks (890
remain)". That arithmetic does not survive contact with
`pools.json`, and the discrepancy is registered here, before
sampling, not discovered after:

- 938 is pool B's size alone. Pools A and B are separate (18 + 938).
- There is no single "spent 48": the diag/bg/creation spent draw is
  the seed-20261109 gauntlet run's A12+B36, and the Friday pack's
  draw (seed 22979062) is a *different* A12+B36 whose B arm is
  disjoint from every earlier B draw by its own registered rule.
- Across all eight spent draws on disk (seven gauntlet run records,
  seeds 999 / 20261103 / 20261104 / 20261109 / 20261164 / 20271132 /
  20365108, plus the Friday draw, seed 22979062), the drawn B union
  is **252** distinct tasks (686 untouched), and the drawn A union
  is **all 18** pool-A tasks. **Zero untouched A tasks exist.** A
  12-A draw excluding every spent A task is impossible, and no
  sampling rule can make it possible.

The probe therefore follows the campaign's own registered
repeat-draw discipline — the one `GAUNTLET.md` states ("Pool A is
therefore precious — ration its draws (default draw uses 12 of 18;
**repeat draws will overlap on A by design** and the drawn ids are
recorded in every run record") and the Friday draw executed
(B/C-disjointness enforced by seed rule; A-overlap computed and
recorded per spent draw). What this preserves, unchanged: the
composition (12 A + 36 B), n = 48, every bar and denominator in §1,
the frozen protocol, and B-freshness — every B task in this draw is
a task no gauntlet lane has ever run. What it cannot preserve: A
novelty. The A arm's overlap with each spent draw is computed and
published in the execution addendum (§8), and per-pool results are
reported separately in the results document so the composition is
fully visible. This deviation is a property of the pool, not a
choice among draws: it is registered here so the results are read
against it.

## 4. The seed rule (fixed here, before sampling)

Sampling replicates `gauntlet.py` byte-for-byte, as
`find_friday_seed.py` verified for the Friday draw: one
`random.Random(seed)`; per-pool `rng.sample(entries, take)` in
draw-spec order over the `pools.json` entry lists; then
`rng.shuffle` of the drawn list. This probe's draw spec is
**A:12, B:36** (no C arm).

**Rule: the smallest seed > 22979062 (the last spent seed) whose
B-draw under this sampling is disjoint from the union of all spent
B draws** (the seven run records plus the Friday draw; 252 distinct
B ids). Before any seed is selected, the sampler must replicate all
eight spent draws exactly — id sets *and* order against the run
records and `friday_draw.json` — exactly the verification gate
`find_friday_seed.py` imposed; if replication fails, no seed is
picked and the probe does not run. The resulting seed and the 48
task IDs (in draw order) are recorded in §8 before the lane runs.
**No re-sampling for any reason:** a task that errors in the run is
reported as an error row, never replaced.

## 5. Protocol (frozen)

The shipped creation lane runs the gauntlet protocol unchanged, as
in `diag2_creation.py` / `diag2_bg.py`: `lane(task, 25.0)` per task,
frozen 25 s/task budget, LOO determinacy as the lane's certification
(unchanged `loo_check`), rows published in the diag format
(`nextgen_probe/diag_fresh_probe_rows.json`) carrying pool, class,
lane_reason, full_fit, accepted, test_ok (checked against the pool's
test outputs — the lane itself never sees them), mechanism, the bg
readouts, and wall time. Local CPU only.

## 6. Definitions (all denominators stated in the results)

- **Full fit:** the lane's `info["full_fit"]` — a complete schema
  fitting all train pairs. "Fits" below = full-fit count on the 48.
- **Certified solve:** `accepted` (the lane's frozen LOO
  certification accepts) **and** every test prediction equals the
  pool's test output.
- **Conversion:** certified solves ÷ full fits, read against the
  grammar's 1/28 and the fit-supply reading 1/18.
- **Sample-U (extended grammar):** the census protocol of
  `nextgen_probe/census_g0.py` as run at G0, applied to this draw's
  full fits: full version-space enumeration over the extended lane
  (all attempt families and background accounts; caps 512 schemas /
  20,000 combinations / 120 s per task; a cap hit marks the task
  **undetermined**, never absorbed). A task is **determined** iff
  enumeration completed; **sample-unanimous** iff determined and
  exactly one distinct rendered grid on the (first) test input;
  **unanimous∧correct** iff that render equals the test output.
  Reported with denominators in the census's three treatments:
  conservative (unanimous∧correct ÷ fits), determined-only
  (÷ determined), ceiling (unanimous∧correct + undetermined ÷ fits).
- **Unanimous∧correct line:** among sample-unanimous judgeable
  tasks (judgeable = the task record carries the test output — all
  48 do, by pool construction), the correct count and rate, with
  its Fisher p against the grammar's 1/9 printed with the line.
  The p is the one-sided Fisher exact test of
  `friday_bigmodel_kit/sample_version_space.py`'s
  `fisher_exact_greater(correct, wrong, 1, 8)` (table
  [[correct, wrong], [1, 8]], hypergeometric, exact integer
  arithmetic; plumbing check filed with FRIDAY_SAMPLE_STATS.md:
  6/8 vs 1/9 → p = 0.013369).
- **Death taxonomy:** the lane's reason strings over all 48 rows,
  identical taxonomy to the bg/creation runs.
  **`creation_unexplained` deaths** (secondary diagnostic, never the
  seat criterion): count on this draw, against the spent draw's
  19/48 (the post-build spent re-run's 8/48 is reported as context,
  not as the comparison).

## 7. Verdict bands (adjudicated exactly as registered here)

- **PASS** — either clause fires:
  - *conversion clause:* conversion ≥ 10 × (1/28) ≈ 0.3571,
    guarded to ≥ 10 fits; **or**
  - *unanimity clause:* ≥ 8 sample-unanimous judgeable tasks with
    ≥ 3/4 of them correct (Fisher p printed with the line).
  Per spec §3: a PASS is a component-to-lane verdict in the packet's
  sense. It approves no solver.
- **KILL** — 0 certified solves on the 48 (the packet's seat
  standard: "0 = KILL for the seat question"; the packet's
  flat-null line: "0 certified; no seat; neither evidence line").
- **MIDDLE — supply without conversion** — ≥ 1 certified solve but
  neither PASS clause fires: the packet's WEAK band (1–3 certified)
  and/or the mere-supply pattern (fit supply without
  truth-concentration) live here; the lane keeps diagnostic
  standing and holds **no seat**. The packet's seat lines —
  seat (a) ≥ 4/48 certified; seat (b) ≥ 20/48 full fits at
  conversion ≥ 1/18 — are printed in the results so the middle
  band's internal shape is visible in the packet's own terms.

**Context carried into the run (not the verdict):** at G0 the
extended grammar's spent-draw reading was point U = 0/11 under every
point treatment (conservative 0/11, determined-only 0/5), ceiling
product 0.982 × 6/11 = **0.535 < 0.90**, with two of five determinate
fits unanimous-and-**wrong** (3d6c6e23, 760b3cac). Nothing in this
probe's design projects any number to 240 tasks; the sealed
in-house exam remains the only 216/240 instrument.

## 8. Execution addendum (seed + draw, recorded before the run)

Executed 2026-11-07 by `nextgen_probe/find_fresh_probe_seed.py`,
**before the lane ran on any drawn task**.

- **Replication gate: PASSED.** All eight spent draws replicated
  exactly — id sets *and* order — against the seven gauntlet run
  records and `friday_draw.json`. Spent B union: **252** distinct
  ids (686 of 938 untouched), as registered in §3.
- **Selected seed: 22988303** — the smallest seed > 22979062 whose
  B-draw is disjoint from all 252 spent B ids. Draw file:
  `nextgen_probe/fresh_probe_draw.json`.
- **The 48 tasks, in draw order** (pool, tid):
  0 B 57edb29d · 1 B a78176bb · 2 A 47996f11 · 3 B 1caeab9d ·
  4 B 256b0a75 · 5 A 4aab4007 · 6 B e345f17b · 7 B cfb2ce5a ·
  8 A af22c60d · 9 B 22208ba4 · 10 B 6a1e5592 · 11 A e95e3d8e ·
  12 B e8593010 · 13 A 67b4a34d · 14 B 1478ab18 · 15 B 6a11f6da ·
  16 B e633a9e5 · 17 B 3b4c2228 · 18 A 1e97544e · 19 B 3bd67248 ·
  20 B 8f2ea7aa · 21 A 55783887 · 22 B fcc82909 · 23 A 477d2879 ·
  24 B 8e1813be · 25 A 929ab4e9 · 26 B 1f85a75f · 27 B 941d9a10 ·
  28 B fafffa47 · 29 B 3345333e · 30 B 9565186b · 31 B c1990cce ·
  32 A 3ed85e70 · 33 B 21f83797 · 34 B 0d87d2a6 · 35 B a834deea ·
  36 B e48d4e1a · 37 B 2072aba6 · 38 B ca8de6ea · 39 B abbfd121 ·
  40 B aab50785 · 41 B 4290ef0e · 42 B 42f14c03 · 43 B 6df30ad6 ·
  44 A 903d1b4a · 45 A e66aafb8 · 46 B 5783df64 · 47 B 81c0276b
- **B arm: 36/36 tasks never run by any gauntlet lane** (disjoint
  from all spent B draws by the seed rule).
- **A arm overlap** (of the 12 drawn A tasks, how many appeared in
  each spent draw — unavoidable, pool A = 18, registered in §3):
  seed 999: 1 · 20261103: 7 · 20261104: 8 · 20261109 (the diag
  spent draw): 8 · 20261164: 6 · 20271132: 7 · 20365108: 8 ·
  22979062 (Friday): 7. A ids drawn: 1e97544e, 3ed85e70, 477d2879,
  47996f11, 4aab4007, 55783887, 67b4a34d, 903d1b4a, 929ab4e9,
  af22c60d, e66aafb8, e95e3d8e.
