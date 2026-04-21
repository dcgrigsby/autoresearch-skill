# Autoresearch: Beyond Model Training (Shopify Engineering)

Source: https://shopify.engineering/autoresearch

## What is Autoresearch?

Autoresearch is an AI-driven autonomous loop system that originated with Andrej Karpathy's work on model training. The core concept involves "emulate a human researcher with AI," enabling automated optimization of tasks that would typically require manual human effort.

## How It Works

The autoresearch pattern follows these key steps:

1. **Metric Selection**: Identify a specific, measurable target (e.g., build time, test speed)
2. **Baseline Measurement**: Establish the current performance metric
3. **Hypothesis Generation**: The AI forms testable hypotheses for improvement
4. **Iterative Testing**: Execute changes and measure outcomes
5. **Evaluation Loop**: Keep improvements that advance the metric, discard failures
6. **Continuous Repetition**: Run indefinitely or until context limits

According to the article, the original Autoresearch could accomplish "training for GPT-2 took months" in hours autonomously.

## Shopify's Extension: Pi-Autoresearch

David Cortés and Tobi Lütke extended the concept beyond model training to general performance optimization. Their implementation added:

- Multi-metric support for simultaneous improvements
- Custom UI displaying iterations as table rows
- Auto-commit functionality for successful changes
- Consistent execution scripts

## Real-World Results

Shopify teams achieved significant improvements:

- Unit tests running "300 times faster"
- React component mounting improved "20% faster"
- Polaris build time reduced "65% faster" through optimization
- Liquid codebase achieved "53% faster combined parse+render time, 61% fewer object allocations"

## Key Insight

The transformative advantage: "Before autoresearch, AI agents were doing the same work humans did, just faster. Autoresearch is different—it does work nobody would attempt manually."

This addresses the critical gap where valuable optimizations lose priority to feature work—ideal territory for autonomous systems with no competing deadlines or competing priorities.
