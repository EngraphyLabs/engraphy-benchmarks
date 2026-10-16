# LoCoMo: the consolidated two-run result

Two independent runs of the current engine over the seven LoCoMo conversations
that no lever was tuned on, each re-ingesting the corpus from scratch. Both
conventions reported. Every figure recomputes from files committed in this
repository.

- Engine: `aa7daa2b9c5f190ee3f10de5b9bf4cbaee44e5a6`, branch
  `bench/settle-20260930` of `EngraphyLabs/engraphy`. The scoring path
  (`bench/core/run.py`) last changed at `af6c96e`; commits after it touch offline
  and reporting tools only.
- Configuration: search width 25 with the wider extraction prompt
  (`llm_wide-conversational/search_only/always_distinct/k25`).
- Artifacts: `results/locomo/locomo-settle-a/` (2026-10-03) and
  `results/locomo/locomo-settle-b/` (2026-10-09).
- Dataset: LoCoMo `locomo10.json`, sha256
  `79fa87e90f04081343b8c8debecb80a9a6842b76a7aa537dc9fdf651ea698ff4`, upstream
  commit `cbfbc1dba6bc53d00625212a0f22d55ffee7c1fc`. CC BY-NC 4.0, not
  redistributed here.
- Split: conv-41, conv-42, conv-43, conv-44, conv-47, conv-48, conv-50. Per run:
  1,486 questions, 1,151 non-adversarial, 335 adversarial, 209 sessions.

Figures are the mean of the two runs with the range across them. Two runs give a
mean and a range, not a standard deviation, so no figure here carries a
plus-or-minus.

## Reproducing every number

    python scripts/consolidate.py results/locomo/locomo-settle-a \
                                  results/locomo/locomo-settle-b

    # the extraction lever, paired per question, from run A's two arms
    git clone https://github.com/EngraphyLabs/engraphy.git ../engraphy
    git -C ../engraphy checkout aa7daa2b9c5f190ee3f10de5b9bf4cbaee44e5a6
    python ../engraphy/scripts/arm_compare.py \
        results/locomo/locomo-settle-a/results.jsonl

Each run directory's `REDACTIONS.md` lists what is committed and what is withheld
as dataset text; `PROVENANCE.md` records the engine commit, dataset hash, models
and prompt hashes.

## 1. The two conventions

**Strict** is Engraphy's own default and the harder of the two. The reader may
decline when memory does not support an answer; the judge requires every item of
a multi-item gold answer; each answer is graded best-of-3 to damp the judge's
measured per-pass instability; adversarial questions are included and scored.

**Matched convention** reproduces the conventions the published figures were
produced under, vendored verbatim from `mem0ai/memory-benchmarks` at
`4b61c5d31b9c668a12b4f5e78064248a02c82d2b`: an answer prompt that forces a
commitment rather than allowing a decline, a judge that accepts one item of a
multi-item gold answer with 14-day date and 50% duration tolerance, categories 1
to 4 only so adversarial is excluded, one judge pass, and up to 200 memories in
context. Engraphy's engine returns at most 25 results by design, so it competes
under that convention with a smaller context than the convention permits.

The published figures are matched-convention figures, so that table is the
like-for-like comparison and the strict table is the conservative number
Engraphy reports as its own default.

Models, both conventions: extractor, reader and adjudicator `claude-opus-4-8`;
judge `claude-sonnet-5`, reached through the Claude Code CLI. Embedder
`nomic-ai/nomic-embed-text-v1.5` at revision
`e9b6763023c676ca8431644204f50c2b100d9aab`, onnx-fp32, 384 dims.

Mem0's published 66.88 used a GPT-4o-mini answerer and is the mean of 10 runs. A
reader model is part of a memory system's measured result under both conventions,
and neither side's figure isolates retrieval from reading. That difference in
setup survives convention matching, and is stated rather than papered over.

## 2. The corrected category alignment

The Mem0 paper's per-category table (arXiv:2504.19413, Table 2) carries column
headers that do not name the LoCoMo categories they hold. Of the 24 possible
assignments of its four columns to LoCoMo's four non-adversarial categories,
exactly one reproduces the paper's own published overall for all five systems it
reports, to within 0.01:

| paper column | LoCoMo category |
|---|---|
| "Single-Hop" | category 1, multi-hop |
| "Multi-Hop" | category 3, open-domain |
| "Open-Domain" | category 4, single-hop |
| "Temporal" | category 2, temporal |

Derivation and sources: `analysis/2026-09-19-locomo-open-domain-findings.md` and
the Fable analysis node `d7c05bc3`. `scripts/consolidate.py` holds the remapped
published values, so the alignment is applied by code rather than by hand.

## 3. Matched convention: the like-for-like comparison

2,302 non-adversarial questions across the two runs.

| category | Engraphy mean (range) | Mem0 | Mem0-graph | Zep (as Mem0 measured) | Zep (self-reported) | margin over the best |
|---|---|---|---|---|---|---|
| excluding adversarial | **91.4%** (91.0 to 91.8), 2,104/2,302, 95% [90, 92] | 66.88 | 68.44 | 65.99 | 75.14 | +16.3 |
| single-hop | 93.3% (92.7 to 94.0), 1,221/1,308 | 72.93 | 75.71 | 76.60 | | +16.7 |
| multi-hop | 91.8% (90.1 to 93.6), 371/404 | 67.13 | 65.71 | 61.70 | | +24.7 |
| temporal | 92.2% (90.7 to 93.8), 415/450 | 55.51 | 58.13 | 49.31 | | +34.1 |
| open-domain | 69.3% (68.6 to 70.0), 97/140 | 51.15 | 47.19 | 41.35 | | +18.2 |

Engraphy holds the highest figure in this table in every category, and each
individual run's figure, not only the mean, sits above every figure in it.

**Mem0 Platform's current figure, from the same harness.** `mem0ai/memory-benchmarks`
at `4b61c5d`, the source of this convention, reports Mem0 Platform's v3 pipeline at
92.5% (1,425/1,540) with up to 200 memories in context and 91.8% (1,414/1,540)
with up to 50, all ten conversations. Per category, averaged over cutoffs of 10
to 200: single-hop 91.2%, multi-hop 91.3%, temporal 92.0%, open-domain 72.7%.
Self-reported; the README does not name the answerer and judge, and the harness
defaults to gpt-5 for both. Against it, Engraphy's 91.4% raw is **level with the
top-50 figure and 0.7 to 1.5 points below the top-200 figure**: both runs, 91.0 and
91.8, and the pooled interval, 90 to 92, sit below 92.5. That is with at most 25
memories in context, on 7 of the 10 conversations. By category, Engraphy is ahead on single-hop,
level on multi-hop and temporal, and behind on open-domain. Mem0 Platform's
figure carries no confabulation control, so the like-for-like comparison with it
is raw against raw.

**Why multi-hop differs so much between the conventions.** Multi-hop gold answers
are typically multi-item. The strict judge requires every item; the matched judge
accepts one. The same stored memory and the same retrieved context therefore
score very differently, and the gap is a property of the grading rule rather than
of the retrieval. Under the convention the published figures use, Engraphy answers
multi-hop questions at least as completely as the leaders do; under its own
stricter rule it does not yet answer them completely.

### 3a. The like-for-like figure, bounded by its validity controls

Added 2026-10-15. The two controls that bounded the earlier three-conversation
figure were rerun on both runs, on the same saved answers, with no new reading:

- **Control A.** The strict judge, one pass, re-graded every answer the matched
  judge accepted: 1,047 in run A and 1,057 in run B.
- **Control B.** 60 accepted questions per run, each paired with the matched
  answer to a different question from the same conversation, graded by both
  judges. Every pair is wrong by construction, so an acceptance measures leniency.
- **Evidence recall.** Per question, the share of LoCoMo's cited evidence turns
  present in the memories the reader saw, computed from the saved envelopes with
  no search and no model. Run A's mean, 87.49%, reproduces section 7's figure for
  width 25 exactly.

The **defensible** figure removes every credit that only the matched rules accept
(control A says no) on a question none of whose evidence turns was retrieved. The
**floor** keeps only answers the strict judge also accepts.

| category | raw, mean (range) | defensible, mean (range) | floor, mean (range) |
|---|---|---|---|
| excluding adversarial | 91.4% (91.0 to 91.8) | **90.0% (89.6 to 90.4)**, 2,072/2,302, 95% [89, 91] | 81.2% (81.1 to 81.2) |
| single-hop | 93.3% | 92.1% (91.6 to 92.7) | 88.8% |
| multi-hop | 91.8% | 89.4% (88.1 to 90.6) | 62.9% |
| temporal | 92.2% | 91.3% (89.8 to 92.9) | 81.6% |
| open-domain | 69.3% | 67.9% (67.1 to 68.6), n=140 | 61.4% |

Control B: the matched judge accepted 2 and 3 of 60 mismatched answers in runs A
and B, and the strict judge 2 and 2. On the earlier split it was 6 against 1.

What this establishes:

- **The adjustment is 1.4 points**, about half the 3 points the earlier split
  measured. The raw figure overstates by little.
- The defensible figure sits **ahead of the Mem0 paper's Mem0, Mem0-graph and Zep
  figures in every category**, and ahead of Zep's self-reported 75.14 overall.
- The floor is the most conservative reading: every credit the strict rubric does
  not also give is removed, including correct partial answers to multi-item
  questions. On that reading multi-hop, 62.9%, sits inside the paper's published
  range rather than above it, which is the grading-rule effect described above.

Recompute: `python scripts/consolidate.py results/locomo/locomo-settle-a
results/locomo/locomo-settle-b` prints all three. The controls are in each run's
`reference/validity_controls.jsonl` with the script that produced them, and the
recall in `reference/evidence_recall.jsonl`.

### 3b. Run C, reported apart (added 2026-10-16)

A third independent run, `locomo-settle-c`, repeated the measurement exactly,
ingest included. It completed after the measurement window closed, so under the
rule fixed before it began (`analysis/2026-10-15-benchmark-expansion-plan.md`,
section 4d), it does not change the headline. It is reported here in full.

| | run A | run B | run C | three-run mean (supplement) |
|---|---|---|---|---|
| strict, excluding adversarial | 74.8% | 76.0% | 75.6% | 75.5% (sd 0.6) |
| matched, raw | 91.0% | 91.8% | 91.9% | 91.6% (sd 0.5) |
| matched, defensible | 89.6% | 90.4% | 91.1% | 90.4% (sd 0.7) |
| matched, floor | 81.2% | 81.1% | 82.9% | 81.8% (sd 1.0) |
| control B, matched / strict judge | 2 / 2 | 3 / 2 | 4 / 4 | |

Run C's strict figure falls inside the two-run range. On the matched lines it is
higher, by 0.1 points raw, 0.7 defensible and 1.7 at the floor. The third run
therefore corroborates the headline and does not lower it; the headline is the
more conservative of the two sets. Recompute either set with
`scripts/consolidate.py`, naming two or three run directories.

## 4. Strict convention: Engraphy's own default

2,302 non-adversarial and 670 adversarial questions across the two runs.

| category | Engraphy mean (range) | Mem0 | Mem0-graph | Zep (as Mem0 measured) | Zep (self-reported) |
|---|---|---|---|---|---|
| excluding adversarial | 75.4% (74.8 to 76.0), 1,736/2,302, 95% [74, 77] | 66.88 | 68.44 | 65.99 | 75.14 |
| single-hop | 83.3% (83.0 to 83.5), 1,089/1,308 | 72.93 | 75.71 | 76.60 | |
| multi-hop | 55.9% (55.9 to 55.9), 226/404 | 67.13 | 65.71 | 61.70 | |
| temporal | 76.7% (74.7 to 78.7), 345/450 | 55.51 | 58.13 | 49.31 | |
| open-domain | 54.3% (52.9 to 55.7), 76/140 | 51.15 | 47.19 | 41.35 | |
| all five categories | 78.8% (78.2 to 79.3), 2,341/2,972 | | | | |
| adversarial | 90.3% (89.9 to 90.7), 605/670 | not reported by any of the three | | | |

Read honestly, under the strict convention:

- Overall it is **level with Zep's own self-reported figure**: the mean is 75.4%
  and the run range, 74.8 to 76.0, straddles 75.14.
- Ahead of the figures Mem0 published for Mem0, Mem0-graph and Zep.
- Ahead on single-hop, temporal and open-domain, with both runs above the best
  comparator in each.
- **Multi-hop is behind all three**, and identically in both runs.
- This table is not like-for-like: it puts Engraphy's harder convention against
  figures produced under the permissive one. It is here because it is the number
  Engraphy stands behind as its default, and because publishing only the
  favourable convention is what a sceptic should attack.

## 5. The run-to-run spread

| | mean | range | runs |
|---|---|---|---|
| matched convention | 91.4% | 0.8 points | 91.0, 91.8 |
| strict, non-adversarial | 75.4% | 1.2 points | 74.8, 76.0 |
| strict, adversarial | 90.3% | 0.9 points | 89.9, 90.7 |
| strict, all five categories | 78.8% | 1.1 points | 78.2, 79.3 |

Each run re-ingested all seven conversations, so this range covers extraction
variation as well as sampling. Per category the widest spread is matched
multi-hop at 3.5 points on 202 questions per run; strict multi-hop came out
identical in both runs.

This is the quantity that was missing from a single run. The sampling intervals
in sections 3 and 4 cover the chance that these questions happened to favour the
system; the range here covers the store being rebuilt by a model call.

## 6. The extraction lever, measured out of sample

Run A carries two arms on one ingest, so the wider extraction prompt is compared
against the shipped one on the same conversations, same reader, same judge, paired
per question. From `results/locomo/locomo-settle-a/arm-compare.json`.

| | shipped prompt | wider prompt | paired result |
|---|---|---|---|
| non-adversarial | 72.11% (830/1,151) | 74.80% (861/1,151) | discordant 62/93, exact McNemar **p 0.016** |
| adversarial | 88.96% (298/335) | 89.85% (301/335) | discordant 11/14, p 0.69 |
| single-hop | 78.90% | 83.03% | +4.13 |
| multi-hop | 55.45% | 55.94% | +0.49 |
| temporal | 73.78% | 74.67% | +0.89 |
| open-domain | 51.43% | 52.86% | +1.43 |

**+2.69 points out of sample, against a run-to-run spread of 1.22 points.** The
pre-registered rule asked for two things: significance against chance, which
p 0.016 gives, and an effect larger than the spread between runs of one
configuration, which the two runs now establish. The lever clears both, and is
kept.

The gain is concentrated in single-hop, which is what the mechanism predicts:
single-hop is one fact in one turn, and what the wider prompt contributes is
storing facts the shipped prompt discarded. Multi-hop barely moves, consistent
with multi-hop being limited by retrieval and reasoning rather than by what is
stored. On the seen split the same comparison came to +7.46 points; that split is
the one the prompt was fitted to, so it is validation and the held-out figure is
the effect.

**Disclosure.** The wider prompt was written against
`2026-09-30-extraction-gap-labels.json`, 46 questions all on the seen split,
hand-labelled by reading each question's gold answer and its cited evidence
turns. The prompt contains no question, gold answer or conversation text, so what
was fitted is the kind of fact worth storing; the exposure is real and bounded,
and the held-out split was never read or labelled while the prompt was written.
The gap-set recovery figure is circular and is not cited as evidence. Full
disclosure in `analysis/2026-09-30-settling-run-preregistration.md`.

## 7. Retrieval isolation, with no model in the loop

From `results/locomo/locomo-settle-a/retrieval-isolation.txt`, built from run A's
store. "Recall" is the share of cited evidence turns present in the retrieved
context; "all evidence" is the share of questions whose every evidence turn is
present. No reader and no judge, so these are retrieval properties, not accuracy.

| retrieval arm | evidence recall | all evidence held | context size |
|---|---|---|---|
| k=20 | 86.47% | 81.88% | 12,034 chars |
| **k=25 (shipped)** | **87.49%** | **83.10%** | 15,029 |
| k=25 + entity roster | 92.62% | 89.11% | 25,807 |
| k=25 + source turns (excluded by design) | 91.29% | 87.37% | 16,701 |
| k=25 + both | 95.97% | 93.38% | 27,489 |
| flat 50 | 88.86% | 84.32% | 18,028 |
| entity 50 | 90.13% | 86.06% | 29,693 |

Width 25 over width 20 is +1.02 points of recall for 25% more context. The entity
roster is +5.13 points of recall for 72% more context.

The accuracy-level replays of k=20 and roster-on were not run, by decision, so
these rows are retrieval measurements only. What is known about whether that
recall converts: on the seen split the roster replay gained 5 non-adversarial
questions at p 0.46 with no adversarial cost, which did not meet the bar to ship,
and the roster stays default-off. The source-turn layer is excluded on design
grounds and because it was measured to cost 8 adversarial declines.

## 8. What these two runs support

### Defensible now

- Every exact figure above, quoted as the mean of two named runs over a named
  split with the artifact path attached.
- Under the matched convention, **ahead of the Mem0 paper's Mem0, Mem0-graph and
  Zep figures on every LoCoMo category**, raw and defensible. The smallest raw
  margin is +16.3 points overall against Zep's own self-reported figure, and each
  run's own figure clears every one of them.
- **Level with Mem0 Platform's same-harness 91.8% at top-50, and 0.7 to 1.5 points
  below its 92.5% at top-200**, raw against raw.
- The hardened like-for-like figure: **90.0% defensible**, range 89.6 to 90.4,
  floor 81.2%.
- Under the strict convention: ahead of the published Mem0, Mem0-graph and Zep
  figures overall, and ahead on single-hop, temporal and open-domain.
- Run-to-run spread under 1.3 points on both conventions.
- The extraction lever's +2.69 points, now clearing both conditions of its rule.

### Stays level, and stays behind

- The strict overall figure against Zep's self-reported 75.14% is **level**: the
  run range straddles it.
- Strict multi-hop is **behind all three**.

### Still not supported

- A plus-or-minus on any figure. Two runs give a mean and a range.
- "Consistently", "stable across runs", "repeatable", "typically". The range is
  the honest form.
- "Best memory system" as a standing property: two runs, one benchmark, one
  split, this harness. The measured claim is the defensible one.
- "The leading memory system on LoCoMo": Mem0 Platform's same-harness figures are
  level with Engraphy's at top-50 and above it at top-200.
- Open-domain quoted without its size: 140 questions pooled, 95% interval 61 to
  76 like-for-like.

## 9. Caveats that travel with every figure

1. **Two runs**, each with its own ingest, reported as a mean with a range.
2. **Held-out split, seven of ten conversations.** The other three carried the
   tuning and are reported separately. Figures on the whole ten-conversation
   suite do not exist for this engine.
3. **Answerer models differ from the published setups.** Engraphy uses
   `claude-opus-4-8` to read and `claude-sonnet-5` to judge; Mem0's 66.88 used
   GPT-4o-mini and is a mean of 10 runs.
4. **The matched-convention figure is bounded** by its validity controls, section
   3a: 91.4% raw, 90.0% defensible, 81.2% floor.
5. **Zep's figure is disputed.** Mem0 published 65.99 for Zep; Zep self-reports
   75.14 after what it describes as three implementation errors in that
   evaluation. The higher figure is used as the comparator throughout.
6. **Mem0 Platform's 92.5%** is published in the harness this convention is
   vendored from, with its retrieval budget stated, so it is a comparator: level,
   section 3. Its answerer and judge models are not stated. Other vendor figures
   in the 90s found by search are self-reported with no stated methodology and are
   not used.
7. **Multi-hop under the strict convention is a genuine deficit**, and the
   convention gap there is a grading-rule effect, explained in section 3.
8. **Engraphy competes under the matched convention with at most 25 memories in
   context** where the convention permits 200.
9. **The Claude CLI route may pass account context to the model.** Found
   2026-10-15 on LongMemEval: the model saw the signed-in operator's identity. It
   has not been tested whether user-level settings also reach the extractor,
   reader and judge. If they do, the effect applies to every run alike. See
   `analysis/2026-10-15-longmemeval-oracle-diagnosis.md`, last section.
