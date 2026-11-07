# EXEC-SYNTH Supply Canary — Preregistration (2026-11-07)

**Status: FILED BEFORE THE FIRST GROQ CALL.** This document fixes the
draw, the seed, the protocol configuration, and the verdict bands
before any model request is made. The draw was computed by
`nextgen_probe/find_exec_synth_seed.py` after the replication gate
below passed; no task in the draw has been shown to any model.

**Governing design:** `SIEVE_REDESIGN_COMMISSION_2026-11-07.md`,
Candidate 1 (EXEC-SYNTH), constraints C1/C5/C7/C8. **Protocol
precedents:** `groq_p2_driver.py` (the repo's established Groq
configuration and service discipline on this account's tier),
`FRESH_PROBE_PREREGISTRATION_2026-11-07.md` §3/§4 (pool arithmetic
and the repeat-draw seed method).

## 1. The commission's canary registration — quoted verbatim

From `SIEVE_REDESIGN_COMMISSION_2026-11-07.md` §3, Candidate 1,
"Cheapest decisive falsifier — supply canary (pre-registered)":

> - *Draw:* 24 tasks, pool B only, from the 686 untouched ids, seed =
>   smallest seed whose B draw is disjoint from all 252 spent B ids
>   (replication-verified before sampling, per C1/C7).
> - *Protocol:* gpt-oss-120b via the Groq API (the user's account;
>   1,000 requests/day/model), k = 8 samples per task, ≤ 3
>   execution-feedback repair rounds per sample; local CPU execution
>   in a sandbox, 25 s/task-equivalent budget discipline; a task is
>   *supplied* iff ≥ 1 sampled program fits all its train pairs
>   exactly under execution.
> - *Bars:* **PASS ≥ 4/24 supplied** (against the same model's measured
>   0/48 on the proposal interface — a supply difference at this size
>   is the interface hypothesis surviving its cheapest test).
>   **KILL ≤ 1/24 supplied** — the species closes at the canary and
>   the model-null is interface-independent at this scale. 2–3/24 is
>   the named middle: exactly one repeat canary on a second disjoint
>   24 is permitted; a second middle closes it.
> - *What a pass earns:* the conversion gate — the identical pipeline
>   on a fresh 48 (B-only), frozen certification unmodified, packet
>   seat bars quoted verbatim (seat (a) ≥ 4/48 certified; conversion
>   clause ≥ 10 × 1/28 guarded to ≥ 10 fits; unanimity reported,
>   never used for selection). A gate pass is a lane verdict in the
>   packet's sense; it approves no solver and spends no exam (§4).

And its rail/cost line:

> Groq API: ≤ 24 × 8 × (1 + ≤ 3 repairs) ≈ ≤ 768 requests worst case —
> inside one day's 1,000-request cap for the model; local CPU
> execution. **$0, ≤ 1 day.** No Kaggle quota is touched until a
> canary pass exists.

## 2. Disclosure: the commission's pool arithmetic, one draw later

The commission's "686 untouched ids / 252 spent B ids" is the fresh
probe preregistration's accounting *before that probe ran*. The
fresh probe (seed 22988303) has since drawn 36 pool-B tasks, and
those 36 are now spent run records under C1 ("verified by offline
replication of every spent run record"). A canary draw taken from
the stale 686 could land on tasks a gauntlet lane measured this
morning. This canary therefore follows the fresh probe's own method
advanced one draw — the same disclosure pattern that document set
in its §3:

- **Spent B union now: 288 distinct ids** (252 + the fresh probe's
  36). **Untouched pool-B ids: 650** (938 − 288).
- **Seed rule:** the smallest seed **> 22988303** (the fresh probe's
  seed, the last spent seed) whose B-draw under the canary's sampling
  (draw spec **B:24**, gauntlet.py's exact rng consumption) is
  disjoint from all 288 spent B ids. Disjointness from the 288
  satisfies the commission's disjointness from its 252 a fortiori.
- Pool A is not used (all 18 spent; the canary is B-only per C7).

**Replication gate: PASSED, before sampling.** All nine spent draws
replicated exactly — id sets *and* order — against the seven gauntlet
run records (seeds 999 / 20261103 / 20261104 / 20261109 / 20261164 /
20271132 / 20365108), `friday_draw.json` (seed 22979062), and
`fresh_probe_draw.json` (seed 22988303), by
`nextgen_probe/find_exec_synth_seed.py`. Spent B union computed from
the replicated draws: **288**.

## 3. The draw (seed fixed here, before any model call)

- **Seed: 23007195** — the smallest seed > 22988303 whose B:24 draw
  is disjoint from all 288 spent B ids. Draw file:
  `nextgen_probe/exec_synth_draw.json`.
- **The 24 tasks, in draw order** (all pool B):
  0 4364c1c4 · 1 fbf15a0b · 2 5207a7b5 · 3 c7d4e6ad · 4 e9fc42f2 ·
  5 53b68214 · 6 fb791726 · 7 d687bc17 · 8 9aec4887 · 9 22806e14 ·
  10 770cc55f · 11 d631b094 · 12 9caba7c3 · 13 252143c9 ·
  14 8d510a79 · 15 7e2bad24 · 16 6ca952ad · 17 9473c6fb ·
  18 3391f8c0 · 19 7acdf6d3 · 20 351d6448 · 21 d89b689b ·
  22 fc4aaf52 · 23 a406ac07
- **No re-sampling for any reason:** a task that errors in the run
  is reported as an error row, never replaced. Prompt-size
  pre-check (rendered train pairs, digit-string format): every
  drawn task's estimated prompt is ≤ ~2,800 tokens — no task
  approaches the tier's measured prompt-size ceiling
  (`groq_p2_driver.py`'s 7,600-token unsampleable line), so no
  drawn task is instrument-unmeasurable on size.

## 4. Protocol as executed (registered configuration)

- **Service:** Groq chat-completions endpoint
  (`https://api.groq.com/openai/v1/chat/completions`), model
  **`openai/gpt-oss-120b`**, API key read from
  `~/workspace/arc_apex2/.groq_key` at runtime by the driver only;
  never printed, logged, or written anywhere else; the sandbox
  environment carries no credentials.
- **Tier-forced configuration (stated once, per C8):**
  `reasoning_effort="low"` — measured 2026-11-03 on this tier
  (`groq_p2_driver.py`): at default effort the model returned empty
  content at max_tokens 1024 and 4000 (all reasoning tokens); "low"
  is the only configuration under which this tier returns content.
  `max_tokens` 4096, `top_p` 0.95 (repo parity).
- **Initial samples:** k = 8 per task — 4 at temperature 0.25, then
  4 at temperature 0.75 (the repo's established sampling split).
- **Prompt:** the task's **train pairs only**, grids rendered as
  rows of digit characters; the contract is a single Python
  function `transform(grid) -> grid` (list of lists of ints),
  standard library only, no I/O, no randomness, returned in one
  ```python block. Test pairs are never read by the driver.
- **Execution:** every extracted program runs in a local sandbox
  (separate subprocess; environment cleared; CPU limit 5 s and
  address-space limit 512 MB via rlimits; wall timeout 6 s per
  program; the `socket` module disabled inside the harness; per-task
  cumulative execution budget 25 s — the commission's
  25 s/task-equivalent discipline — with any program past the
  budget counted not-executed and disclosed per task). A program
  **fits** iff it reproduces **every** train pair's output exactly
  under execution. Sandbox escapes and runaway executions are
  killed by the caps, counted as non-fits, and disclosed.
- **Repairs:** if no initial sample fits, repair rounds proceed
  **best-sample-first** (execution score: total differing cells
  across train pairs, exceptions and shape errors ranked worst).
  Each sample receives **≤ 3 repair rounds** (the commission's
  per-sample cap). A repair request carries the train pairs, the
  sample's current code, and its execution feedback — per failing
  pair: the exception, or the output-vs-expected shapes and the
  differing cells as (row, col, expected, got), capped at 12 per
  pair. Nothing beyond the train pairs the protocol already exposes
  is fed back. Repair temperature 0.25. A task stops the moment any
  program fits.
- **Selection is by execution only.** No sample unanimity, voting,
  or agreement statistic is computed or used anywhere in this
  canary. LOO certification is **not** part of the canary: it
  measures supply of execution-verified fits; certification belongs
  to the conversion gate a pass would earn.
- **Pacing:** the repo's measured tier discipline — a rolling
  60-second window held at ≤ 7,400 total tokens (the measured
  8,000 tok/min cap, `groq_p2_driver.py`), metered on API-reported
  usage where returned, else on a 0.95 tokens/char estimate.
- **Budget:** hard cap **768 requests** total (24 × 8 × (1 + 3)).
  Every HTTP request issued counts, including any that error. If
  the cap is reached before all 24 tasks are fully measured, the
  run stops and the outcome is INSTRUMENT-INCOMPLETE (§5).
- **Service discipline:** a **429 or any rate-limit response stops
  the run immediately** — no retries, no evasion, no second
  provider. Requests completed and tasks fully measured are
  reported with denominators; a partial run is an instrument
  result, not a verdict.

## 5. Definitions and verdict bands (adjudicated exactly as registered)

- **Supplied (per task):** ≥ 1 sampled program (initial or repaired)
  fits all the task's train pairs exactly under execution.
- **Headline:** supplied count x/24; requests used; per-task fits
  found, samples requested, repair rounds used — in the results
  document and `nextgen_probe/exec_synth_rows.json`.
- **PASS — x ≥ 4/24 supplied.** Earns (stated here, **not fired**
  by this lane): the conversion gate — the identical pipeline on a
  fresh 48 (B-only), frozen certification unmodified, packet seat
  bars (seat (a) ≥ 4/48 certified; conversion clause ≥ 10 × 1/28
  guarded to ≥ 10 fits; unanimity reported, never used for
  selection).
- **KILL — x ≤ 1/24 supplied.** The species closes at the canary;
  the model-null is interface-independent at this scale.
- **MIDDLE — x = 2–3/24.** Exactly one repeat canary on a second
  disjoint 24 is permitted — as a separate commission. **It is not
  run by this lane**; the band is reported.
- **INSTRUMENT-INCOMPLETE** — the run stopped early (429 /
  rate-limit, the 768 cap, or a service failure) before all 24
  tasks were fully measured. Bars are adjudicated **only** on a
  complete 24; a partial count is reported with its denominator
  and is not a verdict.

Nothing in this canary projects any number to 240 tasks. Exam #1
stays unspent regardless of outcome; no outcome here is exam
evidence, and a PASS approves no solver.
