# What is committed, and what is withheld

LongMemEval oracle run A, `lme-oracle-a`, 2026-10-15: the LoCoMo-settled engine
unchanged (`llm_wide-conversational/search_only/always_distinct/k25`), over the
90 questions of Mem0's public sampler at `per_type=15, seed=42`, oracle setting.
Harness `9883405` on `EngraphyLabs/engraphy` branch `bench/longmemeval-20261015`;
engine code identical to `aa7daa2`. Dataset `longmemeval_oracle.json`, sha256
`821a2034d219ab45846873dd14c14f12cfe7776e73527a483f9dac095d38620c`, from Hugging Face
`xiaowu0162/longmemeval-cleaned` at `98d7416c`, MIT.

## Committed

| file | contents |
|---|---|
| `results.jsonl` | all 90 questions under the strict convention: id, type, abstention flag, Engraphy's answer, the best-of-3 verdict and how it was graded, models, timings, support fractions, and the sha256 and size of the envelope the reader saw |
| `official/` | the same answers graded by LongMemEval's official judge prompts, vendored at `9e0b455`; the judge's raw reply is the `reason` |
| `official-reader/` | answers from the official answer template over the same envelopes, graded by the official judge |
| `ingest.jsonl` | per-question write statistics: drafts, memories stored, extractor output tokens, write refusals with the engine's message |
| `manifest.json` | harness commit, configuration, prompt and pack hashes, thresholds, models, aggregates |
| `diagnosis/diagnosis.jsonl` | per question, model-free: memories in the store and in the envelope, the gold-support heuristic over each, and the computed failure stage |
| `diagnosis/adjudication.jsonl` | the hand adjudication of every failure under either official convention: stage and reason, no dataset text |

## Withheld

- Question text, gold answers and retrieved context, by the same rule as every
  LoCoMo result here, though LongMemEval's licence would allow them.
- **Operator identity.** On the Claude Code CLI route the extractor sometimes
  named LongMemEval's anonymous "user" after the signed-in operator. 26 occurrences
  of the operator's name or email in this run's files are replaced with
  `[operator]` by `scripts/redact_longmemeval.py`. No verdict changes.

Recompute: `python scripts/consolidate_longmemeval.py results/longmemeval/lme-oracle-a results/longmemeval/lme-oracle-b`.
Diagnosis: `analysis/2026-10-15-longmemeval-oracle-diagnosis.md`.
