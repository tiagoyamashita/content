---
label: "memory-estimator"
group: "System Design"
order: 99
---
System Design — Memory Estimation (interactive)

Use the **graph in Preview mode** to drag sliders for session size, node count, and RAM per node.

**Full write-up** — formulas, concurrency tables, worked scenarios, and diagrams: **[Memory Estimator](mem-memory-estimator.md)**.

## Quick reference

```text
concurrent_users = DAU × concurrency_factor
working_set      = concurrent_users × bytes_per_user
total_RAM        ≈ working_set × 2
nodes            = ceil(total_RAM / usable_RAM_per_node)
```

| App type | Peak concurrent |
|----------|-----------------|
| Web | 5–10% of DAU |
| Real-time | 20–40% of DAU |

## Interactive estimator

Adjust sliders in Preview to explore:

- **Session / cache bytes** per active user
- **Number of nodes** in the cluster
- **RAM per node** (minus OS reserve)

Watch how **headroom** and **sharding** change the safe capacity before OOM.
