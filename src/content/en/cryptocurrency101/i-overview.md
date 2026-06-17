---
label: "I"
subtitle: "Overview"
group: "Cryptocurrency101"
order: 1
---
Cryptocurrency101 — overview
**Cryptocurrency101** introduces **blockchain networks**, how **transactions are stored**, **types of blockchains**, and a recurring **fee-split** smart contract pattern across **BNB**, **Tron**, **TON**, and **Cardano**.

This track is **conceptual and educational**, not financial advice. Contracts shown are **minimal sketches** — audit and test before mainnet use.

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | This page — track map, prerequisites, safety |
| **II — What is cryptocurrency?** | Keys, coins vs tokens, smart contracts |
| **III — How transactions are stored** | Blocks, chain, mempool, UTXO vs account |
| **IV — Types of blockchains** | L1/L2, consensus, EVM vs eUTXO |
| **V — Fee split pattern** | Shared `feeBps` / treasury / recipient rule |
| **VI — Deploy & hosting** | On-chain deployment, no VPS hosting |
| **VII — Failed transactions & funds** | Reverts, gas, insufficient balance |
| **VIII — Verify before broadcast** | Compile, simulate, testnet, canary |
| **IX — Verify safe & completed** | Explorers, confirmations, per network |

## Examples

| Example | Focus |
|---------|--------|
| [Examples overview](examples/i-overview.md) | 2% fee split deploy walkthroughs |
| [Tron — 2% fee split](examples/ii-tron-two-percent-fee-split.md) | Solidity + TronBox, full project |
| [TON — 2% fee split](examples/iii-ton-two-percent-fee-split.md) | Tact + Blueprint, full project |

## Networks (submenu)

| Submenu | Network | VM / model | Contract language |
|---------|---------|------------|-------------------|
| [BNB Chain](networks/bnb/i-overview.md) | BNB Smart Chain (BSC) | EVM | **Solidity** |
| [Tron](networks/tron/i-overview.md) | Tron | TVM (EVM-like) | **Solidity** |
| [TON](networks/ton/i-overview.md) | The Open Network | TON VM | **FunC** / **Tact** |
| [Cardano (ADA)](networks/ada/i-overview.md) | Cardano | eUTXO | **Aiken** / **Plutus** |

Start with foundations: [What is cryptocurrency?](ii-what-is-cryptocurrency.md) → [How transactions are stored](iii-how-transactions-are-stored.md) → [Types of blockchains](iv-types-of-blockchains.md).

## Prerequisites

| Topic | Where |
|-------|--------|
| Hashing, signatures (intuition) | [Cybersecurity](../cybersecurity/i-overview.md) |
| General programming | [SWE101](../swe101/i-overview.md) |

## Safety notes

| Risk | Mitigation |
|------|------------|
| **Reentrancy** (EVM) | Checks-effects-interactions; careful use of `call` |
| **Integer rounding** | Basis points; document rounding toward zero |
| **Admin keys** | Separate from fee recipient; multisig in production |
| **Regulation** | Fees and custody may be regulated — legal review |

Full verification guides: [Verify before broadcast](viii-verify-before-broadcast.md) · [Verify safe & completed](ix-verify-safe-and-completed.md).

## Next

1. [What is cryptocurrency?](ii-what-is-cryptocurrency.md)  
2. Or jump to a network: [BNB Chain](networks/bnb/i-overview.md) (Solidity, EVM) — closest to Ethereum tutorials.
