# Memory nodes staged for Engraphy, 2026-10-15

The Engraphy MCP server was not connected in this session, so these are staged
here for `mcp__engraphy__write` into scope `proj-engraphy`. One node per heading.
Search first for the LoCoMo "92.5% not a comparator" node and correct it with
`update` rather than writing beside it.

## Engraphy: LoCoMo like-for-like figure hardened to 90.0% defensible

The confabulation controls were rerun on both held-out runs (locomo-settle-a and
-b) on 2026-10-15: control A, the strict judge on 1,047 and 1,057 accepted answers;
control B, 60 mismatched answers per run. Evidence recall was computed offline from
the saved envelopes. Result: raw 91.4% (91.0 to 91.8), defensible 90.0% (89.6 to
90.4), floor 81.2%. Control B: the matched judge accepted 2 and 3 of 60, the strict
judge 2 and 2. The adjustment is 1.4 points, half the ~3 points the
three-conversation runs suggested. Committed in results/locomo/locomo-settle-{a,b}/reference
with manifests; recompute with scripts/consolidate.py. Branch
analysis/benchmark-expansion of engraphy-benchmarks.

## Engraphy: Mem0 Platform reports 92.5% LoCoMo in the same harness our matched convention uses

Correction to the earlier position that Mem0's 92.5% states no methodology. The
mem0ai/memory-benchmarks README at 4b61c5d, the commit our matched convention is
vendored from, reports Mem0 Platform v3 at 92.5% (top-200) and 91.8% (top-50) on
1,540 questions. Engraphy's 91.4% raw (top-25, seven held-out conversations) is
level with it, not ahead. By category: ahead on single-hop (93.3 vs 91.2), level on
multi-hop and temporal, behind on open-domain (69.3 vs 72.7). Decision: "the leading
memory system on LoCoMo" is not approved; "among the leading memory systems on
LoCoMo", with Mem0 Platform's figure beside it, is. Mem0's answerer and judge models
are not stated; the harness defaults to gpt-5.

## Engraphy: LongMemEval-S is unaffordable on the subscription route; oracle subset measured instead

LongMemEval-S needs about 23,850 session extractions (61M tokens of input), about
114 LoCoMo held-out ingests by session count. It cannot run with Opus extraction on
the Claude subscription in a 12-hour window. The oracle setting (evidence sessions
only) was measured instead, on Mem0's public seeded sampler (per_type=15, then 30),
with LongMemEval's official judge prompts vendored at 9e0b455. Mem0's own
LongMemEval answer and judge prompts contain rules fitted to specific test items
("chandelier counts as jewelry"), so they were not used. Harness branch
bench/longmemeval-20261015 of EngraphyLabs/engraphy.

## Engraphy: LongMemEval oracle diagnosis, the weakness is assistant-turn recall and reader convention

N=15, two runs: 66.7% with Engraphy's reader and 75.0% with the official answer
template (official judge, Claude Sonnet 5). The paper's raw-read gpt-4o oracle is
87.0. Run A's 30 failures, adjudicated by hand: 13 extraction, 0 retrieval,
15 reading, 2 grading.
- Extraction: 10 of the 13 are single-session-assistant questions (recall what the
  assistant said), which the conversational extractor does not keep by design.
- Reading: the grounded reader declined with the answer present (6), and gave
  one-line answers to preference questions (5).
- Ceiling: with perfect reading the stores would allow 85.6% to 86.7%, beside
  gpt-4o's 87.0.
- Comparison with LoCoMo: the same ceiling height, a different cause.
- N=30 run A agrees: 73.3% and 82.2%, single-session-assistant 23%.
- Analysis: analysis/2026-10-15-longmemeval-oracle-diagnosis.md.

## Engraphy: three harness defects found on LongMemEval

1. **Command-line limit.** On the Claude CLI route, extraction prompts go on the
   command line, because structured output is honoured only there. Windows caps a
   command line at about 32 KB, and a longer window fails at launch and is recorded
   as empty. This affects 13 of 500 oracle questions. LoCoMo never triggers it.
2. **Operator identity.** The CLI exposes the signed-in operator's identity, and
   the extractor named LongMemEval's anonymous "user" after the operator inside
   memories. It is scrubbed from committed files by scripts/redact_longmemeval.py.
3. **Closed-schema refusals.** The write path refuses a whole memory that carries an
   attribute the pack does not declare.

Fix all three before any LongMemEval-S run. Run S on the per-token route only
after deciding whether to extract assistant recommendations. Pilot at per_type=5
(about 4.6M extractor output tokens) first.
