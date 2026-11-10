# Memory nodes staged for Engraphy, 2026-11-10

The Engraphy MCP server was not connected in this session, so these are staged
here for `mcp__engraphy__write` into scope `proj-engraphy`. One node per heading.

## Engraphy: LongMemEval oracle levers measured; extraction fix works, abstention blocks shipping

Pre-registered in analysis/2026-10-27-benchmark-slate-plan.md (31a728e), run
2026-11-10, two runs each, official judge, harness 9d05779 (engine tree = aa7daa2).
Lever (a), extractor llm_wide_asst keeping assistant statements: single-session-assistant
out-of-sample 25.0 -> 87.5 (p = 0.0001). Lever (b), facts reader: no category lifts
out-of-sample (preference +20, p = 0.13). (a)+(b): out-of-sample overall 78.6 -> 88.3
(p = 0.034). Abstention wrongly answered of 20: (a) 4, (b) 2, (a)+(b) 6; the bar is 2.
Cost of (a): store +49%, temporal reasoning about -10 points (user events crowded out of
k=25), extractor output +40%. Nothing shipped; defaults stay llm_wide and grounded.
A shippable (a) needs the reader to separate assistant-attributed memories from user
facts and a revisited envelope depth, each a new pre-registered lever. Analysis:
engraphy-benchmarks analysis/2026-10-27-oracle-fixes-experiment.md, commit c2d572e.

## Engraphy: the operator's CLAUDE.md makes the LongMemEval official judge more lenient

Control on 2026-11-10, baseline lme-oracle-n30 answers. Re-judging identical answers in
the same condition: +0.3 points, flips both ways (judge noise is small and symmetric).
Re-judging with settings withheld (--setting-sources "", env
ENGRAPHY_BENCH_CLI_ISOLATE_SETTINGS=1): -3.3 points, out-of-sample 0 better / 7 worse,
p = 0.016. Reader and judge both isolated: -5.0 (about 3.3 judge, 1.7 reader). The
committed LongMemEval oracle figures, and likely the LoCoMo ones, were graded with the
operator's settings in context. Recommended: an isolated judge-only re-grade of saved
answers before those figures are quoted further. LongMemEval-S and BEAM run isolated.

## Engraphy: the benchmark spend gate governs on the weekly window, ceiling 80%

From 2026-11-10 the OAuth usage endpoint reports five_hour: null and no session row.
spend_gate.py (engraphy-benchmarks/ops/usage-watchdog, untracked) treats an absent
5-hour window as not reported and lets the weekly ceilings govern; no windows at all
still fails closed. ~/.usage-watchdog/config.json sets weekly_ceiling 80, approved by the
owner. One N = 30 LongMemEval oracle re-ingest with its replays costs about 12 points
of weekly usage.

## Engraphy: LongMemEval redaction misses a name after an escaped newline (fixed)

`\b` does not separate `\n` from a following name in JSON text, so four committed
official-reader files carried the operator's first name on the public branch
analysis/benchmark-expansion. scripts/redact_longmemeval.py now also matches after a
JSON escape; the files were re-scrubbed in commit 5c20e76. The name remains in earlier
git history of EngraphyLabs/engraphy-benchmarks; rewriting it is the owner's decision.

## Engraphy: LongMemEval-S small batch measured; full S costs about $1,330 per run per-token

2026-11-10, per_type=1 (6 questions, 287 sessions), two runs, settings withheld, prompt
budget 20,000 chars, harness 391af84. Official judge 3/6 and 2/6; the difference is one
equivalent temporal answer the judge rejected, so substantively 3/6 both runs. Misses
are the oracle failure classes: assistant-said fact not stored, preference not
personalised, multi-session count incomplete. Measured ~1,300 extractor output tokens
per S session (half the oracle rate) and ~2 weekly points per 6 questions. Full S per
run: ~31M output and ~110M input (estimated) tokens, ~$1,330 per-token, ~$670 Batch,
~125 to 210 weekly points on the subscription. The batch found and fixed three harness
flaws: repeated sessions and empty turns in the S file (23c68bb), the splitter dropping
all prior titles (4a6ae6b), and CLI refusals misread as a quota stop (391af84).

## Engraphy: the Claude CLI carries the account email into every call; it blocks BEAM

Verified 2026-11-10 with a direct probe: even with --setting-sources "" and a custom
system prompt, the CLI context includes the signed-in account's email. On BEAM-100K
(conversations 1 and 2, run beam100k-c2, harness 47f6e87 on bench/beam-20261110) the
extractor named the anonymous user after the account in 269 of 342 memories, and an
abstention answer stated that identity. The BEAM run stays uncommitted until the owner
chooses a fix: a route that does not carry the account, or an explicit anonymous-user
instruction recorded as a prompt change. Second BEAM blocker: the reader's bare
INSUFFICIENT token scores 0 under BEAM's rubric judge (3 of 4 abstention answers);
rendering it as a fixed decline sentence is a grading convention left to the owner. The
batch scored 51.3% (harness's unweighted mean). Full BEAM-100K is cheap: ~10 weekly
points or ~$65 per run.
