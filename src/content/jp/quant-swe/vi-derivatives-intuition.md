---
label: "VI"
subtitle: "Derivatives intuition"
group: "Quant SWE"
order: 6
---
Derivatives intuition
A **derivative**’s payoff depends on one or more **underlyings**. Engineers need enough intuition to store the right fields, compute marks, and not confuse notional with cash.

## 1. Why derivatives exist

| Need | Instrument family |
|------|-------------------|
| Lock a future price | Forwards / futures |
| Insurance / convex payoff | Options |
| Swap cashflow profiles | Swaps |
| Leverage / 24h crypto exposure | Perpetuals |

Hedgers and speculators share the same contracts; systems usually don’t care about motive — they care about **lifecycle events**.

## 2. Forwards and futures

| | Forward | Futures |
|--|---------|---------|
| Venue | OTC | Exchange |
| Marking | Bilateral | Daily variation margin |
| Credit risk | Counterparty | Clearinghouse-centric |

**Engineer view:** futures need **expiry**, **multiplier**, **margin**, and **roll** logic for continuous series.

## 3. Options — payoff sketch

Call buyer profit roughly: `max(S - K, 0) − premium` (European, at expiry).

| Term | Meaning |
|------|---------|
| **Spot `S`** | Underlying price |
| **Strike `K`** | Exercise price |
| **Expiry** | When option ends |
| **Premium** | Price of the option |
| **Call / put** | Right to buy / sell underlying (buyer) |

American vs European exercise rules change assignment risk and early-exercise checks in OMS.

## 4. Greeks (operational meaning)

| Greek | Roughly measures | System use |
|-------|------------------|------------|
| **Delta** | Sensitivity to underlying | Hedge ratios, limits |
| **Gamma** | How delta changes | Intraday rehedge stress |
| **Vega** | Sensitivity to vol | Vol shock reports |
| **Theta** | Time decay | Overnight PnL explanation |
| **Rho** | Rates sensitivity | Often smaller for short-dated equity options |

Treat Greeks as **model outputs with a model id and as-of time**, not eternal truths.

## 5. Pricing models vs marks

```text
Market quotes  →  marks (what risk/PnL uses)
Models         →  theoretical values, Greeks, scenario shocks
```

| Source | Role |
|--------|------|
| **Exchange settlement** | Official for clearing |
| **Vendor mid / proprietary** | Internal MTM |
| **Model** | Gap fill, exotic books, research |

Never silently fall back from quote to model without flagging **mark quality**.

## 6. Lifecycle events to encode

| Event | Example |
|-------|---------|
| **Trade** | Open position |
| **Exercise / assignment** | Options |
| **Expiry / cash settle** | Index options |
| **Corporate action on underlying** | Strike adjustments |
| **Funding payment** | Crypto perps |

## 7. Notional vs cash

| Metric | Example |
|--------|---------|
| **Notional** | 10 futures × multiplier × price |
| **Premium paid** | Option debit |
| **Variation margin** | Daily futures PnL movement |

Risk limits often mix these — document which one each limit uses.

## Next

[Research & backtesting](vii-research-and-backtesting.md) — turning ideas into honest simulations.
