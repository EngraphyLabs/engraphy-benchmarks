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
still fails closed. ~/.usage-watchdog/config.json sets weekly_ceiling 80, approved by
Devon. One N = 30 LongMemEval oracle re-ingest with its replays costs about 12 points
of weekly usage.

## Engraphy: LongMemEval redaction misses a name after an escaped newline (fixed)

`\b` does not separate `\n` from a following name in JSON text, so four committed
official-reader files carried the operator's first name on the public branch
analysis/benchmark-expansion. scripts/redact_longmemeval.py now also matches after a
JSON escape; the files were re-scrubbed in commit 5c20e76. The name remains in earlier
git history of EngraphyLabs/engraphy-benchmarks; rewriting it is Devon's decision.
