# Briefing do agente – este repositório

Breves fatos que toda sessão de agente deveria saber. Os procedimentos vivem em`.cursor/skills/`.

## Pilha

- Repositório de conteúdo/markdown (notas educacionais)
- Python 3.10+, por exemplo, scripts em`.cursor/skills/`

## Comandos

| Tarefa | Comando |
|------|---------|
| Habilidade de implantação de teste de fumaça |`python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run`|
| Execute testes (se o pacote existir) |`npm test`|

##Layout

```text
src/content/en/     ← English notes
.cursor/skills/     ← on-demand workflows (user asks)
.cursor/hooks/      ← automatic commit gates
AGENTS.md           ← this file (always loaded)
```

## Habilidades (sob demanda)

| Habilidade | Quando |
|-------|------|
|`pr-review-lite`| Usuário solicita PR / revisão de código |
|`deploy-check`| O usuário pergunta sobre a preparação para implantação |
|`secrets-scan-help`| Commit bloqueado por gancho de segredos |
|`hook-failure-help`| Usuário pergunta por que um gancho bloqueou uma ação |

## Ganchos (automáticos)

- **`beforeShellExecution`** sobre`git commit`→`.cursor/hooks/secrets_scan.py`blocos encenados`.env`e segredos óbvios.
- Hooks são executados **sem** prompt do usuário. Usar`secrets-scan-help`habilidade para explicar falhas.

## Convenções

- Não se comprometa`.cursor/skills/*/logs/`ou`.cursor/hooks/logs/`- Não coloque chaves API reais no markdown - use espaços reservados