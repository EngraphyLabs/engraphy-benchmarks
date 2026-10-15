#!/usr/bin/env python3
"""Consolidate LongMemEval runs into the figures the report quotes.

    python scripts/consolidate_longmemeval.py results/longmemeval/lme-oracle-a \
                                              results/longmemeval/lme-oracle-b

Each argument is a finished run directory: the strict run, with the two official
passes beside it in `official/` (Engraphy's reader, the official judge) and
`official-reader/` (the official answer template, the official judge). Only
complete passes are counted; a pass whose manifest carries `quota_stop` or
ungraded rows is named and left out, never partially averaged.

Prints, per convention, each run's accuracy overall and per question type, the
mean across runs with the range, and the pooled count with its 95% Wilson
interval.

- **Official** conventions count every question, abstention included, each in
  its own type, as LongMemEval's `evaluate_qa.py` does.
- **Strict** leaves out `single-session-preference`, whose gold is a rubric the
  strict judge is not built for, and reports abstention apart as well as inside
  its type.
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

TYPES = ("single-session-user", "single-session-assistant", "single-session-preference",
         "multi-session", "knowledge-update", "temporal-reasoning")
PASSES = (
    ("official judge, Engraphy's reader", "official"),
    ("official judge, official answer template", "official-reader"),
)


def rows(path: pathlib.Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def complete(manifest: pathlib.Path) -> tuple[bool, str]:
    if not manifest.exists():
        return False, "missing"
    m = json.loads(manifest.read_text(encoding="utf-8"))
    if m.get("quota_stop"):
        return False, f"stopped: {m.get('stop_reason')}"
    if m.get("rows_answered_but_ungraded", 0):
        return False, f"{m['rows_answered_but_ungraded']} ungraded"
    if not m.get("aggregate"):
        return False, "no aggregate"
    return True, "complete"


def wilson(k: int, n: int) -> str:
    p, z = k / n, 1.96
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"{100 * p:.1f}% [{100 * (c - h):.0f} to {100 * (c + h):.0f}] ({k}/{n})"


def buckets(result_rows: list[dict], *, strict: bool) -> dict[str, tuple[int, int]]:
    scored = [r for r in result_rows
              if not (strict and r["category"] == "single-session-preference")]
    label = "overall, preference excluded" if strict else "overall"
    out = {label: (sum(bool(r["correct"]) for r in scored), len(scored))}
    for t in TYPES:
        rs = [r for r in scored if r["category"] == t]
        if rs:
            out[t] = (sum(bool(r["correct"]) for r in rs), len(rs))
    ab = [r for r in scored if r.get("abstain_expected")]
    if ab:
        out["abstention (inside its types)"] = (sum(bool(r["correct"]) for r in ab), len(ab))
    return out


def report(title: str, per_run: dict[str, dict[str, tuple[int, int]]]) -> None:
    print(f"\n## {title}  ({len(per_run)} run(s): {', '.join(per_run)})")
    keys: list[str] = []
    for b in per_run.values():
        keys += [k for k in b if k not in keys]
    for key in keys:
        cells = [(run, b[key]) for run, b in per_run.items() if key in b]
        accs = [100 * k / n for _, (k, n) in cells]
        mean = sum(accs) / len(accs)
        spread = (f"range {min(accs):.1f} to {max(accs):.1f}" if len(accs) == 2 else
                  "one run, no spread" if len(accs) == 1 else f"{len(accs)} runs")
        pooled = wilson(sum(k for _, (k, _) in cells), sum(n for _, (_, n) in cells))
        each = "  ".join(f"{run.split('-')[-1]}: {100 * k / n:.1f}%" for run, (k, n) in cells)
        print(f"  {key:32s} mean {mean:5.1f}%  ({spread})  pooled {pooled}   [{each}]")


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    strict: dict[str, dict] = {}
    official: dict[str, dict[str, dict]] = {name: {} for _, name in PASSES}
    for arg in sys.argv[1:]:
        d = pathlib.Path(arg)
        ok, why = complete(d / "manifest.json")
        print(f"{d.name}: strict {why}")
        if ok:
            strict[d.name] = buckets(rows(d / "results.jsonl"), strict=True)
        for _, name in PASSES:
            ok, why = complete(d / name / "manifest.json")
            print(f"{d.name}: {name} {why}")
            if ok:
                official[name][d.name] = buckets(rows(d / name / "results.jsonl"), strict=False)
    for title, name in PASSES:
        if official[name]:
            report(title, official[name])
    if strict:
        report("strict (Engraphy's reader and strict judge, best of 3)", strict)
    print("\nComparator, the only published one for this setting: the LongMemEval paper's "
          "oracle rows, gpt-4o reading the raw evidence sessions (arXiv 2410.10813). Not a "
          "memory system, a different judge, and the full 500 questions rather than this subset.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
