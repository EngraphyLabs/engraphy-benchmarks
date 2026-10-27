# Benchmark slate: the oracle-fix experiment, a LongMemEval-S sample, a BEAM-100K sample

Date: 2026-10-27. Written before any model call of this slate, so the decisions
below are pre-registered. Order, as approved: the oracle-fix experiment first,
then LongMemEval-S, then BEAM-100K. Each starts with a small batch, reports, and
only then grows.

## 0. Preconditions found on 2026-10-27, before anything ran

1. **The spend gate does not exist.** The approved guardrail reads a spend gate
   at `engraphy-public/ops/usage-watchdog` before every expensive batch. There is
   no such path in any checkout, on any branch of `engraphy-public`, or anywhere in
   the project tree or `~/.claude`. Under the guardrail ("if it says HALT or is
   missing, do not start new expensive work"), **no batch below has started.** The
   preparation is zero-spend: code, configuration, dataset fetches and projections.
2. **Docker's engine is down.** Docker Desktop started, but its `docker-desktop`
   WSL distribution stays stopped, so the benchmark Postgres is unreachable and no
   ingest can run. Restarting WSL would touch other projects' containers, so it is
   left for the owner.
3. **A confound affecting every run so far, measured.** A four-call probe on the
   smallest model, run with the harness's own CLI flags, showed:
   - on the default Claude CLI route, the operator's user-level `CLAUDE.md` reaches
     the model in every call (the model quoted its style rules back);
   - `--setting-sources ""` removes it;
   - the account email reaches the model either way.

   So every extractor, reader and judge call of every LoCoMo and LongMemEval run so
   far carried those instructions. They apply to every arm and run alike, so no
   comparison between runs is affected, but an absolute figure could be. The harness
   now has an opt-in switch, `ENGRAPHY_BENCH_CLI_ISOLATE_SETTINGS=1`, recorded in
   every manifest as `cli_settings_isolated`.

Harness for this slate: `EngraphyLabs/engraphy`, branch
`bench/lme-oracle-fixes-20261027`, commit `9af116e`. `git diff aa7daa2 -- engraphy/`
is empty: no engine change.

## 1. The oracle-fix experiment

**Question.** How much do the two levers the oracle diagnosis named lift
single-session-assistant, preference, and the overall?

**Arms.** Both are opt-in; the shipped defaults `llm_wide` and `grounded` are
unchanged and asserted by test.

| arm | what changes | cost |
|---|---|---|
| baseline | nothing: the committed N = 30 runs, A and B | none, already measured |
| **(b) reader** | stance `facts`: answer from any returned memory that bears on the question, decline only when none relates, and give a short personalised answer to a request for advice | reader and judge calls only: a replay of the saved N = 30 envelopes, no ingest |
| **(a) extraction** | extractor `llm_wide_asst`: `extract-wide.md` plus one general section that keeps what an AI assistant recommended, named, listed or explained, attributed to the assistant | a re-ingest of the N = 30 subset, 282 sessions per run |
| **(a)+(b)** | both | the (a) store, read under `facts` |

**Grading.** Everything is graded by the official LongMemEval judge prompts, the
convention the vendors report under, with the strict judge beside it. Every arm runs
under the same CLI condition as the baseline (settings not isolated), so the only
difference between arms is the lever.

**Held-out discipline.** Both levers were written from the hand diagnosis of the
N = 15 questions, so those 90 are seen. The N = 30 set shares 56 questions with
them. Every result is therefore reported twice:
- on all 180 questions;
- on the **124 not in the N = 15 set**, which are the out-of-sample figure.

The prompt and stance text contain no question, gold answer or test item.

**Order and batches.**
1. Plumbing: 6 questions from outside both subsets, one per type, under each new
   arm. Never scored.
2. Lever (b) on run A's saved envelopes, then run B's: 360 reader calls and the judges.
3. Lever (a): re-ingest the N = 30 subset once (about 0.8M extractor output tokens at
   the measured 2,718 per session). Read it under `grounded` and under `facts`. A
   second (a) run only if the first shows an effect worth confirming.

**Decision rule, fixed now.** A lever "lifts" a category if its two-run mean on the
124 out-of-sample questions exceeds the baseline's in that category, and the paired
per-question comparison is significant at p < 0.05 by an exact McNemar test.
Abstention is tracked separately: lever (b) fails the rule if it answers more than 2
of the 20 unanswerable questions, as the official template did with 3.

**Nothing ships from this.** Whether either lever becomes a default is the owner's
decision after the report, and would also require LoCoMo's adversarial declines to
hold.

## 2. LongMemEval-S, small batch

**Why it matters.** S is the setting the competitors report: about 48 sessions per
question, of which one or a few hold the evidence. It is the first measurement in
this repository where retrieval is tested at scale.

**Harness changes it needs, already made, all opt-in:**
- `--max-prompt-chars 20000`: S windows carry up to 200 prior titles, about 14k
  characters, and would otherwise exceed the Windows command-line limit on the CLI
  route. A window over budget drops its oldest titles first, then splits. Counts of
  both are recorded per question.
- `ENGRAPHY_BENCH_CLI_ISOLATE_SETTINGS=1`, recommended for S as a new measurement;
  see question 2 for the owner below.

**Batches.**
1. Mem0's sampler at `per_type=1`: 6 questions, about 286 sessions, about 0.78M
   extractor output tokens. This proves retrieval at scale, the splitting and the
   cost per question. Two runs.
2. Grow to `per_type=2` (12 questions), then `per_type=5` (30), only as the budget
   allows and only after each batch is reported.

No S figure is a headline. It is a sample that proves the harness.

**What a full S figure costs.**

| | per run | two runs, quotable |
|---|---|---|
| sessions to extract | 23,850 | 47,700 |
| extractor output, at the measured 2,718 tokens per session | about 65M tokens | about 130M |
| extractor input (transcript about 61M, plus prompt, schema and prior titles per window) | about 180M tokens | about 360M |
| **per-token route**, Opus 4.8 at $5 / $25 per million | **about $2,500** | **about $5,100** |
| the same through the Batch API at half price | about $1,250 | about $2,550 |
| reader (Opus 4.8) and judges (Sonnet 5) | under $50 | under $100 |

Window-by-window batching is possible: window k of every haystack forms one batch,
about 48 layers, because each window depends only on earlier windows of its own
haystack.

**On the subscription route.** About 114 LoCoMo held-out ingests per run, against
roughly one to one and a half LoCoMo runs per five-hour window measured this month.
That is dozens of weekly windows, so in practice **a full S figure needs the
per-token route.** Prices are from Anthropic's published rates as cached
2026-10-06; check them before committing spend.

## 3. BEAM-100K, small batch

**The data, measured.** `Mohammadta/BEAM` at revision `3205395e`, CC BY-SA 4.0. The
100K split is 20 conversations:
- about 4.5 sessions and 287 turns each, about 612k characters (153k tokens) per
  conversation;
- 400 probing questions in 10 categories: abstention, contradiction resolution,
  event ordering, information extraction, instruction following, knowledge update,
  multi-session reasoning, preference following, summarization, temporal reasoning.

Each question carries a rubric. `100K.parquet` sha256
`c0519be25907005ba873c927c50877471d550873039d96c041554d0075a78ace`.

**Grading.** BEAM's own evaluation (`mohammadtavakoli78/BEAM` at `b2da22e`, MIT,
`src/evaluation/` and `src/prompts.py`) is rubric-based with an LLM judge, and uses
Kendall tau-b for event ordering. It is vendored by hash like LongMemEval's before
any BEAM batch, and its judge model is stated.

**Batch.** 2 conversations (40 questions) to validate the loader, the very long
sessions, the rubric grading and the cost per conversation. Then stop and report.

**Projection.** At the oracle's measured ratio of extractor output to transcript, one
conversation is about 120k extractor output tokens, so 20 conversations come to
about 2.4M per run.
- **Per-token route:** about $85 per run with Opus 4.8.
- **Subscription:** about 3.4 LoCoMo ingests per run.

Two runs of the whole 100K split are within reach on either route. Comparators: Mem0
reports only 1M and 10M; Hindsight's AMB reports 100K on an unstated metric. So a
BEAM-100K figure will have no like-for-like published comparator, and is reported as
a measurement.

## 4. Open questions for the owner

1. **The spend gate.** Where does it live, or should it be created? Nothing
   expensive starts until it reads go.
2. **Settings isolation.** Should new measurements (S, BEAM) run with the operator's
   `CLAUDE.md` withheld? Recommended: yes. Should the oracle-fix arms run as the
   baseline did, without isolation, so the arms compare cleanly? Recommended: yes.
   Then add one isolated replay of the baseline to size the confound.
3. **Docker.** The engine needs restarting, which touches WSL and other projects'
   containers.
