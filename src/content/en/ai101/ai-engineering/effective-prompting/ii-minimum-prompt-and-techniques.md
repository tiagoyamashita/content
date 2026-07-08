---
label: "II"
subtitle: "Minimum prompt & techniques"
group: "AI Applied"
order: 2
---
Minimum prompt & techniques

## 1. The minimum good prompt

Include four pieces when the task matters:

| Piece | Example |
|-------|---------|
| **Role / perspective** | “You are a concise editor for a technical blog.” |
| **Task** | “Rewrite the draft below for clarity.” |
| **Constraints** | “Keep under 300 words; preserve all numbers.” |
| **Output format** | “Use bullet points; no intro paragraph.” |

```text
Role: …
Task: …
Constraints: …
Format: …

[paste content]
```

Weak: “Make this better.”  
Strong: “List three concrete edits; for each, quote the original sentence and your revision.”

## 2. Techniques that actually help

| Technique | When to use | Example phrase |
|-----------|-------------|----------------|
| **Zero-shot** | Simple, well-known task | “Translate to Japanese: …” |
| **Few-shot** | You have a style template | Paste 2 examples, then “Now do the same for …” |
| **Chain-of-thought** | Math, logic, planning | “Think step by step, then give the final answer.” |
| **Draft → critique → revise** | Important documents | “First draft, then list weaknesses, then improved version.” |
| **Audience toggle** | Same content, different reader | “Explain twice: for executives, then for engineers.” |

**Chain-of-thought:** ask for reasoning **before** the final answer when mistakes are costly. Hide the steps in your copy if you only need the conclusion.