# SIEVE Rename Sweep — Execution Plan (PLAN ONLY — execute nothing from this file until §4.0's Friday gate is met)

Written 2026-11-05. The sweep itself is sequenced to **after Friday Nov 6's big-model
session**, so no path the measurement lane depends on moves the day before it fires.
This plan makes that later execution mechanical: explicit file lists, exact strings,
an order, a verification suite, and a rollback at every step.

**The rename, in one line:**
- Local tree: `~/workspace/arc_apex2/` → `~/workspace/sieve/`
- GitLab repo: `thinker-labs/apex-2-solver` → `thinker-labs/sieve` (redirect preserved)
- Local mirror: `~/workspace/gitlab_mirror/apex2-solver/` → `~/workspace/gitlab_mirror/sieve/`
- Forward name is **SIEVE** — established by the 2026-11-04 rename order in `~/MEMORY.md`
  (program renamed APEX-2 → SIEVE; paths frozen until this sweep). No better-established
  target name exists in MEMORY.md, AGENTS.md, or the goal files; `~/workspace/sieve/`
  does not currently exist. Proposed, not assumed: if a `sieve/` collision appears
  before execution, stop and re-plan — do not improvise a variant name.

**Explicitly NOT renamed by this sweep** (each covered below): the Kaggle staging
dataset names (§2), the Python package `apex2/` inside the mirror (§3.4), any dated
or historical record (§1.4), the sealed approval exam's contents (§1.3), and the
2026 campaign's record anywhere it lives.

---

## 0. Grep scope and hit counts

Scope of the census behind this plan (2026-11-05, read-only):

- Tree walk of `~/workspace/**` plus `~/MEMORY.md`, `~/AGENTS.md`, `~/memory/*.md`;
  text files only (`grep -I` semantics), excluding `__pycache__`, `.git`,
  `*.zip`, `*.gz`, `*.pdf`, `*.npz`, `*.pyc`, and files > 5 MB.
- Follow-up targeted `grep -R -n` passes over the live-code subtrees
  (`friday_bigmodel_kit/`, `approval_exam/`, `census/`, `derived_solver/`,
  `gauntlet/`, `nextgen_probe/`), the goal trees, and the GitLab mirror.

Hit counts per class (lines / files):

| Pattern | `~/workspace` total | Inside `arc_apex2/` tree | Outside the tree |
|---|---|---|---|
| `arc_apex2` | 3,909 lines / 1,165 files | 3,907 / 1,163 | `~/MEMORY.md` 2 lines (L30, L37 — counted separately, below); `goals/arc-prize-2026-arc-agi-2-assault/` ≈6 lines in 2 files (historical, §1.4); `custom-skills/credential_capture_and_storage/skill.yaml` 1 live path + narrative |
| `apex-2-solver` | 16 lines / 8 files | — (repo-name string; lives in docs/config) | `~/MEMORY.md` L36 (1); `~/AGENTS.md` L25 (1); mirror `.git/config` remote URL (1) |
| `apex2-` (all `apex2-*` forms) | 72 lines / 22 files | kit + staging docs + drivers | Kaggle dataset names are a subset of this class — see §2 before touching any of it |
| `APEX-2` / `APEX2` | 12,065 lines / 1,040 files | bulk is data (`sft_*.jsonl`, `mining_results*.jsonl`, `frames_results*.jsonl`, library/data JSON) and dated filenames | 2026-campaign records — **historical class, §1.4; the count is the reason a blanket sed is forbidden** |
| `SIEVE` / `sieve` | 77 lines / 25 files in tree | already-SIEVE-named forward artifacts (`SIEVE_ITERATION2_PROBE_RESULTS_2026-11-04.md`, `SIEVE_INTERSECTION_PROBE_RESULTS_2026-11-04.md`, `run_…_seed20271132_sieve_iter2.json`, `run_…_seed20365108_sieve_intersection.json`, …) | confirms SIEVE is the established forward name |

Reading of the counts: the 3,907 in-tree `arc_apex2` lines are overwhelmingly
**generated artifacts** — run logs, gauntlet run JSONs, probe-run caches, the Friday
pack's build logs, `*.jsonl` data — i.e. historical records of where things *were*,
not live resolution of where things *are*. The live-resolution subset is small and
enumerated exhaustively in §1.2 (≈45 files). **The sweep is an explicit-file-list
edit, never a tree-wide find-and-replace.** A blanket `sed` over the tree would
corrupt probe records, invalidate the exam seal's provenance trail, and rewrite
the filed writeup's evidence citations — all standing-rule violations.

---

## 1. Local directory: `~/workspace/arc_apex2/` → `~/workspace/sieve/`

The move itself is a single `mv`. Everything else in this section is the reference
updates that make the moved tree work, divided into MUST (live path resolution —
the tree breaks or silently reads the wrong place without it), SHOULD (operator
documentation an executor will follow), and MUST-NOT (historical record).

### 1.1 Standing pointers outside the tree — MUST change

| File | Exact current string | Change to |
|---|---|---|
| `~/MEMORY.md` L30 | ``Program in `~/workspace/arc_apex2/` `` | ``Program in `~/workspace/sieve/` `` — and append a dated rename note to the SIEVE block recording: old path, new path, sweep date, mirror/repo new paths, and the §2 stay-list (Kaggle names unchanged). The note is how a future reader resolves pre-rename citations. |
| `~/MEMORY.md` L37 | `stored at ~/workspace/arc_apex2/.nvidia_api_key` | `stored at ~/workspace/sieve/.nvidia_api_key` |
| `~/MEMORY.md` L36 | `NS proof repo and apex-2-solver remain private` | `NS proof repo and sieve (formerly apex-2-solver) remain private` — keep the former name in this line once, as the cross-reference. |
| `~/AGENTS.md` L25 | ``project `apex-2-solver`; local mirror at ~/workspace/gitlab_mirror/apex2-solver`` | ``project `sieve` (renamed from `apex-2-solver` 2026-11-0x, redirect live); local mirror at ~/workspace/gitlab_mirror/sieve`` |
| `~/workspace/custom-skills/credential_capture_and_storage/skill.yaml` L11 (+ rationale L19) | `~/workspace/arc_apex2/.nvidia_key` | `~/workspace/sieve/.nvidia_key` — path only; the surrounding narrative is a dated incident record and keeps its wording otherwise. |
| `~/workspace/MEMORY.md` (workspace-root copy, if present at execution) | any `arc_apex2` hit found by the §4.3 residual grep | same pointer update as `~/MEMORY.md`; check at execution, it was not separately censused. |

Zero-hit files verified 2026-11-05 (no change, do not "fix"): 
`~/workspace/HPC_CONTROL_PLANE_2026-11-04.md`, `~/workspace/FAILURE_LEDGER.md`,
`~/workspace/goals/next-generation-arc-solver/GOAL.md` (goal slug
`next-generation-arc-solver` is a platform identifier, not a path — out of scope),
`~/workspace/lp_budget/**`, the Navier–Stokes goal tree.

Daily logs `~/memory/*.md`: contain `arc_apex2` citations — **MUST-NOT** (§1.4);
the `~/MEMORY.md` rename note is the single bridge from old citations to new paths.

### 1.2 Live code inside the tree — MUST change (exact strings)

Universal substitution for this subsection only:
`/home/hatch/workspace/arc_apex2` → `/home/hatch/workspace/sieve` and
`~/workspace/arc_apex2` → `~/workspace/sieve`, applied **only to the lines listed**
(and their direct continuations). The mirror-path lines are §3.3's list; both
substitutions often occur in the same file.

**Friday harness (`friday_bigmodel_kit/harness/`) — the Friday lane itself:**
- `proposer_client.py`: L40 `WORK = Path("/home/hatch/workspace/arc_apex2")`;
  L41 `KIT = Path("/home/hatch/workspace/arc_apex2/friday_bigmodel_kit")`;
  docstring L17 `~/workspace/arc_apex2/.groq_key`, L19 `~/workspace/arc_apex2/.nvidia_api_key`
  (docstrings, but they are the operator's key-location record — MUST).
- `harness_prompts.py`: L44 `WORK = …` (L43 is MIRROR, §3.3).
- `harness_fetch.py`: L39 `WORK = …`.
- `probe_lane.py`: L50 `WORK = …` (L49 MIRROR, §3.3).
- `smoke_test.py`: L42 `WORK = …` (L43 MIRROR, §3.3).
- `build_friday_pack.py`: L17 docstring example `--out ~/workspace/arc_apex2/probe_runs/friday_pack` (SHOULD — it is the rebuild command an operator would paste).
- `lane_runner.py`: **verified clean** — relative `HERE`/`GAUNTLET` `sys.path` inserts only; no change. Same for `certify.py` except its MIRROR line (§3.3) and `verify_friday_pack.py` (takes `--pack`/`--draw` as arguments; no baked path).

**Friday kit (top level):**
- `bigmodel_solve_taxonomy.py`: L40 `WORK = Path("/home/hatch/workspace/arc_apex2")`.
- `gauntlet_lane.py`: L36 `WORK = …` (L35 MIRROR, §3.3); L20 docstring `cd ~/workspace/arc_apex2/gauntlet` (SHOULD).
- `prepare_prompts.py`: L39 `WORK = …`.
- `sample_version_space.py`: L53 `WORK = …`; L6 docstring path to `SHARED_WRONG_BINDING_DERIVATION_2026-11-04.md` (SHOULD).
- `bigmodel_fetch.py`: **no local path** — Kaggle-side only (`/kaggle/working`, `/kaggle/input/apex2-*`, env `APEX2_OUT`). MUST-NOT (§2).
- `stage_model.py`, `serve_config.json`: Kaggle-side only. MUST-NOT (§2).

**Approval exam (`approval_exam/`) — handle under §1.3's seal rules:**
- `build_exam.py`: L22 `BASE = os.path.expanduser('~/workspace/arc_apex2')`.
- `verify_seal.py`: L22 `BASE = os.path.expanduser('~/workspace/arc_apex2')`.
- `APPROVAL_EXAM_PROTOCOL_2026-11-04.md`: L28, L129 cite `~/workspace/arc_apex2/` and
  `~/workspace/arc_apex2/PROBE_LEDGER.jsonl` (SHOULD — update with a one-line
  dated addendum at the file's end, do not edit the protocol body; the protocol
  is a pre-registered record).

**Census (`census/`):**
- `census.py` L46, `census_creation.py` L21, `census_param_bound.py` L55,
  `census_param_aggregate.py` L18 — each `BASE = os.path.expanduser('~/workspace/arc_apex2')`.

**Derived solver (`derived_solver/`) — every `sys.path` / data path is absolute:**
- `ds_lane.py` L34–35; `ds_lane2.py` L63–64; `ds_lane3.py` L63–65 —
  `sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")` / `"…/census"` / `"…/derived_solver"`.
- `controls_ds.py` L25–26; `controls_ds2.py` L25–26; `controls_ds3.py` L25–26 — same inserts.
- `diag_ds.py`, `diag_ds2.py`, `diag_ds3.py`: L12–13 inserts; L19–21 run-dir +
  `POOLS = "/home/hatch/workspace/arc_apex2/gauntlet/pools.json"`; L25–28 census
  `open("/home/hatch/workspace/arc_apex2/census/…")`; the L116/L151 output `open(…/derived_solver/…)` lines.
- `prechecks_ds3.py`: L24–26 inserts; L32 `POOLS = json.load(open("/home/hatch/workspace/arc_apex2/gauntlet/…"))`.
- `survivor_census.py`: L60–62 inserts; L69 `DS = "/home/hatch/workspace/arc_apex2/derived_solver/"`; L70 `ROOT = "/home/hatch/workspace/arc_apex2/"`.
- `wrong_binding_anatomy.py`: L38–40 inserts; L47 `ROOT = "/home/hatch/workspace/arc_apex2/"`.

**Gauntlet (`gauntlet/`):**
- `build_pools.py`: L32 `APEX = WS / "arc_apex2"` → `WS / "sieve"` (L31 is MIRROR, §3.3;
  L131 `MIRROR / "apex2" / "library.json"` is the package path — MUST-NOT, §3.4).
- `GAUNTLET.md` L62: `cd ~/workspace/arc_apex2/gauntlet` (SHOULD).
- `gauntlet.py`: no `arc_apex2` absolute (its only absolute is MIRROR, §3.3);
  its `apex2.solver` / `apex2.library` imports are package references — MUST-NOT (§3.4).

**Top-level drivers and key files:**
- Any `~/workspace/arc_apex2/*.py` hit returned by the §4.3 residual grep at
  execution (the 2026-11-05 census found the live top-level drivers clean apart
  from the kit/census/derived/exam files above; re-grep at execution and list
  before editing — do not assume).
- Secret files move **with** the tree and are never edited: `.groq_key`,
  `.nvidia_api_key`, `.nvidia_key`, `.sambanova_key` (all chmod 600). Post-move
  verification: all four present at `~/workspace/sieve/.*`, mode still 600,
  sizes unchanged (56 / 70 / 70 / 36 bytes at census). Never print contents.
- `__pycache__` directories throughout: delete during the sweep (stale `.pyc`
  files embed the old absolute path); they regenerate on first import.

### 1.3 Approval exam — special handling

- `approval_exam/MANIFEST.json` and `approval_exam/tasks/*.json`: **MUST-NOT edit,
  rename, or re-serialise.** The manifest's `"exam": "APEX-2 approval exam, sealed
  set #1"` and its relative `per_source_counts` keys are part of the sealed record.
  The directory moves only as part of the whole-tree `mv` (file bytes untouched).
- Only the two `BASE =` lines (§1.2) change. First post-move action, before any
  other verification: `python3 ~/workspace/sieve/approval_exam/verify_seal.py`
  must print its SEAL VALID result (16/16 at census). Anything else = stop,
  roll back (§4.4), and treat the exam as potentially compromised until the
  desk re-verifies from the §4.1 pre-move seal output recorded in the sweep log.
- The exam remains **unspent**; the sweep does not run it, read its tasks, or
  count as a use.

### 1.4 Historical record — MUST NOT be rewritten

Standing rule (2026-11-04 rename order): the historical record keeps its names.
Concretely, frozen as-is (content and filenames):

- Every dated artifact in the tree: `APEX2_ARCHITECTURE_DERIVATION_2026-11-04.md`,
  `APEX2_CHARTER_2026-11-01.md`, `APEX2_ASSEMBLY_README.md`,
  `CAMPAIGN_PLAN_2026-11-01.md`, `NEXTGEN_*_2026-11-04.md`,
  `NEXT_IDENTIFICATION_DERIVATION_2026-11-04.md`,
  `PARAMETER_SEMANTICS_DERIVATION_2026-11-04.md`,
  `CONVERSION_DERIVATION_2026-11-04.md`,
  `SHARED_WRONG_BINDING_DERIVATION_2026-11-04.md`,
  `DERIVED_SOLVER_PROBE_RESULTS_2026-11-04.md`, `SIEVE_*_2026-11-04.md`,
  `SURVIVOR_SET_CENSUS_2026-11-04.md` (+ rows JSON), `P3_BUILD.md`,
  `P3_RUNBOOK.md`, `P3_COMPLETION_2026-11-04.md`, `FRIDAY_KIT_REVERIFY_2026-11-03.md`,
  `BLUEPRINT.md`, `PRIVATE_SET_MODEL.md`, `RESEARCH_NOTES_2026-11-01.md`,
  `probe_runbook.md`. Their internal `arc_apex2` citations are provenance.
- All run outputs: `gauntlet/runs/*.json` + `*.log` (embedded `run_file` absolute
  paths), `derived_solver/*_run.log`, `*_rows.json`, `probe_runs/**` (including
  `friday_pack/PACK_READY.md`, `manifest.json`, `units.json`, build logs — by
  sweep time the pack is a spent Friday record), `friday_bigmodel_kit/harness/smoke/**`
  and `smoke_run*.log`, census `*.log` / `*.err` / `per_task*.jsonl`.
- All data: `sft_*.jsonl(.gz)`, `mining_results*.jsonl`, `frames_results*.jsonl`,
  `synth_tasks*.jsonl(.gz)`, `APEX2_FULL_CODEBASE_*.zip`, `BUNDLE_MANIFEST.txt`.
- `PROBE_LEDGER.jsonl` **content**: append-only, never edited in place. Continuity
  is preserved by (a) the file moving with the tree, (b) the first post-sweep
  ledger entry being a rename record `{tag: "rename_sweep", from:
  "~/workspace/arc_apex2", to: "~/workspace/sieve", repo_from:
  "thinker-labs/apex-2-solver", repo_to: "thinker-labs/sieve", date, pre/post
  HEADs}`, and (c) the `~/MEMORY.md` rename note (§1.1). 35 lines at census;
  record the count again pre-move (§4.1).
- Outside the tree: `~/memory/*.md` daily logs; 
  `goals/arc-prize-2026-arc-agi-2-assault/files/WRITEUP_EVIDENCE_PACK_2026-11-01.md`
  and `hidden_files/WRITEUP_FIX_PACK_2026-11-02.md` (they cite
  `arc_apex2/mining_results2.jsonl` / `RESEARCH_NOTES_2026-11-01.md` as the filed
  writeup's evidence provenance — rewriting them falsifies a filed record);
  the whole 2026 campaign (`~/workspace/arc_finals*`, the Kaggle writeup,
  `gitlab.com/masonbradleygilhool/arc-prize-2026-solution`).

---

## 2. Kaggle staging names — STAY as issued (do not rename, ever, in this sweep)

Standing record: `apex2-bigmodel`, `apex2-qwen30b-awq`, `apex2-prompts` were issued
to the user as click-by-click staging orders and exist (or will exist) as Kaggle
datasets under those exact names. Kaggle dataset names are a remote namespace
independent of the local directory; renaming them locally renames nothing on
Kaggle and breaks every `/kaggle/input/…` lookup. **The sweep touches none of
them, and no file below is edited for its Kaggle-name strings.**

Every place that fact is recorded — at sweep time, add the §2 stay-list to the
sweep's own completion note and to the `~/MEMORY.md` rename note (§1.1) so a
future agent does not "helpfully" rename them:

- `friday_bigmodel_kit/HARNESS_READY.md` L66–67, L71–72 — datasets
  `apex2-bigmodel`, `apex2-qwen30b-awq`, upload pack as `apex2-prompts`.
- `friday_bigmodel_kit/STAGING_RUNBOOK.md` L26, L40, L49 — staging output names.
- `friday_bigmodel_kit/README.md` L47, L49, L54–55 — attach list.
- `friday_bigmodel_kit/serve_config.json` L8, L20 —
  `"dataset_dir_glob": "/kaggle/input/apex2-bigmodel"` / `…/apex2-qwen30b-awq`.
- `friday_bigmodel_kit/stage_model.py` L31–32 comments, L37–38, L53–54 —
  `"dataset_name"` / `"out_dir": "/kaggle/working/apex2-*"` (Kaggle-side paths).
- `friday_bigmodel_kit/bigmodel_fetch.py` L58, L62 (mirrored serve configs),
  L150 (`/kaggle/input/apex2-prompts/**/prompts` glob), L156 (error message
  naming `apex2-prompts`), L30/L264 env var `APEX2_OUT` (Kaggle-side run-dir
  name — also stays; it is an environment contract with the Friday notebook,
  not a local path).
- `friday_bigmodel_kit/kit_manifest.json` — `"dataset_name": "apex2-bigmodel"` /
  `"apex2-qwen30b-awq"` fields (a built record; frozen anyway under §1.4).
- This plan, §2 (the preventive note itself).

If Friday's session has already run when the sweep executes, these names are
additionally embedded in its downloaded run record — a second, independent
reason they stay.

---

## 3. GitLab: `thinker-labs/apex-2-solver` → `thinker-labs/sieve`, plus the workspace→repo sync

### 3.1 Pre-rename record (do first, in the sweep log)

- `git -C ~/workspace/gitlab_mirror/apex2-solver rev-parse HEAD` (184cca6 at the
  2026-11-04 record; record the actual value at execution), `git status` clean
  or every dirty file listed, `git ls-remote origin` HEAD for comparison.
- The mirror's `.git/config` at census: remote
  `git@gitlab.com:thinker-labs/apex-2-solver.git`; `core.sshCommand` = the
  identity-file + `proxy_connect.py` ProxyCommand line. **The sshCommand is
  never touched and `GIT_SSH_COMMAND` is never exported** (standing rule);
  the rename changes only the remote URL path.

### 3.2 The rename (GitLab web UI — the executor's browser step)

1. Open `https://gitlab.com/thinker-labs/apex-2-solver/-/settings/general`.
2. **Settings → General → Visibility, project features, permissions** is *not*
   the route; use **Advanced** (same page, bottom): **Change path** —
   set `apex-2-solver` → `sieve`, save.
3. Same page, top section: **Project name** → `SIEVE` (display name only;
   optional but proposed — the path change in step 2 is the load-bearing one).
4. Do **not** transfer the project, do **not** change visibility (stays private),
   do **not** create any new project at the old path afterwards — GitLab's
   redirect from `thinker-labs/apex-2-solver` lives only while the old path
   stays unclaimed.
5. Note the group stays `thinker-labs` (ID 146447642); no group rename is in scope.

GitLab behaviour relied on (verify, don't assume — §3.3): web URLs and the git
remote for the old path redirect to the new path after a path rename.

### 3.3 Post-rename verifications (all must pass before §3.5's sync)

- Browser/fetch check: `https://gitlab.com/thinker-labs/apex-2-solver`
  redirects to `https://gitlab.com/thinker-labs/sieve`.
- Local mirror move + remote update:
  `mv ~/workspace/gitlab_mirror/apex2-solver ~/workspace/gitlab_mirror/sieve`;
  `git -C ~/workspace/gitlab_mirror/sieve remote set-url origin git@gitlab.com:thinker-labs/sieve.git`;
  confirm `.git/config` diff shows **only** the URL line changed.
- `git -C ~/workspace/gitlab_mirror/sieve ls-remote origin` — HEAD equals the
  §3.1 recorded HEAD. Then `git fetch origin` clean.
- Old-remote proof (one shot, read-only): `git ls-remote git@gitlab.com:thinker-labs/apex-2-solver.git`
  resolves via redirect to the same HEAD (if GitLab refuses git-over-redirect,
  record that and rely on the web redirect + new-remote checks; do not treat
  it alone as a failure).
- Harness MIRROR references — MUST change, exact string
  `Path("/home/hatch/workspace/gitlab_mirror/apex2-solver")` →
  `Path("/home/hatch/workspace/gitlab_mirror/sieve")` in:
  `friday_bigmodel_kit/harness/certify.py` L41, `harness_prompts.py` L43,
  `probe_lane.py` L49, `smoke_test.py` L43; `gauntlet/gauntlet.py` L45;
  `gauntlet/build_pools.py` L31 (`WS / "gitlab_mirror" / "apex2-solver"` →
  `"sieve"`); `friday_bigmodel_kit/gauntlet_lane.py` L35.
- CI re-check: the §3.5 sync push triggers the pipeline; read the **raw log**
  to green (standing rule — never claim CI from a badge). Expected content:
  the repo's existing test suite (48/48 at the 184cca6 record).

### 3.4 Out of scope inside the repo: the `apex2` Python package

The mirror contains a package directory `apex2/` (`dsl.py`, `solver.py`,
`library.py`, `library.json`, `proposers.py`, `constraints.py`, `symmetry.py`),
imported as `apex2.dsl`, `apex2.solver`, … by `certify.py` L44,
`gauntlet.py` L63–64, `gauntlet_lane.py` L50/L77, and referenced as the path
segment `apex2/library.json` by `build_pools.py` L131 and `GAUNTLET.md`.
**This sweep does not rename the package.** It is a code identifier, not the
program's public name; renaming it is a refactor with its own import/test gates,
and conflating it with the path sweep is how a mechanical rename becomes a
debugging session. If the desk ever wants it renamed, that is a separate,
separately-gated change. The sweep log must state this exclusion explicitly.

### 3.5 Workspace → repo artifact sync (the sweep's second debt)

At census the repo holds the v1/v2-era tree; the SIEVE-era record lives only in
`~/workspace/arc_apex2/`. Sync target: `~/workspace/gitlab_mirror/sieve/`, in a
dedicated commit (`SIEVE rename sweep: sync workspace record`) after §3.3
passes. Proposed structure (new top-level dirs, dated filenames unchanged):

| Repo destination | Source (post-move paths) | Include | Exclude |
|---|---|---|---|
| `derivations/` | `sieve/APEX2_ARCHITECTURE_DERIVATION_2026-11-04.md`, `PARAMETER_SEMANTICS_DERIVATION_2026-11-04.md`, `NEXT_IDENTIFICATION_DERIVATION_2026-11-04.md`, `CONVERSION_DERIVATION_2026-11-04.md`, `SHARED_WRONG_BINDING_DERIVATION_2026-11-04.md` | all five, byte-identical | — |
| `probes/` | `NEXTGEN_SOLVER_DESIGN_2026-11-04.md`, `NEXTGEN_PROBE_RESULTS_2026-11-04.md`, `NEXTGEN_V2_DESIGN_2026-11-04.md`, `NEXTGEN_V2_PROBE_RESULTS_2026-11-04.md`, `DERIVED_SOLVER_PROBE_RESULTS_2026-11-04.md`, `SIEVE_ITERATION2_PROBE_RESULTS_2026-11-04.md`, `SIEVE_INTERSECTION_PROBE_RESULTS_2026-11-04.md`, `P3_COMPLETION_2026-11-04.md`, `SURVIVOR_SET_CENSUS_2026-11-04.md`, `SURVIVOR_SET_CENSUS_ROWS_2026-11-04.json` | all, byte-identical | — |
| `census/` | `sieve/census/*.py`, `summary.json`, `param_bound.json`, `README.md` | code + headline results | `*.log`, `*.err`, `per_task*.jsonl`, `param_per_task*.jsonl` (bulk data stays workspace-only) |
| `derived_solver/` | `sieve/derived_solver/*.py`, `DESIGN_NOTE{,2,3}.md`, `diag_ds*_rows.json`, `survivor_census_rows.json`, `wrong_binding_rows.json` | code + notes + rows | `*_run.log`, `__pycache__` |
| `nextgen_probe/` | `sieve/nextgen_probe/*.py`, `diag*_rows.json` | code + rows | `__pycache__` |
| `gauntlet/` (merge with repo's existing `gauntlet/`) | `sieve/gauntlet/gauntlet.py`, `build_pools.py`, `GAUNTLET.md`, `REPORT.md`, `pools_manifest.json` | code + docs + manifest | `runs/` (workspace-only; REPORT.md is the curated summary) |
| `friday_bigmodel_kit/` | `sieve/friday_bigmodel_kit/**` incl. `harness/` | all `.py`, `.md`, `serve_config.json`, `kit_manifest.json`, `harness/friday_draw.json`, and the Friday session record (§4.0) once downloaded | `__pycache__`, `harness/smoke/**` caches, any downloaded completion cache (bulk; its record file syncs, the cache stays workspace-only) |
| `approval_exam/` | `APPROVAL_EXAM_PROTOCOL_2026-11-04.md`, `MANIFEST.json`, `verify_seal.py`, `build_exam.py` | protocol + manifest + code | **`tasks/` — never committed.** The sealed set stays out of git history; the manifest's hashes are the repo-side integrity anchor. |
| `PROBE_LEDGER.jsonl` (repo root, exists) | workspace ledger (35 lines at census) | **diff first**: repo copy is older. Merge append-only — repo lines preserved in order, workspace-only lines appended; line count and a spot-check of first/last lines recorded in the sweep log. Never overwrite blindly. | — |
| `README.md` (repo root) | edit in place | title → SIEVE; one dated paragraph: renamed from APEX-2 2026-11-04 (program) / path renamed at this sweep; requirement (90%+ / 216-of-240, approval = in-house sealed exam) stated at current strength; links to `derivations/` and `probes/` | do not rewrite the historical sections; append/amend only |

Never synced, anywhere: the four key files (verify the repo `.gitignore`
covers `.*_key` / `*.key` before the sync commit — AGENTS.md records
`.nvidia_key` and `*.key` as gitignored; confirm `.groq_key` and
`.sambanova_key` patterns too), `__pycache__`, `*.log`, `sft_*`, `mining_*`,
`frames_*`, `synth_tasks*`, the codebase zips, `probe_runs/` caches,
`trm_lane/` (poisoned-lane artifacts stay workspace-only; its BUILD_NOTES
verdict is already carried in the derivations).

Sync verification: `git status` shows only intended adds; the committed
derivations/probes files hash-match their workspace sources (`sha256sum`
spot-check ≥ the five derivations + census rows); push via the repo's own
`core.sshCommand`; `ls-remote` shows the new HEAD; CI raw log green (§3.3).

---

## 4. Execution order, quiesce, verifications, rollback

### 4.0 Gate — Friday artifacts that must exist first (all of them)

The sweep does not start until Friday Nov 6's session is closed and its
outputs are on this disk:

1. The session's completion cache downloaded from Kaggle `/kaggle/working`
   (the `APEX2_OUT` run dir, default `bigmodel_run`) into the workspace tree.
2. The local run record over that cache: `bigmodel_solve_taxonomy.py` output /
   verdict file, and `lane_runner.py`'s record + rows for the draw
   (seed 22979062), wherever the session's HARNESS_READY flow writes them.
3. Any `gauntlet_lane.py` fresh-draw run JSON the session produced.
4. A `PROBE_LEDGER.jsonl` entry for the Friday measurement appended by the
   session's own close-out (the ledger must be final before it moves).
5. `probe_runs/friday_pack/` intact (259 units, PACK_READY.md present) —
   it is both a Friday input record and a §4.3 verification fixture.

Missing any of 1–4 → the sweep waits. No exceptions, no partial sweep.

### 4.1 Pre-move snapshot

- Record in a sweep log (`~/workspace/sieve_rename_sweep_LOG.md`, created at
  execution, outside the moved tree): date/time, §3.1 mirror HEAD,
  PROBE_LEDGER line count, exam seal output (run `verify_seal.py` pre-move),
  Friday pack verifier output (run pre-move, §4.3 command against the old
  paths), key-file sizes/modes.
- Backup: `tar` of `~/workspace/arc_apex2/` (excluding `__pycache__`) and of
  the mirror (including `.git/config`) to
  `~/workspace/backups/sieve_rename_<date>/`. This tarball is the rollback
  substrate for every local step. It is never committed anywhere.

### 4.2 Quiesce check — no live process may reference the tree

- Scan every process: `grep -a -l -E 'arc_apex2|apex2-solver|friday_bigmodel|gauntlet' /proc/[0-9]*/cmdline`
  (read `/proc/<pid>/cmdline` content — never trust `pgrep -f` alone; standing
  lesson). Expected live references at a healthy quiesce: **none**. The NS
  campaign supervisors (campaign_boot) do not reference this tree — verify
  rather than assume, per the scan.
- Confirm no detached build is mid-flight: `probe_runs/friday_pack/build_status.json`
  shows the pack complete; no `build_friday_pack.py` / harness / pack process
  in the scan; Friday's Kaggle session closed (§4.0).
- Any hit → identify, let it finish or stop it deliberately, re-scan.
  The `mv` does not proceed on a dirty scan.

### 4.3 The sequence

1. **GitLab path rename** (§3.2) — first, while all local paths still work
   via the old remote if anything aborts.
2. **Local tree move**: `mv ~/workspace/arc_apex2 ~/workspace/sieve`;
   delete all `__pycache__` under the new tree.
3. **Mirror move + remote** (§3.3 commands).
4. **Reference edits**: §1.1 (standing pointers), §1.2 (live code), §3.3
   (MIRROR lines) — applied from this plan's explicit lists, file by file,
   with a diff of each file saved to the sweep log. No scripted tree-wide
   substitution.
5. **Ledger continuity entry** (§1.4) appended to `~/workspace/sieve/PROBE_LEDGER.jsonl`.
6. **Verifications** (all must pass; failure → §4.4):
   - Exam seal: `python3 ~/workspace/sieve/approval_exam/verify_seal.py` → SEAL VALID (cf. §1.3).
   - Harness smoke: `python3 ~/workspace/sieve/friday_bigmodel_kit/harness/smoke_test.py`
     → controls PASS (oracle certifies + solves its synthetic tasks, null 0 —
     the same control standard as the pre-Friday smoke record).
   - Pack verifier against moved paths:
     `python3 ~/workspace/sieve/friday_bigmodel_kit/harness/verify_friday_pack.py --pack ~/workspace/sieve/probe_runs/friday_pack --draw ~/workspace/sieve/friday_bigmodel_kit/harness/friday_draw.json` → PASS (259 units, seals, zero unexplained leakage).
   - Gauntlet dry import + compile pass: `python3 -m compileall` over every
     edited `.py`; `python3 ~/workspace/sieve/gauntlet/gauntlet.py --help`
     exits 0; import check for `ds_lane3`, `census.census_param_bound`,
     `survivor_census` from the new tree (import only — no probe runs).
   - Residual grep: `grep -R -I -n 'arc_apex2' ~/workspace/sieve --include='*.py'`
     → **zero** live-code hits; a full-tree residual count is taken and every
     remaining hit must fall in a §1.4 frozen class (logs, runs, dated docs,
     data) — the sweep log lists the count and the classes, not the lines.
     Same check for `gitlab_mirror/apex2-solver` in `*.py` → zero.
   - Keys: four key files present in `~/workspace/sieve/`, chmod 600, sizes
     match §4.1.
   - Git: `ls-remote` (§3.3) matches; `git -C ~/workspace/gitlab_mirror/sieve status` understood line by line.
7. **Sync commit + push** (§3.5), then **CI raw-log read** to green.
8. **Close-out**: sweep log completed; `~/MEMORY.md` rename note (§1.1)
   finalised with the new HEAD and CI result; a one-line completion entry in
   the daily memory log. Only now is the sweep "done".

### 4.4 Rollback, per step

- **Before step 1**: nothing has moved; abort = delete the sweep log draft.
- **After GitLab rename, before local moves**: rename the path back in the
  same Advanced → Change path panel (`sieve` → `apex-2-solver`); the redirect
  flips with it. Verify `ls-remote` on the original URL.
- **After local `mv`, before/without edits**: `mv ~/workspace/sieve ~/workspace/arc_apex2`
  restores the tree exactly; mirror likewise; `git remote set-url` back.
- **After reference edits**: the workspace tree is not a git repo — rollback
  is (a) reverse the per-file diffs saved in the sweep log, or (b) restore
  the edited files from the §4.1 tarball (extract over the moved tree, then
  `mv` back if also reverting the move). The tarball is authoritative;
  never reconstruct an edited file from memory.
- **After the sync push**: revert with a normal `git revert` commit (never
  force-push — standing rule; concurrent lanes rebase). If CI fails on the
  sync commit, the revert lands the repo at its pre-sweep HEAD while the
  local rename can stay or roll back independently — decide from the CI log,
  and record the decision in the sweep log.
- **Exam-seal failure at any point**: stop everything; restore
  `approval_exam/` from the tarball byte-for-byte, re-run the seal, and do
  not resume the sweep until the desk has re-verified the exam from the
  §4.1 pre-move output. A seal discrepancy is a P0, not a rename detail.

---

## 5. Section list (for the parent report)

0. Grep scope and hit counts · 1. Local directory (1.1 standing pointers,
1.2 live code file-by-file, 1.3 exam seal handling, 1.4 historical MUST-NOT) ·
2. Kaggle staging names stay · 3. GitLab rename + verifications + package
exclusion + workspace→repo sync structure · 4. Execution order (4.0 Friday
gate, 4.1 snapshot, 4.2 quiesce, 4.3 sequence + verifications, 4.4 rollback) ·
5. Section list.

---

## 6. Amendment (2026-11-05, second grep pass — supersedes the file lists in §1.2/§3.3 where they differ)

A follow-up pass over top-level drivers, `nextgen_probe/`, and every
`gitlab_mirror/apex2-solver` reference in `*.py`/`*.md`/`*.json` found live
references the first pass's enumeration missed. They are added here; the
sweep executor works from §1.2 + §3.3 **as amended by this section**.

### 6.1 Additional §1.2 MUST-change lines (`arc_apex2` → `sieve`)

Top-level drivers (each also carries a MIRROR line — §6.2):
- `conditioned_retrieval.py` L61 `WORK = Path("/home/hatch/workspace/arc_apex2")`.
- `conditioned_retrieval_enlarged.py` L51 `WORK = …` — note: this module is
  imported by the Friday harness (`verify_friday_pack.py` imports
  `conditioned_retrieval` and the pack prepare path uses the enlarged index),
  so these two files are Friday-lane-critical, not legacy.
- `groq_p2_driver.py` L33 `WORK = …`; L23 docstring key path
  `~/workspace/arc_apex2/.groq_key` (MUST, operator record).
- `groq_p3_conditioned_driver.py` L49 `WORK = …`; L39 docstring `.groq_key` path.
- `reprepare_p3_enlarged.py` L22 `WORK = …`.
- `selftest_p3.py` L22 `WORK = …`.
- `sambanova_probe/sambanova_p4_driver.py` L62 `WORK = …`; L49 docstring
  `~/workspace/arc_apex2/.sambanova_key` path.

`nextgen_probe/` (all `sys.path` inserts are absolute):
- `controls.py` L12; `controls2.py` L19; `ng2_lane.py` L23 —
  `sys.path.insert(0, "/home/hatch/workspace/arc_apex2/nextgen_probe")`.
- `diag.py` L10 insert; L13 `RUN = "…/gauntlet/runs/run_1793816913_seed20261104_nextgen_v1.json"`;
  L14 `POOLS = "…/gauntlet/pools.json"`; L108 output `open("…/nextgen_probe/…")`.
- `diag2.py` L10 insert; L13–15 `RUN = "…/gauntlet/runs/…"`; L15 `POOLS = …`;
  L58 output `open("…/nextgen_probe/…")`.
- `ng_lane.py`: no hit in either pass — verified clean, no change.

Kit files carrying **both** substitutions (the §1.2 entry listed only WORK):
- `friday_bigmodel_kit/bigmodel_solve_taxonomy.py` L39 MIRROR + L40 WORK.
- `friday_bigmodel_kit/prepare_prompts.py` L38 MIRROR + L39 WORK.
- `friday_bigmodel_kit/sample_version_space.py` L52 MIRROR + L53 WORK.

### 6.2 Additional §3.3 MUST-change MIRROR lines

Exact string `Path("/home/hatch/workspace/gitlab_mirror/apex2-solver")` (or the
`sys.path.insert` form) → `…/gitlab_mirror/sieve`, in:
- `probe.py` L70 (`sys.path.insert` form);
- `conditioned_retrieval.py` L60; `conditioned_retrieval_enlarged.py` L50;
- `groq_p2_driver.py` L32; `groq_p3_conditioned_driver.py` L48;
- `selftest_p3.py` L23;
- `reprepare_p3_enlarged.py` L30 (`sys.path.insert` form);
- `sambanova_probe/sambanova_p4_driver.py` L61;
- `friday_bigmodel_kit/bigmodel_solve_taxonomy.py` L39;
  `friday_bigmodel_kit/prepare_prompts.py` L38;
  `friday_bigmodel_kit/sample_version_space.py` L52.
(Plus the seven files already listed in §3.3: harness `certify.py`,
`harness_prompts.py`, `probe_lane.py`, `smoke_test.py`, `gauntlet.py`,
`build_pools.py`, kit `gauntlet_lane.py`. Total MIRROR sites in live code: 18.)

### 6.3 Classified MUST-NOT after the second pass

- `private_set_aggregate.py` L127–129: the `arc_apex2/…` strings are provenance
  labels embedded in a computed record (sources of a finished computation) —
  historical, frozen.
- `gauntlet/pools_manifest.json` L6 `"mirror": "/home/hatch/workspace/gitlab_mirror/apex2-solver"`:
  generated build manifest — do not hand-edit; it is regenerated by
  `build_pools.py` (which itself gets the §1.2/§3.3 edits) if pools are ever
  rebuilt, and stands as provenance until then.
- All `probe_runs/**` copies of the above code (e.g.
  `probe_runs/library_growth_compose_2026-11-03/repo_enlarged/probe.py`,
  `growth_driver.py`, `bench_compose_firstfit.py`, `growth_ledger.json`,
  `probe_runs/retrieval_proposer_2026-11-03/retrieval_proposer_run.py`):
  run snapshots — frozen under §1.4 even though identical strings in the
  top-level originals are MUST-change. The distinction is location:
  `probe_runs/` = record of a spent run; tree root/subtrees = live code.
- Daily-log hit counts, for the record (§1.1's MUST-NOT): `~/memory/2026-11-01.md`
  30 lines, `2026-11-02.md` 12, `2026-11-03.md` 16, `2026-11-04.md` 6 —
  64 lines total, all frozen; the `~/MEMORY.md` rename note is the only bridge.

### 6.4 Effect on §4.3's residual grep

The zero-live-code-hits verification now explicitly covers the §6.1/§6.2
files (they are inside the `~/workspace/sieve/**/*.py` scan already specified;
this amendment removes any doubt about whether top-level drivers and
`nextgen_probe/` were in the plan's edit list — they are).

### 6.5 Scope note (third pass, ripgrep over the full workspace)

A full-workspace `rg` pass returns additional `arc_apex2` hits outside the
tree — 864 lines / 393 files — located almost entirely in
`~/workspace/agents/**` (agent tool-output and exec logs),
`~/workspace/proactivity/**` (prepared-edition snapshots), and
`~/workspace/self_improvement/staging/**` (memory-reconciliation copies of
MEMORY.md), plus `~/memory/bank/**` derived-memory copies (combined-pattern
count for `~/memory` = 133 lines). **All of these are runtime/derived
infrastructure, not standing records: MUST-NOT, out of scope, never edited
by the sweep** — they age out or regenerate on their own. The sweep's
authoritative outside-the-tree list remains §1.1 (MEMORY.md, AGENTS.md,
the credential skill) plus §1.4's frozen goal/memory records. An executor
who re-greps the whole workspace at sweep time should expect these
infrastructure hits and leave every one of them alone.

### 6.6 ERRATUM to §0 (2026-11-05, completed census walk — the §0 table is superseded)

§0's aggregate table mixed occurrence counts from an interim process output
and overstated the totals. The completed, reproducible census — line-counting
walk of `~/workspace`, text files only, excluding `__pycache__`, `.git`,
`*.zip`, `*.gz`, `*.pdf`, `*.npz`, `*.pyc`, files > 5 MB — gives:

| Pattern | `~/workspace` total | Of which inside `arc_apex2/` |
|---|---|---|
| `arc_apex2` | **874 lines / 398 files** | 165 lines |
| `apex-2-solver` | **722 lines / 292 files** | 13 lines |
| `apex2-` | **577 lines / 355 files** | 87 lines |
| `APEX-2` / `APEX2` | **3,681 lines / 812 files** | 368 lines |

`arc_apex2` outside the tree, by location: `self_improvement/` 478,
`proactivity/` 83, `agents/` 79 (all §6.5 infrastructure — MUST-NOT),
`fresh_clone_check/` 32, `gitlab_mirror/` 18, `cron.d/` 7,
`HPC_SWEEP_2026-11-03_EVENING.md` 5, `goals/` 5, `custom-skills/` 2.
`~/MEMORY.md` occurrences (exact): `arc_apex2` 2, `apex-2-solver` 1;
`~/AGENTS.md`: `apex-2-solver` 1. `SIEVE|sieve` raw counts are not meaningful
(vendored trees — `torch_cpu`, `.venv-*`, the mirror's data — dominate them)
and are withdrawn as a metric; the forward-name evidence stands on the
2026-11-04 rename order and the already-SIEVE-named artifacts, not on counts.
**What does not change:** the §1.2/§3.3/§6.1/§6.2 edit lists were verified
line-by-line by targeted grep and are unaffected by the aggregate error;
§0's qualitative conclusion (no blanket sed; explicit lists only) is
strengthened, since the majority of all hits workspace-wide are in
infrastructure copies and dated records, not live code.

New locations found by the completed walk — classifications:
- `~/workspace/cron.d/_archive/` (7 `arc_apex2` lines): archived job files,
  including `apex2-kaggle-probe-2026-11-06` (steps citing
  `arc_apex2/PROBE_LEDGER.jsonl` and `finetune_qlora.py`) and
  `apex2-p4-sambanova-gate`. MUST-NOT (archive = historical, inert).
  Additions to §4.2's quiesce: confirm no **active** `cron.d` directory
  (daily/hourly/runonce/…) holds a job referencing the tree; and if the
  archived Nov 6 probe job is ever revived, its paths are updated to
  `~/workspace/sieve/…` **before** it runs — after the sweep its printed
  paths will be stale.
- `~/workspace/fresh_clone_check/` (32 lines): fresh-clone verification
  copies (`apex_clone/`, `remote/apex/`) of the repo, including copied
  `build_pools.py`/`GAUNTLET.md`. MUST-NOT edit in place; at sweep time
  delete the apex clones and re-clone from `thinker-labs/sieve` if the
  fresh-clone check is re-run.
- `~/workspace/gitlab_mirror/` in-tree (18 lines): one live pointer —
  `apex2-solver/CORE_BUILD.md` L130, "persisted under
  `~/workspace/arc_apex2/probe_runs/`" — MUST change to `~/workspace/sieve/…`
  as part of the §3.5 sync commit. The remainder are the mirror's own logs
  and data — frozen.
- `~/workspace/gitlab_elevation_fixes/apex2-solver/` (README, LICENSE,
  FINGERPRINT_PURGES, gitignore additions; `APPLY_ORDER.md` cites
  `apex-2-solver` at banked HEADs): the completed 2026-11-04 elevation
  work product. Frozen; do not rename the staging subdir — record the
  repo's new path in the sweep log instead.
- `~/workspace/HPC_SWEEP_2026-11-03_EVENING.md` (5 lines, incl. key-path
  instructions for `.sambanova_key` / `.baseten_key` / `.cloudflare_key`
  under `arc_apex2/`), `~/workspace/GITLAB_AUDIT_2026-11-03.md`
  (15 `apex-2-solver` lines), `~/workspace/GITLAB_OSS_PROGRAM_PREP_2026-11-03.md`
  (1 line): dated records — MUST-NOT. Their path pointers are superseded
  by the §1.1 MEMORY rename note.
- `goals/arc-prize-2026-arc-agi-2-assault/files/WRITEUP_ADVERSARIAL_PASS_2026-11-01.md`
  L118: add to §1.4's frozen list (goals combined total: 12 lines / 3 files).
- Line-number drift: `~/MEMORY.md` is edited by other work continuously
  (e.g. the 2026-11-05 SA8/SIEVE updates). §1.1's line numbers are census
  values; the executor re-greps `~/MEMORY.md` at execution and edits by
  string, not by line number. The strings themselves are unchanged.
