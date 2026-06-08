---
label: "VI"
subtitle: "Safety & production"
group: "LLMs"
order: 6
---
Safety and production
Shipping LLMs requires **guardrails**, **observability**, and **serving** discipline — not just good prompts.

## 1. Threat model (brief)

| Risk | Example |
|------|---------|
| **Prompt injection** | Untrusted content overrides system |
| **Data exfiltration** | Model leaks secrets from context |
| **Harmful content** | Violence, illegal instructions |
| **PII** | Model outputs or logs customer data |
| **Cost abuse** | Unbounded token usage |

Layer defences — no single filter catches everything.

## 2. Guardrails stack

```text
Input filter → LLM → Output filter → User
     ↑              ↑
  block jailbreak   redact PII, policy classifier
```

| Layer | Tooling examples |
|-------|------------------|
| **Input moderation** | Vendor APIs, open classifiers |
| **System prompt** | Refusals, scope limits |
| **Tool sandbox** | SQL read-only, network off |
| **Output validation** | JSON schema, allow-list |

## 3. Serving architecture

| Component | Role |
|-----------|------|
| **API gateway** | Auth, rate limits — [Rate limiting](../../swe101/sysdesign/scalable-patterns/iv-rate-limiting.md) |
| **Model server** | vLLM, TGI, TensorRT-LLM — batching, KV cache |
| **Vector DB** | RAG retrieval |
| **Queue** | Async long jobs |

Monitor **latency p99**, **tokens/sec**, **GPU util**, **error rate**.

## 4. Logging and privacy

| Do | Don't |
|----|-------|
| Log prompt hashes, token counts, latency | Log full prompts with PII in plain text |
| Sample traces for quality review | Store secrets in prompts |
| Retention policy + redaction | Infinite chat logs without consent |

## 5. Cost control

| Lever | Effect |
|-------|--------|
| **Smaller model** for routing/classify | Cheaper triage |
| **Cache** frequent queries | Dedupe embeddings |
| **Max tokens** cap | Prevent runaway completion |
| **Rate limits per user** | Abuse prevention |

## 6. Human in the loop

| Use case | Pattern |
|----------|---------|
| High-stakes (medical, legal) | Human approval before send |
| Feedback | Thumbs down → eval set for next alignment |
| Escalation | Confidence threshold → support agent |

## 7. Rehearsal questions

- Name three production metrics for an LLM API.
- Prompt injection vs data poisoning — difference?
- When is a smaller local model better than GPT-4 API?

**Related:** [Prompt engineering](iv-prompt-engineering.md), [RAG & fine-tuning](v-rag-and-fine-tuning.md), [ML workflow](../machine-learning/vii-ml-workflow-and-deployment.md).
