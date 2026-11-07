# APEX-2 P3 — Library-Conditioned Proposer: Build Notes

**Status: BUILT, self-tested, prepared. No Groq calls made.** The gate run
fires on a fresh cap day with the single command in
[P3_RUNBOOK.md](sandbox://workspace/arc_apex2/P3_RUNBOOK.md).

## Why

P2 (zero-shot, measured 2026-11-03): 102 completions, 62 parseable,
**0 exact fits, 0 near-misses** on eval-120. The models produce plausible
DSL-2 syntax whose semantics never land. P3 changes exactly one variable:
the proposal distribution is conditioned on the solver's own verified
library, so the model composes from programs that demonstrably solve
tasks instead of free-associating from the op digest.

## What was built

| File | Role |
|---|---|
| `conditioned_retrieval.py` | Retrieval index, scoring, selection, prompt assembly (importable, no API) |
| `groq_p3_conditioned_driver.py` | Phases prepare / fetch / solve / taxonomy / configline; reuses P2's constants, pacing, cache shape, 429-stop discipline |
| `selftest_p3.py` | Local end-to-end proof (stub proposer, no API) |
| `P3_RUNBOOK.md` | The gated first test: tasks, budget math, verdict rules |
| `probe_runs/p3_conditioned_gate/` | Prepared artifacts: `prepare_summary.json`, `prompts/<tid>.json` (sha1-sealed), `retrieval/<tid>.json` (top-15 with score breakdowns) |

Nothing in the mirror repo or the P2 driver was modified (self-test
asserts their sha256 before/after). Nothing pushed to GitLab.

## Design

**Index.** `apex2.library.build_corpus` over the 62 seed programs →
**478 verified programs** (orig + color-canonical + D4 variants, each
re-verified by execution on its own transformed donor task). Each entry
carries its own verified task — recomputed through the same symmetry
transforms in the same order, with the (tid, tag, text) sequence asserted
identical to the corpus build, so an exemplar can never pair a program
with the wrong task.

**Retrieval signals** (all logged per entry in `retrieval/<tid>.json`):

- `exec` (weight 3.0) — the program is parsed and **run on the target's
  train inputs** under `ProgramSpace` (persisted macros on): pair_score
  blended with the exact-fit fraction; fitting all pairs scores 1.0 and
  flags `solves_target`.
- `shape` (1.0) — Jaccard over (in_shape → out_shape) sets.
- `color` (1.0) — mean Jaccard of input/output color sets.
- `delta` (0.5) — Jaccard over colors added by the mapping.
- `size` (0.5) — Jaccard over per-pair size-relation classes.
- `len` (0.25) — brevity prior 1/(1+lines), tie-shaping only.

Score = weighted sum; ties break on (tid, tag, text). Selection is
greedy: ≤ 4 exemplars, ≤ 2 per donor task (symmetry variants are
near-duplicates), each admitted **whole or not at all** — a grid is
never truncated.

**Prompt format.** Byte-disciplined against P2/SFT: system message is
P2's `SYSTEM_TXT + DIGEST`; each exemplar is a demonstration turn pair
(user = `encode(donor_task)`, assistant = program text) in the SFT chat
shape; the final user turn is P2's zero-shot target turn unchanged
(`encode(target)` + "Write the program that maps every IN to its OUT.").
Prepared prompts are sha1-sealed; fetch verifies the hash before
sending anything.

## Token math

Estimator (P2-measured): 0.93 tokens/char over total message content +
4 tokens/message. Hard cap: conditioned prompt ≤ **7,338 est. tokens**,
so P2's per-task `max_tokens = min(4096, 7850 − est_prompt)` stays
≥ 512. Per-task prepared values (fetch order = ascending prompt size):

| Task | Baseline k (P2) | Exemplars | Est. prompt ZS → cond. | max_tokens | Cum. est. run tokens |
|---|---|---|---|---|---|
| 136b0064 | 8 | 4 | 2,993 → 5,394 | 2,456 | 47K |
| 135a2760 | 8 | 4 | 4,486 → 6,455 | 1,395 | 103K |
| 53fb4810 | 1 | 4 | 4,055 → 6,577 | 1,273 | 159K |
| 1ae2feb7 | 2 | 4 | 3,770 → 7,075 | 775 | 220K |
| 142ca369 | 8 | 1 | 6,743 → 7,168 | 682 | 281K |
| 1818057f | 4 | 3 | 4,022 → 7,170 | 680 | 343K |
| 16de56c4 | 8 | 4 | 3,559 → 7,219 | 631 | 404K |
| 20270e3b | 8 | 4 | 2,140 → 7,225 | 625 | 466K |
| 21897d95 | 4 | 2 | 5,655 → 7,329 | 521 | 529K |

All 9 tasks conditioned (none dropped); **72 planned calls** (9 × k=8),
well under the 1,000 req/day cap. Estimated total ≈ **529K tokens**
(+500 completion tokens/call assumed). P2's arms were 429-stopped at
~200–235K cumulative tokens — consistent with an effective per-model
daily token cap in the low 200Ks — so this run should be expected to
span **2–3 cap days**: day 1 plausibly completes the first ~4 tasks and
stops inside the 5th. Fetch is cache-resumable and cheapest-first; the
verdict rules (runbook) handle partial coverage honestly.

## Self-test results (all pass, no API)

- **Index**: 478 entries, alignment asserted.
- **Self-retrieval**: for 3 seed donors, the donor's own program text
  ranks #1 at the maximum attainable score (6.125 / 6.083) with
  `solves_target=True` — the retrieval signal is semantically real.
- **Training tasks**: top exemplars are the intuitively right programs
  (e.g. `scale_up 3` donors for scale tasks, exec 0.54; `fill_holes 2`
  for a fill task, exec 0.59).
- **Gate prepare**: 9/9 tasks within cap, max_tokens 521–2,456.
- **Stub end-to-end**: cache → `SampleFnProposer` → `core_solver.solve`
  → taxonomy all consume conditioned samples exactly as P2's did
  (9 solve rows, 8 samples consumed per task). Stub verdicts are
  machine-flagged NOT meaningful.
- **One honest signal from the stub run**: task 135a2760's top-1
  retrieved exemplar (`local_cross`, donor 3618c87e) **fits all of its
  train pairs exactly** through the real solver — executor retrieval
  does surface semantically exact programs on eval tasks. Its test
  prediction was wrong, so it is a train fit, not a solve; in the real
  run, generalization is the model's job.
- **Positive control**: solver fits a seed task from its retrieved
  program through P2's exact proposer path.
