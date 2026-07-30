---
label: "I"
subtitle: "Visão geral"
group: "Skills examples"
order: 1
---
Exemplos de habilidades – visão geral

Quatro **padrões de copiar e colar** para habilidades, scripts e ganchos. Cada exemplo inclui:

-UM**`scripts/`** Arquivo Python (código real - não dentro`SKILL.md`)
- **Logs de tempo de execução estruturados** (carimbo de data/hora, duração, código de saída, resultados) por meio do stdlib`json`módulo
- Instruções para o agente sobre **o que fazer com a saída do log**

Os scripts **não** são incorporados no markdown — consulte [Onde os scripts ficam](../i-overview.md#where-scripts-live-not-inside-the-md).

Arquivos executáveis ​​ficam em **[`.cursor/`](.cursor/README.md)** — copie essa pasta para a raiz do seu projeto (veja [Copiar para seu projeto](#copy-to-your-project)).

## Copie para o seu projeto

```bash
cd src/content/en/ai101/ai-engineering/skills-and-agent-instructions/examples
chmod +x scripts/copy-to-project.sh
./scripts/copy-to-project.sh /path/to/your-project
```

Ou manualmente: copiar`examples/.cursor/skills/`,`examples/.cursor/hooks/`, e`examples/.cursor/hooks.json`→ seu repositório`.cursor/`. Não são necessárias edições de caminho —`SKILL.md`arquivos já usam`.cursor/...`.

Teste de fumaça:

```bash
python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run
```

## Por que Python (não bash)

| | **Python** | **festa** |
|---|------------|----------|
| JSON registros |`json.dump`- não`jq`| Heredocs + escapando de bugs |
| Argumentos |`argparse`| Manual`case`-&#09;o`getopts`|
| Analisando diferenças, AST, perf |`re`,`pathlib`,`ast`| Frágil`grep`-&#09;o`awk`|
| Ganchos | Leia stdin JSON, retorne dict | O mesmo, mas mais fácil de errar |
| Dep. | **somente stdlib** nestes exemplos | Muitas vezes precisa`jq`,`curl`|

Utilize **Python 3.10+**. Nenhum pacote pip é necessário para os exemplos abaixo.

## Mapa de exemplos

| Exemplo | Padrão | Gatilho |
|--------|---------|---------|
| [Script parametrizado + esclarecimento](ii-parameterized-script-clarify.md) | Passe argumentos; pergunte se está faltando; confirmar intenção | Habilidade (o usuário pede para executar a ferramenta) |
| [Loop nos resultados do script](iii-loop-on-script-results.md) | Reutilize os mesmos dados de registro; refinar entre iterações | Habilidade + loop de agente |
| [Gancho – segredos e`.env`digitalizar](iv-hook-secrets-env-scan.md) | Bloquear ou avisar antes de commit/shell | Cursor gancho |
| [Desempenho e gargalos](v-performance-bottleneck-scan.md) | Perfil/verificação; descobertas de registro | Habilidade |

## Auxiliar de registro compartilhado

Implementado em [`.cursor/skills/deploy-check/scripts/lib/run_log.py`](.cursor/skills/deploy-check/scripts/lib/run_log.py) (copiado em cada habilidade`scripts/lib/`). Mesmo módulo em`test-flake-hunt`e`perf-scan`.

## Formato de log compartilhado

```text
.cursor/skills/<skill-name>/logs/
  run-20260710T120301Z.json
.cursor/hooks/logs/
  secrets-scan-20260710T120405Z.json
```

```json
{
  "script": "deploy_check.py",
  "started_at": "2026-07-10T12:03:01Z",
  "finished_at": "2026-07-10T12:03:04Z",
  "duration_ms": 3120,
  "exit_code": 0,
  "parameters": { "environment": "staging", "dry_run": true },
  "results": { "checks_failed": 0 },
  "messages": ["Health OK"],
  "log_file": ".cursor/skills/deploy-check/logs/run-20260710T120301Z.json"
}
```

Adicionar`logs/`para`.gitignore`se as execuções forem apenas locais; commit **scripts** e **SKILL.md**, não arquivos de log efêmeros.

## Habilidade vs gancho (qual exemplo copiar)

| Necessidade | Copiar |
|------|------|
| O usuário invoca o fluxo de trabalho; pode precisar de parâmetros | [Script parametrizado + esclarecimento](ii-parameterized-script-clarify.md) |
| Iterar na mesma saída do script até que esteja bom o suficiente | [Loop nos resultados do script](iii-loop-on-script-results.md) |
| Verificação automática em commit/git/shell | [Gancho – verificação de segredos](iv-hook-secrets-env-scan.md) |
| Avaliação de desempenho sob demanda | [Verificação de desempenho](v-performance-bottleneck-scan.md) |

## Ordem de estudo

Leia [Script parametrizado + esclarecimento](ii-parameterized-script-clarify.md) primeiro (parâmetros + logs), depois [Loop nos resultados do script](iii-loop-on-script-results.md). Adicionar [Gancho – verificação de segredos](iv-hook-secrets-env-scan.md) quando você precisar de portões **automáticos**.

## Relacionado

- [Usando habilidades, agentes e ganchos](../using-skills-agents-and-hooks/i-overview.md) — quando usar cada camada separadamente
- [Vinculando um script fixo](../iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script)
- [Aviso de loop](../../loop-prompting/i-overview.md)
- [Como MCP funciona](../../how-mcp-works/i-overview.md) — dados ao vivo versus scripts estáticos
