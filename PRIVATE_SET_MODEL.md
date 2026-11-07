# PRIVATE-SET MODEL — what the 240 hidden tasks most plausibly are, and where APEX-2 is blind

Built 2026-11-02 (desk analysis, no GPU). Every number is traceable to a
computation in `private_set_analysis.py` / `private_set_aggregate.py` or to a
file cited next to it. Machine-readable table: `private_set_families.json`.
Per-task labels and evidence: `private_set_analysis_raw.json`.

**Headline.** If the private 240 are drawn the way the public eval-120 are
drawn, **~232 of the 240 tasks (96.7%) sit in the two families where every
measured component of our stack scores exactly zero**: novel mechanisms no
cheap evidence can name (154 expected) and content-determined size changes
(78 expected). The mined library solves **0 of 120** eval tasks; the full
depth-1 DSL-1 battery fits **0 of 120**. Everything our measured stack
provably carries — crops, tilings, gravity, symmetry completion — is
precisely what the eval draw does not contain. The campaign therefore rests
on the one arm with no measurement yet: LLM program induction, which P2
probes first.

## 1. The extrapolated private-240 family mix

Classification rule (one primary family per task, applied identically to all
sets): (1) a mined-library program re-run under the honest gate (parameters
learned from train pairs only; train fit + test exact) — `sft_seed*.jsonl`,
62 programs; (2) a depth-1 DSL-1 battery (~250 parameterized candidates over
the 27 ops in `apex2_probe_launch.py`, incl. the new `copyc` search) plus
learned probes (crop-to-color-bbox, quadrant, interior strip, phased
sample-grid, keep-color), same gate; (3) pair-statistics signatures
(subgrid extraction, enclosed-background fill, object partition / move /
multiplicity, symmetry repair); (4) residual = `novel_unclassified`.
Intervals: Wilson score interval (z = 1.96) on the eval-120 proportion,
scaled ×240; marginal per family, not simultaneous.

| Family | Eval-120 | Train-1000 | Expected in 240 | 95% interval | If drawn like training |
|---|---|---|---|---|---|
| novel_unclassified | 77 (64.2%) | 562 (56.2%) | **154.0** | [132.6, 173.2] | 134.9 |
| size_change_arithmetic | 39 (32.5%) | 249 (24.9%) | **78.0** | [59.5, 99.1] | 59.8 |
| copy_to_markers | 3 (2.5%) | 18 (1.8%) | 6.0 | [2.0, 17.0] | 4.3 |
| fill_enclosure | 1 (0.8%) | 17 (1.7%) | 2.0 | [0.4, 11.0] | 4.1 |
| crop_extract | 0 | 54 (5.4%) | 0 | [0, 7.4] | 13.0 |
| object_recolor_by_property | 0 | 25 (2.5%) | 0 | [0, 7.4] | 6.0 |
| symmetry_repair | 0 | 17 (1.7%) | 0 | [0, 7.4] | 4.1 |
| tiling_scaling | 0 | 17 (1.7%) | 0 | [0, 7.4] | 4.1 |
| counting_conditioned | 0 | 12 (1.2%) | 0 | [0, 7.4] | 2.9 |
| object_move | 0 | 7 (0.7%) | 0 | [0, 7.4] | 1.7 |
| rigid_transform | 0 | 7 (0.7%) | 0 | [0, 7.4] | 1.7 |
| multi_object_relational | 0 | 5 (0.5%) | 0 | [0, 7.4] | 1.2 |
| global_recolor | 0 | 4 (0.4%) | 0 | [0, 7.4] | 1.0 |
| gravity_settle | 0 | 4 (0.4%) | 0 | [0, 7.4] | 1.0 |
| symmetry_completion | 0 | 2 (0.2%) | 0 | [0, 7.4] | 0.5 |

Family definitions are operational, tied to the evidence that assigns them:
`size_change_arithmetic` = output size differs from input size (or varies by
pair) with no depth-1/subgrid explanation — an evidence class, not a proven
mechanism (see §4). `copy_to_markers` in eval rests on the statistics
signature only (an input object pattern's multiplicity grows in the output);
treat its true count as 0–3.

**Distribution shift, eval vs training** (the generator's eval skew): the
eval draw is *less* mechanical than training on every axis the prior census
measured (`arc_census/census.json`): same-shape tasks 81/120 vs 682/1000,
but the eval same-shape tasks are far less often cheap-rule tasks; pair-level
new-color rate 0.128 (eval) vs 0.303 (train); crop signature 0.003 vs 0.061;
tile signature 0.006 vs 0.072; and eval grids are much larger (train-pair
inputs median 18×19 vs 10×10; test inputs median 23×22, 24.6% at maxdim 30
vs 4.4%). This computation's shape layer agrees with the census up to its
task-level tie rule (81 same-only, 3 grow-only, 31 shrink-only, 5
mixed-relation eval tasks). Family-level consequence: training's long tail
of named families (11 families, 189 tasks) collapses in the eval draw to
two residual buckets plus traces — the eval generator spends its budget on
one-off mechanisms at larger grid sizes.

## 2. Coverage map — measured, per family

Channels: **Lib-E / Lib-T** = mined-library full solves on eval / training
tasks in the family (all 62 programs re-run against all 1,120 tasks).
**Batt-E** = depth-1 DSL battery fits on the family's eval tasks.
**Compose** = tasks in `synth_tasks_compose.jsonl` (6,040) whose generating
chain maps to the family. Verdict rubric: a family *present* in eval-120 is
CARRIED only with a library eval solve; otherwise PARTIAL if some measured
channel reaches it, BLIND if none does. A family *absent* from eval-120 is
judged on training machinery: CARRIED = library solves + compose generates
+ DSL expresses; PARTIAL = one channel missing; BLIND = two or more missing
or the language cannot express the mechanism.

| Family | Lib-E | Lib-T | Batt-E | Compose | DSL-1 can express? | Plausible carrier | Verdict |
|---|---|---|---|---|---|---|---|
| novel_unclassified | 0 | 0 | 0 | 0 | no | LLM-Python induction (TRM secondary) | **BLIND** |
| size_change_arithmetic | 0 | 0 | 0 | 0 | partial | LLM-Python induction (DSL chain-induce secondary) | **BLIND** |
| copy_to_markers | 0 | 1 | 0 | 0 | yes | DSL synthesis / LLM-Python | PARTIAL |
| fill_enclosure | 0 | 2 | 0 | 315 | partial | DSL synthesis / TRM | PARTIAL |
| crop_extract | 0 | 4 | 0 | 1,901 | yes | DSL / LLM-Python | CARRIED |
| tiling_scaling | 0 | 17 | 0 | 1,817 | yes | DSL / LLM-Python | CARRIED |
| gravity_settle | 0 | 4 | 0 | 930 | yes | DSL / TRM | CARRIED |
| symmetry_completion | 0 | 2 | 0 | 604 | yes | DSL / TRM | CARRIED |
| multi_object_relational | 0 | 5 | 0 | 216 | yes | DSL / LLM-Python | CARRIED |
| rigid_transform | 0 | 7 | 0 | 170 | yes | DSL / frames-TTA | CARRIED |
| object_move | 0 | 1 | 0 | 87 | yes | DSL / LLM-Python | CARRIED (thin: 1 program) |
| object_recolor_by_property | 0 | 3 | 0 | 0 | partial | LLM-Python / DSL | PARTIAL |
| counting_conditioned | 0 | 12 | 0 | 0 | partial | LLM-Python / DSL | PARTIAL |
| global_recolor | 0 | 4 | 0 | 0 | partial | LLM-Python / DSL | PARTIAL |
| symmetry_repair | 0 | 0 | 0 | 0 | no | TRM / LLM-Python | **BLIND** |

Notes on the non-obvious cells:

- **Compose = 0 for global_recolor / object_recolor_by_property /
  counting_conditioned is structural, not an oversight**: `gen_compose.py`
  excludes pairs-dependent ops (colormap, local_counts, local_cross,
  recolor_by_size) because they learn parameters from pairs and "cannot
  generate standalone." Those three families' only SFT supply is the 62
  real seeds (4 + 3 + 12 = 19 of them).
- **Compose = 0 for copy_to_markers is a vintage artifact**: the bank was
  built 2026-11-01; the `copyc` op shipped 2026-11-02. The op verifies its
  mined instance exactly (3/3 train + 1/1 test, `sft_seed_m6.jsonl`), but
  no generator produces the family yet.
- **fill_enclosure is PARTIAL despite full machinery** (op + 2 programs +
  315 compose tasks) because the one eval instance the fill signature
  labels is fit by *neither* fill mode (fixed color / surrounding
  majority) — its fill rule is a variant the op does not capture.
- **CARRIED verdicts are training-proven, not eval-proven.** They say: if
  the private draw contains these families (each bounded at ≤ ~7 tasks),
  the machinery demonstrably handles them. They contribute 0 expected tasks
  under the eval-draw model.
- The frames result in `PROBE_LEDGER.jsonl` (DSL induce solves 3 tasks
  under all 8 dihedral frames, 0 frame-exclusive) is consistent with this
  map: those solves are training-distribution tasks; on the true eval-120
  the same proposer class fits nothing.

## 3. Blind-spot build list — ordered by expected private tasks at stake × closability

Closability scale: 5 = a single op/generator switch with known semantics
(the `copyc` precedent: specified, ported, differentially verified, and
shipped in a day); 4 = new ops whose probe code already exists, or a
bounded search extension; 3 = generator rework; 2 = needs the LLM/GPU loop
to even measure; 1 = mechanism unknown.

1. **Size-change mechanism kit** — stake 78.0 [59.5, 99.1] × closability 4
   = **312**. Three concrete builds: (a) promote the learned probes that
   already exist in `probe_families.py` / `probe_families2.py` to
   first-class DSL ops — crop-to-frame/color-bbox, quadrant/section
   extraction, separator-split (output = the section of the input cut by
   full separator lines), phased sample-grid (the launcher's `scale_down`
   is phase-0 only); (b) canvas-from-content ops — output dimensions taken
   from an object count, a marker count, or the largest object's size;
   (c) a depth-2/3 chain-induce pass restricted to shape-changing tasks:
   the validation disagreements (§4) prove a real share of shape-changers
   are ordinary op *compositions* (e.g. `crop_bbox | scale_up 2`,
   `rot 2 | tile_mirror`), invisible to a depth-1 battery. SFT shape:
   compose v2 must include size-changing chains, not only same-shape ones.
2. **Novel-mechanism flywheel — the LLM arm's data engine** — stake 154.0
   [132.6, 173.2] × closability 2 = **308**. This family is the
   competition; there is no op to add because the mechanisms are the
   unknown. Builds: (a) the D5 input-generator flywheel from the frontier
   report — LLM-written Python *input generators* paired with verified
   Python programs, unit-test filtered, manufacturing novel-mechanism
   tasks the op bank cannot express (the NVARC recipe); (b) SFT v2
   (6,102 records, audit 6,102/6,102 — `sft_v2_python.jsonl`) already
   carries library + compose in Python; extend its distribution with
   generator-made mechanisms before scaling record count; (c) proposer
   prompting with dual encoding (raw grid + OBJ object stream, BLUEPRINT
   §2) and the temperature ladder — P2's zero-shot recall on eval-30 is
   the first measurement of whether this family is contestable at all,
   and it gates everything downstream (charter G1–G5).
3. **copyc flywheel family** — stake 6.0 [2.0, 17.0] (tentative) ×
   closability 5 = **30**. Compose v2 with `copyc` eligible (one-line
   eligibility change; the bank predates the op), plus a targeted depth-2
   mining pass over the 17 training tasks carrying the copy-multiplicity
   signature to bank more verified instances beyond the single seed.
4. **Symmetry-repair op** — stake 0 expected, ≤7.4 bound (17 training
   instances) × closability 4 = **~15** (bound-midpoint stake).
   `repair h|v|rot` — symmetrize by mirrored-majority vote between the
   two halves — plus a family probe over training to bank verified
   instances. The TRM lane is the secondary carrier for texture-level
   repair.
5. **fill_holes owner mode** — stake 2.0 [0.4, 11.0] × closability 4 =
   **8**. Add `fill_holes owner`: each enclosed background region takes
   the color of the object that encloses it (per-region), the variant the
   eval instance appears to use. Acceptance test is measured and waiting:
   the op must fit that eval task (currently fit by no mode) without
   breaking the 2 library fill programs.
6. **Pairs-dependent compose support (structural)** — stake: three
   PARTIAL families at 0 expected / ≤7.4 bound each, 41 training instances
   combined (25 + 12 + 4) × closability 3. Compose v2 learns a
   pairs-dependent op's parameters from a generated base task (sample the
   base grid, derive the colormap / local rule / size-rank map, then emit
   task + program), removing the exclusion in `gen_compose.py`. Ranked
   last by the expected-value rule; it is nonetheless the cheapest
   diversity fix in the system, because today 19 of the 62 seed programs
   teach mechanisms no synthetic task reinforces.

Watch item (no build ranked): **object_move is CARRIED on a single library
program.** If the private draw leans training-like (crop 13.0,
object_recolor 6.0 expected), thin families matter more than the eval-draw
model prices them.

## 4. Method and validation

- Library integrity: the cross-run reproduces all 62 seed programs on
  their own tasks (62/62 full solves) and finds **zero** cross-task solves
  anywhere — the library's coverage is exactly its 62 mined instances, no
  generalization halo. This matches every prior measurement in
  `PROBE_LEDGER.jsonl` (induce_v0 eval-30 pool recall 0/30; sprint DSL
  eval-12 0/12; analogy transplant eval-120 solves 0).
- Classifier validation: with the library withheld, the battery+stats
  classifier agrees with the solving program's family on **53/62 (85%)**
  of mechanism-known tasks. The 9 disagreements are characterized, not
  random: 6 are multi-op chains whose output size changes (the stats layer
  labels any unexplained shape change `size_change_arithmetic` — that
  family's counts are therefore an upper bound on truly
  content-arithmetic tasks and include an unknown share of compositional
  ones); 2 are depth-2 chains; 1 task is genuinely two-mechanism
  (colormap and local_counts both fit it exactly).
- Spot checks: sampled `novel_unclassified` eval tasks are honestly
  unclassified — e.g. `135a2760` is periodic pattern completion inside a
  frame; `13e47133` is a multi-region quadrant-texture rule. Neither is
  within a depth-1 op of the battery.
- Eval labels were verified against the public solutions file
  (`arc-agi_evaluation_solutions.json`); all solver-side numbers (library,
  battery) were computed under the train-learned gate, i.e. as the solver
  would meet the tasks live.

## 5. The honest page — what this model cannot know

- **Task identity.** This is a distribution model over mechanisms. It says
  nothing about any individual private task, and no line in it should be
  read as "task #N will be X."
- **Sampling width.** n = 120 is small. The headline family's interval
  spans 41 tasks ([132.6, 173.2]); the two big families could jointly be
  anywhere from ~192 to ~272 of 240 at their marginal bounds. Intervals
  are marginal, not simultaneous — do not sum upper bounds, and do not
  read an expected 0 as an actual 0.
- **Unseen families.** A family absent from a 120-task sample can still
  constitute up to ~2.5% of the generator at 95% confidence (rule of
  three: 3/120; Wilson bound here 3.1%, ≈ 7.4 tasks in 240). Eleven
  families sit at zero in eval-120; the private set's tail is wider than
  any single row of the table.
- **Generator drift is the biggest unknown, and we have already measured
  it once.** The eval-120 are the ARC-AGI-2 *public* evaluation set. The
  ARC Prize 2027 private 240 may be refreshed or extended. Our own
  staged-240 file (the 2026 competition's hidden-set stand-in, censused in
  `arc_census/CENSUS_240_2026-10-27.txt`) profiled *training-like*, not
  eval-like: same-shape 70.4%, new-color pair fraction 0.339 vs the public
  eval's 0.128. A hidden set in this ecosystem has already once refused to
  mirror the public eval. The "if drawn like training" column in §1 is
  the standing alternative scenario: under it, ~65 expected tasks move
  from the two blind buckets into named, partly-carried families — better
  for us, still dominated by the unclassified bucket (134.9).
- **Classifier blindness is directional.** `novel_unclassified` is an
  upper bound on true novelty (a depth-2/3 induce pass over eval-120 —
  desk-feasible, not yet run — would name some of it), and
  `size_change_arithmetic` is an upper bound on content-arithmetic size
  rules. Conversely the statistics-signature labels (copy_to_markers in
  eval above all) are signatures, not proofs; that family's eval count is
  honestly 0–3.
- **Coverage is measured only where measurement exists.** CARRIED /
  PARTIAL / BLIND describe the library, the compose bank, and the DSL —
  the components with numbers. The LLM induction arm, the designated
  carrier for ~232 expected tasks, has *no* eval measurement yet
  (zero-shot R0 runs at P2). This model therefore cannot say the private
  set is 97% out of reach; it says 97% of it is out of *measured* reach,
  and the instrument that decides the question has not been switched on.

## ERRATUM (2026-11-02, from the size-change kit build)
§3.1a named "separator-split" among the learned probes that already
exist. It does not: no implementation exists in probe_families.py,
probe_families2.py, private_set_analysis.py, or the sprint solver —
the name appears only in BLUEPRINT.md's aspirational op table. The
kit build ported "quadrant" (build item 1a's other named probe, exact
implementation on record) as op #30 instead of inventing semantics.
Kit outcome: ops #28 crop_frame, #29 sample_grid, #30 quadrant,
DSL v1.5; oracle 120/120, differentials 18,922/18,922 clean, 62/62
seeds re-verify; depth-1 battery on eval-120 unchanged at 0/120 —
the kit closes expressibility, not depth-1 fit. Canvas-from-content
was not added: no probe form exists to port.
