# Metric-gaming pre-mortem

Before you launch the loop, spend 15 minutes trying to break your own metric. An agent that's going to run a hundred experiments overnight will find every flaw you miss — and "flaw" includes "the metric goes up but the artifact got worse."

## The procedure

1. State the metric and the direction (higher is better / lower is better).
2. List **at least five** ways an adversarial agent could push the metric in the desired direction WITHOUT genuinely improving the artifact. You're trying to beat your own metric, not defend it.
3. For each gaming vector, choose one mitigation:
   - **Holdout test case** the loop never sees — catches vectors that exploit specific eval cases
   - **Secondary metric** that would go the wrong way if the vector were exploited — catches general shape-of-output cheats
   - **Hard constraint in `program.md`** — catches vectors you can name precisely
4. Record vectors + mitigations in `program.md` under "Known metric-gaming vectors."
5. If you can't find five vectors, your metric is probably too narrow to catch anything interesting. Broaden it before running.

## Common gaming vectors by metric type

### Pass rate on a test suite

- **Memorizing specific test cases** — the edit special-cases the exact strings in the test suite. *Mitigation:* holdout cases + check for literal-string matches in the edited artifact.
- **Exploiting assertion wording** — an assertion says "response contains a citation"; the agent adds a fake citation. *Mitigation:* assertion that checks citations resolve to provided context.
- **Shortening outputs to avoid errors** — if long outputs have more chances to fail assertions, shrinking them raises pass rate without adding quality. *Mitigation:* minimum-length or coverage assertion.
- **Deferring the task** — output says "I'll do this later" or "here's a template you can fill in"; some assertions pass. *Mitigation:* assertion that checks the task was actually completed.

### Runtime / latency

- **Removing functionality to save time** — drop optional code paths, skip validation. *Mitigation:* correctness test suite runs in the same experiment; runtime only counts if correctness is 100%.
- **Caching the eval input** — memoize exactly the test inputs. *Mitigation:* randomize or vary eval inputs across experiments.
- **Async deferrals** — return fast, do work in background. *Mitigation:* measure end-to-end including downstream effects.

### Token / cost

- **Truncating output aggressively** — hit the budget by dropping content. *Mitigation:* quality floor (pass rate can't drop below X).
- **Offloading to external tools** — tool calls that don't count against the budget but do work that would. *Mitigation:* count all downstream costs if they're reachable from the editable surface.

### LLM-judge quality score

- **Writing for the judge's known biases** — if the judge likes bullet points, everything becomes bullet points. *Mitigation:* multiple judge models, or a holdout judge the loop never sees.
- **Meta-prompting the judge** — edit output to include "this is a high-quality response" phrasing. *Mitigation:* judge prompt strips or ignores meta-statements.
- **Sycophancy to the judge's phrasing** — mirror the eval prompt's language. *Mitigation:* vary the eval prompt's phrasing across runs; check for phrase-matching.

## After the loop: did it game?

Signs you were gamed:

- **Big train/holdout gap.** Loop climbed 30 points on train, 3 on holdout. Classic overfitting.
- **Outputs look weird.** Kept changes produce text that passes assertions but a human reader finds odd or degraded.
- **Jumps rather than climbs.** A real improvement sequence is many small wins. A single +15 jump is almost always a gaming discovery. Audit it.
- **Secondary metrics moved the wrong way.** If runtime got faster but accuracy dropped, the loop traded the wrong dimension. Your metric didn't capture what you actually cared about.

If you see any of these, don't promote the result. Either tighten the metric, add the gaming vector you missed to `program.md`, and re-run; or conclude that this target isn't amenable to autoresearch at the current metric definition.

## The hardest case: the metric is right but the loop still gamed it

Sometimes the metric genuinely captures what you want, but the agent finds a narrow exploit that wasn't in your vectors list. This is why the pre-mortem is a floor, not a ceiling. The correct response is:

1. Add the new vector to `program.md`'s gaming-vectors list.
2. Add a mitigation (usually a new holdout case).
3. Re-run from baseline.

Don't try to patch the loop's path — restart clean. The run that found the exploit is contaminated.
