---
label: "II"
subtitle: "効果的なプロンプト"
group: "Using AI"
order: 2
---
Effective prompting
**Prompting** is how you steer ChatGPT, Claude, Gemini, and similar tools. You are not “programming” the model — you are **specifying the task** so the model has enough context to help once, not after five retries.

For API-level detail (roles, JSON mode), see [LLM prompt engineering](../llms/iv-prompt-engineering.md). This note is for **everyday use**.

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

## 3. Iteration loop (how pros work)

```text
1. Rough prompt → see output
2. Fix ambiguity (“too long”, “wrong tone”, “missed section 3”)
3. Add one constraint or example per iteration
4. Save the prompt that worked (personal library)
```

| Feedback to the model | Better than |
|-----------------------|-------------|
| “Shorter; drop adjectives; keep all dates.” | “Try again.” |
| “Wrong: revenue is in table 2, not table 1.” | “That’s wrong.” |
| “Use the template in my first message.” | Starting a new chat |

**New chat vs continue:** new chat when topic changes or context is polluted; continue when refining the same deliverable.

## 4. Templates by task type

### Summarise

```text
Summarise for a busy [role].
Length: [N bullets / N words].
Include: decisions, open questions, owners.
Exclude: background I already know.
Source:
"""
…
"""
```

### Compare options

```text
Compare A vs B for [decision].
Criteria: cost, risk, time, quality (weight quality highest).
Output: table + one-paragraph recommendation.
Context: …
```

### Code help (without shipping blindly)

```text
Language: [X]. Goal: [one sentence].
Show approach first, then code.
Flag assumptions and edge cases.
Do not invent APIs — say if unsure.
```

### Email / message draft

```text
Tone: [direct / warm / formal].
Relationship: [client / manager / peer].
Goal: [what should reader do after reading].
Facts only from below — do not invent names or dates.
```

## 5. System instructions vs chat message

| Product | Where “always follow” rules live |
|---------|----------------------------------|
| **ChatGPT** | Custom GPT instructions, or first message |
| **Claude** | Project instructions |
| **Cursor** | Rules, `.cursorrules`, project docs |
| **Copilot** | Copilot instructions in VS Code |

Put **stable** rules in system/project instructions; put **this task’s** content in the user message.

## 6. Common mistakes

| Mistake | Fix |
|---------|-----|
| Vague goal | One measurable deliverable |
| Wall of text, no structure | Headings, delimiters `"""…"""` |
| Asking for “best” without criteria | List criteria or weights |
| Trusting first answer on facts | Ask for sources; verify ([Trust & verify](vii-trust-privacy-and-verify.md)) |
| Pasting secrets | Redact; use enterprise tier if required |

## 7. Rehearsal questions

- What four pieces belong in a “minimum good prompt”?
- When is chain-of-thought worth the extra tokens?
- Why save prompts that worked?

**Related:** [Agents & agentic workflows](iii-agents-and-agentic-workflows.md), [Custom assistants](v-custom-assistants-and-knowledge.md).
