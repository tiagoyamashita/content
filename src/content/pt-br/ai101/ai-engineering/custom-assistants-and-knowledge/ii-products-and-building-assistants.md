---
label: "II"
subtitle: "Produtos e assistentes de construção"
group: "AI Applied"
order: 2
---
Produtos e assistentes de construção

## 1. Equivalentes de produtos

| Produto | Recurso | O que você configura |
|--------|---------|-------------------|
| **Bate-papoGPT** | GPTs personalizados, memória (opcional) | Instruções, arquivos, ações |
| **Cláudio** | Projetos | Conhecimento do projeto + instruções |
| **Gêmeos** | Gemas | Persona + arquivos opcionais |
| **Copiloto** | Copilot Studio / M365 Copilot | Dados do locatário, plug-ins |
| **CadernoLM** | Cadernos | Fontes → perguntas e respostas fundamentadas, visão geral do áudio |
| **Cursor** | Regras, índice de documentos | Repositório +`.cursor/rules`|

A mesma ideia em todos os lugares: **instruções + conhecimento + ferramentas (opcionais)**.

## 2. O que colocar em “conhecimento”

| Boas fontes | Fontes pobres |
|--------------|--------------|
| PDFs de políticas, manuais, perguntas frequentes | Exportações aleatórias desatualizadas |
| Especificações do produto, API documentos que você possui | Confidencial, você não tem permissão para fazer upload |
| Notas da reunião **você** curador | Todo o arquivo de e-mail não filtrado |
| Guia de estilo, voz da marca | Documentos do concorrente aos quais você não tem direitos |

**Atualização:** conhecimento obsoleto → respostas erradas confiantes. Data seus uploads; substitua trimestralmente.

## 3. Construindo um assistente personalizado útil

```text
1. One sentence purpose   ("Answers support tier-1 about Billing v2")
2. Audience               (customers vs internal)
3. Tone & format          (short, links, escalate when …)
4. Boundaries             (no legal advice; no discounts)
5. 3–5 example Q&As       (few-shot in instructions)
6. Knowledge files        (indexed docs)
7. Test with edge cases   (unknown product, angry user, non-English)
```

### Modelo de instrução

```text
Purpose: …
Always: cite doc section; say "I don't know" if not in knowledge.
Never: promise refunds; invent SKU prices.
Format: numbered steps for how-to; table for comparisons.
Escalate: billing disputes → human@company.com
```