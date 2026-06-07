---
label: "V"
subtitle: "Storage & databases"
group: "Cloud architecture"
order: 5
---
Storage & databases
Cloud storage splits into **object**, **block**, and **file** — each with different latency, durability, and access patterns. **Managed databases** offload patching and backups.

## 1. Storage types compared

| Type | Access | Latency | Use case |
|------|--------|---------|----------|
| **Object** | HTTP GET/PUT, flat keys | Higher | Static assets, backups, data lakes |
| **Block** | Attached disk to VM | Low random I/O | DB volumes, boot disks |
| **File (NFS)** | Shared mount | Moderate | Legacy apps, shared content |

```text
Object:  s3://bucket/path/file.json     (whole object)
Block:   /dev/xvdf on EC2               (sector read/write)
File:    mount nfs.example.com:/share   (POSIX files)
```

## 2. Object storage

| Cloud | Service | Durability (typical) |
|-------|---------|----------------------|
| AWS | S3 | 11 nines (Standard) |
| Azure | Blob Storage | 11+ nines (LRS) |
| GCP | Cloud Storage | 11 nines (Standard) |

```bash
# Upload static asset
aws s3 cp dist/app.js s3://myapp-assets-prod/v1/app.js \
  --cache-control "public, max-age=31536000"
```

| Feature | Benefit |
|---------|---------|
| Versioning | Roll back accidental deletes |
| Lifecycle rules | Standard → IA → Glacier |
| Event notifications | Trigger Lambda on new upload |
| Presigned URLs | Direct client upload without proxy |

**Default choice** for static web, logs archive, ML datasets, Terraform state (with locking).

## 3. Block storage

| Cloud | Service |
|-------|---------|
| AWS | EBS |
| Azure | Managed Disks |
| GCP | Persistent Disk |

- Attached to **one** VM at a time (except multi-attach types for clustered DBs).
- Snapshot to object storage for backup.
- Choose **gp3/ssd** for general DB; **io2** for sustained IOPS.

**Use when:** PostgreSQL/MySQL on EC2, high-IOPS database, boot volumes.

## 4. File storage

| Cloud | Service |
|-------|---------|
| AWS | EFS |
| Azure | Azure Files |
| GCP | Filestore |

Multiple VMs mount same NFS share — content management, shared config (prefer object/config service for new apps).

## 5. Managed relational databases

| Cloud | Service | Engines |
|-------|---------|---------|
| AWS | RDS / Aurora | PostgreSQL, MySQL, SQL Server, Oracle |
| Azure | Azure SQL / PostgreSQL Flexible | |
| GCP | Cloud SQL / AlloyDB | |

```text
RDS Multi-AZ
  Primary (AZ-a) ──sync replicate──▶ Standby (AZ-b)
  Failover: DNS/connection endpoint switches (~60–120 s)
```

| Feature | Purpose |
|---------|---------|
| **Multi-AZ** | HA failover |
| **Read replica** | Offload read traffic (async lag) |
| **Automated backups** | Point-in-time recovery |
| **Parameter groups** | Tune DB settings as code |

**Use when:** ACID transactions, joins, mature ORM apps (Spring + JPA).

## 6. NoSQL options

| Category | Examples | Access pattern |
|----------|----------|----------------|
| **Key-value** | DynamoDB, Redis (ElastiCache) | O(1) by key, single-digit ms |
| **Document** | MongoDB Atlas, Firestore | Flexible JSON documents |
| **Wide-column** | Cassandra, Bigtable | Time-series, IoT at scale |
| **Graph** | Neptune, Neo4j | Relationships |

```text
DynamoDB partition key: userId
Sort key: orderTimestamp
→ Query all orders for user, sorted by time
```

| Choose SQL | Choose NoSQL |
|------------|--------------|
| Complex joins | Massive scale simple access |
| Strong schema | Flexible/evolving schema |
| Transactions across rows | Partition-key access sufficient |

## 7. Caching layer

| Service | Type |
|---------|------|
| ElastiCache Redis | In-memory, sub-ms |
| Memorystore | GCP Redis/Memcached |
| Azure Cache for Redis | |

Not durable primary storage — session cache, rate limits, hot keys [Scalability & caching](../patterns-and-design/ii-scalability-and-caching.md).

## 8. Example stack

| Data | Service |
|------|---------|
| User uploads | S3 |
| Transactional data | RDS PostgreSQL Multi-AZ |
| Product catalog cache | Redis |
| Analytics events | S3 data lake + Athena |
| Search index | OpenSearch |

## 9. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Database files on object storage | Block storage or managed DB |
| Public S3 bucket for secrets | Private + IAM, block public access |
| One giant RDS for everything | Split by bounded context or read replicas |
| No backup retention tested | Restore drill quarterly |

**Related:** [Regions, AZs & edge](iii-regions-azs-and-edge.md), CS101 databases submenu.
