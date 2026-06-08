---
label: "III"
subtitle: "アライメント (SFT, RLHF, DPO)"
group: "LLMs"
order: 3
---
Alignment — SFT, RLHF, and DPO
Pre-trained models predict **likely** text — not necessarily **helpful** or **safe**. **Alignment** trains behaviour users expect from assistants.

## 1. Supervised fine-tuning (SFT)

Fine-tune on curated **(instruction, response)** pairs.

| Input | Target response |
|-------|-----------------|
| "Summarise this article …" | Good summary |
| "Write SQL for …" | Valid query |

Teaches **format** and **task following** — foundation of chat models.

## 2. RLHF — Reinforcement Learning from Human Feedback

| Step | Action |
|------|--------|
| 1 | Model generates multiple answers |
| 2 | **Humans rank** outputs |
| 3 | Train **reward model** on rankings |
| 4 | Fine-tune LLM with **PPO** to maximise reward |

| Pros | Cons |
|------|------|
| Aligns with human preferences | Expensive labels; reward hacking risk |
| Improves safety tone | Complex pipeline (OpenAI, Anthropic use variants) |

## 3. DPO — Direct Preference Optimisation

Train directly on **(prompt, chosen, rejected)** pairs — **no separate reward model**.

| vs RLHF | DPO |
|---------|-----|
| Pipeline | Simpler — preference loss on policy |
| Stability | Often easier to reproduce in research |

Common in open-source alignment recipes.

## 4. What alignment does not fix

| Limit | Mitigation |
|-------|------------|
| **Factual errors** | RAG, tools, human review |
| **Stale knowledge** | RAG, browsing tools |
| **Jailbreaks** | Layered guardrails, monitoring |
| **Private data in weights** | Don't train on secrets; use RAG |

## 5. Evaluation beyond loss

| Metric type | Example |
|-------------|---------|
| **Automated benchmarks** | MMLU, HumanEval (code) |
| **Human eval** | Helpfulness, harmlessness |
| **Red teaming** | Adversarial prompts |

Same spirit as [ML evaluation](../machine-learning/iv-model-evaluation-and-metrics.md) — pick metrics tied to product risk.

## 6. Rehearsal questions

- SFT vs RLHF — what does each add?
- Why might a model with low training loss still give bad answers?
- What is DPO simplifying compared to RLHF?

**Related:** [Prompt engineering](iv-prompt-engineering.md), [Safety & production](vi-safety-and-production.md).
