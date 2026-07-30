---
label: "I"
subtitle: "Visão geral"
group: "Criptomoedas 101"
order: 1
---
Criptomoeda101 — visão geral
**Cryptocurrency101** apresenta **redes blockchain**, como **as transações são armazenadas**, **tipos de blockchains** e um padrão recorrente de contrato inteligente de **divisão de taxas** em **BNB**, **Tron**, **TON** e **Cardano**.

Este curso é **conceitual e educacional**, não um aconselhamento financeiro. Os contratos mostrados são **esboços mínimos** — auditoria e teste antes do uso da rede principal.

## Mapa desta trilha

| Parte | Foco |
|------|--------|
| **I — Visão geral** | Esta página — mapa de trilhas, pré-requisitos, segurança |
| **II — O que é criptomoeda?** | Chaves, moedas versus tokens, contratos inteligentes |
| **III — Como as transações são armazenadas** | Blocos, cadeia, mempool, UTXO vs conta |
| **IV — Tipos de blockchains** | L1/L2, consenso, EVM vs eUTXO |
| **V — Padrão de divisão de taxas** | Compartilhado`feeBps`/tesouraria/regra do destinatário |
| **VI — Implantação e hospedagem** | Implantação na cadeia, sem hospedagem VPS |
| **VII — Transações e fundos com falha** | Reverte, gás, saldo insuficiente |
| **VIII — Verifique antes da transmissão** | Compilar, simular, testnet, canário |
| **IX — Verifique se está seguro e concluído** | Exploradores, confirmações, por rede |

## Exemplos

| Exemplo | Foco |
|--------|--------|
| [Visão geral dos exemplos](examples/i-overview.md) | Instruções de implantação com divisão de taxa de 2% |
| [Tron – divisão de taxas de 2%](examples/ii-tron-two-percent-fee-split.md) | Solidez + TronBox, projeto completo |
| [TON — divisão de taxas de 2%](examples/iii-ton-two-percent-fee-split.md) | Tato + Blueprint, projeto completo |

## Redes (submenu)

| Submenu | Rede | VM / modelo | Idioma do contrato |
|--------|---------|------------|--------|
| [BNB Cadeia](networks/bnb/i-overview.md) | BNB Cadeia Inteligente (BSC) | EVM | **Solidez** |
| [Tron](networks/tron/i-overview.md) | Tron | TVM (EVM-como) | **Solidez** |
| [TON](networks/ton/i-overview.md) | A Rede Aberta | TON VM | **FunC** / **Tato** |
| [Cardano (ADA)](networks/ada/i-overview.md) | Cardano | eUTXO | **Aiken** / **Plutus** |

Comece com os fundamentos: [O que é criptomoeda?](ii-what-is-cryptocurrency.md) → [Como as transações são armazenadas](iii-how-transactions-are-stored.md) → [Tipos de blockchains](iv-types-of-blockchains.md).

## Pré-requisitos

| Tópico | Onde |
|-------|--------|
| Hashing, assinaturas (intuição) | [Cibersegurança](../cybersecurity/i-overview.md) |
| Programação geral | [SWE101](../swe101/i-overview.md) |

## Notas de segurança

| Risco | Mitigação |
|------|------------|
| **Reentrância** (EVM) | Verificações-efeitos-interações; uso cuidadoso de`call`|
| **Arredondamento inteiro** | Pontos base; documento arredondando para zero |
| **Chaves de administrador** | Separado do destinatário da taxa; multisig em produção |
| **Regulamento** | As taxas e a custódia podem ser regulamentadas — revisão jurídica |

Guias de verificação completos: [Verificar antes da transmissão](viii-verify-before-broadcast.md) · [Verifique se está seguro e concluído](ix-verify-safe-and-completed.md).

## Próximo

1. [O que é criptomoeda?](ii-what-is-cryptocurrency.md)  
2. Ou pule para uma rede: [BNB Chain](networks/bnb/i-overview.md) (Solidity, EVM) — mais próximo dos tutoriais do Ethereum.
