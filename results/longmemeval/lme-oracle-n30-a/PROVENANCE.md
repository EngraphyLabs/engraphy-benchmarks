# Provenance: `lme-oracle-n30-a`

LongMemEval, oracle setting. This renderer uses LoCoMo's labels: 'excluding adversarial' here means excluding LongMemEval's abstention questions, and 'conversations' are question ids, one haystack each. The official LongMemEval figures, which count abstention, are in official/ and official-reader/ and recompute with scripts/consolidate_longmemeval.py. The 'engine commit' is the harness commit; its engraphy/ tree is identical to aa7daa2. Reproduce: config/longmemeval-oracle.json.

## Result

Arm `llm_wide-conversational/search_only/always_distinct/k25`, 95% Wilson intervals in brackets.

| | accuracy |
|---|---|
| **excluding adversarial** | **72.9% [66 to 79] (124/170)** |
| overall, all five categories | 74.4% [68 to 80] (134/180) |
| knowledge-update | 93.3% [79 to 98] (28/30) |
| multi-session | 93.3% [79 to 98] (28/30) |
| single-session-assistant | 26.7% [14 to 44] (8/30) |
| single-session-preference | 43.3% [27 to 61] (13/30) |
| single-session-user | 93.3% [79 to 98] (28/30) |
| temporal-reasoning | 96.7% [83 to 99] (29/30) |

Per-pass judge instability, two single judge passes compared on a sample: 2.5% (1 of 40 items graded twice). The best-of-3 majority verdict changes less often than a single pass.
Write-yield at ingest: 97.4% (1799 of 1847 extracted memories stored).

## What ran

| | |
|---|---|
| run date | 2026-10-15T15:06:51.495223+00:00 |
| engine commit | `9883405554b556828a19216f639ccd97972d9173` |
| engine branch | `bench/longmemeval-20261015` |
| engine tree dirty | True |
| dataset | `longmemeval/longmemeval_oracle.json` `sha256:821a2034d219ab45846873dd14c14f12cfe7776e73527a483f9dac095d38620c`, 500 questions in the file |
| conversations | `08f4fc43`, `982b5123`, `e4e14d04`, `d01c6aa8`, `993da5e2`, `a3045048`, `gpt4_d31cdae3`, `gpt4_4cd9eba1`, `b29f3365`, `6613b389`, `8c18457d`, `d23cf73b`, `eeda8a6d`, `9d25d4e0`, `129d1232`, `a9f6b44c`, `d851d5ba`, `gpt4_e05b82a6`, `1a8a66a6`, `gpt4_372c3eed`, `80ec1f4f_abs`, `60bf93ed_abs`, `gpt4_372c3eed_abs`, `6a1eabeb`, `71315a70`, `07741c44`, `a1eacc2a`, `184da446`, `031748ae`, `4d6b87c8`, `0f05491a`, `f9e8c073`, `5a4f22c0`, `6071bd76`, `e493bb7c`, `618f13b2`, `01493427`, `6a27ffc2`, `18bc8abd`, `7a87bd0c`, `4b24c848`, `7e974930`, `5831f84d`, `eace081b`, `50635ada`, `e66b632c`, `f685340e`, `dfde3500`, `06db6396`, `10e09553`, `5c40ec5b`, `2133c1b5_abs`, `f685340e_abs`, `8a2466db`, `06878be2`, `75832dbd`, `0edc2aef`, `35a27287`, `32260d93`, `195a1a1b`, `afdc33df`, `caf03d32`, `54026fce`, `06f04340`, `6b7dfb22`, `1a1907b4`, `09d032c9`, `38146c39`, `d24813b1`, `57f827a0`, `95228167`, `505af2f5`, `75f70248`, `d6233ab6`, `1da05512`, `fca70973`, `b6025781`, `a89d7624`, `b0479f84`, `1d4e3b97`, `07b6f563`, `1c0ddc50`, `0a34ad58`, `e9327a54`, `4c36ccef`, `6ae235be`, `1903aded`, `ceb54acb`, `fea54f57`, `488d3006`, `8cf51dda`, `1d4da289`, `3249768e`, `1b9b7252`, `6222b6eb`, `d596882b`, `e3fc4d6e`, `51b23612`, `3e321797`, `e982271f`, `fca762bc`, `7a8d0b71`, `5809eb10`, `41275add`, `4388e9dd`, `b759caee`, `ac031881`, `28bcfaac`, `16c90bf4`, `c8f1aeed`, `eaca4986`, `c7cf7dfd`, `65240037`, `c5e8278d`, `5d3d2817`, `7527f7e2`, `3b6f954b`, `726462e0`, `66f24dbb`, `8ebdbe50`, `75499fd8`, `21436231`, `a06e4cfe`, `37d43f65`, `d52b4f67`, `25e5aa4f`, `8550ddae`, `60d45044`, `577d4d32`, `ec81a493`, `15745da0`, `e01b8e2f`, `bc8a6e93`, `001be529`, `b320f3f8`, `19b5f2b3`, `4fd1909e`, `86f00804`, `c19f7a0b`, `1faac195`, `c14c00dd`, `19b5f2b3_abs`, `f4f1d8a4_abs`, `gpt4_f49edff3`, `gpt4_b5700ca9`, `gpt4_e072b769`, `gpt4_6dc9b45b`, `gpt4_1916e0ea`, `gpt4_468eb063`, `gpt4_61e13b3c`, `gpt4_e061b84f`, `gpt4_ec93e27f`, `bcbe585f`, `gpt4_7ddcf75f`, `gpt4_a2d1d1f6`, `gpt4_85da3956`, `gpt4_e061b84g`, `gpt4_d6585ce9`, `gpt4_59149c78`, `gpt4_fa19884d`, `gpt4_b5700ca0`, `gpt4_68e94288`, `7405e8b1`, `6456829e`, `a4996e51`, `60036106`, `681a1674`, `4bc144e2`, `9ee3ecd6`, `92a0aa75`, `1c549ce4`, `61f8c8f8`, `60159905`, `bc149d6b`, `157a136e`, `55241a1f`, `21d02d0d`, `e5ba910e_abs`, `a96c20ee_abs`, `09ba9854_abs` |
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
