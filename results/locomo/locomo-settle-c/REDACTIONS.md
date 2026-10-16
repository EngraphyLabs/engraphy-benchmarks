# What is committed, and what is withheld

Run C of the settling measurement, 2026-10-16: a third independent run of the
combined engine (search width 25, wider extraction prompt) over the seven held-out
LoCoMo conversations, ingest included. Harness `a1b7e736b20da3e1e60739064f4903226f04a5b0`
on `EngraphyLabs/engraphy` branch `bench/settle-20260930`; `engraphy/` identical to
`aa7daa2`, the commit runs A and B measured.

**Status: complete, after the window closed.** The strict pass finished at 06:10
on 2026-10-16. The matched-convention pass rode usage caps over three cycles and
finished at 10:11, after the window's 09:06 close. The validity controls ran in a
second window, 15:06 to 15:25. Under `analysis/2026-10-15-benchmark-expansion-plan.md`
section 4d, fixed before run C had a single answer, a run incomplete at the window's
close is reported on its own, so **the two-run figures stay the headline**. Run C is
reported here in full, and the three-run mean appears only as a labelled supplement.

## Committed

| file | contents |
|---|---|
| `results.jsonl` | all 1,486 questions: id, category, Engraphy's answer, the strict verdict and its best-of-3 tally, models, timings, evidence ids, failure attribution, support fractions, envelope hash and size |
| `ingest.jsonl` | per-conversation write statistics for all 7 ingests |
| `manifest.json` | harness commit, configuration, prompt and pack hashes, thresholds, models, aggregates |
| `PROVENANCE.md` | rendered from the manifest |
| `reference/results.jsonl`, `reference/manifest.json` | the matched-convention pass: 1,151 non-adversarial questions |
| `reference/validity_controls.jsonl`, `reference/evidence_recall.jsonl`, `reference/validity_controls.py`, `reference/validity_controls.manifest.json` | the controls, as for runs A and B |

## Withheld

No LoCoMo question, gold answer or conversation text, as for every LoCoMo run here
(CC BY-NC 4.0). `scripts/redact_run.py` checked every written file for quoted dataset
questions and found none.

Recompute run C alone with `python scripts/consolidate.py results/locomo/locomo-settle-c`.
