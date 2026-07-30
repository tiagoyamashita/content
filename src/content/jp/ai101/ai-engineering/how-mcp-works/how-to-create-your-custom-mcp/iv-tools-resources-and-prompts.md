---
label: "IV"
subtitle: "Tools, resources & prompts"
group: "How to create your custom MCP"
order: 4
---
Tools, resources & prompts

## 1. Tool design rules

| Rule | Why |
|------|-----|
| **Verb-first names** | `create_ticket`, `list_deployments` — clear intent for the LLM |
| **Rich descriptions** | Host shows name + description when picking tools — include “use when…” |
| **Small inputs** | Prefer `id` + `limit` over huge nested blobs |
| **Bounded output** | Truncate lists (top 10–50); summarize large payloads |
| **Explicit read/write** | Description: “Read-only” or “Creates a record — requires user confirmation in UI” |

### Input validation

Use **Zod** (TypeScript) or type hints (FastMCP) so bad arguments fail **before** your API call:

```typescript
{
  issue_id: z.string().uuid(),
  comment: z.string().max(4000),
  dry_run: z.boolean().optional().default(false),
}
```

Return validation errors as tool results with `isError: true` so the model can retry.

## 2. Tool result shape

MCP tools return **content** blocks — usually text:

```typescript
return {
  content: [
    { type: "text", text: "Found 3 open incidents:\n1. ..." },
  ],
};
```

| Content type | Use |
|--------------|-----|
| `text` | JSON as formatted string, human summaries, logs |
| `image` | Base64 or URL (when host supports it) |
| `resource` | Reference to a resource URI |

For structured data, **JSON.stringify** into text is fine — the model parses it on the next turn.

### Errors the model can fix

```typescript
return {
  content: [{ type: "text", text: "Error: Project 'foo' not found. Use list_projects first." }],
  isError: true,
};
```

Avoid stack traces in production — log server-side, return short messages.

## 3. Resources (optional)

Resources expose **readable** content by URI — good for runbooks, config snippets, cached exports.

TypeScript (conceptual):

```typescript
server.resource(
  "runbook://checkout-failures",
  "Runbook for checkout payment failures",
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: "text/markdown",
        text: await loadRunbook("checkout-failures"),
      },
    ],
  }),
);
```

| Tools | Resources |
|-------|-----------|
| Model **invokes** with parameters | Model or user **reads** by URI |
| Search, create, mutate | Static or slowly changing docs |

## 4. Prompts (optional)

Prompts are **named templates** with arguments — like slash commands:

```typescript
server.prompt(
  "incident-summary",
  { incident_id: z.string() },
  async ({ incident_id }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Summarize incident ${incident_id} using get_incident and list_timeline events.`,
        },
      },
    ],
  }),
);
```

Most custom servers skip prompts until tools are stable.

## 5. Multiple related tools — example set

| Tool | Type | Description snippet |
|------|------|---------------------|
| `list_projects` | Read | List projects user can access. Call before other project tools. |
| `get_issue` | Read | Fetch one issue by id. |
| `search_issues` | Read | Search by query string; max 20 results. |
| `add_comment` | Write | Add comment to issue — destructive. |

Ordering hints in descriptions (`Call list_projects first`) improve multi-step agent runs.

## 6. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| One tool that runs arbitrary SQL | Parameterized queries or fixed report ids |
| `run_shell` with full bash | Never — or strictly allowlisted commands in a sandbox |
| Returning 10 MB JSON | Paginate, summarize server-side |
| Tool names that differ only by case | Stick to snake_case |

See [Security & distribution](vi-security-and-distribution.md) and [MCP vs connectors & security](../iv-mcp-vs-connectors-and-security.md).

## Next

[Test & wire into Cursor](v-test-and-wire-cursor.md) — run the server in an IDE.
