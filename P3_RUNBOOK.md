# APEX-2 P3 Gate Run — Runbook

**Question under test:** does conditioning Groq proposals on the solver's
verified library move the proposal distribution at all? P2's zero-shot
lane produced 0 exact fits and 0 near-misses. One variable changes —
the prompt gains retrieved verified-library exemplars — everything else
is held at P2's configuration.

## The gate (decided in advance)

- **PASS** — at least **one exact fit** (a sampled program that parses
  and fits *all* train pairs of its task) **or one near-miss** (parses,
  fits ≥ 1 but not all train pairs) anywhere in the conditioned samples.
  The distribution moved; conditioning in this form lives.
- **FAIL** — 0 exact fits and 0 near-misses with **all 9 tasks at full
  k=8**. Conditioning in this form is dead too; do not re-spend on it.
- **INCOMPLETE** — flat so far but coverage partial (a 429 stop is
  expected; see budget). Resume fetch on the next cap day and re-judge.
  A PASS can trigger on partial coverage; a FAIL cannot.

The taxonomy phase prints the verdict mechanically. A verdict from a
`--stub` cache is flagged STUB and is **never** meaningful.

## Tasks and comparability

The 9 eval-120 tasks the P2 gpt-oss-120b arm actually sampled — every
one classified `samples_no_fit`, 0 fits / 0 near-misses at baseline.
Same model (`openai/gpt-oss-120b`), same temps (0.25 / 0.75, 4 each,
k=8), same reasoning effort ("low" — the only configuration under which
this tier returns content, P2-measured), same solver (25 s/task,
library on), same SFT wire format; the conditioned prompt is the only
difference. Baseline k per task: 135a2760: 8, 136b0064: 8, 142ca369: 8,
16de56c4: 8, 1818057f: 4, 1ae2feb7: 2, 20270e3b: 8, 21897d95: 4,
53fb4810: 1 (the P2 arm was 429-stopped mid-flight; the four partial-k
tasks get a full k=8 here, which only strengthens a FAIL reading).

## Fire it (fresh cap day, caps reset)

```
cd ~/workspace/arc_apex2 && python3 groq_p3_conditioned_driver.py fetch --model openai/gpt-oss-120b && python3 groq_p3_conditioned_driver.py solve --model openai/gpt-oss-120b && python3 groq_p3_conditioned_driver.py taxonomy --model openai/gpt-oss-120b
```

Then, once the verdict is PASS or FAIL (not INCOMPLETE), close the
record:

```
cd ~/workspace/arc_apex2 && python3 groq_p3_conditioned_driver.py configline --model openai/gpt-oss-120b
```

That appends the `kind="p3_conditioned"` full-configuration record to
the mirror `PROBE_LEDGER.jsonl`. Do not push anything to GitLab.

## Budget math (fresh day)

- Requests: 72 planned vs 1,000/day cap. Not the binding constraint.
- Tokens: ≈ **529K estimated total** (per-task conditioned prompts
  5,394–7,329 est. tokens, +500 completion tokens/call, × 8 calls/task;
  estimator 0.93 tok/char, P2-measured). Per-minute pacing holds every
  request inside the 8,000 tok/min window (TPM budget 7,400, P2's
  discipline, unchanged).
- The binding constraint is the effective daily token cap: P2's arms
  were 429-stopped at ~200–235K cumulative tokens. Expect day 1 to
  complete ~4 tasks (cumulative ≈ 220K through 1ae2feb7) and stop
  inside 142ca369. **That is protocol, not failure**: the 429 stops the
  arm, the cache keeps everything banked, and re-running the same
  command on the next cap day resumes exactly where it stopped
  (cheapest tasks were fetched first, so coverage loss is minimal).
  Plan on 2–3 cap days for full coverage.

## Protocol reminders

- Fetch verifies each prepared prompt's sha1 before sending; if
  `prepare` artifacts are stale (e.g. the library grew), re-run
  `python3 groq_p3_conditioned_driver.py prepare` first — it is local
  and spends nothing.
- Never retry a 429, never switch endpoints or models to evade a cap.
  Transient 5xx gets P2's bounded retry; nothing else does.
- Solve runs only over the gate tasks, through `SampleFnProposer` over
  the cache — byte-for-byte P2's consumption path.
- Report results against the baseline (0 fits / 0 near-misses) with
  coverage stated: tasks at full k, total unique texts, per-sample
  classes from `taxonomy_openai_gpt-oss-120b.json` in
  `probe_runs/p3_conditioned_gate/`.
