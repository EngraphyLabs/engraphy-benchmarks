# What Engraphy can claim, benchmark by benchmark

Date: 2026-10-16. The consolidated outcome of the benchmark expansion that began
2026-10-15: what was run, what each result supports, and what it does not. Every
figure recomputes from files committed in this repository, with the command given
beside it.

## The short answer

**Engraphy can credibly claim to lead outright on no benchmark.** On LoCoMo it is
ahead of every figure in the Mem0 paper and level with Mem0 Platform's current
figure in the same harness. On LongMemEval, measured in the oracle setting only, it
is behind the paper's own raw-read baseline. No LongMemEval-S figure exists, and
that is the setting the competitors report.

| benchmark | Engraphy | standing | claim it supports |
|---|---|---|---|
| LoCoMo, like-for-like | 91.4% raw, **90.0% defensible**, two runs | ahead of Mem0, Mem0-graph and Zep as published in the Mem0 paper; level with Mem0 Platform's 91.8% (top-50); 0.7 to 1.5 points below its 92.5% (top-200) | "among the leading memory systems on LoCoMo" |
| LoCoMo, strict | 75.4%, two runs | ahead of the Mem0-paper figures; level with Zep's self-reported 75.14 | Engraphy's own conservative figure |
| LongMemEval, oracle | 73.3% (own reader), 82.2% (official template), two runs, 180 questions | behind gpt-4o reading the raw evidence, 87.0% | a scoped measurement, not a ranking |
| LongMemEval-S | none | not measured | none |

## 1. LoCoMo

Source runs: `results/locomo/locomo-settle-a` and `-b`, the seven held-out
conversations, engine `aa7daa2`.

    python scripts/consolidate.py results/locomo/locomo-settle-a results/locomo/locomo-settle-b

| | mean of two runs | range |
|---|---|---|
| like-for-like, raw | 91.4% | 91.0 to 91.8 |
| like-for-like, **defensible** | **90.0%** | 89.6 to 90.4 |
| like-for-like, floor | 81.2% | 81.1 to 81.2 |
| strict, excluding adversarial | 75.4% | 74.8 to 76.0 |
| adversarial, declined correctly | 90.3% | 89.9 to 90.7 |

**What it supports:**

- **The hardened figure.** The confabulation controls were rerun on both runs this
  week: 2,104 strict re-grades and 120 mismatched answers. They bound the raw
  figure at 90.0% defensible and 81.2% floor. The adjustment is 1.4 points.
- **The Mem0 paper's figures.** Ahead of Mem0, Mem0-graph and Zep (66.88, 68.44,
  65.99) in every category, raw and defensible. Ahead of Zep's self-reported 75.14
  as well.
- **Mem0 Platform's current same-harness figure, raw against raw.**
  - Level with its 91.8% at top-50.
  - 0.7 to 1.5 points below its 92.5% at top-200.
  - Engraphy does this with at most 25 memories in context, on 7 of the 10
    conversations.
  - By category: ahead on single-hop, level on multi-hop and temporal, behind on
    open-domain.

**A third run, as corroboration.** Run C (`results/locomo/locomo-settle-c`) finished
after the window closed, so it is reported apart from the headline, as fixed
before it began. It scored 75.6% strict, 91.9% raw and 91.1% defensible. A
three-run mean is a supplement only: 91.6% raw (sd 0.5), 90.4% defensible.

## 2. LongMemEval, oracle setting

Source runs: `results/longmemeval/lme-oracle-n30-a` and `-b`.
- 180 questions from Mem0's public sampler (`per_type=30, seed=42`), 30 of each
  of the six types.
- Engine configuration unchanged from LoCoMo, never tuned on LongMemEval.
- Official judge prompts vendored from `xiaowu0162/LongMemEval` at `9e0b455`,
  graded by Claude Sonnet 5.

Reproduce end to end: `config/longmemeval-oracle.json`. Recompute:

    python scripts/consolidate_longmemeval.py results/longmemeval/lme-oracle-n30-a \
                                              results/longmemeval/lme-oracle-n30-b

| type | Engraphy's reader, official judge | official answer template, official judge |
|---|---|---|
| **overall** | **73.3%** (73.3, 73.3), 95% [69, 78] | **82.2%** (82.2, 82.2), 95% [78, 86] |
| knowledge-update | 96.7% | 93.3% |
| temporal reasoning | 90.0% | 93.3% |
| multi-session | 93.3% | 93.3% |
| single-session-user | 90.0% | 96.7% |
| single-session-preference | 43.3% | 81.7% |
| single-session-assistant | 26.7% | 35.0% |
| abstention | 20/20 | 17/20 |

Strict, preference excluded: 81.0%. The N = 15 pair, run first, gave 66.7% and
75.0% on 90 questions.

### The oracle caveats, which travel with every LongMemEval figure

1. **Oracle is not S.** Each question comes with only its evidence sessions, about
   two. The figure measures whether extraction keeps the facts and how well they are
   read. It does not measure finding them among about 48 distracting sessions, which
   is LongMemEval-S, the setting Mem0 (94.4%), Zep (71.2%), Supermemory, Mastra and
   Hindsight report. No comparison with those figures is valid.
2. **Memory pipeline against raw read.** The paper's oracle baseline, gpt-4o at
   87.0% (92.4% with chain-of-note), reads the raw transcript. Engraphy reads its
   own extracted memories, so anything not extracted is gone.
3. **Subset, judge and data version.** The figures cover 180 of 500 questions,
   graded by Claude Sonnet 5 rather than gpt-4o, on the cleaned 2025 release.

### Why it scores where it does

From the diagnosis (`analysis/2026-10-15-longmemeval-oracle-diagnosis.md`), run A's 30
failures under Engraphy's reader, adjudicated by hand:

| stage | failures |
|---|---|
| extraction | 13 |
| retrieval | 0 |
| reading | 15 |
| grading | 2 |

- **Extraction.** The losses are mostly questions asking what the *assistant* said,
  which the extractor does not keep by design.
- **Reading.** The losses are mostly the grounded reader declining with the answer
  present, or giving a one-line answer to a request for a recommendation.
- **The ceiling.** With perfect reading the stores would allow 85.6% to 86.7%,
  beside gpt-4o's raw-read 87.0.
- **Without assistant recall.** The official template scores 91.7% on the other
  five types.

## 3. What was deliberately not done

The two levers the diagnosis identifies were **not applied**, so every figure above
measures one unchanged pipeline:

1. widening extraction to keep what the assistant recommended or stated;
2. letting the reader answer from the retrieved facts more readily, and more fully
   on recommendation questions.

Both are product decisions for the owner. If taken, each would be written against
the 90 diagnosed questions, which now count as seen. It would be decided by a
pre-registered rule and confirmed on LongMemEval questions outside that set, while
holding LoCoMo's 90.3% adversarial declines.

## 4. Open items found along the way

These are harness and route defects, not engine behaviour. None was fixed during the
measurement, so that every run measured the same thing.

- **Command-line limit on Windows.** On the Claude CLI route, an extraction window
  larger than about 32 KB fails at launch and is recorded as empty. It touches 13 of
  the 500 oracle questions, and LoCoMo never.
- **Account context reaches the model.** The CLI route showed the signed-in
  operator's identity to the model, which named LongMemEval's anonymous user after
  the operator. It is scrubbed from every committed file. It is untested whether
  user-level settings also reach the extractor, reader and judge; if they do, it
  applies to every run alike.
- **Closed-schema refusals.** The write path refuses a whole memory over one
  undeclared attribute: 8 memories in one oracle run.

## 5. What would change the verdict

- **A LongMemEval-S figure, on the per-token route.** Pilot first: Mem0's sampler
  at `per_type=5`, about 1,430 sessions and 4.6M extractor output tokens. Then all
  500 questions, about 23,850 sessions and 76M output tokens, twice. Fix the
  command-line limit first, and decide on assistant-turn extraction first, or S
  will re-measure both.
- **On LoCoMo**, a figure clear of Mem0 Platform's 92.5% beyond the run-to-run
  spread. That would support "leading on LoCoMo"; the current one does not.

## Wording

`WEBSITE-FIGURES.md` carries the approved wording, what stays level, and what is
off-limits for both benchmarks. Two points matter most:

- **"The leading memory system", with or without "on LoCoMo", is not approved.**
- **Every LongMemEval figure names the oracle setting and both conventions.**

`PUBLISH.md` records the LoCoMo CC BY-NC position and the attribution line.
