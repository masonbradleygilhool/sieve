# APEX-2 Campaign Plan — Director's Plan (2026-11-01)

Authority: user's order, 2026-11-01 — the agent directs and runs this campaign;
the user's hands execute Kaggle account actions only. Charter gates G1–G5 govern.

## What today's measurements changed (2026-11-01, probe ledger)
- induce_v0 (MDL enumeration, geometric/gravity/colormap algebra, depth ≤3,
  4,364 programs/task): control 2/6 (both known positives, after the colormap
  format bug was found and fixed). **Eval-30 (the flagship's exact subset):
  0/30 solves, pool recall 0/30** — no eval task's rule exists anywhere in this
  algebra's depth-≤3 space. Combined with the sprint's 0/120 (twice, wider
  algebra, beam search): **pure enumeration is DEAD as a generation species.**
  It survives as (a) the DSL's semantics testbed and (b) a mining tool.
- Re-weighting, effective now: Species 1 (LLM program induction) is the campaign.
  Species 2 (faithful TRM) is the parallel floor. Species 3's remaining value
  is its verified operator library, which becomes the DSL the LLM writes in.

## The central asset: a verified program library (mining, starts today)
Mine all 1,000 ARC-AGI-2 training tasks with the sprint's full solver
(25 s/task, 2 CPU procs, resumable, every result checkpointed). Output:
(task -> verified program) pairs. Three uses, in order:
1. **Measurement**: the true training-set recall of the strongest CPU search we
   own — the baseline every later proposer is compared against.
2. **Distillation data (the $0 rule-true channel)**: verified programs are
   ground-truth (task, program) pairs for fine-tuning the open-weight proposer
   — the NVARC move (distill a strong teacher) with our own solver as teacher.
3. **DSL design evidence**: which operators actually appear in verified
   solutions sets the DSL v1 grammar the LLM will generate in.

## Phases
- **P0 (today)**: miner launched; DSL v1 grammar drafted from the sprint's
  operator library (program = typed sequence over ~40 verified primitives,
  incl. object ops, with the executor + fit gate already built in induce.py).
- **P1 (Nov, CPU)**: mining completes; library published to the ledger;
  proposer fine-tune set built (task grids -> program text, exact format the
  inference loop will consume). TRM-faithful implementation written from the
  paper and unit-checked locally (shapes, deep-supervision losses, recursion).
- **P2 (first quota windows, ~Sat 00:00 UTC refills)**: Kaggle L4 —
  (a) base-model zero-shot induction probe on eval slices (measure BEFORE any
  fine-tune: Ledger #17), (b) fine-tuned proposer probe, (c) TRM baseline
  training probe. Every number through probe.py, into the ledger.
- **P3 (Dec–2027)**: bake-off iterations on probe math; hybrid assembly
  (LLM induction primary, TRM floor, symbolic banks where they verify);
  full runs only through charter gate G4.

## Kill / promote rules (pre-registered)
- A proposer whose eval pool recall (train-exact program present) stays <10%
  after its P2 probe is demoted to parts; its budget moves to the leader.
- Any component claiming solves must reproduce them through probe.py on the
  full eval-120 before the claim is written anywhere.
- The campaign's standing forecast rule: numbers come from the ledger or they
  are not said.

## Resource ledger
CPU (this box): mining ~2–4 h wall for the full 1,000, then idle-watch.
Kaggle quota: untouched until P2; ~30 h/week meter planned against named
probes only, one run at a time, Save & Run All only.
Spend: $0.
