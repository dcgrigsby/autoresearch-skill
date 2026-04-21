# Parallel rounds (factorial exploration)

Serial hill-climbing — one experiment at a time, each building on the last — is the default. It's easy to debug, easy to interrupt, and the audit trail is linear. Start there.

When the triplet is solid and you want more throughput, switch to **parallel rounds**: dispatch N subagents simultaneously, each testing a different hypothesis from the same baseline. This is what SkyPilot did when they scaled autoresearch to 16 GPUs — and they discovered it doesn't just run faster, it finds different kinds of improvements.

## Why parallel isn't just "faster serial"

Serial hill-climbing is greedy: each experiment starts from the current best. That means you never test hypothesis B on top of baseline once hypothesis A has been committed — you only see A+B or A-only. If A and B individually help but A+B makes things worse (interaction effect), you're stuck.

Parallel rounds test a **factorial grid** from the same starting point. Round 1: test 6 hypotheses from baseline in parallel. Take the winner. Round 2: test 6 new hypotheses from the new best. This catches interactions sequential search misses.

SkyPilot's agent spontaneously discovered this: "tested six model aspect ratios simultaneously in one 5-minute cycle rather than six sequential trials." The same logic applies to prompts, skills, and code.

## The round protocol

One round:

1. **Fix the baseline** for this round: the current best-so-far, as of now.
2. **Generate N hypotheses** from `program.md`'s hypothesis space and the trace from the previous round. N is usually 3–8. More than 8 and hypothesis quality drops (you're scraping the barrel); fewer than 3 and parallelism barely helps.
3. **Dispatch N subagents in the same turn** (one Agent tool call per hypothesis, all in parallel). Each subagent:
   - Receives the baseline editable surface (fresh copy, not current HEAD — don't let subagents see each other's edits)
   - Receives one hypothesis to test
   - Applies the edit, runs the metric within the time budget
   - Returns: the diff, the metric, a short trace explaining what happened
4. **Aggregate results.** Pick the winner — the hypothesis whose metric beat baseline by the largest margin. If no hypothesis beat baseline, keep baseline (no change this round) and log plateau.
5. **Commit the winner** with its hypothesis as the message. This becomes the baseline for the next round.
6. **Append round summary to `log.jsonl`** — include every hypothesis tried, not just the winner. The losing hypotheses are signal for the next round.

## Dispatching subagents

In Claude Code, this is a single message with N Agent tool calls in parallel. Template for each subagent prompt:

```
You are running experiment {round}.{hypothesis_id} in an autoresearch loop.

Baseline artifact: {editable_surface_path} at commit {baseline_sha}
Metric command: {metric_command}
Time budget: {budget}

Hypothesis to test: {one-sentence description of the edit}

Constraints:
- You may only modify {editable_surface}. Do not touch anything else.
- You must not modify the scorer.
- Run the metric exactly once, within the time budget.
- If the metric run exceeds the budget, report failure and stop.

Return JSON:
{
  "hypothesis_id": "...",
  "diff_summary": "...",
  "metric": <number>,
  "metric_direction": "lower_is_better" | "higher_is_better",
  "trace": "what you tried, what happened, why you think it did or didn't work"
}
```

## Sizing rounds

- **Round count**: keep total experiment count similar to a serial run. 10 rounds × 5 parallel = 50 experiments, comparable to a 50-experiment serial loop but finished in roughly 1/5 the wall-clock.
- **N per round**: usually 3–8. If subagents are cheap and hypotheses are abundant, 8. If generating quality hypotheses is the bottleneck, 3–4.
- **Budget per subagent**: the per-experiment time budget from the triplet. All subagents run to the same budget for comparability.

## Model empathy (from AutoAgent)

For tasks where the editable surface is a prompt or a skill that will be run by a specific model family (Claude, GPT, etc.), use the **same model family for both the meta-agent and the task agent**. A Claude meta-agent writes better prompts for a Claude task agent because it has implicit understanding of how the inner model reasons. Cross-family pairings (GPT meta-agent optimizing a Claude skill) measurably underperform.

In practice: if you're optimizing a Claude skill, run the loop with Claude as both the orchestrating agent and the eval runner. Don't mix.

## When to escalate from parallel rounds to unattended

After a few parallel rounds are running cleanly, you can hand off to a background script that calls Claude Code in a loop, with a fixed schedule and a stopping condition. Requirements before escalating:

- **No safety-rail triggers in recent runs.** If metric-gaming pre-mortem items are still tripping, fix those before going unattended.
- **Plateau behavior is clean** — rounds that don't improve don't degrade, and the loop halts or adapts.
- **The debrief process is automated** — an end-of-run report is generated so you wake up to useful output, not a wall of JSONL.

Unattended autoresearch is not a default. It is the last escalation after levels 1 and 2 have been exercised on this specific triplet.
