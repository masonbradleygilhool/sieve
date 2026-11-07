# FRIDAY NOV 6 KITS — FULL LOCAL RE-VERIFICATION (2026-11-03, evening)

Scope: local checks only. No Kaggle account actions, nothing pushed, nothing fixed.
Live-work guard: NS Cycle 45 negp25 sim (PID 8207) was the one heavy worker on the
VM throughout; all checks below are light except where a skip is recorded.

## (A) TRM lane — ~/workspace/arc_apex2/trm_lane/

### (1) Compile — PASS
py_compile OK on all 6 .py files: kaggle_main.py, kaggle_train_trm.py,
probe_capacity.py, smoke_gate.py, trm_data.py, trm_model.py.

### (2) kaggle_train_trm.py exact-bytes + self-audit prints — PASS (one record gap, below)
- Size on disk: **18,744 bytes** — matches BUILD_NOTES.md's build record exactly
  ("18,744 bytes = trm_model.py + kaggle_main.py, compile-verified").
- Concatenation check: `cat trm_model.py kaggle_main.py | cmp - kaggle_train_trm.py`
  → **byte-identical**. Component sizes corroborate: 10,350 + 8,394 = 18,744.
- sha256 (computed in this pass, two ways — direct and via the concatenation):
  `983fce9b8276f629d2adc33515be6113296168f21f9ec0336514cef6ff351554`
- RECORD GAP (report-only): BUILD_NOTES.md / RUN_PLAN.md record the byte size but
  **no sha256 was recorded at build time**; the hash above is the first on record.
- Self-audit prints in source — all present:
  - PROBE cell first in the Kaggle main section: `assert torch.cuda.is_available()`,
    real CUDA matmul, prints `PROBE OK: cuda matmul finite (...); gpus=... name=...`.
  - CFG: `audit_print(..., tag="BASE CFG")` at init prints params/d/layers/heads/
    n_latent/t_cycles/n_sup/lr/betas/wd/warmup/ema/vocab/seq.
  - BASE: `BASE: scratch init, params=...`, `BASE: DataParallel over N GPUs`,
    `BASE: resumed from checkpoint at step N`.
  - SANITY: one forward/backward before the loop; `assert ... "SANITY FAIL: loss ..."`,
    prints `SANITY: finite loss ... at init`.
  - Poison firewall: non-finite loss → `POISON strike k: non-finite loss; reloading
    init`; state never captured from a poisoned step; 3 strikes → `POISON: 3 strikes
    — aborting, init weights saved`.
  - Checkpointing: `CKPT = WORKDIR/trm_ckpt.pt`, periodic save + resume-on-start.
  - EMA artifact: EMA class (decay 0.999), `ema.copy_to(core)` at the end,
    `FINAL: EMA heldout exact=... tok_acc=... steps=...`.

### (3) TRM CPU smoke gates — RE-RUN SKIPPED (contention rule); banked record stands
- smoke_gate.py runs Gate A then Gate B inseparably (no gate selector); the banked
  full run took **wall=1386s (~23 min)** — beyond the "few minutes" contention
  allowance next to the live negp25 sim (VM available RAM ~1.2–1.6 GB during this pass).
- Banked record (trm_lane/smoke_gate.log): data train=950 / heldout=50 tasks,
  4087 / 221 pairs; smoke CFG params=748,928 d=128.
  - Gate A (overfit, faithful detached scheme, 250 steps): **FAIL** — loss
    3.0044 → 0.0796 best → 0.1132 final, exact 0.00 (known result: the published
    1-step gradient approximation under-delivers fit pressure at smoke scale).
  - Gate B (direction): **PASS** — held-out token accuracy **0.0504 → 0.6446** in
    45 steps; train loss 2.7783 → 1.3233.

## (B) Friday big-model kit — ~/workspace/arc_apex2/friday_bigmodel_kit/

### (1) Compile — PASS
py_compile OK on all 5 .py files: bigmodel_fetch.py, bigmodel_solve_taxonomy.py,
gauntlet_lane.py, prepare_prompts.py, stage_model.py.
Imports (manifest's validation claim): bigmodel_solve_taxonomy, gauntlet_lane,
prepare_prompts import clean. stage_model.py does NOT import on this VM —
FileNotFoundError '/kaggle/working' — expected: it is Kaggle-notebook staging
source that targets /kaggle/working at module level; py_compile is the applicable
local check and it passes.

### (3) Kit selftest — PASS
`bigmodel_fetch.py --selftest` → exit 0:
"SELFTEST PASS: config parses, per-temp sums to k=128, harmony final-channel
extraction correct (incl. truncated reasoning -> empty), qwen think-strip correct."
serve_config.json parses as JSON (top-level keys: comment, gptoss, qwen, shared).

### (4) kit_manifest.json hashes — CANNOT VERIFY AS SPECIFIED (report-only)
kit_manifest.json records **no per-file hashes** — its "files" map carries
one-line descriptions, not digests. The only hash-like entries are the primary
model's HF `repo_sha_at_check` (b5c939de8f754692c1647ca79fbf85e8c1e70f8a — a model
repo commit, not a kit file) and stage_model.py's runtime sha256 manifest for the
staged *weights*. So there is nothing in the manifest to check the kit files
against. Baseline sha256 of the kit files as they stand tonight (computed in
this pass, for the desk's future use):

- bigmodel_fetch.py            3588b7cc342ed5e954a3cf8160a40e88824fbe2c30b4a0b3b046f962a9d2a521
- bigmodel_solve_taxonomy.py   a8e247287c108920f5b03559bac4cc0e775283d04728ea051158f30d2257c7c2
- gauntlet_lane.py             0c153f19c16556a75f61c3291880f2037a325f911a7e64838f25a154b5432538
- prepare_prompts.py           d063d469572b510c8b65e5ef14024e8f691a9f75faf4a560e7775c462bbb344d
- stage_model.py               e204af921e00dd8aee13f5cb1f63af1d078f2143f99dd927a4b285f9d0689e9f
- kit_manifest.json            e37222e21852793c0bc99720d9cafdf2492be37d125ccd481d38ae46dda86eb9
- serve_config.json            0b79a4f8911fd140f8cbd61846d8fc907f8dd3e92e04a2dc7da8610fe4547893
- MODEL_SELECTION.md           0a79559a715fa8adf5ab8bd999b8bc4a056ab1a48a6a6e8d9a25726f74cbfc79
- README.md                    b3291b8ac1999d7711125973f6eb9eb1ddc2c0b2704e884cb0b14172c4247248
- STAGING_RUNBOOK.md           6122d50ebe79c1d7a395689557fe24fa061f19bc9a20cbcb3d26cb84df051bd6

Manifest content cross-checks that DO hold: sampling block matches the kit design
(k=128 split 43/43/42 over temps 0.2/0.7/1.0, reasoning_effort "high" for
gpt-oss); primary/fallback model ids and dataset names match MODEL_SELECTION.md
and STAGING_RUNBOOK.md (see item 5).

### (5) Dataset names — PASS for primary; fallback name absent from MODEL_SELECTION.md (no contradiction)
- Primary openai/gpt-oss-120b → **apex2-bigmodel**: STAGING_RUNBOOK.md (staging
  banner + "name it exactly: apex2-bigmodel"), MODEL_SELECTION.md line 56, and
  kit_manifest.json all agree.
- Fallback QuantTrio/Qwen3-Coder-30B-A3B-Instruct-AWQ → **apex2-qwen30b-awq**:
  STAGING_RUNBOOK.md line 49 and kit_manifest.json agree. MODEL_SELECTION.md's
  fallback section names the repo id but **never states the dataset name** —
  silence, not a conflicting name. Flagged for the desk; not edited.

## (C) P3 selftest — PASS
`python3 selftest_p3.py` → exit 0, ~16 s wall, **SELFTEST P3: ALL PASS**.
Evidence from the run:
- [2] Self-retrieval: seed donors' own verified programs at rank 1 / top score
  (6.125, 6.125, 6.083) — retrieval signal semantically real.
- [4] Gate-task prepare: 9/9 gate tasks conditioned, prompts within the hard
  token cap, 72 planned calls, est total 528,896 tokens (base 478-corpus prepare
  path, as the selftest is written).
- [5] Stub end-to-end OK: fetch --stub → solve → taxonomy consumed the
  conditioned cache through the P2 SampleFnProposer + core_solver path
  (9 rows; verdict explicitly "STUB RUN — pipeline check only").
- [6] Positive control: solver fits seed task 00d62c1b with its retrieved program.
- [7] P2 driver + mirror sources verified byte-untouched by the run.

## Verdict summary
- Compile (11/11 files): PASS
- TRM exact-bytes vs build record: PASS (size + concatenation identity; build-time
  sha256 was never recorded — hash now on record)
- TRM self-audit prints (probe/CFG/BASE/SANITY/poison/checkpoint/EMA): PASS
- TRM smoke Gate B: banked PASS (0.0504 → 0.6446); re-run skipped per contention rule
- Big-model kit selftest: PASS
- P3 selftest: PASS (ALL PASS, exit 0)
- kit_manifest file hashes: NOT VERIFIABLE — manifest records none (baseline now taken)
- Dataset names: primary PASS; fallback consistent in runbook+manifest, unnamed in MODEL_SELECTION.md
- Nothing was modified in either kit.
