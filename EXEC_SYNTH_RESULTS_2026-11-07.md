# EXEC-SYNTH Supply Canary — Results (2026-11-07)

**INSTRUMENT-INCOMPLETE — the run was stopped by an HTTP 429
rate-limit response at request 82, per the registered service
discipline (no retries). 2 of 24 tasks were fully measured;
execution-verified fits 0/2 fully measured (0 supplied). The
registered bars (PASS ≥ 4/24, KILL ≤ 1/24, middle 2–3/24) are
adjudicated only on a complete 24 and are therefore NOT adjudicated
here. This document is an instrument result, not a verdict.**

Governing filings: `EXEC_SYNTH_PREREGISTRATION_2026-11-07.md`
(commission registration quoted there verbatim; seed 23007195;
replication gate passed on all nine spent draws, spent B union
288, draw disjoint from all of them). Lane: `openai/gpt-oss-120b`
via Groq, code interface, execution-only selection, no LOO
certification (as registered). Rows:
`nextgen_probe/exec_synth_rows.json`; raw responses:
`nextgen_probe/exec_synth_cache/`; request ledger:
`nextgen_probe/exec_synth_calls.jsonl`.

## 1. The stop

- Run window: first request 10:09 AM ET, stop 11:07 AM ET
  (58.5 minutes). Requests issued: **82** — 81 × HTTP 200,
  1 × HTTP 429.
- The 429, verbatim from `STOPPED_429_exec_synth.json`: *"Rate
  limit reached for model `openai/gpt-oss-120b` in organization
  `org_01kr4584fvfekbegvv9z5k6409` service tier `on_demand` on
  **tokens per day (TPD): Limit 200000, Used 195582, Requested
  4519**."* The stopped request was task 5207a7b5's sample-s0
  repair round 1.
- **The binding cap on this tier is tokens/day, not requests/day.**
  The commission's budget line priced the canary at ≈ ≤ 768
  requests "inside one day's 1,000-request cap." The service's own
  message shows the operative limit for this model is **200,000
  tokens/day**. This run's 81 successful responses carry
  API-reported usage summing to **220,533 total tokens (avg 2,722
  per request)** — against which the service's TPD meter reported
  195,582 used at the stop. The two figures are both reported as
  measured; the meter evidently does not count every token the
  usage field reports (and any same-day account usage outside this
  run is inside the service's figure and not decomposable from
  here). Either way, the arithmetic is decisive: at ~2.7k reported
  tokens per request, one TPD day admits on the order of 70–90
  requests for this model — a full-width canary at full exhaustion
  (768 requests, ≈ 2.1M reported tokens) **cannot complete in one
  day on this tier**. Completing the registered protocol as
  configured is a multi-TPD-day undertaking, or needs a materially
  cheaper configuration, or a higher tier. That is a desk decision;
  per the standing service-limit rule this lane does not retry,
  resume, or reroute around the stop.

## 2. Per-task results

Fully measured (complete protocol: 8 initial samples + all repair
rounds, early stop would have fired on any fit):

| # | Task | Supplied | Samples | Repair rounds | Requests | Best program (execution cost*) |
|---|---|---|---|---|---|---|
| 0 | 4364c1c4 | **No** | 8 | 24 | 32 | 52 differing cells |
| 1 | fbf15a0b | **No** | 8 | 24 | 32 | shape-wrong on ≥ 1 pair (cost 500,000) |

\* Cost = total differing cells across train pairs under execution
(shape errors charged 500,000/pair, exceptions/load errors
10,000,000/pair, as registered in the driver). All 64 programs on
the two fully measured tasks extracted, executed, and failed to
fit; zero load errors on either task. On 4364c1c4 the best program
missed by 52 cells; on fbf15a0b no program ever produced the right
output shapes on all pairs.

Partially measured (not counted in any denominator above):

| # | Task | State when stopped |
|---|---|---|
| 2 | 5207a7b5 | 17 programs received and executed (8 initial + 9 repairs), **0 fits**; best cost **5 differing cells** (sample s3 after 3 repair rounds). Repair chains for s4, s6, s3 completed their 3 rounds — s3's chain improved monotonically 54 → 13 → 6 → 5; the 429 stopped s0's first repair request; s1, s2, s5, s7 never entered repair; 15 requests of this task's protocol were never issued. Partial row reconstructed post-stop from the response cache by local re-execution only (no further API calls) and marked as such in the rows JSON. |

Tasks 3–23 of the draw were never started. No sandbox escapes or
runaway executions occurred; no task hit the 25 s execution budget;
no test pair was read by the driver at any point.

## 3. What this does and does not establish

- It does **not** adjudicate the canary. 0 supplied of 2 fully
  measured is inside every band's shadow — the registered KILL
  line (≤ 1/24) is a statement about 24 tasks, and this run
  measured 2. No species conclusion is drawn.
- It **does** establish an instrument fact about the rail, at full
  strength: the Groq free tier's binding constraint for
  gpt-oss-120b is a 200,000 tokens/day cap that the registered
  canary configuration (~2.7k reported tokens/request, ≤ 768
  requests) exceeds by an order of magnitude against a one-day
  completion. Any completion of this canary — by cache-resume
  across TPD windows (the driver is resumable: cached responses
  are reused, completed rows persist, the request ledger is
  cumulative), by a re-registered cheaper configuration, or on a
  higher tier — is a separate desk decision, to be filed before
  it runs. The repeat-canary provision in the commission's middle
  band is not implicated: no band was reached.
- Early signal, labeled as such and carrying no verdict: on the
  two fully measured tasks the code interface also produced zero
  execution-verified fits in 64 programs — while on the partially
  measured third task, execution-feedback repair was visibly
  converging (best chain 54 → 5 cells) when the service stopped
  the run. Both halves of that sentence are in the rows; neither
  half is a measurement of the species.

Exam #1 remains unspent. Nothing here is projected to 240 tasks,
and no solver is approved, seated, or closed by this document.

---

# Completion on Kaggle — the canary is adjudicated (2026-11-07)

The desk's decision on file (2026-11-07) moved the registered
canary, unmodified, to the Kaggle L4 x4 rail: same frozen draw
(seed 23007195), same configuration (k=8 = 4 @ 0.25 + 4 @ 0.75,
≤3 repair rounds/sample, execution-only selection,
reasoning_effort=low), executed by the kit driver
(`exec_synth_kaggle.py`, one API-shape patch at the generate()
boundary — vLLM returns a list of RequestOutput — applied in the
run cell only; the registered protocol code is otherwise
byte-identical). Notebook `notebook1c118f1637`, Version 14
(scriptVersionId 366690258), Internet OFF, runtime 7275.5 s,
Kaggle status "Successful".

**CANARY_DONE supplied=6/24 tasks_complete=24/24 status=complete
generations=596**

## Per-task results (Kaggle run)

| # | Task | Supplied | Requests |
|---|---|---|---|
| 1 | 4364c1c4 | No | 32 |
| 2 | fbf15a0b | No | 32 |
| 3 | 5207a7b5 | No | 32 |
| 4 | c7d4e6ad | **Yes** | 3 |
| 5 | e9fc42f2 | No | 32 |
| 6 | 53b68214 | No | 32 |
| 7 | fb791726 | No | 32 |
| 8 | d687bc17 | No | 32 |
| 9 | 9aec4887 | No | 32 |
| 10 | 22806e14 | No | 32 |
| 11 | 770cc55f | **Yes** | 4 |
| 12 | d631b094 | **Yes** | 1 |
| 13 | 9caba7c3 | No | 32 |
| 14 | 252143c9 | No | 32 |
| 15 | 8d510a79 | No | 32 |
| 16 | 7e2bad24 | No | 32 |
| 17 | 6ca952ad | No | 32 |
| 18 | 9473c6fb | No | 32 |
| 19 | 3391f8c0 | No | 32 |
| 20 | 7acdf6d3 | No | 32 |
| 21 | 351d6448 | **Yes** | 10 |
| 22 | d89b689b | **Yes** | 1 |
| 23 | fc4aaf52 | No | 32 |
| 24 | a406ac07 | **Yes** | 1 |

All 24 rows complete=true; no execution budget exceeded on any
task; requests_used sums to 596, matching the CANARY_DONE
generations count. Rows: `exec_synth_kaggle_rows.json` (84.74 kB,
Version 14 Output tab; transcribed in full by the run worker
after the browser download did not start). The two tasks fully
measured on Groq (4364c1c4, fbf15a0b) again supplied nothing
under the full Kaggle protocol — cross-rail agreement. The Groq
partial's converging repair chain on 5207a7b5 did not convert on
the full protocol either (32 requests, no fit): the convergence
color recorded in §2 stands as color, not conversion.

## Adjudication at the registered bars

Bars (preregistration): PASS ≥ 4/24, KILL ≤ 1/24, middle 2–3 =
one repeat canary on a disjoint 24 as a separate commission.

**Measured: 6/24 execution-verified fits. Verdict: PASS.**

EXEC-SYNTH is the first species in this campaign to pass a
supply gate. Per the commission's terms, the pass earns exactly
one thing: **the 48-task fresh-draw conversion gate at packet
seat bars** — seat (a) ≥ 4/48 certified; the conversion clause
≥ 10×(1/28) guarded to ≥ 10 fits; unanimity reported, never
used. It approves no solver, seats nothing, and projects nothing
to 240 tasks. Exam #1 remains unspent. The conversion gate is a
separate commission: fresh disjoint 48 from the untouched pool,
filed before it runs.
