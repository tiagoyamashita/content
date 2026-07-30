---
label: "VII"
subtitle: "Metrics and experiments"
group: "Product Manager 101"
order: 7
---
Metrics and experiments
Measurement turns product work into learning. Define the expected behavior change, instrumentation, and decision rule before launch whenever possible.

## Metric hierarchy

| Level | Example |
|-------|---------|
| Business outcome | Retained revenue or cost-to-serve |
| Product outcome | Teams completing a recurring shared workflow |
| Leading indicator | New teams inviting a collaborator in seven days |
| Diagnostic | Step-level onboarding conversion |
| Guardrail | Error rate, complaints, or unsubscribe rate |

A north-star metric can align teams when it reflects recurring customer value, but it should not become the only measure of product health.

## Define metrics precisely

Record:

- event and property definitions;
- numerator, denominator, and eligible population;
- time window and cohort rules;
- exclusions and data-quality checks;
- owner and source of truth;
- expected direction and decision threshold.

“Increase engagement” is not measurable until behavior, population, and period are defined.

## Funnels, retention, and cohorts

Funnels reveal where a multi-step journey loses people. Cohorts compare users who started in a similar period or share a meaningful attribute. Retention shows whether users continue receiving value; choose a cadence that matches the real behavior of the product.

Segment results carefully. An overall improvement can hide harm to a new, small, or high-value group.

## Write a hypothesis

```text
For [segment],
if we [change],
then [behavior/outcome] will improve
because [mechanism].
We will evaluate [primary metric] over [window],
while monitoring [guardrails].
```

## Choose a learning method

- Interviews and prototypes for comprehension and desirability.
- Technical spikes for feasibility.
- Fake-door or concierge tests with clear ethical boundaries.
- Gradual rollout for operational confidence.
- A/B tests when randomization, sample size, and decision stakes justify them.
- Pre/post or matched analysis when experimentation is impractical, with weaker causal claims.

Not every decision needs an A/B test. Low-risk, reversible improvements with strong evidence may be shipped and monitored.

## Experiment integrity

Define eligibility, assignment, duration, stopping rules, sample assumptions, and guardrails in advance. Avoid repeatedly checking results and stopping at a convenient moment. Investigate instrumentation quality before interpreting surprising movement.

## Make the decision

At the review, compare evidence with the hypothesis and threshold. Decide to scale, iterate, hold, or stop. Record uncertainty and what would change the conclusion. A neutral result is useful if it prevents a larger unsupported investment.

**Next:** [Launch and iteration](viii-launch-and-iteration.md).
