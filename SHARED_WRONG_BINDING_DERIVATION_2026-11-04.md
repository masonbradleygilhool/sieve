# SIEVE — Shared-Wrong-Binding Derivation (2026-11-04)

**Commission:** paper only. No solver code, no probe. The
survivor-set census (`SURVIVOR_SET_CENSUS_2026-11-04.md`) moved
this program's binding constraint to version-space *content*:
of the 9 unanimous version spaces among the 28 spent fits, 8 are
unanimously **wrong** — the survivor sets that speak with one
voice are usually wrong together. This derivation starts from
the wrong bindings themselves as data and answers: why does
this grammar's schema space systematically contain a wrong rule
that fits every train pair, and what representation change
would make the true rule the consistent one?

**Method note.** The census measured unanimity *within the
winning frame* — the first (pre-transform × account) frame of
the frozen sweep whose cover verifies. A frame is part of the
hypothesis: the grammar's actual schema space is the union over
all frames. Three of this derivation's five commissioned
questions turn on that distinction, so the census's 9 unanimous
tasks (8 wrong + the 1 correct control, ad38a9d0) were re-run
under a characterization instrument
(`derived_solver/wrong_binding_anatomy.py`, analysis-only)
that, per task: sweeps **every** frame, records each verifying
frame's schema count and test renderings; re-runs every
train-verifying frame with the test pair added as a (k+1)-th
pair (**k+1 consistency** — a frame verifying there means the
grammar contains a schema consistent with all k+1 pairs, i.e.
the truth, or a rule extensionally equal to it on all available
data, is *in* the space); and diffs the winning frame's
unanimous grid against the true test output cell by cell, with
object-level attribution. Spent draws only; the sealed exam was
never read, run, or touched; $0. Cost ≈ 55 CPU-minutes,
disclosed in the Appendix — above the "light" sketch, because
full-frame sweeps over capped spaces are not light, and the
alternative was leaving the decisive tasks unmeasured.

**Verdict up front.** The shared-wrong phenomenon is **two
different diseases wearing one label**, split evenly over the
8 unanimous-wrong spaces:

- **Truth absent — 4 of 8** (d9fac9be, c909285e, caa06a1f,
  67b4a34d). No frame of the sweep renders the true test
  output, and k+1 consistency fails in **every** measured
  frame: the grammar contains *no* rule consistent with the
  train pairs and the test pair jointly. The discriminating
  structure is exercised in every train pair — the pairs are
  not silent — and the grammar has no key that binds it.
  Charge **(a)**, grammar defect, with the missing distinction
  named per task (§1.3, §2.1).
- **Truth present but unselected — 4 of 8** (ecaa0ec1,
  be03b35f, aabf363d, e45ef808). k+1 consistency verifies, and
  in two of the four some frame's schemas render the true test
  output through the predict path itself. The full-grammar
  version space contains the truth and the wrong answer side
  by side; the train pairs do not separate them, and the
  census's "unanimous" was an artifact of committing to the
  first verifying frame. Charge **(c)**, information — relative
  to this grammar's hypothesis space (§2.3).

Charge **(b)** (segmentation merges what the true rule
separates) has **no positive exhibit** among the 8; the
representation defect the record *does* exhibit is the dual —
the grammar *splits* what truth unifies (fates keyed by exact
colored pattern, §2.2). The derived consequence is therefore
shape **(iii)**, genuinely split (§3): the (a)-half names a
grammar commission whose content this document specifies and
whose ceiling it prices; the (c)-half is an information
ceiling that no grammar change and no identification procedure
crosses — only a prior the pairs do not supply can, and §4
states exactly what Friday's measurement would have to exhibit
to count as evidence that such a prior exists. §5 states the
strongest claim the record now supports about 216/240.

One correction is carried throughout, per the census: the
conversion derivation's fold-rejection attribution is
superseded. Of the 64 rejecting folds over the 19 fold-rejected
fits, **58 (90.6%) were (b) certification dynamics killing
correct parents** (17 of 19 tasks; 14/14 folds on the four
census-fully-witnessed tasks) and 6 were (c) fit quality
(2 tasks). As shares of the 27 fit deaths: dynamics 17/27 =
63%, fit quality 2/27 = 7%, the remaining 8/27 the
nondeterminate/canvas/budget deaths. Certification dynamics
were real and large; fixing them was Stage V's design goal;
the census showed the fix does not reach the criterion because
the surviving constraint is the version spaces' content. This
document is about that content.

---

## 1. The wrong-binding anatomy

### 1.1 The eight spaces, measured whole

All figures from `derived_solver/wrong_binding_rows.json` and
`derived_solver/wrong_binding_scoped.json` (the e45ef808
winning-frame battery; its full sweep exceeded the run's
budget and is recorded as scoped, §A.2). "Frames" = distinct
(pre-transform × account) frames of the frozen sweep whose
cover verifies on the train pairs.

| task | k | frames verify | union distinct test grids | truth rendered (predict path) | k+1 verifies | species |
|---|---|---|---|---|---|---|
| d9fac9be | 4 | 18 | 2 | **none** | 0/18 — all die at bg_rules | truth absent |
| c909285e | 3 | 3 | 1 | **none** | 0/3 | truth absent |
| caa06a1f | 3 | 8 | 8 | **none** | 0/8 — all die at bg_rules | truth absent |
| 67b4a34d | 3 | 45* | 1 | **none** | 0/45 — all die at bg_rules | truth absent |
| ecaa0ec1 | 4 | 4 | 4 | **1 frame (rot180\|x1, 64/64 schemas)** | 4/4 | truth present |
| be03b35f | 3 | 78 | 6 | **12 frames** | 76/78 | truth present |
| aabf363d | 2 | 26 | 13 | none | **26/26** | truth present (verify path) |
| e45ef808 | 2 | 1† | 1† | none† | **yes — 512/512 narrowed schemas render truth** | truth present (verify path) |
| ad38a9d0 (control) | 2 | 6 | 6 | 3 frames incl. winning | 3/6 | correct |

\* 67b4a34d's sweep was truncated at its 700 s task wall after
45 verifying frames; unreached frames are unmeasured, and its
charge carries that disclosure (§2.1). † e45ef808 scoped to the
winning frame: train-only space exhausted at 2,196 schemas by
the census's raised-cap re-run, all rendering the test input;
the k+1 run at the same frame verifies and every narrowed
schema renders the truth.

The control behaves as a control must: ad38a9d0's truth is
rendered by its winning frame and k+1 verifies — the
instrument finds truth where truth is reachable, so its
absence elsewhere is a measurement, not an instrument defect.

Three structural facts fall out of the table before any
per-task reading:

1. **Within-frame unanimity is not a grammar-level property.**
   Only c909285e and 67b4a34d are unanimous across every
   measured frame (union distinct = 1). The other six spaces
   are plural across frames — d9fac9be renders 2 distinct
   grids, aabf363d 13, be03b35f 6. The census's Stage-V
   question ("does the survivor set speak with one voice?")
   was asked of a *frame-committed* set; asked of the grammar,
   most of these spaces do not speak with one voice at all.
   This does not rescue them — §1.2 — but it relocates part of
   the phenomenon from "the space is wrong together" to "the
   commitment rule manufactures agreement."
2. **Where truth is absent, it is absent account-first.** In
   the truth-absent tasks d9fac9be, caa06a1f, and 67b4a34d,
   **71 of 71** k+1 attempts made (18 + 45 + 8) die at
   `bg_rules`: adding the test pair makes the background-rule
   family {const, gen, bgmap} unsatisfiable in every frame
   tried — no background function in the family extends to
   the test pair. (c909285e's 3 k+1 attempts die one level
   deeper, at the cover itself.) The account layer is where
   inexpressibility surfaces first (§2.1 reads this as
   symptom, not locus).
3. **The identity fixed point.** In 4 of the 8 spaces
   (aabf363d, c909285e, 67b4a34d, e45ef808) the shared test
   rendering is the **test input itself** — every schema in
   the space renders the input unchanged (16/16, 1/1, 68/68,
   2,196/2,196 schemas respectively at the winning frame).
   Two of these are genuine renderings (aabf363d's schemas
   preserve everything the test input presents; e45ef808's
   render normally and simply create nothing). Two carry a
   disclosure: predict3's frozen failure mode *returns the
   input* when a field schema's train phases do not collapse
   to one offset, and when a bgmap rule has no entry for the
   test input's background value — c909285e's "rendering" is
   proven to be the second artifact (its anatomy re-run hit
   the bgmap KeyError the predict path converts to an input
   return), and 67b4a34d's carries a field binding and is
   recorded as artifact-unresolved. A space that cannot render
   is not a space that agrees on a wrong answer; the census's
   label stands as a solve-relevant rate (a Stage-V solver
   converts none of these), but §2 charges them on the k+1
   evidence, not on the rendering.

### 1.2 Which keys bind wrong

Per task, the shared wrong component at the winning frame
(census rows for key widths; anatomy rows for the diff):

- **d9fac9be — no binding keys at all.** The schema is
  account-level machinery only: canvas `constshape (1,1)`,
  9 deletions (everything), and the background rule
  `bgmap {(0→8), (1→1), (2→2), (8→8)}` — a memorized map from
  the input's corner-generator value to the output cell. It
  predicts **8**; the truth is **4**. The diff is the whole
  output (1 of 1 cells, classified background). The true rule
  — the color at the center of the unique solid 3×3 block
  (train answers 1, 8, 8, 2 are each the odd color enclosed
  by a uniform block; the test's block is 111/141/111, center
  4) — agrees with the bgmap on all 4 train pairs and is a
  different function. There is no key in the grammar — no
  fate, witness, or parameter binding — whose value is the
  wrong one, because there is no key that *could* hold the
  right one: Π (parameter-semantics derivation §1.2) contains
  scene statistics and population scalars, and no addressed
  content of the form "the color enclosed by / at the center
  of a region."
- **c909285e — one key: `('field',)`.** The schema is a single
  field derivation (periodic continuation under a dihedral
  variant). The true rule is a **tile quotient**: inputs are
  large periodic tilings (26×26, 24×24, 28×28) and outputs
  (7×7, 7×7, 7×7; test 24×24 → 6×6) are the arrangement
  pattern of the tiling's tile classes — a two-level
  structure (tile grid × within-tile class) the flat object
  model does not have. The field kind reproduces the train
  outputs because those outputs are phase-consistent crops of
  the periodic structure; on the test input the schema cannot
  render at all (§1.1, fact 3).
- **caa06a1f — 3 `shrink` fate keys (realized width 8 each)
  inside a scaled frame.** The winning frame is id|x2; *no*
  x1 frame verifies — the task's block-structured patterns
  are only coverable at scaled granularity. All pairs are
  same-shape (train 6→6, 8→8, 11→11); the test input is
  18×18 and every one of the space's 512 schemas (enumeration
  completed, not capped) renders a **24×24** grid. The wrong
  component is the size behavior of whole-grid shrink
  bindings: fates are bound to exact whole-pattern signatures
  (the three keys' patterns span the full grid), so the
  size-parametric content of the rule — the same shrink at
  any size — is represented as per-size pattern bindings that
  agree at sizes {6, 8, 11} and diverge at 18, a size no
  train pair exercises.
- **67b4a34d — field + shrink + witness keys; the quotient is
  nowhere.** Every pair, train and test, is 16×16 → 4×4: a
  uniform ÷4 block quotient, exercised identically in all
  pairs. The frame family offers scales {x1, x2, x3, d2, d3}
  — no d4 — and no block-classification kind; the winning
  schema's rendering is the input (§1.1 fact 3, artifact
  unresolved), and k+1 dies at the background family in all
  45 reached frames before content is even reached.
- **ecaa0ec1 — `preserve`/`copy` bindings on rotation
  variants.** Winning-frame diff: **6 of 121 cells** — two
  1→8, two 8→1, one 0→4, one 4→0: a color-arrangement error
  inside one 10-cell object. The object's blind signature is
  exercised in train inputs and outputs; its *colored*
  signature appears in no train output. The grammar keys the
  object's four dihedral variants as four separate keys with
  independent bindings; the binding the test variant carries
  was filled by a candidate that fits the train rotations and
  misarranges this one. Under rot180|x1 the same task's space
  renders the truth with all 64 schemas.
- **be03b35f — a 2-cell swap in a 2×2 output.** Winning-frame
  diff is 2 of 4 cells (0→1, 1→0) under a `delta (−3,−3)`
  canvas. The test input's single object has a blind
  signature that appears in no train input. 78 frames verify;
  12 render the truth.
- **aabf363d — `preserve` bindings; the discriminating class
  is unexercised, full stop.** k=2. The diff is 16 of 49
  cells: a 15-cell object recolored 8→2 in the truth,
  preserved at 8 by every schema (the 16th cell is one 2→0).
  The object's blind signature appears in **no** train input
  and **no** train output — with two pairs, the pairs contain
  literally zero information about this class's fate, and the
  grammar's every consistent rule preserves it (the only fate
  the intersection supports for a class it has never seen
  transformed). All 4 binding keys at the winning frame are
  plural (realized width ≥ 2) yet all renderings coincide on
  the test input — the plurality lives entirely on keys the
  test input does not exercise.
- **e45ef808 — creation bindings that do not fire.** The
  diff is 14 cells, **all** in true-only objects: the truth
  creates two objects (9 cells painted 9, 5 cells painted 4)
  that every train-consistent schema omits. Both of the test
  input's object classes are novel at blind level. One
  created object's signature *was* exercised — it appears in
  train outputs, created there too — but its creation is
  keyed to trigger classes the test input presents only in
  novel form, so no consistent schema fires it here.

**Are the wrong bindings the same keys across tasks?** At key
level, no: the wrong components distribute over fate keys
(4 tasks), the field key (3), witness keys (2), the background
rule (1 operatively, 3 more as the k+1 failure surface), and
the canvas/frame layer (4). No key kind, and no single key,
is the systematic culprit. At the level one step up, the
pattern is exact, **8 of 8**:

> The shared wrong component is never a fate bound to a class
> the train pairs exercise *at the granularity at which the
> key is defined* (exact colored pattern). It is always one
> of: **(i)** an account statistic or frame component (bgmap,
> canvas, scale) whose train agreement with the true rule is
> a coincidence of the statistic; **(ii)** a creation/field
> kind firing — or failing to fire — on a configuration no
> train pair contains; or **(iii)** a binding whose key the
> pairs exercise only in a form that does not discriminate
> it (blind-exercised but colored-unexercised; exercised at
> sizes {6,8,11} but not 18; exercised as a map key whose
> train image coincides with the truth).

And the symmetric fact, which is the anatomy's sharpest
result: **in the 4 truth-absent tasks the discriminating
structure is exercised in every train pair** (a solid block
with an odd center in all 4 pairs; the tile quotient in all
3; the ÷4 quotient in all 3; the block-structured shrink in
all 3) — the pairs shout it, and the grammar cannot bind it.
**In the 4 truth-present tasks the grammar can bind it and
the discriminating configuration is the unexercised part** —
a novel class (aabf363d, be03b35f), a novel colored
arrangement (ecaa0ec1), novel trigger classes (e45ef808).
Exercised-vs-unexercised is therefore not one question but
two, and the two species sit on opposite sides of it.

### 1.3 What the wrong rule does on the train pairs

In every one of the 8, the wrong rule is not an approximation
of the true rule — it is a *different function that the train
pairs render indistinguishable*, and the mechanism of
indistinguishability is one of three, matching §1.2:

- **Statistic coincidence** (d9fac9be, c909285e, 67b4a34d):
  an account-level statistic or a periodic-continuation kind
  computes, on each train scene, the same output as the true
  rule's structural computation. ARC tasks are constructed so
  that train scenes are few and structured; a statistic that
  agrees on 3–4 structured scenes is easy to find in a
  grammar whose account layer is searched over 2
  segmentations × 4×4 background-generator pairs × {const,
  gen, bgmap} rules × 40 pre-transforms. The search's breadth
  at the account layer is precisely what guarantees a
  coincident statistic exists to be found.
- **Per-instance binding coincidence** (caa06a1f, ecaa0ec1):
  bindings keyed to exact instances (whole-pattern
  signatures, rotation variants) are free parameters per
  instance; with k ≤ 4 scenes, the per-instance values that
  fit are underdetermined by exactly the instances the test
  input adds.
- **Default coincidence** (aabf363d, be03b35f, e45ef808):
  for classes the pairs never exercise, every consistent
  schema applies the grammar's default — preserve the unseen
  object, create nothing for an unseen trigger — and the
  defaults agree across the whole space, manufacturing
  unanimity on exactly the cells where the truth does
  something else. The version space is widest where the pairs
  are silent (median 8 plural Stage-A keys per fit task,
  census), but its *renderings* coincide wherever silence
  forces the same default.

---

## 2. The mechanism question — charging (a), (b), (c)

### 2.1 (a) Grammar defect — FIRM for 4 of 8 spaces

The k+1 test is the strongest instrument this program has
pointed at expressiveness: it asks whether *any* schema in
the *entire* swept space (all frames, all accounts, caps as
registered) is consistent with everything ARC shows a solver
about these tasks, test pair included. For d9fac9be,
c909285e, and caa06a1f it fails in every frame, with no
enumeration cap ambiguity (d9fac9be's spaces are singletons;
caa06a1f's are exactly-512 and completed). For 67b4a34d it
fails in all 45 reached frames; its sweep truncation is the
one soft edge in this section, and the charge for that task
is stated as **firm over the reached sweep** — the unreached
frames are disproportionately scaled variants of accounts
already failing at the background family, but they are
unmeasured and the document does not pretend otherwise.

The missing distinctions, named from the anatomy — these are
the grammar's proven absences, not conjectured ones:

1. **Addressed content.** No binding can name "the color at
   the center of the unique solid block," "the odd color
   enclosed by a uniform region," or any positional/relational
   query over the scene. Π names statistics of the scene;
   the true rules in d9fac9be *address* it. (d9fac9be)
2. **Two-level quotient structure.** No kind partitions the
   grid into blocks/tiles and emits the quotient grid of
   per-block classes. The field kind (periodic continuation)
   is the nearest kind and it is a different function.
   (c909285e at tile scale; 67b4a34d at block size 4 — the
   frame scales {d2, d3} cap the expressible quotients below
   the exercised ÷4.)
3. **Size-parametric fates.** Fates bind to exact patterns;
   a rule that is one fate at every size is represented as
   independent per-size bindings, which coincide where sizes
   are exercised and diverge where they are not. (caa06a1f)

The 71/71 background-family deaths (§1.1 fact 2) are read as
(a)'s *surface*, not a fourth absence: the background rule is
the last component still free when content cannot be
produced, so inexpressibility registers there first. A richer
background family would move the failure, not remove it —
for d9fac9be the needed "background" *is* the addressed
content of item 1.

**Population weight, stated carefully.** These are 4 of the
8 unanimous-wrong spaces — themselves 8 of 28 fits, fits
being a witnessing-skewed subset of tasks. The charge is
exact for these tasks and is *not* extrapolated to a
population rate. What is population-level is the census
substrate the absences live in: size changes are non-integer
in 62.9% of size-changing pairs and only 17.6% of tasks
conserve object count (architecture census) — the grammar's
frame/fate structure is integer-scaled and pattern-keyed
against a distribution that mostly is not, which is why
absences 2–3 are structural rather than anecdotal.

### 2.2 (b) Representation defect — NO positive exhibit; the dual defect is exhibited instead

Charge (b) as commissioned is *merging*: the segmentation or
key structure identifies two things the true rule treats
differently, so no binding assignment can be right. Among
the 8 spaces there is **no task** where the anatomy shows
two objects sharing a key and receiving different true fates,
and none where a segmentation merge is the wrong component —
in the truth-absent four, the failure is above the object
layer entirely (account, quotient, size); in the
truth-present four, the truth *is* representable under the
segmentation in force, which refutes merging for them
directly. Charge (b) over these 8: **0 firm, and the band is
narrow** — a merging failure hidden inside a truth-absent
task cannot be excluded from these rows alone (if the truth
is inexpressible, the reason could in principle be a merge
the anatomy did not isolate). The instrument that decides
(b) at scale is named and priced in §3.3: a same-signature
fate-split scan (do two objects with one exact signature ever
receive different fates in one pair?) over pool B's train
pairs and the fit tasks' test pairs, reusing the census's
fate machinery — ≤ 1 CPU-hour, $0, not run here because the
8-task anatomy gave it nothing to explain.

What the record exhibits instead is (b)'s **dual**: the key
structure *splits* what the true rule unifies. Fates are
keyed by exact colored pattern, so a rule that is one
statement ("preserve this motif") is four independent
bindings over its rotation variants (ecaa0ec1), one binding
per grid size (caa06a1f), one per witnessed instance — and
each split multiplies the version space (the parameter
derivation's L1: 86.9% of witness binding signatures tied)
while contributing no discriminating power. Over-splitting
is charged as part of (a): it is a property of the grammar's
keying, it is why per-instance coincidence (§1.3) is always
available, and §3.1 prices its repair as a trade, not a gift.

### 2.3 (c) Intrinsic to the pairs — FIRM for 4 of 8 spaces, at grammar-relative strength

For ecaa0ec1, be03b35f, aabf363d, and e45ef808, the k+1 test
verifies: rules consistent with all k+1 pairs exist in the
grammar. The train-only version space therefore contains —
provably, by exhibition — at least two rules that agree on
every train pair and disagree on the test input, one of
which is (extensionally, on all available data) the truth.
No procedure whose information is the train pairs plus this
grammar can select the true one except by a preference among
consistent rivals that the pairs do not justify: on these
tasks, *identification from the pairs is exhausted*, and the
residual is a prior or nothing. The four exhibits are the
proof objects; §3.2 states the ceiling they imply.

Two strengths must be kept apart. (c) is proven **relative
to this grammar's hypothesis space**: a different space —
with different keys, or a learned prior over programs —
re-partitions which tasks are (c) and which are (a). It is
not proven, and cannot be proven from finite exhibits, that
these four tasks are ambiguous for *every* conceivable
representation. What *is* representation-independent in the
exhibits is the k=2 core: aabf363d's discriminating class
appears in no train pair at all, so any representation whose
hypotheses are functions fit to the pairs faces the same void
there — its fate for that class comes from its prior or its
defaults, never from the data. That sub-case is (c) at full
strength.

### 2.4 The corrected ledger, restated with this derivation's charges

The conversion derivation's ledger for the 27 fit deaths,
with the census's (b)/(c) correction and this derivation's
content charges applied to the classes they reach:

| Charge | Share | Basis |
|---|---|---|
| Certification dynamics killing correct parents | 17/27 deaths (58/64 folds) | census §(i), measured |
| Fit quality (wrong parent) | 2/27 deaths (6/64 folds) | census §(i), measured |
| Version-space content: truth absent from grammar | 4 of the 8 unanimous-wrong spaces | this derivation, k+1 |
| Version-space content: truth present, pairs don't select | 4 of the 8 unanimous-wrong spaces | this derivation, k+1 |
| Nondeterminate / canvas / budget deaths outside the fold question | 8/27 deaths | probe records |

The charges are on different denominators because they answer
different questions — dynamics is a property of folds,
content of spaces — and the document keeps them unmerged for
exactly that reason.

---

## 3. The derived consequence — shape (iii), the split carried through

### 3.1 The (a)-half: a grammar commission, specified and ceiling-priced

The four truth-absent spaces name three additions, stated at
the precision a build commission would need:

1. **A quotient kind.** A derivation that partitions the
   input grid into b×b blocks (b a scene parameter in Π's
   sense — read off the scene's period structure, not a free
   constant), classifies each block by a pattern/parameter
   function from the existing kinds, and emits the quotient
   grid as the output (or as an object in it). This is the
   two-level structure of §2.1 item 2, and it subsumes the
   tile-quotient and block-quotient exhibits at b = tile
   period and b = 4 respectively.
2. **Addressed-content parameters.** Π gains region-query
   functions — enclosed color, center-of-unique-solid-block,
   odd-one-out color within a uniform surround — as named,
   total scene functions, bindable exactly like the existing
   scalars (§2.1 item 1).
3. **Size-parametric fate keys.** Fate keys gain a
   size-quotiented form: a fate may bind to a pattern *modulo
   uniform scaling*, with the size function carried as an
   explicit binding — so one rule can be one binding at
   every size (§2.1 item 3), instead of one binding per
   exercised size.

**The fit-side price, stated as the trade it is.** The census
bound (921/938 = 98.2%) is a necessary-condition candidacy
ceiling over *this* grammar; each addition only adds
candidates, so the recomputed bound can only rise toward the
17-task residue (which sits inside the novel-creation mass
these additions partly address). But the bound was never the
constraint — conversion and content are, and additions cut
both ways there: every new kind is also a new way to fit
wrongly. A quotient kind that fires spuriously widens version
spaces on the 299 size-changing tasks; size-parametric keys
*shrink* spaces (fewer independent bindings) while quotient
and addressing keys *grow* them. The net effect on U is not
computable from this record — it is measurable, by the same
survivor-census instrument on the new grammar's fits, and
**that measurement, not a probe, is the commission's first
gate**, mirroring the discipline that produced this document:
no build is authorized by a bound; it is authorized by a
measured U on spent draws, against a pre-registered band.

**The ceiling on the whole (a)-half, computed on the
determined subset.** Among the census's 13 determined fit
spaces: 1 unanimous-correct, 8 unanimous-wrong (4 truth-
absent + 4 truth-present), 4 plural. A *perfect* repair of
the (a)-half — every truth-absent space becoming
unanimous-correct, an outcome no real commission promises —
moves the determined-subset solve rate from 1/13 to 5/13, and
only if the repairs add no new wrong-unanimous spaces of
their own. Scaled by any fit supply the record supports,
that is a program that converts a third of its determined
fits and abstains or errs on the rest — nowhere near the
F·U ≥ 0.90 arithmetic (conversion derivation §2.5), because
the (c)-half stands untouched behind it. The (a) commission
is worth doing only as what it is: the removal of a proven
expressiveness defect, in a program whose criterion problem
is elsewhere. Commissioned as a path to 216/240, it would be
a false claim, and this derivation does not make it.

### 3.2 The (c)-half: the information ceiling, stated as an argument

**Claim.** Let P be any identification procedure whose input
is a task's k train pairs and whose output is a single rule
(or a single prediction) from a hypothesis space H, with no
information source beyond the pairs and a fixed prior over H.
For each of the four exhibited tasks there exist h_wrong,
h_true ∈ H (H = this grammar) with h_wrong ≠ h_true on the
test input and h_wrong = h_true on every train pair.
Therefore P's output on those tasks is decided entirely by
P's prior restricted to the version space: P is correct
exactly where its prior ranks the truth above every wrong
consistent rival. A prior-free P (any tie-breaking, any
simplicity ordering fixed in advance) is correct on at most
the tasks where its fixed ordering happens to rank truth
first — a property of the ordering, not of the pairs.

**What it caps.** Any pairs-only solver's certified-solve
rate is capped by

> (rate of tasks whose version space is unanimous-correct)
> \+ (prior's win rate on the remaining consistent spaces)
> × (their rate),

with every term measured or measurable in this program: the
first term reads **1/28 of fits** (3.6%); the grammar's own
tie-breaking achieves 1/9 (11%) on the unanimous subset and
0 on the plural one. The cap is not a statement about search
effort, compute, or certification strictness — all three were
varied across this program's probes and none moved the
content terms. It is a statement about what k ∈ {2, 3, 4}
pairs contain.

**What changes the ceiling.** Exactly three things, in
principle: **(i)** more pairs — ARC fixes k; not available.
**(ii)** a prior over hypotheses that concentrates on true
rules — an information source the pairs do not contain,
imported from outside the task (a learned proposer's prior
is the live candidate; §4 prices what it must exhibit).
**(iii)** a different hypothesis space in which the exhibited
rivalries do not occur — i.e., moving tasks between the (a)
and (c) charges. Note what (iii) cannot do: it cannot remove
rivalry as such. Every space rich enough to contain the true
rules of this distribution contains rivals for them at k ≤ 4
unless its keys are functionally determined by witnessed
data — and the census measures how far this distribution is
from that condition (LOO fully determinate on 16.4% of pool
B, 4.2% of eval-120). A grammar change redistributes the
ceiling's terms; it does not repeal the ceiling. The only
term in the cap that can grow without bound is the prior's
win rate, which is why §4, not §3.1, is where the criterion's
remaining life is.

### 3.3 The unrun instrument, priced

The (b) sub-charge (§2.2) is decidable by a **same-signature
fate-split scan**: over pool B's 3,040 train pairs and the 28
fit tasks' test pairs, group each pair's input objects by
exact colored signature and test whether any signature
receives two different fates within one pair (under the
census's fate classification). A positive rate would exhibit
merging directly; a zero rate closes (b) at population
strength for the signature keying. Cost: the census's
`analyze_pair` machinery already computes per-object fates
for the full population in minutes; the scan is an
aggregation change over it — **≤ 1 CPU-hour, $0**. Not run:
the 8-task anatomy produced no merging exhibit for it to
explain, and this derivation's charges do not depend on its
outcome. It is registered here so the (b) question is left
with a priced decider, not an impression.

---

## 4. Friday's place, updated

Friday's measurement (gauntlet draw seed 22979062; local
120B proposer, k=128 per unit; frozen certification;
`friday_bigmodel_kit/HARNESS_READY.md`) runs against a
program whose exact-search lineage is now closed at every
level: fit supply (0.208, economics-invariant across three
organizations), certification dynamics (58/64 — real, and
insufficient to fix), unanimity (U ≤ 0.857 by ceiling,
unanimous∧correct = 1/28 measured), and content (this
derivation). The proposer's position relative to that record
must be stated exactly:

**What Friday is not bound by.** The proposer's hypotheses
are programs from a learned distribution, not schemas of the
derived grammar. The (a)-half's absences — no quotient kind,
no addressed content, no size-parametric fates — are absences
of the *grammar*, and a sampled program can express a block
quotient or an enclosed-color query in one line. The
shared-wrong wall of §1–§2, as a statement about a schema
space, does not apply to it.

**What Friday is still bound by.** Two things, both measured
in this record. First, §3.2's ceiling in its prior form: a
proposer fit is a consistent rival like any other, and where
the pairs leave the version space plural, the proposer
solves only where its *prior* — not its fit — picks the
truth. Second, determinacy at certification: Friday's fits
face the frozen certification (LOO + shape-diverse holdout),
whose folds are additional pair-like constraints; the
grammar's fits died there at 27/28, 63% of those deaths by
dynamics a *set-valued* judgment would not have suffered —
but Friday's certification unit is the frozen single-program
one, and this derivation does not amend it.

**The k=128 sample set is a version space, and it will be
read as one.** For each draw task, Friday's cache contains up
to 128 sampled programs; the subset fitting all train pairs
is an empirical version space, and its renderings on the test
input can be counted exactly as the census counted the
grammar's. The statistics that decide what Friday *means*,
registered here before the run:

- **Sample-U**: among tasks where ≥ 1 sample fits all train
  pairs, the fraction whose fitting samples render exactly
  one distinct test grid.
- **Sample unanimous∧correct rate**: among sample-unanimous
  tasks, the fraction whose single rendering is the true
  output. The grammar's corresponding figure is **1/9 =
  11%** (and its determined-space solve rate is 1/13).
- **Conversion at supply**: certified solves ÷ full fits,
  against the grammar's 1/28 = 3.6% and seat (b)'s floor of
  1/18 ≈ 5.6%.

**What counts as evidence for a truth-concentrating prior**
(the (c)-door's deciding statistic): sample-unanimous tasks
≥ 8 **and** sample unanimous∧correct ≥ 3/4 of them (e.g.
6/8 against the grammar's 1/9 — separable at these counts,
Fisher exact p ≈ 0.013), **or** certified conversion an order above
the grammar's at comparable supply (≥ 4 certified from
≤ 20 fits, i.e. the fits the proposer returns are
*pre-concentrated* on truth, not merely numerous). Either
pattern says the prior ranks true rules above their
consistent rivals at rates the analytic grammar's
tie-breaking does not approach — the one property §3.2
identifies as capable of moving the ceiling's second term.

**What counts as merely more fit supply**: coverage at or
above seat (b) (≥ 20/48 fits) with conversion near its floor
and sample renderings scattered or unanimous-wrong at
grammar-like rates. That pattern earns the proposer its
registered seat as a Stage-V *input* (conversion derivation
§4.3: proposer schemas enter the factored survivor sets and
face the same intersections and unanimity) and nothing more —
inside a set-valued unit, a diverse-wrong proposer *lowers*
U on its tasks, and its effect there must be re-measured, as
§4.3 already registered. Seat (a) (≥ 4/48 certified) without
the unanimity statistics above is likewise ambiguous between
the two readings — certified solves through fold constraints
are stronger than fits, but 4 solves is 8.3% of the draw
against a criterion of 90%, and the seat standard was always
a seat standard, not a criterion trajectory.

**What Friday cannot decide, whatever it returns.** Whether
the §3.1 grammar additions would work (it does not use the
grammar). Whether draw behavior transfers to the sealed exam
(the draw is pool A/B/C; the exam is unspent and untouched).
And — by arithmetic, not by outcome — the criterion itself:
the proposer route reaches 216/240 only if F_prop × W ≥ 0.90
with W its truth-selection rate on consistent spaces; even a
Friday that maxes its seat standard (solves at ~2× the
grammar's best supply with conversion several times 1/28)
establishes the *direction* of W, at one to two orders of
magnitude below the criterion's demand. Friday is the (c)
door's first measurement. It is not the criterion's.

---

## 5. The honest ceiling

In this document's own voice, the strongest statement the
record now supports:

**Over the derived grammar, 216/240 is unreachable by any
identification procedure, including perfect ones.** The
statement is no longer a product of proxies. Fit supply is
measured (0.208; 0.982 is a candidacy bound no lane
approached within 4.7×). Conversion's fixable part is
measured (dynamics 58/64 folds) and its repair is measured
to be insufficient (the survivor census's closure: F·U <
0.90 under every completion of the undecided spaces, best
case 0.842). And now the content is measured: of the spaces
that survive every filter and speak with one voice, 8 of 9
are wrong — 4 because the grammar cannot express the truth
at all (proven absent, k+1, every frame), 4 because the
truth sits inside the space unselected, on configurations
the pairs never exercised (proven present, k+1, every
relevant frame). A perfect search, a perfect certification,
and a perfect version-space mechanism over this grammar
convert this population at the rate its content dictates,
and that rate's ceiling is 0.842 of the criterion's 0.90
before correctness is even asked — and 1/28 after it is.

**Doors closed for good** (each closed by its own registered
instrument, not by fatigue): exact search over the derived
grammar in all three organizations (fit supply,
economics-invariant); intersection-first economics as a fix
(F6, both clauses); version-space conversion over this
grammar (F-unanimity + the ceiling completion argument);
certification-dynamics repair as a path to the criterion
(measured large, measured insufficient); single-hypothesis
identification over this grammar in every form, since its
version spaces are the subject of §§1–2.

**Doors still open, with their deciding measurements:**

1. **The proposer prior (Friday, Nov 6).** The only door
   that addresses the (c)-half — a truth-concentrating prior
   is the ceiling argument's one unbounded term. Deciding
   statistics registered in §4 (sample-U, sample
   unanimous∧correct vs the grammar's 1/9, conversion at
   supply), under the seat standard already frozen. A
   positive result reopens the criterion question as a
   question about W's magnitude; a null closes the
   LLM-proposer species at this scale by the joint reading
   with P3 already registered in HARNESS_READY.
2. **A new grammar commission (§3.1).** Addresses the
   (a)-half only: quotient kind, addressed-content
   parameters, size-parametric fate keys. Its deciding
   measurement is a survivor census of *its* fits on spent
   draws (measured U and measured unanimous∧correct against
   pre-registered bands) before any probe — the same gate
   that closed this grammar, applied prospectively. Even
   total success on this door leaves the (c)-half and the
   F·U arithmetic standing; it is commissioned, if at all,
   as defect removal, not as a criterion path.
3. **Precision on the undetermined spaces.** 14 of the
   census's 15 undetermined version spaces remain
   unexhausted (their enumerated prefixes each render one
   grid; whether the full spaces are unanimous, and whether
   that grid is wrong, is unmeasured). A test-relevant-key
   projection instrument could decide them without
   enumeration. Its outcome moves U's estimate, not the
   criterion: the completion argument already grants them
   all unanimous and still loses, and granting them all
   *correct* as well would raise unanimous∧correct from
   1/28 to at most 15/28 of fits — against a criterion that
   needs the product at 0.90 of *tasks*, with fit supply
   measured at 0.208. This door leads to a sharper number,
   not to a different verdict.

**The one-sentence state of the program.** The 90% criterion
now rests on a single empirical question — whether a learned
prior concentrates on true rules at rates no analytic
tie-breaking approaches — and that question has a registered
measurement, a frozen protocol, and a date: Friday.

---

## Appendix A. Provenance and cost

**A.1 Sources.** `SURVIVOR_SET_CENSUS_2026-11-04.md` +
`SURVIVOR_SET_CENSUS_ROWS_2026-11-04.json` (28 per-task
records; U treatments; the (b)/(c) fold split of §(i));
`CONVERSION_DERIVATION_2026-11-04.md` (§§1–2 the ledger and
the Stage-V design, §2.5 the F·U arithmetic, §4.3 the Friday
seat terms, §5 the proxy ceiling this document supersedes
with measurements); `PARAMETER_SEMANTICS_DERIVATION_2026-
11-04.md` (Π, the binding kinds, L1 tie rate 86.9%, the
921/938 bound and its standing label); the three probe
results files (`DERIVED_SOLVER_PROBE_RESULTS_2026-11-04.md`,
`SIEVE_ITERATION2_PROBE_RESULTS_2026-11-04.md`,
`SIEVE_INTERSECTION_PROBE_RESULTS_2026-11-04.md`) and diag
rows; census outputs in `census/` (`summary.json` fate and
size structure; `per_task.jsonl` witnessing);
`friday_bigmodel_kit/HARNESS_READY.md` (draw seed 22979062,
seat standard, protocol).

**A.2 Fresh measurements (this derivation).** Instrument:
`derived_solver/wrong_binding_anatomy.py` — full-frame sweep
(all pre-transforms × deduped accounts, census caps: 512
schemas / 20,000 combos / frame), k+1 re-runs on
train-verifying frames (added-pair consistency under the
lane's own verify path), winning-frame diff anatomy (cell
diff, object-membership classification, signature exercising
against the task's train pairs under the winning account).
Rows: `derived_solver/wrong_binding_rows.json` (8 tasks) +
`derived_solver/wrong_binding_scoped.json` (e45ef808
winning-frame battery + c909285e anatomy re-run). Per-task
walls: sweep truncated for 67b4a34d at 700 s (45 verifying
frames reached; recorded in its row); e45ef808's full sweep
exceeded the run budget and was replaced by the scoped
winning-frame battery (its train-only space was already
exhausted by the census at raised caps: 2,196 schemas, one
rendering). Total fresh compute ≈ **55 CPU-minutes** (battery
walls 2,347 s + scoped runs ≈ 270 s + the killed first
e45ef808 sweep ≈ 780 s), $0. The k+1 test's logic: a frame
failing on the k train pairs cannot verify with an added
pair (Stage-A intersection only shrinks; covers only gain
constraints), so restricting k+1 to train-verifying frames
loses nothing. The predict-path/verify-path distinction is
kept throughout: `renders_truth` counts schemas whose
`predict3` output equals the true test output; k+1
verification is the lane's `verify3` reconstruction over all
pairs. aabf363d is the case that separates them (k+1
verifies in 26/26 frames; no predict-path rendering is the
truth — its k+1-consistent schemas' phases do not collapse
to a single offset under the frozen predict rule, which is
recorded as a property of the frozen machinery, neither
hidden nor repaired here).

**A.3 What was not measured.** The 4 plural-determined spaces
(e4888269, 1fad071e, 1d61978c, bd283c4a) were not re-swept:
within-frame plurality already places them on the (c) side
of every question this derivation asks, and e4888269's
288/384 input-renderings are noted in §1.1's fact 3 as the
same fixed point at plurality scale. The 14 unexhausted
undetermined spaces are §5 door 3. The (b) scan is §3.3:
specified, priced, unrun.

*Files: this document; instruments and rows in
`derived_solver/`. No solver code was written and no probe
was run. The sealed approval exam was not read, run, or
touched. Certification was nowhere proposed as a dial.*
