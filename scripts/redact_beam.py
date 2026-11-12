#!/usr/bin/env python3
"""Write the committable subset of a BEAM run, with its official pass.

    python scripts/redact_beam.py <beam harness>/runs/<run-id> results/beam/<run-id> \
        --harness <beam harness checkout>

Keeps ids, scores, the system's answers, timings and manifests; drops question,
rubric and context text, and the rubric judge's per-item replies, which quote the
rubric. The rubric is BEAM's gold answer. Every written file is then checked for any
quoted question or rubric item, and operator identity is scrubbed as in
`redact_longmemeval.py` (ENGRAPHY_OPERATOR_NAMES, ENGRAPHY_OPERATOR_EMAIL).
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from benchkit import redact  # noqa: E402
from redact_longmemeval import scrub  # noqa: E402


def index_from_harness(harness: pathlib.Path, dataset: pathlib.Path) -> dict[str, dict]:
    sys.path.insert(0, str(harness))
    from bench.core.run import LOADERS
    corpus = LOADERS["beam"]().load(dataset)
    index = {}
    for q in corpus.questions:
        index[q.question_id] = {"question": q.text}
        for i, item in enumerate(getattr(q, "rubric", ()) or ()):
            index[f"{q.question_id}#rubric{i}"] = {"question": str(item)}
    return index


def main() -> int:
    ap = argparse.ArgumentParser(prog="redact_beam.py")
    ap.add_argument("run_dir", type=pathlib.Path)
    ap.add_argument("dest", type=pathlib.Path)
    ap.add_argument("--harness", type=pathlib.Path, required=True)
    ap.add_argument("--dataset", type=pathlib.Path)
    args = ap.parse_args()
    dataset = args.dataset or args.harness / "datasets" / "beam" / "100K.parquet"

    print(redact.redact_run(args.run_dir, args.dest))
    if (args.run_dir / "official").exists():
        print("official", redact.redact_offline_pass(args.run_dir / "official",
                                                     args.dest / "official"))
    print(f"operator identity occurrences replaced: {scrub(args.dest)}")
    hits = redact.check_clean(args.dest, index_from_harness(args.harness, dataset))
    if hits:
        print(f"dataset text quoted in {sorted(hits)}; do not commit {args.dest}")
        return 1
    print("clean: no question or rubric item is quoted in any written file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
