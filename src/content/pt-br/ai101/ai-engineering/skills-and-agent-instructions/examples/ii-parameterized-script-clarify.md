---
label: "II"
subtitle: "Script parametrizado + esclarecimento"
group: "Skills examples"
order: 2
---
Script parametrizado + esclarecimento

**Objetivo:** executar um script com **parâmetros** (`environment`,`dry_run`, etc.). Se o usuário não forneceu informações suficientes, o agente **pede** valores ausentes e **confirma a intenção** antes de executar. O script **registra** o tempo de execução e os resultados em JSON.

## Arquivos ativos (prontos para cópia)

| Arquivo | Caminho |
|------|------|
| Instruções de habilidade | [`.cursor/skills/deploy-check/SKILL.md`](.cursor/skills/deploy-check/SKILL.md) |
| Roteiro | [`.cursor/skills/deploy-check/scripts/deploy_check.py`](.cursor/skills/deploy-check/scripts/deploy_check.py) |
| Ajudante de registro | [`.cursor/skills/deploy-check/scripts/lib/run_log.py`](.cursor/skills/deploy-check/scripts/lib/run_log.py) |

Copie tudo [`.cursor/`](.cursor/README.md) para o seu projeto — caminhos já usados`.cursor/skills/...`.

## Layout de pasta

```text
.cursor/skills/deploy-check/
  SKILL.md
  scripts/
    lib/run_log.py
    deploy_check.py
  logs/                    ← gitignore; created at runtime
```

## O que a habilidade ensina ao agente

De [`SKILL.md`](.cursor/skills/deploy-check/SKILL.md):

1. **Pergunte** se`environment`está faltando (`staging`|`production`).
2. **Confirme** antes da execução — especialmente para produção.
3. **Correr**`python3 .cursor/skills/deploy-check/scripts/deploy_check.py …`4. **Leia** o log JSON em`logs/`e resumir`duration_ms`,`exit_code`,`messages`.

## Fluxo do agente

```text
User: "check if we're ready to deploy"
  → Skill loads
  → Agent: missing environment → asks user
  → Agent: restates command → user confirms
  → Agent runs script via Shell
  → Script writes logs/run-….json
  → Agent reads log → reports results
```

## Teste

Depois de copiar para o seu projeto:

```bash
python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run
```

Bate-papo com agente novo: *"run deploy check"* — o agente deve solicitar o ambiente antes de executar.

## Próximo

[Loop nos resultados do script](iii-loop-on-script-results.md) — reutilizar dados de log entre iterações.
