# AutoAgent (kevinrgu/autoagent) — README

Source: https://github.com/kevinrgu/autoagent

## Core concept

AutoAgent implements a **meta-agent** pattern for autonomous harness engineering. The meta-agent modifies prompts, tools, configuration, and orchestration while running benchmarks to evaluate improvements. Framing: "Give an AI agent a task, let it build and iterate on an agent harness autonomously overnight."

## Architecture

- **`agent.py`** — Single-file harness containing configuration, tool definitions, and routing logic. The only file the meta-agent edits.
- **`program.md`** — Human-editable instructions and directives for the meta-agent. Captures context, constraints, anti-patterns.
- **`tasks/`** — Evaluation benchmarks (Harbor format).
- **`.agent/`** — Optional workspace artifacts for reusable prompts and skills.

## Loop

The metric is total score produced by the benchmark's task test suites. The meta-agent hill-climbs on this score. Invocation: "Read program.md and let's kick off a new experiment!"

## Key findings (from surrounding writing / article)

- **Meta-agent / task-agent split** — being good at a domain and being good at improving at that domain are different capabilities. The separation lets each specialize.
- **Model empathy** — same-model pairings dramatically outperform cross-model ones. A Claude meta-agent optimizes Claude task agents better than GPT task agents.
- **Traces over scores** — when the meta-agent only saw scores (not reasoning traces from failures), improvement rate dropped hard. Understanding *why* something failed is what enables targeted edits rather than random mutations.
- **Emergent behaviors** — spot-checking (run one task instead of full benchmark for small edits), forced verification loops, steering the task agent to write its own unit tests, progressive-disclosure dumps to files when context overflowed, task-specific sub-agent handoff logic. None specified up front.
- **Self-reflection check** — meta-agent is prompted to ask: "If this exact task disappeared, would this still be a worthwhile harness improvement?" Designed to catch overfitting/metric gaming.

## Requirements

Docker, Python 3.10+, `uv`.
