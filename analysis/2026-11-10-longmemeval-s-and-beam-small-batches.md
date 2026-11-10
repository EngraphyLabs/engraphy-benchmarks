# LongMemEval-S and BEAM-100K: small batches that prove the harness

Plan: `analysis/2026-10-27-benchmark-slate-plan.md` sections 2 and 3. Runs 2026-11-10,
the shipped engine and arm (`llm_wide-conversational/search_only/always_distinct/k25`,
reader stance `grounded`), operator settings withheld from every model call
(`ENGRAPHY_BENCH_CLI_ISOLATE_SETTINGS=1`), extraction prompt budget 20,000 characters.
No figure here is a headline: each batch exists to find flaws in the harness and to
measure cost before anything larger is spent.

## 1. LongMemEval-S, per_type = 1, two runs

Mem0's sampler at `per_type=1, seed=42`: 6 questions, 287 sessions, about 3.0M
characters of transcript. Harness `EngraphyLabs/engraphy` branch
`bench/lme-oracle-fixes-20261027` at `391af84`, `engraphy/` tree identical to `aa7daa2`.
Results: `results/longmemeval/lme-s-pt1-a/` and `-b/`.

| type | run A | run B |
|---|---|---|
| knowledge-update | correct | correct |
| single-session-user | correct | correct |
| temporal-reasoning | correct | judged wrong |
| multi-session | wrong | wrong |
| single-session-preference | wrong | wrong |
| single-session-assistant | wrong | wrong |
| **official judge** | **3 / 6** | **2 / 6** |

The temporal answer is the same fact in both runs; the official judge accepted it in
run A and rejected it in run B. Substantively both runs answer 3 of 6. The three misses
are the same failure classes the oracle diagnosis found, now at S scale:

- single-session-assistant: the answer is a name the assistant gave, which the shipped
  extractor does not keep (lever (a) of the oracle-fix experiment addresses this).
- preference: the evidence reaches the reader, which does not personalise the answer
  (lever (b)).
- multi-session counting: retrieval returns one or two of the three items.

**Ingest, per run:** 287 sessions, 24 windows split to fit the prompt budget, 1 window
declined by the model (`stop_reason: refusal`, recorded as an empty window), 0 other
failed windows; 960 and 970 memories stored; 370k and 379k extractor output tokens,
about 1,300 per session. S sessions are mostly unrelated filler, so the extractor
writes about half of what it writes on oracle sessions.

### Harness changes the batch required

Each is covered by a test; none changes engine behaviour or any committed result.

| commit | change |
|---|---|
| `23c68bb` | The S file places the same session twice, at two dates, in 13 of its 500 haystacks: both placements are ingested, the later under a distinct id. 12 turns in 7 haystacks are empty strings, none of them evidence: they are skipped and counted. Both lists are in each run's corpus notes. |
| `4a6ae6b` | A window whose turns alone exceed the budget is split first, and each piece keeps the newest prior titles that fit. Applies only under `--max-prompt-chars`. |
| `391af84` | A model refusal is a failed call, not a usage cap: the CLI exits 1 with empty stderr for both, and its JSON names `stop_reason: "refusal"`. Each ingest row records `windows_refused` and `windows_failed`. |

### What a full S figure costs, from these measurements

| | per run (500 questions, 23,850 sessions) | two runs |
|---|---|---|
| extractor output, at the measured ~1,300 tokens per session | about 31M tokens | about 62M |
| extractor input, estimated: ~1.08 calls per session at ~4.3k tokens each | about 110M tokens | about 220M |
| **per-token route**, Opus 4.8 at $5 / $25 per million | **about $1,330** | **about $2,700** |
| the same through the Batch API at half price | about $670 | about $1,350 |
| subscription route, at the measured 2 points of weekly usage per 6 questions | about 165 weekly points | about 330 |

The output figure is measured; the input figure is an estimate, because the CLI route
does not report payload input tokens. The plan's earlier projection assumed oracle's
2,718 output tokens per session and is superseded by the measured rate. The weekly
usage reading is whole-percent, so 2 points per batch could be anywhere from about 1.5
to 2.5: the subscription projection spans roughly 125 to 210 points per run. Under the
80% weekly ceiling that is two to three weeks of the plan's allowance per run.

## 2. BEAM-100K, conversations 1 and 2

40 probing questions, 4 per category, over 2 conversations (6 sessions, 388 turns,
about 1.0M characters). Harness `EngraphyLabs/engraphy` branch `bench/beam-20261110`
at `47f6e87`, `engraphy/` tree identical to `aa7daa2`. Graded with BEAM's rubric judge
prompts vendored at `b2da22e`, judge `claude-sonnet-5` in place of upstream's
`gpt-4.1-mini`.

| category | score |
|---|---|
| preference_following | 87.5% |
| instruction_following | 75.0% |
| knowledge_update | 75.0% |
| contradiction_resolution | 56.2% |
| multi_session_reasoning | 50.0% |
| temporal_reasoning | 50.0% |
| summarization | 46.7% |
| information_extraction | 41.7% |
| event_ordering | 30.7% |
| abstention | 0.0% |
| overall, unweighted mean of the ten (the harness's own; upstream reports none) | 51.3% |

**Ingest:** 81 of the windows were split to fit the prompt budget, none refused, none
failed; 342 memories stored; 165k extractor output tokens; about 27 minutes of ingest at
ingest concurrency 2. Weekly usage moved by about 1 point for the whole batch.

This run is kept in the harness checkout and not committed here, for the first finding
below.

### Findings that block a BEAM figure

**The signed-in account's identity enters the store.** The Claude CLI places the
account email in every call's context, including with operator settings withheld
(verified with a direct probe on 2026-11-10). BEAM transcripts almost never name their
user, so the extractor names the user after the account in 269 of 342 memories, and one
abstention answer states that identity as the user's background. LongMemEval-S, whose
sessions carry more user detail, shows no occurrence in either run; the oracle runs
show 21 to 34 per run, redacted in their committed copies. A BEAM figure needs this
closed first, by a model route that does not carry the account into the call, or by an
explicit instruction that the transcript's user is anonymous, recorded as a prompt
change.

**A correct decline scores zero.** The reader's verify contract answers `INSUFFICIENT`
when memory holds nothing relevant. BEAM's rubric judge expects a sentence stating that
the conversation does not contain the information, and grades the bare token as no
response: 3 of the 4 abstention answers are this token. Rendering the token as a fixed
decline sentence before the rubric judge, declared in the pass manifest, would grade
the reader's actual behaviour; it is a grading convention, so it is left for the owner.

**Hedged orderings.** Two event_ordering answers open with "Likely", and the rubric
judge discounts them as speculative. This is the `grounded` stance's hedging, the same
reader behaviour lever (b) of the oracle experiment changes.

**Coverage.** 342 memories for 388 turns of dense technical dialogue is sparse for
information_extraction questions that probe single details; split windows see fewer
neighbouring turns. The per-question failure staging will say whether misses are
extraction or retrieval once the identity issue is closed.

### What a full BEAM-100K figure costs

At the measured rate (165k output tokens and about 1 weekly point for 2 of 20
conversations), all 20 conversations are about 1.65M extractor output tokens and
about 10 weekly points per run on the subscription route, or roughly $65 per run
per-token. BEAM-100K is cheap; the blockers above, not cost, decide when it runs.
