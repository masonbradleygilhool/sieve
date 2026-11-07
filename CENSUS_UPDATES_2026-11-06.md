# SIEVE census updates — background-identification component (2026-11-06)

Executes the five census computations of `NOVEMBER_CONVERSION_PACKET.md` §2.4 over
**pool B: the 938 ARC-AGI-2 training tasks** in `gauntlet/pools.json`
(`B_agi2_train_fresh`; 3,040 train pairs total; train pairs only). Local CPU,
single-threaded, checkpointed per task.

**Component under test** (packet §2.2): background is proposed per pair from the
generator set {modal, border-modal, corner-color, sea} and identified as a colour
binding by cross-pair intersection over 32 accounts (2 segmentations × 4 × 4
generator pairs). A generator pair is **consistent** for a task iff the generated
input-background → output-background values across the task's train pairs form a
*function* — the packet's survival rule for a background binding.

**Files.** Machine-readable results: `census/bg_census_2026-11.json` (copy in
`census_updates_2026-11-06/census_updates_summary.json`). Per-task checkpoints:
`census_updates_2026-11-06/generator_per_task.jsonl` (938 rows),
`accounts_per_task.jsonl` (938 rows), `creation_per_task.jsonl` (113 rows).
Runner: `census_updates_2026-11-06/run_census_updates.py` (resumable; re-running
reproduces the summary from the checkpoints).

**Reuse / labelling.** Generator values come from the existing census machinery
(`census/census_param_bound.py:bg_generators`); full-account viability is read
from the banked substrate `census/param_per_task.jsonl` and the modal/searched
passes are re-aggregated with `census_param_aggregate.task_pass`, so definitions
cannot diverge from the banked bound. Every number below was produced by this
run; where a figure coincides with the 2026-11-04 bank, that is a reproduction,
and it is marked as such.

---

## 1. Generator-pair census

Method: for each task, each of the 16 (input-generator × output-generator)
pairs is marked consistent iff its generated background values are functional
across all of the task's train pairs. Separately, the number of the 32 full
accounts under which the task remains viable is the count of passing account
realisations stored in `param_per_task.jsonl` (the evaluator deduplicates
accounts that induce identical background-value vectors, so this is a count of
distinct stored realisations, ≤ 32).

Consistent tasks per generator pair (denominator 938):

| input ↓ / output → | modal | border-modal | corner-color | sea |
|---|---|---|---|---|
| modal | 762 (81.24%) | 744 (79.32%) | 583 (62.15%) | 692 (73.77%) |
| border-modal | 745 (79.42%) | 773 (82.41%) | 597 (63.65%) | 694 (73.99%) |
| corner-color | 759 (80.92%) | 772 (82.30%) | 752 (80.17%) | 716 (76.33%) |
| sea | 749 (79.85%) | 743 (79.21%) | 586 (62.47%) | 723 (77.08%) |

Corner-colour as the *output* generator is the least often functional
(583–597 of 938); every other cell sits at 692–773.

Consistent pairs per task (denominator 938): mean 12.14, median 14, p90 16.
The distribution is bimodal: **466 tasks (49.68%) are consistent under all 16
pairs** (their generated input values never repeat, so no functional constraint
bites), and **69 tasks (7.36%) are consistent under no pair at all** — for those
69, no account in the 16-pair family can even state a functional background
binding, whatever the content machinery does. 869/938 (92.64%) admit at least
one consistent pair; only 6 tasks admit exactly one (see §4).

Viable full accounts per task (denominator 938): **median 4, mean 5.28, p90 12,
max 32; 17 tasks pass under none.** This reproduces the banked M1 statistics of
`PARAMETER_SEMANTICS_DERIVATION_2026-11-04.md` exactly.

## 2. Modal-sufficiency rate

Method: the (modal, modal) cell of the same functional test — modal-in →
modal-out is a function across the task's pairs.

**762/938 = 81.24%** of the pool is modal-functional; 176/938 (18.76%) is not.
Of the 762, **582 tasks (62.05% of the pool) have a constant modal pair** — the
only case the v2 lane's identification accepts — and **180 tasks are
modal-functional but not constant-pair**: a functional-map identification
(packet §2.2) widens the modal account's binding-level reach from 582 to 762
tasks before any generator search is switched on.

Bound-level context (this run's accounts stage reproduces the banked
`census/param_bound.json` figures exactly): the modal *account* passes the full
grammar's necessary conditions on **808/938 (86.14%)**; searching all accounts
raises this to **921/938 (98.19%)**. The gap between 762 (binding functional)
and 808 (account bound-pass) is expected: the bound's evaluator does not require
the background map to be functional, so the account can pass on tasks where the
§2.2 binding rule would reject it. The component's own rule is the stricter one.

## 3. Background-subtype census

Method: the three failure patterns of packet §2.1 / `NEXTGEN_V2_PROBE_RESULTS`
§4.1, read off each pool task's (modal input, modal output) pair sequence.
Categories are mutually exclusive and, with the constant-pair baseline, sum to
the pool. A *single-pair flip* is the source's pattern (9110e3c5, 5d2a5c43):
one pair differs from an otherwise constant pair in the **input** coordinate
only; a lone output-side deviation under a constant input counts as
context-dependent, not as a flip. The input-modal category is the operational
form of "input modal is not the background" (output modal constant, input
modals vary, no single flip); the semantic reading is the source's, the count
is the pattern's. Spot check: the source's three examples classify into their
named categories (3194b014 → context-dependent; 27f8ce4f → input-modal pattern;
9110e3c5 → single-pair flip).

| pattern | tasks | % of pool | % of nonconstant |
|---|---|---|---|
| constant pair (baseline, not a failure) | 582 | 62.05% | — |
| context-dependent output background | 143 | 15.25% | 40.17% |
| input modal not the background (pattern) | 19 | 2.03% | 5.34% |
| single-pair flip | 22 | 2.35% | 6.18% |
| other nonconstant pattern | 172 | 18.34% | 48.31% |
| **nonconstant total** | **356** | **37.95%** | 100% |

The three named subtypes cover 184/938 tasks (19.62% of the pool; 51.69% of the
nonconstant mass). The largest single bucket is the residual one: **172 tasks
(18.34%) vary in both coordinates with no (k−1)-majority pair** — no named
subtype describes them, and a component built only against the three named
patterns has no subtype-specific story for nearly half the mass the modal
identification mishandles. (Nonconstant modal pair is the *lane's* death
condition, not the searched component's: a non-modal account may still bind
these tasks — §1 counts 869/938 with at least one consistent pair.)

## 4. Background-binding LOO determinacy

Method: for each task and each train pair held out in turn (3,040 folds), the
consistent generator-pair set is recomputed on the remaining k−1 pairs.
*Strict determinacy*: the full task has exactly one consistent pair and every
fold's survivor set equals that same singleton. Segmentation does not enter:
it does not change generated background values, so determinacy over the 16
generator pairs is determinacy over the 32 accounts.

- **Strict LOO determinacy: 0/938 tasks (0.00%).** Only 6 tasks have a unique
  full-task survivor at all; in every one of the 3,040 folds' worth of
  re-identification, dropping a pair admits at least one extra account in at
  least one fold, so no single fold re-identifies the binding uniquely —
  anywhere in the pool.
- Weaker reading — the account common to *all* folds is unique (intersection
  of the fold survivor sets is a singleton): **6/938 (0.64%)**, exactly the six
  unique-survivor tasks (0a1d4ef5, 3bd292e8, d037b0a7, dae9d2b5, de493100,
  e99362f0). The binding is recoverable as the cross-fold intersection, never
  from one fold.
- Survivor-set stability at any size (every fold's set equals the full set):
  542/938 (57.78%); per-fold, 2,333/3,040 folds (76.74%) reproduce the full
  survivor set.

Ceiling reading: LOO folds cannot re-derive the background binding on their
own — on any pool task. Identification must be done once, on all k pairs, and
folds must inherit that binding (which is how §2.2 is written); any variant of
the component that re-identifies background inside each fold has a measured
determinacy of zero to stand on.

## 5. Reachable-mass join

Method: per task, modal-account pass and searched-account pass as in §2
(delta = searched-pass ∧ ¬modal-pass). The delta tasks' modal-account created
instances are then re-classified with `census/census_creation.py` logic
(copy_same_pair → copy_other_pair → ring → novel, in that order).

- Modal-account failures: 130/938. **Delta (rescued by account search):
  113/938 = 12.05% of the pool; rescue rate among modal failures
  113/130 = 86.92%.** 17/938 tasks pass under no account.
- Of the 113 delta tasks, **112 admit at least one consistent generator pair**
  under the §2.2 functional rule (one delta task passes the bound only via a
  non-functional binding the component would reject), and **0 are LOO
  unique-stable** (§4).
- Creation join over the 113 delta tasks: **1,950 created instances** —
  copy_same_pair 833, ring 333, **novel 726**, copy_other_pair 58.
  **All 113 delta tasks contain at least one novel instance** (minimum 1);
  the subset whose remaining content is already sourced elsewhere is **0
  tasks**. Every task the account search rescues at bound level still carries
  genuinely novel content the rest of the grammar must produce: background
  identification is necessary for the whole 113, sufficient for none of it.

---

## Component-ceiling arithmetic for the BG-GATE

The gate's bar is already registered (packet §2.3): PASS = ≥13/17 of the spent
draw's background deaths migrate (76.47%), with bg deaths ≤5/48 and all 4
banked fits preserved. These numbers price the ceiling; they do not move the
bar, and the denominators differ (pool bound failures vs the draw's lane
deaths), so what follows is ceiling arithmetic, not a prediction.

1. **Bound-level rescue rate.** Account search rescues 113 of 130 modal-account
   bound failures = **86.92%**, which is 10.45 points above the bar's 76.47%
   rate; applied mechanically to 17 deaths it is a rate-equivalent of
   **14.78 tasks** against a bar of 13. The pool ceiling does not rule the
   gate out — it clears the bar's rate with ~1.8 tasks of headroom.
2. **Binding-level ceiling.** 69/938 tasks (7.36%) admit no functional
   generator pair at all; on any such task in a future draw the component as
   specified cannot bind, at any content strength. Within the delta mass the
   binding rule costs 1 of 113 (112 stand).
3. **Certification-facing ceiling.** Fold-local re-identification is
   determinate on **0/938** tasks (§4). The component's LOO behaviour is
   therefore entirely carried by full-task identification inherited into the
   folds; a gate variant that re-identifies per fold would be testing a
   mechanism this census measures at zero.
4. **Sufficiency ceiling.** The join (§5) caps what migration can mean: all
   113 rescued tasks carry novel content, so background migration past the
   gate is a *necessary-condition* repair on every one of them; conversion
   still has to be earned by the content machinery downstream, under the
   certification dynamics the survivor census measured as the binding
   constraint (58/64 folds). The 86.92% rescue rate is a ceiling on the
   gate's migration, not an estimate of it.
5. **Subtype coverage.** The named patterns the component was designed
   against cover 184/356 of the pool's nonconstant mass (51.69%); the
   unnamed residual is 172 tasks (48.31%). If the draw's deaths mirror the
   pool's pattern mix, roughly half the migratable mass has no
   subtype-specific mechanism in the current specification — the generic
   cross-pair intersection has to carry it.

**Headline numbers.** (1) Viable accounts per task: median 4, mean 5.28, p90
12, max 32, 17/938 under none; 869/938 admit ≥1 consistent generator pair, 69
admit none. (2) Modal sufficiency: 762/938 = 81.24% functional (582 constant).
(3) Subtypes: context-dependent 143, input-modal pattern 19, single-pair flip
22, other nonconstant 172, constant 582 (of 938). (4) LOO determinacy: strict
0/938; cross-fold common-unique 6/938. (5) Reachable mass: delta 113/938
(12.05%), rescue rate 86.92% of modal failures, all 113 carrying novel content
(726 novel instances of 1,950 created).
