---
label: "VI"
subtitle: "Deploy & hosting"
group: "Cryptocurrency101"
order: 6
---
Cryptocurrency101 — Part VI: Deploy & hosting
Smart contracts **live on the blockchain** — replicated on network nodes. You **do not** host bytecode on a VPS. You pay **once to deploy**, then **gas per transaction**. A website or API is optional.

## 1. Where the contract lives

```text
Your laptop / CI  ──deploy tx──►  Blockchain nodes  ──►  contract address
                                         │
                                    no server bill
                                    for "hosting"
```

| Cost | When |
|------|------|
| **Deploy** | One-time gas to store bytecode |
| **Per call** | Users or you pay when `pay()` runs |
| **Server** | **Optional** — only for website / tx builder UI |

## 2. Deploy pricing (approximate)

**USD ranges shift with coin price and network load** — order-of-magnitude only; simulate on testnet first.

| Network | What you pay | Simple contract (e.g. FeeSplitter) | Testnet |
|---------|--------------|-------------------------------------|---------|
| [BNB Chain](networks/bnb/i-overview.md) | BNB gas | ~**$0.50 – $5** mainnet | Free BNB from faucet |
| [Tron](networks/tron/i-overview.md) | TRX (energy / bandwidth) | ~**$5 – $40** mainnet | Free TRX on Shasta/Nile |
| [TON](networks/ton/i-overview.md) | TON (storage + compute) | ~**$0.50 – $5** mainnet | Free TON from faucet |
| [Cardano (ADA)](networks/ada/i-overview.md) | ADA tx fee + min UTXO | ~**$2 – $15** mainnet | Free ADA from faucet |

| Ongoing cost | Server required? |
|--------------|------------------|
| **None** for “hosting” the contract | **No** — network runs bytecode |
| **Per call** — gas when `pay()` runs | Optional server only for website |

Details and estimation formulas: each [network page](networks/bnb/i-overview.md).

## 3. Developer deploy checklist

| Step | Action |
|------|--------|
| 1 | Compile on target network toolchain |
| 2 | Unit-test fee math and zero-address checks |
| 3 | Deploy to **testnet** |
| 4 | Run test `pay()` with faucet coins |
| 5 | Mainnet deploy + small canary `pay()` |

Full verification flow: [Verify before broadcast](viii-verify-before-broadcast.md).

## 4. Related

- **Part V** — [Fee split pattern](v-fee-split-pattern.md)
- **Part VIII** — [Verify before broadcast](viii-verify-before-broadcast.md)
