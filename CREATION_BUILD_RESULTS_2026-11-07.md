# Creation Build — Results (2026-11-07)

Preregistration: `CREATION_BUILD_PREREGISTRATION_2026-11-07.md` (filed before building).
Spec: `CREATION_MACHINERY_SPEC_2026-11-07.md`. Anatomy: `CREATION_WALL_ANATOMY_2026-11-07.md`.
Built lane: `nextgen_probe/ng2_lane_creation.py` (the bg-fixed lane `ng2_lane_bg.py` is untouched).
Rows: `nextgen_probe/diag2_creation_rows.json` (G2), `nextgen_probe/census_g0_rows.json` (G0).
Solver core byte-identical to the bg lane, diff-verified by AST source-segment comparison:
`pair_assignments`, `combine_iter`, `loo_check` (and the `determinate()` closure) — IDENTICAL.

## Verdict: BUILD PASS — with the G0 caveat stated at full strength

All five of the spec's build kill criteria pass (KC5 with its two cuts applied; see below).
The fresh-draw conversion probe (spec §3) is therefore commissionable as a separate filing.

**The caveat, at full strength:** G0's re-measurement does NOT lift the ceiling to the
successor's needs. Over the extended grammar's own spent-draw fits, unanimity-and-correct is
**0** under every point treatment (conservative 0/11, determined-only 0/5), and the absolute
ceiling product — the census bg-binding bound F ≤ 0.982 times the most generous U treatment
(every undetermined fit unanimous-and-correct, 6/11) — is **0.535 < 0.90**. Two of the five
determinate extended fits are unanimous-and-WRONG: the creation grammar reproduces the old
grammar's identification failure inside its new fits. The probe is commissionable as a
measurement; nothing in this build's arithmetic supports projecting it to 216/240, and per
the standing rule nothing here does. The sealed exam remains the only 216/240 instrument.

## G0 — Census re-measurement (census protocol: full version-space enumeration, caps 512 schemas / 20,000 combos / 120 s per task, cap hit = undetermined; renders via predict on the test input)

Old grammar (bg lane) on the 4 banked fits: determined 0/4, unanimous 0, unanimous∧correct 0.
U: conservative 0/4, determined-only n/a, ceiling 4/4 (vacuous — nothing determined).

Extended grammar on its 11 spent-draw full fits: determined 5/11, unanimous 2/11
(3d6c6e23, 760b3cac — **both unanimous-and-wrong**), unanimous∧correct **0**.
U: conservative 0/11 = 0.000, determined-only 0/5 = 0.000, ceiling 6/11 = 0.545.

Ceiling products (F × U):
- measured F (spent draw, 11/48 = 0.229) × U point (0.000) = **0.000**
- census F bound (0.982, 938-pool bg-binding bound; the creation extension does not alter bg accounts) × U ceiling (0.545) = **0.535** ← the extended grammar's new ceiling product
- measured F × U ceiling = 0.125

The old F × U ≤ 0.842 bound is void as a bound on the extended grammar, as the spec said it
would be; its replacement binds harder (0.535), because the extension bought fit supply
(4 → 11) at zero measured identification. On the 4 banked fits themselves, the extended
enumeration reads identically to the old (0 determined, 0 unanimous∧correct).

## G1 — Fit preservation: PASS (4/4)

7d1f7ee8 full fit / loo_rejected · a61f2674 full fit / nondeterminate_test_class ·
4acc7107 full fit / loo_rejected · 8dae5dfc full fit / loo_rejected — identical to the
banked bg-lane outcomes on every recorded field, re-verified again after the KC5 cuts.

## G2 — Spent-draw re-run (48 A+B, frozen 25 s/task; total wall 541.4 s)

Taxonomy (lane reason counts, bg → creation):

| reason | bg | creation |
|---|---|---|
| creation_unexplained | 19 | **8** |
| budget | 15 | **13** |
| search_cap | 4 | 7 |
| cover_failed | 2 | 4 |
| inconsistent_phi | 2 | 3 |
| inconsistent_param | 0 | 1 |
| canvas | 2 | 1 |
| loo_rejected (fits) | 3 | 8 |
| nondeterminate_test_class (fits) | 1 | 3 |

**Fit-bearing: 11/48** (bg: 4/48). **Certified solves (accepted ∧ test-correct): 0** —
certification rejects every fit on this draw, exactly as it did for the bg lane; the two
unanimous-and-wrong fits (3d6c6e23, 760b3cac) are among the LOO-rejected.

The 19 creation rows (SPENT-DRAW DIAGNOSTIC — migration = leaving the zero-candidate
state in the designated attempt; an upper-bound diagnostic per spec §2, not a fit count):
**migrated 11/19.**

| task | class | before → after | mechanism |
|---|---|---|---|
| 9110e3c5 | Q | creation_unexplained → **full fit** (loo_rejected) | program:quotient |
| 5d2a5c43 | Q | → search_cap | — |
| 55783887 | L | → cover_failed | — |
| 5c0a986e | L | → search_cap | — |
| 41e4d17e | L | → inconsistent_param | — |
| 27f8ce4f | R | → inconsistent_phi | — |
| 760b3cac | M | → **full fit** (loo_rejected) | union of split-part patterns |
| 694f12f3 | F | → **full fit** (nondeterminate) | inset (instance color) |
| 3d6c6e23 | C | → **full fit** (loo_rejected) | countstack |
| e9afcf9a | T | → **full fit** (nondeterminate) | checker texture |
| 604001fa | P | → **full fit** (loo_rejected) | split-and-discard (M-P) |
| 67b4a34d | Q | stays creation_unexplained | classifier unidentified (anatomy's open problem; killed hypotheses not re-tried) |
| e66aafb8 | Q | stays | domain program does not validate |
| e3497940 | Q | stays | — |
| 363442ee | R | stays | motif fused with spine under every account |
| 85fa5666 | R | stays | lattice completion fails under rank-1 union, rank-1 consensus, and rank-2 consensus semantics (all tested) |
| af22c60d | S | stays | no symmetry completion validates (single involution, full-D4 consensus both fail) |
| 08573cc6 | F | stays | measured geometry is a square SPIRAL (segment lengths 5,5,4,3,2…), not the concentric rings the anatomy describes; M-F's ring family does not cover it |
| 6d0160f0 | G | stays | the +4 scaffold cells are created, not preserved (cell-diff verified); mechanism unidentified — anatomy §2-G is in the truncated portion of the anatomy file (see Defects) |

Bonus movement outside the 19: **3194b014 canvas → full fit via program:quotient**;
6cdd2623 budget → cover_failed; b7f8a4d8 budget → search_cap.

Per-class unblocking (designated tasks leaving the zero-candidate state):
Q 2/5 · L 3/3 · R 1/3 · S 0/1 · M 1/1 · F 1/2 · C 1/1 · T 1/1 · P 1/1 · G 0/1.

## The five kill criteria, adjudicated one by one

1. **Fits lost — PASS.** All 4 banked fits re-certify identically (G1), including after the KC5 cuts.
2. **Unblocking floor (≥10 of 19 leave the zero-candidate state) — PASS.** 11/19.
3. **Budget ceiling (budget deaths ≤ bg lane's 15/48) — PASS.** 13/48. Two of the bg lane's own budget deaths improved (cover_failed, search_cap); none of the 19 creation rows dies by budget in the final build.
4. **U band — PASS, at zero.** Extended unanimous∧correct among determinate fits = 0/5; the old grammar's spent-draw reading on the 4 banked fits = 0 (0 determined). No worse — and no better: the band is met at a point value of zero, which is why the verdict carries the G0 caveat at full strength.
5. **Per-class cut — APPLIED.** M-G (color-class gather) unblocked 0/1 and M-S (symmetry completion) unblocked 0/1; both are **cut from the shipped lane** (gather derivations and union parts removed; `_prog_symclose` removed from the program registry). Post-cut re-verification: all 11 G2 fits hold with identical outcomes and mechanisms; the two cut-class tasks are unchanged. Every other mechanism unblocks ≥1 of its class's tasks and stays.

**Verdict: BUILD PASS.** The §3 fresh-draw probe is commissionable (separate filing; it does
not fire in this lane). Its registered bars, from the spec: 48 untouched tasks from the 890
remaining pool tasks, 12A+36B, seed fixed in its own preregistration; seat bar = conversion
≥ 10×(1/28) guarded to ≥10 fits, OR the unanimity clause (≥8 sample-unanimous judgeable
with ≥3/4 correct, Fisher p printed); secondary diagnostic = creation_unexplained deaths
vs the spent draw's 19/48 (now 8/48 post-build on the spent draw itself). A probe pass
approves no solver.

## Build decisions and disclosures (narrower choices, per the preregistration's rule)

- **Zero-out gating:** creation candidates are generated only for output objects with zero standard candidates. Outputs the standard kinds already explain never pay creation cost; this is what keeps the 29 non-creation tasks on the bg lane's timing profile.
- **Identity-pretransform gate:** creation candidates are generated only under the identity pretransform attempt (Stratum-1 programs are likewise identity-only, on raw pairs, after the object pipeline). Basis, profiled: with creation live in all 40 attempts, dense scenes spent the whole task budget failing attempts — the first union search alone profiled at 24.96 s of one 25 s task. The frozen 25 s cap is part of the machinery (KC3); this gate is the build's compliance with it.
- **Union search discipline (M-U):** exact-cover recursion anchored on a fixed uncovered cell, virtual parts first, an exactly-k subset-sum feasibility sieve over part counts, node cap 20,000 per output. Proposals come only from input objects and scene-generated creation patterns — never subset enumeration of the output.
- **M-C semantics, corrected against measurement:** the count shape is the odd-width staircase of the scene's TOTAL count (T must be a perfect odd sum m²; bars 2m−1…1, widest at bottom); a single color takes all bars, multiple colors take the bar equal to their count. The anatomy's "9/4/9 per-pair counts" for 3d6c6e23 does not survive recount (pair totals are 9/4/9 across the whole scene; pair 2 is 5+3+1 over three colors). The count value carries no phi (scene colors by construction); a recolored stack does not fire it.
- **M-F(ii) inset:** the whole margin-1 interior rectangle is the ink region (measured: a 5×5 block's full 3×3 interior takes the ink), overwriting the object's own cells.
- **M-T texture:** built as a pattern derivation (parity class of an exactly-two-color scene), not a binding-level underlay.
- **Instance colors** ride the derivation key/value discipline (key = instance context, value carries the ink), bound by combine_iter's unchanged key→value agreement — the only route to colors absent from the input, as specified.
- **M-P(i):** the split-group prune is removed; `_group_needs` computes kept-set semantics (parts that have candidates), identically at generation and assignment.
- **Cost caps (disclosed):** marker-mode stamps only for sources with bbox area ≤ 12 and ≤ 12 cells on scenes with ≤ 10 objects, references = the source's own cells; rays/crosses/lines skip objects over 40 cells; reflect/lattice stamps skip sources over 30 cells; part-source stamps are offered only as union parts, not standalone.
- **Robustness fixes found by the gates:** (a) copy_out_ref derivations are dropped when their target output carries an ins=() creation candidate (the byte-protected `pair_assignments` resolves copy sources through `in_objs[ins[0]]` and crashes otherwise — 5d2a5c43); (b) quotient identification now requires uniform input/output shapes across pairs before applying a partition (f4081712 has per-pair output shapes 3×3…8×7); (c) a Stratum-1 program family's own exception kills the family for that task, never the lane.
- **Reason instability note:** under deadline pressure, 3d6c6e23's designated failure read creation_unexplained in one smoke run and inconsistent_phi in another (cap flags are timing-sensitive, as in the bg lane). Its G2 row (full fit) is the run of record.

## Defects flagged

- **`CREATION_WALL_ANATOMY_2026-11-07.md` is truncated on disk** (12,969 chars, ends mid-§2-S with a literal `[truncated 8182 chars]` marker). §1's 19-task table and §2-Q/L/R are complete on disk; §§3–5 and the §2 detail for M/F/C/T/P/G are not in the file. The spec is complete and governed the build; where the anatomy's detail was missing, mechanism semantics were derived from direct grid measurement (countstack, inset, spiral) and are disclosed above.
