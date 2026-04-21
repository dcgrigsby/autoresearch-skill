# `program.md` template

`program.md` is the human's instruction file for an autoresearch run. The agent reads it every iteration. It is a living document — update it as you learn what works and what doesn't. Don't let it sprawl; a long `program.md` slows every iteration and starts to contradict itself.

Put it at `autoresearch/program.md` in the target project.

## Template

```markdown
# Autoresearch run: {short descriptive name}

## Triplet

- **Editable surface**: `{exact path to the one file or one coherent artifact}`
- **Metric**: `{command or procedure to produce the number}`
  - Direction: {lower is better | higher is better}
  - Baseline: {number from first run at HEAD}
  - Current best: {updated by the loop}
- **Time budget per experiment**: {wall-clock duration, e.g. "2 minutes"}

## Goal

{One sentence. What are we trying to do and why?}

## Hypothesis space

Things worth trying (not an exhaustive list — the agent should explore):
- {class of hypothesis 1}
- {class of hypothesis 2}
- ...

Things NOT to try (dead ends the human already knows about):
- {dead end 1, with reason}
- {dead end 2, with reason}

## Constraints

- {e.g., must preserve API signature}
- {e.g., no new dependencies}
- {e.g., must complete in under X tokens}

## Known metric-gaming vectors

From the pre-mortem (see metric-gaming-premortem.md):
- {gaming vector 1} — mitigated by {holdout test / secondary metric}
- {gaming vector 2} — mitigated by ...

## Stopping conditions

- Experiment cap: {N}
- Wall-clock cap: {T}
- Plateau: {N consecutive non-improvements}
- Any safety-rail trigger

## Running notes (agent appends here)

- Exp 3: tried {X}, +{delta}. Kept.
- Exp 7: tried {Y}, no change. Reverted. Hypothesis: {why it failed}.
- ...
```

## Notes on each section

**Triplet** — the top section exists so the agent can re-ground itself every iteration without having to derive the constraints from context. Keep it literal and precise (exact path, exact command).

**Goal** — one sentence. The agent will otherwise invent goals. A crisp goal is the main defense against drift.

**Hypothesis space** — not a checklist to tick through. It's a seed. The interesting improvements often come from hypotheses the human didn't list. But listing the first few helps the agent get started and avoids the cold-start problem where every early experiment is obvious.

**Dead ends** — at least as important as hypotheses. If you already tried "raising temperature" and it didn't work, write it down. Otherwise every autoresearch run starts by trying the same obvious things.

**Constraints** — hard rules. The agent should refuse to propose an edit that violates a constraint, even if it would improve the metric. These are what keeps the loop honest about the *shape* of improvement, not just the number.

**Gaming vectors** — cross-reference with the pre-mortem. The agent reads these every iteration so it knows what the user considers cheating.

**Running notes** — short, append-only. This is the agent's scratchpad, not the audit trail (`log.jsonl` is the audit trail). Keep entries to one line: experiment number, what was tried, outcome, one-line why.

## Anti-patterns (in program.md itself)

- **Vague goals.** "Make it better" is not a goal. Replace with something scorable.
- **Metric defined inside the editable surface.** The scorer must live outside the surface, or the agent can rewrite it.
- **"Always do X" instructions.** These stop working the first time X is wrong. Explain the *why* and trust the agent to apply judgment: "prefer simpler implementations because the target runs in resource-constrained settings" beats "always use the simplest implementation."
- **Too many sections.** If `program.md` grows past a page or two, you're programming the agent instead of directing it. Move detail into the eval harness or constraints.
