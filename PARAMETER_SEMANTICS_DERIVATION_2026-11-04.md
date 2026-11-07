# Parameter Semantics for the APEX-2 Grammar — Derivation and Census Bound

**Date:** 2026-11-04. **Status:** paper commission complete. No solver code was
written and no probe was run; this document derives the missing component of
`APEX2_ARCHITECTURE_DERIVATION_2026-11-04.md` (parameter-addressed creation and
counting, routed to abstention there) and recomputes the grammar's census
bound with the component included. The build of any solver is gated on the
number in §0/§6.

**Standing label.** Every bound figure in this document is a *necessary
condition* in the census sense: a per-pair candidate-existence test under one
task-consistent segmentation/background account, a task passing iff all its
train pairs pass. For any grammar containing the tested components,

> census bound ≥ actual full-fit reach ≥ certified solves,

because certification (leave-one-out re-induction, shape-diverse hold-out)
only subtracts, and because the bound — like the census's own bounds — tests
content candidacy, never placement. A bound below a target kills a grammar on
paper. A bound above a target authorizes a build and a probe; it certifies
nothing about solves.

---

## 0. The number and the verdict

Full-grammar census bound (parameter semantics included; background treated
per the v2 finding, §4/M1), same necessary-condition methodology as the
architecture derivation:

| grammar | pool B (938 tasks) | eval-120 |
|---|---|---|
| v1 language | 123 / 938 = **13.1%** | — |
| v2 grammar (derivation) | 654 / 938 = **69.7%** | 79 / 120 = 65.8% |
| **full grammar + parameter semantics** | **921 / 938 = 98.2%** | **119 / 120 = 99.2%** |

Robustness (pool B; every variant is the same bound with the named credit
removed or restricted — details in §6):

| variant | bound |
|---|---|
| headline | 921 (98.2%) |
| minus copies / minus field / minus const / minus parameter kinds | 914 / 905 / 917 / 911 |
| field credit restricted to objects of ≥ 9 cells | 912 (97.2%) |
| parameter + field kinds both removed | 887 (94.6%) |
| parameter + field + copy kinds all removed | 860 (91.7%) |
| modal-background account only (no account search) | 808 (86.1%) |

The bound clears 90% on both populations, and clears it under every ablation
and sensitivity computed, including the variant that strips both components
this document adds (field, parameter) and the variant that strips copies as
well. **Verdict: the bound gate is passed. The build specified in §7 is
authorized** — components, order, and the pre-registered probe protocol of
the derivation's §6, including its fixed seed rule. This verdict authorizes
building a *candidate* and probing it. It does not approve a solver: approval
remains the standing law — a sealed fresh-task measurement replicating
private-eval conditions at 90%+ — and no figure in this document is a solve
rate, a fit rate, or a forecast of either.

The residual uncovered mass is named in §8 even though the gate cleared:
17 pool-B tasks (1.8%) fail every account, and all 17 sit inside the
novel-creation mass.

---

## 1. What a parameter object is

### 1.1 Scenes and accounts

A *scene* is one train pair's input grid together with an *account*: a
segmentation σ ∈ {primary (per-color 4-connected, background removed),
agnostic (8-connected non-background)} and a background generator for inputs
and for outputs (§4/M1). Everything below is defined relative to a fixed
account. Bindings derived under different accounts are never mixed; a task's
schema lives inside one account.

### 1.2 The parameter basis Π

A *parameter* is a named, total function of the input scene, drawn from a
closed basis Π. Π is fixed by the grammar, not learned:

- **Canvas scalars:** `grid_h`, `grid_w`.
- **Population scalars:** `n_obj` (object count under σ), `cells_nonbg`,
  `cells_bg`.
- **Per-color scalars** (for each color c ∈ 0..9): `cells_color_c` (cells of
  color c), `obj_color_c` (objects whose color set is exactly {c}).
- **Extremal object scalars:** `obj_max_cells`, `obj_min_cells`,
  `obj_max_bh`, `obj_max_bw`, `obj_min_bh`, `obj_min_bw`.
- **Run scalar:** `run_max`, the longest horizontal or vertical run of one
  color in the input.
- **Multiset scalars:** for every multiset of object cell-counts of size
  ≤ 3 occurring among the input's objects, `cm_<hash>` = the number of
  objects whose cell count belongs to that multiset. These are the counting
  parameters: "the number of objects of size s", for the sizes the scene
  itself exhibits.

Π is deliberately small (order 10² functions). A value not named by Π is not
a parameter of this grammar; content addressed by it is outside the component
(§3 sizes what that exclusion costs).

### 1.3 Parameter derivations

A *parameter derivation* is a pair (G, β):

- **G**, a *generator* from the family
  - `RECT(h, w)` — filled rectangle;
  - `FRAME(h, w)` — rectangle border (h, w ≥ 3 for a non-degenerate frame);
  - `PLUS(h, w)` — the plus/cross on an odd bounding box (h = w odd, arms on
    the middle row and column);
  - `DIAG(h, w)` — the two diagonals of the bounding box;
  - `CONST(P)` — a fixed colored pattern P (no free shape parameters);
  - `TABLE` — no fixed shape; content is addressed (§1.5).
- **β**, a *binding*: an assignment of every free component of G — each
  dimension, and the color — to either a literal constant or a parameter
  π ∈ Π. A binding component is therefore one of `θ = const` or `θ = π`.

A parameter derivation *renders* content, not placement: given a scene S,
(G, β) determines a colored pattern (evaluate each π on S, substitute,
render G). Where the pattern goes on the output canvas is the business of
the schema's placement/canvas machinery, exactly as for a copied object —
the derivation's cover (§4/M5) treats a parameter derivation and a copy as
the same kind of citizen: a candidate explanation of one leftover object.
This separation is load-bearing: the census bound, here as in the original
census, tests content candidacy only.

### 1.4 Counting is binding, in three forms

There is no separate counting mechanism. A counting rule is a schema whose
bindings mention population parameters:

1. **Count-valued dimension.** A drawn extent equals a count:
   `RECT(h = cm_{sizes}, w = π)` — e.g. a bar whose length is the number of
   objects of a given size. Identified like any dimension binding.
2. **Emission multiplicity.** The schema emits the derivation once per unit
   of a count parameter (the derivation is instantiated `π(S)` times, at
   placements supplied by the canvas machinery). Multiplicity is a property
   of the schema, not of (G, β); at census-bound level it is invisible (the
   bound tests each emitted instance's content separately) and at fit level
   it is identified by the same intersection as any binding: the observed
   instance count per pair must equal π's value in every pair.
3. **Index/table addressing.** §1.5.

### 1.5 Table addressing (glyphs)

Some created content is neither drawn from a shape family nor constant: the
same *address* (a scene parameter's value) selects different content in
different tasks, and within a task the address→content map is the rule. A
`TABLE` derivation is a partial function T from address values (values of a
named π ∈ Π) to colored patterns, induced by the train pairs. It is a
parameter object in the strict sense: the content is *addressed by* a
parameter rather than copied or drawn. Its identification conditions are the
strongest in this component (§2, step 5): T must be *functional* on the
train pairs (no address value maps to two different patterns) and must
*bind* (some address value recurs across pairs with the same pattern);
otherwise the "table" is a memorized list and the derivation is not
identified. Single-pair tasks can never identify a TABLE derivation.

---

## 2. Identification procedure

Identification runs inside one account, mirroring the derivation's M5 with
the parameter layer inserted. For a task with train pairs (S₁→O₁), …,
(S_k→O_k):

1. **Fates first.** The derivation's staged fate matching runs unchanged.
   Parameter derivations are candidates only for *leftover* output objects —
   content no fate, copy, ring, mirror, symmetry, or field candidate
   explains. (At bound level all candidates are tested per leftover; at fit
   level they compete in the cover, step 6.)
2. **θ read-off.** For each leftover object in pair j, and each generator G
   whose rendered shape can equal the object, read off the object's realized
   θ-vector (h, w, cells, colors). This is exact and cheap: the generator
   family is recognized from the pattern itself (a filled rectangle is a
   RECT; a border-only rectangle is a FRAME; etc.), and a pattern matching
   no generator and no CONST candidate yields no parameter candidate.
3. **Candidate bindings.** For each θ-component, the candidate binding set
   is {const = the observed value} ∪ {π ∈ Π : π(S_j) = the observed value}.
   A color component's candidates are restricted to the scene's own colors:
   a color present in the pair's input is addressed by the palette binding
   (the color *is* a scene value); a color absent from the input has no
   parameter candidate — it can only be a rule constant, which is CONST's
   territory at pattern level (step 4), failing which the object is
   *unaddressed* (§3/L3).
4. **CONST by recurrence.** A leftover pattern is a CONST candidate iff its
   colored pattern recurs as an output object in at least one other train
   pair of the task. Recurrence is the identification: a pattern seen once
   is indistinguishable from free creation (§3/L3). (The census tool counts
   CONST credit for patterns of ≥ 3 cells by default; the bound's
   sensitivity to that threshold is §6.)
5. **TABLE by functionality + binding.** Glyph-eligible leftovers (small,
   single-color, non-generator patterns) across all pairs are grouped by
   candidate address π: the induced map value→pattern must be functional
   across pairs and at least one value must repeat with the same pattern.
   One π must serve the whole task.
6. **Cover competition.** All candidate derivations — fates, copies, field,
   CONST, drawn, TABLE — compete in the derivation's exact cover, which
   minimizes (creations, deletions, bindings) lexicographically (the v2
   probe's recorded selection correction is retained: lexicographic minimum,
   not first-found). A parameter derivation whose binding set, intersected
   across all pairs it serves, is empty dies with sub-reason
   `inconsistent_param` — the slot the derivation's §6.5 already reserves.
7. **Certification unchanged in form, extended in scope.** Leave-one-out
   re-induction re-derives β from k−1 pairs: a binding supported by a single
   pair is exactly what LOO exposes. The shape-diverse hold-out applies to
   size-valued bindings unchanged (a dimension binding that only ever saw
   one scene shape is the F1 canvas ambiguity in parameter form). The
   schema's determinacy report is extended with *binding status*: for each
   bound component, whether its cross-pair name intersection is a singleton
   (unique), plural (tied), or empty (inconsistent). Ties are reported,
   never silently resolved by a prior.

---

## 3. Identifiability limits — named and sized

Each limit is a statement about identification strength, measured on pool B
under the modal account unless stated. These limits bound what the built
solver may claim from a fit; they do not lower the census bound (a bound
counts candidacy), and §6 keeps the two apart.

**L1 — Binding ties are the norm, not the exception.** For every
witness-bearing primitive signature (generator, dims, cells, colors) in the
census data, intersect the candidate parameter names across its occurrences.
Of 2,196 signatures: **180 (8.2%) have a unique binding name, 1,909 (86.9%)
are tied** (two or more distinct parameters agree on every train scene),
**107 (4.9%) are name-inconsistent** (no single parameter fits all
occurrences — those derivations are dead at fit level). A tied binding is a
genuine identifiability limit: π₁ ≠ π₂ as functions, equal on all k train
scenes, diverging off-sample. The grammar's answer is procedural, not
statistical: ties are carried into the determinacy report, and LOO +
shape-diverse hold-out (§2 step 7) is the only discriminator. Any build that
resolves ties by plausibility has left this semantics.

**L2 — Small k.** Intersection strength is bounded by the number of scenes.
Pool B: **k = 2 for 146 tasks (15.6%)**, k = 3 for 542 (57.8%), k ≥ 4 for
250 (26.6%). On a 2-pair task, a binding is an intersection over two scenes;
L1's tie rate is the average case, and 2-pair tasks sit at its weak end.
Nothing in the component repairs this; it is priced by certification.

**L3 — Single-occurrence constants are unidentifiable, and new colors are
mostly that.** A pattern, or a drawn primitive in a color absent from the
pair's input, that occurs in exactly one pair carries no evidence
distinguishing "rule constant" from "free creation". Measured: of the 1,884
census-novel instances, **419 (22.2%) are drawn primitives whose color is
not scene-addressed and whose pattern does not recur** (class
`primitive_unaddressed_color`, §5). The semantics does not cover them at
identification strength. Their tasks mostly still pass the bound through
other kinds or other accounts — which is a statement about the bound, not
about these instances.

**L4 — Generator degeneracy off-sample.** The generator family is not
injective at small sizes: `RECT(2,2)`, `FRAME`-degenerates, `PLUS(1,1)`,
`DIAG(1,1)` coincide as patterns. Read-off (§2 step 2) therefore returns a
*set* of generators at small sizes, and the cover + certification arbitrate.
This is L1 in shape form; it is not separately enumerable from the census
data and is stated here at exactly that strength.

**L5 — Content identification is not placement identification.** The bound
never checks where a rendered pattern lands. A schema can have every
binding identified and still misplace every object. The derivation's canvas
component (δ) carries placement; this component neither strengthens nor
weakens it. Fit reach will fall below the bound for this reason alone, as it
did for the v2 grammar (measured fit 8.3% against its 69.7% bound — the gap
is the probe's subject, and no conversion factor between bound and fit is
claimed for the new grammar).

---

## 4. Composition with the derivation's components

**M1 — Segmentation search and the background finding.** Π is
account-relative: object counts and per-color populations differ by
segmentation (the derivation measured 14.5 vs 4.6 objects per pair between
its two account families), so a binding is a statement *inside* an account
and accounts never share bindings. The v2 probe's finding — background is an
identified object, not the modal color (17/48 deaths; the modal-in→modal-out
map is not a function across pairs) — is, in this semantics, the statement
that **the background rule is itself a color binding and must be identified
like one**. The bound operationalizes it as the derivation prescribes
(searched, not assumed): background *generators* {modal, border-modal,
corner-color, sea (largest 4-connected single-color region)} are applied to
inputs and outputs independently, the generator index pair is constant
across a task's pairs, and the bound is taken over all accounts
(2 segmentations × 4 × 4 generator pairs). Measured value of the finding at
bound level: the modal account alone gives 808/938 (86.1%); the searched
accounts give 921/938. Restricting to the primary segmentation alone gives
842/938 (89.8%). The background stage is worth more than any single content
kind added by this document — the v2 probe's retro-diagnosis (its deaths
were segmentation artifacts) is confirmed at census scale.

**M2 — Field layer.** Field derivations and parameter derivations compete
in the same cover for the same leftovers; neither has priority. The bound's
field test is the derivation's field-extend made positional: a leftover is
field-candidate iff, under some dihedral variant of the input, the periodic
continuation of the input field reproduces the leftover's colored pattern
*at its output position* for some phase — and a pair's field-credited
leftovers must share **one** (variant, phase) jointly. (An earlier
position-free version of this test was computed, judged unfaithful to the
mechanism — a per-object free phase is a property of a different, stronger
mechanism not in the grammar — and discarded; §6.) The test's remaining
weakness is measured, not hidden: of the 914 field-credited novel instances,
599 have ≤ 3 cells, and the median instance is consistent with 81 distinct
phases. The joint-phase constraint and the ≥9-cell sensitivity (bound
97.2%, §6) bound how much of the headline this weakness can be carrying.

**M3 — Fates and copies.** Unchanged upstream. Residual copies (a leftover
whose pattern occurs in the same pair's input beyond the count fates
consumed) and cross-pair copies enter the candidate set alongside the
parameter kinds; the census's fate machinery deliberately never credited
them, and the derivation's M3 names cross-pair copy a first-class source.
At bound level copies are the largest single content addition after the
account search (modal ladder, §6).

**M4 — Object-local palette.** The palette gains its binding form: a color
in a parameter derivation is either scene-addressed (present in the pair's
input — the color is a scene value, bound like any π) or pattern-constant
(CONST, §2 step 4). There is no third route, which is exactly L3. The
derivation's measurement that 29.7% of tasks introduce output colors absent
from inputs is thereby split into an identified part (recurrence) and an
unaddressed residue (419 instances, §5).

**M5 — Identification by exact cover.** Form unchanged; the candidate space
grows by the parameter derivations and the death taxonomy gains
`inconsistent_param`. Intersection — the derivation's core identification
move — now runs over bindings as well as over φ/τ/δ choices, with the same
semantics: a candidate that survives alone but whose cross-pair
intersection is empty is dead.

**M6 — Certification.** Unchanged in form; scope extended per §2 step 7.
Determinacy reporting gains binding status (L1's three counts are part of a
schema's report, so a tied binding is visible in every artifact the build
produces).

---

## 5. The novel mass, accounted

Census definitions (fixed by `census/README.md`): under the modal account,
a created instance is *novel* iff it is not a residual copy, not a cross-pair
copy, and not a ring (blind signature). Pool B: 10,405 created instances,
1,884 novel (18.1%), in 254 tasks (27.1%). First-match classification of the
1,884 under the modal account (field = the per-object positional test of
§4/M2; joint-phase satisfiability is enforced at pass level, not per
instance):

| class | instances | share | mechanism |
|---|---|---|---|
| `field_patch` | 914 | 48.5% | field-extend (derivation M2), positional + joint phase |
| `primitive_unaddressed_color` | 419 | 22.2% | drawn shape, color unaddressed — **not covered** (L3) |
| `residual` | 358 | 19.0% | no candidate of any kind — **not covered** (§8) |
| `const_recurrent` | 139 | 7.4% | CONST: pattern recurrent across pairs |
| `witness_tier1` | 49 | 2.6% | drawn primitive, dims bound to a scene scalar/run directly |
| `witness_tier2` | 5 | 0.3% | drawn primitive, dims bound to a sum/difference of two scene scalars |

Task level (254 novel tasks): every novel instance classified by some kind
under the modal account in 140 tasks; classified *purely by the parameter
semantics* (CONST / witness / glyph-table) in 76 tasks; passing the full
bound under at least one account in **237 tasks**; failing every account in
17 tasks (§8). Under the modal account alone, 124 of the 254 pass — the
account search is what carries the other 113.

The parameter semantics proper (CONST + witness + TABLE) classifies
193 + (glyph-eligible pendings) of 1,884 instances directly. Stated plainly:
the drawn-primitive-with-witnessed-dimensions mass is *small* (54 instances
tier1+tier2). The novel mass is dominated by field content (914) and by
content this component does not identify (777 = 419 + 358). The bound
clears 90% because the *grammar as a whole* — accounts, copies, field,
const, parameter kinds together — covers the tasks, not because parameter
addressing alone dissolves the novel mass. Any summary that credits the
headline to "parameter objects" without the decomposition in §6 misstates
this result.

Eval-120 mirror: 1,649 created, 203 novel in 37 tasks; classes: field 134,
residual 55, const 12, unaddressed 2, witness 0. Novel tasks passing: 36/37.

**Residual profile** (the 358 pool-B instances no kind covers): all are
single-color; 207 (58%) have a bounding box exceeding 5 in some dimension;
the size histogram concentrates at large areas (23 instances at the 50-cell
cap, a long tail of 9–20-cell shapes); 151 (42%) are glyph-eligible in shape
but fail the TABLE discipline (no functional, binding address) — they are
the boundary between "addressed content whose address we cannot identify"
and "content addressed by nothing in Π".

---

## 6. The number: methodology, decomposition, validation

**Methodology.** Identical discipline to the census's v2 bound, extended by
the derivation's §6.2 instruction and this commission's terms: per pair,
every leftover must have a candidate among {ring, mirror-union} (v2 kinds)
∪ {residual copy, cross-pair copy, symmetry-union, field (positional, joint
phase), CONST, drawn primitive with witnessed binding, glyph-table pending
(resolved at task level by functionality + binding)} — under **one**
task-consistent account (segmentation × input-bg-generator × output-bg-
generator); split/merge pairs pass as in census.py. Task = all pairs pass.
The v2 component of the test is census.py's own predicate, and the tooling
reproduces census.py *exactly* under the census account (pool B: 10,405
created / 1,884 novel / 254 tasks / v2 bound 654; eval-120: 1,649 / 203 /
37 / 79) — validation, not assumption.

**Decomposition** (pool B, modal account ladder; each row adds one kind to
the v2 kinds): v2 alone 654 → +copy 721 → +field 730 → +const 666 → +param
722 → all kinds, modal account 808 → all accounts **921**. Ablations over
all accounts: minus copy 914, minus field 905, minus const 917, minus param
911. Sensitivities: CONST minimum size 1/2/3/5 cells → 923/921/921/919;
tier1-only witnesses (tier2 arithmetic disabled) → 921 (tier2 carries no
task); field restricted to ≥4-cell objects → 918, to ≥9-cell objects → 912;
field+param removed → 887; field+param+copy removed → 860. Eval-120:
headline 119; minus field 114; minus copy 118; minus param 118; minus const
119; field+param removed → 111; field ≥9 cells → 116.

**Reproduction.** `census/census_param_bound.py` (evaluation, writes
`param_per_task.jsonl`, `param_per_task_eval120.jsonl`) and
`census/census_param_aggregate.py` (aggregation, writes `param_bound.json`;
credit logic imported from the evaluator so the two cannot diverge).
Re-aggregation of the stored per-leftover records reproduces the headline
exactly (921 = 921; 119 = 119). Commands:

```
cd ~/workspace/arc_apex2/census
python3 census_param_bound.py poolB
python3 census_param_bound.py eval120
python3 census_param_aggregate.py
```

**What the number does not say.** It does not say the grammar fits 98.2% of
anything — fit requires the cover, the intersections, and placement to
succeed jointly, and certification then subtracts. It does not rescue the
identification limits of §3. It says exactly: *the full grammar's content
kinds, under searched accounts, leave at most 1.8% of pool B outside
necessary-condition reach* — so the 90% criterion is not arithmetically
dead for this grammar family, the way it was for v1 (13.1%) and v2 (69.7%).
That is the only question a census bound answers, and it is the question
the build gate turns on.

---

## 7. The build this verdict authorizes

Authorized: build the candidate solver implementing the derivation's
architecture with this component included, in dependency order, and run the
pre-registered probe. Not authorized: any claim of capability, any
submission, any relaxation of the probe gates.

**Build order.**

1. **Bound tooling as standing gate** (exists: `census_param_bound.py`).
   Any grammar change re-runs the bound before code; a variant whose bound
   falls below 90% is dead on paper.
2. **Account search (M1 + §4):** dual segmentation × background generators
   {modal, border-modal, corner, sea} for inputs and outputs, generator
   index task-consistent; Π derived per account. Background identification
   is a first-class stage with its own diagnostics (v2's lesson: isolate
   the stage or its failures get misfiled downstream).
3. **Content layer:** staged fates (existing) + candidate generation for
   leftovers: residual/cross-pair copy, ring, mirror-union, symmetry-union,
   field-extend (positional, one phase per pair), CONST, drawn primitives
   with bindings (tier1 + tier2), TABLE.
4. **Identification (M5 + §2):** exact cover minimizing (creations,
   deletions, bindings) lexicographically; binding intersection across
   pairs; `inconsistent_param` death; TABLE functionality + binding checks.
5. **Certification (M6 + §2 step 7):** LOO re-induction including β
   re-derivation; shape-diverse hold-out; determinacy report extended with
   binding status; abstention preserved as a first-class outcome.

**Probe protocol** (the derivation's §6, unchanged): fresh gauntlet draw;
seed = the smallest seed ≥ 20261110 whose B/C draws are disjoint from seeds
20261103 / 20261104 / 20261109; five controls including the abstention
control (a "solve" must fail the set when no schema is determinate); gates
**KILL 0 solves / WEAK 1–3 / ALIVE ≥ 4 of 48 AND full-fit coverage ≥ 30%**;
F1/F3/F4/F5 overrides as pre-registered there; results reported with the
census-class taxonomy (creation / background / parameter / residual classes
named per death), never as a bare score.

---

## 8. The remaining uncovered mass

Named precisely, because a bound of 98.2% is a statement about 17 tasks as
much as about 921:

- **17 pool-B tasks fail every account:** 37ce87bb, 3cd86f4f, 423a55dc,
  54d82841, 6f473927, 8dab14c2, 8f2ea7aa, 973e499e, 9f5f939b, ad7e01d0,
  bc4146bd, c6141b15, d22278a0, d304284e, d5d6de2d, ed98d772, f8c80d96.
  (Eval-120: one task, 45a5af55.) Every one of the 17 is a novel-mass task:
  the grammar's entire bound-level residue lives where content is created.
  Their modal-account blockers are residual instances (31) and
  unaddressed-color primitives (18).
- **The residual class (358 instances)** is free-form single-color content —
  majority large (58% with a bounding-box dimension > 5) — matching no
  generator in the family, not recurrent as a pattern, not a patch of the
  input's periodic continuation, not a copy of anything. The mechanism
  class it would require is a *shape-grammar induction over the residual
  patterns themselves* — a second-order library learned from residuals,
  with its own identification discipline. That is a different component
  than parameter semantics; it is named here as the gap and **not**
  specified, per this commission's terms (no mechanism proposed on spec).
- **The unaddressed-color class (419 instances)** requires either evidence
  this data does not contain (recurrence, scene presence) or a color-rule
  mechanism (colors computed from scene colors by a palette algebra) —
  the derivation's M4 keeps palette mappings object-local and measured a
  consistent global colormap in 0 tasks, so a palette algebra has no
  census support at present. Named, not proposed.
- **Identification-grade residue inside the bound:** binding ties on 86.9%
  of witness signatures (L1) and 146 two-pair tasks (L2) pass the bound
  while carrying weak identification. The probe's certification stage is
  where this residue is priced; if the probe dies, the taxonomy will say
  whether it died here.

---

## 9. Exceptionality gate — this component

1. **Object.** Content *addressed by* scene parameters, separated from
   content *copied from* scene content. The field's pipelines conflate the
   two; the census showed the conflation costs 27.1% of tasks.
2. **Invariants.** A binding is a function of the scene or it is nothing:
   name-inconsistency (4.9% of signatures, measured) kills the derivation;
   nothing is averaged, voted, or prior-weighted anywhere in identification.
3. **Representation.** A closed parameter basis Π + (generator, binding)
   tuples; counting is binding in three forms, not a bolted-on counter.
4. **Operator.** Read-off → intersect → cover → certify; every stage exact.
   The same intersection discipline that identifies φ/τ/δ now identifies β.
5. **Hardware map.** CPU enumeration only; the full bound over 938 tasks is
   minutes-scale CPU. No GPU, no learned model in the identification path —
   the component's cost per verified result is ~zero by construction.
6. **Decisive measurement.** The recomputed necessary-condition bound with
   per-component ablations. Stated plainly: no single new component is
   load-bearing alone — the largest single term is the account search
   (+113 tasks over the modal account), which is the v2 background finding
   operationalized; the parameter kinds are the piece that makes the
   *identification story* complete (CONST/witness/TABLE classify the
   purely-addressed mass and give certification something exact to check).
7. **Frontier consequence.** A grammar family whose paper bound (98.2%,
   ≥ 91.7% under the harshest ablation) clears the 90% criterion the v2
   family failed arithmetically — plus a standing bound tool that kills
   any future variant on paper before a probe is spent on it.

---

*Files: this document; `census/census_param_bound.py`,
`census/census_param_aggregate.py`, `census/param_per_task.jsonl`,
`census/param_per_task_eval120.jsonl`, `census/param_bound.json`. Foundation:
`APEX2_ARCHITECTURE_DERIVATION_2026-11-04.md`, `census/` (census.py,
census_creation.py, per_task.jsonl, creation_split.json, summary.json,
README.md), `NEXTGEN_V2_PROBE_RESULTS_2026-11-04.md`.*
