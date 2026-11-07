# APEX-2 P3 — Library-Conditioned Proposer Gate: COMPLETION RECORD

**Status: CLOSED — verdict PASS (mechanical, pre-registered rule).**
Closed 2026-11-05T01:38:45Z by the `configline` ledger append
(kind `p3_conditioned`; mirror `PROBE_LEDGER.jsonl` and workspace
`PROBE_LEDGER.jsonl`). Segment logs: `RUN_LOG_2026-11-03_resume1.md`
and `RUN_LOG_2026-11-04_resume2.md` in
`probe_runs/p3_conditioned_gate/`. Protocol: `P3_RUNBOOK.md`
(unmodified throughout; the enlarged-corpus re-prepare of
2026-11-03 is the artifact set the live segments ran against).

## The question

P2's zero-shot Groq lane produced 0 exact fits and 0 near-misses in
62 parseable completions. P3 changed exactly one variable —
proposals conditioned on the solver's verified library (39,065
programs at live-run time) as SFT-format demonstration turns — and
asked whether the distribution moves **at all**.

## Headline numbers (MEASURED)

| | P2 zero-shot | P3 conditioned |
|---|---|---|
| Exact fits | 0 | **0** |
| Near-misses | 0 | **1** |
| Unique texts classified | 30 (gate tasks) / 62 parseable (probe-wide) | 8 |
| Certified solves | 0 | **0** |

- The one near-miss: on task **135a2760** (2 train pairs), all five
  banked samples are the single text `fliplr` / `mirror_complete r`,
  which parses and fits **1 of 2** train pairs. It is a semantically
  adjacent program, not a fit; there was no exact fit anywhere, so
  there is nothing to certify and no certification trace exists.
- Gate verdict rule (registered before any live call): PASS = ≥1
  exact fit or ≥1 near-miss anywhere in the conditioned samples;
  PASS may trigger on partial coverage; FAIL requires flat 0/0 at
  full k=8 on all 9 tasks. The verdict is **PASS**, fired at the
  coverage below. The remaining 43 of 72 planned calls were **not
  spent** — the gate was decided, and the runbook's close-out step
  (`configline`) is the protocol's own instruction on PASS.

## Coverage (stated, not rounded)

29 of 72 calls banked (all HTTP 200; 196,221 tokens total across
three live segments, each ended by a protocol 429 stop). Tasks at
full k=8: 3/9 (20270e3b, 1ae2feb7, 1818057f). Partial: 135a2760
(5/8 — the task that produced the near-miss). Unsamped: 136b0064,
142ca369, 16de56c4, 21897d95, 53fb4810. Solve phase over banked
samples: fits 0 on all tasks; task classes — near_only {135a2760},
samples_no_fit {20270e3b, 1ae2feb7, 1818057f}, no_samples {the five
unsampled}.

## What this verdict is, and is not

- It **is** a measured falsification of "conditioning in this form
  is as flat as zero-shot": the conditioned distribution produced a
  near-miss where the baseline produced none, under identical model,
  temps, wire format, solver, and budget. The movement is minimal —
  one near-miss in eight unique texts — and is reported at that size.
- It is **not** conversion. Exact fits 0, certified solves 0. Under
  the proposer_lane_evaluation taxonomy discipline, a lane with a
  near-miss is *not* semantically dead the way P2's lane was — and
  it is also not alive as a solver. The species question (LLM
  proposer as a standalone route) is **not** decided by this gate:
  it is decided by the Friday measurement (fresh-draw gauntlet probe
  through the frozen certification, derivation §6 seat standard),
  whose harness was built and smoke-tested alongside this close-out
  (`friday_bigmodel_kit/HARNESS_READY.md`).
- Extrapolation limit (skill rule 7): this measures gpt-oss-120b as
  served by Groq's free tier, reasoning effort "low" (the only
  configuration that tier returns content under), k≤8, conditioned
  prompts capped at 7,338 est. tokens. It says nothing about the
  model at full reasoning or k=128 — that regime is Friday's.

## Record integrity

Every number above is read from files on disk:
`probe_runs/p3_conditioned_gate/calls_openai_gpt-oss-120b.jsonl`
(32 records), `taxonomy_openai_gpt-oss-120b.json` (verdict string:
"PASS — distribution moved"), `solve_detail_openai_gpt-oss-120b.jsonl`,
the three fetch logs, and the two ledger appends of
2026-11-05T01:38:45Z. No driver, prompt, or mirror file was modified
at any point; the Groq key was read from `.groq_key` at runtime and
appears nowhere in any record.
