---
label: "X"
subtitle: "Agile product development"
group: "Product Manager 101"
order: 10
---
Agile product development
Agile product development combines continuous learning with incremental delivery. The goal is not to produce more backlog items; it is to improve customer and business outcomes while reducing the cost of being wrong.

## Discovery and delivery together

```text
Discover opportunities → test assumptions → choose an outcome
          ↑                                  ↓
     measure results ← release safely ← deliver a small slice
```

Discovery explores whether a problem and solution are valuable, usable, feasible, and viable. Delivery creates a reliable product increment. The activities overlap: learning shapes delivery, and production evidence shapes the next discovery work.

Avoid a permanent handoff where a “discovery team” creates requirements for a “delivery team.” Product, design, and engineering should share evidence and decisions.

## Outcome-oriented planning

Connect work across horizons:

| Horizon | Product question |
|---------|------------------|
| Strategy | Where will the product focus and why can it win? |
| Outcome | Which user or business behavior should change? |
| Opportunity | Which problem is most important to address? |
| Bet | Which approach and assumptions are worth testing? |
| Increment | What is the smallest valuable or informative release? |

A roadmap communicates outcomes and strategic intent. A backlog contains candidate work. Neither should become an unconditional feature contract.

## Product backlog

The backlog is an ordered queue, not a warehouse for every suggestion.

Healthy backlog items include:

- the problem or user scenario;
- expected outcome and evidence;
- acceptance criteria or learning objective;
- constraints, risks, dependencies, and links;
- sufficient detail for the next decision.

Keep near-term items refined and later ideas lightweight. Merge duplicates, close work that no longer fits strategy, and preserve important evidence outside ticket comments.

## Slice work vertically

Deliver a thin end-to-end capability that a user can experience or that tests a meaningful assumption. Horizontal slices such as “build database,” “build API,” and “build UI” delay integration and feedback.

Ways to reduce scope:

- one segment, workflow, channel, or platform;
- happy path before lower-risk edge cases;
- manual operations behind a simple interface;
- limited rollout or pilot;
- reduced configuration with a safe default;
- read-only before write behavior.

Do not remove security, privacy, accessibility, data integrity, or essential quality to make a slice smaller.

## Scrum participation

| Event | Product manager contribution |
|-------|------------------------------|
| Refinement | Explain outcomes, evidence, constraints, and open questions |
| Sprint planning | Clarify priority and help shape a coherent sprint goal |
| Daily Scrum | Join only when useful; do not turn it into a PM status meeting |
| Sprint review | Review working product with stakeholders and gather evidence |
| Retrospective | Participate as a team member and improve the system |

The product manager or product owner orders the backlog. Engineers own implementation choices and estimates. Designers own design craft. The entire team contributes to scope and solution decisions.

## Kanban participation

For continuous flow:

- establish service classes and explicit priority policies;
- limit work in progress;
- review aging and blocked items;
- replenish the queue at a sustainable cadence;
- inspect lead time and outcome evidence;
- avoid inserting “urgent” work without a transparent trade-off.

## Definition of done

Done may include:

- acceptance criteria met;
- review and automated checks complete;
- accessibility, security, privacy, and reliability addressed;
- analytics events validated;
- documentation and support readiness complete;
- releasable or released according to team policy.

A ticket marked done is not proof of product success. Outcome measurement continues after delivery.

## Sustainable team practices

- Set one clear goal rather than a collection of unrelated tickets.
- Protect capacity for discovery, defects, reliability, and maintenance.
- Keep decisions close to the people with relevant context.
- Use stakeholder reviews for feedback, not ceremonial approval theater.
- Make interruptions and dependency costs visible.
- Change process through retrospective experiments.

## Anti-patterns

- Product manager writes tickets alone and hands them to engineering.
- Story points become individual productivity measures.
- Every request enters the backlog without product judgment.
- Sprint success means all tickets closed despite no usable increment.
- Discovery stops once implementation begins.
- Teams ship continuously but never inspect customer outcomes.
- “Agile” is used to avoid strategy, documentation, or commitments.

**Next:** [Product documentation and tools](xi-product-documentation-and-tools.md).
