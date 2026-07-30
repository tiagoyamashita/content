---
label: "VII"
subtitle: "Árvore de pesquisa binária"
group: "Estruturas de dados e algoritmos"
order: 7
---
Árvore de pesquisa binária (BST)
Árvore binária ordenada: todas as chaves da subárvore esquerda são estritamente menores que a chave do nó; todas as chaves na subárvore direita são estritamente maiores (para uma ordem total estrita).

**Ops:** pesquise, insira, exclua siga um caminho da raiz à folha - tempo **O(h)** onde **h** é a altura. Balanceado: **h = O(log n)**; cadeia distorcida de inserções classificadas: **h = Θ(n)**.

**Balanceamento (visão geral):** **AVL** as árvores impõem um equilíbrio rígido de altura com rotações; árvores **vermelho-pretas** usam regras de cores para manter **h = O(log n)** com equilíbrio um pouco mais frouxo e menos rotações em média. Ambos restauram **O(log n)** pesquisa/inserção/exclusão do pior caso.

**Relacionado:** **Nível II — Árvores, heaps, hashing** (`ii-trees-heaps-hashing.md`).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 218" role="img" aria-label="Binary search tree with smaller keys left larger keys right">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">BST ordering (example)</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">search compares target with node; go left if smaller, right if larger</text>
  <circle cx="200" cy="72" r="22" fill="rgba(34,197,94,0.15)" stroke="#86efac" stroke-width="2"/>
  <text x="192" y="78" fill="#e4e4e7" font-size="13" font-family="ui-monospace" font-weight="600">5</text>
  <line x1="184" y1="88" x2="120" y2="128" stroke="#71717a" stroke-width="2"/>
  <line x1="216" y1="88" x2="280" y2="128" stroke="#71717a" stroke-width="2"/>
  <circle cx="120" cy="144" r="20" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="112" y="150" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <circle cx="280" cy="144" r="20" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="272" y="150" fill="#e4e4e7" font-size="12" font-family="ui-monospace">8</text>
  <line x1="104" y1="158" x2="72" y2="178" stroke="#71717a" stroke-width="2"/>
  <circle cx="72" cy="188" r="16" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="66" y="192" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <text x="300" y="72" fill="#71717a" font-size="9">all left &lt; parent &lt; all right</text>
  <text x="12" y="212" fill="#71717a" font-size="9">insert/delete walk one root-to-leaf path — height h dominates cost</text>
</svg></figure>
