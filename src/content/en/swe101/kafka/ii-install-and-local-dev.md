---
label: "II"
subtitle: "Install & local dev"
group: "Kafka"
order: 2
---
Kafka — install & local dev
Run Kafka locally with **Docker Compose** (recommended) or a packaged distribution. Use the **CLI** (`kafka-topics`, console producer/consumer) before wiring application code.

Previous: [Overview](i-overview.md).

## 1. Docker Compose (single broker, KRaft)

Modern Kafka can run **without ZooKeeper** using **KRaft** (Kafka Raft metadata). A minimal dev stack:

```yaml
# docker-compose.kafka.yml
services:
  kafka:
    image: apache/kafka:3.7.0
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
```

```text
docker compose -f docker-compose.kafka.yml up -d
```

**Bootstrap server** for clients: **`localhost:9092`**.

| Tool | Purpose |
|------|---------|
| **Docker Compose** | Local broker + optional UI (Redpanda Console, AKHQ) |
| **Redpanda** | Kafka-compatible, lighter for laptops (alternative image) |
| **Confluent Platform** | Enterprise docs, Schema Registry (optional) |

## 2. Create a topic

```text
docker exec -it <kafka-container> /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic order-events \
  --partitions 3 \
  --replication-factor 1
```

```text
docker exec -it <kafka-container> /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic order-events
```

| Flag | Meaning |
|------|---------|
| **`--partitions 3`** | Three parallel sub-logs — up to 3 consumers in one group at full parallelism |
| **`--replication-factor 1`** | Dev only — one copy; production uses 3+ |

## 3. Console producer and consumer

**Terminal 1 — consume from start:**

```text
docker exec -it <kafka-container> /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic order-events \
  --from-beginning
```

**Terminal 2 — produce:**

```text
docker exec -it <kafka-container> /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic order-events
```

Type JSON lines and press Enter:

```json
{"orderId":"ord_1","type":"OrderPlaced","totalCents":4999}
```

The consumer terminal prints each line — you have a working log.

## 4. Consumer groups in the CLI

```text
docker exec -it <kafka-container> /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic order-events \
  --group demo-group
```

Run a **second** consumer with the **same `--group`** — partitions split between them (see [Consumer groups](v-consumer-groups-and-delivery.md)).

List groups:

```text
docker exec -it <kafka-container> /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --list
```

## 5. Connection from apps

| Setting | Typical dev value |
|---------|-------------------|
| **`bootstrap.servers`** | `localhost:9092` |
| **Security** | `PLAINTEXT` locally; `SASL_SSL` in production |
| **Serializers** | String/JSON for learning; **Avro/Protobuf** + Schema Registry in production |

[Spring Kafka](vi-patterns-and-integration.md) and other clients use the same bootstrap address.

## 6. Optional: UI

| UI | Role |
|----|------|
| **AKHQ** / **Redpanda Console** | Browse topics, messages, consumer lag |
| **kafka-ui** | Open-source topic browser |

Helpful when debugging “did my message land?” without writing a consumer.

## Next

Continue with [Core concepts](iii-core-concepts-and-architecture.md) — brokers, partitions, and replication.
