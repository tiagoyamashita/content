---
label: "VII"
subtitle: "Time-series"
group: "Databases"
order: 7
---
Time-series databases
**Time-series** databases optimize **append-heavy** streams of **(timestamp, measurement)** data: server metrics, sensor readings, stock ticks, application traces. Queries ask **what happened over a time range**, **rates**, **aggregates by bucket**, not “fetch row 8812 by primary key” alone.

## 1. Data model

Typical **line protocol** shape (InfluxDB / Prometheus concepts):

```text
measurement,tag1=v1,tag2=v2 field1=1.2,field2=42i 1716120000000000000
└─ name ─┘ └── labels (indexed) ──┘ └── values ──┘ └──── timestamp ────┘
```

Example — CPU metric:

```text
cpu,host=web-01,region=us-east usage=0.73,idle=0.27 1716120000
```

| Part | Role |
|------|------|
| **Measurement** | Metric name (`cpu`, `http_requests`) |
| **Tags / labels** | Low-cardinality dimensions for filter/group (`host`, `region`) |
| **Fields** | Actual numbers (usage, bytes, count) |
| **Timestamp** | When the sample was taken (often nanosecond precision) |

**Tags** are indexed; **high-cardinality tags** (user id on every request) explode storage and slow queries — design carefully.

## 2. Access patterns

| Query type | Example |
|------------|---------|
| **Range scan** | CPU for `host=web-01` last 24 h |
| **Downsample** | Average per 5-minute bucket |
| **Rate / derivative** | Requests per second from counter |
| **Alert** | `avg(cpu) > 0.9` for 5 minutes |

```text
Writes:  ──► append only (mostly immutable past)
Reads:   ──► recent window hot; old data cold or aggregated
```

## 3. Retention and compaction

TSDBs **drop or roll up** old data automatically:

```text
Raw 10s resolution  → keep 7 days
5m averages         → keep 90 days
1h averages         → keep 2 years
```

**Compaction** merges small files into larger blocks; **WAL** ensures durability on ingest.

## 4. Prometheus-style example

Metric exposition (text format):

```text
http_requests_total{method="GET", status="200"} 1027
http_requests_total{method="POST", status="500"} 3
```

**PromQL** query:

```promql
rate(http_requests_total{status="500"}[5m])
sum by (method) (rate(http_requests_total[1h]))
```

Prometheus is **pull-based** (scrape targets) with a local **TSDB** — common in Kubernetes monitoring.

## 5. SQL time-series extensions

**TimescaleDB** (PostgreSQL extension) and **InfluxDB 3** blur the line with SQL:

```sql
SELECT time_bucket('5 minutes', ts) AS bucket,
       avg(cpu_usage)
FROM metrics
WHERE host = 'web-01'
  AND ts > NOW() - INTERVAL '24 hours'
GROUP BY bucket
ORDER BY bucket;
```

Use when teams already run PostgreSQL and want **hybrid** relational + metrics.

## 6. Strengths and limits

**Strengths**

- **Optimized ingest** — millions of points per second
- **Built-in downsampling** and retention policies
- **Efficient compression** (similar timestamps, delta encoding)
- **Alerting** integrated (Prometheus Alertmanager, Influx tasks)

**Limits**

- **Bad for general OLTP** — don’t store user profiles here
- **Cardinality bombs** — unbounded tag values hurt every TSDB
- **Updates/deletes** of single past points are awkward (immutable log mindset)
- **Long-range ad-hoc JOINs** across business entities — use **warehouse** / SQL

## 7. Time-series vs wide-column

Both handle high write volume. **TSDBs** add **time semantics** (retention, rollups, rate functions). **Cassandra** can store time-ordered rows but you build rollup jobs yourself. Pick **TSDB** when monitoring is the product; **wide-column** when events are generic rows with many attributes [Wide-column](v-wide-column.md).

## 8. When to choose time-series

- **Observability** — metrics, logs-derived counters, SLO dashboards
- **IoT** — sensor streams
- **Finance** — ticks (often specialized systems + TSDB for analytics)
- **Energy / industrial** — SCADA history

## 9. Examples

| Product | Notes |
|---------|--------|
| **Prometheus** | Cloud-native metrics, PromQL |
| **InfluxDB** | Line protocol, Flux / SQL |
| **TimescaleDB** | PostgreSQL extension |
| **OpenTelemetry → backend** | Vendor-neutral ingest to TSDB or SaaS |

## 10. Cardinality rule of thumb

```text
Good tags:   host, service, region, status_class  (bounded sets)
Risky tags:  user_id, request_id, url_path        (millions of values)
```

Prefer **aggregating at the client** or **sampling** high-cardinality dimensions.

## 11. Related

- **Overview** — [Databases overview](i-overview.md)
- **Wide-column** — event logs at scale without TS-specific rollups [Wide-column](v-wide-column.md)
- **Key-value** — short-lived counters before export [Key-value](iii-key-value.md)
