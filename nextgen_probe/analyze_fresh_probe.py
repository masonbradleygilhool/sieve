#!/usr/bin/env python3
"""Fresh-probe analysis: every statistic registered in
FRESH_PROBE_PREREGISTRATION_2026-11-07.md, computed from
diag_fresh_probe_rows.json + census_fresh_rows.json. Prints a JSON
summary (also written to fresh_probe_analysis.json) for the results
document. The Fisher test is fisher_exact_greater copied verbatim
from friday_bigmodel_kit/sample_version_space.py (exact integer
arithmetic via math.comb); the plumbing check against the filed
validation (6/8 vs 1/9 -> p = 0.013369) runs first and aborts on
mismatch."""
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

HERE = Path("/home/hatch/workspace/arc_apex2/nextgen_probe")


def fisher_exact_greater(a, b, c, d):
    """Verbatim from friday_bigmodel_kit/sample_version_space.py:
    one-sided Fisher exact p for table [[a, b], [c, d]]."""
    n = a + b + c + d
    row1 = a + b
    col1 = a + c
    denom = comb(n, row1)
    p = 0.0
    for x in range(a, min(row1, col1) + 1):
        p += comb(col1, x) * comb(n - col1, row1 - x) / denom
    return p


def main():
    p_check = fisher_exact_greater(6, 2, 1, 8)
    assert abs(p_check - 0.013369) < 5e-7, \
        f"Fisher plumbing check FAILED: 6/8 vs 1/9 -> {p_check}"
    print(f"fisher plumbing check: 6/8 vs 1/9 -> {p_check:.6f} "
          f"(filed 0.013369) OK")

    rows = json.load(open(HERE / "diag_fresh_probe_rows.json"))
    census = json.load(open(HERE / "census_fresh_rows.json"))
    assert len(rows) == 48, len(rows)

    fits = [r for r in rows if r["full_fit"]]
    cert = [r for r in rows if r["accepted"] and r["test_ok"]]
    conversion = (len(cert) / len(fits)) if fits else None

    det = [r for r in census if r["completed"]]
    unan = [r for r in det if r["unanimous"]]
    ucorr = [r for r in unan if r["correct"]]
    uwrong = len(unan) - len(ucorr)
    assert {r["tid"] for r in census} == {r["tid"] for r in fits}, \
        "census population != lane full fits"
    fisher_p = fisher_exact_greater(len(ucorr), uwrong, 1, 8) \
        if unan else None
    u_cons = len(ucorr) / len(fits) if fits else None
    u_det = len(ucorr) / len(det) if det else None
    u_ceil = (len(ucorr) + len(fits) - len(det)) / len(fits) \
        if fits else None

    clause_conv = conversion is not None and \
        conversion >= 10 * (1 / 28) and len(fits) >= 10
    clause_unan = len(unan) >= 8 and len(ucorr) * 4 >= 3 * len(unan)
    verdict = "PASS" if (clause_conv or clause_unan) else \
        ("KILL" if len(cert) == 0 else "MIDDLE")

    out = {
        "n_tasks": len(rows),
        "per_pool": {
            pk: {"n": sum(1 for r in rows if r["pool"] == pk),
                 "fits": sum(1 for r in rows
                             if r["pool"] == pk and r["full_fit"]),
                 "certified": sum(1 for r in rows
                                  if r["pool"] == pk and r["accepted"]
                                  and r["test_ok"])}
            for pk in ("A", "B")},
        "fits": len(fits),
        "fit_ids": sorted(r["tid"] for r in fits),
        "certified": len(cert),
        "certified_ids": sorted(r["tid"] for r in cert),
        "conversion": conversion,
        "conversion_vs_1_28": conversion / (1 / 28)
        if conversion is not None else None,
        "conversion_vs_1_18": conversion / (1 / 18)
        if conversion is not None else None,
        "taxonomy": dict(Counter(r["lane_reason"] for r in rows)),
        "classes": dict(Counter(r["class"] for r in rows)),
        "creation_unexplained": sum(
            1 for r in rows if r["lane_reason"] == "creation_unexplained"),
        "errors": [r["tid"] for r in rows if r["class"] == "error"],
        "sample_U": {"treatments": {
            "conservative": [len(ucorr), len(fits), u_cons],
            "determined_only": [len(ucorr), len(det), u_det],
            "ceiling": [len(ucorr) + len(fits) - len(det),
                        len(fits), u_ceil]},
            "determined": len(det), "undetermined": len(fits) - len(det),
            "unanimous": len(unan), "unanimous_correct": len(ucorr),
            "unanimous_wrong": uwrong,
            "unanimous_judgeable": len(unan),
            "fisher_p_vs_grammar_1_of_9": fisher_p},
        "seat_lines": {
            "seat_a_certified_ge_4": len(cert) >= 4,
            "seat_b_fits_ge_20_at_conversion_ge_1_18":
                len(fits) >= 20 and conversion is not None
                and conversion >= 1 / 18},
        "clauses": {"conversion_clause": bool(clause_conv),
                    "unanimity_clause": bool(clause_unan)},
        "verdict": verdict,
    }
    (HERE / "fresh_probe_analysis.json").write_text(
        json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
