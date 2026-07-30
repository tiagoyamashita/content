---
label: "II"
subtitle: "Choose stack & scaffold"
group: "How to create your custom MCP"
order: 2
---
Choose stack & scaffold

Pick **TypeScript** or **Python** — both have official MCP SDKs. For most IDE teams already on Node, **TypeScript** matches Cursor examples; **Python** is fastest if your logic is already in Python scripts or data libs.

## 1. Stack comparison

| | **TypeScript** | **Python (FastMCP)** |
|---|----------------|----------------------|
| **Package** | `@modelcontextprotocol/sdk` | `mcp` (`FastMCP`) |
| **Runtime** | Node 18+ | Python 3.10+ |
| **Schema** | Zod | Type hints / Pydantic |
| **Best when** | JS/TS monorepo, npm publish | Data/ML scripts, FastAPI teams |
| **Cursor spawn** | `node dist/index.js` | `python server.py` or `uv run` |

Start with **stdio** transport — one subprocess, no open ports. Add HTTP later only if you need a remote team-hosted server.

## 2. TypeScript scaffold

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init --module NodeNext --moduleResolution NodeNext --outDir dist --rootDir src
```

**`package.json`** — add bin entry for Cursor:

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": { "my-mcp-server": "./dist/index.js" },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

**Layout:**

```text
my-mcp-server/
├── src/
│   ├── index.ts       # server entry + transport
│   └── tools/         # one file per domain (issues.ts, users.ts)
├── package.json
└── tsconfig.json
```

## 3. Python scaffold

```bash
mkdir my-mcp-server && cd my-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install mcp
```

**Layout:**

```text
my-mcp-server/
├── server.py          # FastMCP entry
├── tools/
│   └── tickets.py     # optional split
├── pyproject.toml     # optional — uv/poetry
└── .venv/
```

With **uv** (recommended for reproducible spawns):

```bash
uv init my-mcp-server
uv add mcp
```

## 4. Naming and versioning

| Field | Guidance |
|-------|----------|
| **Server `name`** | Short snake-case id: `acme-tickets`, not `My Cool Server` |
| **Version** | Semver in server metadata — helps debug which build Cursor launched |
| **Tool names** | Verb + noun: `search_tickets`, `create_ticket` — stable across releases |

Hosts show tool names to the model; renames break agent habits — treat tool names like a small public API.

## 5. Environment and secrets

Never hard-code tokens. Read from env vars the host passes in `mcp.json`:

```json
"env": {
  "ACME_API_TOKEN": "…",
  "ACME_BASE_URL": "https://api.internal.example"
}
```

In code: `process.env.ACME_API_TOKEN` (TS) or `os.environ["ACME_API_TOKEN"]` (Python). Fail fast at startup if required vars are missing.

## Next

[Define tools & resources](iii-define-tools-and-resources.md) — design what the agent can call before writing handlers.
