# SIEVE — Conversion Derivation (2026-11-04)

**Commission:** paper only. No solver code, no probe. The exact-search
family over the derived grammar is closed (three probes: 1/48, 0/48,
0/48 certified solves; economics deaths 28/48, 28/48, 30/48 — invariant
under sweep, reordered sweep, and intersection-first organizations).
The prior derivation (`NEXT_IDENTIFICATION_DERIVATION_2026-11-04.md`)
attacked the economics term and stated, in its §7.1, what it did not
claim: **conversion is the larger wall, and that mechanism did not
claim it.** Across the three probes, frozen certification converted
**1 of 28 full fits**. This document answers the commissioned
question — why, charged stage by stage against the census ambiguity
structure — and derives the identification principle whose conversion
is not capped by the largest of those charges. Its §5 then says,
in its own voice, whether the resulting mechanism reaches a
trajectory toward the acceptance criterion (216/240 = 90% on the
sealed exam). It does not pre-empt Friday's proposer measurement,
and it proposes no silent change to certification: the one
certification change it derives is argued as a change, with its
false-solve exposure priced from the control record (§2.4).

**Verdict up front:** the 27 fit deaths decompose as **(a) intrinsic
ambiguity — firm 15/27 (56%), up to 21/27 (78%) with the unseparated
band; (b)+(c) certification-side losses — firm 4/27 (15%), up to
10/27 (37%), with the (b)/(c) split itself unmeasured and a priced
measurement specified to separate it (§1.4)**; economics inside
certification accounts for the remaining 2/27. The derived mechanism
— **version-space identification: carry the surviving hypothesis
set, in factored form, through a certification redefined as
per-fold forcing, and solve only on unanimity at the test input**
(§2) — removes charge (b) by construction, converts the (c1) part
of (c), and prices (a) exactly instead of dying of it. Its cost
model (§3) is priced from fresh measurements. Its honest ceiling
(§5) is the document's most important section: under every proxy
the record supports, the mechanism's fit-supply × conversion
product reaches **at most ~0.35 of tasks — roughly a third of the
0.90 the criterion demands** — because conversion at scale is
capped by a quantity no lane has ever measured directly, the
test-unanimity rate U of the grammar's version spaces, whose
measured proxies sit at 0.27–0.36. The derivation therefore
authorizes the mechanism first as the **instrument that measures
U exactly** (the §1.4 measurement, ≤ 1 CPU-day, $0, spent draws
only), with the build gated on that number. If U measures at
proxy levels, no identification principle over this grammar
reaches 216/240, and §5 names what would have to be true instead.

---

## 1. The conversion ledger — 28 fits, 27 deaths, charged exactly

### 1.1 The raw account (A+B, all three probes; pool C noted once)

Full fits A+B: iteration 1: 10 (1 certified); iteration 2: 8
(0 certified); iteration 3 (intersection-first): 10 (0 certified).
**Total 28 fits, 1 conversion (3.6%).** Every death below is the
probes' own charged sub-reason, from the three results files and
the per-task diagnostic rows (`derived_solver/diag_ds*_rows.json`),
joined task-by-task to the census substrate
(`census/per_task.jsonl`: per-task LOO witnessing fraction, defined
in §1.2). Pool C fits (4 across the probes: shape-LOO 3, LOO 1)
follow the same pattern and are excluded from the commissioned
A+B account, as in the prior derivations.

| Death stage | Iter 1 | Iter 2 | Iter 3 | Total |
|---|---|---|---|---|
| LOO-rejected | 3 | 4 | 4 | **11** |
| shape-LOO-rejected | 3 | 2 | 3 | **8** |
| nondeterminate test class | 2 | 2 | 1 | **5** |
| canvas-ambiguous | 0 | 0 | 1 | **1** |
| fit-then-budget (economics inside certification) | 1 | 0 | 1 | **2** |
| **certified** | **1** | **0** | **0** | **1** |

### 1.2 The census yardstick, with its definition kept visible

The census's LOO quantity is a **witnessing** measure, not a
schema-determinacy measure (`census/census.py`, LOO substrate):
a held pair counts as determinate iff every output object's
colorblind signature appears among the remaining pairs' input
objects. Fresh-computed over the full populations for this
derivation (Appendix A): pool B mean witnessing fraction
**0.273**, median **0.000**, fully witnessed **154/938 = 16.4%**,
fraction-zero **576/938 = 61.4%**; eval-120 mean **0.119**,
fully witnessed **5/120 = 4.2%**, fraction-zero **79.2%**.
Witnessing is *necessary* for a forced prediction and not
sufficient: a witnessed class can still carry a tied binding —
**1,909 of 2,196 witness binding signatures are tied (86.9%)**
(`census/param_bound.json`). Every use of this yardstick below
keeps the direction straight: witnessing absence proves
ambiguity; witnessing presence does *not* prove determinacy.

The 27 census-joinable fit tasks (one fit task, 67b4a34d, is
pool A and outside both census populations) skew witnessed
relative to the population — mean fraction **0.358** vs 0.273;
**7 of 27 fully witnessed (25.9%)** vs 16.4% — fits concentrate
where the substrate is richer, as expected. The single certified
solve (ad38a9d0) is fully witnessed, determinacy 1.0 — and its
own binding status records **tied_schemas = 8**: even the one
conversion carried a plural version space whose members agreed
where the certification looked. That datum is the mechanism of
§2 in miniature.

### 1.3 The decomposition

Charges: **(a)** intrinsic ambiguity — the train pairs do not
determine the prediction the certification demands, under
single-hypothesis identification; **(b)** certification
strictness beyond what the distribution forces; **(c)** fit
quality — the certified-correct rule was in the fit set's
neighbourhood but not in the returned fit. Fit-then-budget (2)
is charged to economics, not conversion: it is the death the
intersection factoring kills by construction (and iteration 3
still recorded one — the factoring reduced certification's
price, it did not zero it; recorded here because §3 inherits
that honesty).

**(a) — firm 15/27 (55.6%).**
- *Nondeterminate test class, 5/5.* All five are k=2 tasks
  (29c11459, 66e6c45b, e45ef808, aabf363d, bd283c4a). At k=2 a
  LOO fold trains on one pair; the architecture derivation's
  F1 limit is information-theoretic: two pairs do not
  discriminate the rule, and no procedure identifies what the
  pairs do not contain. One flag, kept visible: 66e6c45b is
  census-*fully-witnessed* (fraction 1.0) yet lane-nondeter-
  minate — the two determinacy notions genuinely differ
  (witnessing of output signatures vs the grammar's schema
  classes with their tied bindings, 86.9%), so there is no
  contradiction; the operative notion for certification is
  the grammar's, and under it the charge is (a).
- *Fold rejections on fraction-zero tasks, 9.* LOO: b2bc3ffd,
  ac6f9922, 8e301a54, be03b35f, e21a174a; shape-LOO: 20818e16,
  45737921, 320afe60, c909285e. On these tasks the census
  witnesses **no** held pair completely: whichever fold the
  certification held out, its output carried classes the
  remaining pairs never showed it. A re-induction (or a
  prediction) on that fold was guessing on unwitnessed
  classes; its rejection requires no further explanation.
- *Canvas-ambiguous, 1* (1d61978c, k=2, census-fully-witnessed):
  ≥2 canvas functions fit all pairs and diverge on some input
  shape. Charged (a), shape-conditionally: the ambiguity is
  real wherever the test input's shape is unwitnessed, and
  dissolves where it is witnessed — the one (a) sub-class
  whose payment depends on the test input, and therefore the
  one §2's solve-time unanimity prices exactly instead of
  charging in advance.

**(b)+(c) — firm 4/27 (14.8%), joint.** Fold rejections on
census-**fully-witnessed** tasks: ce4f8723 (LOO), e4888269
(LOO), caa06a1f (shape-LOO), d9fac9be (shape-LOO). Under census
accounting every held pair's classes were shown to the fold;
charge (a) cannot carry these. What remains is the pair
(b)/(c), and the record proves the (b) channel exists as a
mechanism, not a conjecture: iteration 2's fold-seeding
incident (`DESIGN_NOTE2.md` item 5, `SIEVE_ITERATION2` §5) —
seeding a fold with the parent induction's frame flipped a
passing control to a rejection, i.e. **a frozen certification
verdict is a function of re-induction dynamics, not only of
the candidate schema.** A fold that re-induces can reject a
correct parent schema by landing on a different schema that
mispredicts the held pair; a fold that re-induces can also
correctly expose a wrong parent. The records do not say which
happened on these four tasks — the parent schemas were not
retained — so (b) and (c) are charged jointly and the split
is priced in §1.4. The prior derivations' F5 readings are the
same signal at coarser grain: inclusive LOO rejections took
6/10, 6/8, 7/10 of fits in the three probes — certification,
not fitting, is where fits go to die, on tasks across the
whole witnessing range.

**Unseparated band — 6/27 (22.2%).** Fold rejections on
partially witnessed tasks (6430c8c4, fraction 0.75; 67636eac,
0.667; 1fad071e, 0.667; b0c4d837, 0.333; ecaa0ec1, 0.25) plus
the pool-A fit 67b4a34d (LOO-rejected; no census row exists).
The rejecting fold may be exactly the unwitnessed one (then
(a)) or a witnessed one (then (b)/(c)); the diagnostic rows
do not record which fold rejected. Charged as a band:
**(a) ∈ [15, 21]/27 = [56%, 78%]; (b)+(c) ∈ [4, 10]/27 =
[15%, 37%]; economics 2/27 = 7%.**

**Reconciliation against the population.** The ledger is what
the census predicts. A fit supply drawn from a population
whose per-pair witnessing mean is 0.273 (and whose exam-side
sibling reads 0.119) will produce mostly fits whose folds
contain unwitnessed classes; single-hypothesis certification
must then either guess (and be rejected when the guess is
exposed) or abstain (nondeterminate/canvas charges). The
measured 3.6% conversion is not an anomaly to be tuned away;
it is the determinacy structure of the distribution, read
through a certification that collapses each version space to
one schema and then discovers, fold by fold, that the collapse
was a guess. Note the direction of the fit-task skew (§1.2):
fits already concentrate on witnessed tasks (mean 0.358), and
conversion *still* reads 1/28 — because witnessing ≠ binding
determinacy (86.9% ties) and because the collapse itself
discards the information that the surviving rivals agreed.

### 1.4 The separating measurement — specified and priced

Two quantities the records cannot separate, one instrument
measures both, on spent draws only:

**Instrument: survivor-set census on the 28 spent fit tasks.**
Re-run the frozen induction on each fit task with the
survivor set retained (the intersection lane's Stage-A/B
factoring is the natural substrate; instrumentation is
analysis-only, no lane change), then record per task:
(i) **the parent schema's direct held-pair predictions** —
apply the returned fit to each held pair with no re-induction.
Where the parent predicts a held pair correctly that the fold
rejected, the death was **(b)** (re-induction variance); where
it mispredicts, **(c)** (the fit was wrong) — with the census
fraction attached so the (a) caveat rides along on
partially-witnessed tasks. This splits the firm-4 and informs
the band-6.
(ii) **the survivor set's width and its unanimity on the
task's actual test input** — the number of materially distinct
surviving schemas, and whether they render one output or
several on the test input the gauntlet scored. This is
**U, measured directly** on 28 fits (Wilson intervals at
n=28 are wide — ±~18 points at the mid-range — and the
document says so; a wide honest interval on the decisive
quantity beats a precise proxy). Spent draws only: these
tasks' test outputs enter no identification, no lane is
tuned on them, and the sealed exam is untouched.

**Price:** induction re-runs, 28 tasks at the recorded
per-task walls (≤ 25 s cap; measured means 13–14 s) ≈
≤ 12 CPU-minutes; survivor-set instrumentation on the
intersection lane's existing factoring ≈ a build-day of
analysis code; total **≤ 1 CPU-day, $0, no new draw, no
exam.** This measurement is this derivation's paper gate,
mirroring the prior derivation's §4.3 discipline: **no build
of §2 is authorized until (ii) returns.** If U on the 28
measures ≥ 0.85, §2's arithmetic (§5) re-opens; if it
measures at the proxy band (0.27–0.36), §5's ceiling is
confirmed by measurement and the desk acts on that.

---

## 2. The mechanism — version-space identification

### 2.1 The principle

Single-hypothesis identification commits two distinct errors
that the ledger separates: it **guesses where the pairs are
silent** (the (a) deaths are the guesses being caught), and it
**throws away agreement** (the (b) deaths and the tied-but-
correct fits: when eight schemas tie and agree, the collapse
keeps one and certification then judges the *collapse*, not
the agreement). The principle that converts at the rate the
pairs actually support is the dual: **never collapse.**
Identification returns the *surviving hypothesis set* — the
version space of the frozen grammar over the task's pairs, in
the factored form the intersection derivation already
established (one candidate-value set per binding key,
intersected across pairs, covers decided over survivors).
Certification stops asking "does a re-induction find the same
schema?" and asks the question determinacy actually poses:
**"does the survivor set, minus one pair, still force that
pair?"** Solving stops asking "is this schema certified?" and
asks **"does the full survivor set speak with one voice on
this test input?"** A task converts iff its pairs force its
test prediction — no more, and, for the first time in this
program, no less.

### 2.2 Stages (buildable precision)

**Stage V — version space (replaces argmin return).** The
identification pipeline is the frozen grammar's: accounts
intersected up front, bindings intersected per key across all
pairs, residual cover over survivors. What changes is the
return value and the tie discipline: instead of the selection
key's lexicographic argmin, Stage V returns the **factored
survivor set** Ŝ = (per-key value sets after intersection)
× (the cover-feasibility structure over them: which value
combinations survive the per-pair exact covers), together
with the set's **material width** — the number of distinct
*renderings* it can produce, counted on exercised keys only
(§2.3). Schemas that differ only on keys no pair exercises
are the same hypothesis for every purpose below. The frozen
node caps remain as safety; a cap hit is charged `search_cap`
exactly as before. One candidate-source seat is reserved in
Stage V's input, per §4.3: any external proposer's schemas
enter as additional candidate values in the same factored
sets and survive or die by the same intersections.

**Stage C′ — set certification (the argued change; §2.4).**
For each LOO fold j: compute the fold survivor set Ŝ₋ⱼ from
the cached tables by re-intersection on the k−1 remaining
pairs (the prior derivation's Stage-C factoring; removing a
pair only widens value sets — the operation is monotone and
contains no search and no argmin, so the iteration-2 seeding
failure mode is excluded by construction: there is no
per-fold schema choice for anything to steer). The fold
**passes** iff (i) Ŝ₋ⱼ is cover-feasible on every remaining
pair, and (ii) **every schema in Ŝ₋ⱼ renders the held pair's
recorded output on the held pair's input** — unanimity on
the held pair, evaluated on exercised keys (§2.3). The
shape-diverse hold-out is the same construction with folds
partitioned by input shape. The k=2 determinacy gate is
subsumed, not repealed: at k=2 each fold's survivor set is
wide, and condition (ii) is exactly the determinacy demand,
now evaluated on the grammar's own classes rather than
charged as a verdict after a failed re-induction — the five
nondeterminate deaths of §1 reappear here as fold failures
with the *reason* (which keys stayed plural, on which
classes) recorded, instead of as a label. A task is
**certified** iff every fold passes.

**Stage P — prediction under unanimity.** On the test input,
render Ŝ's prediction set: the distinct outputs its schemas
produce on exercised keys. **If the set is a single grid,
that grid is the solve. If it is plural, the lane abstains**
— returns no prediction, charged `abstain_nonunanimous`, a
new taxonomy class charged exactly where the old pipeline
charged its guesses. Abstention is not a euphemism for the
old rejections: the old pipeline *submitted* its collapsed
guess on uncertified fits nowhere (certification gated
submission) — the difference is at certification time, where
the old folds judged a re-induced stranger and the new folds
judge the set itself, and at fit time, where fits whose sets
are unanimous on the test input but whose folds the old
certification would have killed by variance now convert.

### 2.3 Exercised keys and material width

A binding key is **exercised** by an input if the derivation
of that input's output consumes the key (a fate value for a
class present in the input, a canvas function at the input's
shape, a field phase for a leftover the input generates).
Disagreement on unexercised keys cannot change any rendering
of that input and is not ambiguity *for that input* — this
is what makes solve-time unanimity strictly weaker than
full determinacy, and it is the only weakening anywhere in
the design. It is also measured, not assumed: the census
witnessing fraction is precisely an exercised-class measure
at signature granularity (a held pair is witnessed iff all
its exercised classes appear elsewhere), which is why §1's
proxy arithmetic (§5) uses it as U's upper-bound proxy —
and why ties (86.9% of witness signatures) cut below it:
a witnessed class with two surviving binding values that
render differently is exercised, witnessed, and still
non-unanimous.

### 2.4 The certification change, argued as a change

This derivation changes certification's **unit of judgment**:
from *one schema, re-induced per fold and compared* to *the
survivor set, re-intersected per fold and required to force*.
Nothing is relaxed: every task the old certification rejects
for a *substantive* reason — a fold whose information does
not determine the held pair — the new one also rejects
(condition (ii) fails: a survivor disagrees on the held
pair, or the fold's set is infeasible). What the new unit
removes is only the *procedural* rejection channel: folds
killing correct sets by re-induction variance, the channel
iteration 2 proved live when a steering change flipped a
control. The cost side, priced from the control record: the
new unit's false-solve exposure is the **unanimously-wrong
set** — all survivors sharing a wrong binding (a systematic
grammar-level bias on a class, e.g. every kind-variant of a
mis-segmented account agreeing on a wrong fate). That
exposure exists under the old unit too (a single schema can
be the same wrong binding, and folds catch it only when
re-induction happens to diverge), but it is not identical,
and this document does not pretend otherwise: the mitigation
is that the five standing controls — in particular control 4
(abstention: a novel-creation task must produce no solve)
and control 5 (shuffled outputs: no solve) — must pass under
the new unit before any probe counts, and §4 registers any
control-4/5 pass-through as an on-the-spot design death
(F-false-solve). No criterion of the old certification —
cover feasibility on all pairs, fold forcing, shape-diverse
fold forcing, canvas-ambiguity abstention (now a special
case of non-unanimity) — is dropped; the determinacy
*reporting* of the old unit becomes the new unit's verdict
*mechanism*, which is the honest description of the change:
**determinacy stops being a label attached to a schema and
becomes the thing certified.**

### 2.5 Abstention, priced against the threshold

The criterion tolerates **24 non-solves in 240 (10%)** —
total, across every cause: no-fit, non-unanimous abstention,
and error. Under this mechanism errors are ~0 by construction
(a submitted grid is forced by the pairs under the grammar;
its residual error channel is the unanimously-wrong set of
§2.4, controlled, not measured — stated as such). So the
budget is: 240·(1 − F) no-fits + 240·F·(1 − U) abstentions
≤ 24, where F is fit supply and U the unanimity rate among
fits. Equivalently **F·U ≥ 0.90**. Required U at given F:

| Fit supply F | Required U | Record's bearing |
|---|---|---|
| 0.208 (best measured) | 4.33 | impossible (U ≤ 1) |
| 0.30 (prior ALIVE coverage floor) | 3.00 | impossible |
| 0.50 | 1.80 | impossible |
| 0.70 | 1.29 | impossible |
| 0.90 | 1.00 | unanimity must be perfect |
| 0.982 (census bound) | 0.917 | the only arithmetically open row |

Read plainly: even if fit supply reached the grammar's
necessary-condition bound — which no lane has come within
4.7× of — the criterion still demands that **91.7% of fits
be unanimous on their test inputs.** §5 prices that demand
against everything measured about U. The abstention budget
also disciplines the mechanism's own tuning: there is no
setting of this design in which abstaining more helps beyond
the 24 — every abstention is a spent non-solve, and the
design spends them only where the pairs genuinely do not
force an answer.

---

## 3. Cost model — the marginal cost of carrying the set

### 3.1 What this model does and does not price

The conversion mechanism's new machinery is Stages V/C′/P.
Identification itself — the fit supply those stages consume —
is **not re-modeled here.** The prior derivation's identification
cost model was falsified on measurement (modeled median 0.28 s,
measured 12.25 s; its mechanism is closed under F6), and this
document inherits identification at its **measured** values, not
at any model's: per-task wall median **12.25 s**, mean **13.18 s**
(intersection lane, A+B); fit supply **20.8%**; economics deaths
**30/48** at the frozen 25 s/task. Any future economics fix is a
separate derivation's problem (F6's closure assigns it to a
redraw priced at the candidacy stage); the conversion claim
below is priced as a *marginal* cost over whatever identification
supplies the fits, and §4's gates keep the two claims separate.

### 3.2 Measured constants (fresh, this machine, today)

- **Set intersection**, |A|=|B|=29 (field-phase scale):
  **4.0 µs** (timeit, 20,000 reps). At |A|=|B|=1,000:
  **104.6 µs**. (The prior derivation measured 0.60 µs at the
  29-scale with a tighter loop; this model prices at today's
  4.0 µs — the conservative direction, and the discrepancy is
  recorded rather than smoothed.)
- **Object pattern extraction** on real grids (census
  machinery): ~1 µs per object (`pattern_of` over a real
  task's components). A full schema render is object-scale
  work plus grid assembly; this model charges a render at
  **1 ms** — roughly three orders above the measured
  per-object cost — as its conservative unit.
- **Candidacy envelope** (`census_param_bound.analyze()`,
  fresh sample, seed 11, n=12 pool-B tasks): median
  **0.211 s**, mean 3.60 s, max **28.08 s**. The median
  confirms the prior sample (seed 7, n=40: median 0.219 s);
  the tail is fatter than that sample showed (max 20.24 s
  there) — one of twelve sampled tasks spends more than the
  entire 25 s task budget inside candidacy alone. The tail
  warning of the prior derivation's §7.3 stands, strengthened.
- **Fold count** per certification: ≤ k+2 (k = train pairs;
  population mean k = 3.24, max 10) — median ≈ 5.
- **Divergent-combination substrate**: duplicate input classes
  in 682/938 tasks (72.7%); ≥5 duplicate pairs in 27/938
  (2.9%). The frozen candidate caps (64 surviving candidates
  per output in the lanes' precedent) bound the combinations
  a unanimity evaluation can be asked to render.

### 3.3 The marginal model

Per task that reaches a full fit (the only tasks Stages C′/P
touch):

- **Stage V (return the set):** the factored value sets are
  the identification pipeline's own intermediate state; the
  marginal cost is retaining them plus materializing the
  cover-feasibility structure Stage B already computes.
  Charged at ≤ 15 ms (the prior derivation's T_A bound,
  repriced at today's 4.0 µs set-op: p90 accounts 12 × ~20
  classes × ~3 ops ≈ 720 ops ≈ 3 ms; charged 5×).
- **Stage C′ per fold:** re-intersection on k−1 pairs
  (≤ Stage-V scale, ≈ 3–15 ms) + **unanimity evaluation** on
  the held pair: renders of divergent combinations over
  exercised keys, ≤ 64 combinations × 1 ms = **≤ 64 ms**,
  typical far below (most keys are singletons post-
  intersection; divergence concentrates in duplicate-class
  tasks). Per task: ≤ (k+2) folds × ~80 ms ≈ **≤ 0.4 s** at
  the median k; tail (k=10, duplicate-heavy): **≤ 1.0 s**.
- **Stage P:** one unanimity evaluation on the test input:
  **≤ 64 ms**.

**Modeled marginal totals:** median **≤ 0.1 s**, p90
**≤ 0.4 s**, worst construction **≤ 1.5 s** per fit task —
against recorded fit-finding times of 0.16–2.8 s inside
25 s task walls (intersection probe §5), i.e. the set
machinery consumes a small fraction of the headroom a fit
task has already demonstrated. At exam scale the marginal
total is ≤ 240 × 0.4 s ≈ **≤ 100 s**, immaterial beside the
inherited identification total (240 × 13.18 s ≈ 3,163 s of
the 6,000 s protocol parameter). The binding constraint is
never this machinery's price; it is the per-task 25 s cap's
effect on fit supply, inherited unchanged, and one named
residual risk: a fit found later than ~24 s into its budget
leaves less than the marginal tail — the fit-then-budget
class can recur at ≤ ~1/48 on this model, charged to
economics and policed by §4's F-economics clause.

### 3.4 Paper falsifier for this model

This cost model **dies on paper, and §2's build is not
proposed on it**, if any of: **(F-a)** modeled median
marginal cost > 2.5 s; **(F-b)** worst-construction marginal
> 5 s (a third of the headroom the fastest recorded fit
leaves); **(F-c)** the §1.4 instrument's measured Stage-C′
costs, when it runs, exceed the modeled p90 by > 5× (the
model's constants are then wrong in the direction that
matters and must be re-derived, not patched). **Computed
outcome: (F-a) ≤ 0.1 s ✓; (F-b) ≤ 1.5 s ✓; (F-c) armed,
decided by the §1.4 instrument.** The recurring fence, stated
once for the whole document: every figure in §3.3 is an
envelope over measured primitives, not a measurement of new
code; the instrument of §1.4 is where this model first meets
a measurement, and it is gated to run first for exactly that
reason.

---

## 4. Falsifiers and gate

### 4.1 Probe protocol (for the eventual build; gated on §1.4)

Instrument `gauntlet.py`, **unmodified**; budget 25 s/task;
draw A:12, B:36, C:12, single draw. **Seed rule:** the
smallest seed > 20365108 whose B-draw and C-draw are disjoint
from every spent draw at run time (20261103, 20261104,
20261109, 20261164, 20271132, 20365108, smoke 999, and the
Friday draw 22979062 once spent), verified by offline
replication of all prior run records first, per precedent.
**Controls:** the standing five, run under the §2 unit —
(1) object-layer positive, (2) field-layer positive through
the field binding itself, (3) cross-pair copy positive with
certified family exactly the copy schema, (4) abstention
(novel creation → no solve), (5) shuffled-output negative
(no solve). All five must pass before the run counts;
controls 4–5 are load-bearing for §2.4.

### 4.2 Bands — conversion judged jointly, as commissioned

- **KILL:** 0 certified solves, **or** F-unanimity fires.
- **WEAK:** 1–3 certified solves.
- **ALIVE:** ≥4 certified solves **AND** full-fit coverage
  ≥30% **AND** conversion (certified ÷ full fits) **≥ 25%**
  **AND** no override below. The conversion floor is new
  relative to the derived family's gates, by commission:
  this mechanism's claim *is* conversion (recorded family
  rate: 1/28 = 3.6%), and a gate that lets conversion ride
  would certify the claim without measuring it. 25% is ~7×
  the recorded rate and still far below §5's requirement —
  ALIVE certifies the mechanism, not the criterion.
- **F-unanimity (this mechanism's own falsifier):** U,
  measured on the probe's own fits as the share of full fits
  whose survivor set is unanimous on the scored test input,
  **< 0.50** ⇒ the ceiling claim is falsified at the level
  that matters — 0.982 (bound supply) × 0.50 = 0.49 < 0.90,
  so no fit supply this grammar can produce rescues the
  product — the mechanism is **closed as a path to the
  criterion** (its instrumentation value stands), and **no
  conversion iteration is permitted on it.**
- **F-economics (inherited, with its teeth placed
  honestly):** search-economics deaths (budget + search_cap
  + fit-then-budget, charged as the three probes charged
  them) **> 6/48**, **or** median A+B wall **> 2.5 s** ⇒ the
  lane is not a candidate for the freeze-and-exam sequence,
  whatever its conversion verdict. On the inherited
  substrate (median 12.25 s) this clause is *expected* to
  fire; it is registered anyway, because a conversion probe
  must not smuggle an economics resurrection in under a
  conversion headline — the economics redraw F6 assigned
  remains a separate, future derivation, priced at the
  candidacy stage where iteration 3 localized the cost.
- **F-false-solve:** any control-4 or control-5 pass-through
  ⇒ the design is dead on the spot and the probe is void.
  Any realized unanimously-wrong certified solve on the draw
  ⇒ §2.4's exposure is live: verdict capped at WEAK and the
  exposure re-priced before further work; false solves
  ≥ true solves ⇒ KILL.
- **F1/F3/F4** are inherited unchanged (coverage <15% caps
  at WEAK; ≥half of solves from one lookup kind caps at
  WEAK; pool-C solves with zero A+B solves = KILL).

**Consequence statement (registered):** ALIVE with
F-economics intact → the confirmation draw (B:96, next seed
under the same rule) precedes any scale claim, and
freeze-and-exam proceeds by separate order. ALIVE as a
conversion verdict with F-economics fired → the mechanism is
banked as the conversion unit and the desk commissions the
economics redraw before any exam sequence. WEAK → exactly
one iteration, aimed at the taxonomy's largest class.
KILL or F-unanimity → this mechanism closes and §5's
named alternatives are the program's remaining routes. The
sealed approval exam is not read, run, or touched under any
verdict.

### 4.3 What Friday's measurement changes here — and what it cannot

Friday (per the prior derivation's §6 and
`friday_bigmodel_kit/harness/HARNESS_READY.md`) measures a
local 120B proposer at k=128 on a fresh draw (seed 22979062)
through the frozen (old-unit) certification, against the
seat standard: **(a)** ≥4/48 certified solves, or **(b)**
coverage ≥41.6% (2× the derived lane's 20.8%) at conversion
≥ the recorded 1/18. Its bearing on this design is exactly:

- **A seat, if earned, is a Stage-V input seat.** Proposer
  schemas enter the factored survivor sets as additional
  candidate values and face the same intersections, the
  same fold-forcing, and the same solve-time unanimity as
  analytic candidates. A proposer schema that uniquely
  survives *narrows* Ŝ and can raise U on its tasks; one
  that survives alongside disagreeing rivals *lowers* U
  there. Friday's seat standard was registered against the
  old certification unit and does not certify the
  proposer's effect under this one — if the seat is earned,
  that effect is re-measured (the §1.4 instrument extended
  to proposer-seeded sets) before the proposer is admitted
  to any §2 build.
- **A Friday ALIVE changes F's prospects, not the ceiling's
  structure.** Seat (b) at face value doubles modeled fit
  supply (0.208 → ~0.42); §5's table shows the product still
  fails by ≥ 2× at every U the record supports. Friday is
  therefore neither this design's savior nor its rival: it
  auditions for a seat inside it, at a standard this
  document does not amend.
- **A Friday null changes nothing here.** §2's candidate
  source is analytic and self-contained; its falsifiers
  (§3.4, §4.2) are stated in its own terms. P3's completed
  record (conditioning moved the distribution minimally:
  1 near-miss, 0 fits, 0 certified) already prices the
  proposer species' prior at the low end; Friday is the
  remaining measurement, and this derivation neither
  discounts it in advance nor leans on it.
- **Friday cannot relax anything in §2.** Unanimity is not
  a dial a proposer result can turn down: a proposer that
  is *usually* right is, under this design, a candidate
  source whose schemas still must survive intersection and
  speak unanimously — because the recorded disease (196/240
  fitted → 0/40 in the 2026 campaign; 27/28 fit deaths
  here) is precisely confident single answers the pairs did
  not force.

---

## 5. The honest ceiling

The criterion is F·U ≥ 0.90 (§2.5). Everything the record
measures about the two factors:

| Scenario | F | U | F·U | Solves /240 |
|---|---|---|---|---|
| Measured substrate, proxy U (pool-B witnessing mean) | 0.208 | 0.273 | 0.057 | ~14 |
| Measured substrate, generous U (fit-task witnessing mean) | 0.208 | 0.358 | 0.074 | ~18 |
| Bound supply, proxy U | 0.982 | 0.273 | 0.268 | ~64 |
| Bound supply, generous U | 0.982 | 0.358 | 0.352 | ~84 |
| **Criterion** | — | — | **0.900** | **216** |

And the exam does not resemble the friendly column: the
exam-side population (eval-120) reads witnessing mean
**0.119**, fully witnessed **4.2%**, fraction-zero **79.2%** —
worse than pool B on every axis the census computes, as the
architecture census already established. At eval-side proxy
U (0.119) even bound supply yields 0.117 → ~28/240.

**So, in this document's own voice: the mechanism of §2 is
the correct conversion architecture for this grammar — it
converts everything the train pairs genuinely force, it
abstains on exactly the rest, and it removes the one
conversion loss (re-induction variance) that was never the
distribution's fault — and its modeled fit-supply ×
conversion does not reach a trajectory toward 216/240. It
falls short by a factor of ~2.6 under the most generous
proxy pairing the record supports, and by ~8 on the
exam-side population.** The shortfall is not in the
mechanism; it is in U itself — the rate at which this
grammar's version spaces, on this task distribution, speak
with one voice about unseen inputs. Two to four pairs of
examples, over classes with 86.9% tied bindings, usually do
not determine a rule. That is a property of the problem as
ARC-AGI-2 poses it, and three probes plus a census have now
measured it from four independent directions (fit deaths,
witnessing substrate, binding ties, proposer flatness).

**What would have to be true instead — named, in order of
decreasing testability:**

1. **U at schema level is radically higher than the
   witnessing proxy.** The proxy is class-level and
   colorblind; the grammar's actual survivor sets might be
   near-singletons on exercised keys whenever a fit exists.
   Two data point the other way — tied_schemas = 8 on the
   program's only certified solve, and the 86.9% tie rate —
   but neither is a measurement of U. This is the one
   possibility that is cheap to settle, and §1.4 settles
   it: **if U measures ≥ 0.917 at bound-level supply
   prospects — realistically, ≥ 0.85 on the instrument,
   reopening the arithmetic — the path exists and §2 is
   its architecture. If U measures in the proxy band, the
   conversion question over this grammar is answered,
   negatively, at measurement strength.**
2. **Test inputs exercise only witnessed, untied classes.**
   Contradicted on the record: eval-120's substrate is
   worse than pool B's on all eight census axes, and the
   private eval is drawn from the eval side.
3. **A candidate source that collapses version spaces to
   the truth** — a proposer that is right, not merely
   plausible, at near-singleton rates. Friday measures the
   first piece; its seat standard (conversion ≥ 1/18 at
   2× supply) sits two orders of magnitude below what this
   ceiling requires, so even a Friday ALIVE is
   necessary-not-sufficient evidence for this route.
4. **A different grammar** — one whose binding kinds are
   functionally determined by witnessed data, so that
   witnessing and determinacy coincide. Outside this
   derivation's frozen inputs; the census bound's residue
   sections (17 tasks failing every account; 419
   unaddressed-color and 358 residual instances) name
   where this grammar is silent, and a grammar derivation
   is a new commission, not an amendment to this one.

**Commissioned consequence, restated without decoration:**
run §1.4 first (≤ 1 CPU-day, $0, spent draws only). Its
number U is the quantity the whole program's fate turns
on, it is currently bounded only by proxies, and every
further build — this mechanism included — is a bet on its
value. The desk should buy the measurement before the bet.

---

## Appendix A. Measurement provenance

Every number above traces to the record or to computations
run for this derivation (2026-11-04, this machine, CPython,
$0):

- **Probe figures, taxonomies, walls:**
  `DERIVED_SOLVER_PROBE_RESULTS_2026-11-04.md`,
  `SIEVE_ITERATION2_PROBE_RESULTS_2026-11-04.md`,
  `SIEVE_INTERSECTION_PROBE_RESULTS_2026-11-04.md`;
  per-task fit/death joins from
  `derived_solver/diag_ds_rows.json`, `diag_ds2_rows.json`,
  `diag_ds3_rows.json` (28 A+B full fits; death stage =
  `lane_reason`; the certified solve's `binding_status`
  records tied_schemas = 8).
- **Census substrate:** `census/per_task.jsonl` (938 rows),
  `census/per_task_eval120.jsonl` (120), `census/summary.json`,
  `census/param_bound.json` (bound 921/938; witness binding
  signatures: tied 1,909 / 2,196 = 86.9%). LOO witnessing
  definition: `census/census.py` LOO substrate block.
  Fresh-computed for this derivation: population witnessing
  distributions (pool B mean 0.273 / median 0.000 / fully
  16.4% / zero 61.4%; eval-120 mean 0.119 / fully 4.2% /
  zero 79.2%; by-k breakdowns), and the fit-task join
  (27 census-joinable fits: mean 0.358, fully witnessed 7,
  fraction-zero 15; death-stage × witnessing-fraction cross-
  tabulation underlying §1.3's charges).
- **Prior derivations:** `NEXT_IDENTIFICATION_DERIVATION_
  2026-11-04.md` (§1 record, §2 factoring inherited by
  Stage V, §4 cost-model precedent, §6 Friday standard,
  §7.1 the conversion disclaimer this document answers),
  `APEX2_ARCHITECTURE_DERIVATION_2026-11-04.md`,
  `PARAMETER_SEMANTICS_DERIVATION_2026-11-04.md`.
- **Proposer record:** `P3_COMPLETION_2026-11-04.md`
  (conditioned: 0 exact fits, 1 near-miss, 0 certified;
  P2 zero-shot baseline: 0 fits, 0 near-misses, 62 parseable
  completions), `friday_bigmodel_kit/harness/HARNESS_READY.md`
  (Friday draw seed 22979062, seat standard, protocol).
- **Fresh timings for §3:** set intersection |A|=|B|=29:
  4.0 µs; |A|=|B|=1,000: 104.6 µs (timeit, this machine);
  census `pattern_of` ≈ 1 µs/object on real grids;
  `census_param_bound.analyze()` fresh sample (seed 11,
  n=12): median 0.211 s, mean 3.60 s, max 28.08 s —
  against the prior derivation's seed-7 sample (n=40:
  median 0.219 s, mean 1.337 s, max 20.24 s), both cited
  where used.

*Files: this document. Foundation: the three probe results,
the two prior derivations, the census tables, the P3
completion record, and the Friday harness record above. No
solver code was written; no probe was run; the sealed
approval exam was not read, run, or touched.*
