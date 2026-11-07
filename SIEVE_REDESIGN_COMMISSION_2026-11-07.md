# SIEVE — Redesign Commission (2026-11-07)

**Status: DESIGN ONLY.** No code is built, no draw is sampled, no exam is
spent by this document. It designs the next solver program from the
measured closures of every previous one. Every number below is quoted
from a repo document named at the line; nothing is projected to the
240-task scale anywhere in this document.

**Standing requirement (unchanged):** approval only by Sealed Approval
Exam #1 at **216/240**, under its protocol. Approved solvers: **zero**.
Exam #1: **unspent**.

---

## 1. The failure map

### 1.1 The four closures

| # | Species | Instrument | Headline numbers | What exactly died |
|---|---|---|---|---|
| 1 | Derived grammar + version-space identification (Stage-V conversion over the hand-built grammar) | Survivor-set census over the 28 spent A+B full-fit tasks of the three derived-grammar probes (`SURVIVOR_SET_CENSUS_2026-11-04.md`) | Conservative **U = 9/28 = 0.321**; unanimous∧correct **1/28** (8 of 9 unanimous version spaces unanimously *wrong*); ceiling **F × U ≤ 0.982 × 0.857 = 0.842 < 0.90** under every completion of the undecided cases; fit supply F measured **0.208** | The conversion mechanism itself: over this grammar, 216/240 is unreachable by *any* identification procedure, including perfect ones. Fold rejections were mostly certification dynamics (17/19 tasks, 58/64 folds class (b)) — and removing them still loses, because the surviving constraint is the version spaces' content: plural where they should force (4/13 determined), unanimously wrong where they do force (8/9). |
| 2 | gpt-oss-120b LLM proposer, standalone (grid-text propose-then-verify, Kaggle L4×4) | Friday measurement, pre-registered draw seed 22979062, A+B = 48 (`BG_GATE_PREREGISTRATION_2026-11-07.md` §1, recording the closed seat test; bars in `NOVEMBER_CONVERSION_PACKET.md` §0) | **C1a-med 0/24 fits + C1b-med 0/24 fits = 0/48 fit-bearing, 0 certified**; instrument healthy — **287/288 medium completions finished 'stop'**, 0 fits across all 288; the high-effort arm before it also 0 fits (144 completions, 93.8% truncated — retired by the medium arm); per-sample fit rate **< ~1% over 432 completions** | The proposer as a standalone solver seat, at every tested effort. Neither seat clause (≥4/48 certified; ≥20/48 fits at conversion ≥ 1/18) nor either evidence clause (unanimity; conversion ≥ 10 × 1/28) came within range of firing — there was no supply to convert. Closed jointly with P3's completed gate, per the packet. |
| 3 | Searched-background-identification component (packet §2.2) inside the v2-line lane | BG-GATE, spent A+B 48, pre-registered bars (`BG_GATE_RESULTS_2026-11-07.md`) | **PASS: migrated 15/17** (bar ≥ 13/17), **background deaths 2/48** (bar ≤ 5/48, from 17/48), **banked fits preserved 4/4**; solved **0** before and after; full-fit coverage unchanged 4/48 | Nothing died — and that is the finding. The component cleared its wall completely and converted nothing: the 15 migrated tasks died at the next walls (creation_unexplained 8, budget 5, cover_failed 1, canvas 1); none reached certification, none fit. Background identification is a *solved component* whose solution is not a solver. (Pool-scale corroboration, `CENSUS_UPDATES_2026-11-06.md`: account search rescues 113/130 = 86.9% of modal-account bound failures, and **all 113 rescued tasks carry novel created content** — background identification is necessary for every one, sufficient for none.) |
| 4 | Creation-extended grammar (bg component + creation machinery M-Q…M-P) | Build gates on the spent 48 (`CREATION_BUILD_RESULTS_2026-11-07.md`), then the fresh-draw conversion probe, seed 22988303 (`FRESH_PROBE_RESULTS_2026-11-07.md`) | Build: PASS on spent — fits **11/48**, unblocking 11/19, budget deaths 13/48, M-G/M-S cut at 0/1; but G0 re-measurement: extended **point U = 0/11** (determined-only 0/5), **ceiling product 0.535 < 0.90**, **2 of 5 determinate fits unanimous-and-WRONG**, certified **0**. Fresh probe: **KILL — certified 0/48, fits 4/48** (A 0/12, B 4/36), conversion 0.000 vs the ≥ 10 × 1/28 ≈ 0.357 bar, creation deaths **22/48 fresh** vs 19/48 spent | The successor lane as a species. Machinery specified against the spent draw migrated that draw (creation deaths 19 → 8 on the re-run) and did not transfer: on untouched tasks fits collapsed to a third of the spent reading and the creation wall stood at least as large as before the build. Only 1 of the 4 fresh fits came through a creation mechanism at all. |

### 1.2 The shared lessons, as measured facts

- **L1 — Fits do not transfer off their build draw.** Spent-draw
  fit-bearing 11/48 → fresh-draw 4/48 for the identical lane
  (`CREATION_BUILD_RESULTS` vs `FRESH_PROBE_RESULTS`). The creation
  build's spent-draw migration (19 → 8 creation deaths on its own
  draw) measured 22/48 on fresh tasks. Every species in this program
  that was tuned, specified, or gated against a spent draw read
  materially better on that draw than on any fresh one.
- **L2 — Determinate unanimity is unreliable wherever it has been
  measured.** Old grammar: unanimous∧correct **1/28**, with 8 of 9
  unanimous version spaces unanimously wrong — including two
  single-schema spaces: complete determinacy, wrong answer
  (`SURVIVOR_SET_CENSUS_2026-11-04.md` §ii). Extended grammar:
  unanimous∧correct **0/5** determinate fits, with **2 of the 5
  unanimous-and-wrong** (`CREATION_BUILD_RESULTS_2026-11-07.md`, G0).
  On the fresh draw, unanimity was not even measurable: 0 of 4 fits
  determined, 0 sample-unanimous tasks (`FRESH_PROBE_RESULTS`).
  Agreement inside a version space is evidence about the space's
  shared bindings, not about truth.
- **L3 — Certification rejects everything the grammar lanes
  produce.** Certified solves: **0** on the v2 probe draw (4 fits),
  **0** on the bg-lane draw (4 fits), **0** on the creation lane's
  spent draw (11 fits), **0** on the creation lane's fresh draw
  (4 fits), **0/48** for the proposer. The program's single certified
  solve (ad38a9d0) predates all four closures. The survivor census
  priced why: 58/64 rejecting folds were certification dynamics
  (class (b)) — parents correct on held pairs, fold re-induction
  failing — and the residue is version spaces that are plural or
  wrong (L2). A lane whose fits cannot survive its own certification
  has no conversion path, whatever its supply.
- **L4 — Background identification is solved as a component and
  converts nothing alone.** 15/17 migrated, bg deaths 17/48 → 2/48,
  fits 4/4 preserved, solves 0 → 0 (`BG_GATE_RESULTS`). At pool
  scale the same shape: rescue 113/130 with all 113 still carrying
  novel created content (`CENSUS_UPDATES_2026-11-06.md` §5).
  Additionally, fold-local re-identification of the background
  binding is determinate on **0/938** pool tasks — the binding must
  be identified once, on all pairs, and inherited by folds
  (ibid. §4). The component is infrastructure. It is not a seat.
- **L5 — The proposer species supplies no fits at any tested
  effort.** 0 fit-bearing tasks of 48 at medium effort on a healthy
  instrument (287/288 completions finished 'stop'); 0 fits in 288
  medium completions; the 144-completion high-effort arm likewise 0.
  Combined per-sample fit rate < ~1% (0/432). Whatever a future
  neural component is, "ask the model for candidate grids/programs
  and verify" in this interface has a measured supply of zero to
  build on.

---

## 2. Design constraints on any successor

Each constraint is numbered and traceable to the lesson(s) that
impose it. A candidate that violates one is not a candidate.

- **C1 — Fresh-draw-first evaluation.** *(L1)* No spent-draw result
  may authorize a build, a scale-up, or a seat claim. Spent draws
  diagnose components only (the BG-GATE's registered use). Every
  species-level claim is measured on a fresh draw, sampled under the
  campaign's registered seed rule (smallest seed whose B draw is
  disjoint from all spent B draws, verified by offline replication
  of every spent run record before the lane runs).
- **C2 — Identification must not rest on version-space unanimity.**
  *(L2)* Unanimity may be reported (with denominators and its Fisher
  p against 1/9, in the packet's language) but may not be the
  selection mechanism. Selection must be grounded in execution:
  held-pair prediction, fold re-derivation, or an equivalent
  check that can disagree with the majority of the version space.
- **C3 — Certification is part of the design target, not an
  afterthought.** *(L3)* The frozen LOO-determinacy certification
  is not amended, weakened, or routed around — it is the exam's
  local shadow. A design must state, before its first run, *why its
  fits should survive fold re-induction* (e.g. identification done
  once and inherited by folds, per L4's 0/938 measurement; or
  selection scored on the folds themselves). A species whose only
  answer is "more supply" fails this constraint on the record:
  supply rose 4 → 11 on the spent draw and certified stayed 0.
- **C4 — The bg component is adopted as infrastructure, never as a
  solver seat.** *(L4)* Any grammar-bearing successor inherits the
  §2.2 searched-account background stage (15/17, 2/48, fits 4/4) as
  a fixed stage, the way it inherits segmentation. No future gate
  may be a background gate; that wall is measured and cleared.
- **C5 — Any neural component passes a supply canary at small width
  before any scale.** *(L5)* A canary is a small fresh-draw
  measurement (≤ 24 tasks) whose only question is whether the
  component produces *any* verifiable supply (execution-checked
  fits) at a rate distinguishable from the Friday null. No GPU week,
  no integration build, and no second canary at a bigger width is
  authorized by anything but a canary pass at its pre-registered bar.
- **C6 — Creation is a first-class requirement, priced in advance.**
  *(L1, L4)* The largest death class on every recent draw is
  creation (19/48 spent post-bg; 22/48 fresh). A candidate must
  state which creation classes (anatomy Q/L/R/S/M/F/C/T/P/G) its
  mechanism reaches *by construction*, and its falsifier's taxonomy
  must charge creation deaths separately. Hand-specified creation
  machinery aimed at a spent draw's 19 tasks is prohibited as a
  design move: that is precisely the build that measured 11/19 at
  home and 4/48 abroad.
- **C7 — Draws are B-only at species level.** Pool A has **18 tasks,
  all spent** across the eight historical draws; no fresh A arm
  exists (`FRESH_PROBE_PREREGISTRATION_2026-11-07.md` §3). Species
  falsifiers draw from pool B's **686 untouched ids** (938 − 252
  spent union, ibid.). A-arm results, where a mixed draw is run for
  comparability, are reported separately and never carry a verdict.
- **C8 — Bars are the packet's, quoted before the run.** Seat
  standards, evidence clauses, and verdict bands are taken from
  `NOVEMBER_CONVERSION_PACKET.md` §0 (seat (a) ≥ 4/48 certified;
  seat (b) ≥ 20/48 fits at conversion ≥ 1/18; conversion clause
  ≥ 10 × 1/28 guarded to ≥ 10 fits; unanimity clause ≥ 8 judgeable
  with ≥ 3/4 correct, Fisher p printed) or explicitly registered as
  new bars in the candidate's own preregistration before sampling.
  A qualification is stated once, in the preregistration, and does
  not move after the run.

---

## 3. Candidate species

Three candidates, ranked. Costs are to *first measurement* — the
cheapest decisive falsifier — not to a finished solver.

### Candidate 1 — EXEC-SYNTH: execution-verified code synthesis *(non-grammar)* — RANK 1

**What it is.** A large language model writes a *Python transform
program* for the task, not a grid and not a grammar derivation. The
program is executed against the train pairs; execution errors and
mismatching cells are fed back for a bounded number of repair rounds;
programs that fit all train pairs exactly are ranked by a
fold-execution score (fit on k−1 pairs, exact-predict the held pair,
over all folds) and the top program is submitted to the **frozen
certification unchanged**. The bg component (C4) is available to the
synthesizer as a callable pre-stage (background map identified once,
on all pairs, inherited by folds — per L4), not as a seat.

**Which lessons it answers.** L2/C2: selection is execution on held
pairs, never agreement among samples — a program the sampler
produces once beats a wrong program it produces forty times. L3/C3:
fold-execution scoring *is* the certification's dynamics, run inside
selection instead of after it. L5/C5: the Friday null was measured
on the grid-text/proposal interface; this candidate changes the
interface (code + execution feedback), and the canary below exists
precisely to test whether the null was the interface or the model —
cheaply, before anything is built on the answer. C6: code is not
bounded by a hand grammar's kinds; strokes, stamps, counts, and
quotients are all expressible without a per-class mechanism, and no
machinery is specified against any spent task.

**Cheapest decisive falsifier — supply canary (pre-registered).**
- *Draw:* 24 tasks, pool B only, from the 686 untouched ids, seed =
  smallest seed whose B draw is disjoint from all 252 spent B ids
  (replication-verified before sampling, per C1/C7).
- *Protocol:* gpt-oss-120b via the Groq API (the user's account;
  1,000 requests/day/model), k = 8 samples per task, ≤ 3
  execution-feedback repair rounds per sample; local CPU execution
  in a sandbox, 25 s/task-equivalent budget discipline; a task is
  *supplied* iff ≥ 1 sampled program fits all its train pairs
  exactly under execution.
- *Bars:* **PASS ≥ 4/24 supplied** (against the same model's measured
  0/48 on the proposal interface — a supply difference at this size
  is the interface hypothesis surviving its cheapest test).
  **KILL ≤ 1/24 supplied** — the species closes at the canary and
  the model-null is interface-independent at this scale. 2–3/24 is
  the named middle: exactly one repeat canary on a second disjoint
  24 is permitted; a second middle closes it.
- *What a pass earns:* the conversion gate — the identical pipeline
  on a fresh 48 (B-only), frozen certification unmodified, packet
  seat bars quoted verbatim (seat (a) ≥ 4/48 certified; conversion
  clause ≥ 10 × 1/28 guarded to ≥ 10 fits; unanimity reported, never
  used for selection). A gate pass is a lane verdict in the packet's
  sense; it approves no solver and spends no exam (§4).

**Rail and cost to first measurement.** Groq API: ≤ 24 × 8 ×
(1 + ≤ 3 repairs) ≈ ≤ 768 requests worst case — inside one day's
1,000-request cap for the model; local CPU execution. **$0, ≤ 1 day.**
No Kaggle quota is touched until a canary pass exists.

### Candidate 2 — LIBLEARN: cross-task library learning over a minimal program DSL *(learned grammar)* — RANK 2

**What it is.** A DreamCoder-style species: a small, fixed,
Turing-complete-enough program DSL (grid primitives, object
operations, iteration) shared by all tasks, with a *library* of
abstractions learned by compression over solutions found on pool B
tasks themselves, and a learned recognition model guiding search.
Identification of a task's program is by search scored on
fold-execution (C2/C3), not by intersecting a hand-built version
space. The bg component is a DSL primitive stage (C4).

**Which lessons it answers.** The census located the binding
constraint exactly: "any future mechanism must attack grammar
expressiveness / shared-wrong bindings, not conversion"
(`SURVIVOR_SET_CENSUS_2026-11-04.md` §iii). The old grammar's kinds
were hand-written and its ceiling was arithmetic (F × U ≤ 0.842).
A learned library attacks expressiveness with the pool's own 938
tasks as evidence instead of a designer's 19-task anatomy — the
anti-C6-violation: abstractions are learned from the pool, not
specified against a spent draw. L1 is answered structurally: the
library is trained on pool tasks and *evaluated only on disjoint
fresh draws*; nothing in the build loop ever sees a falsifier task.

**Cheapest decisive falsifier (pre-registered).** Two-stage, because
the build is the cost:
- *Stage 1 (supply, spent-pool only):* after a bounded library-
  learning run over a registered training slice of pool B (tasks
  disjoint from all future falsifier draws, listed in the
  preregistration), the solver must fit ≥ 50% of a held-out slice of
  *training-slice-adjacent* pool tasks it did not learn from.
  Below that, the library is not compressing anything real; the
  build stops before any fresh draw is spent.
- *Stage 2 (conversion):* fresh 48, B-only, seed rule per C7; frozen
  certification; bars = seat (b)'s supply line (≥ 20/48 fits) with
  conversion ≥ 1/18, or seat (a) ≥ 4/48 certified. **KILL:** fits
  < 10/48 on the fresh draw (the creation lane's fresh supply was
  4/48; a learned grammar that cannot beat hand-built supply on
  fresh tasks has no premise), or 0 certified with fits ≥ 10
  (L3 repeating itself in a new grammar closes the grammar family
  at every level, permanently).

**Rail and cost to first measurement.** Local CPU (search +
compression) with the recognition model optionally on Kaggle L4×4.
Cost to first measurement is the build itself: **weeks, not days** —
this is why it ranks below a candidate whose falsifier costs a day.
No GPU is committed before Stage 1's slice is registered.

### Candidate 3 — DIRECT-NEURAL: direct neural prediction with test-time augmentation, canary-gated *(non-grammar)* — RANK 3

**What it is.** A grid-to-grid neural model (small transformer over
cell tokens, dihedral test-time augmentation with fold-consistency
voting) trained on synthetic task generators plus pool B train pairs,
predicting test grids directly. No grammar, no version space, no
proposer interface.

**Which lessons it answers — and the record against it.** It answers
L2/L3 by construction (no unanimity, no fold re-induction of a
symbolic program; certification is replaced by the gauntlet's own
exact-match scoring under the exam protocol's discipline — this
candidate, alone of the three, would need its certification
treatment registered explicitly, because the frozen LOO
certification is defined on induced programs; the honest form is:
direct prediction is scored, and its "certification" is the
fresh-draw gate itself, stated once in its preregistration). The
record against it is local and measured: the campaign's own neural
flagship scored 0/40 on the ARC Prize 2026 public set, and the
program has never measured a direct-neural exact-match supply above
zero on any draw. It is ranked third and canary-gated hardest for
exactly that reason.

**Cheapest decisive falsifier — hard supply canary (pre-registered).**
- *Draw:* 24 tasks, B-only, untouched ids, seed rule per C7.
- *Protocol:* a bounded training run — **≤ 6 GPU-hours** on Kaggle
  L4×4 from the banked quota — synthetic generators + pool train
  pairs only, no falsifier-task exposure; prediction with the
  registered augmentation/voting scheme, exact-match scoring.
- *Bars:* **PASS ≥ 2/24 exact test solves.** **KILL 0/24** — the
  local precedent holds and the species closes for the price of the
  canary. 1/24 is a kill at this width as well (a single solve is
  inside every measured null's noise in this program's history);
  it is named a kill in advance so it cannot be negotiated upward
  after the run.
- *What a pass earns:* one 48-task fresh-draw gate at seat (a)'s bar
  (≥ 4/48 certified-equivalent exact solves) before any further
  training spend. Nothing else.

**Rail and cost to first measurement.** Kaggle L4×4: ≤ 6 GPU-hours
of the ~11.3 banked this week (18:42 of the 30-hour weekly quota
used at the C1b close, desk record) — the canary is sized so its
kill leaves the week's rail substantially intact. Local CPU for
data generation.

### Ranking, in one paragraph

EXEC-SYNTH first because its falsifier is the cheapest decisive
measurement in the program's history (≤ 1 day, $0, no GPU) aimed at
the exact ambiguity L5 leaves open (interface vs model), and because
its selection mechanism is the only one that answers L2 and L3 by
construction rather than by repair. LIBLEARN second because it is
the only candidate that attacks the constraint the census actually
located (expressiveness / shared-wrong bindings) — but its first
measurement costs a build, so it does not go first while a one-day
canary is unrun. DIRECT-NEURAL third because its local precedent is
a measured zero and its canary is priced accordingly: it earns
attention only by surviving a test designed to kill it cheaply.

---

## 4. The commission

**Recommended sequence.**

1. **EXEC-SYNTH supply canary** (Candidate 1), preregistration filed
   before sampling, B-only 24 under the seed rule. Desk decision
   point **D1**: the canary's verdict — PASS fires step 2; KILL
   closes the species and fires step 3; the named middle permits
   exactly one repeat canary.
2. **EXEC-SYNTH conversion gate**: fresh 48 (B-only), frozen
   certification, packet seat bars. Desk decision point **D2**: a
   gate PASS makes the lane an *exam candidate in preparation* —
   the packet §1 sequence (integration pre-checks, confirmation
   draw, economics dry run, freeze) is commissioned as its own
   filing, under the packet's own gates. A gate KILL closes the
   species; the record joins §1's table.
3. **LIBLEARN Stage-1 registration** (Candidate 2) — commissioned
   when the EXEC-SYNTH line closes (either way), or in parallel once
   the canary has passed and the gate is running, at the desk's
   call (**D3**). Its build is authorized only with its training
   slice and Stage-1 bar filed in advance.
4. **DIRECT-NEURAL canary** (Candidate 3) — fires only if a Kaggle
   week carries ≥ 6 spare GPU-hours after the EXEC-SYNTH gate's
   needs are met (**D4**); its kill is final and cheap, its pass
   earns exactly one 48-task gate.

**Standing invariants (no desk decision may waive them).**

- **Exam #1 stays unspent** until a species passes its fresh-draw
  conversion gate at packet bars. No canary, build gate, or
  spent-draw result of any strength spends it, moves it, or is
  described as exam evidence.
- **Approval is by the exam alone, at 216/240.** A species that
  passes every gate in this document is an exam *candidate*, never
  an approved solver.
- **No number is projected to 240** from any draw, canary, census,
  or ceiling — in either direction. Ceilings (0.842, 0.535) are
  recorded as properties of the closed grammars they were measured
  on, not as forecasts about unbuilt species.
- **The frozen certification is not amended** by any candidate in
  this commission. Where a species cannot face it as defined
  (Candidate 3), that fact is registered in its preregistration,
  once, and its gates carry the difference openly.
- **Every run files its preregistration before sampling** — bars,
  seed rule, draw composition, verdict bands, and the consequence
  of each band. A result without a prior filing is a diagnostic,
  never a verdict.

---

## 5. What not to do — the dead, with their closure citations

Never re-pitched, in any form, under any new name:

- **The derived/hand-built grammar + version-space identification
  lineage** (all iterations: derived grammar, iteration-2 search
  economics, intersection lane, Stage-V conversion). Closed by the
  survivor-set census: U = 0.321 conservative, unanimous∧correct
  1/28, F × U ≤ 0.842 < 0.90 under every treatment
  (`SURVIVOR_SET_CENSUS_2026-11-04.md`).
- **The gpt-oss-120b proposer as a standalone solver or as a
  grid/program proposal source in the Friday interface.** Closed
  flat null at full pre-registered width on a healthy instrument:
  0/48 fit-bearing, 0 certified, 0 fits in 432 completions across
  efforts (`BG_GATE_PREREGISTRATION_2026-11-07.md` §1;
  `NOVEMBER_CONVERSION_PACKET.md` §0/§2). (Candidate 1 is a
  different interface — code under execution feedback — with its
  own canary; it inherits nothing from this species but its model,
  and its canary is designed to close it too if the null was the
  model.)
- **Any wider hand-built grammar extension aimed at a spent draw's
  death taxonomy** — including further creation machinery in the
  M-Q…M-P line. The creation build passed every one of its own
  spent-draw kill criteria and its fresh-draw probe returned KILL:
  0/48 certified, fits 4/48 vs 11/48 spent, creation deaths 22/48
  fresh (`CREATION_BUILD_RESULTS_2026-11-07.md`;
  `FRESH_PROBE_RESULTS_2026-11-07.md`). Extending it further is
  re-running the measured failure with more machinery.
- **Background-identification work as a research direction.** The
  component passed (15/17; `BG_GATE_RESULTS_2026-11-07.md`) and is
  adopted as infrastructure (C4). There is no next background gate.
  The two unbound tasks (f4081712, c803e39c) are the family's
  measured residue, not a research program.
- **Any lane that keeps background = modal color as an
  identification assumption.** It inherits a measured ~35%
  death ceiling (17/48) before it starts
  (`NOVEMBER_CONVERSION_PACKET.md` §2.1).
- **The published-TRM lane and the 2026 neural flagship line** —
  closed earlier in the campaign and not reopened by anything in
  the current record; Candidate 3 is a separate, canary-gated
  species and may not be built as a revival of either.
- **Spending Exam #1 on anything but a frozen candidate that has
  passed a fresh-draw conversion gate at packet bars** — including
  spending it "to see where we stand." The exam is single-use; a
  measurement taken with it is the approval measurement or it is a
  waste of the only instrument that can approve.

---

## Sources (all on disk in `~/workspace/arc_apex2/`)

`NOVEMBER_CONVERSION_PACKET.md` (seat standards, branch logic,
bg wall §2.1) · `SURVIVOR_SET_CENSUS_2026-11-04.md` (U, ceiling,
(b)/(c) split) · `CENSUS_UPDATES_2026-11-06.md` (rescue 113/130,
LOO determinacy 0/938, novel content in all 113) ·
`BG_GATE_PREREGISTRATION_2026-11-07.md` §1 (Friday flat null:
0/24 + 0/24, 287/288 'stop') · `BG_GATE_RESULTS_2026-11-07.md`
(15/17, 2/48, 4/4, solved 0) · `CREATION_WALL_ANATOMY_2026-11-07.md`
(19 tasks, classes Q/L/R/S/M/F/C/T/P/G — surviving portion; the file
is truncated on disk mid-§2-S, §§3–5 absent, as flagged in
`CREATION_BUILD_RESULTS_2026-11-07.md`) ·
`CREATION_MACHINERY_SPEC_2026-11-07.md` (mechanisms, probe design,
kill criteria) · `CREATION_BUILD_RESULTS_2026-11-07.md` (fits 11/48,
U-extended 0/11 and 0/5, ceiling 0.535, two unanimous-and-wrong,
M-G/M-S cut) · `FRESH_PROBE_PREREGISTRATION_2026-11-07.md` (pool
arithmetic: A = 18 all spent; B spent union 252, 686 untouched;
seed rule) · `FRESH_PROBE_RESULTS_2026-11-07.md` (KILL: 0/48
certified, fits 4/48, creation deaths 22/48 fresh).
