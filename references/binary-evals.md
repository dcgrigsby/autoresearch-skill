# Binary eval assertions

## Why binary beats rubrics

A 1–10 rubric seems richer than a yes/no check, but for an autonomous loop it is strictly worse:

- **Rubric scores drift** — the same output scored twice gets different numbers. Across 50 iterations, that noise swamps real signal.
- **Rubric scores are sensitive to framing** — rewording the rubric question changes the distribution. The agent learns to game the rubric's framing, not the underlying quality.
- **Rubric scores aren't comparable** — "7 on clarity" in experiment 3 may not mean the same thing as "7 on clarity" in experiment 40.
- **Rubric scores degrade under compression** — summing 10 rubric scores into one number hides which dimension moved.

Binary yes/no assertions solve all four: deterministic, stable framing, directly comparable, and they aggregate cleanly (pass rate is just "how many yeses").

## Turning a rubric into assertions

Take each dimension of the rubric. For each, write one or more yes/no questions that get at what the rubric is actually trying to measure.

**Example — rubric dimension "the hook is engaging" (1–5):**

Bad binary: "Is the hook engaging?" (yes/no) — same problem as the rubric, just binarized.

Good binary (multiple assertions):
- Does the hook include a specific number, statistic, or data point?
- Is the hook under 20 words?
- Does the hook name a specific person, company, or event?
- Does the hook avoid generic openers like "In today's world" or "Have you ever"?

Each question is objectively answerable. The aggregate gives you a pass rate that correlates with "engagingness" without being the same thing.

## Guidelines

- **3–6 assertions per skill** (from MindStudio's practitioner writeup). Fewer, and you don't capture enough signal. More, and each assertion carries less weight and the scoring gets slow.
- **Target actual failure modes**, not superficial properties. If your prompt sometimes hallucinates citations, the assertion should be "every cited source appears in the provided context," not "the output contains at least one citation."
- **Objectively checkable** — a script or regex or simple LLM call can answer the question. If answering requires expert judgment, it's not binary yet.
- **Independent of each other** — if passing assertion A always means passing assertion B, one of them is redundant.
- **Failing an assertion should be informative**, not just "worse." The loop reads failure traces to form next hypotheses (see the "traces over scores" principle from AutoAgent).

## What to do when you need a judge model

Sometimes the only way to check an assertion is with another LLM call (e.g., "is this response on-topic?"). Rules for LLM-judge assertions:

- **Use a different model** than the one producing the output where possible (Claude judges GPT, etc.). Reduces same-model sycophancy.
- **Few-shot the judge** with examples of both passes and fails so the judge calibrates.
- **Ask for yes/no only**, not a score. Resist the urge to ask for reasoning unless you'll use it.
- **Run the judge twice on a sample** and check for flip rate. If >5% of assertions flip between runs, the assertion isn't binary enough — tighten it.

## Holdout assertions

Keep 20–30% of your test cases as a **holdout** the loop never sees. The loop optimizes against the train set; the holdout is what tells you whether gains generalized or the loop just overfit.

If train pass rate climbs 30 points and holdout climbs 25, you generalized. If train climbs 30 and holdout climbs 2, the loop found a way to game the train set — this is the pattern you must watch for.

## Typical progression

From MindStudio's data, a starting skill with 40–50% pass rate can reach 75–85% after 30–50 cycles of an overnight loop. Expect:

- Fast early gains (the first 10 iterations find obvious fixes)
- Plateaus around 65–70% pass rate (the "easy wins" are used up)
- Slow grinding gains to 80%+ requiring genuinely creative hypotheses
- Above 90% the loop often starts metric-gaming — treat that as a warning, not a win
