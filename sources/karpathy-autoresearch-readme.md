# AutoResearch (karpathy/autoresearch) — README

Source: https://github.com/karpathy/autoresearch

## Overview

AutoResearch enables autonomous AI agents to conduct LLM research experiments overnight. An agent modifies training code, runs 5-minute experiments, evaluates results, and iterates—producing a research log by morning.

The system trains a simplified single-GPU implementation of nanochat. Rather than directly editing Python files, researchers program `program.md` files that provide context and instructions to autonomous agents.

## Core Files

**`prepare.py`** — Fixed constants, one-time data preparation (downloading training data, BPE tokenizer training), and runtime utilities including dataloader and evaluation functions. This file remains unmodified.

**`train.py`** — The single file agents edit, containing the full GPT model, optimizer (Muon + AdamW), and training loop. Architecture, hyperparameters, optimizer selection, batch size, and all other parameters are fair game for modification.

**`program.md`** — Baseline instructions for agents. This file is edited and refined by humans to guide agent behavior.

## Key Design Parameters

- **Time Budget**: Fixed 5-minute training duration (wall clock, excluding startup/compilation)
- **Metric**: `val_bpb` (validation bits per byte)—lower is better, vocabulary-size-independent
- **Expected Throughput**: Approximately 12 experiments per hour, ~100 overnight

## Quick Start

```bash
# 1. Install uv project manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
uv sync

# 3. Download data and train tokenizer (one-time, ~2 minutes)
uv run prepare.py

# 4. Manually run single training experiment (~5 minutes)
uv run train.py
```

## Running the Agent

Prompt your Claude/Codex instance in the repository with instructions like:

"Hi have a look at program.md and let's kick off a new experiment! let's do the setup first."

The `program.md` functions as a lightweight skill definition for agent guidance.

## Design Principles

**Single Modification Point**: Agents only touch `train.py`, maintaining manageable scope and reviewable diffs.

**Fixed Time Budget**: All training runs exactly 5 minutes regardless of platform, ensuring direct comparability across architectural changes and hyperparameter variations while optimizing for your specific hardware.

**Self-Contained**: Minimal external dependencies beyond PyTorch—no distributed training, no complex configurations. One GPU, one file, one metric.

## Requirements

- Single NVIDIA GPU (tested on H100)
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

## Project Statistics

- **Stars**: 74.4k
- **Forks**: 10.9k
- **License**: MIT
