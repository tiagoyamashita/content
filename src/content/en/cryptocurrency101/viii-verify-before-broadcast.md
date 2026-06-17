---
label: "VIII"
subtitle: "Verify before broadcast"
group: "Cryptocurrency101"
order: 8
---
Cryptocurrency101 — Part VIII: Verify before broadcast
Catch most logic and config errors **before** paying mainnet fees: **compile → test → simulate → testnet → mainnet**.

You cannot guarantee **zero** failures (congestion, wallet bugs, MEV), but everything left of **Broadcast** in the diagrams below is **free or testnet-cheap**.

## 1. End-to-end sequence

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

## 2. Pre-flight checklist

| Step | What you verify | Tool / how | Fails before chain? |
|------|-----------------|------------|---------------------|
| **1. Compile** | Syntax, types, bytecode size | `hardhat compile`, `blueprint build`, `aiken build` | **Yes** |
| **2. Unit tests** | Fee math, zero address rejected | Hardhat, Foundry, Aiken | **Yes** |
| **3. Static analysis** | Reentrancy, overflow | Slither, Mythril (optional) | **Yes** |
| **4. Config review** | `feeAccount`, `feeBps ≤ 10000` | Code review | **Yes** |
| **5. Simulate call** | Tx would succeed without sending | `eth_call`, `triggerConstantContract`, `cardano-cli build` | **Yes** |
| **6. Estimate cost** | Enough native coin + gas headroom | `estimateGas`, energy estimate | **Yes** |
| **7. Wallet / nonce** | Correct network, balance | MetaMask, TronLink, Tonkeeper | **Yes** if blocked |
| **8. Testnet E2E** | Deploy + `pay()` + balances | BSC testnet, Shasta, Preprod | Cheap |
| **9. Mainnet canary** | One small real `pay()` | Mainnet explorer | Costs real fee |

## 3. EVM simulation (BNB / Tron)

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

## 4. Tools by network

| Network | Simulate / dry-run | Testnet | Explorer |
|---------|-------------------|---------|----------|
| [BNB](networks/bnb/i-overview.md) | `eth_call`, `staticCall`, Foundry | BSC testnet | BscScan |
| [Tron](networks/tron/i-overview.md) | `triggerConstantContract` | Shasta / Nile | Tronscan |
| [TON](networks/ton/i-overview.md) | Blueprint, `@ton/sandbox` | TON testnet | Tonviewer |
| [ADA](networks/ada/i-overview.md) | `cardano-cli transaction build`, Lucid | Preprod / Preview | Cardanoscan |

## 5. Common revert reasons (FeeSplitter)

| Contract check | User mistake | Simulation catches? |
|----------------|--------------|---------------------|
| `msg.value > 0` | Sends 0 native coin | **Yes** |
| `recipient != address(0)` | Zero address | **Yes** |
| `payOk` / transfer fail | Recipient rejects | **Yes** on testnet |
| Out of gas | Gas limit too low | **estimateGas** helps |
| Wrong network | Mainnet vs testnet | Wallet UI |
| Insufficient balance | Value + gas | **Often before** broadcast — [Part VII](vii-failed-transactions-and-funds.md) |

## 6. Decision gates

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

## 7. Related

- **Part VII** — [Failed transactions & funds](vii-failed-transactions-and-funds.md)
- **Part IX** — [Verify safe & completed](ix-verify-safe-and-completed.md)
- **Part VI** — [Deploy & hosting](vi-deploy-pricing-and-hosting.md)
