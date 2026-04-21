# Claude Code with AutoResearch: Self-Improving Skills (MindStudio)

Source: https://www.mindstudio.ai/blog/claude-code-autoresearch-self-improving-skills

## Binary evals vs. LLM scoring

"Binary eval assertions cut through all of that noise" compared to subjective 1–10 scoring, which is "inconsistent across runs, sensitive to framing, and impossible to compare between prompt versions."

Each assertion is a **deterministic yes/no check** on specific output properties. Examples: "Does the response cite a source?" "Does the output fit in <500 tokens?" "Does the JSON parse?"

## Typical cycle performance

- One cycle = generate 3 variants, evaluate each against 20 test cases, select the winner
- ~5–15 minutes per cycle
- 30–50 cycles completable in an 8-hour window

## Pass rate improvements

"That's enough to push most prompts from 40–50% pass rates into the 75–85% range" over a single overnight run.

## Practical setup

- Project structure: `/prompts/`, `/evals/`, `/results/`
- 20–100 diverse test cases stored in JSONL
- 3–6 assertions per skill, targeting actual failure modes (not superficial properties)
- **One hypothesis per variant** — isolate what drives improvement. Don't bundle changes.
