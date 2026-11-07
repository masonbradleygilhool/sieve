# SIEVE Friday — Feasible Pass Design (2026-11-06, from the SMOKE calibration)

**Purpose.** Version 2's SMOKE passed and priced the rail. The kit's
Pass A / Pass B as written do not fit the week's quota at the measured
rate (priced in §3.4). This design re-scopes the fetch — unit subset
and per-unit k — so the registered verdict lines in
`friday_bigmodel_kit/HARNESS_READY.md` and
`friday_bigmodel_kit/FRIDAY_SAMPLE_STATS.md` stay **reachable**, in
verdict-bearing order, inside ~20 GPU-hours. No bar is moved; the
frozen certification is untouched; what changes is only the fetched
supply, and the supply is stated exactly wherever a verdict is read
from it. The split-at-unit-boundary remedy is the conversion packet's
own registered gate (`NOVEMBER_CONVERSION_PACKET.md` §1.1: "a fetch
whose extrapolated hours exceed the week's remaining quota is split
at a unit boundary — the cache is resumable and a quota cut loses
nothing").

---

## 1. Calibration (measured, Version 2 commit log, 2026-11-06 ~8:30 PM ET)

- **SMOKE OK (gptoss): 12 completions, 135 completion tok/s** —
  4× L4, vLLM 0.33.0, TP=4, `max_num_seqs` 32, `max_model_len` 32,768,
  completion cap 16,384, reasoning high, flashinfer sampler disabled
  (`VLLM_USE_FLASHINFER_SAMPLER=0` — required in every commit).
- **Mean completion length (central): L̄ = 12,688 tok.** From the
  script's own printed extrapolation (15,360 completions ≈ 401 h at
  135 tok/s ⟹ L̄ = 401 × 3600 × 135 / 15,360 ≈ 12,688). Raw smoke
  totals agree in scale (10 completions = 134,521 tok). Several smoke
  completions hit the 16,384 cap exactly (first two = 32,768 tok).
- **Pessimistic length: 16,384 tok** (every completion truncates at
  cap). Per-completion time: central 12,688/135 = **94.0 s**;
  pessimistic 16,384/135 = **121.4 s**.
- **Uncertainty, stated.** n = 12 completions, one task
  (834ec97d, class B), two fold units — the smallest-prompt units in
  the pack (the smoke takes the first records after the script's
  est-token sort). Full-task units may reason longer. And the smoke's
  135 tok/s was measured at n=2 samples per prompt, largely
  sequential, with ~3 min of model load inside the elapsed window;
  the fetch regime (n = k per prompt, up to 32 concurrent sequences,
  prefix caching on) is expected to run faster per token. **No faster
  rate is priced anywhere in this design** — 135 tok/s is the floor
  every number below is built on, and Commit 1 re-measures the true
  fetch rate before any later commit is sized (§5).
- **Fixed overhead per commit: 0.15 h** (pip install vllm ≈ 3 min,
  measured in the Version 1 log at 183 s; weights + engine load
  3.0 min, measured in Version 2; probe + tokenizer + prompt load
  ≈ 2 min; rounded up).
- **Budget:** ≤ **20.0 h** of commit runtime total (quota remaining
  ≈ 27 h 41 m; ≥ 7 h margin held). Session cap **9 h** per commit.

## 2. Unit-list anatomy (from `bigmodel_fetch.py`, `units.json`, the pack)

- The pack holds **259 prompt files** = one per **unit**. A task's
  units are its **full-task unit** (tid = bare task id, prompt shows
  every train pair) plus **one LOO fold unit per train pair**
  (tid = `<task>__fold<j>`, prompt holds out pair j). Per class:
  **A: 12 tasks, 58 units (12 full + 46 folds); B: 36 tasks, 153
  units (36 full + 117 folds); C: 12 tasks, 48 units (12 full + 36
  folds).** Seat scope A+B = 48 full + 163 folds = 211 units.
  A+B folds per task: min 2, median 3, max 6, mean 3.4. C folds: 3
  per task exactly.
- **`APEX2_MAXIDX` is a per-temperature index ceiling, not a unit
  count.** The script runs temps [0.2, 0.7, 1.0] with per-temp quotas
  per_temp = [43, 43, 42]; a pass with `APEX2_MAXIDX=m` samples
  indices `0..m−1` at **each** temp, so **k per unit = 3m** for
  m ≤ 42. Pass A as kitted: m=14 → k=42/unit. Pass B: unset → k=128.
  This design uses m=2 → **k=6/unit** (2 samples/temp), with top-ups
  to m=3 (k=9) and m=4 (k=12) as budget-gated deepenings (§4).
- **Unit selection is `APEX2_TASKS`** (comma list of unit tids; fold
  tids are individually addressable). Within a run the script sorts
  the selected units by `est_conditioned_tokens` ascending
  (pack estimates: min 2,831, median 7,243, max 16,218 — prompt-side
  only; no unit's completion cap is reduced by its prompt, per the
  2026-11-05 retune note).
- **Run order inside a commit: temps are the outer loop** — all
  selected units at temp 0.2, then all at 0.7, then all at 1.0.
- **What consumes what.**
  - *Step 8½ statistics* (`sample_version_space.py`): the version
    space, sample-U, unanimous∧correct and width are computed from
    the **full-task unit's** cache records only. Correctness is
    judgeable on all 60 draw tasks (the draw records carry test
    outputs).
  - *Frozen certification* (steps 7 and 8½, `certify.certify_task`):
    consumes the full-task unit **and every fold unit** of a task. A
    task whose fold records are missing fails LOO by construction —
    the rows flag `fold_units_present`, so a construction-zero is
    never read as a content-zero (FRIDAY_SAMPLE_STATS caveat). A
    task's folds are therefore always fetched **whole-task**, never
    split.
  - *Seat standard:* certified solves and full-fit coverage are
    counted on **A+B (48 tasks)**. C units feed only the draw-wide
    statistics (sample-U / unanimity denominators in the report).

## 3. Decision-rule mapping (bars verbatim; supply consequences exact)

### 3.1 The registered bars

Seat standard (`HARNESS_READY.md`, "Gates"):

> - **SEAT (a):** ≥ **4/48 certified solves** on A+B → the proposer
>   earns the Stage-T candidate-source seat.
> - **SEAT (b):** full-fit coverage ≥ **41.6%** of A+B (≥20/48 tasks;
>   2× the derived lane's measured 20.8%) at conversion
>   (certified ÷ full-fit) no worse than the recorded **1/18** → seat
>   via fit supply.
> - Otherwise **no seat**: 1–3 certified = WEAK, 0 = KILL for the seat
>   question.

Prior evidence (`FRIDAY_SAMPLE_STATS.md`, "The registered bars"):

> - **EVIDENCE FOR A TRUTH-CONCENTRATING PRIOR** fires iff either:
>   - **unanimity clause:** ≥ **8** sample-unanimous (judgeable) tasks
>     with ≥ **3/4** of them correct; the exact Fisher p against the
>     grammar's 1/9 is printed with the line, or
>   - **conversion clause:** certified conversion an order of
>     magnitude above the grammar's 1/28 at comparable fit supply —
>     the derivation's registered operationalization is **≥ 4
>     certified from ≤ 20 fits**; the module also computes the
>     scale-free ratio reading (conversion ≥ 10 × 1/28) guarded to
>     ≥ 10 fits of supply.
> - **MERELY-MORE-SUPPLY** fires iff seat-(b) coverage is met
>   (≥ 20/48 full fits on A+B at conversion ≥ 1/18) **without** the
>   prior evidence above.

Grammar baselines: unanimous∧correct **1/9 = 11%**; conversion
**1/28 = 3.6%**; seat (b)'s floor **1/18 ≈ 5.6%**.

### 3.2 How the bars meet this design's supply (k=6/unit, unit subsets per §4)

The statistics module and the certification compute every bar from
**whatever cache exists** — there is no minimum-k gate in the
registered operationalization (the only coded supply guard is the
scale-free conversion reading's ≥ 10 fits, `RATIO_MIN_FITS = 10`;
the operationalized conversion clause ≥ 4-from-≤20 has none and
needs none). k is therefore not a parameter of any test; it is a
property of the measurement, and it cuts in two stated directions:

- **Power (down).** Fit-bearing tasks, certified solves, and
  unanimous tasks are all non-decreasing in supply. Every count this
  design produces at k=6 is a **lower bound** on the count the same
  cache would produce at Pass A (k=42) or Pass B (k=128) supply.
  Consequences: a bar **met** at k=6 is met as registered — the bars
  are on achieved counts, computed by the frozen code. A bar **not
  met** at k=6 is a *supply-limited* non-meeting: it must be reported
  with its fetched supply and the `not_sampled` / fold-presence
  flags, and it does **not** carry the strength of the kit's
  full-supply WEAK/KILL or of the packet's flat null. The one
  exception is a zero-fit outcome after the §5 deepening commit,
  which converts the full-task null into a supply-checked null at
  k=12 over all 48 A+B tasks (still not k=42 — labeled as such).
- **Unanimity bias (up).** A task's empirical version space at k=6
  is a subset of its k=128 space: fewer distinct fitting programs
  sampled ⟹ fewer distinct renderings ⟹ sample-unanimity is
  **easier** to achieve at small k, while each unanimous task's
  correctness is whatever the sampled programs say. The Fisher test
  itself needs no recomputation for k — its table is the achieved
  counts vs the grammar's 1-vs-8 split, computed exactly in code
  (registered anchors: 6/8 correct of 8 unanimous → **p = 0.013369**;
  8/8 → **p = 0.000370**; the clause is conjunctive — the ≥8 count
  **and** the ≥3/4 fraction must both hold; e.g. 5/8 correct would
  print p ≈ 0.043 yet the clause still does not fire). But a
  unanimity-clause FIRE at k=6 is weaker evidence than the same
  counts at k=128, for the bias reason above, and the report must
  print k beside the line. The deepening commits (C3b/C4) exist
  precisely to firm up any k=6 fire toward Pass A supply before the
  packet's branch is declared on it.
- **The conversion clause is k-robust in this design's direction.**
  Its operationalization (≥ 4 certified from ≤ 20 fits) was
  registered for small-supply regimes; this schedule's C2 produces
  exactly that regime. The scale-free reading (conversion ≥ 10/28
  ≈ 35.7%, guarded ≥ 10 fits) is likewise reachable if ≥ 10 A+B
  tasks fit and ≥ 4 of them certify.
- **MERELY-MORE-SUPPLY** is testable exactly when SEAT (b)'s counts
  are: after C1 (fits) + C2 (certified). It inherits the same
  supply labeling in both directions.

**Strongest verdict this schedule can deliver:** the full registered
verdict set — SEAT (a) or (b), EVIDENCE FOR A TRUTH-CONCENTRATING
PRIOR (either clause), MERELY-MORE-SUPPLY, or a labeled
supply-limited null — with every count a lower bound at stated
supply (k=6 base; k=9–12 where deepenings landed). It cannot deliver
the kit's full-supply KILL/flat-null at k=42/128 strength, and it
cannot deliver Branch PASS's downstream gates by itself (Pass B
completion remains the packet §1.1/§1.2 Nov 7 charge, re-priced by
tonight's measured fetch rate).

### 3.3 What the verdict feeds (packet branch rules, unchanged)

BRANCH PASS ⟺ EVIDENCE fires (either clause) → the §1 build
sequence, Pass B scheduled Nov 7 as the first charge on quota.
BRANCH FAIL ⟺ flat null or MERELY-MORE-SUPPLY → §2, BG-GATE Nov 7.
Seat met with neither evidence line → seat held at seat strength,
§2's gate fires in parallel. **Tonight's branch declaration must be
made at the supply actually fetched** — if a k=6 fire is firmed by
deepening before the declaration, the firmed counts govern.

### 3.4 Why the scope is cut this way (the arithmetic that forces it)

At the smoke calibration (94.0 s/completion central): Pass A as
kitted = 259 units × 42 = **10,878 completions ≈ 284 h**; Pass B =
259 × 128 = **33,152 completions ≈ 865 h**; even A+B full-task units
alone at Pass A's k=42 = 2,016 completions ≈ 52.6 h. None fits a
30 h week. The alternative cut — Pass A's k=42 kept, unit set cut
to fit — is strictly worse: k=42 on the 12 A full units alone prices
at ≈ 13.2 h, buys no folds (certification unreachable), caps the
seat denominators at 12 of 48, and makes every seat line
unreachable by construction. Count-based bars over the full seat
scope at reduced k keep every line reachable; that is the cut this
design makes.

## 4. The pass schedule

Common env for every commit (notebook exactly as in Version 2, plus
the per-commit vars): `VLLM_USE_FLASHINFER_SAMPLER=0` (already in
the finder cell), `APEX2_SMOKE` **unset**, `APEX2_MODEL_DIR` from the
finder cell, `APEX2_OUT` default (`/kaggle/working/bigmodel_run`),
**prior cache carried in** (§6) before the script cell runs.
Per-commit pricing: central at 94.0 s/completion + 0.15 h overhead;
pessimistic at 121.4 s/completion + 0.15 h. Every commit is
pessimistic-safe under the 9 h cap, and every temp phase is ≤ 96
completions (pessimistic ≤ 3.3 h), so a session kill can lose at
most one temp phase of one commit (§6).

**Launch rule (hard):** a commit launches only if
(spent so far) + (its central projection) ≤ 20.0 h. Commits run in
the order C1a → C1b → C2… → C3a → C3b → C4…; C3b/C4 are the first
cut by the launch rule.

### C1a — calibration + cheapest-half A+B fit census

- `APEX2_MAXIDX=2`, `APEX2_TASKS=` the 24 cheapest (by pack est) A+B
  full-task units:
  `d13f3404,a85d4709,7ec998c9,834ec97d,6773b310,9ddd00f0,66f2d22f,88a62173,cc9053aa,08573cc6,d017b73f,67b4a34d,83b6b474,75b8110e,6165ea8f,4f537728,bc93ec48,f1cefba8,2753e76c,7d419a02,712bf12e,29700607,b548a754,4e469f39`
- 144 completions. **Central 3.91 h; pessimistic 5.01 h.**
- Banks, even if nothing else ever runs: the fetch-regime tok/s and
  completion-length distribution (the re-plan inputs, §5); the fit
  census and k=6 version spaces for 24 A+B tasks; the truncation
  rate (`finish_reason=length` share — the length-regime test, §5).

### C1b — remaining A+B full-task units

- `APEX2_MAXIDX=2`, `APEX2_TASKS=`
  `79fb03f4,f45f5ca7,14b8e18c,e95e3d8e,e0fb7511,3e980e27,50f325b5,9f236235,ae3edfdc,358ba94e,4612dd53,55783887,baf41dbf,009d5c81,604001fa,963f59bc,f4081712,1d0a4b61,e619ca6e,929ab4e9,4aab4007,ca8f78db,3ed85e70,47996f11`
- 144 completions. **Central 3.91 h; pessimistic 5.01 h.**
  Cumulative after C1: **288 completions; central 7.82 h;
  pessimistic 10.02 h.**
- Banks: the complete A+B fit census at k=6 — the fit-bearing set F
  (drives C2), seat (b)'s coverage numerator (a lower bound), the
  A+B unanimity pre-read at k=6.

### C2 — folds of the fit-bearing A+B tasks (certification supply)

- Set defined by C1's downloaded cache (desk step: run
  `sample_version_space.py` on the carried cache, take A+B rows with
  `n_fitting_programs ≥ 1`). `APEX2_TASKS=` **all fold-unit tids of
  those tasks, whole-task** (from `units.json`: `units[tid][1:]`),
  chunked into commits of **≤ 24 fold units**, cheapest-est first;
  if F > 20 fit-bearing tasks, certify the 20 cheapest first (the
  conversion clause's supply window is ≤ 20 fits; seat (a) needs 4).
- `APEX2_MAXIDX=2` (k=6 per fold unit). Per task ≈ 3.4 folds × 6 ≈
  20 completions. Pricing scenarios: F=5 → ~102 completions, 1
  commit, **central 2.81 h**; F=10 → ~204 completions, 2 commits,
  **central 5.62 h** (pessimistic 7.16 h); F=20 → ~408 completions,
  3 commits, **central 11.09 h** — the launch rule will trim this
  tail against C3/C4; a trimmed C2 still serves both clauses.
- Banks: certification inputs for the fit-bearing set → the SEAT (a)
  count, the conversion clause's test (≥ 4 certified from ≤ 20 fits
  is decided here), MERELY-MORE-SUPPLY's conversion term, and
  `fold_units_present` resolved for every task whose verdict is
  read. **This is the commit range the whole verdict turns on** —
  it is protected ahead of C3/C4 in the launch order.

### C3a — C full-task units (draw-wide statistics denominators)

- `APEX2_MAXIDX=2`, `APEX2_TASKS=`
  `gfx90217-0232,gfx90217-0192,gfx90217-0120,gfx90217-0222,gfx90217-0105,gfx90217-0228,gfx90217-0098,gfx90217-0064,gfx90217-0018,gfx90217-0065,gfx90217-0069,gfx90217-0225`
- 72 completions. **Central 2.03 h; pessimistic 2.58 h.**
- Banks: sample-U and unanimity denominators over the full 60-task
  draw (the report's statistics are draw-wide; the seat stays A+B).

### C3b — (budget-gated) deepen A+B full-task units to k=9

- `APEX2_MAXIDX=3`, `APEX2_TASKS=` all 48 A+B full tids (C1a ∪ C1b
  lists). Resume tops up only indices 2 per temp: **+144
  completions. Central 3.91 h; pessimistic 5.01 h.**
- Banks: k=9 version spaces on the seat scope — firms any k=6
  unanimity fire toward Pass A supply before the branch declaration;
  raises every fit count (still lower bounds).

### C4 — (budget-gated) fold deepening, then C folds

- First: `APEX2_MAXIDX=3` top-up (+3/fold unit) on the fold sets of
  fit-bearing A+B tasks, whole-task chunks ≤ 24 units, certified
  tasks first. Then: `APEX2_MAXIDX=2` on C fold units (36 units,
  216 completions, two ≤24-unit chunks at central 3.91 h each).
- Banks: certification at k=9 fold supply; draw-wide conversion at
  supply; C tasks' fold presence for the report's rows.

### Schedule totals

| Path | Completions | Central hours | Pessimistic hours |
|---|---|---|---|
| C1a + C1b (fit census) | 288 | 7.82 | 10.02 |
| + C2 at F=10 | +204 | +5.62 → **13.44** | +7.16 → 17.18 |
| + C3a | +72 | +2.03 → **15.47** | +2.58 → 19.76 |
| + one gated commit (C3b or a C4 chunk) | +144 | +3.91 → **19.38** | (launch rule: only if the *measured* rates keep the cap) |

Unit coverage at the F=10 path through C3a: all 48 A+B full units,
folds of the fit-bearing A+B tasks (~34 units), all 12 C full units
— **~94 of 259 units**, covering 100% of the seat scope's
verdict inputs. The remaining ~165 units (non-fit-bearing tasks'
folds at k=6, all deepening to k=42/128) are Pass B's Nov 7 charge,
re-priced by tonight's measured fetch rate — not tonight's.

## 5. Stop rules and re-plan triggers (exact)

Read after **every** commit from its log + downloaded cache: the
script's per-group tok/s lines, and per-record `usage.
completion_tokens` / `finish_reason` in the cache.

1. **Rate re-plan (after C1a, then after every commit).** Compute
   the fetch-regime rate R₁ (total completion tokens ÷ generation
   time, from log timestamps) and mean length L̄₁ from C1a's cache.
   - If **R₁ ≥ 270 tok/s (2× the smoke floor)**: re-size all later
     commits at R₁ × L̄₁ before launching them; spend the freed
     budget first on raising C1b/C3b to `APEX2_MAXIDX=4` (k=12),
     then on pulling C4 forward.
   - If **R₁ ≥ 540 tok/s (4×)**: re-plan toward Pass A fidelity —
     A+B full units and fit-bearing folds to `APEX2_MAXIDX=14`
     (k=42) inside the same 20 h cap and launch rule, statistics
     then read at Pass A supply as the packet §1.1 registers.
   - If **R₁ < 135**: the smoke floor was optimistic; drop C3b/C4
     entirely, protect C2, and re-price C1b before launching it.
2. **Length-regime stop.** If ≥ 50% of a commit's completions end
   `finish_reason=length`, those records extract to empty content
   by construction (no final channel) — more sampling at this serve
   config buys empty records. Stop fetching after that commit;
   report the truncation regime (cap 16,384 at context 32,768,
   reasoning high) as a measured property of the configuration.
   Any remedy is a serve-config decision, never silent extra spend.
3. **Zero-fit branch.** If C1a + C1b yield **zero** fit-bearing A+B
   tasks, C2 has nothing to certify (conversion undefined; certified
   = 0 is vacuous, not a content null). Spend on exactly **one**
   deepening commit — `APEX2_MAXIDX=4` top-up over all 48 A+B full
   units (+288 completions, central 7.52 h + 0.15 h) — to separate
   supply from content, then stop. A second deepening is outside
   this design.
4. **Session safety.** If a running commit's logged pace projects
   its current temp phase past 8 h, the phase's records are lost if
   the session is killed (see §6) — accept the loss of that one
   phase only; re-chunk the remainder smaller (≤ 16 units) before
   relaunching. Completed temps are already banked in the version's
   output.
5. **Quota guard.** No commit launches if spent + its central
   projection > 20.0 h, or if the Kaggle meter shows < 8 h
   remaining for a commit projected above that. The ≥ 7 h weekly
   margin is not spendable by this design.

## 6. Caching across commits (from the script source — what the schedule must do)

- Cache location: `APEX2_OUT` (default `/kaggle/working/
  bigmodel_run`) → `cache/openai_gpt-oss-120b/<tid>__t<temp>__
  <idx>.json` per completion, plus `calls_openai_gpt-oss-120b.
  jsonl`. At each temp the script rebuilds the have-set by globbing
  that directory and samples **only missing indices** — resume and
  MAXIDX top-up are exact, never re-asked.
- **Across Kaggle versions, `/kaggle/working` does not persist**,
  and the script reads cache from nowhere else. Persistence across
  commits is therefore an operator step, required before every
  commit after the first: (i) download the previous version's
  `bigmodel_run/` output; (ii) attach it to the notebook (prior
  version output or a dataset built from it); (iii) in a pre-cell,
  copy it into `/kaggle/working/bigmodel_run` before the script
  cell runs. Skip this and the commit silently re-samples from an
  empty cache — no error, pure re-spend.
- **Within a commit**, records for a temp are written only after
  that temp's entire generation loop finishes (results are
  accumulated in memory, then written per task). A kill mid-temp
  loses that temp's samples; completed temps are on disk in the
  version output. This is why §4 caps every temp phase at ≤ 96
  completions and every commit pessimistic-safe under the cap.
- The final verdict (steps 7/8½) runs desk-local on the **last
  downloaded `bigmodel_run/`**, which — given the carry-in chain —
  is the union of all commits. Download after the final commit
  before declaring any branch.

---

**Deliverable statement.** At the measured smoke calibration this
design executes in **5–8 commits, ≤ 20 GPU-hours (central path
≈ 15.5 h at F=10 through C3a, +3.9 h for one gated deepening)**,
banking **~560–850 completions over ~94+ units** — the complete
seat-scope verdict inputs (48/48 A+B full-task units at k≥6, folds
of every fit-bearing A+B task, 12/12 C full-task units) — versus
10,878 completions / ~284 h for Pass A as kitted. The strongest
verdict it can deliver is the **full registered verdict set at
stated supply** (§3.2): any seat or evidence line can fire as
registered; non-meetings are lower-bound, supply-labeled results,
never full-supply nulls.
