# A Skill That Makes All My Other Skills Better (aimaker.substack)

Source: https://aimaker.substack.com/p/how-i-built-skill-improves-all-skills-karpathy-autoresearch-loop

## Three-phase system

1. **Setup (human-involved)** — human and agent align on quality standards. The agent analyzes the target skill, generates test cases, builds an evaluation rubric, establishes a baseline, and converts weaknesses into binary checks. Human approves before proceeding.

2. **Autonomous loop (no human)** — system mutates one element, runs all test cases, scores with binary evaluations, keeps or discards. Repeats until stopping criteria met. No human permission required per iteration.

3. **Debrief (human review)** — results are re-scored using the original rubric so before/after comparisons stay consistent. Full report documents what changed and what worked.

## Binary evals insight

1–5 rubrics work for human understanding but fail for unsupervised loops. The fix: "convert the weakest dimensions from the rubric and turn them into binary yes/no checks." Example: "Does the hook include a specific number or data point?" (yes/no) replaces subjective "hook quality 1–5."

## Prerequisites (when this pattern works)

- Target skill must already work **60–80% of the time** with repeatable failure patterns. Below that, the loop thrashes on fundamental issues rather than hill-climbing.
- You must clearly define what "good" looks like before building evaluations.
- Needs Claude Code, preferably Opus 4.6, for long-running tasks.

## Generalization

The approach applies to any system with editable components, measurable outcomes, and time-boxed testing — not just neural networks.
