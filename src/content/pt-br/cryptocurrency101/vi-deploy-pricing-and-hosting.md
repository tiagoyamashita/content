---
label: "VI"
subtitle: "Implantar e hospedar"
group: "Criptomoedas 101"
order: 6
---
Cryptocurrency101 — Parte VI: Implantação e hospedagem
Contratos inteligentes **vivem no blockchain** — replicados em nós da rede. Você **não** hospeda bytecode em um VPS. Você paga **uma vez para implantar** e depois **gás por transação**. Um site ou API é opcional.

## 1. Onde reside o contrato

```text
Your laptop / CI  ──deploy tx──►  Blockchain nodes  ──►  contract address
                                         │
                                    no server bill
                                    for "hosting"
```

| Custo | Quando |
|------|------|
| **Implantar** | Gás único para armazenar bytecode |
| **Por chamada** | Usuários ou você paga quando`pay()`corre |
| **Servidor** | **Opcional** — apenas para construtor de site/tx UI |

## 2. Preço de implantação (aproximado)

**USD varia de acordo com o preço da moeda e a carga da rede** — apenas ordem de grandeza; simule primeiro no testnet.

| Rede | O que você paga | Contrato simples (por exemplo, FeeSplitter) | Rede de teste |
|---------|----------|--------------------------|---------|
| [BNB Cadeia](networks/bnb/i-overview.md) | BNB gás | ~**$0,50 – $5** rede principal | BNB grátis da torneira |
| [Tron](networks/tron/i-overview.md) | TRX (energia/largura de banda) | ~**$5 – $40** rede principal | TRX grátis em Shasta/Nilo |
| [TON](networks/ton/i-overview.md) | TON (armazenamento + computação) | ~**$0,50 – $5** rede principal | TON grátis da torneira |
| [Cardano (ADA)](networks/ada/i-overview.md) | ADA taxa de transferência + min UTXO | ~**$2 – $15** rede principal | ADA grátis da torneira |

| Custo contínuo | Servidor necessário? |
|--------------|------------------|
| **Nenhum** para “hospedar” o contrato | **Não** — a rede executa bytecode |
| **Por chamada** — gás quando`pay()`corre | Servidor opcional apenas para site |

Detalhes e fórmulas de estimativa: cada [página da rede](networks/bnb/i-overview.md).

## 3. Lista de verificação de implantação do desenvolvedor

| Etapa | Ação |
|------|--------|
| 1 | Compilar no conjunto de ferramentas da rede de destino |
| 2 | Taxa de teste unitário matemática e verificações de endereço zero |
| 3 | Implantar em **testnet** |
| 4 | Executar teste`pay()`com moedas de torneira |
| 5 | Implantação da rede principal + pequeno canário`pay()`|

Fluxo de verificação completo: [Verificar antes da transmissão](viii-verify-before-broadcast.md).

## 4. Relacionado

- **Parte V** — [Padrão de divisão de taxas](v-fee-split-pattern.md)
- **Parte VIII** — [Verificar antes da transmissão](viii-verify-before-broadcast.md)
