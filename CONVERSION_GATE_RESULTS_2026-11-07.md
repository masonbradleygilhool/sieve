# EXEC-SYNTH Conversion Gate — Results (2026-11-07/08)

Registration: `~/workspace/arc_apex2/CONVERSION_GATE_PREREGISTRATION_2026-11-07.md`
Draw: seed 23007196, 48 fresh disjoint pool-B tasks. Kit: apex2-conversion-gate dataset.
Notebook: notebook1c118f1637. Model: openai/gpt-oss-120b, L4 x4, internet OFF.

## V15 (failed, instrument-only)
- Committed 2026-11-07 ~5:48 PM EST. Ran 223.1s, Accelerator: None, Output 0 B.
- Root cause (found in the editor): Session options Accelerator was "None currently selected" — the commit inherited it. The gate probe refused (PROBE FAIL: torch.cuda.is_available() is False). 0/48 tasks, no quota burned.

## V16 (complete) — scriptVersionId 366753728
- Accelerator pinned and proven live first (console: True, 4 x NVIDIA L4; Advanced Settings "Run with GPU for all sessions"). Log header: "Accelerator: GPU L4 x4".
- Runtime 18,613.5s (5h 10m 14s), 2026-11-07 6:32 PM – 11:57 PM EST. Finished inside remaining quota (the 00:00 UTC refill landing mid-run is corroborated by completion).
- **GATE_DONE supplied=15/48 certified=7/48 tasks_complete=48/48 status=complete generations=1519**

## Counts (three-way consistent: GATE_DONE line, 48 verbatim per-task lines, full rows-file content read in-browser)
- Supplied / fit.full_fit=true (15): ae4f1146, 5587a8d0, 00576224, d10ecb37, 7ee1c6ea, 77fdfe62, c48954c1, 4347f46a, 19bb5feb, eb281b96, 0b17323b, e9ac8c9e, 91714a58, 1a07d186, 2281f1f4.
- Certified=true (7): 00576224, d10ecb37, 4347f46a, eb281b96, e9ac8c9e, 91714a58, 2281f1f4 — all loo_status pass.
- Supplied, not certified (8): loo_rejected (5) ae4f1146, 7ee1c6ea, 77fdfe62, c48954c1, 0b17323b; shape_loo_rejected (3) 5587a8d0, 19bb5feb, 1a07d186.
- Not supplied (33): all full_fit=false, cert_reason no_fit.

## Adjudication (desk, 2026-11-08) — PASS
- C = 7 >= 4 (seat bar).
- Conversion clause, scale-free reading (operative per desk ruling): F = 15 >= 10; C/F = 7/15 = 0.4667 >= 10x(1/28) = 0.357 — FIRES.
- Packet operationalization: 7 certified from 15 fits (<=20) — also fires.
- **EXEC-SYNTH takes the Stage-T candidate-source seat WITH prior evidence.** Approves no solver; Exam #1 unspent. Packet §1 sequence commissioned as its own filing.
- Scale note: certified 7/48 = 14.6% of tasks; conversion 13.1x the old grammar's measured 1/28.

## Provenance
- Rows file conversion_gate_rows.json (232.34 kB display) exists ONLY as the Version 16 script output — NOT in dataset bigmodel-run-c1a (that holds only a day-old V1; auto-sync off). Browser download of the file failed (Kaggle opens it as a signed GCS page; download tool captured nothing); full raw content was read in-browser and cross-checked against GATE_DONE. Local fetch remains possible any time via a fresh signed URL from the Version 16 Output page.
