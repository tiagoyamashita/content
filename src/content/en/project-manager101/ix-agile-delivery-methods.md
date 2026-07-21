---
label: "IX"
subtitle: "Agile delivery methods"
group: "Project Manager 101"
order: 9
---
Agile delivery methods
Agile delivery uses short feedback loops, incremental value, and adaptable plans to manage uncertain work. It does not mean working without commitments, documentation, governance, or long-term direction.

## Principles in practice

| Principle | Practical behavior |
|-----------|--------------------|
| Deliver value incrementally | Release useful slices instead of waiting for one large handoff |
| Learn from evidence | Review working results with users and stakeholders |
| Adapt the plan | Reprioritize when outcomes, risks, or constraints change |
| Make work visible | Use a shared backlog or board with clear ownership and state |
| Empower the team | Give the team an outcome and boundaries, not only assigned tasks |
| Improve continuously | Use retrospectives and delivery data to change the system |

Agile methods work best when leadership accepts transparency and trade-offs. Renaming meetings while preserving fixed scope, fixed dates, and command-and-control decisions does not create agility.

## Scrum

Scrum organizes work into fixed-length sprints, commonly one or two weeks.

| Element | Purpose |
|---------|---------|
| Product backlog | Ordered list of product work and learning |
| Sprint goal | Coherent outcome the sprint should achieve |
| Sprint planning | Select a feasible goal and plan |
| Daily Scrum | Developers inspect progress toward the goal and adapt |
| Sprint review | Inspect the increment with stakeholders and update direction |
| Retrospective | Improve team practices and working conditions |

The product owner is accountable for backlog value and ordering. The Scrum Master improves the system and coaches the team. Developers determine how to create the increment. A project manager may coordinate cross-team dependencies, budget, external milestones, and governance without taking over these accountabilities.

## Kanban

Kanban manages flow continuously:

1. Visualize the workflow.
2. Define what each state means.
3. Limit work in progress.
4. Pull new work only when capacity is available.
5. Measure flow and remove bottlenecks.
6. Improve policies through experiments.

Useful measures include:

- **Lead time:** request to completion.
- **Cycle time:** work started to completion.
- **Throughput:** items completed per period.
- **Work in progress:** items currently active.
- **Work item age:** how long active work has remained unfinished.

Kanban is not merely a board with columns. Without explicit policies and work-in-progress limits, the board only displays congestion.

## Scrum, Kanban, or hybrid

| Context | Starting point |
|---------|----------------|
| Product team benefits from a regular planning and review rhythm | Scrum |
| Operational or support work arrives continuously | Kanban |
| Team needs sprint goals but also handles interrupts | Scrum with explicit expedite policies and capacity |
| Fixed external milestone with evolving internal scope | Iterative delivery inside milestone governance |

Choose a method based on work characteristics. Do not combine every ceremony and artifact into a heavier process.

## Planning at multiple horizons

```text
Strategy and outcomes
  → roadmap themes and milestones
  → release or quarterly forecast
  → sprint goal or replenishment decision
  → daily coordination
```

Near-term work can be detailed while later work remains probabilistic. Keep dependencies, risks, funding, and external commitments visible outside the team backlog when they require broader governance.

## Healthy delivery metrics

Use metrics to improve the system:

- outcome achieved and value delivered;
- predictability against sprint goals or service expectations;
- lead time, cycle time, throughput, and blocked time;
- escaped defects, rework, reliability, and support burden;
- team health and sustainable pace.

Velocity is a local planning aid, not a performance target. Comparing teams or rewarding higher story-point totals encourages inflated estimates and lower quality.

## Common anti-patterns

- Treating the daily meeting as a status report to a manager.
- Filling every person's capacity instead of optimizing flow.
- Carrying unfinished work across sprints without investigating why.
- Calling a large specification “agile” because delivery uses sprints.
- Changing priorities during a sprint without changing expectations.
- Skipping reviews with users and calling task completion success.
- Using tools to enforce a workflow the team does not understand.

## Adoption checklist

- Define the outcome and who owns product priority.
- Map the current workflow before configuring software.
- Agree work item types, states, entry/exit policies, and completion criteria.
- Establish a regular review and improvement cadence.
- Start with minimal fields and automation.
- Inspect both customer outcomes and delivery flow.
- Change the process when evidence shows a bottleneck.

**Next:** [Jira, Confluence, and delivery tools](x-jira-confluence-and-delivery-tools.md).
