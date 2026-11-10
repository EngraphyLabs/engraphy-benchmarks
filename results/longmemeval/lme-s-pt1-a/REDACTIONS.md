# What is committed, and what is withheld

LongMemEval-S small batch, `lme-s-pt1-a`, 2026-11-10: 6 questions from Mem0's sampler
at `per_type=1, seed=42`, the shipped arm, operator settings withheld. Written by
`scripts/redact_longmemeval.py`.

## Committed

| file | contents |
|---|---|
| `results.jsonl` | the 6 questions under the strict convention: id, type, Engraphy's answer, verdict, models, timings, envelope hash |
| `official/` | the same answers graded by LongMemEval's official judge prompts |
| `ingest.jsonl` | per-question write statistics, including split, refused and failed extraction windows |
| `manifest.json` | harness commit, configuration, prompt hashes, models, aggregates |

## Withheld

- Question text, gold answers and retrieved context, by the same rule as every
  result here.
- **Operator identity.** Every occurrence of the operator's name or email is replaced
  with `[operator]`; this run's files contained none.
