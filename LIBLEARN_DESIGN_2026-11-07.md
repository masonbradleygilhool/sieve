# LIBLEARN — Design Paper (2026-11-07)

**Status: DESIGN ONLY.** No code is built, no slice is sampled, no
draw is taken, no exam is spent by this document. It designs
SIEVE's successor species #2 so the campaign is ready on either
outcome of the EXEC-SYNTH conversion gate: a gate **KILL** makes
LIBLEARN the live design question (gate preregistration §5), and
a gate **SEAT-ONLY** opens LIBLEARN Stage-1 registration in
parallel (§5, packet branch logic). A gate PASS with prior
evidence leaves this paper on file, unfired, behind the packet §1
sequence. Every number below is quoted from a repo document named
at the line; nothing is projected to the 240-task scale except the
ceiling arithmetic of §4, which is stated as arithmetic, not as a
forecast.

**Definition source.** The mechanism is taken from
`SIEVE_REDESIGN_COMMISSION_2026-11-07.md` §3, Candidate 2,
verbatim where it defines:

> A DreamCoder-style species: a small, fixed, Turing-complete-
> enough program DSL (grid primitives, object operations,
> iteration) shared by all tasks, with a *library* of abstractions
> learned by compression over solutions found on pool B tasks
> themselves, and a learned recognition model guiding search.
> Identification of a task's program is by search scored on
> fold-execution (C2/C3), not by intersecting a hand-built version
> space. The bg component is a DSL primitive stage (C4).

**Standing requirement (unchanged):** approval only by Sealed
Approval Exam #1 at **216/240**, under its protocol. Approved
solvers: **zero**. Exam #1: **unspent**. The frozen certification
(`friday_bigmodel_kit/harness/certify.py`) is not amended by this
design.

**Constraint compliance (commission C1–C8).** C1: every
species-level claim is measured on a fresh draw; spent material
diagnoses and trains, never authorizes (§3). C2: selection is by
fold-execution, never version-space unanimity (§1.4). C3: the
design states in advance why its fits should survive fold
re-induction (§1.6). C4: the searched-account background component
is adopted as a fixed DSL primitive stage, never a seat (§1.1).
C5: no neural component is scaled before a supply measurement —
the recognition model is trained only on banked search traces
inside the registered build and is measured first at Stage 1, on
held-out tasks, before any fresh draw (§3). C6: creation reach is
stated by class, in advance, from the measured anatomy (§2); no
machinery is specified against any spent task. C7: species draws
are B-only (§3.3). C8: bars are the packet's, quoted before the
run, or explicitly labeled **[design-registered]** where this
paper adds one (§3).

---

## 1. The mechanism, stated exactly

### 1.1 Representation: one fixed base DSL, shared by all tasks

The base language is a small set of typed primitives over ARC
grids, fixed before any learning and never extended during a
registered run:

- **Grid primitives:** color maps, crops/pads, rotations/
  reflections, translations, overlays, canvas-size functions
  (output dimensions computed from input features, not assumed).
- **Object operations:** segmentation under an account (below),
  object lists with map/filter/fold, per-object transforms,
  object sort/select by measured features (size, color, bounding
  box, symmetry), stamping/tiling of an object at a computed set
  of placements.
- **Iteration and arithmetic:** bounded iterate/fold over object
  lists and over integer ranges, integer arithmetic on measured
  features (counts, extents, quotients) — enough for
  count-parametric and compression/quotient constructions.
- **The background stage (C4, fixed infrastructure):** the
  packet §2.2 searched-account component as a primitive stage —
  background proposed from the generator set {modal, border-modal,
  corner-color, sea}, identified once per task by cross-pair
  intersection over the 32 accounts, the binding inherited by
  every downstream stage and every certification fold
  (`BG_GATE_RESULTS_2026-11-07.md`: migrated 15/17, bg deaths
  17/48 → 2/48, fits 4/4 preserved; `CENSUS_UPDATES_2026-11-06.md`
  §4: fold-local re-identification is determinate on **0/938**
  pool tasks, so inheritance is not a choice but the measured
  requirement).

A **program** is a compositional term over the base primitives
plus the current library (§1.2). A task is *fit* iff its program,
executed, reproduces every train pair's output exactly — the
campaign's standing execution definition of fit.

### 1.2 The library: what a learned abstraction is

A **library entry** is a named, typed function from DSL terms to
DSL terms — an abstraction extracted from solution programs, with
explicit argument slots (grid, object, color, integer, point,
function). Granularity: one entry per reusable *construction* —
e.g. "stamp object X at all positions selected by predicate P",
"emit the quotient grid of partition Π under classifier c",
"draw the lattice segment between two marked points" — not per
task and not per primitive. Entries are the only learned part of
the language; the base DSL (§1.1) never changes.

An entry is admitted when adding it (with its own definition
cost) **reduces the total description length** of the corpus of
solution programs found so far — the DreamCoder compression
criterion. The library is therefore a statement about the pool:
it contains exactly the constructions whose reuse across solved
pool tasks pays for their definition.

### 1.3 Induction: how the library is learned from solved tasks

Wake–sleep over a **registered training population** (§3.1):

- **Wake (search):** for each training task, recognition-guided
  enumerative search (§1.5) over programs in base DSL + current
  library, scored by fold-execution (§1.4). Every fitting program
  found enters the solution corpus with its full search trace.
- **Sleep–abstraction:** the corpus is refactored — recurring
  subterms are anti-unified into candidate library entries;
  entries passing the compression criterion are admitted; corpus
  programs are rewritten over the enlarged library.
- **Sleep–recognition:** the recognition model is retrained on
  (task features → program/entry usage) pairs from the corpus
  traces, so the next wake phase searches the enlarged language
  with a prior concentrated on entries the pool actually uses.

Nothing in this loop ever sees a falsifier task: the training
population and all future falsifier populations are disjoint by
registration (§3.1), and the loop's inputs are banked files and
its own traces only.

### 1.4 Application to a fresh task; selection by fold-execution

For a fresh task: (i) the background binding is identified once,
on all train pairs, by the fixed §1.1 stage and inherited
everywhere; (ii) the recognition model proposes a prior over
base primitives and library entries from the task's pairs;
(iii) enumerative search under that prior generates candidate
programs; (iv) candidates are scored by **fold-execution** — for
each train pair held out in turn, the candidate must have been
derivable and must predict the held pair; the selection score is
the candidate's held-pair predictive record, and the top
candidate by that score is the task's submission to
certification. Selection never consults agreement among
candidates (C2): a program found once with a perfect fold record
beats a program found forty times with a flawed one. This is
EXEC-SYNTH's selection discipline (commission §3, Candidate 1)
carried into a symbolic language — the one selection mechanism in
the program with a measured supply behind it (canary: 6/24
execution-verified fits, `EXEC_SYNTH_RESULTS_2026-11-07.md`).

### 1.5 The recognition model

A learned mapping from task-pair features to a distribution over
library entries and base primitives, trained exclusively on
wake-phase traces (§1.3). It guides enumeration order only; it
cannot propose a program that execution has not verified, and it
is not a proposer in the Friday sense — the closed species
(grid-text propose-then-verify, 0 fits in 432 completions,
commission §1.2 L5) is a different interface and stays closed.
Its cost discipline is C5's: it exists only inside the registered
build and is first measured at Stage 1 (§3.2).

### 1.6 Where execution-verification and the frozen certification sit

Unchanged, in the campaign's standing positions:

- **Execution-verification** is the fit test at every stage:
  search candidates, library corpus programs, and fold candidates
  are all judged by executing them against train pairs in the
  sandbox discipline (the gate kit's harness pattern). No text is
  believed; only executions count.
- **The frozen certification** (`friday_bigmodel_kit/harness/
  certify.py`, unmodified) is the conversion instrument at
  Stage 2, applied criterion-for-criterion exactly as the
  conversion gate applies it to EXEC-SYNTH (gate preregistration
  §4): full fit; LOO — for every fold, the fold candidate set's
  prediction on the held input is exactly the singleton {held
  output}; the shape-diverse-holdout classification; prediction
  unanimity over full-fit programs on every test input. The one
  substitution is the candidate source — certify.py's own
  substitution, registered there and here once: fold candidates
  are produced by re-running the registered LIBLEARN search on
  the fold task (train minus the held pair), with the library and
  the background binding **frozen and inherited**, never re-learned
  per fold. Test outputs are never in the instrument.
- **Why its fits should survive fold re-induction (C3, stated in
  advance):** the two measured killers of certification are
  (a) fold-local re-identification of quantities that are not
  fold-determinate — background determinate on 0/938 folds
  (`CENSUS_UPDATES` §4); LIBLEARN re-identifies *nothing* per
  fold except the final program, and both the binding and the
  library are full-task/full-corpus objects inherited by folds;
  and (b) selection by criteria indifferent to fold dynamics —
  the survivor census priced 58/64 rejecting folds as
  certification dynamics (parents correct on held pairs, fold
  re-induction failing) under version-space selection
  (commission §1.1). LIBLEARN's selection score *is* the fold
  record (§1.4): a candidate is chosen because it already
  predicted held pairs under re-derivation. If fits still die at
  certification at Stage 2, that is the species' kill signature,
  registered as such in §5 — not a surprise to be explained after
  the fact.

---

## 2. Why this species attacks the measured wall

The current death taxonomy, charged identically across the
bg-lane, creation-lane, and fresh-probe runs (denominator 48):

| Death class | Spent draw, post-BG-GATE (`BG_GATE_RESULTS`) | Fresh draw (`FRESH_PROBE_RESULTS`) | LIBLEARN's reach |
|---|---|---|---|
| creation_unexplained | **19** | **22** | **Primary target** — §2.1 |
| budget | 15 | 10 | Direct — recognition-guided search (§2.2) |
| cover_failed | 2 | 4 | Partial — object operations + learned cover constructions |
| canvas | 2 | 4 | Partial — canvas size is a computed function in the DSL (§1.1) |
| search_cap / inconsistent_phi / inconsistent_param | (inside the 19-class re-charge; fresh: 2 / 2 / 0) | 4 combined | Enumeration artifacts of the old schema machinery; in a term-search language they collapse into the budget class |
| loo_rejected / nondeterminate (fits dying at certification) | fits 4, certified 0 (bg lane); creation lane spent: 11 fits, 0 certified | 4 fits: 3 loo_rejected, 1 nondeterminate | Aimed at by construction (§1.6); kill signature if it repeats (§5) |
| background | 2 (from 17) | — (component carried) | **Not a research direction** (C4): fixed component adopted; the 2 unbound tasks (f4081712, c803e39c) are the family's measured residue (commission §5) |

### 2.1 Creation, class by class (anatomy of the spent 19)

`CREATION_WALL_ANATOMY_2026-11-07.md` §1–§2 charges the 19 spent
creation deaths: **Q** quotient/compression 5 · **L** line/ray
drawing 3 · **R** replication/stamping/tiling 3 · **F** frame
generalization 2 · **S** symmetry completion 1 · **M**
mirror-tiling 1 · **C** count/multiset-parametric 1 · **T**
procedural texture 1 · **P** part-selective split 1 · **G**
color-class gather 1. (Census corroboration that creation is the
pool-scale wall, not a draw artifact: of the 113 pool tasks the
bg account search rescues, **all 113 carry novel created
content**, 726 novel instances of 1,950 created —
`CENSUS_UPDATES_2026-11-06.md` §5; background identification is
necessary for every one, sufficient for none.)

LIBLEARN's reach over these classes is **by construction type,
not by per-class machinery** (C6 prohibits the hand-specified
alternative — the creation build's M-Q…M-P machinery is exactly
the prohibited move, and its fresh reading is the reason: spent
creation deaths 19 → 8 at home, **22/48 abroad**):

- Every class above is a *program shape*: Q is partition +
  per-block classification; L is a lattice-segment construction
  between identified endpoints; R is stamping at a computed
  placement set; F/M/S are frame, reflection, and completion
  constructions over objects; C is arithmetic over measured
  counts; T is a periodic-domain extraction; P is a selective
  split; G is a whole-color-class pattern source. Each is
  expressible as a composition of §1.1 primitives — and, once the
  training corpus contains solved instances, compressible into a
  library entry that makes the shape cheap to find on the next
  task. The hand-built grammar also expressed most of these
  shapes; its failure was not expression but *identification and
  transfer* (point U = 0/11 on the extended grammar; fits 11/48
  spent → 4/48 fresh). LIBLEARN's claim is narrower and different:
  abstractions priced by compression over the pool's own 938
  tasks are the pool's recurring shapes, not a designer's anatomy
  of 19 — so they are the shapes with pool-scale frequency behind
  them, and fold-execution selection (§1.4) replaces the
  version-space identification whose U the census measured.
- **The honest limit, stated in advance:** a class with no solved
  instances in the training corpus yields no library entry, and
  the base DSL alone must carry it at enumerative cost (the
  budget class). Class reach is therefore an empirical quantity,
  priced per class at Stage 0/Stage 1 (§3) — the design claims
  the *mechanism* reaches creation as a category; it does not
  claim any class's frequency transfers until the census in §3.0
  reads it.

### 2.2 Budget deaths

15/48 (spent, post-bg) and 10/48 (fresh) die at the search
budget — the second-largest class on both draws. A learned
recognition prior is the direct attack: enumeration concentrated
on entries with measured pool frequency reaches fitting programs
in fewer expansions than the old lane's schema enumeration. The
Stage-2 readout charges budget deaths separately, against these
two baselines; a LIBLEARN lane whose budget deaths do not fall
materially below 10/48 has failed this part of its premise on
measurement, whatever its fits.

### 2.3 What this species cannot touch

- **Tasks outside the base DSL's expressiveness.** If no term of
  base DSL + any library fits a task's train pairs, no search
  finds one. This is a *bound*, measurable over the pool before
  any build (§3.0) — the analogue of the census bounds that
  closed the hand grammars (modal account 808/938; searched
  accounts 921/938; `CENSUS_UPDATES` §2).
- **The 69/938 tasks admitting no functional background binding
  at all** (`CENSUS_UPDATES` §1) — the adopted component's
  measured ceiling, inherited, not improvable by the library.
- **Underdetermined tasks.** Where the train pairs do not
  determine a unique test prediction under any correct program
  (the certification's `ambiguous` / nondeterminate charges), no
  solver species converts the task; that is a property of the
  task, not of the lane.
- **The certification itself.** LIBLEARN faces it unchanged
  (§1.6). A species-level answer of "route around it" is
  prohibited by C3 and by the commission's standing invariants.

---

## 3. The first falsifier

Three stages, in order, each cheaper than the next thing it
protects. Stages 1 and 2 are the commission's own falsifier,
quoted; Stage 0 is added by this design and labeled
**[design-registered]** — it is the §4 ceiling question asked
*before* the build, at $0, in the census tradition that closed
both hand grammars without spending a draw.

### 3.0 Stage 0 — pool expressiveness census (pre-build, $0, local CPU)

Before any library learning is built:

- **Instrument:** a necessary-condition pass in the
  `census/census_param_bound.py` pattern over all 938 pool-B
  tasks: does the task admit *any* account under §1.1's staged
  representation (background binding functional ∧ segmentation
  viable ∧ created content classifiable within the base DSL's
  construction types)? Plus, on the spent draws' banked fits, a
  survivor-set-style census of what fold-execution selection over
  DSL terms would face — the F × U analogue for this language,
  with undecided cases completed both ways, as the survivor
  census completed them (`SURVIVOR_SET_CENSUS_2026-11-04.md`:
  ceiling under every completion).
- **Bars [design-registered]:** if the pool-level fit bound for
  the base DSL reads **< 0.90** of pool B, or the F × U analogue
  reads **< 0.90 under every completion**, the species is
  ceiling-bound exactly as its predecessors were, and it closes
  **here** — no build, no slice, no draw. (The old grammar died
  of precisely this reading: F × U ≤ 0.982 × 0.857 = 0.842.)
  A pass authorizes only Stage 1's registration.
- A secondary readout, reported but not a bar: the per-class
  creation census — for each anatomy class Q/L/R/F/S/M/C/T/P/G,
  how many pool tasks' created content falls in the class and how
  many *solved-able* instances the training population (§3.1)
  holds. This prices §2.1's honest limit before the build leans
  on it.

### 3.1 Training population (registered before the build)

The library may learn only from: **(a)** the spent union — every
pool-B id already consumed by a registered run (312 ids through
the canary; **360** once the conversion gate's 48 are spent —
the gate draw is disjoint from the 312 and joins the union when
it fires); and **(b)** a **training slice** of the untouched
pool, drawn and listed in the Stage-1 preregistration before the
build starts. Slice and all spent ids are excluded from every
future falsifier draw, permanently. *(Correction to the
commissioning brief's arithmetic, stated once: the brief sums
"312 + canary 24 + gate 48 = 384 spent ids"; the canary's 24 are
already inside the 312 (312 = 288 + 24, gate preregistration
§2.1), so the distinct post-gate spent union is **360**, and the
untouched pool after the gate is 938 − 360 = **578**, from which
the training slice and all falsifier draws are taken.)*
Design proposal for the slice size, to be filed exactly in the
Stage-1 preregistration: **240 tasks** — large enough for
compression to find pool-frequency shapes, leaving ≥ 338
untouched ids for Stage 2 (48), its one registered repeat (48),
and later confirmation draws. Stage 1's **held-out slice** is
drawn from the same registered training population: tasks the
library did not learn from, listed in advance.

### 3.2 Stage 1 — supply on held-out training-adjacent tasks (the commission's stage 1, verbatim bar)

From the commission §3, Candidate 2:

> *Stage 1 (supply, spent-pool only):* after a bounded
> library-learning run over a registered training slice of pool B
> (tasks disjoint from all future falsifier draws, listed in the
> preregistration), the solver must fit ≥ 50% of a held-out slice
> of *training-slice-adjacent* pool tasks it did not learn from.
> Below that, the library is not compressing anything real; the
> build stops before any fresh draw is spent.

Design additions, labeled: the held-out slice is **48 tasks**
**[design-registered]** (bar: ≥ 24/48 fit), so the reading carries
the campaign's standard width; and the Stage-1 readout charges
the full death taxonomy, with creation and budget broken out
against §2's baselines — a Stage-1 pass with creation deaths at
fresh-probe proportions (22/48) is reported as a pass at
supply strength with its premise already failing, and the desk
reads it as such. **A Stage-1 pass is a component verdict on
training-adjacent tasks. It authorizes Stage 2 and nothing else;
under L1 it is not capability evidence** (the creation build
passed every spent-draw criterion it was set and read 4/48
fresh).

### 3.3 Stage 2 — fresh-draw conversion gate (the commission's stage 2, verbatim bars)

- **Draw:** 48 tasks, pool B only (C7), from the untouched ids
  remaining after §3.1's exclusions. **Draw discipline:** the
  legacy smallest-seed full-pool search is measured-infeasible at
  this width (exact hit probability C(626,48)/C(938,48) =
  1.986e-09 against the 312 union; worse against 360 — gate
  preregistration §2.1), so the draw uses that filing's admitted
  mechanism: the untouched entries in `gauntlet/pools.json` order,
  sampled at the immediate successor of the last spent seed with
  gauntlet.py's consumption pattern (rng.sample, then
  rng.shuffle), disjointness from the full spent union **and**
  the training slice asserted in code at draw time, after the
  replication gate (all spent run records replicated exactly —
  id sets and order — before sampling, per C1).
- **Protocol:** registered search budget per task (25 s/task-
  equivalent discipline, as every lane in this program);
  fold-execution selection (§1.4); frozen certification
  unchanged (§1.6).
- **Bars (commission §3, Candidate 2, verbatim):** seat (b)'s
  supply line — **≥ 20/48 fits with conversion ≥ 1/18** — or
  seat (a) — **≥ 4/48 certified**. **KILL: fits < 10/48** on the
  fresh draw, **or 0 certified with fits ≥ 10** — the second
  clause is the commission's own: "0 certified with fits ≥ 10
  (L3 repeating itself in a new grammar closes the grammar family
  at every level, permanently)."
- **Middle band [design-registered, campaign pattern]:** fits
  10–19 with ≥ 1 certified but neither seat line met = WEAK:
  exactly one repeat gate on a disjoint 48 as a separate
  commission, same bars; a repeat WEAK or KILL closes the
  species. (The campaign's standing middle-band pattern — the
  canary's and BG-GATE's both permit exactly one re-test; the
  conversion gate's WEAK band registers the same.)

### 3.4 Rail and cost

Stage 0: local CPU, $0, hours. Stage 1: local CPU (search +
compression); the recognition model optionally on Kaggle L4×4 —
no GPU is committed before Stage 1's slice is registered
(commission §3). Stage 2: local CPU. Cost to first *species*
measurement is the build itself — **weeks, not days** (commission
§3) — which is precisely why Stages 0 and 1 stand in front of it:
Stage 0 can close the species for the price of a census, and
Stage 1 can stop the build before any fresh draw is spent.

---

## 4. The ceiling question, answered with arithmetic

The requirement is 216/240 = **0.90** on the sealed exam. For any
species whose conversion instrument is the frozen certification,
the exam-scale identity is:

**score rate = F × (C/F)**, where F = fit supply (fraction of
tasks fit at all) and C/F = certification survival of fits —
each factor ≤ 1, so **F ≥ 0.90 is a necessary condition at exam
scale even under perfect certification survival**, and jointly
F × (C/F) ≥ 0.90. Reference points on that curve: F = 0.95 needs
C/F ≥ 0.947; F = 0.92 needs C/F ≥ 0.978; F = 0.90 needs C/F = 1.

Where the measured program stands against that arithmetic:

| Species | Fresh fit supply F | Conversion C/F | Product |
|---|---|---|---|
| Derived grammar (census) | F measured 0.208; U (identification) 9/28 = 0.321 conservative | ceiling F × U ≤ 0.982 × 0.857 = **0.842** | < 0.90 — unreachable by any identification procedure |
| Creation-extended grammar | 11/48 spent → **4/48 = 0.083 fresh** | 0/4 fresh; point U 0/11 spent | ceiling product **0.535** |
| LLM proposer (Friday) | 0/48 | — | 0 |
| EXEC-SYNTH (canary, uncertified supply) | 6/24 = 0.25 | conversion gate pending | — |

So LIBLEARN matters only if it moves **both** factors off the
grammar family's readings: fit supply from the fresh 0.083–0.25
band toward the ≥ 0.90 the identity demands, and certification
survival from the measured **0** (every grammar lane, every draw)
to a rate that keeps the product at 0.90. The staged bars are
honest waypoints on that arithmetic, no more: Stage 1's ≥ 50%
held-out fit rate is a *training-adjacent* reading (L1 discounts
it by an unmeasured factor — the creation lane's spent→fresh fit
ratio was 11:4); Stage 2's seat lines (≥ 20/48 = 0.417 fits at
conversion ≥ 1/18, product ≈ 0.023; or ≥ 4/48 = 0.083 certified)
are **evidence of conversion life, not of exam reach** — the same
statement the conversion gate's §5 makes about its own PASS. The
distance from a seat to 216/240 is the packet §1 sequence
(integration, confirmation draw at its registered trajectory
gate, economics dry run, freeze), and it is walked only by a
seated lane.

**Evidence that would show the ceiling is below 0.90 before any
large spend** — all $0 or build-internal, all registered above:
(i) Stage 0's pool fit bound for the base DSL < 0.90, or its
F × U analogue < 0.90 under every completion (§3.0) — the exact
instrument that closed the derived grammar at 0.842; (ii) the
Stage-0 per-class census showing the creation mass concentrated
in classes where the training population holds no solved
instances — the library then has nothing to compress for the
dominant class, and the design's §2.1 premise fails on paper;
(iii) Stage 1 held-out fits < 50% — the library is not
compressing anything real (commission's words); (iv) inside the
build, a compression plateau: library growth stops reducing
corpus description length while held-out fits stay flat — the
pool's shared structure is exhausted at that level, and further
build is spend without a mechanism.

---

## 5. Kill criteria for the species, and the closure statement

**The species closes, permanently, on any of:**

1. **Stage 0:** pool fit bound < 0.90 for the base DSL, or the
   F × U analogue < 0.90 under every completion (§3.0).
2. **Stage 1:** held-out fits < 50% after the registered
   library-learning run (commission's bar) — the build stops;
   one redesign of the *learning loop* (not of the bars) may be
   re-registered once, at the desk's call; a second Stage-1
   failure closes the species.
3. **Stage 2 KILL:** fresh fits < 10/48, or 0 certified with
   fits ≥ 10 — the second clause closing the grammar family at
   every level, permanently (commission §3).
4. **Stage 2 repeat:** a WEAK repeat landing WEAK or KILL (§3.3).

**Closure statement.** A Stage-2 pass at either seat line seats
LIBLEARN exactly as the packet seats any lane: seat (a) ≥ 4/48
certified earns the Stage-T candidate-source standing; seat (b)
≥ 20/48 fits at conversion ≥ 1/18 earns the seat via fit supply;
in either case the lane becomes an **exam candidate in
preparation** and the packet §1 sequence is commissioned as its
own filing, under the packet's own gates. A pass approves **no
solver**, spends **no exam**, and projects **nothing** to 240.
The sealed exam remains the only approval instrument, at
216/240, and it is spent exactly once, on a frozen candidate,
by separate order — or not at all.

---

## 6. Confidence, and the strongest argument against

**Honest confidence label: LOW** — the lowest of the commission's
three candidates that remains unclosed, stated at design
strength. The mechanism is coherent, its constraints are met on
paper, and every one of its premises is currently unmeasured
where it matters (fresh draws). Its ranking (second) is the
commission's, and this paper does not raise it.

**The strongest argument against, stated fairly:** LIBLEARN may
be a machine for re-measuring L1 at build cost. The campaign's
deepest measured regularity is that artifacts shaped by a corpus
read worse off it — fits 11/48 on the build draw, 4/48 fresh, for
the identical lane — and a learned library is the most
corpus-shaped artifact the program has ever proposed. The pool
evidence cuts the same way: all 113 bg-rescued tasks still
carried novel content (`CENSUS_UPDATES` §5) — pool B's tasks
demonstrably share *background* structure while their *content*
stays task-specific, and a library compresses only what recurs.
If ARC's content structure is as near-sui-generis per task as
that join suggests, the library compresses the training corpus
beautifully, passes Stage 1 on training-adjacent tasks, and dies
at Stage 2 having spent weeks to learn what the creation
probe's 540 seconds already said. Add the standing alternative:
EXEC-SYNTH's Python interface already contains an implicit
library — the model's pretrained knowledge of program
constructions — and it posted the program's first supply pass
(6/24) in two hours of rail time. LIBLEARN must therefore win on
*certification survival and search economics*, the two places a
symbolic fold-execution lane can in principle beat sampled code
— or it should not be built at all. Stages 0 and 1 exist so that
this argument gets its cheapest possible hearing before the
weeks are spent.

---

## Sources (all on disk in `~/workspace/arc_apex2/`)

`SIEVE_REDESIGN_COMMISSION_2026-11-07.md` (definition §3
Candidate 2; lessons L1–L5; constraints C1–C8; Stage-1/Stage-2
bars) · `CONVERSION_GATE_PREREGISTRATION_2026-11-07.md` (§2.1
pool arithmetic and draw mechanism; §4 certification criteria
and the candidate-source substitution; §5 routing on KILL and
SEAT-ONLY) · `EXEC_SYNTH_RESULTS_2026-11-07.md` (canary PASS
6/24; Groq TPD instrument fact) · `NOVEMBER_CONVERSION_PACKET.md`
§0 (seat standards, evidence clauses), §2.1 (bg wall 17/48 and
subtypes), §2.2 (component specification), §2.3 (BG-GATE) ·
`BG_GATE_RESULTS_2026-11-07.md` (15/17 migrated; re-charged
taxonomy: creation 19, budget 15, cover 2, canvas 2, bg 2) ·
`FRESH_PROBE_RESULTS_2026-11-07.md` (KILL: certified 0/48, fits
4/48; fresh taxonomy: creation 22, budget 10, cover 4, canvas 4;
fits' certification deaths 3 loo_rejected + 1 nondeterminate) ·
`CREATION_WALL_ANATOMY_2026-11-07.md` §§0–2 (the 19 spent
creation deaths by class: Q5 L3 R3 F2 S1 M1 C1 T1 P1 G1) ·
`CENSUS_UPDATES_2026-11-06.md` (§1 69/938 no functional binding;
§2 modal 808/938, searched 921/938; §4 LOO determinacy 0/938;
§5 rescue 113/130 = 86.9%, all 113 carrying novel content, 726
novel instances of 1,950) · `SURVIVOR_SET_CENSUS_2026-11-04.md`
(U = 9/28 = 0.321; ceiling F × U ≤ 0.842; 58/64 folds class (b),
via commission §1.1).

*End of design paper. Filed 2026-11-07. No slice sampled, no
draw taken, no code built, Exam #1 unspent.*
