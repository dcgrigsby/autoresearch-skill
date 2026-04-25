# Autoresearch Skill

Autoresearch is an autonomous optimization loop that iteratively improves a prompt, skill, configuration, or bounded piece of code against a measurable metric.

## Overview

The skill follows the "Karpathy loop" philosophy: autonomously iterating many experiments against one measurable metric. It works by:
1. Proposing a hypothesis-driven edit.
2. Running a metric (reproducible score) within a fixed time budget.
3. Keeping the change if the metric improves, or reverting if it doesn't.
4. Logging the process for audit and review.

## Key Concepts

- **The Triplet**: Every run requires a defined **Editable Surface**, a **Metric**, and a **Time Budget**.
- **Constraints**: Success depends on narrow scope and objective metrics rather than subjective human feedback.
- **Safety**: The scorer is never modified, and every change is tracked via Git.

## Project Structure

- `SKILL.md`: The core definition and protocol for the Autoresearch skill.
- `evals/`: Evaluation configurations and triggers.
- `references/`: Templates and guidelines for binary evals, metric gaming prevention, and more.
- `sources/`: Background research and articles on autoresearch patterns.
- `tests/`: Test fixtures and example targets.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

> **Note**: This project was built with Claude Code and is provided as-is with no warranty. See LICENSE for details.
