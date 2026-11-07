# APEX-2 — ARC Solver Program Charter (2026-11-01)

## Mission
Build the strongest ARC-AGI-2 solver this operation can produce, designed against the
standing bar: **85%+ on the private evaluation set**. Target competition: **ARC Prize 2027**
(the 2026 board closes Mon Nov 2, 2026, 6:59 PM ET with Version 2 as our sole filed entry;
the official bonus text reads "If not met, we intend to roll this forward to 2027").
The 85% figure is the DESIGN TARGET every gate is tuned to. No score is claimed for this
program until the probe prints it from this pipeline's own measurements (Ledger #16/#17).

## Why the last solver scored ~0 (measured, not opinion)
- EVAL FINAL 0/40 test pairs on a 30-task held-out subset; 196 train fits converted to
  zero test solves. Gradient TTT on 2–4 pairs memorizes; train-exact acceptance cannot
  distinguish a rule from a memorization.
- Corpus taught surface statistics, not rules (pretrain loss plateaued ~step 20,000).
- Candidate GENERATION was never measured until the final night. Selection (fit-key
  (1,−1), proved) was optimized on top of a generation stage that produced memorizers.
APEX-2 inverts the order: **generation quality is measured first, cheaply, before any
training run, any corpus build, or any forecast.**

## Architecture — three generation species, bake-off by measured conversion
1. **LLM program induction (primary).** A mid-size open-weight model (Qwen-class, fits an
   L4's 24 GB) generates candidate transformation PROGRAMS in a compact DSL; every program
   is executed against the task's train pairs; only exact-fit programs are scored on test
   inputs; ranking = exact fit, then program simplicity (MDL). This is the architecture
   family the 2026 field's disclosed leaders use, at the largest scale our $0 envelope
   (Kaggle L4 x4, ~30 h/week meter) can run. Test-time search budget per task is set by
   measured yield, not by hope.
2. **Faithful TRM neural lane (floor species).** The published Tiny Recursive Model
   recipe reimplemented as specified — deep-supervised recursive refinement with separate
   latent and answer states — NOT the homebrew variant that shipped in 2026. Published
   anchor for the recipe class: ~8% on ARC-AGI-2 evaluation (reported). Its job: a real,
   honest floor and a bake-off baseline.
3. **DSL synthesis, second generation.** The 2026 sprint's object-centric search, rebuilt
   with its own null results (0/120, twice) as design constraints: wider operator algebra,
   counterexample-guided pruning, MDL ranking, and a hard rule — it competes in the same
   probe as everything else and survives only on measured conversion.

Carried over from v7.1 (proved, keep): the corrected fit-key (1,−1) selection, the
hash-gated packaging discipline, Save & Run All only, one notebook.

## The instrument (built first, before any species)
`probe.py` — the conversion probe. Any component plugs in as
`solve(task) -> up to 2 candidate grids per test input` and is scored exactly as Kaggle
scores: a task counts when every test input has an exact match in its 2 attempts.
Self-validating: an oracle component must print 120/120 and a copy-input null ~0/120
before any real component's number is believed. Every run appends to PROBE_LEDGER.jsonl.
Leading indicator tracked alongside solves: **pool recall** — how often the true rule is
anywhere in the component's candidate pool — because 85% is reachable only when
recall × selection accuracy can arithmetically reach it. A species whose probe math
cannot reach the bar dies in the probe, in hours, not in a six-week run.

## Gates (pre-registered; changes require a written amendment to this charter)
- G1: No component is called a solver before a nonzero probe conversion on held-out eval.
- G2: No Kaggle GPU hour is spent on a component that has not cleared a local probe gate
  (nonzero conversion, or pool recall ≥ 25% with a costed path to selection).
- G3: No forecast is issued except from probe measurements of the actual pipeline on the
  eval distribution (Ledger #16). Fits, loss curves, and queue health are not forecasts.
- G4: Full training runs launch only when probe math projects a private score worth a
  submission slot under the first-sub rule.
- G5: Every result — including zeros — is checkpointed to the ledger the day it lands.

## Resource envelope
$0 spend. Local 2-core CPU: probes, DSL search, harness work. Kaggle L4 x4 (~30 h/week,
refill ~Sat 00:00 UTC, unverified): LLM inference and neural training. The user's hands
execute Kaggle account actions only (ToS), on agent-built, hash-verified packages.

## Sequence
- Nov 2026: probe harness live (today); species 3 v2 into the probe; species 2 spec
  written from the paper; species 1 model + inference smoke prepared for the first
  quota window after refill.
- Dec 2026: first GPU probes (LLM induction on eval slices); bake-off table v1.
- 2027: iterate species on probe math; full runs only through G4.
Alongside: the Nov 8, 2026 writeups (2026's judged money) and the NS campaign continue;
they do not compete with this program for the user's hands.

## Addendum — 2026-11-01 evening (user order, restated non-negotiable)
- DESIGN TARGET restated at full strength: 90%+ on the private eval
  (216+ of 240), picture-perfect standard, built to 2030 standards.
  This is the bar the architecture and gates are set against.
- Method latitude: any means — every generation species, flywheel
  rounds, in-run TTA, ensembles — inside the three standing fences
  (no fabrication, no disqualification risk, no illegal means).
- Certification law unchanged (user's own fabrication ban): no score
  is claimed above what the probe pipeline measures. The target
  governs the build; measurements govern the claims.
