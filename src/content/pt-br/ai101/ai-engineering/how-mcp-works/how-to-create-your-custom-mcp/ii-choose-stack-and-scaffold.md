---
label: "II"
subtitle: "Escolha pilha e andaime"
group: "How to create your custom MCP"
order: 2
---
Escolha pilha e andaime

Escolha **TypeScript** ou **Python** — ambos têm SDKs MCP oficiais. Para a maioria das equipes IDE que já estão no Node, **TypeScript** corresponde aos exemplos Cursor; **Python** é mais rápido se sua lógica já estiver em scripts Python ou bibliotecas de dados.

## 1. Comparação de pilha

| | **TypeScript** | **Python (RápidoMCP)** |
|---|----------------|----------------------|
| **Pacote** |`@modelcontextprotocol/sdk`|`mcp`(`FastMCP`) |
| **Tempo de execução** | Nó 18+ | Python 3.10+ |
| **Esquema** | Zod | Dicas de tipo / Pydantic |
| **Melhor quando** | JS/TS monorepo, npm publicar | Scripts de dados/ML, equipes FastAPI |
| **Cursor geração** |`node dist/index.js`|`python server.py`ou`uv run`|

Comece com transporte **stdio** — um subprocesso, sem portas abertas. Adicione HTTP mais tarde somente se precisar de um servidor remoto hospedado pela equipe.

## 2. Estrutura TypeScript

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init --module NodeNext --moduleResolution NodeNext --outDir dist --rootDir src
```

(R)`package.json`** — adicione entrada bin para Cursor:

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

## 3. Andaime Python

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

Com **uv** (recomendado para spawns reproduzíveis):

```bash
uv init my-mcp-server
uv add mcp
```

## 4. Nomenclatura e controle de versão

| Campo | Orientação |
|-------|----------|
| **Servidor`name`** | ID curto do caso de cobra:`acme-tickets`, não`My Cool Server`|
| **Versão** | Semver nos metadados do servidor — ajuda a depurar qual build Cursor foi lançada |
| **Nomes de ferramentas** | Verbo + substantivo:`search_tickets`,`create_ticket`— estável entre versões |

Hosts mostram nomes de ferramentas para o modelo; renomeia os hábitos do agente de interrupção — trate os nomes das ferramentas como um pequeno API público.

## 5. Meio ambiente e segredos

Nunca codifique tokens. Leia do env vars que o host passa`mcp.json`TÉCNICO.:

```json
"env": {
  "ACME_API_TOKEN": "…",
  "ACME_BASE_URL": "https://api.internal.example"
}
```

No código:`process.env.ACME_API_TOKEN`(TS) ou`os.environ["ACME_API_TOKEN"]`(Python). Falha rapidamente na inicialização se faltarem vars necessários.

## Próximo

[Definir ferramentas e recursos](iii-define-tools-and-resources.md) — projete o que o agente pode chamar antes de escrever manipuladores.
