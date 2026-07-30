---
label: "VIII"
subtitle: "Verifique antes da transmissão"
group: "Criptomoedas 101"
order: 8
---
Cryptocurrency101 — Parte VIII: Verifique antes da transmissão
Capture a maioria dos erros de lógica e configuração **antes** de pagar as taxas da mainnet: **compilar → testar → simular → testnet → mainnet**.

Você não pode garantir **zero** falhas (congestionamento, bugs de carteira, MEV), mas tudo o que resta do **Broadcast** nos diagramas abaixo é **gratuito ou barato para testnet**.

## 1. Sequência de ponta a ponta

```plantuml
@startuml
title Deploy + pay — full flow with verification gates
actor Developer as DEV
actor User as USER
participant "Local toolchain\n(Hardhat / Blueprint / Aiken)" as LOCAL
participant "Testnet" as TEST
participant "Mainnet" as MAIN
participant "FeeSplitter\n(on-chain)" as SC

== Build & verify (off-chain, no chain fee) ==
DEV -> LOCAL: write contract + tests
LOCAL -> LOCAL: compile / build
alt compile error
  LOCAL --> DEV: fix syntax — STOP
end
LOCAL -> LOCAL: unit tests (fee math, zero address)
alt tests fail
  LOCAL --> DEV: fix logic — STOP
end

== Deploy to testnet ==
DEV -> LOCAL: estimate deploy gas / energy / fee
LOCAL --> DEV: show cost preview
DEV -> TEST: broadcast deploy tx
alt deploy reverts / out of gas
  TEST --> DEV: pay testnet fee only — fix & retry
end
TEST --> DEV: contract address

== Simulate pay (before user touches mainnet) ==
DEV -> LOCAL: eth_call / dry-run / cardano build
LOCAL --> DEV: success OR revert reason
alt simulation revert
  LOCAL --> DEV: fix require / datum — STOP
end
DEV -> TEST: pay(recipient) with test coins
TEST -> SC: execute
SC --> DEV: verify feeAccount + recipient balances

== Mainnet (small amount first) ==
DEV -> MAIN: deploy (if not already)
DEV -> MAIN: pay(recipient, tiny amount)
MAIN -> SC: execute
alt success
  SC --> USER: ready for production traffic
else revert
  MAIN --> DEV: post-mortem via explorer
end
@enduml
```

## 2. Lista de verificação pré-voo

| Etapa | O que você verifica | Ferramenta / como | Falha antes da cadeia? |
|------|-----------------|------------|---------------------|
| **1. Compilar** | Sintaxe, tipos, tamanho do bytecode |`hardhat compile`,`blueprint build`,`aiken build`| **Sim** |
| **2. Testes unitários** | Taxa matemática, endereço zero rejeitado | Capacete de segurança, fundição, Aiken | **Sim** |
| **3. Análise estática** | Reentrada, transbordamento | Slither, Mythril (opcional) | **Sim** |
| **4. Revisão de configuração** |`feeAccount`,`feeBps ≤ 10000`| Revisão de código | **Sim** |
| **5. Simular chamada** | Tx teria sucesso sem enviar |`eth_call`,`triggerConstantContract`,`cardano-cli build`| **Sim** |
| **6. Estimar custo** | Moeda nativa suficiente + margem de gás |`estimateGas`, estimativa de energia | **Sim** |
| **7. Carteira / nonce** | Rede correta, equilíbrio | MetaMask, TronLink, Tonkeeper | **Sim** se bloqueado |
| **8. Rede de teste E2E** | Implantar +`pay()`+ saldos | BSC testnet, Shasta, pré-produção | Barato |
| **9. Canário da rede principal ** | Um pequeno real`pay()`| Explorador da rede principal | Custa taxa real |

## 3. Simulação EVM (BNB / Tron)

```plantuml
@startuml
title EVM — verify pay() before broadcast
actor Developer
participant Wallet
participant RPC
participant "FeeSplitter" as SC

Developer -> RPC: eth_call pay(recipient)\n{ value: amount }
RPC -> SC: execute (not mined)
alt require fails
  SC --> RPC: revert + reason
  RPC --> Developer: fix — no mainnet fee
else success
  RPC --> Developer: simulation OK
  Developer -> RPC: eth_estimateGas
  Developer -> Wallet: sign & send (+ 10% gas buffer)
end
@enduml
```

```javascript
// Hardhat / ethers — dry-run before send
await contract.pay.staticCall(recipient, { value: amount });
const gas = await contract.pay.estimateGas(recipient, { value: amount });
await contract.pay(recipient, { value: amount, gasLimit: gas * 110n / 100n });
```

## 4. Ferramentas por rede

| Rede | Simular/ensaio | Rede de teste | Explorador |
|---------|-------------------|---------|----------|
| [BNB](networks/bnb/i-overview.md) |`eth_call`,`staticCall`, Fundição | BSC rede de teste | BscScan |
| [Tron](networks/tron/i-overview.md) |`triggerConstantContract`| Shasta / Nilo | Tronscan |
| [TON](networks/ton/i-overview.md) | Projeto,`@ton/sandbox`| TON rede de teste | Visualizador de tons |
| [ADA](networks/ada/i-overview.md) |`cardano-cli transaction build`, Lúcido | Pré-produção/visualização | Cardanoscan |

## 5. Motivos comuns de reversão (FeeSplitter)

| Verificação do contrato | Erro do usuário | Simulação pega? |
|----------------|-------------|---------------------|
|`msg.value > 0`| Envia 0 moeda nativa | **Sim** |
|`recipient != address(0)`| Endereço zero | **Sim** |
|`payOk`/falha na transferência | Destinatário rejeita | **Sim** na testnet |
| Sem gás | Limite de gás muito baixo | **estimateGas** ajuda |
| Rede errada | Rede principal vs rede de teste | Carteira UI |
| Saldo insuficiente | Valor + gás | **Muitas vezes antes** da transmissão — [Parte VII](vii-failed-transactions-and-funds.md) |

## 6. Portas de decisão

```plantuml
@startuml
title Should I broadcast this transaction?
start
:Compile & unit tests;
if (All pass?) then (yes)
else (no)
  :Fix code;
  stop
endif
:Simulate / constant call;
if (Success?) then (yes)
else (no)
  :Read revert reason;
  stop
endif
:Estimate fee & check balance;
if (balance >= pay amount + gas?) then (yes)
else (no)
  :Top up wallet;
  stop
endif
if (First time on mainnet?) then (yes)
  :Run on testnet E2E;
endif
:Broadcast;
if (Receipt success?) then (yes)
  :Verify on explorer;
else (no)
  :Debug — fee may still be spent;
endif
stop
@enduml
```

## 7. Relacionado

- **Parte VII** — [Transações e fundos com falha](vii-failed-transactions-and-funds.md)
- **Parte IX** — [Verifique se está seguro e concluído](ix-verify-safe-and-completed.md)
- **Parte VI** — [Implantação e hospedagem](vi-deploy-pricing-and-hosting.md)
