---
name: autoresearch
description: Run the Karpathy autoresearch loop — autonomously iterate many experiments against one measurable metric to improve a prompt, skill, config, or bounded piece of code. MUST consult when user says "autoresearch," "use autoresearch to [improve/optimize/tune/fix] X," mentions "the Karpathy loop" or "program.md," or asks for autonomous multi-iteration optimization (overnight hill-climbing, tournament prompt tuning, "try N things and keep what works," or the "propose edit → run → score → keep or revert" pattern repeated many times). Consult even when the task looks simple — naive implementations hit metric-gaming and premature-launch failures within ~10 iterations; this skill provides the triplet-framing intake, pre-mortem, scaffolding deliverables, and loop discipline they lack. Also covers agent harnesses, prompts against binary-assertion test suites, retrieval configs, lint rule sets — any bounded editable surface with a reproducible scorer. Not for one-shot edits or purely subjective goals.
---

# Autoresearch

Autoresearch is an autonomous optimization loop: given one editable artifact, one metric, and a time budget per experiment, the agent proposes a change, runs it, scores it, keeps it if the metric improves, reverts if not — and does this tens or hundreds of times.

**The power is not the agent. It is the constraints.** An agent with a sprawling, multi-file, multi-objective problem will flail. An agent with one file, one number, and a five-minute run will compound improvements a human wouldn't have the patience to try. Your job when running this skill is to pin down the constraints rigorously before the loop starts, and then run the loop honestly.

## The triplet (non-negotiable before the loop starts)

1. **Editable surface** — the thing the agent may modify. Ideally one file. Acceptable: one coherent artifact (a skill directory, one module, one prompt file). The narrower the better, for three reasons: the agent can read the whole surface in one context pass, diffs stay reviewable, and the scoring function stays external to what's being edited (which is what makes the loop honest — see safety rails).

2. **Metric** — one number, reproducible (same input → same number), scored by something outside the editable surface. Objective: pass rate on a binary-assertion test suite, runtime, token count, eval score. Subjective quality scores ("elegance 1–10") don't work — they drift run to run and are the first thing a meta-agent will learn to game.

3. **Time budget** — fixed wall-clock duration per experiment. Enforces comparability (every experiment gets the same runway) and caps cost. Pick something where one experiment runs in seconds to minutes, not hours — iteration rate is the whole point.

If any of the three is fuzzy, **stop and build it before running the loop.** Running autoresearch with a vague metric or a sprawling editable surface is the main way this pattern goes off the rails.

## Protocol

### 1. Intake

Clarify what "better" means to the user, concretely. Common user intents and what they translate to:

| User says | Maps to |
|---|---|
| "Make this prompt better" | Pass rate on a test suite the user hasn't built yet — build it first |
| "Optimize this function" | Runtime, memory, or correctness on a benchmark — pick one |
| "Improve this skill" | Pass rate on eval assertions (see binary-evals.md) |
| "Tune this config" | Some measurable downstream quality or cost |

If the user can't answer "when is the new version better than the old?" with a reproducible procedure, do not start the loop. That's the first project — build the scorer. But do not stop at an explanation — ship scaffolding. See "When intake can't proceed" below.

### 2. Frame the triplet — and ship deliverables

The intake phase produces *named files*, not just conversation. A one-paragraph answer saying "you should build an eval harness" is not the deliverable. The deliverable is the scaffold the user could fill in and run this afternoon. This is the single biggest thing that distinguishes a real autoresearch setup from talking about one.

**If the triplet is fully definable from the user's input, ship:**
- `autoresearch/program.md` — the triplet + goal + hypothesis space + constraints + gaming vectors, filled in from `references/program-md-template.md`. This is mandatory. The agent reads it every iteration.
- `autoresearch/log.jsonl` — audit log, initialized with the baseline entry once step 3 runs.

**When intake can't proceed** (triplet is fuzzy, metric missing, editable surface ambiguous, or target artifact doesn't exist), do not just explain what's needed. Ship the scaffolding that turns the explanation into a concrete next step the user can execute:

- **Missing eval infrastructure** → ship a `program.md` *draft* with the triplet's unknowns marked, plus an eval harness scaffold: a scorer skeleton file with the binary-assertion structure (from `references/binary-evals.md`), a README describing the harness, and one or two worked example test cases showing the `case/diff/context/expected.json` shape.
- **Fuzzy goal** → ship a `triplet-worksheet.md` (fill-in-the-blank for editable surface, metric, time budget), a `metric-candidates.md` (3–5 concrete metric options with pros/cons), and — if the goal is helpfulness-flavored — a `binary-assertion-examples.md` showing what good assertions look like for the user's domain.
- **Target file doesn't exist** → don't fabricate contents. Ask for the file while shipping the other scaffolding so the user can see exactly where it fits.

`program.md` itself, whether draft or final, should contain:

- The editable surface (exact path)
- The metric (how to run it, how to parse the number, direction of improvement)
- The time budget per experiment
- Direction/constraints: what kinds of edits to try, what to avoid, known dead-ends
- Anti-patterns: metric-gaming vectors the human already knows about

The reason to ship files instead of just talking: a long explanation can be skimmed and forgotten. A directory of files is something the user can edit, run, and bring back next session. It also forces the skill to commit to specifics — you can't write a worksheet without deciding what the questions are.

### 3. Baseline + pre-mortem

- Run the metric once at HEAD. Record the starting number in `autoresearch/log.jsonl`.
- **Metric-gaming pre-mortem** (see `references/metric-gaming-premortem.md`): list at least five ways the agent could push the number up WITHOUT genuinely improving the artifact. For each, either add a holdout test the agent doesn't see during the loop, or add a secondary metric that would catch the gaming.
- **Convert fuzzy rubrics to binary assertions** (see `references/binary-evals.md`). Binary yes/no checks beat 1–10 scores — they're stable run-to-run and don't drift.

### 4. Run the loop

Each iteration:

1. Read `program.md` and the current editable surface fully.
2. Form **one** hypothesis-driven edit. One change per iteration. Bundling changes makes it impossible to know what drove the result.
3. Write the edit. Run the metric within the time budget.
4. Compare to best-so-far. **Not** to the previous iteration — the best, so we don't drift downward.
5. If strictly better: commit with the hypothesis as commit message. Update best-so-far.
6. If worse or equal: revert via `git revert` (not "just undo"). Log why you think the hypothesis failed.
7. Append a JSONL line to `autoresearch/log.jsonl`:
   ```json
   {"ts": "...", "exp": 17, "hypothesis": "increase retry count from 2 to 5", "diff_summary": "...", "metric": 0.78, "best": 0.82, "decision": "reverted", "reason": "added latency, no pass-rate gain"}
   ```

The loop runs until one of the stopping conditions (below) fires.

### 5. Debrief

When the loop stops, produce a report at `autoresearch/report.md`:

- **Headline**: baseline → best (delta)
- **Stats**: experiments run, kept, reverted, hit rate, wall-clock
- **Top improvements**: 3–5 kept changes ranked by metric contribution, each with hypothesis and diff
- **Surprising findings**: things the agent tried that a human probably wouldn't have
- **Anti-pattern watch**: did the metric start moving in ways that look like gaming rather than real improvement? (Sudden jumps, weird outputs that still pass evals, outputs trending toward eval-specific shapes.)
- **Recommendation**: promote to main, run another round, or revise the triplet (often the metric)

## Safety rails (each exists for a reason)

- **Only the editable surface is modified.** Prevents scope creep and makes diffs reviewable. If the agent believes it needs to edit outside the surface to make progress, stop and surface that to the user — the triplet may be wrong.
- **The scorer is never touched.** If the agent can edit the scorer, "improvement" is meaningless. If the agent thinks the scorer is broken, stop and ask; don't fix it mid-loop.
- **Every experiment is a git commit.** Revert is `git revert`, never freeform undo. This is the audit trail.
- **Self-reflection check on every kept change**: "If this specific eval disappeared, would this still be a worthwhile improvement?" Borrowed from AutoAgent — designed to catch harness-specific overfitting. Log the answer. Flag "no" answers in the debrief.
- **Stop if the metric starts moving suspiciously.** A sudden 20-point jump, outputs that pass evals while looking wrong, repetitive edits that crush specific test cases — these are gaming signatures. Halt and surface.

## Autonomy levels

Pick the lowest one that fits. Escalate only after the lower level is working cleanly.

1. **In-conversation, serial** (default) — Claude runs experiments one at a time in the current session. Easy to debug, easy to interrupt, easy to audit. Start here even if the user asked for "overnight." You'll catch triplet problems in the first five experiments.

2. **Parallel subagent rounds** — Claude dispatches N subagents per round (each runs one hypothesis), aggregates, picks the winner, next round. Enables factorial exploration — you learn parameter interactions sequential hill-climbing misses. See `references/parallel-rounds.md`. Use once triplet is solid.

3. **Unattended / overnight** — hand off to `/loop` (for periodic ticking) or a background script that calls Claude Code via the CLI. Only after levels 1 and 2 have been exercised on this specific triplet. Requires the user to be genuinely comfortable with the metric-gaming guardrails, because nobody's watching.

## Stopping conditions

Any of these ends the loop:

- **Experiment cap** reached (e.g., 50 experiments).
- **Wall-clock cap** reached (e.g., 4 hours).
- **Plateau**: N consecutive experiments with no improvement (default N=10). Plateau usually means the triplet needs revision — a new metric, a widened surface, or a different class of hypothesis to try.
- **Suspicion**: any safety-rail trigger. Surface and stop.
- **User interrupt**.

Always end with a debrief, even on interrupt.

## When this skill is the wrong tool

- **One-shot edits** — "fix this bug" or "add this feature" is not autoresearch; it's just editing.
- **Purely subjective goals** — "make the copy more engaging" with no scorer. Autoresearch needs a number.
- **Target that doesn't work yet** — if the baseline pass rate is below ~50%, the loop will thrash on foundational issues rather than compound improvements. Stabilize first, then autoresearch.
- **Safety-critical production systems** without the full guardrails in place. Start with internal/low-risk targets. Earn the right to optimize higher-stakes systems by proving the loop works on lower ones first.

## See also

- `references/program-md-template.md` — the per-run human-editable spec
- `references/binary-evals.md` — converting fuzzy goals into yes/no assertions
- `references/metric-gaming-premortem.md` — adversarial metric review before launch
- `references/parallel-rounds.md` — factorial exploration with parallel subagents
- `sources/` — original articles and primary sources (Karpathy's repo, Shopify, AutoAgent, MindStudio, aimaker, SkyPilot)
