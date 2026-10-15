# Benchmark expansion: which benchmarks to run beyond LoCoMo, and what this window can carry

Date: 2026-10-15. Written before any LongMemEval call was made, so the decisions in
sections 4 and 5 are pre-registered.

The aim is a second benchmark that the competitors themselves report, so that a claim
about Engraphy rests on more than LoCoMo. This document surveys the candidates, prices
each one against what one LoCoMo run measurably cost, ranks them, and fixes the rules
for the run before it happens.

## 1. What the competitors report

| benchmark | reported by | published figures (self-reported unless noted) | licence |
|---|---|---|---|
| **LoCoMo** | Mem0, Zep, Letta, MemOS, Memobase, MIRIX, Hindsight, EverMemOS, A-Mem, LangMem | see the LoCoMo report | CC BY-NC 4.0 |
| **LongMemEval-S** (ICLR 2025) | Zep, Mem0, Supermemory, Mastra, Hindsight, MemOS, EverMemOS, Emergence | Zep 71.2 (gpt-4o, arXiv 2501.13956, pre-cleaning); Mem0 Platform 94.4 (memory-benchmarks README); Supermemory 81.6 and later 85.2 (gemini-3-pro); Mastra 84.23 (gpt-4o) to 94.87 (gpt-5-mini); Hindsight 91.4 (arXiv 2512.12818); MemOS 77.8 (gpt-4o-mini); full-context gpt-4o 60.2 (Zep paper) | MIT |
| LongMemEval oracle | the LongMemEval paper only | gpt-4o reading only the evidence sessions: 87.0, 92.4 with chain-of-note | MIT |
| LongMemEval-M | nobody in the set above | | MIT |
| DMR (MemGPT, on MSC) | MemGPT, Zep | Zep 94.8 against full context 94.4 (gpt-4-turbo); Zep 98.2 against full context 98.0 (gpt-4o-mini), arXiv 2501.13956 | derived set Apache-2.0 on HF; the underlying MSC data licence is not stated anywhere found |
| BEAM (ICLR 2026) | Mem0 (1M, 10M), Hindsight's AMB | Mem0 70.1% pass at 1M; metrics are not on one scale across reporters | CC BY-SA 4.0 |
| PersonaMem | MemOS, Hindsight's AMB | MemOS 61.17, Zep 57.83, Mem0 43.12 (MemOS results repo) | MIT |
| PerLTQA | no competitor found | | CC BY-NC 4.0, "non-commercial research use only" |
| MemoryAgentBench, MemBench, LongMemEval-V2 | academic only | | MIT, MIT, unchecked |
| Letta Leaderboard, Context-Bench | Letta | these rank models running inside Letta, not memory systems | |
| Mem0's suite (`mem0ai/memory-benchmarks`) | Mem0 | it is a harness over LoCoMo, LongMemEval-S and BEAM, not a dataset of its own | Apache-2.0 |

Notes that change how any of these can be used:

- **LongMemEval is the de facto second standard.** Eight vendors report it. Their
  figures cluster at 84 to 97 with different answerers, judges and dataset versions:
  the cleaned files of 2025-09 replaced the originals, so Zep's 71.2 and Supermemory's
  first 81.6 were measured on a different file.
- **Mem0's LongMemEval prompts are fitted to the test set.** The answer prompt vendored
  at `mem0ai/memory-benchmarks@4b61c5d` carries rules that only make sense for specific
  LongMemEval questions ("chandelier counts as jewelry", "scratch grains count as new
  layer feed", starting a diorama counts as working on a model kit), and its judge
  prompt carries the same kind ("recent is upto 6 years ago"). A figure produced under
  those prompts is not a held-out figure, so this repository does not use them for any
  figure, and Mem0's 94.4 is cited, where it is cited at all, with that stated.
- **DMR is saturated.** Zep's own paper shows full-context reading matching Zep within
  half a point, and criticises the benchmark.
- **Licences.** None of the candidates restricts reporting a measured score.
  PerLTQA is non-commercial research only, like LoCoMo. BEAM is share-alike, which
  binds redistribution of the data, not a score. LongMemEval and PersonaMem are MIT.

## 2. What a run costs, measured

The yardstick is LoCoMo run B (`locomo-settle-b`, 2026-10-09), the configuration that
would be run here unchanged:

| | |
|---|---|
| ingest, 7 conversations | 209 sessions, 4,585 turns, 563,044 characters of dialogue |
| ingest output | **714,114 extractor output tokens** (`ingest.jsonl`) |
| ingest time | 10,131 s of sequential extraction, 48.5 s per session |
| reader | 1,486 calls, 426,790 output tokens |
| whole run, both conventions | about 7.5 hours of wall time across one session cap |

Ingest is sequential within a haystack by design (a knowledge update is only answerable
if the store saw the old fact first), and the output tokens of an Opus extractor are
what drains a subscription window. Against that yardstick:

| candidate | sessions to extract | characters to extract | in LoCoMo-run ingests |
|---|---|---|---|
| LongMemEval oracle, all 500 | 948 | 13.2M | 4.5x by sessions, 23x by characters |
| LongMemEval-S, all 500 | 23,850 (19,195 unique) | 244.6M | 114x by sessions, 434x by characters |
| LongMemEval-S, **one** question | about 48 | about 489,000 | about 0.9x by characters |
| BEAM-100K | 20 conversations of about 100k tokens | about 8M | about 14x by characters |
| DMR | about 2,500 short sessions | not measured | about 12x by sessions |
| PersonaMem-32K | not verified | | |

Measured from the files: `longmemeval_oracle.json` (sha256 `821a2034...620c`) and
`longmemeval_s_cleaned.json` (sha256 `d6f21ea9...a442`), Hugging Face
`xiaowu0162/longmemeval-cleaned` at revision
`98d7416c24c778c2fee6e6f3006e7a073259d48f`.

**What follows.** This window is about 12 hours, and a whole LoCoMo run used about 7.5
of a comparable window. No benchmark in the table can be run in full, twice, with
Opus extraction on the subscription route in this window. LongMemEval-S, the one the
competitors report, needs roughly a hundred LoCoMo runs' worth of extraction. That is
a route question, not a window question: the OpenAI-compatible route (engine PR #8)
with a per-token extractor is how a full LongMemEval-S figure gets made, and it is
priced in section 6.

## 3. Ranking

Credibility to the claim times feasibility in this window, cheap and credible first.

1. **LoCoMo hardening (the confabulation controls on runs A and B).** It is the
   cheapest work available, judge calls only, about 2,300 of them, no ingest. It turns
   the published 91.4% from a raw figure into a bounded one. Running now.
2. **LongMemEval, oracle setting, on a pre-registered stratified subset, two runs.**
   It is the benchmark the competitors report, it has official judge prompts, and its
   licence is MIT. The oracle setting is the only variant whose extraction fits. Its
   limit is stated in section 5.
3. **LongMemEval-S.** The credible one, and unaffordable here. Priced for later.
4. **BEAM-100K.** Emerging, reported by Mem0 and Hindsight, about 14 LoCoMo ingests.
   Later.
5. **PersonaMem-32K.** Multiple choice, so no judge. The context count needs verifying.
   Later.
6. **DMR.** Saturated, two reporters, unclear underlying licence. Not worth a run.
7. **PerLTQA, MemoryAgentBench, MemBench, LongMemEval-M and -V2, the Letta boards.**
   No competitor reports them, or they do not fit, or they rank models rather than
   memory systems.

## 4. Pre-registration: LongMemEval in this window

**Configuration, unchanged from LoCoMo.** Engine at the commit both LoCoMo runs
measured, `aa7daa2`: `llm_wide` extraction, the `conversational` pack, hybrid search at
width 25, `always_distinct`, reader `claude-opus-4-8`, judge `claude-sonnet-5`. The
harness work below changes how the data is fed in and graded, never the engine.
`git diff aa7daa2 -- engraphy/` against the measured harness commit is recorded in the
run's provenance and must be empty.

**Fully out of sample.** No lever of the engine was ever fitted to LongMemEval. Nothing
in this window is tuned on it either: the configuration above is fixed now, before
the first call, and is not revisited after any result is seen.

**Harness changes, decided before any result.**

- The loader is registered, and each question's sessions are **sorted by their
  `haystack_dates`** before ingest: 34 oracle questions and 211 S questions list their
  sessions out of order in the file, and knowledge-update questions depend on order.
- The question date reaches the reader as `Current date: <question_date>`, in every
  convention. 133 of the 500 questions are temporal.
- Haystacks ingest concurrently with each other (each is its own scope), while each
  haystack's own sessions stay strictly sequential.

**Question set.** Mem0's public sampler, `sample_questions_stratified(per_type=N,
seed=42)` from `mem0ai/memory-benchmarks@4b61c5d`, reproduced exactly, so the subset
is not one this repository chose. N is set by the plumbing measurement below and
recorded before run 1 starts, by this rule: the largest N in {5, 10, 15, 20, 30} for
which two complete runs, projected from the measured extractor output per session,
fit in the window left with a 1.5-hour margin. If N would be below 10, LongMemEval is
reported as a plumbing result only, with no figure.

**Plumbing check.** Three named questions outside the sampled subset, one
knowledge-update, one temporal and one abstention, run end to end to measure cost per
session and to prove the wiring. They are never part of a reported figure.

**Conventions, all from one reader pass where possible.**

- **Official.** The judge prompts of `xiaowu0162/LongMemEval` at
  `9e0b455f4ef0e2ab8f2e582289761153549043fc`, `src/evaluation/evaluate_qa.py`, vendored
  byte for byte with their hashes: a prompt per question type, the abstention prompt
  for `_abs` questions, one pass, `yes` anywhere in the reply counts, as upstream.
  Applied to Engraphy's own reader answers, which is how the vendors above report
  (their own answerer, the official judge). The official protocol uses gpt-4o as
  judge; this run uses Claude Sonnet 5, stated beside every figure.
- **Official reader.** The same official judge over answers from the official
  generation prompt for extracted facts (`run_generation.py`, the facts template with
  step-by-step answering), over the same retrieved memories. This is the analogue of
  LoCoMo's matched convention.
- **Strict.** Engraphy's own reader and its strict judge, best of 3, with abstention
  questions graded by the decline rule. `single-session-preference` gold is a rubric
  the strict judge is not built for, so the strict figure is reported without that
  category and says so.

**Runs.** Run 1 completes end to end, both conventions, before run 2 ingests anything,
so a weekly cap leaves one whole result rather than two halves. A figure is quoted
only with two runs behind it.

### 4a. The plumbing check, and N (recorded 2026-10-15 21:25 AWST, before run 1)

Run `lme-smoke-20261015` on harness `cf74783` (dataset-path fix `9883405` after
it), questions `07741c45`, `0bb5a684` and `031748ae_abs`, six sessions:

| | |
|---|---|
| extractor output | 4,985, 6,036 and 8,130 tokens: 6,384 per question, 3,192 per session (LoCoMo run B: 3,417) |
| time | 69, 82 and 105 s per question, about 43 s per session, three questions side by side |
| wiring | all three conventions graded the same three answers consistently; the official judge replies with a bare yes or no, as upstream expects |

**The rule gives N = 15.** A whole oracle run is 948 sessions, about 3.0M extractor
output tokens, 4.2 times run B's whole ingest, and two of them do not fit. The
budget left for LongMemEval after the LoCoMo controls is estimated at about 2.4
run-B ingests of usage: about 2.3 five-hour windows remain, run B used about 1.5
windows for one ingest plus its answering and grading, and the controls and this
session take a share. Per question, extraction plus answering costs about 6,800
output tokens. N = 20 (120 questions) needs 2.3 ingests for two runs, which does
not fit with the 1.5-hour margin; N = 15 (90 questions, 138 sessions) needs 1.7 and
does. The 90 question ids are those `bench.longmemeval.sample --per-type 15`
prints: 15 of each type, 5 of them abstention. None is a plumbing question.

### 4b. Leftover capacity (recorded 2026-10-15 21:50 AWST, while run A was ingesting and before any LongMemEval answer existed)

If both N = 15 runs complete with capacity and time left, the queue runs two
further independent runs at **N = 30** from the same sampler: 180 questions, 282
sessions, 56 of them shared with the N = 15 set (the sampler draws afresh at each
size). Then:

- the N = 15 pair is reported whatever the N = 30 pair shows;
- if the N = 30 pair completes, it becomes the headline LongMemEval figure, because
  it is the larger sample, and this is decided now rather than after either result
  is seen;
- if only one N = 30 run completes, it is reported as a single run and the headline
  stays the N = 15 pair.

No configuration changes between any of these runs.

## 5. What a LongMemEval oracle figure can and cannot say

The oracle setting hands the system only the sessions that contain the evidence, about
two per question. Retrieval over two sessions is close to trivial, so the setting
measures whether extraction kept the facts and whether the reader reasons over them
correctly. It does **not** measure finding a fact among about 48 sessions of
distraction, which is what LongMemEval-S measures and what the competitors report.

So an oracle figure is never placed in a table against a competitor's LongMemEval-S
figure. Its only published comparator is the LongMemEval paper's own oracle row
(gpt-4o reading the raw evidence sessions: 87.0, 92.4 with chain-of-note), and even
that compares Engraphy's extracted memory with raw transcript, under a different judge.
It can support a sentence like "on LongMemEval's oracle setting, Engraphy's extracted
memory answered X% of a stratified subset", never "leads on LongMemEval".

## 6. What a full LongMemEval-S figure would take

About 23,850 session extractions and about 244.6M characters of input. On the
subscription route at run B's measured 48.5 s per session that is 320 hours of
sequential extraction; at its 3,417 output tokens per session it is about 81M extractor
output tokens. On a per-token route it is a budget line: priced at the extractor's
per-token rate, plus 500 reader calls and 2,000 judge calls. Engine PR #8 carries that
route. Until it is used, Engraphy has no LongMemEval-S figure and claims none.

## Sources

- LongMemEval: arXiv 2410.10813; https://github.com/xiaowu0162/LongMemEval at `9e0b455`;
  https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned
- Zep: arXiv 2501.13956
- Mem0 harness and figures: https://github.com/mem0ai/memory-benchmarks at `4b61c5d`
- Supermemory: https://supermemory.ai/research ; Mastra: https://mastra.ai/research/observational-memory
- Hindsight: arXiv 2512.12818 ; MemOS: Hugging Face `MemTensor/MemOS_eval_result`
- BEAM: arXiv 2510.27246, Hugging Face `Mohammadta/BEAM`
- PersonaMem: arXiv 2504.14225 ; PerLTQA: arXiv 2402.16288 ; DMR: MemGPT, Hugging Face `MemGPT/MSC-Self-Instruct`
