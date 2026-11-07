# SIEVE — November Conversion Packet (2026-11-06)

**Purpose.** Tonight's Friday measurement (local gpt-oss-120b
propose-then-verify, Kaggle L4 x4, draw seed 22979062, A:12 / B:36 /
C:12) produces a verdict. This packet makes that verdict convert to
the next step **the same night, on either outcome** — no step in
either branch waits on a decision, a meeting, or a new derivation.
Every bar below is either quoted verbatim from the registered kit
(`friday_bigmodel_kit/HARNESS_READY.md`,
`friday_bigmodel_kit/FRIDAY_SAMPLE_STATS.md`) or explicitly labeled
**[packet-registered]** as a new bar this packet fixes before the
fact.

**What is already closed and does not reopen on any outcome tonight:**
the derived-grammar lineage (survivor-set census: conservative
U = 9/28 = 0.321; ceiling F × U ≤ 0.842 < 0.90 under every treatment —
over that grammar 216/240 is unreachable by any identification
procedure, including perfect ones); the frozen certification
(`friday_bigmodel_kit/harness/certify.py`, unmodified in every
branch); Sealed Approval Exam #1 (unspent; threshold 216/240; see
`approval_exam/APPROVAL_EXAM_PROTOCOL_2026-11-04.md`).

---

## 0. The same-night verdict sequence (both branches)

GPU work ends when `bigmodel_run/` is downloaded. Then, desk-local,
$0, in this order (commands verbatim from `HARNESS_READY.md`):

7. `APEX2_HARNESS_CACHE=<bigmodel_run> APEX2_HARNESS_MANIFEST=<pack>/manifest.json APEX2_HARNESS_UNITS=<pack>/units.json APEX2_HARNESS_DIAG=<run>_rows.jsonl python3 gauntlet/gauntlet.py --lane probe_lane:lane --lane-path friday_bigmodel_kit/harness --draw A:12,B:36,C:12 --seeds 22979062 --budget 25 --out-tag friday_proposer`
   → a run record in `gauntlet/runs/`, field-identical to the three
   derived-grammar probe records, plus full-info diag rows.
8½. `python3 friday_bigmodel_kit/sample_version_space.py --cache-dir <bigmodel_run> --tasks-json friday_bigmodel_kit/harness/friday_draw.json --units-json probe_runs/friday_pack/units.json`
   → sample-U, sample unanimous∧correct with its Fisher p against the
   grammar's 1/9, width medians, conversion at supply.
8. Charge every non-solved A+B task one sub-reason (no_fit /
   loo_rejected / shape_loo_rejected / ambiguous / budget /
   not_sampled); append the record to `PROBE_LEDGER.jsonl`; state the
   branch (below) and fire its first step before the night ends.

**Registered bars (verbatim).** Seat standard (`HARNESS_READY.md`):

- **SEAT (a):** ≥ **4/48 certified solves** on A+B → the proposer
  earns the Stage-T candidate-source seat.
- **SEAT (b):** full-fit coverage ≥ **41.6%** of A+B (≥20/48 tasks;
  2× the derived lane's measured 20.8%) at conversion (certified ÷
  full-fit) no worse than the recorded **1/18** → seat via fit supply.
- Otherwise **no seat**: 1–3 certified = WEAK, 0 = KILL for the seat
  question.

Prior-evidence standard (`FRIDAY_SAMPLE_STATS.md`) —
**EVIDENCE FOR A TRUTH-CONCENTRATING PRIOR** fires iff either:

- **unanimity clause:** ≥ **8** sample-unanimous (judgeable) tasks
  with ≥ **3/4** of them correct; the exact Fisher p against the
  grammar's 1/9 is printed with the line (the derivation's example,
  6/8 vs 1/9, computes to **p = 0.013369**), or
- **conversion clause:** certified conversion an order of magnitude
  above the grammar's 1/28 at comparable fit supply — the registered
  operationalization is **≥ 4 certified from ≤ 20 fits**; the
  scale-free reading (conversion ≥ 10 × 1/28, guarded to ≥ 10 fits of
  supply) is printed alongside.

**MERELY-MORE-SUPPLY** fires iff seat-(b) coverage is met (≥ 20/48
full fits on A+B at conversion ≥ 1/18) **without** the prior evidence
above; it earns the proposer only its registered **Stage-V input
seat**. Seat (a) without the unanimity statistics is **ambiguous**
between the two readings and is reported as such.

**Branch selection [packet-registered, applying the two registered
standards]:**

- **BRANCH PASS** — EVIDENCE FOR A TRUTH-CONCENTRATING PRIOR fires
  (either clause). → §1.
- **BRANCH FAIL** — flat null (0 certified; no seat; neither evidence
  line) **or** mere-supply fires. → §2. The species verdict is stated
  jointly with P3's completed gate, as `HARNESS_READY.md` registers:
  flat null closes the LLM-proposer species as a standalone route;
  mere-supply leaves it exactly one Stage-V input seat and nothing
  more.
- Seat (a)/(b) met but neither evidence line fires (and mere-supply
  does not apply): the proposer holds its registered seat at seat
  strength, §1 does **not** fire (the build sequence is gated on
  prior evidence, not on supply), and §2's successor gate fires in
  parallel with the seat exercised inside that architecture.

---

## 1. BRANCH PASS — exam-candidate build sequence

Prior evidence means the proposer's samples concentrate on truth at
a rate the grammar's own version spaces do not (grammar baseline:
unanimous∧correct 1/9 = 11%; conversion 1/28 = 3.6%). The proposer
has earned integration as a candidate source — under the discipline
`NEXT_IDENTIFICATION_DERIVATION_2026-11-04.md` §6 already registers:
its proposals enter the same tables, face the same Stage-A
intersections, the same Stage-B cover, and the same Stage-C frozen
certification; nothing downstream changes and no proposal enjoys a
privilege analytic candidates do not have. The **candidate** for the
sealed exam is the composed solver (identification architecture +
proposer source), never the raw proposer alone.

### 1.1 Serving plan across rails (all fetching is resumable-cache)

- **Kaggle (primary fetch rail).** ~30 GPU-h/week, L4 x4 (96 GB
  VRAM), `serve_config.json` as corrected 2026-11-06:
  tensor_parallel_size=4, cpu_offload_gb=0, max_num_seqs=32,
  max_model_len 32,768, max_completion_tokens_cap 16,384,
  reasoning_effort high; model gpt-oss-120b MXFP4 (load + generation
  proven on H100 2026-11-04, 615/615 weights). **Gate on every
  fetch:** the SMOKE timing extrapolation is read before fetching;
  a fetch whose extrapolated hours exceed the week's remaining
  quota is split at a unit boundary — the cache is resumable and a
  quota cut loses nothing (`HARNESS_READY.md` step 5).
- **Pass B (first charge on the quota after tonight).** Tonight's
  session runs Pass A (APEX2_MAXIDX=14, k=42/unit, breadth). Pass B
  is the same pack unset — full k=128/unit over all 259 units (60
  full-task + 199 LOO folds; pack at `probe_runs/friday_pack/`,
  seals recomputed, LOO leakage PASS). Pass B completes the cache
  tonight's statistics were computed from Pass A's breadth, and is
  the fit-supply base for the integration build's spent-task
  pre-checks. **Scheduled: Nov 7**, inside the same weekly quota,
  split per the gate above if the extrapolation demands it.
- **AMD Developer Cloud MI300X (second fetch rail, on arrival).**
  Credit request submitted 2026-11-04; confirmation expected ~Nov 9.
  On arrival the rail is gated by the same PROBE/SMOKE discipline as
  tonight (load canary first, timing extrapolation read before any
  fetch) and takes the confirmation-draw fetch (step 1.2-4), freeing
  Kaggle's quota for the dry-run step. If the credits have not
  landed by Nov 12, the confirmation fetch falls back to Kaggle and
  the schedule in §1.2 slips by the extrapolation, not by redesign.
- **RunPod (canary only — not a fetch rail).** Held balance $4.23 ≈
  63 minutes of H100 at the $4.01/hr rate actually paid. Single named
  use: one timing cross-check of the frozen candidate's serving
  stack (H100 tok/s vs the L4 x4 figures) inside the freeze week.
  It is not spent on bulk fetching; 63 minutes cannot carry a draw
  and pretending otherwise would corrupt the schedule.

### 1.2 Dated path to a sealed-exam-ready candidate

1. **Nov 6 (tonight).** §0 sequence; verdict lines printed; branch
   declared; Pass B scheduled. *Gate: both verdict lines stated at
   exactly the strength the counts support.*
2. **Nov 7.** Pass B fetch (Kaggle, per §1.1 gate). *Gate: cache
   complete over 259 units or the split point recorded with the
   remainder carried, nothing silently dropped.*
3. **Nov 8–10.** Integration build: `harness/proposer_client.py`'s
   proposer wired as an additional Stage-T candidate source into
   the identification architecture; proposals face Stage-A
   intersection, Stage-B cover, Stage-C certification unchanged.
   *Gate — engineering pre-checks, spent tasks only (adapted from
   `NEXT_IDENTIFICATION_DERIVATION_2026-11-04.md` §5): (i) the one
   certified solve ad38a9d0 still solves and certifies through the
   composed path; (ii) candidate-completeness spot-check — the
   tables lose no candidate the frozen lanes generated on sampled
   spent tasks; (iii) fold integrity — every LOO fold runs the
   identical Stages A+B code path as the main induction; (iv) the
   oracle/null harness controls still read 2/2 and 0/2 through
   `harness/certify.py`. Any pre-check failure is a build defect,
   fixed before step 4; it is never a license to amend a bar.*
4. **Nov 11–14.** Fresh-draw probe of the composed candidate:
   gauntlet protocol unmodified (A:12 / B:36 / C:12, 25 s/task,
   budget 25), seed = smallest seed whose B/C draws are disjoint
   from every spent draw including 22979062, verified by offline
   replication of all spent run records before the lane runs
   (the §5 seed rule). Proposal fetch for the draw rides Kaggle;
   if the AMD rail has landed and passed its canary, it rides AMD.
   *Gate [packet-registered]: ALIVE requires ≥4/48 certified AND
   full-fit coverage ≥30% AND the sample-statistics evidence lines
   re-firing at draw scale (unanimity clause or conversion clause,
   same registered bars) AND zero integration regressions against
   tonight's per-class taxonomy. Below ALIVE, the candidate is not
   frozen; exactly one iteration at the taxonomy's largest class is
   permitted, and Exam #1 stays unspent.*
5. **Nov 15–21.** Confirmation draw, B:96, next seed under the same
   disjointness rule. *Gate [packet-registered]: certified rate on
   the confirmation draw ≥ 85% with unanimous∧correct Fisher p ≤
   0.05 against the grammar's 1/9. This is a trajectory gate, stated
   plainly: no 96-task draw certifies 216/240; it is the last cheap
   falsifier before the single-use exam is spent. Below the gate,
   no freeze; the record states the measured rate and the lane
   returns to its largest class.*
6. **Nov 22–25.** Economics dry run: the frozen-candidate build runs
   a 240-task non-exam set (drawn from the then-remaining unused
   pool under the exam protocol's exclusion discipline — never the
   sealed tasks) under the exam protocol's execution parameters —
   25 s per task, 6,000 s total wall (protocol parameters, to be
   re-pinned to the posted ARC Prize 2027 figures if Kaggle has
   posted them by then, per protocol §4 — re-pinned by that clause
   only, never relaxed ad hoc). *Gate: the full set completes inside
   the total budget on the same serving stack that would run the
   exam; the RunPod H100 canary (§1.1) runs inside this window.
   A wall-clock failure here is a result, not an inconvenience: the
   candidate is not exam-ready and Exam #1 stays unspent.*
7. **Nov 26.** Freeze: candidate artifact (code + configuration +
   serving stack definition) hashed; SHA-256 recorded;
   `approval_exam/verify_seal.py` re-run and required to report the
   seal valid immediately before any exam use. **The candidate is
   sealed-exam-ready on Nov 26 if every gate above has passed.**
8. **Nov 27–30 (window).** Sealed Exam #1 may be run — once, by
   separate order, single-use per protocol §6, result appended to
   `PROBE_LEDGER.jsonl` in the protocol §7 format. This packet's
   commitment is readiness inside November; the run itself spends
   the set and is fired as its own act.

**What Branch PASS does not claim.** Tonight's bars are 48-task
bars. Nothing in this branch projects a 240-task score from them;
the only instrument that certifies 216/240 is the sealed exam, and
it is spent exactly once, on a frozen candidate, after gates 4–6.

---

## 2. BRANCH FAIL — the successor species' first gate, fireable tomorrow

A flat null kills the LLM-proposer species as a standalone route
(joint verdict with P3, §0). Mere-supply leaves it a Stage-V input
seat: tonight's cache is banked either way, and under mere-supply
the fitting texts in `sample_version_space.py`'s report are
harvested into the factored survivor sets as that seat prescribes —
no re-fetch, no new spend. Either way, the successor species does
not start from a wider grammar. The measured record names its first
wall, and the first gate attacks exactly that wall.

### 2.1 The wall, as measured

**Background identification is the single largest death class in
the program: 17/48 = 35%** (`NEXTGEN_V2_PROBE_RESULTS_2026-11-04.md`
§4.1, §6 — measured). The failure is the identification assumption
itself — *background = modal color, mapped by one function* — in
three measured subtypes:

- **Context-dependent output background:** same input background,
  different output backgrounds across pairs (e.g. task 3194b014:
  0→3, 0→4, 0→8) — the output background is plausibly set by scene
  content, or is a drawn panel, not background.
- **Input modal color is not the background:** input modals vary
  while the output background is constant (e.g. 27f8ce4f: 5→0, 7→0,
  9→0, 8→0) — a large colored region out-counts the true background,
  so segmentation is built on the wrong background.
- **Single-pair modal flips:** the map is functional except one pair
  where an object outgrows the background (e.g. 9110e3c5: six pairs
  0→0, one 3→0).

Only 4 of the 17 involve a tied modal color, so tie-breaking is a
minor contributor and is not the mechanism. Any successor keeping
background = most-common-colour inherits this ~35% death ceiling
before it starts. (Corroboration at census scale,
`PARAMETER_SEMANTICS_DERIVATION_2026-11-04.md` M1: the modal account
alone bounds 808/938 = 86.1% of pool B; searched accounts bound
921/938 = 98.2%; primary segmentation alone 842/938 = 89.8%.)

### 2.2 The component, specified concretely (spec only — no build in this packet)

**Background is proposed as an identified object, never assumed.**

1. **Candidate generation (per pair, per grid side).** For each
   train pair, candidate input backgrounds are the values produced
   by the generator set **{modal, border-modal, corner-color, sea}**
   applied to the input grid — modal (most common color),
   border-modal (most common color on the grid border),
   corner-color, and sea (the color of the largest 4-connected
   single-color region) — and candidate output backgrounds are the
   same four generators applied to the output grid. (Generator set
   as operationalized in the parameter-semantics bound, M1.)
2. **Identification by cross-pair intersection.** The background
   rule is a color binding and is identified like one: a
   (input-generator, output-generator) index pair is an **account**;
   the index pair must be constant across the task's pairs, and an
   account survives iff one functional background map under it
   reproduces every pair's generated (input-bg → output-bg) values.
   The map may be a function of an identified scene feature (the
   context-dependent subtype's requirement), where the feature is
   itself read off the pair's segmentation under that account.
   Accounts whose intersection is empty die in set arithmetic,
   before any content candidate is generated under them — the
   Stage-0 discipline over the 32 accounts (2 segmentations × 4 × 4
   generator pairs).
3. **Account-relative segmentation.** Segmentation is performed
   relative to each surviving account; a binding is a statement
   inside an account and accounts never share bindings (M1).
   Downstream induction, cover, and the frozen certification are
   unchanged; the component replaces only the background stage of
   the v2-line lane it is tested in.
4. **LOO discipline.** The background binding is re-identified
   inside every certification fold from the fold's pairs alone —
   the component may not import the full-task background verdict
   into a fold (the iteration-2 fold-seeding guard, applied to
   this stage).

### 2.3 The decisive test (BG-GATE) — fires the morning of Nov 7

The test the record names (`NEXTGEN_V2_PROBE_RESULTS_2026-11-04.md`
§6, item 5, inference): **a bg-fixed lane variant on this same draw
shows whether those tasks then die at cover, creation, or
certification.** Specified fireably:

- **Instrument:** the v2-line lane (`nextgen_probe/ng2_lane.py`
  with its diagnostic `nextgen_probe/diag2.py`), with **only** the
  background stage replaced by §2.2's component. Grammar, caps,
  25 s/task budget, and frozen certification unchanged. Local CPU
  only; no GPU, no Kaggle.
- **Draw:** the v2 probe's own A+B draw (n=48, spent — this is a
  component diagnostic on known tasks, not a capability
  measurement, and it claims none). The 17 bg-death tasks are
  extracted by rule from `nextgen_probe/diag2_rows.json` (the rows
  charged to the background class), not hand-listed.
- **Readout:** the full 48-task taxonomy re-charged with the
  identical taxonomy; for each of the 17, its new death class
  (cover / creation / certification sub-reason / solved) is the
  primary row set.
- **Bars [packet-registered, fixed before the run]:**
  - **PASS:** ≥ **13/17** of the bg-death tasks migrate past the
    background gate (they solve, or die at cover, creation, or
    certification instead) **AND** background-class deaths on the
    full 48 fall to ≤ **5/48** **AND** all 4 of the v2 probe's full
    fits still fit under the new background stage.
  - **WEAK:** 7–12/17 migrate, or background deaths land at 6–11/48
    → exactly one refinement iteration, aimed at the largest
    surviving subtype among the three in §2.1, re-tested on the
    same draw under the same bars. A second WEAK closes the
    component as designed.
  - **KILL:** ≤ **6/17** migrate, **OR** background deaths remain
    ≥ **12/48**, **OR** ≥ 2 of the 4 banked full fits are lost.
    A KILL is a clean result: the modal-assumption diagnosis was
    right about the v2 lane's accounting but the searched-account
    component does not reach the class at lane level, and the
    successor redraws from the re-charged taxonomy's largest class
    with the 17-task migration table as its starting evidence.
- **Sequencing:** BG-GATE fires Nov 7 morning regardless of the
  census update (§2.4) — the update prices the component's ceiling
  but does not gate the test the record already named. Readout and
  verdict are reported the day the run completes, at the strength
  the migration table supports.

### 2.4 Census updates the gate needs from the gauntlet pool (938 tasks)

Computed with the existing census machinery
(`census/census_param_bound.py` over `census/per_task.jsonl` and
`census/param_per_task.jsonl`, pool B = the 938-task frame in
`gauntlet/pools.json`), local CPU, detached, $0. Deliverable:
`census/bg_census_2026-11.json` plus a one-page summary appended to
this packet's run record. Five updates, each cheap because the
per-task substrate already exists:

1. **Generator-pair census.** For every pool-B task, which of the
   16 (input-generator × output-generator) pairs are consistent
   across all of the task's pairs, and under how many of the 32
   accounts the task remains viable. (Banked substrate to extend:
   passing accounts per task — median 4, mean 5.28, p90 12, max 32;
   17 tasks pass none.)
2. **Modal-sufficiency rate.** The share of the pool where
   modal-in → modal-out is a function across pairs (the assumption
   the v2 lane died on), stated as a pool rate beside the banked
   bound-level figures (modal-only 808/938 vs searched 921/938).
3. **Subtype census.** Pool-level counts of §2.1's three failure
   subtypes — context-dependent output background; input modal
   equal to no generator's value while another generator is
   consistent; single-pair flip — so the refinement iteration (if
   WEAK) aims at a pool-sized class, not a 17-task anecdote.
4. **Background-binding LOO determinacy.** Per task: whether the
   surviving background account is the same when each pair is held
   out in turn. This is the component's certification-facing
   ceiling, priced before any build beyond the gate.
5. **Reachable-mass join.** The modal-vs-searched per-task delta
   joined to the existing creation split
   (`census/creation_split.json`), so the mass the component can
   actually convert — bg-fixed tasks whose remaining content is
   within the frozen grammar — is a number, not a hope.

---

## 3. SIEVE-axis evidence — what a future re-derivation may count

Measured only. The SIEVE axis moves on measured conversion, on
fresh draws, through the frozen certification — on nothing else.

**Branch PASS produces:**
- The gauntlet run record (step 7) and
  `sample_version_space_report.json` (step 8½): certified solves
  x/48 on A+B, full-fit coverage, conversion at supply (certified ÷
  fits, read against 1/28 and 1/18), sample-U with denominators,
  unanimous∧correct with its Fisher p against 1/9 — all measured on
  a fresh draw (seed 22979062) through `harness/certify.py`
  unmodified.
- Countable at re-derivation: the first measured conversion
  evidence for the LLM-proposer species (superseding P2's 0/120 and
  P3's 0-fit records at their stated strength), and prior evidence
  at exactly the clause that fired. Countable later, only as they
  land: the step-4 fresh-draw record, the step-5 confirmation rate,
  the step-6 wall-clock record — each a separate measured artifact.
- **Not countable:** any projection from 48 or 96 tasks to the
  240-task scale; any exam capability (Exam #1 is unspent until it
  is run, and its result is the only 216/240 evidence that exists);
  Pass B's larger cache as a capability claim (it is supply for
  statistics, not a verdict).

**Branch FAIL produces:**
- The same two artifacts at null/weak strength: a measured 0 (or
  1–3) certified on the same fresh draw, the species verdict stated
  jointly with P3 — a closed lane with a measured verdict, countable
  the way the grammar lineage's closure is countable: as a killed
  path removed from the search space on evidence, not as progress
  toward a score.
- Under mere-supply additionally: the Stage-V input seat at its
  registered strength, and the harvested fitting-text set as a
  banked artifact.
- From Nov 7: the BG-GATE migration table (17 tasks re-charged
  class-by-class) and the §2.4 census update — measured component
  evidence, countable as the successor species' first gate record
  at its registered bars. A BG-GATE PASS is countable as a
  component verdict on a spent draw; it is **not** a conversion
  measurement and moves the axis only when a successor lane
  converts on a fresh draw under the gauntlet protocol.
- **Not countable:** tonight's null as anything but a null. It
  relaxes no bar, spends no exam, and raises no axis.

---

## 4. File index (all verified on disk, 2026-11-06)

- Registered bars: `friday_bigmodel_kit/HARNESS_READY.md`,
  `friday_bigmodel_kit/FRIDAY_SAMPLE_STATS.md`.
- Frozen certification and harness: `friday_bigmodel_kit/harness/
  certify.py`, `proposer_client.py`, `probe_lane.py`,
  `harness_prompts.py`, `friday_draw.json`;
  `friday_bigmodel_kit/sample_version_space.py`,
  `bigmodel_fetch.py`, `serve_config.json`, `stage_model.py`.
- Tonight's pack: `probe_runs/friday_pack/` (`manifest.json`,
  `units.json`, `prompts/`), upload copy
  `friday_pack_upload/apex2-prompts.zip`.
- Gauntlet and pools: `gauntlet/gauntlet.py`, `gauntlet/pools.json`
  (pool B = 938), `gauntlet/GAUNTLET.md`, `PROBE_LEDGER.jsonl`.
- Exam: `approval_exam/APPROVAL_EXAM_PROTOCOL_2026-11-04.md`,
  `approval_exam/MANIFEST.json`, `approval_exam/verify_seal.py`.
- Background record: `NEXTGEN_V2_PROBE_RESULTS_2026-11-04.md`
  (§4.1, §6), `PARAMETER_SEMANTICS_DERIVATION_2026-11-04.md` (M1),
  `nextgen_probe/ng2_lane.py`, `nextgen_probe/diag2.py`,
  `nextgen_probe/diag2_rows.json`.
- Census: `census/census_param_bound.py`, `census/per_task.jsonl`,
  `census/param_per_task.jsonl`, `census/param_bound.json`,
  `census/summary.json`, `census/creation_split.json`.
- Design discipline: `NEXT_IDENTIFICATION_DERIVATION_2026-11-04.md`
  (§5 probe protocol, §6 proposer seat), `CONVERSION_DERIVATION_
  2026-11-04.md`, `SURVIVOR_SET_CENSUS_2026-11-04.md`,
  `SHARED_WRONG_BINDING_DERIVATION_2026-11-04.md` (§4).

---
**Correction (2026-11-06, desk):** §1.1's RunPod line double-books the
$4.23 balance — it was already held for the NS spectral validation
suite (standing assignment, 2026-11-03/04), which fires FIRST. The
freeze-week timing cross-check keeps only the balance the suite
leaves; if the suite consumes the hour, the cross-check is cancelled
(Kaggle L4×4 timings suffice for the exam serving decision). The
§1.1 text above is superseded on this point.
