---
label: "VI"
subtitle: "Requirements and delivery"
group: "Product Manager 101"
order: 6
---
Requirements and delivery
Requirements should give the team enough shared context to make good decisions. They are not a substitute for collaboration or a contract that predicts every detail.

## A lightweight PRD

Include:

1. problem, target user, and evidence;
2. strategic context and desired outcome;
3. success metrics and guardrails;
4. scope, non-goals, and constraints;
5. key scenarios and acceptance conditions;
6. assumptions, risks, and open questions;
7. launch, instrumentation, and operational needs;
8. decision history and owners.

The document should explain why the work matters and what must be true, while leaving solution design to cross-functional collaboration.

## User stories and scenarios

A common format is:

```text
As a [user],
I want [capability],
so that [outcome].
```

Stories help when they capture real context, but the sentence alone is not a requirement. Add examples, edge cases, business rules, and acceptance criteria. For complex workflows, use scenario maps, diagrams, or prototypes.

## Acceptance criteria

Write observable conditions:

```text
Given [starting context]
When [action or event]
Then [observable result]
```

Include permissions, errors, empty states, accessibility, performance, privacy, analytics, and recovery when relevant. Engineering and quality partners should help define testability.

## Scope the smallest valuable release

An MVP is the smallest credible way to test a product hypothesis or deliver meaningful value—not an arbitrarily low-quality version. Separate:

- essential value and safety;
- useful improvements;
- later optimization;
- explicit non-goals.

Use prototypes, concierge workflows, or limited pilots when they test the risky assumption better than production code.

## Collaborate through delivery

Attend refinement and reviews to answer product questions, make trade-offs, and absorb new evidence. Do not micromanage implementation. When scope changes, preserve the outcome and guardrails, document the decision, and update affected teams.

## Definition of ready for launch

Confirm user experience, quality, legal and security requirements, support readiness, pricing or packaging, go-to-market, instrumentation, rollout controls, and rollback or remediation paths.

## Output is not outcome

Shipping is an important checkpoint. Keep ownership through adoption, measurement, follow-up, and the decision to iterate, scale, hold, or stop.

**Next:** [Metrics and experiments](vii-metrics-and-experiments.md).
