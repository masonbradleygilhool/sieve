# EXEC-SYNTH Conversion Gate — Preregistration (2026-11-07)

**Status: FILED BEFORE THE GATE RUN.** This document fixes the draw,
the seed, the protocol configuration, the certification step, and
the verdict bands before any model request is made against the gate
draw. **The run does not fire on this filing** — it fires on the
desk's separate order, after the desk rules on the disclosed
conflict in §2. No task in the draw has been shown to any model.

**Governing filings:** `SIEVE_REDESIGN_COMMISSION_2026-11-07.md`,
Candidate 1 (EXEC-SYNTH), constraints C1–C8;
`EXEC_SYNTH_PREREGISTRATION_2026-11-07.md` (the canary's
registration — this gate is its registered protocol plus the
certification step, on a fresh draw);
`EXEC_SYNTH_RESULTS_2026-11-07.md` (the canary's adjudication: PASS
6/24 on Kaggle, which earned exactly this gate);
`NOVEMBER_CONVERSION_PACKET.md` §0 (seat standards, evidence
clauses, branch logic) and `friday_bigmodel_kit/HARNESS_READY.md` /
`friday_bigmodel_kit/FRIDAY_SAMPLE_STATS.md` (the registered bars
the packet quotes).

## 1. What the canary pass earned — quoted verbatim

From `EXEC_SYNTH_RESULTS_2026-11-07.md`, "Adjudication at the
registered bars":

> Measured: 6/24 execution-verified fits. Verdict: PASS. … Per the
> commission's terms, the pass earns exactly one thing: **the
> 48-task fresh-draw conversion gate at packet seat bars** — seat
> (a) ≥ 4/48 certified; the conversion clause ≥ 10×(1/28) guarded
> to ≥ 10 fits; unanimity reported, never used. It approves no
> solver, seats nothing, and projects nothing to 240 tasks. Exam
> #1 remains unspent. The conversion gate is a separate commission:
> fresh disjoint 48 from the untouched pool, filed before it runs.

From `SIEVE_REDESIGN_COMMISSION_2026-11-07.md` §3, Candidate 1,
"What a pass earns":

> the conversion gate — the identical pipeline on a fresh 48
> (B-only), frozen certification unmodified, packet seat bars
> quoted verbatim (seat (a) ≥ 4/48 certified; conversion clause
> ≥ 10 × 1/28 guarded to ≥ 10 fits; unanimity reported, never used
> for selection). A gate pass is a lane verdict in the packet's
> sense; it approves no solver and spends no exam (§4).

The packet's seat standard (`HARNESS_READY.md`, quoted in
`NOVEMBER_CONVERSION_PACKET.md` §0):

> - **SEAT (a):** ≥ **4/48 certified solves** on A+B → the proposer
>   earns the Stage-T candidate-source seat.
> - **SEAT (b):** full-fit coverage ≥ **41.6%** of A+B (≥20/48
>   tasks; 2× the derived lane's measured 20.8%) at conversion
>   (certified ÷ full-fit) no worse than the recorded **1/18** →
>   seat via fit supply.
> - Otherwise **no seat**: 1–3 certified = WEAK, 0 = KILL for the
>   seat question.

The gate adjudicates seat (a) and the prior-evidence conversion
clause — the earned terms above. Seat (b) is not adjudicated by
this gate (its Stage-V input seat is the Friday proposer's
mere-supply instrument, not part of the earned terms); fit coverage
is measured and printed regardless, as a clause input.

**The certification definition is the packet's, verbatim:**
"the frozen certification (`friday_bigmodel_kit/harness/certify.py`,
unmodified in every branch)" — the packet §0 statement of what is
closed and does not reopen. §4 states how the gate applies it.

## 2. Disclosures (two, both material, both before the fact)

### 2.1 Pool arithmetic and the draw mechanism

The canary preregistration's §2 disclosure pattern, advanced one
draw: the canary (seed 23007195, 24 tasks) has run and is now
itself a spent run record.

- **Spent B union now: 312 distinct ids** (288 + the canary's 24).
  **Untouched pool-B ids: 626** (938 − 312).
- **Replication gate: PASSED, before sampling.** All ten spent draws
  replicated exactly — id sets *and* order — against the seven
  gauntlet run records (seeds 999 / 20261103 / 20261104 / 20261109 /
  20261164 / 20271132 / 20365108), `friday_draw.json` (seed
  22979062), `fresh_probe_draw.json` (seed 22988303), and
  `exec_synth_draw.json` (seed 23007195), by
  `nextgen_probe/find_conversion_gate_seed.py`. Its output:

  ```
  replicated run seed 999: 3 tasks, id set + order exact vs run_1793752808_seed999_smoke.json
  replicated run seed 20261103: 60 tasks, id set + order exact vs run_1793752881_seed20261103_baseline.json
  replicated run seed 20261104: 60 tasks, id set + order exact vs run_1793816913_seed20261104_nextgen_v1.json
  replicated run seed 20261109: 60 tasks, id set + order exact vs run_1793817846_seed20261109_nextgen_v2.json
  replicated run seed 20261164: 60 tasks, id set + order exact vs run_1793829053_seed20261164_derived.json
  replicated run seed 20271132: 60 tasks, id set + order exact vs run_1793832491_seed20271132_sieve_iter2.json
  replicated run seed 20365108: 60 tasks, id set + order exact vs run_1793837074_seed20365108_sieve_intersection.json
  replicated Friday seed 22979062: 60 tasks, order exact vs friday_draw.json
  replicated fresh-probe seed 22988303: 48 tasks, id set + order exact vs fresh_probe_draw.json
  replicated canary seed 23007195: 24 tasks, id set + order exact vs exec_synth_draw.json
  spent B union: 312 distinct ids (626 untouched)
  GATE SEED: 23007196 (immediate successor of the last spent seed 23007195); draw = rng.sample over the 626 untouched B entries in pools.json order + shuffle; asserted disjoint from (a) the 288-id spent union, (b) the canary's 24, (c) the full 312-id spent union
  ```

- **Mechanism deviation, disclosed with its measured reason.** The
  fresh probe and the canary drew by the smallest seed above the
  previous spent seed whose *full-pool* B draw is disjoint from
  the spent union. At width 48 against a 312-id union that search
  is infeasible: the exact probability that a uniform 48-of-938
  sample avoids all 312 spent ids is C(626,48)/C(938,48) =
  **1.986e-09** — an expected ≈ 5.0×10⁸ seeds to the first hit —
  and a 200,000-seed probe above the floor (at ~29,600 seeds/s)
  found 0 hits. (The same search at the canary's width cost 18,891
  seeds; at the fresh probe's, 9,241.) The search's entire
  epistemic content is membership-only, ex-ante-fixed selection
  from the untouched pool — the campaign's anti-cherry-picking
  guarantee (C1) — and direct sampling of the untouched sub-pool
  carries that content identically. **The gate draw is therefore:
  the 626 untouched B entries in `gauntlet/pools.json` order,
  sampled at seed 23007196 (the immediate successor of the last
  spent seed) with gauntlet.py's consumption pattern (rng.sample,
  then rng.shuffle), disjointness from the 288 union, the canary's
  24, and the full 312 union asserted in code at draw time** (all
  three asserts passed). If the desk prefers the legacy search
  despite its cost, it re-cuts the draw and re-files before firing;
  the draw below is the frozen draw of this filing in the meantime.

### 2.2 The conversion clause has two registered readings — CONFLICT

The packet's prior-evidence standard (`NOVEMBER_CONVERSION_PACKET.md`
§0, and `FRIDAY_SAMPLE_STATS.md` "The registered bars", verbatim):

> - **conversion clause:** certified conversion an order of
>   magnitude above the grammar's 1/28 at comparable fit supply —
>   the registered operationalization is **≥ 4 certified from
>   ≤ 20 fits**; the scale-free reading (conversion ≥ 10 × 1/28,
>   guarded to ≥ 10 fits of supply) is printed alongside.

`FRIDAY_SAMPLE_STATS.md` adds: "the module also computes the
scale-free ratio reading (conversion ≥ 10 × 1/28) guarded to ≥ 10
fits of supply, and prints both sub-readings so the desk sees
which fired."

The redesign commission's C8 and the canary's earned terms (§1)
instead register **the scale-free reading as the clause**:
"conversion clause ≥ 10 × 1/28 guarded to ≥ 10 fits". The two
readings are different decision rules on a wide, plausible outcome
region. Two examples at this gate's width: certified 5 on 18 fits
fires the operationalization (≥ 4 from ≤ 20) and fails the
scale-free ratio (5/18 = 0.278 < 10/28 ≈ 0.357); certified 4 on 8
fits fires the operationalization and fails the scale-free guard
(8 < 10 fits). They agree at, e.g., certified 6 on 15 fits (both
fire) and certified 9 on 30 fits under a rate reading of the
operationalization vs the ratio (0.300 < 0.357 — disagree again).

**This filing does not reconcile the conflict.** It files the
earned terms' reading as operative (the scale-free clause: fits
≥ 10 AND certified/fits ≥ 10/28), because the commission and the
results adjudication are the documents that created this gate and
stated its price; the gate's readout prints **both** sub-readings
with their fire/silent status, in the sample-stats module's own
practice; and **the desk rules on which reading is operative
before the run fires** — the run fires on the desk's separate
order in any case, so the ruling costs nothing and settles the
bars before any GPU is spent. A secondary divergence rides with
the same ruling: the packet's evidence standard admits the
unanimity clause as an alternative route to prior evidence; the
earned terms subordinate unanimity to report-only ("unanimity
reported, never used"), so §5 does not let a unanimity-clause fire
substitute for the conversion clause. Unanimity statistics are
computed and printed either way (§4).

## 3. The draw (seed fixed here, before any model call)

- **Seed: 23007196.** Draw file: `nextgen_probe/conversion_gate_draw.json`
  (rule, population, and replication instructions recorded in it).
- **The 48 tasks, in draw order** (all pool B):
  0 ae4f1146 · 1 5587a8d0 · 2 bd14c3bf · 3 10fcaaa3 · 4 f8c80d96 ·
  5 00576224 · 6 de493100 · 7 fe45cba4 · 8 7e02026e · 9 5e6bbc0b ·
  10 d10ecb37 · 11 7ee1c6ea · 12 18286ef8 · 13 77fdfe62 · 14 c48954c1 ·
  15 782b5218 · 16 d6542281 · 17 4347f46a · 18 19bb5feb · 19 a096bf4d ·
  20 eb281b96 · 21 44d8ac46 · 22 0becf7df · 23 39e1d7f9 · 24 8ba14f53 ·
  25 98cf29f8 · 26 e84fef15 · 27 8719f442 · 28 13f06aa5 · 29 762cd429 ·
  30 0b17323b · 31 94414823 · 32 0a2355a6 · 33 88207623 · 34 e9ac8c9e ·
  35 689c358e · 36 469497ad · 37 91714a58 · 38 3bd292e8 · 39 1a07d186 ·
  40 15660dd6 · 41 2281f1f4 · 42 c92b942c · 43 3f7978a0 · 44 90f3ed37 ·
  45 58743b76 · 46 d406998b · 47 f0f8a26d
- **No re-sampling for any reason:** a task that errors in the run
  is reported as an error row, never replaced. Pool A is not used
  (all 18 spent; the gate is B-only per C7).
- **Prompt-size pre-check** (rendered train pairs, digit-string
  format, computed by the draw script): max initial prompt 4,424
  chars (≈ 4,202 tokens at the repo's 0.95 tokens/char estimate),
  mean 1,201 chars — no task approaches the serving envelope
  (max_model_len 32,768 with the 4,096 completion cap).
- **Fold census of the draw:** train pairs per task min 2, max 6,
  mean 3.06 — **147 folds** if every task were supplied (the
  certification's worst-case fold count, priced in §6); test pairs
  1–2 per task.

## 4. Protocol as registered (canary configuration + certification)

**Supply phase — the canary's registered configuration, unchanged**
(`EXEC_SYNTH_PREREGISTRATION_2026-11-07.md` §4, executed by
`canary_core.py`, byte-identical to the canary kit's):

- **Model:** `openai/gpt-oss-120b`, served locally on the rail (§6);
  no model substitution — a different model is a different
  measurement. `reasoning_effort="low"` (the canary registration's
  tier-forced value, stated once per C8), `max_tokens` 4096,
  `top_p` 0.95.
- **Initial samples:** k = 8 per task — 4 at temperature 0.25, then
  4 at temperature 0.75. **Prompt:** the task's train pairs only,
  grids rendered as rows of digit characters; the contract is a
  single Python function `transform(grid) -> grid`, standard
  library only, no I/O, no randomness, returned in one ```python
  block.
- **Execution:** the canary sandbox, as built in
  `exec_synth_harness.py` (separate subprocess; environment
  cleared; RLIMIT_CPU 5 s and RLIMIT_AS 2 GB via rlimits; wall
  timeout 6 s per program; `socket` disabled; per-task cumulative
  execution budget 25 s). A program **fits** iff it reproduces
  every train pair's output exactly under execution.
- **Repairs:** if no initial sample fits, repair rounds proceed
  best-sample-first (execution score: total differing cells across
  train pairs; shape errors charged 500,000/pair, exceptions/load
  errors 10,000,000/pair, as registered in the driver); each sample
  receives ≤ 3 repair rounds at temperature 0.25, carrying the
  train pairs, the current code, and per-failing-pair execution
  feedback (differing cells capped at 12 per pair). A task stops
  the moment any program fits. A task is **supplied** iff ≥ 1
  sampled program fits all its train pairs exactly.
- **Selection is by execution only.** No sample unanimity, voting,
  or agreement statistic is computed or used anywhere in the
  supply phase.

**Certification phase — the frozen certification, applied to every
supplied task.** The criteria are `certify.py`'s, quoted from its
docstring: full fit (≥ 1 proposed program fitting ALL train pairs);
LOO (for every fold j, the fold candidate set's prediction set on
the held input equals exactly the singleton {held output}; an
empty fold candidate set fails the fold; a fold on an empty pair
subset fails); the shape-diverse-holdout classification
(shape_unique folds → `shape_loo_rejected` vs `loo_rejected`); and
prediction unanimity over the full-fit programs on every test input
(disagreement → `ambiguous`, no predictions). A task is
**certified** iff the certification accepts it (full fit ∧ LOO pass
∧ unanimity). Non-supplied tasks are `no_fit` by construction and
consume no certification.

The one substitution, registered once here per the commission's
standing invariant for species that cannot face the certification
literally as coded: **the candidate source.** `certify.py` parses
candidate texts in the derived grammar's ProgramSpace; EXEC-SYNTH
programs are Python, not DSL texts. The gate therefore applies the
criteria criterion-for-criterion with the candidate source
substituted — exactly the substitution `certify.py` itself makes
when it replaces induction with the proposer ("The only
substitution is the candidate source"). Concretely, in
`certify_exec.py`: full-fit and fold-fit are judged by sandbox
execution (the registered EXEC-SYNTH fit test); each fold's
candidate texts come from **re-running the registered supply
protocol on the fold task** (train minus the held pair; the held
pair appears in no fold prompt) through the same machinery, under
a fold-scoped cache namespace; fold prediction sets are the fold
candidates' executed outputs on the held input; test-input
predictions likewise. Folds inherit the protocol's per-task
execution budget (25 s) each. **Test outputs are never in the
instrument:** the kit dataset carries test *inputs* only (stripped
at build time, structurally asserted), read solely by the
unanimity clause, as `certify.py` reads them.

**Rows** (`conversion_gate_rows.json`, one flushed row per
completed task): the canary row fields, plus per task — `fit`
{full_fit, full_fit_count, sampled_texts, fitting_texts},
`certified`, `cert_reason` (null when certified; else no_fit /
loo_rejected / shape_loo_rejected / ambiguous), `loo_status`,
`loo_folds`, `predictions`, `programs`, `cert_requests_used`
(certification-phase generations), `requests_used_total`. The
readout prints, with denominators: supplied x/48, certified x/48,
fit coverage, conversion (certified ÷ fits) under **both**
sub-readings of §2.2 with each one's fire/silent status, and the
report-only unanimity statistics (sample-U and unanimous∧correct
with its Fisher p against the grammar's 1/9, computed desk-side
from the rows and the pool records in the packet §0 step-8½
pattern, per `FRIDAY_SAMPLE_STATS.md`'s definitions).

**Caps and stop semantics.** Internal wall cap **9 h**, checked at
task boundaries (a certification in progress finishes its task).
On the cap or a serve error the run stops, rows stand, and the
outcome is **INSTRUMENT-INCOMPLETE** until the run is completed by
cache-resume in a follow-up session under this same registration
(generation and fold caches persist; completed rows are never
re-measured). Bars (§5) are adjudicated only on a complete 48 —
all rows complete, certification included.

## 5. Definitions and verdict bands (adjudicated exactly as registered)

- **Supplied (per task):** ≥ 1 sampled program (initial or repaired)
  fits all the task's train pairs exactly under execution.
  Headline supply: fits **F** = supplied count /48.
- **Certified (per task):** the frozen certification (§4) accepts
  the task. Headline: certified **C** /48. Conversion = C ÷ F.
- **Conversion clause (operative as filed, §2.2):** F ≥ 10 AND
  C/F ≥ 10 × (1/28) ≈ 0.357. (Note the guard's arithmetic: with
  F ≥ 10, the ratio already forces C ≥ 4 — the clause cannot fire
  below seat (a)'s count.)
- **PASS — C ≥ 4/48 certified AND the conversion clause fires.**
  EXEC-SYNTH holds the **Stage-T candidate-source seat with prior
  evidence**: the lane becomes an *exam candidate in preparation*,
  and the packet §1 sequence (integration pre-checks, fresh-draw
  probe of the composed candidate, confirmation draw, economics
  dry run, freeze) is commissioned as its own filing, under the
  packet's own gates (commission step 2, decision point D2). A
  PASS approves **no solver**, spends **no exam**, and projects
  **nothing** to 240 tasks; the sealed exam remains the only
  approval instrument, at 216/240.
- **SEAT-ONLY — C ≥ 4/48 certified AND the conversion clause does
  not fire.** The packet's branch logic applies verbatim: the lane
  holds its registered seat at seat strength, the §1 build
  sequence does **not** fire (it is gated on prior evidence, not
  on supply), and the successor design question — LIBLEARN Stage-1
  registration (commission step 3) — opens in parallel. SEAT-ONLY
  is a terminal band for this gate, not a repeat band.
- **WEAK — 1 ≤ C ≤ 3 certified** (the packet's word for the seat
  question: no seat). Exactly **one repeat gate** on a disjoint 48
  is permitted — as a separate commission, same bars, fresh draw
  under the §2.1 mechanism against the then-current spent union.
  A repeat landing WEAK or KILL closes the species. (Provenance,
  stated once: the packet names the WEAK band but prescribes no
  repeat for it; the one-repeat consequence is registered here,
  following the campaign's standing middle-band pattern — the
  canary's middle band and BG-GATE's WEAK both permit exactly one
  re-test.)
- **KILL — C = 0 certified** (the packet: "0 = KILL for the seat
  question"). **EXEC-SYNTH closes as a solver species** and
  LIBLEARN becomes the design question (commission step 3). The
  band covers both zero signatures alike: no supply (F = 0) and
  supply without certification (F > 0, C = 0 — the L3 disease,
  measured on every grammar lane).
- **INSTRUMENT-INCOMPLETE** — the run stopped before all 48 rows
  completed (§4). Not a verdict; the run is completed by resume
  and adjudicated whole, or the incompletion is reported with its
  denominator.

Nothing in this gate projects any number to 240 tasks. Exam #1
stays unspent regardless of outcome; no outcome here is exam
evidence.

## 6. Rail and budget plan

- **Rail: Kaggle L4 x4** (gpt-oss-120b from the staged
  apex2-bigmodel dataset, internet OFF, the canary kit's serving
  configuration). Groq cannot carry this gate: the canary's Groq
  phase measured ~2,722 reported tokens per request against the
  tier's binding **200,000 tokens/day** cap for this model; the
  gate's supply phase alone is expected at ≈ 1,192 generations
  (≈ 3.2M tokens) — supply alone is a ≥ 17-day drip on Groq,
  certification excluded. Local CPU execution of candidates rides
  the session, as in the canary.
- **Cost basis (measured, from the canary's Kaggle completion):**
  596 generations, runtime **7275.5 s** (121.3 min) for 24 tasks —
  12.2 s/generation, 303 s/task; supply mix 18 unsupplied × 32
  generations + 6 supplied × 20 generations total (early stops at
  3, 4, 1, 10, 1, 1). (A 118.7-minute figure for the canary appears
  in this gate's commissioning brief; it does not occur in the
  repo record — the results file's desk-verified runtime is
  7275.5 s, and every estimate below is computed on that larger,
  conservative figure.)
- **Supply phase, expected:** the canary's mix at double width —
  ≈ 36 unsupplied × 32 + 12 supplied × ~3.3 ≈ **1,192 generations
  ≈ 4.0 h**. Worst case 48 × 32 = 1,536 generations ≈ 5.2 h.
- **Certification phase, expected:** supplied ≈ 12 tasks × mean
  3.06 folds ≈ 37 fold runs. No measured fold cost exists; the
  planning assumption (labeled as such) is 16 generations per fold
  run — half the 32-generation protocol width, since fold tasks
  are the supplied tasks' own (k−1)-pair subsets and the protocol
  early-stops at the first fold fit → ≈ **590 generations ≈ 2.0 h**.
  Bound at the expected supplied count: 37 × 32 = 1,184 generations
  ≈ 4.0 h. The absolute fold bound is 147 folds (every task
  supplied) × 32 = 4,704 generations, not jointly reachable with a
  full supply phase inside the wall cap; the cap-and-resume
  discipline (§4) governs that tail.
- **Total: expected ≈ 1,780 generations ≈ 6.0 h of session wall**,
  inside the 9 h internal cap with headroom; $0. **Fire-time gate
  (the packet §1.1 pattern):** the desk verifies the week's
  remaining Kaggle GPU quota covers the expected session before
  firing, and splits at a session boundary via cache-resume if it
  does not — the cache makes a quota cut lose nothing.
- The run fires **only on the desk's separate order** after this
  filing (and after the §2.2 ruling). This commission builds the
  instrument and files the bars; it runs no GPU.

## 7. Instrument (kit) — verification results

Kit: `friday_bigmodel_kit/conversion_gate_kit/` — the canary kit
adapted, dataset name **apex2-conversion-gate**. Desk-side builders
`build_tasks_json.py` (dataset from the frozen draw; draw order
verified against §3 programmatically; test outputs stripped and
structurally asserted absent) and `build_driver.py` (the gate
driver generated from the canary's Version-14 driver by asserted
exact substitutions — docstring, wall cap 9 h, EXPECTED_TIDS from
the draw, kit discovery, file names, GateCanary, GATE_DONE block;
probe, model discovery, channel extraction, and generate() —
including the `out[0].outputs[0]` list-indexing fix — carried
byte-for-byte).

**Mock test: PASS** (`mock_test.py`, local, no GPU/API/network —
the canary kit's mock pattern extended through certification).
Three entries through `gate_core.GateCanary` with the real sandbox
harnesses: (i) gate task ae4f1146 with a lookup-table mock — the
mock memorizes each prompt's pairs, fits the full task at sample 0
(supplied, 1 generation), and certification **rejected** it:
certified=False, `loo_rejected`, 4 folds run, 4 certification
generations — a memorizer is not a conversion, which is the frozen
certification's registered job; (ii) gate task 5587a8d0 with an
identity mock — supplied=False after the full 8 samples + 24 repair
rounds (32 generations), cert_reason `no_fit`, 0 certification
generations; (iii) a synthetic color-swap task with a general-rule
mock — certified=True, LOO pass, unanimous test predictions
returned. The rows file landed on disk with all rows complete and
carrying both fit and certified fields; generation accounting
balances exactly (run total 41 == sum of per-row supply +
certification generations).

**Protocol-fidelity diff vs the canary instrument: PASS.**
`canary_core.py` and `exec_synth_harness.py` are byte-identical
in the gate kit (md5 3f17ed7103285ced52912b02f89946cb and
09d869cea63ceb104ce4c4d983da3405, matching the canary kit's). The
gate driver differs from the canary's Version-14 driver
(md5 4dbe4905f78b799a77b2de07a6d1127d) by 113 diff lines, confined
to the seven registered deltas of §7's builder list (docstring,
wall cap 9 h, EXPECTED_TIDS, kit discovery, file names,
GateCanary, GATE_DONE block); `probe()`, `extract_final()`, and
the whole `generate()` block — including the fixed
`o = out[0].outputs[0]` line — are byte-identical between the two
drivers, and the generated EXPECTED_TIDS equals the frozen draw
order (asserted). The gate's additions are new files only
(`gate_core.py`, `certify_exec.py`, `gate_harness.py` — the last
is the canary harness plus a predict mode under identical caps;
the supply phase never uses it). `canary_core`'s one runtime
touch is a display constant (N_TASKS 24 → 48, the progress-line
denominator), set by `gate_core` at import; the file itself is
untouched.

---

Nothing in this gate approves a solver, spends Exam #1, or
projects any count to the 240-task scale. A PASS makes EXEC-SYNTH
an exam candidate in preparation, under the packet's own dated
gates — nothing more, and nothing less.

---

## Desk ruling on the §2.2 conflict (2026-11-07, before any firing)

The filing discloses two registered readings of the conversion
clause and of the unanimity route. The desk rules:

1. **Conversion clause — the scale-free reading is operative**
   (F ≥ 10 AND C/F ≥ 10 × (1/28)), as registered by the redesign
   commission's C8 and restated in the canary results
   adjudication that created this gate. Grounds: the Nov 7
   commission is the later registration and the one specific to
   this species and this gate; the packet's operationalization
   (≥ 4 certified from ≤ 20 fits) was registered for the Friday
   proposer instrument and its fit supply. The packet reading is
   printed alongside at readout with its fire/silent status, per
   the sample-stats module's own practice.
2. **Unanimity — report-only is operative** (same grounds); the
   packet's unanimity clause prints alongside likewise.
3. **Draw mechanism — accepted as filed.** The legacy
   smallest-seed search is measured-infeasible at width 48
   against a 312-id spent union (hit probability ≈ 2e-9); the
   uniform sample of the 626 untouched ids at seed 23007196,
   with the replication gate passed on all ten spent draws and
   disjointness asserted in code, carries the same epistemic
   content. The deviation and its reason stand disclosed in
   §2.1 permanently.

With this ruling the gate is fireable on the desk's separate
order, subject to the fire-time quota read (§6).
