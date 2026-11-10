# Provenance: `lme-s-pt1-b`

LongMemEval-S, a small sample that proves the harness, not a headline: Mem0's sampler at per_type=1, seed 42 (6 questions, 287 sessions). The shipped engine and arm, operator settings withheld from every model call (ENGRAPHY_BENCH_CLI_ISOLATE_SETTINGS=1), extraction prompt budget 20,000 characters. The official LongMemEval figure is in official/. See analysis/2026-11-10-longmemeval-s-and-beam-small-batches.md.

## Result

Arm `llm_wide-conversational/search_only/always_distinct/k25`, 95% Wilson intervals in brackets.

| | accuracy |
|---|---|
| **excluding adversarial** | **50.0% [19 to 81] (3/6)** |
| overall, all five categories | 50.0% [19 to 81] (3/6) |
| knowledge-update | 100.0% [21 to 100] (1/1) |
| multi-session | 0.0% [0 to 79] (0/1) |
| single-session-assistant | 0.0% [0 to 79] (0/1) |
| single-session-preference | 0.0% [0 to 79] (0/1) |
| single-session-user | 100.0% [21 to 100] (1/1) |
| temporal-reasoning | 100.0% [21 to 100] (1/1) |

Per-pass judge instability, two single judge passes compared on a sample: not recorded. The best-of-3 majority verdict changes less often than a single pass.
Write-yield at ingest: 98.7% (970 of 983 extracted memories stored).

## What ran

| | |
|---|---|
| run date | 2026-11-10T14:29:11.085855+00:00 |
| engine commit | `391af849bc290acbd34d69f854ea264dd2b269f6` |
| engine branch | `bench/lme-oracle-fixes-20261027` |
| engine tree dirty | False |
| dataset | `longmemeval/longmemeval_s_cleaned.json` `sha256:d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442`, 500 questions in the file |
| conversations | `6b168ec8`, `0a995998`, `1c0ddc50`, `gpt4_2655b836`, `18bc8abd`, `e3fc4d6e` |
| extractor | `claude-opus-4-8` via claude-cli |
| reader | `claude-opus-4-8` via claude-cli |
| judge | `claude-sonnet-5` via claude-cli, provider `claude` |
| reader stance | `grounded` |
| embedding model | `nomic-ai/nomic-embed-text-v1.5` at `e9b6763023c676ca8431644204f50c2b100d9aab` |
| band thresholds | {"t_high": 0.95, "t_low": 0.8, "resonance.floor": 0.75} |
| prompt hashes | `extract.md` sha256:b7fdf557f7f60a9c, `extract-wide.md` sha256:2f3fa4c9e6c1a457, `judge.md` sha256:947bebcd5375e93e, `adjudicate.md` sha256:740151c30787a630 |
| models that served | judge: `claude-sonnet-5`; reader: `claude-opus-4-8` |

## Where it ran

Host and runtime were not captured for this run.

## Files

- `manifest.json`: the harness manifest, with extracted-memory text removed from its ingest samples.
- `results.jsonl`: one row per question, keyed by `question_id`, with the verdict, the best-of-3 tally and the system's answer. No question text, gold answers or conversation text; restore them from your own copy with `scripts/rejoin.py`.
- `ingest.jsonl`: per-conversation write statistics, including every class of write refusal and the engine's message for it.
