# Scaling Autoresearch to 16 GPUs (SkyPilot blog)

Source: https://blog.skypilot.co/scaling-autoresearch/

## Scaling approach

Parallel experimentation via SkyPilot orchestration: 16 clusters, `sky launch` + `sky exec -d` for queued jobs, runtime env vars to customize each experiment.

- Sequential: ~10 experiments/hour
- Parallel (16 clusters): ~90 experiments/hour (9x throughput)
- 910 experiments in 8 hours total

## Parallelism changes the search strategy

Instead of greedy hill-climbing (each experiment depends on the last), the agent ran **factorial grids of 10–13 experiments per wave**. Tests parameter *interactions* sequential search misses. Example: six model aspect ratios tested simultaneously in one 5-minute cycle.

## Emergent hardware exploitation

Without explicit instruction, the agent developed a two-tier strategy: screen hypotheses cheaply on H100s, promote top candidates to faster H200s for validation.

## Results and cost

- val_bpb: 1.003 → 0.974 (2.87% reduction)
- Total cost: ~$300 ($9 Claude API + ~$260 GPU rental at standard cloud rates)

## Transferable lesson (beyond ML)

The core principle — parallelizing exploratory work to enable factorial testing — applies to any iterative hypothesis testing domain. For prompts/skills/code: run N variants per round rather than sequential hill-climbing; surface parameter interactions.
