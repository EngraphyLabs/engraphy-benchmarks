# Provenance: `locomo-settle-c`

Run C of the settling measurement, 2026-10-16: a third independent run of the combined engine over the seven held-out conversations, ingest included, harness a1b7e73 (aa7daa2 plus a supervisor-only change; engraphy/ identical). Its role was fixed before it had an answer: analysis/2026-10-15-benchmark-expansion-plan.md, section 4d.

## Result

Arm `llm_wide-conversational/search_only/always_distinct/k25`, 95% Wilson intervals in brackets.

| | accuracy |
|---|---|
| **excluding adversarial** | **75.6% [73 to 78] (870/1151)** |
| overall, all five categories | 78.5% [76 to 80] (1166/1486) |
| adversarial | 88.4% [84 to 91] (296/335) |
| multi-hop | 56.9% [50 to 64] (115/202) |
| open-domain-knowledge | 54.3% [43 to 65] (38/70) |
| single-hop | 82.4% [79 to 85] (539/654) |
| temporal-reasoning | 79.1% [73 to 84] (178/225) |

Per-pass judge instability, two single judge passes compared on a sample: 0.0% (0 of 40 items graded twice). The best-of-3 majority verdict changes less often than a single pass.
Write-yield at ingest: 99.3% (2003 of 2017 extracted memories stored).

## What ran

| | |
|---|---|
| run date | 2026-10-15T17:18:20.356187+00:00 |
| engine commit | `a1b7e736b20da3e1e60739064f4903226f04a5b0` |
| engine branch | `bench/settle-20260930` |
| engine tree dirty | False |
| dataset | `locomo10.json` `sha256:79fa87e90f04081343b8c8debecb80a9a6842b76a7aa537dc9fdf651ea698ff4`, 1986 questions in the file |
| conversations | `conv-41`, `conv-42`, `conv-43`, `conv-44`, `conv-47`, `conv-48`, `conv-50` |
| extractor | `claude-opus-4-8` via claude-cli |
| reader | `claude-opus-4-8` via claude-cli |
| judge | `claude-sonnet-5` via claude-cli, provider `claude` |
| reader stance | `grounded` |
| embedding model | `nomic-ai/nomic-embed-text-v1.5` at `e9b6763023c676ca8431644204f50c2b100d9aab` |
| band thresholds | {"t_high": 0.95, "t_low": 0.8, "resonance.floor": 0.75} |
| prompt hashes | `extract.md` sha256:b7fdf557f7f60a9c, `extract-wide.md` sha256:2f3fa4c9e6c1a457, `judge.md` sha256:947bebcd5375e93e, `adjudicate.md` sha256:740151c30787a630 |
| models that served | judge: `claude-sonnet-5`; reader: `claude-opus-4-8`, `claude-opus-5-5` (the CLI reports every model that ran in a call, including one it runs for its own internal work, so a role can list two) |

## Where it ran

Host and runtime were not captured for this run.

## Files

- `manifest.json`: the harness manifest, with extracted-memory text removed from its ingest samples.
- `results.jsonl`: one row per question, keyed by `question_id`, with the verdict, the best-of-3 tally and the system's answer. No question text, gold answers or conversation text; restore them from your own copy with `scripts/rejoin.py`.
- `ingest.jsonl`: per-conversation write statistics, including every class of write refusal and the engine's message for it.
