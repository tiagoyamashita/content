---
label: "III"
subtitle: "Loop nos resultados do script"
group: "Skills examples"
order: 3
---
Loop nos resultados do script

**Objetivo:** executar um script, ler seu **arquivo de log** e **iterar** os mesmos dados — refinar correções ou análises sem buscar novamente do zero todas as vezes. Mantém`current_log_file`na conversa como fonte da verdade.

## Arquivos ativos (prontos para cópia)

| Arquivo | Caminho |
|------|------|
| Instruções de habilidade | [`.cursor/skills/test-flake-hunt/SKILL.md`](.cursor/skills/test-flake-hunt/SKILL.md) |
| Roteiro | [`.cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py`](.cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py) |

## Layout de pasta

```text
.cursor/skills/test-flake-hunt/
  SKILL.md
  scripts/run_flaky_tests.py
  logs/
```

## Padrão de loop (de SKILL.md)

1. **Rodada 1** – corrida`python3 .cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py "[pattern]"`2. Loja`current_log_file`da saída do script.
3. **Rodada 2+** — leia o mesmo registro; propor correção; execute novamente apenas para verificar.
4. **Pare** em`exit_code == 0`, parada do usuário ou 5 iterações sem progresso.

## Opcional: Cursor`stop`gancho

Para loops automáticos de “continuação”, use um`stop`gancho com`loop_limit`— veja [Gancho — verificação de segredos](iv-hook-secrets-env-scan.md). As habilidades por si só dependem do agente seguir o ciclo`SKILL.md`.

## Ligação

[Aviso de loop](../../loop-prompting/i-overview.md) — deltas curtos a cada turno (“iteração 3: ler o último log, corrigir`auth.test.ts`”).

## Próximo

[Gancho – segredos e`.env`digitalizar](iv-hook-secrets-env-scan.md) — verificações automáticas sem solicitação do usuário.
