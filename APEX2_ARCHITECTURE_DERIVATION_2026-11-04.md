# APEX-2 ARCHITECTURE DERIVATION — census first, derivation second (2026-11-04)

**Commission:** maximum thinking before building. The v1 design wrote
its schema language before measuring what the fresh-task population
contains, and the two operation classes that killed 46/48 of its draw
were knowable in advance. This document exists so that never happens
again. **No solver code is written here and no probe is run here.**
Every population number below is MEASURED from the full census of
gauntlet pool B (938 tasks, 3,040 train pairs) in
`census/`; every other claim is labeled. The acceptance criterion
stands as ordered: **90%+ on the ARC-AGI-2 private eval (216+/240)**,
design target 240/240. The v2 probe had not reported at the time of
writing — v2 appears here as a design with pre-registered gates, not
as a measured result.

**How to read the numbers.** Census counts are exact for pool B
under the fixed operational definitions in `census/README.md`. A
"census class" is a class *under those definitions* (staged greedy
matching, modal-color background, primary per-color 4-connected
segmentation). Where a number is an upper bound (necessary
conditions only), it is labeled BOUND. Where a number is a proxy for
a rule class the census cannot see directly, it is labeled PROXY.

---

## 0. The census in one page (pool B, MEASURED)

### 0.1 Sample size and pair counts

| Quantity | Value |
|---|---|
| Tasks (pool B) | 938 |
| Train pairs total | 3,040 (mean 3.24/task) |
| Train pairs per task | 2→146 (15.6%), 3→542 (57.8%), 4→173, 5→48, 6→18, 7→8, 8→2, 10→1 |
| Test pairs (not measured) | recorded per task in the raw table only |

### 0.2 Size change (task-consistent class)

| Class | Tasks | % |
|---|---|---|
| Same size, every pair | 639 | 68.1 |
| Shrink, every pair | 222 | 23.7 |
| Grow, every pair | 68 | 7.2 |
| Mixed signs | 9 | 1.0 |

Pair-level signs: (0,0) 65.3%, (−1,−1) 19.6%, (+,+) 6.6%,
single-dimension shrink 6.7%, single-dimension grow 1.2%,
cross-sign 0.5%. **Of the 1,054 size-changing pairs, 663 (62.9%) are
non-integer deltas** — neither an integer grid scale-up nor
scale-down. Task-level: 167 tasks purely non-integer-delta,
49 purely integer-up, 39 purely integer-down, 44 mixed. Canvas
change in this population is mostly crop/pad/extend semantics, not
uniform scaling.

### 0.3 Object accounting (primary segmentation)

Mean objects per pair: **14.5 in / 12.7 out** (agnostic
segmentation: 4.6 / 3.3 — the two segmentations disagree by ~3x on
object count; see §1.4). Object-count delta pattern, task level:
more 38.3%, fewer 29.9%, mixed 14.3%, same **17.6%**. Only 17.6% of
tasks conserve object count in every pair. Non-background cell
count: more 41.4%, fewer 29.1%, same 19.1%, mixed 10.4%.

### 0.4 Per-object fates (% of tasks exhibiting the fate in ≥1 pair)

| Fate | % tasks | Object instances (all pairs) |
|---|---|---|
| preserved (dihedral + same colors) | 77.9 | 22,392 |
| created (no correspondence) | 55.7 | 10,405 |
| deleted | 46.2 | 15,453 |
| grown (colorblind containment, input ⊂ output) | 38.3 | 2,216 |
| recolored (shape preserved, functional color map) | 33.9 | 3,059 |
| shrunk (output ⊂ input) | 26.3 | 1,717 |
| scaled (integer block scale, either direction) | 9.4 | 341 |
| reshaped (same cells + color multiset, new shape) | 3.8 | 62 |

### 0.5 Creation split (the 10,405 created instances, MEASURED)

| Source of the created object's pattern | Instances | % | Tasks containing it |
|---|---|---|---|
| Copy of a pattern present in the **same pair's** input | 6,697 | 64.4 | 334 (35.6%) |
| Rectangular single-color ring (frame-like) | 1,439 | 13.8 | 213 (22.7%) |
| Copy of a pattern present in **another pair's** input only | 385 | 3.7 | 117 (12.5%) |
| **Novel** — no measured source anywhere in the task | 1,884 | 18.1 | 254 (27.1%) |

### 0.6 Color logic

New colors introduced in ≥1 pair: 279 tasks (29.7%). Colors
removed: 332 (35.4%). Background (modal color) changes in ≥1 pair:
291 (31.0%); consistent across all pairs: 138 (14.7%). A consistent
global cellwise colormap exists for **0 tasks**; 13 tasks (1.4%) have
per-pair functional maps that disagree across pairs. Color logic in
this population is object-local (recolor fate) and
palette-changing, not a global map.

### 0.7 Global whole-grid relations (consistent across all pairs)

| Relation | Tasks | % |
|---|---|---|
| Output == input (identity) | 0 | 0.0 |
| Output == a dihedral image of input | 0 | 0.0 (any-pair: 10, 1.1%) |
| Output == plain a×b tiling of input / a dihedral image | 2 | 0.2 |
| Output == integer block scale of input | 0 | 0.0 (any-pair: 3, 0.3%) |
| Output == subgrid of input (crop) | 50 | 5.3 |
| Input == subgrid of output (embed) | 32 | 3.4 |

Whole-grid rules are a rounding error in this population. An
architecture organized around whole-grid transforms is organized
around ~0% of the tasks.

### 0.8 Split/merge candidates and joint structure

Split candidate (more objects, same non-background cell count):
66 tasks (7.0%). Merge candidate: 47 (5.0%). Union: 110 (11.7%).
Selected joint counts (tasks exhibiting both): creation ×
new-colors 222; size-change × background-change 189; size-change ×
deletion 225; creation × deletion only 139 (creation and deletion
are more often alternatives than companions: 383 creation-only,
294 deletion-only, 122 neither).

### 0.9 Coverage bounds (BOUND — necessary conditions only)

| Language | Full-fit reach, pool B | Reading |
|---|---|---|
| v1 (preserve/delete + dihedral + crop canvas) | **123/938 = 13.1%** | Upper bound: displacement consistency across pairs not checked |
| v2 grammar (derivation kinds + mirror/ring + split/merge allowance) | **654/938 = 69.7%** | Upper bound: exact cover never solved |
| v2 strict (no split/merge allowance) | 609/938 = 64.9% | |
| v2-only beyond v1 | 531 tasks | The grammar extension's measured gain |
| Neither bound reached | 284 tasks = **30.3%** | Outside even the v2 grammar's necessary conditions |

For calibration: v1's *measured* full-fit coverage on its drawn
sample was 2/48 = 4.2%, below the 13.1% bound, exactly as a bound
must be. And v1's measured solves were 0 — fit-reach is a ceiling
on solves, never an estimate of them.

### 0.10 Ambiguity substrates (the identifiability measurements)

| Substrate | Value | Meaning |
|---|---|---|
| All train inputs one shape | 399 tasks (42.5%) | Canvas functions agree on one shape: underdetermined beyond named candidates |
| ≥2 distinct train input shapes | 539 (57.5%) | Canvas functions partially discriminable |
| Duplicate input feature classes in ≥1 pair | 682 (72.7%) | Correspondence role-swap ambiguity substrate is the norm |
| 2-pair tasks | 146 (15.6%) | Minimal constraint mass; weakest certification |
| LOO fully determinate (every held pair's output signatures seen in other pairs' inputs) | 154/938 (16.4%) | Within-task held-out prediction usually faces unseen classes |
| Mean per-held-pair determinate fraction | 0.273 | Same, per held pair |
| Identical input grids with different outputs | 0 | Population is functionally consistent on train pairs |

### 0.11 Eval-120 appendix (census only — scoring-contaminated, never a yardstick)

Same size 67.5%, shrink 22.5%, grow 2.5%, mixed 7.5%.
Created-any 55.0%, deleted-any 61.7%, grown fate 58.3% (vs 38.3%
in B — the eval population leans *more* transformational),
v1 bound 10.0%, v2 necessary bound 65.8%, same-shape 38.3%,
duplicate classes 86.7% (vs 72.7%), LOO fully determinate 4.2%
(vs 16.4%), 2-pair tasks 28.3% (vs 15.6%). **Every ambiguity axis
is worse in the eval sample than in the training sample.**
Transfer from pool-B measurements to the private eval is
optimism-ward, not neutral; §7 states this plainly.

---

## 1. Identification-completeness: the formal statement

### 1.1 Definitions

A task `t` is a set of train pairs `P = {(x_i, y_i)}_{i=1..k}` and
test inputs `X*` with true outputs generated by a rule `r*`
(`y_i = r*(x_i)` on train, `r*` applied to `X*` is what is scored).
A rule language `L` is a set of rules. An identification procedure
`A` maps a train set to a rule in `L` or abstains (`⊥`).

- **Fit-complete for t (relative to L):** some `r ∈ L` fits all of `P`.
- **Identification-complete for a class C (relative to L):** for every
  `t ∈ C` whose true rule `r* ∈ L`, `A(P)` returns `r` with `r ≡ r*`
  on `X*` (test-equivalence, the scoring criterion — full
  rule-equality is stronger than necessary and is not required).
- **Certified-identification-complete:** identification-complete
  **and** `A` abstains whenever it cannot certify test-equivalence
  from `P` alone. Certification is what separates a solver from a
  guesser: an uncertified correct guess and a wrong guess score the
  same on one task but only the certified procedure compounds.

Fit-completeness is strictly weaker than identification-completeness:
a class can be fully fittable while every procedure fails to identify
which fitting rule is the true one. The census measures fit-reach
bounds (§0.9); the derivation's job is to design identification on
top of them, and §7 keeps the two apart.

### 1.2 Where identifiability provably fails regardless of mechanism

These are information-theoretic, not engineering, limits. No
mechanism — no matter how clever — identifies the true rule from
pairs that do not discriminate it.

**(F1) Sample ambiguity.** If two rules `r1 ≠ r2` in `L` both fit
all `k` train pairs but differ on some test input, no procedure
using only `P` can guarantee identification. The census sizes the
substrates on which this failure *lives* (it does not prove any
particular task is ambiguous — that requires knowing the true rule):

- **Canvas ambiguity:** on the 399 tasks (42.5%) whose train inputs
  share one shape, infinitely many canvas functions agree on the
  observed shapes (e.g. "output = input + (2,0)" vs "output = 2·input
  − (h,0)" on a single shape). A named candidate set (dihedral ∘
  scale, crop, pad rules) *chooses* among them; it does not identify
  them. Only the 539 tasks (57.5%) with ≥2 distinct input shapes
  offer any discrimination, and only if the shapes differ in the
  dimension the canvas function acts on.
- **Role-swap ambiguity:** on the 682 tasks (72.7%) containing a
  duplicate input feature class (two input objects with the same
  shape+colors in one pair), symmetric assignments can swap roles
  between the two objects while fitting every pair. If the test input
  breaks the symmetry, the swapped rule predicts wrong. Pair evidence
  cannot break a true symmetry; only a test input that does — which
  is exactly what is scored, not what is given.
- **Small-k ambiguity:** 146 tasks (15.6%) have k=2. Two pairs
  constrain a rule language weakly by any counting argument; the
  number of rules in any expressive `L` fitting two pairs is large,
  and LOO certification degenerates (re-induction from one pair).

**(F2) Free creation.** If the true rule emits output content that is
not a function of the input and of parameters identifiable from the
pairs, the content is unidentifiable from pairs in which it appears
only as output. The census measures the substrate: **1,884 created
objects (18.1% of all created objects) in 254 tasks (27.1%) have no
measured source anywhere in their task** — not in the same pair's
input, not in any other pair's input, and not a ring. Absent a
parameter semantics (a numeral, bar, or count in the input that
addresses the content), those objects' content cannot be identified
by any correspondence mechanism. Note the asymmetry: a novel
creation that *repeats identically* across pairs is still not
identified in its role — the mechanism can copy it, but cannot know
*why* that content rather than any other, and a test input that
changes the addressed parameter (if one exists) breaks the copy.

**(F3) Segmentation relativity.** Objecthood is not in the data.
The two segmentations measured differ by ~3x on object count
(means 14.5 vs 4.6 objects per pair). An object-level identification
is conditional on a segmentation hypothesis, and train pairs can
fail to discriminate two segmentations that differ on the test
input (e.g. whether two touching color regions are one object or
two). No object-level mechanism is identification-complete
unconditionally; it is complete only relative to a segmentation
that the pairs themselves must confirm.

**(F4) Language relativity.** Completeness is only ever relative to
a language `L`. The census bounds prove the point for two concrete
languages: v1's fit-reach bound is 13.1%, v2's is 69.7%, and 30.3% of
the population is outside both. No fixed finite grammar escapes
this argument — the residual is always measured, never assumed
away. The honest target is measured coverage growth with named
residuals, not a claim of closure.

### 1.3 What "identification-complete for this population" would require

A language + procedure pair `(L, A)` is identification-complete for
pool B (to the extent the census can certify) iff, for each census
class in §2's accountability table:

1. **Fit:** `L` contains a rule fitting the task's train pairs
   (the census bounds are the fit evidence, class by class);
2. **Discrimination:** for tasks in the class, the pairs
   discriminate the true rule from every other fitting rule in `L`
   up to test-equivalence — or `A` abstains exactly on the tasks
   where they do not (certified completeness, §1.1);
3. **Certification:** `A`'s acceptance test (LOO re-induction plus
   the strengthenings in §3.3) passes exactly the identified rules
   and rejects the rest, at the rates the census substrates predict.

The census already falsifies the strongest version of this claim
for the v1/v2 family: a fit-reach bound of 69.7% caps
identification-completeness for pool B at 69.7% for that family,
*before* certification losses, *before* search failures, and
*before* population transfer to the eval. The architecture in §2–§3
is therefore designed around two questions the census forces: (a)
what components must be added to raise fit-reach above the 90%
criterion's requirement, and (b) what identification procedure
converts fit into certified solves at a rate the probe can measure.

---

## 2. The architecture, derived from the census

Design rule for everything below: each component exists because a
measured census class demands it, and the component's coverage claim
is the census size of the class it answers. Components are labeled
(C) core (carried from validated machinery), (N) new in this
derivation, or (O) open — named, sized, mechanism not yet supplied.

### 2.1 Representation (M1): the scene is two-level, and segmentation is a variable

**(C) Object scene graph.** Objects with pattern, origin, colors,
size, dihedral-canonical signature — as in v1/v2 correspondence
machinery. Justified by: preserved objects in 77.9% of tasks and
22,392 preserved instances against 10,405 created ones — the
correspondence core of the population is real and large.

**(C) Derivation records.** A rule is a set of derivation bindings
(source class → derivation value), a canvas function, and a
background/palette component — v2's schema tuple, retained.

**(N) Segmentation as a searched variable.** The identification
procedure runs the object analysis under BOTH measured
segmentations (primary per-color 4-connected; agnostic 8-connected)
and over the background choice each implies, and a schema is valid
only if ONE segmentation account is consistent across all pairs.
Reason: F3 (§1.2) is measured (14.5 vs 4.6 objects/pair), and every
prior lane fixed the segmentation a priori, which silently selected
which tasks were even visible to it. Segmentation becomes part of
what intersection decides, like every other parameter.

**(N) Field layer.** Alongside the object graph, the representation
carries a *field* description of the grid: periodicity vectors (the
smallest translation(s) under which the non-background pattern
repeats), symmetry group of the pattern (reflections/rotations
about which the pattern is completed or closed), and anchor
structures (lines/rows/columns that span the grid). Reason: the
single largest unexplained mass in the census is created objects
(10,405 instances, 55.7% of tasks) and the patterned-tiling example
is diagnostic — plain tiling is 0.2% of tasks, so the created mass
is not plain tiling; it is pattern *extension* (periodic fields
continued, symmetry completions, repeated motifs with per-repeat
transforms), which is invisible to per-object correspondence
because the repeated unit is a field property, not an object.
v1 has no such layer; v2 has none (its creation is copy/frame only).
The field layer is where derivations may source content that no
single object correspondence explains.

### 2.2 Derivation grammar (M2): what a derivation may be

The grammar extends v2's kinds with the field layer's constructors.
Each kind's population warrant is the census class that demands it
(§3 table):

- **preserve / recolor / delete** (C) — v1's actions; 77.9% /
  33.9% / 46.2% of tasks.
- **scale-object, grow (ring / holes / bbox-fill), shrink,
  reshape-by-containment, mirror-complete** (C) — v2's transformational
  kinds; grown fate 38.3%, shrunk 26.3%, scaled 9.4% of tasks.
- **split (by color, by separator), merge (≤3 parts, exact tiling)**
  (C) — split/merge candidates 11.7% of tasks.
- **copy, same-pair** (C) — 6,697 instances, 35.6% of tasks.
- **copy, cross-pair** (N) — the template is an object from another
  train pair of the same task, transported into this pair under the
  derivation the template's class takes there. Warrant: 385
  instances in 117 tasks (12.5%) whose created content exists only
  in other pairs' inputs. v2's copy is same-pair only; a same-pair
  mechanism has no way to express this class.
- **frame / ring** (C) — 1,439 instances, 22.7% of tasks.
- **field-extend** (N) — the output field is the input field's
  periodic continuation (or its dihedral-folded continuation) onto
  a larger canvas, or the input field is a window of the output
  field. Parameters: periodicity vector(s), per-repeat transform,
  canvas. Warrant: the correspondence-invisible creation mass
  (55.7% of tasks contain creation; plain tiling accounts for
  0.2%), plus crop/embed relations (11.1%) as its inverse view.
- **symmetry-complete** (N) — output = input ∪ its image(s) under a
  reflection/rotation of the canvas or of an anchor, with colors
  carried. Warrant: overlaps mirror (object level) at the field
  level; sized jointly with field-extend by the residual in §3,
  not separately measurable by this census (labeled: PROXY — the
  census's symmetry fields show output symmetry arising where input
  symmetry does not in the pair records; the exact task share is a
  residual, not a direct count).
- **parameter-addressed creation** (O) — content determined by a
  measured parameter object (count, bar length, numeral-like
  pattern). Warrant: the novel-creation class, 1,884 instances,
  254 tasks (27.1%). The component is *named and routed* by this
  architecture (tasks whose covering derivation is parameter-
  addressed are identified as such and abstained on), but its
  semantics is NOT designed here. This is the architecture's
  largest honest hole, sized rather than hidden (§7).
- **counting / arithmetic derivations** (O) — repeat-N, sort-by-size,
  length-N drawing. Same disposition: named, routed to abstention,
  sized only as part of the neither-bound residual (30.3%) plus
  whatever part hides inside fates this census reads as grow/copy.
  Not separately measurable by this census (labeled).

### 2.3 Canvas (M3): delta-functions, and the two populations of tasks

- **Named candidates** (C): dihedral ∘ integer grid scale, crop to
  content bounding box, pad under a named anchoring rule — v2's set,
  retained for the single-shape population (399 tasks, 42.5%),
  where nothing more is identifiable (F1). Schemas from this
  population carry a `canvas_ambiguous` flag permanently: their
  certification can never exceed what one shape supports.
- **Delta-functions** (N): on the 539 tasks (57.5%) with ≥2 distinct
  input shapes, canvas is identified as a function fitted across
  shapes: candidate family = {identity, constant delta (dh, dw),
  per-dimension ratio, crop-to-content, pad-to-multiple,
  content-bbox + constant margin} — admitted only if it reproduces
  every pair's shape relation exactly, and discriminated by the
  shape diversity itself (each additional distinct shape kills the
  functions that agree on one shape and differ on another, which is
  the only canvas discrimination the data offers).
- **Non-integer deltas are the default case,** per §0.2: 62.9% of
  size-changing pairs. Any canvas machinery that begins with
  integer scaling is fitted to the minority (v2's G tries scale
  first; the census says delta/crop/pad fits first).

### 2.4 Palette (M4): object-local, with a background component

- **Per-derivation functional color maps** (C) — recolor fate in
  33.9% of tasks; maps live on derivations, not the grid (global
  consistent colormap: 0 tasks).
- **Palette introduction** (C/N): derivations may introduce colors
  absent from the input when the color is *identified* — carried by
  a copy/frame/field source, or constant across all pairs'
  corresponding derivations. Warrant: new colors in 29.7% of tasks;
  colors removed in 35.4% (deletion of color classes is a
  derivation-level event, handled by class bindings).
- **Background map** (C): modal-color mapping, consistency-checked
  (background changes in 31.0% of tasks in ≥1 pair, 14.7% in all
  pairs). Background is part of the schema, and segmentation (M1)
  is run *after* the background hypothesis, since the modal color
  is what defines objects.

## 3. Identification and certification

### 3.1 Procedure (M5): cover, intersect, certify — over both segmentations

1. **Per-pair candidate generation (measured facts only).** For
   each pair and each segmentation, compute every derivation in
   the §2.2 grammar under which some input content could produce
   each output object or field region. A candidate is a concrete
   geometric fact about the pair (patterns equal after the stated
   transform; cells exactly the dilation ring; output field exactly
   the periodic continuation; …). No candidate enters from a prior,
   a corpus, or a distribution.
2. **Exact cover per pair.** An assignment accounts for every
   output object/field region exactly once and consumes every
   input object exactly once (derivation, joint split, joint
   merge, deletion). Enumerated by backtracking, fewest-candidates
   first; a cap hit is reported as `search_cap`, never as
   inconsistency (v2's discipline, retained).
3. **Cross-pair intersection.** Bindings (key → derivation value)
   must agree across all pairs and across the ONE chosen
   segmentation account; each pair can only shrink the surviving
   schema set. Canvas and palette components intersect the same way.
4. **Reconstruction.** Surviving schemas must re-render every train
   output exactly (catches placement collisions and canvas/field
   interactions per-object facts cannot see).
5. **Certification** (§3.3). Only certified schemas emit
   predictions; ≥2 certified schemas that disagree on a test input
   → abstain (`ambiguous`), never a coin flip.

### 3.2 What the census changes about the procedure, mechanically

- **Segmentation is decided by intersection,** not fixed (M1, F3).
- **Field derivations compete in the same cover** as object
  derivations: a created object explained by field-extend is not
  marked creation_unexplained; the taxonomy (§6.5) reports which
  layer carried each object, so the probe measures the field layer's
  contribution separately instead of letting it hide inside a
  solve count.
- **Cross-pair copy is a derivation source,** with the template's
  own derivation in its home pair required to be identified first
  (templates are not free parameters; they are bindings).
- **Canvas candidates are ordered delta-first** (M3), reversing
  v2's scale-first order on census evidence (62.9% non-integer).
- **Parameter-addressed and counting classes are routed to
  abstention by construction,** so their measured size in probe
  taxonomies is the size of the open hole — the probe cannot
  silently convert them into search failures.

### 3.3 Certification (M6): LOO plus the two strengthenings the census forces

**(C) LOO re-induction** — the v1-validated component, unchanged in
form: for every held pair j, re-induce the schema from the other
pairs alone and require an exact prediction of pair j. Measured
basis: caught 2/2 full-fit schemas that failed to generalize in
v1's run, on top of passing both synthetic controls. 2-pair tasks
fall back to full fit + test determinacy (v1/v2 form).

**(N) Shape-diverse certification.** On tasks with ≥2 distinct
input shapes (539, 57.5%), the LOO suite must include at least one
hold-out in which the held pair's input *shape* is absent from the
induction pairs (when the shape distribution allows). Reason: F1's
canvas ambiguity is invisible to same-shape LOO (re-induction sees
the same shape evidence minus one pair — v2's §5.1 names this
hole); holding out a shape is the only within-task test that
discriminates canvas functions.

**(N) Determinacy reporting.** Every certification records the
task's output-signature determinacy profile (the census substrate:
pool mean per-held-pair determinate fraction 0.273; fully
determinate tasks 16.4%). A certified schema on a low-determinacy
task is leaning on *generalized actions* (a derivation kind applied
to a class never seen held-out), which is legitimate — that is
what rules are — but the probe must report the determinacy
distribution of its solves so that certified-on-seen-classes and
certified-by-generalization are never blended into one number.

## 3.4 Class-by-class accountability (the census, answered)

| Census class (% of 938) | Component | How identification works | Expected failure mode |
|---|---|---|---|
| Preserved objects (77.9%) | M5 cover, preserve derivations | Colored-signature matching + intersection; displacement constant per binding | Role-swap ambiguity (F1) on duplicate classes (72.7% substrate) |
| Deletion (46.2%) | M5 cover (deletion as consumption) | Class deleted in every pair it appears in; intersection kills mixed fates | Class deleted in train, present-but-transformed in test → abstain/wrong |
| Recolor (33.9%) | M4 per-derivation maps | Functional cellwise map under an aligning transform; map must be identical across pairs | Map conflicts across pairs → intersection death (`inconsistent_phi`) |
| Grown / shrunk (38.3% / 26.3%) | grow/shrink derivations (containment + fill rule) | Containment is a measured fact; the fill rule (ring/holes/bbox + fill color) must re-measure identically in every pair | Partial containment that is actually drawing (lines) → cover fails honestly |
| Scaled objects (9.4%) | scale derivations | Block-scale signature relation, k ∈ {2,3}, either direction, unanimity for downscale | Non-uniform scaling (stretch in one axis) — outside grammar → no-fit |
| Split / merge candidates (11.7%) | split_color / split_sep / merge derivations | Exact partition / exact tiling facts per pair; parts keyed, jointly consumed | Partition ambiguity when parts are interchangeable (F1) → `ambiguous` |
| Creation = copy, same pair (35.6% of tasks; 64.4% of created instances) | copy derivations | Created pattern is a dihedral image of a present class's pattern; template binding intersects like any other | Template class transformed in test pair differently → mispredict |
| Creation = ring/frame (22.7%) | frame derivations | Ring geometry definitional from canvas/anchor bbox + margin + color | Ring around a relational anchor ("around the largest object") — placement is relational → `delta_nonconstant` class |
| Creation = copy, cross-pair (12.5%) | cross-pair copy (N) | Template identified in its home pair first; transported under its binding | Template's home-pair derivation itself ambiguous → propagates |
| Creation = novel (27.1%) | **(O) parameter-addressed creation** | NOT identified by this architecture; routed to abstention | This IS the failure mode — content with no measured source (F2) |
| Field extension / symmetry completion (residual; plain tiling 0.2%, crop/embed 11.1% measured adjacent) | field-extend, symmetry-complete (N) | Periodicity/symmetry are measured facts of the pair; continuation must reproduce every pair's output field exactly | Aperiodic drawing that *looks* periodic on k pairs → LOO is the only guard |
| Size change: non-integer delta (167 tasks pure; 62.9% of changing pairs) | M3 delta-functions / crop / pad | Shape relations fitted across distinct shapes; crop = content-bbox fact; pad = exact embedding + named anchoring | Single-shape tasks (42.5%): canvas underdetermined (F1) → `canvas_ambiguous` flag, LOO-blind spot |
| Size change: integer scaling (88 tasks pure integer) | grid scale in canvas candidates | Shape arithmetic kills all but one (scale, dihedral) combination | ÷k without block unanimity → not a scale → falls to delta class |
| Background change (31.0% any-pair) | M4 background map | Modal-color mapping consistency-checked across pairs; segmentation re-run under it | Background = an input foreground color (swap) → segmentation flips; both accounts searched |
| Global colormap (0% consistent) | — (deliberately absent) | No component: the census says this class does not exist in the population | None — absence is the census-derived choice |
| Counting / arithmetic (unmeasured residual) | **(O)** | NOT identified; routed to abstention | Inside the 30.3% neither-bound mass; sized only as residual |
| Relational placement (unmeasured residual) | — (δ is constant per binding, C) | Not identified; dies at intersection as `delta_nonconstant` | Named successor problem since v2; census cannot size it |

## 4. What is genuinely new — mechanically, against every dead lane

| Dead lane | Its mechanism | This architecture's mechanical difference |
|---|---|---|
| DSL enumeration | Search a fixed operator algebra over whole grids; accept on train fit | No algebra search: candidates are measured per-pair facts; acceptance is LOO re-induction, not fit. (The DSL executor survives only as a rendering/checking substrate, as in v1/v2.) |
| Retrieval / analogy transplant | Transfer a whole stored program to a new task (median cell agreement 0.776, 0 solves) | No cross-task transfer at all. The only cross-*pair* transfer is cross-pair copy, where the template is inside the same task and its own derivation must be identified first — transfer of an *identified binding*, not of a stored program |
| Library growth (478 → 39,065) | Grow the prior; eval delta exactly zero | There is no prior to grow. The hypothesis space is generated from the task's own pairs under BOTH segmentations |
| LLM zero/few-shot (P2/P3) | Sample rules from a language prior; 0 exact fits in every conditioning tried | No sampling step exists. Every parameter of a schema is read off a measured correspondence and must re-measure identically in every pair |
| TRM / gradient TTT | Fit a continuous relaxation by gradient descent; acceptance = train fit (196 fits → 0 solves); CUDA run poisoned at step 0 | No gradient anywhere. Fit is constructed by exact cover + intersection; the acceptance test is held-out prediction inside the task, which memorization cannot pass by construction |
| nextgen v1 (correspondence schema) | Objects preserved (dihedral+recolor) or deleted; same-shape/crop canvas; fixed modal segmentation; LOO gate | Grammar admits transformation (grow/scale/split/merge), creation (copy/frame), and size change as derivations; canvas is delta-first; measured kill: 0/48, coverage 4.2% on the draw vs census bound 13.1% for its language |
| nextgen v2 (derivation grammar) | v1 + transformational derivations, copy/frame creation, grid-scale-first canvas, fixed segmentation, LOO gate | (i) Segmentation is searched and decided by intersection (v2 fixes it); (ii) a FIELD layer — periodic extension and symmetry completion as derivation sources (v2 creation is copy/frame only; the census's created mass is mostly not copies: only 64.4% of created instances are same-pair copies, and field structure is the named source for the patterned remainder); (iii) cross-pair copy (v2: same-pair only; class = 12.5% of tasks); (iv) canvas identified as delta-functions fitted across distinct shapes with shape-diverse certification (v2: named candidates on shapes, scale-first, and its own §5.1 concedes the single-shape LOO blind spot); (v) parameter-addressed creation and counting are routed to labeled abstention so the probe taxonomy measures the open hole instead of dissolving it into generic no-fit |

---

## 5. Exceptionality gate (computational_research_hpc skill)

1. **Conventional approach / why insufficient:** two conventions
   exist and both are measured dead on this population. Propose-
   and-check over a prior (enumeration, retrieval, LLM sampling,
   gradient TTT): 0 fresh-task solves across five priors. And
   correspondence induction over a fixed segmentation with a
   preserve-or-delete language (v1): 0/48, killed by transformation
   and size change that a pre-build census would have sized at
   38.3%/31.9% of the population. The insufficiency is not argued;
   it is tabulated in §0.
2. **New mechanism:** identification by constraint intersection
   over a derivation grammar that includes (a) segmentation as a
   searched variable decided by the same intersection, (b) a field
   layer (periodic extension, symmetry completion) as a derivation
   source competing inside the same exact cover as object
   derivations, and (c) cross-pair copy with identified templates.
   None of the three exists in any dead lane, including v2.
3. **Verification strength above norm:** the census itself is the
   above-norm step — the language was derived from a full-population
   measurement with reproducible data files, so the build's
   coverage expectations are pre-computed (§0.9 bounds and §6's
   gates reference them). Certification = LOO re-induction
   (validated on v1's run) + shape-diverse hold-out + determinacy
   reporting + ambiguity abstention. Probe gates pre-registered
   in §6 before any code exists.
4. **Cheapest decisive falsifier:** the §6 probe — one CPU draw,
   60 tasks, $0. F2 (0 certified solves) kills the architecture at
   probe strength, and the coverage gate (F1) wounds it even if it
   solves, because §0.9 gives this derivation's language a
   computable reach expectation to be measured against.
5. **Independent path that could prove it wrong:** the unmodified
   gauntlet on a B/C-fresh draw; pool C as algebra-shadow detector
   (solves on C with zero A+B solves = the lane learned the
   substrate's algebra, again); the negative control (shuffled
   outputs must yield no certified schema); the census itself,
   re-run against any future pool, as the standing check that the
   population claims in §0 were true.
6. **Compounding asset:** regardless of the probe verdict, the
   census stands — a full-population, per-task, reproducible map
   of what ARC-AGI-2's fresh training population contains, which
   every successor design (and every honest coverage claim) starts
   from. Add to it: the derived grammar's class-accountability
   table, and the probe taxonomies in census-class terms.
7. **Obligation closed if it succeeds:** the campaign's central
   open obligation — any nonzero, certified conversion on fresh
   real ARC tasks — closes, over a language whose fit-reach bound
   (recomputed for this grammar before the build, §6.2) is the
   first one in the campaign that is not arithmetically refuted by
   the 90% criterion on its face. It does not close the criterion
   itself; §7 states the remaining distance exactly.

## 6. Pre-registered probe gates for the eventual build (designed now, fired later)

These gates bind the build that follows this derivation. They are
written before the build exists and are not amendable after its
first run.

### 6.1 Protocol

- **Instrument:** `gauntlet.py`, unmodified. Budget 25 s/task.
- **Draw:** A:12, B:36, C:12, single draw. **Seed rule (fixed
  now):** the smallest seed ≥ 20261110 whose B-draw and C-draw are
  both disjoint from the draws of seeds 20261103 (DSL baseline),
  20261104 (v1), and 20261109 (v2), verified by replicating the
  gauntlet's sampling procedure offline *before the lane is run*.
  Pool A has only 18 tasks; A-overlap with earlier draws is
  unavoidable and is reported with the drawn ids.
- **Confirmation draw (pre-committed):** if and only if the primary
  draw returns ALIVE, a second draw B:96 on the next seed
  satisfying the same disjointness rule runs before any scale
  claim, any grammar extension, or any change of budget.
- **Accounting:** the lane reads train pairs and test *inputs*
  only; test outputs are stripped on entry by construction.
  `fits=1` is reported to the gauntlet only for certified schemas.
  Abstentions land in no-fit with their sub-reason recorded.

### 6.2 Coverage expectation (computed before the build)

Before the probe, the build must recompute this derivation's
grammar's necessary-condition coverage on pool B with the census
tool extended to the new derivation kinds (field-extend,
symmetry-complete, cross-pair copy, dual segmentation). That
number — call it the grammar's census bound — is recorded in the
build's design note *before* the probe runs. (For reference, the
v2 grammar's bound measured here is 69.7%; the derived grammar's
bound must exceed it by construction or the derivation has failed
on paper and the build does not start.)

### 6.3 Controls (all must pass before the run counts)

1. Positive, object layer: a synthetic transformational task
   (split-by-color + grow) solved and certified.
2. Positive, field layer: a synthetic periodic-extension task
   (pattern continues onto a larger canvas) solved and certified.
3. Positive, cross-pair copy: a synthetic task whose created
   object exists only in another pair's input, solved and certified.
4. Abstention control: a synthetic task with a novel creation
   (content with no source) must produce NO certified schema —
   the correct behavior is abstention, and a "solve" here fails
   the control set.
5. Negative control: control 1's inputs with train outputs
   shuffled across pairs → no certified schema, no solve.

### 6.4 Gates on A+B (n=48)

- **KILL:** 0 certified solves → the architecture is dead at probe
  strength. No iteration without a new measured idea.
- **WEAK-ALIVE:** 1–3 certified solves → the identification loop
  fires on real fresh tasks over the derived grammar. Earns
  exactly one iteration, aimed at the §6.5 taxonomy's largest
  class. No scale.
- **ALIVE:** ≥4/48 certified solves (≈8.3%) **and** full-fit
  coverage on A+B ≥ 30% **and** neither override below triggers →
  the confirmation draw (§6.1) runs.
- **F1 (reach) override:** full-fit coverage < 15% on A+B caps the
  verdict at WEAK-ALIVE regardless of solves (the grammar still
  does not reach the population; cf. v1's 4.2%, v2's 69.7% census
  bound).
- **F5 (over-generation) override:** ≥half of full-fit schemas
  LOO-rejected caps the verdict at WEAK-ALIVE (certification
  doing all the work means the language fits by construction).
- **F4 (algebra shadow):** solves on pool C with zero A+B solves
  = KILL, reported as the algebra-shadow finding.
- **F3 (degeneracy):** ≥half of solves from a single derivation
  kind that is a lookup (colormap-only class) caps at WEAK-ALIVE.

### 6.5 Taxonomy the probe must report

Every non-solved A+B task gets exactly one sub-reason, and the
results file must ALSO tabulate the draw in this document's census
classes (size class; fates present; creation split by source;
determinacy profile of solves vs non-solves), so probe outcomes
are directly comparable to §0's population tables. Sub-reasons:
`canvas_ambiguous`, `canvas`, `creation_novel` (the open hole,
measured), `creation_unexplained` (non-novel but ungrammatical),
`cover_failed`, `inconsistent_<field>` (phi / tau / delta / param
/ segmentation), `search_cap`, `loo_rejected`,
`shape_loo_rejected` (the new certification's own kill count,
reported separately — it is the price of the canvas strengthening
and must be visible), `ambiguous`,
`nondeterminate_test_class`.

## 7. Honest distance statement — what this derivation does NOT establish

1. **A census-complete language is not an identification
   procedure.** §0.9's bounds are *necessary-condition* bounds:
   they count tasks not yet refuted, under greedy staged matching,
   with exact cover never solved. The v2 grammar's true fit-reach
   is ≤ 69.7%, possibly far below. Nothing in the census measures
   search tractability: exact cover is worst-case exponential, and
   whether the derived grammar's covers are decidable inside
   25 s/task on the hard tail is an empirical question only the
   build's probe answers. The census removed *one* failure mode —
   designing a language blind to the population. It did not remove
   search, certification loss, or ambiguity.
2. **The arithmetic against the requirement is stark, and is the
   derivation's most important honest output.** The v2 family's
   fit-reach bound on pool B is 69.7% — below the 90% acceptance
   criterion. Even *perfect* identification inside that family
   cannot reach 216/240 on a pool-B-like population, because
   solves ≤ fits ≤ bound. The derived architecture's new
   components (field layer, cross-pair copy, dual segmentation)
   exist precisely to raise the bound, and §6.2 forces their bound
   to be computed before the build. But the classes they must
   additionally capture — parameter-addressed creation (27.1% of
   tasks contain novel creation), counting/arithmetic, relational
   placement — are at this writing **named and sized, not solved**.
   The distance between "language covers the census" and "solver
   identifies rules at 90%" contains at least one mechanism that
   does not yet exist on paper: a semantics for parameter objects.
3. **Certification loss is real and runs the other way.** v1's
   only two full fits were both LOO-rejected: its solve rate (0)
   was strictly below its fit rate (4.2% of the draw). A stronger
   language fits more and therefore presents certification with
   more spurious fits; the F5 override exists because the
   over-generation failure mode grows with the grammar. The census
   substrate (fully determinate tasks: 16.4%) says certification
   will usually be judging rules whose classes were never seen
   held-out — the honest expectation is that certified conversion
   lands well below whatever fit-reach the build measures.
4. **The population measured is not the population scored.** Pool
   B is ARC-AGI-2 *training* data with a disclosure attached
   (miners attempted all of it during DSL development). The
   private eval is a different, hidden draw, and the only eval
   sample available (eval-120, census appendix §0.11) is *harder
   on every ambiguity axis* — more transformation, more duplicate
   classes, fewer determinate tasks, more 2-pair tasks. Any number
   in this document transferred to the private eval without that
   discount is an error this document explicitly refuses to make.
5. **Segmentation-relativity is inherited, not cured.** Searching
   two segmentations (M1) reduces F3; it does not eliminate it —
   the true segmentation hypothesis space is larger than two
   entries, and pairs may not discriminate the searched set on
   test inputs. Object-level completeness claims in §1.3 are
   relative to the segmentation account the pairs confirm.
6. **What the census cannot see, it did not size.** Relational
   placement, counting/arithmetic, selection among equals by a
   global criterion, and line-drawing as such have no direct
   census instrument; they appear only inside residuals (the
   30.3% neither-bound mass; parts of the grown/novel classes).
   A successor census with instruments for those classes is the
   named follow-up measurement — before, not after, any design
   that claims to cover them.

---

## Appendix A. Reproduction

- Census: `cd ~/workspace/arc_apex2/census && python3 census.py`
  (~3 min, pure stdlib, $0) → `per_task.jsonl`,
  `per_task_eval120.jsonl`, `summary.json`.
- Creation split: `python3 census_creation.py` (~3 min) →
  `creation_split.json`.
- Definitions: `census/README.md` (including the one repaired
  table — fate presence at count 0 — and its fix).
- Failure record quoted: `PROBE_LEDGER.jsonl`;
  `NEXTGEN_SOLVER_DESIGN_2026-11-04.md` (§6 = v1 probe verdict);
  `NEXTGEN_PROBE_RESULTS_2026-11-04.md`; `gauntlet/REPORT.md`;
  `NEXTGEN_V2_DESIGN_2026-11-04.md` (design + gates; its probe
  result was not in the record at the time of writing).
