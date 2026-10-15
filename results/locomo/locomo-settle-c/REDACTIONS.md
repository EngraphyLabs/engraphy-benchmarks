# What is committed, and what is withheld

Run C of the settling measurement, 2026-10-16: a third independent run of the
combined engine (search width 25, wider extraction prompt) over the seven held-out
LoCoMo conversations, ingest included. Harness `a1b7e736b20da3e1e60739064f4903226f04a5b0`
on `EngraphyLabs/engraphy` branch `bench/settle-20260930`; `engraphy/` identical to
`aa7daa2`, the commit runs A and B measured.

**Status: the strict pass is complete. The matched-convention pass and the validity
controls were still running when this was committed.** Under
`analysis/2026-10-15-benchmark-expansion-plan.md` section 4d, decided before run C
had a single answer, run C joins a three-run mean only if all three parts complete.
Otherwise it is reported on its own and the two-run figures stand.

## Committed

| file | contents |
|---|---|
| `results.jsonl` | all 1,486 questions: id, category, Engraphy's answer, the strict verdict and its best-of-3 tally, models, timings, evidence ids, failure attribution, support fractions, envelope hash and size |
| `ingest.jsonl` | per-conversation write statistics for all 7 ingests |
| `manifest.json` | harness commit, configuration, prompt and pack hashes, thresholds, models, aggregates |
| `PROVENANCE.md` | rendered from the manifest |

## Withheld

No LoCoMo question, gold answer or conversation text, as for every LoCoMo run here
(CC BY-NC 4.0). `scripts/redact_run.py` checked every written file for quoted dataset
questions and found none.
