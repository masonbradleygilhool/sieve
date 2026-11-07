# SIEVE — Next Identification Derivation (2026-11-04)

**Commission:** paper only. No solver code, no probe. The derived-grammar
species was closed by its own pre-registered gates (iteration 2: KILL,
0/48). This document derives the next identification mechanism from the
complete measured record, and submits it to a cost-model gate before any
build is authorized. The grammar is frozen (census bound 98.2%, parameter
semantics derivation). Certification is frozen at iteration-1 strength
(LOO re-induction + shape-diverse hold-out + determinacy reporting). The
25 s/task budget is frozen.

**Verdict up front:** one mechanism is derived — **intersection-first
identification over cached signature tables** (§2). Its cost model (§4),
built from census data and the two probes' measured figures and charged
at the conservative factor α = 1 (no credit taken for the mechanism's own
structural savings), **clears the pre-registered falsifier on every
clause**: modeled median task 0.28 s (89× headroom under the 25 s
budget; the falsifier demands ≥10×), modeled p90 task 3.1 s, modeled
worst-sampled-task construction 20.8 s ≤ 25 s (the thin margin, stated
as such), modeled 48-task probe wall ≈ 67 s against the 1,200 s protocol
parameter. **A build is proposed**, under the probe protocol of §5 —
which includes a new economics falsifier (F6) that closes this mechanism
on measurement if its central claim fails there, exactly as iteration
2's record demands. Nothing in this document is a capability claim: the
modeled numbers are a cost argument about a procedure, and §7 states
what the mechanism does not fix.

---

## 1. What the two-probe record proves, read quantitatively

The commissioned facts, with the arithmetic that makes them binding:

**(a) The attempt sweep reaches a single-digit percentage of its own
space.** The frozen lane sweeps attempts = pre-transforms × accounts:
40 pre-transforms (8 dihedral × 5 scales {x1, x2, x3, d2, d3},
`ds_lane._build_pretransforms`) × searched accounts (32 raw
configurations — 2 segmentations × 4 input-bg generators × 4 output-bg
generators — deduplicated per task by background-value tuples). The
attempt space is therefore of order 10²–10³ per task. Iteration 1 ran
attempt slices of ≥3 s and ≤⅓ of the remaining budget; iteration 2,
¼ of remaining with a 2.5 s floor. Inside 25 s, at most ~5 (iter 1) to
~7 (iter 2) attempts can even *start*. A task whose schema lives at
attempt #8 or later in the fixed order is dead regardless of grammar,
budget discipline, or ordering priors — iteration 2 reordered by
census priors and the economics total did not move (28/48 → 28/48;
budget 20→24, caps 7→4, fit-then-budget 1→0). **The binding quantity
is exactly what the commission states: space size × per-node cost
against 25 s.** Per-attempt cost is seconds, not milliseconds, because
every attempt re-derives the geometry it needs — candidate generation,
per-pair covers (ASSIGN_NODES cap 6,000), and cross-pair combination
(COMBINE_NODES cap 8,000) are re-run per attempt, in grid space, and
certification then re-runs the whole sweep per fold. An attempt that
burns a 3 s slice inside its capped nodes implies an effective
throughput of at most ~5·10³ node-steps/s (≥0.21 ms/step) — the
signature of heavy per-node grid work, repeated per attempt.

**(b) Intersection is applied last, where it is most expensive.** The
frozen pipeline's order is: generate candidates locally → enumerate
per-pair covers → enumerate schema combinations → intersect bindings
→ reconstruct → certify. Cross-pair intersection — the one operation
in the pipeline whose cost is *set arithmetic* (measured here at
0.60 µs for 29-element sets) — is used only as a filter over already-
enumerated combinations. The pipeline's cost is a **product**
(attempts × pairs × assignments × combinations) because it
enumerates in assignment space first. Intersection is associative
and commutative: applied first, it is not an approximation of the
same computation, it *is* the same computation in a cheaper order.
Any schema the frozen pipeline certifies has all of its bindings
re-measuring in every pair; therefore every one of its bindings
survives a per-key cross-pair intersection computed before any cover
exists. The surviving-schema set is invariant under the reordering.
This is the level at which the cost collapses: from product to sum.

**(c) Certification converts 1 of 18 full fits, and that is the
population talking, not a defect to engineer away.** Across the two
probes: 10 + 8 full fits, 1 certified; the rest died as LOO-rejected
(3+4), shape-LOO-rejected (3+2), nondeterminate test class (2+2), or
budget inside certification (1+0). The census substrates predict
this: LOO fully determinate tasks are 16.4% of pool B, the mean
per-held-pair determinate fraction is 0.273 — certification is
usually judging rules whose classes were never seen held-out. The
frozen certification is retained at full strength (§2, Stage C), and
this derivation claims nothing about improving conversion. What it
claims is narrower: in iteration 1, one full fit *died of budget
inside certification itself*, and every fold in both probes paid the
full sweep's cost again. Certification's *price* is an economics
problem; its *verdicts* are not.

**(d) The grammar's reach is not the open problem.** Census bound
98.2% (921/938; eval-120 99.2%), robust under every ablation computed
(≥91.7% with field+param+copy all removed). Both probes' full-fit
coverage (20.8%, 16.7%) sits far below the bound for the reasons
priced in §1(a) — the sweep starves — plus the lane's own fit-level
restrictions relative to the bound (recorded in `DESIGN_NOTE.md`:
field phase constant across pairs and equal input shapes required;
the bound's own field test requires jointness *per pair* only).
Consistency with the earlier corpses: v2's largest class (bg-map
non-function, 17/48) was the account problem, since absorbed into
the frozen grammar as searched accounts; v2's creation_unexplained
16/48 was missing kinds, since absorbed; the DSL lane died of
algebra enumeration with no intersection anywhere (the same disease
as §1(a), in a larger space); retrieval and the LLM lanes died with
no identification procedure at all. Nothing in the older record
contradicts the mechanism below; the two derived-grammar probes are
its binding constraint.

---

## 2. The mechanism: intersection-first identification over cached signature tables

One mechanism, five stages. The grammar, the candidate kinds, the
selection key (lexicographic minimum over (creations, deletions,
bindings)), and certification's criteria are the frozen ones. What
changes is the *order and factoring* of the identification
computation: **all per-pair geometric facts are computed once, in
signature space, into cached tables; all cross-pair intersections
are computed in binding space before any cover is enumerated; the
exact cover survives only as a residual propagation problem over
bindings that have already survived every pair; certification folds
recompute intersections from the same tables and never re-derive
geometry.**

**Stage T — tables (once per task, once per segmentation).** For
each train pair and each of the two segmentations (primary,
agnostic): segment input and output; compute every object's
dihedral-canonical signature (colored pattern up to the 8 dihedral
maps — the lanes' existing signature machinery); index objects by
signature; record per-object measured facts the grammar's kinds
need (containment relations, ring/hole/bbox relations, periodicity
vectors of the input field, scene parameters Π per the parameter
semantics). Because candidacy facts are stated on canonical
signatures, the dihedral factor of the pre-transform space (8 of
the 40) **ceases to be a sweep dimension**: whether output pattern
O is a dihedral image of input pattern I is a signature equality,
already in the table, for every dihedral map at once. The scale
factor (5 of the 40) is gated per pair by exact arithmetic —
block-unanimity for d2/d3 (the lanes' own `_scale_down_grid`
precondition), size relations for x2/x3 — and intersected across
pairs in Stage 0. Tables are the task's permanent artifact: the
main induction, every certification fold, and the diagnostic all
read them. Nothing downstream re-segments or re-signatures.

**Stage 0 — viability by intersection (accounts and transforms
decided before candidacy).** For each of the 32 accounts: the
background rule is a binding and is intersected across pairs
exactly as the parameter semantics prescribes (candidate rules =
{constant, the four generators applied to the input, functional
maps on the input background value}; a rule must reproduce every
pair's output background). An account whose background intersection
is empty dies here, in set arithmetic, before a single content
candidate is generated under it — all 32 accounts are decided up
front, not reached in sweep order. Transform viability is
intersected the same way (per-pair scale gates + shape-relation
arithmetic across pairs). Stage 0's output is the task's viable
(account × scale) frames — the census sizes the account side:
accounts passing the bound's (stronger) necessary conditions
number median 4, mean 5.28, p90 12, max 32 per task over pool B.

**Stage A — binding intersection before cover.** Inside one viable
frame, for each source class (key), compute the set of derivation
**values** consistent with *all* pairs simultaneously, by
intersecting the per-pair candidate values read off the Stage-T
tables. This is the architecture derivation's M5 intersection,
moved from after the cover to before it, and extended to every
binding type the frozen grammar carries: fate values, canvas
functions (shape-relation arithmetic across the task's distinct
input shapes), palette maps, parameter bindings β (name
intersection — `inconsistent_param` is decided here, in set
operations, not after a sweep), and field bindings: per pair, the
(variant, phase) is **read off positionally** — the leftover's
pattern at its output position under the input field's periodic
continuation determines the consistent phase set — and the pair's
field leftovers must share one (variant, phase) jointly, obtained
by intersecting their phase sets; the variant is then intersected
across pairs. This adopts the bound's own field discipline
(per-pair jointness; `census_param_bound.field_joint`) and drops
the lane's stricter fit-level restriction (phase constant across
pairs, equal input shapes) — a change to the identification
*procedure*, not the grammar: the grammar's field kind, as the
bound defines it, never required cross-pair phase constancy.
Measured size of what intersection collapses here: over pool B,
a field-credited leftover carries a mean of 28.9 consistent phases
per variant (p90 86, max 768; 46,593 nonempty (leftover, variant)
entries) — enumerated, that is a per-object multiplier on the
cover; intersected jointly per pair, it is a handful of
0.60 µs set operations. Stage A never kills a true schema (§1(b));
it computes an over-approximation of the viable binding space —
a binding can survive intersection yet join no exact cover of
some pair — and Stage B decides exactly that question.

**Stage B — residual cover as constraint propagation.** Per pair,
the exact cover is now solved over Stage-A survivors only. The
structural change: most classes have exactly one surviving value,
so the cover is a propagation problem (assign forced classes,
propagate consumption conflicts, branch only where a class's
surviving value-set is plural *and* its values diverge in
placement or binding effect). Role swaps between identical
classes carrying identical values are not branches — they are
the same schema. The branching substrate is census-measured:
duplicate input classes appear in 682/938 tasks (72.7%), with
dup-pair counts 0→256 tasks, 1→65, 2→185, 3→319, 4→86, 5→18,
6→5, 7→4. The frozen node caps are retained as a safety, and a
cap hit is charged `search_cap` exactly as before — the model
(§4) prices how often the pruned space can still reach them.
Reconstruction (the frozen global re-render check) is unchanged.

**Stage C — certification at frozen strength, from cached
tables.** LOO re-induction + shape-diverse hold-out + the k=2
determinacy gate + prediction unanimity + canvas-ambiguity
abstention, criterion for criterion the iteration-1 certification.
A fold is Stages A+B re-run on the fold's pair subset **from the
Stage-T tables**: removing a pair only widens binding sets, so a
fold costs intersections and a residual cover — no re-segmentation,
no re-candidacy, no sweep. The iteration-2 guard is inherited as
a standing rule of this design: nothing may enter a fold that
alters which schema the fold judges (the fold-seeding catch,
`DESIGN_NOTE2.md` item 5 — a change that reached into
certification's judgment was caught by the controls and removed;
here it is excluded by construction, since folds and the main
induction run the identical Stages A+B code path on different
pair subsets of the same tables). The fit-then-budget death —
a found fit dying because certification re-paid the sweep —
does not exist in this factoring.

**What is deliberately not in the mechanism.** No ordering priors
as a cost device (census priors may still order Stage B's branch
choices for determinism of *which* schema is found first among
equals — the selection key decides ties as frozen — but no claim
rests on order). No memoization as a cost device (Stage T is not
memoization of the sweep; it is the removal of the sweep). No
learned proposal anywhere in the identification path (§6 states
what Friday's measurement could and could not change about that).
No grammar change; no certification change; no budget change.

---

## 3. Class-by-class accountability — both probes' taxonomies charged to the mechanism

Charging rules: **killed-by-design** = the death's mechanism does not
exist under §2 (structural, not statistical). **Shrunk-with-numbers**
= the class survives only at a frequency the §4 cost model computes
from census quantities. **Still-open** = the mechanism does not claim
it; the death is identification truth, certification doing its frozen
job, or grammar residue the commission froze. Counts are A+B (n=48)
per probe; pool C charges follow the same classes and are noted once
at the end.

| Death class | Iter 1 | Iter 2 | Charge | Basis |
|---|---|---|---|---|
| budget (lane deadline in the attempt sweep) | 20 | 24 | **Shrunk-with-numbers** | The sweep does not exist (§2: no attempt order to starve — all accounts decided in Stage 0, all frames share Stage-T tables). Residual budget deaths are pure tail cost: §4 models 0/40 sampled tasks ≥25 s at α=1 (worst construction 20.8 s); registered allowance ≤2/48, policed by F6 (§5). |
| search_cap (enumeration caps) | 7 | 4 | **Shrunk-with-numbers** | Covers run over Stage-A survivors (§2 Stage B): modeled cover work is ~10² propagation steps at median inputs (§4). Caps can still bind where post-intersection branching is genuinely large; the census substrate for that is duplicate-class mass — dup ≥5 pairs in 27/938 tasks (2.9%) ⇒ modeled cap-risk ≈1.4/48, vs 11 cap deaths across the two probes. |
| fit-then-budget inside certification | 1 | 0 | **Killed-by-design** | Certification no longer re-pays an induction sweep; folds are re-intersections from cached tables (§2 Stage C). The death's mechanism — budget consumed by re-induction — is absent. |
| inconsistent_segmentation (canonical account: no consistent background rule) | 7 | 8 | **Killed-by-design as charged; residual re-homed with numbers** | The charge was levied at the *canonical* account while later accounts went unreached behind the sweep — a masking artifact. Stage 0 intersects the background rule for **all 32 accounts up front**; the charge survives only where every account's intersection is empty. That true event is sized by the bound: 17/938 tasks (1.8%) fail every account ⇒ ≈0.9/48 expected, where it belongs — grammar residue, not economics. |
| loo_rejected | 3 | 4 | **Still-open, by design** | Certification is frozen; these are its correct verdicts on the population's ambiguity substrate (LOO fully determinate: 16.4% of pool B). The mechanism's only obligation — that fits stop being starved before they can be judged — is discharged by Stages T–B. Counts may *rise* as fit supply rises; F5 prices that. |
| shape_loo_rejected | 3 | 2 | **Still-open, by design** | Same as above; the shape-diverse hold-out is the census-forced strengthening against single-shape canvas ambiguity (42.5% of pool-B tasks have one train input shape). Not negotiable, not claimed. |
| nondeterminate_test_class | 2 | 2 | **Still-open** | Information-theoretic at k=2 (architecture derivation F1): two pairs do not discriminate the rule, and no procedure identifies what the pairs do not contain. Both draws carried the substrate (5 and 9 two-pair tasks on A+B). |
| inconsistent_param | 0 | 2 | **Still-open as outcome; killed-by-design as cost** | An empty β name-intersection is an identification fact about the task — the death stands wherever it is true. What dies is its *price*: Stage A decides it in set operations (~ms) before any cover, instead of after a sweep, and it can no longer hide inside the budget class. |
| creation_unexplained | 3 | 2 | **Split: field-candidacy component shrunk-with-numbers; remainder still-open** | The lane's field candidacy produced ~0 first-match field credits on both draws (iter 1 tabulation: field 1 instance; iter 2: none listed) against the census's 914 field-patch instances (48.5% of the novel mass) — `DESIGN_NOTE2.md` itself records this as a candidacy/reach gap. Stage A adopts the bound's own field discipline (positional read-off + per-pair joint intersection), removing the lane's stricter constant-phase/equal-shapes restriction: the field-attributable share of this class shrinks to the bound's discipline, sized by the 914-instance census mass. The remainder — leftovers with no derivation kind at fit level (arbitrary rearrangement, census S4, has no kind; kind-less free-form content) — is grammar residue, frozen by the commission: still-open. |
| inconsistent_delta | 1 | 0 | **Killed-by-design as charged** | Canvas functions are Stage-A intersections over the task's shape relations — arithmetic decided before any cover, not a verdict reached (or starved) inside a sweep. The true residual (no named canvas function fits all pairs) is grammar-level and belongs to the bound's residue, not to this class. |
| cover_failed | 1 | 0 | **Shrunk-with-numbers** | Stage B decides cover existence over the pruned space at modeled ~ms cost (§4): a genuine no-cover becomes a fast, correctly charged structural verdict instead of an artifact entangled with caps and slices. As a *death* it persists exactly where the frozen grammar truly has no cover — fit-reach truth, counted in coverage, no longer in economics. |

**Joint economics total:** iteration 1 charged 20+7+1 = 28/48 and
iteration 2 charged 24+4+0 = 28/48 to search economics under
identical charging. Under §2 + §4, the same three classes model to
≤2/48 (budget tail allowance) + ≈1.4/48 (cap-risk) + 0 (fit-then-
budget, killed) — i.e. the class that closed the species is
modeled at roughly a tenth of its measured size, with F6 (§5)
registered to close *this* mechanism if the measurement disagrees.

**Pool C (control pool, both probes):** budget 8+7 and search_cap
2+2 across the two C draws charge exactly as their A+B rows;
inconsistent_segmentation 0+1 likewise; creation_unexplained 0+1
takes the split charge; the 2+1 C full fits that died at
certification (shape-LOO in iter 1, LOO in iter 2) are still-open
by design; iter 2's C `creation_novel` (1) is not a death — it is
the abstention control behaving on the control pool.

**The one certified solve** (ad38a9d0, iter 1; reproduced under
ds_lane2 in iter 2): primary/modal/modal account, id|x1 frame —
Stage 0's first frame and Stage A's home ground. The mechanism
keeps it by construction (its bindings survive every intersection
it passed before); §5 registers it as an engineering pre-check on
spent tasks, not as evidence.

---

## 4. Cost model — computed from census data and the two probes' measured figures

### 4.1 Measured constants (provenance in Appendix A)

*Primitive costs, this machine, CPython (the lanes' own runtime):*
canonical dihedral signature of an 8-cell object: **35.6 µs**;
set intersection at field-phase scale (|A|=|B|=29): **0.60 µs**;
dict lookup: **0.155 µs**. Leftover cell counts (pool B, modal
account): median 1, mean 3.6, p90 8 — most objects are cheaper
than the 8-cell signature figure, which is used throughout as
the per-object cost (conservative direction).

*Candidacy envelope:* the bound tool's `analyze()` — full
candidacy at bound strength over **all** distinct account
configurations of a task (the computation whose per-pair records
feed Stages 0/A) — timed by the desk on a 40-task random sample
of pool B (seed 7): **median 0.219 s, mean 1.337 s, p90 2.71 s,
max 20.24 s** per task. Tail anatomy: the slowest task (42f83767,
k=3) spread its 20.14 s over **16 distinct configurations**; the
second slowest (9caba7c3) over 24; per-configuration-unit time
median 0.027 s, p90 0.342 s. `analyze()` re-segments and re-stages
**per configuration**; §2 pays segmentation twice per pair
(Stage T) and per-account kind tests thereafter. The model
therefore uses the envelope at **α = 1 — no structural credit** —
and records the per-configuration factor (up to 16× on the worst
sampled task) as margin argued but not taken.

*Census quantities:* pairs/task k: 2→146, 3→542, 4→173, 5→48,
6→18, 7→8, 8→2, 10→1 (mean 3.24). Objects/pair: primary 14.5 in /
12.7 out; agnostic 4.6 / 3.3 (architecture derivation §0.3).
Leftovers/task (modal account): median 2, mean 11.09, p90 32,
max 202. Candidate kinds per leftover: mean 2.8. Field phase
lists: mean 28.9 phases per nonempty (leftover, variant).
Passing accounts/task: median 4, mean 5.28, p90 12, max 32;
17 tasks pass none. Duplicate-class pairs/task: 0→256, 1→65,
2→185, 3→319, 4→86, 5→18, 6→5, 7→4 (≥5: 27 tasks, 2.9%).

*Old-lane figures (the contrast):* iteration 2 per-task wall
A+B: mean 14.29 s, median 19.86 s, 23/48 at the 25 s cap; total
walls 972.1 s (iter 1) and 952.6 s (iter 2) per 60-task run.

### 4.2 The model

Per task: **T = T_tables + T_cand + T_A + T_B + T_C**, where

- **T_tables** (Stage T): k × (27.2 + 7.9) objects ≈ 114
  signatures at the median k ⇒ 114 × 36 µs ≈ 4 ms, plus
  segmentation cell passes ≈ 1 ms. **≈ 5 ms** (k=10 tail: ~13 ms).
- **T_cand** (candidacy feeding Stages 0/A): bounded by the
  envelope at α=1: **median 0.219 s, mean 1.337 s, p90 2.71 s,
  max 20.24 s**.
- **T_A** (all intersections, all surviving frames): per frame,
  per class, per pair, value-set operations at 0.60 µs; at the
  p90 account count (12) and ~20 classes/pair this is
  ≲ 12 × 3.24 × 20 × ~3 ops × 0.60 µs, plus field joint-phase
  intersections (8 variants × ≤29-entry lists per leftover pair)
  ⇒ **≤ 15 ms** even at tail inputs.
- **T_B** (residual cover): ~ (objects × surviving values)
  propagation steps — ≈120 steps at median inputs (88 objects,
  ~1.3 post-intersection values per class), each a hash/set
  consistency step charged at a conservative 5 µs ⇒ **≈ 1 ms**
  median; tail (max object mass, dup=7 interacting duplicates)
  **≤ 50 ms**, with the frozen node caps as the registered
  safety whose binding frequency is modeled in §3 (≈1.4/48).
- **T_C** (certification): ≤ k+2 folds (median 5.24), each a
  Stage A+B re-run on k−1 pairs from cached tables ⇒
  (T_A + T_B) × folds ≈ **≤ 0.1 s** median, ≤ 0.5 s tail.

**Modeled totals (α=1):**

| Quantity | Modeled | Budget parameter | Headroom |
|---|---|---|---|
| Median task | **0.28 s** | 25 s | **89×** |
| Mean task | **1.40 s** | 25 s | 18× |
| p90 task | **3.1 s** | 25 s | 8× |
| Worst sampled task (construction: envelope max + tail T_A/T_B/T_C) | **20.8 s** | 25 s | 1.2× |
| 48-task probe wall | **≈ 67 s** | 1,200 s (48 × 25 s) | 18× |
| 240-task exam wall (at modeled mean) | **≈ 337 s** | 6,000 s | 18× |

### 4.3 Pre-registered falsifier — stated before any build

This design **dies on paper, and no build is proposed**, if the
model of §4.2, computed as above at α=1, shows any of:

- **(F-a)** modeled median task time > 2.5 s (less than 10×
  headroom under the 25 s budget);
- **(F-b)** modeled p90 task time > 25 s, or the worst-sampled-
  task construction > 25 s;
- **(F-c)** modeled 48-task probe wall > 600 s (half the protocol
  parameter), or modeled 240-task wall > 6,000 s.

**Computed outcome: (F-a) 0.28 s ✓; (F-b) p90 3.1 s ✓, worst
construction 20.8 s ✓; (F-c) 67 s ✓, 337 s ✓. The falsifier does
not fire. A build is proposed (§5).** The thin point is named,
not hidden: clause (F-b)'s worst-task margin is 1.2× at α=1. It
widens by the per-configuration factor the model declined to
take (the worst sampled task's candidacy is spread over 16
configurations; §2 pays its segmentation factor twice), and the
probe protocol (§5) retains iteration 2's hard deadline
discipline (SIGALRM at the task budget on every path), so a tail
breach degrades to a charged budget death policed by F6 — never
to a protocol violation. If the eventual build's measured spent-
draw timings contradict the envelope (i.e. the new candidacy
path is *slower* than the bound tool's), that is a build defect
to be caught by §5's engineering pre-checks, not a license to
amend this model after the fact.

---

## 5. Pre-registered probe protocol for the eventual build

Registered now; not amendable after the build's first run.
Instrument: `gauntlet.py`, **unmodified**. Budget 25 s/task.
Draw A:12, B:36, C:12, single draw.

**Seed rule.** The smallest seed ≥ 20271133 whose B-draw and
C-draw are disjoint from the draws of seeds 20261103, 20261104,
20261109, 20261164, 20271132 and smoke 999 — verified by
replicating the gauntlet's sampling offline and reproducing all
six prior run records' drawn id sets exactly, before the lane
runs. Pool A has 18 tasks; A-overlap with prior draws is
unavoidable and is reported with the drawn ids (B/C disjointness
is the enforceable part, per iterations 1–2 precedent).

**Controls (all five must pass before the run counts)** — the
architecture derivation's §6.3 set, unchanged: (1) positive,
object layer: synthetic split-by-color + grow task solved and
certified; (2) positive, field layer: synthetic periodic-
extension task solved and certified through the field binding
itself; (3) positive, cross-pair copy: synthetic task whose
created object exists only in another pair's input, solved and
certified with the certified schema family exactly the copy
schema; (4) abstention: synthetic novel-creation task produces
**no** certified schema; (5) negative: control 1's inputs with
train outputs shuffled across pairs → no certified schema.

**Engineering pre-checks (spent tasks only; not controls, not
measurement):** (i) deadline discipline on iteration 1's overrun
tasks — ac0c5833 (43.7 s under ds_lane) and 2c0b0aff (28.0 s)
must return ≤ 25.5 s; (ii) iteration 1's solve ad38a9d0 must
still solve and certify; (iii) candidate-completeness spot-check:
on sampled spent tasks, the Stage-T tables must not lose any
candidate the frozen lanes generated (completeness relative to
the frozen grammar is verified at build time, per §1(b)'s
invariance argument, not assumed); (iv) fold-integrity: for a
sampled control, each LOO fold's Stages A+B must be the
identical code path as the main induction on the fold's pair
subset (the iteration-2 seeding guard, restated as a check).

**Gates on A+B (n=48)** — at least as strict as the last, per
the commission:

- **KILL:** 0 certified solves.
- **WEAK:** 1–3 certified solves.
- **ALIVE:** ≥4 certified solves **AND** full-fit coverage
  ≥30% **AND** no override below.
- **F1 (reach):** coverage <15% caps the verdict at WEAK.
- **F5 (over-generation):** ≥half of full fits LOO-rejected
  caps the verdict at WEAK; shape-diverse rejections reported
  separately, with both the strict and inclusive readings
  recorded (iteration-1 precedent).
- **F4 (algebra shadow):** solves on pool C with zero A+B
  solves = KILL.
- **F3 (degeneracy):** ≥half of solves from a single lookup
  kind caps the verdict at WEAK.
- **F6 (economics — new, this design's own falsifier):**
  search-economics deaths (budget + search_cap, charged
  exactly as iterations 1–2 charged them) **> 6/48 (12.5%)**,
  **OR** median A+B per-task wall **> 2.5 s** ⇒ this
  mechanism's central claim is falsified on measurement:
  the verdict is capped at WEAK regardless of solves, the
  mechanism is closed as designed, and **no economics
  iteration is permitted on it** (iteration 2 is the standing
  proof that reordering a falsified economics claim buys
  nothing). If F6 fires with ≥4 solves, the solves are
  credited to the frozen grammar, not to this mechanism,
  and the desk redraws.

**Taxonomy.** Every non-solved A+B task gets exactly one
sub-reason, charged exactly as iterations 1–2 charged them,
plus the census-class tabulation of the draw (size class;
fates present; creation split by source; determinacy profile
of solves vs non-solves), so all three probes of the derived
grammar are directly comparable class by class.

**Consequence statement (registered, mirroring iteration 2's):**
ALIVE → the confirmation draw (B:96, next seed under the same
disjointness rule) runs before any scale claim, and the
freeze-and-exam sequence proceeds by separate order. WEAK
with F6 intact → exactly one iteration, aimed at the
taxonomy's largest class. KILL, F6 falsification, or a second
WEAK → this species closes and the desk redraws from the
three-probe record. The sealed approval exam is not read,
run, or touched under any verdict of this probe.

---

## 6. The pending Friday measurement — what it can and cannot change

**What it is.** A staged local measurement (friday_bigmodel_kit):
an open-weight 120B model (primary gpt-oss-120b; fallback
Qwen3-Coder-30B) served locally on Kaggle, proposing candidate
rules at k=128 on fresh tasks, with proposals verified exactly.
It is a species-level measurement of *learned proposal* as a
candidate source. Its species' prior record in this program:
P2 zero-shot 0/120 with 0 fits; P3 conditioned incomplete with
0 fits in its completed calls. The design of §2 neither needs
it nor assumes its outcome anywhere — every stage's inputs are
measured facts of the task itself.

**What it would have to show to change this design.** Exactly
one thing: that learned proposal is a *better candidate source
than analytic read-off* for the same downstream machinery.
Operationally, either (a) **certified solves at the ALIVE band
(≥4/48) on a fresh gauntlet draw** with proposals passed
through the frozen certification unchanged — solves, not
fits; or (b) a full-fit supply **≥ 2× the derived lane's
measured 20.8%** at certification conversion no worse than
the recorded 1/18. Either result would earn the proposer a
place as an *additional Stage-T candidate source*: its
proposals would enter the same tables, face the same Stage-A
intersections (a proposed binding that does not re-measure in
every pair dies in Stage A like any other), the same Stage-B
cover, and the same Stage-C certification. Nothing downstream
of the tables changes; the proposer's candidates enjoy no
privilege analytic candidates do not have. A strong *fit*
rate with the usual certification collapse changes nothing —
that is the 196/240-to-0/40 disease with a larger proposer,
and F5 exists to name it.

**What it cannot show.** It cannot relax certification (the
certification is the only barrier against the recorded
disease, and it is not this measurement's to amend). It
cannot speak to the information-theoretic classes
(nondeterminate at k=2; binding ties at 86.9% of witness
signatures — a proposer *guesses* among ties, which is
precisely what the determinacy discipline forbids a
certified schema to do silently). It cannot measure the
private eval, the exam, or anything beyond its fresh draw.
It cannot raise or lower the grammar's census bound. And a
null or weak Friday result cannot kill *this* design: §2's
candidate sources are analytic and self-contained, its cost
model never assumed a proposer, and its falsifiers (§4.3,
§5 F6) are stated entirely in its own terms. Friday is an
optional accelerator auditioning for one seat in Stage T —
nothing more, by construction.

---

## 7. What this derivation does not establish — honest limits

1. **Conversion is untouched, and it is the larger wall.**
   Certification converted 1 of 18 full fits across two
   probes, on a population whose LOO determinacy substrate
   (16.4% fully determinate; mean determinate fraction
   0.273) says most fits are judged on classes never seen
   held-out. This mechanism supplies fits cheaply; it does
   not make them truer. Even if §4's model holds exactly,
   the plausible outcome band is: economics deaths collapse,
   coverage rises toward what intersection-complete
   identification can reach, and certification converts at
   its measured character — which may still land below
   ALIVE. The distance from ALIVE (≥4/48) to the approval
   bar (216/240 on the sealed exam) remains the program's
   open distance; this document closes the *economics*
   term of it and no other.
2. **α = 1 is an envelope argument, not a measurement of
   new code.** The candidacy term is bounded by a fatter
   computation's timings (the bound tool's). The new path's
   true constant is unmeasured until the build; §5's
   pre-checks and F6 exist precisely because the model's
   authority ends where measurement begins.
3. **The worst-task margin is thin (1.2× at α=1).** The
   tail of this population (k up to 10, 202 modal
   leftovers, 32 passing accounts) contains tasks no
   40-task sample has seen. The model prices the sampled
   tail honestly and registers the deadline discipline +
   F6 as the containment for the unsampled part; it does
   not claim the tail is solved.
4. **Grammar residue stands where the derivations left
   it:** 17 pool-B tasks fail every account; 419
   unaddressed-color instances and 358 residual instances
   carry no identification-grade mechanism (parameter
   semantics §8); arbitrary rearrangement (S4) has no
   derivation kind. The commission froze the grammar, and
   this derivation obeys — those masses are named here so
   the probe's taxonomy can charge them where they belong
   instead of letting them dissolve into economics classes,
   which is how the v1 probe's taxonomy misfiled its
   background deaths.

---

## 8. Exceptionality — why this is not the field's standard move

The field's standard responses to "exact identification is
too slow" are three, and this program has measured all of
them: **search harder** (better orderings, priors, staged
budgets — iteration 2's commissioned test: 28/48 → 28/48,
the economics total invariant under reordering);
**search with more compute** (the budget is a protocol
parameter of the target evaluation, not a dial — and the
record shows the space growing faster than any plausible
budget: the derived grammar's attempt space is ~10²–10³
per task before covers); and **replace search with learned
proposal** (LLM lanes: 0 exact fits in every conditioning
tried here; gradient TTT in the wider record: 196 fits →
0 solves, the certification disease in its purest form).

This mechanism rejects the premise all three share — that
identification *is* a search over schemas, to be sped up,
scaled, or sampled. It treats identification as a
**constraint computation in binding space**: the version
space of schemas is maintained in factored form (one
candidate-value set per binding key), intersected across
pairs with set arithmetic, and *never materialized*; the
only enumeration that survives is a residual exact cover
over bindings the intersections have already collapsed,
plus a certification whose folds are re-intersections of
the same factored state rather than re-searches. In
concept-learning terms it is candidate elimination lifted
to a structured derivation grammar; in synthesis terms it
inverts the field's default pipeline (propose → enumerate
→ test) into **intersect → cover → certify**, with the
inversion *proved* costless in §1(b): the surviving-schema
set is identical, only the order of operations — and
therefore the complexity class of the bill — changes.

If it works, the contribution is threefold. **First**, a
demonstration, at population scale and under pre-registered
falsifiers, that ARC-AGI-2 identification over an
expressive grammar is intersection-tractable — that the
wall was the pipeline's algebra, not the problem's.
**Second**, machinery that outlives the verdict either
way: per-task candidate tables as a standing artifact any
future lane reads instead of re-deriving geometry; and a
pre-build cost model with a registered paper falsifier
(§4.3) — the same discipline the census bound brought to
grammar reach ("dead on paper before a probe is spent"),
extended to search economics, which is where this
program's last two probes actually died. **Third**, if it
fails — if F6 fires, or if economics collapses and
conversion still reads ~1/48 — the failure is *clean* in
a way the two-probe record could not be: fits supplied
cheaply and certification converting at its measured rate
would isolate conversion, not economics, as the binding
wall, and the next derivation would start from that
discrimination instead of from another entangled taxonomy.
A mechanism whose failure reprices the problem is a
contribution; a mechanism that can only succeed was never
derived, only hoped.

---

## Appendix A. Measurement provenance

Every number in §3–§4 traces to the record or to desk
measurements run for this derivation (2026-11-04, this
machine, CPython, $0):

- Probe figures, taxonomies, caps, slices, walls:
  `DERIVED_SOLVER_PROBE_RESULTS_2026-11-04.md`,
  `SIEVE_ITERATION2_PROBE_RESULTS_2026-11-04.md`,
  `derived_solver/DESIGN_NOTE.md`, `DESIGN_NOTE2.md`,
  `PROBE_LEDGER.jsonl` (tags `derived_solver_probe`,
  `sieve_iteration2_probe`, `nextgen_v1_probe`,
  `nextgen_v2_design_probe`), `gauntlet/REPORT.md`.
- Grammar, bound, identifiability limits:
  `APEX2_ARCHITECTURE_DERIVATION_2026-11-04.md` (§0 census,
  §1.2 limits), `PARAMETER_SEMANTICS_DERIVATION_2026-11-04.md`
  (§0/§6 bound 921/938, §3 limits L1–L5, §5 novel mass,
  §8 residue), `census/param_bound.json`.
- Desk-computed from `census/per_task.jsonl` and
  `census/param_per_task.jsonl` (938 tasks, full population,
  no sampling): passing-account distribution (median 4,
  mean 5.28, p90 12, max 32, zero 17); modal leftovers/task
  (median 2, mean 11.09, p90 32, max 202); candidate kinds
  per leftover (mean 2.8; 967/10,405 with none under the
  modal account); field phase-list sizes (mean 28.9,
  p90 86, max 768 over 46,593 nonempty entries);
  duplicate-class pair counts (0→256 … 7→4 tasks);
  leftover cell sizes (median 1, mean 3.6, p90 8).
- Desk-timed: `census_param_bound.analyze()` on a 40-task
  random sample of pool B (seed 7): median 0.219 s,
  mean 1.337 s, p90 2.71 s, max 20.24 s; slowest-task
  anatomy (42f83767: 20.14 s, 16 distinct configurations,
  12 passing accounts, 19 modal leftovers; 9caba7c3:
  12.52 s, 24 configurations); per-configuration-unit
  time median 0.027 s, p90 0.342 s.
- Desk-benchmarked primitives: canonical signature
  (8-cell object) 35.6 µs; set intersection (|A|=|B|=29)
  0.60 µs; dict lookup 0.155 µs.

*Files: this document. Foundation: the six record files
above; `census/` (census.py, census_param_bound.py,
per_task.jsonl, param_per_task.jsonl, param_bound.json);
`derived_solver/` (ds_lane.py, ds_lane2.py, DESIGN_NOTE.md,
DESIGN_NOTE2.md). The sealed approval exam was not read,
run, or touched.*
