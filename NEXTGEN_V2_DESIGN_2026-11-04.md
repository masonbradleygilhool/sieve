# APEX-2 NEXT-GENERATION SOLVER v2 — DESIGN (2026-11-04)

**Status:** design + pre-registered probe gates, written BEFORE the probe
runs. Foundation: the v1 kill record (`NEXTGEN_SOLVER_DESIGN_2026-11-04.md`,
`NEXTGEN_PROBE_RESULTS_2026-11-04.md`). Every v1 number quoted below is
MEASURED from that probe. No score is claimed for the private eval; the
acceptance criterion stands as ordered: **90%+ on the ARC-AGI-2 private
eval (216+/240)**, design target 240/240.

---

## 1. The starting spec (v1's measured death taxonomy — not re-derived)

On fresh gauntlet A+B (n=48), v1 scored 0/48, Wilson [0%, 7.4%].
Full-fit coverage was 2/48 (4.2%). Deaths:

| Death class | A+B count | What it means mechanically |
|---|---|---|
| Creation / split-merge | 35/48 | An output object had no same-cell-count dihedral source among input objects |
| Non-dihedral size change | 11/48 | Output shape was not a dihedral image of input shape under v1's canvas rules |
| LOO-rejected | 2/48 | Full-fit schema induced; held-out re-induction failed to predict the held pair; lane abstained |

Two components of v1 are **validated at exactly the stated strength and
carry over as machinery, not hypotheses**:

1. **LOO re-induction certification** — caught 2/2 full-fit schemas that
   failed to generalize within-task (plus both synthetic controls behaved:
   positive solved+certified, negative rejected). It is reused unchanged
   in form: re-induce from k−1 pairs, require exact prediction of the
   held pair; 2-pair tasks fall back to full fit + test determinacy.
2. **The correspondence primitives** — modal-background segmentation,
   object patterns, dihedral-canonical shape signatures, functional
   cellwise color maps, grid dihedral factoring. Reused from
   `nextgen_probe/ng_lane.py`.

What died is v1's **schema language**: objects may only be preserved
(dihedral + recolor + translation) or deleted, on a same-shape or
crop-to-content canvas. ARC-AGI-2's fresh-task rules predominantly
*transform* objects and *resize* grids. v2 is a new schema language on
the same identification discipline: **hypotheses are constructed from
measured correspondences and identified by cross-pair intersection;
acceptance is within-task held-out prediction; failure to certify means
abstention.** No prior over whole rules is introduced anywhere — the
grammar below is a representation (what forms a derivation may take),
exactly as v1's dihedral group was; *which* derivation each object
takes, with which parameters, is computed from the pair evidence and
killed by intersection when pairs disagree.

## 2. The v2 rule representation (mechanical)

A **schema** is a tuple `(G, S, canvas, bg_map, rules, deletions)`:

- `G` — a grid pre-transform: a dihedral transform composed with a
  uniform integer grid scale (`×2`, `×3`, `÷2`, `÷3`, or `×1`).
  Applied to the input grid before object analysis. (`÷k` is defined
  only when every k×k block of the transformed input is unanimous.)
- `S` — scale bookkeeping induced by `G` (object coordinates live in
  the pre-transformed grid).
- `canvas` — how the rendered grid becomes the output grid: `same`,
  `crop` (crop to content bounding box), or `pad(rule)` with
  rule ∈ {constant offset, centered, bottom-right anchored}.
- `bg_map` — (background_in → background_out), consistency-checked
  across pairs, as in v1.
- `rules` — a binding from a **derivation key** to a **derivation
  value** (§2.1). Every object in every pair is accounted for by
  exactly one rule binding, by deletion, or the pair fails.
- `deletions` — feature classes deleted in every pair they appear in.

### 2.1 Derivations: the unit of transfer

A **derivation** produces one output object from input objects. Kinds:

| Kind | Sources → outputs | Parameters (the rule value) |
|---|---|---|
| `preserve` | 1 → 1 | (τ dihedral, φ functional color map, δ displacement) — v1's action |
| `scale` | 1 → 1 | (k ∈ {2,3} up, or ÷k down, τ, φ, δ) — pattern scaled cellwise (up: each cell → k×k block; down: unanimous k×k blocks → one cell) |
| `grow` | 1 → 1 | (mode, τ, φ, δ) with mode ∈ {ring (full Chebyshev-1 dilation ring added), holes (interior holes filled), bbox (bounding box filled)}; added cells all one fill color c, part of the value |
| `mirror` | 1 → 1 | (axis ∈ {vertical, horizontal}, τ, φ, δ) — output = source ∪ its reflection across the axis of its own bounding box, colors carried through the reflection |
| `split_color` | 1 → many | per output part: (part color c₀, τ, φ, δ). The parts are exactly the per-color cell slices of the source; jointly they partition the source |
| `split_sep` | 1 → many | per output part: (part index in canonical origin order, τ, φ, δ). Parts are the connected components of the source after removing one full row or column of a single separator color spanning the source's bounding box; the separator cells are consumed (deleted) |
| `merge` | many → 1 | anchor class + per-part (τ, relative offset, φ). Parts are ≤3 input objects placed by translation/dihedral so their cells exactly tile the output pattern without overlap |
| `copy` | 0 → 1 (creation) | (template class X, τ, φ, δ from X's rendered origin) — the created object's pattern is a dihedral image of the pattern that class X's rule produces in the same pair |
| `frame` | 0 → 1 (creation) | (around ∈ {canvas} or a feature class, margin ∈ {0,1}, color c) — the created object is a single-color rectangular ring whose bounding box is the output canvas (margin 0) or the rendered bounding box of the anchor class expanded by the margin |

**Feature class** (the key's source component) is v1's: (sorted colors,
cell count, dihedral-canonical shape). Keys:

- unary kinds: `(kind, source class)` — split kinds key per part:
  `(split_color, source class, c₀)`, `(split_sep, source class, part idx)`.
- `merge`: `(merge, sorted tuple of source classes, anchor class)`.
- `copy`: `(copy, template class)`. `frame`: `(frame, around)`.

### 2.2 Placement

Every derivation value carries δ, the output origin minus the anchor
source origin (for `merge`, the anchor part's origin; for `copy`, the
template's *rendered* origin; for `frame`, placement is definitional).
δ must be **the same vector in every pair** for the binding to survive
intersection. This is v1's known restriction carried over deliberately:
placement is a constant offset per rule, not a relation. (See §5 for
what this excludes and what would identify it.)

## 3. Identification when object counts differ (the core argument)

Per pair, identification is an **exact-cover problem over objects**,
not a greedy matching:

1. **Candidate generation.** For every output object, compute every
   derivation (from the §2.1 grammar) under which some input object(s)
   of this pair could produce it. Candidates are *measured*: each is a
   concrete geometric fact about this pair (patterns equal after the
   stated transform; the output's cells exactly the dilation ring of
   the placed source; the parts exactly tiling the source; …). A
   candidate that is not a fact about the pair is never generated.
2. **Class uniformity within a pair.** All instances of one feature
   class in a pair take the same fate-mode (same rule key, or all
   deletion), as in v1. A split consumes its source jointly: the part
   derivations of one source must exactly partition its cells.
3. **Exact cover.** An assignment for the pair is a set of derivations
   such that every output object is produced exactly once, every input
   object is consumed exactly once (by one derivation, by one split
   jointly, by one merge, or by deletion), and the induced key→value
   bindings are internally consistent. Assignments are enumerated by
   backtracking (outputs ordered by fewest candidates), capped; a cap
   hit is reported as its own sub-reason (`search_cap`), never silently
   treated as inconsistency.
4. **Cross-pair intersection.** One assignment per pair is chosen so
   that all pairs' bindings agree on every shared key and no class is
   both ruled and deleted. This is the same intersection discipline as
   v1, lifted from matchings to covers: each additional pair can only
   shrink the surviving schema set. If no combination survives, the
   pair set refutes the grammar for this task (NO-SCHEMA, sub-reason
   recorded: which stage died — §6 taxonomy).
5. **Reconstruction.** Surviving schemas must reproduce every train
   output exactly by rendering (this catches placement collisions and
   canvas interactions that per-object candidate facts cannot see).
6. **Certification.** Each surviving schema faces v1's LOO
   re-induction gate unchanged. Only certified schemas emit
   predictions. If two certified schemas disagree on any test input,
   the lane **abstains** (sub-reason `ambiguous`) — the probe measures
   certification, and a coin-flip between two certified-but-divergent
   rules is not certification of either. (The production 2-candidate
   contract is deliberately not used.)

**Why this is identification, not search over a prior:** the candidate
set for a pair is a function of that pair's measured geometry alone;
the grammar bounds the *forms* a fact may take but contributes no
parameters. Every parameter in a surviving schema (τ, φ, δ, k, fill
color, axis, part structure) is read off a measured correspondence and
must re-measure identically in every other pair. The failure mode this
cannot have is v1's five dead lanes' mode — the rule absent from a
prior — because there is no prior. The failure modes it *can* have are
enumerated in §5, honestly.

## 4. Size change: parameterization and identification

Grid-level size change lives in `G` and `canvas` (§2):

- **Uniform scaling** (`×k`, `÷k` in `G`): identified by shape
  arithmetic — the pre-transformed input shape must equal the output
  shape in *every* pair — and then by the object analysis proceeding
  in scaled coordinates. `÷k` additionally requires block unanimity of
  the input, itself a measured fact per pair.
- **Crop** (`canvas=crop`): identified when the rendered grid's
  content bounding box, cropped, equals the output in every pair.
- **Pad** (`canvas=pad(rule)`): identified when the rendered grid
  embeds into the output at an offset that follows one named rule
  (same offset in all pairs / centered by formula / bottom-right
  anchored) in every pair; offsets are measured per pair by exact
  embedding search, and only a rule consistent across all pairs
  survives.
- **Object-level size change** is `scale`/`grow`/`mirror`/split/merge
  at derivation level (§2.1) — the grid canvas need not change for an
  object to change size.

Combinations are tried in a fixed order (scale 1 first, then ×2, ×3,
÷2, ÷3, each over the 8 dihedrals) and the first (G, canvas) under
which a certified schema exists wins; shapes kill almost all
combinations before object analysis runs.

## 5. What pairs alone cannot identify (stated, not papered over)

1. **Canvas arithmetic beyond the observed shapes.** Train pairs in
   ARC typically share one input shape. On a single observed shape,
   "output = input + (2,0)", "output = 2·input − (h,0)", and
   infinitely many other canvas functions agree. v2 identifies canvas
   only within its named candidate set {dihedral∘scale, crop, named
   pad rules}; if the true canvas function is outside the set, the
   task dies as NO-SCHEMA (honest), and if a *wrong* in-set function
   agrees on all train shapes but differs on the test shape, **LOO
   cannot catch it when all train input shapes are equal** — LOO
   re-induction sees the same shape evidence minus one pair. What
   would identify it: train pairs with ≥2 distinct input shapes
   mapping to distinct output shapes (then intersection + LOO do
   discriminate), or a stated problem-level prior over canvas
   functions, which this design refuses to smuggle in. This is a live,
   named failure class of v2; the probe's taxonomy cannot see it
   (a wrong-canvas solve attempt looks like a train-fit-only), and it
   is recorded here so the record is not surprised by it.
2. **Unrelated creation content.** An output object that is not a
   copy, frame, symmetry completion, or transform of anything present
   can be *anything*; no pair evidence identifies its content. v2
   identifies creations only when the content is a deterministic
   function of identified context (template class present in the pair,
   canvas geometry, anchor class geometry). Otherwise the object is
   unexplained and the task is NO-SCHEMA with sub-reason
   `creation_unexplained`. What would identify the general case:
   content addressed by a parameter object (e.g., a numeral/bar whose
   measured value determines the created shape) — that requires a
   *semantics of parameter objects* (counting, reading lengths), which
   is a different mechanism, not an extension of this grammar, and is
   out of scope here by statement, not by oversight.
3. **Counting/arithmetic rules generally** (repeat N times, draw
   length-N bars, sort by size): the grammar has no numeric register.
   Same disposition as (2).
4. **Relational placement** ("move until contact", "align to the
   largest", "place between A and B"): δ is a constant per rule (§2.2).
   Tasks whose placement is a relation die at intersection
   (`delta_nonconstant`) or cover stage. Identifying relations
   requires placement to be a function over measured scene features
   with its own intersection discipline — a named successor problem,
   not claimed here.
5. **Genuinely ambiguous assignments.** Symmetric configurations (two
   identical-class objects swapping roles, a split whose parts are
   interchangeable) can admit two covers whose schemas both fit and
   both LOO-certify but predict differently. The lane abstains
   (`ambiguous`). Pair evidence cannot break a true symmetry; only
   additional pairs in which the symmetry is broken could, and the
   gate already uses all pairs there are.

## 6. Death taxonomy for this design (reported in the results file)

Every non-solved A+B task gets exactly one sub-reason, from the lane's
own accounting:

- `canvas` — no (G, canvas) combination made shapes/reconstruction
  compatible.
- `creation_unexplained` — ≥1 output object had zero derivation
  candidates in some pair (content outside the grammar; §5.2).
- `cover_failed` — every output had candidates, but no exact cover
  exists (split/merge accounting cannot be made exact).
- `inconsistent_<field>` — covers exist per pair but cross-pair
  intersection kills all combinations; field ∈ {phi, tau, delta,
  param} records the first binding type that conflicted.
- `search_cap` — enumeration cap hit before the space was decided
  (reported separately; never merged into `inconsistent`).
- `loo_rejected` — full-fit schema(s) induced; LOO certification
  failed for all.
- `ambiguous` — ≥2 certified schemas disagree on a test input.
- `nondeterminate_test_class` — 2-pair fallback: a test object's class
  has no binding.

## 7. Cheapest falsifiers (named before the run)

- **F1 — reach:** full-fit coverage (a schema fitting all train pairs,
  before LOO) on A+B. v1 measured 4.2%. If v2 coverage is <15%, the
  extended grammar still does not reach ARC-AGI-2's rule space and the
  design is wounded regardless of solves.
- **F2 — conversion:** 0 LOO-accepted solves on A+B = kill (as v1).
- **F3 — degeneracy:** if ≥half of all solves are `colormap_only`, the
  active ingredient is a lookup table → verdict capped at WEAK-ALIVE.
- **F4 — algebra shadow:** solves on compose-control pool C but none on
  real pools = the lane has learned the substrate's algebra again.
- **F5 — over-generation (new in v2):** the grammar is strictly more
  powerful than v1's, so fit-by-construction is a live risk. If ≥half
  of full-fit schemas are LOO-rejected, certification is doing all the
  work and the language is suspect → verdict capped at WEAK-ALIVE and
  the over-generation is reported as a finding, not hidden.

## 8. Pre-registered probe gates (written before any run)

**Instrument:** `gauntlet.py`, **unmodified**. Draw **A:12, B:36,
C:12**, budget **25 s/task**, single draw, seed **20261109** — selected
by a rule fixed before the v2 lane existed: the smallest seed
≥ 20261105 whose B-draw and C-draw are both disjoint from v1's
seed-20261104 draw (verified by replicating the gauntlet's sampling
procedure offline; the lane was never run during seed selection). Pool
A has only 18 tasks, so A-overlap with v1's draw is unavoidable (9/12
shared at this seed) and is reported, not hidden; B (938-pool) and C
(240-pool) are fully fresh.

**Controls (must pass before the run counts):**
(i) positive control A — a synthetic task whose rule is a v2-only
transformation (split by color + preserve-with-move, 3 train pairs)
must be solved and LOO-certified;
(ii) positive control B — a synthetic task whose rule is a v2-only
size change (object grow-by-ring on a padded canvas, 3 train pairs)
must be solved and LOO-certified;
(iii) negative control — control A's inputs with train outputs
shuffled across pairs must produce no accepted schema and no solve.

**Primary metric:** accepted-schema solves on A+B (n=48), Wilson 95%
reported for every rate. Solves counted per mechanism tag
(object_schema / object_transform / object_creation / colormap_only /
grid_transform) in the results file. Full-fit coverage on A+B reported
alongside (F1).

**Gates on A+B solves:**
- **KILL:** 0 solves → this schema language is dead at probe strength.
  No iteration on it without a new measured idea.
- **WEAK-ALIVE:** 1–3 solves, all certified → the identification loop
  fires on real fresh tasks with transformation/size-change rules in
  scope. Earns exactly one iteration aimed at the measured taxonomy.
  No scale.
- **ALIVE:** ≥4/48 solves (≈8.3%) AND full-fit coverage ≥15% (F1) →
  earns scale: a 96-task fresh B draw plus the grammar extension the
  taxonomy ranks first.
- **Overrides:** F3 (≥half solves colormap_only) caps at WEAK-ALIVE.
  F5 (≥half of full-fits LOO-rejected) caps at WEAK-ALIVE. F4 (pool C
  solves with zero A+B solves) is reported as the algebra-shadow
  finding and the verdict is KILL regardless of pool C.

**Accounting rules:** as v1 — the lane reads train pairs and test
*inputs* only (test outputs stripped on entry by construction);
`fits=1` is reported to the gauntlet only for certified schemas, so
the gauntlet's train-fit-only class means "certified fit, wrong test"
and abstentions land in no_fit with their sub-reason in the run log.

## 9. Exceptionality gate (brief)

1. **Conventional approach / why insufficient:** v1 measured it — a
   preserve-or-delete correspondence language converts at 0/48 on
   fresh tasks because ARC's rules predominantly transform objects
   and resize grids (46/48 deaths in the two reach classes).
2. **New mechanism:** derivation-based correspondence — exact-cover
   accounting over a transformational derivation grammar (split,
   merge, grow, mirror, scale, copy/frame creation) with grid scale
   as a pre-transform and canvas rules — identified by intersection,
   certified by the v1-validated LOO gate. Neither the derivation
   grammar nor cover-based identification exists in any prior lane.
3. **Verification strength above norm:** pre-registered gates (§8)
   before the run; two positive controls targeting exactly the new
   machinery plus a negative control; per-task sub-reason taxonomy
   (§6) that separates "grammar cannot express it" from "grammar
   over-generates" (F5) from "certification rejected it"; seed
   selected on a freshness rule fixed before the lane existed.
4. **Cheapest decisive falsifier:** this probe — one CPU draw, 60
   tasks, $0. F2 (0 solves) kills the design outright.
5. **Independent path that could prove it wrong:** the unmodified
   gauntlet on a B/C-fresh draw; pool C as algebra-shadow detector
   (F4); the negative control detects solving noise.
6. **Compounding asset:** the derivation/candidate machinery and the
   cover solver are reusable by any successor; the §6 taxonomy is a
   measured map of which transformation classes remain unaddressed,
   ranked — the next design starts from data.
7. **Obligation closed if it succeeds:** the campaign's central open
   obligation — *any* nonzero, certified conversion on fresh real ARC
   tasks — closes, now over a schema language that covers the two
   classes that killed 46/48 of v1's draw.

## 10. Honest distance statement

An ALIVE verdict here is single-digit conversion on 48 fresh tasks
against a 90% acceptance criterion; §5 names classes (parameter-object
semantics, relational placement, general creation) that this grammar
does not touch and that ARC-AGI-2 certainly contains. Nothing in this
probe, whatever its outcome, demonstrates a path to 216+/240 — it
measures whether the identification discipline converts at all once
the language admits what the tasks actually do. (ESTIMATE, labeled:
the §6 taxonomy from this run, not this document, sizes what remains.)
