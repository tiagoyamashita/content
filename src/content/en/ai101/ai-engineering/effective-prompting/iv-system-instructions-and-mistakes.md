---
label: "IV"
subtitle: "System instructions & mistakes"
group: "AI Applied"
order: 4
---
System instructions & mistakes

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
| Trusting first answer on facts | Ask for sources; verify ([Trust & verify](../trust-privacy-and-verify/i-overview.md)) |
| Pasting secrets | Redact; use enterprise tier if required |

## 7. Rehearsal questions

- What four pieces belong in a “minimum good prompt”?
- When is chain-of-thought worth the extra tokens?
- Why save prompts that worked?

**Next:** [Loop prompting — Overview](../loop-prompting/i-overview.md).

**Related:** [Agents & agentic workflows](../agents-and-agentic-workflows/i-overview.md), [Custom assistants](../custom-assistants-and-knowledge/i-overview.md).