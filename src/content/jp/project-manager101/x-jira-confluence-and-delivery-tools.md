---
label: "X"
subtitle: "Jira, Confluence, and delivery tools"
group: "Project Manager 101"
order: 10
---
Jira, Confluence, and delivery tools
Tools should make decisions, ownership, work, and evidence easier to find. They cannot repair unclear priorities or a broken delivery process. Design the workflow first, then configure the smallest toolset that supports it.

## Separate systems of record

| Information | Best home |
|-------------|-----------|
| Work status, owner, priority, and workflow | Jira or another work tracker |
| Project brief, requirements, decisions, meeting notes, and runbooks | Confluence or another knowledge base |
| Source code and technical changes | GitHub, GitLab, or Bitbucket |
| Real-time conversation | Slack or Microsoft Teams |
| Product and operational metrics | Analytics and observability tools |

Chat is useful for coordination but weak as a permanent record. Move decisions and durable context into the appropriate system of record.

## Jira concepts

Jira supports multiple project configurations and customizable issue types. A common hierarchy is:

```text
Initiative or objective
  → Epic
    → Story or task
      → Subtask
```

Bugs may sit alongside stories and tasks. Use the hierarchy only when each level answers a real planning question.

### Useful issue fields

- clear summary and description;
- owner and team;
- priority based on agreed policy;
- acceptance criteria or completion conditions;
- parent or epic;
- release, milestone, or sprint where relevant;
- dependencies and linked issues;
- labels or components with controlled meanings;
- due date only when a real commitment exists.

Avoid making every field mandatory. Excess fields create stale data and encourage users to bypass the process.

### Workflow design

A minimal software workflow may be:

```text
Backlog → Ready → In progress → Review/Test → Done
```

Define entry and exit policies for each state. Add states only when they change ownership, policy, or a decision. “Blocked” is often better represented by a flag plus a reason, because blocked work still belongs to a workflow state.

### Boards and backlogs

- Use a Scrum board when the team plans with sprints and sprint goals.
- Use a Kanban board when work flows continuously.
- Configure columns to reflect the real workflow.
- Set work-in-progress limits where congestion matters.
- Use quick filters for team, service, risk, or work type.
- Keep the backlog ordered and remove obsolete items.

### Dashboards

A useful dashboard answers a management question:

- milestone and release forecast;
- blocked and aging work;
- cumulative flow or cycle-time trend;
- unresolved high-impact risks or defects;
- sprint goal progress;
- workload by team when capacity decisions are needed.

Avoid dashboards built from vanity counts such as tickets created or story points completed without outcome and quality context.

## Confluence structure

Use a predictable space hierarchy:

```text
Project home
  ├── Brief, outcomes, scope, and stakeholders
  ├── Roadmap and milestone plan
  ├── Requirements and design links
  ├── RAID and decision logs
  ├── Meeting notes
  ├── Status reports
  ├── Launch or handover
  └── Retrospective and archive
```

The project home should show the owner, current status, next milestone, important links, and last update date.

### Documentation practices

- Use templates for recurring artifacts, not every page.
- Put an owner and review date on important pages.
- Link to one source instead of copying the same information.
- Record decisions with context, options, rationale, and consequences.
- Archive superseded pages and label their replacement.
- Restrict confidential information and review access periodically.
- Use page history for auditability, but summarize material changes.

## Connect Jira and Confluence

Link requirements and decisions to the Jira epic or work item they affect. Embed filtered Jira views in a Confluence project page when readers need current status. Link Jira releases to release notes and readiness pages.

Maintain one source for each fact:

- Jira owns current work state.
- Confluence owns narrative context and decisions.
- The repository owns code and versioned technical documentation.

Do not manually copy ticket status into several weekly documents. Generate or embed status where possible, then write the interpretation and decisions.

## Automation and integrations

Useful automations include:

- notify an owner when work becomes blocked or stale;
- update a ticket from a pull-request merge or deployment event;
- require critical fields before entering a controlled state;
- create standard subtasks for repeatable compliance or launch work;
- send release or incident updates to the correct channel.

Start with a small number of observable automations. Document ownership and failure behavior; silent automation can create misleading data.

## Other tool options

| Need | Examples |
|------|----------|
| Work tracking | Linear, Azure DevOps Boards, GitHub Projects, Asana, Trello |
| Knowledge base | Notion, SharePoint, Google Workspace, Slite |
| Whiteboarding | Miro, FigJam |
| Product roadmaps | Productboard, Aha!, Jira Product Discovery |
| Team communication | Slack, Microsoft Teams |
| Reporting | Power BI, Tableau, Looker Studio |

Select tools based on workflow fit, integrations, permissions, reporting, audit needs, administration cost, accessibility, and exit/export options—not feature count alone.

## Governance checklist

- Name a business owner and tool administrator.
- Define project, space, naming, and permission standards.
- Keep workflows and fields intentionally minimal.
- Review inactive projects, stale pages, automations, and access.
- Train users on the working agreement, not just button clicks.
- Measure whether the tools reduce search time, delays, and duplicate reporting.

**Related:** [Product documentation and tools](../product-manager101/xi-product-documentation-and-tools.md).

**Back to:** [Project Manager 101 overview](i-overview.md).
