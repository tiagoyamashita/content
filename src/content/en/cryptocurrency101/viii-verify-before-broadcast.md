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

```mermaid
sequenceDiagram
    title Deploy + pay — full flow with verification gates
    actor DEV as Developer
    actor USER as User
    participant LOCAL as Local toolchain (Hardhat / Blueprint / Aiken)
    participant TEST as Testnet
    participant MAIN as Mainnet
    participant SC as FeeSplitter (on-chain)

    Note over DEV,LOCAL: Build & verify (off-chain, no chain fee)
    DEV->>LOCAL: write contract + tests
    LOCAL->>LOCAL: compile / build
    alt compile error
        LOCAL-->>DEV: fix syntax — STOP
    end
    LOCAL->>LOCAL: unit tests (fee math, zero address)
    alt tests fail
        LOCAL-->>DEV: fix logic — STOP
    end

    Note over DEV,TEST: Deploy to testnet
    DEV->>LOCAL: estimate deploy gas / energy / fee
    LOCAL-->>DEV: show cost preview
    DEV->>TEST: broadcast deploy tx
    alt deploy reverts / out of gas
        TEST-->>DEV: pay testnet fee only — fix & retry
    end
    TEST-->>DEV: contract address

    Note over DEV,SC: Simulate pay (before user touches mainnet)
    DEV->>LOCAL: eth_call / dry-run / cardano build
    LOCAL-->>DEV: success OR revert reason
    alt simulation revert
        LOCAL-->>DEV: fix require / datum — STOP
    end
    DEV->>TEST: pay(recipient) with test coins
    TEST->>SC: execute
    SC-->>DEV: verify feeAccount + recipient balances

    Note over DEV,SC: Mainnet (small amount first)
    DEV->>MAIN: deploy (if not already)
    DEV->>MAIN: pay(recipient, tiny amount)
    MAIN->>SC: execute
    alt success
        SC-->>USER: ready for production traffic
    else revert
        MAIN-->>DEV: post-mortem via explorer
    end
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

```mermaid
sequenceDiagram
    title EVM — verify pay() before broadcast
    actor Developer
    participant Wallet
    participant RPC
    participant SC as FeeSplitter

    Developer->>RPC: eth_call pay(recipient) { value: amount }
    RPC->>SC: execute (not mined)
    alt require fails
        SC-->>RPC: revert + reason
        RPC-->>Developer: fix — no mainnet fee
    else success
        RPC-->>Developer: simulation OK
        Developer->>RPC: eth_estimateGas
        Developer->>Wallet: sign & send (+ 10% gas buffer)
    end
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

```mermaid
flowchart TD
    start([Start])
    start --> A[Compile & unit tests]
    A --> B{All pass?}
    B -->|no| C[Fix code]
    C --> stop1([Stop])
    B -->|yes| D[Simulate / constant call]
    D --> E{Success?}
    E -->|no| F[Read revert reason]
    F --> stop2([Stop])
    E -->|yes| G[Estimate fee & check balance]
    G --> H{balance >= pay amount + gas?}
    H -->|no| I[Top up wallet]
    I --> stop3([Stop])
    H -->|yes| J{First time on mainnet?}
    J -->|yes| K[Run on testnet E2E]
    J -->|no| L[Broadcast]
    K --> L
    L --> M{Receipt success?}
    M -->|yes| N[Verify on explorer]
    M -->|no| O[Debug — fee may still be spent]
    N --> stop4([Stop])
    O --> stop4
```

## 7. Related

- **Part VII** — [Failed transactions & funds](vii-failed-transactions-and-funds.md)
- **Part IX** — [Verify safe & completed](ix-verify-safe-and-completed.md)
- **Part VI** — [Deploy & hosting](vi-deploy-pricing-and-hosting.md)
