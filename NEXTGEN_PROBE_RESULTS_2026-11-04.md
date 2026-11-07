# NEXT-GEN PROBE v1 — RESULTS (2026-11-04)

**Design:** `NEXTGEN_SOLVER_DESIGN_2026-11-04.md` (gates pre-registered
in its §5, before the run). **Lane:** `nextgen_probe/ng_lane.py`
(correspondence-first schema induction, LOO acceptance, abstention on
rejection). **Run record:** `gauntlet/runs/run_1793816913_seed20261104_nextgen_v1.json`.
**Diagnostic:** `nextgen_probe/diag.py` → `nextgen_probe/diag_rows.json`.
All numbers MEASURED. Total wall for the 60-task draw: **1.5 s** (the
DSL baseline's same-size draw took 627.6 s). Spend: $0, zero API calls.

## Controls (gate: must pass before the run counts)

| Control | Result |
|---|---|
| Positive — synthetic known object rule (move+recolor, deletion class), 3 train pairs | **PASS** — solved, schema LOO-certified (`loo: True`) |
| Negative — same inputs, train outputs shuffled across pairs | **PASS** — no schema induced, nothing accepted |
| Harness — on record | probe.py oracle 120/120, null 0/120; gauntlet baseline sane on pool C |

## Headline (gauntlet, draw A:12 B:36 C:12, seed 20261104, 25 s/task)

| Pool | n | Solved | Train-fit-only | No-fit | Rate | Wilson 95% |
|---|---|---|---|---|---|---|
| A — AGI-1 eval, strict-fresh | 12 | 0 | 0 | 12 | 0.0% | [0.0%, 24.3%] |
| B — AGI-2 train, record-fresh | 36 | 0 | 0 | 36 | 0.0% | [0.0%, 9.6%] |
| **A+B — fresh real tasks** | **48** | **0** | **0** | **48** | **0.0%** | **[0.0%, 7.4%]** |
| C — compose control | 12 | 0 | 0 | 12 | 0.0% | [0.0%, 24.3%] |
| All | 60 | 0 | 0 | 60 | 0.0% | [0.0%, 6.0%] |

The A+B headline is identical to the DSL baseline's 0/48. No solves of
any mechanism tag (object_schema / colormap_only / grid_transform) were
produced, so the F3 degeneracy override is moot.

## Where induction died (diagnostic taxonomy, all 60 drawn tasks)

| Stage of death | A+B (n=48) | C (n=12) | All |
|---|---|---|---|
| **Creation / split-merge** — an output object has no same-cell-count dihedral source among input objects | 35 | 5 | 40 |
| **No shape-compatible transform** — output shape is not a dihedral image of input shape (size-changing rule outside v1's canvas rules) | 11 | 7 | 18 |
| **LOO-rejected** — full train-fit schema induced, held-out re-induction failed to predict the held pair; lane abstained | 2 | 0 | 2 |
| Accepted schema | 0 | 0 | 0 |

The 2 LOO-rejected tasks (both pool B): `ecb67b6d`, `5521c0d9`. These
are the only tasks in the draw where the v1 schema language fit every
train pair at all — **full-fit coverage 2/48 on A+B (4.2%)**.

Cross-pair consistency (class-action conflicts, nonconstant
displacement, color-map conflicts) was the recorded death stage for
**zero** tasks — not because consistency is easy, but because the two
reach stages starved it: induction almost never survived pair
accounting, so consistency was barely reached.

## Verdict against the pre-registered gates

- **F1 (reach): TRIGGERED.** Full-fit coverage 4.2% on A+B < the 10%
  floor. The v1 correspondence representation — objects preserved up
  to dihedral transform + recolor + translation, or deleted — does not
  reach ARC-AGI-2's rule space.
- **F2 (conversion): TRIGGERED.** 0 accepted solves on A+B.
- **Gate verdict: KILL.** Per the pre-registered text, the design as
  specified — this schema language — is dead at probe strength. No
  iteration on it without a new measured idea. The gates are not
  amended after the fact.

## What the probe established (measured, at exactly this strength)

1. **The acceptance gate works.** LOO re-induction caught 2 of 2
   full-fit schemas that did not generalize within their own task —
   the exact species (train-exact, non-transferring) that produced
   196→0 in 2026 and the gauntlet's 4 DSL false positives. Under the
   dead lanes' acceptance rule these would have been emitted as train
   fits. The certification component is validated machinery and is
   reusable by any successor.
2. **The failure is localized to representation reach, not to
   selection, ranking, budget, or consistency.** 58 of 60 tasks died
   before consistency was even tested: ARC-AGI-2's fresh-task rules,
   at object level under modal-background segmentation, predominantly
   *transform* objects (grow, shrink, reshape, split, merge, draw) and
   *change grid size* — operations the v1 schema language excluded by
   design. Any successor must treat object transformation and size
   change as first-class schema citizens; that is a different schema
   language, not a tuning of this one.
3. **The probe economics are proven:** a decisive, gate-armed
   measurement of a new mechanism cost 1.5 s of CPU and $0. The
   kill was cheap because the falsifier ran first, as designed.

## What was NOT established

- Nothing about the private eval (240 tasks). The 90%+ acceptance
  criterion is untouched by this probe except negatively: this design
  does not move toward it.
- LOO acceptance is validated as a *filter* on 2 positive instances
  plus 1 synthetic control; its value as a component is a measured
  preliminary, not a proof.
- Correspondence-first construction as a *principle* is not falsified
  — its v1 language is. The distinction matters for the record and
  changes nothing about the verdict: principles don't get iterated on
  credit; a successor design starts from the taxonomy above and earns
  its own probe.

## Files

- Design + gates: `NEXTGEN_SOLVER_DESIGN_2026-11-04.md`
- Lane: `nextgen_probe/ng_lane.py`; controls: `nextgen_probe/controls.py`
  (both PASS); diagnostic: `nextgen_probe/diag.py`, `diag_rows.json`
- Gauntlet run record: `gauntlet/runs/run_1793816913_seed20261104_nextgen_v1.json`
- Drawn task ids: in the run record (seed 20261104; A-pool overlap with
  the baseline draw is by construction — pool A has only 18 tasks).
