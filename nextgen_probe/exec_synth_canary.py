#!/usr/bin/env python3
"""EXEC-SYNTH supply canary driver (EXEC_SYNTH_PREREGISTRATION_
2026-11-07.md). gpt-oss-120b via Groq writes Python transform
programs for 24 fresh pool-B tasks; every program is executed in
the local sandbox against the task's train pairs; a task is
supplied iff >= 1 program fits all train pairs exactly.

Discipline (registered): k=8 initial samples (4 @ temp 0.25, 4 @
0.75), <= 3 repair rounds per sample, best-sample-first, early stop
per task at the first verified fit; selection by execution only;
hard request cap 768; rolling 7,400 tok/min pacing (measured tier
cap 8,000); a 429 stops the run immediately (STOP file, no
retries); raw responses cached to disk so a crashed run resumes
without re-spending requests. The API key is read from
~/workspace/arc_apex2/.groq_key at runtime and never printed or
written anywhere.
"""
import json
import os
import re
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
DRAW = HERE / "exec_synth_draw.json"
ROWS = HERE / "exec_synth_rows.json"
CACHE = HERE / "exec_synth_cache"
CALLS = HERE / "exec_synth_calls.jsonl"
STOP429 = HERE / "STOPPED_429_exec_synth.json"
HARNESS = HERE / "exec_synth_harness.py"
KEY_FILE = WORK / ".groq_key"
ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"
MAX_TOKENS = 4096
TOP_P = 0.95
REASONING_EFFORT = "low"
INITIAL_TEMPS = [0.25] * 4 + [0.75] * 4
REPAIR_TEMP = 0.25
MAX_REPAIR_ROUNDS = 3
REQ_CAP = 768
TPM_BUDGET = 7400
EXEC_WALL_S = 6.0
TASK_EXEC_BUDGET_S = 25.0

SYSTEM = (
    "You are writing a Python program that solves an ARC "
    "(Abstraction and Reasoning Corpus) task. You are given "
    "training input/output grid pairs. Write a single Python "
    "function `transform(grid)` that takes a grid (a list of lists "
    "of ints, colors 0-9) and returns the transformed grid (a list "
    "of lists of ints). The same function is run on every pair; it "
    "must reproduce every training output exactly. Infer the "
    "general rule from the pairs. Reply with exactly one ```python "
    "code block containing the function (helper functions "
    "allowed). Use only the Python standard library. Do not read "
    "input, do not print, do not use randomness.")


def render(grid):
    return "\n".join("".join(str(c) for c in row) for row in grid)


def pairs_block(task):
    parts = []
    for i, p in enumerate(task["train"]):
        parts.append(f"Pair {i + 1}\nInput:\n{render(p['input'])}\n"
                     f"Output:\n{render(p['output'])}")
    return "\n\n".join(parts)


def initial_prompt(task):
    return ("Training pairs (each grid is shown as rows of digits, "
            "one row per line):\n\n" + pairs_block(task) +
            "\n\nWrite transform(grid) that maps each input to its "
            "output.")


def feedback_text(res):
    lines = []
    for i, r in enumerate(res["results"]):
        st = r["status"]
        if st == "ok":
            continue
        if res.get("load_error"):
            lines.append(f"Pair {i + 1}: the program failed to "
                         f"load/run: {res['load_error']}")
            break
        if st == "exception":
            lines.append(f"Pair {i + 1}: raised {r['error']}")
        elif st == "shape":
            lines.append(
                f"Pair {i + 1}: output shape "
                f"{r['got_shape'][0]}x{r['got_shape'][1]}, expected "
                f"{r['exp_shape'][0]}x{r['exp_shape'][1]}")
        elif st == "mismatch":
            ds = ", ".join(f"({a},{b},expected {c},got {d})"
                           for a, b, c, d in r["diffs"])
            lines.append(f"Pair {i + 1}: {r['diff_cells']} cells "
                         f"differ; first differences "
                         f"(row,col,expected,got): {ds}")
    return "\n".join(lines) if lines else "no failing pairs"


def repair_prompt(task, code, res):
    return ("Training pairs (each grid is shown as rows of digits, "
            "one row per line):\n\n" + pairs_block(task) +
            "\n\nYour previous program:\n```python\n" + code +
            "\n```\nWhen executed on the training pairs it failed:"
            "\n" + feedback_text(res) +
            "\n\nWrite a corrected program in one ```python block: "
            "a single function transform(grid) (helpers allowed) "
            "that reproduces every training output exactly.")


def extract_code(text):
    if not text:
        return None
    blocks = re.findall(r"```(?:python)?\s*\n(.*?)```", text, re.S)
    for b in blocks:
        if "def transform" in b:
            return b.strip()
    if blocks:
        return blocks[0].strip()
    if "def transform" in text:
        return text[text.index("def transform"):].strip()
    return None


def pair_cost(r, load_error):
    if load_error:
        return 10_000_000
    st = r["status"]
    if st == "ok":
        return 0
    if st == "mismatch":
        return r["diff_cells"]
    if st == "shape":
        return 500_000
    return 10_000_000  # exception / load_error


class StopRun(Exception):
    pass


class Driver:
    def __init__(self):
        self.key = KEY_FILE.read_text().strip()
        self.tokwin = deque()
        self.n_requests = 0
        if CALLS.exists():
            self.n_requests = sum(1 for _ in open(CALLS))
        self.consec_fail = 0
        CACHE.mkdir(exist_ok=True)

    # --- pacing -------------------------------------------------
    def pace(self, est_tokens):
        while True:
            now = time.time()
            while self.tokwin and now - self.tokwin[0][0] > 60:
                self.tokwin.popleft()
            used = sum(t for _, t in self.tokwin)
            if used + est_tokens <= TPM_BUDGET:
                return
            time.sleep(max(1.0, 60 - (now - self.tokwin[0][0]) + 0.5))

    # --- one API call (cached) ----------------------------------
    def call(self, tid, tag, messages, temp):
        cpath = CACHE / f"{tid}__{tag}.json"
        if cpath.exists():
            return json.loads(cpath.read_text())
        if self.n_requests >= REQ_CAP:
            raise StopRun(f"request cap {REQ_CAP} reached")
        prompt_chars = sum(len(m["content"]) for m in messages)
        est = int(prompt_chars * 0.95) + 800
        self.pace(est)
        payload = {"model": MODEL, "messages": messages,
                   "temperature": temp, "top_p": TOP_P,
                   "max_tokens": MAX_TOKENS,
                   "reasoning_effort": REASONING_EFFORT}
        headers = {"Authorization": f"Bearer {self.key}",
                   "Content-Type": "application/json"}
        try:
            resp = requests.post(ENDPOINT, json=payload,
                                 headers=headers, timeout=180)
        except requests.RequestException as e:
            self._count(tid, tag, temp, "transport_error")
            self.consec_fail += 1
            if self.consec_fail >= 5:
                raise StopRun(f"service failure: {e}")
            return {"error": f"transport: {e}", "content": None}
        self._count(tid, tag, temp, f"http_{resp.status_code}")
        if resp.status_code == 429:
            STOP429.write_text(json.dumps(
                {"tid": tid, "tag": tag,
                 "at_requests": self.n_requests,
                 "body": resp.text[:500]}, indent=1))
            raise StopRun("HTTP 429 rate limit — run stopped per "
                          "registered service discipline")
        if resp.status_code != 200:
            self.consec_fail += 1
            if self.consec_fail >= 5:
                raise StopRun(f"service failure: HTTP "
                              f"{resp.status_code}: "
                              f"{resp.text[:200]}")
            rec = {"error": f"http {resp.status_code}: "
                            f"{resp.text[:200]}", "content": None}
            cpath.write_text(json.dumps(rec))
            return rec
        self.consec_fail = 0
        data = resp.json()
        usage = data.get("usage") or {}
        total = usage.get("total_tokens")
        msg = data["choices"][0]["message"]
        content = msg.get("content")
        finish = data["choices"][0].get("finish_reason")
        if total is None:
            total = est + int(len(content or "") * 0.95)
        self.tokwin.append((time.time(), total))
        rec = {"error": None, "content": content, "finish": finish,
               "usage_total_tokens": total}
        cpath.write_text(json.dumps(rec))
        return rec

    def _count(self, tid, tag, temp, outcome):
        self.n_requests += 1
        with open(CALLS, "a") as f:
            f.write(json.dumps({"tid": tid, "tag": tag,
                                "temp": temp, "outcome": outcome,
                                "n": self.n_requests,
                                "ts": time.time()}) + "\n")

    # --- sandbox execution ---------------------------------------
    def execute(self, tid, tag, code, task):
        cpath = CACHE / f"{tid}__{tag}.py"
        cpath.write_text(code)
        pairs = {"pairs": task["train"]}
        t0 = time.time()
        try:
            cp = subprocess.run(
                [sys.executable, str(HARNESS), str(cpath)],
                input=json.dumps(pairs), capture_output=True,
                text=True, timeout=EXEC_WALL_S,
                cwd=str(CACHE), env={"PATH": "/usr/bin:/bin"})
        except subprocess.TimeoutExpired:
            return {"load_error": None, "timeout": True,
                    "results": [{"status": "exception",
                                 "error": "wall timeout (6 s)"}
                                for _ in task["train"]]},
            EXEC_WALL_S
        wall = time.time() - t0
        line = (cp.stdout or "").strip().splitlines()
        if not line:
            return {"load_error": f"harness died: "
                                  f"{(cp.stderr or '')[:200]}",
                    "results": [{"status": "load_error"}
                                for _ in task["train"]]}, wall
        return json.loads(line[-1]), wall


def main():
    draw = json.loads(DRAW.read_text())
    drv = Driver()
    rows = []
    if ROWS.exists():
        rows = json.loads(ROWS.read_text())
    done = {r["tid"] for r in rows if r.get("complete")}
    print(f"start: {drv.n_requests} prior requests counted, "
          f"{len(done)} tasks already complete", flush=True)
    try:
        for entry in draw["tasks"]:
            tid = entry["tid"]
            if tid in done:
                continue
            task = entry["task"]
            row = {"tid": tid, "pool": "B", "supplied": False,
                   "samples_requested": 0, "repair_rounds_used": 0,
                   "requests_used": 0, "exec_budget_exceeded": False,
                   "attempts": [], "complete": False}
            exec_used = 0.0
            samples = []  # (code, res, cost, tag)
            req0 = drv.n_requests
            # --- initial k=8 ------------------------------------
            for idx, temp in enumerate(INITIAL_TEMPS):
                msgs = [{"role": "system", "content": SYSTEM},
                        {"role": "user",
                         "content": initial_prompt(task)}]
                rec = drv.call(tid, f"s{idx}", msgs, temp)
                row["samples_requested"] += 1
                if rec.get("error") or rec.get("content") is None:
                    row["attempts"].append(
                        {"phase": "initial", "idx": idx, "temp": temp,
                         "outcome": f"api_error: {rec.get('error')}"})
                    samples.append((None, None, None, f"s{idx}"))
                    continue
                code = extract_code(rec["content"])
                if code is None:
                    row["attempts"].append(
                        {"phase": "initial", "idx": idx, "temp": temp,
                         "outcome": "no_code_extracted",
                         "finish": rec.get("finish")})
                    samples.append((None, None, None, f"s{idx}"))
                    continue
                if exec_used > TASK_EXEC_BUDGET_S:
                    row["exec_budget_exceeded"] = True
                    row["attempts"].append(
                        {"phase": "initial", "idx": idx, "temp": temp,
                         "outcome": "not_executed_budget"})
                    samples.append((code, None, None, f"s{idx}"))
                    continue
                res, wall = drv.execute(tid, f"s{idx}", code, task)
                exec_used += wall
                cost = sum(pair_cost(r, res.get("load_error"))
                           for r in res["results"])
                fit = cost == 0 and not res.get("timeout")
                row["attempts"].append(
                    {"phase": "initial", "idx": idx, "temp": temp,
                     "outcome": "fit" if fit else "no_fit",
                     "cost": cost,
                     "load_error": res.get("load_error")})
                samples.append((code, res, cost, f"s{idx}"))
                if fit:
                    row["supplied"] = True
                    break
            # --- repairs, best-sample-first ----------------------
            if not row["supplied"]:
                order = sorted(
                    (s for s in samples if s[0] is not None
                     and s[2] is not None),
                    key=lambda s: s[2])
                for code, res, cost, tag in order:
                    if row["supplied"]:
                        break
                    cur_code, cur_res = code, res
                    for rnd in range(1, MAX_REPAIR_ROUNDS + 1):
                        msgs = [{"role": "system", "content": SYSTEM},
                                {"role": "user",
                                 "content": repair_prompt(
                                     task, cur_code, cur_res)}]
                        rtag = f"{tag}r{rnd}"
                        rec = drv.call(tid, rtag, msgs, REPAIR_TEMP)
                        row["repair_rounds_used"] += 1
                        if rec.get("error") or \
                                rec.get("content") is None:
                            row["attempts"].append(
                                {"phase": "repair", "of": tag,
                                 "round": rnd,
                                 "outcome": f"api_error: "
                                            f"{rec.get('error')}"})
                            break
                        ncode = extract_code(rec["content"])
                        if ncode is None:
                            row["attempts"].append(
                                {"phase": "repair", "of": tag,
                                 "round": rnd,
                                 "outcome": "no_code_extracted",
                                 "finish": rec.get("finish")})
                            break
                        if exec_used > TASK_EXEC_BUDGET_S:
                            row["exec_budget_exceeded"] = True
                            row["attempts"].append(
                                {"phase": "repair", "of": tag,
                                 "round": rnd,
                                 "outcome": "not_executed_budget"})
                            break
                        nres, wall = drv.execute(tid, rtag, ncode,
                                                 task)
                        exec_used += wall
                        ncost = sum(pair_cost(r, nres.get("load_error"))
                                    for r in nres["results"])
                        fit = ncost == 0 and not nres.get("timeout")
                        row["attempts"].append(
                            {"phase": "repair", "of": tag,
                             "round": rnd,
                             "outcome": "fit" if fit else "no_fit",
                             "cost": ncost,
                             "load_error": nres.get("load_error")})
                        cur_code, cur_res = ncode, nres
                        if fit:
                            row["supplied"] = True
                            break
            row["requests_used"] = drv.n_requests - req0
            row["complete"] = True
            rows.append(row)
            tmp = ROWS.with_suffix(".tmp")
            tmp.write_text(json.dumps(rows, indent=1))
            os.replace(tmp, ROWS)
            sup = sum(1 for r in rows if r["supplied"])
            print(f"[{len(rows)}/24] {tid}: supplied="
                  f"{row['supplied']} samples="
                  f"{row['samples_requested']} repairs="
                  f"{row['repair_rounds_used']} req_total="
                  f"{drv.n_requests} running_supplied={sup}", 
                  flush=True)
    except StopRun as e:
        print(f"RUN STOPPED: {e}", flush=True)
        tmp = ROWS.with_suffix(".tmp")
        tmp.write_text(json.dumps(rows, indent=1))
        os.replace(tmp, ROWS)
        (HERE / "exec_synth_stopped.json").write_text(json.dumps(
            {"reason": str(e), "requests_used": drv.n_requests,
             "tasks_complete": len(rows),
             "supplied": sum(1 for r in rows if r["supplied"])},
            indent=1))
        return 2
    print(f"DONE: supplied {sum(1 for r in rows if r['supplied'])}"
          f"/24, requests {drv.n_requests}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
