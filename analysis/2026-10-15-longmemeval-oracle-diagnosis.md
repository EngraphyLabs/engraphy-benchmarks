# LongMemEval oracle, run A: where the answers were lost

Date: 2026-10-15. A diagnosis of one run on a 90-question subset, made from that
run's saved data with no new model call. It explains a number; it does not publish
one. A LongMemEval figure is quoted only with two runs behind it, under the rules
in `analysis/2026-10-15-benchmark-expansion-plan.md`.

- Run: `lme-oracle-a`, harness `9883405` (`EngraphyLabs/engraphy`, branch
  `bench/longmemeval-20261015`), engine code identical to `aa7daa2`.
- Configuration: the LoCoMo-settled engine unchanged, `llm_wide-conversational`,
  hybrid search at width 25, reader `claude-opus-4-8`, judge `claude-sonnet-5`.
- Questions: Mem0's public sampler, `per_type=15, seed=42`, 90 questions, 15 of each
  type, 5 of them abstention.
- Artifacts: `results/longmemeval/lme-oracle-a/`, with the diagnosis in
  `diagnosis/diagnosis.jsonl` (computed) and `diagnosis/adjudication.jsonl` (by hand).

## 1. What the oracle setting is, and what this harness does with it

LongMemEval gives every question its own chat history. In the **oracle** setting
that history is cut down to the **evidence sessions only**, the one to six sessions
that contain the answer, about two per question. The distracting sessions that make
up the S and M settings are removed.

The paper's oracle baseline gives those sessions, as raw transcript, straight to
`gpt-4o`, which reads them in full and answers.

This harness runs Engraphy's memory pipeline over them instead:

1. **Ingest.** Each evidence session, in date order, goes through the LLM extractor,
   which writes typed memories (facts, events, preferences and so on) through the
   engine's write path, with de-duplication and schema validation.
2. **Retrieve.** At question time, the engine's hybrid search returns up to 25 of
   those memories.
3. **Read.** A reader answers from the returned memories only, never from the
   transcript.

So the comparison with the paper is a **memory pipeline against a raw read** of the
same sessions. Anything the extractor did not keep is gone for good, and anything
it kept is seen only in the form it was kept in. The oracle setting removes the
retrieval problem almost entirely: these stores hold a median of 9 memories and at
most 27, against a 25-result search. It therefore measures mainly **extraction**
and **reading**.

## 2. The result being explained

| convention | run A | run B |
|---|---|---|
| official judge, Engraphy's reader | 66.7% (60/90), 95% [56, 76] | 66.7% (60/90); 25 of the 30 failures are the same questions |
| official judge, official answer template | 77.8% (70/90), 95% [68, 85] | 72.2% (65/90) |
| strict, preference excluded | 74.7% (56/75) | 74.7% (56/75) |

Across both runs: 66.7% (range 66.7 to 66.7), 75.0% (range 72.2 to 77.8) and
74.7% (range 74.7 to 74.7). Single-session-assistant is 23.3% and preference 36.7%
under Engraphy's reader in both runs together. The weakness reproduces; it is not
one run's noise. The stage analysis below is run A's; run B's computed stages and
its 8 empty stores (6 of them the same questions as run A's) do not contradict it.

Per type, run A, official judge with Engraphy's reader: single-session-user 80.0%,
**single-session-assistant 20.0%**, **single-session-preference 40.0%**,
multi-session 73.3%, knowledge-update 93.3%, temporal reasoning 93.3%, abstention
5 of 5.

### The N = 30 pair, the pre-registered headline

Two further runs on Mem0's sampler at `per_type=30` (180 questions, 56 shared with
the N = 15 set) landed after this diagnosis was written. They confirm it at twice
the size:

| convention | N = 30 run A | N = 30 run B |
|---|---|---|
| official judge, official answer template | 82.2% | 82.2% |
| official judge, Engraphy's reader | 73.3% | 73.3% |
| strict, preference excluded | 80.7% | 81.3% |

Single-session-assistant stays at 27% to 35% across conventions. Leaving it out,
the official template scores 91.7% (275/300).

## 3. Method

The stage a failure belongs to is decided by where the gold answer last existed:

- **extraction**: the gold is not in the question's store at all;
- **retrieval**: it is in the store but not in the 25 memories the reader saw;
- **reading**: it was in front of the reader, who declined or answered wrong;
- **grading**: the answer is right in substance and the judge said no.

**Computed, model-free:** `bench/longmemeval/diagnose.py` on the harness branch, at `5a9a363`.
It reads every active memory in each question's scope straight from the database,
with a plain SELECT that moves no recall statistic. It reads the envelope the reader
saw from the run's saved `envelopes.jsonl`. It applies the harness's own
`gold_support` heuristic to both, the same one LoCoMo's failure attribution uses:
does the text hold at least half of the gold answer's content words.

**Adjudicated by hand:** the heuristic abstains on numeric golds, preference
rubrics and abstention questions, and it can be fooled ("mindful" inside
"mindfulness"). So every one of the 33 questions that failed under either official
convention was read against its store and envelope. Each was given a stage and a
reason, recorded in `adjudication.jsonl` with ids and reason codes, no dataset text.
Where the heuristic made a call it agreed with the hand reading in all but the one
false positive noted. All 33 hand labels agree with the recorded verdicts.

## 4. The failure-stage breakdown

### Official judge, Engraphy's reader: 30 failures

| stage | count | share of the 30 | questions |
|---|---|---|---|
| **extraction** | **13** | 43% | 10 single-session-assistant, 2 preference, 1 multi-session |
| retrieval | **0** | 0% | none |
| **reading** | **15** | 50% | 7 preference, 2 single-session-assistant, 3 multi-session, 1 single-session-user, 1 knowledge-update, 1 temporal |
| grading | 2 | 7% | 2 single-session-user |

### Official judge, official answer template: 20 failures

| stage | count | questions |
|---|---|---|
| **extraction** | **12** | 9 single-session-assistant, 2 preference, 1 multi-session |
| retrieval | 0 | |
| reading | 7 | 2 preference, 2 multi-session, 1 knowledge-update, 2 abstention (the template answered instead of declining) |
| grading | 1 | 1 multi-session |

### Which types dominate

Two types carry most of the loss. **single-session-assistant** accounts for 12 of
the 30 failures and is almost all extraction. **single-session-preference** accounts
for 9, almost all reading. Together they are 21 of the 30. The four types about what
the user did, said or changed (single-session-user, multi-session, knowledge-update,
temporal) lose 9 between them.

## 5. What each stage is made of

### Extraction, 13: three different mechanisms

1. **What the assistant said is not kept: 10 questions.** Every
   single-session-assistant question asks the system to recall something the
   *assistant* said earlier ("which brand did you say uses wild rubber"). Engraphy's
   conversational extractor records what people say and do, and largely discards
   the assistant's side. Four of these stores are empty: the extractor ran, read a
   session whose only content was assistant explanation, and stored nothing. This is
   the extraction prompt behaving as designed, on a question type it was not
   designed for. It is 56 of LongMemEval's 500 questions.
2. **A harness transport limit: 2 questions, both preference.** On the Claude
   Code CLI route, an extraction call has to carry its prompt on the command line,
   because structured output is honoured only there. Windows caps a command line at
   about 32 KB. A single LongMemEval session long enough to push the window, plus
   the 6,249-character system prompt and the 1,576-character schema, past that limit
   fails at launch. The harness records a failed window as empty, by design, so the
   question was scored against an empty store. The same two questions failed
   identically in run B. A third question in the subset lost one of its two windows
   the same way, without a visible trace. Across the full oracle set this would
   affect 13 questions, 14 of 948 windows. LoCoMo's sessions are short and never
   reach the limit. This is a harness defect, not an engine property, and it is
   left in place for the rest of this window so that every run measures the same
   pipeline.
3. **One temporal detail lost: 1 question.** The extractor stored that two novels
   were finished, dated by the session rather than by the months the user named.

One single-session-assistant question also lost both of its memories to the write
path, which refused them for carrying an attribute the pack's closed schema does not
allow (`domain` on an opinion). The same refusal removed 8 memories across 6
questions in run A, mostly a `location` attribute on a fact.

### Retrieval, 0

None. With a median of 9 memories in a store and a 25-result search, the reader saw
essentially the whole store for every question. **The oracle setting does not test
retrieval**, which is what LongMemEval-S, with about 48 sessions per question, is for.

### Reading, 15: two habits of the shipped reader

1. **Declining with the answer in front of it: 6.** In each case a retrieved memory
   stated the answer, and the grounded reader returned INSUFFICIENT. The official
   template, which tells the reader to answer from the facts, got 5 of these 6
   right.
2. **One-line answers to requests for advice: 5, all preference.** A preference
   question asks for a personalised suggestion and is graded against a rubric. The
   shipped reader's contract is a single ANSWER line. It used the right stored
   preference, but the judge found it too narrow for the rubric. The official
   template gave the fuller answer and passed 4 of the 5.
3. **Counting, arithmetic, a stale value and a hedge: 4.** One count was wrong
   with every item in context. One answer gave the total instead of the remainder.
   One knowledge-update question had both the old and the new value stored, with no
   supersede link between them, and the reader chose the older one. One hedged
   answer rested on the user's stated choice because the assistant's recommendation
   itself was not stored.

The official template trades the other way on abstention. It answered 2 of the 5
unanswerable questions, where the shipped reader declined all 5.

### Grading, 2

Two correct answers were marked wrong because they omitted part of the gold wording
("University of Melbourne" without "in Australia"). The official judge prompt asks
for the full answer, and that is upstream's rule, kept as is.

## 6. A fair comparison with the paper

The LongMemEval paper (arXiv 2410.10813, Figure 3b) reports `gpt-4o` reading the
raw evidence sessions at **87.0%**, and **92.4%** with chain-of-note, over all 500
questions.

What separates that figure from this one:

| | paper's oracle baseline | this run |
|---|---|---|
| what is read | the raw sessions, assistant turns included | Engraphy's extracted memories, up to 25 |
| questions | all 500 | 90, a seeded stratified subset |
| data | the original release | the cleaned release of 2025-09 |
| judge | `gpt-4o-2024-08-06` | `claude-sonnet-5`, the same prompts |

Read carefully:

- **The extraction ceiling is close to the raw read.** Taking every extraction loss
  as unrecoverable, a perfect reader over these stores would score at most **85.6%**
  (77/90) with Engraphy's reader and **86.7%** (78/90) with the official template.
  That sits beside gpt-4o's 87.0. Three quarters of what the store loses (10 of
  13) is assistant-turn content, which the raw read keeps by construction.
- **The answered figures are below it.** 66.7% and 77.8% sit below 87.0. With
  n = 90 the official-template interval, 68 to 85, does not reach it. Half of the
  failures under Engraphy's reader are reading, not memory.
- **On the questions about the user, the pipeline holds up.** Leaving out
  single-session-assistant, Engraphy's reader scores 76.0% (57/75) and the official
  template 85.3% (64/75). Knowledge-update and temporal reasoning are 93.3% each.

Neither "Engraphy leads on LongMemEval" nor "Engraphy's memory loses most of what it
is told" is supported. What is supported: the pipeline keeps what the user says
about as completely as a raw read does. It does not keep what the assistant said.
Its shipped reader is conservative in ways LongMemEval's grading penalises.

## 7. Is this LoCoMo's extraction ceiling again?

**In size, yes. In cause, mostly not.**

- On LoCoMo, the wider extraction prompt brought store coverage to 85.8% on the seen
  split. The held-out runs retrieve 87.5% of evidence turns at width 25. Here, the
  gold is in the store for 85.6% of questions. The ceilings are about the same height.
- On LoCoMo the losses were facts said in passing by one of two humans, which is
  what the wider prompt was written to catch. Here, 10 of 13 extraction losses are a
  category LoCoMo does not contain: things the *assistant* said. Two of the remaining
  three are a transport defect LoCoMo cannot trigger.

## 8. What would move it

In order of size on this subset. Each is a decision for later, not a change made
here: this window measures the pipeline as it is.

1. **Keep what the assistant recommended or stated, when the user may ask for it
   back.** This is up to 10 of 90 questions here, and 56 of 500 in LongMemEval. It is
   a product decision about the extractor's scope, because Engraphy stores memory
   about people and work, not a transcript. It would be measured like the wider
   prompt was: written on a seen split, decided by a pre-registered rule, confirmed
   out of sample.
2. **A read convention for advice and recall questions.** Let the reader give a
   fuller answer to a recommendation request, and lower its bar for answering when a
   retrieved memory states the fact. That is up to 11 of 90 here. The official
   template shows both effects are real, and also shows the cost: 2 of 5
   unanswerable questions answered. Any change has to hold LoCoMo's 90.3%
   adversarial declines at the same time.
3. **The transport limit.** Split an extraction window by characters as well as by
   turns, or pass the structured-output prompt in a way that is not bounded by the
   command line. That is 2 to 3 of 90 here and 13 of 500 across the oracle set. It is
   a harness fix with no engine change, and it should land before any longer
   LongMemEval setting is run.
4. **Closed-schema attribute refusals.** Drop or quarantine an attribute the pack
   does not declare, instead of losing the whole memory. That is 8 memories in this
   run and one question.
5. **Knowledge-update supersede.** A corrected value stored beside the old one, with
   no supersede link, cost one question.

**Held-out discipline.** These 90 questions have now been read by hand, failure by
failure, so they count as seen. Any of the changes above would be validated on
LongMemEval questions outside this set. The 410 questions not in the N = 15 subset
are the held-out pool.

## 9. Should a larger oracle subset or LongMemEval-S be run?

**The larger oracle subset, already queued, is worth finishing, but it will not
change this diagnosis.** The pre-registered N = 30 pair (180 questions per run, about
0.75M extractor output tokens each) narrows the 95% interval to about
seven points either side and gives every type 30 questions. It is cheap and decided in advance, so
it runs. Its likely effect is to confirm the same two weak types.

**LongMemEval-S, on the per-token route, is the run that matters, and it should
come second, not first.** S is what the competitors report, and it adds the one
stage oracle cannot test, retrieval among about 48 sessions of distraction. But
three of the losses above would carry into S unchanged:

- assistant-turn content;
- the transport limit, which longer S sessions would trigger more often on the CLI
  route (the OpenAI-compatible route of engine PR #8 does not pass prompts on a
  command line);
- the reader conventions.

An S figure measured before those are decided would mostly re-measure them.

Recommended scope:

1. **Decide items 1 to 3 of section 8 first.** Fix the transport limit in any case.
2. **Pilot.** Run Mem0's sampler at `per_type=5`: 30 questions, about 1,430 sessions.
   At the 3,192 extractor output tokens per session measured here, that is about
   4.6M output tokens, plus 30 reader calls and about 150 judge calls, on the
   per-token route. What it answers: how much retrieval loses under distraction,
   before the full cost is spent.
3. **Full S.** All 500 questions: 23,850 sessions, about 76M extractor output
   tokens at the same rate, two runs for a quotable figure. Price it at the route's
   per-token rate before starting.

## Reproducing

    # model-free, against the run's own store and saved envelopes
    git -C ../engraphy checkout bench/longmemeval-20261015
    python -m bench.longmemeval.diagnose --run-dir runs/lme-oracle-a --out <dir>

    # the figures in section 2, from the committed copies
    python scripts/consolidate_longmemeval.py results/longmemeval/lme-oracle-a

The diagnosis needs the run's database, which is not published; the committed
`diagnosis.jsonl` is its output. `adjudication.jsonl` is the hand reading, with a
reason for every label.

## A hygiene finding, separate from accuracy

On the Claude Code CLI route the model can see the signed-in account's identity.
LongMemEval's transcripts call their speaker "user", and the extractor sometimes
named that user after the operator, by name and account email, inside stored
memories. In run A's files, 26 occurrences reached the answers. No figure depends
on it, and LoCoMo's stores, whose speakers are named, show none. Every committed
LongMemEval file has those occurrences replaced with `[operator]`, by
`scripts/redact_longmemeval.py`. Running the extractor with the account's identity
withheld is a harness fix to make before the next run.

## An open confound on the CLI route, all runs

The operator-identity leak shows that the Claude Code CLI passes some of the
signed-in account's context to the model even with `--system-prompt` set. It has
not been tested whether the operator's user-level `CLAUDE.md`, which carries
writing-style rules, also reaches the extractor, reader and judge. If it does, it
applies equally to every arm and run on this route, LoCoMo included, so it cannot
explain a difference between them. It could still shift an absolute figure. The
fix is to run the harness's CLI calls with user settings and account context
withheld, then measure whether any figure moves.
