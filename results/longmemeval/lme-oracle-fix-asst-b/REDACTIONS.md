# What is committed, and what is withheld

LongMemEval oracle, lever (a) of the oracle-fix experiment, `lme-oracle-fix-asst-b`,
2026-11-10: extractor `llm_wide_asst`, otherwise the flags of `lme-oracle-n30-b`.
Written by `scripts/redact_longmemeval.py`. Analysis:
`analysis/2026-10-27-oracle-fixes-experiment.md`.

## Committed

| file | contents |
|---|---|
| `results.jsonl` | all 180 questions under the strict convention: id, type, abstention flag, Engraphy's answer, verdict, models, timings, envelope hash |
| `official/` | the same answers graded by LongMemEval's official judge prompts |
| `official-facts/` | answers from a `facts` replay of the same envelopes, graded by the official judge: arm (a)+(b) |
| `ingest.jsonl` | per-question write statistics |
| `manifest.json` | harness commit, configuration, prompt hashes, models, aggregates |

## Withheld

- Question text, gold answers and retrieved context, by the same rule as every
  result here.
- **Operator identity.** Every occurrence of the operator's name or email is replaced
  with `[operator]`; this run's files contained none.
