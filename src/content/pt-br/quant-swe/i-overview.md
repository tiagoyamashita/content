---
label: "I"
subtitle: "Overview"
group: "Quant SWE"
order: 1
---
Quant SWE — overview
**Quant SWE** is software engineering for **markets**: market data, research and backtests, order routing, risk, and the low-latency systems that sit next to exchanges. This track is for engineers who already write services and want the **domain vocabulary** and **system shapes** used in quantitative trading and fintech.

Not financial advice. Examples are educational sketches — production trading has legal, compliance, and capital requirements beyond this curriculum.

## Map of Quant SWE

| Note | Focus |
|------|--------|
| [Markets & asset classes](ii-markets-and-asset-classes.md) | Venues, products, who trades what |
| [Returns, risk & statistics](iii-returns-risk-and-statistics.md) | PnL language, volatility, basics quants assume |
| [Market data & time series](iv-market-data-and-time-series.md) | Ticks, bars, clocks, storage shapes |
| [Order books & microstructure](v-order-books-and-microstructure.md) | Bids/asks, queues, spreads, fees |
| [Derivatives intuition](vi-derivatives-intuition.md) | Forwards, options, Greeks for engineers |
| [Research & backtesting](vii-research-and-backtesting.md) | Pipelines, leakage, walk-forward |
| [Trading systems architecture](viii-trading-systems-architecture.md) | Gateways, OMS/EMS, latency paths |
| [Risk, PnL & controls](ix-risk-pnl-and-controls.md) | Limits, marks, kill switches |
| [Day in the life (example)](x-day-in-the-life.md) | Concrete QSE daily loop: open → build → incident → EOD |

## Suggested order

```text
Markets & asset classes
  → Returns, risk & statistics
  → Market data & time series
  → Order books & microstructure
  → Derivatives intuition (as needed)
  → Research & backtesting
  → Trading systems architecture
  → Risk, PnL & controls
  → Day in the life (example)
```

## How this relates to other tracks

| Track | Overlap |
|-------|---------|
| [SWE101](../swe101/i-overview.md) | Services, queues, Postgres, system design |
| [CS101](../cs101/i-overview.md) | Data structures, networking, time-series DB concepts |
| [SRE101](../sre101/i-overview.md) | Observability, failover, capacity for market hours |
| [AI101](../ai101/i-overview.md) | Feature pipelines and model deployment patterns |
| [Cryptocurrency101](../cryptocurrency101/i-overview.md) | On-chain venues and settlement mental models |

## Roles this track maps to

| Role | What they own |
|------|----------------|
| **Quant researcher** | Signals, models, backtests — usually Python/R |
| **Quant developer / QSE** | Productionize research: data, sims, libraries |
| **Trading systems engineer** | Gateways, matching-adjacent clients, OMS |
| **Risk engineer** | Limits, VaR-style monitors, intraday controls |
| **Market data engineer** | Capture, normalize, replay, distribute feeds |

## Prerequisites

| Topic | Where |
|-------|--------|
| HTTP services, databases, messaging | [SWE101](../swe101/i-overview.md) |
| Arrays, hashing, graphs (intuition) | [CS101 data structures](../cs101/data-structures/i-array.md) |
| Basic probability vocabulary | This track’s [returns & risk](iii-returns-risk-and-statistics.md) |

## Next

Start with [Markets & asset classes](ii-markets-and-asset-classes.md).
