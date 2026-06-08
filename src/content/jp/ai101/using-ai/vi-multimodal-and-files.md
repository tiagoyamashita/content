---
label: "VI"
subtitle: "マルチモーダルとファイル"
group: "Using AI"
order: 6
---
Multimodal and files
Modern AI tools accept **images**, **PDFs**, **spreadsheets**, **audio**, and **screenshots** — not just typed prompts. Using files well beats retyping content.

## 1. Modalities at a glance

| Input | Common uses |
|-------|-------------|
| **Text / markdown** | Default; best for precision |
| **PDF** | Contracts, papers, specs — “summarise section 4” |
| **Image / screenshot** | UI bugs, whiteboards, charts — “what’s wrong here?” |
| **Spreadsheet / CSV** | “Trends in column B”, “formula for …” |
| **Audio / video** | Transcription, meeting notes (upload or live) |
| **Code files** | Paste or @-mention in IDE tools |

## 2. PDFs and long documents

| Technique | Example prompt |
|-----------|----------------|
| **Page scope** | “Only pages 12–15: list obligations.” |
| **Structure first** | “Outline headings, then deep-dive §3.” |
| **Compare** | “Diff v1 vs v2 PDF on pricing terms.” |
| **Extract** | “Table of all dates and amounts as CSV.” |

**Limits:** very long PDFs may truncate — split files or use project knowledge with indexed upload.

**Scanned PDFs:** OCR quality varies; if text is garbled, re-scan or paste critical sections.

## 3. Images and screenshots

| Use case | Prompt tip |
|----------|------------|
| **UI / bug report** | “List UI elements; suggest likely cause (hypothesis).” |
| **Chart** | “Describe trend; don’t invent numbers not visible.” |
| **Handwriting / whiteboard** | “Transcribe; mark illegible as [?].” |
| **Generate image** | Separate tools (DALL·E, Midjourney) — be specific on style, aspect ratio |

**Do not** send images you’re not allowed to share (patient IDs, unreleased designs on personal chat).

## 4. Spreadsheets and data

| Task | Approach |
|------|----------|
| **Explore** | Upload CSV; “summary stats and anomalies” |
| **Formula help** | Describe goal + sample rows |
| **Charts** | “Suggest chart type; describe axes” — rebuild in Excel/Sheets yourself |
| **Sensitive data** | Aggregate or redact PII first; use enterprise tier |

AI may **hallucinate rows** — spot-check against source for decisions.

## 5. Voice and meetings

| Workflow | Tools pattern |
|----------|---------------|
| Record → transcribe → summarise | Native or Otter/Fireflies |
| Action items | “Extract tasks with owners and dates; mark uncertain as TBD.” |
| Follow-up email | “Draft recap from transcript; don’t add commitments we didn’t make.” |

Review transcripts before sharing externally — names and confidential topics.

## 6. Code and repos (light user view)

Non-developers: paste snippets or logs. Developers: use [IDE orchestration](iv-tools-and-orchestration.md).

| Input | Prompt |
|-------|--------|
| Stack trace | “Explain in plain English; suggest next debug step.” |
| Config file | “What does this setting do; safe to change for X?” |

## 7. Rehearsal questions

- Why specify page numbers on a PDF question?
- One risk of uploading a customer CSV to a consumer chat app?
- When is image input better than describing the UI in words?

**Related:** [Custom assistants](v-custom-assistants-and-knowledge.md), [Trust & verify](vii-trust-privacy-and-verify.md).
