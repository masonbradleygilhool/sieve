# APEX-2 — complete codebase bundle (assembled 2026-11-01)

Target: ARC Prize 2027, ARC-AGI-2 private set. Design target: 240/240.
Everything in this bundle is verified at the level its section states.
GPU-side numbers (proposer recall) are NOT in this bundle because they do
not exist yet — they are produced by the P2 probe (below), and no claim in
here depends on them.

## The system in one pass

1. **Proposer** — Qwen3-Coder-30B-A3B-Instruct (AWQ 4-bit, ~18 GB, one L4)
   served by vLLM, prefix caching on. Prompts carry a dual encoding of the
   task: raw grid text + an object-segmented token stream. Samples are
   drawn across a temperature ladder (0.2 / 0.7 / 1.0), K=128 per task.
2. **DSL-1** — a closed program language (strict parser, never eval()):
   geometry, gravity (flat + per-object), tiling, learned colormap and
   neighborhood-rewrite tables, crop/scale, fill_holes, tile_collapse,
   recolor_by_size, and ~20 more ops. The prompt DIGEST lists every op and
   is byte-identical between training data and serving.
3. **Gate + rank** — a candidate program must fit ALL train pairs exactly.
   Survivors are grouped by distinct test prediction and ranked by votes,
   then leave-one-out re-induction fraction (soft tier: 44/50 known-true
   programs score 1.0), then parameter provenance, then program length.
   Top 2 distinct predictions become the two attempts.
4. **Refiner** — near-miss programs (deficit <= 2, fit >= 1) enter a
   population mutation loop (delete / insert / swap / perturb /
   arg-sibling swaps). Measured recovery: 4 of 5 seeded near-misses.
5. **Frames pass** — tasks unsolved in the identity frame are retried in
   the 7 nontrivial dihedral frames; predictions are conjugated back
   exactly. Measured on eval-120 partial: +1 solve over 27 tasks.
6. **Flywheel** — every verified program becomes a task GENERATOR:
   unlimited provably-solved synthetic tasks for the next fine-tune round.
   Hard negatives (fitting programs that disagree on test) get 3x weight.
7. **TRM finisher** — a faithful "Less is More" TRM (separate latent /
   answer states, deep supervision, ACT halting) covers tasks where
   induction returns nothing. First run is P2 (needs torch/GPU).

## Files

### Solver core (what runs on Kaggle)
- `apex2_probe_launch.py` — the launcher: DSL-1 executor, encoder, gate,
  LOO ranking, refiner, vLLM sampler, probe prints. SELFTEST 2/2.
- `apex2_solve.py` — the full-run production driver: governor (budget
  spread, per-task clamp 20-600 s), identity pass, frames pass,
  progressive submission.json banking in competition schema.
- `apex2_api_probe.py` — OpenAI-compatible API variant of the probe.
- `finetune_qlora.py` — QLoRA fine-tune (r=64, alpha=128, NF4 base load,
  completion-only loss). Adapters are served UNMERGED on the AWQ base;
  merging into a quantized base is forbidden (breaks quant scales).
- `trm.py` — faithful TRM implementation (compile-checked; first run P2).

### Dataset codebase (what the proposer learns from)
- `sft_seed.py` + `sft_seed.jsonl` (50) + `sft_seed_m34.jsonl` (6) — the
  real seed records: programs mined from the 1,000 training tasks, every
  one executor-verified train-fit AND test-exact.
- `gen_expand.py` / `gen_expand_r1.py` — the flywheel generators: each
  verified program manufactures fresh tasks (random inputs, program as
  ground truth, independent re-verification before banking).
- `build_final_dataset.py` — rebuilds the training set from sources under
  ONE current digest (fixes the digest drift found in the round-1 file).
- `sft_final.jsonl.gz` — **the training set**: 14,160 records (56 real +
  14,104 generated; 13,444 train / 716 dev). Digest uniformity
  14,160/14,160. Independent audit: 200/200 sampled records re-verified
  exact (fourth consecutive clean audit).
- `synth_tasks_r1.jsonl.gz` — the 14,104-task generated bank.
- `miner.py`, `miner2.py`, `miner3.py`, `miner4.py`,
  `probe_families.py`, `probe_families2.py`, `fold_miner3.py` — the
  mining suite (closed: 57 verified programs of 1,000 training tasks).

### Measurement (how every claim gets checked)
- `probe.py` — Kaggle-exact probe harness. Controls re-verified
  2026-11-01: oracle 120/120 tasks (167/167 pairs), null_copy 0/120.
- `induce.py` — the enumeration induction core (measured: eval-30 pool
  recall 0/30 — pure enumeration is demoted to a parts role).
- `loo_cert_test.py` — LOO-certificate calibration (44/50 at 1.0).
- `experiments_v12.py` — E3/E5/E6 (refiner recovery, v1.2 op probes).
- `frames_test.py` + `frames_results.jsonl` — frames measurement.
- `autopsy.py` — coverage autopsy of solved vs unsolved training tasks.
- `solve_integration_test.py` — driver integration: stub proposer solves
  taskA direct, taskB via frames:r180. PASS on this codebase.
- `PROBE_LEDGER.jsonl` — every measurement, zeros included.

### Design record
- `APEX2_CHARTER_2026-11-01.md`, `CAMPAIGN_PLAN_2026-11-01.md`,
  `BLUEPRINT.md` (full spec v1.2), `RESEARCH_NOTES_2026-11-01.md`,
  `probe_runbook.md` (ready-to-fire probe env blocks).

## Verified state (2026-11-01, this machine)

- All modules compile. Launcher SELFTEST 2/2 (also 2/2 on Kaggle's own
  machines with the staged probe kit).
- Probe controls: oracle 120/120, null 0/120 — the harness is sound.
- Mining closed at 57 verified programs; enumeration recall 0/30.
- Final dataset: 14,160 records, uniform digest, audit 200/200.
- Solve driver integration: PASS (direct + frames paths).

## What runs next (agent-initiated, no user steps)

- **P2 probe, ~Fri Nov 6** when the Kaggle GPU meter refills to 30 h:
  controls first, then eval-30 zero-shot pool recall R0 at K=128
  (30B-AWQ on L4; 14B-AWQ fallback on T4 x2). The probe kit on Kaggle is
  already current (dataset v2, launcher v1.2).
- P2b: QLoRA round on `sft_final.jsonl`, then recall R1. Pre-registered
  rule: a proposer under 10% pool recall after P2 is demoted to parts.
- Full runs only when the probe numbers project them (gate G4), solve
  phase <= 6 h for 240 tasks.

## The score call (committed, 2026-11-01)

- **As it stands today** (enumeration + DSL gate, no GPU proposer yet):
  measured 0/30 on eval-30. On a private set today: ~0%.
- **Mature system** (P2 proposer + fine-tune rounds + flywheel, 2027
  private set): **~25%**, band 10-45%. Basis: the strongest demonstrated
  number in this method family is 24.03% (NVARC, 2025 private, TTT class
  with frontier-LLM-distilled data); LLM program induction is a stronger
  class, discounted here for an open-weight proposer and metered compute.
- **Design target: 240/240.** Every gate above is built to that bar. The
  target is the requirement; the call is what the measurements support
  today, and it moves only when probe prints move it (pre-registered:
  zero-shot recall >= 15% on eval-30 pushes the call up hard; < 5% after
  fine-tuning pushes it down and species die per the plan).
