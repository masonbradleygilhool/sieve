# APEX-2 NEXT-GENERATION SOLVER — DESIGN (2026-11-04)

**Status:** design + first local probe. Every number in §6 is MEASURED from the
probe run recorded beside this file; every number elsewhere is either quoted
from the banked failure record (labeled) or labeled TARGET/ESTIMATE. No score
is claimed for the private eval. The acceptance criterion stands as ordered:
**90%+ on the ARC-AGI-2 private eval (216+/240)**; design target 240/240.

---

## 1. What every dead lane had in common (the failure record, measured)

P2 Groq zero-shot: 0/120 tasks, 0 exact fits, 0 near-misses in 102 banked
completions. P3 conditioned (retrieval-grounded): 0 exact fits, 0 near-misses.
Retrieval-as-proposer: 2/120 tasks with a train-fitting corpus program,
0/120 solved at every accounting (top-1, ≤2, unlimited); median cell
agreement 0.776. Library growth 478 → 39,065 verified programs: eval solve
delta exactly zero. DSL enumeration: oracle 120/120 vs 0/120 in fact;
gauntlet fresh A+B = **0/48, Wilson [0%, 7.4%]**, with 4 train-fit-only
false positives. TRM (2026 campaign): 196 train fits → 0 test solves;
smoke Gate A FAIL; the full-config CUDA run poisoned at step 0.

Strip the surface differences and all five lanes are the **same
architecture**:

> **Propose a complete rule from a prior; use the train pairs only as a
> post-hoc accept/reject filter.**

Only the prior changed: a fixed operator algebra (DSL), a corpus of whole
programs (library, retrieval), a language model's distribution (P2/P3), a
continuous relaxation fit by gradient descent (TRM). In every case:

1. **The hypothesis is monolithic.** A whole rule is guessed as one object.
   The space of whole rules consistent with nothing is astronomically
   larger than what 2–5 pairs can pin down, so conversion depended on the
   prior happening to contain the rule at reachable depth/rank/sample —
   measured: it did not, five times.
2. **Evidence enters only at the end.** Train-exactness was the acceptance
   test, and train-exactness is achievable by memorization (TRM, 196→0)
   and by spurious programs (gauntlet `445eab21`: a program fitting every
   train pair, wrong on test; three more from the pairs-dependent family
   that fits *by construction*). No lane ever asked the only
   generalization question answerable inside a task: *can the rule be
   re-induced from fewer pairs and still predict a held-out pair?*
3. **Correspondence was never computed.** No lane ever measured which
   input object becomes which output object, what is deleted, what is
   created, what moves where. Retrieval's 0.776 median cell agreement is
   the signature of this: structurally near, never exact, because the
   unit of transfer was the whole grid/program instead of the object
   correspondence, which is where ARC rules actually live.

**The binding constraint, restated mechanically:** exact-rule
identification fails because the lanes searched a prior over whole rules
with a memorization-blind acceptance test. Generation, ranking, and
budget were never the wall — oracle recall was 120/120 the whole time.

## 2. The mechanism: correspondence-first induction with held-out acceptance

The design inverts both failures. **Evidence first, hypothesis
constructed — never sampled. Acceptance by within-task held-out
prediction — never by fit.**

### 2.1 What it computes that no dead lane computed

For each train pair, the solver computes an **object-level edit script**:

- Segment input and output into objects (8-connected components of
  non-background cells; background = modal color). An object carries its
  cell pattern (relative coordinates × color), size, and
  dihedral-canonical shape signature.
- Match output objects to input objects: same cell count, shape equal
  under a dihedral transform τ, and a cellwise color map φ that is a
  *function* on the object's colors. Unmatched input objects are
  deletions; unmatched output objects are creations.
- Each match yields one **action instance**: (object feature class) →
  (τ, φ, displacement rule). Feature class = (colors, size, canonical
  shape). Displacement is certified only in the forms v1 can verify:
  same origin, or a constant offset shared by every instance of the
  class across all pairs.

### 2.2 Identification by intersection, not by prior

The rule is the **schema**: the assignment of one action per feature
class that is *simultaneously consistent with every train pair's edit
script*. Each additional pair shrinks the schema space multiplicatively
— a class seen in two pairs with different surroundings must take the
same action in both; a color map must be a function everywhere it is
used; a class matched in one pair and deleted in another kills the
schema outright. Nothing is drawn from a corpus, an algebra, or a model
distribution: the hypothesis space is built from the task's own measured
correspondences, so library size, enumeration depth, and sampling
temperature — the three knobs five lanes died turning — do not exist
here.

### 2.3 Acceptance: leave-one-out prediction (the memorization killer)

A schema is accepted only if it **predicts a held-out train pair**:

- ≥3 train pairs: for every pair j, re-induce the schema from the other
  pairs alone and require an exact prediction of pair j's output.
- Exactly 2 train pairs: leave-one-out induction from a single pair
  underdetermines positional actions, so acceptance instead requires
  full fit **plus determinacy** — every test-input object's feature
  class was seen in training. (Known weakness, stated at this strength:
  2-pair tasks carry weaker certification than ≥3-pair tasks.)

A memorizer cannot pass this test (a TRM fit on k−1 pairs does not
predict pair k — that is precisely the 196→0 mechanism, excluded by
construction). A pairs-dependent op that fits by construction cannot
pass it either, because its "rule" is re-fit per pair and the held-out
pair is the one place it was never fit. Spurious whole-rule fits like
`445eab21` survive only if the same wrong schema is *also* what k−1
pairs induce and it *also* predicts the held pair — possible, but a
strictly smaller failure class than "fits all pairs," and it is the
strongest acceptance signal extractable from inside the task.

On acceptance failure the solver **abstains** (emits no candidates)
rather than guessing: the probe measures the mechanism as specified,
and abstention keeps the solve metric identical to the certification
metric.

### 2.4 Composition and size change

Grid-level dihedral transforms are detected by shape-consistency
intersection across pairs and factored out before object analysis (the
2026 frames test measured frames alone at zero exclusive solves — here
they are a normalization step, not the mechanism). Output canvas is the
transformed input canvas, or a crop-to-content-bounding-box when that
is consistent across all pairs. Background recolor is a first-class
schema component (modal-color mapping, consistency-checked).

### 2.5 What v1 deliberately cannot do (coverage honesty)

Creations that are not copies-in-place of input objects, object
splitting/merging, counting/arithmetic rules, relational displacement
("move until contact", "align to the largest object"), and pattern
completion are outside v1's schema language. Tasks needing them return
NO-SCHEMA. The probe reports the coverage rate alongside solves; a
mechanism that solves a slice exactly and names its slice is the
design's claim — nothing more is claimed.

### 2.6 The DSL executor's status

The DSL executor survives **only as substrate, at exactly this
strength**: a verified execution engine for candidate programs. In this
design its one sanctioned future role is residual search — search
restricted to the sub-grid a certified schema leaves unexplained —
which no dead lane ever attempted (they searched whole grids with
whole-rule priors). Probe v1 does not wire it in; the identification
core is measured alone, so its conversion cannot be borrowed from or
blamed on the substrate. Retrieval, library growth, LLM proposing, and
gradient TTT do not survive in any role: their measured conversion is
zero and their failure mode (prior-first, fit-accepted) is the thing
being replaced.

### 2.7 No LLM component

The mechanism constructs its hypothesis from measured correspondences;
there is no step at which sampling text from a language prior enters.
P2/P3 measured that form at 0 exact fits / 0 near-misses across every
conditioning tried, including retrieval grounding. Adding it here would
re-import the dead architecture through a side door. Zero API calls.

## 3. Why this attacks exact-rule identification mechanically

Not by analogy — by construction, at the three measured failure points:

| Dead-lane failure (measured) | Mechanism's counter (structural) |
|---|---|
| Rule absent from prior at reachable depth (DSL modes #1/#2: 8/12 A-pool tasks burned full budget, no fit in space) | No prior. Schema space is generated from the task's own correspondences; if the rule is an object-correspondence rule, it is in the space by construction, and intersection finds it or refutes the class |
| Train-exact false positives (196→0; `445eab21`; pairs-dependent family) | Acceptance = held-out prediction inside the task. Memorization and per-pair fitting are excluded by the form of the test, not by a tuned threshold |
| Whole-program transplant near-miss (retrieval 0.776 cell agreement, 0 solves) | Unit of transfer is the per-object action, composed per task. Objects recur across tasks; whole rules do not — the schema is assembled from the current task's objects only |

## 4. Cheapest falsifiers (named before the run)

- **F1 — reach:** if the schema explains all train pairs (full fit) on
  <10% of fresh A+B tasks, the correspondence representation does not
  reach ARC's rule space and the design is wounded regardless of solves.
- **F2 — conversion:** 0 LOO-accepted solves on A+B = kill (§5 gates).
- **F3 — degeneracy:** if accepted solves are dominated by the
  degenerate single-object colormap case, the active ingredient is a
  lookup table, not object-schema induction → redesign, not scale.
- **F4 — algebra shadow:** if the lane scores on compose-control pool C
  but not on real pools, it has learned the substrate's algebra again —
  the exact disease of every prior lane.

## 5. Pre-registered probe gates (written before any run)

**Instrument:** `gauntlet.py`, unmodified. Draw **A:12, B:36, C:12**,
seed **20261104** (fresh draw; the DSL baseline used seed 20261103),
budget **25 s/task**, single draw. Primary metric: **accepted-schema
solves on A+B (n=48)**, Wilson 95% reported for every rate. Solves are
counted per mechanism tag (object_schema / colormap_only /
grid_transform) in the results file.

**Controls (must pass before the run counts):** (i) positive control —
a synthetic task with a known object move+recolor rule must be solved;
(ii) negative control — the same task with shuffled train outputs must
not be solved and must not produce an accepted schema; (iii) harness
controls already on record (probe.py oracle 120/120, null 0/120;
gauntlet baseline behaved sanely on pool C).

**Gates on A+B solves:**
- **KILL:** 0 solves → the design is dead at probe strength. No
  iteration on this mechanism without a new measured idea.
- **WEAK-ALIVE:** 1–3 solves, all LOO/determinacy-accepted, at most one
  of them colormap_only → the identification loop fires on real fresh
  tasks (a campaign first: every prior lane's fresh A+B solve count is
  0). Earns exactly one iteration: schema-language extension aimed at
  the measured NO-SCHEMA classes. No scale.
- **ALIVE:** ≥4/48 solves (≈8.3%) → earns scale: a 96-task fresh B draw
  plus the schema extensions the NO-SCHEMA taxonomy ranks first.
- **F3 override:** if ≥half of all solves are colormap_only, the
  verdict is capped at WEAK-ALIVE regardless of count.

**Accounting rules:** the lane reads train pairs and test *inputs*
only — test outputs are stripped before induction by construction, so
the cheating channel does not exist in the code path. `fits=1` is
reported to the gauntlet only for accepted schemas, so the gauntlet's
train-fit-only class means "certified fit, wrong test" and abstentions
land in no_fit with their reason in the run log.

## 6. Probe result — VERDICT: KILL (measured, 2026-11-04)

Full record: `NEXTGEN_PROBE_RESULTS_2026-11-04.md`; gauntlet run
`gauntlet/runs/run_1793816913_seed20261104_nextgen_v1.json`.

**A+B = 0/48 solved, Wilson [0%, 7.4%]** — identical to the DSL
baseline. F2 triggered (0 accepted solves) and F1 triggered (full-fit
coverage 2/48 = 4.2% < 10% floor). Per §5, the design as specified —
the v1 schema language of preserved-or-deleted objects — is **dead at
probe strength**; the gates stand unamended. Death taxonomy: creation/
split-merge 35/48, non-dihedral size change 11/48, LOO-rejected 2/48
(the acceptance gate caught both full-fit schemas that failed to
generalize within-task — the certification component is validated and
reusable; the schema language is what died). Controls: positive PASS,
negative PASS. Cost of the measurement: 1.5 s CPU, $0.

## 7. Exceptionality gate (computational_research_hpc skill)

1. **Conventional approach / why insufficient:** propose-and-check over
   a prior (program enumeration, corpus retrieval, LLM sampling,
   gradient TTT). Insufficient *as measured on this exact problem*: five
   independent priors converted at 0 on fresh tasks; the acceptance
   test they share is memorization-blind.
2. **New mechanism:** hypothesis *construction* from measured object
   correspondences, identified by cross-pair constraint intersection,
   certified by within-task held-out prediction. Neither component
   exists in any prior lane of this campaign.
3. **Verification strength above norm:** pre-registered kill/alive
   gates in this document before the run; controls before the scored
   draw; per-task mechanism tags; abstention accounting that makes the
   headline metric identical to the certification metric; test outputs
   stripped by construction; raw gauntlet run record + per-task results
   file published beside the design.
4. **Cheapest decisive falsifier:** this probe — one CPU draw, 60
   tasks, zero spend. F2 (0 solves) kills the design outright.
5. **Independent path that could prove it wrong:** the gauntlet itself
   is the hostile instrument (fresh tasks, fixed harness, baseline
   0/48 banked); pool C is the algebra-shadow detector (F4); the
   negative control detects a lane that "solves" noise.
6. **Compounding asset:** the correspondence extractor + schema
   inducer + LOO certifier are reusable machinery for any future lane;
   the NO-SCHEMA taxonomy it emits is a measured map of exactly which
   rule classes remain unaddressed, ranked by frequency — the next
   design starts from data, not intuition.
7. **Obligation closed if it succeeds:** the campaign's central open
   obligation — *any* nonzero, certified conversion on fresh real ARC
   tasks — closes. That is the first step on the only arithmetic path
   to 216+/240: recall of true rules by construction, certified
   selection, then coverage extension class by measured class.

## 8. Honest distance statement

Even an ALIVE verdict measures single-digit conversion on 48 tasks
against a 90% acceptance criterion. This probe does not claim a path
*demonstrated* to 216/240; it claims a mechanism whose first measured
step either exists or does not, with the kill gate armed. Anything
stronger said before the run would be the fabrication the charter
forbids. (ESTIMATE, labeled: object-correspondence rules are one family
among ARC's rule classes; the NO-SCHEMA taxonomy from this run, not
this document, will size the family's share of pool B.)
