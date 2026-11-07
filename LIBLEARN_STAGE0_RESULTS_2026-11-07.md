# LIBLEARN Stage-0 Census — Verdict (2026-11-07)

**Instrument:** `stage0_census.py` (this directory), executing
`LIBLEARN_DESIGN_2026-11-07.md` §3.0 as registered. Local CPU, $0,
no GPU, no Kaggle, no draw taken, no code built, Exam #1 unspent.
Machine-readable results: `STAGE0_CENSUS.json`. Instrument wall
time: **8.1 s** (all substrate pre-banked; the run is joins and
re-aggregations over `census/param_per_task.jsonl` plus the
functionality recomputation over the 938 task files).

**Substrate validation (all four banked figures reproduced
exactly):** searched param bound 921/938 · modal-account bound
808/938 · tasks with ≥1 consistent generator pair 869/938 ·
(modal, modal) functional 762/938.

---

## The readings against the bars (design §3.0)

### Bar 1 — pool-level fit bound for the base DSL: **0.9083 — NOT triggered**

Staged representation (§1.1): background binding functional ∧
segmentation viable ∧ created content classifiable within the base
DSL's construction types, under one account. Headline reading
(functional account required; glyph credit removed):

| Variant | Tasks | Rate |
|---|---|---|
| A — searched param bound (reference, no staging) | 921 | 0.9819 |
| B — functional account, glyph on | 852 | 0.9083 |
| **C — functional account, glyph off (headline)** | **852** | **0.9083** |
| D — functional, const off, glyph on | 848 | 0.9041 |
| E — functional, const off, glyph off | 848 | 0.9041 |
| F — no functionality requirement, glyph off (reference) | 921 | 0.9819 |

The bound clears 0.90 under every variant — by 7 tasks at the
headline (852 vs the 844.2 threshold), by 4 tasks in the worst
variant. The restriction that binds is the component's own rule:
requiring a *functional* background binding costs 69 tasks
(921 → 852); the glyph exclusion costs **zero** additional tasks
(glyph is never load-bearing once functionality is imposed, and
is not load-bearing anywhere in the searched bound either —
variant F = A); removing const costs 4 more. Supply, at bound
level, is not what kills this species. (Compare the predecessors:
the modal grammar's account bound was 808/938 = 0.8614 and failed
this bar outright; the staged DSL representation is genuinely
wider — searched accounts plus a functional-binding discipline
the old lane never had.)

### Bar 2 — the F × U analogue: **< 0.90 under every completion — TRIGGERED**

Population: the survivor census's 28 spent A+B full-fit tasks.
Transfer to DSL terms by function-level inclusion (adversarial
choice 1, below): the grammar's fitting functions are a subset of
the DSL's, and the frozen certification's test-unanimity
criterion applies to the full-fit candidate population whatever
selection (§1.4) picks — so grammar-determined verdicts transfer:

- **Determined FAIL for DSL terms — 12/28:** the 8 unanimous∧wrong
  fits (a wrong-rendering fitting function exists in the DSL
  population; conversion fails whether it stays unanimous-wrong
  or pluralises to `ambiguous`) and the 4 non-unanimous fits
  (≥2 distinct test renderings already among the subset).
  Determined-only U = **0/12 = 0.000**.
- **Undecided — 16/28:** the 15 enumeration-capped cases plus
  ad38a9d0 (the program's one certified solve — undecided *for
  the DSL*, whose fold candidate sets and test population are
  unmeasured; LIBLEARN is credited with it only in the ceiling
  completion). Completed both ways, as the survivor census
  completed them: U conservative = **0/28 = 0.000**; U ceiling =
  **16/28 = 0.5714**.

Products (bar: F × U ≥ 0.90):

| F | × U ceiling 0.5714 | × U conservative 0 |
|---|---|---|
| 0.9083 (headline bound) | **0.519** | 0 |
| 0.9819 (old grammar bound) | 0.561 | 0 |
| 1.0000 (perfect supply) | **0.571** | 0 |

**Sensitivity — population choice cannot reopen it.** Adding all
15 later banked fits (bg lane, creation lane, fresh probe —
disjoint from the 28, zero accepted in any lane) as *undecided*,
the treatment most favorable to LIBLEARN available for them:
U ceiling = 31/43 = 0.7209, product at F = 1.0 is 0.721 < 0.90.
Adding the canary's 6 Python fits as undecided as well:
37/49 = 0.7551 < 0.90. No assembly of the banked fit record
reaches the bar.

### Disposition: **SPECIES CLOSES PRE-BUILD**

Design §3.0: "if … the F × U analogue reads < 0.90 under every
completion, the species is ceiling-bound exactly as its
predecessors were, and it closes here — no build, no slice, no
draw." That is the reading. Stage 1 is **not** commissionable.

The shape of the closure is worth stating exactly, because it is
not the old grammar's shape: there, F × U ≤ 0.982 × 0.857 failed
on a plural-and-wrong version space over a *narrow* language.
Here the staged representation *passes* the supply bar (0.9083)
and the product still fails at 0.519, because U is measured
against a strictly larger fitting population — every construction
the DSL adds to buy supply also adds fitting terms that can
render the test input differently or wrongly, and certification
prices the population, not the selection. Expressiveness moved
both factors in opposite directions, and the conversion factor
won. The binding constraint remains the survivor census's charge
(a) — candidate-population content on test inputs the train pairs
do not govern — now measured against the widest language the
program has proposed.

---

## Adversarial choices (each recorded per the commission)

1. **Candidate universe for U = the language's fitting functions**
   (version-space level), not a future search's returned sample.
   Basis: the survivor census's own pattern — it enumerated all
   cover-feasible schemas and stated the lane's candidate cap
   "does not apply to the version space" — and certify.py's
   criteria, which judge the candidate population's unanimity,
   not the selected program's quality. Determined verdicts
   transfer from grammar to DSL by function-level inclusion
   (every schema denotes a grid function composable from §1.1
   primitive classes; the commission defines the DSL as a fixed
   Turing-complete-enough term language over those classes). This
   choice is load-bearing for Bar 2 and is argued, not assumed:
   without it the 12 determined cases soften to undecided — and
   the sensitivity assembly above shows the closure survives even
   granting *every* unmeasured fit in the program as undecided
   (0.721–0.755 ceilings), because the 12 determined cases are
   what cap the survivor-population ceiling at 0.571 and no
   population assembly dilutes them below the bar.
2. **Glyph credit excluded** from the base-DSL bound: a glyph is
   an arbitrary pattern whose identity is a memorised function of
   a scene scalar — a learned-layer lookup, not a §1.1 base
   construction type, and Stage 0 prices the base DSL before any
   learning exists. Measured cost: zero tasks (B = C; F = A). The
   disposition does not depend on this choice.
3. **Const credit retained**: a literal pattern is a term in any
   compositional DSL, and §1.1's stamping takes an object (a grid
   value). Reported as sensitivity instead (variants D/E): its
   removal costs 4 tasks and moves no bar.
4. **Background priced at the component's own functional rule**,
   not the param census's looser account pass (which credits
   accounts whose per-pair background values form no function —
   a binding the §1.1 stage could never hand to a fold). This is
   the design's own staging read adversely where the census
   tradition offered a looser one; it is the largest single
   restriction in Part 1 (921 → 852).
5. **ad38a9d0 treated as undecided, not converted**, for the DSL
   (see Bar 2): the one certified solve in program history is
   credited to LIBLEARN only in the ceiling completion.
6. **Later lanes' fits treated as undecided** in the sensitivity
   assembly — never as determined fail — although all 19 of their
   certification attempts failed: their fold charges do not
   transfer under the §1.6 inheritance design, and their test
   unanimity was never censused. This is the most favorable
   treatment available for them, taken so the closure is not
   denominator-dependent.
7. **F for the headline product = the staged bound itself**
   (0.9083), with the product also shown at the old bound and at
   F = 1.0: closure holds at perfect supply, so no F choice is
   load-bearing.

## Secondary readout — per-class creation census (§3.0, not a bar)

The Q/L/R/F/S/M/C/T/P/G anatomy exists only on the 19 spent-draw
creation deaths (`CREATION_WALL_ANATOMY_2026-11-07.md` §1); no
pool-scale classifier for these classes exists in the substrate
and Stage 0 builds none. What is measured:

| Class | Spent-draw deaths | Banked fits in class | Certified solves in class |
|---|---|---|---|
| Q quotient/compression | 5 | 1 (67b4a34d — itself unanimous∧wrong) | 0 |
| L line/ray drawing | 3 | 0 | 0 |
| R replication/stamping | 3 | 0 | 0 |
| F frame generalization | 2 | 0 | 0 |
| S symmetry completion | 1 | 0 | 0 |
| M mirror-tiling | 1 | 0 | 0 |
| C count-parametric | 1 | 0 | 0 |
| T procedural texture | 1 | 0 | 0 |
| P part-selective split | 1 | 0 | 0 |
| G color-class gather | 1 | 0 | 0 |

Pool-scale creation mass (substrate's own classification, modal
account): 254 tasks carry ≥1 novel instance; 1,884 novel
instances — field_patch 914, primitive_unaddressed_color 419,
residual 358, const_recurrent 139, witness_tier1 49,
witness_tier2 5. So 777/1,884 novel instances (41.2%) are reached
by **no** banked construction classification at all (residual +
unaddressed-color primitives), before any fold dynamics.

Training population (spent union, assembled from the ten spent
draws and verified at exactly 312 ids): 80 of its tasks carry
novel content; its banked fits number 41 tasks; its certified
solves number exactly **one** (ad38a9d0 — not a creation-class
task). Per design §4(ii), the warning condition is met in
substance: for the dominant creation classes the library would
have had **zero** certified solved instances to compress in the
only population it may learn from without spending fresh tasks.
The Stage-1 slice was the proposed remedy; Bar 2 closes the
species before the question is reached.

## What this verdict does not claim

Stage 0 prices the *registered design*: this base DSL, this
selection discipline, the frozen certification. It does not
measure EXEC-SYNTH (whose conversion gate is separately in
flight), any future language with a different candidate-source
registration, or the sealed exam. The fit bound is a necessary-
condition bound in the census tradition — it certifies that
0.9083 of the pool is not *provably outside* the staged
representation; it is not a fit measurement, and no fit was
attempted anywhere in this census.
