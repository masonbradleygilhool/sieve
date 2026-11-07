# Fresh-Draw Conversion Probe — Results (2026-11-07)

**VERDICT: KILL — certified solves 0/48, full fits 4/48,
sample-U 0/4 (conservative; determined-only undefined at 0
determined), unanimous∧correct 0/0 judgeable (Fisher p undefined —
no unanimous tasks).**

Preregistration: `FRESH_PROBE_PREREGISTRATION_2026-11-07.md`
(filed before sampling; §8 addendum records the seed and the draw
before the run). Design: `CREATION_MACHINERY_SPEC_2026-11-07.md`
§3. Lane: `nextgen_probe/ng2_lane_creation.py` as shipped by the
creation build, post-KC5 cuts (M-G/M-S out), frozen 25 s/task, LOO
certification unchanged. Draw: seed **22988303** (registered seed
rule; all eight spent draws replicated exactly before selection),
48 tasks (12 A + 36 B), run in draw order, total wall 540.0 s,
local CPU only. Rows: `nextgen_probe/diag_fresh_probe_rows.json`;
census rows: `nextgen_probe/census_fresh_rows.json`; analysis:
`nextgen_probe/fresh_probe_analysis.json`. No task errored; no
re-sampling occurred.

## The registered quantities, against the bars

| Quantity | Measured | Bar / reading |
|---|---|---|
| Certified solves | **0/48** | KILL line: 0 certified |
| Full fits | **4/48** (A 0/12, B 4/36) | conversion guard needs ≥ 10 |
| Conversion (certified ÷ fits) | **0/4 = 0.000** | PASS needs ≥ 10 × 1/28 ≈ 0.3571; read vs 1/28: 0.0×; vs 1/18: 0.0× |
| Sample-U (extended grammar) | conservative **0/4**; determined-only **undefined (0 determined)**; ceiling 4/4 (vacuous) | denominators stated; old U = 0.321 does not apply |
| Unanimous∧correct | **0/0 judgeable** — Fisher p **undefined** (no sample-unanimous tasks; reported as None with the empty denominator, per FRIDAY_SAMPLE_STATS' rule) | unanimity clause needs ≥ 8 unanimous judgeable with ≥ 3/4 correct |
| Seat (a) ≥ 4/48 certified | not met (0) | packet seat standard |
| Seat (b) ≥ 20/48 fits at conversion ≥ 1/18 | not met (4 fits, conversion 0) | packet seat standard |

## Verdict adjudication (bands as registered in the preregistration §7)

- **Conversion clause:** conversion 0.000 < 0.3571, and supply
  4 fits fails the ≥ 10-fit guard independently. **Does not fire.**
- **Unanimity clause:** 0 sample-unanimous judgeable tasks < 8.
  **Does not fire.**
- **KILL:** 0 certified solves on the 48 — the packet's seat
  standard ("0 = KILL for the seat question") and its flat-null
  line ("0 certified; no seat; neither evidence line").
  **The verdict is KILL.** It is not the middle band: the middle
  requires ≥ 1 certified solve, and there are none.

## What the run measured

**Fit supply fell back on fresh tasks.** The spent draw read 11/48
fit-bearing under this lane — a draw the creation mechanisms were
specified against. On untouched B tasks the same lane fits 4/36,
and on the A arm 0/12. The 4 fits: 1caeab9d (mechanism
`object_creation` — the one fit the creation machinery itself
produced), 6a1e5592 (`object_schema`), 9565186b (`object_schema`),
6df30ad6 (`object_transform`). **Certification rejects all four**
(3 loo_rejected, 1 nondeterminate_test_class) — the same
certification wall every fit on the spent draw hit, at fresh-draw
supply a third of the spent reading.

**Identification is unmeasurable at this supply, and what is
measurable is zero.** The census enumeration (G0 protocol, caps
512 schemas / 20,000 combos / 120 s) hit a cap on **all 4** fresh
fits (schema counts at cap: 512, 512, 576-with-cap, and one cap at
0 schemas): determined 0/4. Sample-U is therefore 0/4
conservative, undefined determined-only, and its 4/4 ceiling is
vacuous (it says only that nothing was determined). No fresh fit
is sample-unanimous, so the unanimous∧correct rate and its Fisher
p against the grammar's 1/9 are undefined — printed as such, not
as 0%.

**Death taxonomy (all 48, lane reasons; identical taxonomy to the
bg/creation runs):**

| reason | fresh draw | spent draw (post-build re-run) |
|---|---|---|
| creation_unexplained | **22** | 8 |
| budget | 10 | 13 |
| cover_failed | 4 | 4 |
| canvas | 4 | 1 |
| loo_rejected (fits) | 3 | 8 |
| nondeterminate_test_class (fits) | 1 | 3 |
| search_cap | 2 | 7 |
| inconsistent_phi | 2 | 3 |
| inconsistent_param | 0 | 1 |

**Secondary diagnostic (never the seat criterion):**
`creation_unexplained` deaths are **22/48** on the fresh draw,
against the registered comparison of **19/48** on the spent draw
(the post-build spent re-run's 8/48 is the same-draw reading after
the mechanisms were built against it — reported as context, not
as the comparison). On tasks the machinery was not built against,
the creation wall is at least as large as it was before the build;
the build's spent-draw migration (19 → 8) does not transfer to
fresh tasks at anything like its spent strength.

**Per-pool:** A arm 0 fits / 0 certified of 12; B arm 4 fits /
0 certified of 36. (A-arm overlap disclosure from the
preregistration stands: pool A has 18 tasks, all historically
drawn; 8 of this draw's 12 A tasks appeared in the diag spent
draw. The B arm — 36/36 never run by any gauntlet lane — is the
draw's uncontaminated mass, and it carries all 4 fits and the
same 0 certified.)

## Consequence — the packet's and the spec's own language

The packet's branch rule (§0) names this outcome: "BRANCH FAIL —
flat null (0 certified; no seat; neither evidence line)". Of a
FAIL branch the packet §3 says it produces "a measured 0 … on the
same fresh draw" and that such a verdict is countable "the way the
grammar lineage's closure is countable: as a killed path removed
from the search space on evidence, not as progress toward a
score"; and: "Not countable: tonight's null as anything but a
null. It relaxes no bar, spends no exam, and raises no axis."
The packet's axis rule stands over all of it: "The SIEVE axis
moves on measured conversion, on fresh draws, through the frozen
certification — on nothing else." This draw was that measurement
for the bg+creation successor lane, and it is null: **the lane
converts nothing on fresh tasks, holds no seat, and the SIEVE
axis does not move.** Per spec §3, nothing here was ever an exam
claim: "The sealed in-house exam remains the only 216/240
instrument," and it is unspent. No re-draw, re-run, or bar change
is authorized by this probe's documents; any successor work is a
new commission under the anatomy/spec discipline, not a
continuation of this probe.

## Context the verdict was read against (registered in advance)

G0's spent-draw reading for the extended grammar was point U = 0
(0/11 conservative, 0/5 determined-only) with a ceiling product
of 0.535 < 0.90 and two determinate fits unanimous-and-wrong. The
fresh draw is consistent with that warning at every point: supply
down (4/48 vs 11/48), identification undetermined-to-zero (0/4
determined), conversion zero. The build's PASS was a
spent-draw component verdict; this probe was the conversion
instrument, and it returns the conversion verdict: **none**.

Repository note: `~/workspace/arc_apex2` is not a git repository —
nothing was committed; all artifacts are on disk at the paths
above.
