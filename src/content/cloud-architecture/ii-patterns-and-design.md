---
label: "II"
subtitle: "Patterns & Design"
group: "Cloud architecture"
order: 2
---
Cloud Architecture — Part II: Patterns & Design
Scalability, microservices, event-driven, observability, cost.

## 1. Scalability patterns
Vertical scaling (scale up): bigger machine — CPU, RAM.
+ Simple, no code change. − Hard ceiling, single point of failure.

Horizontal scaling (scale out): more instances behind a load balancer.
+ Near-infinite ceiling, fault tolerant. − App must be stateless.

Stateless services: each request carries all context (JWT, session in DB).
→ Any instance can serve any request — essential for auto scaling.

Auto Scaling:
- Scale out on high CPU / request rate; scale in on idle.
- Cooldown period prevents thrashing.
- Target tracking policy (e.g. keep CPU at 60%) is simpler than step scaling.

Caching layers:
- CDN edge: static assets & cacheable API responses.
- In-memory (Redis / Memcached): hot DB rows, session data.
- DB read replicas: offload read-heavy traffic from primary.

## 2. Microservices vs monolith
Monolith: single deployable unit; all modules share a process.
+ Simple to develop & debug initially.
− Deployments couple all teams; scaling requires scaling the whole app.

Microservices: separate services per business domain; independent deploy.
+ Each service scales independently; teams own their service end-to-end.
− Network latency between services; distributed tracing needed.
− Data consistency is harder (no shared DB).

When to migrate: when release friction or scaling needs outweigh the complexity.
Start modular monolith → extract services at seams where bounded contexts diverge.

## 3. Event-driven architecture
Services communicate via events on a message broker rather than direct calls.

Message queue (point-to-point):
- Producer → Queue → Consumer (one consumer processes each message).
- Decouples producer from consumer speed differences (back-pressure).
- AWS SQS, Azure Service Bus.

Pub/Sub (fan-out):
- Publisher → Topic → multiple subscribers each get a copy.
- AWS SNS + SQS, Google Pub/Sub, Azure Event Grid.

Event streaming:
- Ordered, replayable log; consumers maintain their own offset.
- Kafka, AWS Kinesis, Azure Event Hubs.
- Use when: audit trail, event sourcing, replay, multiple independent consumers.

Saga pattern:
- Distributed transaction across services using choreography or orchestration.
- Each step publishes a success event or a compensating event on failure.

## 4. API Gateway & service mesh
API Gateway (north-south traffic — client → services):
- Single entry point: auth, rate limiting, routing, SSL termination.
- AWS API Gateway, Kong, Azure API Management.

Service mesh (east-west traffic — service ↔ service):
- Sidecar proxy (Envoy) injected next to each service pod.
- Handles retries, circuit breaking, mTLS, observability — without app code.
- Istio, Linkerd, AWS App Mesh.

Circuit breaker pattern:
- Track failure rate to a downstream service.
- Open circuit (fail fast) when threshold exceeded; half-open to probe recovery.
- Prevents cascade failures — fail quickly instead of waiting for timeout.

## 5. Observability in the cloud
Three pillars:
- Logs: timestamped records of events. Aggregate to CloudWatch / Datadog.
- Metrics: numeric time-series (CPU %, req/s, error rate). → Alerts.
- Traces: end-to-end request journey across services (OpenTelemetry).

Key practices:
- Structured logging (JSON) — machine-parseable, filterable.
- Correlation ID: inject a request ID at the gateway; propagate in headers.
- Distributed tracing: spans form a tree — identify which service is slow.
- SLO / SLA / SLI:
– SLI: actual measurement (e.g., p99 latency = 120 ms).
– SLO: target (e.g., p99 latency < 200 ms, 99.9% of time).
– SLA: contractual agreement with customers (breach → penalties).

## 6. Cost & governance
Pricing models:
- On-Demand: pay per second/hour; no commitment. Highest unit price.
- Reserved Instances / Savings Plans: 1–3 yr commitment; 30–70% savings.
- Spot / Preemptible: spare capacity at up to 90% discount; can be reclaimed.
→ Use for batch jobs, ML training, stateless workers with checkpointing.

FinOps practices:
- Tag every resource (team, env, project) → cost allocation reports.
- Set billing alerts and budget thresholds.
- Delete unused snapshots, detached EBS volumes, idle NAT Gateways.
- Right-size: compare actual CPU/RAM usage vs provisioned → downsize.

Governance:
- IAM least privilege: grant only what a role needs, no wildcard *.actions.
- AWS Organizations / Azure Management Groups: policy guardrails at scale.
- Service Control Policies (SCPs): deny restricted actions even to admins.
- CloudTrail / Activity Log: immutable audit trail of all API calls.

## 7. Remember & rehearse
- What makes a service stateless and why does it matter for auto scaling?
- Explain the trade-offs between microservices and a monolith.
- What is the difference between a message queue and pub/sub?
- How does a circuit breaker prevent cascade failures?
- Name the three pillars of observability. What is a correlation ID?
- What is the difference between SLI, SLO, and SLA?
- When would you use Spot instances and why?
