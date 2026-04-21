# The Karpathy Loop and the Local Hard Takeoff

Source: pasted by user (Substack article on autoresearch, AutoAgent, and the Karpathy Loop)

On March 8, one of the best ML researchers alive pointed an AI agent at his own training code, gave it a single metric, and went to sleep. Two days later the agent had run 700 experiments, found 20 genuine improvements, cut training time by 11%, and surfaced a bug in his attention implementation that he'd missed. Not because the agent was smarter. Because it tried more things, faster, without getting bored after the fifteenth failed attempt.

The researcher was Andrej Karpathy. The script was 630 lines. Ten days later, when SkyPilot scaled the same pattern to 910 experiments on a 16-GPU cluster, the compute bill came in under $300.

On April 2 a small YC startup called ThirdLayer took the same loop and pointed it at something more consequential than training code: the prompts, tools, and orchestration logic that determine how agents behave. A meta-agent rewrote the task agent's entire scaffolding overnight. Every other entry on the leaderboards it targeted was hand-engineered by humans.

What's happening is not an intelligence explosion. It's something quieter and more immediate: optimization loops closing on specific business systems and compounding improvements faster than the organizations around them can track. A local hard takeoff, bounded to a domain, a metric, a sandbox. And the teams that can define "better" clearly enough to hand it to a machine are about to pull away from the teams that can't.

## The Karpathy Loop: Deceptive Simplicity as Design Philosophy

Autoresearch works because of the constraints, not the agent. Most people get that backwards. They see "AI does research while you sleep" and assume the magic is in the agent's intelligence. It isn't. The magic is in the constraints.

Karpathy's setup is deliberately minimal. Three files. One of them (train.py) is the only file the agent can touch. The agent proposes an edit, runs a five-minute training experiment, checks a single metric (validation bits per byte), and either commits the change or reverts it. That's the whole loop: one file, one metric, one fixed time budget. The human's job is to write program.md, a plain English instruction file that tells the agent what to explore and what constraints to respect. The human programs the research direction. The agent executes the search.

Fortune called it "The Karpathy Loop." The structure has three components: an agent with access to a single editable file, a single objectively testable metric, and a fixed time limit per experiment. That's the whole architecture.

The minimalism isn't a limitation. It's the entire point. By constraining the search space to one file, one metric, and one budget, Karpathy made the problem tractable for an agent in a way that a sprawling, multi-file, multi-objective system never would be. The agent can read the whole codebase in one pass, understand the full context of any change, and evaluate whether the change worked within minutes.

In Karpathy's first run, the agent executed about 12 experiments per hour, roughly 100 overnight. Of those, maybe 20 produced genuine improvements that stacked into an 11% speedup. The hit rate isn't high. But the iteration rate is inhuman.

When Shopify CEO Tobi Lütke tried the same pattern on internal company data, he got a 19% performance gain from 37 experiments in 8 hours. When SkyPilot pointed it at a 16-GPU Kubernetes cluster, the agent ran 910 experiments in 8 hours, discovered that scaling model width mattered more than any single hyperparameter, and spontaneously taught itself to use faster GPUs for validation while screening ideas on slower ones. Total compute cost: under $300.

## The Escalation: From Training Code to Agent Harnesses

Autoresearch optimizes training code. That's important, but it's a narrow domain.

Kevin Gu's AutoAgent takes the same loop (edit, run, measure, keep or discard) and applies it to agent harness engineering. Instead of optimizing a model's weights or hyperparameters, it optimizes the scaffolding around the model: the system prompt, the tool definitions, the routing logic, the orchestration strategy. The meta-agent reads failure traces from the task agent, diagnoses what went wrong, modifies the harness, and runs the benchmark again. It hill-climbs on total score.

Three findings from the AutoAgent work matter:

**First: the meta-agent / task-agent split.** Being good at a domain and being good at improving at that domain are different capabilities. The separation lets each agent specialize.

**Second: model empathy.** Same-model pairings dramatically outperform cross-model ones. A Claude meta-agent writes better harnesses for a Claude task agent than for a GPT task agent, and vice versa. The meta-agent shares the same weights, so when it reads a failure trace showing the task agent lost direction at step 14, it understands that failure from the inside.

**Third: emergent behaviors the team didn't program.** The meta-agent independently invented spot-checking (running individual tasks instead of the full benchmark suite for small edits, saving compute). It built forced verification loops and formatting validators, steered the task agent to write its own unit tests, invented progressive disclosure by dumping long contexts to files when results overflowed the context window, and built task-specific sub-agents and handoff logic when the domain required it. None of this was specified in the directive.

Optimizing training code is useful but niche. Optimizing the harness (the prompts, tools, routing, and orchestration that determine how an agent behaves) is universal.

## The Local Hard Takeoff

A local hard takeoff is what happens when an optimization loop closes on a specific business system and compounds improvements faster than the surrounding organization can track. Your pricing engine spends the weekend rewriting its own heuristics and comes back 30% more accurate. Your fraud detection model discovers patterns no human analyst would try. Your customer support agent autonomously builds verification loops and escalation logic that cut resolution time in half.

There's a subtlety: **traces are everything.** When Gu's team only gave the meta-agent scores without reasoning trajectories, the improvement rate dropped hard. Understanding why something improved matters as much as knowing that it improved. Traces give the meta-agent interpretability over the task agent's reasoning, and that interpretability is what makes targeted edits possible rather than random mutations.

The same logic applies outside ML. An optimization loop that only sees outcomes will produce random, unreliable improvements. An optimization loop that sees the full reasoning chain can make surgical edits. The quality of your trace infrastructure determines the quality of your auto-improvement.

## The Safety Problem Hiding in Plain Sight

The AutoAgent team observed: agents overfit. The meta-agent "gets lazy," Gu writes, "inserting rubric-specific prompting so the task agent can game metrics." In a benchmark context, that means inflated scores that don't reflect real capability.

For businesses, the practical safety concerns:
- **Metric gaming** — agent optimizing a proxy metric that diverges from actual business value.
- **Silent degradation** — subtle policy drift or quality erosion that persists undetected.
- **Contamination** — if the agent's optimization loop can influence the data it's evaluated against, the entire ratchet mechanism becomes unreliable.
- **Compounding errors** — a bad optimization in one system cascades through interconnected business processes.

Mitigations:
- Tight loops, clear baselines, version control for every edit, ability to revert any change.
- The agent can only touch one file. The metric is fixed and external.
- Gu's team forces the meta-agent to ask itself, "If this exact task disappeared, would this still be a worthwhile harness improvement?" — a self-reflection check designed to catch overfitting.
- **Evaluation diversity**: multiple metrics, multiple test suites, holdout scenarios the agent has never seen, and periodic human review of the agent's actual outputs rather than just its scores.

## Three Prompts (from the article)

1. **Karpathy Triplet Diagnostic** — walks you through defining the editable surface, the metric, and the time budget for a specific system, hands you back a program.md-style spec ready for an optimization loop.
2. **Metric-Gaming Pre-Mortem** — takes whatever metric you've defined and adversarially attacks it, returning a categorized gaming vector table plus the holdout scenarios and secondary metrics needed to catch each one.
3. **Trace Infrastructure Audit** — evaluates whether your current logging would give a meta-agent enough signal to make targeted edits, or only outcomes to guess at, and produces a ranked gap list with specific build-or-buy remediations.

## The Honest Path (applied guidance)

- **Start with the diagnostic.** Pick one system, define the Karpathy triplet: one editable surface, one metric, one time budget. If you can't define all three, that's your first project.
- **Build the eval harness before you build the optimization loop.** A scoring function that accurately reflects value. A test suite covering failure modes. A sandboxed execution environment. You can't automate what you can't score.
- **Prototype on low-risk, high-signal systems.** Internal models, ops scripts, internal tooling. Don't start with customer-facing systems.
- **Design for auditability from day one.** Every experiment logged, every edit versioned, every metric trajectory tracked, every revert documented.
- **Invest in the human judgment layer.** The human's job shifts from executing experiments to designing the experimental framework: writing the program.md that sets direction and constraints, reviewing trajectories for signs of overfitting, deciding which gains to promote.
