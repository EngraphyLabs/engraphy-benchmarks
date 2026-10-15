#!/usr/bin/env python3
"""Write the committable subset of a LongMemEval run, with its official passes.

    python scripts/redact_longmemeval.py <engine>/runs/<run-id> results/longmemeval/<run-id> \
        --dataset <engine>/datasets/longmemeval/longmemeval_oracle.json

Keeps ids, verdicts, the system's answers, timings and manifests; drops the
question, gold and context fields exactly as `benchkit/redact.py` does for LoCoMo.
LongMemEval is MIT and could be committed, but the same rule keeps every result
directory in this repository the same shape.

**Operator identity.** On the Claude Code CLI route the model sees the signed-in
account's identity, and on LongMemEval, whose transcripts call their speaker
"user", the extractor sometimes named that user after the operator. Every
occurrence of the operator's name or account email in the written copy is
replaced with `[operator]`, and the count is printed and recorded in the run's
REDACTIONS.md. The operator identity is read from the environment
(`ENGRAPHY_OPERATOR_NAMES`, comma-separated, and `ENGRAPHY_OPERATOR_EMAIL`), never
written into this script.

Then every written file is checked for quoted dataset questions.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from benchkit import redact

PASSES = ("official", "official-reader")


def scrub(dest: pathlib.Path) -> int:
    names = [n.strip() for n in os.environ.get("ENGRAPHY_OPERATOR_NAMES", "").split(",") if n.strip()]
    email = os.environ.get("ENGRAPHY_OPERATOR_EMAIL", "").strip()
    terms = ([re.escape(email)] if email else []) + \
        [rf"\b{re.escape(n)}\b" for n in sorted(names, key=len, reverse=True)]
    if not terms:
        raise SystemExit("set ENGRAPHY_OPERATOR_NAMES and ENGRAPHY_OPERATOR_EMAIL to scrub")
    pattern = re.compile("|".join(terms))
    total = 0
    for f in sorted(p for p in dest.rglob("*") if p.is_file()):
        text = f.read_text(encoding="utf-8")
        new, n = pattern.subn("[operator]", text)
        if n:
            f.write_text(new, encoding="utf-8", newline="\n")
            total += n
    return total


def main() -> int:
    ap = argparse.ArgumentParser(prog="redact_longmemeval.py")
    ap.add_argument("run_dir", type=pathlib.Path)
    ap.add_argument("dest", type=pathlib.Path)
    ap.add_argument("--dataset", type=pathlib.Path, required=True)
    args = ap.parse_args()

    print(redact.redact_run(args.run_dir, args.dest))
    for p in PASSES:
        if (args.run_dir / p).exists():
            print(p, redact.redact_offline_pass(args.run_dir / p, args.dest / p))
    print(f"operator identity occurrences replaced: {scrub(args.dest)}")

    data = json.loads(args.dataset.read_text(encoding="utf-8"))
    index = {q["question_id"]: {"question": q["question"]} for q in data}
    hits = redact.check_clean(args.dest, index)
    if hits:
        print(f"dataset questions quoted in {sorted(hits)}; do not commit {args.dest}")
        return 1
    print("clean: no dataset question is quoted in any written file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
