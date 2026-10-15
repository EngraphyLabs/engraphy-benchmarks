# Provenance: `lme-oracle-a`

LongMemEval, oracle setting. This renderer uses LoCoMo's labels: 'excluding adversarial' here means excluding LongMemEval's abstention questions, and 'conversations' are question ids, one haystack each. The official LongMemEval figures, which count abstention, are in official/ and official-reader/ and recompute with scripts/consolidate_longmemeval.py. The 'engine commit' is the harness commit; its engraphy/ tree is identical to aa7daa2. Reproduce: config/longmemeval-oracle.json.

## Result

Arm `llm_wide-conversational/search_only/always_distinct/k25`, 95% Wilson intervals in brackets.

| | accuracy |
|---|---|
| **excluding adversarial** | **67.1% [57 to 76] (57/85)** |
| overall, all five categories | 68.9% [59 to 78] (62/90) |
| knowledge-update | 93.3% [70 to 99] (14/15) |
| multi-session | 73.3% [48 to 89] (11/15) |
| single-session-assistant | 20.0% [7 to 45] (3/15) |
| single-session-preference | 40.0% [20 to 64] (6/15) |
| single-session-user | 93.3% [70 to 99] (14/15) |
| temporal-reasoning | 93.3% [70 to 99] (14/15) |

Per-pass judge instability, two single judge passes compared on a sample: 5.0% (2 of 40 items graded twice). The best-of-3 majority verdict changes less often than a single pass.
Write-yield at ingest: 96.9% (851 of 878 extracted memories stored).

## What ran

| | |
|---|---|
| run date | 2026-10-15T13:45:47.950624+00:00 |
| engine commit | `9883405554b556828a19216f639ccd97972d9173` |
| engine branch | `bench/longmemeval-20261015` |
| engine tree dirty | False |
| dataset | `longmemeval/longmemeval_oracle.json` `sha256:821a2034d219ab45846873dd14c14f12cfe7776e73527a483f9dac095d38620c`, 500 questions in the file |
| conversations | `gpt4_2487a7cb`, `gpt4_385a5000`, `f0853d11`, `gpt4_70e84552`, `gpt4_2c50253f`, `gpt4_4cd9eba1`, `gpt4_93159ced_abs`, `0a995998`, `6cb6f249`, `gpt4_d12ceb0e`, `eeda8a6d`, `edced276_abs`, `07741c44`, `a1eacc2a`, `184da446`, `4d6b87c8`, `0f05491a`, `5a4f22c0`, `e493bb7c`, `618f13b2`, `18bc8abd`, `5831f84d`, `50635ada`, `dfde3500`, `06db6396`, `2133c1b5_abs`, `f685340e_abs`, `8a2466db`, `75832dbd`, `32260d93`, `195a1a1b`, `caf03d32`, `06f04340`, `1a1907b4`, `09d032c9`, `95228167`, `75f70248`, `d6233ab6`, `fca70973`, `a89d7624`, `1d4e3b97`, `07b6f563`, `6ae235be`, `fea54f57`, `dc439ea3`, `1d4da289`, `8aef76bc`, `1b9b7252`, `6222b6eb`, `fca762bc`, `7a8d0b71`, `8b9d4367`, `4baee567`, `ac031881`, `16c90bf4`, `eaca4986`, `1de5cff2`, `c960da58`, `3b6f954b`, `94f70d80`, `ad7109d1`, `8ebdbe50`, `75499fd8`, `95bcc1c8`, `a06e4cfe`, `8550ddae`, `15745da0`, `8a137a7f`, `8e9d538c`, `4100d0a0`, `a82c026e`, `29f2956b_abs`, `71017276`, `6e984301`, `eac54adc`, `gpt4_85da3956`, `2ebe6c92`, `gpt4_d6585ce9`, `gpt4_4929293b`, `gpt4_68e94288`, `7405e8b1`, `f35224e0`, `60036106`, `9ee3ecd6`, `77eafa52`, `0100672e`, `bb7c3b45`, `60159905`, `bc149d6b`, `37f165cf` |
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
