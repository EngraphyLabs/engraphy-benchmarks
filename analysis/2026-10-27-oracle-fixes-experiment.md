# LongMemEval oracle: the two pre-registered levers, measured

Plan: `analysis/2026-10-27-benchmark-slate-plan.md` section 1, committed at `31a728e`
before any arm ran. Runs 2026-11-10. Harness `EngraphyLabs/engraphy` branch
`bench/lme-oracle-fixes-20261027` at `9d05779`, whose `engraphy/` tree is identical
to `aa7daa2`: no engine behaviour changed. Both levers are opt-in; the shipped
defaults `llm_wide` and `grounded` are unchanged.

Recompute every figure below from the committed results:

```
python scripts/oracle_fix_report.py --runs results/longmemeval \
    --seen <engine>/runs/lme-oracle-subset-n15.txt \
    --arm "a=lme-oracle-fix-asst-a+lme-oracle-fix-asst-b:official" \
    --arm "ab=lme-oracle-fix-asst-a+lme-oracle-fix-asst-b:official-facts" \
    --arm "b=official-facts" \
    --arm "rejudge=official-rejudge" \
    --arm "rejudge_iso=official-rejudge-isolated@lme-oracle-n30-a" \
    --arm "iso=official-grounded-isolated@lme-oracle-n30-a"
```

## The arms

| arm | change | data |
|---|---|---|
| baseline | none: committed runs `lme-oracle-n30-a` and `-b` | `official/` in each |
| (b) reader | stance `facts` over the saved envelopes, no re-ingest | `official-facts/` in each baseline run |
| (a) extraction | extractor `llm_wide_asst` (`extract-wide-assistant.md`, sha256 `29e77126c09538c0`), a fresh ingest per run | `lme-oracle-fix-asst-a/official`, `-b/official` |
| (a)+(b) | the (a) store read under `facts` | `lme-oracle-fix-asst-a/official-facts`, `-b/official-facts` |

Every arm is graded by LongMemEval's official judge prompts, under the same CLI
condition as the baseline (operator settings in context), so the lever is the only
difference. Arm (a) run A is paired with baseline run A, and run B with run B.

## Result: two-run means, official judge

All 180 questions / the 124 out-of-sample questions (not in the N = 15 set the levers
were written from). p is the exact two-sided McNemar test over per-question outcomes.

| type | baseline | (a) | (b) | (a)+(b) |
|---|---|---|---|---|
| single-session-user | 90.0 / 91.7 | 90.0 / 89.6 | 95.0 / 95.8 | 96.7 / 95.8 |
| single-session-assistant | 26.7 / 25.0 | **88.3 / 87.5** | 26.7 / 25.0 | **86.7 / 87.5** |
| single-session-preference | 43.3 / 56.7 | 43.3 / 50.0 | 61.7 / 76.7 | 61.7 / 80.0 |
| multi-session | 93.3 / 100 | 86.7 / 91.7 | 90.0 / 95.8 | 85.0 / 89.6 |
| temporal-reasoning | 90.0 / 90.4 | 78.3 / 80.8 | 83.3 / 86.5 | 80.0 / 80.8 |
| knowledge-update | 96.7 / 96.7 | 96.7 / 93.3 | 95.0 / 96.7 | 91.7 / 96.7 |
| **overall** | 73.3 / 78.6 | 80.6 / 83.5 | 75.3 / 80.2 | **83.6 / 88.3** |
| abstention, wrongly answered of 20 | 0 | 4 | 2 | 6 |

Out-of-sample tests:

| arm | category that lifts at p < 0.05 | overall, out-of-sample |
|---|---|---|
| (a) | single-session-assistant, 15 better, 0 worse, p = 0.0001 | +4.8, 22 better, 17 worse, p = 0.52 |
| (b) | none; preference +20.0, 6 better, 1 worse, p = 0.13 | +1.6, p = 0.79 |
| (a)+(b) | single-session-assistant, p = 0.0001 | **+9.7, 26 better, 12 worse, p = 0.034** |

## Against the pre-registered rule

- **Lever (b)** lifts no category out-of-sample. Its preference gain is large on all
  180 (p = 0.02) but does not reach significance on the 124 out-of-sample questions.
  Abstention: 2 of 20, within the bar.
- **Lever (a)** lifts single-session-assistant out-of-sample, decisively. The rule
  states its abstention bar for (b); measured by the same bar, (a) answers 4 of 20.
- **(a)+(b)** lifts single-session-assistant and the out-of-sample overall. It answers
  6 of 20 unanswerable question-runs.

**Nothing ships from this.** As pre-registered, whether a lever becomes a default is
the owner's decision, and would also require LoCoMo's adversarial declines to hold.

## What each lever costs

**Abstention.** With the assistant's statements in the store, the reader treats them
as facts about the user. The same two false-premise questions fail in all four (a)
read-outs: a savings figure computed from the assistant's own fare estimate, and a
university named from a poster the assistant described. Under `facts`, two further
answers are partial corrections ("you live in Harajuku, not Shinjuku"; "no iPad
purchase is recorded") that the official judge grades as answered.

**Temporal reasoning and multi-session.** (a) grows the store by about half (2,635
and 2,643 memories against 1,799 and 1,772), while the reader still sees the top 25.
Several temporal answers that were right become INSUFFICIENT, consistent with the
user's dated events being crowded out of the envelope. Multi-session loses 2 to 3
questions under every (a) read-out.

**Ingest.** Extractor output rises by about 40% per run.

A shippable form of (a) would need the reader to keep assistant-attributed memories
apart from facts about the user, and the envelope depth revisited for the larger
store. Both are new levers and would need their own pre-registration.

## Controls: judge noise and the operator's settings

| control (baseline answers, official judge) | all 180 | out-of-sample | p, out-of-sample |
|---|---|---|---|
| same answers re-judged, same condition, both runs | 73.6 (+0.3) | 77.8 | 0.73 |
| same answers re-judged with settings withheld from the judge, run A | 70.0 (−3.3) | 72.6 (−5.6) | 0.016 |
| reader and judge both with settings withheld, run A | 68.3 (−5.0) | 72.6 (−5.6) | 0.039 |

Re-judging identical answers moves the score by 0.3 points, with flips in both
directions: the official judge's noise is small and symmetric. Withholding the
operator's settings from the judge alone lowers the score by 3.3 points, and every
flip runs one way (0 better, 7 worse out-of-sample). The operator's settings make the
official judge more lenient. Of the 5.0 points lost when both reader and judge run
isolated, about 3.3 are the judge and 1.7 the reader.

Every arm in this experiment and its baseline share the same condition, so the
comparisons above stand. The absolute levels do not transfer to an isolated grade.
The LongMemEval oracle figures already committed were graded under the same
condition; an isolated re-grade of their saved answers (judge calls only) would give
the figure comparable to a clean setup. LongMemEval-S and BEAM run isolated.

## Files

- `results/longmemeval/lme-oracle-fix-asst-a/`, `-b/`: lever (a) runs, redacted, with
  PROVENANCE.md.
- `results/longmemeval/lme-oracle-n30-a/`, `-b/`: `official-facts/` (lever b),
  `official-rejudge/`, and in run A `official-rejudge-isolated/` and
  `official-grounded-isolated/`.
- `scripts/oracle_fix_report.py`: the scorer.
