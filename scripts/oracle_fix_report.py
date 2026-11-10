"""Score the LongMemEval oracle-fix experiment against its baseline, as pre-registered.

    python scripts/oracle_fix_report.py --runs <engine>/runs \
        --arm facts=official-facts [--arm asst=... ] [--seen <engine>/runs/lme-oracle-subset-n15.txt]

Every arm and the baseline are graded by the official LongMemEval judge prompts. For
each arm the report gives, by question type, the two-run mean on all 180 questions
and on the out-of-sample set (the N = 30 questions not in the N = 15 set the levers
were written from), against the baseline on the same questions.

Significance, fixed in analysis/2026-10-27-benchmark-slate-plan.md section 1:
per question, the arm's and the baseline's correct counts over the two runs are
compared; an exact two-sided sign test runs over the questions where they differ
(McNemar's exact test on the per-question outcome). Abstention is tracked apart:
lever (b) fails if it answers more than 2 of the 20 unanswerable question-runs.

An arm directory is `<run>/<name>/results.jsonl` for both runs. A single-run arm
(the withheld-settings replay) is compared on its run only. An arm from its own
ingest names its run directory: `asst=lme-oracle-fix-asst-a:official@lme-oracle-n30-a`
compares that run's `official/` with the baseline run named after `@`. A two-run arm
from its own ingests names both, paired in order with the baseline runs:
`asst=lme-oracle-fix-asst-a+lme-oracle-fix-asst-b:official`.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
from collections import defaultdict

RUNS = ("lme-oracle-n30-a", "lme-oracle-n30-b")
TYPES = ("single-session-user", "single-session-assistant", "single-session-preference",
         "multi-session", "temporal-reasoning", "knowledge-update")


def load(path: pathlib.Path) -> dict[str, dict]:
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            rows[r["question_id"]] = r
    return rows


def sign_test(wins: int, losses: int) -> float:
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def score(runs_dir: pathlib.Path, base: str, arm: str, runs: tuple[str, ...], seen: set[str],
          arm_run: str | None = None):
    base_rows = {r: load(runs_dir / r / base / "results.jsonl") for r in runs}
    arm_runs = arm_run.split("+") if arm_run else list(runs)
    if len(arm_runs) == 1:
        arm_runs = arm_runs * len(runs)
    arm_rows = {r: load(runs_dir / ar / arm / "results.jsonl") for r, ar in zip(runs, arm_runs)}
    qids = sorted(set.intersection(*(set(arm_rows[r]) for r in runs)))
    cat = {q: base_rows[runs[0]][q]["category"] for q in qids}
    abs_q = {q for q in qids if base_rows[runs[0]][q]["abstain_expected"]}
    out = {"runs": list(runs), "questions": len(qids), "subsets": {}}
    for subset, keep in (("all", qids), ("out_of_sample", [q for q in qids if q not in seen])):
        by = defaultdict(lambda: {"n": 0, "base": 0, "arm": 0, "wins": 0, "losses": 0})
        for q in keep:
            b = sum(bool(base_rows[r][q]["correct"]) for r in runs)
            a = sum(bool(arm_rows[r][q]["correct"]) for r in runs)
            for key in (cat[q], "overall"):
                s = by[key]
                s["n"] += 1
                s["base"] += b
                s["arm"] += a
                s["wins"] += a > b
                s["losses"] += a < b
        table = {}
        for key in (*TYPES, "overall"):
            s = by.get(key)
            if not s:
                continue
            denom = s["n"] * len(runs)
            table[key] = {"questions": s["n"], "baseline_pct": round(100 * s["base"] / denom, 1),
                          "arm_pct": round(100 * s["arm"] / denom, 1),
                          "lift_points": round(100 * (s["arm"] - s["base"]) / denom, 1),
                          "questions_better": s["wins"], "questions_worse": s["losses"],
                          "p_exact": round(sign_test(s["wins"], s["losses"]), 4)}
        out["subsets"][subset] = table
    answered = sum(not arm_rows[r][q]["correct"] for r in runs for q in abs_q)
    base_answered = sum(not base_rows[r][q]["correct"] for r in runs for q in abs_q)
    out["abstention"] = {"question_runs": len(abs_q) * len(runs),
                         "arm_wrongly_answered": answered,
                         "baseline_wrongly_answered": base_answered}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True, help="the engine checkout's runs/ directory")
    ap.add_argument("--baseline", default="official")
    ap.add_argument("--arm", action="append", required=True, metavar="LABEL=DIR[@RUN]",
                    help="output directory name under each run; @RUN limits it to one run")
    ap.add_argument("--seen", help="comma-separated ids the levers were written from")
    args = ap.parse_args()
    runs_dir = pathlib.Path(args.runs)
    seen = set()
    if args.seen:
        seen = {s.strip() for s in pathlib.Path(args.seen).read_text().split(",") if s.strip()}
    report = {"baseline": args.baseline, "seen_questions": len(seen), "arms": {}}
    for spec in args.arm:
        label, rest = spec.split("=", 1)
        name, _, only = rest.partition("@")
        arm_run, _, name = name.rpartition(":")
        runs = (only,) if only else RUNS
        report["arms"][label] = {"dir": name, "run": arm_run or None,
                                 **score(runs_dir, args.baseline, name, runs, seen, arm_run or None)}
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
