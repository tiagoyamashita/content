---
label: "XI"
subtitle: "Product documentation and tools"
group: "Product Manager 101"
order: 11
---
Product documentation and tools
Product tools support a chain from evidence to decision to delivery to measurement. Choose one authoritative home for each artifact and connect tools with links or integrations instead of duplicating information.

## Toolchain by product activity

| Activity | Common tools |
|----------|--------------|
| Product briefs, PRDs, decisions, and knowledge | Confluence, Notion, Google Workspace |
| Delivery backlog and work tracking | Jira, Linear, Azure DevOps Boards, GitHub Projects |
| Opportunity and roadmap management | Jira Product Discovery, Productboard, Aha!, airfocus |
| Research repository | Dovetail, Condens, EnjoyHQ, Confluence |
| Prototypes and design | Figma, FigJam, Miro |
| Product analytics | Amplitude, Mixpanel, PostHog, GA4 |
| Experiments and feature flags | Optimizely, LaunchDarkly, Statsig, GrowthBook |
| Customer feedback | Intercom, Zendesk, Salesforce, HubSpot |
| Communication | Slack, Microsoft Teams |

The best stack depends on scale, workflow, integrations, security, accessibility, cost, and administration capacity. A smaller connected stack is often more usable than many specialized tools.

## Confluence for product knowledge

A practical product space may contain:

```text
Product home
  ├── Vision, strategy, principles, and glossary
  ├── Outcomes and roadmap
  ├── Opportunities and research
  ├── Product requirements and decisions
  ├── Metrics and experiment results
  ├── Launches and release notes
  └── Archive
```

### Product page standards

Important pages should show:

- owner and status;
- intended audience and decision;
- evidence and source links;
- last reviewed date;
- related roadmap item, Jira epic, design, and dashboard;
- superseding page when archived.

Keep the strategy, PRD, and decision rationale in durable pages rather than fragmented ticket comments. Use templates to improve consistency, but remove sections that do not help the decision.

## Jira for product delivery

Use Jira to make planned and active work visible:

- **Epic:** a coherent product bet, capability, or significant outcome area.
- **Story:** a user-centered, independently valuable slice.
- **Task:** necessary work that is not naturally a user story.
- **Bug:** behavior that fails an agreed expectation.
- **Subtask:** a team-level decomposition when it improves coordination.

Link each epic to its product brief, research, design, metric, and decision record. Tickets should contain enough context to execute and verify the work, but they should not reproduce the entire PRD.

### Backlog hygiene

- Order work according to strategy and evidence.
- Keep the next planning horizon refined.
- Use labels and components with documented meanings.
- Close stale and rejected requests with rationale.
- Distinguish committed work from discovery candidates.
- Avoid due dates unless there is a real external or internal commitment.
- Review blocked, aging, and repeatedly carried-over work.

### Useful Jira views

- roadmap or plan grouped by outcome or epic;
- Scrum or Kanban board for current delivery;
- bugs by severity and age;
- blocked dependencies;
- release readiness;
- cycle-time and cumulative-flow trends.

Jira reports explain delivery flow; product analytics explains user behavior. Do not use ticket completion as a proxy for customer value.

## A connected Jira and Confluence workflow

1. Capture raw feedback in the appropriate source tool.
2. Synthesize evidence into an opportunity page in Confluence.
3. Record the strategy and prioritization decision.
4. Create a Jira epic linked to the approved product brief.
5. Link designs, technical decisions, and experiment plans.
6. Deliver small stories or tasks through the team's workflow.
7. Validate analytics and launch readiness.
8. Record results and the scale, iterate, hold, or stop decision.
9. Update the roadmap and archive superseded assumptions.

This preserves the trace:

```text
Evidence → opportunity → decision → delivery → release → result
```

## Roadmapping tools

Use a dedicated roadmap tool when multiple products, segments, evidence sources, or portfolio views exceed a simple document. Configure it around outcomes and opportunities before importing a feature backlog.

Useful capabilities include:

- linking evidence to opportunities;
- comparing prioritization criteria and confidence;
- grouping work by objective, segment, or theme;
- publishing audience-specific roadmap views;
- syncing approved delivery work with Jira;
- recording assumptions and result metrics.

Avoid maintaining two independent priority lists in the roadmap tool and Jira. Define when an item moves between discovery and committed delivery and which system owns each stage.

## Research, design, and analytics connections

- Store interview recordings and sensitive research with appropriate consent and access.
- Publish synthesized findings and link the underlying evidence.
- Link Figma designs to the relevant product brief and Jira items.
- Keep event definitions and metric formulas in a shared data catalog or measurement plan.
- Link dashboards and experiment results back to the decision they inform.
- Record when evidence is outdated or applies only to a specific segment.

## Automation guidelines

Automation can synchronize approved roadmap items, notify owners, connect pull requests, or create standard launch tasks. Use it carefully:

- define the source of truth;
- document field mapping and ownership;
- prevent update loops and silent overwrites;
- test permissions and failure cases;
- periodically remove unused rules.

Automation should reduce duplicate entry, not spread low-quality data faster.

## Tool selection checklist

Evaluate:

- fit with the team's actual decision and delivery process;
- integration with source control, support, design, and analytics;
- search, linking, templates, history, and export;
- access control, data residency, compliance, and audit needs;
- accessibility and usability for all contributors;
- reporting quality and API availability;
- licensing plus administration and migration cost;
- vendor lock-in and data portability.

Pilot the workflow with one team and a small set of artifacts. Measure whether people find current context faster, make decisions with better evidence, and spend less time duplicating status.

## Documentation anti-patterns

- PRDs become fixed contracts rather than decision records.
- Strategy lives in slides that delivery teams cannot find.
- Jira contains hundreds of unsorted requests labeled as priorities.
- Confluence has duplicate pages with no owner or review date.
- Product decisions disappear in chat.
- Roadmaps promise dates that delivery plans cannot support.
- Dashboards report feature output without adoption or retention.

**Related:** [Jira, Confluence, and delivery tools](../project-manager101/x-jira-confluence-and-delivery-tools.md).

**Next:** [Product manager vs project manager](xii-product-manager-vs-project-manager.md).
