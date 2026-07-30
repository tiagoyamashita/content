---
label: "II"
subtitle: "Markets & asset classes"
group: "Quant SWE"
order: 2
---
Markets & asset classes
Before writing a trading service, know **what** is traded, **where** it trades, and **how** ownership and cash move. Wrong assumptions about venue rules break backtests and production equally.

## 1. Primary vs secondary

| Market | What happens | Engineer touchpoints |
|--------|--------------|----------------------|
| **Primary** | Issuer sells new securities (IPO, bond auction) | Less common for HFT; more for capital markets ops |
| **Secondary** | Investors trade existing instruments | Exchanges, dark pools, OTC desks — most quant systems |

## 2. Asset classes (engineer view)

| Class | Examples | Typical data / systems |
|-------|----------|------------------------|
| **Equities** | Stocks, ETFs | Consolidated tape, lot sizes, corporate actions |
| **Fixed income** | Bonds, treasuries | Quote-driven / RFQ more than continuous book |
| **FX** | Currency pairs | 24h venues, multi-dealer platforms |
| **Futures / listed options** | Index futures, equity options | Central clearing, daily marks, expiries |
| **Crypto** | Spot, perps | Exchange APIs, on-chain settlement variants |

Same math ideas (returns, volatility) appear everywhere; **market structure and calendars** differ.

## 3. Who sits in the market

```text
Retail / buy-side funds / hedge funds / prop firms / market makers / banks
        ↓
   Brokers / clearing members
        ↓
   Exchanges / ATS / OTC
        ↓
   Clearing & settlement (T+1, atomic, etc.)
```

| Participant | Incentive |
|-------------|-----------|
| **Liquidity taker** | Cross the spread to get filled now |
| **Liquidity maker** | Post quotes; earn rebate / spread; manage inventory |
| **Broker** | Route client orders; often aggregate venues |
| **Clearing house** | Novate trades; reduce counterparty risk |

## 4. Venue types

| Venue | Character |
|-------|-----------|
| **Exchange** | Public rulebook, matching engine, market data products |
| **ATS / dark pool** | Less pre-trade transparency; still regulated in many jurisdictions |
| **OTC / RFQ** | Negotiate with dealers; no continuous public book |
| **Crypto CEX** | Exchange-like API; custody and jurisdiction vary |

For system design: each venue is a **protocol + schedule + fee schedule + failure mode**.

## 5. Calendars and sessions

| Concept | Why it matters in code |
|---------|------------------------|
| **Trading hours** | Heartbeats, reconnect windows, “is market open?” gates |
| **Holidays / early closes** | Empty bars are not always bugs |
| **Auction phases** | Open/close auctions change order types and data |
| **Contract roll** | Futures series change — continuous series are constructed |

Store **exchange calendars** as data, not hardcoded `if weekday < 5`.

## 6. Cash vs derivative exposure

| Holding | You get | Engineer note |
|---------|---------|---------------|
| **Cash equity** | Ownership (subject to settlement) | Corporate actions: splits, dividends |
| **Future** | Daily mark-to-market PnL | Margin; expiry; roll |
| **Option** | Right, not obligation (buyer) | Greeks, assignment, early exercise (American) |
| **Perpetual** | Derivative without expiry (crypto) | Funding rate clocks |

## 7. What to model in software first

| Domain object | Fields you will need early |
|---------------|----------------------------|
| **Instrument** | Symbol, venue, currency, tick size, lot size, type |
| **Venue** | MIC/code, timezone, sessions, fee schedule id |
| **Account** | Firm, strategy, risk book, clearing account |
| **Order** | Side, qty, type, TIF, instrument, client order id |

Canonical IDs beat stringly-typed `"AAPL"` alone — same ticker can mean different listings.

## Next

[Returns, risk & statistics](iii-returns-risk-and-statistics.md) — the shared language of PnL and uncertainty.
