---
label: "IV"
subtitle: "Gancho – segredos e verificação de ambiente"
group: "Skills examples"
order: 4
---
Gancho – segredos e`.env`digitalizar

**Objetivo:** Um **bot** que roda em **hooks** — antes da execução do shell`git commit`- e verifica segredos expostos,`.env`arquivos preparados, chaves API em diffs. Grava um **log**; pode **bloquear** a ação quando`failClosed`está definido.

Os ganchos são executados **automaticamente**; habilidades são executadas quando o usuário pergunta. Consulte [Vinculando um script fixo](../../iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script).

## Arquivos ativos (prontos para cópia)

| Arquivo | Caminho |
|------|------|
| Configuração do gancho | [`.cursor/hooks.json`](.cursor/hooks.json) |
| Script de gancho | [`.cursor/hooks/secrets_scan.py`](.cursor/hooks/secrets_scan.py) |
| Lógica de varredura | [`.cursor/hooks/lib/scan_staged_secrets.py`](.cursor/hooks/lib/scan_staged_secrets.py) |
| Pré-comprometer CLI | [`.cursor/hooks/lib/scan_staged_secrets_cli.py`](.cursor/hooks/lib/scan_staged_secrets_cli.py) |
| Habilidade de ajuda | [`.cursor/skills/secrets-scan-help/SKILL.md`](.cursor/skills/secrets-scan-help/SKILL.md) |

Copie tudo [`.cursor/`](.cursor/README.md) para a raiz do seu projeto.

## Layout de pasta

```text
.cursor/
  hooks.json
  hooks/
    secrets_scan.py
    lib/
    logs/
```

## Configuração do gancho

Ver [`.cursor/hooks.json`](.cursor/hooks.json) -`beforeShellExecution`sobre`git\s+commit`,`failClosed: true`.

Teste manualmente:

```bash
echo '{"command":"git commit -m test"}' | python3 .cursor/hooks/secrets_scan.py
```

## Opcional: git pré-commit

```bash
chmod +x .cursor/hooks/lib/scan_staged_secrets_cli.py
# .git/hooks/pre-commit → exec python3 .cursor/hooks/lib/scan_staged_secrets_cli.py
```

## Fluxo de agente/usuário

```text
User or agent: git commit -m "…"
  → beforeShellExecution fires
  → secrets_scan.py runs → writes log
  → exit 2 → commit blocked (if failClosed)
  → secrets-scan-help skill → read log → suggest fixes
```

## Próximo

[Desempenho e gargalos](v-performance-bottleneck-scan.md) — habilidade de criação de perfil sob demanda.
