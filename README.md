# SIEVE

A program-synthesis solver research project for the ARC Prize (ARC-AGI-2),
run measurement-first.

## The approval law

No solver in this project is called a solver until it earns it. Approval
requires a sealed in-house examination — 240 unseen tasks under the
competition's time conditions — passed at 216 of 240 or better. Nothing is
projected to that number from smaller draws, and no score is stated anywhere
in this repository ahead of the measurement that produced it.

## How the work runs

- Every measurement is pre-registered before it fires: the draw, the bar,
  the kill criterion, and what each outcome closes.
- Evaluation is fresh-draw first. A result that does not transfer off the
  draw it was built on is recorded as a failure of the approach, not tuned
  until it passes.
- Approaches are species, and species close. When a line is measured dead —
  a ceiling proof, a flat null at full width, a fresh-draw kill — it is
  closed in the record and replaced, never re-run in the same form.
- Sample unanimity is never used as a selection mechanism. Selection is by
  execution against held-out folds, under a frozen certification procedure.

## Contents

The documents at the root are the campaign record: architecture
derivations, censuses, pre-registrations, and results, in the order they
were produced — including the negative results, unedited. `nextgen_probe/`
holds the current solver instrument and its diagnostic lanes.

Current state, stated once and updated only by measurement: several solver
species have been built, measured, and closed; the redesign commission in
this repository names the lines now under test. Approved solvers: none yet.
That is the honest state of the work, and the record behind it is the point
of this repository.
