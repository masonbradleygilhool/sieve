# APEX-2 research notes — seasoning pass, 2026-11-01
Each finding names its source and the design change it caused. Claims are
labeled with the strength of their evidence.

1. **Separation of perception / proposal / consistency filtering.**
   Compositional neuro-symbolic pipeline (arXiv 2604.02434): object-level
   abstractions + neural transformation proposals + symbolic cross-example
   consistency lifted a base LLM 16% -> 24.4% on ARC-AGI-2 public eval
   (30.8% combined with a second solver). [reported, peer-review track]
   -> APEX-2 already has this shape; the OBJECT CHANNEL was specced but not
   implemented. Now implemented in the prompt encoder (launcher + both data
   builders, byte-identical formats) and the round-0 data regenerated.

2. **Train-perfect is not rule-true; certificates separate them.**
   LOO-by-reinduction study (public draft, render-verified artifacts):
   train-perfect programs were correct on hidden tests only 33.2% of the
   time; programs whose PROCEDURE re-derives under leave-one-out were
   correct 95.3%. Its parameter preference lattice (relational > feature >
   induced-map > constant) predicted hidden-test correctness monotonically
   (0.92 -> 0.09). [reported, single-source, strong internal evidence]
   -> Two changes: (a) the ranker now scores parameter PROVENANCE
   (relational ops +2, geometric +1, constant-bearing +0) after vote count;
   (b) near-miss traces are recorded in probe output as flywheel data.
   The full LOO-reinduction gate is a P2+ item for the sampling loop
   (re-run search on pair subsets for top candidates -- costs samples,
   gated by the governor).

3. **Refinement loops: population yes, sequential self-correction no.**
   Official ARC Prize 2025 report: "the year of the refinement loop";
   SOAR (2nd paper prize) = evolutionary program refinement + fine-tuning
   on its own search traces (52% ARC-AGI-1). Counterweight (arXiv
   2606.31543): iterative refinement and prescriptive templates REDUCE
   hypothesis diversity and degrade results. [official + reported]
   -> refine() in the launcher is population mutation (delete / insert /
   swap / numeric perturb / arg-sibling swap over the whole near-miss set),
   never a sequential chain. Measured E3: sibling-substitution near-misses
   land at fit-deficit 2 (not 1); refine() recovered 4/5. Admission widened
   to deficit <= 2 on that measurement.

4. **TRM test-time adaptation.** McGovern 2025 (arXiv 2511.02886): a TRM
   pretrained on public tasks, then FULLY fine-tuned in-run on the test
   tasks' train pairs (12.5k steps), reached 6.67% semi-private from a ~10%
   public base. [reported]
   -> Blueprint S7 gains an in-run TTA stage for the TRM lane (cheap at 7M
   params; runs inside the envelope before solving).

5. **Grammar-constrained decoding removes parse failure, not semantic
   failure** (PICARD / Synchromesh line, established). [established]
   -> P2 option: vLLM guided decoding with a DSL-1 line grammar; adopted
   only if the P2 parse-fail rate says it pays.

6. **Library learning needs corpus mass.** DreamCoder/STITCH: sleep-phase
   abstraction compresses the corpus into macro-ops. Our census over the
   50 verified programs: only ONE bigram reaches n=2 (rot+tile_mirror).
   [measured, local]
   -> NO macros ship in v1.2. The flywheel grows the corpus; the census
   re-runs every round and macros are admitted only at n>=5 with an MDL
   gain, each macro re-verified against the seed set before admission.

7. **fill_holes port.** Semantics read from the sprint source; first port
   disagreed 62/600 (surround-mode tie-breaking: Counter's first-encounter
   order vs argmax-smallest). Fixed to replicate the reference semantics;
   agreement now 600/600 on random grids x both targets. [measured, local]
   -> The op ships. Standing rule reinforced: a port is verified only at
   100% agreement with its reference on randomized inputs.

## LOO certificate calibration (measured 2026-11-01, loo_cert_test.py)
50 known-true seed programs: full-fit 50/50; LOO re-derivation pass 44/50 = 0.88.
All 6 sub-1.0: induced-map programs (colormap x1, local_cross x2, local_counts x3)
with single-attestation table entries. Verdict: LOO ships as a SOFT ranking tier
(loo_frac on the group representative, after votes, before provenance) in
apex2_probe_launch.py solve_task; never a hard gate. Miner pass 2 launched
same day: sprint solver at 120s/task over the 949 unsolved training tasks,
output mining_results2.jsonl.

## Coverage autopsy + miner3 (measured 2026-11-01, autopsy.py / miner3.py)
Autopsy (1,000 training tasks; solved=51 vs unsolved=949): solved skew SMALL
(median input max-dim 5 vs 12); 301/949 unsolved have median input >15.
Unsolved skew SHRINK (24.3% vs 9.8% of solved); grow tasks solve well (tiling
family covered); new-colors not a discriminator (0.26 vs 0.30).
Miner3 = DSL v1.1 enumeration engine (depth 1 exhaustive, depth 2 reduced,
25s cap) over the 949. FIRST SOLVE inside 10 seconds: 00d62c1b by
'fill_holes 4' — an op the sprint engine never had. Multi-engine coverage
thesis confirmed by measurement; pass running.
Miner2 FINAL (2026-11-01): 949 mined at 120s/task, 0 solved. The sprint
engine's ceiling is its op set — 5x budget bought exactly nothing (null).
Miner3 at 700/949: 2 banked, both fill_holes constant-target (00d62c1b
'fill_holes 4', a5313dff 'fill_holes 1') — a family the sprint engine lacks.
Library now 53 verified programs, miner3 still running (depth-2 tail).
Miner3 FINAL (2026-11-01): 949 tasks, 2 new solves (both fill_holes). Library 53.
DEFECT FOUND + FIXED same day: the prompt DIGEST omitted fill_holes entirely —
the executor had the op, miner3 proved it solves real tasks, but the LLM
proposer would never have been told it exists and round-0 data had 0 examples.
DIGEST fixed in launcher + sft_seed.py (kept byte-identical); selftest 2/2.
Miner3/4 programs folded to sft_seed_m34.jsonl (2 emitted, 0 reverify fails).
Miner4 launched: widened depth-2 (full D1 x reduced D2, 45s cap).
DSL v1.2 (2026-11-01): tile_collapse (pure) + recolor_by_size (pairs-learned)
added to the executor, both relational provenance, DIGEST updated in both
files (byte-identical, selftest 2/2). Family probe over the unsolved 947:
tile_collapse 1 hit, quadrant/half 0 (family killed), recolor_by_size 6 hits.
CORRECTION: the probe's recolor check built its rank->color mapping over
train+test together — test leakage. The launcher gate (learn train, predict
test) is the honest instrument: 4 of 7 banked (7b7f7511 tile_collapse;
08ed6ac7, b230c067, ea32f347 recolor_by_size). Library 53 -> 57.
tile_collapse sanity: 200/200 returned a grid-regenerating tile (194 equal
to the sampled tile; 6 found a smaller true period — correct behavior).
Family probes round 2 (2026-11-01, probe_families2.py, honest train-learn/
test-predict gate): crop_color 0, interior 0, sample_grid 0, keep_color 0.
All four families dead on measurement; no ops shipped. Cheap nulls by design.
MINING CLOSED (2026-11-01): pass 4 final null (947 tasks, 0 solves) — widened
depth-2 enumeration exhausted, consistent with pass 2. Enumeration is dead as
a proposer at every width tried; library final at 57 verified programs.
SFT ROUND 1 BUILT + AUDITED (gen_expand_r1.py): 56 real pairs + 14,104
generated = 14,160 records; bank audit 200/200 exact (third consecutive
clean audit); object channel 500/500; fill_holes taught (1,002 records —
the family the old DIGEST hid); tile_collapse 105 records (low generator
yield, expected); recolor_by_size generates 0 (identity under empty pairs —
real pairs only; generator-side fabricated rank maps are future work).
Gz: sft_round1.jsonl.gz 5.89MB, synth_tasks_r1.jsonl.gz 5.21MB.

## REFORM round (2026-11-01 PM, user order: reform + keep evolving)
- Analogy/transplant proposer BUILT (analogy.py): signature retrieval over
  the 57-program library + generated-bank programs, parameter re-induction
  on the target's train pairs. MEASURED: eval-30 pool recall 0/30;
  eval-120 pool recall 2/120, solves 0/120 (both recall hits fit train and
  missed test — train-fit is not the rule, again). VERDICT: demoted as a
  proposer; signature machinery retained as parts. Whole-program transplant
  does not cross the train/eval boundary at this library scale.
- Qwen OAuth rail CHECKED AND DEAD (2026-11-01 ~5:24 PM): qwen-code CLI
  installed locally; `--auth-type qwen-oauth` returns the tool's own
  notice: "Qwen OAuth free tier was discontinued on 2026-04-15." The
  2,000-req/day free OAuth tier no longer exists; the CLI itself redirects
  to OpenRouter (already in flight). Install removed.

## Frontier research synthesis — 2026-11-01 night (deep-research report,
## ~/workspace/research_notes/arc-agi2-frontier-methods-2026-20261102-0227/)

Facts that move the design (all sourced in the report):
- NO published PRIVATE-eval result >=85% exists anywhere. >=85% appears
  only on SEMI-PRIVATE, only from closed frontier models at max
  reasoning effort (GPT-6 Astra 95.0, Opus 5.5 93.3, GPT-5.6 Sol 92.5,
  Gemini 4 Argon 91.3). Best private on record: NVARC 24.03% (2025 set,
  frontier-distilled synthetic SFT of Qwen3-4B + per-puzzle LoRA TTFT).
- 2026 public board (read live 2026-11-02): Tufa 88.06, Fields 87.22,
  nvbanana 83.89, Domdolus 83.47 (=new figure; supersedes 82.08).
  Public is ~semi-private; private finals unknown. NO top team has
  disclosed a method. Domdolus's only signal: Qwen3.8-Flash-Next
  eligibility (125B MoE, ~74.5GB min GGUF) — fits Kaggle's RTX PRO
  6000 class, NOT a 24GB card. OPEN ITEM: verify what GPU classes
  Kaggle offers our notebooks now (agent read, Friday with P2 prep).
- Winners emit GENERAL PYTHON, not DSLs. Universal gate: exact replay
  of all train pairs. A hand-written object DSL as search space scored
  0/120 public eval (negative control — that is our own sprint result
  cited back). BARC collapsed 38% AGI-1 -> 0.8% AGI-2 eval.
- Selection is a first-class loss: Land oracle 86.23 vs final 76.65
  (10.18% selection failure; 13.17% no-correct-candidate). SOAR vote vs
  oracle gap 9.5 pts; search saturates ~5.2k samples. Berman: LOOCV
  scoring, only 40 candidates/task, top-2 DIVERSE attempts.
- NVARC recipe: NL rule descriptions -> skill-mixing -> LLM-written
  INPUT-GENERATOR programs (unit-test filtered) -> output programs by
  cross-sample consistency -> 3.2M augmented samples; per-puzzle LoRA
  TTFT r=256 + 8-augmentation re-scoring. TRM+Qwen ensemble FAILED on
  scorer mismatch (20.28 < 21.53 Qwen-only).
- Akyurek TTT: per-task LoRA r=128 + LOO task construction from demos
  + invertible-transform voting; all three ablated-necessary (AGI-1).
  McGovern: full FT > LoRA for TRM test-time post-training.

DECISIONS (agent, 2026-11-01 night, from this evidence):
D1. Primary emission language = PYTHON (sandboxed executor, exact
    replay gate unchanged). DSL-1 demoted to flywheel generation +
    mining + fast path. Rationale: every winning induction system;
    the model's pretrained prior is Python; DSL-as-search measured
    0/120 twice (sprint + our enumeration).
D2. SFT v2 data: translate the mined library + compose chains into
    Python programs mechanically (each DSL op is already a Python
    function in the launcher) -> (task, python) pairs at scale.
D3. P2 measures zero-shot pool recall for the PYTHON arm first
    (base coder model natively fluent); DSL recall becomes the
    secondary read. K can shrink if ranking holds (Berman 40/task;
    SOAR saturation) -> protects the 6h envelope.
D4. Finisher lane upgraded: per-task LoRA TTFT (NVARC/Akyurek shape)
    joins TRM as a bake-off arm; transform-vote re-scoring across the
    fixed 8 dihedral transforms for tied candidates.
D5. Flywheel v2 adopts the input-generator trick: generators as
    functions with unit-test filters, not only grid samplers.
