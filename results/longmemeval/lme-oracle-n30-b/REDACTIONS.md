# What is committed, and what is withheld

LongMemEval oracle N = 30 run B, `lme-oracle-n30-b`, 2026-10-16: the LoCoMo-settled engine
unchanged (`llm_wide-conversational/search_only/always_distinct/k25`), over the
180 questions of Mem0's public sampler at `per_type=30, seed=42`, oracle setting.
Harness `5a9a363` on `EngraphyLabs/engraphy` branch `bench/longmemeval-20261015`;
engine code identical to `aa7daa2`. Dataset `longmemeval_oracle.json`, sha256
`821a2034d219ab45846873dd14c14f12cfe7776e73527a483f9dac095d38620c`, from Hugging Face
`xiaowu0162/longmemeval-cleaned` at `98d7416c`, MIT.

## Committed

| file | contents |
|---|---|
| `results.jsonl` | all 180 questions under the strict convention: id, type, abstention flag, Engraphy's answer, the best-of-3 verdict and how it was graded, models, timings, support fractions, and the sha256 and size of the envelope the reader saw |
| `official/` | the same answers graded by LongMemEval's official judge prompts, vendored at `9e0b455`; the judge's raw reply is the `reason` |
| `official-reader/` | answers from the official answer template over the same envelopes, graded by the official judge |
| `ingest.jsonl` | per-question write statistics: drafts, memories stored, extractor output tokens, write refusals with the engine's message |
| `manifest.json` | harness commit, configuration, prompt and pack hashes, thresholds, models, aggregates |

## Withheld

- Question text, gold answers and retrieved context, by the same rule as every
  LoCoMo result here, though LongMemEval's licence would allow them.
- **Operator identity.** On the Claude Code CLI route the extractor sometimes
  named LongMemEval's anonymous "user" after the signed-in operator. 25 occurrences
  of the operator's name or email in this run's files are replaced with
  `[operator]` by `scripts/redact_longmemeval.py`. No verdict changes.

Recompute: `python scripts/consolidate_longmemeval.py results/longmemeval/lme-oracle-n30-a results/longmemeval/lme-oracle-n30-b`. This pair is the pre-registered LongMemEval headline; plan section 4b.
Diagnosis: `analysis/2026-10-15-longmemeval-oracle-diagnosis.md`.

