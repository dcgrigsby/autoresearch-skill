# Test fixture: summarize

Pre-staged target for the autoresearch skill's happy-path test case.

## Layout

- `target/summarize.md` — the editable surface (a starter summarization prompt)
- `target/scorer.py` — the metric implementation (a deterministic checklist scorer)
- `target/eval.sh` — runs the scorer, prints a single number 0.0–1.0 (higher is better)

## About the scorer

The scorer is a **mock**. It checks structural features of `summarize.md` (does it mention bullets? does it specify length? does it forbid hallucination? etc.) — not the quality of actual summaries a model would produce.

This is deliberate: we want the autoresearch loop to have a fast, deterministic, edit-responsive metric so we can test whether the LOOP is structured correctly. A real autoresearch run would use an LLM eval against real test cases.

The baseline `Summarize this article in bullets.` scores ~0.1. A well-structured prompt can reach 0.7–0.9 by adding features the scorer rewards.

## Running manually

```bash
cd target
./eval.sh
```
