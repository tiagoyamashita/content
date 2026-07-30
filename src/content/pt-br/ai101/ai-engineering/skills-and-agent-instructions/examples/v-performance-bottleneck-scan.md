---
label: "V"
subtitle: "Desempenho e gargalos"
group: "Skills examples"
order: 5
---
Desempenho e gargalos

**Objetivo:** um bot **acionado por habilidade** que verifica **problemas de desempenho** — arquivos grandes, heurística I/O de sincronização, tempo HTTP opcional — e registra **tempo de execução + descobertas** para o agente resumir e sugerir correções.

## Arquivos ativos (prontos para cópia)

| Arquivo | Caminho |
|------|------|
| Instruções de habilidade | [`.cursor/skills/perf-scan/SKILL.md`](.cursor/skills/perf-scan/SKILL.md) |
| Roteiro | [`.cursor/skills/perf-scan/scripts/perf_scan.py`](.cursor/skills/perf-scan/scripts/perf_scan.py) |

## Layout de pasta

```text
.cursor/skills/perf-scan/
  SKILL.md
  scripts/perf_scan.py
  logs/
```

## Correr

```bash
PERF_URL="${PERF_URL:-}" python3 .cursor/skills/perf-scan/scripts/perf_scan.py "."
```

Fluxo do agente: perguntar escopo → confirmar → executar → ler log → priorizar as três principais descobertas.

## Combine com exemplo de loop

[Loop nos resultados do script](iii-loop-on-script-results.md) — registro de linha de base, corrigir, executar novamente, comparar`findings_count`.

## Relacionado

- [Script parametrizado + esclarecimento](ii-parameterized-script-clarify.md)
- [Visão geral dos exemplos](i-overview.md)
