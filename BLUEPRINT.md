# APEX-2 BLUEPRINT — system design, exact specs (2026-11-01)

Status labels: [BUILT] exists and is verified · [SPEC] designed, not yet built ·
[P2] first executes in the first Kaggle quota window. Charter gates G1–G5 govern.

## 0. The system in one paragraph
An open-weight code LLM, fine-tuned on verified programs, proposes transformation
PROGRAMS in a closed DSL for each task. Every program is executed against the
task's train pairs; only exact-fitting programs may answer test inputs. Distinct
surviving predictions are ranked by cross-program agreement, then simplicity;
the top two become the two scored attempts. Every verified program ever found
feeds the next fine-tune round (the flywheel). A faithful TRM covers tasks
where induction returns empty. [SPEC as a whole; gate/executor/probe BUILT]

## 1. The model [SPEC — verified from live sources 2026-11-01]
- **Qwen/Qwen3-Coder-30B-A3B-Instruct**, Apache-2.0. MoE: 30.5B total params,
  ~3.3B active/token → knowledge of a 30B, decode cost of a ~3B. Context 256K
  (we use ≤8K). Architecture Qwen3MoeForCausalLM.
- **Artifact: AWQ 4-bit** (community-validated repo
  `QuantTrio/Qwen3-Coder-30B-A3B-Instruct-AWQ`, vLLM-compatible). Weights
  ≈16.9–18 GB. BF16 (61.1 GB) does NOT fit and is never used.
- **VRAM math on one L4 (24 GB)**: weights 18.0 + CUDA overhead ~1.5 + KV cache
  ~4.0 (96 KB/token × ~8K ctx × ~5 concurrent long samples, paged) ≈ 23.5 GB.
  Tight by design; max-model-len is capped at 8192 to hold the line.
- **Serving: vLLM** (offline `LLM` API inside the notebook). Flags: quantization
  auto-detected from the repo config (do NOT force `--quantization` unless
  detection fails); `--dtype half` is the known fallback if AWQ decompression
  kernels misbehave; trust-remote-code on (Qwen3 family requirement);
  gpu-memory-utilization 0.92.
- **Delivery route**: Kaggle notebooks run with internet OFF → the model ships
  as a private Kaggle DATASET (weights + tokenizer + this blueprint's code),
  attached to the probe notebook, loaded from /kaggle/input. Never downloaded
  in-run. [Campaign ops rule, verified 2026-10-19]
- Fallback arm if the AWQ MoE underperforms or OOMs in the P2 smoke:
  Qwen2.5-Coder-14B-Instruct AWQ (~9 GB) — smaller prior, far more samples/hour;
  the bake-off is decided by measured pool recall per GPU-hour, not by params.

## 2. Task encoding (what the model sees) [SPEC]
Two channels, concatenated in the prompt:
- **Grid channel**: each grid as rows of space-separated digits, train pairs
  labeled `IN i` / `OUT i`, test inputs labeled `TEST i`. No color names —
  digits only (the executor's world is digits; names invite hallucinated maps).
- **Object channel**: per grid, the verified extractor's object list:
  `obj(color, size, bbox=(r0,c0,r1,c1), shape_hash)` lines for train inputs.
  Gives the proposer object vocabulary instead of raw pixels.
Prompt skeleton (exact):
  SYSTEM: "You write programs in DSL-1 (spec digest below). Output ONLY the
  program. A program is 1-6 lines, one op per line: OP arg arg."
  USER: <DSL-1 digest: the §3 op table, one line per op> + <grid channel> +
  <object channel> + "Write the program that maps every IN to its OUT."
  ASSISTANT (fine-tune target): the verified program text.

## 3. DSL-1 — the closed language [SPEC; executor semantics BUILT in induce.py]
A program is a straight-line sequence of ops (v1: no branches; composition and
parameterization carry the expressiveness). Parsed by a strict parser into an
AST and executed by the sandbox — NEVER eval(). Op set (signatures exact;
all grid->grid unless noted), seeded from the sprint's verified library:
  Geometry: rot k∈{1,2,3} · fliplr · flipud · transpose · antitranspose
  Gravity:  grav d∈{up,down,left,right} · ograv d (per-object)
  Tiling:   tile_mirror · tile_repeat a b · tile_crop a b
  Crop/pad: crop_bbox [color] · crop_to obj · pad color n · shift dr dc [wrap]
  Color:    colormap (learned from train pairs — parameter-free op) ·
            recolor a->b · swap_colors a b · recolor_by_size rank rule ·
            recolor_by_freq rank rule
  Objects:  keep_largest · keep_smallest · drop_color c · sort_objs axis key ·
            move_obj_to_marker color · copy_obj_to_marker color ·
            complete_symmetry axis · fill_holes [color] · outline color ·
            connect_dots color · draw_line_between color
  Frame:    frame color · separators_split · separators_join
Programs that raise, return non-grids, or change nothing on ALL train inputs
are discarded by the executor before the fit gate.
Expressiveness evidence (not hope): the miner's verified library — every
mined program is already expressible in this table or drives its next entry.

## 4. Sampling + gate + ranking (the solve loop) [SPEC; gate BUILT]
Per task, given a time budget B (set by the §6 governor):
1. Sample programs from the proposer in rounds: temperatures 0.2 / 0.7 / 1.0,
   top_p 0.95, max_tokens 256 (programs are short), until B expires or the
   distinct-fit cap (32 fitting programs) is reached.
2. **Gate**: execute each unique program on all train pairs; keep exact fits
   only. (Soundness: a non-fitting program can never answer — architectural,
   inherited from induce.py, unit-verified.)
3. **Rank**: apply survivors to the test inputs; group by identical prediction
   set; rank groups by (a) number of distinct fitting programs producing them,
   (b) lower mean program length (MDL). Attempt 1 = top group's prediction,
   attempt 2 = second group's (or the top group's runner-up program's).
4. **Pool recall bookkeeping**: per task, record fits_found>0 (recall hit),
   samples_tried, wall time → the probe ledger line. Recall is the master dial.
Planning targets (to be replaced by P2 measurements): K ≈ 300–1,500 programs
per task inside a full-run envelope; probe slices use K = 128.

## 5. Fine-tune + flywheel [SPEC]
- **Round 0 data**: (a) the miner's verified library (running count in
  PROBE_LEDGER/mining_results.jsonl; ~4.3% of training tasks at last check —
  expect ≈40–60 programs from the 1,000); (b) **program-as-generator
  expansion**: every verified program becomes a task GENERATOR — random input
  grids (sampled across size/color/density profiles) are pushed through the
  program to manufacture unlimited provably-solved (task → program) pairs.
  Target set: 20,000 pairs round 0. This is the $0 distillation-volume move:
  programs are not just labels, they are factories.
- **Format**: §2's chat template verbatim. Split: 95/5 train/dev by TASK (never
  by pair — leakage discipline); dev measures exact-program rate + fit rate.
- **Method (route SETTLED by research 2026-11-01; merging is FORBIDDEN)**:
  train QLoRA adapters (r=64, alpha=128, lr 1e-4 cosine, 3 epochs, seqlen
  2048) against a bitsandbytes-NF4 load of the base (the standard QLoRA
  substrate — NOT against the AWQ checkpoint); serve **base + adapter
  UNMERGED** in vLLM (`enable_lora=True`, LoRARequest, max_lora_rank 64).
  Merging into a quantized base breaks its scales, and dequant→merge→requant
  measurably loses accuracy (verified across sources) — the adapter travels
  separately, always. Whether adapters trained on the NF4 substrate transfer
  at full strength to the AWQ serving base is measured, not assumed: it is
  exactly what probe P2b reads. Weights reach the notebook by (in order of
  preference): Kaggle's Hugging Face attachment / an existing public weights
  dataset (one tap) → chunked private dataset (the v8 pattern, scaled).
  The launcher already carries the adapter path (APEX2_ADAPTER_DIR).
- **Flywheel rounds**: after every probe or run, all newly verified programs
  (from ANY source — mining, induction solves on training tasks, self-play
  generation) enter the generator pool; hard negatives (tasks where ≥2 fitting
  programs disagree on test) get 3× generation weight next round. Round data
  is versioned; every round's probe numbers go in the ledger before the next
  round starts.

## 6. Envelope + governor (full-run form) [SPEC; speed is a user-ordered
constraint 2026-11-01: best solver that does NOT take a ton of time]
12h committed-run cap (43,200s) minus 900s reserve. **Design target: the
solve phase finishes in ≤6h for 240 tasks (≤90s/task average)** — a full run
is a same-day instrument, never an overnight prayer. Per-task budget
B_t = clamp(remaining_solve_time / remaining_tasks × pace_factor, 20s, 600s),
pace_factor from the measured fits/hour of the current proposer version; the
probe launcher already enforces a per-task wall budget between sampling
rounds (APEX2_TASK_BUDGET_S, default 90). Speed levers, in order: (1) the
MoE's ~3.3B active params (decode cost of a 3B); (2) vLLM prefix caching —
SYSTEM+DIGEST is an identical prefix for every sample of every task, so its
KV is computed once (the launcher enables it; the prompt is chat-templated
so train and serve formats are byte-identical); (3) batched n-per-request
sampling; (4) the 32-fit early stop. Tasks are processed in a fixed
deterministic order; banking is progressive (submission.json rewritten
after every task — v8.5 discipline, kept).

## 7. TRM finisher [BUILT: trm.py, compile-checked; first run P2]
Faithful to "Less is More" (Jolicoeur-Martineau, 2025): ~7M-param recursive
net, separate latent (z_L) and answer (z_H) states, deep supervision over
N_sup=16 steps, T=3 recursion cycles, halting head unused at inference (fixed
steps), trained on the verified corpus (real training tasks + program-generated
tasks, dihedral-augmented ×8). Deployed ONLY where §4 returns zero fits;
its candidates pass through the same gate (train-exact under the corrected
fit-key (1,−1) selection) before answering. Published class anchor: ~8%.
**In-run TTA stage (added from McGovern 2025, arXiv 2511.02886):** before
solving, the pretrained TRM is fully fine-tuned briefly on the 240 tasks'
own train pairs (the only task-specific signal the rerun provides), inside
the envelope; the published result took a ~10% public base to 6.67%
semi-private with 12.5k such steps.

## 7b. v1.2 upgrades (2026-11-01, research-driven; see RESEARCH_NOTES)
- Object channel in the prompt (finding 1) — implemented + data regenerated.
- Parameter-provenance ranking (finding 2) — implemented in the launcher.
- Population refiner (finding 3) — implemented + measured (E3: 4/5 recovery
  at fit-deficit 2; admission widened to deficit ≤2 on that measurement).
- fill_holes op — ported, agreement-tested 600/600 (finding 7).
- Dihedral-frames wrapper — under measurement (frames_test.py, 120 training
  tasks, enumerator proposer); ships only if the union recall gain is real.
- Macro-ops — census says the corpus is too small (one bigram at n=2);
  none ship (finding 6).

## 8. Measurement plan (what proves what, in order) [probe BUILT]
- P2a: zero-shot proposer, eval-30 (the flagship's exact subset), K=128 →
  pool recall R0. (Baseline before intervention.)
- P2b: round-0 fine-tuned proposer, same subset, same K → recall R1.
  The flywheel exists iff R1 > R0 by a margin that survives eval-120.
- P2c: full eval-120 probe of the best proposer → the campaign's first
  headline number, reported as measured.
- Every later claim traces to a PROBE_LEDGER.jsonl line. No exceptions.

## 9. The launcher [BUILT + SELF-TESTED 2026-11-01: apex2_probe_launch.py]
Compile-verified; its executor core passes a local selftest (SELFTEST=1):
both canned DSL-1 programs (`colormap`; `rot 2` + `tile_mirror`) fit train
and reproduce test exactly on the two known control tasks (2/2 PASS).
Round-0 data BUILT + AUDITED 2026-11-01: miner final 51 verified programs;
DSL v1.1 executor (local_counts/cross, crop_bbox, scale, mirror-complete/
append, fold, del-extremes, ograv, sort_lines — semantics ported from the
sprint source, never guessed) expresses 50/51 (only copyc_largest_to_5
unmapped), 0 re-verification failures. gen_expand.py turned the pure-function
programs into generators: **sft_round0.jsonl = 13,050 pairs** (50 real +
13,000 generated; 694 dev) and a 13,000-task bank (6,339 shape-preserving
for the TRM lane); independent audit re-verified a 200-task sample 200/200.
trm.py (faithful TRM) is written and compile-checked; its first run is the
P2 smoke (no torch on this box).
Single file for the APEX notebook: config block (paths, model dataset name,
K, slice), vLLM load, §2 encoder, §4 loop with induce.py's executor/gate
inlined, probe-format ledger prints, progressive result banking to
/kaggle/working/apex2_probe_results.jsonl. It runs in P2 the moment the
model dataset is attached; it does not download anything.
