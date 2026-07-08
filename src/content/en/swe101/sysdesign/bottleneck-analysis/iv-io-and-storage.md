---
label: "IV"
subtitle: "I/O & storage"
group: "System design"
order: 4
---
I/O and storage bottlenecks
**Disk and object storage** often limit databases, logs, and media pipelines before CPU does.

## 1. Disk I/O — signals

| Signal | Tool |
|--------|------|
| High **iowait** | `top`, `mpstat` |
| **%util → 100%** | `iostat -x` |
| Random read **> 1 ms** on SSD | Latency histogram |
| Write queue depth growing | `await` in iostat |

## 2. Disk — causes and fixes

| Cause | Fix |
|-------|-----|
| Random small reads | Sequential access; read-ahead; indexes |
| Sync logging | Async append; centralized log agent |
| Full table scan | Index on WHERE / JOIN columns |
| fsync per row | Batch writes; WAL batching |
| HDD for OLTP | **NVMe SSD**; io_uring on Linux |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Sequential vs random disk access">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Access pattern matters</text>
  <text x="12" y="40" fill="#86efac" font-size="9">Sequential scan of index range — SSD friendly</text>
  <text x="12" y="56" fill="#f87171" font-size="9">Random lookups across huge table — IOPS limit</text>
  <rect x="12" y="64" width="200" height="12" rx="2" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="220" y="74" fill="#a1a1aa" font-size="8">contiguous</text>
  <rect x="12" y="80" width="40" height="12" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <rect x="80" y="80" width="40" height="12" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <rect x="160" y="80" width="40" height="12" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <text x="220" y="90" fill="#a1a1aa" font-size="8">scattered</text>
</svg></figure>

## 3. Object storage (S3-style)

| Bottleneck | Fix |
|------------|-----|
| **Prefix hot spot** | Randomize key prefix; spread partitions |
| Large upload | **Multipart** upload (5 MB–5 GB parts) |
| Many small LIST | Avoid listing huge prefixes; index metadata in DB |
| Egress cost | CDN in front; same-region reads |

## 4. WAL and checkpoints (databases)

| Issue | Tuning |
|-------|--------|
| WAL fsync latency | Faster disk; group commit |
| Checkpoint spike | `checkpoint_completion_target` spread |
| Replication lag | Network + WAL send rate |

## 5. When to escalate storage tier

| Workload | Tier |
|----------|------|
| OLTP primary | NVMe SSD / provisioned IOPS |
| Analytics scan | Column store / object + Spark |
| Archive | Cold object storage |
| Logs | Stream to aggregator; not local disk forever |

**Related:** [Database](vi-database.md), classic designs video streaming (S3).
